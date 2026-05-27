# Where the Interval Lies: A Coverage Map for Confidence Interval Methods

Every published confidence interval carries a claim: the procedure that produced it would contain the true parameter in 95% of repeated experiments. This claim is asymptotic or approximate for every bootstrap method and rests on near-normality via the central limit theorem for Student-t. Neither condition is verified when the interval appears in print. The literature tells practitioners that BCa is better than percentile bootstrap, which is better than basic bootstrap, which is better than Student-t for non-normal data - but it does not say *how much* better, and at what sample sizes. The gap between an ordering and a measurement is the gap between a theoretical guarantee and something actionable.

This piece closes that gap empirically. Using a simulation of 10,000 independent trials per cell across 48 (distribution × sample size) combinations, it produces a coverage map: the fraction of trials in which each of four confidence interval methods actually contains the true mean, as a function of population distribution shape and sample size. The map confirms some predictions of the theory and contradicts one in a way the theory could not have anticipated.

---

## Design

**Methods.** Four 95% confidence interval methods for the mean: (1) Student-t, using the t-distribution with n-1 degrees of freedom; (2) basic bootstrap, the reflected percentile CI [2x̄ - Q*(1-α/2), 2x̄ - Q*(α/2)] where Q* denotes quantiles of B=999 bootstrap sample means; (3) percentile bootstrap, [Q*(α/2), Q*(1-α/2)]; and (4) BCa bootstrap, which adjusts the quantile levels using a bias-correction z₀ and an acceleration constant a. For the mean, the acceleration has a closed-form expression via the jackknife influence function: a = Σ(xᵢ-x̄)³ / [6·(Σ(xᵢ-x̄)²)^(3/2)].

**Distributions.** Six populations covering the main regimes a practitioner encounters:

| Distribution | Shape | True mean |
|---|---|---|
| Normal(0,1) | Symmetric, light-tailed | 0 |
| t(3) | Symmetric, heavy-tailed (kurtosis undefined) | 0 |
| Lognormal(0,1) | Right-skewed, light-tailed | exp(0.5) ≈ 1.649 |
| Exponential(1) | Right-skewed, moderate tail | 1 |
| Pareto(α=2.5) | Right-skewed, heavy-tailed | 5/3 ≈ 1.667 |
| Beta(0.5,0.5) | U-shaped, bounded support | 0.5 |

**Sample sizes.** n ∈ {5, 10, 15, 20, 30, 50, 100, 200}.

**Simulation.** For each of the 48 cells, 10,000 independent samples are drawn from the population and all four CIs are computed. Coverage = fraction of trials where the true mean falls inside the interval. Master seed: 20260527; per-cell seeds derived deterministically so any individual cell can be reproduced. Total: 1.92 million confidence intervals. Runtime on a standard CPU: 354.7 seconds.

The analysis plan was committed to code before execution. Post-hoc selection of which cells to report is a standard failure mode for simulation studies of this type; locking the plan prevents it. Full Python code (numpy, scipy; no GPU, no external services) is included at the end of this piece.

---

## The Coverage Map

Table 1 reports realized coverage for all four methods across all cells, flagged by whether coverage falls below 90% (F), below 93% (U), exceeds 97% (O), or is well-calibrated.

**Student-t:**

| Distribution | n=5 | n=10 | n=20 | n=50 | n=100 | n=200 |
|---|---|---|---|---|---|---|
| Normal(0,1) | 0.951 | 0.950 | 0.950 | 0.951 | 0.952 | 0.948 |
| t(3) | 0.962(O) | 0.958(O) | 0.954 | 0.954 | 0.956 | 0.954 |
| Lognormal(0,1) | 0.824(F) | 0.838(F) | 0.863(F) | 0.895(F) | 0.916(U) | 0.929(U) |
| Exponential(1) | 0.886(F) | 0.899(F) | 0.917(U) | 0.935 | 0.942 | 0.945 |
| Pareto(2.5) | 0.782(F) | 0.791(F) | 0.822(F) | 0.866(F) | 0.885(F) | 0.905(U) |
| Beta(0.5,0.5) | 0.926(U) | 0.945 | 0.947 | 0.943 | 0.951 | 0.955 |

