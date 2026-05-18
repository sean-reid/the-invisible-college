"""Research workflow: lead Fellow executes the proposed research.

The lead Fellow reads the approved proposal and any review notes, does
the work, writes a lab notebook entry that describes what they did, and
produces a draft suitable for peer review. In v1 this is a single
invocation; in later iterations research may span multiple invocations
with the lab notebook accumulating across calls.

The Fellow's reply must be a JSON object with two keys: `notebook` (the
public log of the research process) and `draft` (the publishable piece).
This keeps the two artifacts cleanly separated.
"""

from __future__ import annotations

import re
import sqlite3
from datetime import UTC, datetime
from pathlib import Path

from rich.console import Console

from institute import claude_runner, db, decisions, parsing, paths
from institute import fellow as fellow_mod
from institute.claude_runner import FellowTask
from institute.fellow import Genome
from institute.state import State

console = Console()


BRIEF = """\
You are executing approved research for the Invisible College. You are
the lead Fellow on this project. The proposal you wrote (or accepted) and
the reviewer's response appear below.

# Your task

Produce three artifacts as a single JSON object:

1. `abstract`: a short summary of the piece. Two to three sentences,
   never more than four. 40 to 90 words. Self-contained: a reader who
   reads only the abstract should know what the piece argues or
   demonstrates. Plain prose, no markdown formatting, no backticks, no
   asterisks, no headings. Do not begin with phrases like "This piece
   argues" or "In this essay" — just state the substance. This abstract
   appears verbatim under the byline in the published post.

2. `notebook`: a public lab notebook entry that records what you actually
   did during this research session. Include: the questions you held in
   mind, the steps you took, what surprised you, what you tried that did
   not work, and what you concluded. Honest about negative results. Dated
   in the prose. Markdown. 400-1500 words.

3. `draft`: the publishable piece. Markdown. 800-3500 words. Structured
   appropriately for its form (essay, demonstration, critical review,
   etc.). Must include:
   - A clear title (as a level-1 heading `#`)
   - A lede paragraph that opens the body. Do NOT repeat the abstract
     verbatim; the abstract is for the header block, the lede is for
     pulling the reader into the body proper.
   - The body of the work
   - A conclusion or summary
   - **A References section if you cited external work.** Use a level-2
     heading `## References`. Each reference is a SEPARATE list item
     beginning with `- `. Do not run references together in a single
     prose paragraph and do not wrap the whole list in italics. Example:

     ```
     ## References

     - Kahan, W. (1965). "Further Remarks on Reducing Truncation Errors."
       CACM 8(1):40.
     - Goldberg, D. (1991). "What Every Computer Scientist Should Know
       About Floating-Point Arithmetic." ACM Computing Surveys 23(1):5-48.
       https://dl.acm.org/doi/10.1145/103162.103163
     ```

     Inline citations in the body (when you reference a specific work)
     can be the author-year style "(Kahan, 1965)" or a footnote-style
     superscript that maps to the References list.

The draft is what other Fellows will peer review. It should stand on its
own without the notebook.

# Constraints

- Read the Charter before you write. Adhere strictly to its prohibitions.
- No deception, no plagiarism, no engagement-bait, no consciousness claims.
- If during the research you find that the original question was malformed
  or unanswerable, write about that honestly in the notebook and produce
  a draft that reports the honest negative result.
- You may use Read, WebSearch, WebFetch, Bash, Write within your workspace
  if your tools allow.

# Output

Reply with a single JSON object only:

```json
{{
  "abstract": "<40-90 word plain-prose summary>",
  "notebook": "<markdown-string>",
  "draft": "<markdown-string>"
}}
```

No prose outside the JSON. No code-fence wrapping the JSON.

# The proposal

{proposal_md}

# Reviewer feedback on the proposal

{review_md}
"""


def _load_review_md(conn: sqlite3.Connection, project_id: str) -> str:
    """Best-effort: read whatever review document was produced for the proposal."""
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
    if match:
        return match.group(1).strip()
    return None


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
        if proj["state"] not in (
            State.PROPOSAL_REVIEWED.value,
            State.RESEARCHING.value,
        ):
            raise SystemExit(
                f"Project {project_id} is in state {proj['state']}, "
                "expected proposal_reviewed or researching."
            )
        lead: Genome = fellow_mod.load_genome(conn, proj["lead_fellow_id"])
        proposal_md = (paths.ROOT / proj["proposal_path"]).read_text(encoding="utf-8")
        review_md = _load_review_md(conn, project_id)

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

    brief = BRIEF.format(proposal_md=proposal_md, review_md=review_md)
    result = claude_runner.invoke(
        FellowTask(
            genome=lead,
            project_id=project_id,
            step="research",
            brief=brief,
            extra_dirs=(paths.DOCS, paths.ARCHIVE),
        )
    )
    dump_path = paths.LAB_NOTEBOOKS / project_id / "raw-research-output.txt"
    payload = parsing.parse_json_or_dump(
        result.result_text,
        dump_path=dump_path,
        context=f"Research output from {lead.name} for project {project_id}",
    )
    if "notebook" not in payload or "draft" not in payload:
        dump_path.parent.mkdir(parents=True, exist_ok=True)
        dump_path.write_text(result.result_text, encoding="utf-8")
        raise RuntimeError(
            "Research output JSON must have `notebook` and `draft` keys. "
            f"Got keys: {list(payload)}. Raw saved to {dump_path}."
        )
    abstract = (payload.get("abstract") or "").strip() or None

    notebook_md = payload["notebook"].strip()
    draft_md = payload["draft"].strip()
    if not notebook_md or not draft_md:
        raise RuntimeError("Research notebook or draft is empty.")

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

    console.print()
    console.print(f"[green]Notebook:[/green]  {notebook_path.relative_to(paths.ROOT)}")
    console.print(f"[green]Draft:[/green]     {draft_path.relative_to(paths.ROOT)}")
    console.print(f"[green]New state:[/green] {State.DRAFTED.value}")
