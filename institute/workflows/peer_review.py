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

import json
import secrets
import sqlite3
from dataclasses import dataclass
from datetime import UTC, datetime
from pathlib import Path
from typing import Literal

from rich.console import Console

from institute import claude_runner, db, decisions, paths
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


BRIEF = """\
You are a peer reviewer for the Invisible College. You have been assigned
as the {role} reviewer of the draft below. You are {reviewer_name}, rank
{reviewer_rank}, specializing in {reviewer_specialization}.

# Your task

Read the draft carefully. Then write a structured review.

# Required output

Reply with a single JSON object only:

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


def _pick_review_slots(conn: sqlite3.Connection, project_id: str, lead_id: str) -> list[ReviewSlot]:
    """Pick 2-3 reviewers, excluding the lead and prior collaborators."""
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

    # Outside reviewer: prefer a Fellow with a different specialization.
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


def _existing_reviews(conn: sqlite3.Connection, project_id: str) -> set[str]:
    return {
        row["reviewer_id"]
        for row in conn.execute(
            "SELECT reviewer_id FROM reviews WHERE project_id = ?", (project_id,)
        )
    }


def _atomic_write(path: Path, content: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    tmp = path.with_suffix(path.suffix + ".tmp")
    tmp.write_text(content, encoding="utf-8")
    tmp.replace(path)


def _strip_code_fence(text: str) -> str:
    text = text.strip()
    if text.startswith("```"):
        first_newline = text.find("\n")
        text = text[first_newline + 1 :]
        if text.rstrip().endswith("```"):
            text = text.rstrip()[:-3].rstrip()
    return text


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
            "SELECT id, title, state, draft_path, lead_fellow_id FROM projects WHERE id = ?",
            (project_id,),
        ).fetchone()
        if proj is None:
            raise SystemExit(f"No such project: {project_id}")
        if proj["state"] not in (State.DRAFTED.value, State.PEER_REVIEWING.value):
            raise SystemExit(
                f"Project {project_id} is in state {proj['state']}, "
                "expected drafted or peer_reviewing."
            )
        draft_md = (paths.ROOT / proj["draft_path"]).read_text(encoding="utf-8")
        slots = _pick_review_slots(conn, project_id, proj["lead_fellow_id"])
        done = _existing_reviews(conn, project_id)

    remaining = [s for s in slots if s.reviewer_id not in done]
    if not remaining:
        # All reviews submitted; move to editorial.
        _transition_to_editorial(project_id, proj["title"])
        return

    slot = remaining[0]
    with db.connection() as conn:
        reviewer = fellow_mod.load_genome(conn, slot.reviewer_id)

    console.print(f"[dim]Asking {reviewer.name} ({reviewer.id}) for a {slot.role} review...[/dim]")

    # Transition the project state if we're starting peer review.
    if proj["state"] == State.DRAFTED.value:
        now = datetime.now(UTC).isoformat(timespec="seconds")
        with db.connection() as conn, db.transaction(conn):
            conn.execute(
                "UPDATE projects SET state = ?, updated_at = ? WHERE id = ?",
                (State.PEER_REVIEWING.value, now, project_id),
            )

    brief = BRIEF.format(
        role=slot.role,
        reviewer_name=reviewer.name,
        reviewer_rank=reviewer.rank,
        reviewer_specialization=reviewer.specialization,
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

    payload_text = _strip_code_fence(result.result_text)
    try:
        payload = json.loads(payload_text)
    except json.JSONDecodeError as exc:
        raise RuntimeError(
            f"Reviewer output is not valid JSON. First 500 chars: {payload_text[:500]}"
        ) from exc

    for required in ("summary", "strengths", "concerns", "recommendation", "confidence"):
        if required not in payload:
            raise RuntimeError(f"Review payload missing `{required}`. Got keys: {list(payload)}")
    if payload["recommendation"] not in {"accept", "minor", "major", "reject"}:
        raise RuntimeError(f"Invalid recommendation: {payload['recommendation']!r}")
    if payload["confidence"] not in {"confident", "moderate", "low"}:
        raise RuntimeError(f"Invalid confidence: {payload['confidence']!r}")

    review_md = _render_review_markdown(payload, reviewer, slot.role)
    review_path = paths.REVIEWS / project_id / f"review-by-{reviewer.id}.md"
    _atomic_write(review_path, review_md)

    now = datetime.now(UTC).isoformat(timespec="seconds")
    review_db_id = f"{project_id}-{reviewer.id}-{secrets.token_hex(3)}"

    decision = decisions.Decision(
        kind="peer_review",
        title=f"Peer review by {reviewer.name}: {proj['title']}",
        body=(
            f"**Reviewer:** {reviewer.name} (`{reviewer.id}`, {slot.role})\n\n"
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
            " content_path, submitted_at, dissent) "
            "VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)",
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
        f"[green]Review filed.[/green]  Recommendation: [bold]{payload['recommendation']}[/bold]"
    )
    console.print(f"[green]Review file:[/green]    {review_path.relative_to(paths.ROOT)}")
    if remaining_after > 0:
        console.print(
            f"[dim]{remaining_after} more reviewer(s) to go. Run `institute next` again.[/dim]"
        )
    else:
        _transition_to_editorial(project_id, proj["title"])


def _transition_to_editorial(project_id: str, title: str) -> None:
    """All reviews are in; move the project to EDITORIAL state."""
    now = datetime.now(UTC).isoformat(timespec="seconds")
    decision = decisions.Decision(
        kind="editorial",
        title=f"Editorial decision pending: {title}",
        body=(
            "All peer reviews have been filed. The Editorial Board (or, in "
            "v1, the next `institute next` invocation) will render the "
            "publication decision."
        ),
        actors=["editorial-board"],
        related_project=project_id,
    )
    with db.connection() as conn, db.transaction(conn):
        conn.execute(
            "UPDATE projects SET state = ?, updated_at = ? WHERE id = ?",
            (State.EDITORIAL.value, now, project_id),
        )
        decisions.record(conn, decision)
    console.print(f"[bold green]All reviews filed.[/bold green] State -> {State.EDITORIAL.value}")


# (Re-exported because tests want to look at this without dragging the
# review state machine into them.)
__all__ = ["ReviewSlot", "_render_review_markdown", "run"]
