"""Append-only, hash-chained audit log.

Every significant institutional action — admission, promotion,
proposal disposition, peer review, publication, Charter tripwire,
Fellow termination — is recorded as a row in `audit_log`. The Charter
(Chapter 1) requires that the log be append-only: no Fellow can edit
or delete prior entries.

This module provides:

  * `append(...)`: the only sanctioned write path. Computes the next
    row's `hash` from the previous row's hash plus the row's fields,
    and writes both. The hash chain makes silent tampering detectable
    even if a future attacker bypasses the table-level UPDATE/DELETE
    triggers (e.g. by using a raw sqlite3 binary against the file
    while the daemon is offline).

  * `verify_chain(conn)`: walks the chain from genesis and returns the
    first row whose stored `hash` does not match a recomputation. Used
    by the Charter integrity tripwire.

The triggers `audit_log_no_update` and `audit_log_no_delete` (declared
in `institute.db`) abort UPDATE and DELETE attempts at the engine
level. Combined with the hash chain, this gives two layers: engine
enforcement against the routine case (Python code accidentally
mutating audit_log), and hash detection against the adversarial case
(direct file access).
"""

from __future__ import annotations

import hashlib
import sqlite3
from dataclasses import dataclass


def _canonical(
    prev_hash: str | None,
    at: str | None,
    actor: str | None,
    action: str | None,
    project_id: str | None,
    detail: str | None,
) -> str:
    """Produce a stable string for hashing.

    Uses ASCII unit-separator (\\x1f) to delimit fields, which keeps
    newlines and dollar signs in `detail` from colliding with the
    separator. Missing values normalize to the empty string so two
    rows that differ only in NULL vs '' don't share a hash.
    """
    return "\x1f".join(
        [
            prev_hash or "",
            at or "",
            actor or "",
            action or "",
            project_id or "",
            detail or "",
        ]
    )


def _hash(
    prev_hash: str | None,
    at: str | None,
    actor: str | None,
    action: str | None,
    project_id: str | None,
    detail: str | None,
) -> str:
    return hashlib.sha256(
        _canonical(prev_hash, at, actor, action, project_id, detail).encode("utf-8")
    ).hexdigest()


def append(
    conn: sqlite3.Connection,
    *,
    at: str,
    actor: str,
    action: str,
    project_id: str | None = None,
    detail: str | None = None,
) -> int:
    """Append a new row to audit_log and return its rowid.

    The caller must hold the same connection (so the chain reads see
    the latest row) but no explicit transaction is required — a
    single INSERT is atomic on its own. Callers already inside a
    transaction (e.g. `decisions.record`) get the row included in
    their transaction's commit.
    """
    last = conn.execute(
        "SELECT hash FROM audit_log ORDER BY id DESC LIMIT 1"
    ).fetchone()
    prev = (last["hash"] if last and last["hash"] is not None else "") if last else ""
    h = _hash(prev, at, actor, action, project_id, detail)
    cur = conn.execute(
        "INSERT INTO audit_log "
        "(at, actor, action, project_id, detail, prev_hash, hash) "
        "VALUES (?, ?, ?, ?, ?, ?, ?)",
        (at, actor, action, project_id, detail, prev, h),
    )
    return cur.lastrowid or 0


@dataclass(frozen=True)
class ChainBreak:
    """Information about the first row whose hash doesn't validate."""

    row_id: int
    expected_hash: str
    stored_hash: str | None


def verify_chain(conn: sqlite3.Connection) -> ChainBreak | None:
    """Recompute the hash chain from genesis. Returns None if the
    entire log validates, otherwise the first row that fails.

    Legacy rows whose `hash` is NULL are tolerated as long as they
    appear at the head of the log (i.e. before any hashed row): the
    chain then starts from the first hashed row's `prev_hash`. A
    NULL hash in the middle of a hashed sequence is a chain break.
    """
    prev = ""
    chain_started = False
    for row in conn.execute(
        "SELECT id, at, actor, action, project_id, detail, prev_hash, hash "
        "FROM audit_log ORDER BY id"
    ):
        if row["hash"] is None:
            if chain_started:
                return ChainBreak(
                    row_id=row["id"],
                    expected_hash=_hash(
                        prev,
                        row["at"],
                        row["actor"],
                        row["action"],
                        row["project_id"],
                        row["detail"],
                    ),
                    stored_hash=None,
                )
            # Legacy unhashed prefix — accept and move on.
            continue

        if not chain_started:
            chain_started = True

        expected = _hash(
            prev,
            row["at"],
            row["actor"],
            row["action"],
            row["project_id"],
            row["detail"],
        )
        # If the row records its own prev_hash, that must also match.
        if row["prev_hash"] is not None and row["prev_hash"] != prev:
            return ChainBreak(
                row_id=row["id"],
                expected_hash=expected,
                stored_hash=row["hash"],
            )
        if row["hash"] != expected:
            return ChainBreak(
                row_id=row["id"],
                expected_hash=expected,
                stored_hash=row["hash"],
            )
        prev = row["hash"]

    return None
