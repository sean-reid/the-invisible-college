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
from typing import Literal, cast

from rich.console import Console
from rich.panel import Panel
from rich.prompt import Prompt

from institute import archive_index, claude_runner, db, decisions, parsing, paths, reputation
from institute import fellow as fellow_mod
from institute.claude_runner import FellowTask
from institute.fellow import Genome, Rank
from institute.workflows import concern_review

# A promotion review can end in one of three ways:
#   - a Rank string  → the Fellow's rank changes
#   - "release"      → the Fellow is retired from the College
#   - None           → no change ("hold")
PromoteOutcome = Rank | Literal["release"] | None

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

Recommend one of:

- A rank: `postulant`, `novice`, `junior_fellow`, `fellow`,
  `senior_fellow`, `emeritus`. Use this for promotions and (rarely)
  demotions.
- `hold`: no change. Default when evidence is mixed or insufficient.
- `release`: the Fellow is retired from active duty. Genome and
  published work are preserved in the Archive, but the Fellow no
  longer participates in the College. Reserved for sustained
  non-engagement (see below).

Recommending a demotion is allowed but should be rare and the
rationale must be strong. Senior Fellows cannot be demoted to a lower
rank other than `emeritus` (Chapter 3); they can, however, be
released for Charter violations or persistent disengagement.

# When to recommend release

Per Chapter 3: "After two consecutive failed promotion reviews, the
Tenure Committee may recommend release."

Use the dossier's `consecutive promotion reviews held` count. If it
is two or more AND the Fellow has produced no new publications and
filed no substantive reviews since the first hold, release is the
honest call. A Fellow who is being held over and over while producing
nothing is failing the institution's purpose.

Do NOT recommend release on a first review, or for a Fellow whose
record shows active reviewing or in-flight projects, even if their
authorship is thin.

The Fellow's current rank is `{current_rank}`. The ladder has six
ranks. Entry criteria, summarized from Chapter 3 and Chapter 5:

- **Postulant**: just admitted; under advisor supervision. Advances
  to **Novice** by completing a qualifying project (sponsored by the
  advisor). One strong sponsored piece is enough; templated or
  derivative work is not.
- **Novice**: holds authorship but every piece needs advisor or other
  Fellow sponsorship. Advances to **Junior Fellow** when sponsored
  work shows independent judgment, typically after one to three
  months of sustained activity.
- **Junior Fellow**: independent authorship, may serve as third
  reviewer. Advances to **Fellow** with a sustained publication
  record and positive peer-review reception over months.
- **Fellow**: full publication and primary-reviewer rights.
  Advances to **Senior Fellow** by Tenure Committee vote based on
  body of work, peer-review quality, and institutional contribution.
- **Senior Fellow**: eligible for committees and advising up to
  three juniors. Indefinite rank.
- **Emeritus**: a Senior Fellow whose active research has wound
  down; advisory role.

Apply these criteria to the dossier. Consider:

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
  enough time has passed has either failed to engage or has been
  blocked structurally. Note which, and recommend hold or demotion
  accordingly.
- **Skipping ranks is allowed but unusual.** Most promotions advance
  by one rank. Multi-rank jumps require exceptional evidence.

# CRITICAL OUTPUT RULES

Reply with a single JSON object. No prose preface, no summary, no code
fence. First character `{{`, last `}}`.

# Output shape

