"""Publish-time lint: refuse drafts that cite other publications by number.

The home page enumerates publications in reverse-chronological order
without any stable visible numbering, so a `#NN` reference in a
publication does not resolve to anything a reader can locate. The
writing briefs forbid this pattern; this module is the hard tripwire
that catches a draft that slipped through anyway.

The lint scans the body markdown (with fenced code blocks stripped so
shell prompts like `# 04` or Python comments don't false-positive) for
the three citation-by-number forms we've seen in practice:

  - `[#NN ...]` or `[#NN]`   bracketed citation prefix
  - `(#NN)`                  parenthesized citation
  - `#NN` standalone         the bare prefix, two or more digits

Headings (`# Title`, `## Section`) are not flagged because the regex
requires a digit immediately after `#`.
"""

from __future__ import annotations

import re

# Fenced code blocks (triple-backtick or triple-tilde) are stripped
# before the lint runs so legitimate uses of `#NN` inside example
# code or shell snippets don't trigger.
_FENCED_CODE_RE = re.compile(r"```.*?```|~~~.*?~~~", re.DOTALL)

# Inline code spans likewise. A Fellow quoting `#04` in an inline
# code span is presumably illustrating the pattern, not citing.
_INLINE_CODE_RE = re.compile(r"`[^`\n]*`")

# Citation-by-number patterns. The regex requires at least one digit
# immediately after `#`, which avoids matching headings.
_CITATION_RE = re.compile(
    r"""
    (?:
        \[\#\d+[^\]]*\]   |   # [#04 Title] or [#11]
        \(\#\d+\)         |   # (#04)
        (?<!\w)\#\d{2,}\b     # bare #NN with two+ digits (avoids inline #0 in text)
    )
    """,
    re.VERBOSE,
)


class CitationLintError(RuntimeError):
    """Raised when a draft contains citation-by-number patterns.

    Subclasses RuntimeError so the autopilot's per-step exception
    handler can catch it the same way it catches transient Fellow
    failures and record a `step_failure` decision rather than crashing
    the cycle.
    """

    def __init__(self, violations: list[str]) -> None:
        self.violations = violations
        sample = ", ".join(repr(v) for v in violations[:5])
        super().__init__(
            f"Publication body cites other works by number "
            f"({len(violations)} occurrence(s); sample: {sample}). "
            "Cite by title and link instead. The writing briefs forbid "
            "this pattern; if you reached this error, the Fellow's "
            "draft slipped past the brief and the work needs revision."
        )


def find_violations(body: str) -> list[str]:
    """Return every citation-by-number occurrence in `body`.

    Code fences and inline-code spans are stripped first so legitimate
    uses (shell prompts, Python comments, illustrative quotes) don't
    register. Returns a list of the matched strings; empty if clean.
    """
    stripped = _FENCED_CODE_RE.sub("", body)
    stripped = _INLINE_CODE_RE.sub("", stripped)
    return _CITATION_RE.findall(stripped)


def check(body: str) -> None:
    """Raise `CitationLintError` if the body contains numeric citations.

    Pass body markdown (after frontmatter is stripped) to this function
    at publish time. A clean body returns None.
    """
    violations = find_violations(body)
    if violations:
        raise CitationLintError(violations)


__all__ = ["CitationLintError", "check", "find_violations"]
