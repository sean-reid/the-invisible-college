# Where the Interval Lies: A Coverage Map for Confidence Interval Methods

Every published confidence interval carries a claim: the procedure that produced it would contain the true parameter in 95% of repeated experiments. This claim is asymptotic or approximate for every bootstrap method and rests on near-normality via the central limit theorem for Student-t. Neither condition is verified when the interval appears in print. The literature tells practitioners that BCa is better than percentile bootstrap, which is better than basic bootstrap, which is better than Student-t for non-normal data-but it does not say *how much* better, and at what sample sizes. The gap between an ordering and a measurement is the gap between a theoretical guarantee and something actionable.

This piece closes that gap empirically. Using a simulation of 10,000 independent trials per cell across 48 (distribution × sample size) combinations, it produces a coverage map: the fraction of trials in which each of four confidence interval methods actually contains the true mean, as a function of population distribution shape and sample size. The map confirms most predictions of the theory and identifies one boundary-case failure-BCa's performance on t(3)-where the procedure's correction machinery depends on a moment that is at the edge of non-existence, causing the finite-sample estimator to behave erratically in a way the asymptotic theory does not foresee.

---

## Design

**Methods.** Four 95% confidence interval methods for the mean: (1) Student-t, using the t-distribution with n−1 degrees of freedom; (2) basic bootstrap, the reflected percentile CI [2x̄ − Q*(1−α/2), 2x̄ − Q*(α/2)] where Q* denotes quantiles of B=999 bootstrap sample means; (3) percentile bootstrap, [Q*(α/2), Q*(1−α/2)]; and (4) BCa bootstrap, which adjusts the quantile levels using a bias-correction z₀ and an acceleration constant a. For the mean, the acceleration has a closed-form expression via the jackknife influence function: a = Σ(xᵢ−x̄)³ / [6·(Σ(xᵢ−x̄)²)^(3/2)]. The studentized (bootstrap-t) interval, which also achieves O(n^{−1}) coverage error (Hall 1988), is excluded from this study; its behavior on the heavy-tailed and symmetric distributions studied here is a natural follow-up question.

**Distributions.** Six populations covering the main regimes a practitioner encounters:

| Distribution | Shape | True mean |
|---|---|---|
| Normal(0,1) | Symmetric, light-tailed | 0 |
| t(3) | Symmetric, heavy-tailed | 0 |
| Lognormal(0,1) | Right-skewed, light-tailed | exp(0.5) ≈ 1.649 |
| Exponential(1) | Right-skewed, moderate tail | 1 |
| Pareto(α=2.5) | Right-skewed, heavy-tailed | 5/3 ≈ 1.667 |
| Beta(0.5,0.5) | U-shaped, bounded support | 0.5 |

**Sample sizes.** n ∈ {5, 10, 15, 20, 30, 50, 100, 200}.

**Simulation.** For each of the 48 cells, 10,000 independent samples are drawn from the population and all four CIs are computed. Coverage = fraction of trials where the true mean falls inside the interval. The denominator for every method is 10,000; BCa produced no degenerate intervals (adjusted quantile levels did not cross) in any cell, so no trials were excluded. Master seed: 20260527; per-cell seeds are derived as `cell_seed = MASTER_SEED + dist_idx * 8 + n_idx`, where `dist_idx` runs 0–5 over the six distributions in the order listed above and `n_idx` runs 0–7 over the eight sample sizes in ascending order. This scheme yields statistically independent cells: NumPy's PCG64 generator has sufficient independence between seeds that differ by small integers, and the reproducibility example below confirms the expected coverage. Total: 1.92 million confidence intervals. Runtime on a standard CPU: 354.7 seconds.

**Simulation precision.** With N=10,000 Bernoulli trials per cell, the Monte Carlo standard error of a coverage estimate is √(p(1−p)/N) ≈ 0.0022 near the nominal target of 0.95. The undercoverage flag (U: below 93%) and failure flag (F: below 90%) were set with this precision in mind: differences of 2 percentage points or more are reliably outside simulation noise.

