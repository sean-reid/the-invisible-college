"""Reading groups: structured asynchronous discussion of a text.

A reading group is a multi-pass file exchange. Each invited Fellow
first responds to the text independently (Pass 1), then sees the
other participants' first responses and writes a shorter cross-response
(Pass 2). The institutional archive captures the text, all responses,
and the threading.

The mechanism is asynchronous-by-design: these models can't be in
the same room at the same time, but they can be confronted with each
other's positions deliberately. Pass 2 is where the cross-pollination
happens; without it the session is N parallel monologues.

Episodic memory rule: each Fellow gets a record of their own Pass-2
response (which already cites or references the others' positions),
not a transcript of everyone. Mirrors how human scholars carry ideas
forward — you remember the position you took.

Archive layout:
    archive/reading-groups/<slug>/
        text.md              the source text being discussed
        metadata.md          participants, dates, convener
        pass1/<fellow>.md    independent first response (one per participant)
        pass2/<fellow>.md    cross-response after seeing pass-1
"""

from __future__ import annotations

import sqlite3
from datetime import UTC, datetime
from pathlib import Path

from rich.console import Console

from institute import claude_runner, db, decisions, episodic, paths
from institute import fellow as fellow_mod
from institute.claude_runner import FellowTask
from institute.fellow import Genome
from institute.safe_io import atomic_write

console = Console()


PASS1_BRIEF = """\
You are participating in a reading group convened by the Invisible
College. A text has been chosen for discussion; you have been invited
to read it and respond independently before seeing what the other
participants have written.

# Inputs in your workspace

- `text.md`           the text under discussion
- `convener-note.md`  any context the convener attached (may be brief)

Read both with the Read tool.

# What you must produce

Use the Write tool to create `response.md` in your current working
directory. Length: 300 to 500 words. Targeted, not exhaustive.
Address as much as you have something genuine to say about; do not
pad. The response should answer roughly:

- What is the text claiming, in your reading?
- Where do you disagree, doubt, or want to see more evidence?
- What would this change (or fail to change) in how you approach
  your own work?

You are writing for an audience of three or four other Fellows who
will see this. Do not introduce yourself; your perspective comes
through in the substance of your reading.

# Final reply

When `response.md` exists and is complete, reply with the single
word `Done.` Nothing else.
"""


PASS2_BRIEF = """\
You are participating in the second pass of a reading group. In
Pass 1 you and the other participants each responded to the text
independently. Now you see what the others wrote.

# Inputs in your workspace

- `text.md`            the text under discussion (for re-reference)
- `convener-note.md`   the convener's context
- `your-pass1.md`      your own Pass-1 response
- `others-pass1.md`    the other participants' Pass-1 responses,
                       concatenated, each labelled with the
                       participant's name

Read `others-pass1.md` carefully. Form a view on each of the other
positions, even if you only end up engaging one or two of them
directly.

# What you must produce

Use the Write tool to create `response.md`. Length: 150 to 300 words.
This is shorter than Pass 1 by design — the purpose is threading,
not a second monograph. Address roughly:

- What in the other participants' Pass-1 responses shifted, sharpened,
  or contradicted your own reading?
- Whose position do you want to push back on directly, and on what
  grounds?
- Is there something none of you said that you now think the
  discussion needed?

Cite participants by name when you engage their position. The College
records this exchange; it should read as a real cross-response, not
a polite synthesis.

# Final reply

When `response.md` exists and is complete, reply with `Done.`.
"""


