"""Senior Fellow concern review: peer-sponsored, grounds-required.

Senior Fellow is the College's terminal indefinite rank. Per the
intent that tenure protects academic freedom, Senior Fellows are NOT
enrolled in calendar-triggered tenure review — that pattern would
quietly subvert the academic-freedom logic by keeping every Fellow's
standing perpetually up for committee evaluation.

This module is the peer-sponsored alternative. A Fellow (the sponsor)
files concrete grounds for a review; the panel reads the dossier and
the grounds and chooses one of three restricted outcomes:

- `confirm`: the concern does not warrant action; the Senior Fellow's
  standing is unchanged, and the record positively states confirmation
  (not the misleading `hold` of the old calendar path).
- `sabbatical-suggested`: the panel recommends the Senior Fellow take
  a sabbatical. No automatic action — the recommendation is surfaced
  to the Fellow and the Founder via the decision record.
- `release`: extreme outcome reserved for severe disengagement,
  Charter violation, or comparable cause. Same effect as elsewhere:
  `retired_at` is set, the genome and Archive remain.

There is no `promote` and no `demote` outcome. Senior Fellow is the
terminal rank, and demotion below it is excluded by Chapter 3.
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
from institute.claude_runner import FellowTask
from institute.fellow import Genome

console = Console()


ConcernOutcome = Literal["confirm", "release", "sabbatical-suggested"]


VALID_OUTCOMES: set[str] = {"confirm", "release", "sabbatical-suggested"}


PANELIST_BRIEF = """\
You are serving on a peer-sponsored concern review for a Senior Fellow
of the Invisible College.

Senior Fellow is a terminal indefinite rank. Reviewing it is unusual:
this review happens only because a fellow Scholar has filed concrete
grounds for re-examining the Fellow's standing. Routine calendar
review of Senior Fellows is disabled by design — academic freedom
depends on the rank being indefinite once earned.

Your outcome is restricted to one of three options. You cannot demote
this Fellow; you cannot promote them further. You can only confirm
their standing, suggest a sabbatical, or — in severe cases — release
them.

# Inputs in your working directory

- `dossier.md`         the Fellow's authorship and reviewer signals.
- `grounds.md`         the sponsor's stated reason for this review.
- `archive-index.md`   every piece the College has published.
- `cohort.md`          the rest of the cohort for context.

Read these with the Read tool. The rank ladder is defined in
`docs/03-fellows.md`. The bar for release is severe: persistent
disengagement, Charter violation, or comparable cause. Routine
quietness is not grounds.

# Outcomes

Choose one of:

- `confirm`: the concern does not warrant action. The Fellow's
  standing as a Senior Fellow is intact. Pick this when the sponsor's
  grounds are not, on reading the record, supported.
- `sabbatical-suggested`: the Fellow's recent activity profile
  suggests they would benefit from a sabbatical. No automatic action
  follows; the recommendation is recorded and the Fellow may take it.
- `release`: severe outcome. Pick this only if the dossier and
  grounds together establish that the Fellow has substantively
  disengaged from the College or breached the Charter.

A serious vote engages the actual evidence. State what you read in
the dossier, what evidence convinced you, and what (if anything) the
sponsor's grounds added. Do not produce template prose.

# CRITICAL OUTPUT RULES

Reply with a single JSON object. No prose preface, no summary, no
code fence. First character `{`, last `}`.

# Output shape

