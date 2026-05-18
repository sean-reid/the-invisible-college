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
ADMISSIONS = ARCHIVE / "admissions"
CURRICULUM = ARCHIVE / "curriculum"

BLOG = ROOT / "blog"
BLOG_CONTENT = BLOG / "src" / "content"
BLOG_POSTS = BLOG_CONTENT / "posts"
BLOG_NOTEBOOKS = BLOG_CONTENT / "notebooks"
BLOG_REVIEWS = BLOG_CONTENT / "reviews"

DB_PATH = ROOT / "institute.db"
AUDIT_LOG = ROOT / "institute-audit.log"


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
        BLOG_POSTS,
        BLOG_NOTEBOOKS,
        BLOG_REVIEWS,
    ]:
        path.mkdir(parents=True, exist_ok=True)
