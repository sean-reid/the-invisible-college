"""Apprenticeship state machine, schema v4, and curriculum tracking helpers."""

from __future__ import annotations

from datetime import UTC, datetime
from pathlib import Path

from institute import curriculum, db
from institute import fellow as fellow_mod
from institute.fellow import Genome
from institute.state import ALLOWED_TRANSITIONS, NEXT_ACTION, State


def _genome(fellow_id: str, name: str, rank: str, spec: str = "x") -> Genome:
    return Genome(
        id=fellow_id,
        name=name,
        rank=rank,
        model="claude-sonnet-4-6",
        specialization=spec,
        system_prompt_addendum=("body " * 60).strip(),
        allowed_tools=["Read"],
    )


def _seed(conn, g: Genome, advisor_id: str | None = None) -> None:
    g.write(fellow_mod.genome_path(g.id))
    fellow_mod.register(conn, g, advisor_id=advisor_id)


# ---------------------------------------------------------------------------
# State machine
# ---------------------------------------------------------------------------


def test_awaiting_advisor_review_state_exists() -> None:
    assert State.AWAITING_ADVISOR_REVIEW == "awaiting_advisor_review"


def test_drafted_can_route_to_advisor_review_or_peer_review() -> None:
    assert State.AWAITING_ADVISOR_REVIEW in ALLOWED_TRANSITIONS[State.DRAFTED]
    assert State.PEER_REVIEWING in ALLOWED_TRANSITIONS[State.DRAFTED]


def test_advisor_review_dispatches_advisor_workflow() -> None:
    assert NEXT_ACTION[State.AWAITING_ADVISOR_REVIEW] == "advisor_review"


def test_advisor_review_transitions_to_revise_or_peer() -> None:
    # REJECTED is also allowed because targeted termination (Chapter 3)
    # can force a REJECTED transition from any in-flight state.
    assert ALLOWED_TRANSITIONS[State.AWAITING_ADVISOR_REVIEW] == {
        State.REVISING,
        State.PEER_REVIEWING,
        State.AWAITING_QUALIFYING_PANEL,
        State.REJECTED,
        State.ABANDONED,
    }


# ---------------------------------------------------------------------------
# Schema v4
# ---------------------------------------------------------------------------


def test_fellows_has_curriculum_columns(isolated: Path) -> None:
    with db.connection() as conn:
        cols = {row["name"] for row in conn.execute("PRAGMA table_info(fellows)")}
    assert "curriculum_designed_at" in cols
    assert "curriculum_completed_at" in cols


def test_projects_has_kind(isolated: Path) -> None:
    with db.connection() as conn:
        cols = {row["name"] for row in conn.execute("PRAGMA table_info(projects)")}
    assert "kind" in cols


def test_curriculum_responses_table_exists(isolated: Path) -> None:
    with db.connection() as conn:
        rows = list(
            conn.execute(
                "SELECT name FROM sqlite_master WHERE type='table' AND name='curriculum_responses'"
            )
        )
    assert len(rows) == 1


# ---------------------------------------------------------------------------
# Curriculum helpers
# ---------------------------------------------------------------------------


def test_next_pending_item_walks_in_order(isolated: Path) -> None:
    with db.connection() as conn, db.transaction(conn):
        _seed(conn, _genome("postulant-one", "Pat One", "postulant"))

    items = [
        curriculum.CurriculumItem(
            id="foun-charter",
            layer="foundational",
            title="The Charter",
            source="docs/01-charter.md",
            prompt="Summarize",
        ),
        curriculum.CurriculumItem(
            id="spec-one",
            layer="specialization",
            title="A piece",
            source="archive/x.md",
            prompt="Critique",
        ),
    ]
    curriculum.save_items("postulant-one", items)

    with db.connection() as conn:
        # No responses yet → first item is pending.
        first = curriculum.next_pending_item(conn, "postulant-one")
        assert first is not None
        assert first.id == "foun-charter"

        # Record a response to the first; the second becomes pending.
        conn.execute(
            "INSERT INTO curriculum_responses (fellow_id, item_id, response_path, submitted_at) "
            "VALUES (?, ?, ?, ?)",
            (
                "postulant-one",
                "foun-charter",
                "archive/curriculum/postulant-one/responses/foun-charter.md",
                datetime.now(UTC).isoformat(timespec="seconds"),
            ),
        )
        second = curriculum.next_pending_item(conn, "postulant-one")
        assert second is not None
        assert second.id == "spec-one"


def test_next_pending_item_returns_none_when_complete(isolated: Path) -> None:
    with db.connection() as conn, db.transaction(conn):
        _seed(conn, _genome("pn", "Pat", "postulant"))
    items = [
        curriculum.CurriculumItem(
            id="only-one", layer="foundational", title="x", source="x", prompt="x"
        )
    ]
    curriculum.save_items("pn", items)
    with db.connection() as conn, db.transaction(conn):
        conn.execute(
            "INSERT INTO curriculum_responses (fellow_id, item_id, response_path, submitted_at) "
            "VALUES (?, ?, ?, ?)",
            ("pn", "only-one", "x", datetime.now(UTC).isoformat(timespec="seconds")),
        )
    with db.connection() as conn:
        assert curriculum.next_pending_item(conn, "pn") is None


def test_render_markdown_groups_by_layer() -> None:
    items = [
        curriculum.CurriculumItem(
            id="m1", layer="methodological", title="Method", source="x", prompt="apply"
        ),
        curriculum.CurriculumItem(
            id="f1", layer="foundational", title="Charter", source="x", prompt="summarize"
        ),
        curriculum.CurriculumItem(
            id="s1", layer="specialization", title="Piece", source="x", prompt="critique"
        ),
    ]
    md = curriculum.render_markdown(items)
    # Layer ordering in render is foundational → specialization → methodological.
    foundational_idx = md.index("## Foundational")
    specialization_idx = md.index("## Specialization")
    methodological_idx = md.index("## Methodological")
    assert foundational_idx < specialization_idx < methodological_idx
