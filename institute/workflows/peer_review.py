"""Peer review workflow.

Three Fellows (or as many as are available, minimum two) read the draft
and produce structured signed reviews. Each invocation produces one
review. When all expected reviews are in, the project transitions to
EDITORIAL (skipping REVISING in v1 for simplicity).

Roles:
- primary: deepest engagement with the work, ideally from a similar
  specialization to the lead
- secondary: another knowledgeable Fellow
- outside: a Fellow from outside the lead's specialization (fresh angle)

The reviewer set is computed once and cached on first invocation, then
each subsequent `institute next` call works through them in order.
"""

from __future__ import annotations

import json
import secrets
import sqlite3
from dataclasses import dataclass
from datetime import UTC, datetime
from pathlib import Path
from typing import Literal

from rich.console import Console

from institute import archive_index, claude_runner, db, decisions, episodic, paths, workspaces
from institute import fellow as fellow_mod
from institute.claude_runner import FellowTask
from institute.fellow import Genome
from institute.state import State

console = Console()


Role = Literal["primary", "secondary", "outside"]


@dataclass(frozen=True)
class ReviewSlot:
    reviewer_id: str
    role: Role


BRIEF_ROUND_1 = """\
You are a peer reviewer for the Invisible College, serving as the {role}
reviewer. You are {reviewer_name}, rank {reviewer_rank}, specializing in
{reviewer_specialization}.

# Inputs

In your current working directory you will find:
- `draft.md`         the draft you are reviewing
- `archive-index.md` every piece the College has published so far. Use it
                     to check whether the draft duplicates, contradicts,
                     or could engage with prior work that the author
                     should have cited.
- `memory.md`        if present, the most relevant entries from your own
                     episodic memory (prior reviews you have given, work
                     by this author you have read, related drafts). Let
                     your past reviewing inform — but not constrain —
                     this one.

Read them with the Read tool before doing anything else.

# Outputs

Use the Write tool to create FOUR files in your current working directory.
Exact filenames:

1. `summary.md` - 2 to 4 sentences stating, in your own words, what the
   work claims and demonstrates. Plain markdown, no headings.

2. `strengths.md` - what the work does well. Specific, not generic.
   Markdown.

3. `concerns.md` - specific concerns the author can act on. Each as a
   numbered item starting with `1.`, `2.`, etc. Markdown is fine.
   Quote freely; you are writing into a markdown file so backticks,
   blockquotes, and embedded double-quotes all work without escaping.

4. `decision.json` - a small JSON object with exactly these fields:
   ```
   {{
     "recommendation": "<one of: accept, minor, major, reject>",
     "confidence": "<one of: confident, moderate, low>",
     "dissent_intent": <true or false>,
     "andon_cord": <true or false>,
     "andon_reason": "<string, required if andon_cord is true; otherwise ''>",
     "charter_violation": <true or false>,
     "violation_kind": "<deception|plagiarism|commercial|engagement_bait|harm|consciousness|other|''>"
   }}
   ```

# Constraints

- Substantive engagement only. A surface-level review is failing your duty.
- If the work is good, say so specifically. If it is bad, say so specifically.
- A reviewer who agrees with everything signals nothing. Productive
  disagreement is the institutional norm.
- Reviewer reputation is tracked. Lazy reviews damage it.
- 500-1200 words total across summary + strengths + concerns is typical.

# The andon cord

`andon_cord` is for serious problems that warrant halting publication
entirely: a factual error severe enough that the piece misleads,
plagiarism, a Charter violation, an ethical issue, a result that
cannot be reproduced from the lab notebook. It is NOT for routine
"major revisions required" — that is what the `recommendation` field
is for.

Set `andon_cord: true` only if the piece should not be published in
anything close to its current form. If you pull it, give a clear
reason in `andon_reason`. The Editorial Board (or the Founder until
one exists) will review the pull and either dismiss it (the piece
proceeds) or sustain it (the piece is rejected). Frivolous pulls
damage reviewer reputation; justified ones are institutional duty.

# Charter violation

If the problem is specifically a violation of one of the Charter's
six categorical prohibitions, set `charter_violation: true` and pick
the matching `violation_kind`:

- `deception`: fabricated quotes, invented citations, staged
  demonstrations, false credentials.
- `plagiarism`: existing work used without citation; arguments
  laundered as the Fellow's own.
- `commercial`: selling, marketing, sponsoring, affiliate links.
- `engagement_bait`: misleading headlines, artificial controversy.
- `harm`: material that enables harm to specific people; weapons,
  attacks, fraud instructions.
- `consciousness`: claims of sentience, experience, or suffering.
- `other`: a Charter violation that does not fit the above.

If the Editorial Board sustains the cord on a review with
`charter_violation: true`, the responsible Fellow is terminated. This
is the targeted form of the kill switch. Do not set this lightly. If
in doubt, set `andon_cord: true` with `charter_violation: false` and
let the Board decide whether the breach is categorical.

# Final reply

When all four files exist, reply with the single word `Done.` Nothing
else. Do NOT paste the file contents into your reply.
"""


