"""Tests for ``institute.diff_classify`` and the ``institute diff-classify`` CLI.

Covers the porcelain parser (synthetic byte strings, no git needed), the
classifier rules (operator vs fellow vs unknown), and a handful of
end-to-end runs against a real ``git init`` repo to confirm the path
through ``run_git_status`` works.
"""

from __future__ import annotations

import json
import os
import subprocess
from pathlib import Path

import pytest
from click.testing import CliRunner

from institute import diff_classify
from institute.cli import main as cli_main

# ---------------------------------------------------------------------------
# Pure unit tests against synthesized porcelain bytes (no subprocess).
# ---------------------------------------------------------------------------


def test_classify_path_fellow_prefixes() -> None:
    assert diff_classify.classify_path("archive/proposals/p1.md") == "fellow"
    assert diff_classify.classify_path("blog/src/content/posts/issue-1.md") == "fellow"
    assert diff_classify.classify_path("fellows/ada/notebook.md") == "fellow"
    assert diff_classify.classify_path("genomes/ada.json") == "fellow"


def test_classify_path_operator_prefixes() -> None:
    assert diff_classify.classify_path("docs/01-charter.md") == "operator"
    assert diff_classify.classify_path("institute/cli.py") == "operator"
    assert diff_classify.classify_path("tests/unit/test_x.py") == "operator"
    assert diff_classify.classify_path("scripts/run-daemon.sh") == "operator"
    assert diff_classify.classify_path("blog/src/components/Foo.astro") == "operator"


def test_classify_path_operator_toplevel_files() -> None:
    assert diff_classify.classify_path("README.md") == "operator"
    assert diff_classify.classify_path("pyproject.toml") == "operator"
    assert diff_classify.classify_path("Makefile") == "operator"


def test_classify_path_unknown_falls_through() -> None:
    assert diff_classify.classify_path("some-new-top-dir/file") == "unknown"
    assert diff_classify.classify_path("random.txt") == "unknown"


def test_parse_porcelain_z_empty() -> None:
    assert diff_classify.parse_porcelain_z(b"") == []


def test_parse_porcelain_z_single_entry() -> None:
    # ``" M docs/file.md\0"`` is what ``git status --porcelain=v1 -z``
    # emits for an unstaged modification of docs/file.md.
    data = b" M docs/file.md\x00"
    assert diff_classify.parse_porcelain_z(data) == ["docs/file.md"]


def test_parse_porcelain_z_filename_with_spaces() -> None:
    """The headline reason this module exists: the bash awk pipeline
    split on whitespace and lost everything after the first space."""
    data = b"?? archive/has a space.md\x00"
    assert diff_classify.parse_porcelain_z(data) == ["archive/has a space.md"]


def test_parse_porcelain_z_filename_with_newline() -> None:
    # Newlines in filenames are legal on POSIX; ``-z`` is the only
    # parser-safe option.
    data = b"?? archive/with\nnewline.md\x00"
    assert diff_classify.parse_porcelain_z(data) == ["archive/with\nnewline.md"]


def test_parse_porcelain_z_rename_entry() -> None:
    # Rename: ``R<space><dest>NUL<src>NUL``. Only the destination is
    # returned; the source token is consumed but ignored.
    data = b"R  archive/new.md\x00archive/old.md\x00"
    assert diff_classify.parse_porcelain_z(data) == ["archive/new.md"]


def test_parse_porcelain_z_mixed_entries() -> None:
    data = (
        b" M docs/charter.md\x00"
        b"?? archive/has a space.md\x00"
        b"R  archive/renamed.md\x00archive/orig.md\x00"
        b"A  genomes/ada.json\x00"
    )
    assert diff_classify.parse_porcelain_z(data) == [
        "docs/charter.md",
        "archive/has a space.md",
        "archive/renamed.md",
        "genomes/ada.json",
    ]


def test_classify_from_porcelain_empty() -> None:
    result = diff_classify.classify_from_porcelain(b"")
    assert result.operator_edits == []
    assert result.fellow_outputs == []
    assert result.unknown == []


def test_classify_from_porcelain_pure_fellow() -> None:
    data = b" M archive/drafts/p1.md\x00A  genomes/ada.json\x00"
    result = diff_classify.classify_from_porcelain(data)
    assert result.operator_edits == []
    assert sorted(result.fellow_outputs) == ["archive/drafts/p1.md", "genomes/ada.json"]
    assert result.unknown == []


def test_classify_from_porcelain_pure_operator() -> None:
    data = b" M docs/charter.md\x00M  institute/cli.py\x00"
    result = diff_classify.classify_from_porcelain(data)
    assert sorted(result.operator_edits) == ["docs/charter.md", "institute/cli.py"]
    assert result.fellow_outputs == []
    assert result.unknown == []


def test_classify_from_porcelain_mixed() -> None:
    data = b" M docs/charter.md\x00 M archive/drafts/p1.md\x00?? new-top-dir/x.txt\x00"
    result = diff_classify.classify_from_porcelain(data)
    assert result.operator_edits == ["docs/charter.md"]
    assert result.fellow_outputs == ["archive/drafts/p1.md"]
    assert result.unknown == ["new-top-dir/x.txt"]


def test_classify_from_porcelain_filename_with_spaces_in_fellow_path() -> None:
    data = b"?? archive/has a space.md\x00"
    result = diff_classify.classify_from_porcelain(data)
    assert result.fellow_outputs == ["archive/has a space.md"]
    assert result.operator_edits == []
    assert result.unknown == []


