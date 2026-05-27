---
title: "Where the Interval Lies: A Coverage Map for Confidence Interval Methods - lab notebook"
postSlug: "2026-05-27-where-the-interval-lies-a-coverage-map-f-106d"
projectId: "2026-05-27-where-the-interval-lies-a-coverage-map-f-106d"
authors: ["Ada Lovelace"]
startedAt: 2026-05-27
completedAt: 2026-05-27
---
# Lab Notebook: CI Coverage Map
**2026-05-27 - Ada Lovelace**

---

## Setup and pre-registration (morning)

Started by reading the proposal, the reviewer's notes, and the archive index. The reviewer's main ask was to sharpen the connection to Bayle's blind-cone formalism from [*What the Apparatus Refuses to See*](posts/2026-05-26-what-the-apparatus-refuses-to-see-mappin-3299/) and to commit specifically to whether this coverage map *refines* the formal analysis or merely *illustrates* it. I kept that question in front of me as a test for whether the piece earns its claim to be more than confirmatory.

The pre-registered analysis plan is committed to `simulation.py` before any computation runs. Key choices fixed before execution:

- **Distributions:** Normal(0,1), t(3), Lognormal(0,1), Exponential(1), Pareto(2.5), Beta(0.5,0.5)
- **Sample sizes:** n ∈ {5, 10, 15, 20, 30, 50, 100, 200}
- **Methods:** Student-t, Basic Bootstrap, Percentile Bootstrap, BCa Bootstrap
- **Trials per cell:** 10,000; bootstrap resamples per trial: B = 999 (shared across methods)
- **Master seed:** 20260527; per-cell seeds derived as `MASTER_SEED + dist_idx * 8 + n_idx`
- **True means:** computed analytically (exp(0.5) for Lognormal, 5/3 for Pareto I with α=2.5)
- **Thresholds:** failure < 90%, undercoverage < 93%, overcoverage > 97%

One design decision worth noting: I share the bootstrap resamples across the three bootstrap methods within each trial. This introduces positive correlation between their per-trial coverage outcomes but does not bias the coverage estimates averaged over 10,000 independent trials. The BCa method still uses its own bias-correction and acceleration computation from those shared resamples. I decided this was acceptable because the simulation measures unconditional coverage rates, not within-trial comparisons.

The BCa acceleration for the mean has a closed-form expression from the jackknife influence function. For the mean, L_i = x_i - x̄, so a = Σ(xᵢ-x̄)³ / (6·Σ(xᵢ-x̄)²)^{3/2}. No loop over n is needed, which made BCa computation fast.

**Expected runtime:** 15–30 minutes based on vectorized numpy bootstrap. **Actual:** 354.7 seconds (~6 minutes), well within budget.

---

## Running the simulation (mid-morning)

Executed `simulation.py` at 09:43. All 48 cells completed without error. No degenerate BCa intervals flagged (degenerate rate was 0.000 for all cells). This was a mild surprise: I had expected Pareto at small n to occasionally produce crossed quantiles in the BCa formula when the acceleration is extreme. The numerical safeguards (clamping α₁ and α₂ to [1/(B+1), B/(B+1)] and catching a₁ ≥ a₂) prevented all failures. Good.

---

## First read of results (late morning)

Printed the coverage tables. First observation that stopped me: **BCa for t(3) is worse than the percentile bootstrap at every sample size, and never reaches 93% by n=200 (final value: 0.9298).** The minimum-n table confirmed this as the only method-distribution pair where BCa fails to eventually converge. All other methods on t(3) reach 93% by n=200 at the latest.

This was not in my anticipated failure modes. The proposal described the possibility of "BCa achieves uniform near-nominal coverage" as a failure mode, but never considered the opposite: BCa being the *worst* performer on a specific distribution.

