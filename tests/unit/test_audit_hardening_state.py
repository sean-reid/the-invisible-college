"""Audit-pass-1 hardening: state machine, actor exact-match, promote tally, group_form, workspaces, decisions."""

from __future__ import annotations

import sqlite3
from datetime import UTC, datetime
from pathlib import Path

import pytest

from institute import db, editorial_board, reputation, workspaces
from institute import fellow as fellow_mod
from institute.fellow import Genome
from institute.state import State, transition
from institute.workflows import group_form
from institute.workflows.promote import _tally


def _genome(slug: str, name: str, *, rank: str = "fellow", spec: str = "general") -> Genome:
    return Genome(
        id=slug,
        name=name,
        rank=rank,
        model="claude-sonnet-4-6",
        specialization=spec,
        system_prompt_addendum=("body " * 60).strip(),
        allowed_tools=["Read"],
    )


def _seed_project(project_id: str, lead_id: str, state_value: str = "drafted") -> None:
    now = datetime.now(UTC).isoformat(timespec="seconds")
    with db.connection() as conn, db.transaction(conn):
        conn.execute(
            "INSERT INTO projects "
            "(id, title, state, lead_fellow_id, draft_path, review_round, "
            " created_at, updated_at) "
            "VALUES (?, ?, ?, ?, ?, ?, ?, ?)",
            (project_id, "t", state_value, lead_id, "draft.md", 1, now, now),
        )


# --- state.transition ----------------------------------------------------


def test_state_transition_rejects_illegal_move(isolated: Path) -> None:
    g = _genome("lead", "Lead Lead")
    g.write(isolated / "genomes" / f"{g.id}.json")
    with db.connection() as conn, db.transaction(conn):
        fellow_mod.register(conn, g)
    _seed_project("p1", "lead", state_value="proposed")
    with db.connection() as conn, db.transaction(conn):
        with pytest.raises(ValueError, match="Illegal transition"):
            transition(conn, "p1", State.PUBLISHED)


def test_state_transition_force_bypasses_validation(isolated: Path) -> None:
    g = _genome("lead", "Lead Lead")
    g.write(isolated / "genomes" / f"{g.id}.json")
    with db.connection() as conn, db.transaction(conn):
        fellow_mod.register(conn, g)
    _seed_project("p1", "lead", state_value="proposed")
    # Force-jumps from PROPOSED → REJECTED (allowed normally too, but a
    # PROPOSED → PUBLISHED force should also work).
    with db.connection() as conn, db.transaction(conn):
        transition(conn, "p1", State.PUBLISHED, force=True)
    with db.connection() as conn:
        row = conn.execute("SELECT state FROM projects WHERE id = 'p1'").fetchone()
    assert row["state"] == "published"


# --- actor exact-match (reputation, editorial_board) ---------------------


def test_consecutive_holds_does_not_match_substring(isolated: Path) -> None:
    # Two Fellows whose ids share a prefix: 'ada' is a substring of 'adam'.
    ada = _genome("ada", "Ada A")
    adam = _genome("adam", "Adam A")
    for g in (ada, adam):
        g.write(isolated / "genomes" / f"{g.id}.json")
    with db.connection() as conn, db.transaction(conn):
        fellow_mod.register(conn, ada)
        fellow_mod.register(conn, adam)
        # Adam has two promotion_review holds. Ada has none.
        for at in ("2026-05-15T01:00:00+00:00", "2026-05-16T01:00:00+00:00"):
            conn.execute(
                "INSERT INTO audit_log (at, actor, action, project_id, detail) "
                "VALUES (?, ?, ?, NULL, NULL)",
                (at, "orchestrator,adam", "promotion_review"),
            )
    with db.connection() as conn:
        # Ada (the substring) must NOT pick up Adam's holds.
        assert reputation.consecutive_holds(conn, "ada") == 0
        assert reputation.consecutive_holds(conn, "adam") == 2


