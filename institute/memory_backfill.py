"""Backfill episodic memory from existing archive artifacts.

Walks the Archive (proposals, lab notebooks, drafts, reviews,
publications, contributions) and the curriculum responses, and ingests
each artifact into the owning Fellow's episodic memory.

Idempotent: every ingest is gated on (fellow_id, kind, source_path),
so a re-run only inserts entries that are genuinely missing — past
publications that were dropped because of a kind-vocab miss get
filled in without duplicating anything already on file.

The first run pays the model-download cost (~30MB) and the embedding
cost. Subsequent runs are limited by IO and CPU.
"""

from __future__ import annotations

import re

from rich.console import Console

from institute import collaborators, db, episodic, paths

console = Console()


_FRONTMATTER_RE = re.compile(r"^---\n(.*?)\n---\n", re.DOTALL)


def _already_ingested(fellow_id: str, kind: str, rel_path: str) -> bool:
    """True iff this (fellow, kind, source_path) combo is already in the table.

    Source path is the natural natural key for backfill: each archive
    artifact has exactly one canonical path. If we've seen it before,
    skip; otherwise ingest.
    """
    with db.connection() as conn:
        row = conn.execute(
            "SELECT 1 FROM episodic_memory "
            "WHERE fellow_id = ? AND kind = ? AND source_path = ? LIMIT 1",
            (fellow_id, kind, rel_path),
        ).fetchone()
    return row is not None


def run(fellow_id: str | None = None) -> None:
    """Backfill memory for one Fellow, or every active Fellow when None."""
    with db.connection() as conn:
        if fellow_id is not None:
            rows = list(conn.execute("SELECT id, name FROM fellows WHERE id = ?", (fellow_id,)))
            if not rows:
                console.print(f"[red]No such Fellow: `{fellow_id}`.[/red]")
                return
        else:
            rows = list(
                conn.execute("SELECT id, name FROM fellows WHERE retired_at IS NULL ORDER BY name")
            )

    total = 0
    for r in rows:
        n = _backfill_one(r["id"], r["name"])
        total += n
        console.print(f"[green]{r['name']} ({r['id']}):[/green] {n} entries ingested.")
    console.print()
    console.print(
        f"[bold green]Backfill complete:[/bold green] {total} entries across {len(rows)} Fellow(s)."
    )


def _backfill_one(fellow_id: str, fellow_name: str) -> int:
    """Ingest every backfillable artifact for one Fellow. Returns count."""
    count = 0
    count += _ingest_curriculum_responses(fellow_id)
    count += _ingest_authored_projects(fellow_id)
    count += _ingest_co_authored_projects(fellow_id)
    count += _ingest_publications(fellow_id)
    count += _ingest_reviews_given(fellow_id)
    count += _ingest_reviews_received(fellow_id)
    return count


def _ingest_curriculum_responses(fellow_id: str) -> int:
    """Pull responses from the curriculum_responses table + read the files."""
    with db.connection() as conn:
        rows = list(
            conn.execute(
                "SELECT item_id, response_path, submitted_at "
                "FROM curriculum_responses WHERE fellow_id = ?",
                (fellow_id,),
            )
        )
    n = 0
    for r in rows:
        path = paths.ROOT / r["response_path"]
        if not path.is_file():
            continue
        content = path.read_text(encoding="utf-8")
        if not content.strip():
            continue
        rel = str(path.relative_to(paths.ROOT))
        if _already_ingested(fellow_id, "curriculum_response", rel):
            continue
        episodic.safe_ingest(
            fellow_id=fellow_id,
            kind="curriculum_response",
            title=f"Curriculum response: {r['item_id']}",
            content=content,
            source_path=rel,
            metadata={"item_id": r["item_id"], "submitted_at": r["submitted_at"]},
        )
        n += 1
    return n


def _ingest_authored_projects(fellow_id: str) -> int:
    """Proposals, lab notebooks, drafts for projects this Fellow led."""
    with db.connection() as conn:
        rows = list(
            conn.execute(
                "SELECT id, title, kind, proposal_path, notebook_path, draft_path "
                "FROM projects WHERE lead_fellow_id = ?",
                (fellow_id,),
            )
        )
    n = 0
    for r in rows:
        project_id = r["id"]
        title = r["title"] or project_id
        if r["proposal_path"]:
            n += _ingest_file(
                fellow_id,
                kind="proposal",
                title=f"Proposal: {title}",
                rel_path=r["proposal_path"],
                project_id=project_id,
                metadata={"kind": r["kind"]},
            )
        if r["notebook_path"]:
            n += _ingest_file(
                fellow_id,
                kind="lab_notebook",
                title=f"Lab notebook: {title}",
                rel_path=r["notebook_path"],
                project_id=project_id,
            )
        if r["draft_path"]:
            n += _ingest_file(
                fellow_id,
                kind="draft",
                title=title,
                rel_path=r["draft_path"],
                project_id=project_id,
            )
    return n


def _ingest_reviews_given(fellow_id: str) -> int:
    """Reviews this Fellow filed on others' work."""
    with db.connection() as conn:
        rows = list(
            conn.execute(
                "SELECT r.project_id, r.role, r.recommendation, r.round, "
                "       r.content_path, p.title "
                "FROM reviews r LEFT JOIN projects p ON p.id = r.project_id "
                "WHERE r.reviewer_id = ?",
                (fellow_id,),
            )
        )
    n = 0
    for r in rows:
        if not r["content_path"]:
            continue
        title = (
            f"Round {r['round']} review of {r['title'] or r['project_id']} "
            f"({r['role']}, recommended {r['recommendation']})"
        )
        n += _ingest_file(
            fellow_id,
            kind="review_given",
            title=title,
            rel_path=r["content_path"],
            project_id=r["project_id"],
            metadata={
                "round": r["round"],
                "role": r["role"],
                "recommendation": r["recommendation"],
            },
        )
    return n


