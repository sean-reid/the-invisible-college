"""Qualifying-project panel (Chapter 5).

After the advisor signals `ready`, the qualifying project still
needs two more votes before it goes to peer review: one Fellow from
the candidate's own department (peer perspective inside the
discipline) and one Fellow from outside (whether the work is
intelligible to someone with no special preparation).

The panel produces:
  * a brief per evaluator (a short, structured read — not a full
    peer review), and
  * an aggregate decision.

Aggregation rule:
  * majority `ready` (advisor + at least one of two extras) →
    PEER_REVIEWING
  * otherwise → REVISING

Selection rule for the two extras:
  * Same-department evaluator: any active Fellow other than the
    candidate and the advisor who shares at least one department
    with the candidate.
  * Outside evaluator: any active Fellow other than the candidate
    and the advisor who shares no department with the candidate.

When departments aren't initialized, both extras fall back to a
specialization-string heuristic: same-spec for the inside slot,
different-spec for the outside slot.

The panel saves each evaluator's feedback alongside the advisor's
under `archive/reviews/<project>/`.
"""

from __future__ import annotations

import json
import sqlite3

from rich.console import Console

from institute import (
    claude_runner,
    db,
    decisions,
    departments,
    paths,
    state,
    workspaces,
)
from institute import fellow as fellow_mod
from institute.claude_runner import FellowTask
from institute.fellow import Genome
from institute.state import State

console = Console()


PANEL_BRIEF = """\
You are a panelist on a qualifying-project review. A Postulant
has produced a draft. Their advisor has already given substantive
feedback. Your job is the second or third vote: does this work
warrant peer review by the College, or should the Postulant
revise first?

# Inputs in your workspace

- `draft.md`         the Postulant's draft of the qualifying project
- `proposal.md`      the original proposal
- `postulant.md`     identity card for the Postulant
- `advisor-feedback.md`  the advisor's feedback (for context, not as
                         a binding instruction)
- `role.md`          your role on this panel — same-department or
                     outside-the-discipline

Read the draft carefully. Read the proposal for scope. Read the
advisor's feedback for what they already named. Then form your own
view, which may or may not agree with the advisor's.

# What you must produce

Use the Write tool to create TWO files:

1. `feedback.md` — 200 to 600 words. Targeted. Address ONE or TWO
   things specific to your role:
   * If you are the same-department panelist, focus on
     methodological soundness within the discipline.
   * If you are the outside panelist, focus on whether the work is
     intelligible to a thoughtful reader without your colleague's
     training. The College publishes for that reader.

2. `decision.json`:
   ```
   {{
     "outcome": "<ready|revise>",
     "summary": "<2-3 sentences for the institutional record>"
   }}
   ```

Reply with `Done.` when both files exist.
"""


# The qualifying panel may only request `revise` a bounded number of
# times before it must render a final verdict. After this many prior
# `revise` rounds, the next convening switches to FINAL mode: panelists
# can choose `ready` or `shelve` but not `revise`. The cap mirrors
# real grad-school practice: a committee that has already asked for
# revisions twice gives a definitive third-round verdict rather than
# looping the candidate indefinitely.
MAX_PANEL_REVISE_ROUNDS = 2


# If a qualifying project has been through this many revisions before
# the panel even sees it (e.g., it spent its loops at the advisor
# layer), the panel's first convening is treated as final. The
# institution does not need the panel to ask for yet more revisions
# on work that has already been revised heavily; render a verdict.
MAX_REVISIONS_BEFORE_PANEL_IS_FINAL = 5


PANEL_BRIEF_FINAL = """\
You are serving as a panel evaluator on the qualifying project of a
Postulant of the Invisible College. **This is the final convening of
the qualifying panel for this project.** The panel has already
requested revisions twice and the work has been revised each time.
The College does not permit a third revision request; this round
ends in either acceptance or shelving.

# Inputs in your workspace

- `draft.md`         the Postulant's current draft
- `proposal.md`      the original proposal
- `postulant.md`     identity card for the Postulant
- `advisor-feedback.md`  the advisor's most recent feedback (context)
- `role.md`          your role on this panel — same-department or
                     outside-the-discipline

Read the draft carefully. Read the proposal for scope. Read the
advisor's feedback for what they already named. Then form your own
view.

# What you must produce

Use the Write tool to create TWO files:

1. `feedback.md` — 200 to 600 words. Targeted to your role. State
   plainly whether the work is now ready or whether the project
   should be shelved. The College's purpose is published research,
   not endless development.

2. `decision.json`:
   ```
   {{
     "outcome": "<ready|shelve>",
     "summary": "<2-3 sentences for the institutional record>"
   }}
   ```

The two outcomes:

- `ready`: the work is good enough to advance to peer review. Not
  perfect, but the bar to clear is the same College bar as any other
  publication. Shelving the project because of remediable concerns
  would be the wrong call.
- `shelve`: the qualifying project should be closed without
  publication. The Postulant retains their rank and may propose a
  new qualifying project; this record stands as institutional
  history of what was attempted. Choose this when the work, after
  two prior rounds of revision, is still not clearable.

`revise` is not available on this convening.

Reply with `Done.` when both files exist.
"""


