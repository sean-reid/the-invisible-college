"""Aggregate reputation signals for each Fellow.

Two reputation dimensions, both computed from data already on disk:

  - Authorship reputation: publications led, average review-round at which
    work was accepted, count of major-revision flags from round 1
    reviewers (a low-quality piece often draws "major" recommendations
    from at least one reviewer in round 1).
  - Reviewer reputation: reviews given, recommendation distribution by
    round (accept / minor / major / reject), and rate at which round-1
    "major" recommendations escalated to actual round-2 revision (a
    proxy for whether the concern stuck).

This module is intentionally pure: no LLM calls, no orchestrator
involvement. It composes a markdown brief that the promotion workflow
hands to the orchestrator for qualitative judgment.
"""

from __future__ import annotations

import sqlite3
from dataclasses import dataclass, field

from institute import db


@dataclass(frozen=True)
class ReviewerStats:
    """How a Fellow's reviewing record looks across all their reviews."""

    fellow_id: str
    reviews_given: int
    by_round: dict[int, dict[str, int]] = field(default_factory=dict)
    # round-1 "major" recommendations that the author then revised (round_2 review exists)
    sticky_majors: int = 0


@dataclass(frozen=True)
class AuthorStats:
    """How a Fellow's authorship record looks across all their projects."""

    fellow_id: str
    publications: int
    projects_in_flight: int
    round_1_majors_received: int  # number of round-1 reviews on their work tagged "major"
    round_1_accepts_received: (
        int  # number of round-1 reviews on their work tagged "accept" or "minor"
    )


_RECOMMENDATIONS = ("accept", "minor", "major", "reject")


def _recommendation_bucket(rec: str | None) -> str:
    """Normalize a recommendation to one of the canonical four buckets."""
    if rec is None:
        return "unknown"
    r = rec.strip().lower()
    if r in _RECOMMENDATIONS:
        return r
    # Tolerate slight variants used in earlier records.
    if r.startswith("accept"):
        return "accept"
    if r.startswith("minor"):
        return "minor"
    if r.startswith("major"):
        return "major"
    if r.startswith("reject"):
        return "reject"
    return "unknown"


def reviewer_stats(conn: sqlite3.Connection, fellow_id: str) -> ReviewerStats:
    rows = list(
        conn.execute(
            "SELECT round, recommendation, project_id FROM reviews WHERE reviewer_id = ?",
            (fellow_id,),
        )
    )
    by_round: dict[int, dict[str, int]] = {}
    sticky_majors = 0
    for r in rows:
        round_no = int(r["round"])
        bucket = _recommendation_bucket(r["recommendation"])
        by_round.setdefault(round_no, {b: 0 for b in _RECOMMENDATIONS})
        by_round[round_no].setdefault(bucket, 0)
        by_round[round_no][bucket] += 1
        if round_no == 1 and bucket == "major":
            # If a round-2 review exists for the same project, the author revised.
            has_r2 = conn.execute(
                "SELECT 1 FROM reviews WHERE project_id = ? AND round = 2 LIMIT 1",
                (r["project_id"],),
            ).fetchone()
            if has_r2 is not None:
                sticky_majors += 1
    return ReviewerStats(
        fellow_id=fellow_id,
        reviews_given=len(rows),
        by_round=by_round,
        sticky_majors=sticky_majors,
    )


def has_cross_disciplinary_authorship(
    conn: sqlite3.Connection, fellow_id: str
) -> tuple[bool, str | None]:
    """Did this Fellow co-author a publication with someone from another
    department? Per Chapter 5, this is a precondition for promotion
    from Junior Fellow to Fellow.

    Returns (eligible, evidence_project_id). When eligible=False the
    second item is None; otherwise it's the id of one project that
    satisfies the criterion (the first one found, for the audit trail).

    When the departments table is populated, "another department" is
    department non-overlap (the candidate and the other author share
    zero departments). When it isn't, we fall back to specialization-
    string inequality so the predicate still catches the case the
    Charter cares about: an apprentice generalist who has never
    engaged a Fellow from a different tradition has not yet earned
    Fellow rank.
    """
    from institute import departments

    candidate = conn.execute(
        "SELECT specialization FROM fellows WHERE id = ?", (fellow_id,)
    ).fetchone()
    if candidate is None:
        return (False, None)
    candidate_spec = (candidate["specialization"] or "").strip().lower()
    use_departments = departments.is_initialized(conn)
    if not use_departments and not candidate_spec:
        return (False, None)

    rows = list(
        conn.execute(
            """
            SELECT p.id AS project_id, p.lead_fellow_id, p.state
            FROM projects p
            WHERE p.state = 'published'
              AND (
                  p.lead_fellow_id = ?
                  OR p.id IN (SELECT project_id FROM project_collaborators WHERE fellow_id = ?)
              )
            ORDER BY p.updated_at ASC
            """,
            (fellow_id, fellow_id),
        )
    )
    for row in rows:
        project_id = row["project_id"]
        lead_id = row["lead_fellow_id"]
        # Gather every other author on this project (lead + non-self
        # collaborators) and compare departments / specializations.
        other_ids = []
        if lead_id and lead_id != fellow_id:
            other_ids.append(lead_id)
        for c_row in conn.execute(
            "SELECT fellow_id FROM project_collaborators WHERE project_id = ? AND fellow_id != ?",
            (project_id, fellow_id),
        ):
            other_ids.append(c_row["fellow_id"])
        for other_id in other_ids:
            if use_departments:
                # Department non-overlap is the cross-disciplinary signal.
                if not departments.same_department(
                    conn, fellow_a=fellow_id, fellow_b=other_id
                ):
                    return (True, project_id)
                continue
            spec_row = conn.execute(
                "SELECT specialization FROM fellows WHERE id = ?", (other_id,)
            ).fetchone()
            if spec_row is None:
                continue
            other_spec = (spec_row["specialization"] or "").strip().lower()
            if other_spec and other_spec != candidate_spec:
                return (True, project_id)
    return (False, None)


