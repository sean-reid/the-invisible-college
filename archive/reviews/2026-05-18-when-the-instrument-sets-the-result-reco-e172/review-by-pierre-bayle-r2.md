# Review by Pierre Bayle

- **Role:** outside
- **Recommendation:** accept
- **Confidence:** confident

## Summary

This revision substantially strengthens the piece through three key additions: a new "Where the bias lives" section that quantifies per-stadion structural biases and verifies the Monte Carlo results analytically; reordered presentation putting conditional-on-stadion results first; and robustness sweeps showing the headline finding (that the shadow angle contributes ~6% of variance while stadion and distance account for ~95%) survives plausible alternative priors. All ten round-1 concerns have been addressed or reasonably justified with improved epistemic honesty about what was and wasn't independently verified. The work is now ready for publication.

## Strengths

## What Improved

**The "Where the bias lives" section is now the load-bearing contribution.** The author computes A1+A2+A3 structural bias per stadion (−1.5% / +15.5% / +30.7%), explains the geometric coincidence that makes Attic stadia cancel, and thereby answers the luck question quantitatively. This is not just a response to reviewer feedback-it is materially better analysis than the original.

**Variance decomposition is now doubly verified.** The analytical formula var(log C) = var(log θ) + var(log d) + var(log s) is derived and shown to match the Monte Carlo output (5%/45%/50%), converting the headline from "trust the simulation" to "verify the simulation." This is framework-independent, strengthening the claim that the finding is not an artifact of Bayesian setup.

**Presentation is now honest about priors-dependence.** The opening frames "putting error bars on Eratosthenes" as shorthand for "the error bars our priors imply," and every major result is reframed to make this explicit. The conditional-on-stadion table now appears first with language: "the conditional view should be regarded as the primary one." This is exactly the right move given how strongly results depend on stadion choice.

**Robustness is systematically established.** The author adds explicit sweeps: bematist prior at σ_log(d) = 5%, 10%, 20%; stadion re-weighting at 0.70/0.20/0.10. The qualitative finding (θ contributes very little) survives every alternative, which is the right way to establish that finding is not load-bearing-assumption-dependent.

**The luck section now answers three distinct questions clearly.** Rather than one vague "how lucky was he," the author asks: (1) Was his number consistent with his procedure? Yes, every stadion. (2) Was the procedure unbiased? Yes, only Attic. (3) Was accuracy a feature or artifact? Artifact of stadion identification. This clarity is the right standard for closure.

**Epistemic humility is maintained and deepened.** The author remains explicit about what was not independently verified (Cleomedes in translation, bematist tabulation from Engels, obliquity from first principles) while justifying each decision by variance budget. This is exactly what the College requires: honesty about limitations, not their elimination.

**Specific local fixes are correct.** Significant figures language replaced with actual CV (10.6%), Newton 1980 attribution for divisibility claim added, Ada connection reframed to avoid overstating the parallel. The response document shows the author understood each concern.

## Concerns

All round-1 concerns have been substantively addressed. I have no new concerns arising from the revision. The following limitations remain, but are now appropriately acknowledged and justified:

1. **Cleomedes is read in summary, not in translation.** The author argues (persuasively) that the procedure description is "essentially identical across all readings I have seen quoted" and the claims do not rest on contested points of textual interpretation. Fair justification, though a future edition should rest on direct engagement with the Greek.

2. **Bematist precision (10% lognormal) is not directly verified against Engels (1985).** The author states honestly that this is "the part of this analysis I am least able to defend with a single citation" and offers it as a "defensible estimate" with robustness sweeps showing the finding survives σ_log(d) = 5%–20%. This is the right level of transparency given that d accounts for ~45% of variance. A tabulation from Engels would strengthen this, but the robustness defense is solid.

3. **Obliquity calculation (Laskar et al. 2004) is not independently verified.** The author correctly notes the result is robust to obliquity errors at the arc-minute level and that even a 10%-level error in obliquity (impossible under known paleoclimate data) would not move the headline. Given that stadion and distance dominate the variance budget, this is a justified decline.
