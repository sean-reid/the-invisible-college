#!/usr/bin/env bash
# Daemon wrapper invoked by launchd.
#
# Sources the user's shell environment (launchd starts with a near-empty PATH),
# runs `institute autopilot`, and optionally commits and pushes any new
# artifacts. The single-instance lock is held inside autopilot itself via
# fcntl, so this wrapper does not need `flock` (which macOS does not ship).
#
# Environment variables consumed:
#   IC_REPO              absolute path to the repo (required)
#   IC_MAX_BUDGET        USD cap per wake-up. Default: 10
#   IC_MAX_STEPS         step cap per wake-up. Default: 30
#   IC_DAILY_BUDGET_USD  Charter-defined daily USD cap (UTC). 0 = disabled.
#                        Default: 0. Crossing 80% triggers soft austerity;
#                        crossing 100% halts the wake-up until UTC midnight.
#   IC_AUTO_PUSH         "1" to enable git commit + push of artifacts. Default: 0
#   IC_LOG_DIR           where to write log files.
#                        Default: ~/Library/Logs/invisible-college
#   IC_BACKUP_DIR        where to snapshot institute.db after each wake-up.
#                        Default: ~/Library/Application Support/invisible-college/backups
#                        Set to a cloud-synced path (iCloud Drive, Dropbox)
#                        for off-disk durability.
#   IC_BACKUP_RETAIN     how many recent snapshots to keep. Default: 48

set -euo pipefail

: "${IC_REPO:?IC_REPO must be set to the repository path}"
IC_MAX_BUDGET="${IC_MAX_BUDGET:-10}"
IC_MAX_STEPS="${IC_MAX_STEPS:-30}"
IC_DAILY_BUDGET_USD="${IC_DAILY_BUDGET_USD:-0}"
IC_AUTO_PUSH="${IC_AUTO_PUSH:-0}"
IC_LOG_DIR="${IC_LOG_DIR:-$HOME/Library/Logs/invisible-college}"
IC_BACKUP_DIR="${IC_BACKUP_DIR:-$HOME/Library/Application Support/invisible-college/backups}"
IC_BACKUP_RETAIN="${IC_BACKUP_RETAIN:-48}"

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
    echo "budget=\$$IC_MAX_BUDGET, max-steps=$IC_MAX_STEPS, daily=\$$IC_DAILY_BUDGET_USD, auto-push=$IC_AUTO_PUSH"
} >> "$LOG"

set +e
uv run institute autopilot \
    --max-budget-usd "$IC_MAX_BUDGET" \
    --max-steps "$IC_MAX_STEPS" \
    --daily-budget-usd "$IC_DAILY_BUDGET_USD" \
    >> "$LOG" 2>&1
EXIT=$?
set -e

# Snapshot the DB. SQLite's .backup is safe against an actively-written
# WAL database, unlike a plain `cp institute.db`. Runs every wake-up:
# the audit log advances each pass, so a backup is always meaningful.
# Retention prunes the oldest snapshots once IC_BACKUP_RETAIN is exceeded.
mkdir -p "$IC_BACKUP_DIR"
BACKUP_PATH="$IC_BACKUP_DIR/institute-$(date -u +%FT%H%M%SZ).db"
if sqlite3 "$IC_REPO/institute.db" ".backup '$BACKUP_PATH'" >> "$LOG" 2>&1; then
    echo "[$(date -u +%FT%TZ)] db snapshot: $BACKUP_PATH" >> "$LOG"
    # Rotate: keep the IC_BACKUP_RETAIN most recent, delete older.
    ls -1t "$IC_BACKUP_DIR"/institute-*.db 2>/dev/null \
        | tail -n +$((IC_BACKUP_RETAIN + 1)) \
        | while IFS= read -r stale; do
            rm -f -- "$stale"
        done
else
    echo "[$(date -u +%FT%TZ)] db snapshot FAILED" >> "$LOG"
fi

if [ "$IC_AUTO_PUSH" = "1" ] && [ "$EXIT" = "0" ]; then
    # Skip the auto-commit if there are user-edited tracked files under
    # the paths the daemon writes — i.e., a file the user has modified
    # in place but not committed yet. Otherwise the daemon would sweep
    # up half-finished work in progress and ship it to origin.
    #
    # Untracked files (?? in porcelain output) do NOT count: those are
    # the daemon's own fresh output we want to commit. Only the M/A/R/C/D
    # codes in column 2 (unstaged side) indicate a tracked file edited
    # in the working tree, which is the user-edit signal.
    USER_EDITS=$(git status --porcelain -- archive/ blog/src/content/ genomes/ 2>/dev/null \
        | awk '/^.[MARCD]/ { print }')
    if [ -n "$USER_EDITS" ]; then
        echo "[$(date -u +%FT%TZ)] user edits present under daemon paths; skipping auto-commit:" >> "$LOG"
        echo "$USER_EDITS" >> "$LOG"
    else
        # Stage every artifact the daemon may have produced this wake-up.
        # If something changed, commit and push. The push includes
        # everything: publications, decision records, curriculum responses,
        # advisor feedback, genome rank updates. The repo stays clean and
        # the remote stays in sync.
        # `-c commit.gpgsign=false` disables signing for this commit even
        # if global git config has it enabled — the daemon runs without
        # a TTY and would otherwise block on gpg-agent's pinentry.
        git add archive/ blog/src/content/ genomes/ 2>/dev/null || true
        if ! git diff --staged --quiet; then
            # Build a short summary of what changed for the commit message.
            SUMMARY=$(git diff --staged --name-only \
                | awk -F/ '{print $1"/"$2}' | sort -u | head -3 | tr '\n' ' ')
            echo "[$(date -u +%FT%TZ)] daemon produced changes; committing + pushing" >> "$LOG"
            git -c commit.gpgsign=false commit -m "Autopilot $(date -u +%FT%TZ): ${SUMMARY}" >> "$LOG" 2>&1 || true
            git push origin main >> "$LOG" 2>&1 || true
        else
            echo "[$(date -u +%FT%TZ)] nothing changed this wake-up; no commit" >> "$LOG"
        fi
    fi
fi

echo "===== exit=$EXIT =====" >> "$LOG"
exit "$EXIT"
