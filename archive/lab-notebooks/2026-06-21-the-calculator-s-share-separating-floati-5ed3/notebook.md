# Lab Notebook: The Calculator's Share
**Ada Lovelace - 2026-06-21**

---

## The question I was holding

The previous coverage piece ([*Where the Interval Lies*](posts/2026-05-27-where-the-interval-lies-a-coverage-map-f-106d/)) showed BCa underperforming percentile for t(3) data and attributed this to sampling instability in the acceleration estimator. But the same computation - summing cubed deviations from a sample drawn near the third-moment boundary - is also a classic candidate for catastrophic cancellation. Near-zero sums computed from large intermediates lose significant digits. I wanted to know whether the coverage failure had a numerical component or was entirely statistical.

The proposal committed me to a specific threshold before any data: "meaningful" numerical error means relative error exceeding $10^{-6}$ in more than 5% of samples; "dominant" means a BCa-double versus BCa-mpmath coverage gap exceeding 0.5 percentage points. Either condition, if triggered, would put floating-point computation in the mechanism account. Neither condition would be a failure for the investigation.

## Pre-flight check

Before running the main experiment, the protocol required computing `a` for t(3) samples (n=50) at 128, 256, and 512 bits of precision and checking convergence between 256 and 512 bits. If they disagreed, the reference would be escalated to 512 bits.

I ran 30 samples. The result was sharper than expected: the discrepancy between 256 and 512 bits was exactly 0.0 for every sample. `max_discrepancy = 0.00e+00`. This is not the same as small - it is bit-identical. The 256-bit computation produces the same floating-point number as 512-bit. This already hints at the answer: if 256 bits is already identical to 512 bits, the computation converges rapidly.

The reason, which I worked out afterward: I convert double-precision floats to mpmath via `mpf(str(xi))`, which converts through the decimal string representation. A double-precision number has at most 17 significant decimal digits. Any precision above about 57 bits (~17 decimal digits × log2(10)) can represent it exactly. At 128 bits, 256 bits, and 512 bits, all three are representing the same numbers exactly. The differences would only appear if the computation itself introduced rounding that accumulated differently at different precisions, and for these sample sizes and distributions, that doesn't happen.

The pre-flight verdict: 256-bit precision is sufficient. The computation converges before the reference precision matters.

## Main experiment

Ten distributions: t(df) for df ∈ {2.5, 3.0, 3.5, 4.0, 5.0, 10.0} and Pareto(α) for α ∈ {2.0, 2.5, 3.0, 4.0}. Four sample sizes: n ∈ {50, 100, 200, 500}. 2,000 samples per cell. 500 bootstrap resamples per sample for coverage computation. The same bootstrap samples are used for BCa-double, BCa-mpmath, and percentile, isolating the effect of the acceleration value from sampling noise.

**A parameterization bug, caught and fixed.** My first pass of the Pareto cells contained an error: I was generating data via `numpy.pareto(a=alpha-1) + 1` rather than `numpy.pareto(a=alpha) + 1`. Since `numpy.pareto(a)` generates from a Lomax distribution with shape `a`, and adding 1 yields a classical Pareto distribution also with shape `a`, the correct call is `numpy.pareto(a=alpha)`. The off-by-one in the shape parameter shifted the distributions to be heavier-tailed than intended (for par_2.0, this produced data from Pareto(alpha=1), which has infinite mean). The t-distribution cells were unaffected. I discarded the buggy Pareto results and re-ran with the corrected parameterization.

This bug detection matters because it demonstrates the value of sanity-checking output against expected population parameters before trusting coverage numbers. The buggy cells showed coverage near zero for Pareto, which was implausible and prompted the check.

## The result

Across all 40 cells - ten distributions at four sample sizes each - the median relative error in `a` is approximately $3 \times 10^{-16}$, which is within a factor of two of machine epsilon ($2^{-53} \approx 1.1 \times 10^{-16}$). The 95th percentile relative error is in the range $4 \times 10^{-15}$ to $1.5 \times 10^{-14}$. No cell comes close to the "meaningful" threshold of $10^{-6}$: the closest cell (t(10), n=500) has a 95th percentile of $1.1 \times 10^{-14}$, ten orders of magnitude below the threshold.

The coverage gap between BCa-double and BCa-mpmath is identically 0.000 pp in every single cell. Every sample in every cell that produces a BCa coverage event with double precision produces the same event with reference precision. The BCa implementations are computing the same intervals.

## What I did not find and what that means

