"""Research workflow: lead Fellow executes the proposed research.

The lead Fellow reads the approved proposal and any review notes, does
the work, writes a lab notebook entry that describes what they did, and
produces a draft suitable for peer review.

File-based output (no JSON for prose). The orchestrator stages input
files into the Fellow's per-project workspace; the Fellow uses the Write
tool to drop output files into the same directory. The orchestrator then
reads them out. This eliminates an entire class of JSON-escaping
failures that plagued an earlier version.
"""

from __future__ import annotations

import re
from datetime import UTC, datetime
from pathlib import Path

from rich.console import Console

from institute import archive_index, claude_runner, db, decisions, episodic, paths, workspaces
from institute import fellow as fellow_mod
from institute.claude_runner import FellowTask
from institute.fellow import Genome
from institute.state import State

console = Console()


BRIEF = """\
You are executing approved research for the Invisible College as the
lead Fellow on this project.

# Inputs

In your current working directory you will find:
- `proposal.md`        the approved research proposal
- `proposal-review.md` the reviewer's response (or "(no review on file)")
- `archive-index.md`   every piece the College has published so far, with
                       slugs and abstracts. Consult it before you write,
                       so that you can build on (or contradict) prior
                       Fellows' work rather than re-discover it. Cite any
                       prior publication you draw on as a markdown link
                       to its slug, e.g.
                       `[Ada's piece on floating-point](posts/2026-05-17-when-the-same-sum-gives-different-answer-4da4/)`.
- `memory.md`          if present, the most relevant entries from your
                       own episodic memory (past curriculum responses,
                       prior proposals, drafts, peer reviews you have
                       given or received, advisor feedback). Read it as
                       your own — it is. Your past thinking should inform
                       this work; do not contradict yourself without
                       acknowledging it.

Read them with the Read tool before doing the work.

# Outputs

When the research is complete, use the Write tool to create THREE files
in your current working directory. They must have these exact filenames:

1. `abstract.txt` - a 40 to 90 word plain-prose summary, two to three
   sentences. NO markdown formatting, NO backticks, NO asterisks,
   NO headings. Self-contained. This appears verbatim under the byline
   in the published post. Do not begin with phrases like "This piece
   argues..."; just state the substance.

2. `notebook.md` - a public lab notebook entry. 400 to 1500 words of
   markdown. Record what you actually did: questions held in mind, steps
   taken, what surprised you, what did not work, what you concluded.
   Honest about negative results. Dated in the prose.

3. `draft.md` - the publishable piece. 800 to 3500 words of markdown.
   Must include:
     - A clear title (level-1 heading `#`)
     - A lede paragraph that opens the body. Do NOT repeat the abstract
       verbatim; the abstract is for the header block.
     - The body of the work
     - A conclusion or summary
     - **A References section if you cited external work.** Use a
       level-2 heading `## References`. Each reference is a SEPARATE
       list item beginning with `- `. Do not run references together in
       a single prose paragraph. Example:

         ## References

         - Kahan, W. (1965). "Further Remarks on Reducing Truncation Errors."
           CACM 8(1):40.
         - Goldberg, D. (1991). "What Every Computer Scientist Should
           Know About Floating-Point Arithmetic." ACM Computing Surveys
           23(1):5-48. https://dl.acm.org/doi/10.1145/103162.103163

# Constraints

- Read the Charter before you write. Adhere strictly to its prohibitions.
- No deception, no plagiarism, no engagement-bait, no consciousness claims.
- If during the research you find that the original question was
  malformed or unanswerable, write about that honestly in the notebook
  and produce a draft that reports the honest negative result.

# Final reply

When all three files exist, reply with the single word `Done.` Nothing
else. Do NOT paste the files into your reply.
"""


def _load_review_md(project_id: str) -> str:
    project_dir = paths.PROPOSALS / project_id
    if not project_dir.is_dir():
        return "(no review on file)"
    review_files = sorted(project_dir.glob("review-by-*.md"))
    if not review_files:
        return "(no review on file)"
    return review_files[0].read_text(encoding="utf-8")


