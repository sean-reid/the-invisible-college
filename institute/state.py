"""The project state machine.

Each project moves through a fixed sequence of states. Each state has
exactly one defined next action. `institute next` looks at the current
state and dispatches the appropriate workflow.

States are stored as strings in the projects table. Transitions are
validated here, and applied as part of the same SQLite transaction that
writes the resulting artifact.
"""

from __future__ import annotations

from enum import StrEnum


class State(StrEnum):
    PROPOSED = "proposed"
    PROPOSAL_REVIEWED = "proposal_reviewed"
    RESEARCHING = "researching"
    DRAFTED = "drafted"
    PEER_REVIEWING = "peer_reviewing"
    REVISING = "revising"
    ANDON_REVIEW = "andon_review"
    EDITORIAL = "editorial"
    PUBLISHED = "published"
    REJECTED = "rejected"


# The single next action that follows each state. Terminal states map to None.
NEXT_ACTION: dict[State, str | None] = {
    State.PROPOSED: "review_proposal",
    State.PROPOSAL_REVIEWED: "research",
    State.RESEARCHING: "research",  # research can take multiple invocations
    State.DRAFTED: "peer_review",
    State.PEER_REVIEWING: "peer_review",
    State.REVISING: "revise",
    State.ANDON_REVIEW: "andon_review",
    State.EDITORIAL: "publish",
    State.PUBLISHED: None,
    State.REJECTED: None,
}


# Allowed forward transitions. Backward transitions only happen on rejection.
ALLOWED_TRANSITIONS: dict[State, set[State]] = {
    State.PROPOSED: {State.PROPOSAL_REVIEWED, State.REJECTED},
    State.PROPOSAL_REVIEWED: {State.RESEARCHING},
    State.RESEARCHING: {State.RESEARCHING, State.DRAFTED},
    State.DRAFTED: {State.PEER_REVIEWING},
    State.PEER_REVIEWING: {
        State.PEER_REVIEWING,
        State.REVISING,
        State.ANDON_REVIEW,
        State.EDITORIAL,
        State.REJECTED,
    },
    State.REVISING: {State.PEER_REVIEWING, State.EDITORIAL},
    State.ANDON_REVIEW: {State.EDITORIAL, State.REJECTED},
    State.EDITORIAL: {State.PUBLISHED, State.REJECTED},
    State.PUBLISHED: set(),
    State.REJECTED: set(),
}


def can_transition(current: State, target: State) -> bool:
    return target in ALLOWED_TRANSITIONS[current]


def assert_transition(current: State, target: State) -> None:
    if not can_transition(current, target):
        raise ValueError(f"Illegal transition: {current} -> {target}")


def is_terminal(state: State) -> bool:
    return NEXT_ACTION[state] is None
