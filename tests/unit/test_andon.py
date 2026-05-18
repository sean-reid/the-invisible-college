"""Tests for andon-cord handling: routing, schema migration, workflow outcomes."""

from __future__ import annotations

from datetime import UTC, datetime
from pathlib import Path

import pytest

from institute import db, decisions, paths, workspaces
from institute import fellow as fellow_mod
from institute.fellow import Genome
from institute.state import ALLOWED_TRANSITIONS, NEXT_ACTION, State
from institute.workflows import andon_review, peer_review


@pytest.fixture()
def isolated(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> Path:
    genomes = tmp_path / "genomes"
    fellows = tmp_path / "fellows"
    archive = tmp_path / "archive"
    drafts = archive / "drafts"
    reviews_dir = archive / "reviews"
    decisions_dir = archive / "decisions"
    for d in (genomes, fellows, drafts, reviews_dir, decisions_dir):
        d.mkdir(parents=True)
    db_path = tmp_path / "institute.db"

    monkeypatch.setattr(db, "DB_PATH", db_path)
    monkeypatch.setattr(decisions, "DECISIONS", decisions_dir)
    monkeypatch.setattr(paths, "GENOMES", genomes)
    monkeypatch.setattr(paths, "FELLOWS", fellows)
    monkeypatch.setattr(paths, "ARCHIVE", archive)
    monkeypatch.setattr(paths, "DRAFTS", drafts)
    monkeypatch.setattr(paths, "REVIEWS", reviews_dir)
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
    g.write(fellow_mod.genome_path(fellow_id))
    fellow_mod.register(conn, g)
    return g


def _seed_project(conn, project_id: str, lead: str) -> None:
    now = datetime.now(UTC).isoformat(timespec="seconds")
    draft_path = paths.DRAFTS / project_id / "draft.md"
    draft_path.parent.mkdir(parents=True, exist_ok=True)
    draft_path.write_text("# Draft body\n\nplaceholder\n", encoding="utf-8")
    conn.execute(
        "INSERT INTO projects (id, title, state, lead_fellow_id, draft_path, "
        "review_round, created_at, updated_at) VALUES (?, ?, ?, ?, ?, 1, ?, ?)",
        (
            project_id,
            f"Title for {project_id}",
            "peer_reviewing",
            lead,
            str(draft_path.relative_to(paths.ROOT)),
            now,
            now,
        ),
    )


def _seed_review(
    conn,
    review_id: str,
    project_id: str,
    reviewer: str,
    rec: str,
    round_no: int,
    andon_cord: bool = False,
    andon_reason: str = "",
) -> None:
    review_path = paths.REVIEWS / project_id / f"review-by-{reviewer}.md"
    review_path.parent.mkdir(parents=True, exist_ok=True)
    review_path.write_text(f"# Review by {reviewer}\n\nbody\n", encoding="utf-8")
    conn.execute(
        "INSERT INTO reviews (id, project_id, reviewer_id, role, recommendation, "
        "confidence, content_path, dissent, round, andon_cord, andon_reason) "
        "VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
        (
            review_id,
            project_id,
            reviewer,
            "primary",
            rec,
            "confident",
            str(review_path.relative_to(paths.ROOT)),
            0,
            round_no,
            int(andon_cord),
            andon_reason or None,
        ),
    )


# ---------------------------------------------------------------------------
# State machine
# ---------------------------------------------------------------------------


def test_andon_review_state_exists() -> None:
    assert State.ANDON_REVIEW == "andon_review"


def test_peer_reviewing_can_transition_to_andon_review() -> None:
    assert State.ANDON_REVIEW in ALLOWED_TRANSITIONS[State.PEER_REVIEWING]


def test_andon_review_transitions_to_editorial_or_rejected() -> None:
    assert ALLOWED_TRANSITIONS[State.ANDON_REVIEW] == {State.EDITORIAL, State.REJECTED}


def test_andon_review_has_next_action() -> None:
    assert NEXT_ACTION[State.ANDON_REVIEW] == "andon_review"


# ---------------------------------------------------------------------------
# Schema migration
# ---------------------------------------------------------------------------


def test_reviews_table_has_andon_columns(isolated: Path) -> None:
    with db.connection() as conn:
        cols = {row["name"] for row in conn.execute("PRAGMA table_info(reviews)")}
    assert "andon_cord" in cols
    assert "andon_reason" in cols


# ---------------------------------------------------------------------------
# Routing: cord pull triggers ANDON_REVIEW
# ---------------------------------------------------------------------------


def test_route_to_andon_review_updates_state(isolated: Path) -> None:
    with db.connection() as conn, db.transaction(conn):
        _seed_fellow(conn, "ada", "Ada")
        _seed_fellow(conn, "bram", "Bram")
        _seed_project(conn, "proj-1", "ada")
        _seed_review(
            conn,
            "rv1",
            "proj-1",
            "bram",
            "major",
            1,
            andon_cord=True,
            andon_reason="reproducibility failure",
        )

    with db.connection() as conn:
        rows = list(
            conn.execute("SELECT reviewer_id, andon_reason FROM reviews WHERE andon_cord = 1")
        )
    assert len(rows) == 1
    peer_review._route_to_andon_review("proj-1", "Test title", 1, rows)

    with db.connection() as conn:
        state = conn.execute("SELECT state FROM projects WHERE id = 'proj-1'").fetchone()
    assert state["state"] == "andon_review"


def test_route_to_andon_review_records_decision(isolated: Path) -> None:
    with db.connection() as conn, db.transaction(conn):
        _seed_fellow(conn, "ada", "Ada")
        _seed_fellow(conn, "bram", "Bram")
        _seed_project(conn, "proj-1", "ada")
        _seed_review(
            conn,
            "rv1",
            "proj-1",
            "bram",
            "major",
            1,
            andon_cord=True,
            andon_reason="charter violation",
        )

    with db.connection() as conn:
        rows = list(
            conn.execute("SELECT reviewer_id, andon_reason FROM reviews WHERE andon_cord = 1")
        )
    peer_review._route_to_andon_review("proj-1", "Test title", 1, rows)

    with db.connection() as conn:
        audit = list(
            conn.execute("SELECT action FROM audit_log WHERE action = 'andon_cord_pulled'")
        )
    assert len(audit) == 1


# ---------------------------------------------------------------------------
# Andon review workflow: panel tally + outcomes
# ---------------------------------------------------------------------------


def test_apply_outcome_dismiss_moves_to_editorial(isolated: Path) -> None:
    with db.connection() as conn, db.transaction(conn):
        _seed_fellow(conn, "ada", "Ada")
        _seed_project(conn, "proj-1", "ada")
        conn.execute("UPDATE projects SET state = 'andon_review' WHERE id = 'proj-1'")
    andon_review._apply_outcome(
        "proj-1",
        "Title",
        "dismiss",
        {"rationale": "frivolous"},
        ["founder", "orchestrator"],
        None,
    )
    with db.connection() as conn:
        state = conn.execute("SELECT state FROM projects WHERE id = 'proj-1'").fetchone()
    assert state["state"] == "editorial"


def test_apply_outcome_sustain_moves_to_rejected(isolated: Path) -> None:
    with db.connection() as conn, db.transaction(conn):
        _seed_fellow(conn, "ada", "Ada")
        _seed_project(conn, "proj-1", "ada")
        conn.execute("UPDATE projects SET state = 'andon_review' WHERE id = 'proj-1'")
    andon_review._apply_outcome(
        "proj-1",
        "Title",
        "sustain",
        {"rationale": "justified"},
        ["founder", "orchestrator"],
        None,
    )
    with db.connection() as conn:
        state = conn.execute("SELECT state FROM projects WHERE id = 'proj-1'").fetchone()
    assert state["state"] == "rejected"


# ---------------------------------------------------------------------------
# Render markdown includes andon section
# ---------------------------------------------------------------------------


def test_review_markdown_renders_andon_section() -> None:
    payload = {
        "summary": "summary text",
        "strengths": "strengths text",
        "concerns": "concerns text",
        "recommendation": "major",
        "confidence": "confident",
        "dissent_intent": False,
        "andon_cord": True,
        "andon_reason": "Plagiarism: substantial overlap with Smith 2024.",
    }
    g = Genome(
        id="bram",
        name="Bram",
        rank="fellow",
        model="claude-sonnet-4-6",
        specialization="x",
        system_prompt_addendum=("body " * 60).strip(),
        allowed_tools=["Read"],
    )
    out = peer_review._render_review_markdown(payload, g, "primary")
    assert "Andon cord pulled:** yes" in out
    assert "## Andon cord" in out
    assert "Plagiarism" in out


def test_review_markdown_no_andon_section_when_not_pulled() -> None:
    payload = {
        "summary": "s",
        "strengths": "st",
        "concerns": "c",
        "recommendation": "minor",
        "confidence": "moderate",
        "dissent_intent": False,
        "andon_cord": False,
        "andon_reason": "",
    }
    g = Genome(
        id="bram",
        name="Bram",
        rank="fellow",
        model="claude-sonnet-4-6",
        specialization="x",
        system_prompt_addendum=("body " * 60).strip(),
        allowed_tools=["Read"],
    )
    out = peer_review._render_review_markdown(payload, g, "primary")
    assert "Andon cord" not in out
