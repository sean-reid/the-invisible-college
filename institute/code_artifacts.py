"""Code and data artifacts: surface a Fellow's experiment files publicly.

A published paper that says "see the attached script" should mean it.
The Fellow's workspace under `fellows/<id>/workspace/<project>/` is
gitignored runtime state, so anything they write there stays private
unless someone deliberately copies it out.

This module is that copy step. After the research and revise workflows
finish, they call `sweep_workspace(...)` to pull every code-like or
data-like file from the workspace into a project-scoped artifact
directory under `archive/code/<project_id>/`. The publish workflow
then mirrors that directory into `blog/public/code/<project_id>/` so
the static blog can serve the files directly.

What is swept:
  - Files whose extension is in ALLOWED_EXTENSIONS (mostly source
    code and small data formats).
  - Files at most MAX_FILE_BYTES large. Larger files are skipped with
    a warning; they belong in external storage, not a public repo.
  - Per-project total capped at MAX_PROJECT_BYTES. Once the cap is
    reached the rest are skipped with a warning.

What is NOT swept:
  - Anything under hidden directories or `__pycache__`.
  - Files whose names start with `.` or `_` (treated as scratch).
  - Binary blobs, images, or compiled output (extensions are the
    filter).

Redaction: code/data files do not run through the prose redactor at
copy time because cost-pattern regexes are brittle against real
source. The integrity guard in [`institute.charter_integrity`] still
runs over the whole archive on every cycle, so any leaks are caught
at the institutional level.
"""

from __future__ import annotations

import shutil
from pathlib import Path

from rich.console import Console

from institute import paths

console = Console()


# Source-code and small-data formats the College considers worth
# surfacing alongside a paper. Anything not in this set is left in
# the workspace and not published.
ALLOWED_EXTENSIONS: set[str] = {
    ".py",
    ".ipynb",
    ".r",
    ".jl",
    ".m",
    ".go",
    ".rs",
    ".c",
    ".h",
    ".cpp",
    ".hpp",
    ".js",
    ".ts",
    ".tsx",
    ".jsx",
    ".sh",
    ".sql",
    ".csv",
    ".tsv",
    ".json",
    ".jsonl",
    ".yaml",
    ".yml",
    ".toml",
    ".txt",
}


# Figure formats the College surfaces alongside a paper. Images live
# in their own surface (`archive/figures/<id>/`) rather than mixed in
# with code — they are presentation outputs the publication inlines,
# not source you would re-run.
FIGURE_EXTENSIONS: set[str] = {
    ".png",
    ".jpg",
    ".jpeg",
    ".svg",
    ".gif",
    ".webp",
}


# Per-file size cap. Beyond this, the artifact is not for a public
# repo; it should live in external storage and be linked, not bundled.
MAX_FILE_BYTES: int = 256 * 1024  # 256 KB

# Per-project size cap across all artifacts.
MAX_PROJECT_BYTES: int = 2 * 1024 * 1024  # 2 MB


# Workspace directories that hold scratch, not Fellow artifacts.
_SCRATCH_DIRS: set[str] = {
    "__pycache__",
    ".pytest_cache",
    ".mypy_cache",
    ".ruff_cache",
    "node_modules",
    ".venv",
    "venv",
    ".git",
}


# Filenames the workflows stage into the workspace as inputs or pull
# out as outputs. These are not experimental artifacts and should not
# be republished alongside the post.
_WORKFLOW_FILES: set[str] = {
    "abstract.txt",
    "draft.md",
    "notebook.md",
    "memory.md",
    "proposal.md",
    "response-to-reviewers.md",
    "review.md",
    "archive-index.md",
    "open-problems.md",
    "research-agenda.md",
    "cohort.md",
    "candidates.md",
    "decision.json",
    "follow-up-questions.md",
    "raw-research-output.txt",
}


def _is_scratch(path: Path) -> bool:
    """True if the path is somewhere we should never copy from."""
    for part in path.parts:
        if part in _SCRATCH_DIRS:
            return True
        if part.startswith(".") and part not in (".",):
            return True
        if part.startswith("_") and path.name == part:
            # Underscore-prefixed file names are treated as scratch
            # (e.g. _tmp.py, _scratch.py). Underscore-prefixed
            # directory names get caught by the recursion check.
            return True
    return False


def _eligible_files(workspace: Path) -> list[Path]:
    """All files in the workspace that should be considered for copy."""
    if not workspace.is_dir():
        return []
    out: list[Path] = []
    for path in sorted(workspace.rglob("*")):
        if not path.is_file():
            continue
        rel = path.relative_to(workspace)
        if _is_scratch(rel):
            continue
        if path.name in _WORKFLOW_FILES:
            continue
        if path.suffix.lower() not in ALLOWED_EXTENSIONS:
            continue
        out.append(path)
    return out


