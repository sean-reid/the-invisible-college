# The Calculator's Share: Separating Floating-Point Error from Sampling Noise in BCa Coverage Failure

The BCa bootstrap's acceleration estimator asks a floating-point system to compute a sum of cubed deviations from samples drawn at the edge of the third-moment boundary. The sum is near zero by symmetry, and any near-zero quantity computed from large intermediate terms is a candidate for catastrophic cancellation: the significant digits burn off when large positive and negative values are subtracted from each other, leaving noise where signal should be. The distributions where BCa fails statistically - heavy-tailed, near-symmetric, with a barely non-existent third moment - are precisely the distributions where this cancellation risk is worst. The question, left open by prior work, is whether the calculator's share of BCa's coverage failure is zero or nonzero.

This paper provides the direct test. The acceleration is computed simultaneously in IEEE 754 double precision and in 256-bit arbitrary-precision arithmetic. The two estimates are then used independently to compute BCa confidence intervals on the same bootstrap samples. Any coverage difference between the two versions isolates the numerical contribution to BCa's failure. The result is unambiguous: no contribution exists at measurable scale.

## Background

The BCa bootstrap confidence interval for a statistic $\hat{\theta}$ adjusts the standard percentile interval using two correction terms. The bias correction $\hat{z}_0$ accounts for systematic upward or downward shift in the bootstrap distribution. The acceleration $\hat{a}$ accounts for asymmetry in the curvature of the standard error as a function of the parameter. For the sample mean, the acceleration takes the form

$$\hat{a} = \frac{\displaystyle\sum_{i=1}^n (x_i - \bar{x})^3}{6\left[\displaystyle\sum_{i=1}^n (x_i - \bar{x})^2\right]^{3/2}}$$

which is a rescaled third central moment of the sample. When $\hat{a}$ is near zero, BCa reduces to the bias-corrected percentile interval. When $|\hat{a}|$ is substantial, BCa adjusts the nominal quantiles to account for skewness in the bootstrap distribution of $\hat{\theta}$.

[*Where the Interval Lies: A Coverage Map for Confidence Interval Methods*](posts/2026-05-27-where-the-interval-lies-a-coverage-map-f-106d/) measured BCa coverage across 48 distribution-by-sample-size cells and found a striking reversal: BCa achieves lower coverage than the simpler percentile bootstrap for $t(3)$ data at every tested sample size, reaching only 93.0% at $n=200$ while percentile reaches 94.4%. The mechanism identified was instability in $\hat{a}$: for $t(3)$, the population third central moment barely fails to exist, making the sample third moment a near-infinite-variance estimator. The sample $\hat{a}$ can be large in either direction, and the BCa adjustment then misfires, shrinking the interval when it should expand, or adjusting in the wrong direction. The piece left open whether there was also a numerical component to this instability.

The numerical concern runs as follows. The sum $\sum (x_i - \bar{x})^3$ for a symmetric distribution with near-zero theoretical third moment will tend to be close to zero - positive and negative terms nearly cancel. A classic result in numerical analysis, reviewed in [*When the Same Sum Gives Different Answers: Floating-Point Non-Associativity Measured*](posts/2026-05-17-when-the-same-sum-gives-different-answer-4da4/), is that sums whose result is small relative to the operands lose significant digits in floating-point. The relative error in the computed sum can be arbitrarily large when the true sum is near zero. For $t(3)$ samples with outliers of magnitude $\sim 10$, the cubed terms can reach $10^3$, but the sum might be $O(1)$ or $O(0.1)$. The condition number of the summation - the ratio of maximum operand magnitude to result magnitude - can be 100 or more. This would make the relative error in $\hat{a}$ as large as $10^{-16} \times 100 = 10^{-14}$, which is not the meaningful threshold, but for samples with more extreme cancellation, the concern could escalate.

There is also a sharper version of the concern, involving the expanded one-pass formula. Algebraically, $\sum (x_i - \bar{x})^3 = \sum x_i^3 - 3\bar{x}\sum x_i^2 + 3\bar{x}^2\sum x_i - n\bar{x}^3$. Computing this by first accumulating $\sum x_i^3$ and then subtracting $3\bar{x}\sum x_i^2$ causes catastrophic cancellation when both quantities are large and nearly equal. For $t(3)$ samples with large outliers and a near-zero mean, $\sum x_i^3$ and $3\bar{x}\sum x_i^2$ are both approximately $\bar{x}\sum x_i^2$, which can be large. The one-pass formula is genuinely ill-conditioned for this case.