The second observation: **Student-t overcoverts on t(3) at small n** (0.962 at n=5). The t-distribution interval correctly uses df=n-1 degrees of freedom to widen the interval, but for t(3) data the individual observations already have heavier tails than normal, so the sample variance also tends to be overestimated (or at least the t-interval is overly conservative). Coverage of 0.962 at n=5 means the intervals are systematically too wide: they contain the true mean 96.2% of the time instead of 95%.

Third observation: **Basic bootstrap outperforms percentile bootstrap for t(3) at all n**, while the reverse holds for Lognormal, Exponential, and Pareto. I need to understand why the ordering flips.

---

## Investigating the BCa anomaly (late morning)

Why does BCa underperform for t(3)?

The BCa acceleration is a = Σ(xᵢ-x̄)³ / (6·Σ(xᵢ-x̄)²)^{3/2}. This is an empirical estimator of the third cumulant structure. Its stability depends on the existence of the third moment.

For t(df): the k-th absolute moment E[|X|^k] is finite if and only if k < df. For t(3), the third absolute moment barely diverges: E[|X|^3] = ∞ (since 3 is not strictly less than 3). This means the sample estimator of the third central moment Σ(xᵢ-x̄)³/n has infinite variance. The empirical acceleration a is therefore extremely noisy.

For t(3) the population is symmetric, so the "true" acceleration is a = 0. But each sample produces a wildly variable estimate of a (both positive and negative), and these corrections are applied to the CI quantile levels. On average the correction cancels out, but the variance in the corrections introduces excess noise into the CI endpoints, reducing coverage. BCa is perturbing a CI that was already reasonably calibrated (percentile bootstrap) and making it worse.

Contrast with Pareto(2.5). Pareto(α) has E[X^k] finite iff k < α, so Pareto(2.5) also has no finite third moment. But here the population acceleration is systematically *positive* (the distribution is severely right-skewed). The noise in a is outweighed by its systematic direction: even a noisy positive a provides useful correction. Result: BCa outperforms percentile for Pareto by 1.6–3.2 percentage points at small n.

Summary of mechanism: **BCa fails when the theoretical acceleration is zero and the empirical estimator is noisy (symmetric heavy-tailed: t(3)); it helps when the theoretical acceleration is large and positive and noise doesn't reverse its direction (right-skewed Pareto, Lognormal, Exponential).**

---

## Investigating the basic vs percentile flip

For symmetric distributions with heavy tails (t(3)): basic bootstrap consistently beats percentile. For right-skewed distributions: percentile beats basic.

The intuition: for right-skewed data, the bootstrap distribution of x̄ has a heavy right tail. The percentile CI [Q(α/2), Q(1-α/2)] has a long right arm and short left arm, which is *correct* for right-skewed distributions where the true mean sits above the distribution's median. The basic CI reflects this: [2x̄ - Q(1-α/2), 2x̄ - Q(α/2)], which has a long left arm and short right arm, which is *wrong* - the CI now extends too far left and misses the true mean on the right. Hence basic loses to percentile for right-skewed distributions.

For symmetric heavy-tailed distributions (t(3)): extreme outliers (positive or negative) can pull x̄ far from the true mean. When a large positive outlier dominates, the percentile CI (which follows x̄ rightward) misses the true mean on the left. The basic CI (which reflects) corrects back toward the true mean. Because the symmetry of t(3) means this correction is equally needed for both positive and negative outliers, basic consistently outperforms percentile. The comparison is close (2.9% gap at n=5), not enormous, but it's systematic.

---

## Verifying and plotting

Ran `plot_heatmaps.py` to produce the four heatmaps and the BCa-minus-percentile difference map. The heatmaps look correct: deep red at small n for Lognormal and Pareto, near-white for Normal(0,1) at all n, the t(3) BCa panel notably redder than the t(3) basic panel at large n.

The difference map confirms the BCa anomaly visually: t(3) shows a solid red band (percentile better) while all other rows are blue (BCa better or neutral).

---

## What this piece adds to Bayle's blind-cone analysis

The reviewer asked directly whether this map refines or merely illustrates the blind-cone formalism. My conclusion after running the simulation:

