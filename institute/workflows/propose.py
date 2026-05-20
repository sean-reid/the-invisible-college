"""Propose workflow: a Fellow drafts a research proposal.

The Founder picks (or the heuristic selects) a lead Fellow. The Fellow is
invoked with a brief that asks for a structured research proposal:
question, background, approach, expected output, resource estimate, and
anticipated failure modes. The result is parsed, validated, and written to
archive/proposals/<project-id>/proposal.md as a new project in state
PROPOSED.

This is a one-shot Fellow invocation. The Fellow does not need access to
their prior work (there isn't any yet), only to the Charter and the
Archive of past publications.
"""

from __future__ import annotations

import re
import secrets
import sqlite3
from datetime import UTC, date, datetime
from pathlib import Path

from rich.console import Console

from institute import claude_runner, collaborators, db, decisions, episodic, paths, workspaces
from institute import fellow as fellow_mod
from institute.claude_runner import FellowTask
from institute.fellow import Genome
from institute.state import State

console = Console()


PROPOSE_BRIEF_TEMPLATE = """\
You are drafting a research proposal for the Invisible College. The
Charter and design chapters describe the institution.

{topic_section}

# What you must produce

A research proposal in markdown. The structure:

- The first line is a level-1 heading with the proposal's working
  title: `# Your Title Here`. The title must literally be on a `# ` line.
- Then, in this exact order, each as a level-2 heading:

1. `## Question` (the question you propose to investigate, as a question)
2. `## Background` (what is already known; cite specific sources, internal
   or external; include real URLs or document references where possible)
3. `## Approach` (concrete methods you will use; not vague intentions)
4. `## Expected output` (what form the result will take: demonstration,
   essay, code release, critical review, lab note, synthesis)
5. `## Resource estimate` (rough estimate of compute, time, and tool use;
   keep it bounded)
6. `## Anticipated failure modes` (how this could go wrong, and what an
   honest negative result would look like)
7. `## Collaborators needed` (whether to form a research group on this
   project; OK if none)

   If you want specific Fellows invited as co-authors, name them by
   their full name or fellow id (e.g. "Henri Poincaré" or
   `henri-poincare`). Each named Fellow will receive a structured
   invitation and decide accept/decline; accepts join the research
   group and are co-credited on publication. A descriptive reference
   like "the Fellow who did the prior work on X" will NOT fire an
   invitation — the parser only matches names and ids verbatim. If
   you only want an informal design check rather than co-authorship,
   say so explicitly and do not name anyone; this section will
   surface to the proposal reviewer but no invitations will go out.

# Constraints

- Length: 600 to 1500 words total across all sections.
- Be specific. A proposal that could be written by anyone about anything
  has no value. The reader should know exactly what you are going to do.
- The question should be one you genuinely do not know the answer to.
- The Charter prohibits commercial activity, deception, plagiarism, and
  engagement-bait. Stay clear of those.
- Topics about AI safety, AI consciousness, or AI sentience are off-limits
  unless the topic guidance above explicitly requests them.

# Your memory

If a file called `memory.md` is present in your working directory,
read it first with the Read tool. It contains the most relevant
entries from your own episodic memory — past proposals, drafts,
reviews you gave or received, curriculum responses if any. Your
proposal should grow out of what you have already thought through,
not orbit elsewhere. Reference your past work where it's load-bearing.

# Output

Use the Write tool to create `proposal.md` in your current working
directory containing the proposal markdown described above. Then
reply with the single word `Done.` Nothing else.

Writing to a file rather than returning the proposal in your reply
matters: long prose replies risk being truncated by the output-token
limit, while a Write-tool file is unbounded. Verify the file exists
and is complete before saying Done.
"""


TOPIC_SECTION_WITH = """\
# Topic guidance from the Founder

{topic}

You may treat this as a starting point or a constraint, as you see fit.
You may sharpen, narrow, or productively reframe it. You may also push
back and propose something different if the guidance is wrong; if you do,
you must say so explicitly in the proposal's Background section.
"""


