"""Wraps the `claude` CLI in headless mode.

Every Fellow invocation in the College flows through this module. Other
modules construct a task brief and a (fellow, project, step) tuple; this
module turns that into a subprocess call to `claude -p` with the right
flags, captures the structured JSON result, and writes a copy of the raw
output to the audit log.

Pause/resume across Mac sleep is handled at the orchestrator level: state
lives in SQLite and in markdown files under archive/. Each `claude -p`
invocation is one-shot with a fresh session id. Long-running work like
research happens in multiple separate invocations that read prior
artifacts (lab notebooks, drafts) from the workspace rather than relying
on Claude Code session continuity.
"""

from __future__ import annotations

import json
import shutil
import subprocess
import uuid
from dataclasses import dataclass
from datetime import UTC, datetime
from pathlib import Path

from institute import charter
from institute.fellow import Genome, ensure_fellow_dirs, workspace_path
from institute.paths import AUDIT_LOG


@dataclass(frozen=True)
class FellowTask:
    """Everything claude_runner needs to invoke a Fellow once."""

    genome: Genome
    project_id: str
    step: str  # e.g. "propose", "research", "peer_review:primary"
    brief: str  # the actual task prompt the Fellow sees
    extra_dirs: tuple[Path, ...] = ()
    # If set, overrides the default workspace (fellows/<id>/workspace).
    # Workflows that produce file-based output set this to a project- and
    # step-scoped directory they have already staged with any input files.
    workspace: Path | None = None


@dataclass(frozen=True)
class FellowResult:
    session_id: str
    result_text: str
    raw: dict
    duration_ms: int | None
    cost_usd: float | None
    is_error: bool


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


def invoke_orchestrator(
    *,
    brief: str,
    step: str,
    model: str = "claude-opus-4-7",
    cwd: Path | None = None,
    json_schema: dict | None = None,
    extra_dirs: tuple[Path, ...] = (),
    allowed_tools: tuple[str, ...] = ("Read", "WebSearch", "WebFetch"),
) -> FellowResult:
    """Invoke Claude as the orchestrator itself, not as any Fellow.

    Used for institution-level meta-tasks where no Fellow exists yet or where
    the work is structural (bootstrap, admissions design, etc.). The Charter
    is still passed as context. The persona is "the orchestrator," not a
    Fellow with a genome.
    """
    from institute.paths import ROOT  # local to avoid import cycle

    actual_cwd = cwd if cwd is not None else ROOT
    # Orchestrator calls are one-shot and not meant to be resumed across
    # invocations. A fresh UUID per call avoids "session already in use"
    # errors from prior aborted runs.
    session_id = str(uuid.uuid4())

    system_prompt = (
        charter.header()
        + charter.load()
        + "\n\n## YOUR ROLE\n\n"
        + "You are the orchestrator of the Invisible College, running outside of "
        + "any Fellow's session. Your job is institution-level work: structural "
        + "decisions, bootstrap, design of admissions materials, and similar "
        + "meta-tasks. You are not a Fellow and have no specialization."
    )

    cmd: list[str] = [
        _claude_executable(),
        "-p",
        brief,
        "--session-id",
        session_id,
        "--append-system-prompt",
        system_prompt,
        "--model",
        model,
        "--allowed-tools",
        ",".join(allowed_tools),
        "--permission-mode",
        "bypassPermissions",
        "--output-format",
        "json",
    ]
    if json_schema is not None:
        cmd.extend(["--json-schema", json.dumps(json_schema)])
    for extra in extra_dirs:
        cmd.extend(["--add-dir", str(extra)])

    proc = subprocess.run(
        cmd,
        cwd=actual_cwd,
        capture_output=True,
        text=True,
        check=False,
    )

    raw_text = proc.stdout.strip()
    try:
        raw = json.loads(raw_text) if raw_text else {}
    except json.JSONDecodeError as exc:
        raise RuntimeError(
            f"claude (orchestrator) returned non-JSON output. stderr: {proc.stderr.strip()[:500]}"
        ) from exc

    result_text = raw.get("result", "") if isinstance(raw, dict) else ""
    is_error = bool(raw.get("is_error", False)) if isinstance(raw, dict) else True

    # Reuse the same audit log structure with a synthetic FellowTask-shaped record.
    entry = {
        "ts": datetime.now(UTC).isoformat(timespec="seconds"),
        "fellow_id": "orchestrator",
        "project_id": "meta",
        "step": step,
        "session_id": session_id,
        "returncode": proc.returncode,
        "duration_ms": raw.get("duration_ms") if isinstance(raw, dict) else None,
        "cost_usd": raw.get("total_cost_usd") if isinstance(raw, dict) else None,
        "is_error": raw.get("is_error") if isinstance(raw, dict) else None,
        "stderr_excerpt": proc.stderr.strip()[:300] if proc.stderr else "",
    }
    AUDIT_LOG.parent.mkdir(parents=True, exist_ok=True)
    with AUDIT_LOG.open("a", encoding="utf-8") as fh:
        fh.write(json.dumps(entry) + "\n")

    if proc.returncode != 0 or is_error:
        raise RuntimeError(
            f"Orchestrator call failed (step={step}): "
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


def invoke(task: FellowTask) -> FellowResult:
    """Run a Fellow task as a `claude -p` subprocess. Blocking.

    Each call uses a fresh session id. Continuity across invocations is
    achieved via files in the Fellow's workspace and via the lab notebook,
    not via Claude Code session reuse.
    """

    ensure_fellow_dirs(task.genome.id)
    cwd = task.workspace if task.workspace is not None else workspace_path(task.genome.id)
    cwd.mkdir(parents=True, exist_ok=True)
    session_id = str(uuid.uuid4())

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
        "ts": datetime.now(UTC).isoformat(timespec="seconds"),
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
