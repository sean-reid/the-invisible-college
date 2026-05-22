"""Shared pytest fixtures for the unit suite."""

from __future__ import annotations

from pathlib import Path

import pytest
from freezegun import freeze_time

from institute import db, decisions, paths, workspaces
from institute import fellow as fellow_mod


@pytest.fixture()
def fixed_now():
    """Freeze wall-clock time to a deterministic instant."""
    with freeze_time("2026-05-20T12:00:00Z") as frozen:
        yield frozen


@pytest.fixture()
def isolated(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> Path:
    """Redirect every persistent module path the institute touches into tmp_path."""
    genomes = tmp_path / "genomes"
    fellows = tmp_path / "fellows"
    archive = tmp_path / "archive"
    proposals = archive / "proposals"
    lab_notebooks = archive / "lab-notebooks"
    reviews_dir = archive / "reviews"
    drafts = archive / "drafts"
    publications = archive / "publications"
    decisions_dir = archive / "decisions"
    open_problems_dir = archive / "open-problems"
    admissions_dir = archive / "admissions"
    curriculum_dir = archive / "curriculum"
    abandonments = archive / "abandonments"
    onboarding = archive / "onboarding"
    code_dir = archive / "code"
    reading_groups = archive / "reading-groups"
    preprints = archive / "preprints"
    departments_dir = archive / "departments"
    figures = archive / "figures"
    blog = tmp_path / "blog"
    blog_content = blog / "src" / "content"
    blog_posts = blog_content / "posts"
    blog_notebooks = blog_content / "notebooks"
    blog_reviews = blog_content / "reviews"
    blog_public = blog / "public"
    blog_code = blog_public / "code"
    blog_figures = blog_public / "figures"
    audit_log = tmp_path / "institute-audit.log"
    db_path = tmp_path / "institute.db"

    for d in (
        genomes,
        fellows,
        archive,
        proposals,
        lab_notebooks,
        reviews_dir,
        drafts,
        publications,
        decisions_dir,
        open_problems_dir,
        admissions_dir,
        curriculum_dir,
        abandonments,
        onboarding,
        code_dir,
        reading_groups,
        preprints,
        departments_dir,
        figures,
        blog_posts,
        blog_notebooks,
        blog_reviews,
        blog_code,
        blog_figures,
    ):
        d.mkdir(parents=True, exist_ok=True)

    monkeypatch.setattr(db, "DB_PATH", db_path)
    monkeypatch.setattr(paths, "ROOT", tmp_path)
    monkeypatch.setattr(paths, "GENOMES", genomes)
    monkeypatch.setattr(paths, "FELLOWS", fellows)
    monkeypatch.setattr(paths, "ARCHIVE", archive)
    monkeypatch.setattr(paths, "PROPOSALS", proposals)
    monkeypatch.setattr(paths, "LAB_NOTEBOOKS", lab_notebooks)
    monkeypatch.setattr(paths, "REVIEWS", reviews_dir)
    monkeypatch.setattr(paths, "DRAFTS", drafts)
    monkeypatch.setattr(paths, "PUBLICATIONS", publications)
    monkeypatch.setattr(paths, "DECISIONS", decisions_dir)
    monkeypatch.setattr(paths, "OPEN_PROBLEMS", open_problems_dir)
    monkeypatch.setattr(paths, "ADMISSIONS", admissions_dir)
    monkeypatch.setattr(paths, "CURRICULUM", curriculum_dir)
    monkeypatch.setattr(paths, "ABANDONMENTS", abandonments)
    monkeypatch.setattr(paths, "ONBOARDING", onboarding)
    monkeypatch.setattr(paths, "CODE", code_dir)
    monkeypatch.setattr(paths, "READING_GROUPS", reading_groups)
    monkeypatch.setattr(paths, "PREPRINTS", preprints)
    monkeypatch.setattr(paths, "DEPARTMENTS", departments_dir)
    monkeypatch.setattr(paths, "FIGURES", figures)
    monkeypatch.setattr(paths, "BLOG", blog)
    monkeypatch.setattr(paths, "BLOG_CONTENT", blog_content)
    monkeypatch.setattr(paths, "BLOG_POSTS", blog_posts)
    monkeypatch.setattr(paths, "BLOG_NOTEBOOKS", blog_notebooks)
    monkeypatch.setattr(paths, "BLOG_REVIEWS", blog_reviews)
    monkeypatch.setattr(paths, "BLOG_PUBLIC", blog_public)
    monkeypatch.setattr(paths, "BLOG_CODE", blog_code)
    monkeypatch.setattr(paths, "BLOG_FIGURES", blog_figures)
    monkeypatch.setattr(paths, "AUDIT_LOG", audit_log)
    monkeypatch.setattr(decisions, "DECISIONS", decisions_dir)
    monkeypatch.setattr(fellow_mod, "GENOMES", genomes)
    monkeypatch.setattr(fellow_mod, "FELLOWS", fellows)
    monkeypatch.setattr(workspaces, "FELLOWS", fellows)

    db.initialize(db_path)
    return tmp_path
