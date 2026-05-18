"""Promotion workflow: move a Fellow up (or down) the tenure ladder.

Two execution paths share the same orchestrator recommendation:

  - **Panel vote.** If one or more Senior Fellows exist (excluding the
    candidate), they serve as the Tenure Committee. Each panelist is
    invoked as a Fellow with the dossier and Chapter 3, and writes a
    structured vote. The aggregator picks the majority rank, or holds
    on a tie. No Founder involvement.
  - **Founder fallback.** Until at least one Senior Fellow exists, the
    Founder serves as committee. The recommendation is shown in the
    terminal and the Founder picks the new rank interactively. This is
    the same pattern admissions uses while the institution is too
    young to have its own admissions committee.

The `auto` flag forces panel-only behavior: if no panel exists the
workflow exits without prompting. Used by `institute run` so the
autonomous loop never blocks waiting on stdin.
"""

from __future__ import annotations

import json
from collections import Counter
from datetime import UTC, datetime
from pathlib import Path
from typing import cast

from rich.console import Console
from rich.panel import Panel
from rich.prompt import Prompt

from institute import archive_index, claude_runner, db, decisions, parsing, paths, reputation
from institute import fellow as fellow_mod
from institute.claude_runner import FellowTask
from institute.fellow import Genome, Rank

console = Console()


RANK_ORDER: tuple[Rank, ...] = (
    "postulant",
    "novice",
    "junior_fellow",
    "fellow",
    "senior_fellow",
    "emeritus",
)


PROMOTE_BRIEF = """\
You are the orchestrator of the Invisible College. The Tenure
Committee has asked you to recommend a rank for a Fellow based on
their body of work. Chapter 3 of the design (`docs/03-fellows.md`)
defines the ladder and the entry criteria.

# Inputs in your working directory

- `dossier.md`       the target Fellow's authorship and reviewer signals.
- `archive-index.md` every piece the College has published.
- `cohort.md`        the full cohort with their current ranks for context.

Read all three with the Read tool. Then read `docs/03-fellows.md` for
the rank criteria.

# Your job

Recommend one of: `postulant`, `novice`, `junior_fellow`, `fellow`,
`senior_fellow`, `emeritus`, or `hold` (no change). Recommending a
demotion is allowed but should be rare and the rationale must be
strong.

The Fellow's current rank is `{current_rank}`. Consider:

- **Publications.** Quality more than count. Even one strong piece can
  warrant promotion; many weak ones should not.
- **Peer review service.** Sustained, substantive reviewing is the
  single clearest signal of a serious Fellow. Look at sticky majors —
  round-1 "major revisions required" recommendations that the author
  then actually revised. They indicate the review caught something
  real.
- **Cross-disciplinary engagement.** Chapter 5 makes this explicit:
  cross-disciplinary work counts more in promotion than within-spec
  work of equivalent quality.
- **Activity.** A Fellow with zero publications and zero reviews after
  the founding cohort has had time to work has either failed to engage
  or has been blocked structurally. Note which, and recommend hold or
  demotion accordingly.

# CRITICAL OUTPUT RULES

Reply with a single JSON object. No prose preface, no summary, no code
fence. First character `{{`, last `}}`.

# Output shape

```
{{
  "recommended_rank": "<one of: postulant | novice | junior_fellow | fellow | senior_fellow | emeritus | hold>",
  "rationale": "<150-600 words of reasoning the committee will read>",
  "key_evidence": ["<short fact 1>", "<short fact 2>", ...],
  "concerns": "<markdown text, or '' if none>"
}}
```
"""


