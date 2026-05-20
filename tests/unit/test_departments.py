"""Tests for the departments module."""

from __future__ import annotations

from pathlib import Path

import pytest

from institute import db, departments
from institute import fellow as fellow_mod
from institute.fellow import Genome


def _register(conn, fellow_id: str, rank: str = "fellow") -> None:
    g = Genome(
        id=fellow_id,
        name=fellow_id.capitalize(),
        rank=rank,
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
        _register(conn, "ada", rank="senior_fellow")
        _register(conn, "henri", rank="senior_fellow")
        _register(conn, "michel")
    return tmp_path


def test_create_idempotent(isolated: Path) -> None:
    with db.connection() as conn, db.transaction(conn):
        d1 = departments.create(
            conn, name="Mathematics", description="Pure math + formal methods"
        )
        d2 = departments.create(
            conn, name="Mathematics", description="Updated description"
        )
    assert d1.id == d2.id == "mathematics"
    assert d2.description == "Updated description"


def test_add_and_list_members(isolated: Path) -> None:
    with db.connection() as conn, db.transaction(conn):
        departments.create(conn, name="Math", description="x")
        departments.add_member(conn, department_id="math", fellow_id="ada")
        departments.add_member(conn, department_id="math", fellow_id="henri")
    with db.connection() as conn:
        ids = departments.member_ids(conn, "math")
    assert set(ids) == {"ada", "henri"}


def test_set_chair_also_adds_membership(isolated: Path) -> None:
    with db.connection() as conn, db.transaction(conn):
        departments.create(conn, name="Math", description="x")
        departments.set_chair(conn, department_id="math", fellow_id="ada")
    with db.connection() as conn:
        d = departments.get(conn, "math")
        ids = departments.member_ids(conn, "math")
    assert d.chair_fellow_id == "ada"
    assert "ada" in ids


def test_for_fellow_returns_open_departments(isolated: Path) -> None:
    with db.connection() as conn, db.transaction(conn):
        departments.create(conn, name="Math", description="x")
        departments.create(conn, name="Biology", description="y")
        departments.add_member(conn, department_id="math", fellow_id="ada")
        departments.add_member(conn, department_id="biology", fellow_id="ada")
        departments.close(conn, "biology")
    with db.connection() as conn:
        depts = departments.for_fellow(conn, "ada")
    assert [d.id for d in depts] == ["math"]  # closed biology omitted


def test_is_initialized(isolated: Path) -> None:
    with db.connection() as conn:
        assert not departments.is_initialized(conn)
    with db.connection() as conn, db.transaction(conn):
        departments.create(conn, name="Math", description="x")
    with db.connection() as conn:
        assert departments.is_initialized(conn)


def test_same_department(isolated: Path) -> None:
    with db.connection() as conn, db.transaction(conn):
        departments.create(conn, name="Math", description="x")
        departments.create(conn, name="Bio", description="y")
        departments.add_member(conn, department_id="math", fellow_id="ada")
        departments.add_member(conn, department_id="math", fellow_id="henri")
        departments.add_member(conn, department_id="bio", fellow_id="michel")
    with db.connection() as conn:
        assert departments.same_department(conn, fellow_a="ada", fellow_b="henri")
        assert not departments.same_department(
            conn, fellow_a="ada", fellow_b="michel"
        )


def test_same_department_false_when_uninitialized(isolated: Path) -> None:
    with db.connection() as conn:
        assert not departments.same_department(
            conn, fellow_a="ada", fellow_b="henri"
        )


def test_create_rejects_empty(isolated: Path) -> None:
    with db.connection() as conn, db.transaction(conn):
        with pytest.raises(ValueError):
            departments.create(conn, name="", description="x")
        with pytest.raises(ValueError):
            departments.create(conn, name="x", description="")


def test_remove_member(isolated: Path) -> None:
    with db.connection() as conn, db.transaction(conn):
        departments.create(conn, name="Math", description="x")
        departments.add_member(conn, department_id="math", fellow_id="ada")
        departments.remove_member(conn, department_id="math", fellow_id="ada")
    with db.connection() as conn:
        assert departments.member_ids(conn, "math") == []
