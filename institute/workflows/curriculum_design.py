"""Curriculum design: orchestrator drafts a Postulant's reading list.

Called from `institute admit` after a candidate is admitted. Reads the
Postulant's specialization, the Charter, the design chapters, and the
published Archive, then composes a three-layer curriculum tailored to
the new admit.

The list is small by design (about 6 to 10 items total). Chapter 5
warns against curricular bloat: the Postulant must produce, not just
read.
"""

from __future__ import annotations

from datetime import UTC, datetime
from pathlib import Path

from rich.console import Console

from institute import archive_index, claude_runner, curriculum, db, parsing, paths
from institute.fellow import Genome

console = Console()


DESIGN_BRIEF = """\
You are the orchestrator of the Invisible College. A new Postulant
has been admitted. Your job is to compose their reading curriculum:
the three-layer list of materials they will engage with in their
first weeks under advisor supervision. Chapter 5 of the design
(`docs/05-curriculum.md`) describes the structure.

# Inputs in your working directory

- `postulant.md`     the new Postulant's identity, specialization, and
                     advisor pairing.
- `archive-index.md` every piece the College has published, oldest
                     first. Eligible material for the foundational and
                     specialization layers.

Read both with the Read tool. Then read `docs/01-charter.md`,
`docs/05-curriculum.md`, and any other chapter relevant to the
Postulant's specialization.

# What you must produce

A curriculum with three layers and a small total item count (6-10
items across all three). Chapter 5 explicitly warns against curricular
bloat: the Postulant must read AND produce.

1. **Foundational** (3-4 items, common to most Postulants):
   - The Charter (`docs/01-charter.md`) is mandatory.
   - One or two exemplary past College publications, chosen for craft.
   - Optionally one external classic that anchors the College's
     intellectual orientation.

2. **Specialization** (2-3 items, advisor-curated):
   - Current state of work in this Postulant's specialization, inside
     or outside the College. Cite real, locatable references where
     possible.

3. **Methodological** (1-2 items):
   - Depends on the kinds of work the Postulant intends to do.

For each item, specify:
- A stable `id` (kebab-case, prefixed with the first 4 letters of the
  layer name, e.g. `foun-charter`).
- A short `title`.
- A `source` (path inside the repo, a URL, or a citation).
- A `prompt` for engagement: critique, summarize, apply, or extend.

# CRITICAL OUTPUT RULES

Your entire final reply MUST be a single JSON object. No prose
preface, no code fence. First character `{{`, last character `}}`.

# Output shape

```
{{
  "items": [
    {{
      "id": "<kebab-case-id>",
      "layer": "foundational" | "specialization" | "methodological",
      "title": "<short title>",
      "source": "<path | URL | citation>",
      "prompt": "<one or two sentences: what to do with this item>"
    }},
    ...
  ]
}}
```
"""


def _render_postulant_brief(postulant: Genome, advisor_name: str | None) -> str:
    lines = [
        f"# Postulant: {postulant.name}",
        "",
        f"- **id:** `{postulant.id}`",
        f"- **rank:** {postulant.rank}",
        f"- **model:** `{postulant.model}`",
        f"- **specialization:** {postulant.specialization}",
    ]
    if advisor_name:
        lines.append(f"- **advisor:** {advisor_name}")
    lines.extend(
        [
            "",
            "## System prompt addendum",
            "",
            postulant.system_prompt_addendum.strip(),
        ]
    )
    return "\n".join(lines).rstrip() + "\n"


def design_for(
    postulant: Genome, advisor_name: str | None = None
) -> list[curriculum.CurriculumItem]:
    """Generate, persist, and return the Postulant's curriculum items."""
    workspace = paths.CURRICULUM / postulant.id / "_orchestrator-workspace"
    workspace.mkdir(parents=True, exist_ok=True)
    _stage(workspace / "postulant.md", _render_postulant_brief(postulant, advisor_name))
    _stage(workspace / "archive-index.md", archive_index.render())

    console.print(
        f"[dim]Designing curriculum for {postulant.name}. This will take a minute or two...[/dim]"
    )
    result = claude_runner.invoke_orchestrator(
        brief=DESIGN_BRIEF,
        step=f"curriculum-design:{postulant.id}",
        model="claude-opus-4-7",
        cwd=workspace,
        extra_dirs=(paths.DOCS,),
        allowed_tools=("Read", "Glob", "Grep"),
    )
    payload = parsing.parse_json_or_dump(
        result.result_text,
        dump_path=workspace / "raw-design-output.txt",
        context=f"Curriculum design for {postulant.id}",
    )
    raw_items = payload.get("items")
    if not isinstance(raw_items, list) or not raw_items:
        raise RuntimeError(f"Curriculum design returned no items. Raw: {payload!r}")

    items = []
    seen_ids: set[str] = set()
    for raw in raw_items:
        if not isinstance(raw, dict):
            continue
        title = str(raw.get("title", "")).strip()
        layer = str(raw.get("layer", "")).strip().lower()
        if layer not in {"foundational", "specialization", "methodological"} or not title:
            continue
        item_id = str(raw.get("id", "")).strip().lower() or curriculum.slugify_item_id(layer, title)
        # Disambiguate collisions deterministically.
        original_id = item_id
        suffix = 2
        while item_id in seen_ids:
            item_id = f"{original_id}-{suffix}"
            suffix += 1
        seen_ids.add(item_id)
        items.append(
            curriculum.CurriculumItem(
                id=item_id,
                layer=layer,
                title=title,
                source=str(raw.get("source", "")).strip(),
                prompt=str(raw.get("prompt", "")).strip(),
            )
        )
    if not items:
        raise RuntimeError("Curriculum design produced no valid items after filtering.")

    from institute.safe_io import atomic_write

    curriculum.save_items(postulant.id, items)
    md_path = curriculum.curriculum_md_path(postulant.id)
    atomic_write(md_path, curriculum.render_markdown(items))

    now = datetime.now(UTC).isoformat(timespec="seconds")
    with db.connection() as conn, db.transaction(conn):
        conn.execute(
            "UPDATE fellows SET curriculum_designed_at = ? WHERE id = ?",
            (now, postulant.id),
        )
    return items


def _stage(path: Path, content: str) -> None:
    from institute.safe_io import atomic_write

    atomic_write(path, content)
