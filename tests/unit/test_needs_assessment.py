"""Tests for the Recruitment Needs Assessment workflow.

Pure-helper tests only: payload normalization, coverage rendering,
list coercion. The orchestrator dispatch + Founder prompt are
exercised indirectly via the admit integration; here we cover the
pieces that don't need a Claude call.
"""

from __future__ import annotations

from datetime import UTC, datetime
from pathlib import Path

import pytest

from institute import db
from institute import fellow as fellow_mod
from institute.fellow import Genome
from institute.workflows import needs_assessment as na


def _genome(
    slug: str,
    name: str,
    *,
    rank: str = "fellow",
    spec: str = "general",
    model: str = "claude-sonnet-4-6",
) -> Genome:
    return Genome(
        id=slug,
        name=name,
        rank=rank,
        model=model,
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


def _seed(slug: str, **kwargs) -> None:
    g = _genome(slug, slug.capitalize(), **kwargs)
    with db.connection() as conn, db.transaction(conn):
        fellow_mod.register(conn, g)


# --- _normalize_recommendation -----------------------------------------


def test_normalize_accepts_valid_payload() -> None:
    rec = na._normalize_recommendation(
        {
            "target_size": 3,
            "target_specializations": ["methodology", "critique"],
            "target_models": ["claude-opus-4-7"],
            "orientations": ["empirical"],
            "rationale": "Cohort is sonnet-heavy.",
        }
    )
    assert rec["target_size"] == 3
    assert rec["target_specializations"] == ["methodology", "critique"]
    assert rec["target_models"] == ["claude-opus-4-7"]
    assert rec["orientations"] == ["empirical"]
    assert "sonnet-heavy" in rec["rationale"]


def test_normalize_rejects_zero_size() -> None:
    with pytest.raises(ValueError, match="must be"):
        na._normalize_recommendation({"target_size": 0})


def test_normalize_rejects_oversize() -> None:
    with pytest.raises(ValueError, match="must be"):
        na._normalize_recommendation({"target_size": 12})


def test_normalize_coerces_lists() -> None:
    rec = na._normalize_recommendation(
        {
            "target_size": 2,
            "target_specializations": "methodology",  # single string
            "target_models": None,  # null
            "orientations": ["", "  ", "critical"],  # empty strings filtered
        }
    )
    assert rec["target_specializations"] == ["methodology"]
    assert rec["target_models"] == []
    assert rec["orientations"] == ["critical"]


def test_normalize_strips_strings() -> None:
    rec = na._normalize_recommendation(
        {
            "target_size": 3,
            "target_specializations": ["  methodology  ", "critique"],
            "rationale": "  reason  ",
        }
    )
    assert rec["target_specializations"] == ["methodology", "critique"]
    assert rec["rationale"] == "reason"


# --- _compute_coverage_md -----------------------------------------------


def test_coverage_handles_empty_cohort(isolated: Path) -> None:
    md = na._compute_coverage_md()
    assert "No active Fellows" in md


def test_coverage_flags_model_monoculture(isolated: Path) -> None:
    # 3 of 3 active fellows on the same model → 100%, well above 50%.
    _seed("ada", model="claude-sonnet-4-6", spec="applied")
    _seed("henri", model="claude-sonnet-4-6", spec="theory")
    _seed("michel", model="claude-sonnet-4-6", spec="essay")
    md = na._compute_coverage_md()
    assert "Imbalance" in md
    assert "claude-sonnet-4-6" in md


def test_coverage_no_imbalance_when_mixed(isolated: Path) -> None:
    _seed("ada", model="claude-sonnet-4-6")
    _seed("henri", model="claude-opus-4-7")
    md = na._compute_coverage_md()
    assert "Imbalance" not in md


def test_coverage_surfaces_departed_fellows(isolated: Path) -> None:
    _seed("ada", model="claude-sonnet-4-6")
    _seed("retired-r", model="claude-opus-4-7", spec="cartography")
    with db.connection() as conn, db.transaction(conn):
        conn.execute(
            "UPDATE fellows SET retired_at = ? WHERE id = ?",
            (datetime.now(UTC).isoformat(timespec="seconds"), "retired-r"),
        )
    md = na._compute_coverage_md()
    assert "Departed Fellows" in md
    assert "cartography" in md


def test_coverage_flags_publication_saturation(isolated: Path) -> None:
    _seed("ada", model="claude-sonnet-4-6")
    now = datetime.now(UTC).isoformat(timespec="seconds")
    with db.connection() as conn, db.transaction(conn):
        for i, title in enumerate(
            [
                "Tokenization Splits in Arithmetic",
                "Tokenization Errors in Floating-Point Addition",
                "Tokenization Patterns Across Models",
                "Walking Mind Peripatetic Survey",
            ]
        ):
            conn.execute(
                "INSERT INTO projects "
                "(id, title, state, lead_fellow_id, draft_path, review_round, "
                " created_at, updated_at) "
                "VALUES (?, ?, ?, ?, ?, ?, ?, ?)",
                (f"p{i}", title, "published", "ada", "x.md", 2, now, now),
            )
    md = na._compute_coverage_md()
    assert "Topic saturation" in md
    # `tokenization` appears in 3 of the 4 titles.
    assert "tokenization" in md


# --- _as_list ----------------------------------------------------------


def test_as_list_handles_falsy() -> None:
    assert na._as_list(None) == []
    assert na._as_list("") == []
    assert na._as_list([]) == []


def test_as_list_wraps_string() -> None:
    assert na._as_list("solo") == ["solo"]


def test_as_list_filters_empty() -> None:
    assert na._as_list(["a", "", "  ", "b"]) == ["a", "b"]


# --- _spec_keywords filter (stopwords + min length) --------------------


def test_spec_keywords_drops_stopwords_and_short_tokens() -> None:
    tokens = na._spec_keywords("the analysis of measurement and observation")
    assert "the" not in tokens
    assert "of" not in tokens
    assert "analysis" in tokens
    assert "measurement" in tokens
    assert "observation" in tokens
