"""Wraps the `claude` CLI in headless mode.

Every Fellow invocation in the College flows through this module. Other
modules construct a task brief and a (fellow, project, step) tuple; this
module turns that into a subprocess call to `claude -p` with the right
flags, captures the structured JSON result, and writes a copy of the raw
output to the audit log.

A deterministic session id derived from (fellow_id, project_id, step) lets
Claude Code resume the same conversation across separate invocations. This
is how a research session can be paused and continued later.
"""

from __future__ import annotations

import json
import shutil
import subprocess
import uuid
from dataclasses import dataclass
from pathlib import Path
from typing import Literal

from institute import charter
from institute.fellow import Genome, ensure_fellow_dirs, workspace_path
from institute.paths import AUDIT_LOG

# Stable namespace so session ids are reproducible across machines/runs.
SESSION_NAMESPACE = uuid.UUID("3d4f0a4e-9f0e-4e8a-9b6a-1e6d5c0c0f30")


@dataclass(frozen=True)
class FellowTask:
    """Everything claude_runner needs to invoke a Fellow once."""

    genome: Genome
    project_id: str
    step: str  # e.g. "propose", "research", "peer_review:primary"
    brief: str  # the actual task prompt the Fellow sees
    extra_dirs: tuple[Path, ...] = ()


@dataclass(frozen=True)
class FellowResult:
    session_id: str
    result_text: str
    raw: dict
    duration_ms: int | None
    cost_usd: float | None
    is_error: bool


def session_id_for(fellow_id: str, project_id: str, step: str) -> str:
    name = f"{fellow_id}|{project_id}|{step}"
    return str(uuid.uuid5(SESSION_NAMESPACE, name))


def _claude_executable() -> str:
    path = shutil.which("claude")
    if path is None:
        raise RuntimeError("The `claude` CLI is not on PATH. Install Claude Code first.")
    return path


def _system_prompt_for(genome: Genome) -> str:
    return (
        charter.header()
        + charter.load()
        + "\n\n## YOUR PERSONA AS A FELLOW\n\n"
        + f"You are {genome.name} ({genome.id}), a Fellow of the College at rank "
        + f"{genome.rank}, specializing in {genome.specialization}.\n\n"
        + genome.system_prompt_addendum.strip()
        + "\n"
    )


def invoke(task: FellowTask, resume: Literal["auto", "never"] = "auto") -> FellowResult:
    """Run a Fellow task as a `claude -p` subprocess. Blocking."""

    ensure_fellow_dirs(task.genome.id)
    cwd = workspace_path(task.genome.id)
    session_id = session_id_for(task.genome.id, task.project_id, task.step)

    cmd: list[str] = [
        _claude_executable(),
        "-p",
        task.brief,
        "--session-id",
        session_id,
        "--append-system-prompt",
        _system_prompt_for(task.genome),
        "--model",
        task.genome.model,
        "--allowed-tools",
        ",".join(task.genome.allowed_tools),
        "--permission-mode",
        "bypassPermissions",
        "--output-format",
        "json",
    ]
    if resume == "auto":
        # If the session already exists, --session-id resumes it transparently.
        # No additional flag needed; claude treats reuse of an existing id as resume.
        pass

    for extra in task.extra_dirs:
        cmd.extend(["--add-dir", str(extra)])

    proc = subprocess.run(
        cmd,
        cwd=cwd,
        capture_output=True,
        text=True,
        check=False,
    )

    raw_text = proc.stdout.strip()
    try:
        raw = json.loads(raw_text) if raw_text else {}
    except json.JSONDecodeError as exc:
        raise RuntimeError(
            f"claude returned non-JSON output. stderr: {proc.stderr.strip()[:500]}"
        ) from exc

    result_text = raw.get("result", "") if isinstance(raw, dict) else ""
    is_error = bool(raw.get("is_error", False)) if isinstance(raw, dict) else True

    _audit(task, session_id, raw, proc.returncode, proc.stderr)

    if proc.returncode != 0 or is_error:
        raise RuntimeError(
            f"Fellow {task.genome.id} failed step {task.step}: "
            f"returncode={proc.returncode}, is_error={is_error}, "
            f"stderr={proc.stderr.strip()[:500]}"
        )

    return FellowResult(
        session_id=session_id,
        result_text=result_text,
        raw=raw,
        duration_ms=raw.get("duration_ms") if isinstance(raw, dict) else None,
        cost_usd=raw.get("total_cost_usd") if isinstance(raw, dict) else None,
        is_error=is_error,
    )


def _audit(
    task: FellowTask,
    session_id: str,
    raw: dict,
    returncode: int,
    stderr: str,
) -> None:
    entry = {
        "ts": __import__("datetime")
        .datetime.now(__import__("datetime").timezone.utc)
        .isoformat(timespec="seconds"),
        "fellow_id": task.genome.id,
        "project_id": task.project_id,
        "step": task.step,
        "session_id": session_id,
        "returncode": returncode,
        "duration_ms": raw.get("duration_ms") if isinstance(raw, dict) else None,
        "cost_usd": raw.get("total_cost_usd") if isinstance(raw, dict) else None,
        "is_error": raw.get("is_error") if isinstance(raw, dict) else None,
        "stderr_excerpt": stderr.strip()[:300] if stderr else "",
    }
    AUDIT_LOG.parent.mkdir(parents=True, exist_ok=True)
    with AUDIT_LOG.open("a", encoding="utf-8") as fh:
        fh.write(json.dumps(entry) + "\n")
