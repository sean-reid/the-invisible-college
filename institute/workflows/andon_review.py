"""Andon-cord review workflow.

A reviewer has pulled the andon cord on a submission. Publication is
halted. The orchestrator reads the cord pull, the draft, and the
pulling reviewer's full review, then recommends `dismiss` or
`sustain`. The Editorial Board (panel of Senior Fellows) or the
Founder makes the final call — same pattern as promotion.

Outcomes:
  - dismiss: the project moves to EDITORIAL and proceeds to publication.
  - sustain: the project moves to REJECTED.
"""

from __future__ import annotations

from datetime import UTC, datetime
from pathlib import Path
from typing import cast

from rich.console import Console
from rich.panel import Panel
from rich.prompt import Prompt

from institute import claude_runner, db, decisions, parsing, paths
from institute import fellow as fellow_mod
from institute.claude_runner import FellowTask
from institute.fellow import Genome
from institute.state import State

console = Console()


ORCHESTRATOR_BRIEF = """\
You are the orchestrator of the Invisible College. A reviewer has
pulled the andon cord on a submission. Publication is halted pending
review. Chapter 7 of the design (`docs/07-peer-review.md`) describes
the cord.

# Inputs in your working directory

- `draft.md`        the submitted piece in full
- `cord-pulls.md`   the cord pull(s) and reasons
- `reviews.md`      the full text of every review filed on this piece
                    so far, across all rounds

Read all three with the Read tool before recommending.

# Your job

Recommend one of:

- `dismiss` — the cord pull is not justified. The piece may proceed
  to editorial and publication. Frivolous pulls damage the puller's
  reputation; the decision should be made on substance, not politics.
- `sustain` — the cord pull is justified. The piece should be
  rejected. The lab notebook and reviews stay in the Archive as a
  record of the work.

# CRITICAL OUTPUT RULES

Reply with a single JSON object. No prose preface, no summary, no code
fence. First character `{{`, last `}}`.

# Output shape

```
{{
  "recommendation": "<dismiss|sustain>",
  "rationale": "<150-500 words explaining your judgment>",
  "concerns": "<markdown text, or '' if none>"
}}
```
"""


PANELIST_BRIEF = """\
You are serving on the Editorial Board. A reviewer has pulled the
andon cord on a submission. Read the piece, the cord pull, and the
prior reviews, then cast your vote on whether to dismiss the pull
(piece proceeds to publication) or sustain it (piece is rejected).

# Inputs in your working directory

- `draft.md`                    the submitted piece
- `cord-pulls.md`               the cord pull(s) and reasons
- `reviews.md`                  every prior review on this piece
- `orchestrator-recommendation.md` the orchestrator's recommendation;
                                read but do not defer

Form your own judgment. The cord is institutional duty — frivolous
pulls damage reviewer reputation, but justified pulls protect the
College's integrity.

# CRITICAL OUTPUT RULES

Reply with a single JSON object. No prose preface, no summary, no code
fence. First character `{{`, last `}}`.

# Output shape

```
{{
  "vote": "<dismiss|sustain>",
  "rationale": "<150-400 words of your reasoning>",
  "concerns": "<markdown text, or '' if none>"
}}
```
"""


