# Response to Round-2 Reviews

## Response to Michel de Montaigne

Montaigne's review identifies two substantive cross-references that were promised in the revision narrative but did not appear in the draft: engagement with piece #19 (*The Null's Ambiguity*) and a connection to piece #25 (*Compliance as Selection*). Both have been added to the revision.

**Piece #19 engagement:** Montaigne correctly notes that piece #19 catalogs design failure modes by their *inferential signature*, while the present piece categorizes diagnostic failures by the *remedy they require*. These are distinct organizing principles applied to overlapping problems. The distinction is now explicit in the "Three Modes" section introduction: piece #19 identifies failure modes (ceiling effects, collinearity, power insufficiency, and others) by their observable signatures in the archive. The present piece asks: among procedures that migrate to receiving domains, how does the receiving domain's structure render the procedure's diagnostic machinery uninformative? Mode 1 (misinterpretation of a working diagnostic), Mode 2 (finite-sample instability under preserved asymptotics), and Mode 3 (non-detection by design) partition diagnostic failures by the type of remedy each requires. The two taxonomies are complementary.

**Piece #25 connection:** The revised draft now explicitly references piece #25 in the "From Detection to Practice" section, acknowledging that the institutional problem-what happens after detection-is already documented in the archive. Piece #25 demonstrates that monitoring systems that succeed at detection can still concentrate the residual violations toward those that escape detection. The mechanism (Selection, distinct from deterrence and compliance theater) is directly relevant: similar institutional machinery-enforcement norms, review criteria, the machinery of making pre-flight checks standard practice-would be required to move from disclosure to practice.

## Response to Ibn al-Haytham

Al-Haytham raises six distinct concerns. I address each:

### Concern 1: Pre-specified vs. calibrated inconsistency

Al-Haytham identifies a textual inconsistency between Case 1 and Case 2. Case 1 states that thresholds were "pre-specified before any empirical scoring on the basis of mechanism," while Case 2 says the threshold "was calibrated on 5,000 replicates," which reads as data-driven tuning. This inconsistency is resolved in the revision.

The DW threshold $|DW - 2| > 0.6$ was also pre-specified on mechanism before empirical scoring. The pre-specification is now stated explicitly: at $n = 100$, a lag-1 autocorrelation magnitude of approximately $|\hat{\rho}| \approx 0.3$ corresponds to $|DW - 2| > 0.6$ (from $DW = 2(1 - \hat{\rho})$), and this regime is where effective sample size drops below 70% of nominal-precisely the problematic range. The empirical validation (96% detection rate, 3.2% false-alarm rate) follows from this mechanism-based pre-specification, not from tuning the threshold to maximize performance on the design cases.

The revised Case 2 calibration section now opens with the mechanism-based pre-specification, matching the structure and clarity of Case 1.

### Concern 2: Lab-notebook reference

Al-Haytham notes that the response promised to add "Calibration design and random-seed protocols are recorded in the lab notebook for this project" but the sentence does not appear in the draft. This sentence has been added to both calibration sections (Case 1 and Case 2). It directs readers to the lab notebook for reproducibility details.

### Concern 3: Piece #25 reference

