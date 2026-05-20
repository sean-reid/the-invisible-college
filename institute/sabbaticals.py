"""Sabbaticals (Chapter 5).

A Senior Fellow may take a sabbatical: a defined window during
which they are skipped by reviewer-selection, panel-formation, and
Editorial Board rotation. The Fellow remains in the cohort and the
genome stays in `genomes/`; only the institutional load they
shoulder is suspended.

Convention: a sabbatical is one calendar month (the doc's
default). Longer is allowed; the operator sets `sabbatical_until`
explicitly. The mechanism is a single nullable timestamp on the
fellows row: when it's NULL or in the past, the Fellow is active.

Other code that picks Fellows for review duty / panels should
combine the existing `retired_at IS NULL` filter with
`on_sabbatical(conn, fellow_id) IS FALSE`. The `eligible_filter`
SQL helper below makes that one consistent fragment.
"""

from __future__ import annotations

import sqlite3
from datetime import UTC, datetime, timedelta

# SQL fragment that filters out on-sabbatical Fellows. Append to any
# query's WHERE clause; pass `now_iso()` as the bound parameter.
# The fragment is unprefixed so callers using a table alias should
# prepend it themselves: e.g. `f.{ACTIVE_FILTER}`.
ACTIVE_FILTER = "(sabbatical_until IS NULL OR sabbatical_until <= ?)"


def now_iso() -> str:
    """Same-tz ISO timestamp used as the ACTIVE_FILTER bound param."""
    return datetime.now(UTC).isoformat(timespec="seconds")


# Backwards-compatible alias for the (briefly) earlier name. New code
# should import ACTIVE_FILTER + now_iso() directly.
SQL_NOT_ON_SABBATICAL = ACTIVE_FILTER
_now_iso = now_iso


def begin(
    conn: sqlite3.Connection,
    *,
    fellow_id: str,
    days: int = 30,
) -> str:
    """Place the Fellow on sabbatical until now+days. Returns the timestamp."""
    if days <= 0:
        raise ValueError("Sabbatical days must be positive.")
    end = (datetime.now(UTC) + timedelta(days=days)).isoformat(timespec="seconds")
    conn.execute(
        "UPDATE fellows SET sabbatical_until = ? WHERE id = ?",
        (end, fellow_id),
    )
    return end


def end(conn: sqlite3.Connection, *, fellow_id: str) -> None:
    """Clear an active sabbatical immediately."""
    conn.execute(
        "UPDATE fellows SET sabbatical_until = NULL WHERE id = ?",
        (fellow_id,),
    )


def on_sabbatical(conn: sqlite3.Connection, fellow_id: str) -> bool:
    row = conn.execute(
        "SELECT sabbatical_until FROM fellows WHERE id = ?", (fellow_id,)
    ).fetchone()
    if row is None or row["sabbatical_until"] is None:
        return False
    return row["sabbatical_until"] > _now_iso()


def currently_on_sabbatical(conn: sqlite3.Connection) -> list[str]:
    """Ids of all Fellows currently on sabbatical."""
    now = _now_iso()
    rows = conn.execute(
        "SELECT id FROM fellows "
        "WHERE retired_at IS NULL AND sabbatical_until IS NOT NULL "
        "  AND sabbatical_until > ? "
        "ORDER BY id",
        (now,),
    ).fetchall()
    return [r["id"] for r in rows]
