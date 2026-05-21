"""Manage the launchd plist that wakes the institution up on a schedule.

The plist invokes `scripts/run-daemon.sh` every `IC_INTERVAL_HOURS` hours.
The daemon script handles the lockfile, runs `institute autopilot`, and
optionally commits + pushes new artifacts.

This module is macOS-specific. Linux / Windows users would need cron or
systemd; left as future work.
"""

from __future__ import annotations

import plistlib
import shutil
import subprocess
from datetime import UTC, datetime
from pathlib import Path

from institute import paths

LABEL = "com.invisible-college.autopilot"
DEFAULT_INTERVAL_HOURS = 12
DEFAULT_MAX_BUDGET = 10.0
DEFAULT_MAX_STEPS = 30
DEFAULT_DAILY_BUDGET = 0.0  # 0 = disabled; set explicitly to enable
LOG_DIR = Path.home() / "Library" / "Logs" / "invisible-college"
PLIST_DIR = Path.home() / "Library" / "LaunchAgents"


def plist_path() -> Path:
    return PLIST_DIR / f"{LABEL}.plist"


def daemon_script() -> Path:
    return paths.ROOT / "scripts" / "run-daemon.sh"


def render_plist(
    *,
    interval_hours: int,
    max_budget_usd: float,
    max_steps: int,
    auto_push: bool,
    daily_budget_usd: float = DEFAULT_DAILY_BUDGET,
    ntfy_topic: str | None = None,
    ntfy_server: str | None = None,
) -> bytes:
    """Render the launchd plist as bytes ready to write to disk.

    `ntfy_topic` is operator-local and treated as semi-secret. When
    non-empty, it lands in EnvironmentVariables so the daemon script
    can post a per-cycle notification. It is never set to a default;
    if the caller omits it, no `IC_NTFY_TOPIC` key is emitted.
    """
    # PATH must include the locations where `uv`, `claude`, and `git` live.
    # The daemon script also re-exports PATH as a fallback. Common tool
    # locations in priority order:
    #   ~/.local/bin   uv, claude (modern installer default)
    #   /opt/homebrew/bin   Homebrew on Apple silicon
    #   /usr/local/bin      Homebrew on Intel + manual installs
    #   /usr/bin, /bin      system tools (git, bash)
    home = str(Path.home())
    env = {
        "IC_REPO": str(paths.ROOT),
        "IC_MAX_BUDGET": str(max_budget_usd),
        "IC_MAX_STEPS": str(max_steps),
        "IC_DAILY_BUDGET_USD": str(daily_budget_usd),
        "IC_AUTO_PUSH": "1" if auto_push else "0",
        "IC_LOG_DIR": str(LOG_DIR),
        "HOME": home,
        "PATH": f"{home}/.local/bin:/opt/homebrew/bin:/usr/local/bin:/usr/bin:/bin",
    }
    if ntfy_topic:
        env["IC_NTFY_TOPIC"] = ntfy_topic
    if ntfy_server:
        env["IC_NTFY_SERVER"] = ntfy_server
    plist: dict[str, object] = {
        "Label": LABEL,
        "ProgramArguments": ["/bin/bash", str(daemon_script())],
        "StartInterval": int(interval_hours) * 3600,
        "RunAtLoad": False,
        "WorkingDirectory": str(paths.ROOT),
        "StandardOutPath": str(LOG_DIR / "stdout.log"),
        "StandardErrorPath": str(LOG_DIR / "stderr.log"),
        "EnvironmentVariables": env,
        # `Adaptive` rather than `Background`: macOS aggressively defers
        # Background tasks under any system load or power signal, which
        # caused scheduled fires to be silently swallowed (a 6-hour
        # interval became 12-15 hours in practice). Adaptive runs the
        # task on time but yields CPU to active foreground work — which
        # is what we actually want for a cadenced research daemon.
        "ProcessType": "Adaptive",
        # ThrottleInterval prevents a fast-failing run from looping at
        # the high end of launchd's scheduling rate.
        "ThrottleInterval": 60,
    }
    return plistlib.dumps(plist, fmt=plistlib.FMT_XML)


