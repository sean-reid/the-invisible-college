"""Tests for the research-group collaborators helpers and the seams
they touch (propose, peer_review, publish, reputation).

These exercises stay below the Claude-runner boundary: no LLM
invocations, just the orchestrator code that decides who counts as a
co-author and who is excluded from reviewing.
"""

from __future__ import annotations

from datetime import UTC, datetime
from pathlib import Path

import pytest

from institute import collaborators, db, reputation
from institute import fellow as fellow_mod
from institute.fellow import Genome
from institute.workflows import propose as propose_workflow
from institute.workflows.peer_review import _pick_review_slots


def _genome(slug: str, name: str, *, rank: str = "fellow", spec: str = "general") -> Genome:
    return Genome(
        id=slug,
        name=name,
        rank=rank,
        model="claude-sonnet-4-6",
        specialization=spec,
        system_prompt_addendum=("body " * 60).strip(),
        allowed_tools=["Read"],
    )


@pytest.fixture()
def cohort(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> dict[str, Genome]:
    monkeypatch.setattr(fellow_mod, "GENOMES", tmp_path / "genomes")
    monkeypatch.setattr(fellow_mod, "FELLOWS", tmp_path / "fellows")
    db_path = tmp_path / "institute.db"
    monkeypatch.setattr(db, "DB_PATH", db_path)
    db.initialize(db_path)
    (tmp_path / "genomes").mkdir(exist_ok=True)

    fellows = {
        "lead": _genome("lead", "Lead Lovelace", spec="applied"),
        "carol": _genome("carol", "Carol Critic", spec="theory"),
        "diana": _genome("diana", "Diana Diderot", spec="critical review"),
        "evan": _genome("evan", "Evan Essayist", spec="long-form essay"),
        "nina": _genome("nina", "Nina Novice", rank="novice", spec="theory"),
        "petra": _genome("petra", "Petra Postulant", rank="postulant", spec="anything"),
        "rita": _genome("rita", "Rita Retired", spec="cartography"),
    }
    with db.connection() as conn, db.transaction(conn):
        for g in fellows.values():
            g.write(tmp_path / "genomes" / f"{g.id}.json")
            fellow_mod.register(conn, g)
        # Mark Rita Retired.
        conn.execute(
            "UPDATE fellows SET retired_at = ? WHERE id = ?",
            (datetime.now(UTC).isoformat(timespec="seconds"), "rita"),
        )
    return fellows


def _insert_project(
    project_id: str,
    *,
    lead_id: str,
    state: str = "drafted",
    review_round: int = 1,
) -> None:
    now = datetime.now(UTC).isoformat(timespec="seconds")
    with db.connection() as conn, db.transaction(conn):
        conn.execute(
            "INSERT INTO projects "
            "(id, title, state, lead_fellow_id, draft_path, review_round, "
            " created_at, updated_at) "
            "VALUES (?, ?, ?, ?, ?, ?, ?, ?)",
            (project_id, "x", state, lead_id, "draft.md", review_round, now, now),
        )


# --- collaborators module ------------------------------------------------


def test_add_collaborator_persists_row(cohort) -> None:
    _insert_project("p-add", lead_id="lead")
    with db.connection() as conn, db.transaction(conn):
        collaborators.add(conn, project_id="p-add", fellow_id="carol")
    with db.connection() as conn:
        members = collaborators.for_project(conn, "p-add")
    assert [m.fellow_id for m in members] == ["carol"]
    assert members[0].role == collaborators.DEFAULT_ROLE


def test_add_collaborator_rejects_lead(cohort) -> None:
    _insert_project("p-lead", lead_id="lead")
    with db.connection() as conn, db.transaction(conn):
        with pytest.raises(ValueError, match="already the lead"):
            collaborators.add(conn, project_id="p-lead", fellow_id="lead")


def test_add_collaborator_enforces_cap(cohort) -> None:
    _insert_project("p-cap", lead_id="lead")
    extra_ids = ["carol", "diana", "evan", "nina"]
    with db.connection() as conn, db.transaction(conn):
        for fid in extra_ids:
            collaborators.add(conn, project_id="p-cap", fellow_id=fid)
    # A fifth would exceed Chapter 6's group cap.
    with db.connection() as conn, db.transaction(conn):
        with pytest.raises(ValueError, match="caps research groups"):
            collaborators.add(conn, project_id="p-cap", fellow_id="petra")


def test_author_ids_lead_first_then_collaborators(cohort) -> None:
    _insert_project("p-auth", lead_id="lead")
    with db.connection() as conn, db.transaction(conn):
        collaborators.add(conn, project_id="p-auth", fellow_id="diana")
        collaborators.add(conn, project_id="p-auth", fellow_id="carol")
    with db.connection() as conn:
        ids = collaborators.author_ids(conn, "p-auth")
    assert ids[0] == "lead"
    assert sorted(ids[1:]) == ["carol", "diana"]


def test_is_author_for_lead_and_collaborator(cohort) -> None:
    _insert_project("p-is", lead_id="lead")
    with db.connection() as conn, db.transaction(conn):
        collaborators.add(conn, project_id="p-is", fellow_id="carol")
    with db.connection() as conn:
        assert collaborators.is_author(conn, "p-is", "lead")
        assert collaborators.is_author(conn, "p-is", "carol")
        assert not collaborators.is_author(conn, "p-is", "diana")


def test_authored_project_ids_includes_both_roles(cohort) -> None:
    _insert_project("p-as-lead", lead_id="carol")
    _insert_project("p-as-collab", lead_id="lead")
    with db.connection() as conn, db.transaction(conn):
        collaborators.add(conn, project_id="p-as-collab", fellow_id="carol")
    with db.connection() as conn:
        ids = sorted(collaborators.authored_project_ids(conn, "carol"))
    assert ids == ["p-as-collab", "p-as-lead"]


# --- propose validation --------------------------------------------------


def test_validate_collaborators_rejects_lead_in_list(cohort) -> None:
    with db.connection() as conn:
        with pytest.raises(SystemExit, match="cannot also be listed"):
            propose_workflow._validate_collaborators(conn, "lead", ["lead", "carol"])


def test_validate_collaborators_rejects_unknown(cohort) -> None:
    with db.connection() as conn:
        with pytest.raises(SystemExit, match="Unknown Fellow"):
            propose_workflow._validate_collaborators(conn, "lead", ["does-not-exist"])


def test_validate_collaborators_rejects_postulants(cohort) -> None:
    with db.connection() as conn:
        with pytest.raises(SystemExit, match="Postulant"):
            propose_workflow._validate_collaborators(conn, "lead", ["petra"])


def test_validate_collaborators_rejects_retired(cohort) -> None:
    with db.connection() as conn:
        with pytest.raises(SystemExit, match="retired"):
            propose_workflow._validate_collaborators(conn, "lead", ["rita"])


def test_validate_collaborators_rejects_duplicates(cohort) -> None:
    with db.connection() as conn:
        with pytest.raises(SystemExit, match="more than once"):
            propose_workflow._validate_collaborators(conn, "lead", ["carol", "carol"])


def test_validate_collaborators_rejects_overflow(cohort) -> None:
    with db.connection() as conn:
        with pytest.raises(SystemExit, match="caps a research group"):
            propose_workflow._validate_collaborators(
                conn, "lead", ["carol", "diana", "evan", "nina", "lead"]
            )


def test_validate_collaborators_resolves_to_genomes(cohort) -> None:
    with db.connection() as conn:
        out = propose_workflow._validate_collaborators(conn, "lead", ["carol", "diana"])
    assert [g.id for g in out] == ["carol", "diana"]


# --- peer review exclusion ----------------------------------------------


def test_peer_review_excludes_all_co_authors(cohort) -> None:
    """Round-1 reviewer pool excludes lead AND every collaborator."""
    _insert_project("p-exclude", lead_id="lead", state="drafted")
    with db.connection() as conn, db.transaction(conn):
        collaborators.add(conn, project_id="p-exclude", fellow_id="carol")
        collaborators.add(conn, project_id="p-exclude", fellow_id="diana")
    with db.connection() as conn:
        slots = _pick_review_slots(conn, "p-exclude", "lead", 1)
    picked = {s.reviewer_id for s in slots}
    # Lead, carol, and diana all sit out; the only remaining non-postulant,
    # non-retired Fellows are evan and nina.
    assert picked.isdisjoint({"lead", "carol", "diana"})
    assert picked <= {"evan", "nina"}


def test_peer_review_works_without_collaborators(cohort) -> None:
    """No collaborators on the project ⇒ reviewer pool unchanged."""
    _insert_project("p-solo", lead_id="lead", state="drafted")
    with db.connection() as conn:
        slots = _pick_review_slots(conn, "p-solo", "lead", 1)
    picked = {s.reviewer_id for s in slots}
    assert "lead" not in picked
    # All other (non-postulant, non-retired) Fellows are eligible.
    assert picked == {"carol", "diana", "evan"}


# --- reputation aggregation ---------------------------------------------


def test_author_stats_counts_co_authored_publication(cohort) -> None:
    """A Fellow's publication count includes projects where they collaborated."""
    now = datetime.now(UTC).isoformat(timespec="seconds")
    with db.connection() as conn, db.transaction(conn):
        # carol leads one published piece
        conn.execute(
            "INSERT INTO projects "
            "(id, title, state, lead_fellow_id, draft_path, review_round, "
            " created_at, updated_at) "
            "VALUES (?, ?, ?, ?, ?, ?, ?, ?)",
            ("p-led", "x", "published", "carol", "draft.md", 2, now, now),
        )
        # diana leads another, with carol as a collaborator
        conn.execute(
            "INSERT INTO projects "
            "(id, title, state, lead_fellow_id, draft_path, review_round, "
            " created_at, updated_at) "
            "VALUES (?, ?, ?, ?, ?, ?, ?, ?)",
            ("p-collab", "y", "published", "diana", "draft.md", 2, now, now),
        )
        collaborators.add(conn, project_id="p-collab", fellow_id="carol")

    with db.connection() as conn:
        stats = reputation.author_stats(conn, "carol")
    assert stats.publications == 2  # 1 led + 1 co-authored


def test_author_stats_counts_in_flight_co_authored(cohort) -> None:
    now = datetime.now(UTC).isoformat(timespec="seconds")
    with db.connection() as conn, db.transaction(conn):
        conn.execute(
            "INSERT INTO projects "
            "(id, title, state, lead_fellow_id, draft_path, review_round, "
            " created_at, updated_at) "
            "VALUES (?, ?, ?, ?, ?, ?, ?, ?)",
            ("p-wip", "x", "researching", "lead", "draft.md", 1, now, now),
        )
        collaborators.add(conn, project_id="p-wip", fellow_id="carol")
    with db.connection() as conn:
        stats_lead = reputation.author_stats(conn, "lead")
        stats_carol = reputation.author_stats(conn, "carol")
    assert stats_lead.projects_in_flight == 1
    assert stats_carol.projects_in_flight == 1