**Prior simulation studies.** Simulation comparisons of bootstrap CI methods appear in DiCiccio and Efron (1996, Table 1 therein) and Hesterberg (2015). Both report BCa favorably across a range of right-skewed distributions and do not isolate the symmetric heavy-tailed regime at sufficient depth to observe the ordering reversal documented below. The specific comparison-BCa against percentile on a symmetric distribution where the third moment fails to exist-is not resolved in those treatments.

**Multiple comparisons.** With 48 cells flagged against the F/U thresholds, roughly 1–2 cells can be expected to fall in a borderline zone by chance even if coverage were exactly nominal. The findings discussed below involve coverage gaps of 5–10 percentage points that are consistent across the entire n=5 to n=200 range, well outside any plausible noise floor. The BCa–percentile comparison on t(3) is an anomaly the analysis plan did not anticipate; it is not a post-hoc selection of a single extreme cell.

The analysis plan was committed to code before execution. Post-hoc selection of which cells to report is a standard failure mode for simulation studies of this type; locking the plan prevents it. Full Python code (numpy, scipy; no GPU, no external services) is included at the end of this piece. To reproduce any specific cell: `run_cell('Pareto(2.5)', 20, 20260562)` (Pareto at n=20 uses dist_idx=4, n_idx=3, so cell_seed = 20260527 + 4·8 + 3 = 20260562).

---

## The Coverage Map

Table 1 reports realized coverage for all four methods across all cells, flagged by whether coverage falls below 90% (F), falls below 93% but at or above 90% (U), or is well-calibrated. No cell in the study exceeds 97%, so the overcoverage flag (O) is not triggered; Student-t values above the nominal 95% on t(3) are discussed in the findings.

**Student-t:**

| Distribution | n=5 | n=10 | n=15 | n=20 | n=30 | n=50 | n=100 | n=200 |
|---|---|---|---|---|---|---|---|---|
| Normal(0,1) | 0.951 | 0.950 | 0.950 | 0.950 | 0.952 | 0.951 | 0.952 | 0.948 |
| t(3) | 0.962 | 0.958 | 0.956 | 0.954 | 0.956 | 0.954 | 0.956 | 0.954 |
| Lognormal(0,1) | 0.824(F) | 0.838(F) | 0.854(F) | 0.863(F) | 0.880(F) | 0.895(F) | 0.916(U) | 0.929(U) |
| Exponential(1) | 0.886(F) | 0.899(F) | 0.914(U) | 0.917(U) | 0.926(U) | 0.935 | 0.942 | 0.945 |
| Pareto(2.5) | 0.782(F) | 0.791(F) | 0.813(F) | 0.822(F) | 0.850(F) | 0.866(F) | 0.885(F) | 0.905(U) |
| Beta(0.5,0.5) | 0.926(U) | 0.945 | 0.947 | 0.947 | 0.946 | 0.943 | 0.951 | 0.955 |

**Basic Bootstrap:**

| Distribution | n=5 | n=10 | n=15 | n=20 | n=30 | n=50 | n=100 | n=200 |
|---|---|---|---|---|---|---|---|---|
| Normal(0,1) | 0.839(F) | 0.898(F) | 0.919(U) | 0.926(U) | 0.936 | 0.939 | 0.947 | 0.943 |
| t(3) | 0.858(F) | 0.919(U) | 0.936 | 0.938 | 0.948 | 0.950 | 0.955 | 0.954 |
| Lognormal(0,1) | 0.699(F) | 0.767(F) | 0.802(F) | 0.824(F) | 0.843(F) | 0.870(F) | 0.897(F) | 0.916(U) |
| Exponential(1) | 0.769(F) | 0.838(F) | 0.871(F) | 0.884(F) | 0.904(U) | 0.918(U) | 0.932 | 0.938 |
| Pareto(2.5) | 0.640(F) | 0.719(F) | 0.756(F) | 0.773(F) | 0.809(F) | 0.836(F) | 0.862(F) | 0.889(F) |
| Beta(0.5,0.5) | 0.798(F) | 0.885(F) | 0.905(U) | 0.916(U) | 0.923(U) | 0.929(U) | 0.943 | 0.950 |

**Percentile Bootstrap:**

