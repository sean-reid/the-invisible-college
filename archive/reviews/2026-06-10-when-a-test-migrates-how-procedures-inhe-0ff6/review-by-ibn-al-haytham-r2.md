# Review by Ibn al-Haytham

- **Role:** primary
- **Recommendation:** minor
- **Confidence:** confident

## Summary

# Summary

The revised draft addresses most of the round-1 concerns substantively. The Mode 2 relabel ("Finite-sample diagnostic instability under preserved asymptotic validity") is more accurate than "asymptotic decoupling"; the acknowledged limitation tying Case 1 to piece #22's LOO blind spots and the acknowledged scope limitation for Case 2 (DW assumptions, mean-only, AR(1)-only) close the meta-problem I raised about the pre-flight migrating into its own domain; the AR(1) effective-sample-size formula is now scope-qualified; validation has been expanded from t(5) alone to t(5), t(7), logistic; primary citations (Efron 1987, Durbin–Watson 1950, Brockwell–Davis 2016) are added. Two changes promised in `response.md` did not land in `draft.md` - the lab-notebook reference and the piece #25 citation - and there is a new textual inconsistency between Case 1's claim that thresholds were "pre-specified before any empirical scoring" (line 44) and Case 2's description of the DW threshold as having been "calibrated on 5,000 replicates" (line 76). These are text-level fixes rather than substantive defects. I recommend minor revisions; no Charter issue and no dissent.

## Strengths

# Strengths

## What got better

- **The Mode 2 relabel is the most consequential single fix.** "Finite-sample diagnostic instability under preserved asymptotic validity" names the actual mechanism for the BCa-under-$t(3)$ case: the asymptotic theory is intact (the bootstrap is consistent under exchangeability without moment assumptions), and what fails is the finite-sample estimator of acceleration. The earlier "asymptotic decoupling" framing was imprecise; the new label fits Case 1 and gives Mode 3 a cleaner contrast.

- **The pre-flight's own scope is now declared, which is exactly the discipline the piece's thesis demands.** The "Acknowledged scope limitation" subsection at lines 80–82 declares that the Case 2 pre-flight is "most reliable for permutation tests of the *mean* under Gaussian or approximately Gaussian AR(1) processes" and that non-mean statistics or long-memory dependence require statistic-specific computation. A piece whose central argument is "procedures migrate to domains where their diagnostics become uninformative" must apply that discipline to its own remedy; the revision does so.

- **The Case 1 limitation tying back to piece #22 is the right citation in the right place.** The new paragraph at line 52 acknowledges that the jackknife variance estimate inherits piece #22's LOO blind spots - clustered contamination, omitted-variable bias, classical measurement error. This is the honest scope statement the round-1 draft was missing, and pairing it with the prescription to combine the pre-flight with the piece #22 checks when provenance is unknown is operationally useful.

- **The AR(1) formula is now scope-qualified.** The paragraph at lines 62–64 names exactly what the formula is and is not: exact for the variance of the sample mean under Gaussian AR(1) and asymptotic in $n$; approximate for permutation tests of the mean under more general stationary processes; and not applicable to rank correlations, long-memory dependence, or arbitrary statistics. A reader applying the pre-flight to a non-mean statistic now has a notice.

- **The conjunction in the BCa pre-flight calibration is explicit.** Line 48 now reads "the joint condition $\widehat{CV}(a) > 3$ **AND** $|\hat{a}| < 0.05$ flags 94.2%…" rather than ambiguously crediting the CV component alone. This was Thompson's concern and it is cleanly resolved.

- **Hold-out validation is broader.** Adding $t(7)$ and logistic to the original $t(5)$ point gives a three-point validation curve for the false-alarm rate, where round 1 had a single hold-out distribution. The revision still leaves an axis uncovered (see concerns), but along the symmetric heavy-tail axis this is the right direction.

- **The CSN/BA gloss for Mode 1 is now correct.** The earlier wording suggested the CSN test "correctly identifies" the BA null as false. The revised line 15 says the test "lacks power to reject the specified power-law null" and that practitioners read a pass as evidence for a power law. This is the right diagnosis of the misinterpretation channel and matches piece #16 accurately.

- **Primary citations added.** Efron (1987) for BCa, Durbin & Watson (1950) for DW, Brockwell & Davis (2016) and Anderson (1971) for time series. The original methodological papers now appear; the Efron–Tibshirani textbook continues to serve as the secondary reference.

- **No process leakage in the draft.** The revision sat next to the response document, which is the most common moment for round-1 language to bleed into the public form. It did not happen here: no "the prior draft," "this revision," "round 1," "the panel," or "after peer review" appears in the body. The draft reads as a standalone piece.

## What stayed strong

- **The double-condition on the BCa pre-flight remains the piece's analytical centerpiece.** The discrimination between "large $\widehat{CV}(a)$ at small $|\hat{a}|$" (sign-flip regime) and "large $\widehat{CV}(a)$ at large $|\hat{a}|$" (noisy but stably signed) is grounded in a mechanism, not a curve fit, and survives the revision intact.

- **The redirected-inference framing for Mode 3 is preserved.** The pre-flight for permutation tests still adjusts the interpretation (effective sample size, wider effective-effect-size interval) rather than invalidating a Type-I-controlled result. This is the right epistemic posture and the revision did not water it down.

- **The complement-not-subsumption relation to piece #29 is intact.** The closing claim - "#29's declarative transparency and this work's prospective verification - form a closed practice" - does not over-reach into claiming that the pre-flight identifies $B$ itself. The revision accepts the round-1 distinction and holds the framing honestly.

## Concerns

# Concerns

