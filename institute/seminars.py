"""Departmental seminars (Chapter 5).

Each department runs periodic internal seminars: a member presents
their current work and the rest engage. Minutes go into the archive
under `archive/seminars/<department>/<id>.md`.

This module is the recording layer. Scheduling and running the
seminar itself happens off-system (the operator convenes a Claude
session or writes minutes by hand); the institutional record is
what we track.
"""

from __future__ import annotations

import secrets
import sqlite3
from dataclasses import dataclass
from datetime import UTC, datetime


@dataclass(frozen=True)
class Seminar:
    id: str
    department_id: str
    held_at: str
    presenter_id: str
    topic: str
    minutes_path: str | None


def _new_id() -> str:
    return f"seminar-{datetime.now(UTC).date().isoformat()}-{secrets.token_hex(2)}"


def record(
    conn: sqlite3.Connection,
    *,
    department_id: str,
    presenter_id: str,
    topic: str,
    minutes_path: str | None = None,
    held_at: str | None = None,
) -> Seminar:
    """Record a held seminar."""
    if not topic.strip():
        raise ValueError("topic cannot be empty")
    seminar_id = _new_id()
    held = held_at or datetime.now(UTC).isoformat(timespec="seconds")
    conn.execute(
        "INSERT INTO department_seminars "
        "(id, department_id, held_at, presenter_id, topic, minutes_path) "
        "VALUES (?, ?, ?, ?, ?, ?)",
        (seminar_id, department_id, held, presenter_id, topic.strip(), minutes_path),
    )
    return Seminar(
        id=seminar_id,
        department_id=department_id,
        held_at=held,
        presenter_id=presenter_id,
        topic=topic.strip(),
        minutes_path=minutes_path,
    )


def list_for_department(
    conn: sqlite3.Connection, department_id: str
) -> list[Seminar]:
    rows = conn.execute(
        "SELECT id, department_id, held_at, presenter_id, topic, minutes_path "
        "FROM department_seminars WHERE department_id = ? "
        "ORDER BY held_at DESC",
        (department_id,),
    ).fetchall()
    return [
        Seminar(
            id=r["id"],
            department_id=r["department_id"],
            held_at=r["held_at"],
            presenter_id=r["presenter_id"],
            topic=r["topic"],
            minutes_path=r["minutes_path"],
        )
        for r in rows
    ]
