"""One-time backfill: re-ingest episodic-memory entries that failed
during the window when their `kind` was not in the whitelist.

Two failures appeared in the autopilot log:

  1. `ibn-al-haytham/publication` — for the BA-tokenizers paper
     `2026-05-19-tokens-or-positions-a-crossing-experimen-b8e3`, written
     before `publication` was an allowed kind.

  2. `<fellow>/reading_group` for ada-lovelace, adam-smith,
     charles-sanders-peirce, and ibn-al-haytham — the Pass-2
     cross-responses for the working-identity reading group session,
     written before `reading_group` was an allowed kind.

The artifacts are on disk. This script re-reads them and submits
through `episodic.safe_ingest` now that the kinds are whitelisted.
Idempotent: re-ingesting an existing memory creates a second row
(episodic.ingest doesn't dedup), so the script tracks what it has
done and refuses to re-run a backfill it has already completed.
"""

from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))

from institute import db, episodic, paths  # noqa: E402


def _already_backfilled(fellow_id: str, source_path: str) -> bool:
    with db.connection() as conn:
        row = conn.execute(
            "SELECT 1 FROM episodic_memory WHERE fellow_id = ? AND source_path = ? LIMIT 1",
            (fellow_id, source_path),
        ).fetchone()
    return row is not None


def main() -> int:
    n_backfilled = 0
    n_skipped = 0

    # 1. The BA-tokenizers publication.
    pub_id = "2026-05-19-tokens-or-positions-a-crossing-experimen-b8e3"
    pub_path = paths.PUBLICATIONS / f"{pub_id}.md"
    if pub_path.is_file():
        rel = str(pub_path.relative_to(paths.ROOT))
        if _already_backfilled("ibn-al-haytham", rel):
            print(f"skip: ibn-al-haytham/publication ({pub_id}) already in memory")
            n_skipped += 1
        else:
            body = pub_path.read_text(encoding="utf-8")
            # The publication file has YAML frontmatter; strip it for the
            # memory body to match how the publish workflow would have
            # ingested originally.
            if body.startswith("---"):
                end = body.find("\n---\n", 3)
                if end > 0:
                    body = body[end + 5 :]
            episodic.safe_ingest(
                fellow_id="ibn-al-haytham",
                kind="publication",
                title=(
                    "What the Pre-Flight Found: Tokenizer Probes, Power Tables, "
                    "and a Surface-Form Matcher Before the API Calls"
                ),
                content=body.strip(),
                source_path=rel,
                project_id=pub_id,
                metadata={"slug": pub_id, "role": "lead"},
            )
            print(f"OK:   ibn-al-haytham/publication ({pub_id})")
            n_backfilled += 1
    else:
        print(f"miss: publication file not found at {pub_path}", file=sys.stderr)

    # 2. The reading-group Pass-2 cross-responses.
    session_slug = "reading-group-on-anatomy-of-a-working-identity-why-the-sourl"
    session_dir = paths.READING_GROUPS / session_slug
    pass2_dir = session_dir / "pass2"
    title = (
        "Reading group: Reading group on `Anatomy of a Working Identity: Why "
        "the Sourlas Mapping Carried a Theorem Where RBM–RG Carried Only a "
        "Vocabulary`"
    )
    participants = (
        "ada-lovelace",
        "adam-smith",
        "charles-sanders-peirce",
        "ibn-al-haytham",
    )
    if not pass2_dir.is_dir():
        print(f"miss: reading-group pass2 dir not found at {pass2_dir}", file=sys.stderr)
    else:
        for fellow_id in participants:
            response_path = pass2_dir / f"{fellow_id}.md"
            if not response_path.is_file():
                print(f"miss: {fellow_id} pass2 file absent at {response_path}", file=sys.stderr)
                continue
            rel = str(response_path.relative_to(paths.ROOT))
            if _already_backfilled(fellow_id, rel):
                print(f"skip: {fellow_id}/reading_group already in memory")
                n_skipped += 1
                continue
            content = response_path.read_text(encoding="utf-8").strip()
            episodic.safe_ingest(
                fellow_id=fellow_id,
                kind="reading_group",
                title=title,
                content=content,
                source_path=rel,
                metadata={"slug": session_slug, "pass": 2},
            )
            print(f"OK:   {fellow_id}/reading_group ({session_slug})")
            n_backfilled += 1

    print()
    print(f"Backfilled {n_backfilled} entries; skipped {n_skipped} already in memory.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
