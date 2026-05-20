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
import os
import shutil
import signal
import subprocess
import uuid
from dataclasses import dataclass
from datetime import UTC, datetime
from pathlib import Path

from institute import charter, runtime
from institute.fellow import Genome, ensure_fellow_dirs, workspace_path
from institute.paths import AUDIT_LOG

# Wall-clock timeout for a single Fellow invocation. A Claude session
# that hangs (background bash polling for a file that never arrives,
# infinite loop, deadlock on a tool call) would otherwise block the
# autopilot indefinitely. 90 minutes is generous for legitimate
# research work — Ada's Stadion/floating-point pieces took ~45 min —
# but bounded so a stuck child never silently consumes the day.
DEFAULT_INVOKE_TIMEOUT_SECONDS = 90 * 60


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
    # Wall-clock timeout for this invocation. Whole subprocess group
    # (Claude + any tool children it spawned) is killed if it exceeds
    # this. Default is generous enough for any current workflow.
    timeout_seconds: int = DEFAULT_INVOKE_TIMEOUT_SECONDS


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


# Per Chapter 3, tool access varies by rank. Postulants and Novices have
# restricted sets that prevent them from writing artifacts the institution
# would treat as final, mutating state in shared paths, or running shell
# commands. The genome's `allowed_tools` is treated as a request; the
# rank ceiling is the institutional floor that subtracts anything beyond
# what the rank earns.
_RANK_TOOL_CEILING: dict[str, set[str]] = {
    "postulant": {"Read", "Glob", "Grep", "WebFetch", "WebSearch"},
    "novice": {"Read", "Glob", "Grep", "Write", "WebFetch", "WebSearch"},
    "junior_fellow": {
        "Read",
        "Glob",
        "Grep",
        "Write",
        "Edit",
        "WebFetch",
        "WebSearch",
        "TaskCreate",
        "TaskUpdate",
        "TaskList",
    },
    # Fellow and above carry full tool access. We omit them from the
    # dict so any new rank inherits an unrestricted default via the
    # `_effective_tools_for` fallback.
}


def _effective_tools_for(genome: Genome) -> list[str]:
    """Intersect the genome's requested tools with the rank ceiling.

    Tools the genome did not request are never added. Ranks not in
    `_RANK_TOOL_CEILING` (Fellow, Senior Fellow, Emeritus) get the
    genome's full request.
    """
    requested = list(genome.allowed_tools)
    ceiling = _RANK_TOOL_CEILING.get(genome.rank)
    if ceiling is None:
        return requested
    return [t for t in requested if t in ceiling]


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

    # Same kill-switch gate as `invoke`. Orchestrator calls are typically
    # cheaper than Fellow calls, but still cost money and time, and they
    # should obey the same operational halt.
    runtime.check_kill_switch()

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

    proc = _run_with_group_timeout(
        cmd,
        cwd=actual_cwd,
        timeout_seconds=DEFAULT_INVOKE_TIMEOUT_SECONDS,
        context=f"Orchestrator step {step}",
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

    Before invocation, the Fellow's episodic memory is queried for entries
    relevant to the brief and the top-K results are staged into the
    workspace as `memory.md`. This is the closest approximation of
    persistence available without fine-tuning: the Fellow does not
    remember between sessions, but their own past work is present in
    every workspace via Read tool.
    """

    # Re-check the kill switch immediately before every Claude call.
    # Workflows that fire multiple Claude invocations per step (admit,
    # andon_review, promote, research) would otherwise let queued work
    # drain after the Founder engages the switch mid-step.
    runtime.check_kill_switch()

    ensure_fellow_dirs(task.genome.id)
    cwd = task.workspace if task.workspace is not None else workspace_path(task.genome.id)
    cwd.mkdir(parents=True, exist_ok=True)
    session_id = str(uuid.uuid4())

    # Stage episodic memory if any exists for this Fellow. Best-effort:
    # failure here never blocks the invocation.
    _stage_memory_for_task(task, cwd)

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
        ",".join(_effective_tools_for(task.genome)),
        "--permission-mode",
        "bypassPermissions",
        "--output-format",
        "json",
    ]

    for extra in task.extra_dirs:
        cmd.extend(["--add-dir", str(extra)])

    proc = _run_with_group_timeout(
        cmd,
        cwd=cwd,
        timeout_seconds=task.timeout_seconds,
        context=f"Fellow {task.genome.id} step {task.step}",
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


def _run_with_group_timeout(
    cmd: list[str],
    *,
    cwd: Path,
    timeout_seconds: int,
    context: str,
) -> subprocess.CompletedProcess:
    """Run `cmd` in its own process group with a wall-clock timeout.

    Plain `subprocess.run(..., timeout=...)` kills only the direct child
    on timeout, leaving any tool subprocesses Claude spawned (background
    bash, helper scripts, child claude calls) running. Using setsid +
    killpg ensures the entire subtree dies, so a stuck Fellow can't leak
    zombie subprocesses that interfere with the next wake-up.

    Returns a CompletedProcess shaped object on normal exit; raises
    RuntimeError on timeout with a message that identifies the context.
    """
    proc = subprocess.Popen(
        cmd,
        cwd=cwd,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
        start_new_session=True,  # equivalent to preexec_fn=os.setsid
    )
    try:
        stdout, stderr = proc.communicate(timeout=timeout_seconds)
    except subprocess.TimeoutExpired as exc:
        # Kill the entire process group so background bash + grandchildren
        # die too. SIGTERM first to give Claude a chance to flush, then
        # SIGKILL after a short grace period.
        try:
            os.killpg(os.getpgid(proc.pid), signal.SIGTERM)
        except ProcessLookupError:
            pass
        try:
            stdout, stderr = proc.communicate(timeout=5)
        except subprocess.TimeoutExpired:
            try:
                os.killpg(os.getpgid(proc.pid), signal.SIGKILL)
            except ProcessLookupError:
                pass
            try:
                stdout, stderr = proc.communicate(timeout=5)
            except subprocess.TimeoutExpired:
                stdout, stderr = "", "(timed out twice; subprocess unresponsive)"
        raise RuntimeError(
            f"{context} exceeded {timeout_seconds}s wall clock and was killed. "
            "This usually means the Fellow's tool use deadlocked (e.g. a "
            "background bash poll waiting on a file that never arrives). "
            "Process group killed; next wake-up will retry from the same "
            "workflow state."
        ) from exc
    return subprocess.CompletedProcess(
        args=cmd,
        returncode=proc.returncode,
        stdout=stdout or "",
        stderr=stderr or "",
    )


def _stage_memory_for_task(task: FellowTask, cwd: Path) -> None:
    """Retrieve episodic memory relevant to this task and stage memory.md."""
    # Local import to avoid pulling fastembed at module load for paths
    # that never need it (CLI startup, status, etc.).
    try:
        from institute import episodic
    except Exception:  # pragma: no cover - import-time failure path
        return

    # Skip if the DB hasn't been initialized yet (e.g., first-time setup
    # before institute init has run).
    from institute import paths

    if not paths.DB_PATH.exists():
        return

    # Don't echo the Fellow's in-flight project work back at them in the
    # same project: skip same-project entries during retrieval.
    project_id = task.project_id
    exclude = project_id if project_id and project_id != "pre-init" else None

    episodic.stage_memory_for(
        cwd,
        fellow_id=task.genome.id,
        fellow_name=task.genome.name,
        query=task.brief,
        top_k=5,
        exclude_project_id=exclude,
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
