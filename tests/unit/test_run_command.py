"""Tests for the `institute run` autonomous loop's helpers.

We do not exercise the full loop here because it makes real subprocess
calls to claude. We test the cost-aggregation helper and the
project-picking helper.
"""

from __future__ import annotations

import json
from datetime import UTC, datetime
from pathlib import Path

import pytest

from institute import cli, db, paths
from institute import fellow as fellow_mod
from institute.fellow import Genome


@pytest.fixture()
def audit_log(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> Path:
    log = tmp_path / "audit.log"
    monkeypatch.setattr(paths, "AUDIT_LOG", log)
    return log


def test_audit_cost_total_returns_zero_when_missing(audit_log: Path) -> None:
    assert cli._audit_cost_total() == 0.0


def test_audit_cost_total_sums_cost_usd(audit_log: Path) -> None:
    audit_log.write_text(
        "\n".join(
            [
                json.dumps({"step": "a", "cost_usd": 0.12}),
                json.dumps({"step": "b", "cost_usd": 0.34}),
                json.dumps({"step": "c", "cost_usd": None}),  # null is fine
                json.dumps({"step": "d"}),  # missing cost is fine
                "",  # blank lines tolerated
            ]
        )
        + "\n"
    )
    assert cli._audit_cost_total() == pytest.approx(0.46)


def test_audit_cost_total_tolerates_garbage_lines(audit_log: Path) -> None:
    audit_log.write_text(
        "\n".join(
            [
                "not json",
                json.dumps({"cost_usd": 1.0}),
                "{half open",
                json.dumps({"cost_usd": 2.5}),
            ]
        )
    )
    assert cli._audit_cost_total() == pytest.approx(3.5)


@pytest.fixture()
def db_with_projects(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> Path:
    db_path = tmp_path / "institute.db"
    monkeypatch.setattr(db, "DB_PATH", db_path)
    monkeypatch.setattr(fellow_mod, "GENOMES", tmp_path / "genomes")
    monkeypatch.setattr(fellow_mod, "FELLOWS", tmp_path / "fellows")
    (tmp_path / "genomes").mkdir()
    db.initialize(db_path)

    genome = Genome(
        id="ada",
        name="Ada",
        rank="fellow",
        model="claude-sonnet-4-6",
        specialization="x",
        system_prompt_addendum=("Short addendum. " * 12).strip(),
        allowed_tools=["Read"],
    )
    genome.write(tmp_path / "genomes" / "ada.json")
    now = datetime.now(UTC).isoformat(timespec="seconds")
    with db.connection() as conn, db.transaction(conn):
        fellow_mod.register(conn, genome)
        # An in-flight project and a published one.
        conn.execute(
            "INSERT INTO projects "
            "(id, title, state, lead_fellow_id, draft_path, created_at, updated_at) "
            "VALUES (?, ?, ?, ?, ?, ?, ?)",
            ("p-live", "live", "proposed", "ada", "x.md", now, now),
        )
        conn.execute(
            "INSERT INTO projects "
            "(id, title, state, lead_fellow_id, draft_path, created_at, updated_at) "
            "VALUES (?, ?, ?, ?, ?, ?, ?)",
            ("p-done", "done", "published", "ada", "x.md", now, now),
        )
    return db_path


def test_pick_in_flight_project_skips_terminal(db_with_projects: Path) -> None:
    row = cli._pick_in_flight_project(None)
    assert row is not None
    assert row["id"] == "p-live"


def test_pick_in_flight_project_by_id(db_with_projects: Path) -> None:
    row = cli._pick_in_flight_project("p-done")
    assert row is not None
    assert row["state"] == "published"  # caller decides what to do


def test_pick_in_flight_project_returns_none_when_missing(
    db_with_projects: Path,
) -> None:
    row = cli._pick_in_flight_project("does-not-exist")
    assert row is None
