"""Qualifying-project plumbing: advisor-as-primary slot and auto-promotion."""

from __future__ import annotations

from datetime import UTC, datetime
from pathlib import Path

from institute import db
from institute import fellow as fellow_mod
from institute.fellow import Genome
from institute.workflows.peer_review import _pick_review_slots


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


def test_qualifying_brief_forbids_collaborators() -> None:
    """Qualifying projects are solo work under advisor supervision
    (Chapter 5). The brief must explicitly forbid co-authors so a
    Postulant cannot list collaborators that the workflow would
    silently ignore."""
    from institute.workflows import qualify

    brief = qualify.PROPOSE_BRIEF
    # The Collaborators section was removed entirely; no `##
    # Collaborators` heading in the proposal-shape instructions.
    assert "## Collaborators" not in brief
    # The constraint must explicitly tell the Postulant this is solo work.
    assert "solo work" in brief.lower()
