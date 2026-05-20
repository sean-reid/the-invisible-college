"""Runtime guards shared across the CLI and the workflow layer.

Two guards run before every Claude invocation:

  1. **Tripwires** (Chapter 1) — Charter file integrity and audit-log
     chain integrity. Any failure fires the kill switch automatically
     with the tripwire as the reason, then exits.

  2. **Kill switch** — if engaged (by the Founder or by a tripwire),
     every queued Fellow call halts cleanly.

Both checks are cheap (one DB read + one file hash). Called from
`claude_runner.invoke` before each subprocess so a mid-workflow trip
stops the next Fellow rather than letting queued work drain.
"""

from __future__ import annotations

import sys

from rich.console import Console

from institute import db

_console = Console()


class KillSwitchEngaged(SystemExit):
    """Raised when the kill switch is on. Inherits SystemExit so the
    process exits cleanly without a traceback splatter; existing
    `except SystemExit` handlers still catch it."""


def check_kill_switch() -> None:
    """Run integrity tripwires, then halt if the kill switch is on.

    Tripwire findings auto-fire the switch with the finding as the
    reason. After firing, this raises so the caller stops.
    """
    _check_tripwires()
    _check_kill_switch_active()


def _check_tripwires() -> None:
    # Local import to avoid an import cycle between runtime and
    # tripwires (which imports db, audit, paths).
    from institute import tripwires

    with db.connection() as conn, db.transaction(conn):
        findings = tripwires.check_all(conn)
        for finding in findings:
            tripwires.fire(conn, reason=str(finding), triggered_by="tripwire")
        if findings:
            _console.print(
                f"[red]Tripwire fired:[/red] {'; '.join(str(f) for f in findings)}"
            )


def _check_kill_switch_active() -> None:
    with db.connection() as conn:
        row = conn.execute("SELECT active, reason FROM kill_switch WHERE id = 1").fetchone()
        if row is None or not row["active"]:
            return
        _console.print("[red]Kill switch is engaged.[/red] All operations are halted.")
        if row["reason"]:
            _console.print(f"Reason: {row['reason']}")
        _console.print("Run `institute kill-switch off` to resume.")
        # SystemExit propagates up cleanly: the lockfile releases via
        # the context manager that holds it, the in-flight transaction
        # rolls back via the BEGIN IMMEDIATE wrapper, and the user sees
        # the message above instead of a traceback.
        sys.exit(2)
