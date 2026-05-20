"""Centers (Chapter 2).

A Center is a finite-term cross-disciplinary convening: a focused
research question that pulls Fellows from multiple departments
for a defined window, ending with a written report.

The shape:
  * `open(name, motivation, term_days)` creates the Center with a
    deadline `term_days` from now (default 90).
  * `add_member(center_id, fellow_id, role='member')` adds a Fellow.
    Convention: at least one member from at least two different
    departments before the Center is considered well-formed.
  * `close(center_id, report_path)` records the final report and
    closes the Center. Closing without a report is allowed but
    surfaces in audits as an unfinished Center.

Centers do not have their own state machine: the Center is just
a roster + deadline + report. Each Fellow's actual work happens in
ordinary research projects whose archive lives elsewhere. The
Center is the convening, not the workflow.
"""

from __future__ import annotations

import re
import sqlite3
from dataclasses import dataclass
from datetime import UTC, datetime, timedelta

DEFAULT_TERM_DAYS = 90


@dataclass(frozen=True)
class Center:
    id: str
    name: str
    motivation: str
    opened_at: str
    closes_at: str
    closed_at: str | None
    report_path: str | None


_ID_RE = re.compile(r"^[a-z][a-z0-9-]{0,40}$")


def _slugify(name: str) -> str:
    out: list[str] = []
    last_dash = True
    for ch in name.lower():
        if ch.isalnum():
            out.append(ch)
            last_dash = False
        elif not last_dash:
            out.append("-")
            last_dash = True
    return "".join(out).strip("-")[:40] or "center"


def _row(row: sqlite3.Row) -> Center:
    return Center(
        id=row["id"],
        name=row["name"],
        motivation=row["motivation"],
        opened_at=row["opened_at"],
        closes_at=row["closes_at"],
        closed_at=row["closed_at"],
        report_path=row["report_path"],
    )


def open_center(
    conn: sqlite3.Connection,
    *,
    name: str,
    motivation: str,
    term_days: int = DEFAULT_TERM_DAYS,
) -> Center:
    if not name.strip():
        raise ValueError("Center name cannot be empty.")
    if not motivation.strip():
        raise ValueError("Center motivation cannot be empty.")
    if term_days < 1:
        raise ValueError("term_days must be positive.")
    center_id = _slugify(name)
    if not _ID_RE.match(center_id):
        raise ValueError(f"Center name yields invalid id: {center_id!r}")
    now = datetime.now(UTC)
    closes = now + timedelta(days=term_days)
    conn.execute(
        "INSERT INTO centers (id, name, motivation, opened_at, closes_at) "
        "VALUES (?, ?, ?, ?, ?) "
        "ON CONFLICT(id) DO UPDATE SET "
        "  name = excluded.name, "
        "  motivation = excluded.motivation, "
        "  closes_at = excluded.closes_at",
        (
            center_id,
            name.strip(),
            motivation.strip(),
            now.isoformat(timespec="seconds"),
            closes.isoformat(timespec="seconds"),
        ),
    )
    row = conn.execute(
        "SELECT id, name, motivation, opened_at, closes_at, closed_at, report_path "
        "FROM centers WHERE id = ?",
        (center_id,),
    ).fetchone()
    return _row(row)


def add_member(
    conn: sqlite3.Connection,
    *,
    center_id: str,
    fellow_id: str,
    role: str = "member",
) -> None:
    now = datetime.now(UTC).isoformat(timespec="seconds")
    conn.execute(
        "INSERT INTO center_memberships (center_id, fellow_id, role, joined_at) "
        "VALUES (?, ?, ?, ?) "
        "ON CONFLICT(center_id, fellow_id) DO UPDATE SET role = excluded.role",
        (center_id, fellow_id, role, now),
    )


def close(
    conn: sqlite3.Connection,
    *,
    center_id: str,
    report_path: str | None = None,
) -> None:
    """Close a Center. Records a final report path if provided."""
    now = datetime.now(UTC).isoformat(timespec="seconds")
    conn.execute(
        "UPDATE centers SET closed_at = ?, report_path = ? "
        "WHERE id = ? AND closed_at IS NULL",
        (now, report_path, center_id),
    )


def get(conn: sqlite3.Connection, center_id: str) -> Center | None:
    row = conn.execute(
        "SELECT id, name, motivation, opened_at, closes_at, closed_at, report_path "
        "FROM centers WHERE id = ?",
        (center_id,),
    ).fetchone()
    return _row(row) if row else None


def list_open(conn: sqlite3.Connection) -> list[Center]:
    rows = conn.execute(
        "SELECT id, name, motivation, opened_at, closes_at, closed_at, report_path "
        "FROM centers WHERE closed_at IS NULL ORDER BY opened_at"
    ).fetchall()
    return [_row(r) for r in rows]


def member_ids(conn: sqlite3.Connection, center_id: str) -> list[str]:
    rows = conn.execute(
        "SELECT fellow_id FROM center_memberships WHERE center_id = ? ORDER BY joined_at",
        (center_id,),
    ).fetchall()
    return [r["fellow_id"] for r in rows]


def expired_unclosed(conn: sqlite3.Connection) -> list[Center]:
    """Centers whose closes_at has passed but which are still open.

    Surfaced by audit tooling so the Founder sees stalled Centers.
    """
    now = datetime.now(UTC).isoformat(timespec="seconds")
    rows = conn.execute(
        "SELECT id, name, motivation, opened_at, closes_at, closed_at, report_path "
        "FROM centers WHERE closed_at IS NULL AND closes_at < ? "
        "ORDER BY closes_at",
        (now,),
    ).fetchall()
    return [_row(r) for r in rows]