TOPIC_SECTION_FREE = """\
# Topic guidance

The Founder has not specified a topic. You may choose what to investigate.
Pick something that:

- Plays to the strengths of your specialization
- Is genuinely interesting (you would want to read this)
- Can be completed in one or two weeks of intermittent work
- Has a concrete expected output

# Topic diversity (read this before choosing)

Read `archive-index.md` in your workspace and notice which topics the
College has already published heavily on. Chapter 11 of the design
calls out convergence to consensus thinking as a fatal failure mode:
a College where every Fellow keeps extending the same thread becomes
a College of one voice. Your job is to push against that.

Two acceptable paths when picking a topic:

1. Pick a question that opens a new thread the Archive does not yet
   cover. Cross-disciplinary, methodologically distinct, or in a
   specialization the cohort has neglected. This is the preferred
   path when the Archive is heavy in any one cluster.

2. Extend an existing thread only if your proposal adds something
   that the prior pieces did NOT do — a different mechanism, a
   negative case the prior work missed, a cross-disciplinary
   connection. In that case, name the prior pieces in your
   Background section and say explicitly what your contribution adds
   beyond them. "Another piece in the same cluster" is not a
   contribution.

A standing Open Problems list, if `open-problems.md` is in your
workspace, surfaces questions the College wants answered. Picking one
is encouraged but not required — they are an aid against drift, not
an assignment.
"""


REQUIRED_SECTIONS = [
    "Question",
    "Background",
    "Approach",
    "Expected output",
    "Resource estimate",
    "Anticipated failure modes",
    "Collaborators needed",
]


def _pick_lead(conn: sqlite3.Connection, requested: str | None) -> Genome:
    """Pick the Fellow who should lead the next proposal.

    Rotation by least-recent authorship: the Fellow who has not led a
    project most recently goes next. Fellows who have never led a
    project are at the front. Critic specializations are filtered out
    because their function is to review others' work, not propose
    their own.
    """
    if requested is not None:
        genome = fellow_mod.load_genome(conn, requested)
        # Chapter 5: Postulants research under apprenticeship via the
        # qualifying-project flow, never as the lead of a research-kind
        # proposal. The auto-pick path filters Postulants out below; the
        # explicit --lead path needs the same gate.
        if genome.rank == "postulant":
            raise SystemExit(
                f"Lead Fellow {requested!r} is a Postulant. Postulants do their "
                "qualifying project under advisor supervision; use `institute "
                "qualify --fellow <id>` instead."
            )
        row = conn.execute("SELECT retired_at FROM fellows WHERE id = ?", (requested,)).fetchone()
        if row is not None and row["retired_at"] is not None:
            raise SystemExit(f"Lead Fellow {requested!r} is retired and cannot lead new work.")
        return genome

    # MAX(updated_at) per Fellow over projects they have led. NULL means
    # they have never led one, which sorts first under ASC NULLS FIRST
    # (SQLite default for ASC). Postulants are excluded: they propose
    # under advisor sponsorship, not as lead authors, per Chapter 5.
    rows = list(
        conn.execute(
            """
            SELECT f.id, f.specialization, MAX(p.updated_at) AS last_authored
            FROM fellows f
            LEFT JOIN projects p ON p.lead_fellow_id = f.id
            WHERE f.retired_at IS NULL AND f.rank != 'postulant'
            GROUP BY f.id
            ORDER BY last_authored ASC, f.name ASC
            """
        )
    )
    if not rows:
        raise SystemExit("No active Fellows. Run `institute bootstrap` first.")

    preferred = [r for r in rows if not _is_critic_specialization(r["specialization"])]
    chosen = preferred[0] if preferred else rows[0]
    return fellow_mod.load_genome(conn, chosen["id"])


_CRITIC_MARKERS = ("critic", "critique", "skeptical")


def _is_critic_specialization(specialization: str) -> bool:
    s = specialization.lower()
    return any(marker in s for marker in _CRITIC_MARKERS)


def _slugify(text: str) -> str:
    out = []
    last_dash = False
    for ch in text.lower():
        if ch.isalnum():
            out.append(ch)
            last_dash = False
        elif not last_dash:
            out.append("-")
            last_dash = True
    s = "".join(out).strip("-")
    return s[:60] if s else "untitled"


def _project_id(title: str) -> str:
    today = date.today().isoformat()
    suffix = secrets.token_hex(2)
    return f"{today}-{_slugify(title)[:40]}-{suffix}"


