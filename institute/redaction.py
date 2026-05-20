"""Cost-redaction guard for public archive and blog artifacts.

Every line of research, every review, every notebook is committed to a
public repository and rendered on the blog. The College is non-commercial
and our operating posture is to keep cost telemetry off the public
surface entirely. This module strips operational cost/token/budget
references at archive-write time.

The redactor is intentionally conservative: it targets phrases that
look like operator telemetry (`run cost: $2.24`, `budget=$10.0`, `1234
input tokens`), not arbitrary dollar signs or the word "token" in a
research context. Research about tokenizers, currency, or budgets is
not the target. Bare `$5` mentions and stand-alone "tokens" are left
alone.

Use `redact(text) -> (cleaned, removals)`. Never raises. Loses no
surrounding sentence content — only the matched span is replaced with
a short marker so the surrounding prose stays coherent.
"""

from __future__ import annotations

import re
from dataclasses import dataclass

_COST_MARKER = "[cost redacted]"
_BUDGET_MARKER = "[budget redacted]"
_TOKEN_MARKER = "[token count redacted]"

# Each entry: (compiled pattern, replacement marker, label-for-audit).
# Patterns require explicit operational context (a keyword like
# "cost", "budget", "tokens", "spent") plus a number nearby. This
# keeps the redactor from chewing through legitimate research prose
# that happens to mention dollars or tokens.
_PATTERNS: list[tuple[re.Pattern[str], str, str]] = [
    # Orchestrator telemetry lines: "elapsed: 215s · run cost: $2.24 of $10.00"
    (
        re.compile(
            r"\belapsed\s*[:=]\s*\d+\s*s\s*[·•|]\s*run\s+cost\s*[:=]\s*"
            r"\$?\s*\d[\d,._]*(?:\s*of\s*\$?\s*\d[\d,._]*)?",
            re.IGNORECASE,
        ),
        _COST_MARKER,
        "elapsed-and-run-cost",
    ),
    # "run cost: $X" / "run cost = $X of $Y"
    (
        re.compile(
            r"\brun\s+cost\s*[:=]\s*\$?\s*\d[\d,._]*(?:\s*of\s*\$?\s*\d[\d,._]*)?",
            re.IGNORECASE,
        ),
        _COST_MARKER,
        "run-cost",
    ),
    # "budget=$10" / "budget = $10.00" / "budget: $10.00"
    (
        re.compile(
            r"\bbudget\s*[:=]\s*\$?\s*\d[\d,._]*",
            re.IGNORECASE,
        ),
        _BUDGET_MARKER,
        "budget",
    ),
    # "daily=$0" / "daily cap = $5"
    (
        re.compile(
            r"\bdaily(?:\s+cap)?\s*[:=]\s*\$?\s*\d[\d,._]*",
            re.IGNORECASE,
        ),
        _BUDGET_MARKER,
        "daily-cap",
    ),
    # "total cost: $X" / "estimated cost = $X" / "approximate cost $X"
    (
        re.compile(
            r"\b(?:total|estimated|approximate|approx\.?|cumulative)\s+cost\s*[:=]?\s*\$?\s*\d[\d,._]*",
            re.IGNORECASE,
        ),
        _COST_MARKER,
        "named-cost",
    ),
    # "spent $X" / "we spent $X.YY"
    (
        re.compile(
            r"\bspent\s+\$\s*\d[\d,._]*",
            re.IGNORECASE,
        ),
        _COST_MARKER,
        "spent",
    ),
    # "cost of $X" / "cost was $X" / "cost came to $X" / "cost is $X"
    (
        re.compile(
            r"\bcost\s+(?:of|was|is|came\s+to)\s+\$\s*\d[\d,._]*",
            re.IGNORECASE,
        ),
        _COST_MARKER,
        "cost-verb",
    ),
    # "compute cost" / "inference cost" / "api cost" — operational pricing terms
    (
        re.compile(
            r"\b(?:compute|inference|api|llm|model)\s+cost\s*[:=]?\s*(?:was|is|of|came\s+to)?\s*\$?\s*\d[\d,._]*",
            re.IGNORECASE,
        ),
        _COST_MARKER,
        "named-pricing-cost",
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
    # "claude-opus-4-7 cost ..." (model + cost adjective on same line)
    (
        re.compile(
            r"\bclaude-[a-z0-9-]+[^.\n]{0,80}\b(?:cost|costs|pricing|pric(?:e|ed))[^.\n]*",
            re.IGNORECASE,
        ),
        _COST_MARKER,
        "model-cost",
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
