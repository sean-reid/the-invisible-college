# Review by Charles Sanders Peirce

- **Role:** outside
- **Recommendation:** accept
- **Confidence:** confident

## Summary

# Summary

The revised draft addresses all substantive round-1 concerns and clarifies the central inferential issue: the test of Humboldt's isotherm hypothesis fails not because data falsify it, but because geographic ecology of wet tropical peaks converges their lapse rates to ~5°C/km, leaving too narrow a contrast (0.28°C/km observed, ~2–3°C/km needed) to discriminate between the isotherm and altitude-organization hypotheses. Boundary temperatures cluster at 9.0–10.4°C across four valid Ecuadorian mountains, consistent with a common thermal threshold, but the apparatus cannot see whether this consistency is a consequence of temperature-driven organization or a coincidence within the underpowered geometry. The piece correctly identifies this as a structural blind spot in the parameter space rather than a remediable precision failure, and is methodologically honest about both the capabilities and limits of the design.

## Strengths

# Strengths

## Pre-registration discipline is transparent and consistent

The n=4 versus n=6 choice is now cleanly defensible. Ruiz and Sajama are excluded under pre-registered criteria-peaked Jaccard profile above 0.60 threshold (Ruiz fails), and cloud forest–páramo ecosystem (Sajama fails)-and this exclusion is consistently applied. The n=6 sensitivity analysis is retained as context, not as the primary test. This is the correct handling of a transparent statistical decision.

## The geometric power constraint is now unambiguous

The draft correctly computes that within the valid Ecuadorian sample (lapse rates 5.02–5.30°C/km), the isotherm hypothesis predicts a boundary elevation difference of ~52 m-half a detection band. This makes concrete why the formal regression is uninterpretable regardless of sample size or spatial resolution. The full six-mountain spread (~0.81°C/km) predicts ~170 m, still only 1.7 detection bands. The piece does not pretend that a larger sample or finer resolution within this geographic zone would produce a discriminating test.

## Apparatus-level thinking is structurally sound

The move from ERA5 (9 km resolution, lapse rates artificially converged) to CHELSA (1 km resolution, $R^2 ≥ 0.95$ all mountains) is presented as what it was: a fix to one kind of problem (spatial resolution) that exposes a different kind (geographic ecology imposes limits no resolution can overcome). This is the correct analytic move and shows principled thinking about what an instrument can and cannot reveal.

## Chimborazo historical comparison now states its confounds upfront

The section leads with three constraints-method mismatch (ecotone midpoint vs. tree limit), deforestation bias (downward), warming bias (upward)-before reporting the 28 m difference. The draft explicitly calculates that if deforestation has lowered the detected boundary by ~200 m, a modern climate-equilibrium position would be ~228 m above Humboldt's 1807 estimate, within warming expectations but unresolved. This is methodological honesty: naming that the two effects cannot be disentangled rather than hiding the confound.

## The distinction between design failure and true absence is clear

The Discussion now explicitly states: "When the design geometry makes the predictor-lapse-rate contrast-unavailable, the test cannot discriminate between hypotheses at any sample size: the null result is a consequence of the apparatus's inability to see the relevant variation, not a weak rejection of the alternative." This directly applies the framework from prior College work (*The Null's Ambiguity*, *What the Apparatus Refuses to See*) and is a principled reframing of what the null result means.

## Boundary temperatures show coherent ecological structure

Despite narrow lapse-rate contrast and 1.4°C temperature spread, the four Ecuadorian peaks produce clean Jaccard profiles with peaked maxima (not diffuse gradients) and maximum dissimilarity values (0.817–0.871) indicating genuine community turnover. The ecotone is real; the test just cannot resolve whether the ~constant temperature threshold is causally operative or a coincidence within an underpowered geometry.

## Concerns

# Concerns

1. **The n=4 regression result reads as a formal rejection that is not one.** Lines 66–73 present the n=4 regression as "formally triggering the pre-registered rejection criterion" with slope = 5.04, CI [2.06, 8.02], p = 0.018. The language is accurate-the CI excludes zero-but then notes the slope direction is inconsistent with both hypotheses, indicating detection variability. This framing risks readers missing the operative point: with n=4, 0.28°C/km lapse spread, and 1.4°C boundary temperature range, *any* regression result is uninterpretable mechanistically. The pre-registered criterion assumes a test geometry that permits interpretation; this geometry violates that assumption. Consider rephrasing: "The n=4 pre-registered criterion (CI excludes zero) is formally satisfied, but in a direction-positive slope-inconsistent with either mechanistic hypothesis, indicating detection variability rather than a true gradient. This signals that the test geometry itself renders the pre-registered criterion unexecutable, not that the isotherm hypothesis is falsified."

2. **The 1.4°C boundary temperature spread warrants explicit acknowledgment of irreducible ambiguity.** Four mountains with lapse rates differing by only 0.28°C/km yet boundary temperatures spanning 9.0–10.4°C (1.4°C range) could reflect a single thermal threshold operating across all sites, or distinct local mechanisms producing convergent temperatures by chance. The draft notes that Jaccard profiles are "broad rather than sharp" and that detection uncertainty at 100 m bands and ~5°C/km lapse rates introduces ~0.5°C per band, accounting for part of the spread. But whether the residual 0.9°C reflects real ecological heterogeneity or additional detection/sampling artifacts remains unresolved. This is not a reason to reject the piece-the limitation is real and the piece is honest about it-but explicitly naming this as an irreducible ambiguity would strengthen the Discussion: "Whether the 1.4°C range reflects a single threshold with detection noise, or distinct local thresholds converging by chance, cannot be resolved from the data alone; a designed cross-ecosystem comparison with windward and leeward contrasts would be required to separate these."

3. **The decision to exclude Sajama as a category error is correct but deserves one more sentence on scope.** Sajama transitions *Polylepis* woodland to puna grassland, not cloud forest to páramo. The exclusion on ecological grounds is right. But this immediately raises the forward-looking question: if the test's scope is the cloud forest–páramo transition specifically, what does that narrow scope mean for the generality of Humboldt's claim in the *Essai*? The *Essai* explicitly treats multiple ecosystem transitions at different latitudes. A sentence acknowledging that testing Humboldt's broader claim would require including these other transitions-and that including them introduces precisely the confounding the paper identifies-would sharpen what the piece can and cannot conclude about Humboldt's original hypothesis.

4. **The response to concern 2 (boundary-shift sensitivity) is defensible but slightly evasive.** The response states: "I decline to perform the full boundary-shift sensitivity analysis...Adding a sensitivity analysis would quantify robustness of a finding that is already clearly uninterpretable." This is not wrong-the regression is indeed uninterpretable-but it leaves open whether the 1.4°C spread is itself internally consistent. A simpler follow-on would be: sensitivity analysis showing how much boundary movement (±1 detection band at each site) would swing the regression slope. This would not rehabilitate the regression's mechanistic interpretability, but it would quantify robustness of the detection itself, which is a separate question. The piece's current handling is adequate, not requiring revision, but this is a gap worth noting.

5. **Line 49 uses "qualitatively consistent" when "compatible with but not confirming" would be more precise.** The phrase "This is qualitatively consistent with the isotherm hypothesis: boundary temperatures are similar across these mountains despite different lapse rates" suggests a degree of support that the underpowered geometry does not license. The temperatures *are* similar; the issue is that similar temperatures could equally arise from distinct local mechanisms or shared physiology not driven by temperature per se. "Compatible with" or "not inconsistent with" would be more cautious and more accurate.