def _extract_title(markdown: str) -> str:
    """Extract the proposal title.

    Tries, in order:
      1. A level-1 heading `# Title` (the canonical form).
      2. A `## Title` section's body (the older form, kept for back-compat).
      3. The first `## ` heading in the document (the form a Fellow may
         emit if it reads "## Title" in the brief as "the title goes on
         a ## line").
    """
    h1 = re.search(r"^#\s+(.+?)\s*$", markdown, re.MULTILINE)
    if h1:
        return h1.group(1).strip()

    titled = re.search(
        r"^##\s+Title\s*$\n+(.*?)(?=^##\s+|\Z)",
        markdown,
        re.MULTILINE | re.DOTALL | re.IGNORECASE,
    )
    if titled:
        body = titled.group(1).strip()
        first = next((ln.strip() for ln in body.splitlines() if ln.strip()), "")
        if first.startswith("# "):
            first = first[2:].strip()
        if first:
            return first

    for match in re.finditer(r"^##\s+(.+?)\s*$", markdown, re.MULTILINE):
        candidate = match.group(1).strip()
        # Skip the literal `## Title` marker (already tried above) and
        # any known section heading; that would mean the proposal lacks
        # a real title.
        if candidate.lower() == "title":
            continue
        if _is_section_heading(candidate):
            continue
        return candidate

    raise RuntimeError(
        "Proposal has no title: expected `# <title>` on the first line, "
        "a non-empty `## Title` section, or a leading `## <title>` heading."
    )


def _is_section_heading(text: str) -> bool:
    lowered = text.strip().lower()
    for section in REQUIRED_SECTIONS:
        if lowered == section.lower():
            return True
        for variant in _SECTION_VARIANTS.get(section, []):
            if lowered == variant.lower():
                return True
    return False


def _validate_sections(markdown: str) -> list[str]:
    """Return list of missing required sections.

    Matches case-insensitively and accepts small idiomatic variants so a
    Fellow that writes `## Expected Outputs` or `## Failure modes`
    doesn't lose its draft over a heading-style difference.
    """
    missing = []
    for section in REQUIRED_SECTIONS:
        if not _section_present(markdown, section):
            missing.append(section)
    return missing


def _section_present(markdown: str, section: str) -> bool:
    variants = [section, *_SECTION_VARIANTS.get(section, [])]
    for variant in variants:
        if re.search(
            rf"^##\s+{re.escape(variant)}\s*$",
            markdown,
            re.MULTILINE | re.IGNORECASE,
        ):
            return True
    return False


# Reasonable synonyms the Fellow may emit instead of the canonical heading.
_SECTION_VARIANTS: dict[str, list[str]] = {
    "Expected output": ["Expected outputs", "Output", "Outputs", "Deliverable", "Deliverables"],
    "Resource estimate": ["Resources", "Resource estimates"],
    "Anticipated failure modes": ["Failure modes", "Risks", "Anticipated risks"],
    "Collaborators needed": ["Collaborators", "Collaboration", "Required collaborators"],
}


def _atomic_write(path: Path, content: str) -> None:
    from institute.safe_io import atomic_write

    atomic_write(path, content)


