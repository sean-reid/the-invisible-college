"""Tests for the Centers module (Chapter 2)."""

from __future__ import annotations

from datetime import UTC, datetime, timedelta
from pathlib import Path

import pytest

from institute import centers, db
from institute import fellow as fellow_mod
from institute.fellow import Genome


def _register(conn, fid: str) -> None:
    g = Genome(
        id=fid,
        name=fid.capitalize(),
        rank="fellow",
        model="claude-sonnet-4-6",
        specialization="general",
        system_prompt_addendum=("body " * 60).strip(),
        allowed_tools=["Read"],
    )
    g.write(fellow_mod.genome_path(fid))
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


def test_open_creates_center(isolated: Path) -> None:
    with db.connection() as conn, db.transaction(conn):
        c = centers.open_center(
            conn,
            name="Computation and Form",
            motivation="Where do morphological and computational generalization meet?",
        )
    assert c.id == "computation-and-form"
    assert c.closed_at is None


def test_open_with_custom_term(isolated: Path) -> None:
    with db.connection() as conn, db.transaction(conn):
        c = centers.open_center(
            conn,
            name="Brief Center",
            motivation="A short one.",
            term_days=30,
        )
    opened = datetime.fromisoformat(c.opened_at)
    closes = datetime.fromisoformat(c.closes_at)
    # 30 days within a small tolerance.
    assert timedelta(days=29) <= (closes - opened) <= timedelta(days=31)


def test_add_member_and_member_ids(isolated: Path) -> None:
    with db.connection() as conn, db.transaction(conn):
        c = centers.open_center(conn, name="Xyz", motivation="y")
        centers.add_member(conn, center_id=c.id, fellow_id="ada", role="convener")
        centers.add_member(conn, center_id=c.id, fellow_id="henri")
    with db.connection() as conn:
        ids = centers.member_ids(conn, c.id)
    assert set(ids) == {"ada", "henri"}


def test_close_records_report(isolated: Path) -> None:
    with db.connection() as conn, db.transaction(conn):
        c = centers.open_center(conn, name="Xyz", motivation="y")
        centers.close(
            conn,
            center_id=c.id,
            report_path="archive/centers/x/report.md",
        )
    with db.connection() as conn:
        got = centers.get(conn, c.id)
    assert got.closed_at is not None
    assert got.report_path == "archive/centers/x/report.md"


def test_list_open_omits_closed(isolated: Path) -> None:
    with db.connection() as conn, db.transaction(conn):
        a = centers.open_center(conn, name="Ax", motivation="a")
        b = centers.open_center(conn, name="Bx", motivation="b")
        centers.close(conn, center_id=a.id)
    with db.connection() as conn:
        listed = [c.id for c in centers.list_open(conn)]
    assert listed == [b.id]


def test_expired_unclosed(isolated: Path) -> None:
    past = (datetime.now(UTC) - timedelta(days=10)).isoformat(timespec="seconds")
    with db.connection() as conn, db.transaction(conn):
        c = centers.open_center(conn, name="Xyz", motivation="y")
        # Directly age its closes_at into the past.
        conn.execute(
            "UPDATE centers SET closes_at = ? WHERE id = ?", (past, c.id)
        )
    with db.connection() as conn:
        expired = centers.expired_unclosed(conn)
    assert [e.id for e in expired] == [c.id]


def test_open_validates_empty_inputs(isolated: Path) -> None:
    with db.connection() as conn, db.transaction(conn):
        with pytest.raises(ValueError):
            centers.open_center(conn, name="", motivation="x")
        with pytest.raises(ValueError):
            centers.open_center(conn, name="xy", motivation="")
        with pytest.raises(ValueError):
            centers.open_center(conn, name="xy", motivation="y", term_days=0)
