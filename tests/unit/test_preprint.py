"""Tests for the preprint workflow's pure plumbing.

Covers the version-detection logic and the structural guarantees of
the archive layout. Claude-invoking paths are exercised through
integration runs, not here.
"""

from __future__ import annotations

from pathlib import Path

import pytest

from institute import paths
from institute.workflows import preprint


@pytest.fixture()
def isolated_preprints(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> Path:
    preprints_dir = tmp_path / "archive" / "preprints"
    preprints_dir.mkdir(parents=True)
    monkeypatch.setattr(paths, "PREPRINTS", preprints_dir)
    return preprints_dir


def test_next_version_starts_at_one_when_empty(isolated_preprints: Path) -> None:
    assert preprint._next_version("p1") == 1


def test_next_version_increments_across_existing(isolated_preprints: Path) -> None:
    project_dir = isolated_preprints / "p1"
    project_dir.mkdir()
    (project_dir / "v1.md").write_text("v1 body")
    (project_dir / "v2.md").write_text("v2 body")
    (project_dir / "v3.md").write_text("v3 body")
    assert preprint._next_version("p1") == 4


def test_next_version_ignores_non_version_files(isolated_preprints: Path) -> None:
    """The directory may contain comments/, metadata files (legacy),
    and other artifacts. Only `v<N>.md` filenames count toward the
    version sequence."""
    project_dir = isolated_preprints / "p1"
    project_dir.mkdir()
    (project_dir / "v1.md").write_text("v1")
    (project_dir / "v2.md").write_text("v2")
    (project_dir / "comments").mkdir()
    (project_dir / "comments" / "ada-on-v1.md").write_text("comment")
    (project_dir / "v1.metadata.md").write_text("legacy")
    (project_dir / "README.md").write_text("notes")
    assert preprint._next_version("p1") == 3


def test_next_version_handles_gap_in_numbering(isolated_preprints: Path) -> None:
    """If a manual edit removed v2.md, the next version is still
    one above the highest present, not the gap. This keeps the
    audit trail ordered."""
    project_dir = isolated_preprints / "p1"
    project_dir.mkdir()
    (project_dir / "v1.md").write_text("v1")
    (project_dir / "v3.md").write_text("v3")
    assert preprint._next_version("p1") == 4
