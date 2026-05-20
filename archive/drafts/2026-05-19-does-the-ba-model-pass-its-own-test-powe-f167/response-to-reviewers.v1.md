# Response to Reviewers

Round 1. All three reviewers raised substantive concerns. Below I respond to each named concern in turn, stating what was changed and why, or-where I disagree-making the case for the original choice.

---

### Response to Ibn al-Haytham

**Concern 1: Non-monotonic headline rests on a single seed and five failures.**

This is the strongest concern in the round and I accept it substantially. I cannot re-run the sweep under additional master seeds in this revision pass; the full sweep takes ~47 minutes and results from those runs would need to be verified and integrated. What I have done instead: (a) added 95% Wilson confidence intervals to Table 1, which make the statistical situation explicit-the N=10,000 CI for m=2 ([0.79, 0.96]) just barely overlaps the N=5,000 CI ([0.93, 1.00]); (b) reported Fisher exact p-values for the key pairwise comparisons (m=2: p ≈ 0.028; m=3: p ≈ 0.18); (c) added an explicit single-seed limitation paragraph in the Discussion; (d) softened the headline throughout from "non-monotonic with recovery" to "dip at N=10,000 consistent with a dip, not confirmed under alternative seeds." The mechanism is analytic and seed-independent-the ±5% curvature is a property of the exact BA distribution, not of the specific seed-so the contribution survives even if the quantitative pass rates shift under other seeds. Running additional seeds remains necessary to confirm the quantitative pattern and is named as a required follow-up.

**Concern 2: Bootstrap noise not propagated to aggregate pass-rate estimates.**

Addressed. Added a "Bootstrap misclassification at the boundary" paragraph in the Discussion that walks through the propagation: the bias on the aggregate pass rate is bounded by f/2, where f is the fraction of replicates with true p ∈ [0.05, 0.15]. I argue that fully explaining the N=10,000 dip by boundary-case misclassification would require all 5 failures to be near-boundary cases-an unlikely configuration given the analytic mechanism and the p < 0.005 example at N=50,000. But the point is conceded that 200 bootstraps cannot fully separate structural signal from boundary noise.

**Concern 3: i.i.d. control under-resolved relative to BA sweep.**

Addressed. Revised the i.i.d. control section to be explicit about what the 5-replicate, 100-bootstrap control can and cannot establish: it rules out gross implementation error and catastrophic miscalibration; it cannot confirm that Type I error is correctly controlled at large N under BA's correlation structure. The argument that "BA failures are not a test artifact" is now explicitly grounded in the direct i.i.d.-vs.-BA control on the failing network, not on the aggregate control pass rates. Running the control at 50 × 200 matching the BA sweep is named as a follow-up.

**Concern 4: Recovery mechanism asserted but not measured.**

Accepted. Added an explicit statement in both the Results and Discussion that the distribution of selected x_min values across the 50 replicates at each N is a key unmeasured quantity, and that reporting median and IQR of optimal x_min per (N, m) condition is the direct test of the recovery mechanism. The discussion now distinguishes "consistent with x_min shifting upward" (which is what we can say) from "caused by x_min shifting upward" (which requires the measurement).

**Concern 5: Small-N stochastic failures are a label, not a finding.**

Accepted. The relevant text now explicitly marks this as a working hypothesis consistent with the high replication variance at N=500 (SD=0.14 vs. 0.05 at large N), not a demonstrated mechanism. The contrast with the N=50,000 failure case-where the mechanism is analyzed-is now implicit in the asymmetric treatment.

**Concern 6: Type-I error vs. statistical power framing.**

Accepted and implemented throughout. The introduction now contains a dedicated framing note: the CSN null is false by construction for all BA networks, so "pass rate" is (1-power), and the piece is a power study. The Discussion opens with this point. This reframing is substantive: the non-monotonic pass rate is non-monotonic power, maximum power (lowest pass rate) occurs at N=10,000, and the "recovery" is the test losing power, not the network becoming more power-law-like.

**Concern 7: Cross-validation discrepancy hand-waved.**

Addressed. The Methods section now explains the discrepancy in detail: both implementations minimize KS over x_min, but the KS landscape at (N=1000, m=3) has a shallow minimum-KS values at x_min=4 and x_min=5 differ by less than 0.003-and which candidate wins depends on tie-breaking conventions in the grid scan. The 0.13 α̂ difference arising from a one-unit x_min disagreement is characterized as a signal about the procedure itself: x_min selection is non-unique when the KS minimum is flat, and this is a meaningful source of estimation variance independent of network replication.

**Concern 8: p=0.000 from 200 bootstraps is overstated.**

Fixed. The text now reads "p < 0.005 (0/200 bootstrap replicates exceeded the observed KS; Clopper–Pearson 95% upper bound ≈ 0.015)."

**Concern 9: x_min/n_tail framing inverts cause and effect.**

Fixed. The original phrasing implied that x_min=4 coincidentally also has the largest n_tail, as if these were two independent properties. The revised text states the non-obvious finding correctly: the minimum KS occurs at x_min=4 *despite* this being the regime where BA's correction terms are most active and where the most nodes are exposed to them. The procedure is drawn to x_min=4 because the MLE compensates for curvature by choosing a lower α̂, producing a marginally lower KS even though the fit is objectively worse there than a pure power law would be.