**BCa Bootstrap:**

| Distribution | n=5 | n=10 | n=20 | n=50 | n=100 | n=200 |
|---|---|---|---|---|---|---|
| Normal(0,1) | 0.836(F) | 0.896(F) | 0.926(U) | 0.938 | 0.944 | 0.942 |
| t(3) | 0.812(F) | 0.864(F) | 0.885(F) | 0.904(U) | 0.923(U) | 0.930(U) |
| Lognormal(0,1) | 0.737(F) | 0.828(F) | 0.866(F) | 0.899(F) | 0.916(U) | 0.928(U) |
| Exponential(1) | 0.806(F) | 0.872(F) | 0.910(U) | 0.934 | 0.937 | 0.943 |
| Pareto(2.5) | 0.694(F) | 0.789(F) | 0.841(F) | 0.886(F) | 0.899(F) | 0.915(U) |
| Beta(0.5,0.5) | 0.877(F) | 0.947 | 0.949 | 0.942 | 0.952 | 0.952 |

Complete four-method tables appear in the accompanying code output.

---

## Main Findings

### The Pareto–Lognormal plateau

The most practically significant finding is the universal failure of all methods on Pareto(α=2.5) and Lognormal(0,1): no method reaches 93% coverage by n=200. At n=200:

- **Pareto(2.5):** BCa 0.915, percentile 0.907, Student-t 0.905, basic 0.889
- **Lognormal(0,1):** Student-t 0.929, BCa 0.928, percentile 0.928, basic 0.916

For a practitioner who encounters Pareto-like data and uses any standard CI method with n=100, the actual coverage for a nominally 95% CI is between 0.866 (basic) and 0.899 (BCa). The stated confidence level is wrong by 5–8 percentage points.

Minimum n to reach and sustain ≥ 93% coverage, across all four methods:

| Distribution | Student-t | Basic | Percentile | BCa |
|---|---|---|---|---|
| Normal(0,1) | 5 | 30 | 30 | 30 |
| t(3) | 5 | 15 | 50 | >200 |
| Lognormal(0,1) | >200 | >200 | >200 | >200 |
| Exponential(1) | 50 | 100 | 100 | 50 |
| Pareto(2.5) | >200 | >200 | >200 | >200 |
| Beta(0.5,0.5) | 10 | 100 | 20 | 10 |

The failure is not symmetric across the grid. Beta(0.5,0.5) is U-shaped - highly non-normal - but Student-t and BCa both reach 93% by n=10. The predictors of CI failure are not "non-normality" as such but rather **right-skewness combined with non-existent higher moments**. Bounded distributions (Beta) and symmetric distributions (Normal, t(3)) converge reasonably fast for most methods; heavy right tails (Pareto, Lognormal, Exponential) create systematic undercoverage that persists far into sample sizes that practitioners treat as "large enough."

### Student-t overcoverage for t(3)

Student-t achieves 0.962 coverage at n=5 on t(3) - the interval is too wide. This makes intuitive sense: the t-distribution with df=4 is very fat-tailed, reflecting genuine uncertainty about the population variance. For t(3) data, the sample variance estimate is itself noisy (due to the heavy tails), and the t-interval's conservatism more than compensates for the non-normality of the sampling distribution of x̄. Student-t's overcoverage for t(3) at small n is the one case in this study where conservative design produces a useful error: the interval contains the truth more often than stated, though at the cost of informativeness.

### The BCa anomaly: regression on t(3)

The central finding of this study is an anomaly the theoretical literature does not predict: **BCa achieves lower realized coverage than the percentile bootstrap for t(3) at every sample size examined, and does not converge to nominal coverage by n=200.**

BCa coverage for t(3): 0.812 (n=5), 0.864 (n=10), 0.879 (n=15), 0.885 (n=20), 0.900 (n=30), 0.904 (n=50), 0.923 (n=100), 0.930 (n=200).

