"""Publish workflow: editorial decision and promotion to the blog.

Given a project in EDITORIAL state with all peer reviews filed, render the
editorial decision and produce the publication artifact:

1. Read all peer reviews from the db.
2. If any reviewer recommended `reject`, the work is published with the
   dissent noted (the design favors transparency over consensus). A
   majority-`reject` would justify killing the project, but in v1 we just
   surface the dissent.
3. Copy the draft to archive/publications/<slug>.md with Astro frontmatter.
4. Copy the lab notebook to blog/src/content/notebooks/<slug>.md.
5. Copy each review to blog/src/content/reviews/<slug>--<reviewer>.md.
6. Transition project to PUBLISHED and emit a decisions record.

Slug derivation: we use the project_id (date + title-slug + hex suffix)
for stability and uniqueness. The blog renders it as the URL path.
"""

from __future__ import annotations

import re
import sqlite3
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

from rich.console import Console

from institute import db, decisions, paths
from institute import fellow as fellow_mod
from institute.state import State

console = Console()


def _atomic_write(path: Path, content: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    tmp = path.with_suffix(path.suffix + ".tmp")
    tmp.write_text(content, encoding="utf-8")
    tmp.replace(path)


def _strip_title_heading(draft_md: str) -> tuple[str, str]:
    """Extract the level-1 title from a draft and return (title, body)."""
    match = re.match(r"\s*#\s+(.+?)\s*\n", draft_md)
    if match:
        title = match.group(1).strip()
        body = draft_md[match.end() :].lstrip("\n")
        return title, body
    return "", draft_md


def _extract_abstract(body_md: str) -> str | None:
    """Pick the first non-empty paragraph as the abstract, if it isn't a heading."""
    for chunk in body_md.split("\n\n"):
        chunk = chunk.strip()
        if not chunk or chunk.startswith("#") or chunk.startswith(">"):
            continue
        # Cap at ~400 chars to keep frontmatter sane.
        return chunk[:400].rstrip()
    return None


def _yaml_string(value: str) -> str:
    """Format a value as a safe single-line YAML string."""
    escaped = value.replace("\\", "\\\\").replace('"', '\\"').replace("\n", " ")
    return f'"{escaped}"'


def _yaml_list(items: list[str]) -> str:
    if not items:
        return "[]"
    return "[" + ", ".join(_yaml_string(i) for i in items) + "]"


def _publication_markdown(
    *,
    title: str,
    body: str,
    authors: list[str],
    reviewers: list[str],
    published_at: datetime,
    project_id: str,
    abstract: str | None,
    has_notebook: bool,
    has_reviews: bool,
) -> str:
    frontmatter_lines = [
        "---",
        f"title: {_yaml_string(title)}",
        f"authors: {_yaml_list(authors)}",
        f"publishedAt: {published_at.date().isoformat()}",
        f"projectId: {_yaml_string(project_id)}",
        f"hasNotebook: {'true' if has_notebook else 'false'}",
        f"hasReviews: {'true' if has_reviews else 'false'}",
    ]
    if reviewers:
        frontmatter_lines.append(f"reviewers: {_yaml_list(reviewers)}")
    if abstract:
        frontmatter_lines.append(f"abstract: {_yaml_string(abstract)}")
    frontmatter_lines.append("---")
    frontmatter_lines.append("")
    return "\n".join(frontmatter_lines) + body.rstrip() + "\n"


def _notebook_markdown(
    *,
    title: str,
    body: str,
    project_id: str,
    post_slug: str,
    authors: list[str],
    started_at: datetime,
    completed_at: datetime,
) -> str:
    frontmatter = [
        "---",
        f"title: {_yaml_string(title + ' — lab notebook')}",
        f"postSlug: {_yaml_string(post_slug)}",
        f"projectId: {_yaml_string(project_id)}",
        f"authors: {_yaml_list(authors)}",
        f"startedAt: {started_at.date().isoformat()}",
        f"completedAt: {completed_at.date().isoformat()}",
        "---",
        "",
    ]
    return "\n".join(frontmatter) + body.rstrip() + "\n"


def _review_markdown(
    *,
    title: str,
    body: str,
    reviewer: str,
    role: str,
    recommendation: str,
    confidence: str,
    post_slug: str,
    submitted_at: datetime,
    dissent: bool,
) -> str:
    frontmatter = [
        "---",
        f"title: {_yaml_string('Review by ' + reviewer)}",
        f"postSlug: {_yaml_string(post_slug)}",
        f"reviewer: {_yaml_string(reviewer)}",
        f"role: {role}",
        f"recommendation: {recommendation}",
        f"confidence: {confidence}",
        f"submittedAt: {submitted_at.date().isoformat()}",
        f"dissent: {'true' if dissent else 'false'}",
        "---",
        "",
    ]
    # Body already includes the review heading and structure; we keep it.
    return "\n".join(frontmatter) + body.rstrip() + "\n"


def _gather_reviews(conn: sqlite3.Connection, project_id: str) -> list[dict[str, Any]]:
    return [
        dict(row)
        for row in conn.execute(
            "SELECT reviewer_id, role, recommendation, confidence, content_path, "
            "submitted_at, dissent FROM reviews WHERE project_id = ? ORDER BY role",
            (project_id,),
        )
    ]


def run(project_id: str) -> None:
    """Publish a project in EDITORIAL state to the blog and archive."""
    with db.connection() as conn:
        proj = conn.execute(
            "SELECT id, title, state, draft_path, notebook_path, lead_fellow_id, "
            "created_at FROM projects WHERE id = ?",
            (project_id,),
        ).fetchone()
        if proj is None:
            raise SystemExit(f"No such project: {project_id}")
        if proj["state"] != State.EDITORIAL.value:
            raise SystemExit(
                f"Project {project_id} is in state {proj['state']}, expected editorial."
            )
        if not proj["draft_path"]:
            raise SystemExit(f"Project {project_id} has no draft.")

        lead = fellow_mod.load_genome(conn, proj["lead_fellow_id"])
        reviews_data = _gather_reviews(conn, project_id)
        # Resolve reviewer names from their ids.
        reviewer_genomes = [fellow_mod.load_genome(conn, r["reviewer_id"]) for r in reviews_data]
        draft_md = (paths.ROOT / proj["draft_path"]).read_text(encoding="utf-8")
        notebook_md = (
            (paths.ROOT / proj["notebook_path"]).read_text(encoding="utf-8")
            if proj["notebook_path"]
            else None
        )

    title, body = _strip_title_heading(draft_md)
    if not title:
        title = proj["title"]

    now = datetime.now(UTC)
    started = datetime.fromisoformat(proj["created_at"])
    abstract = _extract_abstract(body)
    slug = project_id  # stable, unique, sortable
    authors = [lead.name]
    reviewer_names = [g.name for g in reviewer_genomes]

    # Compose publication artifact (archive + blog content)
    publication_md = _publication_markdown(
        title=title,
        body=body,
        authors=authors,
        reviewers=reviewer_names,
        published_at=now,
        project_id=project_id,
        abstract=abstract,
        has_notebook=notebook_md is not None,
        has_reviews=bool(reviews_data),
    )

    publication_archive_path = paths.PUBLICATIONS / f"{slug}.md"
    publication_blog_path = paths.BLOG_POSTS / f"{slug}.md"
    _atomic_write(publication_archive_path, publication_md)
    _atomic_write(publication_blog_path, publication_md)

    if notebook_md is not None:
        nb_text = _notebook_markdown(
            title=title,
            body=notebook_md,
            project_id=project_id,
            post_slug=slug,
            authors=authors,
            started_at=started,
            completed_at=now,
        )
        _atomic_write(paths.BLOG_NOTEBOOKS / f"{slug}.md", nb_text)

    for review, genome in zip(reviews_data, reviewer_genomes, strict=False):
        review_body = (paths.ROOT / review["content_path"]).read_text(encoding="utf-8")
        review_text = _review_markdown(
            title=title,
            body=review_body,
            reviewer=genome.name,
            role=review["role"],
            recommendation=review["recommendation"],
            confidence=review["confidence"],
            post_slug=slug,
            submitted_at=datetime.fromisoformat(review["submitted_at"]),
            dissent=bool(review["dissent"]),
        )
        _atomic_write(paths.BLOG_REVIEWS / f"{slug}--{genome.id}.md", review_text)

    has_dissent = any(r["recommendation"] == "reject" for r in reviews_data)
    decision_body_lines = [
        f"**Title:** {title}",
        f"**Lead Fellow:** {lead.name} (`{lead.id}`)",
        f"**Reviewers:** {', '.join(reviewer_names) if reviewer_names else 'none'}",
        "",
        f"**Publication:** [{publication_archive_path.relative_to(paths.ROOT)}]"
        f"({publication_archive_path.relative_to(paths.ROOT)})",
        f"**Blog post:** [{publication_blog_path.relative_to(paths.ROOT)}]"
        f"({publication_blog_path.relative_to(paths.ROOT)})",
        "",
        "Editorial outcome: accepted. "
        + ("Includes dissenting review(s)." if has_dissent else "Reviews were unanimous."),
    ]
    decision = decisions.Decision(
        kind="publication",
        title=f"Published: {title}",
        body="\n".join(decision_body_lines),
        actors=["editorial-board", lead.id, *(g.id for g in reviewer_genomes)],
        related_project=project_id,
    )

    timestamp = now.isoformat(timespec="seconds")
    with db.connection() as conn, db.transaction(conn):
        conn.execute(
            "UPDATE projects SET state = ?, publication_slug = ?, title = ?, updated_at = ? "
            "WHERE id = ?",
            (State.PUBLISHED.value, slug, title, timestamp, project_id),
        )
        decisions.record(conn, decision)

    console.print()
    console.print(f"[bold green]Published.[/bold green] Title: {title}")
    console.print(f"[green]Archive:[/green]   {publication_archive_path.relative_to(paths.ROOT)}")
    console.print(f"[green]Blog post:[/green] {publication_blog_path.relative_to(paths.ROOT)}")
    if has_dissent:
        console.print("[yellow]Includes dissenting review(s).[/yellow]")
    console.print(
        "[dim]Run `cd blog && npm run build` to preview locally, or push to deploy.[/dim]"
    )
