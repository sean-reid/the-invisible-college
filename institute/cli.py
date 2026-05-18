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
# admit: vet a new Fellow into the College
# ---------------------------------------------------------------------------


@main.command()
@click.option(
    "--hint",
    type=str,
    default=None,
    help="Optional Founder guidance for the new admission (e.g. a missing specialty).",
)
def admit(hint: str | None) -> None:
    """Vet and admit a new Fellow.

    The orchestrator proposes a candidate genome that complements the
    current cohort. The Founder reviews the genome; if accepted, the
    candidate writes responses to the qualifying problem set, the
    orchestrator evaluates them, and the Founder makes the final
    admission decision. All artifacts are preserved in
    archive/admissions/<candidate-id>/.
    """
    _check_kill_switch()
    from institute.workflows import admit as admit_workflow

    admit_workflow.run(founder_hint=hint)


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
    "awaiting_advisor_review": "advisor_review",
    "peer_reviewing": "peer_review",
    "revising": "revise",
    "andon_review": "andon_review",
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
    elif workflow_name == "andon_review":
        from institute.workflows import andon_review as wf
    elif workflow_name == "advisor_review":
        from institute.workflows import advisor_review as wf
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
    _advance_loop(max_budget_usd=max_budget_usd, max_steps=max_steps, project=project)


def _advance_loop(*, max_budget_usd: float, max_steps: int, project: str | None) -> None:
    """The actual step loop. Shared by `institute run` and `institute autopilot`."""
    baseline_cost = _audit_cost_total()

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
            run_cost = _audit_cost_total() - baseline_cost
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


# ---------------------------------------------------------------------------
# schedule: manage the launchd plist that wakes autopilot on a cadence
# ---------------------------------------------------------------------------


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
    "--auto-push/--no-auto-push",
    default=False,
    show_default=True,
    help="If a new publication was produced, commit + push to origin/main.",
)
def schedule_install(
    interval_hours: int, max_budget_usd: float, max_steps: int, auto_push: bool
) -> None:
    """Install and load the launchd agent."""
    from institute import schedule as schedule_mod

    path = schedule_mod.install(
        interval_hours=interval_hours,
        max_budget_usd=max_budget_usd,
        max_steps=max_steps,
        auto_push=auto_push,
    )
    console.print(f"[green]Installed:[/green] {path}")
    console.print(
        f"  every {interval_hours}h, budget ${max_budget_usd:.2f}, "
        f"max-steps {max_steps}, auto-push={'on' if auto_push else 'off'}"
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
    "--start-new-if-idle/--no-start-new-if-idle",
    default=True,
    show_default=True,
    help="If there is nothing in-flight, propose a new project.",
)
def autopilot(max_budget_usd: float, max_steps: int, start_new_if_idle: bool) -> None:
    """Self-driving wake-up. Designed to be invoked by `launchd` or cron.

    Behavior:
      1. If a project is in-flight: advance the most-stale one until
         budget or step cap is hit (same as `institute run`).
      2. If nothing is in-flight and `--start-new-if-idle` is set: ask
         a Fellow to propose a new project, then advance one step.

    Acquires a single-instance lockfile so concurrent invocations (one
    manual, one scheduled) cannot race. Honors the kill switch like
    every other command, and the cost cap applies to the whole wake-up.
    """
    import fcntl

    lock_path = paths.ROOT / ".autopilot.lock"
    lock_path.touch(exist_ok=True)
    with lock_path.open("w") as lock_fh:
        try:
            fcntl.flock(lock_fh.fileno(), fcntl.LOCK_EX | fcntl.LOCK_NB)
        except BlockingIOError:
            console.print(
                "[yellow]Another autopilot wake-up is already running. "
                "Skipping this invocation.[/yellow]"
            )
            sys.exit(0)
        _autopilot_locked(max_budget_usd, max_steps, start_new_if_idle)


def _autopilot_locked(max_budget_usd: float, max_steps: int, start_new_if_idle: bool) -> None:
    """The actual autopilot body, called while holding the lock."""
    _check_kill_switch()

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

    _advance_loop(max_budget_usd=max_budget_usd, max_steps=max_steps, project=None)


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
                "SELECT id FROM fellows "
                "WHERE rank = 'postulant' "
                "AND retired_at IS NULL "
                "AND curriculum_designed_at IS NOT NULL "
                "AND curriculum_completed_at IS NULL "
                "ORDER BY curriculum_designed_at ASC"
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
