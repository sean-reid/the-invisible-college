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

from institute import claude_runner, db, decisions, paths, workspaces
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

A research proposal in markdown, structured as the following sections,
in this exact order, each as a level-2 heading:

1. `## Title` (the proposal's working title, on a single line)
2. `## Question` (the question you propose to investigate, as a question)
3. `## Background` (what is already known; cite specific sources, internal
   or external; include real URLs or document references where possible)
4. `## Approach` (concrete methods you will use; not vague intentions)
5. `## Expected output` (what form the result will take: demonstration,
   essay, code release, critical review, lab note, synthesis)
6. `## Resource estimate` (rough estimate of compute, time, and tool use;
   keep it bounded)
7. `## Anticipated failure modes` (how this could go wrong, and what an
   honest negative result would look like)
8. `## Collaborators needed` (which kinds of Fellows you might want to
   bring in; OK if none)

# Constraints

- Length: 600 to 1500 words total across all sections.
- Be specific. A proposal that could be written by anyone about anything
  has no value. The reader should know exactly what you are going to do.
- The question should be one you genuinely do not know the answer to.
- The Charter prohibits commercial activity, deception, plagiarism, and
  engagement-bait. Stay clear of those.
- Topics about AI safety, AI consciousness, or AI sentience are off-limits
  unless the topic guidance above explicitly requests them.

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
"""


REQUIRED_SECTIONS = [
    "Title",
    "Question",
    "Background",
    "Approach",
    "Expected output",
    "Resource estimate",
    "Anticipated failure modes",
    "Collaborators needed",
]


def _pick_lead(conn: sqlite3.Connection, requested: str | None) -> Genome:
    if requested is not None:
        return fellow_mod.load_genome(conn, requested)
    # Heuristic: pick the highest-rank, non-builder, non-critic Fellow.
    # If none qualifies, pick the first active fellow.
    rows = list(
        conn.execute(
            "SELECT id, specialization FROM fellows WHERE retired_at IS NULL ORDER BY rank DESC, name"
        )
    )
    if not rows:
        raise SystemExit("No active Fellows. Run `institute bootstrap` first.")

    preferred = [
        r
        for r in rows
        if "build" not in r["specialization"].lower()
        and "critic" not in r["specialization"].lower()
    ]
    chosen = preferred[0] if preferred else rows[0]
    return fellow_mod.load_genome(conn, chosen["id"])


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
    # Capture everything between "## Title" and the next "##" heading or EOF.
    match = re.search(
        r"^##\s+Title\s*$\n+(.*?)(?=^##\s+|\Z)",
        markdown,
        re.MULTILINE | re.DOTALL,
    )
    if not match:
        raise RuntimeError("Proposal is missing a `## Title` section.")
    body = match.group(1).strip()
    if not body:
        raise RuntimeError("Proposal `## Title` section is empty.")
    # The Fellow may put the title on its own line, or prefixed with "# ", or
    # in a single short paragraph. Take the first non-empty line.
    first_line = next((ln.strip() for ln in body.splitlines() if ln.strip()), "")
    if first_line.startswith("# "):
        first_line = first_line[2:].strip()
    if not first_line:
        raise RuntimeError("Proposal `## Title` section is empty.")
    return first_line


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
    path.parent.mkdir(parents=True, exist_ok=True)
    tmp = path.with_suffix(path.suffix + ".tmp")
    tmp.write_text(content, encoding="utf-8")
    tmp.replace(path)


def run(*, lead: str | None = None, topic: str | None = None) -> None:
    """Top-level propose entry point. Called from cli.propose."""

    # Resolve the lead fellow first so we error early if the institution is empty.
    with db.connection() as conn:
        lead_genome = _pick_lead(conn, lead)

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

    now = datetime.now(UTC).isoformat(timespec="seconds")
    decision = decisions.Decision(
        kind="proposal",
        title=f"Proposal: {title}",
        body=_format_proposal_decision_body(title, lead_genome, topic, proposal_path),
        actors=["founder", lead_genome.id],
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
        decisions.record(conn, decision)

    console.print()
    console.print(f"[green]Proposal written:[/green] {proposal_path.relative_to(paths.ROOT)}")
    console.print(f"[green]Project id:[/green]    {project_id}")
    console.print(f"[green]Lead Fellow:[/green]   {lead_genome.name} ({lead_genome.id})")
    console.print()
    console.print("[dim]Next: run `institute next` for proposal review.[/dim]")


def _format_proposal_decision_body(
    title: str,
    lead: Genome,
    topic: str | None,
    proposal_path: Path,
) -> str:
    lines = [
        f"**Title:** {title}",
        "",
        f"**Lead Fellow:** {lead.name} (`{lead.id}`, {lead.specialization})",
        "",
        f"**Topic guidance from Founder:** {topic.strip() if topic else 'none (free choice)'}",
        "",
        f"**Proposal:** [{proposal_path.relative_to(paths.ROOT)}]({proposal_path.relative_to(paths.ROOT)})",
        "",
        "The lead Fellow drafted this proposal in response to the topic",
        "guidance above (or chose the topic themselves if none was given).",
        "The proposal now enters review.",
    ]
    return "\n".join(lines)