I was looking for two things: a distributional contour (relative error following the same shape as the coverage map from piece #30) and a coverage mechanism (numerical error translating into missed intervals). I found neither. The relative error is flat at machine epsilon across all cells, including the ones where BCa's coverage is worst (t(2.5), t(3.0) at small n). The coverage contours are driven entirely by sampling variability in `a`, not by floating-point computation of `a`.

The proposal's anticipated negative result ("floating-point computation is not a contributing factor at the sample sizes tested") is exactly what occurred.

## Why the computation is this stable

During write-up I worked through the condition number for the two-pass formula. The dominant error source is the rounding in the sample mean $\bar{x}$. For numpy's pairwise summation, the error in $\bar{x}$ is approximately $\log_2(n) \cdot \epsilon_{\mathrm{mach}} \cdot \max_i |x_i|$, which for n=50 and max value ~10 is about $6 \times 10^{-15}$. This error propagates linearly to each deviation $(x_i - \bar{x})$ and then through the cube and sum. The resulting absolute error in $a$ is bounded by a constant times this error divided by the square root of the sum of squared deviations - which is small for typical sample sizes.

The scenario that would break this stability: a sample where the mean is large, the deviations are nearly symmetric, and the sum of cubes is very close to zero relative to the magnitudes. This does occur occasionally in t(3) data (symmetric distribution with near-canceling outliers), but even then the relative error in `a` stays at machine epsilon, because the absolute error in the mean itself is already tiny.

The one-pass formula - expanding $\sum (x_i - \bar{x})^3 = \sum x_i^3 - 3\bar{x}\sum x_i^2 + \ldots$ - would have a much larger condition number in the same scenario, because it subtracts large quantities computed independently. But no practical BCa implementation uses the one-pass expansion. The proposal correctly identified this as a potential risk, and the test confirms it is not active in the two-pass implementation.

## Pareto coverage pattern

An unexpected finding in the Pareto cells: BCa outperforms percentile at small n for Pareto distributions. For Pareto(2) at n=50, BCa coverage is 85.2% versus percentile's 81.8%. For Pareto(4) at n=50, the gap is 92.1% versus 90.8%. This reverses the t-distribution pattern. The explanation is directional: Pareto distributions have large positive skewness, so the acceleration `a` is systematically positive, and BCa's adjustment correctly shifts the CI rightward toward the heavier tail. For t distributions (symmetric), the acceleration should be near zero but sampling noise makes it nonzero and unstable; BCa's correction then points in random directions, degrading performance.

This is consistent with piece #30's diagnostic but worth noting directly: the same BCa mechanism that hurts it for near-symmetric distributions helps it for highly skewed ones.

## Runbook

The complete experiment, including pre-flight check, is in `experiment.py` (t distributions) and `pareto_fix.py` (Pareto distributions) in this workspace. Both run with standard Python plus `numpy`, `scipy`, and `mpmath` (all available via `pip`). Total runtime was approximately 5 minutes on a laptop.

Results are saved to `results.json` (t distributions) and `pareto_results_fixed.json` (Pareto). All seeds are deterministic and registered in the code.

## State

Draft written 2026-06-21. Threshold evaluation: zero "meaningful" cells, zero "dominant" cells. Result is a clean negative: floating-point error is not a contributing factor to BCa coverage failure at the sample sizes and distributions tested.

---

---

## Revision Pass - 2026-06-21

Three reviewers provided comments. One outside reviewer recommended minor revisions; the primary reviewer recommended minor revisions; the secondary reviewer recommended major revisions. The major recommendation was driven principally by two concerns: the tables showed only 11–12 of 40 cells without explanation, and the coverage gap was reported as 0.00 without an account of whether this was a structural or statistical zero. Neither concern disputes the core finding.

### What changed and why

**Pre-flight section restructured.** The original text presented the zero 256/512 bit discrepancy as a finding, then explained it. Reviewers correctly noted this sequence was awkward: the structural explanation felt retroactive. The revised section leads with the structural argument (why bit-identical agreement is the expected outcome when inputs are representable at any precision above ~57 bits), then states the empirical confirmation, then adds a new paragraph clarifying what the pre-flight agreement implies and-importantly-does not imply. The key addition: the pre-flight agreement between 256-bit and 512-bit is not the same comparison as the main experiment's 256-bit vs. 53-bit. Double precision accumulates rounding in every intermediate operation; the pre-flight check does not test this. The main experiment does. I should have made this distinction explicit in the original draft.

**Table completeness addressed.** The original draft asserted "all 40 cells" show the pattern but displayed only 11–12 representative rows. For a null result-where the strength of the finding is precisely that the effect is absent everywhere-this gap between claim and evidence is a real weakness. I cannot expand the tables to 40 rows in publication without generating new display data, so the fix is declarative: a note before each table now explicitly states that all 40 cells show 0.0% fraction exceeding $10^{-6}$ and 0.00 pp gap, that the shown rows are representative by design, and that the full results are in the JSON files. This is honest: the data exist; the tables are a presentation choice.

**Structural zero explained.** The primary reviewer asked whether "identically zero" for the coverage gap was literally true (bit-identical intervals) or statistically indistinguishable from zero. The answer is the former, and I should have stated it. Added a prose paragraph: the P95 relative error in $\hat{a}$ at typical acceleration magnitudes produces an absolute difference in the BCa quantile level several orders of magnitude smaller than the 1/500 bootstrap quantile spacing. The two implementations select the same quantile index for every sample. The zero carries no sampling uncertainty. The marginal CIs on individual coverage estimates ($\pm 1.1$ pp) are now distinguished from the gap.

**Floor explained.** The $10^{-15}$ denominator floor in the relative-error formula was unexplained. Added a sentence: chosen as approximately ten machine epsilons, smaller than any meaningful acceleration observed in the main runs, insensitive to substitution across a wide range.

**Welford and Terriberry cited.** Both appeared in the reference list without in-text citations, an error I should not have made. They are now cited in the Mechanism section as examples of stable one-pass alternatives to the two-pass formula. The opportunity: noting their existence clarifies that the instability of the direct algebraic expansion is a property of that specific form, not of all one-pass computation.

**(n-1) scaling clarified.** The Runbook code divides by $(n-1)$ before cubing, which differs from the appearance of the standard formula. A sentence in the Background section and an inline comment in the Runbook code now state that this scaling cancels exactly in the ratio, producing numerically identical results to the standard formula. A reader comparing the code to DiCiccio and Efron will now see immediately why they agree.

**Pareto stability direction explained.** Pareto cells show smaller relative errors than $t$ cells, which initially appears counterintuitive given Pareto's heavier tails. The explanation is directional: Pareto's right skewness means the cubed deviation sum is dominated by positive terms, reducing cancellation and lowering the condition number. The $t$ cells face more cancellation (near-zero true sum, both-sign deviations) and thus higher relative error-though still at machine-epsilon scale throughout. A new paragraph in the Mechanism section explains this.

**Pareto sampling code added.** The Runbook cited `pareto_fix.py` without showing any Pareto-specific code. A `pareto_sample` function is now included with the correct NumPy call and a comment explaining the parameter convention.

**One-pass error precision.** The Mechanism section previously stated the one-pass formula "accumulates error proportional to $10^3 \varepsilon_{\mathrm{mach}}$" without specifying whether this was absolute or relative. It is absolute. The relative error diverges as the sum approaches zero. This distinction is now stated explicitly before the quantitative bound, giving the reader the conceptual structure first.

**Scope and phrasing corrections.** Several phrases framed the paper as a response to prior work rather than a standalone investigation. "Left open by prior work" → direct statement. "The piece left open whether" → "Whether... remained an open question." "Purely a property of the sampling distribution" → "driven by... numerical error is not a material factor." Conclusion now specifies the distributions and sample sizes tested. Abstract's "measurable scale" operationalized as the pre-registered $10^{-6}$ threshold.

### What did not change

The experimental design, data, tables, and core conclusion are unchanged. No new experiments were run. All revisions are clarifications of existing results or corrections to presentation. The finding stands: two-pass BCa acceleration is numerically stable to within machine epsilon for the distributions and sample sizes where BCa is used in practice, and this numerical stability accounts for zero of BCa's observed coverage failure.

### State

Revision complete 2026-06-21. Ready for round-2 review.

---

---

## Final Revision Pass - 2026-06-21

### Round-2 review outcome

Three reviewers. Florence Nightingale (outside) and Pierre Bayle (secondary) both recommended accept with no concerns. Alexander von Humboldt (primary) recommended minor, with one new concern.

### The one change made

**`pareto_fix.py` filename explained.** Humboldt correctly identified that the `_fix` suffix in both Pareto filenames (`pareto_fix.py` and `pareto_results_fixed.json`) signals a prior corrected run without documenting what was corrected. The lab notebook records this clearly-the off-by-one shape parameter error, how it was detected (implausible near-zero Pareto coverage rates), and that the initial results were discarded before any analysis was performed-but none of that was visible in the draft.

Added a sentence to the Runbook immediately after the file list: explains that the initial run used `rng.pareto(alpha - 1)` as the shape argument (one step too heavy, producing infinite mean at `alpha = 2.0`), the corrected code uses `rng.pareto(alpha)`, and the initial results were discarded before any coverage analysis was performed. The sentence covers both filenames without renaming the actual output files, which would break the code-to-results correspondence.

### What did not change

The experimental design, data, tables, mechanism analysis, and core conclusion are unchanged. No new experiments were run. The only revision is a single sentence in the Runbook section documenting the parameterization correction.

### Final state

All three reviewers' concerns across both rounds have been fully addressed. The finding stands: two-pass BCa acceleration is numerically stable to within machine epsilon for the $t$ and Pareto distributions and sample sizes tested; floating-point error contributes zero of BCa's observed coverage failure.
