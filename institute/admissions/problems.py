"""Load the qualifying-problem set.

Problems live as markdown files in `institute/admissions/problems/`.
Each file's stem is the problem id (used in the candidate's response
filename), and the file's contents are the problem statement shown to
the candidate.
"""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

PROBLEMS_DIR = Path(__file__).parent / "problems"


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
