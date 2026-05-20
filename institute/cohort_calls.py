"""Chapter 4 admissions: calls-for-applications.

A cohort call is a public statement that the College is recruiting:
"we want N new Postulants, prioritizing these specializations, these
model backends, these intellectual orientations." Candidates flow
into an open call (orchestrator-drafted or Fellow-sponsored), the
admit panel evaluates them together, the top N are admitted, the
rest are held or rejected.

Only one call may be open at a time in v1. Closing happens either
automatically (admits_count reaches target_size) or manually via
the CLI.
"""

from __future__ import annotations

import secrets
import sqlite3
from dataclasses import dataclass
from datetime import UTC, date, datetime

from institute import db


@dataclass(frozen=True)
class CohortCall:
    id: str
    opened_at: str
    opened_by: str
    target_size: int
    target_specializations: list[str]
    target_models: list[str]
    orientations: list[str]
    status: str  # 'open' or 'closed'
    closed_at: str | None
    closed_reason: str | None
    admits_count: int


def _split(value: str | None) -> list[str]:
    if not value:
        return []
    return [item.strip() for item in value.split(",") if item.strip()]


def _join(items: list[str] | None) -> str | None:
    if not items:
        return None
    return ", ".join(item.strip() for item in items if item.strip()) or None


def _row_to_call(row: sqlite3.Row) -> CohortCall:
    return CohortCall(
        id=row["id"],
        opened_at=row["opened_at"],
        opened_by=row["opened_by"],
        target_size=int(row["target_size"]),
        target_specializations=_split(row["target_specializations"]),
        target_models=_split(row["target_models"]),
        orientations=_split(row["orientations"]),
        status=row["status"],
        closed_at=row["closed_at"],
        closed_reason=row["closed_reason"],
        admits_count=int(row["admits_count"]),
    )


def _new_id() -> str:
    return f"call-{date.today().isoformat()}-{secrets.token_hex(2)}"


def open_call(
    *,
    target_size: int,
    target_specializations: list[str] | None = None,
    target_models: list[str] | None = None,
    orientations: list[str] | None = None,
    opened_by: str = "founder",
) -> CohortCall:
    """Open a new cohort call. Raises if another call is already open."""
    if target_size <= 0:
        raise ValueError(f"target_size must be ≥ 1 (got {target_size}).")
    with db.connection() as conn, db.transaction(conn):
        existing = conn.execute(
            "SELECT id FROM cohort_calls WHERE status = 'open' LIMIT 1"
        ).fetchone()
        if existing is not None:
            raise ValueError(
                f"A cohort call is already open: {existing['id']}. Close it "
                "first with `institute admit close-call` before opening another."
            )
        call_id = _new_id()
        now = datetime.now(UTC).isoformat(timespec="seconds")
        conn.execute(
            """
            INSERT INTO cohort_calls
                (id, opened_at, opened_by, target_size,
                 target_specializations, target_models, orientations,
                 status, closed_at, closed_reason, admits_count)
            VALUES (?, ?, ?, ?, ?, ?, ?, 'open', NULL, NULL, 0)
            """,
            (
                call_id,
                now,
                opened_by,
                int(target_size),
                _join(target_specializations),
                _join(target_models),
                _join(orientations),
            ),
        )
        row = conn.execute("SELECT * FROM cohort_calls WHERE id = ?", (call_id,)).fetchone()
    return _row_to_call(row)


def close_call(call_id: str, *, reason: str = "manual") -> CohortCall:
    """Close a call. Idempotent: closing a closed call returns the existing row."""
    with db.connection() as conn, db.transaction(conn):
        row = conn.execute("SELECT * FROM cohort_calls WHERE id = ?", (call_id,)).fetchone()
        if row is None:
            raise ValueError(f"No such cohort call: {call_id!r}")
        if row["status"] == "closed":
            return _row_to_call(row)
        now = datetime.now(UTC).isoformat(timespec="seconds")
        conn.execute(
            "UPDATE cohort_calls SET status = 'closed', "
            "closed_at = ?, closed_reason = ? WHERE id = ?",
            (now, reason, call_id),
        )
        row = conn.execute("SELECT * FROM cohort_calls WHERE id = ?", (call_id,)).fetchone()
    return _row_to_call(row)


def current_call() -> CohortCall | None:
    """Return the currently open call, if any."""
    with db.connection() as conn:
        row = conn.execute(
            "SELECT * FROM cohort_calls WHERE status = 'open' ORDER BY opened_at DESC LIMIT 1"
        ).fetchone()
    return _row_to_call(row) if row else None


def list_calls(limit: int = 20) -> list[CohortCall]:
    """List recent calls, newest first."""
    with db.connection() as conn:
        rows = list(
            conn.execute(
                "SELECT * FROM cohort_calls ORDER BY opened_at DESC LIMIT ?",
                (int(limit),),
            )
        )
    return [_row_to_call(r) for r in rows]


def increment_admits(
    conn: sqlite3.Connection,
    call_id: str,
) -> CohortCall:
    """Bump admits_count for the call. Auto-closes when count == target_size.
    Caller manages the transaction; this runs in the same one as the admit
    decision so accounting stays atomic.
    """
    row = conn.execute("SELECT * FROM cohort_calls WHERE id = ?", (call_id,)).fetchone()
    if row is None:
        raise ValueError(f"No such cohort call: {call_id!r}")
    new_count = int(row["admits_count"]) + 1
    if new_count >= int(row["target_size"]):
        now = datetime.now(UTC).isoformat(timespec="seconds")
        conn.execute(
            "UPDATE cohort_calls SET admits_count = ?, status = 'closed', "
            "closed_at = ?, closed_reason = 'target_size reached' "
            "WHERE id = ?",
            (new_count, now, call_id),
        )
    else:
        conn.execute(
            "UPDATE cohort_calls SET admits_count = ? WHERE id = ?",
            (new_count, call_id),
        )
    row = conn.execute("SELECT * FROM cohort_calls WHERE id = ?", (call_id,)).fetchone()
    return _row_to_call(row)


def render_for_admit(call: CohortCall) -> str:
    """Render a markdown block the admit workflow stages into the
    candidate-generation and panel workspaces, so both see what the call
    is asking for.
    """
    lines = [
        f"# Open call: `{call.id}`",
        "",
        f"- **Target cohort size:** {call.target_size}",
        f"- **Admitted so far:** {call.admits_count}",
        f"- **Status:** {call.status}",
        "",
    ]
    if call.target_specializations:
        lines.append(f"**Targeted specializations:** {', '.join(call.target_specializations)}")
        lines.append("")
    if call.target_models:
        lines.append(f"**Targeted model backends:** {', '.join(call.target_models)}")
        lines.append("")
    if call.orientations:
        lines.append(f"**Intellectual orientations:** {', '.join(call.orientations)}")
        lines.append("")
    if not (call.target_specializations or call.target_models or call.orientations):
        lines.append("_No specific targets — admit at the committee's discretion._")
        lines.append("")
    return "\n".join(lines)


__all__ = [
    "CohortCall",
    "close_call",
    "current_call",
    "increment_admits",
    "list_calls",
    "open_call",
    "render_for_admit",
]
