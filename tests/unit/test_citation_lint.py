"""Tests for the publish-time numeric-citation lint."""

from __future__ import annotations

import pytest

from institute import citation_lint

# ---------------------------------------------------------------------------
# Clean drafts
# ---------------------------------------------------------------------------


def test_empty_body_is_clean() -> None:
    assert citation_lint.find_violations("") == []


def test_prose_without_citations_is_clean() -> None:
    body = (
        "This is a normal essay paragraph. It cites another "
        "publication by title: [*The Other Piece*](posts/something/). "
        "No issue numbers anywhere."
    )
    assert citation_lint.find_violations(body) == []
    citation_lint.check(body)  # must not raise


def test_headings_are_not_citations() -> None:
    body = "# Title\n\n## Section\n\n### Subsection\n\nbody"
    assert citation_lint.find_violations(body) == []


def test_single_digit_anchors_are_ignored() -> None:
    """A bare `#0` or `#1` in prose is too common to flag; only two+
    digit forms (and bracketed/parenthesized forms) are violations."""
    body = "Footnote #1 explains the convention."
    assert citation_lint.find_violations(body) == []


# ---------------------------------------------------------------------------
# Violations: the patterns we've seen
# ---------------------------------------------------------------------------


def test_bracketed_citation_detected() -> None:
    body = "See [#03 *Algorithmic Stability*](posts/x/) for context."
    violations = citation_lint.find_violations(body)
    assert len(violations) == 1
    assert "#03" in violations[0]


def test_parenthesized_citation_detected() -> None:
    body = "Consistent with prior work (#04) on tokenization."
    violations = citation_lint.find_violations(body)
    assert violations == ["(#04)"]


def test_bare_two_digit_citation_detected() -> None:
    body = "The #09 piece ran a different design."
    violations = citation_lint.find_violations(body)
    assert violations == ["#09"]


def test_multiple_violations_collected() -> None:
    body = (
        "Following [#04](posts/a/) and [#11](posts/b/), the present "
        "work extends #09's design and contradicts (#03)."
    )
    violations = citation_lint.find_violations(body)
    assert len(violations) >= 4


# ---------------------------------------------------------------------------
# Code-block exclusion
# ---------------------------------------------------------------------------


def test_fenced_code_block_does_not_trigger() -> None:
    body = (
        "Here is a shell snippet:\n\n```bash\n# 04 is just a comment label\n```\n\nEnd of section."
    )
    assert citation_lint.find_violations(body) == []


def test_inline_code_does_not_trigger() -> None:
    body = "The literal pattern `#04` is what we forbid in prose."
    assert citation_lint.find_violations(body) == []


def test_violation_outside_code_still_caught() -> None:
    """A code block does not protect violations elsewhere in the body."""
    body = "Cite by title, not by #04 in the body.\n\n```python\n# 99 is fine inside code\n```\n"
    violations = citation_lint.find_violations(body)
    assert violations == ["#04"]


# ---------------------------------------------------------------------------
# check() raises
# ---------------------------------------------------------------------------


def test_check_raises_on_violation() -> None:
    body = "Following (#04)."
    with pytest.raises(citation_lint.CitationLintError) as info:
        citation_lint.check(body)
    assert info.value.violations == ["(#04)"]
    assert "Cite by title and link" in str(info.value)


def test_check_passes_clean_body() -> None:
    citation_lint.check("Clean body with no citations.")


def test_citation_lint_error_subclasses_runtime_error() -> None:
    """The autopilot's broader exception catch sweeps this up."""
    exc = citation_lint.CitationLintError(["#04"])
    assert isinstance(exc, RuntimeError)