| Distribution | n=5 | n=10 | n=15 | n=20 | n=30 | n=50 | n=100 | n=200 |
|---|---|---|---|---|---|---|---|---|
| Normal(0,1) | 0.837(F) | 0.898(F) | 0.918(U) | 0.927(U) | 0.934 | 0.940 | 0.946 | 0.943 |
| t(3) | 0.829(F) | 0.892(F) | 0.908(U) | 0.914(U) | 0.926(U) | 0.932 | 0.941 | 0.944 |
| Lognormal(0,1) | 0.725(F) | 0.802(F) | 0.831(F) | 0.852(F) | 0.875(F) | 0.891(F) | 0.913(U) | 0.928(U) |
| Exponential(1) | 0.791(F) | 0.859(F) | 0.890(F) | 0.901(U) | 0.918(U) | 0.929(U) | 0.937 | 0.942 |
| Pareto(2.5) | 0.678(F) | 0.757(F) | 0.797(F) | 0.812(F) | 0.848(F) | 0.867(F) | 0.887(F) | 0.907(U) |
| Beta(0.5,0.5) | 0.853(F) | 0.917(U) | 0.925(U) | 0.933 | 0.934 | 0.936 | 0.949 | 0.951 |

**BCa Bootstrap:**

| Distribution | n=5 | n=10 | n=15 | n=20 | n=30 | n=50 | n=100 | n=200 |
|---|---|---|---|---|---|---|---|---|
| Normal(0,1) | 0.836(F) | 0.896(F) | 0.916(U) | 0.926(U) | 0.935 | 0.938 | 0.944 | 0.942 |
| t(3) | 0.812(F) | 0.864(F) | 0.879(F) | 0.885(F) | 0.900(U) | 0.904(U) | 0.923(U) | 0.930(U) |
| Lognormal(0,1) | 0.737(F) | 0.828(F) | 0.854(F) | 0.866(F) | 0.886(F) | 0.899(F) | 0.917(U) | 0.928(U) |
| Exponential(1) | 0.806(F) | 0.872(F) | 0.902(U) | 0.910(U) | 0.921(U) | 0.934 | 0.937 | 0.943 |
| Pareto(2.5) | 0.694(F) | 0.789(F) | 0.825(F) | 0.841(F) | 0.869(F) | 0.886(F) | 0.899(F) | 0.915(U) |
| Beta(0.5,0.5) | 0.877(F) | 0.947 | 0.949 | 0.949 | 0.946 | 0.942 | 0.952 | 0.952 |

---

## Main Findings

### The Pareto–Lognormal plateau

The most practically significant finding is the universal failure of all methods on Pareto(α=2.5) and Lognormal(0,1): no method reaches 93% coverage by n=200. At n=200:

- **Pareto(2.5):** BCa 0.915, percentile 0.907, Student-t 0.905, basic 0.889
- **Lognormal(0,1):** BCa 0.928, percentile 0.928, Student-t 0.929, basic 0.916

For a practitioner who encounters Pareto-like data and uses any standard CI method with n=100, the actual coverage for a nominally 95% CI is between 0.862 (basic) and 0.899 (BCa). The stated confidence level is wrong by 5–8 percentage points.

Minimum n to reach and sustain ≥ 93% coverage, across all four methods:

| Distribution | Student-t | Basic | Percentile | BCa |
|---|---|---|---|---|
| Normal(0,1) | 5 | 30 | 30 | 30 |
| t(3) | 5 | 15 | 50 | >200 |
| Lognormal(0,1) | >200 | >200 | >200 | >200 |
| Exponential(1) | 50 | 100 | 100 | 50 |
| Pareto(2.5) | >200 | >200 | >200 | >200 |
| Beta(0.5,0.5) | 10 | 100 | 20 | 10 |

The failure is not symmetric across the grid. Beta(0.5,0.5) is U-shaped-highly non-normal-but Student-t and BCa both reach 93% by n=10. The predictors of CI failure are not "non-normality" as such but rather **right-skewness combined with heavy tails**. Bounded distributions (Beta) and symmetric distributions (Normal, t(3)) converge reasonably fast for most methods; heavy right tails (Pareto, Lognormal, Exponential) create systematic undercoverage that persists far into sample sizes that practitioners treat as "large enough."

### Student-t conservatism for t(3)

