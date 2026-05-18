"""Tests for the launchd schedule helpers (plist rendering, status reporting)."""

from __future__ import annotations

import plistlib
from pathlib import Path

import pytest

from institute import paths, schedule


@pytest.fixture()
def isolated(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> Path:
    log_dir = tmp_path / "logs"
    plist_dir = tmp_path / "LaunchAgents"
    log_dir.mkdir()
    plist_dir.mkdir()
    monkeypatch.setattr(schedule, "LOG_DIR", log_dir)
    monkeypatch.setattr(schedule, "PLIST_DIR", plist_dir)
    monkeypatch.setattr(paths, "ROOT", tmp_path)
    return tmp_path


def test_render_plist_default_shape(isolated: Path) -> None:
    body = schedule.render_plist(
        interval_hours=6,
        max_budget_usd=4.0,
        max_steps=20,
        auto_push=True,
    )
    data = plistlib.loads(body)
    assert data["Label"] == schedule.LABEL
    assert data["StartInterval"] == 6 * 3600
    assert data["RunAtLoad"] is False
    assert data["ProgramArguments"][0] == "/bin/bash"
    assert data["EnvironmentVariables"]["IC_MAX_BUDGET"] == "4.0"
    assert data["EnvironmentVariables"]["IC_MAX_STEPS"] == "20"
    assert data["EnvironmentVariables"]["IC_AUTO_PUSH"] == "1"
    assert data["EnvironmentVariables"]["IC_REPO"] == str(isolated)


def test_render_plist_auto_push_off(isolated: Path) -> None:
    body = schedule.render_plist(
        interval_hours=12, max_budget_usd=3.0, max_steps=15, auto_push=False
    )
    data = plistlib.loads(body)
    assert data["EnvironmentVariables"]["IC_AUTO_PUSH"] == "0"


def test_render_plist_includes_path_env(isolated: Path) -> None:
    body = schedule.render_plist(interval_hours=1, max_budget_usd=1.0, max_steps=1, auto_push=False)
    data = plistlib.loads(body)
    path = data["EnvironmentVariables"]["PATH"]
    # The PATH must include homebrew and standard locations so `uv` and
    # `claude` resolve when launchd starts the daemon.
    assert "/opt/homebrew/bin" in path or "/usr/local/bin" in path


def test_render_plist_log_paths(isolated: Path) -> None:
    body = schedule.render_plist(interval_hours=1, max_budget_usd=1.0, max_steps=1, auto_push=False)
    data = plistlib.loads(body)
    assert data["StandardOutPath"].endswith("stdout.log")
    assert data["StandardErrorPath"].endswith("stderr.log")


def test_status_reports_not_installed(isolated: Path) -> None:
    info = schedule.status()
    assert info["installed"] is False
    assert info["interval_hours"] is None
    assert info["log_tail"] == ""


def test_status_reads_interval_from_disk(isolated: Path) -> None:
    body = schedule.render_plist(
        interval_hours=8, max_budget_usd=2.0, max_steps=10, auto_push=False
    )
    schedule.plist_path().write_bytes(body)
    info = schedule.status()
    assert info["installed"] is True
    assert info["interval_hours"] == 8.0


def test_status_includes_log_tail(isolated: Path) -> None:
    log = schedule.LOG_DIR / "autopilot.log"
    log.write_text("line1\nline2\nline3\n", encoding="utf-8")
    info = schedule.status()
    assert "line3" in info["log_tail"]
    assert info["last_log_mtime"] is not None


def test_uninstall_returns_false_when_absent(isolated: Path) -> None:
    assert schedule.uninstall() is False


def test_uninstall_removes_plist(isolated: Path, monkeypatch: pytest.MonkeyPatch) -> None:
    schedule.plist_path().write_bytes(b"<plist/>")
    # Stub out launchctl so the test does not actually shell out.
    monkeypatch.setattr(schedule.shutil, "which", lambda _: None)
    assert schedule.uninstall() is True
    assert not schedule.plist_path().exists()