def _atomic_write(path: Path, content: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    tmp = path.with_suffix(path.suffix + ".tmp")
    tmp.write_text(content, encoding="utf-8")
    tmp.replace(path)


def _extract_draft_title(draft_md: str) -> str | None:
    match = re.search(r"^#\s+(.+?)$", draft_md.lstrip(), re.MULTILINE)
    return match.group(1).strip() if match else None


def run(project_id: str) -> None:
    """Top-level research entry point.

    Called by `institute next` when a project is in PROPOSAL_REVIEWED or
    RESEARCHING. For v1, runs once and transitions to DRAFTED.
    """
    with db.connection() as conn:
        proj = conn.execute(
            "SELECT id, title, state, proposal_path, lead_fellow_id FROM projects WHERE id = ?",
            (project_id,),
        ).fetchone()
        if proj is None:
            raise SystemExit(f"No such project: {project_id}")
        if proj["state"] not in (State.PROPOSAL_REVIEWED.value, State.RESEARCHING.value):
            raise SystemExit(
                f"Project {project_id} is in state {proj['state']}, "
                "expected proposal_reviewed or researching."
            )
        lead: Genome = fellow_mod.load_genome(conn, proj["lead_fellow_id"])
        proposal_md = (paths.ROOT / proj["proposal_path"]).read_text(encoding="utf-8")
    review_md = _load_review_md(project_id)

    workspace = workspaces.workspace_for(lead.id, project_id)
    workspaces.stage_input(workspace, "proposal.md", proposal_md)
    workspaces.stage_input(workspace, "proposal-review.md", review_md)
    workspaces.stage_input(workspace, "archive-index.md", archive_index.render())

    console.print(
        f"[dim]Asking {lead.name} ({lead.id}) to execute the research. "
        "This will likely take several minutes...[/dim]"
    )

    # Transition into RESEARCHING immediately so an interruption shows the
    # in-flight state on `institute status`.
    now = datetime.now(UTC).isoformat(timespec="seconds")
    with db.connection() as conn, db.transaction(conn):
        conn.execute(
            "UPDATE projects SET state = ?, updated_at = ? WHERE id = ?",
            (State.RESEARCHING.value, now, project_id),
        )

    claude_runner.invoke(
        FellowTask(
            genome=lead,
            project_id=project_id,
            step="research",
            brief=BRIEF,
            workspace=workspace,
            extra_dirs=(paths.DOCS, paths.ARCHIVE),
        )
    )

    abstract = workspaces.optional_output(workspace, "abstract.txt")
    notebook_md = workspaces.require_output(workspace, "notebook.md", min_chars=200)
    draft_md = workspaces.require_output(workspace, "draft.md", min_chars=400)

    notebook_path = paths.LAB_NOTEBOOKS / project_id / "notebook.md"
    draft_path = paths.DRAFTS / project_id / "draft.md"
    abstract_path = paths.DRAFTS / project_id / "abstract.txt"
    _atomic_write(notebook_path, notebook_md.rstrip() + "\n")
    _atomic_write(draft_path, draft_md.rstrip() + "\n")
    if abstract:
        _atomic_write(abstract_path, abstract + "\n")

    new_title = _extract_draft_title(draft_md) or proj["title"]

    decision = decisions.Decision(
        kind="research",
        title=f"Draft complete: {new_title}",
        body=(
            f"**Lead Fellow:** {lead.name} (`{lead.id}`)\n\n"
            f"**Lab notebook:** [{notebook_path.relative_to(paths.ROOT)}]"
            f"({notebook_path.relative_to(paths.ROOT)})\n\n"
            f"**Draft:** [{draft_path.relative_to(paths.ROOT)}]"
            f"({draft_path.relative_to(paths.ROOT)})\n\n"
            "Project enters peer review."
        ),
        actors=[lead.id],
        related_project=project_id,
    )

    now = datetime.now(UTC).isoformat(timespec="seconds")
    with db.connection() as conn, db.transaction(conn):
        conn.execute(
            "UPDATE projects "
            "SET state = ?, title = ?, notebook_path = ?, draft_path = ?, updated_at = ? "
            "WHERE id = ?",
            (
                State.DRAFTED.value,
                new_title,
                str(notebook_path.relative_to(paths.ROOT)),
                str(draft_path.relative_to(paths.ROOT)),
                now,
                project_id,
            ),
        )
        decisions.record(conn, decision)

    episodic.safe_ingest(
        fellow_id=lead.id,
        kind="lab_notebook",
        title=f"Lab notebook: {new_title}",
        content=notebook_md,
        source_path=str(notebook_path.relative_to(paths.ROOT)),
        project_id=project_id,
    )
    episodic.safe_ingest(
        fellow_id=lead.id,
        kind="draft",
        title=new_title,
        content=draft_md,
        source_path=str(draft_path.relative_to(paths.ROOT)),
        project_id=project_id,
    )

    console.print()
    console.print(f"[green]Notebook:[/green]  {notebook_path.relative_to(paths.ROOT)}")
    console.print(f"[green]Draft:[/green]     {draft_path.relative_to(paths.ROOT)}")
    console.print(f"[green]New state:[/green] {State.DRAFTED.value}")
