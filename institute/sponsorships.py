"""Chapter 4 admissions: sponsored nominations.

Any Fellow at Junior Fellow rank or above may sponsor a candidate.
The sponsor has identified someone they believe would strengthen the
College in a specific way, and commits to advise during Postulancy
(or to find an appropriate advisor) if the candidate is admitted.

Sponsorship is reputational currency: a Fellow who repeatedly sponsors
candidates who fail at qualifying or wash out early sees their sponsor
reputation decay. The promote workflow can read `success_rate` to
factor this into a Fellow's own promotion case.

States:

  - `pending`   nomination recorded; admit panel has not yet decided
  - `admitted`  the candidate became a Postulant
  - `rejected`  the admit panel rejected the candidate
  - `withdrawn` the sponsor pulled the nomination before review
  - `advanced`  the admitted candidate later promoted past Postulant
                (terminal positive: this is the sponsorship-success
                signal)
"""

from __future__ import annotations

import secrets
import sqlite3
from dataclasses import dataclass
from datetime import UTC, date, datetime

from institute import db

VALID_OUTCOMES = ("pending", "admitted", "rejected", "withdrawn", "advanced")
# Outcomes that count toward sponsor success calculations.
_RESOLVED_OUTCOMES = ("admitted", "rejected", "advanced")
_SUCCESS_OUTCOMES = ("admitted", "advanced")


@dataclass(frozen=True)
class Sponsorship:
    id: str
    sponsor_id: str
    candidate_genome_path: str | None
    candidate_fellow_id: str | None
    rationale: str
    opened_at: str
    resolved_at: str | None
    outcome: str
    cohort_call_id: str | None


def _new_id() -> str:
    return f"sponsor-{date.today().isoformat()}-{secrets.token_hex(2)}"


def _row(row: sqlite3.Row) -> Sponsorship:
    return Sponsorship(
        id=row["id"],
        sponsor_id=row["sponsor_id"],
        candidate_genome_path=row["candidate_genome_path"],
        candidate_fellow_id=row["candidate_fellow_id"],
        rationale=row["rationale"],
        opened_at=row["opened_at"],
        resolved_at=row["resolved_at"],
        outcome=row["outcome"],
        cohort_call_id=row["cohort_call_id"],
    )


def nominate(
    *,
    sponsor_id: str,
    rationale: str,
    cohort_call_id: str | None = None,
) -> Sponsorship:
    """Open a new sponsorship for the named Fellow. Validates the sponsor
    is eligible (Junior Fellow rank or above, not retired).
    """
    rationale = rationale.strip()
    if not rationale:
        raise ValueError("Sponsorship rationale must be non-empty.")
    with db.connection() as conn, db.transaction(conn):
        sponsor = conn.execute(
            "SELECT id, rank, retired_at FROM fellows WHERE id = ?",
            (sponsor_id,),
        ).fetchone()
        if sponsor is None:
            raise ValueError(f"No such Fellow: {sponsor_id!r}")
        if sponsor["retired_at"] is not None:
            raise ValueError(f"Fellow {sponsor_id!r} is retired and cannot sponsor candidates.")
        if sponsor["rank"] in ("postulant", "novice"):
            raise ValueError(
                f"Fellow {sponsor_id!r} is rank {sponsor['rank']!r}. Chapter 4 "
                "requires Junior Fellow rank or above to sponsor."
            )
        if cohort_call_id is not None:
            call = conn.execute(
                "SELECT status FROM cohort_calls WHERE id = ?",
                (cohort_call_id,),
            ).fetchone()
            if call is None:
                raise ValueError(f"No such cohort call: {cohort_call_id!r}")
            if call["status"] != "open":
                raise ValueError(
                    f"Cohort call {cohort_call_id!r} is closed; cannot attach new sponsorships."
                )
        nomination_id = _new_id()
        now = datetime.now(UTC).isoformat(timespec="seconds")
        conn.execute(
            """
            INSERT INTO sponsorships
                (id, sponsor_id, candidate_genome_path, candidate_fellow_id,
                 rationale, opened_at, resolved_at, outcome, cohort_call_id)
            VALUES (?, ?, NULL, NULL, ?, ?, NULL, 'pending', ?)
            """,
            (nomination_id, sponsor_id, rationale, now, cohort_call_id),
        )
        row = conn.execute("SELECT * FROM sponsorships WHERE id = ?", (nomination_id,)).fetchone()
    return _row(row)