def _ingest_reviews_received(fellow_id: str) -> int:
    """Reviews filed on projects this Fellow co-authored (lead or collaborator).

    Chapter 6 research groups receive reviews collectively: the live
    peer_review step ingests review_received for every author, so the
    backfill must do the same to stay in sync.
    """
    with db.connection() as conn:
        co_authored = set(collaborators.authored_project_ids(conn, fellow_id))
    if not co_authored:
        return 0
    placeholders = ",".join("?" * len(co_authored))
    with db.connection() as conn:
        rows = list(
            conn.execute(
                f"SELECT r.project_id, r.reviewer_id, r.role, r.recommendation, "
                f"       r.round, r.content_path, p.title, f.name AS reviewer_name "
                f"FROM reviews r JOIN projects p ON p.id = r.project_id "
                f"LEFT JOIN fellows f ON f.id = r.reviewer_id "
                f"WHERE r.project_id IN ({placeholders}) AND r.reviewer_id != ?",
                (*co_authored, fellow_id),
            )
        )
    n = 0
    for r in rows:
        if not r["content_path"]:
            continue
        title = (
            f"Review from {r['reviewer_name'] or r['reviewer_id']} on "
            f"{r['title'] or r['project_id']} (round {r['round']})"
        )
        n += _ingest_file(
            fellow_id,
            kind="review_received",
            title=title,
            rel_path=r["content_path"],
            project_id=r["project_id"],
            metadata={
                "reviewer": r["reviewer_id"],
                "round": r["round"],
                "recommendation": r["recommendation"],
            },
        )
    return n


def _ingest_file(
    fellow_id: str,
    *,
    kind: str,
    title: str,
    rel_path: str,
    project_id: str | None = None,
    metadata: dict | None = None,
) -> int:
    """Ingest the contents of one file. Returns 1 on success, 0 on skip.

    Skips when the (fellow_id, kind, source_path) triple is already in
    episodic_memory, so re-running backfill never duplicates.
    """
    path = paths.ROOT / rel_path
    if not path.is_file():
        return 0
    if _already_ingested(fellow_id, kind, rel_path):
        return 0
    content = path.read_text(encoding="utf-8")
    if not content.strip():
        return 0
    episodic.safe_ingest(
        fellow_id=fellow_id,
        kind=kind,
        title=title,
        content=_strip_frontmatter(content),
        source_path=rel_path,
        project_id=project_id,
        metadata=metadata,
    )
    return 1


def _ingest_co_authored_projects(fellow_id: str) -> int:
    """Proposals, lab notebooks, drafts for projects this Fellow collaborated on
    (but did not lead). Mirrors what propose+research now ingest live."""
    with db.connection() as conn:
        rows = list(
            conn.execute(
                "SELECT p.id, p.title, p.kind, p.proposal_path, p.notebook_path, "
                "       p.draft_path "
                "FROM project_collaborators pc "
                "JOIN projects p ON p.id = pc.project_id "
                "WHERE pc.fellow_id = ?",
                (fellow_id,),
            )
        )
    n = 0
    for r in rows:
        project_id = r["id"]
        title = r["title"] or project_id
        if r["proposal_path"]:
            n += _ingest_file(
                fellow_id,
                kind="proposal",
                title=f"Joined research group: {title}",
                rel_path=r["proposal_path"],
                project_id=project_id,
            )
        if r["draft_path"]:
            n += _ingest_file(
                fellow_id,
                kind="draft",
                title=title,
                rel_path=r["draft_path"],
                project_id=project_id,
            )
        # The collaborator's own contribution.md lives under
        # archive/lab-notebooks/<project>/contributions/<fellow>.md.
        contribution_rel = f"archive/lab-notebooks/{project_id}/contributions/{fellow_id}.md"
        if (paths.ROOT / contribution_rel).is_file():
            n += _ingest_file(
                fellow_id,
                kind="contribution",
                title=f"Contribution to research group on {project_id}",
                rel_path=contribution_rel,
                project_id=project_id,
            )
    return n


def _ingest_publications(fellow_id: str) -> int:
    """The published piece for every project this Fellow co-authored
    (as lead OR collaborator). Backfills the per-author publication
    ingest that the multi-author publish step was silently dropping."""
    with db.connection() as conn:
        project_ids = collaborators.authored_project_ids(conn, fellow_id)
        if not project_ids:
            return 0
        placeholders = ",".join("?" * len(project_ids))
        rows = list(
            conn.execute(
                f"SELECT id, title, publication_slug, lead_fellow_id "
                f"FROM projects WHERE id IN ({placeholders}) "
                f"  AND state = 'published'",
                tuple(project_ids),
            )
        )
    n = 0
    for r in rows:
        project_id = r["id"]
        slug = r["publication_slug"] or project_id
        rel = f"archive/publications/{slug}.md"
        if not (paths.ROOT / rel).is_file():
            continue
        n += _ingest_file(
            fellow_id,
            kind="publication",
            title=r["title"] or project_id,
            rel_path=rel,
            project_id=project_id,
            metadata={
                "slug": slug,
                "role": "lead" if r["lead_fellow_id"] == fellow_id else "collaborator",
            },
        )
    return n


def _strip_frontmatter(text: str) -> str:
    """Drop a leading YAML frontmatter block if present. Embeddings should
    see the prose, not the metadata."""
    return _FRONTMATTER_RE.sub("", text, count=1)
