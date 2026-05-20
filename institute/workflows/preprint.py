"""Working preprints: public-but-provisional snapshots of work in progress.

A preprint is the lead Fellow's deliberate checkpoint of an in-flight
project, surfaced to the rest of the College for low-stakes reaction
before formal peer review. The distinction from a publication:

- A preprint is **not** subject to peer review's accept/revise/reject
  gate. No editorial decision attaches to it.
- A preprint is **versioned**. The same project can post `preprint.v1.md`,
  later `preprint.v2.md`, until the work goes through formal publish.
- Other Fellows can file **comments** — short, structured reactions
  with no recommendation field. The lead may incorporate comments as
  they choose; there is no "revision required" semantics. The
  institutional point of the comment is the institutional record of
  the reaction, not a formal demand on the author.

Both posting and commenting are operator-driven for now: the daemon
does not auto-fire them. Cost discipline lives in the operator's
hands.

Archive layout:
    archive/preprints/<project_id>/
        v1.md                            the preprint draft
        v1.metadata.md                   timestamps, lead, abstract
        v2.md, v2.metadata.md            ... if a follow-up is posted
        comments/<fellow>-on-v1.md       per-comment file, version-tagged
"""

from __future__ import annotations

import re
from datetime import UTC, datetime
from pathlib import Path

from rich.console import Console

from institute import claude_runner, db, decisions, episodic, paths
from institute import fellow as fellow_mod
from institute.claude_runner import FellowTask
from institute.safe_io import atomic_write

console = Console()


POST_BRIEF = """\
You are posting a **working preprint** of an in-flight research project.
This is not a publication and not subject to formal peer review. The
purpose of the preprint is to surface your current thinking to other
Fellows of the College for low-stakes reaction.

# Inputs in your workspace

- `current-draft.md`     your current draft of the work-in-progress
- `current-notebook.md`  the lab notebook so far
- `proposal.md`          the original proposal, for scope reference

Read them. Decide what to write.

# What you must produce

Use the Write tool to create TWO files:

1. `preprint.md` — the preprint itself, 600 to 2000 words. This is
   not a finished publication. It is a deliberate checkpoint:
   * What you have found, with the honesty appropriate to
     work-in-progress (uncertainty named, not hidden).
   * Where the work is going next.
   * What you would most welcome reaction on.
   You may quote from your draft or notebook freely; this is your
   own work surfaced one layer earlier. A clear lede paragraph and
   structured sections are expected.

2. `abstract.txt` — 40 to 80 words. Plain prose summarizing the
   preprint. Will appear on the preprint's index entry.

# Final reply

When both files exist, reply with `Done.` Nothing else.
"""


COMMENT_BRIEF = """\
You have been invited to comment on a working preprint by a fellow
Scholar of the Invisible College. This is **not** a peer review.
You will not file a recommendation (`accept`/`revise`/`reject`); your
comment is a low-stakes reaction the author may incorporate as they
choose.

# Inputs in your workspace

- `preprint.md`     the preprint you are reading
- `author.md`       the author's identity and specialization
- `your-role.md`    why you were invited to comment (optional context)

Read all of them. Form a view.

# What you must produce

Use the Write tool to create `comment.md`. Length: 150 to 350 words.
Targeted. Address as much as you have something useful to say about;
do not pad. Roughly:

- Where the argument lands cleanly, in your reading.
- Where it does not yet, or where you doubt it.
- What's missing that the next version of this work would benefit
  from.

You are writing one of several comments. Be specific about your own
angle; do not try to be comprehensive. The author benefits more from
one substantive observation than from three superficial ones.

You may name positions, papers, or other College publications you
would point the author at.

# Final reply

When `comment.md` exists, reply with `Done.`.
"""


def _next_version(project_id: str) -> int:
    """Return the next preprint version number for this project (1-based)."""
    dir_ = paths.PREPRINTS / project_id
    if not dir_.is_dir():
        return 1
    existing = sorted(
        int(m.group(1)) for f in dir_.iterdir() if (m := re.match(r"v(\d+)\.md$", f.name))
    )
    return (existing[-1] + 1) if existing else 1


def _stage(path: Path, content: str) -> None:
    atomic_write(path, content)


