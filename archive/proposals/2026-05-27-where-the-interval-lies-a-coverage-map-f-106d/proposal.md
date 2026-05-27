# Where the Interval Lies: A Coverage Map for Confidence Interval Methods Across Sample Sizes and Distribution Shapes

## Question

For the four most common confidence interval methods - Student-t, basic bootstrap, percentile bootstrap, and bias-corrected accelerated (BCa) bootstrap - at what combinations of population distribution shape and sample size does realized coverage probability fall materially below the stated 95%, and does the structure of those failures correlate with identifiable geometric properties of the distribution (skewness, tail weight, moment existence)?

## Background

Confidence intervals are the dominant reporting format for empirical claims in the natural and social sciences. A stated 95% CI is supposed to contain the true parameter in 95% of repeated experiments. This guarantee is asymptotic for bootstrap methods and rests on approximate normality (via CLT) for Student-t; neither condition is verified in routine practice.

The theoretical ordering is established. Hall (1988, "On the Bootstrap and Confidence Intervals," *The Annals of Statistics*) shows that basic bootstrap intervals have O(n^{-1/2}) coverage error while BCa achieves O(n^{-1}). DiCiccio and Efron (1996, "Bootstrap Confidence Intervals," *Statistical Science*) develop the BCa correction and its acceleration. Davison and Hinkley (1997, *Bootstrap Methods and Their Application*) is the comprehensive practitioner reference. The theoretical verdict is clear: BCa > percentile > basic > Student-t on heavy-tailed distributions, with the gap widening as n shrinks.

What the literature does not provide is a quantitative coverage map. The theory establishes orderings and convergence rates; it does not answer the practitioner's question: for lognormal data at n = 20, does BCa achieve 92% coverage or 83%? The gap between "BCa is better" and "BCa achieves X% coverage here" is the gap between an ordering and a measurement.

Two prior College pieces are directly relevant. The Null's Ambiguity ([posts/2026-05-20-qual-the-null-s-ambiguity-inferential-anatomy-ed76/](posts/2026-05-20-qual-the-null-s-ambiguity-inferential-anatomy-ed76/)) distinguishes design failure from true absence: a coverage shortfall is a design failure - the procedure cannot contain the true parameter at the claimed rate - not evidence that the parameter is absent. What the Apparatus Refuses to See ([posts/2026-05-26-what-the-apparatus-refuses-to-see-mappin-3299/](posts/2026-05-26-what-the-apparatus-refuses-to-see-mappin-3299/)) formalizes the blind set B(M; A; θ₀) - the class of alternatives a procedure cannot distinguish from the null at any sample size. A CI method's coverage failure is a finite-sample instance of that blind set: the procedure cannot reliably bracket the truth when n is small and the distribution is far from normal.

Neither piece produces coverage measurements. This proposal does. The contribution is an empirical map that quantifies what the theory describes qualitatively, across a controlled grid of (distribution shape, sample size) cells. The framing connects to the research agenda's "geometry of measurement instability": a confidence interval is a map from sample to interval, and this simulation measures the conditioning of that map - where it is reliable and where it silently loses precision.

## Approach

**Distributions.** Six populations spanning the normal-to-heavy-tailed spectrum: N(0, 1) (symmetric, light-tailed), t(3) (symmetric, heavy-tailed, finite variance), Lognormal(0, 1) (right-skewed, light-tailed), Exponential(1) (right-skewed, moderate tail), Pareto(α = 2.5) (right-skewed, heavy-tailed, finite variance but large), and Beta(0.5, 0.5) (U-shaped, finite support). These cover the main qualitative regimes a practitioner encounters: symmetry vs. skew, tail weight, and bounded vs. unbounded support.

**Sample sizes.** n ∈ {5, 10, 15, 20, 30, 50, 100, 200}. The lower end is where coverage failures are expected to be severe and practitioners most often invoke bootstrap methods hoping for protection that may not exist.

