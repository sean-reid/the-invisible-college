"""Collaborator module: persistence, caps, author resolution."""

from __future__ import annotations

from datetime import UTC, datetime
from pathlib import Path

import pytest

from institute import collaborators, db
from institute import fellow as fellow_mod
from institute.fellow import Genome


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
