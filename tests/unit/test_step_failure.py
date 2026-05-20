"""Tests for graceful Fellow-invocation-failure handling in the autopilot loop.

A transient Claude CLI failure on one Fellow invocation should not
crash the whole daemon cycle. The loop catches `FellowInvocationError`,
records a `step_failure` decision, marks the project as failed for the
remainder of the cycle, and continues.
"""

from __future__ import annotations

from datetime import UTC, datetime
from pathlib import Path

import pytest

from institute import claude_runner, db, decisions, paths
from institute import fellow as fellow_mod
from institute.cli import _pick_in_flight_project, _record_step_failure
from institute.fellow import Genome


@pytest.fixture()
def isolated(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> Path:
    archive = tmp_path / "archive"
    decisions_dir = archive / "decisions"
    genomes = tmp_path / "genomes"
    fellows = tmp_path / "fellows"
    for d in (archive, decisions_dir, genomes, fellows):
        d.mkdir(parents=True)
    db_path = tmp_path / "institute.db"
    monkeypatch.setattr(db, "DB_PATH", db_path)
    monkeypatch.setattr(decisions, "DECISIONS", decisions_dir)
    monkeypatch.setattr(paths, "ROOT", tmp_path)
    monkeypatch.setattr(paths, "ARCHIVE", archive)
    monkeypatch.setattr(paths, "GENOMES", genomes)
    monkeypatch.setattr(paths, "FELLOWS", fellows)
    monkeypatch.setattr(fellow_mod, "GENOMES", genomes)
    monkeypatch.setattr(fellow_mod, "FELLOWS", fellows)
    db.initialize(db_path)

    # Seed one Fellow so projects can FK their lead_fellow_id.
    lead = Genome(
        id="lead-fellow",
        name="Lead",
        rank="fellow",
        model="claude-sonnet-4-6",
        specialization="theory",
        system_prompt_addendum=("body " * 60).strip(),
        allowed_tools=["Read"],
    )
    lead.write(fellow_mod.genome_path(lead.id))
    with db.connection() as conn, db.transaction(conn):
        fellow_mod.register(conn, lead)
    return tmp_path


def _seed_project(
    conn, project_id: str, state: str = "proposed", *, updated_at: str | None = None
) -> None:
    now = updated_at or datetime.now(UTC).isoformat(timespec="seconds")
    conn.execute(
        "INSERT INTO projects (id, title, state, lead_fellow_id, "
        "created_at, updated_at) VALUES (?, 't', ?, 'lead-fellow', ?, ?)",
        (project_id, state, now, now),
    )


# ---------------------------------------------------------------------------
# FellowInvocationError
# ---------------------------------------------------------------------------


def test_fellow_invocation_error_subclasses_runtime() -> None:
    """Existing `except RuntimeError` callers keep working."""
    exc = claude_runner.FellowInvocationError(
        fellow_id="ada",
        step="propose",
        project_id="p1",
        returncode=1,
        is_error=True,
        stderr="kaboom",
    )
    assert isinstance(exc, RuntimeError)
    assert exc.fellow_id == "ada"
    assert exc.step == "propose"
    assert exc.project_id == "p1"
    assert exc.returncode == 1
    assert "ada" in str(exc)
    assert "kaboom" in str(exc)


# ---------------------------------------------------------------------------
# _pick_in_flight_project exclude_ids
# ---------------------------------------------------------------------------


def test_pick_excludes_failed_project(isolated: Path) -> None:
    with db.connection() as conn, db.transaction(conn):
        _seed_project(conn, "p1", "proposed", updated_at="2026-05-20T01:00:00+00:00")
        _seed_project(conn, "p2", "proposed", updated_at="2026-05-20T02:00:00+00:00")

    # No exclusions: p1 (oldest updated_at) wins.
    row = _pick_in_flight_project(None)
    assert row["id"] == "p1"

    # Exclude p1: p2 is next.
    row = _pick_in_flight_project(None, exclude_ids={"p1"})
    assert row["id"] == "p2"

    # Exclude both: nothing.
    row = _pick_in_flight_project(None, exclude_ids={"p1", "p2"})
    assert row is None


def test_pick_named_project_respects_exclusion(isolated: Path) -> None:
    """When the operator names a specific project but it failed earlier
    this cycle, the picker returns None so the loop halts gracefully."""
    with db.connection() as conn, db.transaction(conn):
        _seed_project(conn, "p1", "proposed")

    assert _pick_in_flight_project("p1", exclude_ids={"p1"}) is None


def test_pick_skips_terminal_states(isolated: Path) -> None:
    """Sanity: published/rejected projects are never returned."""
    with db.connection() as conn, db.transaction(conn):
        _seed_project(conn, "live", "proposed")
        _seed_project(conn, "shipped", "published")
        _seed_project(conn, "killed", "rejected")

    row = _pick_in_flight_project(None)
    assert row["id"] == "live"


# ---------------------------------------------------------------------------
# _record_step_failure
# ---------------------------------------------------------------------------


def test_record_step_failure_writes_decision(isolated: Path) -> None:
    with db.connection() as conn, db.transaction(conn):
        _seed_project(conn, "p1", "peer_reviewing")

    _record_step_failure(
        project_id="p1",
        state="peer_reviewing",
        fellow_id="ibn-al-haytham",
        step="peer_review:secondary",
        returncode=1,
        stderr="some stderr text",
    )

    decision_files = sorted(p for p in decisions.DECISIONS.iterdir() if p.is_file())
    assert len(decision_files) == 1
    body = decision_files[0].read_text(encoding="utf-8")
    assert "kind: step_failure" in body
    assert "ibn-al-haytham" in body
    assert "peer_review:secondary" in body
    assert "Returncode:** 1" in body
    assert "some stderr text" in body


def test_record_step_failure_handles_empty_stderr(isolated: Path) -> None:
    with db.connection() as conn, db.transaction(conn):
        _seed_project(conn, "p1", "peer_reviewing")

    _record_step_failure(
        project_id="p1",
        state="peer_reviewing",
        fellow_id="ada",
        step="research",
        returncode=1,
        stderr="",
    )

    decision_files = sorted(p for p in decisions.DECISIONS.iterdir() if p.is_file())
    assert len(decision_files) == 1
    body = decision_files[0].read_text(encoding="utf-8")
    # Empty stderr does not emit the code-fenced section.
    assert "## stderr" not in body