def record_genome(sponsorship_id: str, *, genome_path: str) -> Sponsorship:
    """Attach a drafted candidate genome path to a pending sponsorship."""
    with db.connection() as conn, db.transaction(conn):
        existing = conn.execute(
            "SELECT outcome FROM sponsorships WHERE id = ?", (sponsorship_id,)
        ).fetchone()
        if existing is None:
            raise ValueError(f"No such sponsorship: {sponsorship_id!r}")
        if existing["outcome"] != "pending":
            raise ValueError(f"Sponsorship {sponsorship_id!r} is already {existing['outcome']!r}.")
        conn.execute(
            "UPDATE sponsorships SET candidate_genome_path = ? WHERE id = ?",
            (genome_path, sponsorship_id),
        )
        row = conn.execute("SELECT * FROM sponsorships WHERE id = ?", (sponsorship_id,)).fetchone()
    return _row(row)


def record_outcome(
    sponsorship_id: str,
    *,
    outcome: str,
    candidate_fellow_id: str | None = None,
    conn: sqlite3.Connection | None = None,
) -> Sponsorship:
    """Update sponsorship outcome.

    Pass `conn` to participate in an enclosing transaction (the admit
    workflow uses this so the sponsorship outcome lands in the same tx
    as the admit decision). Without a conn, opens its own transaction.
    """
    if outcome not in VALID_OUTCOMES:
        raise ValueError(f"Invalid outcome {outcome!r}. Must be one of {VALID_OUTCOMES}.")

    def _apply(conn: sqlite3.Connection) -> Sponsorship:
        existing = conn.execute(
            "SELECT outcome FROM sponsorships WHERE id = ?", (sponsorship_id,)
        ).fetchone()
        if existing is None:
            raise ValueError(f"No such sponsorship: {sponsorship_id!r}")
        now = datetime.now(UTC).isoformat(timespec="seconds")
        conn.execute(
            "UPDATE sponsorships SET outcome = ?, resolved_at = ?, "
            "candidate_fellow_id = COALESCE(?, candidate_fellow_id) WHERE id = ?",
            (outcome, now, candidate_fellow_id, sponsorship_id),
        )
        row = conn.execute("SELECT * FROM sponsorships WHERE id = ?", (sponsorship_id,)).fetchone()
        return _row(row)

    if conn is not None:
        return _apply(conn)
    with db.connection() as own, db.transaction(own):
        return _apply(own)


def list_sponsorships(sponsor_id: str | None = None, limit: int = 50) -> list[Sponsorship]:
    with db.connection() as conn:
        if sponsor_id is None:
            rows = list(
                conn.execute(
                    "SELECT * FROM sponsorships ORDER BY opened_at DESC LIMIT ?",
                    (int(limit),),
                )
            )
        else:
            rows = list(
                conn.execute(
                    "SELECT * FROM sponsorships WHERE sponsor_id = ? "
                    "ORDER BY opened_at DESC LIMIT ?",
                    (sponsor_id, int(limit)),
                )
            )
    return [_row(r) for r in rows]


def success_rate(sponsor_id: str) -> tuple[int, int, float | None]:
    """Return (successes, resolved_total, rate) for a sponsor.

    Successes = sponsored candidates who were admitted or later advanced.
    Resolved total = successes + rejected. Withdrawn and pending do not
    count in either side of the ratio. Rate is None when nothing has
    resolved yet (don't display a denominator that doesn't exist).
    """
    with db.connection() as conn:
        rows = list(
            conn.execute(
                "SELECT outcome FROM sponsorships WHERE sponsor_id = ?",
                (sponsor_id,),
            )
        )
    successes = sum(1 for r in rows if r["outcome"] in _SUCCESS_OUTCOMES)
    resolved = sum(1 for r in rows if r["outcome"] in _RESOLVED_OUTCOMES)
    rate: float | None = successes / resolved if resolved > 0 else None
    return successes, resolved, rate


def render_sponsor_reputation_md(sponsor_id: str) -> str:
    """Markdown block the admit panel reads alongside a sponsored
    candidate, so the panel can see the sponsor's track record.
    """
    successes, resolved, rate = success_rate(sponsor_id)
    if resolved == 0:
        return (
            f"_Sponsor `{sponsor_id}` has no resolved sponsorships on "
            "record. This is their first nomination — treat the rationale "
            "on its own merit._\n"
        )
    rate_str = f"{rate * 100:.0f}%" if rate is not None else "n/a"
    return (
        f"_Sponsor `{sponsor_id}`: {successes}/{resolved} sponsorships "
        f"have produced admitted Fellows ({rate_str})._\n"
    )


__all__ = [
    "VALID_OUTCOMES",
    "Sponsorship",
    "list_sponsorships",
    "nominate",
    "record_genome",
    "record_outcome",
    "render_sponsor_reputation_md",
    "success_rate",
]
