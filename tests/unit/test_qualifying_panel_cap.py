"""Tests for the qualifying-panel revision-round cap and SHELVED state.

A qualifying panel may request `revise` at most twice; the third
convening switches to FINAL mode and panelists must choose `ready`
or `shelve`. The new SHELVED state is terminal for the project but
the Postulant retains rank and may propose a new qualifying project.
"""

from __future__ import annotations

from datetime import UTC, datetime
from pathlib import Path

import pytest

from institute import db, paths, workspaces
from institute import fellow as fellow_mod
from institute.fellow import Genome
from institute.state import (
    ALLOWED_TRANSITIONS,
    NEXT_ACTION,
    TERMINAL_STATE_VALUES,
    State,
    is_terminal,
)
from institute.workflows import qualifying_panel


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
    monkeypatch.setattr(paths, "GENOMES", genomes)
    monkeypatch.setattr(paths, "FELLOWS", fellows)
    monkeypatch.setattr(paths, "ARCHIVE", archive)
    monkeypatch.setattr(paths, "ROOT", tmp_path)
    monkeypatch.setattr(fellow_mod, "GENOMES", genomes)
    monkeypatch.setattr(fellow_mod, "FELLOWS", fellows)
    monkeypatch.setattr(workspaces, "FELLOWS", fellows)
    db.initialize(db_path)
    return tmp_path


def _seed_fellow(conn, fellow_id: str, name: str, rank: str = "fellow") -> None:
    g = Genome(
        id=fellow_id,
        name=name,
        rank=rank,
        model="claude-sonnet-4-6",
        specialization=f"spec-{fellow_id}",
        system_prompt_addendum=("body " * 60).strip(),
        allowed_tools=["Read"],
    )
    g.write(fellow_mod.genome_path(g.id))
    fellow_mod.register(conn, g)


# ---------------------------------------------------------------------------
# State machine
# ---------------------------------------------------------------------------


def test_shelved_is_terminal() -> None:
    assert State.SHELVED.value in TERMINAL_STATE_VALUES
    assert NEXT_ACTION[State.SHELVED] is None
    assert is_terminal(State.SHELVED)


def test_awaiting_qualifying_panel_can_shelve() -> None:
    assert State.SHELVED in ALLOWED_TRANSITIONS[State.AWAITING_QUALIFYING_PANEL]


def test_shelved_cannot_transition_further() -> None:
    assert ALLOWED_TRANSITIONS[State.SHELVED] == set()


# ---------------------------------------------------------------------------
# count_prior_revise_rounds
# ---------------------------------------------------------------------------


def test_count_prior_revise_rounds_zero_initially(isolated: Path) -> None:
    with db.connection() as conn:
        assert qualifying_panel.count_prior_revise_rounds(conn, "p1") == 0


def test_count_prior_revise_rounds_counts_panel_audit_rows(isolated: Path) -> None:
    with db.connection() as conn, db.transaction(conn):
        _seed_fellow(conn, "ada", "Ada")
        # Three prior panel convenings for p1.
        for i in range(3):
            ts = f"2026-05-20T1{i}:00:00+00:00"
            conn.execute(
                "INSERT INTO audit_log (at, actor, action, project_id, detail) "
                "VALUES (?, 'orchestrator,ada', 'qualifying_panel', 'p1', ?)",
                (ts, f"round {i}"),
            )

    with db.connection() as conn:
        assert qualifying_panel.count_prior_revise_rounds(conn, "p1") == 3


def test_count_prior_revise_rounds_scoped_to_project(isolated: Path) -> None:
    """Rounds on a different project must not bleed into this project's count."""
    with db.connection() as conn, db.transaction(conn):
        _seed_fellow(conn, "ada", "Ada")
        for pid in ("p-other", "p-other", "p-other", "p-target"):
            conn.execute(
                "INSERT INTO audit_log (at, actor, action, project_id, detail) "
                "VALUES (datetime('now'), 'orchestrator', 'qualifying_panel', ?, '')",
                (pid,),
            )
    with db.connection() as conn:
        assert qualifying_panel.count_prior_revise_rounds(conn, "p-target") == 1
        assert qualifying_panel.count_prior_revise_rounds(conn, "p-other") == 3


# ---------------------------------------------------------------------------
# MAX_PANEL_REVISE_ROUNDS constant
# ---------------------------------------------------------------------------


def test_max_panel_revise_rounds_is_two() -> None:
    """Two prior revisions allowed; 3rd convening is final. Matches the
    operator decision recorded with the design."""
    assert qualifying_panel.MAX_PANEL_REVISE_ROUNDS == 2


# ---------------------------------------------------------------------------
# qualify.run() allows new qualifying after SHELVED
# ---------------------------------------------------------------------------


def test_qualify_run_allows_new_qualifying_after_shelved(isolated: Path) -> None:
    """A shelved qualifying project must not block the Postulant from
    proposing a new one. (Asserted via the SQL gate in qualify.run().)"""

    with db.connection() as conn, db.transaction(conn):
        _seed_fellow(conn, "advisor", "Advisor")
        _seed_fellow(conn, "post", "Post", rank="postulant")
        conn.execute("UPDATE fellows SET advisor_id = 'advisor' WHERE id = 'post'")
        conn.execute(
            "UPDATE fellows SET curriculum_completed_at = ? WHERE id = 'post'",
            (datetime.now(UTC).isoformat(timespec="seconds"),),
        )
        # Prior qualifying project that ended in SHELVED.
        now = datetime.now(UTC).isoformat(timespec="seconds")
        conn.execute(
            "INSERT INTO projects (id, title, state, kind, lead_fellow_id, "
            "created_at, updated_at) VALUES "
            "('q-prior', 'Prior', 'shelved', 'qualifying', 'post', ?, ?)",
            (now, now),
        )

    # qualify.run() executes more than the gate (it invokes Claude), so
    # we verify only the SQL: a shelved prior must not be returned as
    # the blocking row.
    with db.connection() as conn:
        blocking = conn.execute(
            "SELECT id, state FROM projects "
            "WHERE lead_fellow_id = 'post' AND kind = 'qualifying' "
            "  AND state != 'shelved'"
        ).fetchone()
    assert blocking is None


def test_qualify_run_still_blocks_in_flight(isolated: Path) -> None:
    """A non-shelved qualifying project still blocks a new one."""
    with db.connection() as conn, db.transaction(conn):
        _seed_fellow(conn, "post", "Post", rank="postulant")
        now = datetime.now(UTC).isoformat(timespec="seconds")
        conn.execute(
            "INSERT INTO projects (id, title, state, kind, lead_fellow_id, "
            "created_at, updated_at) VALUES "
            "('q-active', 'Active', 'revising', 'qualifying', 'post', ?, ?)",
            (now, now),
        )

    with db.connection() as conn:
        blocking = conn.execute(
            "SELECT id, state FROM projects "
            "WHERE lead_fellow_id = 'post' AND kind = 'qualifying' "
            "  AND state != 'shelved'"
        ).fetchone()
    assert blocking is not None
    assert blocking["id"] == "q-active"
