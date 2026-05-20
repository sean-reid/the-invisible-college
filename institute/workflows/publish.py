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

from institute import (
    citation_lint,
    code_artifacts,
    collaborators,
    db,
    decisions,
    editorial_followups,
    episodic,
    paths,
    state,
)
from institute import fellow as fellow_mod
from institute.state import State

console = Console()


def _atomic_write(path: Path, content: str) -> None:
    from institute.safe_io import atomic_write

    atomic_write(path, content)


def _strip_title_heading(draft_md: str) -> tuple[str, str]:
    """Extract the level-1 title from a draft and return (title, body)."""
    match = re.match(r"\s*#\s+(.+?)\s*\n", draft_md)
    if match:
        title = match.group(1).strip()
        body = draft_md[match.end() :].lstrip("\n")
        return title, body
    return "", draft_md


def _read_abstract_file(project_id: str) -> str | None:
    """Return the Fellow-written abstract if it exists."""
    path = paths.DRAFTS / project_id / "abstract.txt"
    if not path.is_file():
        return None
    text = path.read_text(encoding="utf-8").strip()
    return text or None


def _extract_abstract_fallback(body_md: str) -> str | None:
    """Fallback for pieces published before abstracts were a separate field.

    Picks the first non-empty body paragraph that is not a heading or
    blockquote. Returns the full paragraph (no truncation); the styling
    handles whatever length comes back.
    """
    for chunk in body_md.split("\n\n"):
        chunk = chunk.strip()
        if not chunk or chunk.startswith("#") or chunk.startswith(">"):
            continue
        return chunk
    return None


_ISSUE_RE = re.compile(r"^issueNumber:\s*(\d+)\s*$", re.MULTILINE)


def _next_issue_number() -> int:
    """Return one more than the max `issueNumber` across blog post frontmatters.

    We look at the blog content directory (which is the authoritative copy
    consumed by the build) rather than the archive, because hand-authored
    pieces like First Light only exist in the blog content. Falls back to 1
    when no existing publications are found.
    """
    max_seen = 0
    if paths.BLOG_POSTS.is_dir():
        for md in paths.BLOG_POSTS.glob("*.md"):
            text = md.read_text(encoding="utf-8")
            m = _ISSUE_RE.search(text)
            if m:
                max_seen = max(max_seen, int(m.group(1)))
    return max_seen + 1


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
    issue_number: int,
    abstract: str | None,
    has_notebook: bool,
    has_reviews: bool,
) -> str:
    # Use a full ISO timestamp (not just the date) so same-day publications
    # sort deterministically by the moment they actually went out.
    iso = published_at.isoformat(timespec="seconds")
    if iso.endswith("+00:00"):
        iso = iso[:-6] + "Z"
    frontmatter_lines = [
        "---",
        f"title: {_yaml_string(title)}",
        f"issueNumber: {issue_number}",
        f"authors: {_yaml_list(authors)}",
        f"publishedAt: {iso}",
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
    round_number: int,
) -> str:
    round_title = (
        f"Round-{round_number} review by {reviewer}"
        if round_number > 1
        else f"Review by {reviewer}"
    )
    frontmatter = [
        "---",
        f"title: {_yaml_string(round_title)}",
        f"postSlug: {_yaml_string(post_slug)}",
        f"reviewer: {_yaml_string(reviewer)}",
        f"role: {role}",
        f"recommendation: {recommendation}",
        f"confidence: {confidence}",
        f"submittedAt: {submitted_at.date().isoformat()}",
        f"dissent: {'true' if dissent else 'false'}",
        f"round: {round_number}",
        "---",
        "",
    ]
    return "\n".join(frontmatter) + body.rstrip() + "\n"


