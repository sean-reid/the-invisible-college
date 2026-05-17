"""Tests for the SQLite layer."""

from pathlib import Path

import pytest

from institute import db


@pytest.fixture()
def temp_db(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> Path:
    path = tmp_path / "institute.db"
    monkeypatch.setattr(db, "DB_PATH", path)
    db.initialize(path)
    return path


def test_initialize_is_idempotent(tmp_path: Path) -> None:
    path = tmp_path / "x.db"
    db.initialize(path)
    db.initialize(path)
    db.initialize(path)
    with db.connection(path) as conn:
        version = conn.execute("SELECT version FROM schema_version").fetchone()
        assert version["version"] == db.SCHEMA_VERSION


def test_kill_switch_row_is_seeded(temp_db: Path) -> None:
    with db.connection(temp_db) as conn:
        row = conn.execute("SELECT * FROM kill_switch WHERE id = 1").fetchone()
        assert row is not None
        assert row["active"] == 0


def test_transaction_commits_on_success(temp_db: Path) -> None:
    with db.connection(temp_db) as conn, db.transaction(conn):
        conn.execute(
            "INSERT INTO fellows "
            "(id, name, rank, model, specialization, genome_path, created_at) "
            "VALUES (?, ?, ?, ?, ?, ?, ?)",
            (
                "hypatia",
                "Hypatia",
                "fellow",
                "opus",
                "applied-demos",
                "/tmp/h.json",
                "2026-01-01T00:00:00",
            ),
        )

    with db.connection(temp_db) as conn:
        row = conn.execute("SELECT id FROM fellows WHERE id = 'hypatia'").fetchone()
        assert row is not None


def test_transaction_rolls_back_on_error(temp_db: Path) -> None:
    with pytest.raises(RuntimeError):
        with db.connection(temp_db) as conn, db.transaction(conn):
            conn.execute(
                "INSERT INTO fellows "
                "(id, name, rank, model, specialization, genome_path, created_at) "
                "VALUES (?, ?, ?, ?, ?, ?, ?)",
                ("d", "D", "fellow", "opus", "x", "/tmp/d.json", "2026-01-01T00:00:00"),
            )
            raise RuntimeError("simulated failure")

    with db.connection(temp_db) as conn:
        row = conn.execute("SELECT id FROM fellows WHERE id = 'd'").fetchone()
        assert row is None


def test_foreign_keys_are_enforced(temp_db: Path) -> None:
    import sqlite3

    with (
        pytest.raises(sqlite3.IntegrityError),
        db.connection(temp_db) as conn,
        db.transaction(conn),
    ):
        # No such fellow exists; this should fail with a foreign key violation.
        conn.execute(
            "INSERT INTO projects "
            "(id, title, state, lead_fellow_id, created_at, updated_at) "
            "VALUES (?, ?, ?, ?, ?, ?)",
            ("proj-1", "x", "proposed", "ghost", "2026-01-01", "2026-01-01"),
        )


def test_connection_errors_when_uninitialized(tmp_path: Path) -> None:
    missing = tmp_path / "missing.db"
    with pytest.raises(RuntimeError, match="not initialized"):
        with db.connection(missing):
            pass
