"""Promotion side-effects: panel discovery, decision body, rank-change, release."""

from __future__ import annotations

from pathlib import Path

from institute import db, reputation
from institute import fellow as fellow_mod
from institute.fellow import Genome
from institute.workflows import promote


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


# ---------------------------------------------------------------------------
# _apply_release
# ---------------------------------------------------------------------------


def test_apply_release_sets_retired_at_and_records_decision(isolated: Path) -> None:
    with db.connection() as conn, db.transaction(conn):
        _seed_fellow(conn, "ada", "Ada", rank="fellow")
    rep = reputation.load_fellow("ada")
    assert rep is not None
    promote._apply_release(
        rep,
        {"rationale": "two holds, no activity"},
        ["founder", "orchestrator", "ada"],
        None,
    )
    with db.connection() as conn:
        row = conn.execute("SELECT rank, retired_at FROM fellows WHERE id = 'ada'").fetchone()
    assert row["retired_at"] is not None, "retired_at must be set on release"
    assert row["rank"] == "fellow", "rank stays put; release is orthogonal to demotion"
    # Decision row written under the release kind.
    with db.connection() as conn:
        kinds = [
            r["action"]
            for r in conn.execute("SELECT action FROM audit_log WHERE action = 'release'")
        ]
    assert kinds == ["release"]


def test_release_removes_fellow_from_active_workflows(isolated: Path) -> None:
    """Released Fellows should not show up in cohort_reputation or _senior_panel."""
    with db.connection() as conn, db.transaction(conn):
        _seed_fellow(conn, "active", "Active Fellow", rank="senior_fellow")
        _seed_fellow(conn, "released", "Released Fellow", rank="senior_fellow")
    rep = reputation.load_fellow("released")
    assert rep is not None
    promote._apply_release(rep, {"rationale": "x"}, ["founder", "released"], None)

    # Cohort no longer includes the released Fellow.
    cohort_ids = {r.fellow_id for r in reputation.load_cohort()}
    assert "released" not in cohort_ids
    assert "active" in cohort_ids

    # Senior panel excludes released Fellows even when looking from another.
    panel = promote._senior_panel("someone-else")
    assert {g.id for g in panel} == {"active"}