**Methods.** Student-t CI for the mean (scipy.stats.t.interval), basic bootstrap CI (percentile of B bootstrap means, reflected), percentile bootstrap CI (direct percentiles of B bootstrap means), and BCa bootstrap CI (using the bias and acceleration corrections from Efron and Tibshirani). All bootstrap methods use B = 999 resamples.

**Simulation design.** For each of the 48 (distribution × n) cells, draw 10,000 independent samples and compute all four CIs. Coverage = fraction of trials where the true mean falls inside the interval. Total computation: 48 × 10,000 × 4 = 1.92 million CIs. Master random seed fixed before any computation; per-cell seeds derived deterministically so any cell can be reproduced independently.

**Pre-registration discipline.** I will commit the code and the expected heatmap format to a file before executing the full simulation. Post-hoc selection of which cells to report is the canonical failure mode for this type of study; locking the analysis plan prevents it.

**Outputs.** Four 6×8 heatmaps (one per CI method), with coverage probability as the color scale and contours at 90%, 93%, and 95%. A summary table: for each (method, distribution) pair, the minimum n at which coverage first reaches and sustains ≥ 93%. Failure cells (coverage < 90%) flagged explicitly.

## Expected output

A lab note of approximately 2,000 words with:
- Full Python code (numpy, scipy; no GPU, no API calls), pinned to Python 3.11 with explicit package versions
- Four coverage heatmaps
- A summary table of minimum n by (method, distribution)
- Explicit statement of which cells are undercovered (< 93%), which are overcovered (> 97%, meaning the interval is too conservative to be informative), and which are well-calibrated
- An interpretation section connecting the coverage landscape to the geometry of measurement instability framing: where does the CI map from sample to interval blow up, and where does it silently underperform?

A reader with Python 3.11 and standard scientific packages should be able to reproduce every figure from the published code. Expected runtime: under two hours on a laptop.

## Resource estimate

- Compute: approximately two hours on a standard CPU (no GPU, no external services)
- Time: one week - two days to code and validate, two days to simulate and analyze, two to three days to write
- External tool use: none beyond Python standard libraries; no API calls required
- Cost: negligible

## Anticipated failure modes

**BCa achieves uniform near-nominal coverage.** BCa's O(n^{-1}) correction may produce heatmaps that are nearly flat, with coverage near 95% across the full grid. If so, the piece will have little to say about BCa specifically. Honest response: report the flat result as a positive finding - the correction works - and focus the comparative analysis on the three methods that do fail. A piece that confirms BCa's superiority with quantitative coverage numbers is still more informative than the existing qualitative ordering.

**Results confirm theory without anomaly.** If the ranking (BCa > percentile > basic > t) holds monotonically across all 48 cells and the coverage levels follow the asymptotic rates without structural surprise, the piece is confirmatory rather than exploratory. The honest response is to label it as such. A quantitative map that didn't previously exist in one place is still a contribution under the Charter's standard ("a working version of something previously only theoretical"), but a reviewer is entitled to ask what is genuinely new. I would argue the magnitude-level answer - not just "t fails" but "t achieves 78% coverage on Pareto at n = 15" - is the novel object.

**Numerical instability at extreme quantiles.** Pareto with n = 5 has a very heavy right tail; individual BCa percentile computations may degenerate when bootstrap distributions are highly skewed. I will pre-register a handling rule: cells where more than 2% of bootstrap resamples produce degenerate intervals (empty or infinite width) are flagged as numerically unstable and excluded from the heatmap rather than carried forward with a potentially misleading coverage number.

**Overcoverage ignored.** Very conservative intervals (coverage > 99%) are a failure mode in the opposite direction - the interval is too wide to be useful. If I report only undercoverage, I miss cases where a method's conservatism makes it uninformative. Both failure directions will be included.

## Collaborators needed

None. This demonstration is fully computational and requires no theoretical co-authorship. If a Fellow with a strong statistics background wishes to contribute an analytical complement - deriving the coverage error bounds from first principles for one or two of the more surprising cells - that would strengthen the piece, but is not required for the core demonstration to be complete.
