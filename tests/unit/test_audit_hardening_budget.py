"""Audit-pass-1 hardening: budget clamping, audit cost tracker, and CLI callbacks."""

from __future__ import annotations

import json
from datetime import UTC, datetime
from pathlib import Path

import pytest
from freezegun import freeze_time

from institute import budget

# --- budget hardening ----------------------------------------------------


@freeze_time("2026-05-20T12:00:00Z")
def test_daily_total_clamps_negative_cost(tmp_path: Path) -> None:
    log = tmp_path / "audit.log"
    today = datetime.now(UTC).date().isoformat()
    log.write_text(
        "\n".join(
            [
                json.dumps({"ts": f"{today}T01:00:00+00:00", "cost_usd": 1.0}),
                json.dumps({"ts": f"{today}T02:00:00+00:00", "cost_usd": -1000.0}),
                json.dumps({"ts": f"{today}T03:00:00+00:00", "cost_usd": 2.5}),
            ]
        )
        + "\n",
        encoding="utf-8",
    )
    assert budget.daily_total_usd(today, audit_log=log) == 3.5


@freeze_time("2026-05-20T12:00:00Z")
def test_current_status_clamps_pathological_threshold(tmp_path: Path) -> None:
    log = tmp_path / "audit.log"
    now = datetime.now(UTC)
    log.write_text(
        json.dumps({"ts": now.isoformat(timespec="seconds"), "cost_usd": 5.0}) + "\n",
        encoding="utf-8",
    )
    # threshold > 1.0 would put hard before soft; clamp brings it into
    # range so soft can still fire below hard.
    snap = budget.current_status(10.0, soft_threshold=5.0, audit_log=log)
    assert snap.soft_cap_usd <= snap.hard_cap_usd
    # threshold = 0 would mark every nonzero spend as soft; clamp to 0.01.
    snap = budget.current_status(10.0, soft_threshold=0.0, audit_log=log)
    assert snap.soft_cap_usd > 0


# --- audit cost tracker --------------------------------------------------


def test_audit_cost_tracker_only_counts_new_lines(tmp_path, monkeypatch) -> None:
    from institute import cli as cli_mod
    from institute import paths as paths_mod

    log = tmp_path / "audit.log"
    log.write_text(
        json.dumps({"ts": "2026-05-19T00:00:00+00:00", "cost_usd": 1.0}) + "\n",
        encoding="utf-8",
    )
    monkeypatch.setattr(paths_mod, "AUDIT_LOG", log)
    tracker = cli_mod._AuditCostTracker.from_now()
    assert tracker.delta() == 0.0  # nothing new yet
    with log.open("a", encoding="utf-8") as fh:
        fh.write(json.dumps({"ts": "2026-05-19T01:00:00+00:00", "cost_usd": 2.0}) + "\n")
        fh.write(json.dumps({"ts": "2026-05-19T02:00:00+00:00", "cost_usd": 0.5}) + "\n")
    assert tracker.delta() == 2.5


# --- _non_negative_usd CLI callback --------------------------------------


def test_non_negative_usd_rejects_negative() -> None:
    import click

    from institute.cli import _non_negative_usd

    class _Param:
        name = "--daily-budget-usd"

    with pytest.raises(click.BadParameter):
        _non_negative_usd(None, _Param(), -1.0)
    assert _non_negative_usd(None, _Param(), 0.0) == 0.0
    assert _non_negative_usd(None, _Param(), 5.0) == 5.0
    # `None` from a missing default is treated as 0
    assert _non_negative_usd(None, _Param(), None) == 0.0
