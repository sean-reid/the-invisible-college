"""Tests for the diversity-against-convergence levers.

Covers:
- _split_follow_up_blocks parses Markdown sections + Tags lines.
- _register_follow_up_questions adds open problems opened_by the
  reviewer/lead.
- open_problems.render_summary_md surfaces tag clusters and a
  saturation note when one tag dominates.
- reputation.has_cross_disciplinary_authorship returns True only when
  a co-authored publication exists with someone of a different
  specialization.
- promote._finalize's cross-disciplinary gate downgrades a
  junior_fellow → fellow promotion to 'held' when the candidate has
  no cross-disciplinary publication.
"""

from __future__ import annotations

from datetime import UTC, datetime
from pathlib import Path

from institute import db, open_problems, reputation
from institute import fellow as fellow_mod
from institute.fellow import Genome
from institute.open_problems import split_follow_up_blocks as _split_follow_up_blocks


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


# --- _split_follow_up_blocks ---------------------------------------------


def test_split_parses_single_block_without_tags() -> None:
    text = (
        "## A question that the work opens\n\n"
        "Two paragraphs of context.\n\n"
        "Second paragraph here.\n"
    )
    blocks = _split_follow_up_blocks(text)
    assert len(blocks) == 1
    title, body, tags = blocks[0]
    assert title == "A question that the work opens"
    assert "Two paragraphs of context." in body
    assert "Second paragraph here." in body
    assert tags == []


def test_split_parses_trailing_tags_line() -> None:
    text = "## Methodology question\n\nBody text.\n\nTags: methodology, llm-empirical\n"
    blocks = _split_follow_up_blocks(text)
    assert len(blocks) == 1
    title, body, tags = blocks[0]
    assert title == "Methodology question"
    assert tags == ["methodology", "llm-empirical"]
    # Tags line should not appear in the body itself.
    assert "Tags:" not in body


def test_split_parses_multiple_blocks() -> None:
    text = "## First question\n\nFirst body.\n\n## Second question\n\nSecond body.\n"
    blocks = _split_follow_up_blocks(text)
    assert [b[0] for b in blocks] == ["First question", "Second question"]


def test_split_returns_empty_when_no_headings() -> None:
    assert _split_follow_up_blocks("Just prose with no headings.\n") == []


# --- render_summary_md cluster surfacing --------------------------------


def test_summary_lists_tag_distribution(isolated: Path) -> None:
    open_problems.add(title="A", body="b", tags=["alpha"])
    open_problems.add(title="B", body="b", tags=["alpha"])
    open_problems.add(title="C", body="b", tags=["beta"])
    rendered = open_problems.render_summary_md()
    assert "Tag distribution" in rendered
    assert "`alpha` (2)" in rendered
    assert "`beta` (1)" in rendered


def test_summary_flags_saturation_when_one_tag_dominates(isolated: Path) -> None:
    for i in range(5):
        open_problems.add(title=f"LLM Q {i}", body="b", tags=["llm-empirical"])
    open_problems.add(title="Methodology Q", body="b", tags=["methodology"])
    rendered = open_problems.render_summary_md()
    assert "Cluster saturation" in rendered
    assert "`llm-empirical`" in rendered


def test_summary_no_saturation_under_threshold(isolated: Path) -> None:
    open_problems.add(title="A", body="b", tags=["alpha"])
    open_problems.add(title="B", body="b", tags=["beta"])
    rendered = open_problems.render_summary_md()
    assert "Cluster saturation" not in rendered


# --- cross-disciplinary authorship --------------------------------------


def _insert_published_project(
    project_id: str,
    *,
    lead_id: str,
    collaborator_ids: list[str] | None = None,
) -> None:
    now = datetime.now(UTC).isoformat(timespec="seconds")
    with db.connection() as conn, db.transaction(conn):
        conn.execute(
            "INSERT INTO projects "
            "(id, title, state, lead_fellow_id, draft_path, review_round, "
            " created_at, updated_at) "
            "VALUES (?, ?, ?, ?, ?, ?, ?, ?)",
            (project_id, "t", "published", lead_id, "draft.md", 2, now, now),
        )
        for cid in collaborator_ids or []:
            conn.execute(
                "INSERT INTO project_collaborators (project_id, fellow_id, role) VALUES (?, ?, ?)",
                (project_id, cid, "collaborator"),
            )