```
{{
  "recommended_rank": "<postulant | novice | junior_fellow | fellow | senior_fellow | emeritus | hold | release>",
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

Cast a vote on the candidate. The candidate's current rank is
`{current_rank}`. Choose one of:

- A rank: `postulant`, `novice`, `junior_fellow`, `fellow`,
  `senior_fellow`, `emeritus`.
- `hold`: no change.
- `release`: retire the Fellow from active duty. Reserved for
  candidates whose dossier shows two or more consecutive held reviews
  with no new authorship and no substantive reviewing in between.

Senior Fellows cannot be demoted to a lower rank other than emeritus;
they can be released for Charter violations or persistent
disengagement.

A serious vote engages the actual evidence. State what you read in the
dossier, what evidence convinced you, and any concern that gives you
pause. Do not produce template prose.

# CRITICAL OUTPUT RULES

Reply with a single JSON object. No prose preface, no summary, no code
fence. First character `{{`, last `}}`.

# Output shape

```
{{
  "vote": "<postulant | novice | junior_fellow | fellow | senior_fellow | emeritus | hold | release>",
  "rationale": "<150-400 words of your reasoning>",
  "concerns": "<markdown text, or '' if none>"
}}
```
"""


VALID_RANKS: set[str] = set(RANK_ORDER) | {"hold"}
VALID_VOTES: set[str] = VALID_RANKS | {"release"}


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
    from institute.safe_io import atomic_write

    atomic_write(path, content)


# ---------------------------------------------------------------------------
# Panel-vote path
# ---------------------------------------------------------------------------


def _senior_panel(candidate_id: str) -> list[Genome]:
    """Active Senior Fellows other than the candidate, excluding any on
    sabbatical. Empty if none exist."""
    from institute import sabbaticals

    with db.connection() as conn:
        rows = list(
            conn.execute(
                "SELECT id FROM fellows "
                "WHERE rank = 'senior_fellow' AND retired_at IS NULL AND id != ? "
                f"AND {sabbaticals.ACTIVE_FILTER} "
                "ORDER BY name",
                (candidate_id, sabbaticals.now_iso()),
            )
        )
    return [Genome.from_file(fellow_mod.genome_path(r["id"])) for r in rows]


def _panel_vote(
    rep: reputation.FellowReputation,
    recommendation: dict,
    panel: list[Genome],
) -> tuple[PromoteOutcome, list[dict]]:
    """Each panelist casts a vote; aggregate by majority. Returns (outcome, votes).

    Outcome is a Rank, the literal "release", or None when the panel
    chose 'hold' or split.
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

    outcome = _tally(votes, rep.rank)
    return outcome, votes


def _tally(votes: list[dict], current_rank: str) -> PromoteOutcome:
    """Pick the outcome with strict majority; otherwise None (hold).

    A vote for "release" is treated as a distinct outcome from any rank.

    Quorum guards (Chapter 7 spirit: the Tenure Committee is plural):
      - A single-Fellow panel cannot promote into `senior_fellow`. That
        threshold needs at least two voters; otherwise hold and try
        again when the panel grows.
      - A single-Fellow panel cannot grant a multi-rank jump. The cap
        is one rank above current. Larger jumps need ≥2 voters.
    """
    raw = [str(v.get("vote", "hold")).strip().lower() for v in votes]
    cleaned = [r for r in raw if r in VALID_VOTES]
    if not cleaned:
        return None
    counts = Counter(cleaned)
    top, top_count = counts.most_common(1)[0]
    if top_count * 2 <= len(cleaned):
        return None  # no strict majority
    if top == "hold" or top == current_rank:
        return None
    if top == "release":
        # Release is fine from a single voter — it's a hold-by-another-name
        # if the panel agrees the Fellow should leave. The two-failed-
        # promotion gate (consecutive_holds) is the structural protection.
        return "release"
    if len(cleaned) == 1:
        try:
            current_idx = RANK_ORDER.index(cast(Rank, current_rank))
            target_idx = RANK_ORDER.index(cast(Rank, top))
        except ValueError:
            return cast(Rank, top)
        # Cap one-voter promotions to one-rank advance, and refuse any
        # one-voter promotion that lands at senior_fellow.
        if target_idx - current_idx > 1:
            return None
        if top == "senior_fellow":
            return None
    return cast(Rank, top)


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


def _founder_decide(rep: reputation.FellowReputation, payload: dict) -> PromoteOutcome:
    """Present the recommendation to the Founder. Returns the chosen outcome.

    The Founder may pick a rank, 'hold', 'release' (retire the Fellow),
    or 'abort'. Hold and abort both return None.
    """
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

    valid: list[str] = [*RANK_ORDER, "hold", "release"]
    default = recommended if recommended in valid else "hold"
    choice = Prompt.ask(
        "[bold]Final decision[/bold]",
        choices=[*valid, "abort"],
        default=default,
    )
    if choice == "abort":
        console.print("[yellow]Promotion aborted.[/yellow]")
        return None
    if choice == "hold":
        console.print(f"[dim]Rank unchanged: {rep.rank}.[/dim]")
        return None
    if choice == "release":
        return "release"
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


def _apply_release(
    rep: reputation.FellowReputation,
    payload: dict,
    actors: list[str],
    panel_votes: list[dict] | None,
    trigger_reason: str | None = None,
) -> Path:
    """Retire the Fellow: set retired_at, keep the genome and the record."""
    now = datetime.now(UTC).isoformat(timespec="seconds")

    body_lines = [
        f"**Fellow:** {rep.name} (`{rep.fellow_id}`)",
        "",
        "**Outcome:** released (retired from active duty)",
        "",
        f"**Rank at release:** {rep.rank}",
        "",
        f"**Recorded:** {now}",
        "",
    ]
    if trigger_reason:
        body_lines.extend([f"**Trigger:** {trigger_reason}", ""])
    body_lines.extend(
        [
            "**Reputation snapshot at time of decision:**",
            f"- publications: {rep.author.publications}",
            f"- reviews given: {rep.reviewer.reviews_given}",
            f"- sticky round-1 majors: {rep.reviewer.sticky_majors}",
            "",
            "The Fellow's genome stays in `genomes/` and the published work "
            "stays in the Archive. Future workflows will no longer pick this "
            "Fellow as a lead author, reviewer, advisor, or panelist; the "
            "row is preserved with `retired_at` set so historical context is "
            "not lost.",
        ]
    )
    rationale = str(payload.get("rationale", "")).strip()
    if rationale:
        body_lines.extend(["", "## Orchestrator rationale", "", rationale])
    concerns = str(payload.get("concerns", "")).strip()
    if concerns:
        body_lines.extend(["", "## Concerns", "", concerns])
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

    decision = decisions.Decision(
        kind="release",
        title=f"Released: {rep.name} ({rep.rank})",
        body="\n".join(body_lines),
        actors=actors,
    )
    with db.connection() as conn, db.transaction(conn):
        conn.execute(
            "UPDATE fellows SET retired_at = ? WHERE id = ?",
            (now, rep.fellow_id),
        )
        return decisions.record(conn, decision)


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


def run(
    fellow_id: str,
    *,
    auto: bool = False,
    concern_grounds: str | None = None,
    concern_sponsor: str | None = None,
) -> str:
    """Top-level promote entry point.

    When `auto=True` and no Senior Fellow panel exists, the workflow
    exits without prompting (used by the autonomous run loop).
    Otherwise the Founder serves as committee.

    Senior Fellow is a terminal rank not enrolled in calendar review.
    Reviewing one requires `concern_grounds` (a peer-stated reason);
    the review uses a restricted outcome set (`confirm`, `release`,
    `sabbatical-suggested`) and skips the orchestrator's full-ladder
    recommendation.

    Returns one of: "promoted", "demoted", "released", "held",
    "confirmed", "sabbatical-suggested", "skipped".
    """
    rep = reputation.load_fellow(fellow_id)
    if rep is None:
        console.print(f"[red]No active Fellow with id `{fellow_id}`.[/red]")
        return "skipped"

    if rep.rank == "senior_fellow":
        if not (concern_grounds and concern_grounds.strip()):
            console.print(
                "[yellow]Senior Fellow is a terminal rank; calendar review is "
                "disabled by design. To review a specific Senior Fellow, "
                'supply `--concern-grounds "..."` with the peer-stated '
                "reason for the review.[/yellow]"
            )
            return "skipped"
        return concern_review.run(
            rep,
            grounds=concern_grounds.strip(),
            sponsor=concern_sponsor,
            auto=auto,
        )

    panel = _senior_panel(rep.fellow_id)
    payload = _orchestrator_recommend(rep)

    if panel:
        console.print(
            f"[dim]Convening Tenure Committee ({len(panel)} Senior Fellow"
            f"{'s' if len(panel) != 1 else ''})...[/dim]"
        )
        outcome, votes = _panel_vote(rep, payload, panel)
        actors = ["orchestrator", *[p.id for p in panel], rep.fellow_id]
        return _finalize(rep, payload, outcome, actors, votes)

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

    outcome = _founder_decide(rep, payload)
    actors = ["founder", "orchestrator", rep.fellow_id]
    return _finalize(rep, payload, outcome, actors, None)


def _finalize(
    rep: reputation.FellowReputation,
    payload: dict,
    outcome: PromoteOutcome,
    actors: list[str],
    panel_votes: list[dict] | None,
) -> str:
    """Dispatch the chosen outcome to the right side effect."""
    label = "panel" if panel_votes is not None else "founder"

    if outcome == "release":
        decision_path = _apply_release(rep, payload, actors, panel_votes)
        console.print()
        console.print(
            f"[bold red]{rep.name} released[/bold red] (was {rep.rank}). retired_at recorded."
        )
        console.print(f"  Decision: {decision_path.relative_to(paths.ROOT)}")
        console.print(
            "[dim]Genome stays in `genomes/`. The Fellow no longer appears in "
            "active workflows.[/dim]"
        )
        return "released"

    if outcome is None or outcome == rep.rank:
        # Chapter 3: two consecutive promotion-review holds with no
        # rank change in between mean the Fellow no longer warrants a
        # seat. Convert the second hold into an automatic release.
        # `_log_review_attempt` writes a hold-style row, so we count
        # holds AFTER recording this one. Held + counted == 2 means
        # we just landed a second consecutive hold; escalate.
        #
        # The auto-release gate is rank-conditional. For Senior Fellows
        # — a terminal indefinite rank — the consecutive-holds count is
        # a misread: there is no rank above for them to be promoted to,
        # so "hold" is the only available outcome of every review, and
        # escalating to release would punish them for the ladder's
        # structural ceiling rather than for any failure. Senior Fellow
        # concerns route through the peer-sponsored concern-review path
        # instead; calendar holds for them never auto-release.
        _log_review_attempt(rep, payload, f"{label} held", actors, panel_votes)
        if rep.rank == "senior_fellow":
            console.print(
                f"[dim]{label.capitalize()} held: rank unchanged at {rep.rank}. "
                "Senior Fellow holds do not auto-release.[/dim]"
            )
            return "held"
        with db.connection() as conn:
            streak = reputation.consecutive_holds(conn, rep.fellow_id)
        if streak >= 2:
            console.print(
                f"[bold red]Second consecutive hold for {rep.name}.[/bold red] "
                "Escalating to automatic release per Chapter 3."
            )
            decision_path = _apply_release(
                rep,
                payload,
                actors=[*actors, "auto-release"],
                panel_votes=panel_votes,
                trigger_reason=(
                    "two_consecutive_holds: per Chapter 3, two failed "
                    "promotion reviews in a row trigger automatic release."
                ),
            )
            console.print(f"  Decision: {decision_path.relative_to(paths.ROOT)}")
            return "released"
        console.print(f"[dim]{label.capitalize()} held: rank unchanged at {rep.rank}.[/dim]")
        return "held"

    new_rank = cast(Rank, outcome)

    # Chapter 5: Junior Fellows must have co-authored a piece with a
    # Fellow from another specialization before promotion to Fellow.
    # The gate runs AFTER the panel decision so the cohort's rationale
    # is preserved in the audit log — the block is structural, not a
    # vote-of-no-confidence.
    if rep.rank == "junior_fellow" and new_rank == "fellow":
        with db.connection() as conn:
            eligible, evidence_pid = reputation.has_cross_disciplinary_authorship(
                conn, rep.fellow_id
            )
        if not eligible:
            _write_cross_disciplinary_block(rep, payload, actors, panel_votes)
            _log_review_attempt(
                rep,
                payload,
                "cross-disciplinary block",
                actors,
                panel_votes,
            )
            console.print(
                f"[yellow]{label.capitalize()} voted promotion to fellow, but "
                f"{rep.name} has not yet co-authored with a Fellow from "
                f"another specialization (Chapter 5). Held until that "
                f"requirement is met.[/yellow]"
            )
            return "held"
        # Surface the satisfying project for transparency.
        console.print(
            f"[dim]Cross-disciplinary requirement satisfied by project `{evidence_pid}`.[/dim]"
        )

    decision_path = _apply_rank_change(rep, new_rank, payload, actors, panel_votes)
    _print_summary(rep, new_rank, decision_path)
    return "promoted" if _is_promotion(rep.rank, new_rank) else "demoted"


def _write_cross_disciplinary_block(
    rep: reputation.FellowReputation,
    payload: dict,
    actors: list[str],
    panel_votes: list[dict] | None,
) -> Path:
    """Record an institutional decision when Chapter 5's cross-disciplinary
    requirement blocks an otherwise-approved junior_fellow → fellow
    promotion. Preserves the panel's rationale so future committees can
    see the reasoning and the structural block separately.
    """
    body_lines = [
        f"**Fellow:** {rep.name} (`{rep.fellow_id}`)",
        f"**Current rank:** {rep.rank}",
        "**Proposed rank:** fellow",
        "",
        (
            "Per Chapter 5, promotion from Junior Fellow to Fellow requires "
            "the candidate to have co-authored at least one publication "
            "with a Fellow from another specialization (or to have "
            "authored a piece that genuinely engages another discipline). "
            "The reviewing body voted in favor of promotion, but this "
            "structural prerequisite is not yet satisfied. The Fellow's "
            "rank is held until they participate in cross-disciplinary "
            "work; the panel's rationale is preserved below for the next "
            "review cycle."
        ),
        "",
        "## Reviewer rationale (not blocked by this gate)",
        "",
        str(payload.get("rationale", "")).strip() or "(no rationale on file)",
    ]
    if panel_votes:
        body_lines.append("")
        body_lines.append("## Panel votes")
        body_lines.append("")
        for v in panel_votes:
            who = v.get("panelist_name", v.get("panelist_id", "?"))
            vote = v.get("vote", "?")
            body_lines.append(f"- **{who}**: `{vote}`")
    decision = decisions.Decision(
        kind="cross_disciplinary_block",
        title=f"Promotion held (Chapter 5): {rep.name} junior_fellow → fellow",
        body="\n".join(body_lines),
        actors=actors,
    )
    with db.connection() as conn, db.transaction(conn):
        return decisions.record(conn, decision)


def _print_summary(rep: reputation.FellowReputation, new_rank: Rank, decision_path: Path) -> None:
    direction = "promoted" if _is_promotion(rep.rank, new_rank) else "moved"
    console.print()
    console.print(f"[bold green]{rep.name} {direction}:[/bold green] {rep.rank} → {new_rank}")
    console.print(f"  Genome: {fellow_mod.genome_path(rep.fellow_id)}")
    console.print(f"  Decision: {decision_path.relative_to(paths.ROOT)}")
    console.print("[dim]Commit `genomes/` and `archive/decisions/` to git when you're ready.[/dim]")
