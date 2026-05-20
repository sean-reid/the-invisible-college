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

    eligible_ids = [
        r["id"]
        for r in conn.execute(
            "SELECT id FROM fellows "
            "WHERE retired_at IS NULL AND id NOT IN (?, ?) "
            "ORDER BY id",
            (candidate_id, advisor_id),
        )
    ]
    if not eligible_ids:
        return (None, None)

    use_departments = departments.is_initialized(conn)
    same_dept: str | None = None
    outside: str | None = None
    for fid in eligible_ids:
        if use_departments:
            shares = departments.same_department(
                conn, fellow_a=candidate_id, fellow_b=fid
            )
        else:
            row = conn.execute(
                "SELECT specialization FROM fellows WHERE id = ?", (fid,)
            ).fetchone()
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


def _run_evaluator(
    *,
    project_id: str,
    evaluator: Genome,
    role: str,
    draft_md: str,
    proposal_md: str,
    postulant_card: str,
    advisor_feedback_md: str,
) -> tuple[str, str, str]:
    """Run one panelist. Returns (outcome, summary, feedback_md)."""
    workspace = workspaces.workspace_for(
        evaluator.id, f"panel-{project_id}-{role}"
    )
    workspaces.stage_input(workspace, "draft.md", draft_md)
    workspaces.stage_input(workspace, "proposal.md", proposal_md)
    workspaces.stage_input(workspace, "postulant.md", postulant_card)
    workspaces.stage_input(workspace, "advisor-feedback.md", advisor_feedback_md)
    workspaces.stage_input(workspace, "role.md", _evaluator_brief(role))
    for stale in ("feedback.md", "decision.json"):
        p = workspace / stale
        if p.exists():
            p.unlink()
    claude_runner.invoke(
        FellowTask(
            genome=evaluator,
            project_id=project_id,
            step=f"qualifying-panel:{role}",
            brief=PANEL_BRIEF,
            workspace=workspace,
            extra_dirs=(paths.DOCS, paths.ARCHIVE),
        )
    )
    feedback_md = workspaces.require_output(
        workspace, "feedback.md", min_chars=150
    ).strip()
    decision_text = workspaces.require_output(workspace, "decision.json", min_chars=10)
    try:
        decision_payload = json.loads(decision_text)
    except json.JSONDecodeError as exc:
        raise RuntimeError(
            f"panelist {evaluator.id} decision.json is not valid JSON: {decision_text!r}"
        ) from exc
    outcome = str(decision_payload.get("outcome", "")).strip().lower()
    if outcome not in {"ready", "revise"}:
        raise RuntimeError(
            f"panelist {evaluator.id} returned unrecognized outcome {outcome!r}"
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
            raise SystemExit(
                f"Project {project_id} is kind=`{proj['kind']}`, not qualifying."
            )
        if proj["state"] != State.AWAITING_QUALIFYING_PANEL.value:
            raise SystemExit(
                f"Project {project_id} is in state {proj['state']}, expected "
                "awaiting_qualifying_panel."
            )
        postulant_row = conn.execute(
            "SELECT id, name, model, specialization, advisor_id "
            "FROM fellows WHERE id = ?",
            (proj["lead_fellow_id"],),
        ).fetchone()
        if postulant_row is None:
            raise SystemExit(f"Postulant {proj['lead_fellow_id']} not found.")
        same_panel, outside_panel = _pick_panel(
            conn,
            candidate_id=postulant_row["id"],
            advisor_id=postulant_row["advisor_id"],
        )
        advisor_feedback_path = paths.REVIEWS / project_id / f"advisor-{postulant_row['advisor_id']}.md"

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
            console.print(
                f"[yellow]No {role} panelist available; "
                "treating slot as `ready` (small cohort).[/yellow]"
            )
            outcomes.append("ready")
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
        )
        outcomes.append(outcome)
        panel_summaries.append((evaluator.id, role, summary))
        # Write the feedback into the same reviews directory the
        # advisor uses, with a distinguishing prefix.
        feedback_path = (
            paths.REVIEWS / project_id / f"panel-{role}-{evaluator.id}.md"
        )
        atomic_write(
            feedback_path,
            f"# Qualifying-panel feedback by {evaluator.name} ({role})\n\n"
            f"- **Outcome:** `{outcome}`\n\n"
            f"## Summary\n\n{summary}\n\n## Feedback\n\n{feedback_md}\n",
        )

    ready_count = sum(1 for o in outcomes if o == "ready")
    target = (
        State.PEER_REVIEWING
        if ready_count >= 2
        else State.REVISING
    )

    decision_body_lines = [
        f"**Postulant:** {postulant_row['name']} (`{postulant_row['id']}`)",
        "",
        f"**Panel outcomes:** {ready_count}/{len(outcomes)} ready",
        "",
    ]
    for pid, role, summary in panel_summaries:
        decision_body_lines.append(f"- **{role}** (`{pid}`): {summary or '(no summary)'}")
    decision_body_lines.extend(
        ["", f"Project advances to `{target.value}`."]
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
        state.transition(conn, project_id, target)
        decisions.record(conn, decision)

    console.print(
        f"[bold green]Qualifying panel:[/bold green] {ready_count}/{len(outcomes)} ready "
        f"→ state `{target.value}`"
    )