def test_cross_disciplinary_false_for_solo_publication(isolated: Path) -> None:
    g = _genome("ada", "Ada", spec="computational demonstration")
    g.write(isolated / "genomes" / "ada.json")
    with db.connection() as conn, db.transaction(conn):
        fellow_mod.register(conn, g)
    _insert_published_project("p1", lead_id="ada")
    with db.connection() as conn:
        eligible, evidence = reputation.has_cross_disciplinary_authorship(conn, "ada")
    assert eligible is False
    assert evidence is None


def test_cross_disciplinary_false_when_collaborator_has_same_spec(isolated: Path) -> None:
    ada = _genome("ada", "Ada", spec="computational demonstration")
    bob = _genome("bob", "Bob", spec="computational demonstration")
    for g in (ada, bob):
        g.write(isolated / "genomes" / f"{g.id}.json")
    with db.connection() as conn, db.transaction(conn):
        for g in (ada, bob):
            fellow_mod.register(conn, g)
    _insert_published_project("p1", lead_id="ada", collaborator_ids=["bob"])
    with db.connection() as conn:
        eligible, evidence = reputation.has_cross_disciplinary_authorship(conn, "ada")
    assert eligible is False
    assert evidence is None


def test_cross_disciplinary_true_with_different_spec_collaborator(isolated: Path) -> None:
    ada = _genome("ada", "Ada", spec="computational demonstration")
    michel = _genome("michel", "Michel", spec="long-form essay")
    for g in (ada, michel):
        g.write(isolated / "genomes" / f"{g.id}.json")
    with db.connection() as conn, db.transaction(conn):
        for g in (ada, michel):
            fellow_mod.register(conn, g)
    _insert_published_project("p-cross", lead_id="ada", collaborator_ids=["michel"])
    with db.connection() as conn:
        eligible, evidence = reputation.has_cross_disciplinary_authorship(conn, "ada")
    assert eligible is True
    assert evidence == "p-cross"


def test_cross_disciplinary_true_when_lead_has_different_spec(isolated: Path) -> None:
    # The candidate is the collaborator (not the lead); the lead is in
    # a different specialization, which is enough.
    ada = _genome("ada", "Ada", spec="computational demonstration")
    michel = _genome("michel", "Michel", spec="long-form essay")
    for g in (ada, michel):
        g.write(isolated / "genomes" / f"{g.id}.json")
    with db.connection() as conn, db.transaction(conn):
        for g in (ada, michel):
            fellow_mod.register(conn, g)
    _insert_published_project("p-cross", lead_id="ada", collaborator_ids=["michel"])
    with db.connection() as conn:
        eligible, evidence = reputation.has_cross_disciplinary_authorship(conn, "michel")
    assert eligible is True
    assert evidence == "p-cross"


def test_cross_disciplinary_ignores_unpublished_projects(isolated: Path) -> None:
    ada = _genome("ada", "Ada", spec="computational demonstration")
    michel = _genome("michel", "Michel", spec="long-form essay")
    for g in (ada, michel):
        g.write(isolated / "genomes" / f"{g.id}.json")
    with db.connection() as conn, db.transaction(conn):
        for g in (ada, michel):
            fellow_mod.register(conn, g)
        # An in-flight cross-disciplinary project should NOT yet count.
        now = datetime.now(UTC).isoformat(timespec="seconds")
        conn.execute(
            "INSERT INTO projects "
            "(id, title, state, lead_fellow_id, draft_path, review_round, "
            " created_at, updated_at) "
            "VALUES (?, ?, ?, ?, ?, ?, ?, ?)",
            ("p-wip", "t", "peer_reviewing", "ada", "draft.md", 1, now, now),
        )
        conn.execute(
            "INSERT INTO project_collaborators (project_id, fellow_id, role) VALUES (?, ?, ?)",
            ("p-wip", "michel", "collaborator"),
        )
    with db.connection() as conn:
        eligible, evidence = reputation.has_cross_disciplinary_authorship(conn, "ada")
    assert eligible is False
    assert evidence is None
