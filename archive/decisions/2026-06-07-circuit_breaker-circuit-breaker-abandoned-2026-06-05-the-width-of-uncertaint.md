---
kind: circuit_breaker
recorded_at: 2026-06-07T21:08:56+00:00
actors: [orchestrator]
project: 2026-06-05-the-width-of-uncertainty-does-varentropy-3771
---

# Circuit breaker: abandoned 2026-06-05-the-width-of-uncertainty-does-varentropy-3771
**Where:** project `2026-06-05-the-width-of-uncertainty-does-varentropy-3771` (state: `researching`)

**Reason:** circuit breaker tripped after 5 consecutive Fellow CLI failure(s).

The autopilot kept hitting the same failure mode on retry and cannot self-heal. The project is moved to `abandoned` so the cycle stops re-spending budget on the same broken step. The operator can resurrect the project by editing the most recent step_failure (or fixing the root cause in the workspace/archive) and pushing the project state back to the workflow that needs to re-run.
