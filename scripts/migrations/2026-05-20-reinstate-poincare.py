"""One-time migration: reinstate Henri Poincaré.

On 2026-05-20 the calendar-triggered tenure-review cadence reached
Poincaré (Senior Fellow) for the third time. The orchestrator's
recommendation and Pierre Bayle's panel vote both held, both with
rationales explicitly stating the holds reflected the ladder's
terminal-rank ceiling and not Poincaré's performance. The
`two_consecutive_holds` gate then auto-released him anyway, against
the panel's and orchestrator's stated intent.

This script reverses that release. It:

  1. Loads Poincaré (including retired_at).
  2. Refuses to run if he has already been reinstated (idempotent).
  3. Writes a `senior_fellow_confirmed` decision that explains the
     institutional cause of the release (structural ceiling, not
     performance) and confirms his Senior Fellow standing.
  4. Clears `retired_at` in the same transaction so he reappears in
     active workflows.

The original release decision in archive/decisions/ stays in place as
the audit trail of what actually happened. The new confirmation
decision is the institutional acknowledgement of the error.

Run once:
    uv run python scripts/migrations/2026-05-20-reinstate-poincare.py
"""

from __future__ import annotations

import sys
from datetime import UTC, datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))

from institute import db, decisions, reputation  # noqa: E402

FELLOW_ID = "henri-poincare"


def main() -> int:
    with db.connection() as conn:
        row = conn.execute(
            "SELECT id, name, rank, retired_at FROM fellows WHERE id = ?",
            (FELLOW_ID,),
        ).fetchone()
    if row is None:
        print(f"No such Fellow: {FELLOW_ID!r}", file=sys.stderr)
        return 1
    if row["retired_at"] is None:
        print(f"{row['name']} is already active. No action taken.")
        return 0

    # Reputation builder skips retired Fellows; build a snapshot the
    # decision body can quote by clearing retired_at temporarily would
    # be a hack. Instead, read the numbers directly from the prior
    # release record's snapshot, which is the contemporaneous truth.
    # We re-quote a short version here; the full numbers live in the
    # release record next to this one in the archive.
    now = datetime.now(UTC).isoformat(timespec="seconds")
    body = f"""**Fellow:** {row["name"]} (`{row["id"]}`)

**Outcome:** confirmed (Senior Fellow standing restored)

**Recorded:** {now}

**Trigger:** institutional correction of a structural auto-release.

Between 2026-05-18 and 2026-05-20 the calendar-triggered tenure-review
cadence held {row["name"]} three times at the senior_fellow rank. The
holds reflected the ladder's terminal-rank ceiling (no rank above
senior_fellow except emeritus, which is reserved for Fellows winding
down) and not any failure of his work. Both the orchestrator and
panelist Pierre Bayle stated this explicitly in the third review;
Bayle voted hold, the orchestrator's rationale read "Release would
be punishing him for the ladder topping out, not for disengagement."

The `two_consecutive_holds` gate then auto-released him anyway. The
archive preserves that release record at
`archive/decisions/2026-05-20-release-released-henri-poincaré-senior-fellow.md`
as the audit trail of what happened.

This decision is the institutional acknowledgement that the release
was a structural error. The institution rules have since been changed
to prevent this pattern: Senior Fellows are no longer enrolled in
calendar-triggered tenure review, the consecutive-holds count is
reset by `senior_fellow_confirmed` events, and the auto-release gate
is rank-conditional and does not fire for the terminal rank.

{row["name"]}'s Senior Fellow standing is restored. His
publications, reviews, and reviewer record stand. The `retired_at`
field is cleared in the same transaction that records this decision.
"""

    decision = decisions.Decision(
        kind="senior_fellow_confirmed",
        title=f"{row['name']}: Senior Fellow standing restored",
        body=body,
        actors=["founder", FELLOW_ID],
    )

    with db.connection() as conn, db.transaction(conn):
        conn.execute(
            "UPDATE fellows SET retired_at = NULL WHERE id = ?",
            (FELLOW_ID,),
        )
        path = decisions.record(conn, decision)

    with db.connection() as conn:
        streak = reputation.consecutive_holds(conn, FELLOW_ID)
        active = conn.execute(
            "SELECT rank, retired_at FROM fellows WHERE id = ?",
            (FELLOW_ID,),
        ).fetchone()

    print(f"Reinstated: {row['name']} ({FELLOW_ID})")
    print(f"  rank: {active['rank']}")
    print(f"  retired_at: {active['retired_at']!r}")
    print(f"  consecutive_holds: {streak}")
    print(f"  decision: {path.relative_to(ROOT)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
