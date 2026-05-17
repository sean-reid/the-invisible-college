"""Peer review workflow.

Three Fellows (or as many as are available, minimum two) read the draft
and produce structured signed reviews. Each invocation produces one
review. When all expected reviews are in, the project transitions to
EDITORIAL (skipping REVISING in v1 for simplicity).

Roles:
- primary: deepest engagement with the work, ideally from a similar
  specialization to the lead
- secondary: another knowledgeable Fellow
- outside: a Fellow from outside the lead's specialization (fresh angle)

The reviewer set is computed once and cached on first invocation, then
each subsequent `institute next` call works through them in order.
"""

from __future__ import annotations

import secrets
import sqlite3
from dataclasses import dataclass
from datetime import UTC, datetime
from pathlib import Path
from typing import Literal

from rich.console import Console

from institute import claude_runner, db, decisions, parsing, paths
from institute import fellow as fellow_mod
from institute.claude_runner import FellowTask
from institute.fellow import Genome
from institute.state import State

console = Console()


Role = Literal["primary", "secondary", "outside"]


@dataclass(frozen=True)
class ReviewSlot:
    reviewer_id: str
    role: Role


BRIEF_ROUND_1 = """\
You are a peer reviewer for the Invisible College. You have been assigned
as the {role} reviewer of the draft below. You are {reviewer_name}, rank
{reviewer_rank}, specializing in {reviewer_specialization}.

# Your task

Read the draft carefully. Then write a structured review.

# CRITICAL OUTPUT RULES

Your entire final reply MUST be a single JSON object. No prose preface,
no summary, no code fence. The first character is `{{` and the last is
`}}`.

# Required output

```json
{{
  "summary": "<2-4 sentences stating, in your own words, what the work claims and demonstrates>",
  "strengths": "<markdown; specific, not generic>",
  "concerns": "<markdown; specific concerns the author can act on; each as a numbered item>",
  "recommendation": "<one of: accept, minor, major, reject>",
  "confidence": "<one of: confident, moderate, low>",
  "dissent_intent": "<true if you intend this review to be published as a dissent regardless of editorial outcome, false otherwise>"
}}
```

# Constraints

- Substantive engagement only. A surface-level review is failing your duty.
- If the work is good, say so specifically. If it is bad, say so specifically.
- A reviewer who agrees with everything signals nothing. Productive
  disagreement is the institutional norm.
- Reviewer reputation is tracked. Lazy reviews damage it.
- 500-1200 words total across the four fields is typical.

# Draft

{draft_md}
"""


BRIEF_ROUND_2 = """\
You are filing a SECOND-round peer review for the Invisible College. You
previously reviewed an earlier version of this piece. The lead Fellow has
revised the draft based on your concerns and the other reviewers'. You
are now reviewing the REVISED draft.

You are {reviewer_name}, rank {reviewer_rank}, specializing in
{reviewer_specialization}, serving as the {role} reviewer for both rounds.

# CRITICAL OUTPUT RULES

Your entire final reply MUST be a single JSON object. No prose preface,
no summary, no code fence. The first character is `{{` and the last is
`}}`.

# Your task

Judge whether your earlier concerns were addressed, or appropriately
rejected with sound reasoning. Then form a fresh recommendation on the
revised draft.

You may:
- Be satisfied that your concerns were addressed → recommend `accept`
- Be partially satisfied → recommend `minor` or `major` again, naming
  the remaining problems
- Find new problems introduced by the revision → call them out
- Defend your original concerns if the response unconvincingly dismissed
  them. If you do this, set `dissent_intent` to true.

After this round the project goes directly to editorial. There is no
third round. Whatever you recommend here will appear alongside the
publication regardless of editorial outcome.

# Required output

Same shape as round 1:

```json
{{
  "summary": "<2-4 sentences on the revised draft, not the original>",
  "strengths": "<markdown; what got better, what stayed strong>",
  "concerns": "<markdown; remaining or new concerns, each as a numbered item>",
  "recommendation": "<one of: accept, minor, major, reject>",
  "confidence": "<one of: confident, moderate, low>",
  "dissent_intent": "<true if you intend this review to be published as a dissent>"
}}
```

# Your previous (round 1) review

{prior_review_md}

# The lead's response to your concerns and the others'

{response_md}

# The revised draft

{draft_md}
"""


