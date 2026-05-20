"""Tests for the Editorial Board: membership and routing.

These tests exercise the pure plumbing (member resolution, routing
decision based on round-2 review outcomes, applying accept/reject).
"""

from __future__ import annotations

from datetime import UTC, datetime
from pathlib import Path

from institute import db, editorial_board, paths
from institute import fellow as fellow_mod
from institute.fellow import Genome
from institute.state import ALLOWED_TRANSITIONS, NEXT_ACTION, State
from institute.workflows import editorial_review, peer_review


def _genome(fellow_id: str, name: str, rank: str = "fellow") -> Genome:
    return Genome(
        id=fellow_id,
        name=name,
        rank=rank,
        model="claude-sonnet-4-6",
        specialization=f"spec-{fellow_id}",
        system_prompt_addendum=("body " * 60).strip(),
        allowed_tools=["Read"],
    )


def _seed(conn, g: Genome) -> None:
    g.write(fellow_mod.genome_path(g.id))
    fellow_mod.register(conn, g)


def _seed_project(conn, project_id: str, lead: str, *, state: str = "peer_reviewing") -> None:
    now = datetime.now(UTC).isoformat(timespec="seconds")
    draft_path = paths.DRAFTS / project_id / "draft.md"
    draft_path.parent.mkdir(parents=True, exist_ok=True)
    draft_path.write_text("# Test\nbody\n", encoding="utf-8")
    conn.execute(
        "INSERT INTO projects (id, title, state, lead_fellow_id, draft_path, "
        " review_round, created_at, updated_at) "
        "VALUES (?, ?, ?, ?, ?, 2, ?, ?)",
        (
            project_id,
            f"Title for {project_id}",
            state,
            lead,
            str(draft_path.relative_to(paths.ROOT)),
            now,
            now,
        ),
    )


def _seed_review(conn, review_id, project_id, reviewer, rec, round_no, *, dissent=False):
    review_path = paths.REVIEWS / project_id / f"review-by-{reviewer}.md"
    review_path.parent.mkdir(parents=True, exist_ok=True)
    review_path.write_text(f"# Review by {reviewer}\nbody\n", encoding="utf-8")
    conn.execute(
        "INSERT INTO reviews (id, project_id, reviewer_id, role, recommendation, "
        " confidence, content_path, dissent, round) "
        "VALUES (?, ?, ?, 'primary', ?, 'confident', ?, ?, ?)",
        (
            review_id,
            project_id,
            reviewer,
            rec,
            str(review_path.relative_to(paths.ROOT)),
            int(dissent),
            round_no,
        ),
    )


# ---------------------------------------------------------------------------
# State machine
# ---------------------------------------------------------------------------


def test_editorial_review_state_exists() -> None:
    assert State.EDITORIAL_REVIEW == "editorial_review"


def test_editorial_review_dispatches_correct_workflow() -> None:
    assert NEXT_ACTION[State.EDITORIAL_REVIEW] == "editorial_review"


def test_editorial_review_transitions() -> None:
    assert ALLOWED_TRANSITIONS[State.EDITORIAL_REVIEW] == {
        State.EDITORIAL,
        State.REJECTED,
        State.ABANDONED,
    }


def test_peer_reviewing_can_transition_to_editorial_review() -> None:
    assert State.EDITORIAL_REVIEW in ALLOWED_TRANSITIONS[State.PEER_REVIEWING]


# ---------------------------------------------------------------------------
# Membership resolution
# ---------------------------------------------------------------------------


def test_no_senior_fellows_means_empty_board(isolated: Path) -> None:
    with db.connection() as conn, db.transaction(conn):
        _seed(conn, _genome("ada", "Ada"))
    with db.connection() as conn:
        assert editorial_board.current_member_ids(conn) == []
        assert not editorial_board.has_quorum(conn)


def test_all_seniors_serve_when_three_or_fewer(isolated: Path) -> None:
    with db.connection() as conn, db.transaction(conn):
        _seed(conn, _genome("pierre", "Pierre", rank="senior_fellow"))
        _seed(conn, _genome("henri", "Henri", rank="senior_fellow"))
    with db.connection() as conn:
        ids = set(editorial_board.current_member_ids(conn))
        assert ids == {"pierre", "henri"}
        assert editorial_board.has_quorum(conn)


