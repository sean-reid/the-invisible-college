"""Integration-style tests for the publish workflow.

These tests do not invoke Claude. They simulate the end-state of a project
that has reached EDITORIAL, then run publish.run() and verify the
artifacts it produces match the Astro content collection schemas declared
in blog/src/content.config.ts.
"""

from __future__ import annotations

import json
import re
from datetime import UTC, datetime
from pathlib import Path

import pytest

from institute import db, decisions, paths
from institute import fellow as fellow_mod
from institute.fellow import Genome
from institute.state import State
from institute.workflows import publish


def _make_genome(idx: int, name: str, spec: str) -> Genome:
    return Genome(
        id=name.lower().replace(" ", "-"),
        name=name,
        rank="fellow",
        model="claude-sonnet-4-6",
        specialization=spec,
        system_prompt_addendum=("You think carefully and write directly. " * 8).strip(),
        allowed_tools=["Read", "Write"],
    )


@pytest.fixture()
def staged(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> dict[str, Path]:
    """Set up a fake institute layout in tmp_path and stage a project at EDITORIAL."""
    root = tmp_path
    archive = root / "archive"
    blog_posts = root / "blog" / "src" / "content" / "posts"
    blog_notebooks = root / "blog" / "src" / "content" / "notebooks"
    blog_reviews = root / "blog" / "src" / "content" / "reviews"
    for d in (
        archive / "proposals",
        archive / "lab-notebooks",
        archive / "reviews",
        archive / "drafts",
        archive / "publications",
        archive / "decisions",
        blog_posts,
        blog_notebooks,
        blog_reviews,
        root / "genomes",
    ):
        d.mkdir(parents=True, exist_ok=True)

    monkeypatch.setattr(paths, "ROOT", root)
    monkeypatch.setattr(paths, "ARCHIVE", archive)
    monkeypatch.setattr(paths, "PROPOSALS", archive / "proposals")
    monkeypatch.setattr(paths, "LAB_NOTEBOOKS", archive / "lab-notebooks")
    monkeypatch.setattr(paths, "REVIEWS", archive / "reviews")
    monkeypatch.setattr(paths, "DRAFTS", archive / "drafts")
    monkeypatch.setattr(paths, "PUBLICATIONS", archive / "publications")
    monkeypatch.setattr(paths, "DECISIONS", archive / "decisions")
    monkeypatch.setattr(paths, "BLOG_POSTS", blog_posts)
    monkeypatch.setattr(paths, "BLOG_NOTEBOOKS", blog_notebooks)
    monkeypatch.setattr(paths, "BLOG_REVIEWS", blog_reviews)
    monkeypatch.setattr(paths, "GENOMES", root / "genomes")
    monkeypatch.setattr(decisions, "DECISIONS", archive / "decisions")
    # fellow.py captured GENOMES at import time, so we need to patch its
    # local reference as well.
    monkeypatch.setattr(fellow_mod, "GENOMES", root / "genomes")
    monkeypatch.setattr(fellow_mod, "FELLOWS", root / "fellows")

    db_path = root / "institute.db"
    monkeypatch.setattr(db, "DB_PATH", db_path)
    db.initialize(db_path)

    lead = _make_genome(1, "Hypatia", "applied demonstrations")
    rev1 = _make_genome(2, "Diderot", "critical review")
    rev2 = _make_genome(3, "Margaret Cavendish", "long-form essay")

    for g in (lead, rev1, rev2):
        g.write(root / "genomes" / f"{g.id}.json")
    with db.connection() as conn, db.transaction(conn):
        for g in (lead, rev1, rev2):
            fellow_mod.register(conn, g)

    project_id = "2026-05-17-a-test-finding-ab12"
    draft_path = archive / "drafts" / project_id / "draft.md"
    notebook_path = archive / "lab-notebooks" / project_id / "notebook.md"
    rev1_path = archive / "reviews" / project_id / "review-by-diderot.md"
    rev2_path = archive / "reviews" / project_id / "review-by-margaret-cavendish.md"
    draft_path.parent.mkdir(parents=True, exist_ok=True)
    notebook_path.parent.mkdir(parents=True, exist_ok=True)
    rev1_path.parent.mkdir(parents=True, exist_ok=True)
    rev2_path.parent.mkdir(parents=True, exist_ok=True)

    draft_path.write_text(
        "# A test finding\n\n"
        "This is the lede paragraph of the test finding.\n\n"
        "## Body\n\nMore content goes here. " * 5 + "\n",
        encoding="utf-8",
    )
    notebook_path.write_text(
        "## Day 1\n\nDid some research. Hit a wall. Tried again.\n",
        encoding="utf-8",
    )
    rev1_path.write_text("# Review by Diderot\n\nLooked good to me.\n", encoding="utf-8")
    rev2_path.write_text(
        "# Review by Margaret Cavendish\n\nWell-written but unconvinced on point 3.\n",
        encoding="utf-8",
    )

    now = datetime.now(UTC).isoformat(timespec="seconds")
    with db.connection() as conn, db.transaction(conn):
        conn.execute(
            "INSERT INTO projects "
            "(id, title, state, lead_fellow_id, proposal_path, draft_path, "
            " notebook_path, created_at, updated_at) "
            "VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)",
            (
                project_id,
                "A test finding",
                State.EDITORIAL.value,
                lead.id,
                "archive/proposals/x/proposal.md",
                str(draft_path.relative_to(root)),
                str(notebook_path.relative_to(root)),
                now,
                now,
            ),
        )
        for genome, recommendation, dissent in (
            (rev1, "accept", False),
            (rev2, "minor", False),
        ):
            review_path = rev1_path if genome.id == rev1.id else rev2_path
            conn.execute(
                "INSERT INTO reviews "
                "(id, project_id, reviewer_id, role, recommendation, confidence, "
                " content_path, submitted_at, dissent) "
                "VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)",
                (
                    f"r-{genome.id}",
                    project_id,
                    genome.id,
                    "primary" if genome.id == rev1.id else "outside",
                    recommendation,
                    "confident",
                    str(review_path.relative_to(root)),
                    now,
                    int(dissent),
                ),
            )

    return {
        "root": root,
        "project_id": project_id,
        "blog_posts": blog_posts,
        "blog_notebooks": blog_notebooks,
        "blog_reviews": blog_reviews,
        "publications": archive / "publications",
    }


def _parse_frontmatter(text: str) -> dict:
    """Tiny YAML-frontmatter parser for keys produced by publish.py."""
    m = re.match(r"^---\n(.*?)\n---\n", text, re.DOTALL)
    assert m, "expected frontmatter"
    fm: dict = {}
    for line in m.group(1).splitlines():
        if ":" not in line:
            continue
        key, _, raw_value = line.partition(":")
        key = key.strip()
        value = raw_value.strip()
        if value.startswith('"') and value.endswith('"'):
            fm[key] = value[1:-1].replace('\\"', '"')
        elif value.startswith("["):
            fm[key] = json.loads(value)
        elif value in ("true", "false"):
            fm[key] = value == "true"
        else:
            fm[key] = value
    return fm


def test_publish_writes_publication_and_blog_post(staged: dict[str, Path]) -> None:
    publish.run(staged["project_id"])

    archive_path = staged["publications"] / f"{staged['project_id']}.md"
    blog_path = staged["blog_posts"] / f"{staged['project_id']}.md"
    assert archive_path.exists()
    assert blog_path.exists()

    text = blog_path.read_text(encoding="utf-8")
    fm = _parse_frontmatter(text)
    assert fm["title"] == "A test finding"
    assert fm["authors"] == ["Hypatia"]
    assert fm["projectId"] == staged["project_id"]
    assert fm["hasNotebook"] is True
    assert fm["hasReviews"] is True
    # Reviewers are ordered by role (outside before primary, alphabetically).
    assert sorted(fm["reviewers"]) == ["Diderot", "Margaret Cavendish"]


def test_publish_writes_notebook_and_reviews(staged: dict[str, Path]) -> None:
    publish.run(staged["project_id"])

    nb = staged["blog_notebooks"] / f"{staged['project_id']}.md"
    assert nb.exists()
    nb_fm = _parse_frontmatter(nb.read_text(encoding="utf-8"))
    assert nb_fm["postSlug"] == staged["project_id"]
    assert nb_fm["projectId"] == staged["project_id"]

    review_files = list(staged["blog_reviews"].glob(f"{staged['project_id']}--*.md"))
    assert len(review_files) == 2
    for rf in review_files:
        rfm = _parse_frontmatter(rf.read_text(encoding="utf-8"))
        assert rfm["postSlug"] == staged["project_id"]
        assert rfm["recommendation"] in {"accept", "minor", "major", "reject"}
        assert rfm["confidence"] in {"confident", "moderate", "low"}
        assert rfm["role"] in {"primary", "secondary", "outside"}


def test_publish_transitions_state_to_published(staged: dict[str, Path]) -> None:
    publish.run(staged["project_id"])
    with db.connection() as conn:
        row = conn.execute(
            "SELECT state, publication_slug FROM projects WHERE id = ?",
            (staged["project_id"],),
        ).fetchone()
        assert row["state"] == State.PUBLISHED.value
        assert row["publication_slug"] == staged["project_id"]
