"""Tests for the autopilot circuit breaker.

When a project trips the same workflow-level failure repeatedly, the
autopilot must stop retrying so a deterministic loop (citation_lint
on a body it can't edit, etc.) does not burn budget indefinitely.
"""

from __future__ import annotations

from datetime import UTC, datetime
from pathlib import Path

from institute import autopilot, db
from institute import fellow as fellow_mod
from institute.fellow import Genome
from institute.state import State


def _genome(slug: str, name: str = "Lead") -> Genome:
    return Genome(
        id=slug,
        name=name,
        rank="fellow",
        model="claude-sonnet-4-6",
        specialization="general",
        system_prompt_addendum=("body " * 60).strip(),
        allowed_tools=["Read"],
    )


def _seed_project(project_id: str, state: str = "editorial") -> None:
    now = datetime.now(UTC).isoformat(timespec="seconds")
    lead = _genome("lead")
    with db.connection() as conn, db.transaction(conn):
        lead.write(fellow_mod.genome_path(lead.id))
        fellow_mod.register(conn, lead)
        conn.execute(
            "INSERT INTO projects "
            "(id, title, state, lead_fellow_id, draft_path, review_round, "
            " created_at, updated_at) "
            "VALUES (?, ?, ?, ?, ?, ?, ?, ?)",
            (project_id, "T", state, lead.id, "draft.md", 1, now, now),
        )


def _record_failures(project_id: str, actors: list[str]) -> None:
    """Append step_failure audit rows in order. `actors` is a list of
    actor strings (e.g. 'orchestrator,orchestrator' for workflow-level
    failures, 'orchestrator,lead' for Fellow-CLI failures)."""
    with db.connection() as conn, db.transaction(conn):
        for i, actor in enumerate(actors):
            at = f"2026-05-26T00:0{i}:00+00:00"
            conn.execute(
                "INSERT INTO audit_log (at, actor, action, project_id, detail) "
                "VALUES (?, ?, 'step_failure', ?, '')",
                (at, actor, project_id),
            )


def test_two_workflow_failures_trip_breaker(isolated: Path) -> None:
    _seed_project("p1")
    _record_failures("p1", ["orchestrator,orchestrator"] * 2)
    autopilot._maybe_circuit_break("p1")
    with db.connection() as conn:
        proj = conn.execute("SELECT state FROM projects WHERE id = 'p1'").fetchone()
    assert proj["state"] == State.ABANDONED.value


def test_one_workflow_failure_does_not_trip(isolated: Path) -> None:
    _seed_project("p2")
    _record_failures("p2", ["orchestrator,orchestrator"])
    autopilot._maybe_circuit_break("p2")
    with db.connection() as conn:
        proj = conn.execute("SELECT state FROM projects WHERE id = 'p2'").fetchone()
    assert proj["state"] == State.EDITORIAL.value


def test_four_fellow_failures_do_not_trip(isolated: Path) -> None:
    """Fellow-CLI failures are usually transient (network blip, model
    flake). Threshold is 5 — four in a row is still 'try once more.'"""
    _seed_project("p3")
    _record_failures("p3", ["orchestrator,lead"] * 4)
    autopilot._maybe_circuit_break("p3")
    with db.connection() as conn:
        proj = conn.execute("SELECT state FROM projects WHERE id = 'p3'").fetchone()
    assert proj["state"] == State.EDITORIAL.value


def test_five_fellow_failures_trip_breaker(isolated: Path) -> None:
    _seed_project("p4")
    _record_failures("p4", ["orchestrator,lead"] * 5)
    autopilot._maybe_circuit_break("p4")
    with db.connection() as conn:
        proj = conn.execute("SELECT state FROM projects WHERE id = 'p4'").fetchone()
    assert proj["state"] == State.ABANDONED.value


def test_non_failure_row_resets_streak(isolated: Path) -> None:
    """If a successful step (any non-step_failure audit action) is
    interleaved with failures, the streak ends. Two prior failures
    followed by a successful publication then one more failure must
    NOT trip the breaker (only one trailing failure)."""
    _seed_project("p5")
    with db.connection() as conn, db.transaction(conn):
        conn.execute(
            "INSERT INTO audit_log (at, actor, action, project_id, detail) "
            "VALUES ('2026-05-26T00:00:00+00:00', 'orchestrator,orchestrator', "
            "'step_failure', 'p5', '')"
        )
        conn.execute(
            "INSERT INTO audit_log (at, actor, action, project_id, detail) "
            "VALUES ('2026-05-26T00:01:00+00:00', 'orchestrator,orchestrator', "
            "'step_failure', 'p5', '')"
        )
        conn.execute(
            "INSERT INTO audit_log (at, actor, action, project_id, detail) "
            "VALUES ('2026-05-26T00:02:00+00:00', 'lead', 'revision', 'p5', '')"
        )
        conn.execute(
            "INSERT INTO audit_log (at, actor, action, project_id, detail) "
            "VALUES ('2026-05-26T00:03:00+00:00', 'orchestrator,orchestrator', "
            "'step_failure', 'p5', '')"
        )
    autopilot._maybe_circuit_break("p5")
    with db.connection() as conn:
        proj = conn.execute("SELECT state FROM projects WHERE id = 'p5'").fetchone()
    assert proj["state"] == State.EDITORIAL.value


def test_terminal_state_not_touched(isolated: Path) -> None:
    """A project already in PUBLISHED/REJECTED/etc. is never re-touched."""
    _seed_project("p6", state=State.PUBLISHED.value)
    _record_failures("p6", ["orchestrator,orchestrator"] * 3)
    autopilot._maybe_circuit_break("p6")
    with db.connection() as conn:
        proj = conn.execute("SELECT state FROM projects WHERE id = 'p6'").fetchone()
    assert proj["state"] == State.PUBLISHED.value


def test_circuit_breaker_records_decision(isolated: Path) -> None:
    _seed_project("p7")
    _record_failures("p7", ["orchestrator,orchestrator"] * 2)
    autopilot._maybe_circuit_break("p7")
    with db.connection() as conn:
        row = conn.execute(
            "SELECT detail FROM audit_log WHERE project_id = 'p7' AND action = 'circuit_breaker'"
        ).fetchone()
    assert row is not None
    assert "circuit_breaker" in row["detail"]