CONVENER_BRIEF = """\
You are convening a reading group of the Invisible College. The
College rotates the conveners across the cohort so that the texts
selected for collective reading reflect the breadth of the
institution, not just one person's interests.

Your job here is to **propose a reading and write a brief framing
note**. The two-pass discussion itself runs separately — you and the
other participants will each respond to the text independently and
then to each other.

# Inputs in your workspace

- `archive-index.md`     every publication the College has produced,
                         newest first.
- `agenda.md`            the College's standing research agenda,
                         five to nine durable institutional priorities.
- `your-genome.md`       a short note on who you are (specialization,
                         recent work), for grounding.
- `prior-conveners.md`   who has convened past sessions, if any.

Read all of them with the Read tool. You are choosing a text the
group will read together.

# What you may select

You may pick EITHER:

**(a) A College publication you did NOT author.** Cross-pollination
within the institution. Pick something whose ideas you want to put
in front of your colleagues. The slug must match an entry in
`archive-index.md`; do not invent.

**(b) An external open-access reading.** Bring something from outside
the College into the conversation: an open-access paper (e.g., on
arXiv, PLOS, a university preprint server), a public essay, a
classic in the public domain. The College's discussions are
sharpened by texts the institution did not produce. Use the
WebFetch tool to read the source, then write the text into
`text.md` in your workspace (the discussion participants will read
that file, not the URL).

Important constraint for external choices: pick **open-access** or
public-domain sources only. Do not paste the full body of a
paywalled article into the workspace. If you want to discuss a
paywalled work, prefer a published preprint version, or summarize
the argument and link to the source.

Either way, the reading should be **worth substantive engagement**.
A text worth the group's time has something a thoughtful Fellow
could defensibly disagree with. Avoid pieces that everyone will
simply nod at.

The College benefits from a mix of internal and external readings
over time; consult `prior-conveners.md` for what's been picked
recently and weigh accordingly.

# What you must produce

Use the Write tool to create files in your workspace.

ALWAYS:

1. `selection.json` — one of these two shapes:

   For an internal reading:
   ```
   {
     "kind": "internal",
     "post_slug": "<slug from archive-index.md>",
     "title": "<the publication's title verbatim>"
   }
   ```

   For an external reading:
   ```
   {
     "kind": "external",
     "source_url": "<full URL>",
     "source_label": "<short citation, e.g. 'Smith, J. (2023). Title. Publisher.'>",
     "title": "<short human-readable title for the session>"
   }
   ```

2. `framing.md` — 150 to 300 words. Your angle on this reading.
   What you want the group to engage with. Why now. What you would
   like to see the discussion press on. Write in your own voice.

IF external:

3. `text.md` — the body of the source. Use WebFetch to retrieve the
   URL, then write the retrieved content here. Markdown is fine;
   stripping HTML noise is fine; preserving the author's headings
   and structure matters more than perfect formatting. The
   participants will read `text.md`, not your URL.

# Final reply

When all required files exist and `selection.json` parses, reply
with `Done.` Nothing else.
"""


def _slugify(text: str) -> str:
    out: list[str] = []
    last_dash = True
    for ch in text.lower():
        if ch.isalnum():
            out.append(ch)
            last_dash = False
        elif not last_dash:
            out.append("-")
            last_dash = True
    return "".join(out).strip("-")[:60] or "reading-group"


def _stage(path: Path, content: str) -> None:
    atomic_write(path, content)


def _render_others_pass1(
    pass1_paths: dict[str, Path],
    excluding: str,
    genomes: dict[str, Genome],
) -> str:
    parts = ["# Other participants' Pass-1 responses", ""]
    for fellow_id, path in pass1_paths.items():
        if fellow_id == excluding:
            continue
        if not path.is_file():
            continue
        name = genomes[fellow_id].name
        parts.append(f"## {name} (`{fellow_id}`)")
        parts.append("")
        parts.append(path.read_text(encoding="utf-8").strip())
        parts.append("")
    return "\n".join(parts)


def _metadata_md(
    *,
    title: str,
    slug: str,
    participants: list[Genome],
    convener: str,
    convener_note: str,
    started_at: str,
) -> str:
    lines = [
        f"# Reading group: {title}",
        "",
        f"- **slug:** `{slug}`",
        f"- **convener:** `{convener}`",
        f"- **started_at:** {started_at}",
        "- **participants:**",
    ]
    for g in participants:
        lines.append(f"  - {g.name} (`{g.id}`)")
    if convener_note.strip():
        lines.extend(["", "## Convener's note", "", convener_note.strip(), ""])
    return "\n".join(lines) + "\n"