PANELIST_BRIEF = """\
You are serving on the Tenure Committee. The College has asked you to
review a fellow Scholar's body of work and cast a written vote on
their rank.

# Inputs in your working directory

- `dossier.md`         the candidate's authorship and reviewer signals.
- `archive-index.md`   every piece the College has published.
- `cohort.md`          the rest of the cohort for context.
- `orchestrator-recommendation.md` the orchestrator's recommendation
                       and rationale. Read it but do not defer to it;
                       form your own judgment first.

Read these with the Read tool. The rank ladder is defined in
`docs/03-fellows.md`.

# Your job

Cast a vote on the candidate's rank. The candidate's current rank is
`{current_rank}`. Choose one of: `postulant`, `novice`,
`junior_fellow`, `fellow`, `senior_fellow`, `emeritus`, or `hold` (no
change).

A serious vote engages the actual evidence. State what you read in the
dossier, what evidence convinced you, and any concern that gives you
pause. Do not produce template prose.

# CRITICAL OUTPUT RULES

Reply with a single JSON object. No prose preface, no summary, no code
fence. First character `{{`, last `}}`.

# Output shape

```
{{
  "vote": "<one of: postulant | novice | junior_fellow | fellow | senior_fellow | emeritus | hold>",
  "rationale": "<150-400 words of your reasoning>",
  "concerns": "<markdown text, or '' if none>"
}}
```
"""


VALID_RANKS: set[str] = set(RANK_ORDER) | {"hold"}


# ---------------------------------------------------------------------------
# Orchestrator recommendation
# ---------------------------------------------------------------------------


def _orchestrator_recommend(rep: reputation.FellowReputation) -> dict:
    """Stage inputs, call the orchestrator, parse the JSON recommendation."""
    workspace = paths.ARCHIVE / "promotions" / "_orchestrator-workspace"
    workspace.mkdir(parents=True, exist_ok=True)

    cohort = reputation.load_cohort()
    _stage(workspace / "dossier.md", reputation.render_fellow_dossier(rep))
    _stage(workspace / "archive-index.md", archive_index.render())
    _stage(workspace / "cohort.md", reputation.render_cohort_brief(cohort))

    console.print(
        f"[dim]Asking the orchestrator to recommend a rank for {rep.name}. "
        "This will take a minute or two...[/dim]"
    )
    result = claude_runner.invoke_orchestrator(
        brief=PROMOTE_BRIEF.format(current_rank=rep.rank),
        step=f"promote-recommend:{rep.fellow_id}",
        model="claude-opus-4-7",
        cwd=workspace,
        extra_dirs=(paths.DOCS,),
        allowed_tools=("Read", "Glob", "Grep"),
    )
    return parsing.parse_json_or_dump(
        result.result_text,
        dump_path=workspace / "raw-recommendation.txt",
        context=f"Promotion recommendation for {rep.fellow_id}",
    )