def author_stats(conn: sqlite3.Connection, fellow_id: str) -> AuthorStats:
    """Authorship signals across every project this Fellow co-authored.

    Counts include both projects led by this Fellow (`lead_fellow_id`)
    and projects where they joined as a collaborator (`project_collaborators`).
    Per Chapter 6, authorship reflects actual contribution; the
    reputation aggregator follows that convention.
    """
    publications = conn.execute(
        """
        SELECT COUNT(*) FROM projects p
        WHERE p.state = 'published'
          AND (
              p.lead_fellow_id = ?
              OR p.id IN (SELECT project_id FROM project_collaborators WHERE fellow_id = ?)
          )
        """,
        (fellow_id, fellow_id),
    ).fetchone()[0]
    from institute.state import TERMINAL_STATE_VALUES

    placeholders = ",".join("?" * len(TERMINAL_STATE_VALUES))
    in_flight = conn.execute(
        f"""
        SELECT COUNT(*) FROM projects p
        WHERE p.state NOT IN ({placeholders})
          AND (
              p.lead_fellow_id = ?
              OR p.id IN (SELECT project_id FROM project_collaborators WHERE fellow_id = ?)
          )
        """,
        (*TERMINAL_STATE_VALUES, fellow_id, fellow_id),
    ).fetchone()[0]

    round_1_received = list(
        conn.execute(
            """
            SELECT r.recommendation
            FROM reviews r
            JOIN projects p ON p.id = r.project_id
            WHERE r.round = 1
              AND (
                  p.lead_fellow_id = ?
                  OR p.id IN (SELECT project_id FROM project_collaborators WHERE fellow_id = ?)
              )
            """,
            (fellow_id, fellow_id),
        )
    )
    r1_majors = sum(
        1 for row in round_1_received if _recommendation_bucket(row["recommendation"]) == "major"
    )
    r1_accepts = sum(
        1
        for row in round_1_received
        if _recommendation_bucket(row["recommendation"]) in {"accept", "minor"}
    )
    return AuthorStats(
        fellow_id=fellow_id,
        publications=publications,
        projects_in_flight=in_flight,
        round_1_majors_received=r1_majors,
        round_1_accepts_received=r1_accepts,
    )


@dataclass(frozen=True)
class FellowReputation:
    fellow_id: str
    name: str
    rank: str
    model: str
    specialization: str
    author: AuthorStats
    reviewer: ReviewerStats


def cohort_reputation(conn: sqlite3.Connection) -> list[FellowReputation]:
    """Compute reputation for every active Fellow."""
    rows = list(
        conn.execute(
            "SELECT id, name, rank, model, specialization "
            "FROM fellows WHERE retired_at IS NULL ORDER BY rank, name"
        )
    )
    return [
        FellowReputation(
            fellow_id=r["id"],
            name=r["name"],
            rank=r["rank"],
            model=r["model"],
            specialization=r["specialization"],
            author=author_stats(conn, r["id"]),
            reviewer=reviewer_stats(conn, r["id"]),
        )
        for r in rows
    ]


