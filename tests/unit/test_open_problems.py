"""Tests for the Open Problems standing list."""

from __future__ import annotations

from pathlib import Path

import pytest

from institute import open_problems as op


def test_add_creates_file_and_loads_round_trip(isolated: Path) -> None:
    problem = op.add(
        title="When does noise floor exceed effect?",
        body="A standing methodological question about ceiling effects.",
        tags=["methodology", "llm-empirical"],
        opened_by="founder",
    )
    assert problem.slug == "when-does-noise-floor-exceed-effect"
    assert problem.status == "open"
    assert problem.path.is_file()
    # Default project_id is "standing"; verify the path layout.
    assert problem.path.parent.name == op.STANDING

    loaded = op.get(problem.slug, op.STANDING)
    assert loaded is not None
    assert loaded.title == problem.title
    assert loaded.tags == ["methodology", "llm-empirical"]
    assert loaded.opened_by == "founder"
    assert loaded.source_project_id == op.STANDING


def test_add_rejects_duplicate_slug_in_same_project(isolated: Path) -> None:
    op.add(title="A question", body="body", opened_by="founder")
    with pytest.raises(ValueError, match="already exists"):
        op.add(title="A question", body="other body", opened_by="founder")


def test_same_slug_allowed_across_different_projects(isolated: Path) -> None:
    """Two papers raising the same question is not a collision. Each
    file lives under its own project subdir."""
    a = op.add(title="A shared question", body="b1", project_id="paper-a")
    b = op.add(title="A shared question", body="b2", project_id="paper-b")
    assert a.slug == b.slug == "a-shared-question"
    assert a.path != b.path
    assert a.path.parent.name == "paper-a"
    assert b.path.parent.name == "paper-b"
    assert op.get(a.slug, "paper-a").body == "b1"
    assert op.get(b.slug, "paper-b").body == "b2"


def test_load_all_orders_open_first_then_resolved(isolated: Path) -> None:
    p1 = op.add(title="First", body="b", opened_by="founder")
    op.add(title="Second", body="b", opened_by="founder")
    op.add(title="Third", body="b", opened_by="founder")
    op.resolve(p1, by_project="proj-1", by_fellow="ada")

    listed = op.load_all()
    statuses = [p.status for p in listed]
    # Open before resolved
    assert statuses.index("resolved") > max(i for i, s in enumerate(statuses) if s == "open")


def test_resolve_marks_and_records_metadata(isolated: Path) -> None:
    problem = op.add(title="Test problem", body="body", opened_by="founder")
    resolved = op.resolve(problem, by_project="proj-42", by_fellow="ada")
    assert resolved.status == "resolved"
    assert resolved.resolved_by_project == "proj-42"
    assert resolved.resolved_by_fellow == "ada"
    assert resolved.resolved_at is not None
    # Re-resolving is rejected
    with pytest.raises(ValueError, match="already resolved"):
        op.resolve(problem, by_project="proj-43", by_fellow="ada")


def test_resolve_missing_problem_raises(isolated: Path) -> None:
    ghost = op.OpenProblem(
        slug="nonexistent",
        title="x",
        body="x",
        status="open",
        opened_at="2026-05-20T00:00:00+00:00",
        opened_by="founder",
        tags=[],
        source_project_id=op.STANDING,
    )
    with pytest.raises(ValueError, match="No such open problem"):
        op.resolve(ghost, by_project="p", by_fellow="f")


def test_open_problems_filters_to_open(isolated: Path) -> None:
    a = op.add(title="A", body="b", opened_by="founder")
    op.add(title="B", body="b", opened_by="founder")
    op.resolve(a, by_project="p", by_fellow="f")
    open_only = op.open_problems()
    assert {p.slug for p in open_only} == {"b"}


def test_render_summary_md_empty_states_sentinel(isolated: Path) -> None:
    rendered = op.render_summary_md()
    assert "Open Problems" in rendered
    assert "(None on the standing list" in rendered


def test_render_summary_md_lists_open_problems(isolated: Path) -> None:
    op.add(title="A Question", body="Body of A.", tags=["x"], opened_by="founder")
    op.add(title="Another", body="Body of Another.", opened_by="founder")
    rendered = op.render_summary_md()
    assert "a-question" in rendered
    assert "another" in rendered
    assert "Body of A." in rendered
    assert "[x]" in rendered


def test_slugify_normalizes_punctuation(isolated: Path) -> None:
    problem = op.add(
        title="What happens when X / Y collides???",
        body="body",
        opened_by="founder",
    )
    assert problem.slug == "what-happens-when-x-y-collides"


def test_frontmatter_round_trip_preserves_tags(isolated: Path) -> None:
    op.add(
        title="With tags",
        body="b",
        tags=["alpha", "beta", "gamma"],
        opened_by="founder",
    )
    loaded = op.get("with-tags", op.STANDING)
    assert loaded is not None
    assert loaded.tags == ["alpha", "beta", "gamma"]


def test_for_project_reads_from_project_subdir(isolated: Path) -> None:
    op.add(title="X", body="b", project_id="proj-a")
    op.add(title="Y", body="b", project_id="proj-a")
    op.add(title="Z", body="b", project_id="proj-b")
    op.add(title="Standing", body="b")  # default "standing"

    a = op.for_project("proj-a")
    b = op.for_project("proj-b")
    standing = op.for_project(op.STANDING)
    assert {p.slug for p in a} == {"x", "y"}
    assert {p.slug for p in b} == {"z"}
    assert {p.slug for p in standing} == {"standing"}
    assert op.for_project("nonexistent") == []


def test_mark_promoted_and_discard_keep_file(isolated: Path) -> None:
    p = op.add(title="P", body="b", project_id="paper-a")
    q = op.add(title="Q", body="b", project_id="paper-a")
    op.mark_promoted(p)
    op.discard(q)

    promoted = op.get("p", "paper-a")
    discarded = op.get("q", "paper-a")
    assert promoted is not None
    assert promoted.status == "promoted"
    assert discarded is not None
    assert discarded.status == "dropped"
    # Neither should still appear in `open_problems()`.
    assert {x.slug for x in op.open_problems()} == set()


def test_add_rejects_empty_project_id(isolated: Path) -> None:
    with pytest.raises(ValueError, match="project_id is required"):
        op.add(title="x", body="b", project_id="")