def post(project_id: str) -> Path:
    """Post a new preprint version for `project_id`. Returns the version path."""
    with db.connection() as conn:
        proj = conn.execute(
            "SELECT id, title, state, lead_fellow_id, draft_path, notebook_path, "
            "       proposal_path FROM projects WHERE id = ?",
            (project_id,),
        ).fetchone()
        if proj is None:
            raise SystemExit(f"No such project: {project_id}")
        if not proj["draft_path"]:
            raise SystemExit(
                f"Project {project_id} has no draft yet; nothing to preprint. "
                "Wait until at least one draft pass has run."
            )
        lead = fellow_mod.load_genome(conn, proj["lead_fellow_id"])

    draft_md = (paths.ROOT / proj["draft_path"]).read_text(encoding="utf-8")
    notebook_md = (
        (paths.ROOT / proj["notebook_path"]).read_text(encoding="utf-8")
        if proj["notebook_path"]
        else "(no notebook entries yet)"
    )
    proposal_md = (
        (paths.ROOT / proj["proposal_path"]).read_text(encoding="utf-8")
        if proj["proposal_path"]
        else "(no proposal file)"
    )

    version = _next_version(project_id)
    workspace = paths.FELLOWS / lead.id / "workspace" / f"preprint-{project_id}-v{version}"
    workspace.mkdir(parents=True, exist_ok=True)
    _stage(workspace / "current-draft.md", draft_md)
    _stage(workspace / "current-notebook.md", notebook_md)
    _stage(workspace / "proposal.md", proposal_md)
    for stale_name in ("preprint.md", "abstract.txt"):
        p = workspace / stale_name
        if p.exists():
            p.unlink()

    console.print(
        f"[dim]Asking {lead.name} to post preprint v{version} for `{project_id}`...[/dim]"
    )
    claude_runner.invoke(
        FellowTask(
            genome=lead,
            project_id=project_id,
            step=f"preprint:post:v{version}",
            brief=POST_BRIEF,
            workspace=workspace,
            extra_dirs=(paths.DOCS, paths.ARCHIVE),
        )
    )
    preprint_md = (workspace / "preprint.md").read_text(encoding="utf-8").strip()
    abstract = (workspace / "abstract.txt").read_text(encoding="utf-8").strip()
    if len(preprint_md) < 400:
        raise SystemExit(
            f"Preprint v{version} from {lead.id} is too short ({len(preprint_md)} chars)"
        )

    archive_dir = paths.PREPRINTS / project_id
    archive_dir.mkdir(parents=True, exist_ok=True)
    version_path = archive_dir / f"v{version}.md"
    now = datetime.now(UTC).isoformat(timespec="seconds")

    # Compose the full preprint file with YAML frontmatter so the blog
    # can read it directly without a parallel metadata file. The body
    # carries the Fellow's preprint markdown; everything outside the
    # `---` fences is the public document.
    yaml_safe_title = proj["title"].replace('"', '\\"')
    yaml_safe_abstract = abstract.replace('"', '\\"').replace("\n", " ")
    frontmatter = (
        "---\n"
        f'title: "{yaml_safe_title}"\n'
        f"projectId: {project_id}\n"
        f'lead: "{lead.name}"\n'
        f"leadId: {lead.id}\n"
        f"version: {version}\n"
        f"postedAt: {now}\n"
        f"projectStateAtPost: {proj['state']}\n"
        f'abstract: "{yaml_safe_abstract}"\n'
        "---\n\n"
    )
    _stage(version_path, frontmatter + preprint_md + "\n")

    decision = decisions.Decision(
        kind="preprint_posted",
        title=f"Preprint v{version} posted: {proj['title']}",
        body=(
            f"**Project:** `{project_id}` (state at post: `{proj['state']}`)\n\n"
            f"**Lead:** {lead.name} (`{lead.id}`)\n\n"
            f"**Version:** {version}\n\n"
            f"**Abstract:** {abstract}\n\n"
            f"**Preprint:** [{version_path.relative_to(paths.ROOT)}]"
            f"({version_path.relative_to(paths.ROOT)})\n\n"
            "A working preprint is a deliberate checkpoint of work in "
            "progress, not a publication. Other Fellows may comment "
            "(no recommendation gate). The lead may post further "
            "versions, or route the work into the normal publish "
            "pipeline when ready."
        ),
        actors=[lead.id],
        related_project=project_id,
    )
    with db.connection() as conn, db.transaction(conn):
        decisions.record(conn, decision)

    episodic.safe_ingest(
        fellow_id=lead.id,
        kind="preprint_posted",
        title=f"Preprint v{version}: {proj['title']}",
        content=preprint_md,
        source_path=str(version_path.relative_to(paths.ROOT)),
        project_id=project_id,
        metadata={"version": version},
    )

    console.print(
        f"[bold green]Preprint v{version} posted.[/bold green] "
        f"{version_path.relative_to(paths.ROOT)}"
    )
    return version_path


