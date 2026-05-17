"""Tests for the publish workflow's pure helpers."""

from datetime import UTC, datetime

from institute.workflows import publish


def test_strip_title_pulls_h1() -> None:
    draft = "# A first finding\n\nThe lede paragraph.\n\nMore body.\n"
    title, body = publish._strip_title_heading(draft)
    assert title == "A first finding"
    assert body.startswith("The lede paragraph.")


def test_strip_title_when_missing_returns_empty() -> None:
    draft = "Just some text with no heading.\n"
    title, body = publish._strip_title_heading(draft)
    assert title == ""
    assert body == draft


def test_extract_abstract_picks_first_paragraph() -> None:
    body = "First short lede paragraph.\n\nSecond paragraph.\n"
    assert publish._extract_abstract(body) == "First short lede paragraph."


def test_extract_abstract_skips_headings_and_blockquotes() -> None:
    body = "## A heading\n\n> a quote\n\nThe actual lede.\n"
    assert publish._extract_abstract(body) == "The actual lede."


def test_extract_abstract_returns_none_when_only_headings() -> None:
    body = "## h1\n\n### h2\n"
    assert publish._extract_abstract(body) is None


def test_yaml_string_escapes_quotes_and_newlines() -> None:
    assert publish._yaml_string('a "quoted" string') == '"a \\"quoted\\" string"'
    assert publish._yaml_string("line one\nline two") == '"line one line two"'


def test_yaml_list_empty_and_populated() -> None:
    assert publish._yaml_list([]) == "[]"
    assert publish._yaml_list(["Hypatia", "Diderot"]) == '["Hypatia", "Diderot"]'


def test_publication_markdown_includes_required_frontmatter() -> None:
    text = publish._publication_markdown(
        title="A finding",
        body="The body of the work.\n",
        authors=["Hypatia"],
        reviewers=["Diderot", "Margaret Cavendish"],
        published_at=datetime(2026, 5, 17, tzinfo=UTC),
        project_id="2026-05-17-a-finding-ab12",
        abstract="A short summary.",
        has_notebook=True,
        has_reviews=True,
    )
    assert text.startswith("---\n")
    assert 'title: "A finding"' in text
    assert 'authors: ["Hypatia"]' in text
    assert "publishedAt: 2026-05-17" in text
    assert "hasNotebook: true" in text
    assert "hasReviews: true" in text
    assert 'projectId: "2026-05-17-a-finding-ab12"' in text
    assert text.rstrip().endswith("The body of the work.")
