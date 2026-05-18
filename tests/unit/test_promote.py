"""Tests for the promote workflow's pure logic (tally, formatting, panel discovery)."""

from __future__ import annotations

from pathlib import Path

import pytest

from institute import db, decisions, paths, reputation, workspaces
from institute import fellow as fellow_mod
from institute.fellow import Genome
from institute.workflows import promote


@pytest.fixture()
def isolated(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> Path:
    genomes = tmp_path / "genomes"
    fellows = tmp_path / "fellows"
    archive = tmp_path / "archive"
    decisions_dir = archive / "decisions"
    promotions = archive / "promotions"
    for d in (genomes, fellows, decisions_dir, promotions):
        d.mkdir(parents=True)
    db_path = tmp_path / "institute.db"

    monkeypatch.setattr(db, "DB_PATH", db_path)
    monkeypatch.setattr(decisions, "DECISIONS", decisions_dir)
    monkeypatch.setattr(paths, "GENOMES", genomes)
    monkeypatch.setattr(paths, "FELLOWS", fellows)
    monkeypatch.setattr(paths, "ARCHIVE", archive)
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


# ---------------------------------------------------------------------------
# _tally
# ---------------------------------------------------------------------------


def test_tally_strict_majority_promotes() -> None:
    votes = [
        {"vote": "senior_fellow"},
        {"vote": "senior_fellow"},
        {"vote": "hold"},
    ]
    assert promote._tally(votes, "fellow") == "senior_fellow"


def test_tally_no_majority_holds() -> None:
    votes = [{"vote": "senior_fellow"}, {"vote": "fellow"}, {"vote": "hold"}]
    assert promote._tally(votes, "fellow") is None


def test_tally_majority_hold_returns_none() -> None:
    votes = [{"vote": "hold"}, {"vote": "hold"}, {"vote": "senior_fellow"}]
    assert promote._tally(votes, "fellow") is None


def test_tally_majority_equal_to_current_returns_none() -> None:
    # All votes agree, but the agreement is "stay at the current rank".
    votes = [{"vote": "fellow"}, {"vote": "fellow"}, {"vote": "hold"}]
    assert promote._tally(votes, "fellow") is None


def test_tally_ignores_unknown_votes() -> None:
    votes = [
        {"vote": "garbage"},
        {"vote": "senior_fellow"},
        {"vote": "senior_fellow"},
    ]
    assert promote._tally(votes, "fellow") == "senior_fellow"


def test_tally_empty_returns_none() -> None:
    assert promote._tally([], "fellow") is None


# ---------------------------------------------------------------------------
# _senior_panel
# ---------------------------------------------------------------------------


def test_senior_panel_empty_when_no_seniors(isolated: Path) -> None:
    with db.connection() as conn, db.transaction(conn):
        _seed_fellow(conn, "ada", "Ada")
    assert promote._senior_panel("ada") == []


def test_senior_panel_excludes_candidate(isolated: Path) -> None:
    with db.connection() as conn, db.transaction(conn):
        _seed_fellow(conn, "ada", "Ada", rank="senior_fellow")
        _seed_fellow(conn, "bram", "Bram", rank="senior_fellow")
    panel = promote._senior_panel("ada")
    assert [g.id for g in panel] == ["bram"]


def test_senior_panel_returns_all_seniors(isolated: Path) -> None:
    with db.connection() as conn, db.transaction(conn):
        _seed_fellow(conn, "ada", "Ada")
        _seed_fellow(conn, "bram", "Bram", rank="senior_fellow")
        _seed_fellow(conn, "carol", "Carol", rank="senior_fellow")
    panel = promote._senior_panel("ada")
    assert {g.id for g in panel} == {"bram", "carol"}


# ---------------------------------------------------------------------------
# _is_promotion
# ---------------------------------------------------------------------------


def test_is_promotion_up_the_ladder() -> None:
    assert promote._is_promotion("fellow", "senior_fellow")
    assert promote._is_promotion("novice", "fellow")
    assert promote._is_promotion("postulant", "emeritus")


def test_is_promotion_down_or_equal() -> None:
    assert not promote._is_promotion("senior_fellow", "fellow")
    assert not promote._is_promotion("fellow", "fellow")


# ---------------------------------------------------------------------------
# decision body formatting
# ---------------------------------------------------------------------------


def _rep(rank: str = "fellow") -> reputation.FellowReputation:
    return reputation.FellowReputation(
        fellow_id="ada",
        name="Ada Lovelace",
        rank=rank,
        model="claude-sonnet-4-6",
        specialization="x",
        author=reputation.AuthorStats(
            fellow_id="ada",
            publications=3,
            projects_in_flight=0,
            round_1_majors_received=0,
            round_1_accepts_received=8,
        ),
        reviewer=reputation.ReviewerStats(
            fellow_id="ada",
            reviews_given=12,
            by_round={},
            sticky_majors=4,
        ),
    )


def test_format_decision_body_includes_rationale_and_evidence() -> None:
    body = promote._format_decision_body(
        _rep(),
        "senior_fellow",
        {
            "rationale": "Solid track record.",
            "key_evidence": ["3 publications", "12 reviews"],
            "concerns": "",
        },
        None,
        "2026-05-17T00:00:00+00:00",
    )
    assert "Ada Lovelace" in body
    assert "fellow → senior_fellow" in body
    assert "Solid track record." in body
    assert "- 3 publications" in body


def test_format_decision_body_with_panel_votes() -> None:
    body = promote._format_decision_body(
        _rep(),
        "senior_fellow",
        {"rationale": "ok"},
        [
            {
                "panelist_id": "bram",
                "panelist_name": "Bram",
                "vote": "senior_fellow",
                "rationale": "Substantive reviewer.",
                "concerns": "",
            }
        ],
        "2026-05-17T00:00:00+00:00",
    )
    assert "## Panel votes" in body
    assert "### Bram: `senior_fellow`" in body
    assert "Substantive reviewer." in body


# ---------------------------------------------------------------------------
# _log_review_attempt
# ---------------------------------------------------------------------------


def test_log_review_attempt_writes_decision_row(isolated: Path) -> None:
    with db.connection() as conn, db.transaction(conn):
        _seed_fellow(conn, "ada", "Ada")
    rep = reputation.load_fellow("ada")
    assert rep is not None
    promote._log_review_attempt(rep, {"rationale": "x"}, "founder held", ["founder"], None)
    with db.connection() as conn:
        rows = list(conn.execute("SELECT action FROM audit_log WHERE action = 'promotion_review'"))
    assert len(rows) == 1


# ---------------------------------------------------------------------------
# _apply_rank_change
# ---------------------------------------------------------------------------


def test_apply_rank_change_updates_db_and_genome(isolated: Path) -> None:
    with db.connection() as conn, db.transaction(conn):
        _seed_fellow(conn, "ada", "Ada", rank="fellow")
    rep = reputation.load_fellow("ada")
    assert rep is not None
    promote._apply_rank_change(
        rep,
        "senior_fellow",
        {"rationale": "earned"},
        ["founder", "orchestrator", "ada"],
        None,
    )
    # DB row updated.
    with db.connection() as conn:
        row = conn.execute("SELECT rank FROM fellows WHERE id = 'ada'").fetchone()
    assert row["rank"] == "senior_fellow"
    # Genome file on disk updated.
    g = Genome.from_file(fellow_mod.genome_path("ada"))
    assert g.rank == "senior_fellow"