def _gather_reviews(conn: sqlite3.Connection, project_id: str) -> list[dict[str, Any]]:
    return [
        dict(row)
        for row in conn.execute(
            "SELECT reviewer_id, role, recommendation, confidence, content_path, "
            "submitted_at, dissent, round FROM reviews WHERE project_id = ? "
            "ORDER BY round, role",
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
        collaborator_genomes = [
            fellow_mod.load_genome(conn, c.fellow_id)
            for c in collaborators.for_project(conn, project_id)
        ]
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

    # Refuse drafts that cite other publications by number. The home
    # page has no stable visible numbering, so `#NN` references do
    # not resolve. The writing briefs already forbid this; this is
    # the hard tripwire.
    citation_lint.check(body)

    now = datetime.now(UTC)
    started = datetime.fromisoformat(proj["created_at"])
    abstract = _read_abstract_file(project_id) or _extract_abstract_fallback(body)
    slug = project_id  # stable, unique, sortable
    author_genomes = [lead, *collaborator_genomes]
    authors = [g.name for g in author_genomes]
    reviewer_names = [g.name for g in reviewer_genomes]
    issue_number = _next_issue_number()

    # Editorial pass: a Senior Fellow (not lead, not collaborator, not
    # reviewer) reads the draft and the candidate follow-up questions
    # the research/peer-review workflows captured, picks at most three,
    # and the rest are dropped. The selected ones are spliced into the
    # body above `## References`. Done before composing the publication
    # so the rendered artifact carries the editor's selection.
    with db.connection() as conn:
        editorial_result = editorial_followups.run(
            conn=conn,
            project_id=project_id,
            draft_md=draft_md,
            lead_id=lead.id,
            collaborator_ids=[g.id for g in collaborator_genomes],
            reviewer_ids=[g.id for g in reviewer_genomes],
        )
    if editorial_result.footer_md:
        body = editorial_followups.splice_above_references(body, editorial_result.footer_md)

    # Compose publication artifact (archive + blog content)
    publication_md = _publication_markdown(
        title=title,
        body=body,
        authors=authors,
        reviewers=reviewer_names,
        published_at=now,
        project_id=project_id,
        issue_number=issue_number,
        abstract=abstract,
        has_notebook=notebook_md is not None,
        has_reviews=bool(reviews_data),
    )

    publication_archive_path = paths.PUBLICATIONS / f"{slug}.md"
    publication_blog_path = paths.BLOG_POSTS / f"{slug}.md"
    _atomic_write(publication_archive_path, publication_md)
    _atomic_write(publication_blog_path, publication_md)

    # Mirror any code/data artifacts the research and revise steps
    # archived into the blog's public/ tree so the static site can
    # serve them alongside the post.
    mirrored_artifacts = code_artifacts.mirror_to_blog(project_id)

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
        review_round = int(review.get("round") or 1)
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
            round_number=review_round,
        )
        suffix = f"--r{review_round}" if review_round > 1 else ""
        _atomic_write(paths.BLOG_REVIEWS / f"{slug}--{genome.id}{suffix}.md", review_text)

    has_dissent = any(r["recommendation"] == "reject" for r in reviews_data)
    decision_body_lines = [
        f"**Title:** {title}",
        f"**Lead Fellow:** {lead.name} (`{lead.id}`)",
    ]
    if collaborator_genomes:
        members = ", ".join(f"{g.name} (`{g.id}`)" for g in collaborator_genomes)
        decision_body_lines.append(f"**Collaborators:** {members}")
    decision_body_lines.extend(
        [
            f"**Reviewers:** {', '.join(reviewer_names) if reviewer_names else 'none'}",
        ]
    )
    if editorial_result.editor is not None:
        decision_body_lines.append(
            f"**Follow-ups editor:** {editorial_result.editor.name} "
            f"(`{editorial_result.editor.id}`) — promoted "
            f"{len(editorial_result.promoted)}, discarded "
            f"{len(editorial_result.discarded)}"
        )
    decision_body_lines.extend(
        [
            "",
            f"**Publication:** [{publication_archive_path.relative_to(paths.ROOT)}]"
            f"({publication_archive_path.relative_to(paths.ROOT)})",
            f"**Blog post:** [{publication_blog_path.relative_to(paths.ROOT)}]"
            f"({publication_blog_path.relative_to(paths.ROOT)})",
            "",
            "Editorial outcome: accepted. "
            + ("Includes dissenting review(s)." if has_dissent else "Reviews were unanimous."),
        ]
    )
    actors = [
        "editorial-board",
        lead.id,
        *(g.id for g in collaborator_genomes),
        *(g.id for g in reviewer_genomes),
    ]
    if editorial_result.editor is not None and editorial_result.editor.id not in actors:
        actors.append(editorial_result.editor.id)
    decision = decisions.Decision(
        kind="publication",
        title=f"Published: {title}",
        body="\n".join(decision_body_lines),
        actors=actors,
        related_project=project_id,
    )

    timestamp = now.isoformat(timespec="seconds")

    # Detect qualifying-project publication so we can auto-promote the
    # Postulant in the same transaction.
    with db.connection() as conn:
        kind_row = conn.execute("SELECT kind FROM projects WHERE id = ?", (project_id,)).fetchone()
    is_qualifying = kind_row is not None and kind_row["kind"] == "qualifying"

    with db.connection() as conn, db.transaction(conn):
        state.transition(conn, project_id, State.PUBLISHED)
        conn.execute(
            "UPDATE projects SET publication_slug = ?, title = ? WHERE id = ?",
            (slug, title, project_id),
        )
        decisions.record(conn, decision)
        if is_qualifying:
            _auto_promote_to_novice(conn, lead.id, project_id, timestamp)

    # Every co-author gets the published piece in their episodic memory
    # so future proposals and reviews can build on their own published work.
    for author in author_genomes:
        episodic.safe_ingest(
            fellow_id=author.id,
            kind="publication",
            title=title,
            content=body,
            source_path=str(publication_archive_path.relative_to(paths.ROOT)),
            project_id=project_id,
            metadata={
                "slug": slug,
                "issue": issue_number,
                "role": "lead" if author.id == lead.id else "collaborator",
            },
        )

    console.print()
    console.print(f"[bold green]Published.[/bold green] Title: {title}")
    console.print(f"[green]Archive:[/green]   {publication_archive_path.relative_to(paths.ROOT)}")
    console.print(f"[green]Blog post:[/green] {publication_blog_path.relative_to(paths.ROOT)}")
    if editorial_result.editor is not None:
        console.print(
            f"[green]Follow-ups editor:[/green] {editorial_result.editor.name} "
            f"(promoted {len(editorial_result.promoted)}, "
            f"discarded {len(editorial_result.discarded)})"
        )
    if mirrored_artifacts:
        console.print(
            f"[green]Code/data artifacts:[/green] {len(mirrored_artifacts)} "
            f"file(s) at blog/public/code/{slug}/"
        )
    if has_dissent:
        console.print("[yellow]Includes dissenting review(s).[/yellow]")
    if is_qualifying:
        console.print(
            f"[bold green]Postulant {lead.name} → Novice.[/bold green] Qualifying project complete."
        )
    console.print(
        "[dim]Run `cd blog && npm run build` to preview locally, or push to deploy.[/dim]"
    )


def _auto_promote_to_novice(conn, postulant_id: str, project_id: str, timestamp: str) -> None:
    """Advance a Postulant to Novice on successful qualifying-project publication.

    Per Chapter 5: a successful qualifying project promotes the
    Postulant. Done inside the publication transaction so the rank
    change cannot land without the qualifying piece being live.
    """
    row = conn.execute("SELECT rank, name FROM fellows WHERE id = ?", (postulant_id,)).fetchone()
    if row is None or row["rank"] != "postulant":
        return  # nothing to do (already advanced or not a postulant)

    # Rewrite the genome on disk to reflect the new rank.
    from institute import fellow as fellow_mod  # local import to avoid cycle
    from institute.fellow import Genome

    genome = Genome.from_file(fellow_mod.genome_path(postulant_id))
    genome.model_copy(update={"rank": "novice"}).write(fellow_mod.genome_path(postulant_id))
    conn.execute("UPDATE fellows SET rank = 'novice' WHERE id = ?", (postulant_id,))
    decision = decisions.Decision(
        kind="promotion",
        title=f"{row['name']}: postulant to novice",
        body=(
            f"**Fellow:** {row['name']} (`{postulant_id}`)\n\n"
            f"**Rank change:** postulant → novice\n\n"
            f"**Trigger:** qualifying project published as `{project_id}`.\n\n"
            "Per Chapter 5, a successful qualifying project advances the "
            "Postulant to Novice. This promotion is automatic on publication."
        ),
        actors=["orchestrator", postulant_id],
    )
    decisions.record(conn, decision)