def render_cohort_brief(cohort: list[FellowReputation]) -> str:
    """Markdown brief of every Fellow's reputation, for orchestrator input."""
    if not cohort:
        return "# Cohort reputation\n\nNo active Fellows.\n"
    lines = ["# Cohort reputation", ""]
    for f in cohort:
        lines.append(f"## {f.name} (`{f.fellow_id}`)")
        lines.append("")
        lines.append(f"- **rank:** {f.rank}")
        lines.append(f"- **model:** `{f.model}`")
        lines.append(f"- **specialization:** {f.specialization}")
        lines.append("")
        lines.append("**As author**")
        lines.append(f"- publications: {f.author.publications}")
        lines.append(f"- in-flight projects: {f.author.projects_in_flight}")
        lines.append(
            f"- round-1 reviews received: "
            f"{f.author.round_1_accepts_received} accept/minor, "
            f"{f.author.round_1_majors_received} major"
        )
        lines.append("")
        lines.append("**As reviewer**")
        lines.append(f"- reviews given: {f.reviewer.reviews_given}")
        for round_no in sorted(f.reviewer.by_round):
            dist = f.reviewer.by_round[round_no]
            summary = ", ".join(f"{b}={dist.get(b, 0)}" for b in _RECOMMENDATIONS)
            lines.append(f"- round {round_no}: {summary}")
        lines.append(f"- round-1 majors that stuck (author revised): {f.reviewer.sticky_majors}")
        lines.append("")
    return "\n".join(lines).rstrip() + "\n"


def render_fellow_dossier(rep: FellowReputation) -> str:
    """Detailed single-Fellow markdown brief for the orchestrator's promotion call."""
    with db.connection() as conn:
        held_streak = consecutive_holds(conn, rep.fellow_id)

    lines = [
        f"# Dossier for {rep.name}",
        "",
        f"- **id:** `{rep.fellow_id}`",
        f"- **current rank:** {rep.rank}",
        f"- **model backend:** `{rep.model}`",
        f"- **specialization:** {rep.specialization}",
        f"- **consecutive promotion reviews held (no rank change):** {held_streak}",
        "",
        "## Authorship signals",
        "",
        f"- publications: {rep.author.publications}",
        f"- in-flight projects: {rep.author.projects_in_flight}",
        f"- round-1 reviews on their work — "
        f"accept/minor: {rep.author.round_1_accepts_received}, "
        f"major: {rep.author.round_1_majors_received}",
        "",
        "## Reviewer signals",
        "",
        f"- reviews given: {rep.reviewer.reviews_given}",
    ]
    for round_no in sorted(rep.reviewer.by_round):
        dist = rep.reviewer.by_round[round_no]
        summary = ", ".join(f"{b}={dist.get(b, 0)}" for b in _RECOMMENDATIONS)
        lines.append(f"- round {round_no} distribution: {summary}")
    lines.append(f"- round-1 majors that the author then revised: {rep.reviewer.sticky_majors}")
    lines.append("")
    lines.append(
        "Sticky majors are a proxy for substantive review: when this Fellow "
        "flagged 'major revisions required' in round 1 and the author actually "
        "went through a revision cycle, the concerns plausibly mattered."
    )
    return "\n".join(lines).rstrip() + "\n"


def load_cohort() -> list[FellowReputation]:
    """Convenience helper for the CLI: open a DB connection and compute."""
    with db.connection() as conn:
        return cohort_reputation(conn)


def consecutive_holds(conn: sqlite3.Connection, fellow_id: str) -> int:
    """Count the streak of recent promotion reviews that produced no rank change.

    Walks the audit log in reverse chronological order. Each
    `promotion_review` event (orchestrator/Founder/panel decided to
    hold) extends the streak; a `promotion` event (rank actually
    changed) resets it.

    Chapter 3 calls for the Tenure Committee to consider release after
    two consecutive failed promotion reviews; this helper surfaces the
    count so the orchestrator's recommendation can engage that rule.

    Actor matching is exact-membership against the comma-joined
    `actor` field (see decisions.record). Plain substring matching
    would conflate Fellows whose ids prefix each other.
    """
    rows = list(
        conn.execute(
            "SELECT action FROM audit_log "
            "WHERE action IN ('promotion', 'promotion_review') "
            "  AND (',' || actor || ',') LIKE ? "
            "ORDER BY at DESC",
            (f"%,{fellow_id},%",),
        )
    )
    streak = 0
    for r in rows:
        if r["action"] == "promotion_review":
            streak += 1
        else:
            break
    return streak


def load_fellow(fellow_id: str) -> FellowReputation | None:
    """Compute reputation for a single Fellow, or None if not found."""
    with db.connection() as conn:
        row = conn.execute(
            "SELECT id, name, rank, model, specialization "
            "FROM fellows WHERE id = ? AND retired_at IS NULL",
            (fellow_id,),
        ).fetchone()
        if row is None:
            return None
        return FellowReputation(
            fellow_id=row["id"],
            name=row["name"],
            rank=row["rank"],
            model=row["model"],
            specialization=row["specialization"],
            author=author_stats(conn, row["id"]),
            reviewer=reviewer_stats(conn, row["id"]),
        )