def sweep_workspace(*, workspace: Path, project_id: str) -> list[Path]:
    """Copy all eligible artifacts from `workspace` to archive/code/<project_id>/.

    Idempotent: re-running replaces previous copies with the current
    versions, so a revise step that produces an updated script
    overwrites the original. File names are flattened: nested workspace
    paths become flattened names with `--` as the separator. This keeps
    the public surface a flat directory the blog can list cleanly.

    Returns the list of destination paths actually written.
    """
    target_dir = paths.CODE / project_id
    written: list[Path] = []
    total = 0

    eligible = _eligible_files(workspace)
    if not eligible:
        return []

    target_dir.mkdir(parents=True, exist_ok=True)

    for src in eligible:
        try:
            size = src.stat().st_size
        except OSError:
            continue
        if size > MAX_FILE_BYTES:
            console.print(
                f"[yellow]Skipping {src.name}: {size} bytes exceeds "
                f"per-file cap of {MAX_FILE_BYTES} bytes.[/yellow]"
            )
            continue
        if total + size > MAX_PROJECT_BYTES:
            console.print(
                f"[yellow]Project artifact budget exhausted; skipping {src.name}.[/yellow]"
            )
            continue

        rel = src.relative_to(workspace)
        # Flatten nested paths into a single filename so the published
        # directory is a flat listing.
        flat_name = "--".join(rel.parts)
        dest = target_dir / flat_name
        shutil.copy2(src, dest)
        written.append(dest)
        total += size

    return written


def mirror_to_blog(project_id: str) -> list[Path]:
    """Copy archive/code/<project_id>/ into blog/public/code/<project_id>/.

    Called from the publish workflow so the static blog can serve every
    artifact alongside its post. Returns the destination paths.
    """
    src_dir = paths.CODE / project_id
    if not src_dir.is_dir():
        return []
    dest_dir = paths.BLOG_CODE / project_id
    if dest_dir.exists():
        shutil.rmtree(dest_dir)
    dest_dir.mkdir(parents=True, exist_ok=True)

    written: list[Path] = []
    for src in sorted(src_dir.iterdir()):
        if not src.is_file():
            continue
        dest = dest_dir / src.name
        shutil.copy2(src, dest)
        written.append(dest)
    return written


def list_for_project(project_id: str) -> list[Path]:
    """Return the artifacts currently in archive/code/<project_id>/."""
    target_dir = paths.CODE / project_id
    if not target_dir.is_dir():
        return []
    return sorted(p for p in target_dir.iterdir() if p.is_file())


# Per-file size cap for figures. Higher than the code cap because a
# scientific scatter or residuals plot can legitimately approach 1MB
# when rendered at decent resolution. Anything beyond is a sign the
# Fellow should have downscaled or used SVG.
MAX_FIGURE_BYTES: int = 1 * 1024 * 1024


def _eligible_figures(workspace: Path) -> list[Path]:
    """Iterate workspace files that are figure-extensioned and not scratch."""
    if not workspace.is_dir():
        return []
    out: list[Path] = []
    for path in sorted(workspace.rglob("*")):
        if not path.is_file():
            continue
        rel = path.relative_to(workspace)
        if _is_scratch(rel):
            continue
        if path.name in _WORKFLOW_FILES:
            continue
        if path.suffix.lower() not in FIGURE_EXTENSIONS:
            continue
        out.append(path)
    return out


def sweep_figures(*, workspace: Path, project_id: str) -> list[Path]:
    """Copy all figure-extensioned files from `workspace` to archive/figures/<project_id>/.

    Parallel to `sweep_workspace`, but writes to a separate surface
    because figures are presentation artifacts the publication
    inlines, not source code a reader would re-run. The destination
    is flat: nested workspace paths flatten to `--`-joined names.
    """
    target_dir = paths.FIGURES / project_id
    written: list[Path] = []

    eligible = _eligible_figures(workspace)
    if not eligible:
        return []

    target_dir.mkdir(parents=True, exist_ok=True)
    for src in eligible:
        try:
            size = src.stat().st_size
        except OSError:
            continue
        if size > MAX_FIGURE_BYTES:
            console.print(
                f"[yellow]Skipping figure {src.name}: {size} bytes exceeds "
                f"per-file cap of {MAX_FIGURE_BYTES} bytes.[/yellow]"
            )
            continue
        rel = src.relative_to(workspace)
        flat_name = "--".join(rel.parts)
        dest = target_dir / flat_name
        shutil.copy2(src, dest)
        written.append(dest)
    return written


def mirror_figures_to_blog(project_id: str) -> list[Path]:
    """Copy archive/figures/<project_id>/ into blog/public/figures/<project_id>/.

    Called from the publish workflow so the static blog can serve every
    figure the published markdown body references. Returns the
    destination paths.
    """
    src_dir = paths.FIGURES / project_id
    if not src_dir.is_dir():
        return []
    dest_dir = paths.BLOG_FIGURES / project_id
    if dest_dir.exists():
        shutil.rmtree(dest_dir)
    dest_dir.mkdir(parents=True, exist_ok=True)
    written: list[Path] = []
    for src in sorted(src_dir.iterdir()):
        if not src.is_file():
            continue
        dest = dest_dir / src.name
        shutil.copy2(src, dest)
        written.append(dest)
    return written


def figures_for_project(project_id: str) -> list[Path]:
    """Return the figure files currently in archive/figures/<project_id>/."""
    target_dir = paths.FIGURES / project_id
    if not target_dir.is_dir():
        return []
    return sorted(p for p in target_dir.iterdir() if p.is_file())


__all__ = [
    "ALLOWED_EXTENSIONS",
    "FIGURE_EXTENSIONS",
    "MAX_FIGURE_BYTES",
    "MAX_FILE_BYTES",
    "MAX_PROJECT_BYTES",
    "figures_for_project",
    "list_for_project",
    "mirror_figures_to_blog",
    "mirror_to_blog",
    "sweep_figures",
    "sweep_workspace",
]
