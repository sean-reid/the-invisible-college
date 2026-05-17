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