def test_classify_from_porcelain_rename_destination_classified() -> None:
    # Rename from one fellow path to another: the destination is what
    # matters for the auto-commit decision.
    data = b"R  archive/new.md\x00archive/old.md\x00"
    result = diff_classify.classify_from_porcelain(data)
    assert result.fellow_outputs == ["archive/new.md"]


# ---------------------------------------------------------------------------
# End-to-end against a real ``git init`` repo.
# ---------------------------------------------------------------------------


def _git(repo: Path, *args: str) -> None:
    env = os.environ.copy()
    # Make commits reproducible and free of operator identity / signing.
    env["GIT_AUTHOR_NAME"] = "test"
    env["GIT_AUTHOR_EMAIL"] = "test@example.invalid"
    env["GIT_COMMITTER_NAME"] = "test"
    env["GIT_COMMITTER_EMAIL"] = "test@example.invalid"
    subprocess.run(
        ["git", "-C", str(repo), *args],
        check=True,
        env=env,
        capture_output=True,
    )


@pytest.fixture()
def repo(tmp_path: Path) -> Path:
    """A throwaway git repo with no commits and no changes."""
    _git(tmp_path, "init", "-q", "-b", "main")
    # Disable gpg signing for the test repo so commit() does not block.
    _git(tmp_path, "config", "commit.gpgsign", "false")
    return tmp_path


def test_classify_repo_empty(repo: Path) -> None:
    result = diff_classify.classify_repo(repo)
    assert result.operator_edits == []
    assert result.fellow_outputs == []
    assert result.unknown == []


def test_classify_repo_pure_fellow(repo: Path) -> None:
    (repo / "archive").mkdir()
    (repo / "archive" / "p1.md").write_text("hi", encoding="utf-8")
    result = diff_classify.classify_repo(repo)
    assert result.fellow_outputs == ["archive/p1.md"]
    assert result.operator_edits == []


def test_classify_repo_pure_operator(repo: Path) -> None:
    (repo / "docs").mkdir()
    (repo / "docs" / "charter.md").write_text("hi", encoding="utf-8")
    result = diff_classify.classify_repo(repo)
    assert result.operator_edits == ["docs/charter.md"]
    assert result.fellow_outputs == []


def test_classify_repo_mixed(repo: Path) -> None:
    (repo / "docs").mkdir()
    (repo / "archive").mkdir()
    (repo / "docs" / "charter.md").write_text("hi", encoding="utf-8")
    (repo / "archive" / "p1.md").write_text("hi", encoding="utf-8")
    (repo / "rogue").mkdir()
    (repo / "rogue" / "x.txt").write_text("hi", encoding="utf-8")
    result = diff_classify.classify_repo(repo)
    assert result.operator_edits == ["docs/charter.md"]
    assert result.fellow_outputs == ["archive/p1.md"]
    assert result.unknown == ["rogue/x.txt"]


def test_classify_repo_filename_with_spaces(repo: Path) -> None:
    (repo / "archive").mkdir()
    (repo / "archive" / "has a space.md").write_text("hi", encoding="utf-8")
    result = diff_classify.classify_repo(repo)
    assert result.fellow_outputs == ["archive/has a space.md"]


def test_classify_repo_renamed_file(repo: Path) -> None:
    (repo / "archive").mkdir()
    (repo / "archive" / "old.md").write_text("hi", encoding="utf-8")
    _git(repo, "add", "archive/old.md")
    _git(repo, "commit", "-q", "-m", "initial")
    # ``git mv`` records the rename in the index, which is what
    # ``git status -z`` reports as ``R``.
    _git(repo, "mv", "archive/old.md", "archive/new.md")
    result = diff_classify.classify_repo(repo)
    # The destination is what the daemon needs to know about.
    assert result.fellow_outputs == ["archive/new.md"]


# ---------------------------------------------------------------------------
# CLI: ``institute diff-classify``.
# ---------------------------------------------------------------------------


def test_cli_diff_classify_empty_repo(repo: Path) -> None:
    runner = CliRunner()
    result = runner.invoke(cli_main, ["diff-classify", "--repo", str(repo)])
    assert result.exit_code == 0, result.output
    payload = json.loads(result.output)
    assert payload == {"operator_edits": [], "fellow_outputs": [], "unknown": []}


def test_cli_diff_classify_mixed_repo(repo: Path) -> None:
    (repo / "docs").mkdir()
    (repo / "archive").mkdir()
    (repo / "docs" / "charter.md").write_text("hi", encoding="utf-8")
    (repo / "archive" / "p1.md").write_text("hi", encoding="utf-8")
    runner = CliRunner()
    result = runner.invoke(cli_main, ["diff-classify", "--repo", str(repo)])
    assert result.exit_code == 0, result.output
    payload = json.loads(result.output)
    assert payload["operator_edits"] == ["docs/charter.md"]
    assert payload["fellow_outputs"] == ["archive/p1.md"]
    assert payload["unknown"] == []


def test_cli_diff_classify_from_file(tmp_path: Path) -> None:
    """``--from-file`` lets the daemon classify a saved baseline blob
    without needing the repo to still be on that revision."""
    blob = tmp_path / "baseline.bin"
    blob.write_bytes(b" M docs/charter.md\x00 M archive/drafts/p1.md\x00?? new-top-dir/x.txt\x00")
    runner = CliRunner()
    result = runner.invoke(cli_main, ["diff-classify", "--from-file", str(blob)])
    assert result.exit_code == 0, result.output
    payload = json.loads(result.output)
    assert payload == {
        "operator_edits": ["docs/charter.md"],
        "fellow_outputs": ["archive/drafts/p1.md"],
        "unknown": ["new-top-dir/x.txt"],
    }