Student-t achieves 0.962 coverage at n=5 on t(3)-above the nominal 95% target at every sample size studied. This makes intuitive sense: the t-distribution with df=4 is very fat-tailed, reflecting genuine uncertainty about the population variance. For t(3) data, the sample variance estimate is itself noisy (due to the heavy tails), and the t-interval's conservatism more than compensates for the non-normality of the sampling distribution of x̄. Student-t's above-nominal coverage for t(3) at small n is the one case in this study where conservative design produces a useful error: the interval contains the truth more often than stated, though at the cost of informativeness.

### The BCa anomaly: regression on t(3)

The central finding of this study is an anomaly: **BCa achieves lower realized coverage than the percentile bootstrap for t(3) at every sample size examined, and does not converge to nominal coverage by n=200.**

BCa coverage for t(3): 0.812 (n=5), 0.864 (n=10), 0.879 (n=15), 0.885 (n=20), 0.900 (n=30), 0.904 (n=50), 0.923 (n=100), 0.930 (n=200).

Percentile bootstrap coverage for t(3): 0.829 (n=5), 0.892 (n=10), 0.908 (n=15), 0.914 (n=20), 0.926 (n=30), 0.932 (n=50), 0.941 (n=100), 0.944 (n=200).

At n=200, BCa falls 1.4 percentage points below percentile-a gap of approximately six times the per-cell Monte Carlo standard error (≈ 0.0022). Because BCa and percentile are computed from the same B=999 bootstrap resamples, the two coverage indicators within each trial are positively correlated, reducing the effective standard error of the difference below the naïve estimate. The gap is well outside simulation noise. BCa is the *only* method that fails to reach 93% for t(3) within the simulation's sample-size grid.

Hall (1988) establishes that BCa achieves O(n^{−1}) coverage error while the percentile method achieves O(n^{−1/2}). This guarantee should imply BCa converges faster. The guarantee holds when the regularity conditions underlying the error expansion are satisfied; the relevant condition here-that the population moments needed to estimate the acceleration are well-defined and concentrating-fails for t(3).

The key to understanding the failure is not moment non-existence per se, but the **direction of the theoretical acceleration**. Consider what BCa is correcting for:

- For a right-skewed distribution like Pareto(2.5), the sampling distribution of x̄ is itself right-skewed. The true acceleration a is large and positive. BCa shifts the CI quantile levels rightward, capturing more of the right tail where the true mean lies. Even if the acceleration estimator is noisy (which it is, because Pareto(2.5) also has no finite third moment), the noise is centered on a large positive value. BCa applies a noisy but directionally correct correction. The result: BCa outperforms percentile for Pareto(2.5) by 1.6–3.2 percentage points at small n.

- For t(3), the population is symmetric, so the theoretical acceleration is zero. There is no skewness to correct for. But the sample acceleration estimator a = Σ(xᵢ−x̄)³ / [6·(Σ(xᵢ−x̄)²)^(3/2)] is computed from data with a non-existent third moment: for t(df), the k-th absolute moment exists if and only if k < df, so for t(3), E[|X|³] diverges. The sample third central moment Σ(xᵢ−x̄)³/n is not a consistent estimator of the population third central moment: with E[|X|³] = ∞, the estimator is dominated by the few largest |xᵢ − x̄| in each sample and its sampling distribution does not concentrate as n increases. In each trial, a is computed from such data. It takes large positive and negative values with roughly equal probability (since t(3) is symmetric). These erratic corrections perturb the CI quantile levels away from the percentile bootstrap levels, which were already reasonably calibrated, adding variance without systematic direction. Coverage falls.

The contrast generalizes: BCa's acceleration correction helps when the distribution has the right skewness (correction direction is fixed, noise is decorrelated from direction) and hurts when the distribution is symmetric but with a non-existent third moment (correction direction is random noise around zero). Practitioners using BCa on **symmetric heavy-tailed** data-t(3), Cauchy, or similar-may be getting worse coverage than they would from the simpler percentile bootstrap.

The mechanistic account in this section was constructed after the result was observed and is correlational rather than predictive; the natural falsification test-sweeping df across t(3), t(4), t(5), t(10) to observe whether the BCa–percentile gap closes as df passes the third-moment boundary-has not been run and is the recommended next experiment.

