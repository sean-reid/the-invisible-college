"""Propose-time validation of co-author lists."""

from __future__ import annotations

from datetime import UTC, datetime
from pathlib import Path

import pytest

from institute import db
from institute import fellow as fellow_mod
from institute.fellow import Genome
from institute.workflows import propose as propose_workflow


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
        conn.execute(
            "UPDATE fellows SET retired_at = ? WHERE id = ?",
            (datetime.now(UTC).isoformat(timespec="seconds"), "rita"),
        )
    return fellows


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
