"""Tests for the advisor-review revision-round cap.

Mirrors the panel cap one layer up. After MAX_ADVISOR_REVISE_ROUNDS
prior revisions, an advisor `revise` vote is overridden and the
project routes to AWAITING_QUALIFYING_PANEL anyway. The advisor's
feedback stands as institutional record.
"""

from __future__ import annotations

from pathlib import Path

import pytest

from institute import db, paths
from institute.workflows import advisor_review


@pytest.fixture()
def isolated(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> Path:
    archive = tmp_path / "archive"
    archive.mkdir(parents=True)
    db_path = tmp_path / "institute.db"
    monkeypatch.setattr(db, "DB_PATH", db_path)
    monkeypatch.setattr(paths, "ROOT", tmp_path)
    monkeypatch.setattr(paths, "ARCHIVE", archive)
    db.initialize(db_path)
    return tmp_path


def test_max_advisor_revise_rounds_is_three() -> None:
    assert advisor_review.MAX_ADVISOR_REVISE_ROUNDS == 3


def test_count_prior_revisions_zero_initially(isolated: Path) -> None:
    with db.connection() as conn:
        assert advisor_review._count_prior_revisions(conn, "p1") == 0


def test_count_prior_revisions_counts_revision_rows(isolated: Path) -> None:
    with db.connection() as conn, db.transaction(conn):
        for i in range(4):
            conn.execute(
                "INSERT INTO audit_log (at, actor, action, project_id, detail) "
                "VALUES (?, 'lead', 'revision', 'p1', '')",
                (f"2026-05-20T1{i}:00:00+00:00",),
            )
    with db.connection() as conn:
        assert advisor_review._count_prior_revisions(conn, "p1") == 4


def test_count_prior_revisions_scoped_to_project(isolated: Path) -> None:
    """Revisions on other projects don't bleed into this project's count."""
    with db.connection() as conn, db.transaction(conn):
        for pid in ("a", "a", "a", "b"):
            conn.execute(
                "INSERT INTO audit_log (at, actor, action, project_id, detail) "
                "VALUES (datetime('now'), 'lead', 'revision', ?, '')",
                (pid,),
            )
    with db.connection() as conn:
        assert advisor_review._count_prior_revisions(conn, "a") == 3
        assert advisor_review._count_prior_revisions(conn, "b") == 1
