"""Review a research proposal.

One Fellow other than the lead reads the proposal and renders a decision:
approve, approve-with-revisions, or reject. A short written rationale is
required for any non-approve decision.

In v1 we collapse "approve-with-revisions" to "approve" with the
revisions captured in the decision body. The lead Fellow reads the
revisions during research.
"""

from __future__ import annotations

import re
import sqlite3

from rich.console import Console

from institute import claude_runner, db, decisions, paths, state
from institute import fellow as fellow_mod
from institute.claude_runner import FellowTask
from institute.fellow import Genome
from institute.state import State

console = Console()


BRIEF = """\
You are reviewing a research proposal for the Invisible College. The
proposal text appears below. Your job is to render a fast, honest verdict.

# Evaluation criteria

1. **Novelty.** Does this question add to what the Archive already contains?
   Is the answer obvious in advance?
2. **Feasibility.** Can the proposed approach actually produce the expected
   output? Are the resource estimates plausible?
3. **Fit.** Is this work appropriate for the College, given the Charter?
4. **Topic diversity.** Read the Archive index. If this proposal extends
   a thread the College has already published heavily on (three or more
   pieces, or two by the same lead Fellow), it adds to a saturation
   problem the Charter calls out in Chapter 11. Recommend
   `approve-with-revisions` and ask the lead to either (a) name what
   their proposal contributes beyond the prior pieces in concrete
   terms, or (b) pivot to a different question. Do NOT approve another
   piece in a saturated cluster on the strength of competence alone —
   competence in a single track is what convergence looks like.

# Required output

Reply with markdown, structured as the following sections, in this exact
order, each as a level-2 heading:

1. `## Recommendation` — one of: `approve`, `approve-with-revisions`, `reject`
2. `## Confidence` — one of: `confident`, `moderate`, `low`
3. `## Rationale` — 2-6 paragraphs. Be specific. If you are recommending
   anything other than approve, you must say exactly what is wrong and what
   the lead Fellow should change. If you approve, you may still note
   concerns or suggestions.
4. `## Revisions requested` — present only when recommendation is
   `approve-with-revisions`. A numbered list of specific changes.

# Constraints

- Sycophantic approvals damage the institution. If the proposal is
  uninteresting, say so.
- A reject is rare. Most flawed proposals can be salvaged with revisions.
- Stay terse. The Fellow proposing this work needs your verdict more than
  your rhetoric.

# The proposal

{proposal_md}
"""


def _pick_reviewer(conn: sqlite3.Connection, project_id: str) -> Genome:
    """Pick any active Fellow other than the lead."""
    row = conn.execute("SELECT lead_fellow_id FROM projects WHERE id = ?", (project_id,)).fetchone()
    if row is None:
        raise SystemExit(f"No such project: {project_id}")
    lead = row["lead_fellow_id"]

    # Prefer Fellows whose specialization includes "critic" or "review";
    # otherwise pick any active Fellow other than the lead.
    rows = list(
        conn.execute(
            "SELECT id, specialization FROM fellows "
            "WHERE retired_at IS NULL AND id != ? "
            "ORDER BY rank DESC, name",
            (lead,),
        )
    )
    if not rows:
        raise SystemExit("No Fellow available to review (only the lead exists).")

    critics = [
        r
        for r in rows
        if "critic" in r["specialization"].lower() or "review" in r["specialization"].lower()
    ]
    chosen = critics[0] if critics else rows[0]
    return fellow_mod.load_genome(conn, chosen["id"])


def _parse_recommendation(markdown: str) -> str:
    match = re.search(
        r"^##\s+Recommendation\s*$\n+(.*?)(?=^##\s+|\Z)",
        markdown,
        re.MULTILINE | re.DOTALL,
    )
    if not match:
        raise RuntimeError("Reviewer output is missing a `## Recommendation` section.")
    body = match.group(1).strip().lower()
    # Take the first non-empty line and normalize.
    first = next((ln.strip() for ln in body.splitlines() if ln.strip()), "")
    first = first.strip("`*_ ")
    if first in {"approve", "approve-with-revisions", "reject"}:
        return first
    raise RuntimeError(f"Unrecognized recommendation: {first!r}")


def run(project_id: str) -> None:
    """Top-level review-proposal entry point.

    Called by `institute next` when a project is in state PROPOSED.
    """
    with db.connection() as conn:
        proj = conn.execute(
            "SELECT id, title, state, proposal_path, lead_fellow_id FROM projects WHERE id = ?",
            (project_id,),
        ).fetchone()
        if proj is None:
            raise SystemExit(f"No such project: {project_id}")
        if proj["state"] != State.PROPOSED.value:
            raise SystemExit(f"Project {project_id} is in state {proj['state']}, not proposed.")
        proposal_md = (paths.ROOT / proj["proposal_path"]).read_text(encoding="utf-8")
        reviewer = _pick_reviewer(conn, project_id)

    console.print(f"[dim]Asking {reviewer.name} ({reviewer.id}) to review the proposal...[/dim]")

    brief = BRIEF.format(proposal_md=proposal_md)
    result = claude_runner.invoke(
        FellowTask(
            genome=reviewer,
            project_id=project_id,
            step="review_proposal",
            brief=brief,
            extra_dirs=(paths.DOCS, paths.ARCHIVE),
        )
    )
    review_md = result.result_text.strip()
    if review_md.startswith("```"):
        first_newline = review_md.find("\n")
        review_md = review_md[first_newline + 1 :]
        if review_md.rstrip().endswith("```"):
            review_md = review_md.rstrip()[:-3].rstrip()

    recommendation = _parse_recommendation(review_md)

    # Write the proposal review under the project's proposal directory.
    review_path = paths.PROPOSALS / project_id / f"review-by-{reviewer.id}.md"
    review_path.parent.mkdir(parents=True, exist_ok=True)
    tmp = review_path.with_suffix(".md.tmp")
    tmp.write_text(review_md.rstrip() + "\n", encoding="utf-8")
    tmp.replace(review_path)

    target_state = State.PROPOSAL_REVIEWED if recommendation != "reject" else State.REJECTED

    decision = decisions.Decision(
        kind="proposal_review",
        title=f"Proposal review for {proj['title']}",
        body=(
            f"**Reviewer:** {reviewer.name} (`{reviewer.id}`, {reviewer.specialization})\n\n"
            f"**Recommendation:** `{recommendation}`\n\n"
            f"**Review document:** [{review_path.relative_to(paths.ROOT)}]"
            f"({review_path.relative_to(paths.ROOT)})\n\n"
            f"The project transitions to `{target_state.value}`."
        ),
        actors=[reviewer.id],
        related_project=project_id,
    )

    with db.connection() as conn, db.transaction(conn):
        state.transition(conn, project_id, target_state)
        decisions.record(conn, decision)

    console.print()
    console.print(
        f"[green]Review complete.[/green]   Recommendation: [bold]{recommendation}[/bold]"
    )
    console.print(f"[green]Review file:[/green]      {review_path.relative_to(paths.ROOT)}")
    console.print(f"[green]New state:[/green]        {target_state.value}")