def is_loaded() -> bool:
    """True if launchctl reports the agent loaded."""
    if shutil.which("launchctl") is None:
        return False
    result = subprocess.run(
        ["launchctl", "list", LABEL],
        capture_output=True,
        text=True,
        check=False,
    )
    return result.returncode == 0


def _existing_env_value(key: str) -> str | None:
    """Read an EnvironmentVariables value from the on-disk plist.

    Used so re-running `install` preserves operator-set values
    (e.g. the ntfy topic) without forcing the operator to re-pass
    them on every install.
    """
    path = plist_path()
    if not path.exists():
        return None
    try:
        data = plistlib.loads(path.read_bytes())
    except Exception:
        return None
    env = data.get("EnvironmentVariables")
    if not isinstance(env, dict):
        return None
    value = env.get(key)
    return value if isinstance(value, str) and value else None


def install(
    *,
    interval_hours: int = DEFAULT_INTERVAL_HOURS,
    max_budget_usd: float = DEFAULT_MAX_BUDGET,
    max_steps: int = DEFAULT_MAX_STEPS,
    auto_push: bool = False,
    daily_budget_usd: float = DEFAULT_DAILY_BUDGET,
    ntfy_topic: str | None = None,
    ntfy_server: str | None = None,
) -> Path:
    """Write the plist and load it via launchctl. Returns the plist path.

    `ntfy_topic` and `ntfy_server` are operator-local. If the caller
    leaves either as None, the value is preserved from the existing
    on-disk plist (so re-running `install` to bump the interval does
    not blow away the topic). Pass an empty string to explicitly
    clear a previously-set value.
    """
    if shutil.which("launchctl") is None:
        raise RuntimeError("`launchctl` not on PATH. macOS-only feature.")
    PLIST_DIR.mkdir(parents=True, exist_ok=True)
    LOG_DIR.mkdir(parents=True, exist_ok=True)

    if ntfy_topic is None:
        ntfy_topic = _existing_env_value("IC_NTFY_TOPIC")
    elif ntfy_topic == "":
        ntfy_topic = None
    if ntfy_server is None:
        ntfy_server = _existing_env_value("IC_NTFY_SERVER")
    elif ntfy_server == "":
        ntfy_server = None

    body = render_plist(
        interval_hours=interval_hours,
        max_budget_usd=max_budget_usd,
        max_steps=max_steps,
        auto_push=auto_push,
        daily_budget_usd=daily_budget_usd,
        ntfy_topic=ntfy_topic,
        ntfy_server=ntfy_server,
    )
    path = plist_path()
    tmp = path.with_suffix(path.suffix + ".tmp")
    tmp.write_bytes(body)
    tmp.replace(path)

    # Unload first in case it was already loaded; ignore errors.
    subprocess.run(
        ["launchctl", "unload", str(path)],
        capture_output=True,
        check=False,
    )
    subprocess.run(["launchctl", "load", str(path)], check=True)
    return path


def uninstall() -> bool:
    """Unload and remove the plist. Returns True if anything was removed."""
    path = plist_path()
    if not path.exists():
        return False
    if shutil.which("launchctl") is not None:
        subprocess.run(
            ["launchctl", "unload", str(path)],
            capture_output=True,
            check=False,
        )
    path.unlink()
    return True


def status() -> dict[str, object]:
    """Return a structured status snapshot for the CLI to render."""
    path = plist_path()
    info: dict[str, object] = {
        "installed": path.exists(),
        "plist_path": str(path),
        "loaded": False,
        "label": LABEL,
        "interval_hours": None,
        "last_log_mtime": None,
        "log_tail": "",
        "log_path": str(LOG_DIR / "autopilot.log"),
    }
    if path.exists():
        try:
            data = plistlib.loads(path.read_bytes())
            interval = data.get("StartInterval")
            if isinstance(interval, int):
                info["interval_hours"] = round(interval / 3600, 2)
        except Exception:
            pass
    info["loaded"] = is_loaded()
    log = LOG_DIR / "autopilot.log"
    if log.exists():
        info["last_log_mtime"] = datetime.fromtimestamp(log.stat().st_mtime, UTC).isoformat(
            timespec="seconds"
        )
        text = log.read_text(encoding="utf-8", errors="replace").splitlines()
        info["log_tail"] = "\n".join(text[-40:])
    return info
