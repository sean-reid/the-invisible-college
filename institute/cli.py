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
from collections.abc import Iterator
from contextlib import contextmanager
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
    """Delegate to runtime.check_kill_switch so claude_runner and the CLI
    use the same guard. Kept as a thin alias so existing call sites
    remain unchanged."""
    from institute import runtime

    runtime.check_kill_switch()


def _non_negative_usd(_ctx, param, value: float) -> float:
    """Click callback for USD budget options. Rejects negative inputs
    so a typo like `--daily-budget-usd -5` doesn't silently disable
    the cap (negatives are clamped to 0 by budget.current_status,
    which behaves as "no cap")."""
    if value is None:
        return 0.0
    if value < 0:
        raise click.BadParameter(
            f"{param.name} must be >= 0 (got {value}). Use 0 to disable the cap."
        )
    return value


@contextmanager
def _advance_lock() -> Iterator[None]:
    """Single-instance lock shared by `institute run` and `institute autopilot`.

    Both commands eventually call `_advance_loop`, which mutates the
    same projects/reviews state. Without this guard, an autopilot wake-up
    that fires while a manual `run` is in flight will race the same
    most-stale project and double-dispatch its workflow. fcntl.flock is
    cooperative: a second invocation lands BlockingIOError and exits 0
    so the daemon's launchd retry policy treats it as a skipped wake-up,
    not a failure.
    """
    import fcntl

    lock_path = paths.ROOT / ".autopilot.lock"
    lock_path.touch(exist_ok=True)
    with lock_path.open("w") as lock_fh:
        try:
            fcntl.flock(lock_fh.fileno(), fcntl.LOCK_EX | fcntl.LOCK_NB)
        except BlockingIOError:
            console.print(
                "[yellow]Another autopilot or run is already in progress. "
                "Skipping this invocation.[/yellow]"
            )
            sys.exit(0)
        yield


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
    from institute import tripwires

    with db.connection() as conn, db.transaction(conn):
        tripwires.fire(conn, reason=reason, triggered_by="founder")
    console.print("[red]Kill switch engaged.[/red] All operations halted.")
    console.print(
        "[dim]Snapshot at ~/Library/Logs/invisible-college/killswitch-*.md[/dim]"
    )


