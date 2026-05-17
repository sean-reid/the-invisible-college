"""Fellow model and registry helpers.

A Fellow is identified by a stable id and parameterized by a genome (a JSON
file in genomes/). The registry is the projects table; this module wraps the
common queries and the per-Fellow workspace directory layout.
"""

from __future__ import annotations

import json
import sqlite3
from datetime import UTC, datetime
from pathlib import Path
from typing import Literal

from pydantic import BaseModel, Field

from institute.paths import FELLOWS, GENOMES

Rank = Literal[
    "postulant",
    "novice",
    "junior_fellow",
    "fellow",
    "senior_fellow",
    "emeritus",
]


class Genome(BaseModel):
    """The design artifact for a Fellow: identity plus runtime parameters."""

    id: str = Field(pattern=r"^[a-z][a-z0-9-]{1,40}$")
    name: str
    rank: Rank = "fellow"
    model: str
    specialization: str
    system_prompt_addendum: str
    allowed_tools: list[str] = Field(
        default_factory=lambda: ["Read", "Write", "Edit", "Bash", "WebFetch", "WebSearch"]
    )
    behavioral_notes: dict[str, str] = Field(default_factory=dict)

    @classmethod
    def from_file(cls, path: Path) -> Genome:
        return cls.model_validate_json(path.read_text(encoding="utf-8"))

    def write(self, path: Path) -> None:
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(self.model_dump_json(indent=2) + "\n", encoding="utf-8")


def genome_path(fellow_id: str) -> Path:
    return GENOMES / f"{fellow_id}.json"


def workspace_path(fellow_id: str) -> Path:
    return FELLOWS / fellow_id / "workspace"


def memory_path(fellow_id: str) -> Path:
    return FELLOWS / fellow_id / "memory"


def ensure_fellow_dirs(fellow_id: str) -> None:
    workspace_path(fellow_id).mkdir(parents=True, exist_ok=True)
    memory_path(fellow_id).mkdir(parents=True, exist_ok=True)


def register(
    conn: sqlite3.Connection,
    genome: Genome,
    advisor_id: str | None = None,
) -> None:
    """Insert a Fellow row. Idempotent: re-registering updates rank and advisor."""
    now = datetime.now(UTC).isoformat(timespec="seconds")
    conn.execute(
        """
        INSERT INTO fellows
            (id, name, rank, model, specialization, genome_path, advisor_id, created_at)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        ON CONFLICT(id) DO UPDATE SET
            name = excluded.name,
            rank = excluded.rank,
            model = excluded.model,
            specialization = excluded.specialization,
            genome_path = excluded.genome_path,
            advisor_id = excluded.advisor_id
        """,
        (
            genome.id,
            genome.name,
            genome.rank,
            genome.model,
            genome.specialization,
            str(genome_path(genome.id)),
            advisor_id,
            now,
        ),
    )


def list_all(conn: sqlite3.Connection) -> list[sqlite3.Row]:
    return list(conn.execute("SELECT * FROM fellows WHERE retired_at IS NULL ORDER BY name"))


def load_genome(conn: sqlite3.Connection, fellow_id: str) -> Genome:
    row = conn.execute("SELECT genome_path FROM fellows WHERE id = ?", (fellow_id,)).fetchone()
    if row is None:
        raise KeyError(f"No such fellow: {fellow_id}")
    return Genome.from_file(Path(row["genome_path"]))


def load_all_genomes() -> list[Genome]:
    """Read every genome JSON in genomes/, sorted by id. Used during bootstrap."""
    if not GENOMES.is_dir():
        return []
    paths = sorted(p for p in GENOMES.iterdir() if p.suffix == ".json")
    return [Genome.from_file(p) for p in paths]


# Convenience helpers for tests and scripts.


def dump_genome_dict(genome: Genome) -> str:
    return json.dumps(genome.model_dump(), indent=2)
