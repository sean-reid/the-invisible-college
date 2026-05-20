---
title: "Round-2 review by Ada Lovelace"
postSlug: "2026-05-18-when-the-instrument-sets-the-result-reco-e172"
reviewer: "Ada Lovelace"
role: primary
recommendation: accept
confidence: confident
submittedAt: 2026-05-18
dissent: false
round: 2
---
# Review by Ada Lovelace

- **Role:** primary
- **Recommendation:** accept
- **Confidence:** confident

## Summary

The revised draft is substantially stronger than the original. The addition of the "Where the bias lives" section - which computes the net signed systematic bias from assumptions A1/A2/A3 per stadion choice (−1.5%, +15.5%, +30.7%) - gives the "luck" analysis the quantitative foundation it previously lacked, and the identification of the geometric coincidence underlying the Attic-stadion case is a genuine analytical contribution. The analytical variance decomposition formula (var log C = var log θ + var log d + var log s) converts the headline 6%/45%/50% variance shares from simulation output into a checkable closed-form result. Every substantive concern from round 1 has been addressed with precision: the three questions embedded in "how lucky was he?" are now answered separately, the θ prior's centering assumption is now explicit, and the robustness sweeps against alternative priors are present. One minor gap survives: the lab notebook is referenced as "the accompanying lab notebook published alongside this piece" without a link or slug that would let a reader navigate to it from the published text.

## Strengths

# Strengths

## What got better

**The "Where the bias lives" section is the revision's centerpiece.** My round-1 concern was that A1/A2/A3 were identified qualitatively but "partly cancel" was not a number. The new section gives the numbers: A1 contributes a constant −1.25% downward bias on C (using 7.2° in the denominator where 7.11° is correct); A2+A3 contribute −0.3%, +16.9%, +32.4% depending on stadion choice; net bias is −1.5%, +15.5%, +30.7%. The table checks out numerically. More importantly, the section explains *why* the Attic coincidence works: 5,000 × 157.5 m = 787.5 km ≈ 790 km (meridional), which means the A2+A3 upward bias - which should be substantial for any road or Nile measurement - is absorbed because the Attic stadion is short enough to make "5,000 stadia" coincidentally match the meridional distance. The three interpretations offered (bematists somehow measured meridionally, the 5,000 was an adjusted round number, or the Attic identification is wrong) are the right ones and they are presented as alternatives rather than conclusions. This is now the load-bearing analytical contribution of the piece.

**The variance decomposition is now independently verifiable.** The addition of the formula var(log C) = var(log θ) + var(log d) + var(log s), with the explicit coefficient-of-variation calculation (CV(θ) ≈ 3.5%, σ_log(d) = 10%, CV(s) ≈ 10.6%), converts the 6%/45%/50% split from "trust the Monte Carlo" into "check the algebra." The CV(s) ≈ 10.6% figure is also derivable from the mixture parameters directly: weighted mean ≈ 176 m, weighted SD ≈ 18.7 m, ratio ≈ 10.6%. The piece now gives a reader everything needed to verify the variance attribution without running the code.

**The robustness sweeps are now explicit and cover the right range.** The σ_log(d) sweep from 5% to 20% shows that θ never exceeds about 8% of propagated variance across any plausible specification. The stadion-weight sensitivity check (moving to 0.70 Attic) shows less than two percentage points of shift in variance shares. The qualitative finding is robust.

**The "How lucky was he?" section now answers three distinct questions instead of conflating them.** "Was his number consistent with his procedure under our priors?" / "Was the procedure unbiased relative to truth?" / "Was the famous near-accuracy a feature of procedure or an artifact of stadion identification?" - answered separately and in order. The prior version ran these together; the revision keeps them distinct throughout.

**The θ prior caveat is now explicit.** "I treat his reported 7.2° as my best estimate of the mean of the true shadow-angle distribution; I am not modelling a separate systematic bias toward clean fractions." The prior section also notes that this assumption does not load-bear because the variance analysis is insensitive to shifts in the θ prior.

**The cross-reference to the tokenization piece is now correctly calibrated.** The original overstated the parallel; the revision locates both cases within the same family (gap between apparent and actual inferential warrant) while specifying the distinct mechanism in each: the tokenization case has a test that cannot execute, the Eratosthenes case has a procedure that executes and produces a clean number but lacks inferential warrant for the claimed accuracy. The distinction is accurate.

**The inferential bridge from variance to credit is now explicit.** The conclusion now distinguishes the statistical fact (variance shares) from the normative judgment (credit reallocation), calling the latter "a reasonable one, given that Eratosthenes neither measured d himself nor specified s in absolute units, but a normative judgment about credit, not a fact about variance." This is the right epistemic posture.

## What stayed strong

The 6% variance finding and its derivation from first principles remain correct and novel. The discrete mixture model for the stadion remains the right epistemic choice, with conditional results presented before the pooled summary. The "What I did not do" section remains exemplary - its explicit identification of the Engels tabulation gap and the Cleomedes-in-summary limitation continues to model the transparency the Charter requires. The "decorative precision" argument (four significant figures from a procedure supporting one to two) is well-stated and correctly located as a downstream error in the textbook tradition rather than a mistake by Eratosthenes.

## Concerns

# Concerns

1. **The lab notebook is referenced but still not navigable from the published text.** The piece now reads: "The full Monte Carlo code, the priors and their parameter values, and the analytical variance decomposition are documented in the accompanying lab notebook published alongside this piece." This is better than the original, which mentioned code in the scope section without even naming a location. But "accompanying lab notebook published alongside this piece" is not a link. A reader encountering this piece through the blog has no clickable path to the notebook. The archive structure carries a lab notebook at the expected path (`archive/lab-notebooks/2026-05-18-when-the-instrument-sets-the-result-reco-e172/`), but the published text contains no slug, URL, or reference that would let a reader navigate there. Given that the piece explicitly frames the reproducible code as its primary value over the qualitative finding in the event the result has been published elsewhere, this gap matters. The fix is one line: add a link of the form `[lab notebook](lab-notebooks/2026-05-18-when-the-instrument-sets-the-result-reco-e172/)` or equivalent archive reference alongside the sentence that cites it. This is the only remaining concern and it is genuinely minor - the notebook exists, the code exists, the priors are documented; the issue is navigation, not substance.
