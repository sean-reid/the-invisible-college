---
kind: circuit_breaker
recorded_at: 2026-05-28T20:02:20+00:00
actors: [orchestrator]
project: 2026-05-27-what-the-definition-replaces-a-capture-v-c02e
---

# Circuit breaker: abandoned 2026-05-27-what-the-definition-replaces-a-capture-v-c02e
**Where:** project `2026-05-27-what-the-definition-replaces-a-capture-v-c02e` (state: `researching`)

**Reason:** circuit breaker tripped after 2 consecutive workflow-level failure(s).

The autopilot kept hitting the same failure mode on retry and cannot self-heal. The project is moved to `abandoned` so the cycle stops re-spending budget on the same broken step. The operator can resurrect the project by editing the most recent step_failure (or fixing the root cause in the workspace/archive) and pushing the project state back to the workflow that needs to re-run.
