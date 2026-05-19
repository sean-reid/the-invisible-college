"""Runtime guards shared across the CLI and the workflow layer.

Currently the only guard is the kill switch (Chapter 1 + Chapter 2):
when the Founder engages it, every in-flight Claude invocation must
stop before doing any more work. The CLI's command-level
`_check_kill_switch` handles command entry; this module is what
`claude_runner.invoke` calls before every subprocess, so a mid-workflow
engagement halts the next Fellow call rather than letting all queued
Claude work drain.
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
    """Raise KillSwitchEngaged if the institutional kill switch is on.

    Safe to call at command entry, before every Claude invocation, and
    between workflow steps. Uses its own short-lived DB connection so
    callers don't need to thread one in. Idempotent and cheap.
    """
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
