"""Tests for safe_io.atomic_write.

Public text files must be redacted before they hit disk. JSON files
and non-public paths must pass through unchanged.
"""

from __future__ import annotations

from pathlib import Path

import pytest

from institute import paths, safe_io


@pytest.fixture()
def archive_path(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> Path:
    monkeypatch.setattr(paths, "ROOT", tmp_path)
    monkeypatch.setattr(paths, "ARCHIVE", tmp_path / "archive")
    monkeypatch.setattr(paths, "BLOG", tmp_path / "blog")
    return tmp_path


def test_archive_markdown_gets_redacted(archive_path: Path) -> None:
    target = archive_path / "archive" / "reviews" / "x" / "review.md"
    body = "The reviewer noted that run cost: $1.23 hit the daily cap.\n"
    report = safe_io.atomic_write(target, body)
    assert report.total >= 1
    assert "$1.23" not in target.read_text()


def test_archive_text_gets_redacted(archive_path: Path) -> None:
    target = archive_path / "archive" / "drafts" / "x" / "abstract.txt"
    safe_io.atomic_write(target, "Compute cost was $5.00.")
    assert "$5.00" not in target.read_text()


def test_blog_content_gets_redacted(archive_path: Path) -> None:
    target = archive_path / "blog" / "src" / "content" / "posts" / "x.md"
    safe_io.atomic_write(target, "We spent $14.00 on this draft.")
    assert "$14.00" not in target.read_text()


def test_archive_json_passes_through(archive_path: Path) -> None:
    target = archive_path / "archive" / "admissions" / "x" / "evaluation.json"
    payload = '{"cost": 1.23, "tokens": 5000}'
    report = safe_io.atomic_write(target, payload)
    assert report.total == 0
    assert target.read_text() == payload


def test_non_public_path_passes_through(archive_path: Path) -> None:
    target = archive_path / "fellows" / "ada" / "notes.md"
    body = "run cost: $4.20 (fellow workspace, not public)."
    report = safe_io.atomic_write(target, body)
    assert report.total == 0
    assert target.read_text() == body


def test_clean_content_unchanged(archive_path: Path) -> None:
    target = archive_path / "archive" / "publications" / "x.md"
    body = "An essay about the moral sentiments of Adam Smith.\n"
    report = safe_io.atomic_write(target, body)
    assert report.total == 0
    assert target.read_text() == body


def test_atomic_write_creates_parent_dirs(archive_path: Path) -> None:
    target = archive_path / "archive" / "deeply" / "nested" / "dir" / "out.md"
    safe_io.atomic_write(target, "hello")
    assert target.read_text() == "hello"


def test_atomic_write_replaces_existing(archive_path: Path) -> None:
    target = archive_path / "archive" / "publications" / "x.md"
    safe_io.atomic_write(target, "first")
    safe_io.atomic_write(target, "second")
    assert target.read_text() == "second"