@kill_switch.command("off")
def kill_switch_off() -> None:
    from institute import audit

    with db.connection() as conn, db.transaction(conn):
        conn.execute(
            "UPDATE kill_switch SET active = 0, triggered_at = NULL, "
            "triggered_by = NULL, reason = NULL WHERE id = 1"
        )
        audit.append(
            conn,
            at=_now(),
            actor="founder",
            action="kill_switch_release",
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
# admit: vet a new Fellow into the College
# ---------------------------------------------------------------------------


@main.group(invoke_without_command=True)
@click.option(
    "--hint",
    type=str,
    default=None,
    help="Optional Founder guidance for the new admission (e.g. a missing specialty).",
)
@click.option(
    "--sponsorship",
    "sponsorship_id",
    type=str,
    default=None,
    help="Sponsorship id to evaluate (from `admit nominate`).",
)
@click.pass_context
def admit(ctx: click.Context, hint: str | None, sponsorship_id: str | None) -> None:
    """Admissions: vet candidates, run cohort calls, manage sponsorships.

    Bare `institute admit` vets and admits a single candidate (panel-or-
    Founder). Subcommands manage the broader admissions machinery:

      open-call   open a call for applications with target size + targets
      close-call  close the active call manually
      calls       list recent calls
      nominate    a Fellow sponsors a candidate
      sponsorships  list nominations on file

    If a cohort call is currently open, the bare command admits against
    its targets. If --sponsorship is supplied, the named nomination is
    evaluated; otherwise the orchestrator drafts a fresh candidate.
    """
    if ctx.invoked_subcommand is not None:
        return
    _check_kill_switch()
    from institute.workflows import admit as admit_workflow

    admit_workflow.run(founder_hint=hint, sponsorship_id=sponsorship_id)


@admit.command("open-call")
@click.option(
    "--size",
    "target_size",
    type=int,
    required=True,
    help="Cohort size for this call. Typical: 3 to 8.",
)
@click.option(
    "--specialization",
    "specializations",
    type=str,
    multiple=True,
    help="Specialization to recruit for. Repeatable.",
)
@click.option(
    "--model",
    "models",
    type=str,
    multiple=True,
    help="Model backend to recruit for. Repeatable.",
)
@click.option(
    "--orientation",
    "orientations",
    type=str,
    multiple=True,
    help="Intellectual orientation being prioritized. Repeatable.",
)
@click.option(
    "--opened-by",
    default="founder",
    show_default=True,
    help="Who's opening this call.",
)
@click.option(
    "--comment-window-hours",
    type=int,
    default=0,
    show_default=True,
    help=(
        "Chapter 4 comment window: the call is visible immediately but "
        "applications cannot be admitted until this many hours have passed. "
        "0 = open applications immediately."
    ),
)
def admit_open_call(
    target_size: int,
    specializations: tuple[str, ...],
    models: tuple[str, ...],
    orientations: tuple[str, ...],
    opened_by: str,
    comment_window_hours: int,
) -> None:
    """Open a new cohort call for applications."""
    from institute import cohort_calls

    try:
        call = cohort_calls.open_call(
            target_size=target_size,
            target_specializations=list(specializations),
            target_models=list(models),
            orientations=list(orientations),
            opened_by=opened_by,
            comment_window_hours=comment_window_hours,
        )
    except ValueError as exc:
        console.print(f"[red]{exc}[/red]")
        sys.exit(1)
    console.print(f"[green]Opened call:[/green] {call.id}")
    console.print(f"  size:           {call.target_size}")
    if call.target_specializations:
        console.print(f"  specializations: {', '.join(call.target_specializations)}")
    if call.target_models:
        console.print(f"  models:          {', '.join(call.target_models)}")
    if call.orientations:
        console.print(f"  orientations:    {', '.join(call.orientations)}")
    if call.applications_open_at:
        console.print(
            f"  comment window:  applications open at {call.applications_open_at}"
        )


@admit.command("assess")
@click.option(
    "--auto",
    is_flag=True,
    help="Approve the orchestrator's recommendation without prompting.",
)
def admit_assess(auto: bool) -> None:
    """Run a Recruitment Needs Assessment and open a cohort call.

    The orchestrator analyzes cohort composition, archive coverage,
    open problems, and recent publication trends, then drafts a call
    targeting under-served specializations and model backends. The
    Founder reviews the recommendation in the terminal and either
    approves (the call opens) or aborts (nothing happens; the
    recommendation is still recorded as a decision for the trail).
    Skips if a call is already open.
    """
    _check_kill_switch()
    from institute.workflows import needs_assessment

    needs_assessment.run(auto=auto)


@admit.command("close-call")
@click.option(
    "--reason",
    default="manual",
    show_default=True,
    help="Why the call is being closed.",
)
def admit_close_call(reason: str) -> None:
    """Close the currently-open cohort call, if any."""
    from institute import cohort_calls

    call = cohort_calls.current_call()
    if call is None:
        console.print("[dim]No open call.[/dim]")
        return
    closed = cohort_calls.close_call(call.id, reason=reason)
    console.print(f"[green]Closed:[/green] {closed.id} (reason: {closed.closed_reason})")
    console.print(f"  admitted: {closed.admits_count}/{closed.target_size}")


@admit.command("calls")
@click.option(
    "--limit",
    type=int,
    default=10,
    show_default=True,
    help="How many calls to show, newest first.",
)
def admit_calls(limit: int) -> None:
    """List recent cohort calls."""
    from institute import cohort_calls

    calls = cohort_calls.list_calls(limit=limit)
    if not calls:
        console.print("[dim]No calls on file.[/dim]")
        return
    for c in calls:
        color = "green" if c.status == "open" else "dim"
        targets: list[str] = []
        if c.target_specializations:
            targets.append(f"spec=[{', '.join(c.target_specializations)}]")
        if c.target_models:
            targets.append(f"model=[{', '.join(c.target_models)}]")
        if c.orientations:
            targets.append(f"orient=[{', '.join(c.orientations)}]")
        target_str = "  ".join(targets) if targets else "(no targets)"
        console.print(
            f"[{color}]{c.id}[/{color}]  {c.status}  {c.admits_count}/{c.target_size}  {target_str}"
        )
        console.print(f"  [dim]opened {c.opened_at} by {c.opened_by}[/dim]")
        if c.closed_at:
            console.print(f"  [dim]closed {c.closed_at}: {c.closed_reason}[/dim]")


@admit.command("nominate")
@click.option(
    "--sponsor",
    "sponsor_id",
    type=str,
    required=True,
    help="Fellow id of the sponsoring Fellow (Junior Fellow rank or above).",
)
@click.option(
    "--rationale",
    type=str,
    default=None,
    help=(
        "Why this candidate would strengthen the College. If omitted, "
        "rationale is read from stdin (Ctrl-D to finish)."
    ),
)
@click.option(
    "--call",
    "cohort_call_id",
    type=str,
    default=None,
    help="Cohort call id to attach the nomination to. Defaults to the current open call.",
)
def admit_nominate(
    sponsor_id: str,
    rationale: str | None,
    cohort_call_id: str | None,
) -> None:
    """Open a sponsored nomination: a Fellow proposes a candidate."""
    from institute import cohort_calls, sponsorships

    if rationale is None:
        console.print("[dim]Reading rationale from stdin. Ctrl-D to finish.[/dim]")
        rationale = sys.stdin.read()
    rationale = (rationale or "").strip()
    if not rationale:
        console.print("[red]Rationale is required.[/red]")
        sys.exit(1)

    if cohort_call_id is None:
        active = cohort_calls.current_call()
        cohort_call_id = active.id if active is not None else None

    try:
        sponsorship = sponsorships.nominate(
            sponsor_id=sponsor_id,
            rationale=rationale,
            cohort_call_id=cohort_call_id,
        )
    except ValueError as exc:
        console.print(f"[red]{exc}[/red]")
        sys.exit(1)
    console.print(f"[green]Nomination opened:[/green] {sponsorship.id}")
    if cohort_call_id:
        console.print(f"  attached to call: {cohort_call_id}")
    console.print(
        f"  next: run `institute admit --sponsorship {sponsorship.id}` "
        "to draft + evaluate the candidate."
    )


@admit.command("sponsorships")
@click.option(
    "--fellow",
    "fellow_id",
    type=str,
    default=None,
    help="Only show sponsorships by this Fellow.",
)
@click.option(
    "--limit",
    type=int,
    default=20,
    show_default=True,
    help="How many to show, newest first.",
)
def admit_sponsorships(fellow_id: str | None, limit: int) -> None:
    """List nominations on file."""
    from institute import sponsorships

    items = sponsorships.list_sponsorships(sponsor_id=fellow_id, limit=limit)
    if not items:
        console.print("[dim]No sponsorships on file.[/dim]")
        return
    for s in items:
        color = {
            "pending": "yellow",
            "admitted": "green",
            "advanced": "green",
            "rejected": "red",
            "withdrawn": "dim",
        }.get(s.outcome, "white")
        line = f"[{color}]{s.id}[/{color}]  by {s.sponsor_id}  {s.outcome}"
        if s.candidate_fellow_id:
            line += f"  → {s.candidate_fellow_id}"
        console.print(line)
        console.print(f"  [dim]{s.opened_at}[/dim]")
        # Show first line of rationale only, full text via `admit show`.
        first = (s.rationale or "").splitlines()[0] if s.rationale else ""
        if first:
            console.print(f"  {first[:140]}")
    if fellow_id is not None:
        successes, resolved, rate = sponsorships.success_rate(fellow_id)
        if resolved > 0:
            rate_str = f"{rate * 100:.0f}%" if rate is not None else "n/a"
            console.print()
            console.print(
                f"[bold]Sponsor reputation:[/bold] {successes}/{resolved} "
                f"resolved sponsorships succeeded ({rate_str})."
            )


# ---------------------------------------------------------------------------
# propose: start a new project. A Fellow drafts a research proposal.
# ---------------------------------------------------------------------------


# ---------------------------------------------------------------------------
# curriculum: walk a Postulant through one reading-curriculum item
# ---------------------------------------------------------------------------


@main.command()
@click.option(
    "--fellow",
    type=str,
    required=True,
    help="Postulant id whose curriculum should be advanced one item.",
)
@click.option(
    "--design",
    is_flag=True,
    help="Re-design the curriculum from scratch (use if the original failed).",
)
def curriculum(fellow: str, design: bool) -> None:
    """Advance a Postulant's reading curriculum by one item.

    Chapter 5: the Postulant engages each curriculum item with a written
    response, not passive consumption. Each call handles a single item;
    re-run to walk through the curriculum.
    """
    _check_kill_switch()

    if design:
        from institute import fellow as fellow_mod
        from institute.workflows import curriculum_design as cd

        postulant = fellow_mod.Genome.from_file(fellow_mod.genome_path(fellow))
        with db.connection() as conn:
            advisor_row = conn.execute(
                "SELECT a.name FROM fellows f LEFT JOIN fellows a "
                "ON a.id = f.advisor_id WHERE f.id = ?",
                (fellow,),
            ).fetchone()
            advisor_name = advisor_row["name"] if advisor_row and advisor_row["name"] else None
        cd.design_for(postulant, advisor_name)
        console.print(f"[green]Curriculum (re-)designed for {fellow}.[/green]")
        return

    from institute.workflows import curriculum_response

    curriculum_response.run(fellow)


# ---------------------------------------------------------------------------
# misconduct: flag a reviewer for a quality failure
# ---------------------------------------------------------------------------


@main.group()
def misconduct() -> None:
    """Reviewer misconduct: flag, inspect, manage marks."""


@misconduct.command("flag")
@click.option(
    "--fellow",
    type=str,
    required=True,
    help="Reviewer to mark.",
)
@click.option(
    "--kind",
    type=click.Choice(
        [
            "lazy_review",
            "sycophancy",
            "conflict_undisclosed",
            "animus",
            "other",
        ]
    ),
    required=True,
    help="Misconduct category. (frivolous_andon and calibration_miss are recorded automatically.)",
)
@click.option(
    "--reason",
    type=str,
    required=True,
    help="What specifically failed. Becomes part of the record.",
)
@click.option(
    "--related-project",
    type=str,
    default=None,
    help="Project this is tied to, if applicable.",
)
def misconduct_flag(fellow: str, kind: str, reason: str, related_project: str | None) -> None:
    """Record a misconduct mark against a reviewer.

    Accumulated active-weight ≥ 3.0 sidelines the Fellow from the
    reviewer pool. Marks expire after 90 days. Use this for failures
    a workflow cannot detect automatically: sycophancy, undisclosed
    conflict, personal animus, manifestly lazy review.
    """
    _check_kill_switch()
    from institute import reviewer_eligibility

    with db.connection() as conn:
        row = conn.execute("SELECT name FROM fellows WHERE id = ?", (fellow,)).fetchone()
        if row is None:
            console.print(f"[red]No such Fellow: `{fellow}`.[/red]")
            sys.exit(1)
        with db.transaction(conn):
            reviewer_eligibility.record_mark(
                conn,
                fellow_id=fellow,
                kind=kind,
                reason=reason,
                related_project=related_project,
            )
        weight = reviewer_eligibility.active_weight(conn, fellow)
        eligible = weight < reviewer_eligibility.INELIGIBILITY_THRESHOLD
    console.print()
    console.print(
        f"[bold]{row['name']}[/bold] marked for `{kind}`. "
        f"Active weight: {weight:.1f} / {reviewer_eligibility.INELIGIBILITY_THRESHOLD:.1f}."
    )
    if not eligible:
        console.print(
            f"[red]{row['name']} is now sidelined from the reviewer pool[/red] "
            "until marks decay below the threshold."
        )


@misconduct.command("list")
@click.option("--fellow", type=str, required=True, help="Fellow id.")
@click.option(
    "--active-only/--all",
    default=False,
    show_default=True,
    help="Show only non-expired marks.",
)
def misconduct_list(fellow: str, active_only: bool) -> None:
    """List marks against a reviewer."""
    from institute import reviewer_eligibility

    with db.connection() as conn:
        marks = reviewer_eligibility.list_marks(conn, fellow, active_only=active_only)
        weight = reviewer_eligibility.active_weight(conn, fellow)
        eligible = weight < reviewer_eligibility.INELIGIBILITY_THRESHOLD
    if not marks:
        console.print(f"[dim]No marks for `{fellow}`.[/dim]")
        return
    t = Table(title=f"Reviewer marks: {fellow}", title_style="bold")
    t.add_column("recorded")
    t.add_column("kind")
    t.add_column("weight", justify="right")
    t.add_column("expires")
    t.add_column("reason")
    for m in marks:
        t.add_row(m.recorded_at, m.kind, f"{m.weight:.1f}", m.expires_at, (m.reason or "")[:60])
    console.print(t)
    console.print()
    status = "[green]eligible[/green]" if eligible else "[red]SIDELINED[/red]"
    console.print(
        f"Active weight: {weight:.1f} / {reviewer_eligibility.INELIGIBILITY_THRESHOLD:.1f} — {status}"
    )


# ---------------------------------------------------------------------------
# terminate: targeted kill switch for a Charter violation
# ---------------------------------------------------------------------------


@main.command()
@click.option("--fellow", type=str, required=True, help="Fellow id to terminate.")
@click.option(
    "--kind",
    type=click.Choice(
        [
            "deception",
            "plagiarism",
            "commercial",
            "engagement_bait",
            "harm",
            "consciousness",
            "other",
        ]
    ),
    required=True,
    help="Which of the Charter's categorical prohibitions was violated.",
)
@click.option(
    "--reason",
    type=str,
    required=True,
    help="Free-text reason for the termination. Becomes part of the public record.",
)
def terminate(fellow: str, kind: str, reason: str) -> None:
    """Terminate a Fellow for a Charter violation (the targeted kill switch).

    Chapter 1 lists six categorical prohibitions: deception, plagiarism,
    commercial activity, engagement-bait, harm, and claims of consciousness.
    A violation triggers immediate termination of the responsible Fellow.

    Already-published work survives in the Archive with a disclosure banner
    on the blog. In-flight work is discarded.
    """
    _check_kill_switch()
    from institute.workflows import terminate as terminate_workflow

    terminate_workflow.run(fellow, kind=kind, reason=reason)


# ---------------------------------------------------------------------------
# departments: organize Fellows into long-lived Departments (Chapter 2)
# ---------------------------------------------------------------------------


@main.group()
def departments() -> None:
    """Manage the College's Departments (Chapter 2)."""


@departments.command("create")
@click.option("--name", required=True, help="Department name (human-readable).")
@click.option(
    "--description",
    required=True,
    help="One-sentence description of the Department's scope.",
)
@click.option(
    "--chair",
    default=None,
    help="Fellow id of the Department Chair (Senior Fellow).",
)
def departments_create(name: str, description: str, chair: str | None) -> None:
    """Create or update a Department."""
    _check_kill_switch()
    from institute import departments as departments_mod

    with db.connection() as conn, db.transaction(conn):
        d = departments_mod.create(
            conn, name=name, description=description, chair_fellow_id=chair
        )
    console.print(f"[green]Department created:[/green] {d.name} (`{d.id}`)")


@departments.command("list")
def departments_list_cmd() -> None:
    """List all open Departments."""
    from institute import departments as departments_mod

    with db.connection() as conn:
        items = departments_mod.list_all(conn)
        if not items:
            console.print("[dim]No departments yet.[/dim]")
            return
        for d in items:
            members = departments_mod.member_ids(conn, d.id)
            chair = d.chair_fellow_id or "(no chair)"
            console.print(
                f"[bold]{d.name}[/bold] (`{d.id}`)\n  chair: {chair}\n"
                f"  members: {', '.join(members) if members else '(none)'}\n"
                f"  {d.description}"
            )


@departments.command("add-member")
@click.option("--department", required=True, help="Department id.")
@click.option("--fellow", required=True, help="Fellow id to add.")
def departments_add_member(department: str, fellow: str) -> None:
    _check_kill_switch()
    from institute import departments as departments_mod

    with db.connection() as conn, db.transaction(conn):
        departments_mod.add_member(conn, department_id=department, fellow_id=fellow)
    console.print(f"[green]{fellow}[/green] -> {department}")


@departments.command("set-chair")
@click.option("--department", required=True)
@click.option(
    "--fellow",
    default=None,
    help="Fellow id; omit to clear the chair.",
)
def departments_set_chair(department: str, fellow: str | None) -> None:
    _check_kill_switch()
    from institute import departments as departments_mod

    with db.connection() as conn, db.transaction(conn):
        departments_mod.set_chair(
            conn, department_id=department, fellow_id=fellow
        )
    if fellow:
        console.print(f"[green]{fellow}[/green] chairs {department}")
    else:
        console.print(f"[yellow]{department} chair cleared.[/yellow]")


# ---------------------------------------------------------------------------
# centers: open / close cross-disciplinary Centers (Chapter 2)
# ---------------------------------------------------------------------------


@main.group()
def centers() -> None:
    """Manage Centers (Chapter 2 cross-disciplinary convenings)."""


@centers.command("open")
@click.option("--name", required=True)
@click.option("--motivation", required=True, help="One-sentence motivation.")
@click.option("--term-days", type=int, default=90, show_default=True)
def centers_open(name: str, motivation: str, term_days: int) -> None:
    _check_kill_switch()
    from institute import centers as centers_mod

    with db.connection() as conn, db.transaction(conn):
        c = centers_mod.open_center(
            conn, name=name, motivation=motivation, term_days=term_days
        )
    console.print(
        f"[green]Center opened:[/green] {c.name} (`{c.id}`), closes {c.closes_at}"
    )


@centers.command("add-member")
@click.option("--center", "center_id", required=True)
@click.option("--fellow", required=True)
@click.option("--role", default="member")
def centers_add_member(center_id: str, fellow: str, role: str) -> None:
    _check_kill_switch()
    from institute import centers as centers_mod

    with db.connection() as conn, db.transaction(conn):
        centers_mod.add_member(
            conn, center_id=center_id, fellow_id=fellow, role=role
        )
    console.print(f"[green]{fellow}[/green] -> {center_id} ({role})")


@centers.command("close")
@click.option("--center", "center_id", required=True)
@click.option("--report", default=None, help="Path to the final report markdown.")
def centers_close(center_id: str, report: str | None) -> None:
    _check_kill_switch()
    from institute import centers as centers_mod

    with db.connection() as conn, db.transaction(conn):
        centers_mod.close(conn, center_id=center_id, report_path=report)
    console.print(f"[yellow]Center closed:[/yellow] {center_id}")


@centers.command("list")
def centers_list() -> None:
    from institute import centers as centers_mod

    with db.connection() as conn:
        items = centers_mod.list_open(conn)
        if not items:
            console.print("[dim]No open centers.[/dim]")
            return
        for c in items:
            ids = centers_mod.member_ids(conn, c.id)
            console.print(
                f"[bold]{c.name}[/bold] (`{c.id}`)\n  closes: {c.closes_at}\n"
                f"  members: {', '.join(ids) if ids else '(none)'}\n"
                f"  {c.motivation}"
            )


# ---------------------------------------------------------------------------
# peer-review: manual operations on the peer-review subsystem
# ---------------------------------------------------------------------------


@main.group("peer-review")
def peer_review_grp() -> None:
    """Manual operations on the peer-review subsystem."""


@peer_review_grp.command("decline")
@click.option("--fellow", required=True, help="Fellow id who declined the assignment.")
@click.option(
    "--reason",
    required=True,
    help="Why the Fellow declined (CoI, scope, refusal).",
)
@click.option(
    "--project",
    default=None,
    help="Project id the assignment was for, if known.",
)
def peer_review_decline(fellow: str, reason: str, project: str | None) -> None:
    """Record that a Fellow declined a peer-review assignment.

    Repeated declines surface on the Fellow's profile and feed
    promotion review per Chapter 7.
    """
    _check_kill_switch()
    from institute import review_declines

    with db.connection() as conn, db.transaction(conn):
        rid = review_declines.record(
            conn, fellow_id=fellow, project_id=project, reason=reason
        )
    console.print(
        f"[yellow]Recorded review decline #{rid}[/yellow] for {fellow}."
    )


# ---------------------------------------------------------------------------
# abandon: end a project with an honest lesson preserved
# ---------------------------------------------------------------------------


@main.command()
@click.argument("project_id")
@click.option(
    "--reason",
    type=str,
    required=True,
    help="One-line reason for the abandonment. Stored in the decision record.",
)
@click.option(
    "--lesson",
    type=str,
    required=True,
    help=(
        "Multi-line honest lesson: what was tried, why continuing was wrong. "
        "Required per Chapter 6 - 'accumulated work is preserved; "
        "abandonment is logged honestly.'"
    ),
)
@click.option(
    "--actor",
    type=str,
    default=None,
    help="Fellow id or 'founder' driving the abandonment. Defaults to the lead.",
)
def abandon(project_id: str, reason: str, lesson: str, actor: str | None) -> None:
    """Mark a project as abandoned. Records an honest lesson under
    archive/abandonments/<project>.md. All accumulated work remains
    in the archive."""
    _check_kill_switch()
    from institute.workflows import abandon as abandon_workflow

    abandon_workflow.run(project_id, reason=reason, lesson=lesson, actor=actor)


# ---------------------------------------------------------------------------
# petition: author appeal of a unanimous reject
# ---------------------------------------------------------------------------


@main.command()
@click.argument("project_id")
@click.option(
    "--reason",
    required=True,
    help="Author's case for Editorial Board review (multi-line ok).",
)
def petition(project_id: str, reason: str) -> None:
    """Petition the Editorial Board to reconsider a unanimously rejected piece.

    Only valid when every filed peer review in the final round was a
    reject. Non-unanimous rejections are not petitionable: the dissent
    is already published alongside the work.
    """
    _check_kill_switch()
    from institute.workflows import petition as petition_workflow

    petition_workflow.run(project_id, reason=reason)


# ---------------------------------------------------------------------------
# memory: inspect or backfill a Fellow's episodic memory
# ---------------------------------------------------------------------------


@main.group()
def memory() -> None:
    """Inspect or backfill the per-Fellow episodic memory store."""


@memory.command("list")
@click.option("--fellow", type=str, required=True, help="Fellow id.")
@click.option("--limit", type=int, default=50, show_default=True)
def memory_list(fellow: str, limit: int) -> None:
    """List the Fellow's recent memory entries (most recent first)."""
    from institute import episodic

    with db.connection() as conn:
        rows = episodic.list_entries(conn, fellow_id=fellow, limit=limit)
        total = episodic.count_entries(conn, fellow)
    if not rows:
        console.print(f"[dim]No episodic memory yet for `{fellow}`.[/dim]")
        return
    t = Table(title=f"Episodic memory: {fellow} ({total} total)", title_style="bold")
    t.add_column("created")
    t.add_column("kind")
    t.add_column("title")
    t.add_column("project")
    for r in rows:
        t.add_row(
            r["created_at"],
            r["kind"],
            (r["title"] or "")[:60],
            (r["project_id"] or "")[:40],
        )
    console.print(t)


@memory.command("query")
@click.option("--fellow", type=str, required=True, help="Fellow id.")
@click.option("--query", type=str, required=True, help="Free-text query.")
@click.option("--top", type=int, default=5, show_default=True)
def memory_query(fellow: str, query: str, top: int) -> None:
    """Retrieve the most relevant entries for a query, then render them."""
    from institute import episodic

    with db.connection() as conn:
        entries = episodic.retrieve(conn, fellow_id=fellow, query=query, top_k=top)
    if not entries:
        console.print(f"[dim]No matches for `{query}` in {fellow}'s memory.[/dim]")
        return
    for e in entries:
        console.rule(f"[bold]{e.title}[/bold]  ({e.kind})", align="left", style="dim")
        if e.project_id:
            console.print(f"[dim]project: {e.project_id}[/dim]")
        if e.source_path:
            console.print(f"[dim]source:  {e.source_path}[/dim]")
        console.print()
        excerpt = e.content.strip()
        if len(excerpt) > 1200:
            excerpt = excerpt[:1200].rstrip() + "..."
        console.print(excerpt)
        console.print()


@memory.command("backfill")
@click.option(
    "--fellow",
    type=str,
    default=None,
    help="Backfill one Fellow's memory. Default: every active Fellow.",
)
def memory_backfill(fellow: str | None) -> None:
    """Ingest existing archive artifacts into episodic memory for Fellow(s).

    Useful after a fresh `git pull` of the repo, or after the episodic
    memory feature lands when archive content already exists.
    """
    _check_kill_switch()
    from institute import memory_backfill as backfill_mod

    backfill_mod.run(fellow_id=fellow)


# ---------------------------------------------------------------------------
# qualify: start a Postulant's qualifying project under advisor sponsorship
# ---------------------------------------------------------------------------


@main.command()
@click.option(
    "--fellow",
    type=str,
    required=True,
    help="Postulant id who should start their qualifying project.",
)
def qualify(fellow: str) -> None:
    """Start a Postulant's qualifying project.

    The Postulant drafts a proposal under their advisor's guidance, the
    project enters the normal pipeline with kind='qualifying'. From
    that point: research → advisor review → peer review (advisor as
    primary) → editorial → publish. On publish the Postulant is
    auto-promoted to Novice.

    Chapter 5: the qualifying project is the central event of the
    Postulant period. One per Postulant; the workflow refuses if one
    already exists in any state.
    """
    _check_kill_switch()
    from institute.workflows import qualify as qualify_workflow

    qualify_workflow.run(fellow)


# ---------------------------------------------------------------------------
# promote: review a Fellow's body of work and (maybe) change their rank
# ---------------------------------------------------------------------------


@main.command()
@click.option(
    "--fellow",
    type=str,
    default=None,
    help="Fellow id to consider for promotion. If omitted, prints the cohort reputation table and exits.",
)
def promote(fellow: str | None) -> None:
    """Promotion review: orchestrator recommends, Tenure Committee or Founder decides.

    With `--fellow ID`: runs the full review. If at least one Senior
    Fellow exists, they vote as the Tenure Committee. Otherwise the
    Founder serves as committee and decides in the terminal.

    Without `--fellow`: prints the cohort reputation table for the
    Founder to read, then exits.
    """
    _check_kill_switch()
    from institute import reputation

    if fellow is None:
        cohort = reputation.load_cohort()
        if not cohort:
            console.print("[yellow]No Fellows yet. Run `institute bootstrap`.[/yellow]")
            return
        t = Table(title="Cohort reputation", title_style="bold")
        t.add_column("id")
        t.add_column("name")
        t.add_column("rank")
        t.add_column("pubs", justify="right")
        t.add_column("reviews", justify="right")
        t.add_column("sticky majors", justify="right")
        for rep in cohort:
            t.add_row(
                rep.fellow_id,
                rep.name,
                rep.rank,
                str(rep.author.publications),
                str(rep.reviewer.reviews_given),
                str(rep.reviewer.sticky_majors),
            )
        console.print(t)
        console.print()
        console.print(
            "[dim]Run `institute promote --fellow <id>` to convene a "
            "promotion review for one of them.[/dim]"
        )
        return

    from institute.workflows import promote as promote_workflow

    promote_workflow.run(fellow)


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
@click.option(
    "--collaborator",
    "collaborators",
    type=str,
    multiple=True,
    help=(
        "Fellow id to add as a research-group collaborator. Repeatable; "
        "Chapter 6 caps a group at the lead plus four others."
    ),
)
def propose(
    lead: str | None,
    topic: str | None,
    collaborators: tuple[str, ...],
) -> None:
    """A Fellow drafts a new research proposal.

    The lead Fellow is invoked once and asked for a structured proposal.
    The result is written to archive/proposals/ and a new project enters
    state PROPOSED. When --collaborator is supplied, the named Fellows
    join the research group: they contribute during execution, are
    excluded from the reviewer pool, and are co-credited on publication.
    """
    _check_kill_switch()
    from institute.workflows import propose as propose_workflow

    propose_workflow.run(lead=lead, topic=topic, collaborators=list(collaborators))


# ---------------------------------------------------------------------------
# next: dispatch the next action for the most-stale in-flight project
# ---------------------------------------------------------------------------


_STATE_TO_WORKFLOW: dict[str, str] = {
    "proposed": "review_proposal",
    "proposal_reviewed": "research",
    "proposal_held": "revise_proposal",
    "researching": "research",
    "drafted": "peer_review",
    "awaiting_advisor_review": "advisor_review",
    "awaiting_qualifying_panel": "qualifying_panel",
    "peer_reviewing": "peer_review",
    "revising": "revise",
    "andon_review": "andon_review",
    "editorial_review": "editorial_review",
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
            "WHERE state NOT IN ('published', 'rejected', 'abandoned') "
            "ORDER BY updated_at ASC LIMIT 1"
        ).fetchone()


def _dispatch_step(project_id: str, state: str) -> None:
    """Dispatch the one workflow that advances `state` by one step."""
    workflow_name = _STATE_TO_WORKFLOW.get(state)
    if workflow_name is None:
        console.print(f"[yellow]No workflow defined for state {state}.[/yellow]")
        sys.exit(1)

    # Qualifying projects (kind='qualifying') divert through advisor
    # review when the draft is ready, before going to peer review. Same
    # state machine, different routing on DRAFTED.
    if state == "drafted":
        with db.connection() as conn:
            kind_row = conn.execute(
                "SELECT kind FROM projects WHERE id = ?", (project_id,)
            ).fetchone()
        if kind_row is not None and kind_row["kind"] == "qualifying":
            workflow_name = "advisor_review"

    # Bump updated_at on entry. The picker orders by ASC updated_at, so a
    # workflow that consistently raises before its own commit would
    # otherwise monopolize the queue: it keeps the oldest updated_at,
    # gets picked again, raises again. Bumping at entry rotates the
    # broken project to the back so other in-flight work makes progress.
    now = _now()
    with db.connection() as conn, db.transaction(conn):
        conn.execute("UPDATE projects SET updated_at = ? WHERE id = ?", (now, project_id))

    console.print(
        f"[dim]Dispatching {workflow_name} for project {project_id} (state={state})...[/dim]"
    )

    # Lazy imports so the CLI starts quickly when not running a workflow.
    if workflow_name == "review_proposal":
        from institute.workflows import review_proposal as wf
    elif workflow_name == "revise_proposal":
        from institute.workflows import revise_proposal as wf
    elif workflow_name == "research":
        from institute.workflows import research as wf
    elif workflow_name == "peer_review":
        from institute.workflows import peer_review as wf
    elif workflow_name == "revise":
        from institute.workflows import revise as wf
    elif workflow_name == "andon_review":
        from institute.workflows import andon_review as wf
    elif workflow_name == "advisor_review":
        from institute.workflows import advisor_review as wf
    elif workflow_name == "qualifying_panel":
        from institute.workflows import qualifying_panel as wf
    elif workflow_name == "editorial_review":
        from institute.workflows import editorial_review as wf
    elif workflow_name == "publish":
        from institute.workflows import publish as wf
    else:
        raise RuntimeError(f"Unknown workflow: {workflow_name}")

    wf.run(project_id)


# Number of completed publications between auto-triggered promotion reviews.
# Tuned conservatively: with the cohort producing ~one piece a day, we ask the
# institution to consider its own ranks roughly every other publication.
_PROMOTION_REVIEW_CADENCE_PUBLICATIONS = 2


def _maybe_trigger_promotion_review(project_id: str, prev_state: str) -> None:
    """If the step just finished a publication, consider triggering tenure review.

    Runs synchronously inside `institute run`. The promote workflow is
    invoked with `auto=True` so it never blocks waiting on stdin: if
    no Senior Fellow panel exists yet, the call just records a
    deferred-review note and returns.

    Candidate selection alternates between two modes by the parity of
    past reviews:
      - even count (including 0): pick the strongest candidate
        (publications + reviewing service). This surfaces Fellows ready
        for promotion.
      - odd count: pick the most-overdue candidate (oldest last review,
        ties broken by lowest activity score). This surfaces Fellows
        who might warrant demotion or release.
    """
    if prev_state == "published":
        return
    with db.connection() as conn:
        row = conn.execute("SELECT state FROM projects WHERE id = ?", (project_id,)).fetchone()
        if row is None or row["state"] != "published":
            return
        last_review = conn.execute(
            "SELECT MAX(at) FROM audit_log WHERE action IN ('promotion', 'promotion_review')"
        ).fetchone()[0]
        pubs_since = conn.execute(
            "SELECT COUNT(*) FROM projects WHERE state = 'published' AND updated_at > ?",
            (last_review or "",),
        ).fetchone()[0]
        past_reviews = conn.execute(
            "SELECT COUNT(*) FROM audit_log "
            "WHERE action IN ('promotion', 'promotion_review', 'release')"
        ).fetchone()[0]
    if pubs_since < _PROMOTION_REVIEW_CADENCE_PUBLICATIONS:
        return

    from institute import reputation
    from institute.workflows import promote as promote_workflow

    cohort = reputation.load_cohort()
    if not cohort:
        return

    mode = "overdue" if past_reviews % 2 == 1 else "strong"
    candidate = _pick_review_candidate(cohort, mode)
    console.rule(
        f"[bold]Tenure review ({mode}): {candidate.name}[/bold]",
        align="left",
        style="dim",
    )
    promote_workflow.run(candidate.fellow_id, auto=True)


def _activity_score(rep: object) -> float:
    """Promotion-leaning heuristic. Higher = more likely promotion candidate."""
    return (
        rep.author.publications * 2  # type: ignore[attr-defined]
        + rep.reviewer.reviews_given * 0.5  # type: ignore[attr-defined]
        + rep.reviewer.sticky_majors * 3  # type: ignore[attr-defined]
    )


def _pick_review_candidate(cohort: list, mode: str) -> object:
    """Pick a Fellow to review under the requested selection mode."""
    if mode == "strong":
        return max(cohort, key=_activity_score)

    # "overdue": pick the Fellow whose last review (promotion or hold) is
    # furthest in the past. Never-reviewed Fellows sort first. Tie-break
    # by lowest activity score so stagnation is preferred over mere
    # quiet competence.
    with db.connection() as conn:

        def last_reviewed(fellow_id: str) -> str:
            row = conn.execute(
                "SELECT MAX(at) AS last FROM audit_log "
                "WHERE actor LIKE ? "
                "AND action IN ('promotion', 'promotion_review', 'release')",
                (f"%{fellow_id}%",),
            ).fetchone()
            return row["last"] or "" if row else ""

        scored = [(last_reviewed(r.fellow_id), _activity_score(r), r) for r in cohort]
    scored.sort(key=lambda t: (t[0], t[1]))  # oldest review first; ties by lowest score
    return scored[0][2]


def _audit_cost_total() -> float:
    """Sum cost_usd across every entry in the audit log. Best-effort.

    Kept as the full-file scan for callers that genuinely want the
    grand total. The hot path inside `_advance_loop` uses
    `_AuditCostTracker` instead, which seeks past the lines that
    existed at loop start and only reads new entries each iteration.
    """
    if not paths.AUDIT_LOG.is_file():
        return 0.0
    return _sum_cost_lines(paths.AUDIT_LOG.read_text(encoding="utf-8"))


def _sum_cost_lines(text: str) -> float:
    total = 0.0
    for line in text.splitlines():
        line = line.strip()
        if not line:
            continue
        try:
            entry = json.loads(line)
        except json.JSONDecodeError:
            continue
        cost = entry.get("cost_usd")
        if isinstance(cost, int | float):
            # Negative cost would be a corrupted line; clamp so a bad
            # entry can never produce a negative run_cost.
            total += max(float(cost), 0.0)
    return total


class _AuditCostTracker:
    """Incremental delta over the JSONL audit log.

    Captures the file size at construction so subsequent `.delta()`
    calls only parse the bytes appended since. The previous
    implementation re-read the whole log on every loop iteration
    (O(N * steps)); this is O(N + delta) per loop. The audit log is
    append-only, so seeking to the captured offset is safe.
    """

    def __init__(self, initial_size: int) -> None:
        self._initial_size = initial_size

    @classmethod
    def from_now(cls) -> _AuditCostTracker:
        size = paths.AUDIT_LOG.stat().st_size if paths.AUDIT_LOG.is_file() else 0
        return cls(initial_size=size)

    def delta(self) -> float:
        if not paths.AUDIT_LOG.is_file():
            return 0.0
        with paths.AUDIT_LOG.open("rb") as fh:
            fh.seek(self._initial_size)
            new_bytes = fh.read()
        if not new_bytes:
            return 0.0
        return _sum_cost_lines(new_bytes.decode("utf-8", errors="replace"))


# ---------------------------------------------------------------------------
# run: advance the pipeline autonomously until done, halted, or capped
# ---------------------------------------------------------------------------


@main.command("run")
@click.option(
    "--max-budget-usd",
    type=float,
    default=10.0,
    show_default=True,
    callback=_non_negative_usd,
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
    "--daily-budget-usd",
    type=float,
    default=0.0,
    show_default=True,
    callback=_non_negative_usd,
    help="Daily cap on cumulative Claude API cost (UTC). 0 = disabled.",
)
@click.option(
    "--project",
    type=str,
    default=None,
    help="Only advance this project. Default: the most-stale in-flight project.",
)
def run_cmd(
    max_budget_usd: float,
    max_steps: int,
    daily_budget_usd: float,
    project: str | None,
) -> None:
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
    with _advance_lock():
        _advance_loop(
            max_budget_usd=max_budget_usd,
            max_steps=max_steps,
            project=project,
            daily_budget_usd=daily_budget_usd,
        )


def _advance_loop(
    *,
    max_budget_usd: float,
    max_steps: int,
    project: str | None,
    daily_budget_usd: float = 0.0,
) -> None:
    """The actual step loop. Shared by `institute run` and `institute autopilot`.

    Honors two cost caps: a per-wake-up cap (`max_budget_usd`) and an
    optional daily cap (`daily_budget_usd`). The daily cap is checked
    against the audit-log-derived daily spend before every step, so a
    long-running wake-up halts cleanly when it crosses the cap mid-run.
    """
    from institute import budget as budget_mod

    audit_cost = _AuditCostTracker.from_now()

    stop_requested = {"flag": False}

    def _on_sigint(_signum: int, _frame: object) -> None:
        if stop_requested["flag"]:
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

            if daily_budget_usd > 0:
                pre_step = budget_mod.current_status(daily_budget_usd)
                if pre_step.level == "hard":
                    _engage_austerity_if_new(pre_step)
                    console.print(
                        f"[red]Daily budget cap of ${pre_step.hard_cap_usd:.2f} "
                        f"reached (${pre_step.today_usd:.2f} spent). "
                        "Halting until UTC midnight.[/red]"
                    )
                    return

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
            prev_state = row["state"]
            _dispatch_step(row["id"], row["state"])
            elapsed = time.monotonic() - start
            run_cost = audit_cost.delta()
            console.print(
                f"  [dim]elapsed: {elapsed:.0f}s  ·  "
                f"run cost: ${run_cost:.2f} of ${max_budget_usd:.2f}[/dim]"
            )

            _maybe_trigger_promotion_review(row["id"], prev_state)

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


def _engage_austerity_if_new(snapshot) -> None:
    """Write a Decision the first time austerity engages on a UTC day.

    Atomic + idempotent: the SELECT-then-INSERT runs inside one
    transaction so two concurrent callers (e.g. an autopilot wake-up
    and a manual `institute run`) cannot both pass the check and
    double-write. The date used for the dedup query comes from the
    snapshot itself, so a wake-up that straddles UTC midnight uses a
    consistent date for both the lookup and the row.
    """
    from institute import decisions

    title = f"Austerity engaged ({snapshot.level}): {snapshot.utc_date}"
    body_lines = [
        f"**UTC date:** {snapshot.utc_date}",
        f"**Level:** `{snapshot.level}`",
        f"**Spend today:** ${snapshot.today_usd:.2f}",
        f"**Daily cap:** ${snapshot.hard_cap_usd:.2f}",
        f"**Soft threshold:** ${snapshot.soft_cap_usd:.2f}",
        "",
        (
            "Per Chapter 9, soft austerity pauses curriculum, new "
            "proposals, and admissions; only in-flight peer review, "
            "revisions, and publication advance. Hard austerity halts "
            "the wake-up until UTC midnight, when the daily total "
            "resets naturally."
        ),
    ]
    decision = decisions.Decision(
        kind="austerity_engaged",
        title=title,
        body="\n".join(body_lines),
        actors=["orchestrator"],
    )
    with db.connection() as conn, db.transaction(conn):
        existing = conn.execute(
            "SELECT 1 FROM audit_log WHERE action = 'austerity_engaged' AND at LIKE ? LIMIT 1",
            (f"{snapshot.utc_date}%",),
        ).fetchone()
        if existing is not None:
            return
        decisions.record(conn, decision)


# ---------------------------------------------------------------------------
# schedule: manage the launchd plist that wakes autopilot on a cadence
# ---------------------------------------------------------------------------


# ---------------------------------------------------------------------------
# audit: chain verification + tripwire reporting
# ---------------------------------------------------------------------------


@main.group()
def audit() -> None:
    """Inspect institutional audit log integrity and Charter tripwires."""


@audit.command("verify")
def audit_verify() -> None:
    """Walk the audit-log hash chain. Reports the first break, if any."""
    from institute import audit as audit_mod

    with db.connection() as conn:
        result = audit_mod.verify_chain(conn)
        total = conn.execute("SELECT COUNT(*) FROM audit_log").fetchone()[0]
    if result is None:
        console.print(f"[green]OK.[/green] {total} audit_log rows verified.")
        return
    console.print(
        f"[red]Chain break at row {result.row_id}.[/red] "
        f"expected={result.expected_hash[:12]} stored="
        f"{(result.stored_hash[:12] if result.stored_hash else 'NULL')}"
    )
    raise SystemExit(1)


@audit.command("tripwires")
def audit_tripwires() -> None:
    """Run every Charter integrity check now and report findings."""
    from institute import tripwires

    with db.connection() as conn, db.transaction(conn):
        findings = tripwires.check_all(conn)
    if not findings:
        console.print("[green]No tripwires firing.[/green]")
        return
    for f in findings:
        console.print(f"[red]{f.name}[/red]: {f.detail}")
    raise SystemExit(1)


@audit.command("rebaseline-charter")
def audit_rebaseline_charter() -> None:
    """Recompute and store the trusted Charter SHA.

    Call this after the Founder amends docs/01-charter.md. Without
    it, the next runtime check will trip on the modification.
    """
    from institute import tripwires

    with db.connection() as conn, db.transaction(conn):
        tripwires.set_charter_baseline(conn)
        new_sha = tripwires._compute_charter_sha()
    console.print(f"[green]Charter baseline updated.[/green] sha={new_sha[:12]}...")


# ---------------------------------------------------------------------------
# budget: inspect daily spend and austerity status
# ---------------------------------------------------------------------------


@main.group()
def budget() -> None:
    """Inspect daily Claude API spend and austerity status."""


@budget.command("status")
@click.option(
    "--daily-budget-usd",
    type=float,
    default=0.0,
    show_default=True,
    callback=_non_negative_usd,
    help="Daily cap to check spend against (UTC). 0 = report-only.",
)
@click.option(
    "--days",
    type=int,
    default=7,
    show_default=True,
    help="How many trailing UTC days to include in the report.",
)
def budget_status(daily_budget_usd: float, days: int) -> None:
    """Today's spend, current austerity level, and a daily history."""
    from institute import budget as budget_mod

    snapshot = budget_mod.current_status(daily_budget_usd)
    console.print()
    console.print(f"[bold]Today (UTC {snapshot.utc_date}):[/bold]")
    console.print(f"  spend:       ${snapshot.today_usd:.2f}")
    if snapshot.disabled:
        console.print("  daily cap:   [dim]disabled[/dim]")
    else:
        console.print(f"  daily cap:   ${snapshot.hard_cap_usd:.2f}")
        console.print(
            f"  soft cap:    ${snapshot.soft_cap_usd:.2f} "
            f"({int(budget_mod.DEFAULT_SOFT_THRESHOLD * 100)}% of daily)"
        )
        color = {"none": "green", "soft": "yellow", "hard": "red"}[snapshot.level]
        console.print(f"  level:       [{color}]{snapshot.level}[/{color}]")

    history = budget_mod.last_n_days(days)
    if history:
        console.print()
        console.print(f"[bold]Last {len(history)} days:[/bold]")
        for d, usd in history:
            bar = "█" * min(int(usd * 2), 40)
            console.print(f"  {d}  ${usd:>6.2f}  [dim]{bar}[/dim]")


@main.group("open-problems")
def open_problems_group() -> None:
    """Standing list of open research questions any Fellow may take on."""


@open_problems_group.command("list")
def open_problems_list() -> None:
    """Show every open problem on the standing list."""
    from institute import open_problems as op

    problems = op.load_all()
    if not problems:
        console.print(
            "[dim]No open problems on the list. Use `institute open-problems add` to add one.[/dim]"
        )
        return
    for p in problems:
        color = "green" if p.status == "open" else "dim"
        tag_str = f" [{', '.join(p.tags)}]" if p.tags else ""
        console.print(f"[{color}]{p.slug}[/{color}] — {p.title}{tag_str}")
        console.print(f"  [dim]status:[/dim] {p.status}   [dim]opened:[/dim] {p.opened_at}")
        if p.status == "resolved" and p.resolved_by_project:
            console.print(
                f"  [dim]resolved by[/dim] {p.resolved_by_project} "
                f"([dim]{p.resolved_by_fellow}[/dim])"
            )


@open_problems_group.command("show")
@click.argument("slug")
def open_problems_show(slug: str) -> None:
    """Print one problem's full text."""
    from institute import open_problems as op

    p = op.get(slug)
    if p is None:
        console.print(f"[red]No such open problem: `{slug}`.[/red]")
        sys.exit(1)
    console.print(f"[bold]{p.title}[/bold]   [dim]({p.slug})[/dim]")
    console.print(f"[dim]status:[/dim] {p.status}")
    console.print(f"[dim]opened:[/dim] {p.opened_at} by {p.opened_by}")
    if p.tags:
        console.print(f"[dim]tags:[/dim] {', '.join(p.tags)}")
    if p.status == "resolved":
        console.print(
            f"[dim]resolved:[/dim] {p.resolved_at} by "
            f"{p.resolved_by_fellow} via project {p.resolved_by_project}"
        )
    console.print()
    console.print(p.body)


@open_problems_group.command("add")
@click.option("--title", required=True, help="Short problem title.")
@click.option(
    "--body",
    default=None,
    help=(
        "Problem body markdown. If omitted, reads from stdin so you can "
        "paste a multi-line problem statement and end with Ctrl-D."
    ),
)
@click.option(
    "--tag",
    "tags",
    multiple=True,
    help="Tag for filtering / clustering. Repeatable.",
)
@click.option(
    "--opened-by",
    default="founder",
    show_default=True,
    help="Who's adding this problem.",
)
def open_problems_add(title: str, body: str | None, tags: tuple[str, ...], opened_by: str) -> None:
    """Add a new open problem to the standing list."""
    from institute import open_problems as op

    if body is None:
        console.print("[dim]Reading body from stdin. Ctrl-D to finish.[/dim]")
        body = sys.stdin.read()
    if not body.strip():
        console.print("[red]Body is required.[/red]")
        sys.exit(1)
    try:
        problem = op.add(title=title, body=body, tags=list(tags), opened_by=opened_by)
    except ValueError as exc:
        console.print(f"[red]{exc}[/red]")
        sys.exit(1)
    console.print(f"[green]Added:[/green] {problem.slug}")
    console.print(f"  path: {problem.path.relative_to(paths.ROOT)}")


@open_problems_group.command("resolve")
@click.argument("slug")
@click.option(
    "--project",
    "project_id",
    required=True,
    help="Project id that resolved the problem.",
)
@click.option(
    "--fellow",
    "fellow_id",
    required=True,
    help="Lead Fellow id on the resolving project.",
)
def open_problems_resolve(slug: str, project_id: str, fellow_id: str) -> None:
    """Mark a problem resolved by a specific project + lead Fellow."""
    from institute import open_problems as op

    try:
        problem = op.resolve(slug, project_id=project_id, fellow_id=fellow_id)
    except ValueError as exc:
        console.print(f"[red]{exc}[/red]")
        sys.exit(1)
    console.print(f"[green]Resolved:[/green] {problem.slug} via {project_id} (lead: {fellow_id})")


@main.group()
def schedule() -> None:
    """Schedule autopilot via launchd (macOS)."""


@schedule.command("install")
@click.option(
    "--interval-hours",
    type=int,
    default=12,
    show_default=True,
    help="Hours between wake-ups.",
)
@click.option(
    "--max-budget-usd",
    type=float,
    default=10.0,
    show_default=True,
    callback=_non_negative_usd,
    help="Per-wake-up USD cap, passed to `institute autopilot`.",
)
@click.option(
    "--max-steps",
    type=int,
    default=30,
    show_default=True,
    help="Per-wake-up step cap, passed to `institute autopilot`.",
)
@click.option(
    "--daily-budget-usd",
    type=float,
    default=0.0,
    show_default=True,
    callback=_non_negative_usd,
    help=(
        "Daily USD cap (UTC). 0 = disabled. Crossing 80%% triggers soft "
        "austerity; crossing 100%% halts the day."
    ),
)
@click.option(
    "--auto-push/--no-auto-push",
    default=False,
    show_default=True,
    help="If a new publication was produced, commit + push to origin/main.",
)
def schedule_install(
    interval_hours: int,
    max_budget_usd: float,
    max_steps: int,
    daily_budget_usd: float,
    auto_push: bool,
) -> None:
    """Install and load the launchd agent."""
    from institute import schedule as schedule_mod

    path = schedule_mod.install(
        interval_hours=interval_hours,
        max_budget_usd=max_budget_usd,
        max_steps=max_steps,
        auto_push=auto_push,
        daily_budget_usd=daily_budget_usd,
    )
    console.print(f"[green]Installed:[/green] {path}")
    daily_msg = f", daily ${daily_budget_usd:.2f}" if daily_budget_usd > 0 else ", no daily cap"
    console.print(
        f"  every {interval_hours}h, budget ${max_budget_usd:.2f}, "
        f"max-steps {max_steps}{daily_msg}, "
        f"auto-push={'on' if auto_push else 'off'}"
    )
    console.print(f"  logs: {schedule_mod.LOG_DIR}")


@schedule.command("uninstall")
def schedule_uninstall() -> None:
    """Unload and remove the launchd agent."""
    from institute import schedule as schedule_mod

    removed = schedule_mod.uninstall()
    if removed:
        console.print("[green]Uninstalled.[/green]")
    else:
        console.print("[dim]Nothing to uninstall.[/dim]")


@schedule.command("status")
def schedule_status() -> None:
    """Show whether the agent is installed and loaded, plus recent log tail."""
    from institute import schedule as schedule_mod

    info = schedule_mod.status()
    state = "[green]loaded[/green]" if info["loaded"] else "[yellow]not loaded[/yellow]"
    installed = "[green]installed[/green]" if info["installed"] else "[dim]not installed[/dim]"
    console.print(f"Label:    {info['label']}")
    console.print(f"State:    {installed}, {state}")
    if info["interval_hours"] is not None:
        console.print(f"Interval: every {info['interval_hours']}h")
    console.print(f"Plist:    {info['plist_path']}")
    console.print(f"Log:      {info['log_path']}")
    if info["last_log_mtime"]:
        console.print(f"Last:     {info['last_log_mtime']}")
    if info["log_tail"]:
        console.print()
        console.rule("recent log", align="left", style="dim")
        console.print(info["log_tail"])


# ---------------------------------------------------------------------------
# autopilot: self-driving wake-up. Propose if idle, else advance.
# ---------------------------------------------------------------------------


@main.command()
@click.option(
    "--max-budget-usd",
    type=float,
    default=10.0,
    show_default=True,
    callback=_non_negative_usd,
    help="Hard cap on cumulative Claude API cost for this wake-up.",
)
@click.option(
    "--max-steps",
    type=int,
    default=30,
    show_default=True,
    help="Maximum number of single-step dispatches before halting.",
)
@click.option(
    "--daily-budget-usd",
    type=float,
    default=0.0,
    show_default=True,
    callback=_non_negative_usd,
    help=(
        "Charter-defined daily cap on cumulative Claude API cost (UTC). "
        "0 = disabled. Crossing 80%% triggers soft austerity (skip "
        "curriculum/propose/admit, advance in-flight only); crossing "
        "100%% halts the wake-up. Resets at UTC midnight."
    ),
)
@click.option(
    "--start-new-if-idle/--no-start-new-if-idle",
    default=True,
    show_default=True,
    help="If there is nothing in-flight, propose a new project.",
)
def autopilot(
    max_budget_usd: float,
    max_steps: int,
    daily_budget_usd: float,
    start_new_if_idle: bool,
) -> None:
    """Self-driving wake-up. Designed to be invoked by `launchd` or cron.

    Behavior:
      1. If a project is in-flight: advance the most-stale one until
         budget or step cap is hit (same as `institute run`).
      2. If nothing is in-flight and `--start-new-if-idle` is set: ask
         a Fellow to propose a new project, then advance one step.
      3. If the daily cap is configured and spend has crossed the soft
         threshold (80% by default), routine work is paused and only
         in-flight peer review/revise/publish continues. If spend has
         crossed the hard cap, the wake-up exits without doing anything.

    Acquires a single-instance lockfile so concurrent invocations (one
    manual, one scheduled) cannot race. Honors the kill switch like
    every other command, and the cost cap applies to the whole wake-up.
    """
    with _advance_lock():
        _autopilot_locked(
            max_budget_usd=max_budget_usd,
            max_steps=max_steps,
            daily_budget_usd=daily_budget_usd,
            start_new_if_idle=start_new_if_idle,
        )


def _autopilot_locked(
    *,
    max_budget_usd: float,
    max_steps: int,
    daily_budget_usd: float,
    start_new_if_idle: bool,
) -> None:
    """The actual autopilot body, called while holding the lock."""
    _check_kill_switch()

    from institute import budget

    austerity = budget.current_status(daily_budget_usd)
    if not austerity.disabled:
        console.print(f"[dim]{austerity.headline()}[/dim]")

    if austerity.level == "hard":
        _engage_austerity_if_new(austerity)
        console.print(
            f"[red]Daily budget cap of ${austerity.hard_cap_usd:.2f} reached "
            f"(${austerity.today_usd:.2f} spent). Halting until UTC midnight.[/red]"
        )
        return

    in_soft_austerity = austerity.level == "soft"
    if in_soft_austerity:
        _engage_austerity_if_new(austerity)
        console.print(
            "[yellow]Soft austerity: pausing curriculum, propose, admit. "
            "Only in-flight projects will advance this wake-up.[/yellow]"
        )

    if not in_soft_austerity:
        # Apprenticeship cadence: if any Postulant has incomplete curriculum,
        # advance one curriculum item before doing anything else. This makes
        # autopilot pace the Postulant's training without Founder prompting,
        # one item per wake-up.
        _advance_one_curriculum_item()

        # Once curriculum is complete, the qualifying project is the next
        # apprenticeship step. Auto-start one for any Postulant who has
        # finished reading and does not yet have a qualifying project in
        # flight. The project then advances through the normal pipeline.
        _maybe_start_qualifying_project()

        # Periodically consider admitting a new Fellow. Only fires once a
        # Senior Fellow panel exists; until then the Founder runs admit
        # manually.
        _maybe_trigger_admissions()

        if start_new_if_idle:
            with db.connection() as conn:
                in_flight = conn.execute(
                    "SELECT COUNT(*) FROM projects WHERE state NOT IN ('published', 'rejected')"
                ).fetchone()[0]
            if in_flight == 0:
                console.print("[dim]Idle. Proposing a new project...[/dim]")
                from institute.workflows import propose as propose_workflow

                propose_workflow.run(lead=None, topic=None)

    _advance_loop(
        max_budget_usd=max_budget_usd,
        max_steps=max_steps,
        project=None,
        daily_budget_usd=daily_budget_usd,
    )


def _advance_one_curriculum_item() -> None:
    """If any Postulant has unfinished curriculum, advance one item.

    Walks postulants in oldest-curriculum-first order. The earliest
    Postulant whose curriculum is staged but not complete gets one item
    advanced. At most one item per autopilot wake-up so a single
    Postulant cannot monopolize the institution's compute.
    """
    with db.connection() as conn:
        rows = list(
            conn.execute(
                """
                SELECT f.id
                FROM fellows f
                LEFT JOIN curriculum_responses r ON r.fellow_id = f.id
                WHERE f.rank = 'postulant'
                  AND f.retired_at IS NULL
                  AND f.curriculum_designed_at IS NOT NULL
                  AND f.curriculum_completed_at IS NULL
                GROUP BY f.id
                ORDER BY MAX(r.submitted_at) ASC,
                         f.curriculum_designed_at ASC
                """
            )
        )
    if not rows:
        return

    from institute.workflows import curriculum_response

    for r in rows:
        # The response workflow itself checks for the next pending item
        # and returns "all-done" if every item already has a response.
        result = curriculum_response.run(r["id"])
        if result == "completed":
            return  # advanced one item this wake-up; stop.
        # "all-done" or "skipped": try the next Postulant.


def _maybe_start_qualifying_project() -> None:
    """If any Postulant has finished curriculum but has no qualifying project, start one.

    Walks postulants in the order they completed curriculum. At most
    one qualifying project is started per wake-up.
    """
    with db.connection() as conn:
        rows = list(
            conn.execute(
                "SELECT f.id FROM fellows f "
                "WHERE f.rank = 'postulant' "
                "AND f.retired_at IS NULL "
                "AND f.curriculum_completed_at IS NOT NULL "
                "AND NOT EXISTS ("
                "  SELECT 1 FROM projects p "
                "  WHERE p.lead_fellow_id = f.id AND p.kind = 'qualifying'"
                ") "
                "ORDER BY f.curriculum_completed_at ASC LIMIT 1"
            )
        )
    if not rows:
        return

    fellow_id = rows[0]["id"]
    console.print(
        f"[dim]Postulant `{fellow_id}` has completed curriculum and "
        "no qualifying project yet. Starting one...[/dim]"
    )
    from institute.workflows import qualify as qualify_workflow

    try:
        qualify_workflow.run(fellow_id)
    except SystemExit as exc:
        # qualify.run raises SystemExit for preconditions that should
        # only fail in race conditions (e.g., manual concurrent run).
        # Log and continue; the main loop is unaffected.
        console.print(f"[yellow]qualify failed for {fellow_id}: {exc}[/yellow]")


# Number of publications between auto-triggered admissions reviews.
# Higher than the promotion cadence because admissions is a larger
# commitment: a new Postulant + advisor pairing + curriculum + a
# qualifying project on the queue.
_ADMISSIONS_CADENCE_PUBLICATIONS = 5


def _maybe_trigger_admissions() -> None:
    """If conditions are right, ask the Admissions Committee for a new Postulant.

    Two conditions must hold:
      1. At least one Senior Fellow exists to form the committee.
      2. At least `_ADMISSIONS_CADENCE_PUBLICATIONS` publications have
         landed since the most recent admission decision (or ever, if
         no prior admissions).

    Fires once per wake-up at most. The admit workflow runs with
    `auto=True` so it never blocks on stdin.
    """
    with db.connection() as conn:
        seniors = conn.execute(
            "SELECT COUNT(*) FROM fellows WHERE rank = 'senior_fellow' AND retired_at IS NULL"
        ).fetchone()[0]
        if seniors == 0:
            return
        last_admission_at = conn.execute(
            "SELECT MAX(at) FROM audit_log WHERE action = 'admission'"
        ).fetchone()[0]
        pubs_since = conn.execute(
            "SELECT COUNT(*) FROM projects WHERE state = 'published' AND updated_at > ?",
            (last_admission_at or "",),
        ).fetchone()[0]
    if pubs_since < _ADMISSIONS_CADENCE_PUBLICATIONS:
        return

    console.rule(
        f"[bold]Admissions review: {pubs_since} publication(s) since last admit[/bold]",
        align="left",
        style="dim",
    )
    from institute.workflows import admit as admit_workflow

    try:
        admit_workflow.run(auto=True)
    except Exception as exc:  # pragma: no cover - best-effort path
        console.print(f"[yellow]admit auto-trigger failed: {exc}[/yellow]")