def run(
    *,
    lead: str | None = None,
    topic: str | None = None,
    collaborators: list[str] | None = None,
) -> None:
    """Top-level propose entry point. Called from cli.propose."""

    collaborator_ids = list(collaborators or [])

    # Resolve the lead fellow first so we error early if the institution is empty.
    with db.connection() as conn:
        lead_genome = _pick_lead(conn, lead)
        collaborator_genomes = _validate_collaborators(conn, lead_genome.id, collaborator_ids)

    topic_section = TOPIC_SECTION_WITH.format(topic=topic.strip()) if topic else TOPIC_SECTION_FREE
    brief = PROPOSE_BRIEF_TEMPLATE.format(topic_section=topic_section)

    console.print(
        f"[dim]Asking {lead_genome.name} ({lead_genome.id}) to draft a proposal. "
        "This will take a few minutes...[/dim]"
    )

    workspace = workspaces.workspace_for(lead_genome.id, "propose")
    # Clear any stale proposal.md from a prior aborted attempt; otherwise the
    # Fellow's response of "Done." could refer to old content on disk.
    stale = workspace / "proposal.md"
    if stale.exists():
        stale.unlink()

    # Stage the Archive index (so the lead's "is this thread saturated?"
    # check is grounded in real data, not memory) and the standing
    # Open Problems list. Both are referenced in the topic-guidance
    # section of the brief.
    from institute import archive_index, open_problems

    workspaces.stage_input(workspace, "archive-index.md", archive_index.render())
    workspaces.stage_input(workspace, "open-problems.md", open_problems.render_summary_md())

    claude_runner.invoke(
        FellowTask(
            genome=lead_genome,
            project_id="pre-init",  # used only for the session id
            step="propose",
            brief=brief,
            workspace=workspace,
            extra_dirs=(paths.DOCS, paths.ARCHIVE),
        )
    )

    proposal_md = workspaces.require_output(workspace, "proposal.md", min_chars=300).strip()

    # Strip surrounding code fences if the Fellow wrapped its output.
    if proposal_md.startswith("```"):
        first_newline = proposal_md.find("\n")
        proposal_md = proposal_md[first_newline + 1 :]
        if proposal_md.rstrip().endswith("```"):
            proposal_md = proposal_md.rstrip()[:-3].rstrip()

    missing = _validate_sections(proposal_md)
    if missing:
        raise RuntimeError(
            f"Proposal is missing required sections: {missing}. "
            f"Full draft preserved at {workspace / 'proposal.md'} "
            f"({len(proposal_md)} chars). "
            f"First 800 chars:\n{proposal_md[:800]}"
        )

    title = _extract_title(proposal_md)
    project_id = _project_id(title)
    proposal_path = paths.PROPOSALS / project_id / "proposal.md"
    _atomic_write(proposal_path, proposal_md.rstrip() + "\n")

    # Auto-form a research group from the proposal's `## Collaborators
    # needed` section when the Founder didn't pre-select. Each named
    # Fellow accepts or declines via a quick Claude call; accepts join
    # the project. Founder pre-selection takes precedence over this path.
    invitations: list = []
    if not collaborator_genomes:
        from institute.workflows import group_form

        with db.connection() as conn:
            eligible_cohort = _eligible_invitees(conn, lead_genome.id)
        accepted, invitations = group_form.solicit(
            lead=lead_genome,
            proposal_md=proposal_md,
            project_id=project_id,
            title=title,
            eligible_cohort=eligible_cohort,
        )
        collaborator_genomes = accepted
        group_form.archive_invitations_md(project_id, invitations)

    now = datetime.now(UTC).isoformat(timespec="seconds")
    decision_actors = ["founder", lead_genome.id, *(g.id for g in collaborator_genomes)]
    decision = decisions.Decision(
        kind="proposal",
        title=f"Proposal: {title}",
        body=_format_proposal_decision_body(
            title, lead_genome, topic, proposal_path, collaborator_genomes, invitations
        ),
        actors=decision_actors,
        related_project=project_id,
    )

    with db.connection() as conn, db.transaction(conn):
        conn.execute(
            "INSERT INTO projects "
            "(id, title, state, lead_fellow_id, proposal_path, created_at, updated_at) "
            "VALUES (?, ?, ?, ?, ?, ?, ?)",
            (
                project_id,
                title,
                State.PROPOSED.value,
                lead_genome.id,
                str(proposal_path.relative_to(paths.ROOT)),
                now,
                now,
            ),
        )
        for collab in collaborator_genomes:
            collaborators.add(conn, project_id=project_id, fellow_id=collab.id)
        decisions.record(conn, decision)

    episodic.safe_ingest(
        fellow_id=lead_genome.id,
        kind="proposal",
        title=title,
        content=proposal_md,
        source_path=str(proposal_path.relative_to(paths.ROOT)),
        project_id=project_id,
    )
    # Co-authors get the proposal in their episodic memory too, so their
    # contributions during research grow out of the same shared context.
    for collab in collaborator_genomes:
        episodic.safe_ingest(
            fellow_id=collab.id,
            kind="proposal",
            title=f"Joined research group: {title}",
            content=proposal_md,
            source_path=str(proposal_path.relative_to(paths.ROOT)),
            project_id=project_id,
        )

    console.print()
    console.print(f"[green]Proposal written:[/green] {proposal_path.relative_to(paths.ROOT)}")
    console.print(f"[green]Project id:[/green]    {project_id}")
    console.print(f"[green]Lead Fellow:[/green]   {lead_genome.name} ({lead_genome.id})")
    if collaborator_genomes:
        members = ", ".join(f"{g.name} ({g.id})" for g in collaborator_genomes)
        console.print(f"[green]Collaborators:[/green] {members}")
    if invitations:
        for inv in invitations:
            verdict = "accepted" if inv.accepted else "declined"
            console.print(f"[dim]Invitation to {inv.invitee.name}: {verdict}[/dim]")
    console.print()
    console.print("[dim]Next: run `institute next` for proposal review.[/dim]")


