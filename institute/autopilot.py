"""Autopilot loop and its helpers, extracted from ``institute.cli``.

This module owns the step-by-step advance loop that ``institute run``
and ``institute autopilot`` share, plus the pre-loop and post-step
"maybe" helpers (curriculum advance, qualifying-project start,
admissions, reading group, editorial preprint, promotion review). The
CLI module re-exports the names it used to expose so existing tests and
external callers continue to work without change.
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
from pathlib import Path

from rich.console import Console

from institute import claude_runner, db, paths

console = Console()


def _now() -> str:
    return datetime.now(UTC).isoformat(timespec="seconds")


def _check_kill_switch() -> None:
    """Delegate to runtime.check_kill_switch so claude_runner and the CLI
    use the same guard. Kept as a thin alias so existing call sites
    remain unchanged."""
    from institute import runtime

    runtime.check_kill_switch()


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


def _guarded(label: str, fn) -> None:
    """Run a pre-loop autopilot helper, swallowing Fellow CLI failures.

    The pre-loop helpers (curriculum advance, qualifying-project
    start, admit, idle-propose) each invoke Claude at least once.
    Without a guard, a transient CLI failure on any of them kills the
    whole wake-up before the step loop even gets a chance to run.
    This helper catches the failure, records it as a `step_failure`
    decision (project_id is None since these helpers are not bound
    to a single project), and returns so the wake-up continues.
    """
    try:
        fn()
    except claude_runner.FellowInvocationError as exc:
        console.print(
            f"[yellow]Autopilot helper `{label}` failed: Fellow "
            f"{exc.fellow_id} ({exc.step}) returned "
            f"returncode={exc.returncode}. Skipping this helper for "
            "this cycle; the next cycle will retry.[/yellow]"
        )
        _record_step_failure(
            project_id=exc.project_id or label,
            state=label,
            fellow_id=exc.fellow_id,
            step=exc.step,
            returncode=exc.returncode,
            stderr=exc.stderr,
        )
    except Exception as exc:
        console.print(
            f"[yellow]Autopilot helper `{label}` failed: "
            f"{type(exc).__name__}: {exc}. Skipping this helper for "
            "this cycle.[/yellow]"
        )
        _record_step_failure(
            project_id=label,
            state=label,
            fellow_id="orchestrator",
            step=label,
            returncode=1,
            stderr=f"{type(exc).__name__}: {exc}",
        )


def _record_step_failure(
    *,
    project_id: str | None,
    state: str,
    fellow_id: str,
    step: str,
    returncode: int,
    stderr: str,
) -> None:
    """Record a transient Fellow invocation failure as an institutional
    decision. The daemon retries on the next cycle; this row exists so
    the record shows the attempt rather than silently skipping it.

    `project_id` is None for pre-loop helper failures (curriculum
    advance, idle-propose, etc.) that are not bound to a specific
    project. For step-loop failures it's the project_id."""
    from datetime import UTC, datetime

    from institute import decisions

    now = datetime.now(UTC).isoformat(timespec="seconds")
    where = f"project `{project_id}` (state: `{state}`)" if project_id else f"phase `{state}`"
    body_lines = [
        f"**Where:** {where}",
        f"**Fellow:** `{fellow_id}`",
        f"**Step:** `{step}`",
        f"**Returncode:** {returncode}",
        f"**Recorded:** {now}",
        "",
        (
            "The Fellow's Claude invocation returned non-zero. The "
            "autopilot caught the failure, recorded this row, and "
            "moved on. The next cycle will retry the same step. No "
            "project state was changed."
        ),
    ]
    if stderr:
        body_lines.extend(["", "## stderr (truncated)", "", "```", stderr, "```"])
    title_suffix = f" on {project_id}" if project_id else f" ({state})"
    decision = decisions.Decision(
        kind="step_failure",
        title=f"Step failure: {fellow_id}{title_suffix}",
        body="\n".join(body_lines),
        actors=["orchestrator", fellow_id],
        related_project=project_id,
    )
    try:
        with db.connection() as conn, db.transaction(conn):
            decisions.record(conn, decision)
    except Exception:  # pragma: no cover - best-effort
        # Never let the audit write itself crash the loop.
        pass


