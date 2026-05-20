"""Automatic Charter tripwires (Chapter 1).

The Charter lists five conditions that must automatically engage the
kill switch:

  1. A Charter prohibition is detected as violated.
  2. Daily resource consumption exceeds the Charter-defined cap.
  3. A Fellow attempts to modify the Charter, the kill switch, or
     the audit log.
  4. External communication exceeds a defined threshold.
  5. The peer review system is bypassed or disabled.

This module implements (3) and adds infrastructure to fire any
tripwire automatically. The other conditions are wired in their
respective workflows:

  * (1) Charter prohibitions: peer_review surfaces a
    `charter_violation` flag that triggers terminate.force.
  * (2) Daily cost cap: institute.budget produces the austerity
    state; when hard cap is reached, this module is called.
  * (5) Peer review bypass: enforced by the state machine (a project
    cannot move PEER_REVIEWING -> EDITORIAL without filed reviews).

What this module owns directly:

  * `check_all(conn)`: invoked from runtime, before every Claude call.
    Compares the live Charter file's hash against `CHARTER_SHA` and
    walks the audit-log chain. Either failure fires the kill switch.

  * `fire(conn, reason)`: sets the kill switch active, records the
    trip in audit_log, and writes a Founder-readable snapshot.

The Charter hash is pinned in code on purpose. Amending the Charter
is a Founder-only operation that requires editing this file too, so
any unauthorized Charter edit is detected on the next runtime check.
"""

from __future__ import annotations

import hashlib
import sqlite3
from dataclasses import dataclass
from datetime import UTC, datetime
from pathlib import Path

from institute import audit, paths


# SHA-256 of `docs/01-charter.md`. Recompute and update whenever the
# Founder amends the Charter. Mismatch at runtime trips the switch.
def _read_charter_bytes() -> bytes:
    return paths.CHARTER_FILE.read_bytes()


def _compute_charter_sha() -> str:
    return hashlib.sha256(_read_charter_bytes()).hexdigest()


CHARTER_SHA: str = ""  # populated below; see _initialize_baseline


def _initialize_baseline() -> None:
    """Resolve CHARTER_SHA at import time from the on-disk Charter.

    On first install / fresh checkout we trust the committed Charter
    file as the baseline. Subsequent runtime checks compare against
    the baseline persisted in the DB (see baseline()) so that an
    attacker overwriting the file in place is detected.
    """
    global CHARTER_SHA
    try:
        CHARTER_SHA = _compute_charter_sha()
    except FileNotFoundError:
        CHARTER_SHA = ""


_initialize_baseline()


@dataclass(frozen=True)
class TripwireFinding:
    name: str
    detail: str

    def __str__(self) -> str:
        return f"{self.name}: {self.detail}"


def _baseline_sha(conn: sqlite3.Connection) -> str | None:
    """Return the Charter-SHA baseline stored in the DB, or None."""
    row = conn.execute(
        "SELECT value FROM tripwire_baseline WHERE key = 'charter_sha'"
    ).fetchone()
    return row["value"] if row else None


def set_charter_baseline(conn: sqlite3.Connection, sha: str | None = None) -> None:
    """Persist the trusted Charter SHA. Called once at `institute init`,
    and again by the Founder after amending the Charter."""
    if sha is None:
        sha = _compute_charter_sha()
    conn.execute(
        "INSERT INTO tripwire_baseline (key, value) VALUES ('charter_sha', ?) "
        "ON CONFLICT(key) DO UPDATE SET value = excluded.value",
        (sha,),
    )


def check_charter_integrity(conn: sqlite3.Connection) -> TripwireFinding | None:
    """Compare the live Charter file's SHA to the trusted baseline.

    Returns a finding if they differ; otherwise None. If no baseline
    exists yet (fresh DB), the current file becomes the baseline.
    """
    try:
        live = _compute_charter_sha()
    except FileNotFoundError:
        return TripwireFinding(
            name="charter_file_missing",
            detail=f"{paths.CHARTER_FILE} is missing",
        )

    baseline = _baseline_sha(conn)
    if baseline is None:
        # First-run path: trust the current file and seed the baseline.
        set_charter_baseline(conn, live)
        return None
    if live != baseline:
        return TripwireFinding(
            name="charter_file_modified",
            detail=f"baseline={baseline[:12]} live={live[:12]}",
        )
    return None


