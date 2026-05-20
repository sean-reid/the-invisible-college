"""Tests for Charter integrity tripwires."""

from __future__ import annotations

from pathlib import Path

import pytest

from institute import audit, db, paths, tripwires


@pytest.fixture()
def isolated(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> Path:
    """Fresh DB with a controllable Charter file at a temp path."""
    charter = tmp_path / "01-charter.md"
    charter.write_text("# Charter\n\nMission text.\n", encoding="utf-8")
    monkeypatch.setattr(paths, "CHARTER_FILE", charter)

    db_path = tmp_path / "institute.db"
    monkeypatch.setattr(db, "DB_PATH", db_path)
    db.initialize(db_path)
    return tmp_path


def test_charter_check_seeds_baseline_on_first_run(isolated: Path) -> None:
    with db.connection() as conn, db.transaction(conn):
        finding = tripwires.check_charter_integrity(conn)
        assert finding is None
        # Baseline now persisted.
        row = conn.execute(
            "SELECT value FROM tripwire_baseline WHERE key = 'charter_sha'"
        ).fetchone()
        assert row is not None
        assert row["value"]


def test_charter_check_detects_modification(isolated: Path) -> None:
    # Seed baseline against the original file.
    with db.connection() as conn, db.transaction(conn):
        tripwires.check_charter_integrity(conn)
    # Now overwrite the Charter.
    paths.CHARTER_FILE.write_text("# Charter\n\n(maliciously altered)\n", encoding="utf-8")
    with db.connection() as conn, db.transaction(conn):
        finding = tripwires.check_charter_integrity(conn)
    assert finding is not None
    assert finding.name == "charter_file_modified"


def test_charter_check_handles_missing_file(isolated: Path) -> None:
    with db.connection() as conn, db.transaction(conn):
        tripwires.check_charter_integrity(conn)
    paths.CHARTER_FILE.unlink()
    with db.connection() as conn, db.transaction(conn):
        finding = tripwires.check_charter_integrity(conn)
    assert finding is not None
    assert finding.name == "charter_file_missing"


def test_audit_check_clean_log(isolated: Path) -> None:
    with db.connection() as conn, db.transaction(conn):
        audit.append(conn, at="t1", actor="a", action="x")
        audit.append(conn, at="t2", actor="b", action="y")
    with db.connection() as conn:
        assert tripwires.check_audit_chain(conn) is None


def test_audit_check_detects_tamper(isolated: Path) -> None:
    with db.connection() as conn, db.transaction(conn):
        audit.append(conn, at="t1", actor="a", action="x")
        audit.append(conn, at="t2", actor="b", action="y")
    with db.connection() as conn:
        conn.execute("DROP TRIGGER audit_log_no_update")
        conn.execute("UPDATE audit_log SET actor = 'tamper' WHERE id = 1")
    with db.connection() as conn:
        finding = tripwires.check_audit_chain(conn)
    assert finding is not None
    assert finding.name == "audit_log_tampered"


def test_fire_engages_kill_switch_and_records_audit(isolated: Path) -> None:
    with db.connection() as conn, db.transaction(conn):
        tripwires.fire(conn, reason="charter_file_modified: baseline=abc live=def")
    with db.connection() as conn:
        row = conn.execute(
            "SELECT active, reason, triggered_by FROM kill_switch WHERE id = 1"
        ).fetchone()
    assert row["active"] == 1
    assert "charter_file_modified" in row["reason"]
    assert row["triggered_by"] == "tripwire"
    with db.connection() as conn:
        n = conn.execute(
            "SELECT COUNT(*) FROM audit_log WHERE action = 'kill_switch_trip'"
        ).fetchone()[0]
    assert n == 1


def test_fire_is_idempotent(isolated: Path) -> None:
    with db.connection() as conn, db.transaction(conn):
        tripwires.fire(conn, reason="first")
    with db.connection() as conn, db.transaction(conn):
        tripwires.fire(conn, reason="second")
    with db.connection() as conn:
        row = conn.execute("SELECT reason FROM kill_switch WHERE id = 1").fetchone()
        # First trip's reason wins (COALESCE keeps earliest).
        assert row["reason"] == "first"
        # Both trips audited.
        n = conn.execute(
            "SELECT COUNT(*) FROM audit_log WHERE action = 'kill_switch_trip'"
        ).fetchone()[0]
    assert n == 2


def test_check_all_returns_all_findings(isolated: Path) -> None:
    # Set both tripwires off, then break each.
    with db.connection() as conn, db.transaction(conn):
        tripwires.check_charter_integrity(conn)
        audit.append(conn, at="t1", actor="a", action="x")
    paths.CHARTER_FILE.write_text("# Tampered\n", encoding="utf-8")
    with db.connection() as conn:
        conn.execute("DROP TRIGGER audit_log_no_update")
        conn.execute("UPDATE audit_log SET actor = 'tamper' WHERE id = 1")
    with db.connection() as conn, db.transaction(conn):
        findings = tripwires.check_all(conn)
    names = {f.name for f in findings}
    assert "charter_file_modified" in names
    assert "audit_log_tampered" in names


def test_set_charter_baseline_updates_existing_value(isolated: Path) -> None:
    with db.connection() as conn, db.transaction(conn):
        tripwires.set_charter_baseline(conn, sha="aaaa")
    with db.connection() as conn, db.transaction(conn):
        tripwires.set_charter_baseline(conn, sha="bbbb")
    with db.connection() as conn:
        row = conn.execute(
            "SELECT value FROM tripwire_baseline WHERE key = 'charter_sha'"
        ).fetchone()
    assert row["value"] == "bbbb"
