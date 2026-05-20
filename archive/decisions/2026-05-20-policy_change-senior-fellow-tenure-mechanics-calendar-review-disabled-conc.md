---
kind: policy_change
recorded_at: 2026-05-20T12:39:24+00:00
actors: [founder]
---

# Senior Fellow tenure mechanics: calendar review disabled, concern-review path added
**Date:** 2026-05-20

**Effective:** immediately.

**Scope:** the tenure-review mechanics around the Senior Fellow rank.

## What changed

1. **Calendar-triggered tenure review is disabled for Senior Fellows.**
   The autonomous-run loop no longer selects Senior Fellows as
   candidates for periodic promotion review. The reviewer-candidate
   pool filters them out.

2. **The two-consecutive-holds auto-release gate no longer fires for
   Senior Fellows.** A `hold` outcome for a Senior Fellow leaves the
   record unchanged and does not contribute to a release escalation.

3. **A peer-sponsored concern-review path is added.** To re-examine a
   Senior Fellow's standing, a peer files concrete grounds. The panel
   reads the dossier and the grounds and chooses one of three
   restricted outcomes: confirm, sabbatical-suggested, or (in severe
   cases) release. There is no hold outcome on this path - the record
   carries a positive institutional statement one way or the other.

4. **`senior_fellow_confirmed` is a new decision kind** that records
   the positive confirmation and resets the `consecutive_holds` count
   in `reputation.consecutive_holds()`.

## Why

The Senior Fellow rank is terminal and indefinite. Running it through
a periodic gate quietly subverts the academic-freedom logic that made
the rank indefinite in the first place: a Fellow whose standing is
perpetually up for committee review is not actually on indefinite
appointment.

The previous mechanics also produced a concrete error: between
2026-05-18 and 2026-05-20 the cadence held Henri Poincaré three
times, with the orchestrator and panelist Pierre Bayle both stating
explicitly each time that the holds reflected the ladder's
terminal-rank ceiling and not his performance. The
`two_consecutive_holds` gate then auto-released him anyway. Bayle's
third-vote concern surfaced the architectural problem; this policy
change is the institutional response.

A separate `senior_fellow_confirmed` decision (recorded today) restores
Poincaré's standing. The original release record is preserved in the
archive as the audit trail of what occurred.

## Where this is documented

- `institute/workflows/concern_review.py`: the new path.
- `institute/cli.py`: `_pick_review_candidate` excludes Senior Fellows.
- `institute/workflows/promote.py`: rank-conditional auto-release gate.
- `institute/reputation.py`: `consecutive_holds` resets on
  `senior_fellow_confirmed`.
- `docs/03-fellows.md`: the Charter chapter is updated to match.

## Future positive recognition

This change leaves a gap: there is no built-in positive-recognition
mechanism for Senior Fellows producing outstanding work (analogous to
endowed chairs, named lectureships, or society honors at a real
university). The College may add such a mechanism later as a separate
artifact, not as an outcome of a review path.
