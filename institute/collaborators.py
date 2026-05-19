"""Research-group collaborators on a project.

Per Chapter 6, a research group has a lead Fellow plus up to four
additional collaborators. The lead is stored on `projects.lead_fellow_id`;
non-lead co-authors live in `project_collaborators` and are surfaced as
co-authors on the publication, excluded from the reviewer pool for the
project they worked on, and credited toward authorship reputation.

The `role` field distinguishes the slot. v1 uses a single role
(`collaborator`); finer-grained roles like `methodologist` or `critic`
can be added later without a schema change.
"""

from __future__ import annotations

import sqlite3
from dataclasses import dataclass

MAX_COLLABORATORS: int = 4
DEFAULT_ROLE: str = "collaborator"


@dataclass(frozen=True)
class Collaborator:
    project_id: str
    fellow_id: str
    role: str


def add(
    conn: sqlite3.Connection,
    *,
    project_id: str,
    fellow_id: str,
    role: str = DEFAULT_ROLE,
) -> None:
    """Insert a collaborator row. Caller manages the transaction.

    Raises ValueError if the row would violate institutional invariants:
    the lead Fellow cannot also be a collaborator on their own project,
    and a project cannot exceed MAX_COLLABORATORS additional members.
    """
    lead_row = conn.execute(
        "SELECT lead_fellow_id FROM projects WHERE id = ?", (project_id,)
    ).fetchone()
    if lead_row is None:
        raise ValueError(f"No such project: {project_id}")
    if lead_row["lead_fellow_id"] == fellow_id:
        raise ValueError(
            f"Fellow {fellow_id} is already the lead on project {project_id}; "
            "they cannot also be listed as a collaborator."
        )

    existing = conn.execute(
        "SELECT COUNT(*) AS n FROM project_collaborators WHERE project_id = ?",
        (project_id,),
    ).fetchone()
    if existing and int(existing["n"]) >= MAX_COLLABORATORS:
        raise ValueError(
            f"Project {project_id} already has {MAX_COLLABORATORS} collaborators; "
            "Chapter 6 caps research groups at one lead plus four others."
        )

    conn.execute(
        "INSERT OR IGNORE INTO project_collaborators (project_id, fellow_id, role) "
        "VALUES (?, ?, ?)",
        (project_id, fellow_id, role),
    )


def for_project(conn: sqlite3.Connection, project_id: str) -> list[Collaborator]:
    """List collaborators on a project, ordered by fellow id for determinism."""
    rows = list(
        conn.execute(
            "SELECT project_id, fellow_id, role FROM project_collaborators "
            "WHERE project_id = ? ORDER BY fellow_id",
            (project_id,),
        )
    )
    return [
        Collaborator(
            project_id=r["project_id"],
            fellow_id=r["fellow_id"],
            role=r["role"],
        )
        for r in rows
    ]


def collaborator_ids(conn: sqlite3.Connection, project_id: str) -> list[str]:
    """Just the fellow ids, in stable order."""
    return [c.fellow_id for c in for_project(conn, project_id)]


def author_ids(conn: sqlite3.Connection, project_id: str) -> list[str]:
    """All co-author fellow ids: lead first, then collaborators in stable order.

    Returns an empty list if the project does not exist.
    """
    row = conn.execute("SELECT lead_fellow_id FROM projects WHERE id = ?", (project_id,)).fetchone()
    if row is None:
        return []
    return [row["lead_fellow_id"], *collaborator_ids(conn, project_id)]


def is_author(conn: sqlite3.Connection, project_id: str, fellow_id: str) -> bool:
    """Is this Fellow either the lead or a collaborator on this project?"""
    return fellow_id in author_ids(conn, project_id)


def authored_project_ids(conn: sqlite3.Connection, fellow_id: str) -> list[str]:
    """Every project this Fellow has co-authored: as lead or as collaborator."""
    rows = list(
        conn.execute(
            "SELECT id FROM projects WHERE lead_fellow_id = ? "
            "UNION "
            "SELECT project_id AS id FROM project_collaborators WHERE fellow_id = ?",
            (fellow_id, fellow_id),
        )
    )
    return [r["id"] for r in rows]


def decliner_ids(conn: sqlite3.Connection, project_id: str) -> set[str]:
    """Fellows invited to this project's research group who declined.

    Per Chapter 7, declining an invitation is a conflict of interest:
    such a Fellow cannot serve as a peer reviewer on the same project.
    """
    rows = conn.execute(
        "SELECT fellow_id FROM project_invitations WHERE project_id = ? AND decision = 'decline'",
        (project_id,),
    )
    return {r["fellow_id"] for r in rows}
