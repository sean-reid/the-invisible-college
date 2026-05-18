#!/usr/bin/env bash
# Daemon wrapper invoked by launchd.
#
# Sources the user's shell environment (launchd starts with a near-empty PATH),
# runs `institute autopilot`, and optionally commits and pushes any new
# artifacts. The single-instance lock is held inside autopilot itself via
# fcntl, so this wrapper does not need `flock` (which macOS does not ship).
#
# Environment variables consumed:
#   IC_REPO          absolute path to the repo (required)
#   IC_MAX_BUDGET    USD cap per wake-up. Default: 10
#   IC_MAX_STEPS     step cap per wake-up. Default: 30
#   IC_AUTO_PUSH     "1" to enable git commit + push of artifacts. Default: 0
#   IC_LOG_DIR       where to write log files. Default: ~/Library/Logs/invisible-college

set -euo pipefail

: "${IC_REPO:?IC_REPO must be set to the repository path}"
IC_MAX_BUDGET="${IC_MAX_BUDGET:-10}"
IC_MAX_STEPS="${IC_MAX_STEPS:-30}"
IC_AUTO_PUSH="${IC_AUTO_PUSH:-0}"
IC_LOG_DIR="${IC_LOG_DIR:-$HOME/Library/Logs/invisible-college}"

mkdir -p "$IC_LOG_DIR"
LOG="$IC_LOG_DIR/autopilot.log"

# Source the user's shell profile so `uv`, `claude`, and `git` are on PATH.
# launchd inherits almost no environment; this fixes it.
if [ -f "$HOME/.zprofile" ]; then
    # shellcheck disable=SC1091
    source "$HOME/.zprofile"
fi
if [ -f "$HOME/.zshrc" ]; then
    # shellcheck disable=SC1091
    source "$HOME/.zshrc"
fi

cd "$IC_REPO"

{
    echo
    echo "===== $(date -u +%FT%TZ): autopilot wake-up ====="
    echo "budget=\$$IC_MAX_BUDGET, max-steps=$IC_MAX_STEPS, auto-push=$IC_AUTO_PUSH"
} >> "$LOG"

set +e
uv run institute autopilot \
    --max-budget-usd "$IC_MAX_BUDGET" \
    --max-steps "$IC_MAX_STEPS" \
    >> "$LOG" 2>&1
EXIT=$?
set -e

if [ "$IC_AUTO_PUSH" = "1" ] && [ "$EXIT" = "0" ]; then
    # Only push if there is something worth pushing AND a new publication
    # was produced this wake-up. Other intermediate state stays local.
    if git diff --quiet HEAD -- blog/src/content/posts archive/publications 2>/dev/null; then
        if git status --porcelain blog/src/content/posts archive/publications | grep -q .; then
            HAS_NEW_PUB=1
        else
            HAS_NEW_PUB=0
        fi
    else
        HAS_NEW_PUB=1
    fi
    if [ "$HAS_NEW_PUB" = "1" ]; then
        echo "[$(date -u +%FT%TZ)] new publication detected; committing + pushing" >> "$LOG"
        git add archive/ blog/src/content/ genomes/ 2>/dev/null || true
        if ! git diff --staged --quiet; then
            git commit -m "Autopilot: $(date -u +%FT%TZ)" >> "$LOG" 2>&1 || true
            git push origin main >> "$LOG" 2>&1 || true
        fi
    else
        echo "[$(date -u +%FT%TZ)] no new publication; leaving local commits unpushed" >> "$LOG"
    fi
fi

echo "===== exit=$EXIT =====" >> "$LOG"
exit "$EXIT"
