"""Departments (Chapter 2).

A Department is a long-lived gathering of Fellows whose work shares
a methodology or subject matter. A Department Chair, a Senior
Fellow, convenes the seminar, signs off on cross-departmental
collaborations, and is one of the three co-evaluators on a
Postulant's qualifying-project panel (Chapter 5).

A Fellow may belong to multiple Departments. When the department
table is empty (fresh install, before the Founder has set anything
up), code that needs "another department" falls back to the
existing specialization-string proxy in
[`reputation.has_cross_disciplinary_authorship`][institute.reputation.has_cross_disciplinary_authorship]
so the system stays usable during the transition.
"""

from __future__ import annotations

import re
import sqlite3
from dataclasses import dataclass
from datetime import UTC, datetime


@dataclass(frozen=True)
class Department:
    id: str
    name: str
    description: str
    chair_fellow_id: str | None
    created_at: str
    closed_at: str | None


_ID_RE = re.compile(r"^[a-z][a-z0-9-]{1,40}$")


def _slugify(name: str) -> str:
    """Stable, idempotent department id from the human name."""
    out: list[str] = []
    last_dash = True  # don't lead with a dash
    for ch in name.lower():
        if ch.isalnum():
            out.append(ch)
            last_dash = False
        elif not last_dash:
            out.append("-")
            last_dash = True
    s = "".join(out).strip("-")
    return s[:40] or "department"


def create(
    conn: sqlite3.Connection,
    *,
    name: str,
    description: str,
    chair_fellow_id: str | None = None,
) -> Department:
    """Create a new department. Idempotent on (name)."""
    if not name.strip():
        raise ValueError("Department name cannot be empty.")
    if not description.strip():
        raise ValueError("Department description cannot be empty.")
    dept_id = _slugify(name)
    if not _ID_RE.match(dept_id):
        raise ValueError(f"Department name yields invalid id: {dept_id!r}")
    now = datetime.now(UTC).isoformat(timespec="seconds")
    conn.execute(
        "INSERT INTO departments (id, name, description, chair_fellow_id, created_at) "
        "VALUES (?, ?, ?, ?, ?) "
        "ON CONFLICT(id) DO UPDATE SET "
        "  name = excluded.name, "
        "  description = excluded.description, "
        "  chair_fellow_id = COALESCE(excluded.chair_fellow_id, departments.chair_fellow_id)",
        (dept_id, name.strip(), description.strip(), chair_fellow_id, now),
    )
    row = conn.execute(
        "SELECT id, name, description, chair_fellow_id, created_at, closed_at "
        "FROM departments WHERE id = ?",
        (dept_id,),
    ).fetchone()
    return _row_to_department(row)


def _row_to_department(row: sqlite3.Row) -> Department:
    return Department(
        id=row["id"],
        name=row["name"],
        description=row["description"],
        chair_fellow_id=row["chair_fellow_id"],
        created_at=row["created_at"],
        closed_at=row["closed_at"],
    )


def get(conn: sqlite3.Connection, dept_id: str) -> Department | None:
    row = conn.execute(
        "SELECT id, name, description, chair_fellow_id, created_at, closed_at "
        "FROM departments WHERE id = ?",
        (dept_id,),
    ).fetchone()
    return _row_to_department(row) if row else None


def list_all(conn: sqlite3.Connection, *, include_closed: bool = False) -> list[Department]:
    where = "" if include_closed else "WHERE closed_at IS NULL"
    rows = conn.execute(
        f"SELECT id, name, description, chair_fellow_id, created_at, closed_at "
        f"FROM departments {where} ORDER BY name"
    ).fetchall()
    return [_row_to_department(r) for r in rows]


def add_member(
    conn: sqlite3.Connection, *, department_id: str, fellow_id: str
) -> None:
    """Add a Fellow to a Department. Idempotent."""
    now = datetime.now(UTC).isoformat(timespec="seconds")
    conn.execute(
        "INSERT INTO department_memberships (department_id, fellow_id, joined_at) "
        "VALUES (?, ?, ?) "
        "ON CONFLICT(department_id, fellow_id) DO NOTHING",
        (department_id, fellow_id, now),
    )


def remove_member(
    conn: sqlite3.Connection, *, department_id: str, fellow_id: str
) -> None:
    conn.execute(
        "DELETE FROM department_memberships "
        "WHERE department_id = ? AND fellow_id = ?",
        (department_id, fellow_id),
    )


def set_chair(
    conn: sqlite3.Connection, *, department_id: str, fellow_id: str | None
) -> None:
    """Assign or clear the chair. The chair is also added as a member."""
    conn.execute(
        "UPDATE departments SET chair_fellow_id = ? WHERE id = ?",
        (fellow_id, department_id),
    )
    if fellow_id is not None:
        add_member(conn, department_id=department_id, fellow_id=fellow_id)


def for_fellow(conn: sqlite3.Connection, fellow_id: str) -> list[Department]:
    """All open departments this Fellow belongs to."""
    rows = conn.execute(
        "SELECT d.id, d.name, d.description, d.chair_fellow_id, d.created_at, d.closed_at "
        "FROM departments d "
        "JOIN department_memberships m ON m.department_id = d.id "
        "WHERE m.fellow_id = ? AND d.closed_at IS NULL "
        "ORDER BY d.name",
        (fellow_id,),
    ).fetchall()
    return [_row_to_department(r) for r in rows]


def member_ids(conn: sqlite3.Connection, department_id: str) -> list[str]:
    rows = conn.execute(
        "SELECT fellow_id FROM department_memberships "
        "WHERE department_id = ? ORDER BY joined_at",
        (department_id,),
    ).fetchall()
    return [r["fellow_id"] for r in rows]


def is_initialized(conn: sqlite3.Connection) -> bool:
    """True if any department exists. Used by code that falls back to
    specialization-string equality when departments aren't set up."""
    row = conn.execute("SELECT COUNT(*) FROM departments").fetchone()
    return row is not None and row[0] > 0


def same_department(
    conn: sqlite3.Connection, *, fellow_a: str, fellow_b: str
) -> bool:
    """Do two Fellows share at least one department?

    Returns False when departments aren't initialized (fall-back path
    is the caller's responsibility — typically specialization-string
    inequality).
    """
    if not is_initialized(conn):
        return False
    row = conn.execute(
        "SELECT 1 FROM department_memberships a "
        "JOIN department_memberships b "
        "  ON a.department_id = b.department_id "
        "WHERE a.fellow_id = ? AND b.fellow_id = ? "
        "LIMIT 1",
        (fellow_a, fellow_b),
    ).fetchone()
    return row is not None


def close(conn: sqlite3.Connection, department_id: str) -> None:
    """Mark a department closed (terminal). Existing memberships
    remain in the table for audit but stop affecting active queries."""
    now = datetime.now(UTC).isoformat(timespec="seconds")
    conn.execute(
        "UPDATE departments SET closed_at = ? WHERE id = ? AND closed_at IS NULL",
        (now, department_id),
    )