def test_board_caps_at_three_when_more_seniors_exist(isolated: Path) -> None:
    with db.connection() as conn, db.transaction(conn):
        for name in ["a", "b", "c", "d", "e"]:
            _seed(conn, _genome(f"sen-{name}", f"Senior {name}", rank="senior_fellow"))
        # Give them staggered tenure so the test is deterministic.
        for i, fid in enumerate(["sen-a", "sen-b", "sen-c", "sen-d", "sen-e"]):
            conn.execute(
                "INSERT INTO audit_log (at, actor, action, detail) VALUES (?, ?, ?, ?)",
                (
                    f"2026-01-{10 + i:02d}T00:00:00+00:00",
                    f"founder,orchestrator,{fid}",
                    "promotion",
                    "x",
                ),
            )
    # Tenure-ordered cohort is [sen-a, sen-b, sen-c, sen-d, sen-e].
    # Each calendar month the rotation cycles by one position.
    base = datetime(2026, 1, 1, tzinfo=UTC)
    with db.connection() as conn:
        m0 = editorial_board.current_member_ids(conn, at=base)
        m1 = editorial_board.current_member_ids(conn, at=base.replace(month=2))
        # Five months later wraps the 5-member cohort exactly once.
        m_after_full_cycle = editorial_board.current_member_ids(
            conn, at=base.replace(year=2026, month=6)
        )
    assert len(m0) == editorial_board.BOARD_SEAT_COUNT == 3
    # Members are unique within a window.
    assert len(set(m0)) == 3
    # One month forward rotates by exactly one position.
    assert m1[0] == m0[1]
    # A full cycle of the cohort (5 months for 5 Fellows) restores the
    # selection.
    assert m_after_full_cycle == m0


def test_retired_seniors_do_not_serve(isolated: Path) -> None:
    with db.connection() as conn, db.transaction(conn):
        _seed(conn, _genome("active", "Active", rank="senior_fellow"))
        _seed(conn, _genome("retired", "Retired", rank="senior_fellow"))
        conn.execute(
            "UPDATE fellows SET retired_at = ? WHERE id = 'retired'",
            (datetime.now(UTC).isoformat(timespec="seconds"),),
        )
    with db.connection() as conn:
        assert editorial_board.current_member_ids(conn) == ["active"]


# ---------------------------------------------------------------------------
# Routing: peer_review._transition_after_all_reviews
# ---------------------------------------------------------------------------


def test_round_2_reject_routes_to_editorial_review(isolated: Path) -> None:
    """A round-2 reject recommendation triggers Editorial Board review."""
    with db.connection() as conn, db.transaction(conn):
        _seed(conn, _genome("ada", "Ada"))
        _seed(conn, _genome("r1", "R1"))
        _seed(conn, _genome("r2", "R2"))
        _seed(conn, _genome("r3", "R3"))
        _seed_project(conn, "proj-1", "ada")
        # Round 1 minor recommendations; we just need round 2 to drive routing.
        _seed_review(conn, "v1", "proj-1", "r1", "minor", 1)
        _seed_review(conn, "v2", "proj-1", "r2", "minor", 1)
        _seed_review(conn, "v3", "proj-1", "r3", "minor", 1)
        # Round 2: one reject, two accept.
        _seed_review(conn, "v4", "proj-1", "r1", "accept", 2)
        _seed_review(conn, "v5", "proj-1", "r2", "reject", 2)
        _seed_review(conn, "v6", "proj-1", "r3", "accept", 2)

    peer_review._transition_after_all_reviews("proj-1", "Title", 2)

    with db.connection() as conn:
        row = conn.execute("SELECT state FROM projects WHERE id = 'proj-1'").fetchone()
    assert row["state"] == "editorial_review"


