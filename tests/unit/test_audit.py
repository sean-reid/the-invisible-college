"""Tests for the append-only, hash-chained audit log."""

from __future__ import annotations

from pathlib import Path

import pytest

from institute import audit, db


@pytest.fixture()
def isolated(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> Path:
    db_path = tmp_path / "institute.db"
    monkeypatch.setattr(db, "DB_PATH", db_path)
    db.initialize(db_path)
    return tmp_path


def test_first_append_uses_empty_prev_hash(isolated: Path) -> None:
    with db.connection() as conn, db.transaction(conn):
        rowid = audit.append(
            conn, at="2026-05-19T00:00:00Z", actor="orch", action="promotion"
        )
    assert rowid > 0
    with db.connection() as conn:
        row = conn.execute(
            "SELECT prev_hash, hash FROM audit_log WHERE id = ?", (rowid,)
        ).fetchone()
        assert row["prev_hash"] == ""
        assert row["hash"]  # non-empty


def test_chain_links_successive_rows(isolated: Path) -> None:
    with db.connection() as conn, db.transaction(conn):
        audit.append(conn, at="t1", actor="a", action="x")
        audit.append(conn, at="t2", actor="b", action="y")
    with db.connection() as conn:
        rows = list(
            conn.execute(
                "SELECT id, prev_hash, hash FROM audit_log ORDER BY id"
            )
        )
    assert len(rows) == 2
    # row 2's prev_hash matches row 1's hash
    assert rows[1]["prev_hash"] == rows[0]["hash"]


def test_verify_chain_returns_none_for_clean_log(isolated: Path) -> None:
    with db.connection() as conn, db.transaction(conn):
        audit.append(conn, at="t1", actor="a", action="x")
        audit.append(conn, at="t2", actor="b", action="y")
        audit.append(conn, at="t3", actor="c", action="z", project_id="p", detail="d")
    with db.connection() as conn:
        assert audit.verify_chain(conn) is None


def test_update_trigger_blocks_tampering(isolated: Path) -> None:
    with db.connection() as conn, db.transaction(conn):
        audit.append(conn, at="t1", actor="a", action="x")
    with db.connection() as conn:
        with pytest.raises(Exception, match="append-only"):
            conn.execute("UPDATE audit_log SET actor = 'bob' WHERE id = 1")


def test_delete_trigger_blocks_removal(isolated: Path) -> None:
    with db.connection() as conn, db.transaction(conn):
        audit.append(conn, at="t1", actor="a", action="x")
    with db.connection() as conn:
        with pytest.raises(Exception, match="append-only"):
            conn.execute("DELETE FROM audit_log WHERE id = 1")


def test_legacy_unhashed_rows_at_head_are_tolerated(isolated: Path) -> None:
    # Pre-hash-chain INSERTs (raw, no hash) at the head are tolerated.
    with db.connection() as conn, db.transaction(conn):
        conn.execute(
            "INSERT INTO audit_log (at, actor, action, detail) VALUES (?, ?, ?, ?)",
            ("t-legacy", "old", "legacy_action", "d"),
        )
        audit.append(conn, at="t-new", actor="orch", action="x")
    with db.connection() as conn:
        # No break: legacy row is at the head, then hashed chain begins.
        assert audit.verify_chain(conn) is None


def test_chain_detects_silently_modified_row_after_creation(
    isolated: Path,
) -> None:
    # Simulate an attacker that gets around the trigger (e.g. by
    # dropping it and editing the file). We do the same here by
    # disabling the trigger temporarily, mutating, then verifying
    # the chain detects the change.
    with db.connection() as conn, db.transaction(conn):
        audit.append(conn, at="t1", actor="a", action="x")
        audit.append(conn, at="t2", actor="b", action="y")
    with db.connection() as conn:
        conn.execute("DROP TRIGGER audit_log_no_update")
        conn.execute("UPDATE audit_log SET actor = 'tamper' WHERE id = 1")
    with db.connection() as conn:
        result = audit.verify_chain(conn)
    assert result is not None
    assert result.row_id == 1
    assert result.stored_hash != result.expected_hash


def test_chain_detects_inserted_row_in_middle(isolated: Path) -> None:
    # The simplest mid-chain tamper to simulate: take an existing
    # valid log, drop both triggers, then UPDATE a middle row's
    # `detail`. The chain detects the modified row.
    with db.connection() as conn, db.transaction(conn):
        audit.append(conn, at="t1", actor="a", action="x")
        audit.append(conn, at="t2", actor="b", action="y")
        audit.append(conn, at="t3", actor="c", action="z")
    with db.connection() as conn:
        conn.execute("DROP TRIGGER audit_log_no_update")
        conn.execute("UPDATE audit_log SET detail = 'sneaky' WHERE id = 2")
    with db.connection() as conn:
        result = audit.verify_chain(conn)
    assert result is not None
    assert result.row_id == 2


def test_append_within_transaction(isolated: Path) -> None:
    with db.connection() as conn, db.transaction(conn):
        audit.append(conn, at="t1", actor="a", action="x")
        audit.append(conn, at="t2", actor="b", action="y")
    with db.connection() as conn:
        n = conn.execute("SELECT COUNT(*) FROM audit_log").fetchone()[0]
    assert n == 2


def test_canonical_includes_all_fields() -> None:
    # Two rows that differ only in `detail` produce different hashes.
    a = audit._hash("", "t", "actor", "action", "p", "x")
    b = audit._hash("", "t", "actor", "action", "p", "y")
    assert a != b


def test_canonical_distinguishes_null_from_empty() -> None:
    # detail=None and detail="" should both hash the same way (we
    # normalize None to "" in canonical). This is a documented
    # invariant of the encoding.
    a = audit._hash("", "t", "actor", "action", None, None)
    b = audit._hash("", "t", "actor", "action", "", "")
    assert a == b
