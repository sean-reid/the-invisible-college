"""Research-group formation by Fellow nomination.

When the lead Fellow drafts a proposal, the `## Collaborators needed`
section is prose the lead writes naming people they want to invite
(or "none"). This module parses that section against the active
cohort, invites each named Fellow with a quick accept/decline call,
and returns the accepters.

The Founder may still pre-select collaborators via
`institute propose --collaborator <id>`; in that case this module is
not invoked. Auto-formation only runs when the Founder left the slot
empty, which is the autopilot path.
"""

from __future__ import annotations

import json
import re
import unicodedata
from dataclasses import dataclass
from datetime import UTC, datetime
from pathlib import Path

from rich.console import Console

from institute import claude_runner, collaborators, db, parsing, paths, workspaces
from institute.claude_runner import FellowTask
from institute.fellow import Genome

console = Console()


INVITATION_BRIEF = """\
You are {invitee_name}, a {invitee_rank} at the Invisible College
specializing in {invitee_specialization}. {lead_name} has invited you
to join their research group on a project titled "{title}".

# Inputs

In your current working directory you will find:
- `proposal.md`     the proposal {lead_name} has drafted
- `memory.md`       if present, the most relevant entries from your own
                    episodic memory

Read them with the Read tool before deciding.

# Your decision

Accept only if you can contribute substantively. Per Chapter 6, a
nominal contributor is not listed as a coauthor; a vague yes that
produces no real work is worse than a clean decline. Decline if:

- The topic is outside your range of useful contribution.
- You are already heavy on in-flight work.
- The proposal is structurally weak in a way you cannot help fix.

Accepting means you will write a 300-800 word contribution.md during
research and be co-credited on the publication. Reviewers will judge
you on what you actually contributed.

# Output

Use the Write tool to create `decision.json` with exactly these fields:

{{
  "decision": "<accept|decline>",
  "rationale": "<2 to 4 sentences explaining your reasoning>"
}}

# Final reply

When `decision.json` exists, reply with the single word `Done.` Nothing
else. Do NOT paste the decision into your reply.
"""


@dataclass(frozen=True)
class Invitation:
    invitee: Genome
    accepted: bool
    rationale: str


def _norm(text: str) -> str:
    """Lowercase + strip combining marks for accent-tolerant matching."""
    nfkd = unicodedata.normalize("NFKD", text)
    stripped = "".join(c for c in nfkd if not unicodedata.combining(c))
    return stripped.lower()


def extract_collaborators_section(proposal_md: str) -> str | None:
    """Return the body of the `## Collaborators needed` section, or None.

    Matches the canonical heading and any of the accepted synonyms (kept
    in sync with propose._SECTION_VARIANTS). Returns the prose between
    that heading and the next level-2 heading (or end of file).
    """
    headings = [
        "Collaborators needed",
        "Collaborators",
        "Collaboration",
        "Required collaborators",
    ]
    for heading in headings:
        pattern = rf"^##\s+{re.escape(heading)}\s*$\n+(.*?)(?=^##\s+|\Z)"
        m = re.search(pattern, proposal_md, re.MULTILINE | re.DOTALL | re.IGNORECASE)
        if m:
            return m.group(1).strip()
    return None


def match_invitees(
    section_text: str,
    cohort: list[tuple[str, str]],
    *,
    max_count: int = collaborators.MAX_COLLABORATORS,
) -> list[str]:
    """Return fellow ids the lead named, ordered by first appearance.

    cohort is a list of `(fellow_id, fellow_name)` for every Fellow
    eligible to be invited (active, non-postulant, not the lead).
    Matching is case- and accent-insensitive. A match counts if either
    the full name or the fellow id appears as a substring in the
    section. Output is deduplicated and capped at `max_count`.
    """
    if not section_text:
        return []
    norm_text = _norm(section_text)
    positions: list[tuple[int, str]] = []
    for fid, name in cohort:
        candidates: list[int] = []
        norm_name = _norm(name)
        if norm_name:
            pos = norm_text.find(norm_name)
            if pos != -1:
                candidates.append(pos)
        pos = norm_text.find(fid.lower())
        if pos != -1:
            candidates.append(pos)
        if candidates:
            positions.append((min(candidates), fid))
    positions.sort()
    out: list[str] = []
    seen: set[str] = set()
    for _, fid in positions:
        if fid in seen:
            continue
        seen.add(fid)
        out.append(fid)
        if len(out) >= max_count:
            break
    return out


