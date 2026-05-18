"""Tests for the archive index that workflows stage in Fellow workspaces."""

from pathlib import Path

import pytest

from institute import archive_index
from institute.archive_index import IndexEntry


@pytest.fixture()
def blog_posts_dir(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> Path:
    posts = tmp_path / "posts"
    posts.mkdir()
    monkeypatch.setattr(archive_index, "BLOG_POSTS", posts)
    return posts


def _write(blog_posts_dir: Path, slug: str, body: str) -> Path:
    path = blog_posts_dir / f"{slug}.md"
    path.write_text(body, encoding="utf-8")
    return path


def test_load_entries_when_no_posts(blog_posts_dir: Path) -> None:
    assert archive_index.load_entries() == []


def test_load_entries_parses_frontmatter(blog_posts_dir: Path) -> None:
    _write(
        blog_posts_dir,
        "a",
        """---
title: "First piece"
issueNumber: 1
authors: ["Ada Lovelace", "Henri Poincare"]
publishedAt: 2026-05-17T22:00:00Z
abstract: "A short summary."
---
Body text here.
""",
    )
    entries = archive_index.load_entries()
    assert len(entries) == 1
    e = entries[0]
    assert e.slug == "a"
    assert e.title == "First piece"
    assert e.issue_number == 1
    assert e.authors == ["Ada Lovelace", "Henri Poincare"]
    assert e.published_at == "2026-05-17"
    assert e.abstract == "A short summary."


def test_load_entries_sorted_by_issue_then_date(blog_posts_dir: Path) -> None:
    _write(blog_posts_dir, "c", '---\ntitle: "C"\nissueNumber: 3\npublishedAt: 2026-05-19\n---\n')
    _write(blog_posts_dir, "a", '---\ntitle: "A"\nissueNumber: 1\npublishedAt: 2026-05-17\n---\n')
    _write(blog_posts_dir, "b", '---\ntitle: "B"\nissueNumber: 2\npublishedAt: 2026-05-18\n---\n')

    entries = archive_index.load_entries()
    assert [e.slug for e in entries] == ["a", "b", "c"]


def test_render_markdown_index_empty_state(blog_posts_dir: Path) -> None:
    text = archive_index.render_markdown_index([])
    assert "first piece the College has produced" in text


def test_render_markdown_index_includes_each_entry(blog_posts_dir: Path) -> None:
    entries = [
        IndexEntry(
            slug="a",
            title="A finding",
            authors=["Ada"],
            published_at="2026-05-17",
            abstract="A short summary.",
            issue_number=1,
        ),
        IndexEntry(
            slug="b",
            title="A different finding",
            authors=["Henri", "Ada"],
            published_at="2026-05-18",
            abstract=None,
            issue_number=2,
        ),
    ]
    text = archive_index.render_markdown_index(entries)
    assert "## #01 A finding" in text
    assert "## #02 A different finding" in text
    assert "**slug:** `a`" in text
    assert "**slug:** `b`" in text
    assert "**authors:** Ada" in text
    assert "**authors:** Henri, Ada" in text
    assert "A short summary." in text