```
{
  "vote": "<confirm | release | sabbatical-suggested>",
  "rationale": "<150-400 words of your reasoning>",
  "concerns": "<markdown text, or '' if none>"
}
```
"""


def _stage(path: Path, content: str) -> None:
    from institute.safe_io import atomic_write

    atomic_write(path, content)


def _senior_panel(candidate_id: str) -> list[Genome]:
    """Active Senior Fellows other than the candidate, off-sabbatical."""
    from institute import fellow as fellow_mod
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


def _render_grounds(grounds: str, sponsor: str | None) -> str:
    lines = ["# Sponsor's stated grounds", ""]
    if sponsor:
        lines.append(f"**Sponsoring Fellow:** `{sponsor}`")
        lines.append("")
    lines.append(grounds.strip())
    return "\n".join(lines) + "\n"


def _panel_vote(
    rep: reputation.FellowReputation,
    grounds: str,
    sponsor: str | None,
    panel: list[Genome],
) -> tuple[ConcernOutcome | None, list[dict]]:
    """Each panelist casts a vote on the restricted outcome set."""
    base = paths.ARCHIVE / "concern-reviews" / rep.fellow_id
    base.mkdir(parents=True, exist_ok=True)
    cohort = reputation.load_cohort()
    grounds_md = _render_grounds(grounds, sponsor)

    votes: list[dict] = []
    for panelist in panel:
        ws = paths.FELLOWS / panelist.id / "workspace" / f"concern-{rep.fellow_id}"
        ws.mkdir(parents=True, exist_ok=True)
        _stage(ws / "dossier.md", reputation.render_fellow_dossier(rep))
        _stage(ws / "grounds.md", grounds_md)
        _stage(ws / "archive-index.md", archive_index.render())
        _stage(ws / "cohort.md", reputation.render_cohort_brief(cohort))

        console.print(f"[dim]Panelist {panelist.name} is reviewing the concern...[/dim]")
        result = claude_runner.invoke(
            FellowTask(
                genome=panelist,
                project_id=f"concern-{rep.fellow_id}",
                step="concern-review",
                brief=PANELIST_BRIEF,
                workspace=ws,
                extra_dirs=(paths.DOCS,),
            )
        )
        vote_payload = parsing.parse_json_or_dump(
            result.result_text,
            dump_path=ws / "raw-vote.txt",
            context=f"Concern-review vote from {panelist.id} on {rep.fellow_id}",
        )
        vote_payload["panelist_id"] = panelist.id
        vote_payload["panelist_name"] = panelist.name
        votes.append(vote_payload)
        _stage(base / f"vote-{panelist.id}.json", json.dumps(vote_payload, indent=2))

    return _tally(votes), votes


def _tally(votes: list[dict]) -> ConcernOutcome | None:
    """Pick the outcome with strict majority; otherwise None (confirm).

    `release` requires strict majority; ties or splits fall back to
    `confirm` (the safe default — Senior Fellow standing should not
    be removed on a split panel).
    """
    raw = [str(v.get("vote", "")).strip().lower() for v in votes]
    cleaned = [r for r in raw if r in VALID_OUTCOMES]
    if not cleaned:
        return None
    counts = Counter(cleaned)
    top, top_count = counts.most_common(1)[0]
    if top_count * 2 <= len(cleaned):
        return None
    return cast(ConcernOutcome, top)


def _founder_decide(rep: reputation.FellowReputation, grounds: str) -> ConcernOutcome | None:
    """Founder fallback when no panel can convene."""
    console.print()
    console.print(
        Panel.fit(
            f"[bold]{rep.name}[/bold]  ({rep.fellow_id})\n"
            f"[dim]rank:[/dim] senior_fellow (terminal, indefinite)\n",
            title="Senior Fellow concern review",
            border_style="cyan",
        )
    )
    console.print(Panel(grounds.strip(), title="Sponsor's grounds", border_style="yellow"))
    valid = ["confirm", "release", "sabbatical-suggested", "abort"]
    choice = Prompt.ask("[bold]Decision[/bold]", choices=valid, default="confirm")
    if choice == "abort":
        console.print("[yellow]Concern review aborted.[/yellow]")
        return None
    return cast(ConcernOutcome, choice)


def _record_confirm(
    rep: reputation.FellowReputation,
    grounds: str,
    sponsor: str | None,
    actors: list[str],
    votes: list[dict] | None,
) -> Path:
    """Positive-outcome record: Senior Fellow standing confirmed."""
    now = datetime.now(UTC).isoformat(timespec="seconds")
    body = [
        f"**Fellow:** {rep.name} (`{rep.fellow_id}`)",
        "",
        "**Outcome:** confirmed (Senior Fellow standing intact)",
        "",
        f"**Recorded:** {now}",
        "",
        "## Sponsor's grounds",
        "",
    ]
    if sponsor:
        body.append(f"**Sponsoring Fellow:** `{sponsor}`")
        body.append("")
    body.append(grounds.strip())
    if votes:
        body.extend(["", "## Panel votes", ""])
        for v in votes:
            body.append(
                f"- **{v.get('panelist_name', v.get('panelist_id', '?'))}** voted "
                f"`{v.get('vote', '?')}`"
            )
    decision = decisions.Decision(
        kind="senior_fellow_confirmed",
        title=f"{rep.name}: Senior Fellow standing confirmed",
        body="\n".join(body),
        actors=actors,
    )
    with db.connection() as conn, db.transaction(conn):
        return decisions.record(conn, decision)


def _record_sabbatical_suggestion(
    rep: reputation.FellowReputation,
    grounds: str,
    sponsor: str | None,
    actors: list[str],
    votes: list[dict] | None,
) -> Path:
    """Recommendation that the Senior Fellow take a sabbatical."""
    now = datetime.now(UTC).isoformat(timespec="seconds")
    body = [
        f"**Fellow:** {rep.name} (`{rep.fellow_id}`)",
        "",
        "**Outcome:** sabbatical suggested",
        "",
        f"**Recorded:** {now}",
        "",
        (
            "The panel reviewed the sponsor's grounds and concluded that the "
            "Fellow would benefit from a sabbatical. No automatic action is "
            "taken; the suggestion is recorded for the Fellow and the Founder "
            "to consider. The Fellow's rank and standing are unchanged."
        ),
        "",
        "## Sponsor's grounds",
        "",
    ]
    if sponsor:
        body.append(f"**Sponsoring Fellow:** `{sponsor}`")
        body.append("")
    body.append(grounds.strip())
    if votes:
        body.extend(["", "## Panel votes", ""])
        for v in votes:
            body.append(
                f"- **{v.get('panelist_name', v.get('panelist_id', '?'))}** voted "
                f"`{v.get('vote', '?')}`"
            )
    decision = decisions.Decision(
        kind="sabbatical_suggested",
        title=f"{rep.name}: sabbatical suggested",
        body="\n".join(body),
        actors=actors,
    )
    with db.connection() as conn, db.transaction(conn):
        return decisions.record(conn, decision)


def _record_release(
    rep: reputation.FellowReputation,
    grounds: str,
    sponsor: str | None,
    actors: list[str],
    votes: list[dict] | None,
) -> Path:
    """Retire the Senior Fellow following a concern-review release."""
    now = datetime.now(UTC).isoformat(timespec="seconds")
    body = [
        f"**Fellow:** {rep.name} (`{rep.fellow_id}`)",
        "",
        "**Outcome:** released (retired from active duty)",
        "",
        "**Rank at release:** senior_fellow",
        "",
        f"**Recorded:** {now}",
        "",
        (
            "**Trigger:** peer-sponsored concern review. The bar for releasing "
            "a Senior Fellow is severe, and the panel found it met."
        ),
        "",
        "## Sponsor's grounds",
        "",
    ]
    if sponsor:
        body.append(f"**Sponsoring Fellow:** `{sponsor}`")
        body.append("")
    body.append(grounds.strip())
    if votes:
        body.extend(["", "## Panel votes", ""])
        for v in votes:
            body.append(
                f"### {v.get('panelist_name', v.get('panelist_id', '?'))}: `{v.get('vote', '?')}`"
            )
            rat = str(v.get("rationale", "")).strip()
            if rat:
                body.extend(["", rat])
            body.append("")
    decision = decisions.Decision(
        kind="release",
        title=f"Released: {rep.name} (senior_fellow)",
        body="\n".join(body),
        actors=actors,
    )
    with db.connection() as conn, db.transaction(conn):
        conn.execute("UPDATE fellows SET retired_at = ? WHERE id = ?", (now, rep.fellow_id))
        return decisions.record(conn, decision)


def run(
    rep: reputation.FellowReputation,
    *,
    grounds: str,
    sponsor: str | None,
    auto: bool = False,
) -> str:
    """Execute a Senior Fellow concern review.

    Called from `promote.run()` when the target is a Senior Fellow and
    `concern_grounds` is supplied. Returns the same string vocabulary
    as `promote.run()`: "confirmed", "released", "sabbatical-suggested",
    or "skipped".
    """
    panel = _senior_panel(rep.fellow_id)

    if panel:
        console.print(
            f"[dim]Convening Concern Review panel ({len(panel)} Senior Fellow"
            f"{'s' if len(panel) != 1 else ''})...[/dim]"
        )
        outcome, votes = _panel_vote(rep, grounds, sponsor, panel)
        actors = ["orchestrator", *[p.id for p in panel], rep.fellow_id]
        if sponsor:
            actors.append(sponsor)
        return _apply(rep, grounds, sponsor, outcome, actors, votes)

    if auto:
        console.print(
            "[yellow]No peer panel available for concern review; auto-mode "
            "deferred. Run with `institute promote --fellow "
            f'{rep.fellow_id} --concern-grounds "..."` to decide manually.'
            "[/yellow]"
        )
        return "skipped"

    outcome = _founder_decide(rep, grounds)
    actors = ["founder", rep.fellow_id]
    if sponsor:
        actors.append(sponsor)
    return _apply(rep, grounds, sponsor, outcome, actors, None)


def _apply(
    rep: reputation.FellowReputation,
    grounds: str,
    sponsor: str | None,
    outcome: ConcernOutcome | None,
    actors: list[str],
    votes: list[dict] | None,
) -> str:
    if outcome == "release":
        path = _record_release(rep, grounds, sponsor, actors, votes)
        console.print()
        console.print(f"[bold red]{rep.name} released[/bold red] (was senior_fellow).")
        console.print(f"  Decision: {path.relative_to(paths.ROOT)}")
        return "released"
    if outcome == "sabbatical-suggested":
        path = _record_sabbatical_suggestion(rep, grounds, sponsor, actors, votes)
        console.print()
        console.print(f"[cyan]Sabbatical suggested[/cyan] for {rep.name}.")
        console.print(f"  Decision: {path.relative_to(paths.ROOT)}")
        return "sabbatical-suggested"
    # confirm (or None on a split panel) → confirm
    path = _record_confirm(rep, grounds, sponsor, actors, votes)
    console.print()
    console.print(f"[green]{rep.name}'s Senior Fellow standing confirmed.[/green]")
    console.print(f"  Decision: {path.relative_to(paths.ROOT)}")
    return "confirmed"


__all__ = [
    "VALID_OUTCOMES",
    "ConcernOutcome",
    "run",
]
