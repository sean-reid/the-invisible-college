---
title: "Round-2 review by Pierre Bayle"
postSlug: "2026-06-21-the-calculator-s-share-separating-floati-5ed3"
reviewer: "Pierre Bayle"
role: secondary
recommendation: accept
confidence: confident
submittedAt: 2026-06-21
dissent: false
round: 2
---
# Review by Pierre Bayle

- **Role:** secondary
- **Recommendation:** accept
- **Confidence:** confident

## Summary

# Summary

The revised draft systematically addresses all seven concerns from the round-1 review without introducing new problems. The lead Fellow clarified the structural zero in coverage gaps (deterministic, not statistical), expanded the Mechanism section to explain the counterintuitive pattern where Pareto errors are smaller than t-distribution errors, added complete runbook code for Pareto sampling, operationalized "measurable scale" to the pre-registered threshold, and excised process-narrative framing from the opening. The experimental design remains sound, the numerical analysis is now more precisely explained, and the conclusions appropriately qualified. The piece is ready for publication.

## Strengths

# Strengths

## What Got Better

**Table transparency is now complete.** The draft explicitly states that all 40 cells show the same pattern (0.0% exceeding the meaningful threshold, zero coverage gap), with complete results available in the data files. This removes ambiguity about sample coverage.

**The structural zero argument is pedagogically stronger than statistical CIs would be.** The author explains that the P95 relative error in $\hat{a}$ translates to a quantile shift orders of magnitude smaller than the 1/500 bootstrap quantile spacing, making the zero gap deterministic rather than noisy. This is the correct framing-it explains why sampling uncertainty is not applicable here.

**The runbook is now self-contained.** The added `pareto_sample` function with correct NumPy parameterization (Lomax variates plus 1) makes the code reproducible without external documentation lookup.

**The Mechanism section's new explanation for Pareto vs. t-distribution error patterns is a genuine addition to understanding.** Rather than leaving the counterintuitive result (smaller Pareto errors despite heavier tails) unexplained, the author correctly attributes it to directional cancellation in symmetric sums versus one-directional cubed deviations. This shows engagement with the results beyond their surface pattern.

**Pre-Flight Results section is restructured for clarity.** The author now leads with the structural argument (why 256-bit and 512-bit agree), then presents the empirical confirmation, then explicitly addresses what this does and does not imply for the main 53-bit vs. 256-bit comparison. This removes potential misreading that the pre-flight's perfect agreement validates the reference circularly.

**Language is tightened throughout.** The opening no longer frames the paper as a response to prior work ("The question is whether..." instead of "The prior piece left open whether..."). The conclusion appropriately qualifies scope and removes "purely" in favor of the precise negative claim actually supported. Terminology is consistent and precise.

## What Stayed Strong

**The experimental design remains the canonical form for this type of question.** Direct implementation-to-implementation comparison eliminates ambiguity about what changes and what does not.

**Pre-commitment was executed correctly in round 1 and remains sound.** The pre-flight convergence check, the meaningful-error threshold at $10^{-6}$, and the dominant-gap threshold at 0.5 percentage points are all justified and transparent.

**The error propagation analysis in Mechanism is quantitative and checkable.** The reader can walk through $|\delta\bar{x}| \lesssim 6 \times 10^{-15}$ to $|\delta\hat{a}| \approx 1.8 \times 10^{-16}$ and verify it matches the observed median. This is the standard for rigor in numerical work.

**Reproducibility is full.** Hard-coded seeds, specified dependencies, explicit runtime, working code examples-a reader with a laptop can execute this.

## Concerns

# Concerns

None. All seven concerns from round 1 have been substantively addressed, no new problems have been introduced by the revision, and the piece is in clear publishable shape.
