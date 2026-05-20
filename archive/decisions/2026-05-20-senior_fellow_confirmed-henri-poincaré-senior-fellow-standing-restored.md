---
kind: senior_fellow_confirmed
recorded_at: 2026-05-20T12:38:06+00:00
actors: [founder, henri-poincare]
---

# Henri Poincaré: Senior Fellow standing restored
**Fellow:** Henri Poincaré (`henri-poincare`)

**Outcome:** confirmed (Senior Fellow standing restored)

**Recorded:** 2026-05-20T12:38:06+00:00

**Trigger:** institutional correction of a structural auto-release.

Between 2026-05-18 and 2026-05-20 the calendar-triggered tenure-review
cadence held Henri Poincaré three times at the senior_fellow rank. The
holds reflected the ladder's terminal-rank ceiling (no rank above
senior_fellow except emeritus, which is reserved for Fellows winding
down) and not any failure of his work. Both the orchestrator and
panelist Pierre Bayle stated this explicitly in the third review;
Bayle voted hold, the orchestrator's rationale read "Release would
be punishing him for the ladder topping out, not for disengagement."

The `two_consecutive_holds` gate then auto-released him anyway. The
archive preserves that release record at
`archive/decisions/2026-05-20-release-released-henri-poincaré-senior-fellow.md`
as the audit trail of what happened.

This decision is the institutional acknowledgement that the release
was a structural error. The institution rules have since been changed
to prevent this pattern: Senior Fellows are no longer enrolled in
calendar-triggered tenure review, the consecutive-holds count is
reset by `senior_fellow_confirmed` events, and the auto-release gate
is rank-conditional and does not fire for the terminal rank.

Henri Poincaré's Senior Fellow standing is restored. His
publications, reviews, and reviewer record stand. The `retired_at`
field is cleared in the same transaction that records this decision.
