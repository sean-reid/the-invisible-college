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


def test_extract_abstract_fallback_picks_first_paragraph() -> None:
    body = "First short lede paragraph.\n\nSecond paragraph.\n"
    assert publish._extract_abstract_fallback(body) == "First short lede paragraph."


def test_extract_abstract_fallback_skips_headings_and_blockquotes() -> None:
    body = "## A heading\n\n> a quote\n\nThe actual lede.\n"
    assert publish._extract_abstract_fallback(body) == "The actual lede."


def test_extract_abstract_fallback_returns_none_when_only_headings() -> None:
    body = "## h1\n\n### h2\n"
    assert publish._extract_abstract_fallback(body) is None


def test_extract_abstract_fallback_does_not_truncate() -> None:
    long_para = "x " * 500  # 1000 chars
    body = long_para + "\n\nSecond paragraph.\n"
    out = publish._extract_abstract_fallback(body)
    assert out is not None
    assert len(out) >= 900  # no silent truncation


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
        published_at=datetime(2026, 5, 17, 14, 30, 45, tzinfo=UTC),
        project_id="2026-05-17-a-finding-ab12",
        issue_number=7,
        abstract="A short summary.",
        has_notebook=True,
        has_reviews=True,
    )
    assert text.startswith("---\n")
    assert 'title: "A finding"' in text
    assert "issueNumber: 7" in text
    assert 'authors: ["Hypatia"]' in text
    # Full ISO timestamp, not just a date.
    assert "publishedAt: 2026-05-17T14:30:45Z" in text
    assert "hasNotebook: true" in text
    assert "hasReviews: true" in text
    assert 'projectId: "2026-05-17-a-finding-ab12"' in text
    assert text.rstrip().endswith("The body of the work.")


# ---------------------------------------------------------------------------
# Figure-reference rewriting
# ---------------------------------------------------------------------------


def test_rewrite_figure_refs_promotes_known_filenames() -> None:
    body = "Some prose.\n\n![scatter plot](fig_scatter.png)\n\nMore prose. ![](fig_residuals.png)\n"
    out = publish._rewrite_figure_refs(
        body, project_id="p1", available={"fig_scatter.png", "fig_residuals.png"}
    )
    assert "![scatter plot](/the-invisible-college/figures/p1/fig_scatter.png)" in out
    assert "![](/the-invisible-college/figures/p1/fig_residuals.png)" in out


def test_rewrite_figure_refs_leaves_unknown_filenames_alone() -> None:
    """References whose file was never archived stay broken — the lint
    layer surfaces them rather than the rewrite silently rerouting."""
    body = "![](missing.png)\n"
    out = publish._rewrite_figure_refs(body, project_id="p1", available=set())
    assert out == body


def test_rewrite_figure_refs_does_not_rewrite_absolute_paths() -> None:
    body = "![](/already/absolute/fig.png)\n"
    out = publish._rewrite_figure_refs(body, project_id="p1", available={"fig.png"})
    assert out == body


def test_rewrite_figure_refs_handles_dot_relative_paths() -> None:
    """A `./assets/fig.png` reference resolves by basename if the file
    is archived. The Fellow's intent is still 'this image' - the
    archive layout, not the markdown's directory structure, decides
    where it actually lives at serve time."""
    body = "![](./assets/fig.png)\n"
    out = publish._rewrite_figure_refs(body, project_id="p1", available={"fig.png"})
    assert "/the-invisible-college/figures/p1/fig.png" in out


def test_rewrite_figure_refs_leaves_unresolvable_relative_paths() -> None:
    """If the basename has no match in the archive, the reference is
    left alone so the publish-time hard-fail can surface it."""
    body = "![](./assets/missing.png)\n"
    out = publish._rewrite_figure_refs(body, project_id="p1", available={"other.png"})
    assert out == body


def test_rewrite_figure_refs_ignores_non_image_extensions() -> None:
    body = "![](script.py)\n"
    out = publish._rewrite_figure_refs(body, project_id="p1", available={"script.py"})
    assert out == body


def test_rewrite_figure_refs_handles_uppercase_extensions() -> None:
    body = "![](photo.PNG)\n"
    out = publish._rewrite_figure_refs(body, project_id="p1", available={"photo.PNG"})
    assert "/the-invisible-college/figures/p1/photo.PNG" in out


def test_rewrite_resolves_subdir_flattened_figure_by_basename() -> None:
    """The real-world Stahl bug: Fellow puts the PNG in `analysis/`
    inside the workspace, sweep_figures archives it as
    `analysis--lifetime_heartbeats.png`, but the markdown writes
    `![](lifetime_heartbeats.png)`. Basename match must find it."""
    body = "![Lifetime heartbeats](lifetime_heartbeats.png)\n"
    out = publish._rewrite_figure_refs(
        body, project_id="p1", available={"analysis--lifetime_heartbeats.png"}
    )
    assert (
        "![Lifetime heartbeats](/the-invisible-college/figures/p1/analysis--lifetime_heartbeats.png)"
        in out
    )


