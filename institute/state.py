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
    AWAITING_ADVISOR_REVIEW = "awaiting_advisor_review"
    PEER_REVIEWING = "peer_reviewing"
    REVISING = "revising"
    ANDON_REVIEW = "andon_review"
    EDITORIAL_REVIEW = "editorial_review"
    EDITORIAL = "editorial"
    PUBLISHED = "published"
    REJECTED = "rejected"


# The single next action that follows each state. Terminal states map to None.
NEXT_ACTION: dict[State, str | None] = {
    State.PROPOSED: "review_proposal",
    State.PROPOSAL_REVIEWED: "research",
    State.RESEARCHING: "research",  # research can take multiple invocations
    State.DRAFTED: "peer_review",
    State.AWAITING_ADVISOR_REVIEW: "advisor_review",
    State.PEER_REVIEWING: "peer_review",
    State.REVISING: "revise",
    State.ANDON_REVIEW: "andon_review",
    State.EDITORIAL_REVIEW: "editorial_review",
    State.EDITORIAL: "publish",
    State.PUBLISHED: None,
    State.REJECTED: None,
}


# Allowed forward transitions. Backward transitions only happen on rejection.
ALLOWED_TRANSITIONS: dict[State, set[State]] = {
    State.PROPOSED: {State.PROPOSAL_REVIEWED, State.REJECTED},
    State.PROPOSAL_REVIEWED: {State.RESEARCHING},
    State.RESEARCHING: {State.RESEARCHING, State.DRAFTED},
    # A qualifying-kind project routes through AWAITING_ADVISOR_REVIEW
    # before peer review. A research-kind project skips straight to
    # PEER_REVIEWING. Both transitions are allowed; the workflow chooses.
    State.DRAFTED: {State.AWAITING_ADVISOR_REVIEW, State.PEER_REVIEWING},
    State.AWAITING_ADVISOR_REVIEW: {State.REVISING, State.PEER_REVIEWING},
    State.PEER_REVIEWING: {
        State.PEER_REVIEWING,
        State.REVISING,
        State.ANDON_REVIEW,
        State.EDITORIAL_REVIEW,
        State.EDITORIAL,
        State.REJECTED,
    },
    State.REVISING: {State.PEER_REVIEWING, State.EDITORIAL, State.AWAITING_ADVISOR_REVIEW},
    State.ANDON_REVIEW: {State.EDITORIAL, State.REJECTED},
    # Editorial Board makes the final call after round-2 peer review with
    # reject recommendations or dissent. Accept → editorial; reject → rejected.
    State.EDITORIAL_REVIEW: {State.EDITORIAL, State.REJECTED},
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