def _pick_in_flight_project(
    project: str | None,
    *,
    exclude_ids: set[str] | None = None,
) -> sqlite3.Row | None:
    """Return the row to advance next, or None if there is nothing to do.

    `exclude_ids` lets the autopilot loop skip projects that already
    failed earlier in the same cycle, so a transient Claude error on
    one project does not pin the loop to the same project until budget
    exhaustion.
    """
    from institute.state import TERMINAL_STATE_VALUES

    placeholders = ",".join("?" * len(TERMINAL_STATE_VALUES))
    exclude_ids = exclude_ids or set()
    with db.connection() as conn:
        if project is not None:
            if project in exclude_ids:
                return None
            return conn.execute(
                "SELECT id, state FROM projects WHERE id = ?", (project,)
            ).fetchone()
        if exclude_ids:
            exclude_placeholders = ",".join("?" * len(exclude_ids))
            return conn.execute(
                f"SELECT id, state FROM projects "
                f"WHERE state NOT IN ({placeholders}) "
                f"  AND id NOT IN ({exclude_placeholders}) "
                f"ORDER BY updated_at ASC LIMIT 1",
                (*TERMINAL_STATE_VALUES, *exclude_ids),
            ).fetchone()
        return conn.execute(
            f"SELECT id, state FROM projects "
            f"WHERE state NOT IN ({placeholders}) "
            f"ORDER BY updated_at ASC LIMIT 1",
            TERMINAL_STATE_VALUES,
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
    try:
        candidate = _pick_review_candidate(cohort, mode)
    except ValueError:
        # All active Fellows are Senior Fellows, so no one is on the
        # calendar review cadence. Senior Fellows are reviewed only
        # via the peer-sponsored concern-review path.
        return
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
    """Pick a Fellow to review under the requested selection mode.

    Senior Fellows are excluded from the calendar-triggered candidate
    pool. Senior Fellow is a terminal, indefinite rank; periodically
    re-evaluating it would subvert the academic-freedom logic that
    makes it indefinite in the first place. Concern about a specific
    Senior Fellow's standing routes through the peer-sponsored
    concern-review path (`institute promote --fellow X --concern-grounds
    ...`), not through the calendar.
    """
    cohort = [
        rep
        for rep in cohort
        if getattr(rep, "rank", None) != "senior_fellow"  # type: ignore[attr-defined]
    ]
    if not cohort:
        # Nothing to do this cycle. Callers tolerate ValueError below
        # via the cohort emptiness check upstream; if every active
        # Fellow is a Senior Fellow we simply do not auto-review.
        raise ValueError("no calendar-eligible candidates")
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

    # Projects whose step raised a FellowInvocationError this cycle.
    # The loop excludes them from `_pick_in_flight_project` so a
    # transient Claude failure on one project doesn't pin the loop to
    # the same project until the budget runs out.
    failed_this_cycle: set[str] = set()

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

            row = _pick_in_flight_project(project, exclude_ids=failed_this_cycle)
            if row is None:
                if project is not None:
                    if project in failed_this_cycle:
                        console.print(
                            f"[yellow]Project {project} failed earlier this "
                            "cycle; halting.[/yellow]"
                        )
                        return
                    console.print(f"[red]No such project: {project}[/red]")
                    sys.exit(1)
                if failed_this_cycle:
                    console.print(
                        f"[yellow]No in-flight projects remaining "
                        f"({len(failed_this_cycle)} skipped due to earlier "
                        "failures this cycle). Done.[/yellow]"
                    )
                else:
                    console.print("[dim]No in-flight projects. Done.[/dim]")
                return
            if row["state"] in ("published", "rejected"):
                console.print(f"[green]Project {row['id']} is {row['state']}. Done.[/green]")
                return

            console.rule(f"[bold]Step {step}[/bold]", align="left", style="dim")
            start = time.monotonic()
            prev_state = row["state"]
            try:
                _dispatch_step(row["id"], row["state"])
            except claude_runner.FellowInvocationError as exc:
                # Transient Claude CLI failure on a single Fellow
                # invocation. Don't crash the cycle - record the
                # failure, mark the project as failed-this-cycle so
                # the loop doesn't immediately re-pick it, and
                # continue to other in-flight work.
                console.print(
                    f"[yellow]Step on {row['id']} failed: Fellow "
                    f"{exc.fellow_id} ({exc.step}) returned "
                    f"returncode={exc.returncode}. Skipping for this "
                    "cycle; the next cycle will retry.[/yellow]"
                )
                _record_step_failure(
                    project_id=row["id"],
                    state=row["state"],
                    fellow_id=exc.fellow_id,
                    step=exc.step,
                    returncode=exc.returncode,
                    stderr=exc.stderr,
                )
                failed_this_cycle.add(row["id"])
                continue
            except Exception as exc:
                # Catch-all for workflow-level failures (e.g. publish
                # citation lint, parsing errors, malformed JSON). The
                # cycle keeps going; the project is skipped for the
                # rest of this cycle and the next cycle retries unless
                # the operator intervenes. Genuine code bugs surface
                # as the recorded decision; the operator decides
                # whether to fix the code or revise the draft.
                console.print(
                    f"[yellow]Step on {row['id']} failed: "
                    f"{type(exc).__name__}: {exc}. Skipping for this "
                    "cycle; the next cycle will retry.[/yellow]"
                )
                _record_step_failure(
                    project_id=row["id"],
                    state=row["state"],
                    fellow_id="orchestrator",
                    step=row["state"],
                    returncode=1,
                    stderr=f"{type(exc).__name__}: {exc}",
                )
                failed_this_cycle.add(row["id"])
                continue
            elapsed = time.monotonic() - start
            run_cost = audit_cost.delta()
            console.print(
                f"  [dim]elapsed: {elapsed:.0f}s  ·  "
                f"run cost: ${run_cost:.2f} of ${max_budget_usd:.2f}[/dim]"
            )

            # The promotion-review hook also invokes Claude (panel
            # votes), so a transient failure here would kill the loop.
            # Guard it the same way as the pre-loop helpers.
            _guarded(
                "promotion-review",
                lambda row_id=row["id"], prev=prev_state: _maybe_trigger_promotion_review(
                    row_id, prev
                ),
            )

            # Editorial-checkpoint preprint: when a project transitions
            # into EDITORIAL for the first time, the lead posts a
            # preprint snapshot of the work, and one non-author Fellow
            # files an auto-comment. Costs 2 Claude calls per
            # publication, deliberately bounded.
            _guarded(
                "editorial-preprint",
                lambda row_id=row["id"], prev=prev_state: _maybe_post_editorial_preprint(
                    row_id, prev
                ),
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


def _autopilot_locked(
    *,
    max_budget_usd: float,
    max_steps: int,
    daily_budget_usd: float,
    start_new_if_idle: bool,
) -> None:
    """The actual autopilot body, called while holding the lock."""
    _check_kill_switch()

    # Garbage-collect workspaces of terminal projects. Cheap (DB read +
    # directory enumeration), worth doing once per wake-up so disk
    # doesn't accumulate without bound. Per-project workspaces have
    # held a half-gigabyte+ historically when this was unwired.
    try:
        from institute import workspaces as _ws

        removed = _ws.gc_terminal_projects()
        if removed:
            console.print(f"[dim]Reclaimed {removed} terminal-project workspace(s).[/dim]")
    except Exception as exc:  # pragma: no cover - best-effort cleanup
        console.print(f"[dim]Workspace GC skipped: {exc}[/dim]")

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
        _guarded("curriculum", _advance_one_curriculum_item)

        # Once curriculum is complete, the qualifying project is the next
        # apprenticeship step. Auto-start one for any Postulant who has
        # finished reading and does not yet have a qualifying project in
        # flight. The project then advances through the normal pipeline.
        _guarded("qualifying-start", _maybe_start_qualifying_project)

        # Periodically consider admitting a new Fellow. Only fires once a
        # Senior Fellow panel exists; until then the Founder runs admit
        # manually.
        _guarded("admit", _maybe_trigger_admissions)

        # Periodic reading group: a rotating convener proposes a text
        # (a College publication not their own) and a 3-Fellow group
        # cross-reads it. Cadence is roughly one session per
        # _READING_GROUP_CADENCE_PUBLICATIONS publications.
        _guarded("reading-group", _maybe_convene_reading_group)

        if start_new_if_idle:
            from institute.state import TERMINAL_STATE_VALUES

            placeholders = ",".join("?" * len(TERMINAL_STATE_VALUES))
            with db.connection() as conn:
                in_flight = conn.execute(
                    f"SELECT COUNT(*) FROM projects WHERE state NOT IN ({placeholders})",
                    TERMINAL_STATE_VALUES,
                ).fetchone()[0]
            if in_flight == 0:
                console.print("[dim]Idle. Proposing a new project...[/dim]")
                from institute.workflows import propose as propose_workflow

                _guarded("propose", lambda: propose_workflow.run(lead=None, topic=None))

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


# Reading groups are cadenced against publications rather than calendar
# time. Roughly one session for every N publications keeps reading
# tied to active institutional output. With the cohort currently
# producing roughly one paper per day, 7 publications ≈ a weekly session.
_READING_GROUP_CADENCE_PUBLICATIONS = 7


def _maybe_convene_reading_group() -> None:
    """If enough publications have landed since the last reading group,
    convene a new session with a rotating convener.

    Cadence: at least _READING_GROUP_CADENCE_PUBLICATIONS publications
    must have shipped since the most recent `reading_group` audit row
    (or since institution genesis, if none).
    """
    from institute.workflows import reading_group as reading_group_workflow

    with db.connection() as conn:
        last_session_at = conn.execute(
            "SELECT MAX(at) FROM audit_log WHERE action = 'reading_group'"
        ).fetchone()[0]
        pubs_since = conn.execute(
            "SELECT COUNT(*) FROM projects WHERE state = 'published' AND updated_at > ?",
            (last_session_at or "",),
        ).fetchone()[0]
    if pubs_since < _READING_GROUP_CADENCE_PUBLICATIONS:
        return

    console.rule(
        f"[bold]Reading group: {pubs_since} publication(s) since last session[/bold]",
        align="left",
        style="dim",
    )
    reading_group_workflow.convene_with_rotating_leader()


def _maybe_post_editorial_preprint(project_id: str, prev_state: str) -> None:
    """If a project just transitioned into EDITORIAL for the first
    time, post a preprint snapshot. Public checkpoint of the work
    right before formal publication.

    Skipped if a preprint is already on file for this project.
    """
    if prev_state == "editorial":
        return  # not a transition; ignore
    with db.connection() as conn:
        row = conn.execute("SELECT state FROM projects WHERE id = ?", (project_id,)).fetchone()
    if row is None or row["state"] != "editorial":
        return

    # Skip if a preprint already exists for this project.
    preprint_dir = paths.PREPRINTS / project_id
    if preprint_dir.is_dir() and any(
        f.name.startswith("v") and f.name.endswith(".md") for f in preprint_dir.iterdir()
    ):
        return

    from institute.workflows import preprint as preprint_workflow

    console.print(f"[dim]Posting editorial-checkpoint preprint for `{project_id}`...[/dim]")
    version_path = preprint_workflow.post(project_id)

    # Auto-comment: pick one non-author Fellow (least-recently-commented)
    # and have them file a single reaction. Cheap institutional signal.
    _maybe_auto_comment_on_preprint(project_id, version_path)


def _maybe_auto_comment_on_preprint(project_id: str, version_path: Path) -> None:
    """Pick one eligible Fellow and have them file a comment on the
    just-posted preprint version. Best-effort: failures are swallowed
    so a comment hiccup doesn't drag down the publish cycle."""
    import re

    m = re.match(r"v(\d+)\.md$", version_path.name)
    if not m:
        return
    version = int(m.group(1))

    with db.connection() as conn:
        proj = conn.execute(
            "SELECT lead_fellow_id FROM projects WHERE id = ?", (project_id,)
        ).fetchone()
        if proj is None:
            return
        lead_id = proj["lead_fellow_id"]

        # Pick: least-recently-commented active Fellow other than the lead.
        rows = list(
            conn.execute(
                "SELECT id FROM fellows WHERE retired_at IS NULL AND id != ?",
                (lead_id,),
            )
        )
        if not rows:
            return
        last_comment_at: dict[str, str] = {}
        for r in conn.execute(
            "SELECT at, actor FROM audit_log WHERE action = 'preprint_comment' ORDER BY at ASC"
        ):
            for actor in r["actor"].split(","):
                actor = actor.strip()
                if actor and actor != "orchestrator":
                    last_comment_at[actor] = r["at"]

        def sort_key(fellow_id: str) -> tuple[int, str]:
            if fellow_id not in last_comment_at:
                return (0, "")
            return (1, last_comment_at[fellow_id])

        eligible = sorted([r["id"] for r in rows], key=sort_key)
        commenter_id = eligible[0]

    try:
        from institute.workflows import preprint as preprint_workflow

        preprint_workflow.comment(project_id, commenter_id=commenter_id, version=version)
    except Exception as exc:
        console.print(f"[yellow]Auto-comment skipped: {exc}[/yellow]")


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