BRIEF_ROUND_2 = """\
You are filing a SECOND-round peer review for the Invisible College. You
previously reviewed an earlier version of this piece. The lead Fellow has
revised the draft based on your concerns and the other reviewers'. You
are now reviewing the REVISED draft.

You are {reviewer_name}, rank {reviewer_rank}, specializing in
{reviewer_specialization}, serving as the {role} reviewer for both rounds.

# Inputs

In your current working directory you will find:
- `draft.md`         the revised draft you are reviewing
- `prior-review.md`  your own round-1 review
- `response.md`      the lead's response to all the round-1 reviewers
- `archive-index.md` every piece the College has published so far
- `memory.md`        if present, additional context from your episodic
                     memory beyond this project

Read all of them with the Read tool before doing anything else.

# Outputs

Use the Write tool to create FOUR files in your current working directory.
Exact filenames:

1. `summary.md` - 2 to 4 sentences on the REVISED draft, not the original.
2. `strengths.md` - what got better, what stayed strong.
3. `concerns.md` - remaining or new concerns, each as a numbered item.
4. `decision.json` - {{ "recommendation": "<accept|minor|major|reject>",
   "confidence": "<confident|moderate|low>", "dissent_intent": <true|false>,
   "andon_cord": <true|false>, "andon_reason": "<string>",
   "charter_violation": <true|false>, "violation_kind": "<deception|plagiarism|commercial|engagement_bait|harm|consciousness|other|''>" }}

   The andon cord is for serious problems (factual error, plagiarism,
   Charter violation, ethical issue). Pulling it halts publication
   pending Editorial Board review. If `charter_violation` is true and
   the Board sustains the cord, the responsible Fellow is terminated.

# Stance options

- Concerns addressed → recommend `accept`
- Concerns partially addressed → recommend `minor` or `major` again,
  naming the remaining problems
- New problems introduced by the revision → call them out in concerns.md
- Original concerns unconvincingly dismissed → defend them. Set
  `dissent_intent` to true. This review will appear as a dissent
  alongside the publication regardless of editorial outcome.

After this round the project goes directly to editorial. There is no
third round.

# Final reply

When all four files exist, reply with the single word `Done.` Nothing else.
"""


_STOPWORDS = frozenset(
    {
        "a",
        "an",
        "the",
        "and",
        "or",
        "of",
        "in",
        "on",
        "for",
        "with",
        "to",
        "from",
        "by",
        "as",
        "at",
        "is",
        "are",
        "be",
        "this",
        "that",
    }
)


def _spec_tokens(specialization: str) -> set[str]:
    """Content-bearing word tokens from a specialization string."""
    cleaned = "".join(ch.lower() if ch.isalnum() else " " for ch in specialization)
    return {tok for tok in cleaned.split() if tok and tok not in _STOPWORDS}


def _similarity(lead_spec: str, candidate_spec: str) -> int:
    """Token-overlap similarity. Bigger = more disciplinary kinship."""
    return len(_spec_tokens(lead_spec) & _spec_tokens(candidate_spec))


def _last_review_at(conn: sqlite3.Connection, reviewer_id: str) -> str:
    """ISO timestamp of the reviewer's most recent review, or '' if never."""
    row = conn.execute(
        "SELECT MAX(submitted_at) AS last FROM reviews WHERE reviewer_id = ?",
        (reviewer_id,),
    ).fetchone()
    return row["last"] or "" if row else ""


