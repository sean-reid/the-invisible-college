"""The project state machine.

Each project moves through a fixed sequence of states. Each state has
exactly one defined next action. `institute next` looks at the current
state and dispatches the appropriate workflow.

States are stored as strings in the projects table. Transitions are
validated here, and applied as part of the same SQLite transaction that
writes the resulting artifact.
"""

from __future__ import annotations

import sqlite3
from datetime import UTC, datetime
from enum import StrEnum


class State(StrEnum):
    PROPOSED = "proposed"
    PROPOSAL_REVIEWED = "proposal_reviewed"
    PROPOSAL_HELD = "proposal_held"  # reviewer asked for refine + resubmit
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
    ABANDONED = "abandoned"  # Fellow withdrew with honest lesson


# The single next action that follows each state. Terminal states map to None.
NEXT_ACTION: dict[State, str | None] = {
    State.PROPOSED: "review_proposal",
    State.PROPOSAL_REVIEWED: "research",
    State.PROPOSAL_HELD: "revise_proposal",
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
    State.ABANDONED: None,
}


# Allowed forward transitions. Every non-terminal state allows REJECTED
# as an exit, because targeted termination (Chapter 3) can hit a Fellow
# mid-project from any state.
ALLOWED_TRANSITIONS: dict[State, set[State]] = {
    State.PROPOSED: {
        State.PROPOSAL_REVIEWED,
        State.PROPOSAL_HELD,
        State.REJECTED,
        State.ABANDONED,
    },
    State.PROPOSAL_REVIEWED: {State.RESEARCHING, State.REJECTED, State.ABANDONED},
    State.PROPOSAL_HELD: {State.PROPOSED, State.REJECTED, State.ABANDONED},
    State.RESEARCHING: {
        State.RESEARCHING,
        State.DRAFTED,
        State.REJECTED,
        State.ABANDONED,
    },
    # A qualifying-kind project routes through AWAITING_ADVISOR_REVIEW
    # before peer review. A research-kind project skips straight to
    # PEER_REVIEWING. Both transitions are allowed; the workflow chooses.
    State.DRAFTED: {
        State.AWAITING_ADVISOR_REVIEW,
        State.PEER_REVIEWING,
        State.REJECTED,
        State.ABANDONED,
    },
    State.AWAITING_ADVISOR_REVIEW: {
        State.REVISING,
        State.PEER_REVIEWING,
        State.REJECTED,
        State.ABANDONED,
    },
    State.PEER_REVIEWING: {
        State.PEER_REVIEWING,
        State.REVISING,
        State.ANDON_REVIEW,
        State.EDITORIAL_REVIEW,
        State.EDITORIAL,
        State.REJECTED,
        State.ABANDONED,
    },
    # REVISING can self-loop when the revise step itself produces another
    # round of concerns. AWAITING_ADVISOR_REVIEW is the qualifying-project
    # path back to the advisor instead of leaping into peer review.
    State.REVISING: {
        State.REVISING,
        State.PEER_REVIEWING,
        State.EDITORIAL,
        State.AWAITING_ADVISOR_REVIEW,
        State.REJECTED,
        State.ABANDONED,
    },
    # Andon dismiss may need to route back through revise or editorial
    # review based on the non-cord-pulling reviewers' recommendations.
    State.ANDON_REVIEW: {
        State.EDITORIAL,
        State.REJECTED,
        State.REVISING,
        State.EDITORIAL_REVIEW,
        State.ABANDONED,
    },
    # Editorial Board makes the final call after round-2 peer review with
    # reject recommendations or dissent. Accept → editorial; reject → rejected.
    State.EDITORIAL_REVIEW: {State.EDITORIAL, State.REJECTED, State.ABANDONED},
    State.EDITORIAL: {State.PUBLISHED, State.REJECTED, State.ABANDONED},
    State.PUBLISHED: set(),
    State.REJECTED: set(),
    State.ABANDONED: set(),
}


def can_transition(current: State, target: State) -> bool:
    return target in ALLOWED_TRANSITIONS[current]


def assert_transition(current: State, target: State) -> None:
    if not can_transition(current, target):
        raise ValueError(f"Illegal transition: {current} -> {target}")


def is_terminal(state: State) -> bool:
    return NEXT_ACTION[state] is None


def transition(
    conn: sqlite3.Connection,
    project_id: str,
    target: State,
    *,
    force: bool = False,
) -> None:
    """Write a state transition with validation. Caller manages the transaction.

    Reads current state from the DB, asserts the move is allowed, and
    updates `state` + `updated_at` atomically. `force=True` skips the
    validation; only the targeted-termination workflow should use it, and
    only because terminate explicitly overrides all in-flight states to
    REJECTED.
    """
    row = conn.execute("SELECT state FROM projects WHERE id = ?", (project_id,)).fetchone()
    if row is None:
        raise ValueError(f"No such project: {project_id}")
    current = State(row["state"])
    if not force:
        assert_transition(current, target)
    now = datetime.now(UTC).isoformat(timespec="seconds")
    conn.execute(
        "UPDATE projects SET state = ?, updated_at = ? WHERE id = ?",
        (target.value, now, project_id),
    )
