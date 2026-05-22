"""Centralized path resolution for the College.

Every other module asks `paths` where things live. The repository root is
located by walking upward from this file's location until we find one of
the known project markers (pyproject.toml + docs/01-charter.md).
"""

from __future__ import annotations

from pathlib import Path


def _find_root(start: Path) -> Path:
    for candidate in [start, *start.parents]:
        if (candidate / "pyproject.toml").is_file() and (
            candidate / "docs" / "01-charter.md"
        ).is_file():
            return candidate
    raise RuntimeError(
        "Could not locate project root; expected pyproject.toml and docs/01-charter.md"
    )


ROOT: Path = _find_root(Path(__file__).resolve())

DOCS = ROOT / "docs"
CHARTER_FILE = DOCS / "01-charter.md"

GENOMES = ROOT / "genomes"
FELLOWS = ROOT / "fellows"

ARCHIVE = ROOT / "archive"
PROPOSALS = ARCHIVE / "proposals"
LAB_NOTEBOOKS = ARCHIVE / "lab-notebooks"
REVIEWS = ARCHIVE / "reviews"
DRAFTS = ARCHIVE / "drafts"
PUBLICATIONS = ARCHIVE / "publications"
DECISIONS = ARCHIVE / "decisions"
OPEN_PROBLEMS = ARCHIVE / "open-problems"
ADMISSIONS = ARCHIVE / "admissions"
CURRICULUM = ARCHIVE / "curriculum"
ABANDONMENTS = ARCHIVE / "abandonments"
ONBOARDING = ARCHIVE / "onboarding"
CODE = ARCHIVE / "code"
READING_GROUPS = ARCHIVE / "reading-groups"
PREPRINTS = ARCHIVE / "preprints"
DEPARTMENTS = ARCHIVE / "departments"
FIGURES = ARCHIVE / "figures"

BLOG = ROOT / "blog"
BLOG_CONTENT = BLOG / "src" / "content"
BLOG_POSTS = BLOG_CONTENT / "posts"
BLOG_NOTEBOOKS = BLOG_CONTENT / "notebooks"
BLOG_REVIEWS = BLOG_CONTENT / "reviews"
BLOG_PUBLIC = BLOG / "public"
BLOG_CODE = BLOG_PUBLIC / "code"
BLOG_FIGURES = BLOG_PUBLIC / "figures"

DB_PATH = ROOT / "institute.db"
AUDIT_LOG = ROOT / "institute-audit.log"

# Base URL the blog is served under. Must match `base` in
# `blog/astro.config.mjs`. Used by the publish workflow to rewrite
# bare-filename image references in the post body to absolute paths
# that resolve against `blog/public/figures/<id>/` at runtime.
BLOG_BASE_URL = "/the-invisible-college"


def ensure_runtime_dirs() -> None:
    """Create directories that may not yet exist but are needed at runtime."""
    for path in [
        GENOMES,
        FELLOWS,
        ARCHIVE,
        PROPOSALS,
        LAB_NOTEBOOKS,
        REVIEWS,
        DRAFTS,
        PUBLICATIONS,
        DECISIONS,
        ADMISSIONS,
        CURRICULUM,
        OPEN_PROBLEMS,
        ABANDONMENTS,
        ONBOARDING,
        CODE,
        READING_GROUPS,
        PREPRINTS,
        DEPARTMENTS,
        FIGURES,
        BLOG_POSTS,
        BLOG_NOTEBOOKS,
        BLOG_REVIEWS,
        BLOG_CODE,
        BLOG_FIGURES,
    ]:
        path.mkdir(parents=True, exist_ok=True)
