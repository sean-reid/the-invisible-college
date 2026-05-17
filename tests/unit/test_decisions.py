"""Tests for the institutional decisions log."""

from pathlib import Path

import pytest

from institute import db, decisions


@pytest.fixture()
def isolated(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> Path:
    archive = tmp_path / "archive"
    archive.mkdir()
    decisions_dir = archive / "decisions"
    decisions_dir.mkdir()
    db_path = tmp_path / "institute.db"
    monkeypatch.setattr(decisions, "DECISIONS", decisions_dir)
    monkeypatch.setattr(db, "DB_PATH", db_path)
    db.initialize(db_path)
    return decisions_dir


def test_record_writes_markdown_with_frontmatter(isolated: Path) -> None:
    d = decisions.Decision(
        kind="bootstrap",
        title="Founding cohort",
        body="Four Fellows admitted.",
        actors=["founder", "orchestrator"],
    )

    with db.connection() as conn, db.transaction(conn):
        path = decisions.record(conn, d)

    text = path.read_text(encoding="utf-8")
    assert text.startswith("---\n")
    assert "kind: bootstrap" in text
    assert "actors: [founder, orchestrator]" in text
    assert "# Founding cohort" in text
    assert "Four Fellows admitted." in text


def test_record_inserts_audit_row(isolated: Path) -> None:
    d = decisions.Decision(
        kind="promotion",
        title="Hypatia to Senior Fellow",
        body="Approved unanimously.",
        actors=["tenure-committee"],
        related_project=None,
    )

    with db.connection() as conn, db.transaction(conn):
        decisions.record(conn, d)

    with db.connection() as conn:
        rows = list(conn.execute("SELECT action, actor FROM audit_log"))
        assert len(rows) == 1
        assert rows[0]["action"] == "promotion"
        assert rows[0]["actor"] == "tenure-committee"


def test_record_uniquifies_path(isolated: Path) -> None:
    d = decisions.Decision(
        kind="note",
        title="A duplicate title",
        body="x",
        actors=["a"],
    )
    with db.connection() as conn, db.transaction(conn):
        first = decisions.record(conn, d)
        second = decisions.record(conn, d)
    assert first != second
    assert first.exists() and second.exists()


def test_slugify_handles_special_chars() -> None:
    assert decisions._slugify("Hello, World!") == "hello-world"
    assert decisions._slugify("Hyphens---collapse") == "hyphens-collapse"
    assert decisions._slugify("") == "untitled"
    assert decisions._slugify("   ") == "untitled"
