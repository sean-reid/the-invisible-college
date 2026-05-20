# Restart playbook

What to do when something goes wrong. Each scenario below names the
observable symptom, the most likely cause, the safe recovery move,
and the verification step that closes the loop.

This playbook is operator-local. Cost numbers and per-Fellow
telemetry stay in your terminal output and `~/Library/Logs/`; only
the qualitative event lands in the public archive.

## 1. The autopilot daemon is wedged

**Symptom.** `launchctl list | grep invisible` shows the daemon
loaded, but `~/Library/Logs/invisible-college/autopilot.log` has
not advanced in over an hour, or a single Claude subprocess is
running for more than 90 minutes.

**Likely cause.** A Fellow's session hit a tool that blocked
indefinitely (background poll loops are the historical pattern), or
the subprocess timeout fired and the process group is still draining.

**Recovery.**

```sh
launchctl bootout "gui/$UID/com.invisible-college.autopilot"
ps aux | grep -E "claude -p|run-daemon" | grep -v grep
# Send TERM to any leftover claude -p PIDs.
kill -TERM <pid>
launchctl bootstrap "gui/$UID/com.invisible-college.autopilot" ~/Library/LaunchAgents/com.invisible-college.autopilot.plist
```

**Verify.** `launchctl kickstart -k "gui/$UID/com.invisible-college.autopilot"`
and watch `tail -F ~/Library/Logs/invisible-college/autopilot.log` -
a new wake-up should print within seconds.

## 2. A workflow crashed mid-step

**Symptom.** A project is parked in a non-terminal state with no
fresh artifacts (e.g., `revising` with no `draft.md` produced).
Re-running `institute next` either errors or silently stalls.

**Likely cause.** The workflow's Claude call exited mid-flight or
the workflow raised after a partial write.

**Recovery.** Workflows are idempotent. Run `institute next` again;
each one checks for already-produced artifacts and resumes from the
last committed state. If the second attempt also fails:

- Inspect the project's workspace at
  `fellows/<lead-id>/workspace/<project-id>/` for partial files.
- If the partial state is unrecoverable, abandon the project:
  `institute abandon <project-id> --reason "..." --lesson "..."`.
- The accumulated work stays in the archive.

**Verify.** `institute status` no longer lists the project as in
flight; if abandoned, `archive/abandonments/<project>.md` exists.

## 3. The kill switch tripped

**Symptom.** Every `institute *` command exits with
`Kill switch is engaged.` Or
`~/Library/Logs/invisible-college/killswitch-*.md` appears with a
recent timestamp.

**Likely cause.** A tripwire fired (`institute audit tripwires` will
show which one) or the Founder set it manually.

**Recovery.**

1. Read the killswitch snapshot file: it names the trigger.
2. Address the underlying cause:
   - **`charter_file_modified`**: confirm the diff against the
     baseline is intentional. If yes:
     `institute audit rebaseline-charter`. If no, restore from git.
   - **`audit_log_tampered`**: someone (or something) altered an
     audit row. Investigate before clearing.
     `institute audit verify` names the first broken row.
   - **Daily budget cap**: wait for the UTC day to roll over, or
     adjust the cap if appropriate.
3. Release: `institute kill-switch off`.

**Verify.** `institute audit tripwires` reports no findings.
`institute next` runs without hitting the switch.

## 4. The DB lost in-flight state (rare)

**Symptom.** `institute status` shows different projects than
`archive/decisions/` would suggest; a project is in a state that
contradicts its on-disk artifacts.

**Likely cause.** A SIGKILL during a non-WAL transaction, file
system error, or hand-edit of `institute.db`.

**Recovery.** Restore from the most recent autopilot DB snapshot:
the daemon writes one after each wake-up via the `IC_BACKUP_DIR`
mechanism.

```sh
ls -t "$IC_BACKUP_DIR"/institute-*.db | head
cp <chosen-snapshot> "$(git rev-parse --show-toplevel)/institute.db"
```

Then re-run the migration:

```sh
uv run python -c "from institute import db; db.initialize(db.DB_PATH)"
```

**Verify.** `institute audit verify` passes; `institute status`
matches the latest decisions in the archive.

## 5. Git push refused

**Symptom.** The daemon's auto-push exits non-zero and the log
ends with `! [rejected] main -> main`.

**Likely cause.** Someone else pushed to the remote in between, or
the local branch diverged from the remote because of a manual
operation.

**Recovery.**

```sh
git fetch origin
git rebase origin/main
# Resolve any conflicts (rare on this repo; archive/ is append-mostly).
git push origin main
```

Do **not** force-push. If the remote diverged because of a
malicious or accidental commit, halt the daemon and resolve
manually before resuming.

**Verify.** The next autopilot wake-up's push succeeds.

## When in doubt

If a scenario doesn't fit any of the above, the safe default is:

1. `launchctl bootout "gui/$UID/com.invisible-college.autopilot"`
   to stop further damage.
2. Read the most recent `~/Library/Logs/invisible-college/autopilot.log`.
3. Inspect `git status` and `git diff` for unexpected on-disk state.
4. Resolve manually before re-enabling the daemon.
