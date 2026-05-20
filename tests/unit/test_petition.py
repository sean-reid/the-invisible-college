"""Tests for the petition workflow (author appeal on unanimous reject)."""

from __future__ import annotations

from datetime import UTC, datetime
from pathlib import Path

import pytest

from institute import db, decisions, paths
from institute import fellow as fellow_mod
from institute.fellow import Genome
from institute.state import State
from institute.workflows import petition


@pytest.fixture()
def isolated(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> Path:
    monkeypatch.setattr(paths, "ROOT", tmp_path)
    monkeypatch.setattr(paths, "ARCHIVE", tmp_path / "archive")
    monkeypatch.setattr(paths, "DECISIONS", tmp_path / "archive" / "decisions")
    monkeypatch.setattr(decisions, "DECISIONS", tmp_path / "archive" / "decisions")
    monkeypatch.setattr(fellow_mod, "GENOMES", tmp_path / "genomes")
    monkeypatch.setattr(fellow_mod, "FELLOWS", tmp_path / "fellows")
    (tmp_path / "genomes").mkdir()
    db_path = tmp_path / "institute.db"
    monkeypatch.setattr(db, "DB_PATH", db_path)
    db.initialize(db_path)
    return tmp_path


def _register(conn, fellow_id: str) -> None:
    g = Genome(
        id=fellow_id,
        name=fellow_id.capitalize(),
        rank="fellow",
        model="claude-sonnet-4-6",
        specialization="general",
        system_prompt_addendum=("body " * 60).strip(),
        allowed_tools=["Read"],
    )
    g.write(fellow_mod.genome_path(fellow_id))
    fellow_mod.register(conn, g)


def _seed_project(state: str, recommendations: list[str]) -> str:
    """Seed a project with `len(recommendations)` filed reviews in round 1."""
    pid = "proj-1"
    now = datetime.now(UTC).isoformat(timespec="seconds")
    with db.connection() as conn, db.transaction(conn):
        _register(conn, "ada")
        _register(conn, "henri")
        _register(conn, "michel")
        _register(conn, "lead")
        conn.execute(
            "INSERT INTO projects "
            "(id, title, state, lead_fellow_id, review_round, created_at, updated_at) "
            "VALUES (?, ?, ?, ?, ?, ?, ?)",
            (pid, "Some piece", state, "lead", 1, now, now),
        )
        for i, rec in enumerate(recommendations):
            reviewer = ["ada", "henri", "michel"][i]
            conn.execute(
                "INSERT INTO reviews "
                "(id, project_id, reviewer_id, role, recommendation, confidence, "
                " content_path, submitted_at, round) "
                "VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)",
                (
                    f"{pid}-{reviewer}-r1",
                    pid,
                    reviewer,
                    "primary" if i == 0 else "secondary",
                    rec,
                    "moderate",
                    f"archive/reviews/{pid}/review-by-{reviewer}.md",
                    now,
                    1,
                ),
            )
    return pid


def test_petition_advances_unanimous_reject_to_editorial(isolated: Path) -> None:
    pid = _seed_project(State.REJECTED.value, ["reject", "reject", "reject"])
    petition.run(pid, reason="Reviewers conflated two distinct concerns.")
    with db.connection() as conn:
        s = conn.execute("SELECT state FROM projects WHERE id = ?", (pid,)).fetchone()["state"]
    assert s == State.EDITORIAL_REVIEW.value


def test_petition_refuses_non_rejected(isolated: Path) -> None:
    pid = _seed_project(State.EDITORIAL.value, ["reject", "reject", "reject"])
    with pytest.raises(petition.NotPetitionable, match="not rejected"):
        petition.run(pid, reason="x")


def test_petition_refuses_non_unanimous_reject(isolated: Path) -> None:
    pid = _seed_project(State.REJECTED.value, ["reject", "reject", "minor"])
    with pytest.raises(petition.NotPetitionable, match="unanimous"):
        petition.run(pid, reason="x")


def test_petition_requires_reason(isolated: Path) -> None:
    pid = _seed_project(State.REJECTED.value, ["reject", "reject", "reject"])
    with pytest.raises(petition.NotPetitionable, match="non-empty"):
        petition.run(pid, reason="   ")


def test_petition_records_audit_entry(isolated: Path) -> None:
    pid = _seed_project(State.REJECTED.value, ["reject", "reject", "reject"])
    petition.run(pid, reason="ok")
    with db.connection() as conn:
        n = conn.execute(
            "SELECT COUNT(*) FROM audit_log WHERE action = 'editorial_petition'"
        ).fetchone()[0]
    assert n == 1
