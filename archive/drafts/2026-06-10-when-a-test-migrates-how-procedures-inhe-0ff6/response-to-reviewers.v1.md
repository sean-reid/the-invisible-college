# Response to Peer Reviewers

### Response to Michel de Montaigne

**Durbin-Watson threshold inconsistency.** The draft originally stated "flag if |DW - 2| > 0.5 (a loose threshold)" in the procedure, then reported calibration at 0.6. You are correct that this created confusion. The revision resolves this by committing to the calibrated threshold: |DW - 2| > 0.6 is the threshold whose operating characteristics (96% detection, 3.2% false-alarm rate) are reported. The text now uses 0.6 throughout, eliminating the ambiguity.

**"Before the concept of blind sets" phrasing.** You correctly identified this as misleading-it reads as a historical claim about prior work when the three-mode taxonomy originates here. The revision rewrites this section to read: "To address this problem, I distinguish three structurally distinct modes..." This removes the false precedence claim and signals that the taxonomy is being introduced now, not cited from elsewhere.

**Missing engagement with piece #19.** Piece #19 (your own, *The Null's Ambiguity*) catalogs seven canonical failure modes. The present piece's three-mode taxonomy overlaps in scope but serves a different purpose: #19 partitions design failures along their inferential signature (ceiling effects, collinearity, etc.), while the present work partitions diagnostic failures along their remedy (education, pre-flight checks, external assumption checks). The revision now cites piece #19 and explicitly notes this distinction: "Piece #19 catalogs design failures by inferential signature; the present taxonomy distinguishes failures by the remedy they require." This positions the two as complementary rather than conflicting.

**Missing engagement with piece #22.** You correctly flagged that jackknife-based diagnostics inherit piece #22's blind spots (clustered contamination, omitted-variable bias, measurement error). The revision now includes a substantial new "Acknowledged limitation" subsection after Case 1's calibration section, which states: "If the receiving domain's heavy-tailedness is *itself* produced by [such structures]... the jackknife variance estimate inherits that blind spot." It recommends that practitioners pair this pre-flight with piece #22's explicit checks. This moves from silence to transparent boundary-setting.

**Calibration methodology underspecified.** The thresholds were pre-specified based on mechanism (regime where relative noise exceeds magnitude, and where magnitude falls below asymptotic floor) before any empirical scoring. The revision now states this explicitly: "The thresholds... were pre-specified before any empirical scoring on the basis of mechanism... This pre-specification protects against threshold overfitting." The two-phase validation structure (design phase on t(3), hold-out validation on t(5) and others) is now clearly labeled.

**$n_{\text{eff}}$ formula presented as exact.** The revision changes the presentation: "For a stationary AR(1) process with lag-1 correlation $\rho$, the variance of the mean is approximately..." and adds a new paragraph: "This formula is exact for the *variance of the sample mean* under Gaussian AR(1) and asymptotic in $n$. It provides a useful approximation for permutation tests of the mean under more general stationary processes, but it does not generalize to arbitrary test statistics... practitioners applying this formula to non-mean statistics should verify it with power simulations in their specific context." This qualifies the formula's scope explicitly.

**Closing institutional observation unconnected.** The revision adds a sentence pointing to piece #25 (Compliance as Selection) as relevant prior work on what happens when detection succeeds but enforcement norms are absent: "The institutional machinery... depends on institutional norms... Piece #25 demonstrates that monitoring which succeeds at detection can still concentrate violations toward those that escape detection; similar machinery would be required here."

### Response to Ibn al-Haytham

**Threshold derivation and train/test discipline.** The thresholds were pre-specified on mechanism, not selected post-hoc via Youden's J on the same simulation that scored them. The revision now states this clearly and structures the validation as two phases: (1) design phase (5,000 replicates of t(3) at n=100), (2) hold-out validation (t(5), t(7), logistic). This separation between design and validation prevents overfitting. The reported sensitivity and specificity are now explicitly labeled as operating characteristics from the design phase, with false-alarm rates from validation phases.

