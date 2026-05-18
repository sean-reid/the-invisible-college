"""Reading curriculum for newly admitted Postulants.

Chapter 5 of the design specifies a three-layer curriculum staged for
each Postulant on entry:

  - Foundational: common to all Postulants. Charter + exemplary past
    publications + a few external classics.
  - Specialization: advisor-curated, the current state of work in the
    Postulant's declared specialization.
  - Methodological: depends on the kind of work the Postulant intends
    to do (review, building, synthesis, essay).

The orchestrator generates the curriculum during admissions. Each item
gets a stable id; the Postulant writes a response per item; the
Archive (and the DB) tracks which items have been responded to.

Layout on disk:

    archive/curriculum/<postulant-id>/
        curriculum.md           the curriculum, generated once
        items.json              structured list (id, layer, title, source, prompt)
        responses/
            <item-id>.md        the Postulant's written response
"""

from __future__ import annotations

import json
import re
import sqlite3
from dataclasses import dataclass
from pathlib import Path

from institute import paths


@dataclass(frozen=True)
class CurriculumItem:
    id: str
    layer: str  # "foundational" | "specialization" | "methodological"
    title: str
    source: str  # path or URL or descriptive reference
    prompt: str  # what to do with the item: critique, summarize, apply, extend


def curriculum_dir(fellow_id: str) -> Path:
    return paths.CURRICULUM / fellow_id


def items_path(fellow_id: str) -> Path:
    return curriculum_dir(fellow_id) / "items.json"


def curriculum_md_path(fellow_id: str) -> Path:
    return curriculum_dir(fellow_id) / "curriculum.md"


def responses_dir(fellow_id: str) -> Path:
    return curriculum_dir(fellow_id) / "responses"


def response_path(fellow_id: str, item_id: str) -> Path:
    return responses_dir(fellow_id) / f"{item_id}.md"


def load_items(fellow_id: str) -> list[CurriculumItem]:
    path = items_path(fellow_id)
    if not path.is_file():
        return []
    raw = json.loads(path.read_text(encoding="utf-8"))
    return [CurriculumItem(**item) for item in raw]


def save_items(fellow_id: str, items: list[CurriculumItem]) -> Path:
    curriculum_dir(fellow_id).mkdir(parents=True, exist_ok=True)
    payload = [
        {
            "id": item.id,
            "layer": item.layer,
            "title": item.title,
            "source": item.source,
            "prompt": item.prompt,
        }
        for item in items
    ]
    path = items_path(fellow_id)
    tmp = path.with_suffix(path.suffix + ".tmp")
    tmp.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")
    tmp.replace(path)
    return path


def completed_item_ids(conn: sqlite3.Connection, fellow_id: str) -> set[str]:
    return {
        r["item_id"]
        for r in conn.execute(
            "SELECT item_id FROM curriculum_responses WHERE fellow_id = ?",
            (fellow_id,),
        )
    }


def next_pending_item(conn: sqlite3.Connection, fellow_id: str) -> CurriculumItem | None:
    """Return the first item the Postulant has not yet responded to, or None."""
    items = load_items(fellow_id)
    if not items:
        return None
    done = completed_item_ids(conn, fellow_id)
    for item in items:
        if item.id not in done:
            return item
    return None


def render_markdown(items: list[CurriculumItem]) -> str:
    """Render the curriculum as a single markdown document for the Postulant."""
    if not items:
        return "# Reading curriculum\n\n(No items.)\n"
    lines = [
        "# Reading curriculum",
        "",
        "Per Chapter 5 of the design. Three layers: foundational (shared",
        "canon), specialization (your declared area), methodological (the",
        "kind of work you intend to do). Engage each item with a written",
        "response, not passive consumption.",
        "",
    ]
    by_layer: dict[str, list[CurriculumItem]] = {
        "foundational": [],
        "specialization": [],
        "methodological": [],
    }
    for item in items:
        by_layer.setdefault(item.layer, []).append(item)
    for layer in ("foundational", "specialization", "methodological"):
        bucket = by_layer.get(layer, [])
        if not bucket:
            continue
        lines.append(f"## {layer.capitalize()}")
        lines.append("")
        for item in bucket:
            lines.append(f"### {item.title}  `{item.id}`")
            lines.append("")
            lines.append(f"- **Source:** {item.source}")
            lines.append(f"- **Prompt:** {item.prompt}")
            lines.append("")
    return "\n".join(lines).rstrip() + "\n"


_ID_SAFE_RE = re.compile(r"[^a-z0-9-]+")


def slugify_item_id(layer: str, title: str) -> str:
    base = title.lower()
    base = _ID_SAFE_RE.sub("-", base).strip("-")
    if not base:
        base = "item"
    return f"{layer[:4]}-{base[:50]}"
