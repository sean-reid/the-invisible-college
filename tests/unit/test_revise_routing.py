"""Tests for the post-revision routing matrix.

`_route_after_revise(kind, current_round)` decides where a project
goes after the lead Fellow finishes a revision pass. The matrix has
four cases (research/qualifying x round-1/round-2+) and the
qualifying-round-≥2 path was added 2026-05-20 to stop a loop where
the panel's stale-reviews bump kept the project oscillating between
peer_review and advisor_review.
"""

from __future__ import annotations

from institute.state import State
from institute.workflows.revise import _route_after_revise


def test_research_round_one_routes_to_peer_review_round_two() -> None:
    target, next_round, _ = _route_after_revise("research", current_round=1)
    assert target is State.PEER_REVIEWING
    assert next_round == 2


def test_research_round_two_routes_to_editorial() -> None:
    target, next_round, _ = _route_after_revise("research", current_round=2)
    assert target is State.EDITORIAL
    assert next_round == 2


def test_qualifying_round_one_routes_back_to_advisor() -> None:
    target, next_round, _ = _route_after_revise("qualifying", current_round=1)
    assert target is State.AWAITING_ADVISOR_REVIEW
    assert next_round == 1


def test_qualifying_round_two_routes_directly_to_editorial() -> None:
    """The 2026-05-20 fix: a round-2 qualifying revision goes to
    EDITORIAL, not back through advisor/panel/peer-review. Prevents
    the loop where the panel's stale-reviews bump kept incrementing
    the round indefinitely."""
    target, next_round, description = _route_after_revise("qualifying", current_round=2)
    assert target is State.EDITORIAL
    assert next_round == 2
    assert "editorial" in description.lower()


def test_qualifying_round_three_also_routes_to_editorial() -> None:
    """Any round >= 2 on a qualifying project goes straight to
    editorial. Defensive: if anything ever increments the round past
    two, we don't fall back into the advisor loop."""
    target, _, _ = _route_after_revise("qualifying", current_round=3)
    assert target is State.EDITORIAL
