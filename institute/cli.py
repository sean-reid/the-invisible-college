"""Command-line interface for the College.

This module is the single entry point for the Founder. Every command is
designed to be safely interruptible: state is persisted before the command
returns, and re-running picks up where things left off.
"""

from __future__ import annotations

import sys
from datetime import UTC, datetime

import click
from rich.console import Console
from rich.table import Table

from institute import __version__, db, paths
from institute import fellow as fellow_mod

console = Console()


def _now() -> str:
    return datetime.now(UTC).isoformat(timespec="seconds")


def _check_kill_switch() -> None:
    with db.connection() as conn:
        row = conn.execute("SELECT active, reason FROM kill_switch WHERE id = 1").fetchone()
        if row is not None and row["active"]:
            console.print("[red]Kill switch is engaged.[/red] All operations are halted.")
            if row["reason"]:
                console.print(f"Reason: {row['reason']}")
            console.print("Run `institute kill-switch off` to resume.")
            sys.exit(2)


@click.group()
@click.version_option(__version__, prog_name="institute")
def main() -> None:
    """The Invisible College orchestrator."""


# ---------------------------------------------------------------------------
# init: set up directory structure and database
# ---------------------------------------------------------------------------


@main.command()
def init() -> None:
    """Initialize the institute: directories, database, schema."""
    paths.ensure_runtime_dirs()
    db.initialize()
    console.print(f"[green]Initialized.[/green] Database at {paths.DB_PATH}")
    console.print(f"Archive at {paths.ARCHIVE}")
    console.print(f"Genomes at {paths.GENOMES}")


# ---------------------------------------------------------------------------
# status: show a summary
# ---------------------------------------------------------------------------


@main.command()
def status() -> None:
    """Show current institute state: fellows, in-flight projects, kill switch."""
    if not paths.DB_PATH.exists():
        console.print("[yellow]Not initialized.[/yellow] Run `institute init`.")
        return

    with db.connection() as conn:
        kill = conn.execute("SELECT active, reason FROM kill_switch WHERE id = 1").fetchone()
        kill_active = bool(kill and kill["active"])

        if kill_active:
            console.print("[red bold]Kill switch: ON[/red bold]")
            if kill["reason"]:
                console.print(f"  reason: {kill['reason']}")
        else:
            console.print("[green]Kill switch: off[/green]")

        fellows = list(
            conn.execute(
                "SELECT id, name, rank, model, specialization "
                "FROM fellows WHERE retired_at IS NULL ORDER BY rank, name"
            )
        )
        console.print()
        if not fellows:
            console.print("[dim]No Fellows yet. Run `institute bootstrap`.[/dim]")
        else:
            t = Table(title="Fellows", title_style="bold", show_lines=False)
            t.add_column("id")
            t.add_column("name")
            t.add_column("rank")
            t.add_column("model")
            t.add_column("specialization")
            for f in fellows:
                t.add_row(f["id"], f["name"], f["rank"], f["model"], f["specialization"])
            console.print(t)

        projects = list(
            conn.execute(
                "SELECT id, title, state, lead_fellow_id, updated_at "
                "FROM projects ORDER BY updated_at DESC"
            )
        )
        console.print()
        if not projects:
            console.print("[dim]No projects yet.[/dim]")
        else:
            t = Table(title="Projects", title_style="bold")
            t.add_column("id")
            t.add_column("title")
            t.add_column("state")
            t.add_column("lead")
            t.add_column("updated")
            for p in projects:
                t.add_row(
                    p["id"], p["title"][:50], p["state"], p["lead_fellow_id"], p["updated_at"]
                )
            console.print(t)


# ---------------------------------------------------------------------------
# kill-switch: on/off
# ---------------------------------------------------------------------------


@main.group("kill-switch")
def kill_switch() -> None:
    """Halt or resume all College operations."""


@kill_switch.command("on")
@click.option("--reason", default="manual", help="Why the switch was thrown.")
def kill_switch_on(reason: str) -> None:
    with db.connection() as conn, db.transaction(conn):
        conn.execute(
            "UPDATE kill_switch SET active = 1, triggered_at = ?, triggered_by = ?, reason = ? WHERE id = 1",
            (_now(), "founder", reason),
        )
    console.print("[red]Kill switch engaged.[/red] All operations halted.")


@kill_switch.command("off")
def kill_switch_off() -> None:
    with db.connection() as conn, db.transaction(conn):
        conn.execute(
            "UPDATE kill_switch SET active = 0, triggered_at = NULL, triggered_by = NULL, reason = NULL WHERE id = 1"
        )
    console.print("[green]Kill switch released.[/green] Operations may resume.")


# ---------------------------------------------------------------------------
# bootstrap: placeholder for now; full implementation lands in Milestone 3
# ---------------------------------------------------------------------------


@main.command()
@click.option(
    "--from-genomes",
    is_flag=True,
    help="Skip the design step and register genomes already in genomes/.",
)
@click.option(
    "--force",
    is_flag=True,
    help="Allow redrafting even if genomes/ already contains files.",
)
def bootstrap(from_genomes: bool, force: bool) -> None:
    """Instantiate the founding cohort.

    By default the orchestrator-side Claude reads the Charter and proposes
    four Fellow genomes, and the Founder reviews each one in the terminal.
    Use --from-genomes to skip the design step and register whatever JSON
    files are already in genomes/.
    """
    _check_kill_switch()

    if from_genomes:
        genomes = fellow_mod.load_all_genomes()
        if not genomes:
            console.print(f"[red]No genomes found in {paths.GENOMES}.[/red]")
            sys.exit(1)
        with db.connection() as conn, db.transaction(conn):
            for g in genomes:
                fellow_mod.register(conn, g)
                fellow_mod.ensure_fellow_dirs(g.id)
        console.print(f"[green]Registered {len(genomes)} Fellow(s):[/green]")
        for g in genomes:
            console.print(f"  - {g.id} ({g.name}, {g.specialization})")
        return

    from institute.workflows import bootstrap as bootstrap_workflow

    bootstrap_workflow.run(force=force)


# ---------------------------------------------------------------------------
# next: advance the state machine. Placeholder until workflows land.
# ---------------------------------------------------------------------------


@main.command("next")
def next_cmd() -> None:
    """Advance the most stale in-flight project by one step."""
    _check_kill_switch()
    console.print("[yellow]Workflow dispatch not yet implemented.[/yellow] Coming in Milestone 4.")
