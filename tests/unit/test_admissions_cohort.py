"""Tests for cohort_calls + sponsorships modules + admit integration."""

from __future__ import annotations

from datetime import UTC, datetime
from pathlib import Path

import pytest

from institute import cohort_calls, db, sponsorships
from institute import fellow as fellow_mod
from institute.fellow import Genome


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
def isolated(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> Path:
    monkeypatch.setattr(fellow_mod, "GENOMES", tmp_path / "genomes")
    monkeypatch.setattr(fellow_mod, "FELLOWS", tmp_path / "fellows")
    db_path = tmp_path / "institute.db"
    monkeypatch.setattr(db, "DB_PATH", db_path)
    db.initialize(db_path)
    (tmp_path / "genomes").mkdir(exist_ok=True)
    return tmp_path


def _seed_fellow(slug: str, *, rank: str = "fellow", spec: str = "general") -> None:
    g = _genome(slug, slug.capitalize(), rank=rank, spec=spec)
    with db.connection() as conn, db.transaction(conn):
        fellow_mod.register(conn, g)


# --- cohort_calls -------------------------------------------------------


def test_open_call_persists_and_returns(isolated: Path) -> None:
    call = cohort_calls.open_call(
        target_size=3,
        target_specializations=["methodology", "critique"],
        target_models=["claude-opus-4-7"],
        orientations=["empirical"],
        opened_by="founder",
    )
    assert call.status == "open"
    assert call.target_size == 3
    assert call.target_specializations == ["methodology", "critique"]
    assert call.target_models == ["claude-opus-4-7"]
    assert call.orientations == ["empirical"]
    assert call.admits_count == 0


def test_open_call_rejects_second_open(isolated: Path) -> None:
    cohort_calls.open_call(target_size=3)
    with pytest.raises(ValueError, match="already open"):
        cohort_calls.open_call(target_size=2)


def test_open_call_rejects_zero_size(isolated: Path) -> None:
    with pytest.raises(ValueError, match="must be"):
        cohort_calls.open_call(target_size=0)


def test_close_call_idempotent(isolated: Path) -> None:
    call = cohort_calls.open_call(target_size=3)
    closed = cohort_calls.close_call(call.id)
    assert closed.status == "closed"
    closed_again = cohort_calls.close_call(call.id)
    assert closed_again.status == "closed"
    assert closed.closed_at == closed_again.closed_at


def test_current_call_returns_open(isolated: Path) -> None:
    assert cohort_calls.current_call() is None
    call = cohort_calls.open_call(target_size=2)
    cur = cohort_calls.current_call()
    assert cur is not None and cur.id == call.id
    cohort_calls.close_call(call.id)
    assert cohort_calls.current_call() is None


def test_increment_admits_auto_closes_when_target_reached(isolated: Path) -> None:
    call = cohort_calls.open_call(target_size=2)
    with db.connection() as conn, db.transaction(conn):
        first = cohort_calls.increment_admits(conn, call.id)
    assert first.status == "open"
    assert first.admits_count == 1
    with db.connection() as conn, db.transaction(conn):
        second = cohort_calls.increment_admits(conn, call.id)
    assert second.status == "closed"
    assert second.admits_count == 2
    assert second.closed_reason == "target_size reached"


def test_render_for_admit_includes_targets(isolated: Path) -> None:
    call = cohort_calls.open_call(
        target_size=3,
        target_specializations=["methodology"],
        target_models=["opus"],
        orientations=["empirical"],
    )
    md = cohort_calls.render_for_admit(call)
    assert "methodology" in md
    assert "opus" in md
    assert "empirical" in md
    assert "3" in md


# --- sponsorships -------------------------------------------------------


def test_nominate_requires_eligible_sponsor(isolated: Path) -> None:
    _seed_fellow("ada", rank="postulant")
    with pytest.raises(ValueError, match="Junior Fellow rank or above"):
        sponsorships.nominate(sponsor_id="ada", rationale="Want X")


def test_nominate_rejects_retired_sponsor(isolated: Path) -> None:
    _seed_fellow("ada", rank="senior_fellow")
    with db.connection() as conn, db.transaction(conn):
        conn.execute(
            "UPDATE fellows SET retired_at = ? WHERE id = ?",
            (datetime.now(UTC).isoformat(timespec="seconds"), "ada"),
        )
    with pytest.raises(ValueError, match="retired"):
        sponsorships.nominate(sponsor_id="ada", rationale="X")


def test_nominate_records_pending(isolated: Path) -> None:
    _seed_fellow("ada", rank="senior_fellow")
    n = sponsorships.nominate(sponsor_id="ada", rationale="Need methodology Fellow")
    assert n.outcome == "pending"
    assert n.rationale == "Need methodology Fellow"


def test_nominate_rejects_empty_rationale(isolated: Path) -> None:
    _seed_fellow("ada", rank="senior_fellow")
    with pytest.raises(ValueError, match="non-empty"):
        sponsorships.nominate(sponsor_id="ada", rationale="   ")


def test_nominate_with_closed_call_rejected(isolated: Path) -> None:
    _seed_fellow("ada", rank="senior_fellow")
    call = cohort_calls.open_call(target_size=1)
    cohort_calls.close_call(call.id)
    with pytest.raises(ValueError, match="closed"):
        sponsorships.nominate(sponsor_id="ada", rationale="X", cohort_call_id=call.id)


def test_record_outcome_transitions(isolated: Path) -> None:
    _seed_fellow("ada", rank="senior_fellow")
    n = sponsorships.nominate(sponsor_id="ada", rationale="Need X")
    updated = sponsorships.record_outcome(n.id, outcome="admitted", candidate_fellow_id="cand-1")
    assert updated.outcome == "admitted"
    assert updated.candidate_fellow_id == "cand-1"
    assert updated.resolved_at is not None


def test_record_outcome_rejects_invalid(isolated: Path) -> None:
    _seed_fellow("ada", rank="senior_fellow")
    n = sponsorships.nominate(sponsor_id="ada", rationale="X")
    with pytest.raises(ValueError, match="Invalid outcome"):
        sponsorships.record_outcome(n.id, outcome="not_a_real_outcome")


def test_success_rate_ignores_pending_and_withdrawn(isolated: Path) -> None:
    _seed_fellow("ada", rank="senior_fellow")
    pending = sponsorships.nominate(sponsor_id="ada", rationale="X")
    admitted = sponsorships.nominate(sponsor_id="ada", rationale="Y")
    rejected = sponsorships.nominate(sponsor_id="ada", rationale="Z")
    withdrawn = sponsorships.nominate(sponsor_id="ada", rationale="W")
    sponsorships.record_outcome(admitted.id, outcome="admitted")
    sponsorships.record_outcome(rejected.id, outcome="rejected")
    sponsorships.record_outcome(withdrawn.id, outcome="withdrawn")

    successes, resolved, rate = sponsorships.success_rate("ada")
    assert successes == 1  # only admitted counts
    assert resolved == 2  # admitted + rejected
    assert rate == 0.5
    # pending is the lone untouched record
    pending_check = next(s for s in sponsorships.list_sponsorships("ada") if s.id == pending.id)
    assert pending_check.outcome == "pending"


def test_success_rate_no_resolved_returns_none(isolated: Path) -> None:
    _seed_fellow("ada", rank="senior_fellow")
    sponsorships.nominate(sponsor_id="ada", rationale="X")
    successes, resolved, rate = sponsorships.success_rate("ada")
    assert successes == 0
    assert resolved == 0
    assert rate is None


def test_render_sponsor_reputation_empty_signals_first_time(isolated: Path) -> None:
    _seed_fellow("ada", rank="senior_fellow")
    md = sponsorships.render_sponsor_reputation_md("ada")
    assert "no resolved sponsorships" in md


def test_render_sponsor_reputation_shows_ratio(isolated: Path) -> None:
    _seed_fellow("ada", rank="senior_fellow")
    n1 = sponsorships.nominate(sponsor_id="ada", rationale="X")
    n2 = sponsorships.nominate(sponsor_id="ada", rationale="Y")
    sponsorships.record_outcome(n1.id, outcome="admitted")
    sponsorships.record_outcome(n2.id, outcome="rejected")
    md = sponsorships.render_sponsor_reputation_md("ada")
    assert "1/2" in md
    assert "50%" in md


def test_advanced_outcome_counts_as_success(isolated: Path) -> None:
    _seed_fellow("ada", rank="senior_fellow")
    n = sponsorships.nominate(sponsor_id="ada", rationale="X")
    sponsorships.record_outcome(n.id, outcome="advanced")
    successes, resolved, rate = sponsorships.success_rate("ada")
    assert successes == 1
    assert resolved == 1
    assert rate == 1.0