def _stage(path: Path, content: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    tmp = path.with_suffix(path.suffix + ".tmp")
    tmp.write_text(content, encoding="utf-8")
    tmp.replace(path)


# ---------------------------------------------------------------------------
# Panel-vote path
# ---------------------------------------------------------------------------


def _senior_panel(candidate_id: str) -> list[Genome]:
    """Active Senior Fellows other than the candidate. Empty if none exist."""
    with db.connection() as conn:
        rows = list(
            conn.execute(
                "SELECT id FROM fellows "
                "WHERE rank = 'senior_fellow' AND retired_at IS NULL AND id != ? "
                "ORDER BY name",
                (candidate_id,),
            )
        )
    return [Genome.from_file(fellow_mod.genome_path(r["id"])) for r in rows]


def _panel_vote(
    rep: reputation.FellowReputation,
    recommendation: dict,
    panel: list[Genome],
) -> tuple[Rank | None, list[dict]]:
    """Each panelist casts a vote; aggregate by majority. Returns (rank, votes).

    Returns rank=None when the panel chose 'hold' or split.
    """
    base = paths.ARCHIVE / "promotions" / rep.fellow_id
    base.mkdir(parents=True, exist_ok=True)
    cohort = reputation.load_cohort()
    rec_md = _render_recommendation_markdown(recommendation)

    votes: list[dict] = []
    for panelist in panel:
        ws = paths.FELLOWS / panelist.id / "workspace" / f"tenure-{rep.fellow_id}"
        ws.mkdir(parents=True, exist_ok=True)
        _stage(ws / "dossier.md", reputation.render_fellow_dossier(rep))
        _stage(ws / "archive-index.md", archive_index.render())
        _stage(ws / "cohort.md", reputation.render_cohort_brief(cohort))
        _stage(ws / "orchestrator-recommendation.md", rec_md)

        console.print(f"[dim]Panelist {panelist.name} is reviewing...[/dim]")
        result = claude_runner.invoke(
            FellowTask(
                genome=panelist,
                project_id=f"tenure-{rep.fellow_id}",
                step="panel-vote",
                brief=PANELIST_BRIEF.format(current_rank=rep.rank),
                workspace=ws,
                extra_dirs=(paths.DOCS,),
            )
        )
        vote_payload = parsing.parse_json_or_dump(
            result.result_text,
            dump_path=ws / "raw-vote.txt",
            context=f"Panel vote from {panelist.id} on {rep.fellow_id}",
        )
        vote_payload["panelist_id"] = panelist.id
        vote_payload["panelist_name"] = panelist.name
        votes.append(vote_payload)
        _stage(base / f"vote-{panelist.id}.json", json.dumps(vote_payload, indent=2))

    rank = _tally(votes, rep.rank)
    return rank, votes


def _tally(votes: list[dict], current_rank: str) -> Rank | None:
    """Pick the rank with strict majority; otherwise None (hold)."""
    raw = [str(v.get("vote", "hold")).strip().lower() for v in votes]
    cleaned = [r for r in raw if r in VALID_RANKS]
    if not cleaned:
        return None
    counts = Counter(cleaned)
    top_rank, top_count = counts.most_common(1)[0]
    if top_count * 2 <= len(cleaned):
        return None  # no strict majority
    if top_rank == "hold" or top_rank == current_rank:
        return None
    return cast(Rank, top_rank)


def _render_recommendation_markdown(payload: dict) -> str:
    lines = [
        "# Orchestrator's recommendation",
        "",
        f"**Recommended rank:** {payload.get('recommended_rank', 'hold')}",
        "",
        "## Rationale",
        "",
        str(payload.get("rationale", "")).strip(),
    ]
    evidence = payload.get("key_evidence") or []
    if evidence:
        lines.extend(["", "## Key evidence", ""])
        for item in evidence:
            if isinstance(item, str) and item.strip():
                lines.append(f"- {item.strip()}")
    concerns = str(payload.get("concerns", "")).strip()
    if concerns:
        lines.extend(["", "## Concerns", "", concerns])
    return "\n".join(lines) + "\n"


# ---------------------------------------------------------------------------
# Founder-fallback path
# ---------------------------------------------------------------------------


def _founder_decide(rep: reputation.FellowReputation, payload: dict) -> Rank | None:
    """Present the recommendation to the Founder. Returns the chosen rank, or None to abort."""
    recommended = str(payload.get("recommended_rank", "hold")).strip().lower()
    rationale = str(payload.get("rationale", "")).strip()
    evidence = payload.get("key_evidence", [])
    concerns = str(payload.get("concerns", "")).strip()

    console.print()
    console.print(
        Panel.fit(
            f"[bold]{rep.name}[/bold]  ({rep.fellow_id})\n"
            f"[dim]current rank:[/dim] {rep.rank}\n"
            f"[dim]orchestrator recommends:[/dim] {recommended}",
            title="Promotion review",
            border_style="cyan",
        )
    )
    if rationale:
        console.print(Panel(rationale, title="Rationale", border_style="dim"))
    if evidence:
        lines = "\n".join(f"- {e}" for e in evidence if isinstance(e, str))
        console.print(Panel(lines, title="Key evidence", border_style="dim"))
    if concerns:
        console.print(Panel(concerns, title="Concerns", border_style="yellow"))

    valid: list[str] = [*RANK_ORDER, "hold"]
    default = recommended if recommended in valid else "hold"
    choice = Prompt.ask(
        "[bold]Final rank decision[/bold]",
        choices=[*valid, "abort"],
        default=default,
    )
    if choice == "abort":
        console.print("[yellow]Promotion aborted.[/yellow]")
        return None
    if choice == "hold":
        console.print(f"[dim]Rank unchanged: {rep.rank}.[/dim]")
        return None
    return cast(Rank, choice)


# ---------------------------------------------------------------------------
# Apply + log
# ---------------------------------------------------------------------------


def _apply_rank_change(
    rep: reputation.FellowReputation,
    new_rank: Rank,
    payload: dict,
    actors: list[str],
    panel_votes: list[dict] | None,
) -> Path:
    """Persist the rank change to the DB, genome file, and decision log."""
    now = datetime.now(UTC).isoformat(timespec="seconds")

    genome = Genome.from_file(fellow_mod.genome_path(rep.fellow_id))
    updated = genome.model_copy(update={"rank": new_rank})
    updated.write(fellow_mod.genome_path(rep.fellow_id))

    decision_body = _format_decision_body(rep, new_rank, payload, panel_votes, now)
    decision = decisions.Decision(
        kind="promotion",
        title=f"{rep.name}: {rep.rank} to {new_rank}",
        body=decision_body,
        actors=actors,
    )

    with db.connection() as conn, db.transaction(conn):
        conn.execute(
            "UPDATE fellows SET rank = ? WHERE id = ?",
            (new_rank, rep.fellow_id),
        )
        path = decisions.record(conn, decision)
    return path


def _log_review_attempt(
    rep: reputation.FellowReputation,
    payload: dict,
    outcome: str,
    actors: list[str],
    panel_votes: list[dict] | None,
) -> Path:
    """Record a promotion review that did NOT result in a rank change.

    Auto-trigger relies on this row to know when the cohort was last
    reviewed, so it can space out reviews instead of recomputing on
    every publication.
    """
    now = datetime.now(UTC).isoformat(timespec="seconds")
    body = [
        f"**Fellow:** {rep.name} (`{rep.fellow_id}`)",
        "",
        f"**Outcome:** {outcome}",
        "",
        f"**Current rank (unchanged):** {rep.rank}",
        "",
        f"**Recorded:** {now}",
    ]
    rationale = str(payload.get("rationale", "")).strip()
    if rationale:
        body.extend(["", "## Orchestrator rationale", "", rationale])
    if panel_votes:
        body.extend(["", "## Panel votes", ""])
        for v in panel_votes:
            body.append(
                f"- **{v.get('panelist_name', v.get('panelist_id', '?'))}** voted "
                f"`{v.get('vote', '?')}`"
            )
    decision = decisions.Decision(
        kind="promotion_review",
        title=f"{rep.name}: review at {rep.rank} ({outcome})",
        body="\n".join(body),
        actors=actors,
    )
    with db.connection() as conn, db.transaction(conn):
        return decisions.record(conn, decision)


def _format_decision_body(
    rep: reputation.FellowReputation,
    new_rank: Rank,
    payload: dict,
    panel_votes: list[dict] | None,
    recorded_at: str,
) -> str:
    rationale = str(payload.get("rationale", "")).strip()
    evidence = payload.get("key_evidence", [])
    concerns = str(payload.get("concerns", "")).strip()
    lines = [
        f"**Fellow:** {rep.name} (`{rep.fellow_id}`)",
        "",
        f"**Rank change:** {rep.rank} → {new_rank}",
        "",
        f"**Recorded:** {recorded_at}",
        "",
        "**Reputation snapshot at time of decision:**",
        f"- publications: {rep.author.publications}",
        f"- reviews given: {rep.reviewer.reviews_given}",
        f"- sticky round-1 majors: {rep.reviewer.sticky_majors}",
    ]
    if rationale:
        lines.extend(["", "## Orchestrator rationale", "", rationale])
    if evidence:
        lines.extend(["", "## Key evidence", ""])
        for item in evidence:
            if isinstance(item, str) and item.strip():
                lines.append(f"- {item.strip()}")
    if concerns:
        lines.extend(["", "## Concerns", "", concerns])
    if panel_votes:
        lines.extend(["", "## Panel votes", ""])
        for v in panel_votes:
            lines.append(
                f"### {v.get('panelist_name', v.get('panelist_id', '?'))}: `{v.get('vote', '?')}`"
            )
            rat = str(v.get("rationale", "")).strip()
            if rat:
                lines.extend(["", rat])
            con = str(v.get("concerns", "")).strip()
            if con:
                lines.extend(["", f"_Concerns:_ {con}"])
            lines.append("")
    return "\n".join(lines)


def _is_promotion(old: str, new: str) -> bool:
    try:
        return RANK_ORDER.index(cast(Rank, new)) > RANK_ORDER.index(cast(Rank, old))
    except ValueError:
        return False


# ---------------------------------------------------------------------------
# Public entry points
# ---------------------------------------------------------------------------


def run(fellow_id: str, *, auto: bool = False) -> str:
    """Top-level promote entry point.

    When `auto=True` and no Senior Fellow panel exists, the workflow
    exits without prompting (used by the autonomous run loop).
    Otherwise the Founder serves as committee.

    Returns one of: "promoted", "demoted", "held", "skipped".
    """
    rep = reputation.load_fellow(fellow_id)
    if rep is None:
        console.print(f"[red]No active Fellow with id `{fellow_id}`.[/red]")
        return "skipped"

    panel = _senior_panel(rep.fellow_id)
    payload = _orchestrator_recommend(rep)

    if panel:
        console.print(
            f"[dim]Convening Tenure Committee ({len(panel)} Senior Fellow"
            f"{'s' if len(panel) != 1 else ''})...[/dim]"
        )
        new_rank, votes = _panel_vote(rep, payload, panel)
        actors = ["orchestrator", *[p.id for p in panel], rep.fellow_id]
        if new_rank is None or new_rank == rep.rank:
            _log_review_attempt(rep, payload, "panel held", actors, votes)
            console.print(f"[dim]Panel held: rank unchanged at {rep.rank}.[/dim]")
            return "held"
        decision_path = _apply_rank_change(rep, new_rank, payload, actors, votes)
        _print_summary(rep, new_rank, decision_path)
        return "promoted" if _is_promotion(rep.rank, new_rank) else "demoted"

    if auto:
        # No panel and we cannot block on stdin. Log the review attempt
        # so the auto-trigger does not re-fire next cycle, then exit.
        _log_review_attempt(
            rep,
            payload,
            "deferred: no Senior Fellow panel",
            ["orchestrator"],
            None,
        )
        console.print(
            "[yellow]No Senior Fellow panel; auto-mode deferred. "
            f"Run `institute promote --fellow {rep.fellow_id}` to decide manually."
            "[/yellow]"
        )
        return "skipped"

    new_rank = _founder_decide(rep, payload)
    actors = ["founder", "orchestrator", rep.fellow_id]
    if new_rank is None or new_rank == rep.rank:
        _log_review_attempt(rep, payload, "founder held", actors, None)
        return "held"
    decision_path = _apply_rank_change(rep, new_rank, payload, actors, None)
    _print_summary(rep, new_rank, decision_path)
    return "promoted" if _is_promotion(rep.rank, new_rank) else "demoted"


def _print_summary(rep: reputation.FellowReputation, new_rank: Rank, decision_path: Path) -> None:
    direction = "promoted" if _is_promotion(rep.rank, new_rank) else "moved"
    console.print()
    console.print(f"[bold green]{rep.name} {direction}:[/bold green] {rep.rank} → {new_rank}")
    console.print(f"  Genome: {fellow_mod.genome_path(rep.fellow_id)}")
    console.print(f"  Decision: {decision_path.relative_to(paths.ROOT)}")
    console.print("[dim]Commit `genomes/` and `archive/decisions/` to git when you're ready.[/dim]")
