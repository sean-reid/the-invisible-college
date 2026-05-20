"""Publish-time editorial pass: select per-paper follow-up questions.

When a Fellow ships a paper, the research and revise workflows already
captured a handful of candidate follow-up questions in
`archive/open-problems/` with `source_project_id` set to the paper's
project. Most of those questions are too close to the paper to belong
in the College's standing list. They are local to the paper and should
either appear in its own footer or be discarded.

This module runs that triage. A Senior Fellow on the current Editorial
Board (excluding the lead, collaborators, and reviewers of the paper)
reads the draft and the candidate questions, picks at most three, and
the rest are dropped. The selected ones are rendered into a
"Questions this leaves open" section that the publish workflow splices
into the body of the paper, above the References section.

The editor is a Fellow, deliberately. The orchestrator does not pick.
This is the same design move the Editorial Board makes for accept/reject
calls: institutional judgment lives in Fellows, not in the runtime.

If no eligible editor exists (e.g. there are no Senior Fellows yet, or
all of them are on the author/reviewer side of this paper), the pass
returns no footer and leaves the candidate questions in their open
state. The paper publishes without a Questions section; the candidates
remain in the standing list and may be cleaned up later by hand.
"""

from __future__ import annotations

import json
import re
import sqlite3
from dataclasses import dataclass
from pathlib import Path

from rich.console import Console

from institute import (
    claude_runner,
    editorial_board,
    open_problems,
    parsing,
    paths,
)
from institute import (
    fellow as fellow_mod,
)
from institute.claude_runner import FellowTask
from institute.fellow import Genome

console = Console()

MAX_SURVIVORS = 3


EDITOR_BRIEF = """\
You are serving as the editor for a paper the College is about to
publish. The paper's author and reviewers have proposed a handful of
follow-up questions while writing the piece. Most of those are too
close to the paper to belong in the College's standing list of open
problems; some, however, are worth attaching to the published piece so
readers know what the work leaves open.

Your job is to read the draft and the candidate follow-up questions
and pick the two or three that most belong in the paper's footer.

# Inputs in your workspace

- `draft.md`        the paper that is about to publish.
- `candidates.md`   the candidate follow-up questions, each with a slug,
                    a title, and a body. Read these carefully.

Read both with the Read tool.

# Selection criteria

- Pick at most three. Two is often enough. Zero is allowed if none of
  the candidates is good enough to ship in the paper.
- Prefer questions that are concrete, that point somewhere the paper
  did not go, and that a reader can imagine making progress on.
- Drop near-duplicates. If two candidates are restating the same
  question with different wording, pick the better-stated one.
- Drop questions that merely paraphrase a result the paper already
  established or that are too vague to act on.
- The questions you keep will appear in the paper's footer. The
  questions you drop are discarded permanently. There is no
  intermediate fate.

# CRITICAL OUTPUT RULES

Reply with a single JSON object. No prose preface, no summary, no
code fence. First character `{`, last `}`.

# Output shape

```
{
  "selected_slugs": ["<slug>", "<slug>", "<slug>"],
  "rationale": "<60-200 words on why these three (or fewer), and what you cut>"
}
```

The slugs must be the exact slug strings from `candidates.md`. Order
in `selected_slugs` is the order they will appear in the paper's
footer; put the strongest first.
"""


@dataclass(frozen=True)
class EditorialPassResult:
    """What the publish workflow needs back from the pass."""

    editor: Genome | None  # None if no eligible editor was available
    promoted: list[open_problems.OpenProblem]
    discarded: list[open_problems.OpenProblem]
    rationale: str
    footer_md: str  # empty string if no section should be appended


def _eligible_editor(
    conn: sqlite3.Connection,
    *,
    lead_id: str,
    collaborator_ids: list[str],
    reviewer_ids: list[str],
) -> Genome | None:
    """Pick a Senior Fellow on the Board who is not on the paper's side.

    Preference order:
      1. A current Editorial Board member who is not author/reviewer.
      2. Any active Senior Fellow not author/reviewer (fallback when the
         Board has been eaten by this paper's review roster).
    Returns None if no candidate exists.
    """
    excluded = {lead_id, *collaborator_ids, *reviewer_ids}

    board_ids = editorial_board.current_member_ids(conn)
    for fid in board_ids:
        if fid not in excluded:
            return fellow_mod.load_genome(conn, fid)

    rows = list(
        conn.execute(
            "SELECT id FROM fellows "
            "WHERE rank = 'senior_fellow' AND retired_at IS NULL "
            "ORDER BY created_at"
        )
    )
    for r in rows:
        if r["id"] not in excluded:
            return fellow_mod.load_genome(conn, r["id"])
    return None


def _candidates_md(items: list[open_problems.OpenProblem]) -> str:
    out: list[str] = ["# Candidate follow-up questions", ""]
    for p in items:
        out.append(f"## {p.title}")
        out.append("")
        out.append(f"`slug: {p.slug}`")
        out.append("")
        out.append(p.body.strip())
        out.append("")
    return "\n".join(out)


def _stage(path: Path, content: str) -> None:
    from institute.safe_io import atomic_write

    atomic_write(path, content)


