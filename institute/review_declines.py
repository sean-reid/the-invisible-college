"""Reviewer-decline tracking (Chapter 7 reliability metric).

A Fellow who is assigned a peer review may decline the assignment
(undisclosed CoI, scope outside specialization, simple refusal).
Each decline is recorded here. The count surfaces on the Fellow's
profile and feeds promotion review: repeated declines indicate the
Fellow is unwilling or unable to bear the institutional load that
the rank requires.

The actual peer-review workflow assigns reviewers algorithmically;
this module is the manual fallback for a Founder who needs to mark
that a Fellow refused or could not deliver a review they were asked
for. Auto-detection from invocation failures is a future
enhancement.
"""

from __future__ import annotations

import sqlite3
from dataclasses import dataclass
from datetime import UTC, datetime


@dataclass(frozen=True)
class Decline:
    id: int
    fellow_id: str
    project_id: str | None
    declined_at: str
    reason: str


def record(
    conn: sqlite3.Connection,
    *,
    fellow_id: str,
    reason: str,
    project_id: str | None = None,
    at: str | None = None,
) -> int:
    """Insert a new decline record. Returns its row id."""
    if not reason.strip():
        raise ValueError("decline requires a non-empty reason")
    at = at or datetime.now(UTC).isoformat(timespec="seconds")
    cur = conn.execute(
        "INSERT INTO review_declines (fellow_id, project_id, declined_at, reason) "
        "VALUES (?, ?, ?, ?)",
        (fellow_id, project_id, at, reason.strip()),
    )
    return cur.lastrowid or 0


def count_for(conn: sqlite3.Connection, fellow_id: str) -> int:
    """Number of recorded declines for a Fellow."""
    return conn.execute(
        "SELECT COUNT(*) FROM review_declines WHERE fellow_id = ?", (fellow_id,)
    ).fetchone()[0]


def list_for(conn: sqlite3.Connection, fellow_id: str) -> list[Decline]:
    """All declines for a Fellow, oldest first."""
    rows = conn.execute(
        "SELECT id, fellow_id, project_id, declined_at, reason "
        "FROM review_declines WHERE fellow_id = ? ORDER BY declined_at",
        (fellow_id,),
    ).fetchall()
    return [
        Decline(
            id=r["id"],
            fellow_id=r["fellow_id"],
            project_id=r["project_id"],
            declined_at=r["declined_at"],
            reason=r["reason"],
        )
        for r in rows
    ]


def reliability_label(decline_count: int, completed_reviews: int) -> str:
    """One-word label for the Fellow's reviewer reliability.

    Used on the public profile alongside the raw counts. Conservative
    thresholds: a Fellow needs several completed reviews before any
    decline-rate reading is meaningful.
    """
    if completed_reviews < 3 and decline_count == 0:
        return "new"
    if decline_count == 0:
        return "reliable"
    rate = decline_count / max(decline_count + completed_reviews, 1)
    if rate < 0.1:
        return "reliable"
    if rate < 0.3:
        return "mixed"
    return "unreliable"
