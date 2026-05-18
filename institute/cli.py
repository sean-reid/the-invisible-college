"""Command-line interface for the College.

This module is the single entry point for the Founder. Every command is
designed to be safely interruptible: state is persisted before the command
returns, and re-running picks up where things left off.
"""

from __future__ import annotations

import json
import signal
import sqlite3
import sys
import time
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
    # Make sure the schema is current before any subcommand runs. initialize()
    # is idempotent: it creates a fresh DB if missing, runs forward migrations
    # if the on-disk schema is behind, and errors out if it is ahead.
    if paths.DB_PATH.exists():
        db.initialize()


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
# propose: start a new project. A Fellow drafts a research proposal.
# ---------------------------------------------------------------------------


@main.command()
@click.option(
    "--lead",
    type=str,
    default=None,
    help="Fellow id to draft the proposal. If omitted, a sensible default is chosen.",
)
@click.option(
    "--topic",
    type=str,
    default=None,
    help="Optional topic guidance. The Fellow may sharpen, narrow, or push back.",
)
def propose(lead: str | None, topic: str | None) -> None:
    """A Fellow drafts a new research proposal.

    The lead Fellow is invoked once and asked for a structured proposal.
    The result is written to archive/proposals/ and a new project enters
    state PROPOSED.
    """
    _check_kill_switch()
    from institute.workflows import propose as propose_workflow

    propose_workflow.run(lead=lead, topic=topic)


# ---------------------------------------------------------------------------
# next: dispatch the next action for the most-stale in-flight project
# ---------------------------------------------------------------------------


_STATE_TO_WORKFLOW: dict[str, str] = {
    "proposed": "review_proposal",
    "proposal_reviewed": "research",
    "researching": "research",
    "drafted": "peer_review",
    "peer_reviewing": "peer_review",
    "revising": "revise",
    "editorial": "publish",
}


@main.command("next")
@click.option(
    "--project",
    type=str,
    default=None,
    help="Project id to advance. Defaults to the most-stale non-terminal project.",
)
def next_cmd(project: str | None) -> None:
    """Advance the most-stale in-flight project by one step.

    Looks at the project's current state and dispatches the corresponding
    workflow. Each call advances by exactly one step (one Claude invocation
    or one transition). Safe to pause and resume between calls.
    """
    _check_kill_switch()
    row = _pick_in_flight_project(project)
    if row is None:
        if project is not None:
            console.print(f"[red]No such project: {project}[/red]")
            sys.exit(1)
        console.print("[dim]No in-flight projects. Start one with `institute propose`.[/dim]")
        return
    _dispatch_step(row["id"], row["state"])


def _pick_in_flight_project(project: str | None) -> sqlite3.Row | None:
    """Return the row to advance next, or None if there is nothing to do."""
    with db.connection() as conn:
        if project is not None:
            return conn.execute(
                "SELECT id, state FROM projects WHERE id = ?", (project,)
            ).fetchone()
        return conn.execute(
            "SELECT id, state FROM projects "
            "WHERE state NOT IN ('published', 'rejected') "
            "ORDER BY updated_at ASC LIMIT 1"
        ).fetchone()


def _dispatch_step(project_id: str, state: str) -> None:
    """Dispatch the one workflow that advances `state` by one step."""
    workflow_name = _STATE_TO_WORKFLOW.get(state)
    if workflow_name is None:
        console.print(f"[yellow]No workflow defined for state {state}.[/yellow]")
        sys.exit(1)

    console.print(
        f"[dim]Dispatching {workflow_name} for project {project_id} (state={state})...[/dim]"
    )

    # Lazy imports so the CLI starts quickly when not running a workflow.
    if workflow_name == "review_proposal":
        from institute.workflows import review_proposal as wf
    elif workflow_name == "research":
        from institute.workflows import research as wf
    elif workflow_name == "peer_review":
        from institute.workflows import peer_review as wf
    elif workflow_name == "revise":
        from institute.workflows import revise as wf
    elif workflow_name == "publish":
        from institute.workflows import publish as wf
    else:
        raise RuntimeError(f"Unknown workflow: {workflow_name}")

    wf.run(project_id)