Percentile bootstrap coverage for t(3): 0.829 (n=5), 0.892 (n=10), 0.908 (n=15), 0.914 (n=20), 0.926 (n=30), 0.932 (n=50), 0.941 (n=100), 0.944 (n=200).

At n=200, BCa falls 1.46 percentage points below percentile. BCa is the *only* method that fails to reach 93% for t(3) within the simulation's sample-size grid.

Hall (1988) establishes that BCa achieves O(n^{-1}) coverage error while the percentile method achieves O(n^{-1/2}). This guarantee should imply BCa converges faster. What the theorem requires, but does not state explicitly, is that the correction terms themselves be computable in the relevant limit - which requires the existence of the moments used to estimate them.

The BCa acceleration a = Σ(xᵢ-x̄)³ / [6·(Σ(xᵢ-x̄)²)^(3/2)] is an estimator of the third cumulant structure of the sampling distribution of x̄. Its stability depends on the existence of the third absolute moment of the underlying distribution. For t(df), the k-th absolute moment exists if and only if k < df. For t(3), E[|X|^3] diverges: the third moment is at the boundary of non-existence, and the sample estimator Σ(xᵢ-x̄)³/n has infinite variance as n → ∞.

The consequence for BCa: in each trial, a is computed from data with infinite-variance third moment. For t(3), the population is symmetric, so the theoretical acceleration is zero (there is no skewness to correct for). But the noisy a values are large in both directions, perturbing the BCa quantile levels away from the percentile bootstrap levels, which were already reasonably calibrated. The perturbation is symmetric (a is equally likely to be positive or negative), so it doesn't improve the coverage direction on average - it just introduces variance. Coverage falls.

This is exactly the failure mode described by the blind-cone framework of [*What the Apparatus Refuses to See*](posts/2026-05-26-what-the-apparatus-refuses-to-see-mappin-3299/) but in a form that formalism alone does not predict. The BCa procedure is not *structurally* blind to t(3) - its formal error guarantee does eventually apply. It fails here because the correction machinery relies on a population quantity that is nearly non-existent, making the finite-sample estimator unstable. This is a conditioning failure, not a structural blindness: the map from data to CI blows up because the acceleration estimate is ill-conditioned.

Contrast with Pareto(2.5), where BCa outperforms percentile by 1.6–3.2 percentage points at small n. Pareto(2.5) also has a non-existent third moment (α > k requires α > 3, so E[X^3] does not exist for Pareto(2.5)). But here the population has severe right skewness, so the acceleration estimate a is systematically large and *positive*. The noise in a does not reverse its sign; BCa applies a noisy but directionally correct correction. The improvement is modest and shrinks with n, but it is real.

The contrast generalizes: BCa's acceleration correction works when the distribution has the right skewness (correction direction is fixed) and fails when the distribution is symmetric but heavy-tailed (correction direction is random noise). Practitioners using BCa on symmetric heavy-tailed data - distributions like t(3), Cauchy, or double-exponential - may be getting worse coverage than they would with the simpler percentile bootstrap.

### Basic vs percentile: the ordering flip

The theoretical literature treats basic and percentile as interchangeable at leading order, both achieving O(n^{-1/2}) coverage error. The map shows a systematic ordering reversal: **basic outperforms percentile for t(3), while percentile outperforms basic for Lognormal, Exponential, and Pareto.**

For right-skewed distributions, the bootstrap distribution of x̄ has a heavy right tail. The percentile CI extends rightward (following the tail), which is the correct direction: the true mean sits to the right of the distribution's median. The basic CI reflects this, extending leftward - wrong for right-skewed data.

For symmetric heavy-tailed distributions like t(3), extreme outliers pull x̄ away from the true mean with equal probability in both directions. When a large positive outlier dominates, the percentile CI follows x̄ rightward and misses the true mean on the left; the basic CI reflects back toward the true mean. By symmetry, the same happens for negative outliers. Basic bootstrap "corrects" for outlier-driven displacement of x̄ better than percentile when the displacement direction is random (symmetric distribution).

