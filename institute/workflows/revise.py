"""Revise workflow: lead Fellow incorporates peer review feedback.

When peer review is filed with any non-accept recommendation, the project
enters REVISING. The lead Fellow re-enters their workspace with: the
current draft, the lab notebook, and every signed review verbatim. The
Fellow produces a revised draft, a response-to-reviewers document, an
updated abstract, and a lab-notebook addendum recording what changed.

File-based output. No JSON for prose. The orchestrator stages every
input file the Fellow needs in the workspace and reads typed output
files back out.

The prior draft is preserved as draft.v1.md (or .v2, .v3, ...) for
provenance. The lab notebook is appended-to, never overwritten.

Two passes are supported:
  - current_round == 1 -> revise pass 1, then peer_review round 2
  - current_round == 2 -> final polish, then editorial (hard cap)
"""

from __future__ import annotations

import re
import sqlite3
from pathlib import Path

from rich.console import Console

from institute import (
    archive_index,
    claude_runner,
    db,
    decisions,
    episodic,
    paths,
    state,
    workspaces,
)
from institute import fellow as fellow_mod
from institute.claude_runner import FellowTask
from institute.state import State

console = Console()


BRIEF = """\
You are revising your own research piece for the Invisible College after
{round_label} peer review. You are the lead author.

{round_context}

# Inputs

In your current working directory:
- `current-draft.md`     the draft you are revising
- `current-notebook.md`  your lab notebook so far
- `reviews.md`           every signed peer review from this round,
                         concatenated, with the reviewer's name and
                         recommendation in each section header
- `archive-index.md`     every piece the College has published so far.
                         If a reviewer suggested engaging with prior
                         work, this is where to find it.
- `memory.md`            if present, the most relevant entries from your
                         episodic memory beyond this project

Read all of them with the Read tool before doing the work.

# Your task

Read every review carefully. For each concern raised, decide one of:

1. **Address it**: change the draft to fix the problem.
2. **Decline it with reasoning**: keep the draft as-is and explain why in
   the response document.

Sycophantic capitulation is not the goal. If a reviewer is wrong, say so
in the response and defend the original choice. If a reviewer is right,
fix the draft and acknowledge the correction.

# Outputs

Use the Write tool to create FOUR files in your current working directory:

1. `abstract.txt` - updated 40-90 word plain-prose abstract. May be
   identical to the previous one if the piece's substance did not change.

2. `draft.md` - the full revised draft. This replaces the previous draft
   as the publishable artifact. Markdown. Include References as a list
   under a `## References` heading if you cite external work.

3. `response.md` - response to reviewers. Markdown. Address each named
   reviewer's concerns explicitly. Use level-3 headings:
       ### Response to <reviewer name>

4. `notebook-addendum.md` - a new dated lab-notebook entry recording the
   revision pass. This will be APPENDED to the existing notebook, not
   replacing it. Be specific about what changed and why.

# Final reply

When all four files exist, reply with the single word `Done.` Nothing else.
"""


def _format_reviews_for_brief(conn: sqlite3.Connection, project_id: str, review_round: int) -> str:
    """Concatenate filed reviews for the given round with reviewer attribution."""
    rows = list(
        conn.execute(
            "SELECT reviewer_id, role, recommendation, confidence, content_path "
            "FROM reviews WHERE project_id = ? AND round = ? ORDER BY role",
            (project_id, review_round),
        )
    )
    if not rows:
        return "(no reviews on file)"

    blocks = []
    for row in rows:
        genome = fellow_mod.load_genome(conn, row["reviewer_id"])
        body = (paths.ROOT / row["content_path"]).read_text(encoding="utf-8")
        blocks.append(
            "\n".join(
                [
                    f"## Review by {genome.name}",
                    f"- Role: {row['role']}",
                    f"- Recommendation: {row['recommendation']}",
                    f"- Confidence: {row['confidence']}",
                    "",
                    body.strip(),
                    "",
                ]
            )
        )
    return "\n\n".join(blocks)


def _atomic_write(path: Path, content: str) -> None:
    from institute.safe_io import atomic_write

    atomic_write(path, content)


def _next_draft_version(draft_dir: Path) -> int:
    versions = [
        int(m.group(1))
        for p in draft_dir.glob("draft.v*.md")
        if (m := re.match(r"draft\.v(\d+)\.md$", p.name))
    ]
    return max(versions, default=0) + 1


def _extract_draft_title(draft_md: str) -> str | None:
    match = re.search(r"^#\s+(.+?)$", draft_md.lstrip(), re.MULTILINE)
    return match.group(1).strip() if match else None