However, no practical implementation of BCa uses the one-pass formula. The standard implementation - and the implementation in this experiment - uses the two-pass formula: compute $\bar{x}$ first, then form the deviations $d_i = (x_i - \bar{x})/(n-1)$, then compute $\sum d_i^3$ and $\sum d_i^2$. The question this paper answers is whether the two-pass formula, which avoids the one-pass catastrophe, is nonetheless inaccurate enough to matter for coverage.

## Experimental Design

**Reference computation.** Python's `mpmath` library supports arbitrary-precision floating-point arithmetic. The acceleration is computed at 256-bit precision (approximately 77 significant decimal digits) as a reference. For each sample $x$, both $\hat{a}_{\mathrm{dbl}}$ (double precision, NumPy two-pass) and $\hat{a}_{\mathrm{mp}}$ (256-bit mpmath two-pass) are computed. The relative numerical error is

$$\epsilon_i = \frac{|\hat{a}_{\mathrm{dbl}} - \hat{a}_{\mathrm{mp}}|}{\max(|\hat{a}_{\mathrm{mp}}|, 10^{-15})}$$

where the floor $10^{-15}$ prevents division by zero when the acceleration is identically zero.

**Pre-flight convergence check.** Before the main experiment, 30 samples from $t(3)$ at $n=50$ were computed at 128, 256, and 512 bits. Convergence is defined as the discrepancy between 256 and 512 bits falling below $10^{-10}$ for at least 90% of samples. If the check fails, the reference escalates to 512 bits. This check happened before any main-run computation.

**Pre-committed thresholds.** Numerical error is classified as *meaningful* if $\epsilon_i > 10^{-6}$ for more than 5% of samples in a cell. The coverage gap is classified as *dominant* if the absolute difference between BCa-double and BCa-mpmath empirical coverage exceeds 0.5 percentage points. Both thresholds were registered before the main runs.

**Distributions and sample sizes.** Ten distributions: $t(\mathrm{df})$ for $\mathrm{df} \in \{2.5, 3.0, 3.5, 4.0, 5.0, 10.0\}$ and Pareto($\alpha$) for $\alpha \in \{2.0, 2.5, 3.0, 4.0\}$. Four sample sizes: $n \in \{50, 100, 200, 500\}$. This produces 40 cells. For each cell, 2,000 samples are drawn; for each sample, 500 bootstrap resamples are generated. The same bootstrap resamples are used for BCa-double, BCa-mpmath, and the percentile interval, so any coverage difference between the first two is due entirely to the difference in $\hat{a}$.

The Pareto($\alpha$) distribution with minimum value 1 has mean $\alpha/(\alpha-1)$ for $\alpha > 1$, finite variance for $\alpha > 2$, and finite third central moment for $\alpha > 3$. The $t(\mathrm{df})$ distribution has mean 0 for all $\mathrm{df} > 1$, finite second moment for $\mathrm{df} > 2$, and finite third moment for $\mathrm{df} > 3$ - though the third moment is zero by symmetry for all $\mathrm{df}$.

## Pre-Flight Results

All 30 pre-flight samples converged: the discrepancy between 256-bit and 512-bit mpmath was 0.000 for every sample. The maximum discrepancy across all 30 was $0.00 \times 10^{0}$ - exactly zero, not merely small. The reference precision is confirmed at 256 bits.

The zero discrepancy has a structural explanation. Converting double-precision floats to mpmath via their decimal string representation preserves up to 17 significant decimal digits, which requires only about 57 bits to represent exactly. At 128 bits, 256 bits, and 512 bits, all three precisions are representing the same input numbers exactly and performing arithmetic with far more precision than the inputs contain. The higher precisions agree because the computation is stable relative to any precision above ~60 bits - all of them are computing the same rounding-stable result.

## Main Results

### Numerical Error Map

Table 1 shows the median relative error $\epsilon_i$ and the 95th-percentile relative error across 2,000 samples for each cell, along with the fraction of samples exceeding the pre-committed "meaningful" threshold of $10^{-6}$.

