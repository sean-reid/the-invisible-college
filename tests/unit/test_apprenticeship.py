"""Tests for the apprenticeship pieces: curriculum tracking, qualifying-project
routing, advisor-as-primary review slot, and auto-promotion on qualifying
publication.

These tests exercise the pure plumbing without invoking Claude.
"""

from __future__ import annotations

from datetime import UTC, datetime
from pathlib import Path

import pytest

from institute import curriculum, db, decisions, paths, workspaces
from institute import fellow as fellow_mod
from institute.fellow import Genome
from institute.state import ALLOWED_TRANSITIONS, NEXT_ACTION, State
from institute.workflows.peer_review import _pick_review_slots


@pytest.fixture()
def isolated(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> Path:
    genomes = tmp_path / "genomes"
    fellows = tmp_path / "fellows"
    archive = tmp_path / "archive"
    drafts = archive / "drafts"
    reviews_dir = archive / "reviews"
    decisions_dir = archive / "decisions"
    curriculum_dir = archive / "curriculum"
    for d in (genomes, fellows, drafts, reviews_dir, decisions_dir, curriculum_dir):
        d.mkdir(parents=True)
    db_path = tmp_path / "institute.db"

    monkeypatch.setattr(db, "DB_PATH", db_path)
    monkeypatch.setattr(decisions, "DECISIONS", decisions_dir)
    monkeypatch.setattr(paths, "GENOMES", genomes)
    monkeypatch.setattr(paths, "FELLOWS", fellows)
    monkeypatch.setattr(paths, "ARCHIVE", archive)
    monkeypatch.setattr(paths, "DRAFTS", drafts)
    monkeypatch.setattr(paths, "REVIEWS", reviews_dir)
    monkeypatch.setattr(paths, "CURRICULUM", curriculum_dir)
    monkeypatch.setattr(paths, "ROOT", tmp_path)
    monkeypatch.setattr(fellow_mod, "GENOMES", genomes)
    monkeypatch.setattr(fellow_mod, "FELLOWS", fellows)
    monkeypatch.setattr(workspaces, "FELLOWS", fellows)
    db.initialize(db_path)
    return tmp_path


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
    assert ALLOWED_TRANSITIONS[State.AWAITING_ADVISOR_REVIEW] == {
        State.REVISING,
        State.PEER_REVIEWING,
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


# ---------------------------------------------------------------------------
# Peer review: advisor as primary on qualifying projects
# ---------------------------------------------------------------------------


def test_qualifying_review_slots_advisor_is_primary(isolated: Path) -> None:
    with db.connection() as conn, db.transaction(conn):
        _seed(conn, _genome("advisor-fellow", "Advisor", "senior_fellow", spec="theory"))
        _seed(
            conn,
            _genome("postulant-x", "Pat", "postulant", spec="theory"),
            advisor_id="advisor-fellow",
        )
        _seed(conn, _genome("reviewer-a", "Reva", "fellow", spec="related"))
        _seed(conn, _genome("reviewer-b", "Revb", "fellow", spec="unrelated"))
        now = datetime.now(UTC).isoformat(timespec="seconds")
        conn.execute(
            "INSERT INTO projects "
            "(id, title, state, lead_fellow_id, draft_path, review_round, kind, "
            " created_at, updated_at) "
            "VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)",
            (
                "proj-q",
                "Qualifying piece",
                "drafted",
                "postulant-x",
                "draft.md",
                1,
                "qualifying",
                now,
                now,
            ),
        )

    with db.connection() as conn:
        slots = _pick_review_slots(conn, "proj-q", "postulant-x", 1)
    by_role = {s.role: s.reviewer_id for s in slots}
    assert by_role["primary"] == "advisor-fellow", (
        "Qualifying project must put the advisor in the primary slot"
    )
    # Secondary and outside should come from the rotation pool, NOT the advisor.
    assert by_role.get("secondary") != "advisor-fellow"
    assert by_role.get("outside") != "advisor-fellow"


def test_research_review_slots_keep_normal_rotation(isolated: Path) -> None:
    """A kind='research' project should not pin the advisor as primary."""
    with db.connection() as conn, db.transaction(conn):
        _seed(conn, _genome("advisor-fellow", "Advisor", "senior_fellow", spec="theory"))
        # Lead has an advisor in the DB, but kind='research' so the advisor
        # rule should NOT fire.
        _seed(
            conn,
            _genome("lead-fellow", "Lead", "fellow", spec="theory"),
            advisor_id="advisor-fellow",
        )
        _seed(conn, _genome("reviewer-a", "Reva", "fellow", spec="related"))
        _seed(conn, _genome("reviewer-b", "Revb", "fellow", spec="unrelated"))
        now = datetime.now(UTC).isoformat(timespec="seconds")
        conn.execute(
            "INSERT INTO projects "
            "(id, title, state, lead_fellow_id, draft_path, review_round, kind, "
            " created_at, updated_at) "
            "VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)",
            (
                "proj-r",
                "Regular piece",
                "drafted",
                "lead-fellow",
                "draft.md",
                1,
                "research",
                now,
                now,
            ),
        )

    with db.connection() as conn:
        slots = _pick_review_slots(conn, "proj-r", "lead-fellow", 1)
    by_role = {s.role: s.reviewer_id for s in slots}
    # The advisor is eligible as a regular reviewer but should not be
    # forced into primary by the qualifying rule.
    assert by_role["primary"] in {"advisor-fellow", "reviewer-a", "reviewer-b"}
    # All other Fellows should be picked from the same pool.
    assert set(by_role.values()).issubset({"advisor-fellow", "reviewer-a", "reviewer-b"})


# ---------------------------------------------------------------------------
# Auto-promote on qualifying publish
# ---------------------------------------------------------------------------


def test_auto_promote_to_novice_on_qualifying_publish(isolated: Path) -> None:
    from institute.workflows.publish import _auto_promote_to_novice

    with db.connection() as conn, db.transaction(conn):
        _seed(conn, _genome("advisor", "Adv", "fellow"))
        _seed(conn, _genome("pat", "Pat", "postulant"), advisor_id="advisor")

    with db.connection() as conn, db.transaction(conn):
        _auto_promote_to_novice(
            conn, "pat", "proj-x", datetime.now(UTC).isoformat(timespec="seconds")
        )
    with db.connection() as conn:
        row = conn.execute("SELECT rank FROM fellows WHERE id = 'pat'").fetchone()
    assert row["rank"] == "novice"

    g = Genome.from_file(fellow_mod.genome_path("pat"))
    assert g.rank == "novice"


def test_auto_promote_skips_non_postulant(isolated: Path) -> None:
    """If the lead is already past Postulant, auto-promote is a no-op."""
    from institute.workflows.publish import _auto_promote_to_novice

    with db.connection() as conn, db.transaction(conn):
        _seed(conn, _genome("ada", "Ada", "fellow"))

    with db.connection() as conn, db.transaction(conn):
        _auto_promote_to_novice(
            conn, "ada", "proj-x", datetime.now(UTC).isoformat(timespec="seconds")
        )
    with db.connection() as conn:
        row = conn.execute("SELECT rank FROM fellows WHERE id = 'ada'").fetchone()
    assert row["rank"] == "fellow", "Non-postulant must not be touched"


# ---------------------------------------------------------------------------
# Autopilot's curriculum → qualifying picker
# ---------------------------------------------------------------------------


def test_qualifying_picker_finds_postulant_done_with_curriculum(isolated: Path) -> None:
    """A Postulant with curriculum_completed_at and no qualifying project is selected."""
    now = datetime.now(UTC).isoformat(timespec="seconds")
    with db.connection() as conn, db.transaction(conn):
        _seed(conn, _genome("advisor", "Adv", "fellow"))
        _seed(conn, _genome("ready", "Ready Pat", "postulant"), advisor_id="advisor")
        # Completed curriculum, no qualifying project yet.
        conn.execute(
            "UPDATE fellows SET curriculum_completed_at = ? WHERE id = 'ready'",
            (now,),
        )
        rows = list(
            conn.execute(
                "SELECT f.id FROM fellows f "
                "WHERE f.rank = 'postulant' "
                "AND f.retired_at IS NULL "
                "AND f.curriculum_completed_at IS NOT NULL "
                "AND NOT EXISTS ("
                "  SELECT 1 FROM projects p "
                "  WHERE p.lead_fellow_id = f.id AND p.kind = 'qualifying'"
                ") "
                "ORDER BY f.curriculum_completed_at ASC LIMIT 1"
            )
        )
    assert [r["id"] for r in rows] == ["ready"]


def test_qualifying_picker_skips_postulant_with_existing_qualifying(isolated: Path) -> None:
    """A Postulant who already has a qualifying project (any state) is not picked again."""
    now = datetime.now(UTC).isoformat(timespec="seconds")
    with db.connection() as conn, db.transaction(conn):
        _seed(conn, _genome("advisor", "Adv", "fellow"))
        _seed(conn, _genome("inflight", "In Flight", "postulant"), advisor_id="advisor")
        conn.execute(
            "UPDATE fellows SET curriculum_completed_at = ? WHERE id = 'inflight'",
            (now,),
        )
        # Existing qualifying project in mid-pipeline.
        conn.execute(
            "INSERT INTO projects "
            "(id, title, state, lead_fellow_id, review_round, kind, "
            " created_at, updated_at) "
            "VALUES (?, ?, ?, ?, 1, 'qualifying', ?, ?)",
            ("proj-existing", "x", "researching", "inflight", now, now),
        )
        rows = list(
            conn.execute(
                "SELECT f.id FROM fellows f "
                "WHERE f.rank = 'postulant' "
                "AND f.retired_at IS NULL "
                "AND f.curriculum_completed_at IS NOT NULL "
                "AND NOT EXISTS ("
                "  SELECT 1 FROM projects p "
                "  WHERE p.lead_fellow_id = f.id AND p.kind = 'qualifying'"
                ") "
                "ORDER BY f.curriculum_completed_at ASC LIMIT 1"
            )
        )
    assert rows == [], "Postulant with existing qualifying project should not be picked"


def test_curriculum_picker_interleaves_postulants(isolated: Path) -> None:
    """Autopilot's curriculum picker should rotate, not exhaust one Postulant first.

    Regression: the original picker sorted by curriculum_designed_at ASC,
    which meant the Postulant whose curriculum was designed first
    monopolized every wake-up until their curriculum was done. With two
    Postulants admitted minutes apart, the second would wait days.
    """
    with db.connection() as conn, db.transaction(conn):
        _seed(conn, _genome("adam", "Adam", "postulant"))
        _seed(conn, _genome("charles", "Charles", "postulant"))
        conn.execute(
            "UPDATE fellows SET curriculum_designed_at = ? WHERE id = 'adam'",
            ("2026-05-18T18:49:25+00:00",),
        )
        conn.execute(
            "UPDATE fellows SET curriculum_designed_at = ? WHERE id = 'charles'",
            ("2026-05-18T18:51:06+00:00",),
        )
        # Adam has two completed responses; Charles has zero. The picker
        # should prefer Charles next, not Adam.
        conn.execute(
            "INSERT INTO curriculum_responses (fellow_id, item_id, response_path, submitted_at) "
            "VALUES (?, ?, ?, ?)",
            ("adam", "foun-charter", "x", "2026-05-18T19:45:23+00:00"),
        )
        conn.execute(
            "INSERT INTO curriculum_responses (fellow_id, item_id, response_path, submitted_at) "
            "VALUES (?, ?, ?, ?)",
            ("adam", "foun-exemplum", "x", "2026-05-19T00:41:28+00:00"),
        )

    with db.connection() as conn:
        rows = list(
            conn.execute(
                """
                SELECT f.id
                FROM fellows f
                LEFT JOIN curriculum_responses r ON r.fellow_id = f.id
                WHERE f.rank = 'postulant'
                  AND f.retired_at IS NULL
                  AND f.curriculum_designed_at IS NOT NULL
                  AND f.curriculum_completed_at IS NULL
                GROUP BY f.id
                ORDER BY MAX(r.submitted_at) ASC,
                         f.curriculum_designed_at ASC
                """
            )
        )
    assert [r["id"] for r in rows] == ["charles", "adam"], (
        "Charles (no responses yet) should be picked before Adam (2 responses)"
    )


def test_qualifying_picker_skips_postulant_with_unfinished_curriculum(isolated: Path) -> None:
    """A Postulant who hasn't finished curriculum is not picked for qualifying."""
    with db.connection() as conn, db.transaction(conn):
        _seed(conn, _genome("advisor", "Adv", "fellow"))
        _seed(conn, _genome("midway", "Midway", "postulant"), advisor_id="advisor")
        # curriculum_completed_at stays NULL.
        rows = list(
            conn.execute(
                "SELECT f.id FROM fellows f "
                "WHERE f.rank = 'postulant' "
                "AND f.retired_at IS NULL "
                "AND f.curriculum_completed_at IS NOT NULL "
                "AND NOT EXISTS ("
                "  SELECT 1 FROM projects p "
                "  WHERE p.lead_fellow_id = f.id AND p.kind = 'qualifying'"
                ") "
                "ORDER BY f.curriculum_completed_at ASC LIMIT 1"
            )
        )
    assert rows == [], "Postulant still reading should not be picked for qualifying"
