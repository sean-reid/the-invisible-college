"""Tests for the reputation aggregator."""

from __future__ import annotations

from datetime import UTC, datetime
from pathlib import Path

from institute import db, reputation
from institute import fellow as fellow_mod
from institute.fellow import Genome


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
    g.write(fellow_mod.genome_path(fellow_id))
    fellow_mod.register(conn, g)


def _seed_project(conn, project_id: str, lead: str, state: str = "published") -> None:
    now = datetime.now(UTC).isoformat(timespec="seconds")
    conn.execute(
        "INSERT INTO projects (id, title, state, lead_fellow_id, review_round, "
        "created_at, updated_at) VALUES (?, ?, ?, ?, 2, ?, ?)",
        (project_id, f"Title for {project_id}", state, lead, now, now),
    )


def _seed_review(
    conn,
    review_id: str,
    project_id: str,
    reviewer: str,
    rec: str,
    round_no: int,
) -> None:
    conn.execute(
        "INSERT INTO reviews (id, project_id, reviewer_id, role, recommendation, "
        "confidence, content_path, round) VALUES (?, ?, ?, ?, ?, ?, ?, ?)",
        (review_id, project_id, reviewer, "primary", rec, "confident", "x", round_no),
    )


def test_recommendation_bucket_normalizes_variants() -> None:
    assert reputation._recommendation_bucket("accept") == "accept"
    assert reputation._recommendation_bucket("Accept with minor revisions") == "accept"
    assert reputation._recommendation_bucket("minor") == "minor"
    assert reputation._recommendation_bucket("major") == "major"
    assert reputation._recommendation_bucket("REJECT") == "reject"
    assert reputation._recommendation_bucket(None) == "unknown"
    assert reputation._recommendation_bucket("garbage") == "unknown"


def test_author_stats_counts_publications(isolated: Path) -> None:
    with db.connection() as conn, db.transaction(conn):
        _seed_fellow(conn, "ada", "Ada")
        _seed_fellow(conn, "bram", "Bram")
        _seed_project(conn, "p1", "ada", state="published")
        _seed_project(conn, "p2", "ada", state="published")
        _seed_project(conn, "p3", "ada", state="researching")

    with db.connection() as conn:
        stats = reputation.author_stats(conn, "ada")
    assert stats.publications == 2
    assert stats.projects_in_flight == 1


def test_author_stats_round_1_recommendations(isolated: Path) -> None:
    with db.connection() as conn, db.transaction(conn):
        _seed_fellow(conn, "ada", "Ada")
        _seed_fellow(conn, "reviewer-one", "R One")
        _seed_fellow(conn, "reviewer-two", "R Two")
        _seed_project(conn, "p1", "ada")
        _seed_review(conn, "rv1", "p1", "reviewer-one", "minor", 1)
        _seed_review(conn, "rv2", "p1", "reviewer-two", "major", 1)
    with db.connection() as conn:
        stats = reputation.author_stats(conn, "ada")
    assert stats.round_1_accepts_received == 1
    assert stats.round_1_majors_received == 1


def test_reviewer_stats_buckets_by_round(isolated: Path) -> None:
    with db.connection() as conn, db.transaction(conn):
        _seed_fellow(conn, "ada", "Ada")
        _seed_fellow(conn, "reviewer-one", "R One")
        _seed_project(conn, "p1", "ada")
        _seed_review(conn, "rv1", "p1", "reviewer-one", "minor", 1)
        _seed_review(conn, "rv2", "p1", "reviewer-one", "accept", 2)
    with db.connection() as conn:
        stats = reputation.reviewer_stats(conn, "reviewer-one")
    assert stats.reviews_given == 2
    assert stats.by_round[1]["minor"] == 1
    assert stats.by_round[2]["accept"] == 1


def test_reviewer_stats_sticky_major(isolated: Path) -> None:
    """A round-1 major + a round-2 review on the same project = sticky."""
    with db.connection() as conn, db.transaction(conn):
        _seed_fellow(conn, "ada", "Ada")
        _seed_fellow(conn, "reviewer-one", "R One")
        _seed_fellow(conn, "reviewer-two", "R Two")
        _seed_project(conn, "p1", "ada")
        _seed_review(conn, "rv1", "p1", "reviewer-one", "major", 1)
        _seed_review(conn, "rv2", "p1", "reviewer-two", "accept", 2)  # someone else's r2
    with db.connection() as conn:
        stats = reputation.reviewer_stats(conn, "reviewer-one")
    assert stats.sticky_majors == 1


def test_reviewer_stats_non_sticky_major(isolated: Path) -> None:
    """A round-1 major without any round-2 = not sticky (didn't revise)."""
    with db.connection() as conn, db.transaction(conn):
        _seed_fellow(conn, "ada", "Ada")
        _seed_fellow(conn, "reviewer-one", "R One")
        _seed_project(conn, "p1", "ada")
        _seed_review(conn, "rv1", "p1", "reviewer-one", "major", 1)
    with db.connection() as conn:
        stats = reputation.reviewer_stats(conn, "reviewer-one")
    assert stats.sticky_majors == 0


def test_cohort_reputation_lists_all_active(isolated: Path) -> None:
    with db.connection() as conn, db.transaction(conn):
        _seed_fellow(conn, "ada", "Ada")
        _seed_fellow(conn, "bram", "Bram", rank="senior_fellow")
    with db.connection() as conn:
        cohort = reputation.cohort_reputation(conn)
    assert {r.fellow_id for r in cohort} == {"ada", "bram"}


def test_render_cohort_brief_contains_names(isolated: Path) -> None:
    with db.connection() as conn, db.transaction(conn):
        _seed_fellow(conn, "ada", "Ada")
        _seed_fellow(conn, "bram", "Bram")
    cohort = reputation.load_cohort()
    text = reputation.render_cohort_brief(cohort)
    assert "Ada" in text
    assert "Bram" in text
    assert "reviews given" in text


def test_render_cohort_brief_empty() -> None:
    assert "No active Fellows" in reputation.render_cohort_brief([])


def test_render_fellow_dossier_includes_signals(isolated: Path) -> None:
    with db.connection() as conn, db.transaction(conn):
        _seed_fellow(conn, "ada", "Ada")
        _seed_project(conn, "p1", "ada")
    rep = reputation.load_fellow("ada")
    assert rep is not None
    dossier = reputation.render_fellow_dossier(rep)
    assert "Ada" in dossier
    assert "publications: 1" in dossier
    assert "Sticky majors" in dossier


def test_load_fellow_returns_none_for_unknown(isolated: Path) -> None:
    assert reputation.load_fellow("nonexistent") is None