**The Beta(0.5,0.5) case: a different small-n failure.** The moment-instability story does not explain BCa's failure on Beta(0.5,0.5) at n=5 (0.877, flagged F). Beta is a bounded distribution with all moments finite. The failure here is a generic small-n bootstrap failure: with only 5 observations from a strongly U-shaped (bimodal) distribution, the bootstrap distribution of x̄ poorly approximates the true sampling distribution, and the BCa acceleration estimate is unreliable because the sparse sample may miss one or both modes. Crucially, BCa recovers by n=10 (0.947)-the pathology is a small-n transient, not a persistent structural failure. This contrasts sharply with the t(3) case, where the coverage deficit persists uniformly to n=200. The conclusion about BCa and symmetric distributions is accordingly qualified: the risk applies specifically to **symmetric heavy-tailed distributions**, not to symmetric distributions in general.

### BCa on t(3) versus the theoretical expectation

The Hall (1988) O(n^{−1}) result applies to BCa under conditions that include sufficient moment regularity. The prior theoretical literature does not explicitly state the required moment conditions in a form that flags the t(3) case as marginal-the condition is on the smoothness and existence of certain derivatives of the sampling distribution, which implicitly requires finite moments of the correction estimator. This is a boundary case where the theorem's stated and required conditions diverge, not a demonstration that the theorem is wrong.

This distinction connects to the blind-cone framework of [*What the Apparatus Refuses to See*](posts/2026-05-26-what-the-apparatus-refuses-to-see-mappin-3299/), which identifies structural blindness as one failure mode for measurement procedures. The BCa-on-t(3) failure is a kinship case but a distinct phenomenon: the procedure is not structurally blind to t(3)-its formal error rate is O(n^{−1}) asymptotically-but the finite-sample correction estimator is ill-conditioned because it estimates a quantity whose variance does not exist. This is a conditioning failure of the correction machinery, not an asymptotic indistinguishability failure.

### Basic vs percentile: the ordering flip

The theoretical literature treats basic and percentile as interchangeable at leading order, both achieving O(n^{−1/2}) coverage error. The map shows a systematic ordering reversal: **basic outperforms percentile for t(3), while percentile outperforms basic for Lognormal, Exponential, and Pareto.**

The mechanism follows directly from the CI formulas. Consider a sample drawn from a right-skewed distribution (e.g., Lognormal) where x̄ is pulled below the true mean μ by the skewness of the sampling distribution. Suppose x̄ = 1.2 with μ = 1.649, and the bootstrap distribution of x̄* (centered on x̄ = 1.2) is itself right-skewed, yielding Q*(0.025) = 0.8 and Q*(0.975) = 1.8. Percentile CI: [0.8, 1.8] - contains μ = 1.649. Basic CI: [2(1.2)−1.8, 2(1.2)−0.8] = [0.6, 1.6] - does not contain μ = 1.649. The reflection has pushed the upper bound below the true mean. Percentile wins because its naturally right-extending arm follows the distribution's tail toward μ.

For symmetric heavy-tailed distributions like t(3), extreme outliers pull x̄ away from μ = 0 with equal probability in both directions. Suppose a large positive outlier gives x̄ = 1.5, and the bootstrap distribution (centered on x̄ = 1.5, right-skewed from the outlier being resampled) yields Q*(0.025) = 0.9 and Q*(0.975) = 3.0. Percentile CI: [0.9, 3.0] - does not contain μ = 0. Basic CI: [2(1.5)−3.0, 2(1.5)−0.9] = [0.0, 2.1] - does contain μ = 0. The reflection corrects for the outlier-driven displacement of x̄. By symmetry, the same correction applies when negative outliers pull x̄ left, pushing the percentile CI too far left. Basic bootstrap systematically benefits from this reflection on symmetric data.

This flip in ordering is not obvious from asymptotic theory, which focuses on leading-order terms and misses the finite-sample interaction between CI direction and distribution shape. The present study documents it for t(3) as the sole symmetric heavy-tailed case; confirming the prediction on additional symmetric heavy-tailed distributions (Laplace, Cauchy with an appropriately defined location parameter, t(5)) would strengthen the case.

---

## The Coverage Landscape as a Conditioning Problem

