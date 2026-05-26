"""Classify ``git status`` entries into operator edits vs fellow output.

The daemon wakes, does a Fellow cycle, and then needs to decide which files
on disk are safe to auto-commit. The rule is:

  * Anything under a *fellow path* (``archive/``, ``blog/src/content/``,
    ``fellows/``, ``genomes/``) is daemon output unless it was already
    modified in the working tree before the cycle started.
  * Anything else (``docs/``, ``institute/``, ``tests/``, ``scripts/``,
    top-level dotfiles, etc.) is an operator edit and must never be
    committed by the autopilot.
  * Anything we cannot classify (a brand-new top-level directory the
    operator created, say) is flagged ``unknown`` so the caller can
    decide.

This module owns the path rules so the CLI command and any future
consumer (autopilot pre-flight checks, audit reports) share one source of
truth. ``git status --porcelain=v1 -z`` is used everywhere instead of
the default newline-terminated format: NUL separation removes the
filename-with-spaces / filename-with-newline footgun the previous awk
pipeline tripped over.
"""

from __future__ import annotations

import subprocess
from dataclasses import dataclass, field
from pathlib import Path

# Path prefixes that the Fellows write to. Anything matching one of these
# (interpreted as a path component prefix, not a substring) is fellow
# output. Order does not matter; the longest match is not required
# because these are disjoint.
FELLOW_PREFIXES: tuple[str, ...] = (
    "archive/",
    "blog/public/code/",
    "blog/public/figures/",
    "blog/src/content/",
    "fellows/",
    "genomes/",
)

# Path prefixes the operator owns. The daemon must never stage these
# even if they happen to be modified during a Fellow cycle (e.g. the
# operator was editing a doc while the daemon woke).
OPERATOR_PREFIXES: tuple[str, ...] = (
    ".github/",
    "blog/public/",
    "blog/src/components/",
    "blog/src/layouts/",
    "blog/src/pages/",
    "blog/src/styles/",
    "docs/",
    "institute/",
    "scripts/",
    "tests/",
)

# Top-level files (no slash in the path) that are always operator-owned.
OPERATOR_TOPLEVEL_FILES: frozenset[str] = frozenset(
    {
        ".env.example",
        ".gitignore",
        ".python-version",
        "CODE_OF_CONDUCT.md",
        "CONTRIBUTING.md",
        "LICENSE",
        "Makefile",
        "README.md",
        "SECURITY.md",
        "pyproject.toml",
        "uv.lock",
    }
)


@dataclass(frozen=True)
class Classification:
    """Result of classifying a porcelain status snapshot."""

    operator_edits: list[str] = field(default_factory=list)
    fellow_outputs: list[str] = field(default_factory=list)
    unknown: list[str] = field(default_factory=list)

    def as_dict(self) -> dict[str, list[str]]:
        return {
            "operator_edits": sorted(self.operator_edits),
            "fellow_outputs": sorted(self.fellow_outputs),
            "unknown": sorted(self.unknown),
        }


def classify_path(path: str) -> str:
    """Return one of ``"fellow"``, ``"operator"``, ``"unknown"``.

    Pure function over a forward-slash repo-relative path string. Splitting
    out from ``classify_from_porcelain`` so other callers (an audit tool,
    a pre-commit hook) can reuse the rules without parsing porcelain.
    """
    # Normalize: git porcelain always uses forward slashes, but be
    # defensive in case a Windows path slips in via a test fixture.
    normalized = path.replace("\\", "/").lstrip("./")

    for prefix in FELLOW_PREFIXES:
        if normalized.startswith(prefix):
            return "fellow"

    for prefix in OPERATOR_PREFIXES:
        if normalized.startswith(prefix):
            return "operator"

    if "/" not in normalized and normalized in OPERATOR_TOPLEVEL_FILES:
        return "operator"

    return "unknown"


def parse_porcelain_z(data: bytes) -> list[str]:
    """Parse ``git status --porcelain=v1 -z`` output into repo-relative paths.

    Porcelain v1 -z format, per ``git-status(1)``:

      XY SP <path> NUL [<origPath> NUL]

    where ``XY`` is the two-character status code, ``SP`` is a single
    space, and ``<origPath>`` only appears for rename/copy entries (status
    codes ``R`` or ``C``). Each record is NUL-terminated rather than
    newline-terminated so paths may contain spaces, tabs, or newlines.
    """
    paths: list[str] = []
    # ``-z`` output: split on NUL, but rename/copy entries consume TWO
    # NUL-terminated fields (the destination and the source). Walk a
    # cursor instead of relying on a fixed stride.
    tokens = data.split(b"\x00")
    # Trailing empty token from final NUL; drop it.
    if tokens and tokens[-1] == b"":
        tokens.pop()

    i = 0
    while i < len(tokens):
        entry = tokens[i]
        # Entries are ``XY <path>``; minimum length 4 (e.g. ``" M f"``).
        if len(entry) < 4 or entry[2:3] != b" ":
            # Malformed token; skip defensively.
            i += 1
            continue
        status = entry[:2]
        path = entry[3:].decode("utf-8", errors="surrogateescape")
        paths.append(path)
        # Rename (``R``) and copy (``C``) entries have a second token
        # that is the original path. For classification we only care
        # about the *destination*, so we skip the source token.
        if status[:1] in (b"R", b"C"):
            i += 2
        else:
            i += 1
    return paths


def classify_from_porcelain(data: bytes) -> Classification:
    """Classify the contents of a ``git status --porcelain=v1 -z`` snapshot."""
    operator: list[str] = []
    fellow: list[str] = []
    unknown: list[str] = []

    for path in parse_porcelain_z(data):
        bucket = classify_path(path)
        if bucket == "fellow":
            fellow.append(path)
        elif bucket == "operator":
            operator.append(path)
        else:
            unknown.append(path)

    return Classification(
        operator_edits=operator,
        fellow_outputs=fellow,
        unknown=unknown,
    )


def run_git_status(repo: Path) -> bytes:
    """Run ``git status --porcelain=v1 -z -uall`` and return its raw bytes.

    ``-uall`` (a.k.a. ``--untracked-files=all``) is essential: the
    default ``normal`` mode collapses an untracked directory to just
    its top-level name (``archive/``), which would classify as
    ``unknown`` instead of pulling in each individual fellow output.
    """
    result = subprocess.run(
        ["git", "-C", str(repo), "status", "--porcelain=v1", "-z", "-uall"],
        check=True,
        capture_output=True,
    )
    return result.stdout


def classify_repo(repo: Path) -> Classification:
    """Run ``git status`` against ``repo`` and classify the result."""
    return classify_from_porcelain(run_git_status(repo))
