"""Cost-redaction guard for public archive and blog artifacts.

Every line of research, every review, every notebook is committed to a
public repository and rendered on the blog. The College is non-commercial
and our operating posture is to keep cost telemetry off the public
surface entirely. This module strips operational cost/token/budget
references at archive-write time.

The redactor targets *numerical* cost telemetry, not the abstract idea
of cost. A research piece may legitimately discuss "the cost of carry"
or note that a model was chosen "for cost reasons" — those don't leak
dollar figures and they pass through. What gets stripped is the
combination of a numerical value with an operational marker: dollar
amounts after `cost:`, `budget=`, `spent`, `under`, `approximately`;
token counts adjacent to `input tokens` / `output tokens`; orchestrator
telemetry lines like `elapsed: 215s · run cost: $2.24 of $10.00`.

Use `redact(text) -> (cleaned, RedactionReport)`. Never raises. Loses
no surrounding sentence content — only the matched span is replaced
with a short marker so the surrounding prose stays coherent.
"""

from __future__ import annotations

import re
from dataclasses import dataclass

_COST_MARKER = "[cost redacted]"
_BUDGET_MARKER = "[budget redacted]"
_TOKEN_MARKER = "[token count redacted]"

# Suffix appended to any $X dollar-amount pattern. Negative lookahead
# that bails when another `$` appears within the next 10 same-line
# characters — that pattern is overwhelmingly LaTeX inline math
# (`$N$`, `$0.017°$`) rather than operational cost telemetry. Without
# this guard the redactor swallows the opening `$` of a math span and
# leaves a corrupted trailing `°$` behind.
_NOT_LATEX = r"(?![^$\n]{0,10}\$)"

# Each entry: (compiled pattern, replacement marker, label-for-audit).
# Every pattern requires both an operational keyword and a number
# (dollar amount or token count). This keeps the redactor from
# touching prose that discusses cost abstractly without revealing
# any actual values.
_PATTERNS: list[tuple[re.Pattern[str], str, str]] = [
    # Full orchestrator-output line: "elapsed: 215s · run cost: $2.24 of $10.00"
    (
        re.compile(
            r"\belapsed\s*[:=]\s*\d+\s*s\s*[·•|]\s*run\s+cost\s*[:=]\s*"
            r"\$?\s*\d[\d,._]*(?:\s*of\s*\$?\s*\d[\d,._]*)?" + _NOT_LATEX,
            re.IGNORECASE,
        ),
        _COST_MARKER,
        "elapsed-and-run-cost",
    ),
    # "run cost: $X" / "run cost = $X of $Y"
    (
        re.compile(
            r"\brun\s+cost\s*[:=]\s*\$?\s*\d[\d,._]*(?:\s*of\s*\$?\s*\d[\d,._]*)?"
            + _NOT_LATEX,
            re.IGNORECASE,
        ),
        _COST_MARKER,
        "run-cost",
    ),
    # "budget=$X" / "budget = $X" / "budget: $X"
    (
        re.compile(
            r"\bbudget\s*[:=]\s*\$?\s*\d[\d,._]*" + _NOT_LATEX,
            re.IGNORECASE,
        ),
        _BUDGET_MARKER,
        "budget",
    ),
    # "daily=$0" / "daily cap = $5"
    (
        re.compile(
            r"\bdaily(?:\s+cap)?\s*[:=]\s*\$?\s*\d[\d,._]*" + _NOT_LATEX,
            re.IGNORECASE,
        ),
        _BUDGET_MARKER,
        "daily-cap",
    ),
    # "total cost: $X" / "estimated cost = $X" / "approximate cost $X"
    (
        re.compile(
            r"\b(?:total|estimated|approximate|approx\.?|cumulative)\s+cost\s*[:=]?\s*"
            r"\$\s*\d[\d,._]*" + _NOT_LATEX,
            re.IGNORECASE,
        ),
        _COST_MARKER,
        "named-cost",
    ),
    # "spent $X"
    (
        re.compile(
            r"\bspent\s+\$\s*\d[\d,._]*" + _NOT_LATEX,
            re.IGNORECASE,
        ),
        _COST_MARKER,
        "spent",
    ),
    # "cost of $X" / "cost was $X" / "cost came to $X" / "cost is $X"
    (
        re.compile(
            r"\bcost\s+(?:of|was|is|came\s+to)\s+\$\s*\d[\d,._]*" + _NOT_LATEX,
            re.IGNORECASE,
        ),
        _COST_MARKER,
        "cost-verb",
    ),
    # "cost: $X" / "cost = $X" — explicit value after `cost`
    (
        re.compile(
            r"\bcost(?:s)?\s*[:=]\s*\$\s*\d[\d,._]*" + _NOT_LATEX,
            re.IGNORECASE,
        ),
        _COST_MARKER,
        "cost-equals",
    ),
    # Qualified dollar totals: "under $3 total" / "approximately $X" /
    # "about $0.50" / "less than $1". The qualifier plus a $ amount is
    # how operational estimates show up; research prose almost never
    # uses these together.
    (
        re.compile(
            r"\b(?:under|approximately|approx\.?|about|around|roughly|less\s+than|over)"
            r"\s+\$\s*\d[\d,._]*(?:\s+total)?" + _NOT_LATEX,
            re.IGNORECASE,
        ),
        _COST_MARKER,
        "qualified-dollar",
    ),
    # Token telemetry: "1,234 input tokens" / "5000 output tokens" / "12k total tokens"
    (
        re.compile(
            r"\b\d[\d,._]*\s*k?\s+(?:input|output|prompt|completion|total)\s+tokens?\b",
            re.IGNORECASE,
        ),
        _TOKEN_MARKER,
        "labelled-tokens",
    ),
    # "input tokens: 1234" / "output tokens = 5000"
    (
        re.compile(
            r"\b(?:input|output|prompt|completion|total)\s+tokens?\s*[:=]\s*\d[\d,._]*",
            re.IGNORECASE,
        ),
        _TOKEN_MARKER,
        "tokens-equals",
    ),
    # "used N tokens" / "consumed N tokens"
    (
        re.compile(
            r"\b(?:used|consumed|spent)\s+\d[\d,._]*\s+tokens?\b",
            re.IGNORECASE,
        ),
        _TOKEN_MARKER,
        "verb-tokens",
    ),
]


@dataclass(frozen=True)
class RedactionReport:
    """Per-call summary of what the redactor removed."""

    total: int
    by_pattern: dict[str, int]

    def __bool__(self) -> bool:
        return self.total > 0


def redact(text: str) -> tuple[str, RedactionReport]:
    """Strip operational cost/token/budget references from text.

    Returns the cleaned text and a report of how many matches each
    pattern removed. Never raises; an empty input round-trips.
    """
    if not text:
        return text, RedactionReport(total=0, by_pattern={})

    by_pattern: dict[str, int] = {}
    total = 0
    for pattern, replacement, label in _PATTERNS:
        text, n = pattern.subn(replacement, text)
        if n:
            by_pattern[label] = n
            total += n
    return text, RedactionReport(total=total, by_pattern=by_pattern)


def has_cost_leak(text: str) -> bool:
    """True if any redaction pattern matches. Used by audit tooling."""
    if not text:
        return False
    return any(pattern.search(text) for pattern, _, _ in _PATTERNS)