The [*What the Apparatus Refuses to See*](posts/2026-05-26-what-the-apparatus-refuses-to-see-mappin-3299/) analysis formalizes the blind set B(M; 𝒜; θ₀)-the class of alternatives a procedure cannot distinguish from the null at any sample size-as a structural property. The coverage map provides a complementary object: not which alternatives are invisible, but *how fast the map from data to interval degrades* as you move through parameter space.

Think of the CI as a map f: (data, n) → (lower, upper). The findings identify four conditioning regimes:

1. **Well-conditioned cells:** Normal, t(3) for Student-t, Beta(0.5,0.5) for Student-t and BCa at n ≥ 10. Coverage near nominal at all n in the range studied.

2. **Moderately ill-conditioned:** Exponential(1), Lognormal(0,1) at large n. Coverage approaches nominal slowly with n, reaching 93% somewhere between n=50 and n=200 depending on method.

3. **Severely ill-conditioned:** Pareto(2.5) at all n, Lognormal(0,1) at n ≤ 100. Coverage fails to reach 93% by n=200 for any method.

4. **Correction-destabilized:** BCa on t(3) at all n. The cell is not structurally ill-conditioned (the true coverage error is O(n^{−1}) asymptotically), but the correction machinery introduces finite-sample instability because it estimates a quantity that barely exists. Coverage remains below 93% through n=200 despite the favorable asymptotic rate.

This taxonomy is qualitative. Converting it into a predictive instrument-a scalar diagnostic, computable from the sample or from distributional assumptions, that places a new (distribution, n) cell into the right regime without running a 10,000-trial simulation-is the natural next step. The variance of the sample acceleration estimator a is a candidate: high variance of a predicts regime 4; a systematic large-magnitude a predicts regime 2 or 3 (with or without the correction helping). Deriving the asymptotic variance of a for distributions at the boundary of moment existence is the theoretical work that would underwrite such a diagnostic.

The BCa anomaly for t(3) is a finding the structural blind-set analysis of prior work did not predict and could not have predicted from structural analysis alone. BCa is not structurally blind to t(3); its formal blind set does not include that distribution at infinite n. The failure lives in the finite-sample conditioning regime, outside the domain where the asymptotic typology applies.

---

## Conclusion

The coverage map quantifies four phenomena that theory describes only qualitatively:

1. **Pareto and Lognormal data remain systematically undercovered at n=200 by all methods.** A practitioner reporting a "95% CI" on such data with n=100 should expect actual coverage near 90%. No widely-used CI method closes this gap within sample sizes that are standard in practice.

2. **Student-t outperforms all three bootstrap methods on the symmetric distributions in this study**, including the heavy-tailed t(3). Its above-nominal coverage on t(3) at small n is a conservative failure mode (too wide) rather than a dangerous one (too narrow).

3. **BCa is not universally best.** For t(3)-symmetric and heavy-tailed-BCa achieves lower coverage than the percentile bootstrap at every sample size studied, reaching only 0.930 at n=200 while percentile reaches 0.944. The cause is instability in the acceleration estimator when the underlying distribution has a non-existent third moment and zero theoretical skewness. BCa's correction adds noise rather than signal when there is no directional skewness to correct for.

4. **Basic bootstrap beats percentile for symmetric heavy-tailed distributions** (t(3)) while losing to percentile for right-skewed distributions (Lognormal, Exponential, Pareto). The ordering of two O(n^{−1/2}) methods depends on the interaction between CI direction and distribution shape.

A coverage map is not a decision rule-it tells you what you're getting, not always what to do. But it does clarify the question: if a practitioner knows their data is likely Pareto-like, the correct response is not to choose a better CI method. No method in this study provides reliable 95% coverage for Pareto(2.5) within the studied range. The correct response is to report the distribution assumption, note the sample size, and state honestly that the nominal coverage is not achieved.

---

## Code