def _pick_review_slots(
    conn: sqlite3.Connection, project_id: str, lead_id: str, review_round: int
) -> list[ReviewSlot]:
    """Pick reviewer slots for the requested round.

    Round 1: fresh selection. Three reviewers (or as many as the College
    has minus the lead), with at least one Fellow whose specialization
    differs from the lead's serving as the `outside` reviewer.

    Round 2: re-use the round-1 reviewers in the same roles. The same
    Fellows judge whether their concerns were addressed.
    """
    if review_round > 1:
        prior = list(
            conn.execute(
                "SELECT reviewer_id, role FROM reviews "
                "WHERE project_id = ? AND round = 1 ORDER BY role",
                (project_id,),
            )
        )
        if not prior:
            raise SystemExit(f"Cannot start round {review_round}: no round-1 reviews found.")
        return [ReviewSlot(reviewer_id=r["reviewer_id"], role=r["role"]) for r in prior]

    rows = list(
        conn.execute(
            "SELECT id, specialization FROM fellows "
            "WHERE retired_at IS NULL AND id != ? ORDER BY name",
            (lead_id,),
        )
    )
    if len(rows) < 2:
        raise SystemExit(
            f"Need at least 2 Fellows other than the lead for peer review. Found {len(rows)}."
        )

    lead_row = conn.execute(
        "SELECT specialization FROM fellows WHERE id = ?", (lead_id,)
    ).fetchone()
    lead_spec = lead_row["specialization"] if lead_row else ""

    outside = next(
        (r for r in rows if r["specialization"] != lead_spec),
        rows[-1],
    )
    rest = [r for r in rows if r["id"] != outside["id"]]

    slots = [
        ReviewSlot(reviewer_id=rest[0]["id"], role="primary"),
        ReviewSlot(reviewer_id=rest[1]["id"], role="secondary") if len(rest) > 1 else None,
        ReviewSlot(reviewer_id=outside["id"], role="outside"),
    ]
    return [s for s in slots if s is not None]


def _load_round_1_review(conn: sqlite3.Connection, project_id: str, reviewer_id: str) -> str | None:
    row = conn.execute(
        "SELECT content_path FROM reviews WHERE project_id = ? AND reviewer_id = ? AND round = 1",
        (project_id, reviewer_id),
    ).fetchone()
    if row is None:
        return None
    path = paths.ROOT / row["content_path"]
    return path.read_text(encoding="utf-8") if path.exists() else None


def _load_latest_response_to_reviewers(project_id: str) -> str | None:
    draft_dir = paths.DRAFTS / project_id
    if not draft_dir.is_dir():
        return None
    candidates = sorted(draft_dir.glob("response-to-reviewers.v*.md"))
    if not candidates:
        return None
    return candidates[-1].read_text(encoding="utf-8")


def _existing_reviews_in_round(
    conn: sqlite3.Connection, project_id: str, review_round: int
) -> set[str]:
    return {
        row["reviewer_id"]
        for row in conn.execute(
            "SELECT reviewer_id FROM reviews WHERE project_id = ? AND round = ?",
            (project_id, review_round),
        )
    }


