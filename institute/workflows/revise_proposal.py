"""Redraft a proposal that the reviewer placed on hold.

Per Chapter 6, a `hold` disposition is *not* a rejection. The
research question is worth pursuing, but the proposal as written
lacks something the reviewer named: a missing comparison, an
unclear methodology, a scope that needs sharpening. The lead Fellow
gets the reviewer's guidance and redrafts the proposal.

State flow:
  PROPOSAL_HELD --(revise_proposal)--> PROPOSED  (re-review)

The previous proposal text is preserved at
`archive/proposals/<id>/proposal.v<n>.md` so the iteration history
stays visible in the archive.
"""

from __future__ import annotations

import sqlite3

from rich.console import Console

from institute import claude_runner, db, decisions, paths, state, workspaces
from institute import fellow as fellow_mod
from institute.claude_runner import FellowTask
from institute.fellow import Genome
from institute.state import State

console = Console()


BRIEF = """\
You are the lead Fellow on a research proposal that the reviewer
placed on **hold**. The research question is worth pursuing; the
proposal as written needs specific changes before it can be
approved.

# Your task

Read your prior proposal and the reviewer's hold guidance (both in
your working directory). Produce a revised proposal that addresses
the named concerns. Then we re-review.

# Inputs (in your current working directory)

- `prior-proposal.md` — the proposal you wrote previously
- `hold-guidance.md`  — the reviewer's named concerns and required changes

# Constraints

- Keep the proposal's original spirit when the reviewer's concerns
  are local. A hold is not a request to abandon the question.
- Where the reviewer asks for something you cannot deliver, say so
  explicitly in the rationale and propose an alternative. Do not
  silently drop a requirement.
- If on reflection you think the proposal *should* be abandoned,
  reply with `Abandon.` as the entire response. The Founder will
  route the project through the abandonment workflow.

# Output

Write the revised proposal to `proposal.md` (single file in the
working directory). The file is the new canonical proposal — it
replaces the prior version. Use the same structure as the original
proposal (title, question, background, approach, expected output,
resource estimate, anticipated failure modes, collaborators).

When the file exists and is complete, reply with the single word
`Done.` and nothing else.
"""


def _load_lead_and_review(
    conn: sqlite3.Connection, project_id: str
) -> tuple[Genome, str]:
    proj = conn.execute(
        "SELECT lead_fellow_id, proposal_path FROM projects WHERE id = ?",
        (project_id,),
    ).fetchone()
    if proj is None:
        raise SystemExit(f"No such project: {project_id}")
    lead = fellow_mod.load_genome(conn, proj["lead_fellow_id"])
    # The most recent proposal review (by submitted_at desc) carries the
    # hold guidance the lead must address. We pull it from the audit_log
    # decision record path rather than the reviews table because proposal
    # reviews aren't stored in `reviews` (which is per-draft, not per-proposal).
    review_dir = paths.PROPOSALS / project_id
    review_files = sorted(
        review_dir.glob("review-by-*.md"),
        key=lambda p: p.stat().st_mtime,
        reverse=True,
    )
    if not review_files:
        raise SystemExit(
            f"No proposal review found under {review_dir}; cannot resolve hold."
        )
    review_md = review_files[0].read_text(encoding="utf-8")
    return lead, review_md


def run(project_id: str) -> None:
    """Have the lead Fellow redraft a held proposal."""
    with db.connection() as conn:
        proj = conn.execute(
            "SELECT id, title, state, proposal_path FROM projects WHERE id = ?",
            (project_id,),
        ).fetchone()
        if proj is None:
            raise SystemExit(f"No such project: {project_id}")
        if proj["state"] != State.PROPOSAL_HELD.value:
            raise SystemExit(
                f"Project {project_id} is in state {proj['state']}, "
                f"not {State.PROPOSAL_HELD.value}."
            )
        lead, review_md = _load_lead_and_review(conn, project_id)
        prior_proposal = (paths.ROOT / proj["proposal_path"]).read_text(encoding="utf-8")

    console.print(
        f"[dim]Asking {lead.name} ({lead.id}) to redraft the held proposal...[/dim]"
    )

    workspace = workspaces.workspace_for(lead.id, project_id)
    workspaces.stage_input(workspace, "prior-proposal.md", prior_proposal)
    workspaces.stage_input(workspace, "hold-guidance.md", review_md)

    result = claude_runner.invoke(
        FellowTask(
            genome=lead,
            project_id=project_id,
            step="revise_proposal",
            brief=BRIEF,
            workspace=workspace,
            extra_dirs=(paths.DOCS, paths.ARCHIVE),
        )
    )

    # An honest "Abandon." reply is treated by the Founder as a
    # signal to route the project through abandonment, not by this
    # workflow. We surface it back to the operator.
    reply = result.result_text.strip()
    if reply.lower().startswith("abandon"):
        console.print(
            f"[yellow]{lead.name} declined to redraft.[/yellow] "
            "Run `institute abandon` to record the honest lesson."
        )
        return

    from institute.safe_io import atomic_write

    new_proposal_md = workspaces.require_output(
        workspace, "proposal.md", min_chars=200
    )

    # Preserve the prior version, then overwrite the canonical proposal.
    proposal_path = paths.PROPOSALS / project_id / "proposal.md"
    if proposal_path.exists():
        version = 1
        while (paths.PROPOSALS / project_id / f"proposal.v{version}.md").exists():
            version += 1
        archived = paths.PROPOSALS / project_id / f"proposal.v{version}.md"
        atomic_write(archived, prior_proposal)
    atomic_write(proposal_path, new_proposal_md.rstrip() + "\n")

    decision = decisions.Decision(
        kind="proposal_revision",
        title=f"Held proposal redrafted: {proj['title']}",
        body=(
            f"**Lead Fellow:** {lead.name} (`{lead.id}`)\n\n"
            f"**Previous proposal:** archived alongside the canonical "
            f"proposal in `{(paths.PROPOSALS / project_id).relative_to(paths.ROOT)}`\n\n"
            f"The project returns to `{State.PROPOSED.value}` for re-review."
        ),
        actors=[lead.id],
        related_project=project_id,
    )
    with db.connection() as conn, db.transaction(conn):
        state.transition(conn, project_id, State.PROPOSED)
        decisions.record(conn, decision)

    console.print(
        f"[green]Redraft complete.[/green] Proposal returned to "
        f"[bold]{State.PROPOSED.value}[/bold] for re-review."
    )