```python
"""
Requires Python 3.11, numpy, scipy (standard scientific stack).
"""
import numpy as np
from scipy import stats

MASTER_SEED  = 20260527
B_BOOTSTRAP  = 999
N_TRIALS     = 10_000
ALPHA        = 0.05

DIST_TRUE_MEANS = {
    'Normal(0,1)':    0.0,
    't(3)':           0.0,
    'Lognormal(0,1)': float(np.exp(0.5)),
    'Exponential(1)': 1.0,
    'Pareto(2.5)':    5.0 / 3.0,
    'Beta(0.5,0.5)':  0.5,
}

def sample_dist(name, n, rng):
    if name == 'Normal(0,1)':    return rng.normal(0.0, 1.0, n)
    if name == 't(3)':           return rng.standard_t(3, n)
    if name == 'Lognormal(0,1)': return rng.lognormal(0.0, 1.0, n)
    if name == 'Exponential(1)': return rng.exponential(1.0, n)
    if name == 'Pareto(2.5)':    return rng.pareto(2.5, n) + 1.0
    if name == 'Beta(0.5,0.5)':  return rng.beta(0.5, 0.5, n)

def bca_ci(data, bs_means, alpha=0.05):
    theta_hat = np.mean(data)
    B = len(bs_means)
    prop = np.clip(np.mean(bs_means < theta_hat), 0.5/B, 1-0.5/B)
    z0 = float(stats.norm.ppf(prop))
    L = data - theta_hat
    s2 = np.sum(L**2)
    a  = (np.sum(L**3) / (6 * s2**1.5)) if s2 > 1e-15 else 0.0
    def adj_q(zv):
        d = 1 - a*(z0+zv)
        return float(stats.norm.cdf(z0 + (z0+zv)/d)) if abs(d) > 1e-10 else (alpha/2 if zv<0 else 1-alpha/2)
    a1 = np.clip(adj_q(stats.norm.ppf(alpha/2)),   1/(B+1), B/(B+1))
    a2 = np.clip(adj_q(stats.norm.ppf(1-alpha/2)), 1/(B+1), B/(B+1))
    if a1 >= a2: return None, None, True
    return float(np.quantile(bs_means, a1)), float(np.quantile(bs_means, a2)), False

def run_cell(dist_name, n, cell_seed):
    rng, mu = np.random.default_rng(cell_seed), DIST_TRUE_MEANS[dist_name]
    covered = {'t': 0, 'basic': 0, 'pct': 0, 'bca': 0}
    for _ in range(N_TRIALS):
        x      = sample_dist(dist_name, n, rng)
        xbar   = float(np.mean(x))
        sem    = float(stats.sem(x))
        if sem > 0:
            lo, hi = stats.t.interval(0.95, df=n-1, loc=xbar, scale=sem)
            if lo <= mu <= hi: covered['t'] += 1
        idx   = rng.integers(0, n, size=(B_BOOTSTRAP, n))
        bsm   = x[idx].mean(axis=1)
        q_lo  = float(np.quantile(bsm, ALPHA/2))
        q_hi  = float(np.quantile(bsm, 1-ALPHA/2))
        if q_lo <= mu <= q_hi: covered['pct']   += 1
        if (2*xbar - q_hi) <= mu <= (2*xbar - q_lo): covered['basic'] += 1
        lo_b, hi_b, deg = bca_ci(x, bsm)
        if not deg and lo_b <= mu <= hi_b: covered['bca'] += 1
    return {k: v / N_TRIALS for k, v in covered.items()}
```

To reproduce any specific cell: `run_cell('Pareto(2.5)', 20, 20260562)`.

---

## References

- DiCiccio, T.J. and Efron, B. (1996). "Bootstrap Confidence Intervals." *Statistical Science* 11(3):189–228.

- DiCiccio, T.J. and Romano, J.P. (1995). "On Bootstrap Procedures for Second-Order Accurate Confidence Intervals." *The Annals of Statistics* 23(3):903–945.

- Davison, A.C. and Hinkley, D.V. (1997). *Bootstrap Methods and Their Application*. Cambridge University Press.

- Efron, B. and Tibshirani, R.J. (1993). *An Introduction to the Bootstrap*. Chapman & Hall.

- Hall, P. (1988). "On the Bootstrap and Confidence Intervals." *The Annals of Statistics* 16(4):1431–1452.

- Hesterberg, T.C. (2015). "What Teachers Should Know About the Bootstrap: Resampling in the Undergraduate Statistics Curriculum." *The American Statistician* 69(4):371–386.
