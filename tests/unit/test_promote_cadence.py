"""Promotion cadence: consecutive-hold streaks and auto-trigger candidate selection."""

from __future__ import annotations

from datetime import UTC, datetime, timedelta
from pathlib import Path

from freezegun import freeze_time

from institute import db, reputation
from institute import fellow as fellow_mod
from institute.fellow import Genome


def _seed_fellow(conn, fellow_id: str, name: str, rank: str = "fellow") -> Genome:
    g = Genome(
        id=fellow_id,
        name=name,
        rank=rank,
        model="claude-sonnet-4-6",
        specialization=f"spec-{fellow_id}",
        system_prompt_addendum=("body " * 60).strip(),
        allowed_tools=["Read"],
    )
    g.write(fellow_mod.genome_path(fellow_id))
    fellow_mod.register(conn, g)
    return g


# ---------------------------------------------------------------------------
# consecutive_holds
# ---------------------------------------------------------------------------


@freeze_time("2026-05-20T12:00:00Z")
def test_consecutive_holds_counts_recent_holds_only(isolated: Path) -> None:
    """A streak of promotion_review entries with no rank change extends; a promotion resets."""
    from datetime import UTC, datetime, timedelta

    with db.connection() as conn, db.transaction(conn):
        _seed_fellow(conn, "ada", "Ada", rank="fellow")
        # Earliest: a real promotion (rank change). This should reset the streak.
        earlier = (datetime.now(UTC) - timedelta(days=5)).isoformat(timespec="seconds")
        mid = (datetime.now(UTC) - timedelta(days=3)).isoformat(timespec="seconds")
        later = (datetime.now(UTC) - timedelta(days=1)).isoformat(timespec="seconds")
        conn.execute(
            "INSERT INTO audit_log (at, actor, action, detail) VALUES (?, ?, ?, ?)",
            (earlier, "founder,orchestrator,ada", "promotion", "x"),
        )
        conn.execute(
            "INSERT INTO audit_log (at, actor, action, detail) VALUES (?, ?, ?, ?)",
            (mid, "founder,orchestrator,ada", "promotion_review", "x"),
        )
        conn.execute(
            "INSERT INTO audit_log (at, actor, action, detail) VALUES (?, ?, ?, ?)",
            (later, "founder,orchestrator,ada", "promotion_review", "x"),
        )

    with db.connection() as conn:
        assert reputation.consecutive_holds(conn, "ada") == 2


def test_consecutive_holds_zero_when_no_history(isolated: Path) -> None:
    with db.connection() as conn, db.transaction(conn):
        _seed_fellow(conn, "ada", "Ada")
    with db.connection() as conn:
        assert reputation.consecutive_holds(conn, "ada") == 0


# ---------------------------------------------------------------------------
# Auto-trigger candidate selection (alternating strong / overdue)
# ---------------------------------------------------------------------------


def test_pick_review_candidate_strong_picks_highest_score(isolated: Path) -> None:
    """Strong mode picks the Fellow with the highest activity score."""
    from institute import cli

    with db.connection() as conn, db.transaction(conn):
        _seed_fellow(conn, "high", "High Activity")
        _seed_fellow(conn, "low", "Low Activity")
        # Give "high" a publication so its activity score beats "low".
        now = datetime.now(UTC).isoformat(timespec="seconds")
        conn.execute(
            "INSERT INTO projects "
            "(id, title, state, lead_fellow_id, review_round, created_at, updated_at) "
            "VALUES (?, ?, ?, ?, 1, ?, ?)",
            ("p1", "t", "published", "high", now, now),
        )
    cohort = reputation.load_cohort()
    chosen = cli._pick_review_candidate(cohort, "strong")
    assert chosen.fellow_id == "high"


@freeze_time("2026-05-20T12:00:00Z")
def test_pick_review_candidate_overdue_picks_never_reviewed(isolated: Path) -> None:
    """Overdue mode prefers the Fellow whose last review is furthest in the past."""
    from institute import cli

    with db.connection() as conn, db.transaction(conn):
        _seed_fellow(conn, "recent", "Recently Reviewed")
        _seed_fellow(conn, "old", "Old Review")
        _seed_fellow(conn, "never", "Never Reviewed")
        # recent: a promotion two days ago
        # old: a hold ten days ago
        # never: nothing in audit_log
        recent_ts = (datetime.now(UTC) - timedelta(days=2)).isoformat(timespec="seconds")
        old_ts = (datetime.now(UTC) - timedelta(days=10)).isoformat(timespec="seconds")
        conn.execute(
            "INSERT INTO audit_log (at, actor, action, detail) VALUES (?, ?, ?, ?)",
            (recent_ts, "founder,orchestrator,recent", "promotion", "x"),
        )
        conn.execute(
            "INSERT INTO audit_log (at, actor, action, detail) VALUES (?, ?, ?, ?)",
            (old_ts, "founder,orchestrator,old", "promotion_review", "x"),
        )
    cohort = reputation.load_cohort()
    chosen = cli._pick_review_candidate(cohort, "overdue")
    assert chosen.fellow_id == "never", "A Fellow with no review history is the most overdue"