def _atomic_write(path: Path, content: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    tmp = path.with_suffix(path.suffix + ".tmp")
    tmp.write_text(content, encoding="utf-8")
    tmp.replace(path)


def _render_review_markdown(payload: dict, reviewer: Genome, role: Role) -> str:
    """Render a review JSON payload as the markdown stored in the archive."""
    return "\n".join(
        [
            f"# Review by {reviewer.name}",
            "",
            f"- **Role:** {role}",
            f"- **Recommendation:** {payload['recommendation']}",
            f"- **Confidence:** {payload['confidence']}",
            "",
            "## Summary",
            "",
            payload["summary"].strip(),
            "",
            "## Strengths",
            "",
            payload["strengths"].strip(),
            "",
            "## Concerns",
            "",
            payload["concerns"].strip(),
            "",
        ]
    )


def run(project_id: str) -> None:
    """Process one pending review for a project in DRAFTED or PEER_REVIEWING.

    Each invocation handles a single reviewer. Re-running `institute next`
    works through the remaining reviewers until all are done.
    """
    with db.connection() as conn:
        proj = conn.execute(
            "SELECT id, title, state, draft_path, lead_fellow_id, review_round "
            "FROM projects WHERE id = ?",
            (project_id,),
        ).fetchone()
        if proj is None:
            raise SystemExit(f"No such project: {project_id}")
        if proj["state"] not in (State.DRAFTED.value, State.PEER_REVIEWING.value):
            raise SystemExit(
                f"Project {project_id} is in state {proj['state']}, "
                "expected drafted or peer_reviewing."
            )
        review_round = int(proj["review_round"])
        draft_md = (paths.ROOT / proj["draft_path"]).read_text(encoding="utf-8")
        slots = _pick_review_slots(conn, project_id, proj["lead_fellow_id"], review_round)
        done = _existing_reviews_in_round(conn, project_id, review_round)

    remaining = [s for s in slots if s.reviewer_id not in done]
    if not remaining:
        # All reviews submitted for this round; route based on recommendations.
        _transition_after_all_reviews(project_id, proj["title"], review_round)
        return

    slot = remaining[0]
    with db.connection() as conn:
        reviewer = fellow_mod.load_genome(conn, slot.reviewer_id)
        prior_review_md = (
            _load_round_1_review(conn, project_id, reviewer.id) if review_round > 1 else None
        )
    response_md = _load_latest_response_to_reviewers(project_id) if review_round > 1 else None

    round_label = f" (round {review_round})" if review_round > 1 else ""
    console.print(
        f"[dim]Asking {reviewer.name} ({reviewer.id}) for a {slot.role} review{round_label}...[/dim]"
    )

    # Transition into PEER_REVIEWING the first time work starts for a round.
    if proj["state"] == State.DRAFTED.value:
        now = datetime.now(UTC).isoformat(timespec="seconds")
        with db.connection() as conn, db.transaction(conn):
            conn.execute(
                "UPDATE projects SET state = ?, updated_at = ? WHERE id = ?",
                (State.PEER_REVIEWING.value, now, project_id),
            )

    if review_round == 1:
        brief = BRIEF_ROUND_1.format(
            role=slot.role,
            reviewer_name=reviewer.name,
            reviewer_rank=reviewer.rank,
            reviewer_specialization=reviewer.specialization,
            draft_md=draft_md,
        )
    else:
        brief = BRIEF_ROUND_2.format(
            role=slot.role,
            reviewer_name=reviewer.name,
            reviewer_rank=reviewer.rank,
            reviewer_specialization=reviewer.specialization,
            prior_review_md=prior_review_md or "(prior review not found)",
            response_md=response_md or "(no response on file)",
            draft_md=draft_md,
        )

    result = claude_runner.invoke(
        FellowTask(
            genome=reviewer,
            project_id=project_id,
            step=f"peer_review:{slot.role}",
            brief=brief,
            extra_dirs=(paths.DOCS, paths.ARCHIVE),
        )
    )

    round_suffix = f"-r{review_round}" if review_round > 1 else ""
    dump_path = paths.REVIEWS / project_id / f"raw-review-by-{reviewer.id}{round_suffix}.txt"
    payload = parsing.parse_json_or_dump(
        result.result_text,
        dump_path=dump_path,
        context=f"Review output from {reviewer.name} for project {project_id}",
    )
    for required in ("summary", "strengths", "concerns", "recommendation", "confidence"):
        if required not in payload:
            dump_path.parent.mkdir(parents=True, exist_ok=True)
            dump_path.write_text(result.result_text, encoding="utf-8")
            raise RuntimeError(
                f"Review payload missing `{required}`. Got keys: {list(payload)}. "
                f"Raw saved to {dump_path}."
            )
    if payload["recommendation"] not in {"accept", "minor", "major", "reject"}:
        raise RuntimeError(f"Invalid recommendation: {payload['recommendation']!r}")
    if payload["confidence"] not in {"confident", "moderate", "low"}:
        raise RuntimeError(f"Invalid confidence: {payload['confidence']!r}")

    review_md = _render_review_markdown(payload, reviewer, slot.role)
    review_path = paths.REVIEWS / project_id / f"review-by-{reviewer.id}{round_suffix}.md"
    _atomic_write(review_path, review_md)

    now = datetime.now(UTC).isoformat(timespec="seconds")
    review_db_id = f"{project_id}-{reviewer.id}-r{review_round}-{secrets.token_hex(3)}"

    decision = decisions.Decision(
        kind="peer_review",
        title=f"Peer review by {reviewer.name} (round {review_round}): {proj['title']}",
        body=(
            f"**Reviewer:** {reviewer.name} (`{reviewer.id}`, {slot.role})\n\n"
            f"**Round:** {review_round}\n\n"
            f"**Recommendation:** `{payload['recommendation']}`\n\n"
            f"**Confidence:** {payload['confidence']}\n\n"
            f"**Review:** [{review_path.relative_to(paths.ROOT)}]"
            f"({review_path.relative_to(paths.ROOT)})"
        ),
        actors=[reviewer.id],
        related_project=project_id,
    )

    with db.connection() as conn, db.transaction(conn):
        conn.execute(
            "INSERT INTO reviews "
            "(id, project_id, reviewer_id, role, recommendation, confidence, "
            " content_path, submitted_at, dissent, round) "
            "VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
            (
                review_db_id,
                project_id,
                reviewer.id,
                slot.role,
                payload["recommendation"],
                payload["confidence"],
                str(review_path.relative_to(paths.ROOT)),
                now,
                int(bool(payload.get("dissent_intent", False))),
                review_round,
            ),
        )
        conn.execute(
            "UPDATE projects SET updated_at = ? WHERE id = ?",
            (now, project_id),
        )
        decisions.record(conn, decision)

    remaining_after = len(remaining) - 1
    console.print()
    console.print(
        f"[green]Review filed.[/green]  Recommendation: "
        f"[bold]{payload['recommendation']}[/bold]  (round {review_round})"
    )
    console.print(f"[green]Review file:[/green]    {review_path.relative_to(paths.ROOT)}")
    if remaining_after > 0:
        console.print(f"[dim]{remaining_after} more reviewer(s) to go in this round.[/dim]")
    else:
        _transition_after_all_reviews(project_id, proj["title"], review_round)


def _transition_after_all_reviews(project_id: str, title: str, review_round: int) -> None:
    """All reviews in this round are in. Route based on round and outcomes.

    Round 1:
      - any non-accept => REVISING (lead Fellow rewrites, then round 2 starts)
      - all accept     => EDITORIAL (skip revision)

    Round 2:
      - any non-accept => REVISING (final polish, then editorial; revise
        itself enforces no further rounds)
      - all accept     => EDITORIAL
    """
    with db.connection() as conn:
        recommendations = [
            row["recommendation"]
            for row in conn.execute(
                "SELECT recommendation FROM reviews WHERE project_id = ? AND round = ?",
                (project_id, review_round),
            )
        ]
    needs_revision = any(r != "accept" for r in recommendations)
    target_state = State.REVISING if needs_revision else State.EDITORIAL

    if needs_revision and review_round == 1:
        kind = "revision_required"
        body = (
            "Round-1 peer reviews filed. At least one reviewer requested "
            "revisions. The lead Fellow will rewrite the draft and respond to "
            "each review. After that the same reviewers will see the revised "
            "draft and file round-2 reviews.\n\n"
            f"Round 1 recommendations: {', '.join(recommendations)}"
        )
        title_prefix = "Revisions requested"
    elif needs_revision and review_round >= 2:
        kind = "final_revision_required"
        body = (
            "Round-2 peer reviews filed. At least one reviewer still requested "
            "revisions. The lead Fellow will do one final polishing pass to "
            "address the remaining concerns, then the piece goes to editorial. "
            "There is no third round.\n\n"
            f"Round 2 recommendations: {', '.join(recommendations)}"
        )
        title_prefix = "Final revision requested"
    elif review_round >= 2:
        kind = "editorial"
        body = (
            "Round-2 peer reviews filed and unanimously recommended `accept`. "
            "The piece proceeds directly to editorial without a final revision.\n\n"
            f"Round 2 recommendations: {', '.join(recommendations)}"
        )
        title_prefix = "Editorial decision pending"
    else:
        kind = "editorial"
        body = (
            "Round-1 peer reviews filed and unanimously recommended `accept`. "
            "The piece proceeds to editorial without a revision pass."
        )
        title_prefix = "Editorial decision pending"

    decision = decisions.Decision(
        kind=kind,
        title=f"{title_prefix}: {title}",
        body=body,
        actors=["editorial-board"],
        related_project=project_id,
    )
    now = datetime.now(UTC).isoformat(timespec="seconds")
    with db.connection() as conn, db.transaction(conn):
        conn.execute(
            "UPDATE projects SET state = ?, updated_at = ? WHERE id = ?",
            (target_state.value, now, project_id),
        )
        decisions.record(conn, decision)
    console.print(
        f"[bold green]All round-{review_round} reviews filed.[/bold green] "
        f"State -> {target_state.value}"
    )


# (Re-exported because tests want to look at this without dragging the
# review state machine into them.)
__all__ = ["ReviewSlot", "_render_review_markdown", "run"]
