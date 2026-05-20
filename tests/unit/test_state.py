"""Tests for the project state machine."""

from itertools import pairwise

import pytest

from institute.state import (
    NEXT_ACTION,
    State,
    assert_transition,
    can_transition,
    is_terminal,
)

TERMINAL = (State.PUBLISHED, State.REJECTED, State.ABANDONED)


def test_terminal_states_have_no_next_action() -> None:
    for s in TERMINAL:
        assert NEXT_ACTION[s] is None
        assert is_terminal(s)


def test_non_terminal_states_have_an_action() -> None:
    for s in State:
        if s in TERMINAL:
            continue
        assert NEXT_ACTION[s] is not None, f"state {s} has no next action"


def test_happy_path_transitions() -> None:
    path = [
        State.PROPOSED,
        State.PROPOSAL_REVIEWED,
        State.RESEARCHING,
        State.DRAFTED,
        State.PEER_REVIEWING,
        State.REVISING,
        State.EDITORIAL,
        State.PUBLISHED,
    ]
    for current, target in pairwise(path):
        assert can_transition(current, target), f"{current} -> {target} should be allowed"


def test_rejection_is_allowed_from_proposal_peer_review_and_editorial() -> None:
    assert can_transition(State.PROPOSED, State.REJECTED)
    assert can_transition(State.PEER_REVIEWING, State.REJECTED)
    assert can_transition(State.EDITORIAL, State.REJECTED)


def test_skipping_a_step_is_forbidden() -> None:
    assert not can_transition(State.PROPOSED, State.RESEARCHING)
    assert not can_transition(State.DRAFTED, State.EDITORIAL)


def test_assert_transition_raises_on_illegal() -> None:
    with pytest.raises(ValueError):
        assert_transition(State.PROPOSED, State.PUBLISHED)


def test_researching_can_self_loop() -> None:
    # Long research sessions stay in researching across multiple invocations.
    assert can_transition(State.RESEARCHING, State.RESEARCHING)


def test_peer_reviewing_can_self_loop() -> None:
    # Multiple reviewer assignments accrete in the same state.
    assert can_transition(State.PEER_REVIEWING, State.PEER_REVIEWING)