def test_tenure_timestamp_does_not_match_substring(isolated: Path) -> None:
    ada = _genome("ada", "Ada A", rank="senior_fellow")
    adam = _genome("adam", "Adam A", rank="senior_fellow")
    for g in (ada, adam):
        g.write(isolated / "genomes" / f"{g.id}.json")
    with db.connection() as conn, db.transaction(conn):
        fellow_mod.register(conn, ada)
        fellow_mod.register(conn, adam)
        # Adam has an earlier promotion record; ada has none.
        conn.execute(
            "INSERT INTO audit_log (at, actor, action, project_id, detail) "
            "VALUES (?, ?, ?, NULL, NULL)",
            ("2026-04-01T00:00:00+00:00", "orchestrator,adam", "promotion"),
        )
    with db.connection() as conn:
        # Ada's tenure should fall back to her created_at, NOT pick up
        # Adam's earlier promotion via substring match.
        ada_ts = editorial_board._tenure_timestamp(conn, "ada")
        adam_ts = editorial_board._tenure_timestamp(conn, "adam")
    assert ada_ts != "2026-04-01T00:00:00+00:00"
    assert adam_ts == "2026-04-01T00:00:00+00:00"


# --- promote._tally panel quorum -----------------------------------------


def test_tally_single_vote_cannot_reach_senior_fellow() -> None:
    votes = [{"vote": "senior_fellow"}]
    assert _tally(votes, "fellow") is None


def test_tally_single_vote_cannot_multi_rank_jump() -> None:
    # junior_fellow → fellow is one rank: allowed.
    assert _tally([{"vote": "fellow"}], "junior_fellow") == "fellow"
    # junior_fellow → senior_fellow is two ranks: refused even though
    # the single voter said senior_fellow.
    assert _tally([{"vote": "senior_fellow"}], "junior_fellow") is None


def test_tally_two_voters_can_promote_into_senior() -> None:
    votes = [{"vote": "senior_fellow"}, {"vote": "senior_fellow"}]
    assert _tally(votes, "fellow") == "senior_fellow"


# --- group_form.match_invitees word boundaries ---------------------------


def test_match_invitees_skips_substring_in_unrelated_word() -> None:
    cohort = [("ada", "Ada Lovelace")]
    # "parade" contains "ada"; word-boundary match must skip it.
    section = "The next big parade is coming."
    assert group_form.match_invitees(section, cohort) == []


def test_match_invitees_still_matches_word_form() -> None:
    cohort = [("ada", "Ada Lovelace")]
    assert group_form.match_invitees("Invite Ada Lovelace please.", cohort) == ["ada"]
    assert group_form.match_invitees("Invite `ada` please.", cohort) == ["ada"]


# --- workspaces.clear_outputs --------------------------------------------


def test_clear_outputs_unlinks_named_files(tmp_path: Path) -> None:
    (tmp_path / "summary.md").write_text("x", encoding="utf-8")
    (tmp_path / "decision.json").write_text("{}", encoding="utf-8")
    (tmp_path / "keep.md").write_text("y", encoding="utf-8")
    workspaces.clear_outputs(tmp_path, ("summary.md", "decision.json", "missing.md"))
    assert not (tmp_path / "summary.md").exists()
    assert not (tmp_path / "decision.json").exists()
    assert (tmp_path / "keep.md").exists()  # unaffected


# --- decisions.record orphan cleanup -------------------------------------


def test_decisions_record_cleans_orphan_on_sql_failure(
    isolated: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    from institute import decisions

    decision = decisions.Decision(
        kind="test_kind",
        title="Test title",
        body="body",
        actors=["orchestrator"],
    )
    written: list[Path] = []
    real_atomic = decisions._atomic_write

    def capturing_write(path: Path, content: str) -> None:
        real_atomic(path, content)
        written.append(path)

    monkeypatch.setattr(decisions, "_atomic_write", capturing_write)

    class _BoomConn:
        def execute(self, *_a, **_k):
            raise sqlite3.OperationalError("boom")

    with pytest.raises(sqlite3.OperationalError):
        decisions.record(_BoomConn(), decision)
    # The .md file was written but should have been cleaned up.
    assert written, "atomic_write should have been called"
    assert not written[0].exists(), "orphan markdown must be deleted on rollback"