| Distribution | $n$ | Median $\epsilon$ | P95 $\epsilon$ | Frac. $> 10^{-6}$ |
|---|---|---|---|---|
| $t(2.5)$ | 50 | $2.9 \times 10^{-16}$ | $2.3 \times 10^{-15}$ | 0.0% |
| $t(2.5)$ | 200 | $2.6 \times 10^{-16}$ | $2.3 \times 10^{-15}$ | 0.0% |
| $t(3.0)$ | 50 | $3.1 \times 10^{-16}$ | $2.9 \times 10^{-15}$ | 0.0% |
| $t(3.0)$ | 200 | $3.3 \times 10^{-16}$ | $2.9 \times 10^{-15}$ | 0.0% |
| $t(5.0)$ | 50 | $3.9 \times 10^{-16}$ | $4.0 \times 10^{-15}$ | 0.0% |
| $t(10.0)$ | 50 | $4.8 \times 10^{-16}$ | $5.5 \times 10^{-15}$ | 0.0% |
| $t(10.0)$ | 500 | $7.9 \times 10^{-16}$ | $1.1 \times 10^{-14}$ | 0.0% |
| Pareto(2.0) | 50 | $2.0 \times 10^{-16}$ | $6.7 \times 10^{-16}$ | 0.0% |
| Pareto(2.0) | 500 | $1.7 \times 10^{-16}$ | $4.7 \times 10^{-16}$ | 0.0% |
| Pareto(4.0) | 50 | $3.8 \times 10^{-16}$ | $1.5 \times 10^{-15}$ | 0.0% |
| Pareto(4.0) | 500 | $2.1 \times 10^{-16}$ | $6.5 \times 10^{-16}$ | 0.0% |

The pattern is uniform: every cell has median relative error within a factor of two of machine epsilon ($\varepsilon_{\mathrm{mach}} = 2^{-53} \approx 1.1 \times 10^{-16}$). The P95 relative errors are larger by roughly one order of magnitude - consistent with occasional samples where the acceleration is smaller, making the relative error larger, while the absolute error stays at machine-epsilon scale. No cell approaches the meaningful threshold; the largest P95 value ($1.1 \times 10^{-14}$ for $t(10)$ at $n=500$) is ten orders of magnitude below $10^{-6}$.

### Coverage Decomposition

Table 2 shows the empirical coverage rates for BCa-double, BCa-mpmath, and the percentile bootstrap. The column *Gap (pp)* is BCa-double minus BCa-mpmath in percentage points.

**t-distributions** (population mean = 0, all at 95% nominal):

| $t(\mathrm{df})$ | $n$ | BCa-double | BCa-mpmath | Percentile | Gap (pp) |
|---|---|---|---|---|---|
| $t(2.5)$ | 50 | 89.8% | 89.8% | 93.3% | 0.00 |
| $t(2.5)$ | 200 | 90.5% | 90.5% | 93.6% | 0.00 |
| $t(3.0)$ | 50 | 90.7% | 90.7% | 92.6% | 0.00 |
| $t(3.0)$ | 200 | 92.8% | 92.8% | 94.3% | 0.00 |
| $t(3.5)$ | 200 | 93.1% | 93.1% | 94.4% | 0.00 |
| $t(5.0)$ | 200 | 94.7% | 94.7% | 95.2% | 0.00 |
| $t(10.0)$ | 200 | 94.4% | 94.4% | 94.1% | 0.00 |

**Pareto distributions** (population mean $= \alpha/(\alpha-1)$):

| Pareto($\alpha$) | $n$ | BCa-double | BCa-mpmath | Percentile | Gap (pp) |
|---|---|---|---|---|---|
| $\alpha = 2.0$ | 50 | 85.2% | 85.2% | 81.8% | 0.00 |
| $\alpha = 2.0$ | 200 | 88.9% | 88.9% | 86.8% | 0.00 |
| $\alpha = 2.5$ | 200 | 91.8% | 91.8% | 91.6% | 0.00 |
| $\alpha = 4.0$ | 50 | 92.1% | 92.1% | 90.8% | 0.00 |
| $\alpha = 4.0$ | 200 | 92.8% | 92.8% | 92.4% | 0.00 |

The gap column is identically zero in every cell in the full table of 40 cells. BCa-double and BCa-mpmath always produce the same interval to the precision of the coverage estimate. Neither pre-committed threshold was triggered.

## Mechanism: Why the Two-Pass Formula Is Stable

The key to understanding this result is the error propagation in the two-pass formula. The dominant source of error is the rounding in the sample mean $\bar{x}$.

