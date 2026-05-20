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


@pytest.fixture(autouse=True)
def _seeded(isolated: Path) -> None:
    """Seed three Fellows on top of the shared isolated fixture."""
    with db.connection() as conn, db.transaction(conn):
        _register(conn, "ada", rank="senior_fellow")
        _register(conn, "henri", rank="senior_fellow")
        _register(conn, "michel")


def test_create_idempotent(isolated: Path) -> None:
    with db.connection() as conn, db.transaction(conn):
        d1 = departments.create(conn, name="Mathematics", description="Pure math + formal methods")
        d2 = departments.create(conn, name="Mathematics", description="Updated description")
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
        assert not departments.same_department(conn, fellow_a="ada", fellow_b="michel")


def test_same_department_false_when_uninitialized(isolated: Path) -> None:
    with db.connection() as conn:
        assert not departments.same_department(conn, fellow_a="ada", fellow_b="henri")


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


# ---------------------------------------------------------------------------
# archive export
# ---------------------------------------------------------------------------


def test_render_archive_markdown_pins_shape(isolated: Path) -> None:
    """The archive file shape is a public contract the sync script reads.
    Pin it so a refactor cannot silently drop a frontmatter key the blog
    depends on."""
    with db.connection() as conn, db.transaction(conn):
        dept = departments.create(
            conn, name="Math", description="formal methods", chair_fellow_id="ada"
        )
        departments.add_member(conn, department_id="math", fellow_id="henri")

    members = ["ada", "henri"]
    out = departments.render_archive_markdown(department=dept, members=members)
    assert out.startswith("---\n")
    assert 'name: "Math"' in out
    assert "chair: ada" in out
    assert "members:" in out
    assert "  - ada" in out
    assert "  - henri" in out
    # The body carries only the human description (chair + members are
    # rendered by the Astro page from frontmatter).
    assert "formal methods" in out
    assert "../fellows/" not in out


def test_render_archive_markdown_vacant_chair(isolated: Path) -> None:
    with db.connection() as conn, db.transaction(conn):
        dept = departments.create(conn, name="Letters", description="reading texts")
    out = departments.render_archive_markdown(department=dept, members=[])
    # Vacant chair: no `chair:` key in frontmatter (rather than `chair: null`)
    # so the blog's Zod schema's `.nullable().optional()` does not produce
    # a literal string "null".
    assert "chair:" not in out
    assert "members: []" in out


def test_export_to_archive_writes_one_file_per_open_department(
    isolated: Path,
) -> None:
    from institute import paths

    with db.connection() as conn, db.transaction(conn):
        departments.create(conn, name="Math", description="formal methods", chair_fellow_id="ada")
        # `create` does not auto-add the chair as a member; the
        # bootstrap-departments migration adds every member explicitly,
        # including the chair. Mirror that convention here.
        departments.add_member(conn, department_id="math", fellow_id="ada")
        departments.add_member(conn, department_id="math", fellow_id="henri")
        departments.create(conn, name="Bio", description="life sciences")
        departments.create(conn, name="Ghost", description="will be closed")
        departments.close(conn, "ghost")

    with db.connection() as conn:
        written = departments.export_to_archive(conn)

    assert set(written) == {"math", "bio"}, "closed departments are not exported"
    math_path = paths.DEPARTMENTS / "math.md"
    bio_path = paths.DEPARTMENTS / "bio.md"
    assert math_path.is_file()
    assert bio_path.is_file()
    ghost_path = paths.DEPARTMENTS / "ghost.md"
    assert not ghost_path.exists()

    math_md = math_path.read_text(encoding="utf-8")
    assert "chair: ada" in math_md
    assert "  - ada" in math_md
    assert "  - henri" in math_md
    assert "formal methods" in math_md


def test_export_to_archive_is_idempotent(isolated: Path) -> None:
    from institute import paths

    with db.connection() as conn, db.transaction(conn):
        departments.create(conn, name="Math", description="formal methods")
    with db.connection() as conn:
        first = departments.export_to_archive(conn)
        first_text = (paths.DEPARTMENTS / "math.md").read_text(encoding="utf-8")
        second = departments.export_to_archive(conn)
        second_text = (paths.DEPARTMENTS / "math.md").read_text(encoding="utf-8")
    assert first == second
    assert first_text == second_text
