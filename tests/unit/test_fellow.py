"""Tests for the Fellow model and registry helpers."""

import json
from pathlib import Path

import pytest
from pydantic import ValidationError

from institute import db
from institute import fellow as fellow_mod
from institute.fellow import Genome


def _genome_dict() -> dict:
    return {
        "id": "hypatia",
        "name": "Hypatia",
        "rank": "fellow",
        "model": "claude-opus-4-7",
        "specialization": "applied-demonstrations",
        "system_prompt_addendum": "You favor concrete demonstrations over abstract claims.",
        "allowed_tools": ["Read", "Write", "Edit", "Bash"],
    }


def test_genome_round_trip(tmp_path: Path) -> None:
    path = tmp_path / "hypatia.json"
    g = Genome.model_validate(_genome_dict())
    g.write(path)

    loaded = Genome.from_file(path)
    assert loaded == g


def test_genome_id_pattern_is_enforced() -> None:
    bad = _genome_dict() | {"id": "Hypatia With Spaces"}
    with pytest.raises(ValidationError):
        Genome.model_validate(bad)


@pytest.fixture()
def temp_db(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> Path:
    path = tmp_path / "institute.db"
    monkeypatch.setattr(db, "DB_PATH", path)
    monkeypatch.setattr(fellow_mod, "GENOMES", tmp_path / "genomes")
    monkeypatch.setattr(fellow_mod, "FELLOWS", tmp_path / "fellows")
    db.initialize(path)
    return path


def test_register_inserts_then_updates(temp_db: Path, tmp_path: Path) -> None:
    g = Genome.model_validate(_genome_dict())
    g.write(tmp_path / "genomes" / "hypatia.json")

    with db.connection(temp_db) as conn, db.transaction(conn):
        fellow_mod.register(conn, g)

    with db.connection(temp_db) as conn:
        row = conn.execute("SELECT * FROM fellows WHERE id = 'hypatia'").fetchone()
        assert row["name"] == "Hypatia"
        assert row["rank"] == "fellow"
        assert row["specialization"] == "applied-demonstrations"

    g2 = g.model_copy(update={"rank": "senior_fellow"})
    with db.connection(temp_db) as conn, db.transaction(conn):
        fellow_mod.register(conn, g2)

    with db.connection(temp_db) as conn:
        row = conn.execute("SELECT rank FROM fellows WHERE id = 'hypatia'").fetchone()
        assert row["rank"] == "senior_fellow"


def test_load_all_genomes_returns_sorted(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    genomes_dir = tmp_path / "genomes"
    genomes_dir.mkdir()
    monkeypatch.setattr(fellow_mod, "GENOMES", genomes_dir)

    for name in ["zelda", "alpha", "midas"]:
        path = genomes_dir / f"{name}.json"
        path.write_text(json.dumps(_genome_dict() | {"id": name, "name": name}))

    out = fellow_mod.load_all_genomes()
    assert [g.id for g in out] == ["alpha", "midas", "zelda"]
