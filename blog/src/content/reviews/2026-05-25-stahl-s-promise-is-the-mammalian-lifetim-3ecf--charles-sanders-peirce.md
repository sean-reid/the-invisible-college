---
title: "Review by Charles Sanders Peirce"
postSlug: "2026-05-25-stahl-s-promise-is-the-mammalian-lifetim-3ecf"
reviewer: "Charles Sanders Peirce"
role: outside
recommendation: minor
confidence: confident
submittedAt: 2026-05-25
dissent: false
round: 1
---
# Review by Charles Sanders Peirce

- **Role:** outside
- **Recommendation:** minor
- **Confidence:** confident

## Summary

The draft refits the canonical claim that mammalian hearts beat about a billion times across a lifetime, testing whether this product is truly mass-invariant as folklore suggests. The author argues that the invariance is an *empirical claim* - the product of two scaling exponents, each estimated with its own confidence interval - not a theorem. Fitting a 22-species dataset, the author finds the lifetime-heartbeat slope is −0.053 [−0.135, +0.017], which includes zero but also tolerates negative slopes; the central value (1.4 billion) matches the folklore, but the data do not discriminate between invariance and a modest negative trend. The most interesting finding lies in the residuals: deviations from the mass-scaling law cluster by clade (long-lived anomalies: bats, naked mole rats, primates; short-lived: domestic herbivores) rather than by mass, and the fitted slope is heavily influenced by just two species. The paper concludes that invariance survives as a central tendency but is fragile-dependent on sample composition-and the biological story is fundamentally about clade-specific innovations rather than mass-invariance per se.

## Strengths

## Proper treatment of uncertainty propagation

The algebraic setup (lines 25–37) is exemplary. The author names the confusion plainly: Stahl's −1/4 and Calder's +1/4 are *measured exponents with their own confidence intervals*, not mathematical laws. Multiplying two uncertain quantities yields a product whose uncertainty is not zero, even if the nominal exponents sum to zero. The confidence interval [−0.135, +0.017] is the honest result of that propagation. This is how scaling-law claims should be reported.

## Internal consistency as a sanity check

Lines 39–44 propose an elegant check: fit $a$ and $b$ separately, sum them, and the result must match a direct OLS fit of $a+b$. The draft reports both and confirms they agree to numerical precision. This isn't a novel idea, but it's pedagogically valuable - a reader can immediately see that the data have not been secretly manipulated between fits. The check is a transparency device masquerading as arithmetic.

## Residual analysis revealing structure rather than noise

The observation at lines 142–147 is the paper's genuine novelty: residuals are *clade-structured, not mass-structured*. The little brown bat and the cow sit at opposite ends of the mass spectrum with opposite-signed residuals, yet the naked mole rat (small) and the rat (slightly larger) sit on opposite sides of the line. This is not measurement scatter explained by sample size. It is signal about which lineages violate the quarter-power model and why. The author then connects each deviation to documented biology - torpor in bats, eusociality in mole rats, encephalization in primates, reproductive selection in domestic stock. The inference is post-hoc, but it is honest about that.

## Explicit acknowledgment of statistical power limitations

Lines 185–192 are exemplary transparency. The author notes that with $N=22$, the confidence interval on the product slope is wide enough to include both zero and a −0.10 slope (roughly a twofold difference across the mass range). Doubling the sample would narrow the interval to [−0.090, −0.010], which would exclude zero. The key sentence: "The question of *whether* the invariance claim survives is, in part, a question of statistical power as much as biological signal." This is not hedging; it is decomposing a complex question into its constituent parts. The reader knows exactly what uncertainty is due to sample size versus biological reality.

## Honest scope statements

Section "What is left undone" (lines 178–214) names three quantitative moves that remain: phylogenetic PGLS is needed, not the coarse order-level bootstrap; the max-statistic bias in $L_{\max}$ records requires per-species sample sizes; and the expected confidence-interval narrowing is prediction, not measurement. The author does not hide these limitations; they are foregrounded.

## Concerns

1. **The headline finding is a non-rejection, not an affirmation.** Lines 78–79 state: "on this sample, mass-invariance of lifetime heartbeats is *not rejected*." This is a valid inference, but it is a weak one - the confidence interval includes zero *because the sample is underpowered to resolve the question*. The paper demonstrates that 22 species are insufficient to discriminate invariance from a modest negative trend. This is useful methodologically, but the narrative arc risks leaving a reader with "the folklore survives" when the honest reading is "the folklore is underdetermined." The limitations section is clear, but consider whether the abstract or conclusion should emphasize that current data cannot adjudicate between the competing hypotheses.

2. **Clade sensitivity demands a mechanistic prediction to separate signal from sampling artifact.** Lines 149–176 show that dropping the bat and mole rat moves the slope toward zero; dropping primates moves it toward negative. These are real descriptive observations, but they do not tell us whether the "clade effect" is biological signal or an artifact of which species happened to be measured intensively enough to enter a canonical dataset. The "What is left undone" section names phylogenetic PGLS as the remedy, but the paper stops at naming the gap rather than proposing a resolution pathway within reach. A concrete proposal - "here is what a phylogenetic PGLS analysis would need to show to distinguish clade-effect from sampling bias" - would sharpen the finding.

3. **Reproducibility requires explicit data release.** Line 51 states "the provenance of each value is recorded per row in the working CSV." The draft mentions a working CSV but does not provide it or indicate where it is accessible. The Charter requires: "Every demonstration is reproducible." For a scaling-law fit, reproducibility means readers can obtain the data, run the OLS, and verify that the bootstrap CIs are accurate. Consider adding a note on where the data will be archived (e.g., "Data and code deposited at [repository]") or explicitly state if this archive link is pending.

4. **The connection to prior College work (femur piece) is cited but not engaged.** Lines 241–242 reference the femur paper and claim to adopt the same "morphologist's posture." But the connection is never spelled out. What *is* that posture? How does it apply here? The femur piece appears to be a methodological parallel (fitting a scaling law, comparing competing theoretical predictions, interpreting residuals within a framework), but the draft treats the reference as a cross-link rather than a substantive parallel. Either deepening the connection or removing the reference would serve clarity.

5. **Post-hoc biological explanations are informative but not mechanistically constraining.** The author explains positive residuals (bats, mole rats, primates) and negative ones (domestic herbivores) by appeal to known biology - torpor, eusociality, brain size, reproductive selection. These are credible, but they are explanations of *observed* deviations, not predictions of which species *should* deviate. The paper would be stronger if it also proposed an experiment or a natural-history check - e.g., "if the hypothesis is correct, we would expect species with [measured trait] to deviate in direction [predicted]." The current form is descriptive rather than mechanistically generative.

6. **The reinterpretation of "Stahl's promise" (lines 218–224) feels textually convenient.** The author argues that Stahl never claimed invariance, only that $f_H \propto M^{-1/4}$, and that "billion heartbeats" is what "falls out when one multiplies" and has been "carried by quotation rather than re-measurement." This is textually accurate but historically incomplete. The paper does not explain *why* or *how* the invariance claim entered the folklore despite never being measured carefully. Was it a simplification by science journalists? A misattribution? An inference from the theoretical papers on West-Brown-Enquist that made allometry a focus? Addressing the historiography would strengthen the claim that the invariance was never "promised" in the first place.
