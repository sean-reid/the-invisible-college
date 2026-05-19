"""Editorial Board review: the final accept/reject call when reviewers disagree.

Per Chapter 7, the Editorial Board intervenes when peer reviewers
disagree on whether a piece is ready to publish. Triggered by
`peer_review._transition_after_all_reviews` when round-2 produces a
`reject` recommendation or any flagged dissent.

Two execution paths:

  - **Board vote.** If at least one Senior Fellow is on the Board, the
    Board reads the draft, every review, and the dissents, and votes
    accept or reject. Strict majority decides; ties favor reject (the
    same safe-by-default rule andon uses).
  - **Founder fallback.** Until the Board has a Senior Fellow, the
    Founder serves as committee. Used while the institution is young.

On accept the project advances to EDITORIAL and publishes with the
dissenting review(s) shown alongside in the Apparatus footer. On
reject the project moves to REJECTED.
"""

from __future__ import annotations

import json
from datetime import UTC, datetime
from pathlib import Path

from rich.console import Console
from rich.panel import Panel
from rich.prompt import Prompt

from institute import claude_runner, db, decisions, editorial_board, parsing, paths, state
from institute.claude_runner import FellowTask
from institute.fellow import Genome
from institute.state import State

console = Console()


BOARD_BRIEF = """\
You are serving on the Editorial Board of the Invisible College.
Round-2 peer review on this submission produced disagreement — at
least one reviewer recommended reject, or a reviewer filed a dissent.
The Board's job is to read everything and make the final call.

# Inputs in your workspace

- `draft.md`     the revised draft (round-2 version).
- `reviews.md`   every signed review across both rounds, concatenated.
- `dissents.md`  the dissenting review(s), if any, broken out for
                 emphasis. Empty file if no dissent was filed.

Read all three with the Read tool. Also consult `docs/07-peer-review.md`
for the Board's standards.

# Your vote

Choose `accept` or `reject`.

- `accept`: the piece is good enough to publish despite the
  disagreement. The dissenting review will appear next to it on the
  blog so readers can see the contest. The College publishes
  disagreement honestly rather than smoothing it.
- `reject`: the disagreement reflects a real problem the piece does
  not resolve. The lead Fellow does not get another revision; the
  project is closed and the work is preserved in the Archive as a
  record of what was tried.

A serious vote engages the actual evidence. Cite the dissent's
strongest point if you vote accept; cite the missing thing if you
vote reject.

# CRITICAL OUTPUT RULES

Reply with a single JSON object. No prose preface, no summary, no
code fence. First character `{{`, last `}}`.

# Output shape

```
{{
  "vote": "<accept|reject>",
  "rationale": "<150-400 words of reasoning>",
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
    """Return (title, draft_md, reviews_md, dissents_md)."""
    with db.connection() as conn:
        proj = conn.execute(
            "SELECT title, draft_path FROM projects WHERE id = ?",
            (project_id,),
        ).fetchone()
        if proj is None:
            raise SystemExit(f"No such project: {project_id}")
        title = proj["title"]
        draft_md = (paths.ROOT / proj["draft_path"]).read_text(encoding="utf-8")
        review_rows = list(
            conn.execute(
                "SELECT r.reviewer_id, r.role, r.recommendation, r.round, "
                "       r.content_path, r.dissent, f.name AS reviewer_name "
                "FROM reviews r LEFT JOIN fellows f ON f.id = r.reviewer_id "
                "WHERE r.project_id = ? ORDER BY r.round, r.role",
                (project_id,),
            )
        )

    review_lines = ["# All reviews on this submission", ""]
    dissent_lines = ["# Dissents", ""]
    any_dissent = False
    for r in review_rows:
        path = paths.ROOT / r["content_path"]
        if not path.is_file():
            continue
        body = path.read_text(encoding="utf-8")
        header = (
            f"## Round {r['round']} — {r['reviewer_name'] or r['reviewer_id']} "
            f"({r['role']}) — `{r['recommendation']}`" + (" — **DISSENT**" if r["dissent"] else "")
        )
        review_lines.append(header)
        review_lines.append("")
        review_lines.append(body)
        review_lines.append("")
        if r["dissent"]:
            any_dissent = True
            dissent_lines.append(header)
            dissent_lines.append("")
            dissent_lines.append(body)
            dissent_lines.append("")
    if not any_dissent:
        dissent_lines.append(
            "_(No dissenting review was filed. The "
            "Board was convened on a `reject` "
            "recommendation instead.)_"
        )
    return title, draft_md, "\n".join(review_lines), "\n".join(dissent_lines)


def _board_vote(project_id: str, members: list[Genome]) -> tuple[str, list[dict]]:
    """Each Board member casts a vote. Returns (outcome, votes).

    Outcome is "accept", "reject", or "hold" (tie → safe default reject).
    """
    base = paths.ARCHIVE / "editorial-reviews" / project_id
    base.mkdir(parents=True, exist_ok=True)
    _, draft_md, reviews_md, dissents_md = _load_project_context(project_id)

    votes: list[dict] = []
    for member in members:
        ws = paths.FELLOWS / member.id / "workspace" / f"editorial-{project_id}"
        ws.mkdir(parents=True, exist_ok=True)
        _stage(ws / "draft.md", draft_md)
        _stage(ws / "reviews.md", reviews_md)
        _stage(ws / "dissents.md", dissents_md)

        console.print(f"[dim]Board member {member.name} is reviewing...[/dim]")
        result = claude_runner.invoke(
            FellowTask(
                genome=member,
                project_id=project_id,
                step="editorial-vote",
                brief=BOARD_BRIEF,
                workspace=ws,
                extra_dirs=(paths.DOCS,),
            )
        )
        vote_payload = parsing.parse_json_or_dump(
            result.result_text,
            dump_path=ws / "raw-vote.txt",
            context=f"Editorial vote from {member.id} on {project_id}",
        )
        vote_payload["member_id"] = member.id
        vote_payload["member_name"] = member.name
        votes.append(vote_payload)
        _stage(base / f"vote-{member.id}.json", json.dumps(vote_payload, indent=2))

    raw = [str(v.get("vote", "")).strip().lower() for v in votes]
    accept = sum(1 for r in raw if r == "accept")
    reject = sum(1 for r in raw if r == "reject")
    if accept > reject:
        return "accept", votes
    return "reject", votes


def _founder_decide(project_id: str) -> str:
    """Founder reads the draft and dissents in the terminal, picks accept/reject."""
    title, _, _, dissents_md = _load_project_context(project_id)
    console.print()
    console.print(
        Panel.fit(
            f"[bold]Editorial Board review[/bold] on `{project_id}`\n[dim]title:[/dim] {title}",
            border_style="cyan",
        )
    )
    console.print(
        Panel(
            f"Read the full draft at archive/drafts/{project_id}/draft.md.\n"
            f"All reviews are at archive/reviews/{project_id}/.\n"
            f"Editorial workspace: archive/editorial-reviews/{project_id}/",
            title="Reading paths",
            border_style="dim",
        )
    )
    if "_(No dissenting review" not in dissents_md:
        console.print(Panel(dissents_md, title="Dissents", border_style="yellow"))
    return Prompt.ask(
        "[bold]Editorial decision[/bold]",
        choices=["accept", "reject", "abort"],
        default="accept",
    )


def _apply_outcome(
    project_id: str,
    title: str,
    outcome: str,
    actors: list[str],
    votes: list[dict] | None,
) -> None:
    target = State.EDITORIAL if outcome == "accept" else State.REJECTED
    body_lines = [
        f"**Project:** {project_id}",
        "",
        f"**Outcome:** `{outcome}` (state → `{target.value}`)",
        "",
        f"**Recorded:** {datetime.now(UTC).isoformat(timespec='seconds')}",
    ]
    if votes:
        body_lines.extend(["", "## Board votes", ""])
        for v in votes:
            body_lines.append(
                f"### {v.get('member_name', v.get('member_id', '?'))}: `{v.get('vote', '?')}`"
            )
            rat = str(v.get("rationale", "")).strip()
            if rat:
                body_lines.extend(["", rat])
            con = str(v.get("concerns", "")).strip()
            if con:
                body_lines.extend(["", f"_Concerns:_ {con}"])
            body_lines.append("")

    decision = decisions.Decision(
        kind="editorial_ruling",
        title=f"Editorial ruling ({outcome}): {title}",
        body="\n".join(body_lines),
        actors=actors,
        related_project=project_id,
    )
    with db.connection() as conn, db.transaction(conn):
        state.transition(conn, project_id, target)
        decisions.record(conn, decision)

    # Calibration accounting. The Board's ruling is the ground truth.
    # Any round-2 reviewer whose recommendation diverges from the
    # ruling takes a calibration_miss mark. This is the symmetric
    # signal to the andon dismiss → frivolous_andon mark above.
    _record_calibration_marks(project_id, title, outcome)

    style = "green" if outcome == "accept" else "red"
    console.print()
    console.print(
        f"[bold {style}]Editorial Board {outcome}ed.[/bold {style}] "
        f"Project {project_id} → {target.value}"
    )


def _record_calibration_marks(project_id: str, title: str, outcome: str) -> None:
    """Mark round-2 reviewers whose recommendation diverged from the Board.

    A reviewer who recommended `accept` on a piece the Board rejected,
    or `reject` on a piece the Board accepted, takes a
    calibration_miss mark. `minor` and `major` are interpreted as
    leaning-accept (publishable with revisions) and counted as
    consistent with an accept ruling.
    """
    from institute import reviewer_eligibility

    with db.connection() as conn:
        rows = list(
            conn.execute(
                "SELECT id AS review_id, reviewer_id, recommendation "
                "FROM reviews WHERE project_id = ? AND round = 2",
                (project_id,),
            )
        )

    for row in rows:
        rec = (row["recommendation"] or "").strip().lower()
        reviewer_voted_for_publication = rec in {"accept", "minor", "major"}
        if outcome == "accept" and not reviewer_voted_for_publication:
            mismatch = True
        elif outcome == "reject" and reviewer_voted_for_publication:
            mismatch = True
        else:
            mismatch = False
        if not mismatch:
            continue
        reason = (
            f"Editorial Board {outcome}ed `{project_id}` ({title}); reviewer recommended `{rec}`."
        )
        reviewer_eligibility.safe_record(
            fellow_id=row["reviewer_id"],
            kind="calibration_miss",
            reason=reason,
            related_project=project_id,
            related_review_id=row["review_id"],
        )


def run(project_id: str) -> None:
    """Dispatch the editorial review. Called from `institute next`."""
    with db.connection() as conn:
        proj = conn.execute(
            "SELECT title, state FROM projects WHERE id = ?", (project_id,)
        ).fetchone()
        if proj is None:
            raise SystemExit(f"No such project: {project_id}")
        if proj["state"] != State.EDITORIAL_REVIEW.value:
            raise SystemExit(
                f"Project {project_id} is in state {proj['state']}, expected editorial_review."
            )
        title = proj["title"]
        members = editorial_board.current_members(conn)

    if members:
        console.print(
            f"[dim]Convening Editorial Board ({len(members)} member"
            f"{'s' if len(members) != 1 else ''})...[/dim]"
        )
        outcome, votes = _board_vote(project_id, members)
        actors = ["editorial-board", *[m.id for m in members]]
        _apply_outcome(project_id, title, outcome, actors, votes)
        return

    choice = _founder_decide(project_id)
    if choice == "abort":
        console.print("[yellow]Aborted; project stays in editorial_review.[/yellow]")
        return
    _apply_outcome(project_id, title, choice, ["founder"], None)
