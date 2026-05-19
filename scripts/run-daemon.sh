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

# launchd starts with a near-empty PATH. We need `uv`, `claude`, and `git`
# resolvable. Set PATH explicitly here rather than sourcing ~/.zshrc:
# launchd runs this under bash, and .zshrc is full of zsh-only commands
# (zmodload, autoload, compinit) that fail in bash with exit code 127.
# The plist also sets PATH; this is a belt-and-braces fallback.
export PATH="$HOME/.local/bin:/opt/homebrew/bin:/usr/local/bin:/usr/bin:/bin:$PATH"

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
    # Stage every artifact the daemon may have produced this wake-up.
    # If something changed, commit and push. The push includes
    # everything: publications, decision records, curriculum responses,
    # advisor feedback, genome rank updates. The repo stays clean and
    # the remote stays in sync.
    git add archive/ blog/src/content/ genomes/ 2>/dev/null || true
    if ! git diff --staged --quiet; then
        # Build a short summary of what changed for the commit message.
        SUMMARY=$(git diff --staged --name-only \
            | awk -F/ '{print $1"/"$2}' | sort -u | head -3 | tr '\n' ' ')
        echo "[$(date -u +%FT%TZ)] daemon produced changes; committing + pushing" >> "$LOG"
        git commit -m "Autopilot $(date -u +%FT%TZ): ${SUMMARY}" >> "$LOG" 2>&1 || true
        git push origin main >> "$LOG" 2>&1 || true
    else
        echo "[$(date -u +%FT%TZ)] nothing changed this wake-up; no commit" >> "$LOG"
    fi
fi

echo "===== exit=$EXIT =====" >> "$LOG"
exit "$EXIT"