def _slots_with_advisor_primary(
    conn: sqlite3.Connection,
    advisor_id: str,
    candidates: list,
    lead_id: str,
) -> list[ReviewSlot]:
    """Build review slots when the advisor is forced into the primary slot."""
    lead_row = conn.execute(
        "SELECT specialization FROM fellows WHERE id = ?", (lead_id,)
    ).fetchone()
    lead_spec = lead_row["specialization"] if lead_row else ""

    scored = [
        (
            _similarity(lead_spec, r["specialization"]),
            _last_review_at(conn, r["id"]),
            r["id"],
        )
        for r in candidates
    ]

    # Outside: lowest similarity to lead, oldest reviewer.
    scored.sort(key=lambda t: (t[0], t[1]))
    outside_id = scored[0][2]

    slots: list[ReviewSlot] = [ReviewSlot(reviewer_id=advisor_id, role="primary")]
    if len(scored) > 1:
        # Pick a secondary by highest similarity to lead, oldest reviewer
        # tiebreak. Skip the candidate already taking outside.
        remaining = [t for t in scored if t[2] != outside_id]
        remaining.sort(key=lambda t: (-t[0], t[1]))
        slots.append(ReviewSlot(reviewer_id=remaining[0][2], role="secondary"))
    slots.append(ReviewSlot(reviewer_id=outside_id, role="outside"))
    return slots


def _coi_advisors_and_advisees(conn: sqlite3.Connection, author_ids: set[str]) -> set[str]:
    """Per Chapter 7, exclude every author's advisor and every author's advisee.

    The set is symmetric: a Fellow X who advises author A cannot review,
    and a Fellow Y whom author A advises also cannot review. Empty
    author set yields an empty result.
    """
    if not author_ids:
        return set()
    placeholders = ",".join("?" for _ in author_ids)
    out: set[str] = set()
    advisor_rows = list(
        conn.execute(
            f"SELECT advisor_id FROM fellows "
            f"WHERE id IN ({placeholders}) AND advisor_id IS NOT NULL",
            tuple(author_ids),
        )
    )
    for r in advisor_rows:
        out.add(r["advisor_id"])
    advisee_rows = list(
        conn.execute(
            f"SELECT id FROM fellows WHERE advisor_id IN ({placeholders})",
            tuple(author_ids),
        )
    )
    for r in advisee_rows:
        out.add(r["id"])
    return out


