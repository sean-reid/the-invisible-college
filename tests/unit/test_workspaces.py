"""Tests for the per-invocation workspace helpers."""

from pathlib import Path

import pytest

from institute import workspaces


@pytest.fixture()
def fellows_root(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> Path:
    monkeypatch.setattr(workspaces, "FELLOWS", tmp_path / "fellows")
    return tmp_path / "fellows"


def test_workspace_for_creates_nested_dirs(fellows_root: Path) -> None:
    ws = workspaces.workspace_for("hypatia", "proj-1")
    assert ws.is_dir()
    assert ws == fellows_root / "hypatia" / "workspace" / "proj-1"


def test_stage_input_writes_atomically(fellows_root: Path) -> None:
    ws = workspaces.workspace_for("h", "x")
    path = workspaces.stage_input(ws, "proposal.md", "# Hello\n\nbody")
    assert path.read_text() == "# Hello\n\nbody"
    # Atomic: no leftover .tmp file.
    assert not (ws / "proposal.md.tmp").exists()


def test_require_output_reads_existing(fellows_root: Path) -> None:
    ws = workspaces.workspace_for("h", "x")
    (ws / "draft.md").write_text("the draft content " * 30)
    text = workspaces.require_output(ws, "draft.md", min_chars=100)
    assert "the draft content" in text


def test_require_output_raises_when_missing(fellows_root: Path) -> None:
    ws = workspaces.workspace_for("h", "x")
    with pytest.raises(RuntimeError, match="did not produce"):
        workspaces.require_output(ws, "missing.md")


def test_require_output_raises_when_too_short(fellows_root: Path) -> None:
    ws = workspaces.workspace_for("h", "x")
    (ws / "draft.md").write_text("short")
    with pytest.raises(RuntimeError, match="shorter than"):
        workspaces.require_output(ws, "draft.md", min_chars=100)


def test_optional_output_returns_none_when_missing(fellows_root: Path) -> None:
    ws = workspaces.workspace_for("h", "x")
    assert workspaces.optional_output(ws, "abstract.txt") is None


def test_optional_output_returns_text_when_present(fellows_root: Path) -> None:
    ws = workspaces.workspace_for("h", "x")
    (ws / "abstract.txt").write_text("A short summary.\n")
    assert workspaces.optional_output(ws, "abstract.txt") == "A short summary."


def test_stage_input_creates_nested_parent_dir(fellows_root: Path) -> None:
    """`stage_input` must mkdir the parent for nested filenames like
    `contributions/<id>.md`. Otherwise the atomic temp-write fails
    with FileNotFoundError."""
    ws = workspaces.workspace_for("h", "x")
    path = workspaces.stage_input(ws, "contributions/pierre-bayle.md", "hello")
    assert path.is_file()
    assert path.read_text() == "hello"
    assert path.parent.name == "contributions"