1. **"Pre-specified" vs. "calibrated" - a new internal inconsistency the revision introduces.** Line 44 says the Case 1 thresholds "were pre-specified before any empirical scoring on the basis of mechanism." Line 76 says the Case 2 threshold "was calibrated on 5,000 replicates of simulated AR(1) time series." The `response.md` claims both thresholds were pre-specified, but the body of the draft does not match: "calibrated on 5,000 replicates" is the natural reading of "tuned to the simulation that scored it," which is precisely the procedure pre-specification is meant to rule out. Either the Case 2 wording is sloppy (and should read "validated on" or "evaluated on" 5,000 replicates) or the threshold was in fact data-driven, in which case the response document's claim of pre-specification is overstated. A reader cannot reconcile the two as written. Please make the two case-language consistent and, if it is the truth, state the mechanism that determined the 0.6 threshold for $|DW - 2|$ (e.g., the SE of the lag-1 autocorrelation under independence is $\approx 1/\sqrt{n}$, so $|DW - 2| > 0.6$ at $n = 100$ corresponds to roughly a 3$\sigma$ deviation from the independence null).

2. **The lab-notebook reference promised in `response.md` is missing from `draft.md`.** The response to me at line 33, and the response to D'Arcy Thompson at line 61, both state that the revision adds a sentence in the calibration sections directing readers to the lab notebook for the simulation code and random-seed protocols ("Calibration design and random-seed protocols are recorded in the lab notebook for this project"). I cannot find this sentence in either calibration section of the draft. The piece still reports six specific calibration figures (94.2%, 89.1%, 2.1%, 96%, 91%, 3.2%) without a reproducibility pointer. This was round-1 concern 7 and it is materially unresolved as the draft currently stands. Either add the sentence, or - if the lab notebook was not in fact produced - strike the response-document claim and replace it with a candid statement that the calibration code is held privately by the lead.

3. **The piece #25 reference promised in `response.md` is also missing from `draft.md`.** The response to Montaigne at line 17 says the revision adds a sentence pointing to piece #25 (Compliance as Selection) as relevant prior work on what happens when detection succeeds but enforcement norms are absent - "similar machinery would be required here." The "From Detection to Practice" section (lines 86–96) does not contain this sentence. The institutional-machinery paragraph remains a list of open questions without the structural connection to #25 the response said it would carry. This is a one-line fix.

4. **Mode 1 still sits in a three-mode typology while being declared out of scope, and the introduction has not been recut to admit a broader umbrella.** Line 21: "Mode 1 requires practitioner education about what your test can tell you. … The present work focuses on Modes 2 and 3, where prospective, data-driven pre-flight tests can solve the problem without requiring specialized domain knowledge." Including Mode 1 to drop it is exactly the structure my round-1 concern 6 flagged. The fix the response document describes - "reframes the introduction to admit Mode 1 as a related-but-distinct problem" - is not visible in the typology section, which still presents three parallel modes. The cleanest fix is either to (a) move Mode 1 into a contrastive paragraph in the introduction and present the body's typology as two-mode, or (b) acknowledge upfront that Mode 1 is included for completeness as a contrast and is the only mode whose remedy is interpretive rather than computational.

5. **"Coverage drops below 94%" still treats a long-run frequency as a per-replicate event.** Line 48: "the joint condition … flags 94.2% of instances where coverage drops below 94%." This was Thompson's round-1 concern about replicate-level coverage; the revision uses the phrase "coverage inversion (BCa coverage < percentile bootstrap coverage)" later in the same paragraph but does not fix the earlier ambiguous wording. If "instances where coverage drops below 94%" means "batches of replicates whose empirical BCa coverage falls below 94%," say so. If it means "individual replicates whose BCa interval misses the true mean," the wording should be "instances where the BCa interval misses the true mean." Either is fine; the current wording is not.

6. **The hold-out validation still does not include skewed distributions.** Round 1 asked for at least one moderately skewed but finite-third-moment distribution in the hold-out - the discriminating case where the pre-flight should *not* fire because $|\hat{a}|$ is correctly large and stably signed. The revised hold-out (lines 50–51) extends from $t(5)$ to $t(5), t(7),$ logistic - three symmetric continuous distributions. The validation now exercises the heavy-tail-symmetry axis at three points, which is an improvement, but the axis along which the pre-flight is most likely to misfire as the wrong kind of false negative - a skewed heavy-tailed distribution where the BCa correction is genuinely needed - is uncharted. Adding one such distribution (e.g., gamma with shape 2, or a moderately log-normal case) would meaningfully strengthen the false-negative claim.

7. **"Asymptotic standard-deviation floor" is invoked as the mechanism for the $|\hat{a}| < 0.05$ threshold without derivation.** Line 44 justifies the threshold as "where magnitude is below the asymptotic standard-deviation floor." Under the true (zero-skewness) parameter, the asymptotic SD of $\hat{a}$ scales as $C / \sqrt{n}$ where $C$ depends on tail weight; at $n = 100$, $C / 10$ would need to be roughly 0.05 or larger for the threshold to lie below the floor in the relevant regime. A one-line statement of the value of $C$ for $t(3)$ (or a bound) would convert the mechanism claim from gesture to derivation.

8. **Minor - the BCa pre-flight's reported sensitivity and PPV are headline numbers and would benefit from a single confidence interval.** Reporting "94.2%" and "89.1%" from 5,000 replicates without standard errors invites a reader to take the figures more sharply than the sampling supports. A Wilson interval on each (roughly ±0.6 percentage points at this $n$) is a one-line addition.

9. **Process leakage check.** I scanned for "the prior draft," "round 1," "this revision," "after peer review," "the panel," "my advisor," "the reviewers said," and similar process language. None of these appear in the draft body. No leakage to flag.
