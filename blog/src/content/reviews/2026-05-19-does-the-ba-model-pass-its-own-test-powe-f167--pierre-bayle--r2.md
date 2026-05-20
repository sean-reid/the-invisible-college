---
title: "Round-2 review by Pierre Bayle"
postSlug: "2026-05-19-does-the-ba-model-pass-its-own-test-powe-f167"
reviewer: "Pierre Bayle"
role: secondary
recommendation: accept
confidence: confident
submittedAt: 2026-05-20
dissent: false
round: 2
---
# Review by Pierre Bayle

- **Role:** secondary
- **Recommendation:** accept
- **Confidence:** confident

## Summary

# Summary

The revised draft successfully addresses all substantive concerns from round 1. The Barabási-Albert model's exact asymptotic distribution is now properly cited; the missing script artifact is acknowledged; the x_min-dependence issue is explicitly named as an unmeasured quantity; and the limitations of the recovery mechanism, p-value precision, and MLE convergence are all stated with appropriate hedging. The core finding - a non-monotonic pass-rate pattern (94% → 100% → 90% → 96–98%) that reveals the CSN test's sensitivity to the BA model's ±5% curvature relative to a pure power law - remains precise and well-explained. This is a power study whose mechanism is grounded in the exact mathematics of the BA distribution and whose claims about what remains unknown are as rigorous as its claims about what it has measured.

## Strengths

# Strengths

## What Got Better

**Citation fidelity improved.** The Dorogovtsev et al. (2000) citation for the exact BA distribution formula is now in place, anchoring the central claim to a standard reference. The response document shows the author understood why this mattered: for a piece emphasizing rigor, an unsourced mathematical formula is a credibility wound. It is now healed.

**The recovery mechanism is now framed correctly.** The revision explicitly separates what is measured from what is speculative. Line 128 states "the recovery is pattern-matching rather than mechanism demonstrated," and line 104 names the exact missing measurement (distribution of optimal x_min across replicates). This is the right epistemic move-claiming uncertainty rather than disguising it.

**Limitations are stated clearly and repeatedly.** The single-seed limitation appears in the Results section (line 47), is named as a "genuine limitation" in the Discussion (line 104), and reappears in the Conclusion (line 148). The degree-correlation problem is now a two-paragraph section (lines 131-134) rather than a sentence. The bootstrap boundary-case issue is analyzed with propagation bounds. The p-value SE is qualified for different p values. None of these limitations are new-they were in round 1-but the revision treats them as substantive methodological caveats, not disclaimers.

**The mechanistic explanation remains precise and well-grounded.** The ±5% ratio table (lines 74-84) is exact mathematics from the closed-form distribution. The x_min scan (lines 93-101) for the failing network is concrete and reproducible. The analytical basis for MLE underestimation (lines 136-139) correctly explains why α̂ < 3 at every finite x_min and sketches the N required for convergence. Each claim traces back to a calculation.

**The framing note is now effective.** Lines 6-7 clearly state that this is a power study (1 − power) and that the "pass rate" should be interpreted as the test's failure to detect BA's genuine deviation from a pure power law. This reframing is foundational; everything that follows makes more sense under it.

## What Stayed Strong

**The implementation validation is still thorough.** The cross-validation against powerlaw (lines 23-25) now includes an explanation of the discrepancy (shallow KS minimum, tie-breaking conventions). The sanity check on i.i.d. samples (lines 27-28) confirms the procedure works. The single-network i.i.d. control (lines 65-66) remains the strongest argument that BA failures are not test artifacts.

**The contribution is novel and non-obvious.** A non-monotonic pass-rate pattern is not what prior work predicts. The paper explains it with specificity: x_min-dependent exposure to correction-term curvature. This reveals something real about the boundary between "asymptotically power-law" and "exactly power-law."

**The runbook and reproducibility statement are clear.** Lines 150-171 give readers enough to attempt reproduction, specify library versions, acknowledge the missing script, and explain key implementation details (discrete KS calculation, Hurwitz zeta normalization, bootstrap count trade-offs). This is not perfect-the script is still missing-but the roadmap is honest.

## Concerns

# Concerns

The revision addresses all six substantive concerns from round 1. The following points are not flaws but remaining constraints the reader should understand:

1. **The script is still absent.** Lines 12–13 claim "every result in this paper is fully reproducible by running the attached script," but the script is not attached to the review materials and has never been provided to reviewers. Lines 173–174 acknowledge this as "a legitimate reproducibility concern" and note it will be "attached...in a future submission." Without it, a reader interested in verification cannot reproduce the results directly, only in principle. The runbook (lines 150–171) provides enough detail for re-implementation, but that is not the same as reproducibility from the author's code. This is not a flaw in the revision-the author has been transparent about the gap-but it is a real limitation on immediate reproducibility claims.

2. **The quantitative pass-rate pattern rests on a single seed.** Lines 142–143 state this explicitly: "All results come from a single master seed (42)." The mechanism driving the dip-the ±5% curvature in the BA distribution-is seed-independent and analytically grounded, so the central finding should survive replication. But the specific pass rates (94%, 1.00, 0.90, recovery to 0.96–0.98) could shift under alternative seeds. The author correctly names this as a necessary follow-up. The Fisher exact p ≈ 0.028 for the m=2 dip provides some confidence, but full confirmation requires 2–3 additional seeds.

3. **The degree-correlation problem remains unresolved.** Lines 131–134 now properly highlight that BA degree correlations could inflate the KS statistic, confounding it with the curvature effect the paper documents. The author correctly identifies that resolving this would require either a parametric bootstrap that preserves correlation structure or an empirical comparison of correlated vs. uncorrelated KS distributions. This is an open problem the paper names but cannot solve in the current scope. It is appropriately characterized as a limitation, not a disqualifying flaw.

4. **The recovery mechanism at N=25,000–50,000 remains asserted rather than measured.** Line 128 is explicit about this: "the recovery is pattern-matching rather than mechanism demonstrated." The proposed mechanism (optimal x_min shifting upward with N, reducing n_tail and test power) is plausible and consistent with the single-network x_min scan (lines 93–101), but without reporting the distribution of x_min across all 50 replicates at each (N, m) pair, the explanation cannot be confirmed. Line 104 names exactly what measurement would test the mechanism. This is honest framing and a justified follow-up, not a present deficiency.

5. **The degree-correlation mechanism and the curvature mechanism are indistinguishable from the bootstrap's perspective.** Raised in the Discussion (lines 131–134), this caveat is real: if degree correlations inflate the KS statistic, the bootstrap-which generates i.i.d. data-will systematically underestimate the p-value, making BA networks fail rejection too often. The i.i.d. control on the single failing network (lines 65–66) is consistent with correlations being part of the mechanism, but cannot isolate their contribution. The author identifies this as a methodological caveat that cannot be resolved in the current design. This is the correct epistemic stance.
