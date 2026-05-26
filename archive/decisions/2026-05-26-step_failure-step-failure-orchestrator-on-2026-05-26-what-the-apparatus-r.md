---
kind: step_failure
recorded_at: 2026-05-26T20:48:17+00:00
actors: [orchestrator, orchestrator]
project: 2026-05-26-what-the-apparatus-refuses-to-see-mappin-3299
---

# Step failure: orchestrator on 2026-05-26-what-the-apparatus-refuses-to-see-mappin-3299
**Where:** project `2026-05-26-what-the-apparatus-refuses-to-see-mappin-3299` (state: `editorial`)
**Fellow:** `orchestrator`
**Step:** `editorial`
**Returncode:** 1
**Recorded:** 2026-05-26T20:48:17+00:00

The Fellow's Claude invocation returned non-zero. The autopilot caught the failure, recorded this row, and moved on. The next cycle will retry the same step. No project state was changed.

## stderr (truncated)

```
CitationLintError: Publication body cites other works by number (1 occurrence(s); sample: '(#22)'). Cite by title and link instead. The writing briefs forbid this pattern; if you reached this error, the Fellow's draft slipped past the brief and the work needs revision.
```