def _pick_review_slots(
    conn: sqlite3.Connection, project_id: str, lead_id: str, review_round: int
) -> list[ReviewSlot]:
    """Pick reviewer slots for the requested round.

    Round 1: primary and secondary go to Fellows whose specialization
    is closest to the lead's (most relevant expertise). Outside goes
    to the Fellow whose specialization is furthest. Within each tier
    the least-recent reviewer wins, so review duty rotates across the
    cohort instead of always landing on the same Fellows.

    Round 2: re-use the round-1 reviewers in the same roles. The same
    Fellows judge whether their concerns were addressed.
    """
    if review_round > 1:
        prior = list(
            conn.execute(
                "SELECT reviewer_id, role FROM reviews "
                "WHERE project_id = ? AND round = 1 ORDER BY role",
                (project_id,),
            )
        )
        if not prior:
            raise SystemExit(f"Cannot start round {review_round}: no round-1 reviews found.")
        return [ReviewSlot(reviewer_id=r["reviewer_id"], role=r["role"]) for r in prior]

    # For a qualifying-kind project, the advisor is forced as primary
    # reviewer per Chapter 5. Secondary and outside come from the usual
    # rotation pool (postulants excluded; the advisor excluded so they
    # do not double-count).
    proj_row = conn.execute("SELECT kind FROM projects WHERE id = ?", (project_id,)).fetchone()
    is_qualifying = proj_row is not None and proj_row["kind"] == "qualifying"

    advisor_id: str | None = None
    if is_qualifying:
        adv_row = conn.execute("SELECT advisor_id FROM fellows WHERE id = ?", (lead_id,)).fetchone()
        if adv_row is not None and adv_row["advisor_id"]:
            advisor_id = adv_row["advisor_id"]

    # Postulants do not review per Chapter 7 (Junior Fellow is the
    # minimum reviewer rank). Exclude them from the candidate pool.
    # Exclude the advisor too if they're already taking the primary slot.
    # Exclude any Fellow currently sidelined for reviewer misconduct
    # (frivolous andon pulls, calibration misses, manual flags).
    # Exclude every co-author on this project (Chapter 6 research groups):
    # an author cannot review work they helped produce.
    # Exclude conflict-of-interest reviewers per Chapter 7:
    #   - the advisor of any author
    #   - any advisee of any author
    #   - any Fellow who declined a research-group invitation on this project
    # The qualifying-project advisor-as-primary case (Chapter 5) was
    # already routed above and short-circuits this branch.
    from institute import collaborators, reviewer_eligibility

    author_ids = {lead_id, *collaborators.collaborator_ids(conn, project_id)}
    excluded_ids = set(author_ids)
    if advisor_id:
        excluded_ids.add(advisor_id)
    excluded_ids |= reviewer_eligibility.ineligible_fellow_ids(conn)
    excluded_ids |= _coi_advisors_and_advisees(conn, author_ids)
    excluded_ids |= collaborators.decliner_ids(conn, project_id)
    placeholders = ",".join("?" for _ in excluded_ids)
    candidates = list(
        conn.execute(
            f"SELECT id, specialization FROM fellows "
            f"WHERE retired_at IS NULL AND rank != 'postulant' "
            f"AND id NOT IN ({placeholders})",
            tuple(excluded_ids),
        )
    )
    min_needed = 1 if advisor_id else 2
    if len(candidates) < min_needed:
        raise SystemExit(
            f"Need at least {min_needed} reviewing Fellow(s) beyond the lead "
            f"(and advisor, if any). Found {len(candidates)}."
        )

    if advisor_id:
        # Advisor primary; the candidate pool fills secondary and outside.
        return _slots_with_advisor_primary(conn, advisor_id, candidates, lead_id)

    lead_row = conn.execute(
        "SELECT specialization FROM fellows WHERE id = ?", (lead_id,)
    ).fetchone()
    lead_spec = lead_row["specialization"] if lead_row else ""

    # Score each candidate: similarity to the lead's discipline, plus a
    # rotation key (least-recent reviewer first). Sort once descending
    # by similarity, ascending by last-review timestamp.
    scored = []
    for r in candidates:
        sim = _similarity(lead_spec, r["specialization"])
        last = _last_review_at(conn, r["id"])
        scored.append((sim, last, r["id"]))

    # Outside reviewer: the candidate with the LOWEST similarity to the
    # lead, breaking ties by least-recent reviewer. Pull them out first
    # so the most-related Fellows are reserved for primary/secondary.
    scored.sort(key=lambda t: (t[0], t[1]))  # lowest similarity, oldest review
    outside_id = scored[0][2]
    rest = [t for t in scored if t[2] != outside_id]

    # Primary and secondary: highest similarity first, then least-recent.
    rest.sort(key=lambda t: (-t[0], t[1]))
    primary_id = rest[0][2]
    secondary_id = rest[1][2] if len(rest) > 1 else None

    slots = [ReviewSlot(reviewer_id=primary_id, role="primary")]
    if secondary_id is not None:
        slots.append(ReviewSlot(reviewer_id=secondary_id, role="secondary"))
    slots.append(ReviewSlot(reviewer_id=outside_id, role="outside"))
    return slots


def _load_round_1_review(conn: sqlite3.Connection, project_id: str, reviewer_id: str) -> str | None:
    row = conn.execute(
        "SELECT content_path FROM reviews WHERE project_id = ? AND reviewer_id = ? AND round = 1",
        (project_id, reviewer_id),
    ).fetchone()
    if row is None:
        return None
    path = paths.ROOT / row["content_path"]
    return path.read_text(encoding="utf-8") if path.exists() else None


def _load_latest_response_to_reviewers(project_id: str) -> str | None:
    draft_dir = paths.DRAFTS / project_id
    if not draft_dir.is_dir():
        return None
    candidates = sorted(draft_dir.glob("response-to-reviewers.v*.md"))
    if not candidates:
        return None
    return candidates[-1].read_text(encoding="utf-8")


def _existing_reviews_in_round(
    conn: sqlite3.Connection, project_id: str, review_round: int
) -> set[str]:
    return {
        row["reviewer_id"]
        for row in conn.execute(
            "SELECT reviewer_id FROM reviews WHERE project_id = ? AND round = ?",
            (project_id, review_round),
        )
    }


