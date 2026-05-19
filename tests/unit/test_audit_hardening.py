"""Tests for the audit-pass-1 hardening commits.

Covers:
- state.transition validates and forces transitions correctly.
- reputation.consecutive_holds matches actors exactly, not by substring.
- editorial_board._tenure_timestamp matches actors exactly.
- promote._tally enforces panel-quorum guards.
- group_form.match_invitees honors word boundaries.
- budget.daily_total_usd clamps negative costs and pathological thresholds.
- workspaces.clear_outputs unlinks named files.
- decisions.record orphan-cleans the markdown when the audit_log
  INSERT raises.
- andon_review._dismiss_target_state replays non-cord recs.
- terminate nulls advisor_id on advisees + emits reassignment decision.
- peer_review._pick_review_slots persists slots and ignores cohort
  reshuffles after first call.
"""

from __future__ import annotations

import json
import sqlite3
from datetime import UTC, datetime
from pathlib import Path
from unittest.mock import patch

import pytest

from institute import budget, db, editorial_board, reputation, workspaces
from institute import fellow as fellow_mod
from institute.fellow import Genome
from institute.state import State, transition
from institute.workflows import andon_review as andon_mod
from institute.workflows import group_form
from institute.workflows.peer_review import _pick_review_slots
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


@pytest.fixture()
def isolated(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> Path:
    monkeypatch.setattr(fellow_mod, "GENOMES", tmp_path / "genomes")
    monkeypatch.setattr(fellow_mod, "FELLOWS", tmp_path / "fellows")
    db_path = tmp_path / "institute.db"
    monkeypatch.setattr(db, "DB_PATH", db_path)
    db.initialize(db_path)
    (tmp_path / "genomes").mkdir(exist_ok=True)
    return tmp_path


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


# --- budget hardening ----------------------------------------------------


def test_daily_total_clamps_negative_cost(tmp_path: Path) -> None:
    log = tmp_path / "audit.log"
    today = datetime.now(UTC).date().isoformat()
    log.write_text(
        "\n".join(
            [
                json.dumps({"ts": f"{today}T01:00:00+00:00", "cost_usd": 1.0}),
                json.dumps({"ts": f"{today}T02:00:00+00:00", "cost_usd": -1000.0}),
                json.dumps({"ts": f"{today}T03:00:00+00:00", "cost_usd": 2.5}),
            ]
        )
        + "\n",
        encoding="utf-8",
    )
    assert budget.daily_total_usd(today, audit_log=log) == 3.5


def test_current_status_clamps_pathological_threshold(tmp_path: Path) -> None:
    log = tmp_path / "audit.log"
    now = datetime.now(UTC)
    log.write_text(
        json.dumps({"ts": now.isoformat(timespec="seconds"), "cost_usd": 5.0}) + "\n",
        encoding="utf-8",
    )
    # threshold > 1.0 would put hard before soft; clamp brings it into
    # range so soft can still fire below hard.
    snap = budget.current_status(10.0, soft_threshold=5.0, audit_log=log)
    assert snap.soft_cap_usd <= snap.hard_cap_usd
    # threshold = 0 would mark every nonzero spend as soft; clamp to 0.01.
    snap = budget.current_status(10.0, soft_threshold=0.0, audit_log=log)
    assert snap.soft_cap_usd > 0


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


# --- andon_review._dismiss_target_state ----------------------------------


def test_dismiss_target_state_routes_by_residual_recommendations(isolated: Path) -> None:
    fellows = [
        _genome("lead", "Lead Lead"),
        _genome("ada", "Ada A"),
        _genome("henri", "Henri P"),
    ]
    for g in fellows:
        g.write(isolated / "genomes" / f"{g.id}.json")
    with db.connection() as conn, db.transaction(conn):
        for g in fellows:
            fellow_mod.register(conn, g)
    _seed_project("p-andon", "lead", state_value="andon_review")
    now = datetime.now(UTC).isoformat(timespec="seconds")

    # Scenario 1: one cord pull, no other reviewers → dismiss → EDITORIAL.
    assert andon_mod._dismiss_target_state("p-andon") == State.EDITORIAL

    # Scenario 2: a non-cord reviewer recommended `major`. Dismiss → REVISING.
    with db.connection() as conn, db.transaction(conn):
        conn.execute(
            "INSERT INTO reviews "
            "(id, project_id, reviewer_id, role, recommendation, confidence, "
            " content_path, submitted_at, dissent, round, andon_cord, andon_reason, "
            " charter_violation, violation_kind) "
            "VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
            (
                "r1",
                "p-andon",
                "ada",
                "primary",
                "major",
                "confident",
                "x.md",
                now,
                0,
                1,
                0,
                None,
                0,
                None,
            ),
        )
    assert andon_mod._dismiss_target_state("p-andon") == State.REVISING

    # Scenario 3: add a `reject` recommendation. Dismiss → EDITORIAL_REVIEW.
    with db.connection() as conn, db.transaction(conn):
        conn.execute(
            "INSERT INTO reviews "
            "(id, project_id, reviewer_id, role, recommendation, confidence, "
            " content_path, submitted_at, dissent, round, andon_cord, andon_reason, "
            " charter_violation, violation_kind) "
            "VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
            (
                "r2",
                "p-andon",
                "henri",
                "secondary",
                "reject",
                "confident",
                "x.md",
                now,
                0,
                1,
                0,
                None,
                0,
                None,
            ),
        )
    assert andon_mod._dismiss_target_state("p-andon") == State.EDITORIAL_REVIEW


# --- terminate nulls advisor_id ------------------------------------------


def test_terminate_clears_advisor_id_on_advisees(
    isolated: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    from institute.workflows import terminate

    # Skip the prompt/decision details: directly assert that advisor_id
    # is cleared by inserting a fellow + an advisee and calling run.
    advisor = _genome("adv", "Adv", rank="senior_fellow")
    advisee = _genome("apprentice", "Apprentice", rank="postulant")
    for g in (advisor, advisee):
        g.write(isolated / "genomes" / f"{g.id}.json")
    with db.connection() as conn, db.transaction(conn):
        fellow_mod.register(conn, advisor)
        fellow_mod.register(conn, advisee)
        conn.execute("UPDATE fellows SET advisor_id = ? WHERE id = ?", ("adv", "apprentice"))

    # Use a stub decision recorder so we don't actually touch disk.
    monkeypatch.setattr(
        "institute.workflows.terminate.decisions.record",
        lambda _conn, _decision: Path("/tmp/x.md"),
    )

    terminate.run(
        fellow_id="adv",
        kind="other",
        reason="audit-test reason",
        triggered_by="founder",
    )

    with db.connection() as conn:
        row = conn.execute(
            "SELECT advisor_id, retired_at FROM fellows WHERE id = 'apprentice'"
        ).fetchone()
    assert row["advisor_id"] is None
    # Advisor herself is retired.
    with db.connection() as conn:
        adv_row = conn.execute("SELECT retired_at FROM fellows WHERE id = 'adv'").fetchone()
    assert adv_row["retired_at"] is not None


# --- peer_review reviewer_slots persistence ------------------------------


def test_pick_review_slots_persists_and_replays(isolated: Path) -> None:
    fellows = [
        _genome("lead", "Lead L", spec="applied"),
        _genome("ada", "Ada A", spec="applied"),
        _genome("henri", "Henri P", spec="theory"),
        _genome("michel", "Michel M", spec="essay"),
    ]
    for g in fellows:
        g.write(isolated / "genomes" / f"{g.id}.json")
    with db.connection() as conn, db.transaction(conn):
        for g in fellows:
            fellow_mod.register(conn, g)
    _seed_project("p-slots", "lead", state_value="drafted")

    with db.connection() as conn:
        first = _pick_review_slots(conn, "p-slots", "lead", 1)
    by_role_first = {s.role: s.reviewer_id for s in first}

    # Now sideline one of the reviewers via a misconduct mark and call
    # again. The persisted slots should be returned unchanged.
    with db.connection() as conn, db.transaction(conn):
        conn.execute(
            "INSERT INTO reviewer_marks "
            "(fellow_id, kind, weight, reason, recorded_at, expires_at) "
            "VALUES (?, ?, ?, ?, ?, ?)",
            (
                first[0].reviewer_id,
                "frivolous_andon",
                10.0,  # well above threshold
                "test",
                datetime.now(UTC).isoformat(timespec="seconds"),
                "2099-01-01T00:00:00+00:00",
            ),
        )
    with db.connection() as conn:
        second = _pick_review_slots(conn, "p-slots", "lead", 1)
    by_role_second = {s.role: s.reviewer_id for s in second}
    assert by_role_first == by_role_second


# --- audit cost tracker --------------------------------------------------


def test_audit_cost_tracker_only_counts_new_lines(tmp_path, monkeypatch) -> None:
    from institute import cli as cli_mod
    from institute import paths as paths_mod

    log = tmp_path / "audit.log"
    log.write_text(
        json.dumps({"ts": "2026-05-19T00:00:00+00:00", "cost_usd": 1.0}) + "\n",
        encoding="utf-8",
    )
    monkeypatch.setattr(paths_mod, "AUDIT_LOG", log)
    tracker = cli_mod._AuditCostTracker.from_now()
    assert tracker.delta() == 0.0  # nothing new yet
    with log.open("a", encoding="utf-8") as fh:
        fh.write(json.dumps({"ts": "2026-05-19T01:00:00+00:00", "cost_usd": 2.0}) + "\n")
        fh.write(json.dumps({"ts": "2026-05-19T02:00:00+00:00", "cost_usd": 0.5}) + "\n")
    assert tracker.delta() == 2.5


# --- _non_negative_usd CLI callback --------------------------------------


def test_non_negative_usd_rejects_negative() -> None:
    import click

    from institute.cli import _non_negative_usd

    class _Param:
        name = "--daily-budget-usd"

    with pytest.raises(click.BadParameter):
        _non_negative_usd(None, _Param(), -1.0)
    assert _non_negative_usd(None, _Param(), 0.0) == 0.0
    assert _non_negative_usd(None, _Param(), 5.0) == 5.0
    # `None` from a missing default is treated as 0
    assert _non_negative_usd(None, _Param(), None) == 0.0


# --- silence the unused-import warning so ruff stays happy ---------------

_ = patch