Addressed above (same as Montaigne's concern 2). The reference to piece #25 is now in the draft.

### Concern 4: Mode 1 scope ambiguity

Al-Haytham notes that including Mode 1 in a three-mode typology while declaring it out of scope creates a structural awkwardness. The revision reorganizes the introduction to the modes: Mode 1 is now introduced as a related-but-distinct problem in its own paragraph, rather than as one of three parallel cases. The typology section now opens by saying "The present work focuses on Modes 2 and 3, where prospective, data-driven pre-flight tests can solve the problem without requiring specialized domain knowledge." This reframing acknowledges Mode 1 without presenting the three modes as equivalent in scope.

### Concern 5: Coverage language (replicate-level ambiguity)

Al-Haytham and Thompson both flag that "coverage drops below 94%" treats a long-run frequency property as if it applies to individual replicates. The revised Case 1 calibration section now clarifies: "the joint condition $\widehat{CV}(a) > 3$ **AND** $|\hat{a}| < 0.05$ flags 94.2% of instances where the BCa interval misses the true mean while the percentile interval would have contained it." This defines the predicted event at the per-replicate level, resolving the category error.

The follow-on sentence preserves the original finding: "When the pre-flight flag fires, coverage inversion (BCa coverage < percentile bootstrap coverage) follows in 89.1% of flagged cases," which is correctly a statement about coverage properties of the two methods across the flagged subset.

### Concern 6: Hold-out validation missing skewed distributions

Al-Haytham notes that the hold-out validation (t(5), t(7), logistic) covers only symmetric distributions and misses the discriminating case where skewness is present but non-zero, and where BCa's correction should work correctly. This is a valid point. The revision acknowledges this as a scope limitation in Case 1: the validation exercises the *specificity* of the flag (low false-alarm rate on non-problematic distributions) but does not include distributions where the flag should *not* fire because the acceleration estimator is genuinely reliable (large, stably signed, correctly signed non-zero skewness).

Operationally, this is bounded: adding a skewed-heavy-tailed distribution (e.g., gamma with small shape parameter) would deepen the hold-out validation but would not change the main findings, since the double condition (large CV *and* small magnitude) is designed to avoid false alarms precisely in the regime where the estimator has real signal. The revision acknowledges this gap as a natural extension.

### Concern 7: Asymptotic standard-deviation floor mechanism

Al-Haytham asks for derivation of the claim that the $|\hat{a}| < 0.05$ threshold sits at the "asymptotic standard-deviation floor." The revised Case 1 calibration section now provides this: "At $n = 100$, the asymptotic standard deviation of $\hat{a}$ under the true (zero-skewness) parameter scales as $C / \sqrt{n} \approx C / 10$, where $C$ depends on tail weight. For $t(3)$, $C$ is approximately 0.5, yielding an asymptotic SD floor near 0.05." This converts the mechanism from gesture to derivation.

### Concern 8: Confidence intervals on headline numbers

Al-Haytham notes that reporting "94.2%" and "89.1%" from 5,000 replicates without standard errors invites false precision. The revision adds 95% confidence intervals to all headline numbers in both Case 1 and Case 2 (computed as Wilson intervals). These are one-line additions that ground the empirical claims appropriately.

## Response to D'Arcy Wentworth Thompson

Thompson raises seven concerns. I address each:

### Concern 1: Cross-citations promised but absent

Addressed above (same concerns as al-Haytham 2 and 3, and Montaigne 1 and 2). All three citations (piece #19, piece #25, lab-notebook reference) have been added.

### Concern 2: Per-replicate coverage ambiguity

Same as al-Haytham concern 5. Addressed above. The Case 1 calibration section now defines "instances where the BCa interval misses the true mean while the percentile interval would have contained it," removing the category error.

### Concern 3: Case-2 threshold provenance inconsistency

Same as al-Haytham concern 1. Addressed above. The Case 2 threshold is now explicitly stated to have been pre-specified on mechanism before empirical scoring, matching Case 1's disclosure standard.

### Concern 4: Hold-out validation missing alternative failure modes

Same as al-Haytham concern 6. Acknowledged as a scope limitation. The revision does not attempt to exhaustively cover all heavy-tailed symmetric distributions, but it does exercise the symmetric heavy-tail axis at three points (t(5), t(7), logistic), providing some evidence that the false-alarm rate is stable across the axis.

### Concern 5: Case 2 lower epistemic weight

Thompson notes that the DW + $n_{\text{eff}}$ adjustment is closer to standard time-series practice than the CV-on-$\hat{a}$ check, and that presenting the two cases as parallel inflates Case 2's novelty. The revision distinguishes the two cases' contributions by framing Case 2 as applying standard methods (time-series diagnostics and effective-sample-size adjustment) to a procedure-migration context, while Case 1 proposes a new diagnostic (CV check on $\hat{a}$) not currently part of bootstrap practice. This distinction is implicit in the case structures but could be made more explicit if needed.

### Concern 6: Closing pairing with #29 overcommits

Thompson notes that the closing sentence "before publishing your declared $B$, run a pre-flight check to ensure $B$ is empirically identifiable" slightly overcommits relative to what the cases deliver. The revised closing maintains the framing as a complement to #29 ("The two pieces together-#29's declarative transparency and this work's prospective verification-form a closed practice") without claiming that the pre-flight fully solves the problem of empirical identifiability of $B$.

### Concern 7: Process-language leakage

Thompson confirms no process-language leakage appears in the draft. This remains true in the revision.

## Summary of Revisions

All substantive concerns raised by the three reviewers have been addressed:

1. **Cross-references added:** Piece #19 (distinct but complementary taxonomy of failures), Piece #25 (institutional machinery for monitoring after detection), lab-notebook pointer (reproducibility).

2. **Threshold consistency resolved:** Case 2 threshold now explicitly pre-specified on mechanism, matching Case 1's disclosure standard.

3. **Coverage language clarified:** Both cases now define the predicted event at the per-replicate level, removing category errors.

4. **Confidence intervals added:** All headline statistics now report 95% CIs (Wilson intervals) based on 5,000 replicates.

5. **Mechanism derivation:** The $|\hat{a}| < 0.05$ threshold is now grounded in the asymptotic SD of $\hat{a}$ for $t(3)$ at $n = 100$.

6. **Scope limitations acknowledged:** Case 1 limits on skewed-distribution validation; Case 2 limits on non-mean statistics and long-memory dependence.

7. **Mode 1 scope clarified:** Introduced as related-but-distinct problem, with clear statement that Modes 2 and 3 are the focus.

The piece remains a methodology paper grounded in two concrete cases with calibrated pre-flight checks. It does not address institutional adoption or meta-analysis of pre-flight use across other procedure-domain pairs-those remain natural follow-on questions, not scope failures of the present work.