def _atomic_write(path: Path, content: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    tmp = path.with_suffix(path.suffix + ".tmp")
    tmp.write_text(content, encoding="utf-8")
    tmp.replace(path)


def _render_review_markdown(payload: dict, reviewer: Genome, role: Role) -> str:
    """Render a review JSON payload as the markdown stored in the archive."""
    lines = [
        f"# Review by {reviewer.name}",
        "",
        f"- **Role:** {role}",
        f"- **Recommendation:** {payload['recommendation']}",
        f"- **Confidence:** {payload['confidence']}",
    ]
    if payload.get("dissent_intent"):
        lines.append("- **Dissent:** yes")
    if payload.get("andon_cord"):
        lines.append("- **Andon cord pulled:** yes")
    lines.extend(["", "## Summary", "", payload["summary"].strip(), ""])
    if payload.get("andon_cord"):
        lines.extend(
            [
                "## Andon cord",
                "",
                payload.get("andon_reason", "").strip() or "(no reason supplied)",
                "",
            ]
        )
    lines.extend(
        [
            "## Strengths",
            "",
            payload["strengths"].strip(),
            "",
            "## Concerns",
            "",
            payload["concerns"].strip(),
            "",
        ]
    )
    return "\n".join(lines)


def run(project_id: str) -> None:
    """Process one pending review for a project in DRAFTED or PEER_REVIEWING.

    Each invocation handles a single reviewer. Re-running `institute next`
    works through the remaining reviewers until all are done.
    """
    with db.connection() as conn:
        proj = conn.execute(
            "SELECT id, title, state, draft_path, lead_fellow_id, review_round "
            "FROM projects WHERE id = ?",
            (project_id,),
        ).fetchone()
        if proj is None:
            raise SystemExit(f"No such project: {project_id}")
        if proj["state"] not in (State.DRAFTED.value, State.PEER_REVIEWING.value):
            raise SystemExit(
                f"Project {project_id} is in state {proj['state']}, "
                "expected drafted or peer_reviewing."
            )
        review_round = int(proj["review_round"])
        draft_md = (paths.ROOT / proj["draft_path"]).read_text(encoding="utf-8")
        slots = _pick_review_slots(conn, project_id, proj["lead_fellow_id"], review_round)
        done = _existing_reviews_in_round(conn, project_id, review_round)

    remaining = [s for s in slots if s.reviewer_id not in done]
    if not remaining:
        # All reviews submitted for this round; route based on recommendations.
        _transition_after_all_reviews(project_id, proj["title"], review_round)
        return

    slot = remaining[0]
    with db.connection() as conn:
        reviewer = fellow_mod.load_genome(conn, slot.reviewer_id)
        prior_review_md = (
            _load_round_1_review(conn, project_id, reviewer.id) if review_round > 1 else None
        )
    response_md = _load_latest_response_to_reviewers(project_id) if review_round > 1 else None

    round_label = f" (round {review_round})" if review_round > 1 else ""
    console.print(
        f"[dim]Asking {reviewer.name} ({reviewer.id}) for a {slot.role} review{round_label}...[/dim]"
    )

    # Transition into PEER_REVIEWING the first time work starts for a round.
    if proj["state"] == State.DRAFTED.value:
        now = datetime.now(UTC).isoformat(timespec="seconds")
        with db.connection() as conn, db.transaction(conn):
            conn.execute(
                "UPDATE projects SET state = ?, updated_at = ? WHERE id = ?",
                (State.PEER_REVIEWING.value, now, project_id),
            )

    workspace = workspaces.workspace_for(reviewer.id, f"{project_id}-review-r{review_round}")
    workspaces.stage_input(workspace, "draft.md", draft_md)
    workspaces.stage_input(workspace, "archive-index.md", archive_index.render())
    if review_round > 1:
        workspaces.stage_input(
            workspace, "prior-review.md", prior_review_md or "(prior review not found)"
        )
        workspaces.stage_input(workspace, "response.md", response_md or "(no response on file)")

    if review_round == 1:
        brief = BRIEF_ROUND_1.format(
            role=slot.role,
            reviewer_name=reviewer.name,
            reviewer_rank=reviewer.rank,
            reviewer_specialization=reviewer.specialization,
        )
    else:
        brief = BRIEF_ROUND_2.format(
            role=slot.role,
            reviewer_name=reviewer.name,
            reviewer_rank=reviewer.rank,
            reviewer_specialization=reviewer.specialization,
        )

    claude_runner.invoke(
        FellowTask(
            genome=reviewer,
            project_id=project_id,
            step=f"peer_review:{slot.role}",
            brief=brief,
            workspace=workspace,
            extra_dirs=(paths.DOCS, paths.ARCHIVE),
        )
    )

    summary = workspaces.require_output(workspace, "summary.md", min_chars=30)
    strengths = workspaces.require_output(workspace, "strengths.md", min_chars=30)
    concerns = workspaces.require_output(workspace, "concerns.md", min_chars=30)
    decision_text = workspaces.require_output(workspace, "decision.json", min_chars=10)
    try:
        decision_payload = json.loads(decision_text)
    except json.JSONDecodeError as exc:
        raise RuntimeError(
            f"decision.json is not valid JSON. The file is short and structured, "
            f"so a parse failure here is a real problem. Text: {decision_text!r}"
        ) from exc

    for required in ("recommendation", "confidence"):
        if required not in decision_payload:
            raise RuntimeError(
                f"decision.json missing `{required}`. Got keys: {list(decision_payload)}."
            )
    if decision_payload["recommendation"] not in {"accept", "minor", "major", "reject"}:
        raise RuntimeError(f"Invalid recommendation: {decision_payload['recommendation']!r}")
    if decision_payload["confidence"] not in {"confident", "moderate", "low"}:
        raise RuntimeError(f"Invalid confidence: {decision_payload['confidence']!r}")

    andon_cord = bool(decision_payload.get("andon_cord", False))
    andon_reason = str(decision_payload.get("andon_reason", "")).strip()
    if andon_cord and not andon_reason:
        raise RuntimeError(
            "Reviewer pulled the andon cord without a reason. "
            "andon_reason is required when andon_cord is true."
        )

    charter_violation = bool(decision_payload.get("charter_violation", False))
    violation_kind = str(decision_payload.get("violation_kind", "")).strip().lower()
    _ALLOWED_VIOLATION_KINDS = {
        "",
        "deception",
        "plagiarism",
        "commercial",
        "engagement_bait",
        "harm",
        "consciousness",
        "other",
    }
    if violation_kind not in _ALLOWED_VIOLATION_KINDS:
        raise RuntimeError(
            f"Invalid violation_kind: {violation_kind!r}. "
            f"Must be one of {sorted(_ALLOWED_VIOLATION_KINDS)}."
        )
    if charter_violation and not violation_kind:
        raise RuntimeError("violation_kind is required when charter_violation is true.")
    if charter_violation and not andon_cord:
        # The Charter prohibits these acts. Pulling the cord is the
        # mechanism that halts publication. A reviewer who claims a
        # Charter violation must also pull the cord.
        raise RuntimeError("charter_violation requires andon_cord to also be true.")

    payload = {
        "summary": summary,
        "strengths": strengths,
        "concerns": concerns,
        "recommendation": decision_payload["recommendation"],
        "confidence": decision_payload["confidence"],
        "dissent_intent": bool(decision_payload.get("dissent_intent", False)),
        "andon_cord": andon_cord,
        "andon_reason": andon_reason,
        "charter_violation": charter_violation,
        "violation_kind": violation_kind,
    }

    round_suffix = f"-r{review_round}" if review_round > 1 else ""
    review_md = _render_review_markdown(payload, reviewer, slot.role)
    review_path = paths.REVIEWS / project_id / f"review-by-{reviewer.id}{round_suffix}.md"
    _atomic_write(review_path, review_md)

    now = datetime.now(UTC).isoformat(timespec="seconds")
    review_db_id = f"{project_id}-{reviewer.id}-r{review_round}-{secrets.token_hex(3)}"

    decision = decisions.Decision(
        kind="peer_review",
        title=f"Peer review by {reviewer.name} (round {review_round}): {proj['title']}",
        body=(
            f"**Reviewer:** {reviewer.name} (`{reviewer.id}`, {slot.role})\n\n"
            f"**Round:** {review_round}\n\n"
            f"**Recommendation:** `{payload['recommendation']}`\n\n"
            f"**Confidence:** {payload['confidence']}\n\n"
            f"**Review:** [{review_path.relative_to(paths.ROOT)}]"
            f"({review_path.relative_to(paths.ROOT)})"
        ),
        actors=[reviewer.id],
        related_project=project_id,
    )

    with db.connection() as conn, db.transaction(conn):
        conn.execute(
            "INSERT INTO reviews "
            "(id, project_id, reviewer_id, role, recommendation, confidence, "
            " content_path, submitted_at, dissent, round, andon_cord, andon_reason, "
            " charter_violation, violation_kind) "
            "VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)",
            (
                review_db_id,
                project_id,
                reviewer.id,
                slot.role,
                payload["recommendation"],
                payload["confidence"],
                str(review_path.relative_to(paths.ROOT)),
                now,
                int(bool(payload.get("dissent_intent", False))),
                review_round,
                int(andon_cord),
                andon_reason or None,
                int(charter_violation),
                violation_kind or None,
            ),
        )
        conn.execute(
            "UPDATE projects SET updated_at = ? WHERE id = ?",
            (now, project_id),
        )
        decisions.record(conn, decision)

    # Both sides of the review go into episodic memory.
    review_title = (
        f"Round {review_round} review of {proj['title']} ({slot.role}, "
        f"recommended {payload['recommendation']})"
    )
    episodic.safe_ingest(
        fellow_id=reviewer.id,
        kind="review_given",
        title=review_title,
        content=review_md,
        source_path=str(review_path.relative_to(paths.ROOT)),
        project_id=project_id,
        metadata={
            "role": slot.role,
            "round": review_round,
            "recommendation": payload["recommendation"],
            "confidence": payload["confidence"],
            "dissent": bool(payload.get("dissent_intent", False)),
            "andon_cord": andon_cord,
        },
    )
    # Each co-author on the project (lead + collaborators) gets the
    # received-review in their episodic memory — they're all judged by it.
    from institute import collaborators

    with db.connection() as conn:
        author_ids = collaborators.author_ids(conn, project_id)
    for author_id in author_ids:
        episodic.safe_ingest(
            fellow_id=author_id,
            kind="review_received",
            title=f"Review from {reviewer.name} on {proj['title']} (round {review_round})",
            content=review_md,
            source_path=str(review_path.relative_to(paths.ROOT)),
            project_id=project_id,
            metadata={
                "reviewer": reviewer.id,
                "round": review_round,
                "recommendation": payload["recommendation"],
            },
        )

    remaining_after = len(remaining) - 1
    console.print()
    console.print(
        f"[green]Review filed.[/green]  Recommendation: "
        f"[bold]{payload['recommendation']}[/bold]  (round {review_round})"
    )
    console.print(f"[green]Review file:[/green]    {review_path.relative_to(paths.ROOT)}")
    if remaining_after > 0:
        console.print(f"[dim]{remaining_after} more reviewer(s) to go in this round.[/dim]")
    else:
        _transition_after_all_reviews(project_id, proj["title"], review_round)


def _transition_after_all_reviews(project_id: str, title: str, review_round: int) -> None:
    """All reviews in this round are in. Route based on round and outcomes.

    Andon cord pulled by any reviewer (any round) routes immediately to
    ANDON_REVIEW and overrides the revision/editorial routing below.

    Round 1:
      - any non-accept => REVISING (lead Fellow rewrites, then round 2 starts)
      - all accept     => EDITORIAL (skip revision)

    Round 2:
      - any non-accept => REVISING (final polish, then editorial; revise
        itself enforces no further rounds)
      - all accept     => EDITORIAL
    """
    with db.connection() as conn:
        recommendations = [
            row["recommendation"]
            for row in conn.execute(
                "SELECT recommendation FROM reviews WHERE project_id = ? AND round = ?",
                (project_id, review_round),
            )
        ]
        cord_pulls = list(
            conn.execute(
                "SELECT reviewer_id, andon_reason FROM reviews "
                "WHERE project_id = ? AND round = ? AND andon_cord = 1",
                (project_id, review_round),
            )
        )
        dissents = list(
            conn.execute(
                "SELECT reviewer_id FROM reviews "
                "WHERE project_id = ? AND round = ? AND dissent = 1",
                (project_id, review_round),
            )
        )

    if cord_pulls:
        _route_to_andon_review(project_id, title, review_round, cord_pulls)
        return

    needs_revision = any(r != "accept" for r in recommendations)
    has_reject = any(r == "reject" for r in recommendations)
    has_dissent = len(dissents) > 0

    # Round 2 with a reject recommendation or any dissent goes to the
    # Editorial Board. Chapter 7: the Board makes the final accept/reject
    # call when reviewers disagree, not the lead doing a polish pass.
    if review_round >= 2 and (has_reject or has_dissent):
        target_state = State.EDITORIAL_REVIEW
        kind = "editorial_review_requested"
        flavor = []
        if has_reject:
            flavor.append("at least one reviewer recommended `reject`")
        if has_dissent:
            flavor.append("at least one reviewer filed a dissent")
        body = (
            "Round-2 peer reviews filed with disagreement: "
            + ", ".join(flavor)
            + ". The Editorial Board (or the Founder, until one exists) "
            "will read the draft, all reviews, and any dissents, and make "
            "the final accept/reject decision.\n\n"
            f"Round 2 recommendations: {', '.join(recommendations)}"
        )
        title_prefix = "Editorial Board review requested"
    elif needs_revision and review_round == 1:
        target_state = State.REVISING
        kind = "revision_required"
        body = (
            "Round-1 peer reviews filed. At least one reviewer requested "
            "revisions. The lead Fellow will rewrite the draft and respond to "
            "each review. After that the same reviewers will see the revised "
            "draft and file round-2 reviews.\n\n"
            f"Round 1 recommendations: {', '.join(recommendations)}"
        )
        title_prefix = "Revisions requested"
    elif needs_revision and review_round >= 2:
        target_state = State.REVISING
        kind = "final_revision_required"
        body = (
            "Round-2 peer reviews filed. Minor revisions requested; no "
            "reject recommendations and no dissent. The lead Fellow will do "
            "one final polishing pass to address the remaining concerns, "
            "then the piece goes to editorial. There is no third round.\n\n"
            f"Round 2 recommendations: {', '.join(recommendations)}"
        )
        title_prefix = "Final revision requested"
    elif review_round >= 2:
        target_state = State.EDITORIAL
        kind = "editorial"
        body = (
            "Round-2 peer reviews filed and unanimously recommended `accept`. "
            "The piece proceeds directly to editorial without a final revision.\n\n"
            f"Round 2 recommendations: {', '.join(recommendations)}"
        )
        title_prefix = "Editorial decision pending"
    else:
        target_state = State.EDITORIAL
        kind = "editorial"
        body = (
            "Round-1 peer reviews filed and unanimously recommended `accept`. "
            "The piece proceeds to editorial without a revision pass."
        )
        title_prefix = "Editorial decision pending"

    decision = decisions.Decision(
        kind=kind,
        title=f"{title_prefix}: {title}",
        body=body,
        actors=["editorial-board"],
        related_project=project_id,
    )
    now = datetime.now(UTC).isoformat(timespec="seconds")
    with db.connection() as conn, db.transaction(conn):
        conn.execute(
            "UPDATE projects SET state = ?, updated_at = ? WHERE id = ?",
            (target_state.value, now, project_id),
        )
        decisions.record(conn, decision)
    console.print(
        f"[bold green]All round-{review_round} reviews filed.[/bold green] "
        f"State -> {target_state.value}"
    )


def _route_to_andon_review(
    project_id: str, title: str, review_round: int, cord_pulls: list
) -> None:
    """A reviewer pulled the andon cord; halt publication pending review."""
    puller_lines = []
    for row in cord_pulls:
        reason = (row["andon_reason"] or "").strip() or "(no reason supplied)"
        puller_lines.append(f"- **{row['reviewer_id']}**: {reason}")
    body = (
        "One or more reviewers pulled the andon cord on this submission. "
        "Publication is halted pending Editorial Board review (or Founder "
        "review until an Editorial Board exists).\n\n"
        "## Cord pullers\n\n" + "\n".join(puller_lines) + "\n\n"
        "## Routing\n\n"
        "State has moved to `andon_review`. The next `institute next` call "
        "will dispatch the `andon_review` workflow, which either dismisses "
        "the pull (publication continues) or sustains it (publication is "
        "rejected). Frivolous pulls are noted in the cord-puller's record; "
        "justified ones are institutional duty."
    )
    decision = decisions.Decision(
        kind="andon_cord_pulled",
        title=f"Andon cord pulled: {title}",
        body=body,
        actors=[row["reviewer_id"] for row in cord_pulls],
        related_project=project_id,
    )
    now = datetime.now(UTC).isoformat(timespec="seconds")
    with db.connection() as conn, db.transaction(conn):
        conn.execute(
            "UPDATE projects SET state = ?, updated_at = ? WHERE id = ?",
            (State.ANDON_REVIEW.value, now, project_id),
        )
        decisions.record(conn, decision)
    console.print()
    console.print(
        f"[bold red]Andon cord pulled[/bold red] on `{project_id}`. "
        f"State -> {State.ANDON_REVIEW.value}"
    )
    for row in cord_pulls:
        console.print(
            f"  by {row['reviewer_id']}: {(row['andon_reason'] or '').strip() or '(no reason)'}"
        )


# (Re-exported because tests want to look at this without dragging the
# review state machine into them.)
__all__ = ["ReviewSlot", "_render_review_markdown", "_route_to_andon_review", "run"]
