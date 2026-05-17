"""Revise workflow: lead Fellow incorporates peer review feedback.

When peer review is filed with any non-accept recommendation, the project
enters REVISING. The lead Fellow re-enters their workspace with: the
current draft, the lab notebook, and every signed review verbatim. The
Fellow produces a revised draft, a response-to-reviewers document, an
updated abstract, and a lab-notebook addendum recording what changed.

The prior draft is preserved as draft.v1.md (or .v2, .v3, ...) for
provenance. The lab notebook is appended-to, never overwritten.

For v1.1 we do one revision pass and then go straight to EDITORIAL. A
later iteration can send the revised draft back through peer review for
a second round.
"""

from __future__ import annotations

import re
import sqlite3
from datetime import UTC, datetime
from pathlib import Path

from rich.console import Console

from institute import claude_runner, db, decisions, parsing, paths
from institute import fellow as fellow_mod
from institute.claude_runner import FellowTask
from institute.state import State

console = Console()


BRIEF = """\
You are revising your own research piece for the Invisible College after
{round_label} peer review. You are the lead author. You have the current
draft, your lab notebook so far, and the signed peer reviews you are
responding to.

{round_context}

# Your task

Read every review carefully. For each concern raised, decide one of:

1. **Address it**: change the draft to fix the problem.
2. **Decline it with reasoning**: keep the draft as-is and explain why in
   the response-to-reviewers document.

Sycophantic capitulation is not the goal. If a reviewer is wrong, say so
in the response and defend the original choice. If a reviewer is right,
fix the draft and acknowledge the correction.

# CRITICAL OUTPUT RULES

Your entire final reply MUST be a single JSON object. No prose preface,
no summary, no code fence. The first character is `{{` and the last is
`}}`. The receiving program parses your reply with `json.loads`.

# Output shape

```json
{{
  "abstract": "<updated 40-90 word abstract reflecting any changes>",
  "draft": "<the revised draft, full markdown>",
  "response_to_reviewers": "<markdown; address each reviewer's concerns by name>",
  "notebook_addendum": "<markdown; a new dated lab-notebook entry recording the revision pass>"
}}
```

# Constraints

- The revised `draft` is a full markdown document, not a diff. It
  replaces the previous draft as the publishable artifact.
- The `response_to_reviewers` must address each named reviewer's
  recommendation explicitly. Use level-3 headings (`### Response to
  <reviewer name>`) for each.
- The `notebook_addendum` will be APPENDED to your existing notebook,
  not replacing it. Date it. Be specific about what changed and why.
- The `abstract` may be identical to the previous one if the piece's
  substance did not change. But if you addressed substantive concerns,
  update it accordingly.

# Your previous draft

{draft_md}

# Your lab notebook so far

{notebook_md}

# The peer reviews

{reviews_md}
"""


def _format_reviews_for_brief(conn: sqlite3.Connection, project_id: str, review_round: int) -> str:
    """Concatenate filed reviews for the given round with reviewer attribution."""
    rows = list(
        conn.execute(
            "SELECT reviewer_id, role, recommendation, confidence, content_path "
            "FROM reviews WHERE project_id = ? AND round = ? ORDER BY role",
            (project_id, review_round),
        )
    )
    if not rows:
        return "(no reviews on file)"

    blocks = []
    for row in rows:
        genome = fellow_mod.load_genome(conn, row["reviewer_id"])
        body = (paths.ROOT / row["content_path"]).read_text(encoding="utf-8")
        blocks.append(
            "\n".join(
                [
                    f"## Review by {genome.name}",
                    f"- Role: {row['role']}",
                    f"- Recommendation: {row['recommendation']}",
                    f"- Confidence: {row['confidence']}",
                    "",
                    body.strip(),
                    "",
                ]
            )
        )
    return "\n\n".join(blocks)