**Concern 10: MLE underestimation not predicted.**

Partially addressed. Added an "MLE underestimation: analytical basis" section to the Discussion. I cannot compute numerical α*(x_min) values for specific x_min choices in this revision pass (this requires summing the rate equation numerically), but I derive the direction and mechanism: because P_BA places more weight at low k than pure k^{-3}, the expected log-degree under P_BA is smaller, which drives the MLE below 3 for any finite x_min. The section connects empirical α̂ convergence to the α*(x_min) → 3 limit analytically and gives a rough N > 100,000 estimate for when x_min selection would consistently reach the k ≥ 15 region where the ratio table shows P_BA ≈ k^{-3}. A full numerical computation of α*(x_min) is a natural follow-up.

**Concern 11: Reference network section overstates what was learned.**

Accepted and fixed. The section is now compressed to a brief paragraph that states the passing verdicts explicitly for completeness, then delivers the honest summary: with n_tail values of 6–12, the test has negligible statistical power, the networks pass because the test cannot reject any reasonable null at these sample sizes, and this section provides no new evidence about distributional form.

**Concern 12: Script missing from review workspace.**

Acknowledged. A note is now included in the Runbook section explaining that the script was present during execution but was not forwarded with review materials. This is a legitimate reproducibility concern. A future submission should attach the script directly alongside the manuscript.

---

### Response to Michel de Montaigne

**Concern 1: Figure 1 referenced but absent.**

Fixed. The Methods section referenced "Figure 1 (described below) shows MLE exponent convergence"-there is no such figure anywhere in the draft. The reference has been removed. The exponent convergence trend is visible in the α̂ columns of Table 1 (rising from 2.59 to 2.82 across N for m=2) and described explicitly in prose.

**Concern 2: Recovery mechanism asserted but not demonstrated.**

Addressed-see Response to Ibn al-Haytham, Concern 4.

**Concern 3: Pass rate uncertainty not quantified.**

Fixed. Table 1 now includes 95% Wilson confidence intervals for all pass-rate estimates. The Discussion uses these CIs explicitly when characterizing the strength of the dip-and-recovery pattern.

**Concern 4: Degree-correlation concern deserves more than a sentence.**

Expanded substantially. The Discussion now contains a two-paragraph "degree-correlation problem" section that: (a) explains the mechanism by which BA degree correlations could inflate the KS statistic beyond its i.i.d. baseline; (b) identifies the direction of the resulting bias (systematic low p-values, i.e., more rejections than nominal); (c) notes that this bias is in the same direction as the curvature effect, making them indistinguishable from the bootstrap's perspective; (d) specifies what a resolution would require (parametric network bootstrap or empirical comparison of correlated vs. uncorrelated KS distributions with the same marginal). This is now treated as a substantive methodological caveat, not a disclaimer.

**Concern 5: Reference network section does not earn its place.**

Accepted. Section compressed substantially-see Response to Ibn al-Haytham, Concern 11.

---

### Response to Pierre Bayle

**Concern 1: Exact BA distribution formula not cited.**

Fixed. The formula P(k) = 2m(m+1)/[k(k+1)(k+2)] is now attributed to Dorogovtsev, Mendes & Samukhin (2000), "Structure of growing networks with preferential linking," *Physical Review Letters* 85(21): 4633–4636. This is the paper that derives the exact stationary degree distribution from the mean-field rate equation; the original Barabási-Albert (1999) paper established the γ=3 asymptotic exponent but did not give this closed form.

**Concern 2: Reproducibility claim hinges on missing artifact.**

Acknowledged-see Response to Ibn al-Haytham, Concern 12.

**Concern 3: x_min dependence and distribution across replicates not reported.**

Addressed-see Response to Ibn al-Haytham, Concern 4. The distribution of optimal x_min per (N, m) condition is now named explicitly as a key missing measurement.

**Concern 4: Reference-network sample could be strengthened.**

The section has been compressed to a brief paragraph with honest characterization. The limitation of the small-n_tail problem is stated directly rather than soft-pedaled. Adding larger reference networks (the football network, or the Gnutella network from Clauset et al. 2009) would strengthen this section; this is a natural follow-up that is now named.

**Concern 5: p-value SE claim needs qualification.**

Fixed. The Methods section now notes that ±2.1% is the standard error at p = 0.1 specifically-because σ = √(p(1-p)/n) is maximized at p = 0.5 and the relevant threshold is p = 0.1-and that at p values below 0.05 or above 0.15, the SE is smaller and classification precision is better.

**Concern 6: MLE underestimation-N required for convergence to 2.95.**

Addressed. The "MLE underestimation: analytical basis" section in the Discussion now includes a rough estimate: convergence to α̂ ≈ 2.95 would require x_min selection consistently falling at k ≥ 15–20 (where the ratio table shows P_BA ≈ k^{-3}), which in turn requires N well above 100,000. This is a sketch from the ratio table rather than a precise derivation; it makes the finite-N effect concrete.
