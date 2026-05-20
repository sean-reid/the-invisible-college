"""Tests for the code/data artifact sweep."""

from __future__ import annotations

from pathlib import Path

import pytest

from institute import code_artifacts, paths


def test_sweep_copies_allowed_extensions(isolated: Path) -> None:
    ws = isolated / "ws"
    ws.mkdir()
    (ws / "experiment.py").write_text("print('hi')")
    (ws / "data.csv").write_text("a,b\n1,2\n")
    (ws / "config.json").write_text("{}")

    written = code_artifacts.sweep_workspace(workspace=ws, project_id="p1")
    names = {p.name for p in written}
    assert names == {"experiment.py", "data.csv", "config.json"}


def test_sweep_skips_workflow_outputs(isolated: Path) -> None:
    """draft.md, notebook.md, abstract.txt etc. are workflow artifacts,
    not experimental output."""
    ws = isolated / "ws"
    ws.mkdir()
    (ws / "abstract.txt").write_text("an abstract")
    (ws / "draft.md").write_text("# Title")
    (ws / "experiment.py").write_text("print('hi')")

    written = code_artifacts.sweep_workspace(workspace=ws, project_id="p1")
    assert [p.name for p in written] == ["experiment.py"]


def test_sweep_skips_unknown_extensions(isolated: Path) -> None:
    ws = isolated / "ws"
    ws.mkdir()
    (ws / "image.png").write_bytes(b"\x89PNG")
    (ws / "scratch.bin").write_bytes(b"\x00\x01")
    (ws / "real.py").write_text("ok")

    written = code_artifacts.sweep_workspace(workspace=ws, project_id="p1")
    assert [p.name for p in written] == ["real.py"]


def test_sweep_skips_scratch_dirs(isolated: Path) -> None:
    ws = isolated / "ws"
    (ws / "__pycache__").mkdir(parents=True)
    (ws / "__pycache__" / "stale.py").write_text("x")
    (ws / ".venv" / "lib").mkdir(parents=True)
    (ws / ".venv" / "lib" / "thing.py").write_text("x")
    (ws / "real.py").write_text("ok")

    written = code_artifacts.sweep_workspace(workspace=ws, project_id="p1")
    assert [p.name for p in written] == ["real.py"]


def test_sweep_per_file_size_cap(isolated: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    ws = isolated / "ws"
    ws.mkdir()
    monkeypatch.setattr(code_artifacts, "MAX_FILE_BYTES", 100)
    (ws / "small.py").write_text("x" * 50)
    (ws / "big.py").write_text("y" * 500)

    written = code_artifacts.sweep_workspace(workspace=ws, project_id="p1")
    assert [p.name for p in written] == ["small.py"]


def test_sweep_per_project_size_cap(isolated: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    ws = isolated / "ws"
    ws.mkdir()
    monkeypatch.setattr(code_artifacts, "MAX_FILE_BYTES", 1000)
    monkeypatch.setattr(code_artifacts, "MAX_PROJECT_BYTES", 1200)
    (ws / "a.py").write_text("a" * 800)
    (ws / "b.py").write_text("b" * 800)  # would push total past 1200
    (ws / "c.py").write_text("c" * 200)

    written = code_artifacts.sweep_workspace(workspace=ws, project_id="p1")
    # a.py fits (800 <= 1200), b.py would push to 1600 (skip), c.py fits at 1000.
    names = {p.name for p in written}
    assert "a.py" in names
    assert "b.py" not in names
    assert "c.py" in names


def test_sweep_flattens_nested_paths(isolated: Path) -> None:
    ws = isolated / "ws"
    (ws / "sub" / "deeper").mkdir(parents=True)
    (ws / "sub" / "deeper" / "thing.py").write_text("ok")

    written = code_artifacts.sweep_workspace(workspace=ws, project_id="p1")
    assert [p.name for p in written] == ["sub--deeper--thing.py"]


def test_sweep_idempotent_overwrites(isolated: Path) -> None:
    ws = isolated / "ws"
    ws.mkdir()
    (ws / "experiment.py").write_text("v1")
    code_artifacts.sweep_workspace(workspace=ws, project_id="p1")
    (ws / "experiment.py").write_text("v2")
    code_artifacts.sweep_workspace(workspace=ws, project_id="p1")
    dest = paths.CODE / "p1" / "experiment.py"
    assert dest.read_text() == "v2"


def test_sweep_returns_empty_for_missing_workspace(isolated: Path) -> None:
    assert code_artifacts.sweep_workspace(workspace=isolated / "nonexistent", project_id="p1") == []


def test_list_for_project(isolated: Path) -> None:
    ws = isolated / "ws"
    ws.mkdir()
    (ws / "a.py").write_text("a")
    (ws / "b.csv").write_text("b")
    code_artifacts.sweep_workspace(workspace=ws, project_id="p1")
    names = [p.name for p in code_artifacts.list_for_project("p1")]
    assert names == ["a.py", "b.csv"]


def test_list_returns_empty_for_unknown_project(isolated: Path) -> None:
    assert code_artifacts.list_for_project("nope") == []


def test_mirror_to_blog_copies_then_replaces(isolated: Path) -> None:
    ws = isolated / "ws"
    ws.mkdir()
    (ws / "a.py").write_text("first")
    code_artifacts.sweep_workspace(workspace=ws, project_id="p1")
    code_artifacts.mirror_to_blog("p1")
    dest = paths.BLOG_CODE / "p1" / "a.py"
    assert dest.read_text() == "first"

    # Update and re-mirror: blog mirror should reflect the new content.
    (ws / "a.py").write_text("second")
    code_artifacts.sweep_workspace(workspace=ws, project_id="p1")
    code_artifacts.mirror_to_blog("p1")
    assert dest.read_text() == "second"


def test_mirror_to_blog_handles_no_archive(isolated: Path) -> None:
    assert code_artifacts.mirror_to_blog("nonexistent") == []