def _stage(path: Path, content: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    tmp = path.with_suffix(path.suffix + ".tmp")
    tmp.write_text(content, encoding="utf-8")
    tmp.replace(path)


def _load_project_context(project_id: str) -> tuple[str, str, str, str]:
    """Return (title, draft_md, cord_pulls_md, reviews_md)."""
    with db.connection() as conn:
        proj = conn.execute(
            "SELECT title, draft_path FROM projects WHERE id = ?", (project_id,)
        ).fetchone()
        if proj is None:
            raise SystemExit(f"No such project: {project_id}")
        title = proj["title"]
        draft_md = (paths.ROOT / proj["draft_path"]).read_text(encoding="utf-8")
        cord_rows = list(
            conn.execute(
                "SELECT reviewer_id, andon_reason, round FROM reviews "
                "WHERE project_id = ? AND andon_cord = 1 ORDER BY round",
                (project_id,),
            )
        )
        review_rows = list(
            conn.execute(
                "SELECT reviewer_id, role, recommendation, round, content_path "
                "FROM reviews WHERE project_id = ? ORDER BY round, role",
                (project_id,),
            )
        )

    cord_lines = ["# Andon cord pull(s)", ""]
    for r in cord_rows:
        reason = (r["andon_reason"] or "").strip() or "(no reason supplied)"
        cord_lines.append(f"## {r['reviewer_id']} (round {r['round']})\n\n{reason}\n")

    review_lines = ["# Reviews on this submission", ""]
    for r in review_rows:
        path = paths.ROOT / r["content_path"]
        if not path.is_file():
            continue
        review_lines.append(
            f"## Round {r['round']} — {r['reviewer_id']} ({r['role']}) — `{r['recommendation']}`\n"
        )
        review_lines.append(path.read_text(encoding="utf-8"))
        review_lines.append("")

    return title, draft_md, "\n".join(cord_lines), "\n".join(review_lines)


def _orchestrator_recommend(project_id: str) -> dict:
    """Stage inputs and call the orchestrator for a dismiss/sustain recommendation."""
    workspace = paths.ARCHIVE / "andon-reviews" / project_id
    workspace.mkdir(parents=True, exist_ok=True)
    _, draft_md, cord_md, reviews_md = _load_project_context(project_id)
    _stage(workspace / "draft.md", draft_md)
    _stage(workspace / "cord-pulls.md", cord_md)
    _stage(workspace / "reviews.md", reviews_md)

    console.print(
        "[dim]Asking the orchestrator to review the andon cord pull. "
        "This will take a minute or two...[/dim]"
    )
    result = claude_runner.invoke_orchestrator(
        brief=ORCHESTRATOR_BRIEF,
        step=f"andon-recommend:{project_id}",
        model="claude-opus-4-7",
        cwd=workspace,
        extra_dirs=(paths.DOCS,),
        allowed_tools=("Read", "Glob", "Grep"),
    )
    return parsing.parse_json_or_dump(
        result.result_text,
        dump_path=workspace / "raw-recommendation.txt",
        context=f"Andon review recommendation for {project_id}",
    )


def _senior_panel() -> list[Genome]:
    """Active Senior Fellows. Empty if none exist."""
    with db.connection() as conn:
        rows = list(
            conn.execute(
                "SELECT id FROM fellows "
                "WHERE rank = 'senior_fellow' AND retired_at IS NULL ORDER BY name"
            )
        )
    return [Genome.from_file(fellow_mod.genome_path(r["id"])) for r in rows]


def _panel_vote(
    project_id: str, recommendation: dict, panel: list[Genome]
) -> tuple[str, list[dict]]:
    """Each panelist votes dismiss/sustain. Returns (outcome, votes).

    Outcome is "dismiss", "sustain", or "hold" (tie, treated as sustain
    because the cord pull stands by default).
    """
    base = paths.ARCHIVE / "andon-reviews" / project_id
    base.mkdir(parents=True, exist_ok=True)
    _, draft_md, cord_md, reviews_md = _load_project_context(project_id)
    rec_md = _render_recommendation_markdown(recommendation)

    votes: list[dict] = []
    for panelist in panel:
        ws = paths.FELLOWS / panelist.id / "workspace" / f"andon-{project_id}"
        ws.mkdir(parents=True, exist_ok=True)
        _stage(ws / "draft.md", draft_md)
        _stage(ws / "cord-pulls.md", cord_md)
        _stage(ws / "reviews.md", reviews_md)
        _stage(ws / "orchestrator-recommendation.md", rec_md)

        console.print(f"[dim]Panelist {panelist.name} is reviewing...[/dim]")
        result = claude_runner.invoke(
            FellowTask(
                genome=panelist,
                project_id=project_id,
                step="andon-vote",
                brief=PANELIST_BRIEF,
                workspace=ws,
                extra_dirs=(paths.DOCS,),
            )
        )
        vote_payload = parsing.parse_json_or_dump(
            result.result_text,
            dump_path=ws / "raw-vote.txt",
            context=f"Andon panel vote from {panelist.id} on {project_id}",
        )
        vote_payload["panelist_id"] = panelist.id
        vote_payload["panelist_name"] = panelist.name
        votes.append(vote_payload)

    raw = [str(v.get("vote", "")).strip().lower() for v in votes]
    dismiss = sum(1 for r in raw if r == "dismiss")
    sustain = sum(1 for r in raw if r == "sustain")
    if dismiss > sustain:
        return "dismiss", votes
    if sustain > dismiss:
        return "sustain", votes
    # Tie: cord pull stands. Better to err on caution.
    return "sustain", votes


def _render_recommendation_markdown(payload: dict) -> str:
    lines = [
        "# Orchestrator's recommendation",
        "",
        f"**Recommended:** {payload.get('recommendation', '?')}",
        "",
        "## Rationale",
        "",
        str(payload.get("rationale", "")).strip(),
    ]
    concerns = str(payload.get("concerns", "")).strip()
    if concerns:
        lines.extend(["", "## Concerns", "", concerns])
    return "\n".join(lines) + "\n"


def _founder_decide(project_id: str, recommendation: dict) -> str:
    """Founder reviews the recommendation in the terminal. Returns dismiss/sustain/abort."""
    recommended = str(recommendation.get("recommendation", "sustain")).strip().lower()
    rationale = str(recommendation.get("rationale", "")).strip()
    concerns = str(recommendation.get("concerns", "")).strip()

    console.print()
    console.print(
        Panel.fit(
            f"[bold]Andon-cord review[/bold] on `{project_id}`\n"
            f"[dim]orchestrator recommends:[/dim] {recommended}",
            border_style="red",
        )
    )
    if rationale:
        console.print(Panel(rationale, title="Rationale", border_style="dim"))
    if concerns:
        console.print(Panel(concerns, title="Concerns", border_style="yellow"))

    valid = ["dismiss", "sustain", "abort"]
    default = recommended if recommended in {"dismiss", "sustain"} else "sustain"
    return Prompt.ask("[bold]Decision[/bold]", choices=valid, default=default)


def _apply_outcome(
    project_id: str,
    title: str,
    outcome: str,
    recommendation: dict,
    actors: list[str],
    panel_votes: list[dict] | None,
) -> None:
    """Persist the andon outcome: update state + write decision record."""
    if outcome == "dismiss":
        target = State.EDITORIAL
        verb = "dismissed"
    else:
        target = State.REJECTED
        verb = "sustained"

    body_lines = [
        f"**Project:** {project_id}",
        "",
        f"**Outcome:** {verb} (state → `{target.value}`)",
        "",
        "## Orchestrator rationale",
        "",
        str(recommendation.get("rationale", "")).strip(),
    ]
    if panel_votes:
        body_lines.extend(["", "## Panel votes", ""])
        for v in panel_votes:
            body_lines.append(
                f"### {v.get('panelist_name', v.get('panelist_id', '?'))}: `{v.get('vote', '?')}`"
            )
            rat = str(v.get("rationale", "")).strip()
            if rat:
                body_lines.extend(["", rat])
            body_lines.append("")
    body = "\n".join(body_lines)

    decision = decisions.Decision(
        kind="andon_cord_outcome",
        title=f"Andon cord {verb}: {title}",
        body=body,
        actors=actors,
        related_project=project_id,
    )
    now = datetime.now(UTC).isoformat(timespec="seconds")
    with db.connection() as conn, db.transaction(conn):
        conn.execute(
            "UPDATE projects SET state = ?, updated_at = ? WHERE id = ?",
            (target.value, now, project_id),
        )
        decisions.record(conn, decision)

    # Charter-violation auto-termination. If the sustained cord was
    # filed as a Charter violation, fire the targeted kill switch on
    # the responsible Fellow. Per Chapter 3, in-flight work is
    # discarded; already-published work survives in the Archive with
    # disclosure.
    if outcome == "sustain":
        _maybe_auto_terminate(project_id, title)
    elif outcome == "dismiss":
        # A dismissed cord pull is a frivolous-pull mark against each
        # reviewer who pulled it. Chapter 7: "A frivolous pull damages
        # the puller's reputation."
        _mark_frivolous_andon_pulls(project_id, title)

    console.print()
    style = "green" if outcome == "dismiss" else "red"
    console.print(
        f"[bold {style}]Andon cord {verb}.[/bold {style}] Project {project_id} -> {target.value}"
    )


def _mark_frivolous_andon_pulls(project_id: str, title: str) -> None:
    """Record a frivolous_andon mark against every Fellow who pulled the cord.

    Called from _apply_outcome when the Editorial Board dismisses the
    cord. Chapter 7 considers frivolous pulls damaging to reviewer
    reputation; this is the codification.
    """
    from institute import reviewer_eligibility

    with db.connection() as conn:
        pullers = list(
            conn.execute(
                "SELECT id AS review_id, reviewer_id, andon_reason "
                "FROM reviews WHERE project_id = ? AND andon_cord = 1",
                (project_id,),
            )
        )
    for row in pullers:
        reason = (
            f"Editorial Board dismissed andon cord on `{project_id}` "
            f"({title}). Stated reason: "
            + ((row["andon_reason"] or "").strip() or "(no reason supplied)")
        )
        reviewer_eligibility.safe_record(
            fellow_id=row["reviewer_id"],
            kind="frivolous_andon",
            reason=reason,
            related_project=project_id,
            related_review_id=row["review_id"],
        )


def _maybe_auto_terminate(project_id: str, title: str) -> None:
    """If any cord-pulling review on this project flagged a Charter violation,
    fire the targeted kill switch on the project's lead Fellow.

    Picks the most specific violation_kind across the flagged reviews
    (first non-null wins). Builds a reason from the cord-pullers' stated
    reasons. Idempotent: terminate.run is a no-op for already-retired
    Fellows.
    """
    with db.connection() as conn:
        rows = list(
            conn.execute(
                "SELECT reviewer_id, andon_reason, violation_kind FROM reviews "
                "WHERE project_id = ? AND andon_cord = 1 AND charter_violation = 1",
                (project_id,),
            )
        )
        if not rows:
            return
        lead_row = conn.execute(
            "SELECT lead_fellow_id FROM projects WHERE id = ?", (project_id,)
        ).fetchone()
    if lead_row is None or not lead_row["lead_fellow_id"]:
        return
    lead_id = lead_row["lead_fellow_id"]

    # Pick the first non-empty violation_kind. If none, fall back to 'other'.
    kind = next(
        (r["violation_kind"] for r in rows if r["violation_kind"]),
        "other",
    )
    # Compose a reason that names each cord-pulling reviewer.
    parts = []
    for r in rows:
        reviewer = r["reviewer_id"]
        reason_text = (r["andon_reason"] or "").strip() or "(no reason supplied)"
        parts.append(f"{reviewer}: {reason_text}")
    reason = (
        f"Editorial Board sustained the andon cord on `{project_id}` "
        f"({title}) with `charter_violation` flagged. " + " | ".join(parts)
    )

    from institute.workflows import terminate as terminate_workflow

    terminate_workflow.run(
        lead_id,
        kind=kind,
        reason=reason,
        triggered_by="editorial-board",
        related_project=project_id,
    )


def run(project_id: str) -> None:
    """Dispatch the andon review. Called from `institute next`."""
    with db.connection() as conn:
        proj = conn.execute(
            "SELECT title, state FROM projects WHERE id = ?", (project_id,)
        ).fetchone()
        if proj is None:
            raise SystemExit(f"No such project: {project_id}")
        if proj["state"] != State.ANDON_REVIEW.value:
            raise SystemExit(
                f"Project {project_id} is in state {proj['state']}, expected andon_review."
            )
        title = proj["title"]

    recommendation = _orchestrator_recommend(project_id)
    panel = _senior_panel()

    if panel:
        console.print(
            f"[dim]Convening Editorial Board ({len(panel)} Senior Fellow"
            f"{'s' if len(panel) != 1 else ''})...[/dim]"
        )
        outcome, votes = _panel_vote(project_id, recommendation, panel)
        actors = ["orchestrator", *[p.id for p in panel]]
        _apply_outcome(project_id, title, outcome, recommendation, actors, votes)
        return

    choice = _founder_decide(project_id, recommendation)
    if choice == "abort":
        console.print("[yellow]Andon review aborted; project stays in andon_review.[/yellow]")
        return
    actors = ["founder", "orchestrator"]
    _apply_outcome(project_id, title, cast(str, choice), recommendation, actors, None)