def run(project_id: str) -> None:
    """Top-level revise entry point. Called when state is REVISING."""
    with db.connection() as conn:
        proj = conn.execute(
            "SELECT id, title, state, kind, draft_path, notebook_path, lead_fellow_id, "
            "review_round FROM projects WHERE id = ?",
            (project_id,),
        ).fetchone()
        if proj is None:
            raise SystemExit(f"No such project: {project_id}")
        if proj["state"] != State.REVISING.value:
            raise SystemExit(
                f"Project {project_id} is in state {proj['state']}, expected revising."
            )
        current_round = int(proj["review_round"])
        kind = proj["kind"] or "research"
        lead = fellow_mod.load_genome(conn, proj["lead_fellow_id"])
        draft_md = (paths.ROOT / proj["draft_path"]).read_text(encoding="utf-8")
        notebook_md = (paths.ROOT / proj["notebook_path"]).read_text(encoding="utf-8")
        reviews_md = _format_reviews_for_brief(conn, project_id, current_round)

    if current_round == 1:
        round_label = "round-1"
        round_context = (
            "After this revision the same reviewers will see the revised draft "
            "and file a second round of reviews. So this is a substantive "
            "rewrite responding to specific concerns, not the final polish."
        )
    else:
        round_label = "round-2"
        round_context = (
            "This is the FINAL polishing pass. After this revision the project "
            "goes directly to editorial; there is no third round. Address any "
            "remaining concerns as best you can, or defend the prior version "
            "explicitly in the response document. The previous draft already "
            "incorporated round-1 feedback; do not undo those changes."
        )

    workspace = workspaces.workspace_for(lead.id, f"{project_id}-revise-r{current_round}")
    workspaces.stage_input(workspace, "current-draft.md", draft_md)
    workspaces.stage_input(workspace, "current-notebook.md", notebook_md)
    workspaces.stage_input(workspace, "reviews.md", reviews_md)
    workspaces.stage_input(workspace, "archive-index.md", archive_index.render())

    console.print(
        f"[dim]Asking {lead.name} ({lead.id}) to revise their draft in light of "
        f"the {round_label} peer reviews. This will likely take several minutes...[/dim]"
    )

    brief = BRIEF.format(round_label=round_label, round_context=round_context)
    claude_runner.invoke(
        FellowTask(
            genome=lead,
            project_id=project_id,
            step=f"revise:r{current_round}",
            brief=brief,
            workspace=workspace,
            extra_dirs=(paths.DOCS, paths.ARCHIVE),
        )
    )

    new_abstract = workspaces.optional_output(workspace, "abstract.txt")
    new_draft_md = workspaces.require_output(workspace, "draft.md", min_chars=400)
    response_md = workspaces.require_output(workspace, "response.md", min_chars=100)
    addendum = workspaces.optional_output(workspace, "notebook-addendum.md")

    # Preserve the prior draft as draft.vN.md before overwriting.
    draft_dir = paths.DRAFTS / project_id
    draft_dir.mkdir(parents=True, exist_ok=True)
    version = _next_draft_version(draft_dir)
    prior_draft_path = draft_dir / f"draft.v{version}.md"
    _atomic_write(prior_draft_path, draft_md.rstrip() + "\n")
    _atomic_write(draft_dir / "draft.md", new_draft_md + "\n")

    if new_abstract:
        _atomic_write(draft_dir / "abstract.txt", new_abstract + "\n")

    response_path = draft_dir / f"response-to-reviewers.v{version}.md"
    _atomic_write(response_path, response_md.rstrip() + "\n")

    # Append to the lab notebook rather than overwriting.
    if addendum:
        notebook_path = paths.ROOT / proj["notebook_path"]
        existing = notebook_path.read_text(encoding="utf-8").rstrip()
        combined = existing + "\n\n---\n\n" + addendum.rstrip() + "\n"
        _atomic_write(notebook_path, combined)

    new_title = _extract_draft_title(new_draft_md) or proj["title"]

    if kind == "qualifying":
        # Chapter 5: qualifying projects are advisor-supervised. After
        # the Postulant addresses the advisor's revision request, the
        # piece routes back to AWAITING_ADVISOR_REVIEW (not into peer
        # review or editorial), so the same advisor confirms the fix
        # before the project enters the normal peer-review pipeline.
        target_state = State.AWAITING_ADVISOR_REVIEW
        next_round = current_round
        next_description = (
            "Qualifying project: revised draft returns to the advisor for a "
            "second look. The advisor either approves (advancing to peer "
            "review) or requests further revision."
        )
    elif current_round == 1:
        target_state = State.PEER_REVIEWING
        next_round = 2
        next_description = (
            f"Project transitions to `peer_reviewing` for round {next_round}. "
            "The same reviewers will see the revised draft and the response."
        )
    else:
        target_state = State.EDITORIAL
        next_round = current_round
        next_description = (
            "Final polishing pass after round-2 feedback. Project transitions "
            "directly to `editorial` for publication. No further review rounds."
        )

    decision = decisions.Decision(
        kind="revision",
        title=f"Revision pass (round {current_round} feedback): {new_title}",
        body=(
            f"**Lead Fellow:** {lead.name} (`{lead.id}`)\n\n"
            f"**Addressing:** round-{current_round} reviews\n\n"
            f"**Prior draft preserved:** [{prior_draft_path.relative_to(paths.ROOT)}]"
            f"({prior_draft_path.relative_to(paths.ROOT)})\n\n"
            f"**Revised draft:** [archive/drafts/{project_id}/draft.md]"
            f"(archive/drafts/{project_id}/draft.md)\n\n"
            f"**Response to reviewers:** [{response_path.relative_to(paths.ROOT)}]"
            f"({response_path.relative_to(paths.ROOT)})\n\n"
            f"{next_description}"
        ),
        actors=[lead.id],
        related_project=project_id,
    )

    with db.connection() as conn, db.transaction(conn):
        state.transition(conn, project_id, target_state)
        conn.execute(
            "UPDATE projects SET title = ?, review_round = ? WHERE id = ?",
            (new_title, next_round, project_id),
        )
        decisions.record(conn, decision)

    episodic.safe_ingest(
        fellow_id=lead.id,
        kind="revision",
        title=f"Revision (v{next_round}): {new_title}",
        content=new_draft_md,
        source_path=str((draft_dir / "draft.md").relative_to(paths.ROOT)),
        project_id=project_id,
        metadata={"round": next_round, "response_path": str(response_path.relative_to(paths.ROOT))},
    )

    console.print()
    console.print(
        f"[green]Revision filed.[/green]   Prior draft: {prior_draft_path.relative_to(paths.ROOT)}"
    )
    console.print(f"[green]Response:[/green]         {response_path.relative_to(paths.ROOT)}")
    round_label_print = f" (round {next_round})" if target_state == State.PEER_REVIEWING else ""
    console.print(f"[green]New state:[/green]       {target_state.value}{round_label_print}")
