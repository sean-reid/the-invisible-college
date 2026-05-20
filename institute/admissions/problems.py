"""Load the qualifying-problem set.

Problems live as markdown files in `institute/admissions/problems/`.
Each file's stem is the problem id (used in the candidate's response
filename), and the file's contents are the problem statement shown to
the candidate.

Per Chapter 4, problems are *rotated* across candidates to prevent
overfitting on the same five questions. `for_candidate` returns a
deterministic subset of `PROBLEMS_PER_CANDIDATE` problems chosen by
hashing the candidate id — the same id always gets the same subset,
but two candidates in the same cohort see different problems.
"""

from __future__ import annotations

import hashlib
from dataclasses import dataclass
from pathlib import Path

PROBLEMS_DIR = Path(__file__).parent / "problems"

# Each candidate sees this many problems. With five problems in the
# pool, that yields C(5,3) = 10 distinct combinations, enough to
# vary across a typical cohort while keeping the load per candidate
# comparable to the prior 3-problem flow.
PROBLEMS_PER_CANDIDATE = 3


@dataclass(frozen=True)
class Problem:
    id: str  # filename stem, e.g. "01-critique"
    text: str  # full markdown contents


def load_problems() -> list[Problem]:
    """Return every qualifying problem, in sorted order by filename."""
    return [
        Problem(id=path.stem, text=path.read_text(encoding="utf-8").rstrip() + "\n")
        for path in sorted(PROBLEMS_DIR.glob("*.md"))
    ]


def for_candidate(candidate_id: str, *, count: int | None = None) -> list[Problem]:
    """Return the rotated problem subset for a single candidate.

    `count` defaults to PROBLEMS_PER_CANDIDATE; setting it higher than
    the pool clamps to the pool size. Deterministic per candidate id.
    """
    pool = load_problems()
    if not pool:
        return []
    if count is None:
        count = PROBLEMS_PER_CANDIDATE
    count = min(count, len(pool))

    # Stable, deterministic rotation: hash the candidate id to a 32-bit
    # int, use it as an offset into a stably-ordered pool, take `count`
    # entries with wrap. Different ids produce different offsets, so
    # two candidates in the same cohort rarely see the same problems.
    digest = hashlib.sha256(candidate_id.encode("utf-8")).digest()
    offset = int.from_bytes(digest[:4], "big") % len(pool)
    rotated = pool[offset:] + pool[:offset]
    return rotated[:count]
