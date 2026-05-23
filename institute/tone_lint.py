"""Publish-time lint: flag review-process language leaking into a draft.

The writing briefs for `research` and `revise` tell Fellows that
`draft.md` is the published piece - the College's final word - and
that it must not narrate the review process, name advisors or
reviewers, or refer to "the prior draft," "round 1/2," etc. Process
narrative belongs in `response.md`, not in the public artifact.

This module is the safety net for when that guidance fails. It scans
the body for a small set of telltale patterns that indicate the
Fellow accidentally backfilled response-to-reviewers content into
the draft. It runs at publish time alongside `citation_lint`.

Modes:
  - `mode="warn"` (default): print a yellow warning summarising the
    matches. Publication continues. Used while the institution is
    still calibrating the pattern set; false positives don't block.
  - `mode="raise"`: raise `ToneLintError` and halt the publish step.
    The autopilot's per-step handler records a `step_failure`
    decision and the next cycle re-tries the publish.

Patterns are conservative on purpose - we tolerate false negatives
in exchange for very few false positives. The intent is to catch
the obvious leaks (the example that prompted this lint had three
in a single paragraph), not to police every sentence.
"""

from __future__ import annotations

import re

from rich.console import Console

console = Console()


# Fenced code blocks (triple-backtick or triple-tilde) are stripped
# before the lint runs so example commands that mention "round 1"
# in a flag name don't false-positive.
_FENCED_CODE_RE = re.compile(r"```.*?```|~~~.*?~~~", re.DOTALL)
_INLINE_CODE_RE = re.compile(r"`[^`\n]*`")


# Each pattern is `(regex, short_label)`. The label is what the warning
# surfaces so the operator can see which class of leak fired without
# reading the full regex. Patterns are case-insensitive.
_PATTERNS: list[tuple[re.Pattern[str], str]] = [
    # First-person ownership of an advisor or reviewer.
    (
        re.compile(r"\bmy advisor\b", re.IGNORECASE),
        "my advisor",
    ),
    (
        re.compile(r"\bmy (?:peer )?reviewers?\b", re.IGNORECASE),
        "my reviewer(s)",
    ),
    # Possessive references to advisor/reviewer/panel actions.
    (
        re.compile(
            r"\b(?:advisor|reviewer|panel|panelist)['\u2019]?s "
            r"(?:reply|response|note|feedback|push|concerns?|comments?|critique)\b",
            re.IGNORECASE,
        ),
        "advisor/reviewer/panel possessive action",
    ),
    # Round-N peer review or panel review narration.
    (
        re.compile(
            r"\bround[- ](?:one|two|three|1|2|3)\s+"
            r"(?:peer\s+)?(?:review|panel|feedback|reviews?)\b",
            re.IGNORECASE,
        ),
        "round-N review/panel",
    ),
    # Prior-draft references.
    (
        re.compile(
            r"\bthe\s+(?:prior|previous|earlier|first|initial)\s+(?:draft|version|submission|revision)\b",
            re.IGNORECASE,
        ),
        "prior draft / previous version",
    ),
    # Process-arc phrasing.
    (
        re.compile(r"\bafter\s+(?:peer\s+)?review\b", re.IGNORECASE),
        "after (peer) review",
    ),
    (
        re.compile(r"\bduring\s+revision\b", re.IGNORECASE),
        "during revision",
    ),
    (
        re.compile(r"\bin\s+(?:this\s+)?revision\b", re.IGNORECASE),
        "in (this) revision",
    ),
    (
        re.compile(r"\bthis\s+revision\s+(?:addresses|adds|reframes|changes)\b", re.IGNORECASE),
        "this revision addresses/adds/...",
    ),
    # The qualifying-panel specifically.
    (
        re.compile(
            r"\bqualifying[- ]panel(?:'s)?\s+(?:review|feedback|note|reply)\b", re.IGNORECASE
        ),
        "qualifying-panel review/feedback",
    ),
    # "The panel said/asked/pushed" attribution.
    (
        re.compile(
            r"\bthe\s+panel\s+(?:said|asked|pushed|wrote|noted|raised|flagged|pressed)\b",
            re.IGNORECASE,
        ),
        "the panel said/asked/...",
    ),
]


class ToneLintError(RuntimeError):
    """Raised in `mode='raise'` when the body contains review-process language."""

    def __init__(self, violations: list[tuple[str, str]]) -> None:
        self.violations = violations
        sample = "; ".join(f"{label}: {match!r}" for label, match in violations[:5])
        super().__init__(
            f"Publication body contains review-process language "
            f"({len(violations)} occurrence(s); sample: {sample}). "
            "The draft must read as the published piece, not a process "
            "narrative. Move this content to response.md."
        )


def find_violations(body: str) -> list[tuple[str, str]]:
    """Return every (label, matched_text) pair found in `body`.

    Code fences and inline-code spans are stripped first so a quoted
    example or a CLI flag doesn't trigger. Empty list means the body
    is clean.
    """
    stripped = _FENCED_CODE_RE.sub("", body)
    stripped = _INLINE_CODE_RE.sub("", stripped)
    out: list[tuple[str, str]] = []
    for pattern, label in _PATTERNS:
        for match in pattern.finditer(stripped):
            out.append((label, match.group(0)))
    return out


def check(body: str, *, mode: str = "warn") -> list[tuple[str, str]]:
    """Lint the body for review-process language.

    Returns the list of (label, match) tuples even when not raising,
    so the caller can decide what to do with them. In `warn` mode the
    function also prints a yellow summary to the console.
    """
    violations = find_violations(body)
    if not violations:
        return []
    if mode == "raise":
        raise ToneLintError(violations)
    if mode == "warn":
        sample = "; ".join(f"{label} -> {match!r}" for label, match in violations[:5])
        more = f" (+{len(violations) - 5} more)" if len(violations) > 5 else ""
        console.print(
            f"[yellow]tone_lint: {len(violations)} review-process phrase(s) "
            f"in draft body. {sample}{more}[/yellow]"
        )
        return violations
    raise ValueError(f"Unknown tone_lint mode {mode!r}; expected 'warn' or 'raise'.")


__all__ = ["ToneLintError", "check", "find_violations"]
