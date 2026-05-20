"""Author petition for Editorial Board review of a rejected piece.

Per Chapter 7, when all three peer reviewers recommend reject, the
author may petition the Editorial Board to look again. This is the
only path from REJECTED back into an active state.

The petition workflow:

  1. Verifies the project is REJECTED.
  2. Verifies that the rejection was unanimous — all filed reviews
     from the final review round have `recommendation = 'reject'`.
     A non-unanimous rejection is not petitionable; the dissent is
     already published alongside the piece and the Editorial Board
     does not re-litigate it.
  3. Transitions REJECTED -> EDITORIAL_REVIEW with an audit record.
  4. The editorial_review workflow runs on the next `institute next`,
     and the Board renders a final accept / reject.

A successful petition is rare. Most rejections stand. The mechanism
exists to keep the system honest: a Fellow whose piece was killed by
a coordinated reviewer error has a clear path to appeal.
"""

from __future__ import annotations

import sqlite3
from datetime import UTC, datetime

from rich.console import Console

from institute import db, decisions, state
from institute import fellow as fellow_mod
from institute.state import State

console = Console()


class NotPetitionable(SystemExit):
    """The project doesn't meet the petition criteria."""


def _all_reviews_were_reject(conn: sqlite3.Connection, project_id: str) -> bool:
    """True iff every filed review in the final review round was a reject."""
    row = conn.execute(
        "SELECT MAX(round) AS final_round FROM reviews WHERE project_id = ?",
        (project_id,),
    ).fetchone()
    if row is None or row["final_round"] is None:
        return False
    final_round = row["final_round"]
    rows = list(
        conn.execute(
            "SELECT recommendation FROM reviews WHERE project_id = ? AND round = ?",
            (project_id, final_round),
        )
    )
    if not rows:
        return False
    return all(r["recommendation"] == "reject" for r in rows)


def run(project_id: str, *, reason: str) -> None:
    """Initiate an author petition for Editorial Board review."""
    if not reason.strip():
        raise NotPetitionable("Petition requires a non-empty reason.")

    with db.connection() as conn:
        proj = conn.execute(
            "SELECT id, title, state, lead_fellow_id FROM projects WHERE id = ?",
            (project_id,),
        ).fetchone()
        if proj is None:
            raise SystemExit(f"No such project: {project_id}")
        if proj["state"] != State.REJECTED.value:
            raise NotPetitionable(
                f"Project {project_id} is in state {proj['state']}, not rejected. "
                "Petition only applies to rejected projects."
            )
        if not _all_reviews_were_reject(conn, project_id):
            raise NotPetitionable(
                f"Project {project_id} did not have a unanimous reject in the "
                "final review round; Editorial Board does not re-litigate dissents."
            )
        lead = fellow_mod.load_genome(conn, proj["lead_fellow_id"])

    now = datetime.now(UTC).isoformat(timespec="seconds")
    decision = decisions.Decision(
        kind="editorial_petition",
        title=f"Petition filed: {proj['title']}",
        body=(
            f"**Lead Fellow:** {lead.name} (`{lead.id}`)\n\n"
            f"**Previous state:** `rejected` "
            f"(unanimous reject in final review round)\n\n"
            f"**Reason for petition:**\n\n{reason.strip()}\n\n"
            "The project transitions to `editorial_review`. The Editorial "
            "Board's decision (accept or reject) is final."
        ),
        actors=[lead.id, "founder"],
        related_project=project_id,
    )

    with db.connection() as conn, db.transaction(conn):
        state.transition(conn, project_id, State.EDITORIAL_REVIEW)
        decisions.record(conn, decision)
        conn.execute("UPDATE projects SET updated_at = ? WHERE id = ?", (now, project_id))

    console.print(
        f"[yellow]Petition filed.[/yellow] {proj['title']} -> editorial_review. "
        "Run `institute next` for Board decision."
    )
