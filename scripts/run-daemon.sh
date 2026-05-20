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

# Pre-cycle baseline of the daemon-managed paths' working-tree state.
# Captured at the start of an uncommitted work chain so the auto-commit
# step at the end can distinguish user edits (present before this chain
# of cycles began) from daemon output (everything new since).
#
# Why persist across cycles: if a cycle exits with uncommitted work
# still on disk — autopilot hit its cost cap mid-step, was killed by
# the OS, or the operator pulled the plug — the next cycle should be
# able to identify that uncommitted state as the prior daemon's work,
# not as user edits. Reusing the baseline from the prior cycle gives
# that signal without a separate sentinel: the baseline anchors to
# "what the tree looked like when this daemon work chain started,"
# regardless of how many cycles since.
PRE_STATUS_FILE="$IC_REPO/.daemon-cycle.pre-status"

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

# Capture the pre-cycle baseline ONLY if not already captured. A prior
# cycle that didn't reach its auto-commit step left its baseline in
# place; reusing it means this cycle's auto-commit can still tell
# pre-existing edits apart from daemon-produced ones.
if [ ! -f "$PRE_STATUS_FILE" ]; then
    git status --porcelain -- archive/ blog/src/content/ genomes/ 2>/dev/null \
        > "$PRE_STATUS_FILE" || true
    echo "[$(date -u +%FT%TZ)] captured pre-cycle baseline" >> "$LOG"
else
    echo "[$(date -u +%FT%TZ)] reusing pre-cycle baseline from prior interrupted cycle" >> "$LOG"
fi

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
    # Identify which files (if any) had unstaged modifications OR were
    # untracked-but-present BEFORE this chain of daemon cycles started.
    # Those are user edits and must be preserved. Files newly modified
    # or newly created since are daemon output and should be committed
    # even if a prior cycle left them behind.
    #
    # We include `?` (untracked) in addition to M/A/R/C/D so a file the
    # operator hand-creates in a daemon path before the daemon starts
    # is preserved across the auto-commit. Files only appearing in POST
    # (not in PRE) are treated as daemon output.
    PRE_FILES=$(awk '/^.[MARCD?]/ { print $2 }' "$PRE_STATUS_FILE" 2>/dev/null | sort -u)
    POST_FILES=$(git status --porcelain -- archive/ blog/src/content/ genomes/ 2>/dev/null \
        | awk '/^.[MARCD?]/ { print $2 }' | sort -u)
    USER_EDIT_FILES=$(comm -12 <(printf '%s\n' "$PRE_FILES") <(printf '%s\n' "$POST_FILES"))

    if [ -n "$USER_EDIT_FILES" ]; then
        echo "[$(date -u +%FT%TZ)] preserving pre-existing user edits:" >> "$LOG"
        printf '%s\n' "$USER_EDIT_FILES" >> "$LOG"
    fi

    # Stage everything in daemon paths, then back out the user-edited
    # files. Anything that remains staged is daemon output — files the
    # daemon either created fresh this chain of cycles or modified
    # from a state already committed at the time of the baseline.
    git add -- archive/ blog/src/content/ genomes/ 2>/dev/null || true
    if [ -n "$USER_EDIT_FILES" ]; then
        while IFS= read -r f; do
            [ -z "$f" ] && continue
            git restore --staged -- "$f" 2>/dev/null || true
        done <<< "$USER_EDIT_FILES"
    fi

    if ! git diff --staged --quiet; then
        # Build a short summary of what changed for the commit message.
        SUMMARY=$(git diff --staged --name-only \
            | awk -F/ '{print $1"/"$2}' | sort -u | head -3 | tr '\n' ' ')
        echo "[$(date -u +%FT%TZ)] daemon produced changes; committing + pushing" >> "$LOG"
        # `-c commit.gpgsign=false` disables signing for this commit even
        # if global git config has it enabled — the daemon runs without
        # a TTY and would otherwise block on gpg-agent's pinentry.
        git -c commit.gpgsign=false commit -m "Autopilot $(date -u +%FT%TZ): ${SUMMARY}" >> "$LOG" 2>&1 || true
        git push origin main >> "$LOG" 2>&1 || true
    else
        echo "[$(date -u +%FT%TZ)] nothing changed this wake-up; no commit" >> "$LOG"
    fi

    # Clear the baseline now that the auto-commit step has run. The
    # next cycle will snapshot a fresh baseline from the current
    # working tree (which still holds any preserved user edits, plus
    # whatever the daemon and/or operator do between now and then).
    rm -f "$PRE_STATUS_FILE"
fi

echo "===== exit=$EXIT =====" >> "$LOG"
exit "$EXIT"