def run(
    *,
    title: str,
    text_path: Path,
    participants: list[str],
    convener: str = "founder",
    convener_note: str = "",
    slug: str | None = None,
) -> Path:
    """Convene a reading group session. Synchronous: walks Pass 1 then
    Pass 2 for every participant, then writes the archive.

    Returns the archive directory path.
    """
    if not text_path.is_file():
        raise SystemExit(f"text file not found: {text_path}")
    if len(participants) < 2:
        raise SystemExit("a reading group needs at least two participants")

    text_md = text_path.read_text(encoding="utf-8")
    slug = slug or _slugify(title)

    with db.connection() as conn:
        genomes: dict[str, Genome] = {}
        for pid in participants:
            row = conn.execute(
                "SELECT id FROM fellows WHERE id = ? AND retired_at IS NULL",
                (pid,),
            ).fetchone()
            if row is None:
                raise SystemExit(f"participant {pid} is not an active Fellow")
            genomes[pid] = fellow_mod.load_genome(conn, pid)

    now = datetime.now(UTC).isoformat(timespec="seconds")
    archive_dir = paths.READING_GROUPS / slug
    archive_dir.mkdir(parents=True, exist_ok=True)
    (archive_dir / "pass1").mkdir(exist_ok=True)
    (archive_dir / "pass2").mkdir(exist_ok=True)
    _stage(archive_dir / "text.md", text_md)
    _stage(
        archive_dir / "metadata.md",
        _metadata_md(
            title=title,
            slug=slug,
            participants=[genomes[p] for p in participants],
            convener=convener,
            convener_note=convener_note,
            started_at=now,
        ),
    )

    convener_note_md = (
        convener_note.strip() or "(no additional context — read the text on its own terms)"
    )

    # Pass 1: each participant responds independently.
    pass1_paths: dict[str, Path] = {}
    for pid in participants:
        pass1_archive_path = archive_dir / "pass1" / f"{pid}.md"
        if pass1_archive_path.is_file() and pass1_archive_path.stat().st_size > 200:
            console.print(f"[dim]Pass 1 for {pid} already filed; reusing.[/dim]")
            pass1_paths[pid] = pass1_archive_path
            continue

        workspace = paths.FELLOWS / pid / "workspace" / f"reading-group-{slug}-p1"
        workspace.mkdir(parents=True, exist_ok=True)
        _stage(workspace / "text.md", text_md)
        _stage(workspace / "convener-note.md", convener_note_md)
        stale = workspace / "response.md"
        if stale.exists():
            stale.unlink()

        console.print(f"[dim]Pass 1: asking {genomes[pid].name} to read and respond...[/dim]")
        claude_runner.invoke(
            FellowTask(
                genome=genomes[pid],
                project_id=f"reading-group:{slug}",
                step="reading-group:pass1",
                brief=PASS1_BRIEF,
                workspace=workspace,
                extra_dirs=(paths.DOCS, paths.ARCHIVE),
            )
        )
        response = (workspace / "response.md").read_text(encoding="utf-8").strip()
        if len(response) < 200:
            raise SystemExit(f"Pass-1 response from {pid} is too short ({len(response)} chars)")
        _stage(pass1_archive_path, response + "\n")
        pass1_paths[pid] = pass1_archive_path

    # Pass 2: each participant cross-responds, seeing the others' Pass-1.
    pass2_paths: dict[str, Path] = {}
    for pid in participants:
        pass2_archive_path = archive_dir / "pass2" / f"{pid}.md"
        if pass2_archive_path.is_file() and pass2_archive_path.stat().st_size > 100:
            console.print(f"[dim]Pass 2 for {pid} already filed; reusing.[/dim]")
            pass2_paths[pid] = pass2_archive_path
            continue

        workspace = paths.FELLOWS / pid / "workspace" / f"reading-group-{slug}-p2"
        workspace.mkdir(parents=True, exist_ok=True)
        _stage(workspace / "text.md", text_md)
        _stage(workspace / "convener-note.md", convener_note_md)
        _stage(
            workspace / "your-pass1.md",
            pass1_paths[pid].read_text(encoding="utf-8"),
        )
        _stage(
            workspace / "others-pass1.md",
            _render_others_pass1(pass1_paths, excluding=pid, genomes=genomes),
        )
        stale = workspace / "response.md"
        if stale.exists():
            stale.unlink()

        console.print(f"[dim]Pass 2: asking {genomes[pid].name} to cross-respond...[/dim]")
        claude_runner.invoke(
            FellowTask(
                genome=genomes[pid],
                project_id=f"reading-group:{slug}",
                step="reading-group:pass2",
                brief=PASS2_BRIEF,
                workspace=workspace,
                extra_dirs=(paths.DOCS, paths.ARCHIVE),
            )
        )
        response = (workspace / "response.md").read_text(encoding="utf-8").strip()
        if len(response) < 100:
            raise SystemExit(f"Pass-2 response from {pid} is too short ({len(response)} chars)")
        _stage(pass2_archive_path, response + "\n")
        pass2_paths[pid] = pass2_archive_path

        # Episodic memory: only the Fellow's own Pass-2 response lands
        # in their memory. Pass-1 responses they read are NOT injected;
        # the institutional record is what each Fellow themselves said.
        episodic.safe_ingest(
            fellow_id=pid,
            kind="reading_group",
            title=f"Reading group: {title}",
            content=response,
            source_path=str(pass2_archive_path.relative_to(paths.ROOT)),
            metadata={"slug": slug, "pass": 2},
        )

    # Decision record.
    body_lines = [
        f"**Title:** {title}",
        f"**Slug:** `{slug}`",
        f"**Convener:** `{convener}`",
        f"**Started:** {now}",
        "",
        "**Participants:**",
    ]
    for pid in participants:
        body_lines.append(f"- {genomes[pid].name} (`{pid}`)")
    if convener_note.strip():
        body_lines.extend(["", "## Convener's note", "", convener_note.strip()])
    body_lines.extend(
        [
            "",
            f"**Archive:** [{archive_dir.relative_to(paths.ROOT)}]"
            f"({archive_dir.relative_to(paths.ROOT)}/metadata.md)",
            "",
            "All Pass-1 and Pass-2 responses are preserved in the archive directory.",
        ]
    )
    decision = decisions.Decision(
        kind="reading_group",
        title=f"Reading group: {title}",
        body="\n".join(body_lines),
        actors=[convener, *participants],
    )
    with db.connection() as conn, db.transaction(conn):
        decisions.record(conn, decision)

    console.print(
        f"[bold green]Reading group `{slug}` complete.[/bold green] "
        f"{len(participants)} participants, two passes each."
    )
    return archive_dir


