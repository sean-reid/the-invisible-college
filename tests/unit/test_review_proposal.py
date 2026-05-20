"""Tests for the proposal-review workflow's pure logic.

Most coverage here focuses on _pick_reviewer's conflict-of-interest
exclusion: a Fellow who is the lead OR a collaborator on a proposal
cannot review it. The previous implementation excluded only the lead,
producing a real CoI when an auto-formed research group accepted a
collaborator who then got picked as reviewer.
"""

from __future__ import annotations

from datetime import UTC, datetime
from pathlib import Path

import pytest

from institute import collaborators, db, paths, workspaces
from institute import fellow as fellow_mod
from institute.fellow import Genome
from institute.workflows import review_proposal


@pytest.fixture()
def isolated(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> Path:
    genomes = tmp_path / "genomes"
    fellows = tmp_path / "fellows"
    archive = tmp_path / "archive"
    proposals = archive / "proposals"
    for d in (genomes, fellows, proposals):
        d.mkdir(parents=True)
    db_path = tmp_path / "institute.db"

    monkeypatch.setattr(db, "DB_PATH", db_path)
    monkeypatch.setattr(paths, "GENOMES", genomes)
    monkeypatch.setattr(paths, "FELLOWS", fellows)
    monkeypatch.setattr(paths, "ARCHIVE", archive)
    monkeypatch.setattr(paths, "PROPOSALS", proposals)
    monkeypatch.setattr(paths, "ROOT", tmp_path)
    monkeypatch.setattr(fellow_mod, "GENOMES", genomes)
    monkeypatch.setattr(fellow_mod, "FELLOWS", fellows)
    monkeypatch.setattr(workspaces, "FELLOWS", fellows)
    db.initialize(db_path)
    return tmp_path


def _seed_fellow(conn, fellow_id: str, name: str, rank: str = "fellow") -> Genome:
    g = Genome(
        id=fellow_id,
        name=name,
        rank=rank,
        model="claude-sonnet-4-6",
        specialization=f"spec-{fellow_id}",
        system_prompt_addendum=("body " * 60).strip(),
        allowed_tools=["Read"],
    )
    g.write(fellow_mod.genome_path(g.id))
    fellow_mod.register(conn, g)
    return g


def _seed_project(conn, project_id: str, lead: str) -> None:
    now = datetime.now(UTC).isoformat(timespec="seconds")
    conn.execute(
        "INSERT INTO projects (id, title, state, lead_fellow_id, "
        " proposal_path, created_at, updated_at) "
        "VALUES (?, 't', 'proposed', ?, 'archive/proposals/x/proposal.md', ?, ?)",
        (project_id, lead, now, now),
    )


def test_pick_reviewer_excludes_lead(isolated: Path) -> None:
    with db.connection() as conn, db.transaction(conn):
        _seed_fellow(conn, "ada", "Ada")
        _seed_fellow(conn, "henri", "Henri")
        _seed_project(conn, "p1", lead="henri")

    with db.connection() as conn:
        reviewer = review_proposal._pick_reviewer(conn, "p1")
    assert reviewer.id == "ada"


def test_pick_reviewer_excludes_collaborators(isolated: Path) -> None:
    """The lead and every collaborator are conflicted; reviewer must
    come from outside the research group."""
    with db.connection() as conn, db.transaction(conn):
        _seed_fellow(conn, "ada", "Ada")
        _seed_fellow(conn, "henri", "Henri")
        _seed_fellow(conn, "pierre", "Pierre")
        _seed_project(conn, "p1", lead="henri")
        collaborators.add(conn, project_id="p1", fellow_id="pierre")

    with db.connection() as conn:
        reviewer = review_proposal._pick_reviewer(conn, "p1")
    assert reviewer.id == "ada"
    assert reviewer.id != "henri"
    assert reviewer.id != "pierre"


def test_pick_reviewer_raises_when_everyone_is_conflicted(isolated: Path) -> None:
    with db.connection() as conn, db.transaction(conn):
        _seed_fellow(conn, "ada", "Ada")
        _seed_fellow(conn, "henri", "Henri")
        _seed_project(conn, "p1", lead="henri")
        collaborators.add(conn, project_id="p1", fellow_id="ada")

    with db.connection() as conn, pytest.raises(SystemExit, match="No Fellow available"):
        review_proposal._pick_reviewer(conn, "p1")


def test_pick_reviewer_prefers_critic_specialization(isolated: Path) -> None:
    with db.connection() as conn, db.transaction(conn):
        # `_seed_fellow` builds specialization as `spec-<id>`; override
        # the critic so it actually contains the keyword.
        _seed_fellow(conn, "noncritic", "Noncritic")
        g_critic = Genome(
            id="critic-bayle",
            name="Critic Bayle",
            rank="fellow",
            model="claude-sonnet-4-6",
            specialization="historical critic and skeptic",
            system_prompt_addendum=("body " * 60).strip(),
            allowed_tools=["Read"],
        )
        g_critic.write(fellow_mod.genome_path(g_critic.id))
        fellow_mod.register(conn, g_critic)
        _seed_fellow(conn, "henri", "Henri")
        _seed_project(conn, "p1", lead="henri")

    with db.connection() as conn:
        reviewer = review_proposal._pick_reviewer(conn, "p1")
    assert reviewer.id == "critic-bayle"