def _pick_panel(
    conn: sqlite3.Connection,
    *,
    candidate_id: str,
    advisor_id: str,
) -> tuple[Genome | None, Genome | None]:
    """Return (same_dept_panelist, outside_panelist).

    Either may be None when the cohort is too small. The caller
    decides how to handle a missing panelist; the conservative
    default is to require both slots to be filled, otherwise treat
    the missing slot as `ready` so the workflow doesn't stall on
    a small cohort.
    """
    candidate_row = conn.execute(
        "SELECT specialization FROM fellows WHERE id = ?", (candidate_id,)
    ).fetchone()
    candidate_spec = (candidate_row["specialization"] or "").strip().lower()

    from institute import sabbaticals

    eligible_ids = [
        r["id"]
        for r in conn.execute(
            "SELECT id FROM fellows "
            "WHERE retired_at IS NULL AND id NOT IN (?, ?) "
            f"AND {sabbaticals.ACTIVE_FILTER} "
            "ORDER BY id",
            (candidate_id, advisor_id, sabbaticals.now_iso()),
        )
    ]
    if not eligible_ids:
        return (None, None)

    use_departments = departments.is_initialized(conn)
    same_dept: str | None = None
    outside: str | None = None
    for fid in eligible_ids:
        if use_departments:
            shares = departments.same_department(conn, fellow_a=candidate_id, fellow_b=fid)
        else:
            row = conn.execute("SELECT specialization FROM fellows WHERE id = ?", (fid,)).fetchone()
            other_spec = (row["specialization"] or "").strip().lower()
            shares = bool(candidate_spec) and other_spec == candidate_spec
        if shares and same_dept is None:
            same_dept = fid
        elif not shares and outside is None:
            outside = fid
        if same_dept and outside:
            break

    same = fellow_mod.load_genome(conn, same_dept) if same_dept else None
    out = fellow_mod.load_genome(conn, outside) if outside else None
    return (same, out)


def _evaluator_brief(role: str) -> str:
    return f"# Role\n\n{role}\n"


def _read_cached_panel_feedback(path) -> tuple[str, str] | None:
    """Parse a previously-written panel feedback file. Returns
    (outcome, summary) if the file exists and matches the writer's
    shape; None otherwise (re-invoke the evaluator).
    """
    import re

    if not path.is_file():
        return None
    try:
        text = path.read_text(encoding="utf-8")
    except OSError:
        return None
    outcome_match = re.search(r"\*\*Outcome:\*\*\s*`(ready|revise|shelve)`", text)
    if not outcome_match:
        return None
    summary_match = re.search(r"## Summary\s*\n+(.+?)(?=\n## |\Z)", text, re.DOTALL)
    summary = summary_match.group(1).strip() if summary_match else ""
    return (outcome_match.group(1), summary)


def count_prior_revise_rounds(conn: sqlite3.Connection, project_id: str) -> int:
    """How many prior qualifying-panel convenings on this project
    ended with the panel routing back to revision rather than
    advancing to peer review or shelving.

    Implementation: every prior qualifying_panel decision on this
    project that did NOT result in advancement counts as one revise
    round. We approximate by counting all prior qualifying_panel
    audit rows. Once a panel says `ready` the project leaves the
    AWAITING_QUALIFYING_PANEL → REVISING → AWAITING_QUALIFYING_PANEL
    loop and never re-enters it (a clean panel decision routes to
    PEER_REVIEWING). So the loop count equals the panel-row count.
    """
    row = conn.execute(
        "SELECT COUNT(*) AS n FROM audit_log WHERE action = 'qualifying_panel' AND project_id = ?",
        (project_id,),
    ).fetchone()
    return int(row["n"]) if row else 0