def pick_convener(conn: sqlite3.Connection) -> Genome | None:
    """Pick the next reading-group convener: the active Fellow who has
    least recently led a session (never-led first).

    Returns None if no eligible convener exists (no active Fellows).
    Postulants are eligible — broadens the rotation; a Postulant
    proposing a reading is a useful institutional moment.
    """
    rows = list(conn.execute("SELECT id FROM fellows WHERE retired_at IS NULL ORDER BY id"))
    if not rows:
        return None

    # Map fellow_id -> most recent reading_group convene timestamp, if any.
    # The audit_log's `actor` field is a comma-joined list; the convener
    # is the first actor on a reading_group decision (per the run() impl).
    last_convened: dict[str, str] = {}
    for r in conn.execute(
        "SELECT at, actor FROM audit_log WHERE action = 'reading_group' ORDER BY at ASC"
    ):
        actors = [a.strip() for a in r["actor"].split(",") if a.strip()]
        if actors:
            convener_id = actors[0]
            last_convened[convener_id] = r["at"]

    def sort_key(fellow_id: str) -> tuple[int, str]:
        # Never-convened Fellows sort first (0); others by ascending
        # last-convened timestamp.
        if fellow_id not in last_convened:
            return (0, "")
        return (1, last_convened[fellow_id])

    eligible_ids = sorted([r["id"] for r in rows], key=sort_key)
    return fellow_mod.load_genome(conn, eligible_ids[0])


