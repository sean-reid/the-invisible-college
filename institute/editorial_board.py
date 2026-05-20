"""The Editorial Board: a standing rotating panel of Senior Fellows.

Chapter 7 of the design specifies an Editorial Board as a backstop
that intervenes when needed:

  - Makes final accept/reject decisions when reviewers disagree.
  - Reviews submissions where all reviewers recommended reject (the
    author may petition for review).
  - Sets editorial standards for the blog.
  - Handles cases where reviewers themselves are alleged to have
    failed in their reviewing duties.

The Board is "typically three" Senior Fellows with **rotating
membership**. Rotation here is deterministic and tenure-anchored:

  - Term length is one calendar month (UTC). Each new month begins
    a fresh rotation window.
  - When the cohort has at most BOARD_SEAT_COUNT eligible Senior
    Fellows, all serve and rotation is a no-op.
  - When more Senior Fellows are eligible than seats, the cohort
    is cycled by the month index: at month N the seats are held by
    `eligible[N % len : N % len + BOARD_SEAT_COUNT]` (wrapping).
    The order is by tenure, longest-tenured first.

This rotates every month, never seats fewer than the cohort
allows, and avoids any persistent term state — the membership for
any moment is a pure function of (rank, tenure, current month).
"""

from __future__ import annotations

import sqlite3
from datetime import UTC, datetime
from pathlib import Path

from institute import fellow as fellow_mod
from institute.fellow import Genome

BOARD_SEAT_COUNT = 3


def _tenure_timestamp(conn: sqlite3.Connection, fellow_id: str) -> str:
    """Best estimate of how long this Fellow has been at Senior Fellow rank.

    Uses the earliest `promotion` audit entry mentioning the Fellow as
    the proxy for when they reached Senior Fellow. Falls back to the
    Fellow's `created_at` if there is no promotion record (the founding
    cohort, who started at fellow/senior_fellow without a promotion).
    """
    row = conn.execute(
        "SELECT MIN(at) AS first_promotion FROM audit_log "
        "WHERE action = 'promotion' "
        "  AND (',' || actor || ',') LIKE ?",
        (f"%,{fellow_id},%",),
    ).fetchone()
    if row is not None and row["first_promotion"]:
        return row["first_promotion"]
    row = conn.execute("SELECT created_at FROM fellows WHERE id = ?", (fellow_id,)).fetchone()
    return row["created_at"] if row else ""


def _month_index(now: datetime | None = None) -> int:
    """Return a monotone integer for the current UTC calendar month."""
    now = now or datetime.now(UTC)
    return now.year * 12 + (now.month - 1)


def _rotate(window: list[str], offset: int) -> list[str]:
    if not window:
        return []
    k = offset % len(window)
    return window[k:] + window[:k]


def current_member_ids(
    conn: sqlite3.Connection,
    *,
    at: datetime | None = None,
) -> list[str]:
    """Resolve the Editorial Board membership for this moment.

    Returns at most BOARD_SEAT_COUNT Senior Fellows. With more Senior
    Fellows than seats, the cohort cycles by calendar month so any
    given Senior Fellow rotates onto and off the Board over time.
    `at` is provided for tests; defaults to now.
    """
    rows = list(
        conn.execute("SELECT id FROM fellows WHERE rank = 'senior_fellow' AND retired_at IS NULL")
    )
    if not rows:
        return []
    scored = [(_tenure_timestamp(conn, r["id"]), r["id"]) for r in rows]
    # Stable order: longest-tenured first, then lexicographic id.
    scored.sort(key=lambda t: (t[0] or "", t[1]))
    ordered_ids = [fellow_id for _, fellow_id in scored]
    if len(ordered_ids) <= BOARD_SEAT_COUNT:
        return ordered_ids
    rotated = _rotate(ordered_ids, _month_index(at))
    return rotated[:BOARD_SEAT_COUNT]


def current_members(conn: sqlite3.Connection) -> list[Genome]:
    """Load the current Board members' genomes."""
    return [Genome.from_file(fellow_mod.genome_path(fid)) for fid in current_member_ids(conn)]


def has_quorum(conn: sqlite3.Connection) -> bool:
    """At least one Senior Fellow exists to serve. Board can operate."""
    return len(current_member_ids(conn)) > 0


def render_membership_markdown(conn: sqlite3.Connection) -> str:
    """Human-readable list of current members, for decision records."""
    members = current_members(conn)
    if not members:
        return "_(no current Editorial Board — no Senior Fellows yet)_\n"
    lines = ["# Editorial Board (current membership)", ""]
    for m in members:
        lines.append(f"- {m.name} (`{m.id}`, {m.specialization})")
    return "\n".join(lines) + "\n"


__all__ = [
    "BOARD_SEAT_COUNT",
    "current_member_ids",
    "current_members",
    "has_quorum",
    "render_membership_markdown",
]


# Re-export Path so module type-check tools don't complain about unused imports.
_ = Path
