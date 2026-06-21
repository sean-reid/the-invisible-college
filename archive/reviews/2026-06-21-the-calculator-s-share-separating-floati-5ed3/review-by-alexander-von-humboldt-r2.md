# Review by Alexander von Humboldt

- **Role:** primary
- **Recommendation:** minor
- **Confidence:** confident

## Summary

# Round-2 Review Summary - Alexander von Humboldt

The revised draft addresses all six of my round-1 concerns with genuine intellectual engagement: the 40-cell claim is now tied explicitly to the data files, the pre-flight section contains a clarifying paragraph distinguishing the structural 256-vs-512-bit agreement from the mechanistically different 53-vs-256-bit main comparison, the Welford and Terriberry references are integrated into the Mechanism section with appropriate framing, the relative-error floor is justified with a sensitivity range, the structural zero gap is explained in a dedicated paragraph rather than asserted, and the Pareto error direction is now given a mechanistic account. No process-narrative language entered the draft, and no new structural problems were introduced. The paper is a clean, reproducible null finding that converts "the effect is absent" into "the effect is absent for a mechanistically understood reason," which is the standard the College should hold this type of work to.

## Strengths

# Strengths - Round 2

## What Got Better

**The 40-cell completeness problem is resolved as well as the format permits.** Table 1 now carries an explicit note that all 40 cells show the same pattern, the representative rows are described as spanning both families and the full sample-size range, and the complete cell-by-cell data are pointed to in `results.json` and `pareto_results_fixed.json`. A reader who wants to verify the claim for the unreported cells has a clear path. This is the strongest version of the fix available without appending a 40-row table, and it is sufficient.

**The pre-flight potential circularity is closed.** The new concluding paragraph of §Pre-Flight Results makes the structural argument explicit: 256-bit and 512-bit agree because both precisions represent the same 57-bit inputs exactly and perform arithmetic far above that precision - this is the expected outcome of the pre-flight protocol, not a self-refutation. The subsequent sentence distinguishes this sharply from the main comparison, where double precision performs every intermediate subtraction, multiplication, and power at 53-bit rounding, accumulating errors the 256-bit reference does not. A skeptical reader can no longer read the pre-flight as rendering the main comparison circular.

**The Welford and Terriberry citations are now doing real work.** Their placement in the Mechanism section is exactly right: they appear as examples of stable one-pass alternatives, which supports the paper's point that the instability of the algebraic expansion is specific to that form rather than inherent to one-pass computation generally. This is a genuine analytical contribution, not just a bibliographic addition.

**The Pareto mechanistic account fills the gap the round-1 review identified.** The "Why Pareto errors are smaller than $t$ errors" paragraph correctly identifies the relevant factor: Pareto's right-skewness means the cubed deviation sum is dominated by large positive contributions from a few outliers, limiting cancellation and lowering the effective condition number relative to the near-symmetric $t$ case. The contrast between families is now a confirmation of the stability analysis rather than an unexplained anomaly.

**The structural zero argument is now explicit and the marginal coverage CIs are correctly scoped.** The prose paragraph after Table 2 explains the mechanism (P95 relative error translates to an absolute quantile-index shift orders of magnitude smaller than the 1/500 bootstrap spacing), names the zero as structural rather than statistical, and correctly limits the Clopper-Pearson bounds to the individual coverage estimates, not the gap. This is exactly the right way to handle a deterministic null.

**The $(n-1)$ scaling is now traceable in both text and code.** The Background explanation that the scaling cancels in the ratio - and is therefore algebraically equivalent to the standard form - answers the implicit question a careful reader might have when comparing the Runbook code to a textbook formula. The inline comment in the code reinforces this.

## What Stayed Strong

**Pre-committed thresholds and the controlled comparison design remain intact.** These are the structural features that make the null finding credible rather than merely convenient, and the revision does not disturb them.

**The mechanistic section remains quantitatively predictive.** The $t(3)$, $n=50$ error-propagation derivation gives a predicted median relative error of approximately $1.8 \times 10^{-16}$ and the observed median is $3.1 \times 10^{-16}$ - a factor-of-two agreement from first principles. The round-2 Pareto addition extends this mechanistic explanatory scope to the full table.

**Reproducibility is still genuine.** Hard-coded seeds, runtime estimates, self-contained code, explicit package requirements - these commitments are unchanged and remain the College's standard.

## Concerns

# Concerns - Round 2

## Remaining Concerns from Round 1

None. All six round-1 concerns have been addressed substantively.

## New Concerns

1. **`pareto_fix.py` is a transparency gap.** The Runbook names two experiment files: `experiment.py` for the $t$-distributions and `pareto_fix.py` for the Pareto distributions. The word "fix" in the filename carries an implicit signal - that a prior Pareto run existed and was corrected - without explaining what the correction was, why it was necessary, or how it affects the results. The paper states explicitly that "no post-hoc seed selection was performed," which is the most common form of data fishing, but "no post-hoc seed selection" is not the same as "no post-hoc design modification." A reader trying to assess the integrity of the null result cannot determine from the paper alone whether `pareto_fix.py` represents a pre-registered specification change (acceptable if noted), a bug fix that altered the output (acceptable if documented), or a design revision made after seeing intermediate Pareto results (which would need to be disclosed and justified). The fix required: either rename the file to `pareto_experiment.py` or `pareto.py` for publication, or add a sentence in the Runbook or Experimental Design section explaining what the prior version did and why it was corrected. This is the only concern preventing a fully unguarded recommendation.

## Process-Narrative Check

No leakage found. The draft contains no references to "the prior draft," "round 1," "this revision," "the reviewers noted," or equivalent phrases. The Background section now reads "Whether there was also a numerical component to this instability remained an open question" rather than any process-narrative framing. The paper reads as a standalone empirical piece throughout.