def _run_evaluator(
    *,
    project_id: str,
    evaluator: Genome,
    role: str,
    draft_md: str,
    proposal_md: str,
    postulant_card: str,
    advisor_feedback_md: str,
    is_final_round: bool,
) -> tuple[str, str, str]:
    """Run one panelist. Returns (outcome, summary, feedback_md).

    `is_final_round=True` switches the brief to FINAL mode: panelists
    must choose `ready` or `shelve`; `revise` is rejected.
    """
    workspace = workspaces.workspace_for(evaluator.id, f"panel-{project_id}-{role}")
    workspaces.stage_input(workspace, "draft.md", draft_md)
    workspaces.stage_input(workspace, "proposal.md", proposal_md)
    workspaces.stage_input(workspace, "postulant.md", postulant_card)
    workspaces.stage_input(workspace, "advisor-feedback.md", advisor_feedback_md)
    workspaces.stage_input(workspace, "role.md", _evaluator_brief(role))
    for stale in ("feedback.md", "decision.json"):
        p = workspace / stale
        if p.exists():
            p.unlink()
    brief = PANEL_BRIEF_FINAL if is_final_round else PANEL_BRIEF
    step_suffix = f"{role}-final" if is_final_round else role
    claude_runner.invoke(
        FellowTask(
            genome=evaluator,
            project_id=project_id,
            step=f"qualifying-panel:{step_suffix}",
            brief=brief,
            workspace=workspace,
            extra_dirs=(paths.DOCS, paths.ARCHIVE),
        )
    )
    feedback_md = workspaces.require_output(workspace, "feedback.md", min_chars=150).strip()
    decision_text = workspaces.require_output(workspace, "decision.json", min_chars=10)
    try:
        decision_payload = json.loads(decision_text)
    except json.JSONDecodeError as exc:
        raise RuntimeError(
            f"panelist {evaluator.id} decision.json is not valid JSON: {decision_text!r}"
        ) from exc
    outcome = str(decision_payload.get("outcome", "")).strip().lower()
    if is_final_round:
        valid = {"ready", "shelve"}
    else:
        valid = {"ready", "revise"}
    if outcome not in valid:
        # A final-round panelist who returns `revise` despite the brief
        # is coerced to `shelve` (the conservative final-round default):
        # the work did not earn a `ready` after two prior revisions and
        # the institution will not loop further. Anything else is a
        # malformed response.
        if is_final_round and outcome == "revise":
            outcome = "shelve"
        else:
            raise RuntimeError(
                f"panelist {evaluator.id} returned unrecognized outcome "
                f"{outcome!r} (valid: {sorted(valid)}, final_round={is_final_round})"
            )
    summary = str(decision_payload.get("summary", "")).strip()
    return outcome, summary, feedback_md