def _audit_cost_total() -> float:
    """Sum cost_usd across every entry in the audit log. Best-effort."""
    if not paths.AUDIT_LOG.is_file():
        return 0.0
    total = 0.0
    for line in paths.AUDIT_LOG.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if not line:
            continue
        try:
            entry = json.loads(line)
        except json.JSONDecodeError:
            continue
        cost = entry.get("cost_usd")
        if isinstance(cost, int | float):
            total += float(cost)
    return total


# ---------------------------------------------------------------------------
# run: advance the pipeline autonomously until done, halted, or capped
# ---------------------------------------------------------------------------


@main.command("run")
@click.option(
    "--max-budget-usd",
    type=float,
    default=10.0,
    show_default=True,
    help="Hard cap on cumulative Claude API cost for this run.",
)
@click.option(
    "--max-steps",
    type=int,
    default=30,
    show_default=True,
    help="Maximum number of single-step dispatches before halting.",
)
@click.option(
    "--project",
    type=str,
    default=None,
    help="Only advance this project. Default: the most-stale in-flight project.",
)
def run_cmd(max_budget_usd: float, max_steps: int, project: str | None) -> None:
    """Advance the pipeline autonomously until done, halted, or capped.

    Calls the equivalent of `institute next` repeatedly. Stops when:
      - the active project reaches a terminal state (published or rejected)
      - there are no in-flight projects left
      - the kill switch is engaged
      - the cumulative cost for this run exceeds --max-budget-usd
      - --max-steps iterations are executed
      - the user presses Ctrl-C (the current step finishes; then halts)
      - a workflow step raises

    Designed to be safe to leave running unattended: hard caps on cost
    and steps, kill-switch check before every iteration, atomic state
    transitions between iterations.
    """
    _check_kill_switch()
    baseline_cost = _audit_cost_total()

    stop_requested = {"flag": False}

    def _on_sigint(_signum: int, _frame: object) -> None:
        if stop_requested["flag"]:
            # Second Ctrl-C: hard exit. The first set the flag.
            console.print("\n[red]Hard stop. Mid-step state may need recovery.[/red]")
            sys.exit(130)
        stop_requested["flag"] = True
        console.print(
            "\n[yellow]Stop requested. Will exit after the current step finishes. "
            "Press Ctrl-C again to abort immediately.[/yellow]"
        )

    previous_handler = signal.signal(signal.SIGINT, _on_sigint)
    try:
        for step in range(1, max_steps + 1):
            if stop_requested["flag"]:
                console.print("[yellow]Stopped by user between steps.[/yellow]")
                return

            _check_kill_switch()

            row = _pick_in_flight_project(project)
            if row is None:
                if project is not None:
                    console.print(f"[red]No such project: {project}[/red]")
                    sys.exit(1)
                console.print("[dim]No in-flight projects. Done.[/dim]")
                return
            if row["state"] in ("published", "rejected"):
                console.print(f"[green]Project {row['id']} is {row['state']}. Done.[/green]")
                return

            console.rule(f"[bold]Step {step}[/bold]", align="left", style="dim")
            start = time.monotonic()
            _dispatch_step(row["id"], row["state"])
            elapsed = time.monotonic() - start
            run_cost = _audit_cost_total() - baseline_cost
            console.print(
                f"  [dim]elapsed: {elapsed:.0f}s  ·  "
                f"run cost: ${run_cost:.2f} of ${max_budget_usd:.2f}[/dim]"
            )

            if run_cost >= max_budget_usd:
                console.print(
                    f"[red]Budget cap of ${max_budget_usd:.2f} reached "
                    f"(spent ${run_cost:.2f}). Halting.[/red]"
                )
                return

        console.print(
            f"[yellow]Reached max-steps ({max_steps}) without finishing. "
            "Run again to continue.[/yellow]"
        )
    finally:
        signal.signal(signal.SIGINT, previous_handler)