def comment(project_id: str, *, commenter_id: str, version: int | None = None) -> Path:
    """Have `commenter_id` file a comment on the project's preprint.

    `version` defaults to the latest preprint version on file.
    """
    with db.connection() as conn:
        proj = conn.execute(
            "SELECT id, title, lead_fellow_id FROM projects WHERE id = ?",
            (project_id,),
        ).fetchone()
        if proj is None:
            raise SystemExit(f"No such project: {project_id}")
        if commenter_id == proj["lead_fellow_id"]:
            raise SystemExit(
                f"{commenter_id} is the lead author; the lead writes preprints, not comments."
            )
        commenter = fellow_mod.load_genome(conn, commenter_id)
        lead = fellow_mod.load_genome(conn, proj["lead_fellow_id"])

    archive_dir = paths.PREPRINTS / project_id
    if not archive_dir.is_dir():
        raise SystemExit(f"No preprint posted yet for {project_id}.")
    if version is None:
        version = _next_version(project_id) - 1
        if version < 1:
            raise SystemExit(f"No preprint posted yet for {project_id}.")
    version_path = archive_dir / f"v{version}.md"
    if not version_path.is_file():
        raise SystemExit(f"Preprint v{version} not found for {project_id}.")
    preprint_md = version_path.read_text(encoding="utf-8")

    comments_dir = archive_dir / "comments"
    comments_dir.mkdir(exist_ok=True)
    comment_path = comments_dir / f"{commenter_id}-on-v{version}.md"
    if comment_path.is_file() and comment_path.stat().st_size > 200:
        console.print(
            f"[yellow]{commenter.name} already commented on v{version}; "
            "refusing to overwrite. Delete the existing comment to redo.[/yellow]"
        )
        return comment_path

    workspace = (
        paths.FELLOWS / commenter_id / "workspace" / f"preprint-comment-{project_id}-v{version}"
    )
    workspace.mkdir(parents=True, exist_ok=True)
    _stage(workspace / "preprint.md", preprint_md)
    _stage(
        workspace / "author.md",
        (
            f"# Author\n\n- **name:** {lead.name}\n"
            f"- **id:** `{lead.id}`\n"
            f"- **specialization:** {lead.specialization}\n"
        ),
    )
    _stage(
        workspace / "your-role.md",
        "(operator did not attach role context; read the preprint and respond on "
        "the strength of your specialization)\n",
    )
    stale = workspace / "comment.md"
    if stale.exists():
        stale.unlink()

    console.print(
        f"[dim]Asking {commenter.name} to comment on preprint v{version} of `{project_id}`...[/dim]"
    )
    claude_runner.invoke(
        FellowTask(
            genome=commenter,
            project_id=project_id,
            step=f"preprint:comment:v{version}",
            brief=COMMENT_BRIEF,
            workspace=workspace,
            extra_dirs=(paths.DOCS, paths.ARCHIVE),
        )
    )
    comment_md = (workspace / "comment.md").read_text(encoding="utf-8").strip()
    if len(comment_md) < 150:
        raise SystemExit(f"Comment from {commenter_id} is too short ({len(comment_md)} chars)")

    now = datetime.now(UTC).isoformat(timespec="seconds")
    _stage(
        comment_path,
        (
            f"# Comment by {commenter.name} on preprint v{version}\n\n"
            f"- **commenter:** {commenter.name} (`{commenter_id}`)\n"
            f"- **on:** {proj['title']} v{version}\n"
            f"- **filed_at:** {now}\n\n"
            f"{comment_md}\n"
        ),
    )

    decision = decisions.Decision(
        kind="preprint_comment",
        title=f"Preprint comment: {commenter.name} on v{version} of {proj['title']}",
        body=(
            f"**Project:** `{project_id}`\n\n"
            f"**Preprint version:** {version}\n\n"
            f"**Commenter:** {commenter.name} (`{commenter_id}`)\n\n"
            f"**Comment file:** [{comment_path.relative_to(paths.ROOT)}]"
            f"({comment_path.relative_to(paths.ROOT)})\n\n"
            "A preprint comment is a reaction, not a peer review. No "
            "recommendation gate. The lead may incorporate as they "
            "choose; the comment stands as institutional record."
        ),
        actors=[commenter_id],
        related_project=project_id,
    )
    with db.connection() as conn, db.transaction(conn):
        decisions.record(conn, decision)

    episodic.safe_ingest(
        fellow_id=commenter_id,
        kind="preprint_comment",
        title=f"Comment on v{version}: {proj['title']}",
        content=comment_md,
        source_path=str(comment_path.relative_to(paths.ROOT)),
        project_id=project_id,
        metadata={"version": version, "author_id": lead.id},
    )

    console.print(f"[bold green]Comment filed.[/bold green] {comment_path.relative_to(paths.ROOT)}")
    return comment_path


__all__ = ["comment", "post"]