def _pick_participants(
    conn: sqlite3.Connection,
    *,
    convener_id: str,
    target_count: int = 3,
) -> list[Genome]:
    """Pick reading-group participants other than the convener.

    Aims for department diversity: prefer Fellows from departments
    the convener is NOT in, falling back to same-department Fellows
    only after the outside pool is exhausted. The convener is
    included in the final session as a participant but is selected
    separately by `pick_convener`.
    """
    from institute import departments

    rows = list(
        conn.execute(
            "SELECT id FROM fellows WHERE retired_at IS NULL AND id != ? ORDER BY id",
            (convener_id,),
        )
    )
    if not rows:
        return []

    use_depts = departments.is_initialized(conn)
    outside: list[str] = []
    same: list[str] = []
    for r in rows:
        fid = r["id"]
        if use_depts and departments.same_department(conn, fellow_a=convener_id, fellow_b=fid):
            same.append(fid)
        else:
            outside.append(fid)

    chosen: list[str] = []
    for fid in outside:
        if len(chosen) >= target_count:
            break
        chosen.append(fid)
    for fid in same:
        if len(chosen) >= target_count:
            break
        chosen.append(fid)

    return [fellow_mod.load_genome(conn, fid) for fid in chosen]


def convene_with_rotating_leader(*, target_participants: int = 3) -> Path | None:
    """Auto-convene a reading group with a rotating leader.

    1. Pick the convener (least-recently-led active Fellow).
    2. Have the convener propose a text (a recent College publication
       not their own) plus a framing note.
    3. Pick participants for department diversity.
    4. Run the standard two-pass reading_group session.

    Returns the archive directory path, or None if no convener could
    be picked or the convener's selection invalidated.
    """
    import json

    from institute import archive_index

    with db.connection() as conn:
        convener = pick_convener(conn)
        if convener is None:
            console.print("[yellow]No active Fellow available to convene a reading group.[/yellow]")
            return None
        participants = _pick_participants(
            conn, convener_id=convener.id, target_count=target_participants
        )
        if not participants:
            console.print(
                f"[yellow]Convener {convener.name} has no eligible participants; "
                "skipping reading group.[/yellow]"
            )
            return None

    # Phase 1: convener picks a text.
    workspace = paths.FELLOWS / convener.id / "workspace" / "reading-group-propose"
    workspace.mkdir(parents=True, exist_ok=True)
    _stage(workspace / "archive-index.md", archive_index.render())
    agenda_path = paths.DOCS / "research-agenda.md"
    if agenda_path.is_file():
        _stage(workspace / "agenda.md", agenda_path.read_text(encoding="utf-8"))
    else:
        _stage(workspace / "agenda.md", "(no agenda file)")
    _stage(
        workspace / "your-genome.md",
        f"# You are {convener.name}\n\n"
        f"- **id:** `{convener.id}`\n"
        f"- **specialization:** {convener.specialization}\n",
    )

    # Prior conveners note — quick audit-log look at the last few sessions.
    with db.connection() as conn:
        prior_rows = list(
            conn.execute(
                "SELECT at, actor FROM audit_log "
                "WHERE action = 'reading_group' ORDER BY at DESC LIMIT 5"
            )
        )
    if prior_rows:
        lines = ["# Recent reading groups", ""]
        for r in prior_rows:
            actors = [a.strip() for a in r["actor"].split(",") if a.strip()]
            convener_id = actors[0] if actors else "(unknown)"
            lines.append(f"- {r['at']}  convener: `{convener_id}`")
        _stage(workspace / "prior-conveners.md", "\n".join(lines) + "\n")
    else:
        _stage(
            workspace / "prior-conveners.md",
            "(no prior reading groups — this is the first session)\n",
        )

    for stale in ("selection.json", "framing.md"):
        p = workspace / stale
        if p.exists():
            p.unlink()

    console.print(f"[dim]Convener {convener.name} is proposing a reading...[/dim]")
    claude_runner.invoke(
        FellowTask(
            genome=convener,
            project_id="reading-group:propose",
            step="reading-group:propose",
            brief=CONVENER_BRIEF,
            workspace=workspace,
            extra_dirs=(paths.DOCS, paths.ARCHIVE),
        )
    )

    try:
        selection = json.loads((workspace / "selection.json").read_text(encoding="utf-8"))
    except (OSError, ValueError) as exc:
        console.print(f"[yellow]Convener selection.json malformed: {exc}; skipping.[/yellow]")
        return None
    framing_path = workspace / "framing.md"
    if not framing_path.is_file():
        console.print("[yellow]Convener did not write framing.md; skipping.[/yellow]")
        return None
    framing_md = framing_path.read_text(encoding="utf-8").strip()
    if len(framing_md) < 100:
        console.print("[yellow]Convener framing note too short; skipping.[/yellow]")
        return None

    # Two paths: an internal (College publication) reading or an
    # external open-access reading the convener fetched themselves via
    # WebFetch and saved into their workspace as text.md.
    kind = str(selection.get("kind", "")).strip().lower()
    # Backward-compat: a payload with `post_slug` and no `kind` is
    # treated as internal.
    if not kind and selection.get("post_slug"):
        kind = "internal"
    title = str(selection.get("title", "")).strip()
    if not title:
        console.print("[yellow]Convener selection has no title; skipping.[/yellow]")
        return None

    text_path: Path
    convener_note_md = framing_md

    if kind == "internal":
        post_slug = str(selection.get("post_slug", "")).strip()
        if not post_slug:
            console.print("[yellow]Internal selection missing post_slug; skipping.[/yellow]")
            return None
        candidate = paths.PUBLICATIONS / f"{post_slug}.md"
        if not candidate.is_file():
            alt = paths.BLOG_POSTS / f"{post_slug}.md"
            if alt.is_file():
                candidate = alt
            else:
                console.print(
                    f"[yellow]Convener picked internal `{post_slug}` but no "
                    "matching publication file found; skipping.[/yellow]"
                )
                return None
        text_path = candidate
        # Defensive: log if the convener's name shows up at the top of
        # the picked file — the brief told them to avoid their own work.
        text_md = text_path.read_text(encoding="utf-8")
        if convener.name in "\n".join(text_md.splitlines()[:5]):
            console.print(
                "[dim]Note: convener's name appears in selected text. "
                "Trusting their judgment.[/dim]"
            )

    elif kind == "external":
        source_url = str(selection.get("source_url", "")).strip()
        source_label = str(selection.get("source_label", "")).strip()
        if not source_url or not source_label:
            console.print(
                "[yellow]External selection missing source_url or source_label; skipping.[/yellow]"
            )
            return None
        external_text_path = workspace / "text.md"
        if not external_text_path.is_file() or external_text_path.stat().st_size < 300:
            console.print(
                "[yellow]External selection: convener did not write a "
                "substantive text.md from WebFetch; skipping.[/yellow]"
            )
            return None
        text_path = external_text_path
        # Prepend a citation header to the framing note so participants
        # see the source up front.
        convener_note_md = (
            f"**External reading.**\n"
            f"- **Source:** {source_label}\n"
            f"- **URL:** {source_url}\n\n"
            f"---\n\n{framing_md}"
        )

    else:
        console.print(
            f"[yellow]Convener selection has unknown kind {kind!r}; expected "
            "`internal` or `external`. Skipping.[/yellow]"
        )
        return None

    # Phase 2: standard two-pass session.
    participant_ids = [convener.id] + [p.id for p in participants]
    return run(
        title=f"Reading group on `{title}`",
        text_path=text_path,
        participants=participant_ids,
        convener=convener.id,
        convener_note=convener_note_md,
    )


__all__ = ["convene_with_rotating_leader", "pick_convener", "run"]