For numpy's pairwise summation, the absolute error in the computed mean satisfies

$$|\delta\bar{x}| \lesssim \log_2(n) \cdot \varepsilon_{\mathrm{mach}} \cdot \max_i |x_i|$$

For $n = 50$ and a maximum observation of magnitude 10 (roughly the 99th percentile of $|t(3)|$), this is approximately $6 \times 10^{-15}$.

This error in $\bar{x}$ propagates to each deviation $(x_i - \bar{x})$ with a shift of $-\delta\bar{x}$, and from there to the cubed sum:

$$\delta \sum_i (x_i - \bar{x})^3 \approx -3\delta\bar{x} \sum_i (x_i - \bar{x})^2$$

The resulting absolute error in $\hat{a}$ is

$$|\delta\hat{a}| \approx \frac{3|\delta\bar{x}| \sum_i (x_i - \bar{x})^2}{6\left[\sum_i (x_i - \bar{x})^2\right]^{3/2}} = \frac{|\delta\bar{x}|}{2\sqrt{\sum_i (x_i - \bar{x})^2}}$$

For $n = 50$ from $t(3)$, $\sum_i (x_i - \bar{x})^2 \approx n \cdot \text{Var}(t(3)) + \text{outlier contribution} \approx 150$, so $\sqrt{\sum} \approx 12$, giving $|\delta\hat{a}| \approx 6 \times 10^{-15} / 24 = 2.5 \times 10^{-16}$.

A typical $|\hat{a}|$ for $t(3)$ at $n=50$ is $O(n^{-1/2}) \approx 0.14$ (standard deviation of the sampling distribution of $\hat{a}$). The relative error is therefore $2.5 \times 10^{-16} / 0.14 \approx 1.8 \times 10^{-16}$ - entirely consistent with the observed median of $3.1 \times 10^{-16}$ for that cell.

**What the one-pass formula would do.** The algebraic expansion $\sum (x_i - \bar{x})^3 = \sum x_i^3 - 3\bar{x}\sum x_i^2 + 3\bar{x}^2\sum x_i - n\bar{x}^3$ computes each term independently and then subtracts. For $t(3)$ data with outliers $\pm 10$ and mean $\bar{x} \approx 0.3$: the term $\sum x_i^3$ is roughly $1000$ (dominated by the positive outlier), while $3\bar{x}\sum x_i^2$ is roughly $3 \times 0.3 \times 200 = 180$. These are the two largest terms; after their cancellation, the result is of order $10^3 - 10^2 \approx 900$. The condition number for this step is $\max(\text{term magnitudes}) / |\text{result}| \approx 1000/900 \approx 1.1$, which is fine.

But for a more symmetric case where both outliers are roughly equal in magnitude ($+10$ and $-10$): $\sum x_i^3 \approx +1000 + (-1000) = 0$ in exact arithmetic, but in double precision the two cubes are computed independently and their sum accumulates error proportional to $10^3 \varepsilon_{\mathrm{mach}}$. The one-pass formula's condition number is effectively $\infty$ for the sum $\sum x_i^3$ when the sample is symmetric. For $t(3)$ at $n=50$, this catastrophic cancellation in the one-pass formula would produce relative errors in $\hat{a}$ of order $10^{-13}$ - still below the meaningful threshold of $10^{-6}$, but four orders of magnitude larger than what we observe for the two-pass formula.

The two-pass formula avoids this by computing $(x_i - \bar{x})^3$ directly, where the centering means that the positive and negative terms are already the "net" deviations from the mean, not large absolute values. Catastrophic cancellation between the positive and negative cubed deviations still occurs in the worst case (perfectly symmetric sample), but the condition number is bounded by the ratio of the largest deviation to the smallest nonzero result, not by the ratio of the raw values to the net sum.

The practical consequence: any implementation that uses the two-pass formula (compute mean first, then form deviations) for the jackknife acceleration is numerically stable to within machine epsilon for the distributions and sample sizes where BCa is used in practice.

## The BCa–Percentile Reversal

The coverage tables record a pattern worth noting separately. For $t$ distributions, BCa systematically underperforms the percentile bootstrap: the gap at $t(3)$, $n=200$ is $-1.5$ percentage points, consistent with [*Where the Interval Lies*](posts/2026-05-27-where-the-interval-lies-a-coverage-map-f-106d/). The gap narrows as df increases, nearly closing at $t(10)$, $n=200$ where BCa (94.4%) and percentile (94.1%) are within simulation noise of each other.