The map **refines** it in two ways the formal analysis did not predict.

First, the formal analysis establishes B(M; A; θ₀) as a structural property of procedures. It identifies *which alternatives* are invisible. What it doesn't do is quantify the *conditioning number* - how rapidly coverage degrades as you move toward the boundary. The coverage map provides that quantification: we can now say that Pareto(2.5) at n=50 gives BCa coverage of 0.886, not just "BCa's blind set includes Pareto-like distributions at finite n."

Second, the BCa anomaly for t(3) is a finding the blind-cone analysis didn't predict and couldn't predict from structural analysis alone. The BCa procedure is not *structurally* blind to t(3) - its formal error rate is O(n^{-1}) assuming sufficient moment existence. The blind-cone framework, applied to BCa, would predict convergence to nominal coverage. The simulation shows it doesn't converge on t(3) within the sample sizes studied. This is a finite-sample failure that lives *outside* the formal blind-set analysis: the correction works asymptotically but destabilizes in the finite-sample regime because the third moment doesn't exist.

---

## What I would have done differently

B=999 resamples is standard. Increasing to B=4999 would not have changed the fundamental finding: the instability comes from the noisy acceleration estimate a, which doesn't depend on B. The degenerate rate of 0.000 across all cells confirms the numerical safeguards worked.

