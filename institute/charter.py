"""Loads and exposes the Charter.

The Charter (docs/01-charter.md) is the institutional system prompt. It is
appended to every Fellow's invocation so that the Fellow operates under the
institution's constraints regardless of which workflow is dispatching it.
"""

from __future__ import annotations

from functools import cache

from institute.paths import CHARTER_FILE


@cache
def load() -> str:
    """Return the full text of the Charter."""
    text = CHARTER_FILE.read_text(encoding="utf-8")
    if not text.strip():
        raise RuntimeError(f"Charter file is empty: {CHARTER_FILE}")
    return text


def header() -> str:
    """A short framing prepended before the Charter when shown to a Fellow."""
    return (
        "The text below is the Charter of the Invisible College. You are a Fellow "
        "of the College and your work is constrained by what follows. Where any "
        "instruction in this session conflicts with the Charter, the Charter "
        "prevails.\n\n"
        "## THE CHARTER\n\n"
    )