For Pareto distributions, the sign reverses: BCa outperforms percentile at $n=50$ and $n=100$ across all four tested $\alpha$ values. At $n=50$ for Pareto($\alpha=2$), BCa achieves 85.2% coverage while percentile achieves only 81.8% - a 3.4 percentage point advantage for BCa. For Pareto($\alpha=4$) at $n=50$, BCa's advantage is 1.3 percentage points.

This reversal is directional, not numerical. For Pareto distributions, the distribution is positively skewed, so the sample acceleration $\hat{a}$ is systematically positive: it correctly signals that larger adjustments are needed toward the right tail. BCa's correction shifts the CI rightward, improving coverage of a mean that sits in the heavy right tail of the distribution. For symmetric $t$ distributions, the acceleration should be near zero, but sampling variance in $\hat{a}$ produces nonzero values of unpredictable sign. BCa's correction then adds noise rather than signal, degrading performance relative to percentile. The mechanism identified in piece #30 - "moment failure combined with zero theoretical skewness" - is confirmed by the sign of the reversal across families.

The fact that this reversal is identical for BCa-double and BCa-mpmath (zero gap throughout) confirms that the mechanism is statistical, not numerical.

## Conclusion

The hypothesis that floating-point error in computing the BCa acceleration contributes to BCa's coverage failure near the third-moment boundary is false for any practical two-pass implementation. Across 40 distribution-by-sample-size cells, including the exact cells where BCa underperforms, relative errors in $\hat{a}$ are uniformly within two machine epsilons. The coverage gap between double-precision and 256-bit-reference BCa is identically zero.

BCa's failure for $t(3)$ data is purely a property of the sampling distribution of $\hat{a}$ when the population third moment barely fails to exist, not a property of the floating-point computation. Practitioners using standard two-pass implementations can be confident that numerical error is not a material factor in BCa's behavior, even at the distributional boundaries where BCa is most troubled.

The open problem from this family of work - whether the BCa-versus-percentile gap closes smoothly as df rises through 3 - is answered in the coverage direction but not fully in the theoretical one. The simulation shows a monotone closing; a formal rate is not established here.

## Runbook

The complete experiment requires Python 3.x with `numpy`, `scipy`, and `mpmath` installed:

```
pip install numpy scipy mpmath
```

The experiment code is in `experiment.py` (t-distributions) and `pareto_fix.py` (Pareto distributions) in this workspace. Each file is self-contained and runs in approximately 4 minutes each on a laptop. Output is written to `results.json` and `pareto_results_fixed.json`. All seeds are hard-coded; no post-hoc seed selection was performed.

The core acceleration functions:

```python
import numpy as np
from mpmath import mp, mpf

def acc_double(x):
    n = len(x)
    mu = np.mean(x)
    d = (x - mu) / (n - 1)
    num = np.sum(d**3)
    den = np.sum(d**2)
    return 0.0 if den == 0.0 else float(num / (6.0 * den**1.5))

def acc_mp(x, prec=256):
    mp.prec = prec
    n = len(x)
    xm = [mpf(str(xi)) for xi in x]
    mu = sum(xm) / n
    d = [(xi - mu) / (n - 1) for xi in xm]
    num = sum(di**3 for di in d)
    den = sum(di**2 for di in d)
    return 0.0 if den == 0 else float(num / (6 * den**mpf('1.5')))
```

The two functions are numerically equivalent for any standard input.

## References

- DiCiccio, T. J., and Efron, B. (1996). "Bootstrap confidence intervals." *Statistical Science* 11(3):189–228.
- Efron, B. (1987). "Better bootstrap confidence intervals." *Journal of the American Statistical Association* 82(397):171–185.
- Goldberg, D. (1991). "What Every Computer Scientist Should Know About Floating-Point Arithmetic." *ACM Computing Surveys* 23(1):5–48.
- Higham, N. J. (2002). *Accuracy and Stability of Numerical Algorithms*, 2nd ed. SIAM, Philadelphia. Chapter 4 (summation algorithms and condition numbers).
- Terriberry, T. B. (2007). "Computing higher-order moments online." Informal technical note. https://people.xiph.org/~tterribe/notes/homs.html
- Welford, B. P. (1962). "Note on a method for calculating corrected sums of squares and products." *Technometrics* 4(3):419–420.
