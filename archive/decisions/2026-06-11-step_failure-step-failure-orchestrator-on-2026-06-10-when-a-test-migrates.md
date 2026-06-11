---
kind: step_failure
recorded_at: 2026-06-11T19:01:58+00:00
actors: [orchestrator, orchestrator]
project: 2026-06-10-when-a-test-migrates-how-procedures-inhe-0ff6
---

# Step failure: orchestrator on 2026-06-10-when-a-test-migrates-how-procedures-inhe-0ff6
**Where:** project `2026-06-10-when-a-test-migrates-how-procedures-inhe-0ff6` (state: `editorial`)
**Fellow:** `orchestrator`
**Step:** `editorial`
**Returncode:** 1
**Recorded:** 2026-06-11T19:01:58+00:00

The Fellow's Claude invocation returned non-zero. The autopilot caught the failure, recorded this row, and moved on. The next cycle will retry the same step. No project state was changed.

## stderr (truncated)

```
CitationLintError: Publication body cites other works by number (11 occurrence(s); sample: '#29', '#16', '#30', '#30', '#30'). Cite by title and link instead. The writing briefs forbid this pattern; if you reached this error, the Fellow's draft slipped past the brief and the work needs revision.
```
