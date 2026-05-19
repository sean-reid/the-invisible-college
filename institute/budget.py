"""Daily cost cap and austerity mode.

Chapter 1 lists daily resource consumption exceeding the Charter-defined
cap as an automatic kill-switch tripwire. Chapter 9 describes austerity
mode: when monthly spend approaches the budget cap, the institute
defers new proposals, pauses routine work, and lets in-flight peer
review continue (because it is upstream of publication and cannot pause
without breaking the pipeline).

This module is the read-side accounting layer over the audit log. Every
Claude invocation already records `cost_usd` and `ts` in a JSONL audit
log on disk; this module groups those by UTC date and decides which
austerity level the institute is in right now.

Cap = 0 means "no daily cap." The autopilot then behaves as it always
did, gated only by the per-wake-up `--max-budget-usd`.

Soft threshold defaults to 80%. Below it: normal operation. At or above
soft but below hard: soft austerity (skip curriculum, propose, admit;
let in-flight projects advance). At or above hard: full halt until UTC
midnight, when the daily total resets naturally because the query
filter advances with the calendar.
"""

from __future__ import annotations

import json
from dataclasses import dataclass
from datetime import UTC, datetime, timedelta
from pathlib import Path
from typing import Literal

from institute import paths

AusterityLevel = Literal["none", "soft", "hard"]

DEFAULT_SOFT_THRESHOLD: float = 0.8


@dataclass(frozen=True)
class Austerity:
    """Snapshot of the institution's daily-spend posture."""

    level: AusterityLevel
    today_usd: float
    hard_cap_usd: float
    soft_cap_usd: float
    utc_date: str

    @property
    def disabled(self) -> bool:
        """True when no daily cap is configured."""
        return self.hard_cap_usd <= 0

    def headline(self) -> str:
        """One-line summary suitable for the autopilot log."""
        if self.disabled:
            return f"spend today ${self.today_usd:.2f} (no daily cap)"
        return (
            f"spend today ${self.today_usd:.2f} of ${self.hard_cap_usd:.2f} "
            f"(soft ${self.soft_cap_usd:.2f}); level={self.level}"
        )


def _today_str() -> str:
    return datetime.now(UTC).date().isoformat()


def _iter_audit_entries(audit_log: Path | None = None) -> list[dict]:
    """Yield parsed audit entries, skipping unparseable lines.

    The audit log is JSONL; one Claude invocation per line. Each entry
    has at minimum `ts` (ISO timestamp) and `cost_usd` (float).
    Malformed lines are silently dropped so a single bad line never
    blocks the daily total. Returns a list, not a generator, so callers
    can iterate twice for free.
    """
    path = audit_log or paths.AUDIT_LOG
    if not path.is_file():
        return []
    out: list[dict] = []
    for line in path.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if not line:
            continue
        try:
            out.append(json.loads(line))
        except json.JSONDecodeError:
            continue
    return out


def daily_total_usd(utc_date: str, *, audit_log: Path | None = None) -> float:
    """Sum cost_usd across all audit entries dated `utc_date` (YYYY-MM-DD).

    Entries without a parseable ts or cost are skipped, not counted.
    """
    total = 0.0
    for entry in _iter_audit_entries(audit_log):
        ts = entry.get("ts")
        cost = entry.get("cost_usd")
        if not isinstance(ts, str) or not isinstance(cost, int | float):
            continue
        if ts.startswith(utc_date):
            total += float(cost)
    return total


def today_usd(audit_log: Path | None = None) -> float:
    """Sum cost_usd across audit entries dated today (UTC)."""
    return daily_total_usd(_today_str(), audit_log=audit_log)


def last_n_days(n: int, *, audit_log: Path | None = None) -> list[tuple[str, float]]:
    """Return (date, usd) pairs for the last n UTC days, oldest first.

    Includes days with zero spend so a sparse log still renders as a
    contiguous timeline. Today is the last entry.
    """
    if n <= 0:
        return []
    today = datetime.now(UTC).date()
    entries = _iter_audit_entries(audit_log)
    totals: dict[str, float] = {}
    for entry in entries:
        ts = entry.get("ts")
        cost = entry.get("cost_usd")
        if not isinstance(ts, str) or not isinstance(cost, int | float):
            continue
        totals[ts[:10]] = totals.get(ts[:10], 0.0) + float(cost)
    out: list[tuple[str, float]] = []
    for offset in range(n - 1, -1, -1):
        d = (today - timedelta(days=offset)).isoformat()
        out.append((d, totals.get(d, 0.0)))
    return out


def _classify(today_spent: float, hard_cap: float, soft_threshold: float) -> AusterityLevel:
    if hard_cap <= 0:
        return "none"
    if today_spent >= hard_cap:
        return "hard"
    if today_spent >= hard_cap * soft_threshold:
        return "soft"
    return "none"


def current_status(
    hard_cap_usd: float,
    *,
    soft_threshold: float = DEFAULT_SOFT_THRESHOLD,
    audit_log: Path | None = None,
) -> Austerity:
    """Compute today's austerity snapshot from the live audit log.

    A `hard_cap_usd` of 0 disables the cap entirely; level stays "none"
    regardless of spend.
    """
    today_spent = today_usd(audit_log=audit_log)
    today_str = _today_str()
    return Austerity(
        level=_classify(today_spent, hard_cap_usd, soft_threshold),
        today_usd=today_spent,
        hard_cap_usd=max(hard_cap_usd, 0.0),
        soft_cap_usd=max(hard_cap_usd, 0.0) * soft_threshold,
        utc_date=today_str,
    )


def status_for_date(
    utc_date_str: str,
    hard_cap_usd: float,
    *,
    soft_threshold: float = DEFAULT_SOFT_THRESHOLD,
    audit_log: Path | None = None,
) -> Austerity:
    """Compute austerity snapshot for any UTC date. Used by tests + reports."""
    spent = daily_total_usd(utc_date_str, audit_log=audit_log)
    return Austerity(
        level=_classify(spent, hard_cap_usd, soft_threshold),
        today_usd=spent,
        hard_cap_usd=max(hard_cap_usd, 0.0),
        soft_cap_usd=max(hard_cap_usd, 0.0) * soft_threshold,
        utc_date=utc_date_str,
    )


__all__ = [
    "DEFAULT_SOFT_THRESHOLD",
    "Austerity",
    "AusterityLevel",
    "current_status",
    "daily_total_usd",
    "last_n_days",
    "status_for_date",
    "today_usd",
]