def _atomic_write(path: Path, content: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    tmp = path.with_suffix(path.suffix + ".tmp")
    tmp.write_text(content, encoding="utf-8")
    tmp.replace(path)


def _next_draft_version(draft_dir: Path) -> int:
    """Inspect existing draft.v*.md files and return the next version number."""
    versions = [
        int(m.group(1))
        for p in draft_dir.glob("draft.v*.md")
        if (m := re.match(r"draft\.v(\d+)\.md$", p.name))
    ]
    return max(versions, default=0) + 1


def _extract_draft_title(draft_md: str) -> str | None:
    match = re.search(r"^#\s+(.+?)$", draft_md.lstrip(), re.MULTILINE)
    return match.group(1).strip() if match else None


def run(project_id: str) -> None:
    """Top-level revise entry point. Called when state is REVISING."""
    with db.connection() as conn:
        proj = conn.execute(
            "SELECT id, title, state, draft_path, notebook_path, lead_fellow_id, "
            "review_round FROM projects WHERE id = ?",
            (project_id,),
        ).fetchone()
        if proj is None:
            raise SystemExit(f"No such project: {project_id}")
        if proj["state"] != State.REVISING.value:
            raise SystemExit(
                f"Project {project_id} is in state {proj['state']}, expected revising."
            )
        current_round = int(proj["review_round"])
        lead = fellow_mod.load_genome(conn, proj["lead_fellow_id"])
        draft_md = (paths.ROOT / proj["draft_path"]).read_text(encoding="utf-8")
        notebook_md = (paths.ROOT / proj["notebook_path"]).read_text(encoding="utf-8")
        reviews_md = _format_reviews_for_brief(conn, project_id, current_round)

    console.print(
        f"[dim]Asking {lead.name} ({lead.id}) to revise their draft in light of "
        "the peer reviews. This will likely take several minutes...[/dim]"
    )

    if current_round == 1:
        round_label = "round-1"
        round_context = (
            "After this revision the same reviewers will see the revised draft "
            "and file a second round of reviews. So this is a substantive "
            "rewrite responding to specific concerns, not the final polish."
        )
    else:
        round_label = "round-2"
        round_context = (
            "This is the FINAL polishing pass. After this revision the project "
            "goes directly to editorial; there is no third round. Address any "
            "remaining concerns as best you can, or defend the prior version "
            "explicitly in the response document. The previous draft already "
            "incorporated round-1 feedback; do not undo those changes."
        )
    brief = BRIEF.format(
        round_label=round_label,
        round_context=round_context,
        draft_md=draft_md,
        notebook_md=notebook_md,
        reviews_md=reviews_md,
    )
    result = claude_runner.invoke(
        FellowTask(
            genome=lead,
            project_id=project_id,
            step="revise",
            brief=brief,
            extra_dirs=(paths.DOCS, paths.ARCHIVE),
        )
    )

    dump_path = paths.DRAFTS / project_id / "raw-revise-output.txt"
    payload = parsing.parse_json_or_dump(
        result.result_text,
        dump_path=dump_path,
        context=f"Revise output from {lead.name} for project {project_id}",
    )
    for required in ("draft", "response_to_reviewers"):
        if required not in payload:
            dump_path.parent.mkdir(parents=True, exist_ok=True)
            dump_path.write_text(result.result_text, encoding="utf-8")
            raise RuntimeError(
                f"Revise payload missing `{required}`. Got keys: {list(payload)}. "
                f"Raw saved to {dump_path}."
            )

    new_abstract = (payload.get("abstract") or "").strip() or None
    new_draft_md = payload["draft"].strip()
    response_md = payload["response_to_reviewers"].strip()
    addendum = (payload.get("notebook_addendum") or "").strip()
    if not new_draft_md or not response_md:
        raise RuntimeError("Revised draft or response_to_reviewers is empty.")

    # Preserve the prior draft as draft.vN.md before overwriting.
    draft_dir = paths.DRAFTS / project_id
    draft_dir.mkdir(parents=True, exist_ok=True)
    version = _next_draft_version(draft_dir)
    prior_draft_path = draft_dir / f"draft.v{version}.md"
    _atomic_write(prior_draft_path, draft_md.rstrip() + "\n")
    _atomic_write(draft_dir / "draft.md", new_draft_md + "\n")

    if new_abstract:
        _atomic_write(draft_dir / "abstract.txt", new_abstract + "\n")

    response_path = draft_dir / f"response-to-reviewers.v{version}.md"
    _atomic_write(response_path, response_md.rstrip() + "\n")

    # Append to the lab notebook rather than overwriting.
    if addendum:
        notebook_path = paths.ROOT / proj["notebook_path"]
        existing = notebook_path.read_text(encoding="utf-8").rstrip()
        combined = existing + "\n\n---\n\n" + addendum.rstrip() + "\n"
        _atomic_write(notebook_path, combined)

    new_title = _extract_draft_title(new_draft_md) or proj["title"]

    # Where this revision goes depends on which round triggered it.
    #
    #   current_round == 1 (just addressed round-1 reviews)
    #     -> back to peer_reviewing for round 2; same reviewers see the
    #        revised draft and the response.
    #   current_round == 2 (just addressed round-2 reviews)
    #     -> final polishing pass; project moves directly to editorial.
    #        There is no third round.
    if current_round == 1:
        target_state = State.PEER_REVIEWING
        next_round = 2
        next_description = (
            f"Project transitions to `peer_reviewing` for round {next_round}. "
            "The same reviewers will see the revised draft and the response."
        )
    else:
        target_state = State.EDITORIAL
        next_round = current_round  # do not advance; this is the final polish
        next_description = (
            "Final polishing pass after round-2 feedback. Project transitions "
            "directly to `editorial` for publication. No further review rounds."
        )

    decision = decisions.Decision(
        kind="revision",
        title=f"Revision pass (round {current_round} feedback): {new_title}",
        body=(
            f"**Lead Fellow:** {lead.name} (`{lead.id}`)\n\n"
            f"**Addressing:** round-{current_round} reviews\n\n"
            f"**Prior draft preserved:** [{prior_draft_path.relative_to(paths.ROOT)}]"
            f"({prior_draft_path.relative_to(paths.ROOT)})\n\n"
            f"**Revised draft:** [archive/drafts/{project_id}/draft.md]"
            f"(archive/drafts/{project_id}/draft.md)\n\n"
            f"**Response to reviewers:** [{response_path.relative_to(paths.ROOT)}]"
            f"({response_path.relative_to(paths.ROOT)})\n\n"
            f"{next_description}"
        ),
        actors=[lead.id],
        related_project=project_id,
    )

    now = datetime.now(UTC).isoformat(timespec="seconds")
    with db.connection() as conn, db.transaction(conn):
        conn.execute(
            "UPDATE projects "
            "SET state = ?, title = ?, review_round = ?, updated_at = ? "
            "WHERE id = ?",
            (target_state.value, new_title, next_round, now, project_id),
        )
        decisions.record(conn, decision)

    console.print()
    console.print(
        f"[green]Revision filed.[/green]   Prior draft: {prior_draft_path.relative_to(paths.ROOT)}"
    )
    console.print(f"[green]Response:[/green]         {response_path.relative_to(paths.ROOT)}")
    round_label = f" (round {next_round})" if target_state == State.PEER_REVIEWING else ""
    console.print(f"[green]New state:[/green]       {target_state.value}{round_label}")
