"""Reviewer reputation, misconduct, and calibration tracking.

Chapter 7's symmetric counterpart to Charter-violation termination.
Authors who violate the Charter are terminated; reviewers who pull
frivolous andon cords, recommend accept on work the Editorial Board
rejects, write lazy reviews, or fail their reviewing duties accumulate
"marks" against their reviewer eligibility.

A Fellow whose active (non-expired) mark weight crosses the threshold
is sidelined from the reviewer pool until enough marks expire to
bring them back under. The genome is unchanged; the Fellow can still
lead proposals, sit on panels, and otherwise participate — only
reviewer eligibility is gated.

Mark kinds and weights:

| kind                  | weight | typical trigger                                   |
|-----------------------|--------|---------------------------------------------------|
| frivolous_andon       | 2.0    | Editorial Board dismissed an andon cord they pulled |
| calibration_miss      | 1.0    | Their round-2 recommendation diverged from the Board |
| lazy_review           | 1.0    | Manual: review lacked substantive engagement      |
| sycophancy            | 2.0    | Manual: accepted weak work because of who wrote it |
| conflict_undisclosed  | 3.0    | Manual: failed to disclose a conflict of interest |
| animus                | 3.0    | Manual: review showed personal animus             |
| other                 | 1.0    | Manual: catch-all                                 |

Default expiry is 90 days. Threshold for ineligibility is total
active weight ≥ 3.0 — a single isolated mistake (one calibration
miss, one frivolous pull) does not sideline a Fellow, but a pattern
does.
"""

from __future__ import annotations

import sqlite3
from dataclasses import dataclass
from datetime import UTC, datetime, timedelta

from institute import db

MARK_KINDS: tuple[str, ...] = (
    "frivolous_andon",
    "calibration_miss",
    "lazy_review",
    "sycophancy",
    "conflict_undisclosed",
    "animus",
    "other",
)

DEFAULT_WEIGHTS: dict[str, float] = {
    "frivolous_andon": 2.0,
    "calibration_miss": 1.0,
    "lazy_review": 1.0,
    "sycophancy": 2.0,
    "conflict_undisclosed": 3.0,
    "animus": 3.0,
    "other": 1.0,
}

DEFAULT_EXPIRY_DAYS: int = 90
INELIGIBILITY_THRESHOLD: float = 3.0


@dataclass(frozen=True)
class Mark:
    id: int
    fellow_id: str
    kind: str
    weight: float
    reason: str | None
    related_project: str | None
    related_review_id: str | None
    recorded_at: str
    expires_at: str


def record_mark(
    conn: sqlite3.Connection,
    *,
    fellow_id: str,
    kind: str,
    reason: str,
    weight: float | None = None,
    expiry_days: int | None = None,
    related_project: str | None = None,
    related_review_id: str | None = None,
) -> int:
    """Record a mark against a reviewer. Caller manages the transaction."""
    if kind not in MARK_KINDS:
        raise ValueError(f"Unknown mark kind: {kind!r}. Must be one of {MARK_KINDS}.")
    if not reason.strip():
        raise ValueError("reason must be non-empty.")
    if weight is None:
        weight = DEFAULT_WEIGHTS[kind]
    if expiry_days is None:
        expiry_days = DEFAULT_EXPIRY_DAYS

    now = datetime.now(UTC)
    expires = now + timedelta(days=expiry_days)
    cursor = conn.execute(
        """
        INSERT INTO reviewer_marks
            (fellow_id, kind, weight, reason, related_project,
             related_review_id, recorded_at, expires_at)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """,
        (
            fellow_id,
            kind,
            float(weight),
            reason.strip(),
            related_project,
            related_review_id,
            now.isoformat(timespec="seconds"),
            expires.isoformat(timespec="seconds"),
        ),
    )
    return int(cursor.lastrowid or 0)


def active_weight(conn: sqlite3.Connection, fellow_id: str) -> float:
    """Total weight of marks that have not yet expired."""
    now = datetime.now(UTC).isoformat(timespec="seconds")
    row = conn.execute(
        "SELECT COALESCE(SUM(weight), 0.0) AS total "
        "FROM reviewer_marks WHERE fellow_id = ? AND expires_at > ?",
        (fellow_id, now),
    ).fetchone()
    return float(row["total"]) if row else 0.0


def is_eligible(conn: sqlite3.Connection, fellow_id: str) -> bool:
    """Eligible to serve as a peer reviewer right now?

    A Fellow is ineligible while their active mark weight is at or
    above the threshold. Eligibility is restored automatically as
    marks expire.
    """
    return active_weight(conn, fellow_id) < INELIGIBILITY_THRESHOLD


def list_marks(
    conn: sqlite3.Connection,
    fellow_id: str,
    *,
    active_only: bool = False,
) -> list[Mark]:
    """List marks for a Fellow, newest first."""
    now = datetime.now(UTC).isoformat(timespec="seconds")
    if active_only:
        rows = list(
            conn.execute(
                "SELECT id, fellow_id, kind, weight, reason, related_project, "
                "       related_review_id, recorded_at, expires_at "
                "FROM reviewer_marks "
                "WHERE fellow_id = ? AND expires_at > ? "
                "ORDER BY recorded_at DESC",
                (fellow_id, now),
            )
        )
    else:
        rows = list(
            conn.execute(
                "SELECT id, fellow_id, kind, weight, reason, related_project, "
                "       related_review_id, recorded_at, expires_at "
                "FROM reviewer_marks WHERE fellow_id = ? "
                "ORDER BY recorded_at DESC",
                (fellow_id,),
            )
        )
    return [
        Mark(
            id=int(r["id"]),
            fellow_id=r["fellow_id"],
            kind=r["kind"],
            weight=float(r["weight"]),
            reason=r["reason"],
            related_project=r["related_project"],
            related_review_id=r["related_review_id"],
            recorded_at=r["recorded_at"],
            expires_at=r["expires_at"],
        )
        for r in rows
    ]


def ineligible_fellow_ids(conn: sqlite3.Connection) -> set[str]:
    """Set of fellow_ids currently above the threshold. For peer_review filter."""
    now = datetime.now(UTC).isoformat(timespec="seconds")
    rows = list(
        conn.execute(
            "SELECT fellow_id, SUM(weight) AS total "
            "FROM reviewer_marks WHERE expires_at > ? "
            "GROUP BY fellow_id HAVING total >= ?",
            (now, INELIGIBILITY_THRESHOLD),
        )
    )
    return {r["fellow_id"] for r in rows}


def safe_record(
    *,
    fellow_id: str,
    kind: str,
    reason: str,
    related_project: str | None = None,
    related_review_id: str | None = None,
) -> None:
    """Best-effort mark recording from workflow code.

    Failures (unknown fellow, bad kind) are logged but never raised,
    so a mark hiccup never blocks the workflow that triggered it.
    """
    try:
        with db.connection() as conn, db.transaction(conn):
            record_mark(
                conn,
                fellow_id=fellow_id,
                kind=kind,
                reason=reason,
                related_project=related_project,
                related_review_id=related_review_id,
            )
    except Exception as exc:  # pragma: no cover - best-effort path
        from rich.console import Console

        Console().print(f"[yellow]reviewer mark failed for {fellow_id}/{kind}: {exc}[/yellow]")