_TRAILING_TAGS_OR_SEP_RE = re.compile(
    r"(?:\s*\n\s*-{3,}\s*)?(?:\s*\n\s*[Tt]ags\s*:[^\n]*)?(?:\s*\n\s*-{3,}\s*)?\s*\Z",
)


def _render_footer(items: list[open_problems.OpenProblem]) -> str:
    if not items:
        return ""
    lines = ["## Questions this leaves open", ""]
    for p in items:
        # Defensive strip: even with the upstream parser fixed, an
        # open-problem body filed before that fix may still carry a
        # trailing `Tags: ...` line and/or `---` separator. Strip them
        # here so the footer never leaks the source-file scaffolding
        # into the published markdown.
        body = _TRAILING_TAGS_OR_SEP_RE.sub("", p.body).strip()
        body = body.replace("\n", " ")
        body = re.sub(r"\s+", " ", body)
        lines.append(f"- **{p.title}.** {body}")
    return "\n".join(lines) + "\n"


def splice_above_references(body: str, footer_md: str) -> str:
    """Insert `footer_md` immediately before a `## References` heading.

    If the body has no References section, the footer is appended at the
    end. Either way, the footer ends with a single trailing newline so
    the publication renders with consistent spacing.
    """
    if not footer_md:
        return body
    if not footer_md.endswith("\n"):
        footer_md += "\n"
    ref_re = re.compile(r"^## References\b", re.MULTILINE)
    m = ref_re.search(body)
    if m is None:
        return body.rstrip() + "\n\n" + footer_md
    head = body[: m.start()].rstrip()
    tail = body[m.start() :]
    return head + "\n\n" + footer_md + "\n" + tail


def run(
    *,
    conn: sqlite3.Connection,
    project_id: str,
    draft_md: str,
    lead_id: str,
    collaborator_ids: list[str],
    reviewer_ids: list[str],
) -> EditorialPassResult:
    """Run the editorial pass for `project_id`.

    Mutates open-problem files on disk (promoted vs dropped) but does NOT
    touch the publication body. The caller splices the returned
    `footer_md` into the body via `splice_above_references`.
    """
    candidates = [p for p in open_problems.for_project(project_id) if p.status == "open"]
    if not candidates:
        return EditorialPassResult(
            editor=None, promoted=[], discarded=[], rationale="", footer_md=""
        )

    editor = _eligible_editor(
        conn,
        lead_id=lead_id,
        collaborator_ids=collaborator_ids,
        reviewer_ids=reviewer_ids,
    )
    if editor is None:
        console.print(
            "[yellow]No eligible editor for follow-up pass on "
            f"{project_id}. Leaving {len(candidates)} candidate "
            "question(s) in the standing list.[/yellow]"
        )
        return EditorialPassResult(
            editor=None,
            promoted=[],
            discarded=[],
            rationale="",
            footer_md="",
        )

    ws = paths.FELLOWS / editor.id / "workspace" / f"followups-{project_id}"
    ws.mkdir(parents=True, exist_ok=True)
    _stage(ws / "draft.md", draft_md)
    _stage(ws / "candidates.md", _candidates_md(candidates))

    console.print(
        f"[dim]Editor {editor.name} is selecting follow-up "
        f"questions from {len(candidates)} candidate(s)...[/dim]"
    )
    result = claude_runner.invoke(
        FellowTask(
            genome=editor,
            project_id=project_id,
            step="editorial-followups",
            brief=EDITOR_BRIEF,
            workspace=ws,
        )
    )

    payload = parsing.parse_json_or_dump(
        result.result_text,
        dump_path=ws / "raw-decision.txt",
        context=f"Editorial follow-ups decision from {editor.id} on {project_id}",
    )
    selected_slugs_raw = payload.get("selected_slugs") or []
    if not isinstance(selected_slugs_raw, list):
        selected_slugs_raw = []
    selected_slugs: list[str] = []
    for s in selected_slugs_raw:
        if isinstance(s, str) and s.strip():
            selected_slugs.append(s.strip())
    rationale = str(payload.get("rationale") or "").strip()

    by_slug = {p.slug: p for p in candidates}
    promoted: list[open_problems.OpenProblem] = []
    for slug in selected_slugs[:MAX_SURVIVORS]:
        if slug in by_slug and slug not in [p.slug for p in promoted]:
            promoted.append(by_slug[slug])

    promoted_set = {p.slug for p in promoted}
    discarded = [p for p in candidates if p.slug not in promoted_set]

    for p in promoted:
        open_problems.mark_promoted(p.slug)
    for p in discarded:
        open_problems.discard(p.slug)

    _stage(
        ws / "decision.json",
        json.dumps(
            {
                "editor_id": editor.id,
                "editor_name": editor.name,
                "promoted": [p.slug for p in promoted],
                "discarded": [p.slug for p in discarded],
                "rationale": rationale,
            },
            indent=2,
        ),
    )

    return EditorialPassResult(
        editor=editor,
        promoted=promoted,
        discarded=discarded,
        rationale=rationale,
        footer_md=_render_footer(promoted),
    )


__all__ = [
    "MAX_SURVIVORS",
    "EditorialPassResult",
    "run",
    "splice_above_references",
]