def run(project_id: str) -> None:
    """Run the two extra qualifying-project evaluators after the advisor."""
    with db.connection() as conn:
        proj = conn.execute(
            "SELECT id, title, state, kind, lead_fellow_id, proposal_path, draft_path "
            "FROM projects WHERE id = ?",
            (project_id,),
        ).fetchone()
        if proj is None:
            raise SystemExit(f"No such project: {project_id}")
        if proj["kind"] != "qualifying":
            raise SystemExit(f"Project {project_id} is kind=`{proj['kind']}`, not qualifying.")
        if proj["state"] != State.AWAITING_QUALIFYING_PANEL.value:
            raise SystemExit(
                f"Project {project_id} is in state {proj['state']}, expected "
                "awaiting_qualifying_panel."
            )
        postulant_row = conn.execute(
            "SELECT id, name, model, specialization, advisor_id FROM fellows WHERE id = ?",
            (proj["lead_fellow_id"],),
        ).fetchone()
        if postulant_row is None:
            raise SystemExit(f"Postulant {proj['lead_fellow_id']} not found.")
        same_panel, outside_panel = _pick_panel(
            conn,
            candidate_id=postulant_row["id"],
            advisor_id=postulant_row["advisor_id"],
        )
        advisor_feedback_path = (
            paths.REVIEWS / project_id / f"advisor-{postulant_row['advisor_id']}.md"
        )
        # `prior_revise_rounds` counts panel convenings that ended in
        # `request-revisions`. `prior_revisions` counts every revision
        # ever recorded against this project — advisor- and panel-
        # induced alike. They measure different things deliberately:
        # the first bounds how often THIS reviewer (the panel) sends
        # back for more work, the second catches projects that have
        # been bouncing at the advisor layer with the panel never the
        # cause but every cycle eating real time.
        prior_revise_rounds = count_prior_revise_rounds(conn, project_id)
        prior_revisions = conn.execute(
            "SELECT COUNT(*) AS n FROM audit_log WHERE action = 'revision' AND project_id = ?",
            (project_id,),
        ).fetchone()["n"]

    # Two paths to final-round mode:
    #   - the panel has already requested revisions MAX_PANEL_REVISE_ROUNDS times
    #   - the project has been revised many times already (typically because
    #     the loop was stuck at the advisor layer); the panel needs to render
    #     a verdict rather than asking for more revision.
    is_final_round = (
        prior_revise_rounds >= MAX_PANEL_REVISE_ROUNDS
        or prior_revisions >= MAX_REVISIONS_BEFORE_PANEL_IS_FINAL
    )
    if is_final_round:
        reason = (
            f"{prior_revise_rounds} prior panel revise round(s)"
            if prior_revise_rounds >= MAX_PANEL_REVISE_ROUNDS
            else f"{prior_revisions} prior revisions (heavy revision history)"
        )
        console.print(
            f"[yellow]Qualifying panel ({reason}); this convening is final. "
            "Panelists choose `ready` or `shelve`.[/yellow]"
        )

    draft_md = (paths.ROOT / proj["draft_path"]).read_text(encoding="utf-8")
    proposal_md = (paths.ROOT / proj["proposal_path"]).read_text(encoding="utf-8")
    advisor_feedback_md = (
        advisor_feedback_path.read_text(encoding="utf-8")
        if advisor_feedback_path.is_file()
        else "(advisor feedback file missing)"
    )
    postulant_card = (
        f"# Postulant: {postulant_row['name']}\n\n"
        f"- **id:** `{postulant_row['id']}`\n"
        f"- **specialization:** {postulant_row['specialization']}\n"
    )

    # Collect outcomes. The advisor is implicitly `ready` (otherwise
    # we would not be in AWAITING_QUALIFYING_PANEL).
    outcomes: list[str] = ["ready"]  # advisor
    panel_summaries: list[tuple[str, str, str]] = []  # (panelist_id, role, summary)

    from institute.safe_io import atomic_write

    for evaluator, role in [
        (same_panel, "same-department"),
        (outside_panel, "outside-the-discipline"),
    ]:
        if evaluator is None:
            # Small-cohort tolerance on non-final rounds: a missing
            # slot defaults to ready so an early panel doesn't stall
            # on cohort size alone. On the FINAL round the default
            # flips to shelve: when the institution is forced to
            # render a verdict, an unstaffed slot must not push the
            # decision toward advancement. A panel that cannot be
            # convened properly on a final round produces a safer-
            # default shelve.
            default_outcome = "shelve" if is_final_round else "ready"
            console.print(
                f"[yellow]No {role} panelist available; "
                f"treating slot as `{default_outcome}` "
                f"({'final round' if is_final_round else 'small cohort'}).[/yellow]"
            )
            outcomes.append(default_outcome)
            continue
        # Round-numbered feedback path. The resume guard must only fire
        # within a single panel convening (so a mid-cycle crash doesn't
        # re-pay for the first evaluator). A verdict from an earlier
        # convening of the same panel is stale: the project was sent
        # back to revision, the draft has changed, the evaluator must
        # render a fresh judgment. Using r<N> in the filename keeps
        # convenings cleanly separated.
        convening_number = prior_revise_rounds + 1
        feedback_path = (
            paths.REVIEWS / project_id / f"panel-{role}-{evaluator.id}-r{convening_number}.md"
        )
        cached = _read_cached_panel_feedback(feedback_path)
        if cached is not None:
            cached_outcome, cached_summary = cached
            console.print(
                f"[dim]{evaluator.name} ({role}) already filed; "
                f"reusing cached verdict (`{cached_outcome}`).[/dim]"
            )
            outcomes.append(cached_outcome)
            panel_summaries.append((evaluator.id, role, cached_summary))
            continue
        console.print(
            f"[dim]Asking {evaluator.name} ({role}) to evaluate qualifying "
            f"project `{project_id}`...[/dim]"
        )
        outcome, summary, feedback_md = _run_evaluator(
            project_id=project_id,
            evaluator=evaluator,
            role=role,
            draft_md=draft_md,
            proposal_md=proposal_md,
            postulant_card=postulant_card,
            advisor_feedback_md=advisor_feedback_md,
            is_final_round=is_final_round,
        )
        outcomes.append(outcome)
        panel_summaries.append((evaluator.id, role, summary))
        atomic_write(
            feedback_path,
            f"# Qualifying-panel feedback by {evaluator.name} ({role})\n\n"
            f"- **Outcome:** `{outcome}`\n\n"
            f"## Summary\n\n{summary}\n\n## Feedback\n\n{feedback_md}\n",
        )

    ready_count = sum(1 for o in outcomes if o == "ready")
    shelve_count = sum(1 for o in outcomes if o == "shelve")
    if ready_count >= 2:
        target = State.PEER_REVIEWING
    elif is_final_round:
        # Two prior revise rounds already; this convening did not
        # produce a ready majority. Shelve the project. The
        # Postulant retains rank and may propose a new qualifying
        # project on the next cycle.
        target = State.SHELVED
    else:
        target = State.REVISING

    decision_body_lines = [
        f"**Postulant:** {postulant_row['name']} (`{postulant_row['id']}`)",
        "",
        f"**Panel outcomes:** {ready_count}/{len(outcomes)} ready"
        + (f", {shelve_count}/{len(outcomes)} shelve" if shelve_count else ""),
        "",
        f"**Prior revise rounds:** {prior_revise_rounds} "
        + ("(final round)" if is_final_round else f"(of {MAX_PANEL_REVISE_ROUNDS} allowed)"),
        "",
    ]
    for pid, role, summary in panel_summaries:
        decision_body_lines.append(f"- **{role}** (`{pid}`): {summary or '(no summary)'}")

    # Determine whether transitioning to PEER_REVIEWING needs to bump
    # `review_round`. We compute it before constructing the decision
    # body so the decision record reflects the bump.
    will_bump_review_round = False
    bump_from = bump_to = 0
    if target == State.PEER_REVIEWING:
        with db.connection() as conn:
            row = conn.execute(
                "SELECT review_round FROM projects WHERE id = ?",
                (project_id,),
            ).fetchone()
            current_review_round = int(row["review_round"]) if row else 1
            existing_reviews = conn.execute(
                "SELECT COUNT(*) AS n FROM reviews WHERE project_id = ? AND round = ?",
                (project_id, current_review_round),
            ).fetchone()["n"]
        if existing_reviews > 0:
            will_bump_review_round = True
            bump_from = current_review_round
            bump_to = current_review_round + 1

    if target == State.SHELVED:
        decision_body_lines.extend(
            [
                "",
                (
                    f"Project shelved after {MAX_PANEL_REVISE_ROUNDS} prior "
                    "rounds of panel-requested revision and a final "
                    "convening that did not earn a majority `ready`. The "
                    f"Postulant ({postulant_row['name']}) retains their rank "
                    "and may propose a new qualifying project. The shelved "
                    "draft and all panel feedback remain in the archive."
                ),
            ]
        )
    else:
        decision_body_lines.extend(["", f"Project advances to `{target.value}`."])
        if will_bump_review_round:
            decision_body_lines.append(
                f"Stale reviews from a prior pass exist for round "
                f"{bump_from}. Bumping `review_round` to {bump_to} so the "
                "next peer-review pass requests fresh reviews against the "
                "current draft."
            )
    decision = decisions.Decision(
        kind="qualifying_panel",
        title=f"Qualifying-project panel: {proj['title']}",
        body="\n".join(decision_body_lines),
        actors=[
            postulant_row["advisor_id"],
            postulant_row["id"],
            *(p[0] for p in panel_summaries),
        ],
        related_project=project_id,
    )
    with db.connection() as conn, db.transaction(conn):
        if will_bump_review_round:
            # Invalidate stale reviews from a prior peer-review pass by
            # incrementing review_round. peer_review.run() will then
            # look for fresh round-N+1 reviews and find none, prompting
            # a new round against the current draft.
            conn.execute(
                "UPDATE projects SET review_round = ? WHERE id = ?",
                (bump_to, project_id),
            )
        state.transition(conn, project_id, target)
        decisions.record(conn, decision)

    console.print(
        f"[bold green]Qualifying panel:[/bold green] {ready_count}/{len(outcomes)} ready "
        f"→ state `{target.value}`"
    )
