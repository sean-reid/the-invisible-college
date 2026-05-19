"""The Editorial Board: a standing rotating panel of Senior Fellows.

Chapter 7 of the design specifies an Editorial Board as a backstop
that intervenes when needed:

  - Makes final accept/reject decisions when reviewers disagree.
  - Reviews submissions where all reviewers recommended reject (the
    author may petition for review).
  - Sets editorial standards for the blog.
  - Handles cases where reviewers themselves are alleged to have
    failed in their reviewing duties.

The Board is "typically three" Senior Fellows with rotating
membership. In v1, with ≤3 Senior Fellows in the cohort, all serve
simultaneously and the rotation never fires. When the cohort grows to
>3 Senior Fellows, the three longest-tenured (by promotion timestamp
in the audit log; created_at fallback for the founding cohort) serve
as members. Rotation by term length comes in a follow-up.
"""

from __future__ import annotations

import sqlite3
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


def current_member_ids(conn: sqlite3.Connection) -> list[str]:
    """Resolve the Editorial Board membership for this moment.

    Up to BOARD_SEAT_COUNT Senior Fellows, longest-tenured first.
    Stable for a given DB state; will only change when a Fellow
    becomes Senior, gets demoted from Senior, or is released.
    """
    rows = list(
        conn.execute("SELECT id FROM fellows WHERE rank = 'senior_fellow' AND retired_at IS NULL")
    )
    if not rows:
        return []
    scored = [(_tenure_timestamp(conn, r["id"]), r["id"]) for r in rows]
    scored.sort(key=lambda t: (t[0] or "", t[1]))
    return [fellow_id for _, fellow_id in scored[:BOARD_SEAT_COUNT]]


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