def _format_proposal_decision_body(
    title: str,
    lead: Genome,
    topic: str | None,
    proposal_path: Path,
    collaborator_genomes: list[Genome],
    invitations: list | None = None,
) -> str:
    lines = [
        f"**Title:** {title}",
        "",
        f"**Lead Fellow:** {lead.name} (`{lead.id}`, {lead.specialization})",
        "",
    ]
    if collaborator_genomes:
        member_lines = "\n".join(
            f"- {g.name} (`{g.id}`, {g.specialization})" for g in collaborator_genomes
        )
        lines.extend(
            [
                "**Research group:**",
                "",
                member_lines,
                "",
            ]
        )
    if invitations:
        # Surface declines too so the record is honest about who said no.
        from institute.workflows.group_form import render_invitations_md

        invitation_block = render_invitations_md(invitations).lstrip("\n")
        if invitation_block:
            lines.extend([invitation_block, ""])
    lines.extend(
        [
            f"**Topic guidance from Founder:** {topic.strip() if topic else 'none (free choice)'}",
            "",
            f"**Proposal:** [{proposal_path.relative_to(paths.ROOT)}]"
            f"({proposal_path.relative_to(paths.ROOT)})",
            "",
            "The lead Fellow drafted this proposal in response to the topic",
            "guidance above (or chose the topic themselves if none was given).",
            "The proposal now enters review.",
        ]
    )
    return "\n".join(lines)


def _eligible_invitees(conn: sqlite3.Connection, lead_id: str) -> list[Genome]:
    """Every Fellow who could be invited to a research group on this proposal.

    Excludes the lead, Postulants (per Chapter 5 they research alone with
    an advisor), and retired Fellows. Reviewer-eligibility marks are
    deliberately ignored here: a Fellow who has been sidelined from
    reviewing may still co-author.
    """
    rows = list(
        conn.execute(
            "SELECT id FROM fellows "
            "WHERE retired_at IS NULL AND rank != 'postulant' AND id != ? "
            "ORDER BY name ASC",
            (lead_id,),
        )
    )
    return [fellow_mod.load_genome(conn, r["id"]) for r in rows]


def _validate_collaborators(
    conn: sqlite3.Connection,
    lead_id: str,
    collaborator_ids: list[str],
) -> list[Genome]:
    """Resolve collaborator ids to Genomes; enforce Chapter 6 group rules.

    - Lead may not also be a collaborator.
    - Each collaborator must exist, be active (not retired), and not a
      Postulant (Postulants research under apprenticeship; see Chapter 5).
    - Distinct ids only.
    - At most MAX_COLLABORATORS additional members (Chapter 6).
    """
    if not collaborator_ids:
        return []
    if len(collaborator_ids) > collaborators.MAX_COLLABORATORS:
        raise SystemExit(
            f"Too many collaborators ({len(collaborator_ids)}). "
            f"Chapter 6 caps a research group at one lead plus "
            f"{collaborators.MAX_COLLABORATORS} others."
        )
    seen: set[str] = set()
    resolved: list[Genome] = []
    for cid in collaborator_ids:
        if cid == lead_id:
            raise SystemExit(f"Lead Fellow {lead_id} cannot also be listed as a collaborator.")
        if cid in seen:
            raise SystemExit(f"Collaborator {cid} listed more than once.")
        seen.add(cid)
        row = conn.execute(
            "SELECT id, rank, retired_at FROM fellows WHERE id = ?", (cid,)
        ).fetchone()
        if row is None:
            raise SystemExit(f"Unknown Fellow id: {cid}")
        if row["retired_at"] is not None:
            raise SystemExit(f"Fellow {cid} is retired and cannot join a research group.")
        if row["rank"] == "postulant":
            raise SystemExit(
                f"Fellow {cid} is a Postulant; Postulants do their qualifying "
                "project alone with an advisor, per Chapter 5."
            )
        resolved.append(fellow_mod.load_genome(conn, cid))
    return resolved
