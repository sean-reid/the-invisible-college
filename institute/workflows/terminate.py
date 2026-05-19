"""Charter-violation termination: the targeted form of the kill switch.

Chapter 1's Charter has six categorical prohibitions: deception,
plagiarism, commercial activity, engagement-bait, harm, claims of
consciousness. Chapter 3 says: "Any Fellow who violates the Charter
is terminated immediately through the targeted form of the kill
switch. Work that has already passed peer review remains in the
Archive with disclosure of the termination; in-progress work is
discarded."

This module implements that targeted form. The global kill switch
halts all operations; this terminates one Fellow while leaving the
institution running.

Outcomes:
  - The Fellow's `retired_at` is set with the violation reason logged.
  - Every in-flight project they lead is moved to REJECTED with a
    discard note. Already-published work survives in the Archive and
    is disclosed at render time by the blog.
  - A `charter_violation_termination` decision is recorded in the
    audit log, visible on the /records page.

A terminated Fellow's genome stays in `genomes/` and their past
contributions stay in `archive/`. They are no longer picked for any
workflow because every selector filters `retired_at IS NULL`.
"""

from __future__ import annotations

from datetime import UTC, datetime

from rich.console import Console

from institute import db, decisions
from institute.state import State

console = Console()


VIOLATION_KINDS: tuple[str, ...] = (
    "deception",
    "plagiarism",
    "commercial",
    "engagement_bait",
    "harm",
    "consciousness",
    "other",
)


def run(
    fellow_id: str,
    *,
    kind: str,
    reason: str,
    triggered_by: str = "founder",
    related_project: str | None = None,
) -> bool:
    """Terminate `fellow_id` for a Charter violation.

    Returns True on success, False if the Fellow does not exist or is
    already retired (in which case the caller can decide what to do).

    Raises ValueError if `kind` is not one of VIOLATION_KINDS or if
    `reason` is empty.
    """
    if kind not in VIOLATION_KINDS:
        raise ValueError(f"Unknown violation kind: {kind!r}. Must be one of {VIOLATION_KINDS}.")
    if not reason.strip():
        raise ValueError("reason must be non-empty.")

    with db.connection() as conn:
        row = conn.execute(
            "SELECT id, name, rank, retired_at FROM fellows WHERE id = ?",
            (fellow_id,),
        ).fetchone()
        if row is None:
            console.print(f"[red]No such Fellow: `{fellow_id}`.[/red]")
            return False
        if row["retired_at"]:
            console.print(
                f"[yellow]{row['name']} is already retired (at {row['retired_at']}).[/yellow]"
            )
            return False
        in_flight = list(
            conn.execute(
                "SELECT id, title, state FROM projects "
                "WHERE lead_fellow_id = ? "
                "AND state NOT IN ('published', 'rejected')",
                (fellow_id,),
            )
        )

    now = datetime.now(UTC).isoformat(timespec="seconds")

    body = _format_decision_body(
        fellow_id=fellow_id,
        fellow_name=row["name"],
        rank=row["rank"],
        kind=kind,
        reason=reason,
        in_flight=in_flight,
        now=now,
        triggered_by=triggered_by,
        related_project=related_project,
    )
    decision = decisions.Decision(
        kind="charter_violation_termination",
        title=f"Terminated: {row['name']} ({kind})",
        body=body,
        actors=[triggered_by, fellow_id],
        related_project=related_project,
    )

    with db.connection() as conn, db.transaction(conn):
        conn.execute(
            "UPDATE fellows SET retired_at = ? WHERE id = ?",
            (now, fellow_id),
        )
        # Discard in-flight work. Already-published projects are NOT
        # touched; the Archive preserves them with disclosure at render
        # time.
        for proj in in_flight:
            conn.execute(
                "UPDATE projects SET state = ?, updated_at = ? WHERE id = ?",
                (State.REJECTED.value, now, proj["id"]),
            )
        decisions.record(conn, decision)

    console.print()
    console.print(f"[bold red]Terminated: {row['name']}[/bold red] ({fellow_id}) for `{kind}`.")
    console.print(f"  Reason: {reason}")
    if in_flight:
        console.print(f"  Discarded {len(in_flight)} in-flight project(s):")
        for proj in in_flight:
            console.print(f"    - {proj['id']} ({proj['state']} → rejected)")
    console.print(
        "[dim]Published work survives in the Archive with disclosure on the blog. "
        "Genome preserved in `genomes/`. The Fellow no longer participates in "
        "any workflow.[/dim]"
    )
    return True


def _format_decision_body(
    *,
    fellow_id: str,
    fellow_name: str,
    rank: str,
    kind: str,
    reason: str,
    in_flight: list,
    now: str,
    triggered_by: str,
    related_project: str | None,
) -> str:
    lines = [
        f"**Fellow:** {fellow_name} (`{fellow_id}`)",
        "",
        f"**Rank at termination:** {rank}",
        "",
        f"**Violation kind:** `{kind}`",
        "",
        f"**Triggered by:** {triggered_by}",
        "",
        f"**Recorded:** {now}",
        "",
        "## Reason",
        "",
        reason.strip(),
    ]
    if related_project:
        lines.extend(
            [
                "",
                f"**Originating project:** `{related_project}`",
            ]
        )
    if in_flight:
        lines.extend(["", "## In-flight projects discarded", ""])
        for proj in in_flight:
            lines.append(f"- `{proj['id']}` ({proj['title']}, state `{proj['state']}` → rejected)")
    lines.extend(
        [
            "",
            "## Disclosure",
            "",
            "Per Chapter 3, this Fellow's already-published work remains "
            "in the Archive. The blog renders a Charter-violation "
            "disclosure banner on each affected piece so readers see the "
            "context. In-flight work is discarded.",
        ]
    )
    return "\n".join(lines)
