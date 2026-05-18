"""Backfill episodic memory from existing archive artifacts.

Walks the Archive (proposals, lab notebooks, drafts, reviews) and the
curriculum responses, and ingests each artifact into the owning Fellow's
episodic memory. Idempotent in the sense that re-running will simply
re-ingest entries — the table has no UNIQUE constraint on content, so
duplicates are possible. Run it once after the episodic memory feature
lands, or after manually editing archive content.

The first run pays the model-download cost (~30MB) and the embedding
cost. Subsequent runs are limited by IO and CPU.
"""

from __future__ import annotations

import re

from rich.console import Console

from institute import db, episodic, paths

console = Console()


_FRONTMATTER_RE = re.compile(r"^---\n(.*?)\n---\n", re.DOTALL)


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
        episodic.safe_ingest(
            fellow_id=fellow_id,
            kind="curriculum_response",
            title=f"Curriculum response: {r['item_id']}",
            content=content,
            source_path=str(path.relative_to(paths.ROOT)),
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
    """Reviews filed on projects this Fellow led."""
    with db.connection() as conn:
        rows = list(
            conn.execute(
                "SELECT r.project_id, r.reviewer_id, r.role, r.recommendation, "
                "       r.round, r.content_path, p.title, f.name AS reviewer_name "
                "FROM reviews r JOIN projects p ON p.id = r.project_id "
                "LEFT JOIN fellows f ON f.id = r.reviewer_id "
                "WHERE p.lead_fellow_id = ? AND r.reviewer_id != ?",
                (fellow_id, fellow_id),
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
    """Ingest the contents of one file. Returns 1 on success, 0 on skip."""
    path = paths.ROOT / rel_path
    if not path.is_file():
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


def _strip_frontmatter(text: str) -> str:
    """Drop a leading YAML frontmatter block if present. Embeddings should
    see the prose, not the metadata."""
    return _FRONTMATTER_RE.sub("", text, count=1)
