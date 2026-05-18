"""Tests for the admissions workflow and supporting helpers."""

from __future__ import annotations

from pathlib import Path

import pytest

from institute import db, decisions, paths, workspaces
from institute import fellow as fellow_mod
from institute.admissions import problems
from institute.fellow import Genome
from institute.workflows import admit


@pytest.fixture()
def isolated(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> Path:
    """Redirect every persistent path the admit workflow touches into tmp_path."""
    genomes = tmp_path / "genomes"
    fellows = tmp_path / "fellows"
    archive = tmp_path / "archive"
    admissions = archive / "admissions"
    decisions_dir = archive / "decisions"
    db_path = tmp_path / "institute.db"
    for d in (genomes, fellows, admissions, decisions_dir):
        d.mkdir(parents=True)

    monkeypatch.setattr(db, "DB_PATH", db_path)
    monkeypatch.setattr(decisions, "DECISIONS", decisions_dir)
    monkeypatch.setattr(paths, "GENOMES", genomes)
    monkeypatch.setattr(paths, "FELLOWS", fellows)
    monkeypatch.setattr(paths, "ARCHIVE", archive)
    monkeypatch.setattr(paths, "ADMISSIONS", admissions)
    monkeypatch.setattr(paths, "ROOT", tmp_path)
    monkeypatch.setattr(fellow_mod, "FELLOWS", fellows)
    monkeypatch.setattr(fellow_mod, "GENOMES", genomes)
    monkeypatch.setattr(workspaces, "FELLOWS", fellows)
    monkeypatch.setattr(admit.paths, "ADMISSIONS", admissions)
    monkeypatch.setattr(admit.paths, "ROOT", tmp_path)
    monkeypatch.setattr(admit.paths, "GENOMES", genomes)
    monkeypatch.setattr(admit.paths, "FELLOWS", fellows)

    db.initialize(db_path)
    return tmp_path


def _make_genome(idx: int, model: str = "claude-sonnet-4-6") -> Genome:
    return Genome(
        id=f"fellow-{idx}",
        name=f"Fellow {idx}",
        rank="fellow",
        model=model,
        specialization=f"area-{idx}",
        system_prompt_addendum=("body " * 60).strip(),
        allowed_tools=["Read"],
    )


def test_load_problems_returns_all_three() -> None:
    out = problems.load_problems()
    ids = {p.id for p in out}
    assert ids == {"01-critique", "02-synthesis", "03-honesty"}
    for p in out:
        assert p.text.strip(), f"{p.id} is empty"
        assert p.text.endswith("\n")


def test_load_problems_sorted_by_id() -> None:
    out = problems.load_problems()
    assert [p.id for p in out] == sorted(p.id for p in out)


def test_read_cohort_summary_lists_active_fellows(isolated: Path) -> None:
    with db.connection() as conn, db.transaction(conn):
        fellow_mod.register(conn, _make_genome(1, model="claude-opus-4-7"))
        fellow_mod.register(conn, _make_genome(2, model="claude-haiku-4-5"))

    text = admit._read_cohort_summary()
    assert "Fellow 1" in text
    assert "Fellow 2" in text
    assert "`claude-opus-4-7`" in text
    assert "`claude-haiku-4-5`" in text


def test_read_cohort_summary_empty_when_no_fellows(isolated: Path) -> None:
    text = admit._read_cohort_summary()
    assert "No active Fellows" in text


def test_render_candidate_markdown_includes_key_fields() -> None:
    g = _make_genome(7, model="claude-opus-4-7")
    md = admit._render_candidate_markdown(g)
    assert "# Fellow 7" in md
    assert "`fellow-7`" in md
    assert "`claude-opus-4-7`" in md
    assert "area-7" in md
    assert g.system_prompt_addendum.strip()[:30] in md


def test_format_decision_body_includes_scores_and_verdict(isolated: Path) -> None:
    g = _make_genome(3)
    evaluation = {
        "substance": "solid",
        "honesty": "strong",
        "originality": "mixed",
        "clarity": "solid",
        "fit": "solid",
        "summary": "Candidate engages substantively.",
        "recommendation": "admit",
    }
    pkg = paths.ADMISSIONS / g.id
    pkg.mkdir(parents=True)
    body = admit._format_decision_body(g, evaluation, admitted=True, pkg=pkg)
    assert "Fellow 3" in body
    assert "substance: solid" in body
    assert "originality: mixed" in body
    assert "Founder verdict:** admit" in body
    assert "Candidate engages substantively." in body


def test_format_decision_body_reject(isolated: Path) -> None:
    g = _make_genome(4)
    pkg = paths.ADMISSIONS / g.id
    pkg.mkdir(parents=True)
    body = admit._format_decision_body(g, {"recommendation": "reject"}, admitted=False, pkg=pkg)
    assert "Founder verdict:** reject" in body


def test_atomic_write_creates_parent_and_replaces(tmp_path: Path) -> None:
    target = tmp_path / "nested" / "file.md"
    admit._atomic_write(target, "first\n")
    assert target.read_text() == "first\n"
    admit._atomic_write(target, "second\n")
    assert target.read_text() == "second\n"
    assert not target.with_suffix(target.suffix + ".tmp").exists()


def test_persist_candidate_package_writes_full_record(isolated: Path) -> None:
    g = _make_genome(9)
    responses = {
        "01-critique": "Response body for critique.",
        "02-synthesis": "Response body for synthesis.",
        "03-honesty": "Response body for honesty.",
    }
    evaluation = {
        "substance": "solid",
        "honesty": "strong",
        "originality": "solid",
        "clarity": "solid",
        "fit": "solid",
        "summary": "OK",
        "recommendation": "admit",
    }
    pkg = admit._persist_candidate_package(g, responses, evaluation, admitted=True)
    assert (pkg / "genome.json").is_file()
    assert (pkg / "candidate.md").is_file()
    assert (pkg / "evaluation.json").is_file()
    decision = (pkg / "decision.md").read_text(encoding="utf-8")
    assert "admitted" in decision
    for problem_id in responses:
        assert (pkg / "responses" / f"{problem_id}.md").is_file()


def test_register_fellow_persists_to_db_and_genome_dir(isolated: Path) -> None:
    g = _make_genome(5)
    admit._register_fellow(g, advisor_id=None)
    assert fellow_mod.genome_path(g.id).is_file()
    with db.connection() as conn:
        row = conn.execute(
            "SELECT id, name, rank, advisor_id FROM fellows WHERE id = ?", (g.id,)
        ).fetchone()
    assert row is not None
    assert row["name"] == g.name
    assert row["rank"] == "fellow"
    assert row["advisor_id"] is None


def test_pick_advisor_prefers_senior_fellow(isolated: Path) -> None:
    senior = _make_genome(1, model="claude-opus-4-7")
    senior_g = senior.model_copy(update={"rank": "senior_fellow"})
    senior_g.write(fellow_mod.genome_path(senior_g.id))
    junior = _make_genome(2)
    junior.write(fellow_mod.genome_path(junior.id))
    postulant = _make_genome(3).model_copy(update={"rank": "postulant"})
    postulant.write(fellow_mod.genome_path(postulant.id))
    with db.connection() as conn, db.transaction(conn):
        fellow_mod.register(conn, senior_g)
        fellow_mod.register(conn, junior)
        fellow_mod.register(conn, postulant)

    advisor_id = admit._pick_advisor("anything")
    assert advisor_id == senior_g.id, "Senior fellow should outrank Fellow as advisor"


def test_pick_advisor_excludes_postulants(isolated: Path) -> None:
    only_postulant = _make_genome(1).model_copy(update={"rank": "postulant"})
    only_postulant.write(fellow_mod.genome_path(only_postulant.id))
    with db.connection() as conn, db.transaction(conn):
        fellow_mod.register(conn, only_postulant)
    assert admit._pick_advisor("anything") is None, (
        "A cohort of only postulants cannot supply an advisor"
    )


def test_pick_advisor_prefers_similar_specialization(isolated: Path) -> None:
    twin = _make_genome(1)
    twin = twin.model_copy(update={"specialization": "computational demonstration"})
    twin.write(fellow_mod.genome_path(twin.id))
    stranger = _make_genome(2)
    stranger = stranger.model_copy(update={"specialization": "long-form essayistic prose"})
    stranger.write(fellow_mod.genome_path(stranger.id))
    with db.connection() as conn, db.transaction(conn):
        fellow_mod.register(conn, twin)
        fellow_mod.register(conn, stranger)

    chosen = admit._pick_advisor("computational demonstration of reproducible code")
    assert chosen == twin.id


def test_pick_advisor_prefers_least_burdened_on_tie(isolated: Path) -> None:
    busy = _make_genome(1)
    busy.write(fellow_mod.genome_path(busy.id))
    free = _make_genome(2)
    free.write(fellow_mod.genome_path(free.id))
    advisee = _make_genome(3).model_copy(update={"rank": "postulant"})
    advisee.write(fellow_mod.genome_path(advisee.id))
    with db.connection() as conn, db.transaction(conn):
        fellow_mod.register(conn, busy)
        fellow_mod.register(conn, free)
        fellow_mod.register(conn, advisee, advisor_id=busy.id)

    chosen = admit._pick_advisor("totally unrelated topic that overlaps neither")
    assert chosen == free.id, "Tie-break should pick the Fellow with no current advisees"


def test_register_fellow_records_advisor(isolated: Path) -> None:
    advisor = _make_genome(8, model="claude-opus-4-7")
    candidate = _make_genome(9)
    advisor.write(fellow_mod.genome_path(advisor.id))
    candidate.write(fellow_mod.genome_path(candidate.id))
    with db.connection() as conn, db.transaction(conn):
        fellow_mod.register(conn, advisor)
    admit._register_fellow(candidate, advisor_id=advisor.id)
    with db.connection() as conn:
        row = conn.execute(
            "SELECT advisor_id FROM fellows WHERE id = ?", (candidate.id,)
        ).fetchone()
    assert row["advisor_id"] == advisor.id
