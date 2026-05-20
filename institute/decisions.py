"""Writes institutional decisions to archive/decisions/ as markdown files.

These files are committed to the repo and form the College's institutional
memory. One file per significant decision: admission of a Fellow, promotion,
proposal disposition, peer review outcome, kill switch event, charter
amendment.

The SQLite audit_log table is a fast index of the same events for queries;
the markdown files are the canonical record.
"""

from __future__ import annotations

import sqlite3
from dataclasses import dataclass
from datetime import UTC, datetime
from pathlib import Path

from institute.paths import DECISIONS


@dataclass(frozen=True)
class Decision:
    kind: str  # bootstrap, admission, promotion, proposal, review, publication, kill_switch
    title: str
    body: str
    actors: list[str]  # fellow ids or "founder" or "orchestrator"
    related_project: str | None = None


def record(
    conn: sqlite3.Connection,
    decision: Decision,
) -> Path:
    """Write a decision markdown file and an audit_log row.

    Caller is responsible for the surrounding transaction.
    """
    now = datetime.now(UTC)
    DECISIONS.mkdir(parents=True, exist_ok=True)

    # File naming: <date>-<kind>-<slug>.md, no spaces.
    date_prefix = now.date().isoformat()
    slug = _slugify(decision.title)
    counter = 0
    while True:
        suffix = f"-{counter}" if counter else ""
        path = DECISIONS / f"{date_prefix}-{decision.kind}-{slug}{suffix}.md"
        if not path.exists():
            break
        counter += 1

    front = [
        "---",
        f"kind: {decision.kind}",
        f"recorded_at: {now.isoformat(timespec='seconds')}",
        f"actors: [{', '.join(decision.actors)}]",
    ]
    if decision.related_project:
        front.append(f"project: {decision.related_project}")
    front.append("---")
    front.append("")
    front.append(f"# {decision.title}")
    front.append("")

    body_text = "\n".join(front) + decision.body.strip() + "\n"
    _atomic_write(path, body_text)

    try:
        from institute import audit

        audit.append(
            conn,
            at=now.isoformat(timespec="seconds"),
            actor=",".join(decision.actors),
            action=decision.kind,
            project_id=decision.related_project,
            detail=str(path.relative_to(DECISIONS.parent.parent)),
        )
    except Exception:
        # Drop the just-written markdown so we never leave an orphan
        # in archive/decisions/ that has no matching audit_log row.
        # `missing_ok` covers the edge case where the file was already
        # unlinked between write and exception (extremely unlikely
        # but cheap to handle).
        try:
            path.unlink(missing_ok=True)
        except OSError:
            pass
        raise
    return path


def _slugify(text: str) -> str:
    out = []
    last_dash = False
    for ch in text.lower():
        if ch.isalnum():
            out.append(ch)
            last_dash = False
        elif not last_dash:
            out.append("-")
            last_dash = True
    s = "".join(out).strip("-")
    return s[:60] if s else "untitled"


def _atomic_write(path: Path, content: str) -> None:
    from institute.safe_io import atomic_write

    atomic_write(path, content)
