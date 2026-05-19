"""Per-invocation Fellow workspaces.

Workflows that produce long-form prose use file-based output instead of
JSON: the Fellow writes `draft.md`, `notebook.md`, etc. to a workspace
the orchestrator has staged with the relevant inputs. This module owns
the layout and the helpers for staging inputs and reading outputs.

Layout:
    fellows/<fellow-id>/workspace/<scope>/
        <input files placed by the orchestrator>
        <output files written by the Fellow>

A scope is a project-id, sometimes suffixed by step (e.g.
"<project>-review-r2", "<project>-revise-v1"). Each scope is its own
directory so different calls do not stomp on each other and we can
inspect what each Fellow produced.
"""

from __future__ import annotations

from pathlib import Path

from institute.paths import FELLOWS


def workspace_for(fellow_id: str, scope: str) -> Path:
    """Return the workspace path for `(fellow, scope)`. Creates it if missing."""
    path = FELLOWS / fellow_id / "workspace" / scope
    path.mkdir(parents=True, exist_ok=True)
    return path


def stage_input(workspace: Path, filename: str, content: str) -> Path:
    """Write `content` to `workspace/filename`. Atomic. Returns the path."""
    path = workspace / filename
    tmp = path.with_suffix(path.suffix + ".tmp")
    tmp.write_text(content, encoding="utf-8")
    tmp.replace(path)
    return path


def require_output(workspace: Path, filename: str, *, min_chars: int = 1) -> str:
    """Read `workspace/filename`. Raise if missing or shorter than `min_chars`."""
    path = workspace / filename
    if not path.is_file():
        raise RuntimeError(
            f"Fellow did not produce expected output file `{filename}` in workspace `{workspace}`."
        )
    text = path.read_text(encoding="utf-8").strip()
    if len(text) < min_chars:
        raise RuntimeError(
            f"Output file `{filename}` is shorter than {min_chars} chars "
            f"({len(text)} chars). Workspace: {workspace}."
        )
    return text


def optional_output(workspace: Path, filename: str) -> str | None:
    """Read `workspace/filename`, return None if missing or empty."""
    path = workspace / filename
    if not path.is_file():
        return None
    text = path.read_text(encoding="utf-8").strip()
    return text or None


def clear_outputs(workspace: Path, filenames: tuple[str, ...]) -> None:
    """Unlink any of the named output files that exist in `workspace`.

    Each Fellow invocation can run more than once for the same step (a
    parse error on the previous run, a retry by the operator). Without
    clearing the prior outputs, a Claude call that fails to re-write
    every expected file would let `require_output` silently return the
    stale content. Call this at the top of each workflow that uses
    require_output, before invoking the runner.
    """
    for name in filenames:
        path = workspace / name
        if path.is_file():
            path.unlink()