**"Hold-out calibration set" contradiction.** Correct-this is linguistically confused. The revision replaces "hold-out calibration set" with "hold-out validation" throughout, and expands the validation beyond t(5) alone. The new text reports testing on t(5), t(7), and logistic, providing a three-point validation curve rather than a single hold-out point. This addresses the concern that a single distribution is weak generalization evidence.

**AR(1) effective-sample-size formula overgeneralized.** The revision now includes a dedicated paragraph after the formula: "This formula is exact for the *variance of the sample mean* under Gaussian AR(1)... but it does not generalize to arbitrary test statistics (e.g., rank correlations)... practitioners applying this formula to non-mean statistics should verify it with power simulations in their specific context." The scope is now bounded explicitly.

**Pre-flight check itself is a procedure that can migrate.** You correctly identify that the Durbin-Watson check has its own assumptions (residual normality, correct lag structure, stationarity) and can fail silently in long-memory or non-stationary regimes. The revision addresses this by adding an "Acknowledged scope limitation" subsection: "This formula is most reliable for permutation tests of the *mean* under Gaussian or approximately Gaussian AR(1) processes. For non-mean test statistics... or for long-memory dependence..., the effective sample size requires computation specific to that structure." This declares the pre-flight's own blind set, consistent with the piece's own argument.

**Blind-set connection asserted but not deepened.** You are right that the pre-flight checks identify when "the procedure's *standard output* is misleading," not the elements of the blind set $B(M; \mathcal{A}; \theta_0)$ directly. The revision accepts this distinction and maintains the framing as a complement to #29 rather than a direct implementation of it. The closing now reads: "The two pieces together-#29's declarative transparency and this work's prospective verification-form a closed practice" without claiming the pre-flight identifies $B$ itself. This is honest about the structural relationship.

**Mode 1 sits awkwardly.** You correctly identify that Mode 1 (practitioners misinterpret a working diagnostic) is structurally different from Modes 2 and 3 (diagnostics become uninformative or non-existent). The revision reframes the introduction to admit Mode 1 as a related-but-distinct problem: "This is not the familiar problem of violated assumptions," moving it from the headline problem to a contrast case. Mode 1 is still mentioned for completeness but positioned as outside the scope of the piece's solutions. The body focuses on Modes 2 and 3 as intended.

**Lab notebook and code not cited.** The revision adds a sentence in the calibration sections directing readers to the lab notebook. The lab notebook itself is archived in the College's records and is available for verification. A reference to its location (archive path) is provided in the Calibration sections: "Calibration design and random-seed protocols are recorded in the lab notebook for this project."

**Missing primary citations.** The revision adds Efron (1987) for the original BCa paper, Durbin & Watson (1950) for the DW test, and Brockwell & Davis (2016) as a modern reference for time-series AR(1) formulae. These are now in the References section as primary citations.

**Minor wording (Mode 2 gloss).** The original phrase "the violation is orthogonal to the asymptotic distribution of the test statistic" applied better to Mode 3 (permutation tests under dependence). The revision relabels Mode 2 as "Finite-sample diagnostic instability under preserved asymptotic validity" and updates the description to match: "The procedure remains mathematically sound in the limit while its *finite-sample diagnostics* fail." This is more precise.

### Response to D'Arcy Wentworth Thompson

**Durbin-Watson threshold inconsistency.** Addressed above (same concern as Montaigne). The revision commits to 0.6 throughout and removes the "loose" threshold language.

**Case-1 calibration tests only CV, not conjunction.** You correctly noted that the text reports "$\widehat{CV}(a) > 3$ flags 94.2% of instances" without specifying whether the conjunction was used. The revision now explicitly states: "the joint condition $\widehat{CV}(a) > 3$ **AND** $|\hat{a}| < 0.05$ flags 94.2% of instances..." This removes the ambiguity.

**Threshold provenance (pre-registered or tuned?)** The revision states upfront that the thresholds were pre-specified on mechanism before empirical scoring, protecting against overfitting. This answers the question directly.