def test_round_2_dissent_routes_to_editorial_review(isolated: Path) -> None:
    """A flagged dissent (even with non-reject recs) still triggers the Board."""
    with db.connection() as conn, db.transaction(conn):
        _seed(conn, _genome("ada", "Ada"))
        _seed(conn, _genome("r1", "R1"))
        _seed(conn, _genome("r2", "R2"))
        _seed_project(conn, "proj-2", "ada")
        _seed_review(conn, "v1", "proj-2", "r1", "accept", 2)
        _seed_review(conn, "v2", "proj-2", "r2", "minor", 2, dissent=True)

    peer_review._transition_after_all_reviews("proj-2", "Title", 2)

    with db.connection() as conn:
        row = conn.execute("SELECT state FROM projects WHERE id = 'proj-2'").fetchone()
    assert row["state"] == "editorial_review"


def test_round_2_unanimous_accept_skips_editorial_review(isolated: Path) -> None:
    """All accept, no dissent → straight to EDITORIAL, no Board needed."""
    with db.connection() as conn, db.transaction(conn):
        _seed(conn, _genome("ada", "Ada"))
        _seed(conn, _genome("r1", "R1"))
        _seed(conn, _genome("r2", "R2"))
        _seed_project(conn, "proj-3", "ada")
        _seed_review(conn, "v1", "proj-3", "r1", "accept", 2)
        _seed_review(conn, "v2", "proj-3", "r2", "accept", 2)

    peer_review._transition_after_all_reviews("proj-3", "Title", 2)

    with db.connection() as conn:
        row = conn.execute("SELECT state FROM projects WHERE id = 'proj-3'").fetchone()
    assert row["state"] == "editorial"


def test_round_2_minor_concerns_no_dissent_goes_to_revising(isolated: Path) -> None:
    """Mixed minor/accept with no dissent stays in the revise-once flow."""
    with db.connection() as conn, db.transaction(conn):
        _seed(conn, _genome("ada", "Ada"))
        _seed(conn, _genome("r1", "R1"))
        _seed(conn, _genome("r2", "R2"))
        _seed_project(conn, "proj-4", "ada")
        _seed_review(conn, "v1", "proj-4", "r1", "minor", 2)
        _seed_review(conn, "v2", "proj-4", "r2", "accept", 2)

    peer_review._transition_after_all_reviews("proj-4", "Title", 2)

    with db.connection() as conn:
        row = conn.execute("SELECT state FROM projects WHERE id = 'proj-4'").fetchone()
    assert row["state"] == "revising"


# ---------------------------------------------------------------------------
# _apply_outcome
# ---------------------------------------------------------------------------


def test_apply_outcome_accept_moves_to_editorial(isolated: Path) -> None:
    with db.connection() as conn, db.transaction(conn):
        _seed(conn, _genome("ada", "Ada"))
        _seed_project(conn, "proj-5", "ada", state="editorial_review")

    editorial_review._apply_outcome("proj-5", "Title", "accept", ["editorial-board"], None)
    with db.connection() as conn:
        row = conn.execute("SELECT state FROM projects WHERE id = 'proj-5'").fetchone()
    assert row["state"] == "editorial"


def test_apply_outcome_reject_moves_to_rejected(isolated: Path) -> None:
    with db.connection() as conn, db.transaction(conn):
        _seed(conn, _genome("ada", "Ada"))
        _seed_project(conn, "proj-6", "ada", state="editorial_review")

    editorial_review._apply_outcome("proj-6", "Title", "reject", ["editorial-board"], None)
    with db.connection() as conn:
        row = conn.execute("SELECT state FROM projects WHERE id = 'proj-6'").fetchone()
    assert row["state"] == "rejected"


def test_apply_outcome_records_decision(isolated: Path) -> None:
    with db.connection() as conn, db.transaction(conn):
        _seed(conn, _genome("ada", "Ada"))
        _seed_project(conn, "proj-7", "ada", state="editorial_review")

    editorial_review._apply_outcome("proj-7", "Title", "accept", ["editorial-board"], None)
    with db.connection() as conn:
        rows = list(conn.execute("SELECT action FROM audit_log WHERE action = 'editorial_ruling'"))
    assert len(rows) == 1