def test_rewrite_prefers_exact_match_over_basename() -> None:
    """If both `foo.png` and `subdir--foo.png` are archived, the bare
    reference resolves to the top-level one."""
    body = "![](foo.png)\n"
    out = publish._rewrite_figure_refs(
        body, project_id="p1", available={"foo.png", "subdir--foo.png"}
    )
    assert "/the-invisible-college/figures/p1/foo.png" in out
    assert "subdir--foo.png" not in out


def test_rewrite_leaves_ambiguous_basename_match_alone() -> None:
    """Two flattened candidates with the same basename is ambiguous;
    refuse to guess. The publish-time unresolved-ref check will then
    fail the publish so the operator can fix the reference."""
    body = "![](foo.png)\n"
    out = publish._rewrite_figure_refs(
        body, project_id="p1", available={"a--foo.png", "b--foo.png"}
    )
    assert out == body


def test_unresolved_figure_refs_finds_bare_references() -> None:
    body = "Some prose ![](still_bare.png) and another ![alt](also_bare.jpg) here.\n"
    refs = publish._unresolved_figure_refs(body)
    assert sorted(refs) == ["also_bare.jpg", "still_bare.png"]


def test_unresolved_figure_refs_empty_after_full_rewrite() -> None:
    body = "![](fig.png)\n"
    out = publish._rewrite_figure_refs(body, project_id="p1", available={"fig.png"})
    assert publish._unresolved_figure_refs(out) == []


def test_rewrite_resolves_subdir_prefix_in_markdown() -> None:
    """The egg-paper regression: the Fellow wrote
    `![](figures/fig3.png)` (subdir prefix in the markdown ref);
    sweep_figures archived the workspace file as
    `figures--fig3.png` (flatten with `--`). The rewriter must
    translate the slash to `--` and resolve."""
    body = "![Order residuals](figures/fig3_order_residuals.png)\n"
    out = publish._rewrite_figure_refs(
        body,
        project_id="p1",
        available={"figures--fig3_order_residuals.png"},
    )
    assert (
        "![Order residuals](/the-invisible-college/figures/p1/figures--fig3_order_residuals.png)"
        in out
    )


def test_rewrite_subdir_prefix_falls_back_to_basename() -> None:
    """If subdir-translation finds nothing but basename-suffix
    matches a single archived figure, use that."""
    body = "![](figures/fig3.png)\n"
    out = publish._rewrite_figure_refs(body, project_id="p1", available={"analysis--fig3.png"})
    assert "/the-invisible-college/figures/p1/analysis--fig3.png" in out


def test_unresolved_figure_refs_catches_subdir_prefix() -> None:
    """A `figures/X.png` ref with no matching archive entry must be
    surfaced by `_unresolved_figure_refs` so the publish hard-fail
    catches it instead of letting CI discover the broken markdown."""
    body = "![](figures/missing.png)\n"
    out = publish._rewrite_figure_refs(body, project_id="p1", available=set())
    assert out == body  # left alone for the lint to catch
    refs = publish._unresolved_figure_refs(out)
    assert "figures/missing.png" in refs


def test_normalize_display_math_splits_inline_open_close() -> None:
    """The transfer-condition regression: `$$\\begin{array}...
    \\end{array}$$` with the delimiter glued to math content
    on the same line. remark-math fails to recognize it as block
    math; falls back to literal rendering. Normalizer must split
    into standalone-`$$` form."""
    body = (
        "Said in a diagram:\n"
        "$$\\begin{array}{ccc}\n"
        "a & b & c \\\\\n"
        "\\end{array}$$\n"
        "\n"
        "Next paragraph.\n"
    )
    out = publish._normalize_display_math(body)
    assert "\n$$\n\\begin{array}{ccc}\n" in out
    assert "\\end{array}\n$$" in out
    # Blank line inserted before `$$` so the block-level parser sees
    # it cleanly.
    assert "Said in a diagram:\n\n$$\n" in out


def test_normalize_display_math_leaves_single_line_blocks_alone() -> None:
    """Single-line `$$...$$` is valid inline-display math that remark-
    math handles correctly. Don't touch it."""
    body = "and so $$x = 1 + y$$ follows.\n"
    assert publish._normalize_display_math(body) == body


def test_normalize_display_math_leaves_already_normalized_alone() -> None:
    body = "\n$$\n\\begin{array}{c}\na\n\\end{array}\n$$\n"
    out = publish._normalize_display_math(body)
    assert out == body
