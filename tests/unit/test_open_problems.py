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

    loaded = op.get(problem.slug)
    assert loaded is not None
    assert loaded.title == problem.title
    assert loaded.tags == ["methodology", "llm-empirical"]
    assert loaded.opened_by == "founder"


def test_add_rejects_duplicate_slug(isolated: Path) -> None:
    op.add(title="A question", body="body", opened_by="founder")
    with pytest.raises(ValueError, match="already exists"):
        op.add(title="A question", body="other body", opened_by="founder")


def test_load_all_orders_open_first_then_resolved(isolated: Path) -> None:
    p1 = op.add(title="First", body="b", opened_by="founder")
    op.add(title="Second", body="b", opened_by="founder")
    op.add(title="Third", body="b", opened_by="founder")
    op.resolve(p1.slug, project_id="proj-1", fellow_id="ada")

    listed = op.load_all()
    statuses = [p.status for p in listed]
    # Open before resolved
    assert statuses.index("resolved") > max(i for i, s in enumerate(statuses) if s == "open")


def test_resolve_marks_and_records_metadata(isolated: Path) -> None:
    problem = op.add(title="Test problem", body="body", opened_by="founder")
    resolved = op.resolve(problem.slug, project_id="proj-42", fellow_id="ada")
    assert resolved.status == "resolved"
    assert resolved.resolved_by_project == "proj-42"
    assert resolved.resolved_by_fellow == "ada"
    assert resolved.resolved_at is not None
    # Re-resolving is rejected
    with pytest.raises(ValueError, match="already resolved"):
        op.resolve(problem.slug, project_id="proj-43", fellow_id="ada")


def test_resolve_missing_problem_raises(isolated: Path) -> None:
    with pytest.raises(ValueError, match="No such open problem"):
        op.resolve("nonexistent", project_id="p", fellow_id="f")


def test_open_problems_filters_to_open(isolated: Path) -> None:
    a = op.add(title="A", body="b", opened_by="founder")
    op.add(title="B", body="b", opened_by="founder")
    op.resolve(a.slug, project_id="p", fellow_id="f")
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
    loaded = op.get("with-tags")
    assert loaded is not None
    assert loaded.tags == ["alpha", "beta", "gamma"]
