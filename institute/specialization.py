"""Helpers for comparing Fellow specialization strings."""

from __future__ import annotations

_STOPWORDS = frozenset(
    {
        "a",
        "an",
        "the",
        "and",
        "or",
        "of",
        "in",
        "on",
        "for",
        "with",
        "to",
        "from",
        "by",
        "as",
        "at",
        "is",
        "are",
        "be",
        "this",
        "that",
    }
)


def _spec_tokens(specialization: str) -> set[str]:
    """Content-bearing word tokens from a specialization string."""
    cleaned = "".join(ch.lower() if ch.isalnum() else " " for ch in specialization)
    return {tok for tok in cleaned.split() if tok and tok not in _STOPWORDS}


def similarity(lead_spec: str, candidate_spec: str) -> int:
    """Token-overlap similarity. Bigger = more disciplinary kinship."""
    return len(_spec_tokens(lead_spec) & _spec_tokens(candidate_spec))


__all__ = ["similarity"]
