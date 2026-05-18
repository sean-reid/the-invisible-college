"""Curriculum response: the Postulant engages one curriculum item.

Each invocation handles one un-completed item. Re-running the workflow
walks through the curriculum one item at a time. The Postulant writes a
substantive response (no passive consumption); the response is filed
to `archive/curriculum/<postulant>/responses/<item-id>.md` and recorded
in the `curriculum_responses` table.

When all items have responses, `fellows.curriculum_completed_at` is set
and the Postulant is ready for their qualifying project.
"""

from __future__ import annotations

from datetime import UTC, datetime

from rich.console import Console

from institute import claude_runner, curriculum, db, decisions, episodic, paths, workspaces
from institute import fellow as fellow_mod
from institute.claude_runner import FellowTask
from institute.fellow import Genome

console = Console()


RESPONSE_BRIEF = """\
You are a Postulant at the Invisible College. Per Chapter 5 of the
design, you are working through your reading curriculum. One item is
staged in your workspace right now; write your response to it.

# Inputs in your workspace

- `item.md`         the curriculum item: title, source, and the
                    prompt that tells you what kind of engagement is
                    expected (critique, summarize, apply, or extend).
- `curriculum.md`   your full curriculum, for context on how this
                    item fits the larger arc.
- `memory.md`       if present, your prior curriculum responses and
                    any other relevant work you have produced. Build on
                    what you have already thought through.

Read them with the Read tool, then read the source if it is locatable
(a file in `docs/`, in `archive/`, or a URL).

# What you must produce

Use the Write tool to create `response.md` in your workspace. The
response should:

- Engage the prompt directly. If you are asked to critique, critique;
  if to apply, demonstrate the application; if to extend, propose the
  extension and motivate it.
- Be honest about uncertainty. Pretending to understand what you do
  not is the failure mode the curriculum is built against.
- Cite specifics from the source where possible. A response that
  could be written without reading the source is failing the exercise.
- Be 400 to 1200 words. Substantive engagement, not a recitation.

When `response.md` exists and is complete, reply with the single word
`Done.` Nothing else.
"""


def run(fellow_id: str) -> str:
    """Walk through one curriculum item for this Postulant.

    Returns "completed" when the item was handled, "all-done" when the
    curriculum is already fully responded to, or "skipped" when there
    is no curriculum staged or the Fellow is not a Postulant.
    """
    with db.connection() as conn:
        row = conn.execute(
            "SELECT id, rank, retired_at, curriculum_completed_at, genome_path "
            "FROM fellows WHERE id = ?",
            (fellow_id,),
        ).fetchone()
    if row is None:
        console.print(f"[red]No such Fellow: `{fellow_id}`.[/red]")
        return "skipped"
    if row["retired_at"]:
        console.print(f"[yellow]{fellow_id} is retired.[/yellow]")
        return "skipped"
    if row["rank"] != "postulant":
        console.print(
            f"[yellow]{fellow_id} is rank `{row['rank']}`. Curriculum is for postulants.[/yellow]"
        )
        return "skipped"

    items = curriculum.load_items(fellow_id)
    if not items:
        console.print(
            f"[yellow]No curriculum staged for {fellow_id}. "
            "Run admit first, or design one manually.[/yellow]"
        )
        return "skipped"

    with db.connection() as conn:
        item = curriculum.next_pending_item(conn, fellow_id)
    if item is None:
        _maybe_mark_curriculum_complete(fellow_id, row["curriculum_completed_at"])
        console.print(f"[green]Curriculum complete for {fellow_id}.[/green]")
        return "all-done"

    postulant = Genome.from_file(fellow_mod.genome_path(fellow_id))
    workspace = workspaces.workspace_for(fellow_id, f"curriculum-{item.id}")
    workspaces.stage_input(workspace, "item.md", _render_item(item))
    workspaces.stage_input(workspace, "curriculum.md", curriculum.render_markdown(items))
    # Clear any prior response.md so the model's "Done." cannot refer
    # to old content from a re-run.
    stale = workspace / "response.md"
    if stale.exists():
        stale.unlink()

    console.print(
        f"[dim]Asking {postulant.name} to engage `{item.id}` "
        f"({item.layer}). This will take a minute or two...[/dim]"
    )
    claude_runner.invoke(
        FellowTask(
            genome=postulant,
            project_id=f"curriculum:{fellow_id}",
            step=f"curriculum-response:{item.id}",
            brief=RESPONSE_BRIEF,
            workspace=workspace,
            extra_dirs=(paths.DOCS, paths.ARCHIVE),
        )
    )

    response_md = workspaces.require_output(workspace, "response.md", min_chars=300).strip()
    final_path = curriculum.response_path(fellow_id, item.id)
    final_path.parent.mkdir(parents=True, exist_ok=True)
    tmp = final_path.with_suffix(final_path.suffix + ".tmp")
    tmp.write_text(response_md.rstrip() + "\n", encoding="utf-8")
    tmp.replace(final_path)

    now = datetime.now(UTC).isoformat(timespec="seconds")
    decision = decisions.Decision(
        kind="curriculum_response",
        title=f"{postulant.name}: response to `{item.id}`",
        body=(
            f"**Postulant:** {postulant.name} (`{fellow_id}`)\n\n"
            f"**Curriculum item:** {item.title} (`{item.id}`, layer {item.layer})\n\n"
            f"**Source:** {item.source}\n\n"
            f"**Response file:** [{final_path.relative_to(paths.ROOT)}]"
            f"({final_path.relative_to(paths.ROOT)})\n"
        ),
        actors=["orchestrator", fellow_id],
    )
    with db.connection() as conn, db.transaction(conn):
        conn.execute(
            "INSERT OR REPLACE INTO curriculum_responses "
            "(fellow_id, item_id, response_path, submitted_at) "
            "VALUES (?, ?, ?, ?)",
            (
                fellow_id,
                item.id,
                str(final_path.relative_to(paths.ROOT)),
                now,
            ),
        )
        decisions.record(conn, decision)

    # Ingest into the Postulant's episodic memory so their reading
    # carries forward into future invocations.
    episodic.safe_ingest(
        fellow_id=fellow_id,
        kind="curriculum_response",
        title=f"{item.title} ({item.layer})",
        content=response_md,
        source_path=str(final_path.relative_to(paths.ROOT)),
        metadata={"item_id": item.id, "layer": item.layer, "source": item.source},
    )

    console.print()
    console.print(
        f"[green]Response filed.[/green]  {item.id} → {final_path.relative_to(paths.ROOT)}"
    )
    # Was this the last item? If yes, stamp completion.
    with db.connection() as conn:
        remaining = curriculum.next_pending_item(conn, fellow_id)
    if remaining is None:
        _maybe_mark_curriculum_complete(fellow_id, None)
        console.print(
            f"[bold green]Curriculum complete.[/bold green] "
            f"{postulant.name} is ready for the qualifying project."
        )
    return "completed"


def _render_item(item: curriculum.CurriculumItem) -> str:
    return "\n".join(
        [
            f"# {item.title}",
            "",
            f"- **id:** `{item.id}`",
            f"- **layer:** {item.layer}",
            f"- **source:** {item.source}",
            "",
            "## Prompt",
            "",
            item.prompt,
            "",
        ]
    )


def _maybe_mark_curriculum_complete(fellow_id: str, already: str | None) -> None:
    if already:
        return
    now = datetime.now(UTC).isoformat(timespec="seconds")
    with db.connection() as conn, db.transaction(conn):
        conn.execute(
            "UPDATE fellows SET curriculum_completed_at = ? WHERE id = ?",
            (now, fellow_id),
        )
