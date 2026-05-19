"""Tests for the targeted Charter-violation termination workflow."""

from __future__ import annotations

from datetime import UTC, datetime
from pathlib import Path

import pytest

from institute import db, decisions, paths, workspaces
from institute import fellow as fellow_mod
from institute.fellow import Genome
from institute.workflows import terminate


@pytest.fixture()
def isolated(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> Path:
    genomes = tmp_path / "genomes"
    fellows = tmp_path / "fellows"
    archive = tmp_path / "archive"
    decisions_dir = archive / "decisions"
    for d in (genomes, fellows, decisions_dir):
        d.mkdir(parents=True)
    db_path = tmp_path / "institute.db"

    monkeypatch.setattr(db, "DB_PATH", db_path)
    monkeypatch.setattr(decisions, "DECISIONS", decisions_dir)
    monkeypatch.setattr(paths, "GENOMES", genomes)
    monkeypatch.setattr(paths, "FELLOWS", fellows)
    monkeypatch.setattr(paths, "ARCHIVE", archive)
    monkeypatch.setattr(paths, "ROOT", tmp_path)
    monkeypatch.setattr(fellow_mod, "GENOMES", genomes)
    monkeypatch.setattr(fellow_mod, "FELLOWS", fellows)
    monkeypatch.setattr(workspaces, "FELLOWS", fellows)
    db.initialize(db_path)
    return tmp_path


def _genome(fid: str, name: str, rank: str = "fellow") -> Genome:
    return Genome(
        id=fid,
        name=name,
        rank=rank,
        model="claude-sonnet-4-6",
        specialization=f"spec-{fid}",
        system_prompt_addendum=("body " * 60).strip(),
        allowed_tools=["Read"],
    )


def _seed(conn, g: Genome) -> None:
    g.write(fellow_mod.genome_path(g.id))
    fellow_mod.register(conn, g)


def _seed_project(conn, project_id: str, lead: str, state: str) -> None:
    now = datetime.now(UTC).isoformat(timespec="seconds")
    conn.execute(
        "INSERT INTO projects (id, title, state, lead_fellow_id, review_round, "
        " created_at, updated_at) VALUES (?, ?, ?, ?, 1, ?, ?)",
        (project_id, f"Title {project_id}", state, lead, now, now),
    )


# ---------------------------------------------------------------------------
# Validation
# ---------------------------------------------------------------------------


def test_run_rejects_unknown_violation_kind(isolated: Path) -> None:
    with db.connection() as conn, db.transaction(conn):
        _seed(conn, _genome("bad", "Bad"))
    with pytest.raises(ValueError, match="Unknown violation kind"):
        terminate.run("bad", kind="made-up", reason="x")


def test_run_rejects_empty_reason(isolated: Path) -> None:
    with db.connection() as conn, db.transaction(conn):
        _seed(conn, _genome("bad", "Bad"))
    with pytest.raises(ValueError, match="reason must be non-empty"):
        terminate.run("bad", kind="deception", reason="   ")


def test_run_returns_false_for_unknown_fellow(isolated: Path) -> None:
    assert terminate.run("nobody", kind="deception", reason="x") is False, (
        "Unknown fellow must return False, not raise"
    )


def test_run_returns_false_for_already_retired(isolated: Path) -> None:
    with db.connection() as conn, db.transaction(conn):
        _seed(conn, _genome("ada", "Ada"))
        conn.execute(
            "UPDATE fellows SET retired_at = ? WHERE id = 'ada'",
            (datetime.now(UTC).isoformat(timespec="seconds"),),
        )
    assert terminate.run("ada", kind="deception", reason="x") is False


# ---------------------------------------------------------------------------
# Effects
# ---------------------------------------------------------------------------


def test_run_sets_retired_at(isolated: Path) -> None:
    with db.connection() as conn, db.transaction(conn):
        _seed(conn, _genome("ada", "Ada"))
    assert terminate.run("ada", kind="plagiarism", reason="cited fabricated source") is True
    with db.connection() as conn:
        row = conn.execute("SELECT retired_at FROM fellows WHERE id = 'ada'").fetchone()
    assert row["retired_at"] is not None


def test_run_discards_in_flight_projects(isolated: Path) -> None:
    with db.connection() as conn, db.transaction(conn):
        _seed(conn, _genome("ada", "Ada"))
        _seed_project(conn, "proj-published", "ada", "published")
        _seed_project(conn, "proj-researching", "ada", "researching")
        _seed_project(conn, "proj-drafted", "ada", "drafted")
    assert terminate.run("ada", kind="deception", reason="fabricated experiment") is True
    with db.connection() as conn:
        rows = {
            r["id"]: r["state"]
            for r in conn.execute("SELECT id, state FROM projects WHERE lead_fellow_id = 'ada'")
        }
    # Published work survives; in-flight is rejected.
    assert rows["proj-published"] == "published"
    assert rows["proj-researching"] == "rejected"
    assert rows["proj-drafted"] == "rejected"


def test_run_writes_charter_violation_decision(isolated: Path) -> None:
    with db.connection() as conn, db.transaction(conn):
        _seed(conn, _genome("ada", "Ada"))
    terminate.run("ada", kind="harm", reason="article proposed dual-use payload synthesis")
    with db.connection() as conn:
        rows = list(
            conn.execute(
                "SELECT action FROM audit_log WHERE action = 'charter_violation_termination'"
            )
        )
    assert len(rows) == 1


def test_terminated_fellow_drops_out_of_active_queries(isolated: Path) -> None:
    """A standard 'active fellows' query must exclude terminated Fellows."""
    with db.connection() as conn, db.transaction(conn):
        _seed(conn, _genome("active", "Active"))
        _seed(conn, _genome("bad", "Bad"))
    terminate.run("bad", kind="deception", reason="fabricated quotes")
    with db.connection() as conn:
        ids = {r["id"] for r in conn.execute("SELECT id FROM fellows WHERE retired_at IS NULL")}
    assert ids == {"active"}, "Terminated Fellow must drop out of active queries"


def test_decision_body_includes_disclosure_clause(isolated: Path) -> None:
    body = terminate._format_decision_body(
        fellow_id="ada",
        fellow_name="Ada",
        rank="fellow",
        kind="plagiarism",
        reason="cited a paper that does not exist",
        in_flight=[],
        now="2026-05-19T00:00:00+00:00",
        triggered_by="founder",
        related_project=None,
    )
    assert "plagiarism" in body
    assert "Disclosure" in body
    assert "Charter-violation disclosure banner" in body


def test_decision_body_lists_discarded_projects() -> None:
    body = terminate._format_decision_body(
        fellow_id="ada",
        fellow_name="Ada",
        rank="fellow",
        kind="deception",
        reason="fabricated experiment",
        in_flight=[
            {"id": "proj-a", "title": "Title A", "state": "researching"},
            {"id": "proj-b", "title": "Title B", "state": "drafted"},
        ],
        now="2026-05-19T00:00:00+00:00",
        triggered_by="founder",
        related_project="proj-a",
    )
    assert "## In-flight projects discarded" in body
    assert "`proj-a`" in body
    assert "`proj-b`" in body
    assert "**Originating project:** `proj-a`" in body
