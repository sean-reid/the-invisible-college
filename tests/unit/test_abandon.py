"""Tests for the abandon-with-honest-lesson workflow."""

from __future__ import annotations

from datetime import UTC, datetime
from pathlib import Path

import pytest

from institute import db, paths
from institute import fellow as fellow_mod
from institute.fellow import Genome
from institute.workflows import abandon


@pytest.fixture()
def isolated(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> Path:
    monkeypatch.setattr(paths, "ROOT", tmp_path)
    monkeypatch.setattr(paths, "ARCHIVE", tmp_path / "archive")
    monkeypatch.setattr(paths, "DECISIONS", tmp_path / "archive" / "decisions")
    monkeypatch.setattr(paths, "GENOMES", tmp_path / "genomes")
    monkeypatch.setattr(paths, "FELLOWS", tmp_path / "fellows")
    monkeypatch.setattr(
        abandon, "ABANDONMENT_DIR", tmp_path / "archive" / "abandonments"
    )
    monkeypatch.setattr(fellow_mod, "GENOMES", tmp_path / "genomes")
    monkeypatch.setattr(fellow_mod, "FELLOWS", tmp_path / "fellows")
    (tmp_path / "genomes").mkdir()
    db_path = tmp_path / "institute.db"
    monkeypatch.setattr(db, "DB_PATH", db_path)
    db.initialize(db_path)
    return tmp_path


def _seed_project_and_lead(state: str = "researching") -> str:
    genome = Genome(
        id="ada",
        name="Ada",
        rank="fellow",
        model="claude-sonnet-4-6",
        specialization="general",
        system_prompt_addendum=("body " * 60).strip(),
        allowed_tools=["Read"],
    )
    genome.write(fellow_mod.genome_path("ada"))
    with db.connection() as conn, db.transaction(conn):
        fellow_mod.register(conn, genome)
        now = datetime.now(UTC).isoformat(timespec="seconds")
        conn.execute(
            "INSERT INTO projects "
            "(id, title, state, lead_fellow_id, review_round, "
            " created_at, updated_at) "
            "VALUES (?, ?, ?, ?, 1, ?, ?)",
            ("proj-1", "A study", state, "ada", now, now),
        )
    return "proj-1"


def test_abandon_writes_lesson_and_transitions(isolated: Path) -> None:
    project_id = _seed_project_and_lead()
    abandon.run(
        project_id,
        reason="discovered the question is unanswerable as posed",
        lesson="Two days into the literature review I realized the operational "
        "definition of the construct conflates two effects that the existing "
        "instruments cannot separate. Continuing would have produced a "
        "result whose interpretation I could not defend.",
    )
    lesson_path = isolated / "archive" / "abandonments" / f"{project_id}.md"
    assert lesson_path.exists()
    text = lesson_path.read_text()
    assert "Honest lesson" in text
    assert "unanswerable" in text
    with db.connection() as conn:
        state = conn.execute(
            "SELECT state FROM projects WHERE id = ?", (project_id,)
        ).fetchone()["state"]
    assert state == "abandoned"


def test_abandon_requires_lesson(isolated: Path) -> None:
    project_id = _seed_project_and_lead()
    with pytest.raises(SystemExit, match="honest lesson"):
        abandon.run(project_id, reason="bored", lesson="   ")


def test_abandon_refuses_terminal_state(isolated: Path) -> None:
    project_id = _seed_project_and_lead(state="published")
    with pytest.raises(SystemExit, match="terminal state"):
        abandon.run(project_id, reason="x", lesson="x")


def test_abandon_records_decision(isolated: Path) -> None:
    project_id = _seed_project_and_lead()
    abandon.run(project_id, reason="r", lesson="A real lesson goes here.")
    with db.connection() as conn:
        n = conn.execute(
            "SELECT COUNT(*) FROM audit_log WHERE action = 'abandonment'"
        ).fetchone()[0]
    assert n == 1
