"""Tests for peer_review's round-aware bookkeeping.

These tests exercise the slot-picking and existing-reviews helpers without
invoking Claude. They guard against a regression in which
_existing_reviews_in_round forgot to filter by round, causing round-2
peer review to skip itself and jump to editorial.
"""

from datetime import UTC, datetime
from pathlib import Path

import pytest

from institute import db
from institute import fellow as fellow_mod
from institute.fellow import Genome
from institute.workflows.peer_review import (
    _existing_reviews_in_round,
    _pick_review_slots,
)


def _genome(name: str, spec: str) -> Genome:
    return Genome(
        id=name.lower().replace(" ", "-"),
        name=name,
        rank="fellow",
        model="claude-sonnet-4-6",
        specialization=spec,
        system_prompt_addendum=("Short addendum. " * 10).strip(),
        allowed_tools=["Read"],
    )


@pytest.fixture()
def seeded(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> str:
    monkeypatch.setattr(fellow_mod, "GENOMES", tmp_path / "genomes")
    monkeypatch.setattr(fellow_mod, "FELLOWS", tmp_path / "fellows")
    db_path = tmp_path / "institute.db"
    monkeypatch.setattr(db, "DB_PATH", db_path)
    db.initialize(db_path)

    fellows = [
        _genome("Ada Lovelace", "applied"),
        _genome("Henri Poincare", "theory"),
        _genome("Pierre Bayle", "critical review"),
        _genome("Michel de Montaigne", "long-form essay"),
    ]
    (tmp_path / "genomes").mkdir(exist_ok=True)
    for g in fellows:
        g.write(tmp_path / "genomes" / f"{g.id}.json")

    project_id = "proj-round-test"
    now = datetime.now(UTC).isoformat(timespec="seconds")
    with db.connection() as conn, db.transaction(conn):
        for g in fellows:
            fellow_mod.register(conn, g)
        conn.execute(
            "INSERT INTO projects "
            "(id, title, state, lead_fellow_id, draft_path, review_round, "
            " created_at, updated_at) "
            "VALUES (?, ?, ?, ?, ?, ?, ?, ?)",
            (
                project_id,
                "x",
                "peer_reviewing",
                "ada-lovelace",
                "draft.md",
                2,
                now,
                now,
            ),
        )
        # Three round-1 reviews already on file.
        for i, (fid, role, rec) in enumerate(
            [
                ("henri-poincare", "outside", "minor"),
                ("michel-de-montaigne", "primary", "minor"),
                ("pierre-bayle", "secondary", "major"),
            ]
        ):
            conn.execute(
                "INSERT INTO reviews "
                "(id, project_id, reviewer_id, role, recommendation, "
                " confidence, content_path, submitted_at, dissent, round) "
                "VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
                (
                    f"r-{i}",
                    project_id,
                    fid,
                    role,
                    rec,
                    "confident",
                    f"x/{fid}.md",
                    now,
                    0,
                    1,
                ),
            )
    return project_id


def test_existing_reviews_in_round_filters_by_round(seeded: str) -> None:
    project_id = seeded
    with db.connection() as conn:
        # Round-1 reviews exist; round-2 reviews do not.
        assert _existing_reviews_in_round(conn, project_id, 1) == {
            "henri-poincare",
            "michel-de-montaigne",
            "pierre-bayle",
        }
        assert _existing_reviews_in_round(conn, project_id, 2) == set()


def test_pick_review_slots_round_2_reuses_round_1_reviewers(seeded: str) -> None:
    project_id = seeded
    with db.connection() as conn:
        slots = _pick_review_slots(conn, project_id, "ada-lovelace", 2)
    by_id = {s.reviewer_id: s.role for s in slots}
    assert by_id == {
        "henri-poincare": "outside",
        "michel-de-montaigne": "primary",
        "pierre-bayle": "secondary",
    }


def test_round_2_has_work_to_do_before_any_round_2_reviews(seeded: str) -> None:
    """Regression for the bug where round-2 skipped straight to editorial."""
    project_id = seeded
    with db.connection() as conn:
        slots = _pick_review_slots(conn, project_id, "ada-lovelace", 2)
        done = _existing_reviews_in_round(conn, project_id, 2)
    remaining = [s for s in slots if s.reviewer_id not in done]
    assert len(remaining) == 3, "Round 2 must start with all 3 reviewers pending"


def test_round_1_primary_is_closest_discipline(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    """Round-1 primary should be the candidate most similar to the lead's specialization."""
    monkeypatch.setattr(fellow_mod, "GENOMES", tmp_path / "genomes")
    monkeypatch.setattr(fellow_mod, "FELLOWS", tmp_path / "fellows")
    db_path = tmp_path / "institute.db"
    monkeypatch.setattr(db, "DB_PATH", db_path)
    db.initialize(db_path)
    (tmp_path / "genomes").mkdir(exist_ok=True)

    lead = _genome("Ada Builder", "computational demonstration and reproducible artifacts")
    twin = _genome("Tina Twin", "computational demonstration of reproducible code")
    cousin = _genome("Cassie Cousin", "computational analysis and reproducible methods")
    stranger = _genome("Sam Stranger", "long-form essayistic prose")
    for g in (lead, twin, cousin, stranger):
        g.write(tmp_path / "genomes" / f"{g.id}.json")
    now = datetime.now(UTC).isoformat(timespec="seconds")
    with db.connection() as conn, db.transaction(conn):
        for g in (lead, twin, cousin, stranger):
            fellow_mod.register(conn, g)
        conn.execute(
            "INSERT INTO projects "
            "(id, title, state, lead_fellow_id, draft_path, review_round, "
            " created_at, updated_at) "
            "VALUES (?, ?, ?, ?, ?, ?, ?, ?)",
            ("proj-disc", "x", "drafted", lead.id, "draft.md", 1, now, now),
        )

    with db.connection() as conn:
        slots = _pick_review_slots(conn, "proj-disc", lead.id, 1)
    by_role = {s.role: s.reviewer_id for s in slots}
    assert by_role["primary"] == twin.id, "primary should be the closest-discipline Fellow"
    assert by_role["outside"] == stranger.id, "outside should be the most-distant Fellow"
    # secondary is whatever's left in the middle
    assert by_role["secondary"] == cousin.id


def test_round_1_rotates_among_equally_distant_reviewers(
    tmp_path: Path, monkeypatch: pytest.MonkeyPatch
) -> None:
    """When multiple candidates score the same, the least-recent reviewer wins."""
    monkeypatch.setattr(fellow_mod, "GENOMES", tmp_path / "genomes")
    monkeypatch.setattr(fellow_mod, "FELLOWS", tmp_path / "fellows")
    db_path = tmp_path / "institute.db"
    monkeypatch.setattr(db, "DB_PATH", db_path)
    db.initialize(db_path)
    (tmp_path / "genomes").mkdir(exist_ok=True)

    # Lead has a single-word specialization; the three candidates share no
    # tokens with it, so similarity = 0 for all three. Rotation breaks ties.
    lead = _genome("Lead", "alpha")
    busy = _genome("Busy", "beta")  # has a very recent review
    medium = _genome("Medium", "gamma")  # has an older review
    fresh = _genome("Fresh", "delta")  # has never reviewed
    for g in (lead, busy, medium, fresh):
        g.write(tmp_path / "genomes" / f"{g.id}.json")
    now = datetime.now(UTC).isoformat(timespec="seconds")
    with db.connection() as conn, db.transaction(conn):
        for g in (lead, busy, medium, fresh):
            fellow_mod.register(conn, g)
        conn.execute(
            "INSERT INTO projects "
            "(id, title, state, lead_fellow_id, draft_path, review_round, "
            " created_at, updated_at) "
            "VALUES (?, ?, ?, ?, ?, ?, ?, ?)",
            ("proj-rot", "x", "drafted", lead.id, "draft.md", 1, now, now),
        )
        # Add a dummy project so reviews have something to FK to.
        conn.execute(
            "INSERT INTO projects "
            "(id, title, state, lead_fellow_id, draft_path, review_round, "
            " created_at, updated_at) "
            "VALUES (?, ?, ?, ?, ?, ?, ?, ?)",
            ("proj-history", "h", "published", lead.id, "draft.md", 1, now, now),
        )
        conn.execute(
            "INSERT INTO reviews "
            "(id, project_id, reviewer_id, role, recommendation, confidence, "
            " content_path, submitted_at, dissent, round) "
            "VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
            ("r-busy", "proj-history", busy.id, "primary", "minor",
             "confident", "x", "2026-05-18T20:00:00+00:00", 0, 1),
        )
        conn.execute(
            "INSERT INTO reviews "
            "(id, project_id, reviewer_id, role, recommendation, confidence, "
            " content_path, submitted_at, dissent, round) "
            "VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
            ("r-medium", "proj-history", medium.id, "primary", "minor",
             "confident", "x", "2026-05-01T10:00:00+00:00", 0, 1),
        )

    with db.connection() as conn:
        slots = _pick_review_slots(conn, "proj-rot", lead.id, 1)
    by_role = {s.role: s.reviewer_id for s in slots}
    # All three score 0 similarity. Rotation order should be: fresh
    # (never reviewed) first, medium (older review) second, busy
    # (recent review) last.
    # Outside is picked first (lowest similarity, oldest reviewer) so
    # `fresh` becomes outside; primary then takes the most-recent oldest
    # among remaining = `medium`.
    assert by_role["outside"] == fresh.id
    assert by_role["primary"] == medium.id
    assert by_role["secondary"] == busy.id
