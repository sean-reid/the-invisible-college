"""One-time migration: shard archive/open-problems/ by source project.

Open problems used to live in a flat directory at
`archive/open-problems/<slug>.md`. With the College now writing follow-
up questions from every reviewer of every paper, the slug namespace
grew to the point where a 60-char-truncated slug from paper A could
collide with a meaningfully different slug from paper B. This
migration moves each file into a per-publication subdir so the
namespace shards per paper:

    archive/open-problems/<source_project_id>/<slug>.md

Problems with no `source_project_id` in their frontmatter (founder- or
fellow-authored standing questions) go under the sentinel subdir
`standing/`.

Idempotent: files already inside a subdir are left alone.

Run once:
    uv run python scripts/migrations/2026-05-20-shard-open-problems.py
"""

from __future__ import annotations

import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))

from institute import paths  # noqa: E402
from institute.open_problems import STANDING  # noqa: E402

_FRONTMATTER_RE = re.compile(r"\A---\n(.*?)\n---\n", re.DOTALL)
_SOURCE_RE = re.compile(r"^source_project_id:\s*(.+?)\s*$", re.MULTILINE)


def _read_source_project_id(path: Path) -> str:
    text = path.read_text(encoding="utf-8")
    m = _FRONTMATTER_RE.match(text)
    if not m:
        return STANDING
    front = m.group(1)
    match = _SOURCE_RE.search(front)
    if match is None:
        return STANDING
    value = match.group(1).strip()
    return value or STANDING


def main() -> int:
    base = paths.OPEN_PROBLEMS
    if not base.is_dir():
        print(f"No open-problems directory at {base}; nothing to do.")
        return 0

    moved = 0
    skipped_already = 0
    by_project: dict[str, int] = {}
    for entry in sorted(base.iterdir()):
        if entry.is_dir():
            # Already in a subdir, presumably from a prior partial run.
            skipped_already += 1
            continue
        if entry.suffix != ".md":
            continue
        if entry.name == "INDEX.md":
            continue

        project_id = _read_source_project_id(entry)
        dest_dir = base / project_id
        dest_dir.mkdir(parents=True, exist_ok=True)
        dest_path = dest_dir / entry.name
        if dest_path.exists():
            print(
                f"REFUSING to overwrite existing {dest_path.relative_to(ROOT)}; "
                f"skipping source {entry.relative_to(ROOT)}.",
                file=sys.stderr,
            )
            return 1
        entry.rename(dest_path)
        moved += 1
        by_project[project_id] = by_project.get(project_id, 0) + 1

    print(f"Moved {moved} file(s); already-sharded subdirs: {skipped_already}.")
    if by_project:
        print("Per-project counts:")
        for pid in sorted(by_project):
            print(f"  {pid}: {by_project[pid]}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