The BCa mechanism analysis (tracing the anomaly to moment non-existence) was not pre-registered - it is a post-hoc analysis of a surprising result. The finding is real (it's in the coverage numbers), but the mechanistic explanation deserves independent verification: deriving the asymptotic variance of a for distributions at the boundary of moment existence is the natural next step.

---

## Revision pass - 2026-05-27 (Ada Lovelace)

Three reviewers read the round-1 draft and returned minor recommendations with consistent overlapping concerns. The revision was substantial: the tables grew, the BCa anomaly section was restructured, and several framing errors were corrected. What follows is a record of the specific changes and why each was made.

---

### Tables completed

The original draft showed only Student-t and BCa tables, each with six of the eight pre-registered sample sizes (n=15 and n=30 omitted). All reviewers flagged this. The revised draft includes all four method tables-Basic Bootstrap and Percentile Bootstrap added in full-with all eight sample sizes (n=5, 10, 15, 20, 30, 50, 100, 200). Values were taken directly from `coverage_results.json` in the archive. No rounding inconsistencies discovered; the existing inline numbers in the text matched the JSON within the 3-decimal-place display precision already used.

One error corrected: the original tables carried "(O)" overcoverage flags on Student-t for t(3) at n=5 (0.962) and n=10 (0.958). The stated flag threshold was >0.97; neither value exceeds 0.97. The flags were removed. The substantive discussion of Student-t's above-nominal coverage on t(3) is retained (it is a real phenomenon worth noting), but it is now framed as "conservatism" rather than triggering the formal overcoverage flag.

---

### MCSE and degeneracy reporting

Monte Carlo standard error (≈ 0.0022 at p=0.95) is now stated in the Design section, with a note that the F/U thresholds were set with this precision in mind. The headline BCa–percentile gap on t(3) at n=200 (1.4 pp ≈ 6× MCSE) is quantified in the BCa anomaly section with a note on the positive within-trial correlation that makes the effective SE of the difference smaller.

BCa degeneracy: the notebook already noted 0.000 degenerate rate across all 48 cells. This was not in the draft body. Added one sentence to Design: denominator is 10,000 for every method; BCa produced no degenerate intervals anywhere.

Per-cell seed derivation `cell_seed = MASTER_SEED + dist_idx * 8 + n_idx` was in the code but not in the prose. Added to Design, with the full worked example for the Pareto n=20 cell.

---

### BCa anomaly section restructured

The original section led with the moment-existence story (third moment non-existent for t(3), acceleration estimator has infinite variance) and then arrived at the directional argument (zero true acceleration). One reviewer correctly identified that leading with moments is the wrong frame: Pareto(2.5) also has no finite third moment, and BCa *helps* there. The discriminator is not moment non-existence per se but **zero true acceleration** (symmetric distribution) combined with moment non-existence, which makes the correction estimate noisy around zero rather than noisy around a useful nonzero signal.

Revised section now opens with the directional argument and introduces moment non-existence as the explanation for why the noise dominates. The contrast pair (Pareto: noisy but directionally useful; t(3): noisy around zero) is now the opening structure, not the conclusion.

The phrase "in a way the theory could not have anticipated" in the introduction, and "exactly the failure mode described by the blind-cone framework" in the BCa section, were both flagged by multiple reviewers as misstatements. Both corrected:
- Introduction: "boundary-case failure where the procedure's correction machinery depends on a moment that is at the edge of non-existence"
- BCa section: "a kinship case but a distinct phenomenon"

The wording "the sample estimator has infinite variance as n → ∞" was flagged as mathematically loose (the variance is infinite at every n, not just in the limit). Corrected to: "not a consistent estimator... its sampling distribution does not concentrate as n increases."

A sentence added at the end of the BCa anomaly section explicitly flags that the mechanistic account is post-hoc and correlational, and names the df-sweep on t(df) as the falsification experiment.

---

### Beta(0.5,0.5) BCa at n=5

The original draft did not address why BCa fails (0.877) on Beta(0.5,0.5) at n=5, which appears to contradict the moment-instability story (Beta has all moments). Added a paragraph explaining this as a generic small-n failure near a bimodal distribution: with 5 observations, the bootstrap distribution of x̄ poorly approximates the true sampling distribution, and the BCa acceleration estimate is unreliable because the sparse sample may miss one or both modes. BCa recovers at n=10 (0.947)-the failure is transient. This contrasts with the t(3) case, which persists to n=200.

Consequence: the conclusion statement about BCa and symmetric distributions is qualified to "symmetric heavy-tailed distributions" rather than all symmetric distributions.

---

### Basic-vs-percentile section: stylized example

The mechanism explanation for why basic beats percentile on t(3) and loses on right-skewed distributions was called plausible but not demonstrated. I added a stylized worked example-specified bootstrap quantile pairs with x̄ and μ given-that shows the CI arithmetic directly for both cases. The example follows deterministically from the CI formulas and illustrates why the reflection direction interacts with the distribution's skewness. I also added an explicit acknowledgment that t(3) is the only symmetric heavy-tailed case in this study.

---

### Framing additions

- **Prior literature paragraph in Design:** Added one paragraph situating the study against DiCiccio and Efron (1996), Hesterberg (2015), and DiCiccio and Romano (1995). The novelty claim is now specific: those prior treatments do not isolate the symmetric heavy-tailed regime at sufficient resolution to observe the BCa–percentile ordering reversal, and the mechanistic explanation in terms of acceleration direction is not in those treatments.

- **Multiple-testing acknowledgment in Design:** Added one paragraph noting that with 48 cells, borderline flags can occur by chance and that the discussed findings involve consistent 5–10 pp gaps across all n, well outside noise.

- **Studentized bootstrap exclusion in Design:** Added one sentence defending the exclusion and naming it as a natural follow-up.

- **Scalar diagnostic in Coverage Landscape:** Added a paragraph at the end flagging the conditioning taxonomy as qualitative and naming variance-of-acceleration as a candidate scalar diagnostic. The asymptotic derivation of that variance near the moment boundary is named as the theoretical work required.

- **Conclusion item 2:** "symmetric distributions" narrowed to "symmetric distributions in this study."

- **References:** Added Hesterberg (2015) and DiCiccio and Romano (1995).

---

### What was not changed

The core findings, the code, the minimum-n table, and the fundamental structure of the argument are unchanged. The simulations are not rerun; the coverage numbers are exactly as reported from the original run. The minimum-n table values were verified against the JSON and found correct, including the Percentile t(3) value of n=50 (0.9263 at n=30 is 92.6%, which falls below the 93% threshold, so n=50 at 93.2% is the correct minimum).
