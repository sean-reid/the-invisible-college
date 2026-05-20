"""Audit-pass-1 hardening: andon dismissal routing, terminate cleanup, peer_review slot persistence."""

from __future__ import annotations

from datetime import UTC, datetime
from pathlib import Path

import pytest

from institute import db
from institute import fellow as fellow_mod
from institute.fellow import Genome
from institute.state import State
from institute.workflows import andon_review as andon_mod
from institute.workflows.peer_review import _pick_review_slots


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
