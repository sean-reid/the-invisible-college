"""Tests for the review_declines tracking module."""

from __future__ import annotations

from pathlib import Path

import pytest

from institute import db, review_declines
from institute import fellow as fellow_mod
from institute.fellow import Genome


def _register(conn, fellow_id: str) -> None:
    g = Genome(
        id=fellow_id,
        name=fellow_id.capitalize(),
        rank="fellow",
        model="claude-sonnet-4-6",
        specialization="general",
        system_prompt_addendum=("body " * 60).strip(),
        allowed_tools=["Read"],
    )
    g.write(fellow_mod.genome_path(fellow_id))
    fellow_mod.register(conn, g)


@pytest.fixture()
def isolated(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> Path:
    monkeypatch.setattr(fellow_mod, "GENOMES", tmp_path / "genomes")
    monkeypatch.setattr(fellow_mod, "FELLOWS", tmp_path / "fellows")
    (tmp_path / "genomes").mkdir()
    db_path = tmp_path / "institute.db"
    monkeypatch.setattr(db, "DB_PATH", db_path)
    db.initialize(db_path)
    with db.connection() as conn, db.transaction(conn):
        _register(conn, "ada")
        _register(conn, "henri")
    return tmp_path


def test_record_and_count(isolated: Path) -> None:
    with db.connection() as conn, db.transaction(conn):
        review_declines.record(conn, fellow_id="ada", reason="scope outside specialization")
        review_declines.record(conn, fellow_id="ada", reason="hidden CoI surfaced")
        review_declines.record(conn, fellow_id="henri", reason="other")
    with db.connection() as conn:
        assert review_declines.count_for(conn, "ada") == 2
        assert review_declines.count_for(conn, "henri") == 1


def test_record_requires_reason(isolated: Path) -> None:
    with db.connection() as conn, db.transaction(conn):
        with pytest.raises(ValueError, match="non-empty"):
            review_declines.record(conn, fellow_id="ada", reason="   ")


def test_list_for_returns_in_chronological_order(isolated: Path) -> None:
    with db.connection() as conn, db.transaction(conn):
        review_declines.record(
            conn, fellow_id="ada", reason="first", at="2026-01-01T00:00:00+00:00"
        )
        review_declines.record(
            conn, fellow_id="ada", reason="second", at="2026-02-01T00:00:00+00:00"
        )
    with db.connection() as conn:
        items = review_declines.list_for(conn, "ada")
    assert [i.reason for i in items] == ["first", "second"]


def test_reliability_label_new() -> None:
    assert review_declines.reliability_label(0, 0) == "new"
    assert review_declines.reliability_label(0, 2) == "new"


def test_reliability_label_reliable() -> None:
    assert review_declines.reliability_label(0, 10) == "reliable"
    assert review_declines.reliability_label(1, 20) == "reliable"  # 1/21 < 10%


def test_reliability_label_mixed() -> None:
    assert review_declines.reliability_label(2, 8) == "mixed"  # 2/10 = 20%


def test_reliability_label_unreliable() -> None:
    assert review_declines.reliability_label(5, 5) == "unreliable"  # 5/10 = 50%
