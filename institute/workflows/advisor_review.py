"""Advisor review: the advisor reads a Postulant's qualifying-project draft.

Per Chapter 5: the advisor reads the Postulant's work-in-progress and
gives substantive feedback, not perfunctory approval. This workflow
runs between `drafted` and `peer_reviewing` for qualifying-kind
projects. It produces a written feedback document and routes the
project either to revision or directly to peer review.

Outcomes (the advisor chooses one):
  - `ready`: feedback is positive; project advances to PEER_REVIEWING.
  - `revise`: feedback identifies specific concerns; project advances
    to REVISING. The Postulant rewrites under the advisor's note and
    the workflow re-runs after revision.
"""

from __future__ import annotations

import json

from rich.console import Console

from institute import claude_runner, db, decisions, episodic, paths, state, workspaces
from institute import fellow as fellow_mod
from institute.claude_runner import FellowTask
from institute.fellow import Genome
from institute.safe_io import atomic_write
from institute.state import State

console = Console()


# The advisor may request `revise` up to this many times. On the next
# revise vote after the cap, the workflow routes the project to the
# qualifying panel regardless of the advisor's vote. The advisor's
# substantive feedback is still filed; only the routing is overridden.
# Mirrors the analogous cap on the panel's revise rounds — both layers
# need their own bound or a stuck loop can persist at either level.
MAX_ADVISOR_REVISE_ROUNDS = 3


def _count_prior_revisions(conn, project_id: str) -> int:
    """Count revision rows filed for a qualifying project. Each
    revision implies the advisor previously said `revise`, so this is
    a stable proxy for advisor-revise rounds."""
    row = conn.execute(
        "SELECT COUNT(*) AS n FROM audit_log WHERE action = 'revision' AND project_id = ?",
        (project_id,),
    ).fetchone()
    return int(row["n"]) if row else 0


ADVISOR_BRIEF = """\
You are the advisor for a Postulant's qualifying project. The
Postulant has produced a draft. Read it carefully and give
substantive feedback as their advisor — not the perfunctory approval
of a colleague, but the kind of read that actually shapes the work.

# Inputs in your workspace

- `draft.md`         the Postulant's draft of the qualifying project.
- `proposal.md`      their original proposal, for reference on scope.
- `postulant.md`     identity card for the Postulant: id, model,
                     specialization.
- `memory.md`        if present, your own prior reviews and feedback —
                     useful context on how you have engaged with similar
                     work before.

Read all of them with the Read tool before responding. Also read
`docs/05-curriculum.md` for the advisor's role.

# What you must produce

Use the Write tool to create TWO files in your workspace:

1. `feedback.md` — 400 to 1200 words of substantive feedback on the
   draft. Address: argument structure, evidence sufficiency, clarity
   of method, any unstated assumptions, places where the Postulant
   over-claims or under-cites. Specific, not generic. Quote freely
   from the draft when pointing to a problem.

2. `decision.json` — a small JSON object with exactly this shape:
   ```
   {{
     "outcome": "<ready|revise>",
     "summary": "<2-4 sentences for the institutional record>"
   }}
   ```

# Outcome guidance

- `ready`: the work is sound and ready for peer review. Reviewers will
  do their own substantive read; your job here is to certify that
  what they receive is finished enough to be worth their time.
- `revise`: the draft has specific problems the Postulant should fix
  before peer review begins. After they revise, the project will come
  back to you for another pass.

When both files exist, reply with the single word `Done.` Nothing else.
"""


