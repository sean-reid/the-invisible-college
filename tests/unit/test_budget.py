"""Tests for daily-spend accounting and austerity-level classification.

Pure helpers only; no autopilot dispatch. Each test writes its own
synthetic audit log to a tmp path so production state stays untouched.
"""

from __future__ import annotations

import json
from datetime import UTC, datetime, timedelta
from pathlib import Path

from freezegun import freeze_time

from institute import budget

FROZEN = "2026-05-20T12:00:00Z"


def _write_audit(path: Path, entries: list[dict]) -> None:
    path.write_text("\n".join(json.dumps(e) for e in entries) + "\n", encoding="utf-8")


def _ts(when: datetime) -> str:
    return when.isoformat(timespec="seconds")


@freeze_time(FROZEN)
def test_today_usd_sums_only_today(tmp_path: Path) -> None:
    log = tmp_path / "audit.log"
    now = datetime.now(UTC)
    yesterday = now - timedelta(days=1)
    _write_audit(
        log,
        [
            {"ts": _ts(yesterday), "cost_usd": 5.00, "fellow_id": "ada"},
            {"ts": _ts(now), "cost_usd": 1.25, "fellow_id": "ada"},
            {"ts": _ts(now), "cost_usd": 0.75, "fellow_id": "henri"},
        ],
    )
    assert budget.today_usd(audit_log=log) == 2.0


def test_today_usd_empty_log_is_zero(tmp_path: Path) -> None:
    assert budget.today_usd(audit_log=tmp_path / "missing.log") == 0.0


@freeze_time(FROZEN)
def test_daily_total_skips_malformed_lines(tmp_path: Path) -> None:
    log = tmp_path / "audit.log"
    today = datetime.now(UTC).date().isoformat()
    log.write_text(
        "\n".join(
            [
                json.dumps({"ts": f"{today}T01:00:00+00:00", "cost_usd": 1.0}),
                "not json at all",
                json.dumps({"ts": f"{today}T02:00:00+00:00"}),  # missing cost
                json.dumps({"cost_usd": 9.99}),  # missing ts
                json.dumps({"ts": f"{today}T03:00:00+00:00", "cost_usd": 2.5}),
            ]
        )
        + "\n",
        encoding="utf-8",
    )
    assert budget.daily_total_usd(today, audit_log=log) == 3.5


@freeze_time(FROZEN)
def test_austerity_disabled_when_cap_zero(tmp_path: Path) -> None:
    log = tmp_path / "audit.log"
    now = datetime.now(UTC)
    _write_audit(log, [{"ts": _ts(now), "cost_usd": 100.0}])
    snapshot = budget.current_status(0.0, audit_log=log)
    assert snapshot.level == "none"
    assert snapshot.disabled


@freeze_time(FROZEN)
def test_austerity_levels_at_thresholds(tmp_path: Path) -> None:
    log = tmp_path / "audit.log"
    now = datetime.now(UTC)
    cap = 10.0
    # Spend = 5: below soft threshold (8.0)
    _write_audit(log, [{"ts": _ts(now), "cost_usd": 5.0}])
    assert budget.current_status(cap, audit_log=log).level == "none"
    # Spend = 8: exactly at soft (80% of 10)
    _write_audit(log, [{"ts": _ts(now), "cost_usd": 8.0}])
    assert budget.current_status(cap, audit_log=log).level == "soft"
    # Spend = 9.5: between soft and hard
    _write_audit(log, [{"ts": _ts(now), "cost_usd": 9.5}])
    assert budget.current_status(cap, audit_log=log).level == "soft"
    # Spend = 10: hard cap
    _write_audit(log, [{"ts": _ts(now), "cost_usd": 10.0}])
    assert budget.current_status(cap, audit_log=log).level == "hard"
    # Spend = 12: over hard cap
    _write_audit(log, [{"ts": _ts(now), "cost_usd": 12.0}])
    assert budget.current_status(cap, audit_log=log).level == "hard"


@freeze_time(FROZEN)
def test_austerity_levels_respect_custom_soft_threshold(tmp_path: Path) -> None:
    log = tmp_path / "audit.log"
    now = datetime.now(UTC)
    _write_audit(log, [{"ts": _ts(now), "cost_usd": 6.0}])
    # 50% threshold: $6 of $10 crosses soft (which is $5)
    snap = budget.current_status(10.0, soft_threshold=0.5, audit_log=log)
    assert snap.level == "soft"
    assert snap.soft_cap_usd == 5.0


@freeze_time(FROZEN)
def test_status_for_date_isolates_one_day(tmp_path: Path) -> None:
    log = tmp_path / "audit.log"
    today = datetime.now(UTC).date()
    yesterday = today - timedelta(days=1)
    _write_audit(
        log,
        [
            {"ts": f"{yesterday.isoformat()}T08:00:00+00:00", "cost_usd": 7.0},
            {"ts": f"{today.isoformat()}T08:00:00+00:00", "cost_usd": 2.0},
        ],
    )
    yest_snap = budget.status_for_date(yesterday.isoformat(), 10.0, audit_log=log)
    today_snap = budget.status_for_date(today.isoformat(), 10.0, audit_log=log)
    assert yest_snap.today_usd == 7.0
    assert yest_snap.level == "none"  # 7 < 8 soft threshold
    assert today_snap.today_usd == 2.0
    assert today_snap.level == "none"


@freeze_time(FROZEN)
def test_last_n_days_includes_zero_days(tmp_path: Path) -> None:
    log = tmp_path / "audit.log"
    today = datetime.now(UTC).date()
    two_days_ago = today - timedelta(days=2)
    _write_audit(
        log,
        [
            {"ts": f"{two_days_ago.isoformat()}T08:00:00+00:00", "cost_usd": 3.0},
            {"ts": f"{today.isoformat()}T08:00:00+00:00", "cost_usd": 1.5},
        ],
    )
    series = budget.last_n_days(3, audit_log=log)
    assert len(series) == 3
    assert series[0][0] == two_days_ago.isoformat()
    assert series[0][1] == 3.0
    # Middle day had no spend
    assert series[1][1] == 0.0
    assert series[-1][1] == 1.5


def test_last_n_days_handles_n_le_zero() -> None:
    assert budget.last_n_days(0) == []
    assert budget.last_n_days(-1) == []


@freeze_time(FROZEN)
def test_headline_disabled_message(tmp_path: Path) -> None:
    log = tmp_path / "audit.log"
    now = datetime.now(UTC)
    _write_audit(log, [{"ts": _ts(now), "cost_usd": 4.20}])
    snap = budget.current_status(0.0, audit_log=log)
    assert "no daily cap" in snap.headline()


@freeze_time(FROZEN)
def test_headline_enabled_message(tmp_path: Path) -> None:
    log = tmp_path / "audit.log"
    now = datetime.now(UTC)
    _write_audit(log, [{"ts": _ts(now), "cost_usd": 4.20}])
    snap = budget.current_status(10.0, audit_log=log)
    h = snap.headline()
    assert "$4.20" in h
    assert "$10.00" in h
    assert snap.level in h
