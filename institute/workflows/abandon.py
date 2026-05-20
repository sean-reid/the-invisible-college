"""Abandon a project with an honest record of what was learned.

Per Chapter 6, a Fellow may abandon any in-flight project. The
abandonment is *not* a rejection — the work is preserved, the
reasoning is logged, and the lesson (what was tried, why it stopped
being worth pursuing) is recorded for the Archive. The state
machine routes the project to ABANDONED (terminal) so it stops
appearing as in-flight, but everything written so far remains.

The lesson markdown is written to
`archive/abandonments/<project_id>.md`. It captures:

  * who abandoned it,
  * what state it was in,
  * what the lead Fellow learned that made continuing the wrong
    move (the "honest lesson"),
  * pointers to whatever artifacts (proposal, draft, notebook,
    reviews) exist so a future Fellow can find them.

This is the appropriate path for a Fellow who, mid-research,
discovers the question is unanswerable as posed, or that the
finding will be uninteresting, or that the proposal's premise is
wrong. The Charter values honest failure over silent abandonment.
"""

from __future__ import annotations

from datetime import UTC, datetime

from rich.console import Console

from institute import db, decisions, paths, state
from institute import fellow as fellow_mod
from institute.state import State

console = Console()


ABANDONMENT_DIR = paths.ARCHIVE / "abandonments"


def _render_lesson_md(
    *,
    project_id: str,
    title: str,
    lead_name: str,
    lead_id: str,
    last_state: str,
    reason: str,
    lesson: str,
    abandoned_at: str,
) -> str:
    lines = [
        "---",
        f"projectId: \"{project_id}\"",
        f"title: \"{title.replace(chr(34), chr(39))}\"",
        f"leadFellow: \"{lead_name} ({lead_id})\"",
        f"lastState: {last_state}",
        f"abandonedAt: {abandoned_at}",
        "---",
        "",
        f"# Abandoned: {title}",
        "",
        f"**Lead Fellow:** {lead_name} (`{lead_id}`)",
        "",
        f"**Last state before abandonment:** `{last_state}`",
        "",
        f"**Reason given:** {reason}",
        "",
        "## Honest lesson",
        "",
        lesson.strip(),
        "",
        "## Artifacts preserved",
        "",
        "All work produced before abandonment remains in the archive:",
        f"- `archive/proposals/{project_id}/`",
        f"- `archive/drafts/{project_id}/` (if any draft was written)",
        f"- `archive/lab-notebooks/{project_id}/` (if any notebook was written)",
        f"- `archive/reviews/{project_id}/` (if any reviews were filed)",
        "",
        "These files are not deleted. The project is closed; the work is",
        "available for any future Fellow asking a related question.",
    ]
    return "\n".join(lines) + "\n"


def run(
    project_id: str,
    *,
    reason: str,
    lesson: str,
    actor: str | None = None,
) -> None:
    """Mark a project as abandoned and record the honest lesson.

    Args:
        project_id: target project
        reason: one-line reason given by the Fellow or operator
        lesson: multi-paragraph lesson learned (what was tried,
            why it stopped being worth pursuing). Required.
        actor: id of the Fellow or 'founder' driving the abandonment.
            Defaults to the project's lead.
    """
    if not lesson.strip():
        raise SystemExit(
            "Abandonment requires an honest lesson. Pass --lesson with "
            "what the work taught you that made continuing wrong."
        )

    with db.connection() as conn:
        proj = conn.execute(
            "SELECT id, title, state, lead_fellow_id FROM projects WHERE id = ?",
            (project_id,),
        ).fetchone()
        if proj is None:
            raise SystemExit(f"No such project: {project_id}")
        if proj["state"] in {State.PUBLISHED.value, State.REJECTED.value, State.ABANDONED.value}:
            raise SystemExit(
                f"Project {project_id} is in terminal state {proj['state']}; cannot abandon."
            )
        lead = fellow_mod.load_genome(conn, proj["lead_fellow_id"])

    abandoned_by = actor or lead.id
    now = datetime.now(UTC).isoformat(timespec="seconds")
    lesson_md = _render_lesson_md(
        project_id=project_id,
        title=proj["title"] or project_id,
        lead_name=lead.name,
        lead_id=lead.id,
        last_state=proj["state"],
        reason=reason,
        lesson=lesson,
        abandoned_at=now,
    )

    from institute.safe_io import atomic_write

    lesson_path = ABANDONMENT_DIR / f"{project_id}.md"
    atomic_write(lesson_path, lesson_md)

    decision = decisions.Decision(
        kind="abandonment",
        title=f"Abandoned: {proj['title'] or project_id}",
        body=(
            f"**Lead Fellow:** {lead.name} (`{lead.id}`)\n\n"
            f"**Last state:** `{proj['state']}`\n\n"
            f"**Reason:** {reason}\n\n"
            f"**Lesson file:** `{lesson_path.relative_to(paths.ROOT)}`\n\n"
            "The project transitions to `abandoned` and stops appearing as "
            "in-flight. All accumulated work remains in the archive."
        ),
        actors=[abandoned_by, lead.id] if abandoned_by != lead.id else [lead.id],
        related_project=project_id,
    )
    with db.connection() as conn, db.transaction(conn):
        state.transition(conn, project_id, State.ABANDONED)
        decisions.record(conn, decision)

    console.print(
        f"[yellow]Abandoned.[/yellow] Lesson written to "
        f"{lesson_path.relative_to(paths.ROOT)}."
    )