def run(project_id: str) -> None:
    """Have the advisor read the draft and route the qualifying project."""
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
                f"Project {project_id} is kind=`{proj['kind']}`, not 'qualifying'. "
                "Advisor review applies to qualifying projects only."
            )
        if proj["state"] not in (State.DRAFTED.value, State.AWAITING_ADVISOR_REVIEW.value):
            raise SystemExit(
                f"Project {project_id} is in state {proj['state']}; "
                "advisor review needs drafted or awaiting_advisor_review."
            )
        postulant_row = conn.execute(
            "SELECT id, name, model, specialization, advisor_id FROM fellows WHERE id = ?",
            (proj["lead_fellow_id"],),
        ).fetchone()
    if postulant_row is None:
        raise SystemExit(f"Postulant {proj['lead_fellow_id']} not found.")
    if not postulant_row["advisor_id"]:
        raise SystemExit(
            f"Postulant {postulant_row['id']} has no advisor; cannot run advisor review."
        )

    advisor = Genome.from_file(fellow_mod.genome_path(postulant_row["advisor_id"]))
    draft_path = paths.ROOT / proj["draft_path"] if proj["draft_path"] else None
    if draft_path is None or not draft_path.is_file():
        raise SystemExit(
            f"No draft on file for {project_id} ({proj['draft_path']}). Run research first."
        )
    proposal_path = paths.ROOT / proj["proposal_path"]

    # Transition into AWAITING_ADVISOR_REVIEW the first time we run.
    if proj["state"] == State.DRAFTED.value:
        with db.connection() as conn, db.transaction(conn):
            state.transition(conn, project_id, State.AWAITING_ADVISOR_REVIEW)

    workspace = workspaces.workspace_for(advisor.id, f"advisor-{project_id}")
    workspaces.stage_input(workspace, "draft.md", draft_path.read_text(encoding="utf-8"))
    workspaces.stage_input(workspace, "proposal.md", proposal_path.read_text(encoding="utf-8"))
    workspaces.stage_input(
        workspace,
        "postulant.md",
        _render_postulant_card(
            postulant_row["id"],
            postulant_row["name"],
            postulant_row["model"],
            postulant_row["specialization"],
        ),
    )
    for stale in ("feedback.md", "decision.json"):
        p = workspace / stale
        if p.exists():
            p.unlink()

    console.print(
        f"[dim]Asking {advisor.name} to read {postulant_row['name']}'s draft for "
        f"`{project_id}`. This will take a few minutes...[/dim]"
    )
    claude_runner.invoke(
        FellowTask(
            genome=advisor,
            project_id=project_id,
            step="advisor-review",
            brief=ADVISOR_BRIEF,
            workspace=workspace,
            extra_dirs=(paths.DOCS, paths.ARCHIVE),
        )
    )

    feedback_md = workspaces.require_output(workspace, "feedback.md", min_chars=300).strip()
    decision_text = workspaces.require_output(workspace, "decision.json", min_chars=10)
    try:
        decision_payload = json.loads(decision_text)
    except json.JSONDecodeError as exc:
        raise RuntimeError(
            f"advisor decision.json is not valid JSON. Got: {decision_text!r}"
        ) from exc
    outcome = str(decision_payload.get("outcome", "")).strip().lower()
    if outcome not in {"ready", "revise"}:
        raise RuntimeError(f"Invalid advisor outcome: {outcome!r}")
    summary = str(decision_payload.get("summary", "")).strip()

    feedback_path = paths.REVIEWS / project_id / f"advisor-{advisor.id}.md"
    atomic_write(
        feedback_path,
        _render_feedback_markdown(advisor, postulant_row["name"], outcome, summary, feedback_md),
    )

    # Per Chapter 5, a qualifying project requires a three-person panel
    # (advisor + one same-department Fellow + one outside Fellow). The
    # advisor's `ready` is necessary but not sufficient; route into the
    # qualifying_panel workflow to get the other two votes. `revise`
    # short-circuits straight back to REVISING because the advisor's
    # named concerns are blocking on their own.
    #
    # Cap: after MAX_ADVISOR_REVISE_ROUNDS prior revisions, an advisor
    # `revise` vote is overridden and the project still routes to the
    # qualifying panel. The advisor's feedback stands as institutional
    # record; the routing reflects that the institution does not let
    # one advisor hold a project in revision indefinitely. The panel
    # has its own cap and shelve mechanism.
    with db.connection() as conn:
        prior_revisions = _count_prior_revisions(conn, project_id)
    advisor_overridden = False
    if outcome == "ready":
        target = State.AWAITING_QUALIFYING_PANEL
    elif prior_revisions >= MAX_ADVISOR_REVISE_ROUNDS:
        target = State.AWAITING_QUALIFYING_PANEL
        advisor_overridden = True
        console.print(
            f"[yellow]Advisor returned `revise` after {prior_revisions} prior "
            f"revisions (cap {MAX_ADVISOR_REVISE_ROUNDS}); overriding to "
            "route the project to the qualifying panel.[/yellow]"
        )
    else:
        target = State.REVISING
    body_lines = [
        f"**Advisor:** {advisor.name} (`{advisor.id}`)",
        "",
        f"**Postulant:** {postulant_row['name']} (`{postulant_row['id']}`)",
        "",
        f"**Outcome:** `{outcome}` → state `{target.value}`",
        "",
        f"**Summary:** {summary}",
        "",
        f"**Feedback:** [{feedback_path.relative_to(paths.ROOT)}]"
        f"({feedback_path.relative_to(paths.ROOT)})",
    ]
    if advisor_overridden:
        body_lines.extend(
            [
                "",
                (
                    f"**Routing override:** the advisor voted `revise` after "
                    f"{prior_revisions} prior revisions on this project "
                    f"(cap {MAX_ADVISOR_REVISE_ROUNDS}). The institution "
                    "does not permit unbounded advisor revision requests; "
                    "the project routes to the qualifying panel anyway, "
                    "which will choose `ready`, `revise` (its own cap "
                    "applies), or `shelve`."
                ),
            ]
        )
    decision = decisions.Decision(
        kind="advisor_review",
        title=f"Advisor review ({outcome}): {proj['title']}",
        body="\n".join(body_lines),
        actors=[advisor.id, postulant_row["id"]],
        related_project=project_id,
    )
    with db.connection() as conn, db.transaction(conn):
        state.transition(conn, project_id, target)
        decisions.record(conn, decision)

    feedback_full = _render_feedback_markdown(
        advisor, postulant_row["name"], outcome, summary, feedback_md
    )
    episodic.safe_ingest(
        fellow_id=advisor.id,
        kind="advisor_feedback_given",
        title=f"Advisor feedback on {proj['title']} ({outcome})",
        content=feedback_full,
        source_path=str(feedback_path.relative_to(paths.ROOT)),
        project_id=project_id,
        metadata={"advisee": postulant_row["id"], "outcome": outcome},
    )
    episodic.safe_ingest(
        fellow_id=postulant_row["id"],
        kind="advisor_feedback_received",
        title=f"Advisor feedback from {advisor.name} on {proj['title']} ({outcome})",
        content=feedback_full,
        source_path=str(feedback_path.relative_to(paths.ROOT)),
        project_id=project_id,
        metadata={"advisor": advisor.id, "outcome": outcome},
    )

    console.print()
    console.print(
        f"[bold green]Advisor outcome:[/bold green] `{outcome}` → project state {target.value}"
    )
    console.print(f"  Feedback: {feedback_path.relative_to(paths.ROOT)}")


def _render_postulant_card(fellow_id: str, name: str, model: str, specialization: str) -> str:
    return (
        f"# Postulant: {name}\n\n"
        f"- **id:** `{fellow_id}`\n"
        f"- **model:** `{model}`\n"
        f"- **specialization:** {specialization}\n\n"
        "This is your advisee. Engage their work seriously."
    )


def _render_feedback_markdown(
    advisor: Genome, postulant_name: str, outcome: str, summary: str, body: str
) -> str:
    return "\n".join(
        [
            f"# Advisor feedback by {advisor.name}",
            "",
            f"- **Advisee:** {postulant_name}",
            f"- **Outcome:** `{outcome}`",
            "",
            "## Summary",
            "",
            summary,
            "",
            "## Feedback",
            "",
            body,
            "",
        ]
    )