def invite(
    invitee: Genome,
    *,
    lead: Genome,
    proposal_md: str,
    project_id: str,
    title: str,
) -> Invitation:
    """Run one accept/decline invitation. Persists the response to the archive.

    A malformed or absent response is treated as an implicit decline so
    a hiccup in one invitation never blocks the whole proposal. The
    rationale records the parse failure so the audit trail is honest.
    """
    workspace = workspaces.workspace_for(invitee.id, f"{project_id}-invite")
    workspaces.stage_input(workspace, "proposal.md", proposal_md)

    console.print(
        f"[dim]Inviting {invitee.name} ({invitee.id}) to join "
        f"{lead.name}'s research group on `{project_id}`...[/dim]"
    )

    brief = INVITATION_BRIEF.format(
        invitee_name=invitee.name,
        invitee_rank=invitee.rank,
        invitee_specialization=invitee.specialization,
        lead_name=lead.name,
        title=title,
    )

    claude_runner.invoke(
        FellowTask(
            genome=invitee,
            project_id=project_id,
            step=f"invitation:{invitee.id}",
            brief=brief,
            workspace=workspace,
            extra_dirs=(paths.DOCS,),
        )
    )

    invitations_dir = paths.PROPOSALS / project_id / "invitations"
    invitations_dir.mkdir(parents=True, exist_ok=True)
    decision_path = invitations_dir / f"{invitee.id}.json"

    try:
        decision_text = workspaces.require_output(workspace, "decision.json", min_chars=10)
        payload = parsing.parse_json_or_dump(
            decision_text,
            dump_path=invitations_dir / f"{invitee.id}.raw.txt",
            context=f"Invitation response from {invitee.id} on {project_id}",
        )
    except Exception as exc:
        payload = {
            "decision": "decline",
            "rationale": (
                f"Implicit decline: invitation response was missing or unparseable ({exc})."
            ),
        }

    decision = str(payload.get("decision", "decline")).strip().lower()
    rationale = str(payload.get("rationale", "")).strip()
    accepted = decision == "accept"

    recorded_at = datetime.now(UTC).isoformat(timespec="seconds")
    record = {
        "invitee_id": invitee.id,
        "invitee_name": invitee.name,
        "lead_id": lead.id,
        "lead_name": lead.name,
        "project_id": project_id,
        "decision": "accept" if accepted else "decline",
        "rationale": rationale or "(no rationale provided)",
        "recorded_at": recorded_at,
    }
    tmp = decision_path.with_suffix(decision_path.suffix + ".tmp")
    tmp.write_text(json.dumps(record, indent=2) + "\n", encoding="utf-8")
    tmp.replace(decision_path)

    # Also write the decision into project_invitations so peer-review's
    # CoI exclusion (Chapter 7: an invited Fellow who declined cannot
    # review the same project) stays a pure SQL filter. The JSON file
    # remains the canonical institutional record; the DB row is the index.
    try:
        with db.connection() as conn, db.transaction(conn):
            conn.execute(
                "INSERT OR REPLACE INTO project_invitations "
                "(project_id, fellow_id, decision, rationale, invited_at) "
                "VALUES (?, ?, ?, ?, ?)",
                (
                    project_id,
                    invitee.id,
                    "accept" if accepted else "decline",
                    rationale or None,
                    recorded_at,
                ),
            )
    except Exception as exc:  # pragma: no cover - best-effort path
        console.print(
            f"[yellow]invitation DB write failed for {invitee.id}/{project_id}: {exc}[/yellow]"
        )

    return Invitation(invitee=invitee, accepted=accepted, rationale=rationale)


def solicit(
    *,
    lead: Genome,
    proposal_md: str,
    project_id: str,
    title: str,
    eligible_cohort: list[Genome],
) -> tuple[list[Genome], list[Invitation]]:
    """Top-level: parse, match, invite. Returns (accepted_genomes, all_invitations).

    `eligible_cohort` is every Fellow who could be invited (active,
    non-postulant, not the lead, not retired, etc). Callers must filter
    upstream — this function only handles parsing and dispatch.
    """
    section = extract_collaborators_section(proposal_md)
    if not section:
        return [], []
    cohort_pairs = [(g.id, g.name) for g in eligible_cohort]
    invitee_ids = match_invitees(section, cohort_pairs)
    if not invitee_ids:
        return [], []

    by_id = {g.id: g for g in eligible_cohort}
    invitations: list[Invitation] = []
    accepted: list[Genome] = []
    for fid in invitee_ids:
        invitee = by_id[fid]
        result = invite(
            invitee,
            lead=lead,
            proposal_md=proposal_md,
            project_id=project_id,
            title=title,
        )
        invitations.append(result)
        if result.accepted:
            accepted.append(invitee)

    return accepted, invitations


def render_invitations_md(invitations: list[Invitation]) -> str:
    """Render an invitations summary for the proposal decision body."""
    if not invitations:
        return ""
    lines = ["", "## Invitations", ""]
    for inv in invitations:
        verdict = "accepted" if inv.accepted else "declined"
        lines.append(f"- **{inv.invitee.name}** (`{inv.invitee.id}`): {verdict}")
        if inv.rationale:
            lines.append(f"  - _{inv.rationale}_")
    return "\n".join(lines)


def archive_invitations_md(project_id: str, invitations: list[Invitation]) -> Path | None:
    """Write a human-readable invitations log next to the proposal."""
    if not invitations:
        return None
    summary = render_invitations_md(invitations).lstrip("\n")
    path = paths.PROPOSALS / project_id / "invitations" / "summary.md"
    path.parent.mkdir(parents=True, exist_ok=True)
    tmp = path.with_suffix(path.suffix + ".tmp")
    tmp.write_text(summary + "\n", encoding="utf-8")
    tmp.replace(path)
    return path