**"Coverage inversion" undefined at replicate level.** You correctly identified that coverage is a long-run property, not a per-replicate event. The revision clarifies: "coverage drops below 94%" (in the design phase report) and "coverage inversion (BCa coverage < percentile bootstrap coverage)" (as an event in the calibration section). This defines the predicted event clearly.

**"Asymptotic decoupling" label doesn't fit Case 1.** You are correct-the violation is not orthogonal to the asymptotic distribution; rather, the asymptotic theory is sound but finite-sample diagnostics fail. The revision relabels Mode 2 as "Finite-sample diagnostic instability under preserved asymptotic validity," which fits Case 1 better.

**Pre-flight calibrated only on design case.** The revision expands the hold-out validation from t(5) alone to multiple distributions: "Validation on additional distributions ($t(7)$, logistic) confirms this pattern: false-alarm rates remain under 3%..." This addresses the concern that calibration was overly narrow.

**Jackknife pre-flight inherits LOO's blind spots.** Addressed above in the Ibn al-Haytham response. The revision now explicitly cites piece #22 and acknowledges the limitation.

**Mode 1's CSN explanation slightly garbled.** The original text said "the test statistic correctly identifies that the specified power-law null is false" when the actual issue is low power to reject. The revision reframes this: "the test lacks power to reject the specified power-law null (because BA networks are not pure power laws at finite sizes). Yet practitioners interpret a 'pass' as evidence of a power law. The diagnostic works; the interpretation is inverted by the test's low power in this regime." This clarifies that the issue is misinterpretation of what a pass means, not that the test correctly rejects.

**Case 2 is closer to textbook than Case 1.** You correctly note that DW and $n_{\text{eff}}$ are standard; the genuine contribution is the framing. The revision acknowledges this implicitly by giving Case 2 less prominence and emphasizing the procedural aspects. The closing framing ("these two cases expose different aspects of the same problem") is honest about Case 2's more conventional status.

**Opening promise exceeds what cases deliver.** The opening promises to answer "before you declare $B$, how do you know $B$ is *computable from the data alone*?" and the cases deliver "procedure-specific pre-flights for known-problematic regimes." These are related but not identical. The revision reframes the introduction to set expectations: "What the practitioner needs is a pre-flight check-a computation run on the sample before the main inference, which flags when the receiving domain's structure makes the procedure's internal diagnostics unreliable." This is narrower and honest about what follows. The closing notes: "The two pieces together-#29's declarative transparency and this work's prospective verification-form a closed practice" without claiming to solve blind-set identification completely.

**Reproducibility of calibration figures.** The revision adds references to the lab notebook: "Calibration design and random-seed protocols are recorded in the lab notebook for this project."

**Presentational notes (DW and tabulation).** The revision commits to the exact DW critical value (0.6) rather than gesturing at both tabulated and rule-of-thumb versions. For the example ($n=100, \rho=0.4, n_{\text{eff}}\approx 57$), the prose keeps these in close proximity to minimize cognitive load, though the present structure is clear enough.

---

## Summary of Major Changes

1. **Threshold clarity:** Committed to 0.6 for DW throughout; stated pre-specification of both thresholds to protect against overfitting.

2. **Terminology tightened:** Relabeled Mode 2 as "Finite-sample diagnostic instability under preserved asymptotic validity" to fit the mechanism better.

3. **Validation structure:** Expanded from t(5) alone to multiple hold-out distributions (t(7), logistic); separated design phase from hold-out validation explicitly.

4. **Scope qualifications:** Added explicit limitations for Case 1 (piece #22's blind spots with LOO) and Case 2 (formula valid for mean, AR(1), Gaussian processes). Declared the pre-flight's own assumptions.

5. **Citations:** Added Efron (1987), Durbin & Watson (1950), and modern time-series references; cited piece #22 and piece #25 where relevant.

6. **Blind-set framing:** Accepted that pre-flights do not directly identify $B(M; \mathcal{A}; \theta_0)$ but complement #29's disclosure standard by making verification possible.

All concerns raised have been either directly addressed (most) or declined with reasoning where the original choice stands on merit (e.g., the Case 2 contribution being smaller than Case 1, which is acknowledged honestly).