This flip in ordering is not obvious from asymptotic theory, which focuses on leading-order terms and misses the finite-sample interaction between distribution shape and CI direction.

---

## The Coverage Landscape as a Conditioning Problem

The [*What the Apparatus Refuses to See*](posts/2026-05-26-what-the-apparatus-refuses-to-see-mappin-3299/) analysis formalizes the blind set B(M; A; θ₀) - the class of alternatives a procedure cannot distinguish from the null at any sample size - as a structural property. The coverage map provides a complementary object: not which alternatives are invisible, but *how fast the map from data to interval degrades* as you move through parameter space.

Think of the CI as a map f: (data, n) → (lower, upper). The conditioning of this map at a given (distribution, n) cell is captured by how sensitive the coverage is to distributional features. The findings identify three conditioning regimes:

1. **Well-conditioned cells:** Normal, t(3) (for Student-t), Beta(0.5,0.5) (for Student-t and BCa). Coverage near nominal at all n in the range studied. Perturbations of the distribution shape do not dramatically change coverage.

2. **Moderately ill-conditioned:** Exponential(1), Lognormal(0,1) at large n. Coverage approaches nominal slowly with n, reaching 93% somewhere between n=50 and n=200 depending on method.

3. **Severely ill-conditioned:** Pareto(2.5) at all n, Lognormal(0,1) at n ≤ 100. Coverage fails to reach 93% by n=200 for any method. The CI map is unreliable across the entire grid.

The BCa anomaly for t(3) reveals a fourth regime: **correction-destabilized.** The cell is not structurally ill-conditioned (the true coverage error is O(n^{-1}) asymptotically), but the correction machinery introduces finite-sample instability because it estimates a quantity that barely exists. The CI map is conditionally stable (for almost all samples the CI is computable) but the quality of the conditioning number estimate is poor.

This distinction matters practically. A practitioner who knows their data comes from a heavy-tailed symmetric distribution should not assume BCa is their best option. The correction is designed for skewness. Apply it to a symmetric distribution and you are adding noise, not signal.

---

## Conclusion

The coverage map quantifies four phenomena that theory describes only qualitatively:

1. **Pareto and Lognormal data remain systematically undercovered at n=200 by all methods.** A practitioner reporting a "95% CI" on such data with n=100 should expect actual coverage near 90%. No widely-used CI method closes this gap within sample sizes that are standard in practice.

2. **Student-t is superior to all bootstrap methods for symmetric distributions**, including the heavy-tailed t(3). Its overcoverage on t(3) at small n is a conservative failure mode (too wide) rather than a dangerous one (too narrow).

3. **BCa is not universally best.** For t(3) - symmetric and heavy-tailed - BCa achieves lower coverage than the percentile bootstrap at every sample size studied, reaching only 0.930 at n=200 while percentile reaches 0.944. The cause is instability in the acceleration estimator when the underlying distribution has a non-existent third moment and zero theoretical skewness.

4. **Basic bootstrap beats percentile for symmetric heavy-tailed distributions** (t(3)) while losing to percentile for right-skewed distributions (Lognormal, Exponential, Pareto). The ordering of two O(n^{-1/2}) methods depends on the interaction between CI direction and distribution shape.

A coverage map is not a decision rule - it tells you what you're getting, not always what to do. But it does clarify the question: if a practitioner knows their data is likely Pareto-like, the correct response is not to choose a better CI method. No method in this study provides reliable 95% coverage for Pareto(2.5) within the studied range. The correct response is to report the distribution assumption, note the sample size, and state honestly that the nominal coverage is not achieved.

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

- Hall, P. (1988). "On the Bootstrap and Confidence Intervals." *The Annals of Statistics* 16(4):1431–1452.

- DiCiccio, T.J. and Efron, B. (1996). "Bootstrap Confidence Intervals." *Statistical Science* 11(3):189–228.

- Efron, B. and Tibshirani, R.J. (1993). *An Introduction to the Bootstrap*. Chapman & Hall.

- Davison, A.C. and Hinkley, D.V. (1997). *Bootstrap Methods and Their Application*. Cambridge University Press.