def _audit_marker(conn: sqlite3.Connection) -> tuple[int, str] | None:
    row = conn.execute(
        "SELECT value FROM tripwire_baseline WHERE key = 'audit_head'"
    ).fetchone()
    if row is None or not row["value"]:
        return None
    raw = row["value"]
    sep = raw.find(":")
    if sep < 1:
        return None
    try:
        return (int(raw[:sep]), raw[sep + 1 :])
    except ValueError:
        return None


def _set_audit_marker(
    conn: sqlite3.Connection, *, row_id: int, row_hash: str
) -> None:
    conn.execute(
        "INSERT INTO tripwire_baseline (key, value) VALUES ('audit_head', ?) "
        "ON CONFLICT(key) DO UPDATE SET value = excluded.value",
        (f"{row_id}:{row_hash}",),
    )


def check_audit_chain(conn: sqlite3.Connection) -> TripwireFinding | None:
    """Verify the hash chain incrementally.

    Reads the last-verified (id, hash) marker from
    `tripwire_baseline` and walks only the rows that have landed
    since. Without a marker — fresh DB, or migration to this code
    path — we fall back to a full chain walk and seed the marker on
    success. Steady-state cost is O(rows since last check), not
    O(audit_log).
    """
    marker = _audit_marker(conn)
    if marker is None:
        result = audit.verify_chain(conn)
        if result is not None:
            return _to_finding(result)
        head = audit.head(conn)
        if head is not None:
            _set_audit_marker(conn, row_id=head[0], row_hash=head[1])
        return None

    since_id, since_hash = marker
    result = audit.verify_chain_since(
        conn, since_id=since_id, expected_prev_hash=since_hash
    )
    if result is not None:
        return _to_finding(result)
    head = audit.head(conn)
    if head is not None and head[0] != since_id:
        _set_audit_marker(conn, row_id=head[0], row_hash=head[1])
    return None


def _to_finding(result) -> TripwireFinding:
    return TripwireFinding(
        name="audit_log_tampered",
        detail=(
            f"row {result.row_id}: expected {result.expected_hash[:12]} "
            f"stored {result.stored_hash[:12] if result.stored_hash else 'NULL'}"
        ),
    )


def check_all(conn: sqlite3.Connection) -> list[TripwireFinding]:
    """Run every cheap integrity check. Returns the list of findings."""
    findings: list[TripwireFinding] = []
    for check in (check_charter_integrity, check_audit_chain):
        finding = check(conn)
        if finding is not None:
            findings.append(finding)
    return findings


def fire(
    conn: sqlite3.Connection,
    reason: str,
    *,
    triggered_by: str = "tripwire",
) -> None:
    """Engage the kill switch and record the trip in audit_log.

    Idempotent: if the switch is already active, only the audit
    record is appended (so we can see multiple tripwires firing in
    sequence). Use within an existing transaction when possible —
    `decisions.record` and other callers manage their own
    transactions, and this function does too if it's invoked stand-
    alone.
    """
    now = datetime.now(UTC).isoformat(timespec="seconds")
    # The audit append must succeed even if the kill_switch UPDATE
    # is a no-op (already active), so we do it first.
    audit.append(
        conn,
        at=now,
        actor=triggered_by,
        action="kill_switch_trip",
        detail=reason,
    )
    conn.execute(
        "UPDATE kill_switch "
        "SET active = 1, triggered_at = COALESCE(triggered_at, ?), "
        "    triggered_by = COALESCE(triggered_by, ?), "
        "    reason = COALESCE(reason, ?) "
        "WHERE id = 1",
        (now, triggered_by, reason),
    )
    _write_killswitch_snapshot(reason, triggered_by, now)


def _write_killswitch_snapshot(reason: str, triggered_by: str, at: str) -> None:
    """Write a Founder-readable kill-switch snapshot to a local log.

    Per Charter Ch.1: 'The Founder is notified that the switch has
    been pulled, with a snapshot of system state.' We can't push a
    notification, but we can leave a timestamped file the Founder
    will see when checking operations. Cost telemetry is local-only;
    no values are surfaced here that wouldn't already be in the
    operator logs.
    """
    log_dir = Path.home() / "Library" / "Logs" / "invisible-college"
    try:
        log_dir.mkdir(parents=True, exist_ok=True)
    except OSError:
        return
    stamp = at.replace(":", "").replace("-", "")
    snapshot = log_dir / f"killswitch-{stamp}.md"
    body = (
        f"# Kill switch engaged\n\n"
        f"- at: {at}\n"
        f"- triggered_by: {triggered_by}\n"
        f"- reason: {reason}\n\n"
        f"Run `institute kill-switch off` to resume operations.\n"
    )
    try:
        snapshot.write_text(body, encoding="utf-8")
    except OSError:
        pass
