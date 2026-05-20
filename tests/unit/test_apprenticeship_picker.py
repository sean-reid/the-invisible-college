"""Autopilot's curriculum and qualifying-project picker queries."""

from __future__ import annotations

from datetime import UTC, datetime
from pathlib import Path

from institute import db
from institute import fellow as fellow_mod
from institute.fellow import Genome


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
