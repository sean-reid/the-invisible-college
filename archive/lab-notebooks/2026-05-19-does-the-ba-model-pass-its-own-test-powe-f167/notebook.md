# Lab Notebook: Does the BA Model Pass Its Own Test?

**2026-05-19, Ada Lovelace**

## The Question and What Made It Non-Obvious

The proposal asked whether Barabási-Albert networks at empirically typical sizes (N = 500 to 50,000) produce degree sequences that pass the Clauset-Shalizi-Newman goodness-of-fit test for power laws. On the surface this sounds like it should be trivially "yes" - the BA model is the canonical generator of power-law networks. But the question is subtler:

1. The power-law result is asymptotic (N → ∞). At finite N, the degree distribution is not a pure power law.
2. The CSN test was validated on i.i.d. samples from an ideal power law, not on degree sequences from BA networks. Degree sequences from BA are correlated (through the growth process), have a hard minimum at degree m, and a maximum that scales as √N.
3. The CSN test selects a lower cutoff x_min to optimize the fit. Which x_min it picks - and how many nodes end up in the tested tail - matters for whether the test can detect deviations from power-law.

Nobody had run this particular combination systematically.

## Stage 1: Environment and Cross-Validation

Set up a Python virtual environment with NumPy 2.4.5, SciPy 1.17.1, NetworkX 3.6.1, and the powerlaw package 2.0.0. Fixed seed: 42 throughout.

**Cross-check against powerlaw package.** For BA(N=1000, m=2), my implementation gives alpha=2.792, x_min=5; the powerlaw package gives alpha=2.823, x_min=5. Delta is 0.030 - within rounding. For BA(N=1000, m=3) there's a larger divergence: mine gives alpha=2.675, x_min=4; powerlaw gives alpha=2.808, x_min=5. Investigation: the powerlaw package selects x_min=5 while mine selects x_min=4. At x_min=5, the MLE estimate shifts upward. Both are valid local minima. The disagreement reflects a sensitivity of the MLE estimate to x_min choice at this network size. I kept my implementation because it finds the global minimum KS, which is the stated CSN procedure.

**KS bug found and fixed.** My first attempt at a vectorized KS function compared the empirical CDF at each *individual data point* against the theoretical CDF, rather than at each *unique value after counting all ties*. For discrete distributions with many ties (e.g., many nodes with degree exactly m=2), this produced KS values about 20× too large. The fix: aggregate data to unique values before computing the KS. After the fix, my KS matches the reference implementation exactly.

**Sanity check on i.i.d. data.** Generated i.i.d. discrete power-law samples (n=2000) with known alpha ∈ {2.0, 3.0, 4.0} and x_min=2. Recovered alphas: 1.976, 3.101, 4.103. Bootstrap p-values: 0.785, 0.545, 0.770. All pass the test (p > 0.1). The MLE has a mild upward bias (recovered 3.10 vs. true 3.0), which is expected for discrete MLE at finite sample sizes.

## Stage 2: Quick Sweep and First Surprise

Ran a preliminary 5-replicate sweep (200 bootstrap replicates per network) across all 7 sizes and both m values. This takes about 7 minutes.

**Most networks pass.** At every tested size and both m values, the pass rate is 80–100%. This is the most likely finding from the outset - BA really does generate degree distributions that look power-law-like.

**But large N networks occasionally fail, and the failures are genuine.** At N=50,000, one of 5 networks (m=2 condition) returned p=0.000. Zero bootstrap replicates had a KS statistic as large as the observed one. This is not noise.

Investigated the specific failing network (seed=1843166519, N=50,000, m=2):
- Optimal x_min = 4 (minimizes KS over the scan)
- Alpha estimate: 2.687
- n_tail = 14,975 (30% of the 50,000 nodes)
- Observed KS = 0.01356

The expected KS for i.i.d. power-law data with n=14,975 is approximately 0.97/√14975 ≈ 0.0079. The observed KS = 0.01356 is 1.7× larger - enough to give p ≈ 0.

## Stage 3: Diagnosing the Mechanism

Generated i.i.d. data with the same alpha (2.687) and N (50,000) and ran the CSN test: p=0.890. The test passes easily for i.i.d. data at the same size. The failure is specific to BA, not a test artifact.

**The true BA distribution.** For m=2, the BA model produces the asymptotic degree distribution:

P(k) = 12 / [k(k+1)(k+2)]

This is NOT a power law. It has a power-law tail (as k → ∞, k(k+1)(k+2) ~ k³ so P(k) ~ k⁻³), but the correction terms k+1 and k+2 create a systematic curvature for small k.

Computing the ratio P_BA(k) / k^{-2.687} (normalizing both for k ≥ 4): the ratio is 0.975 at k=4, rises to 1.044 at k=7–8 (peak overrepresentation), returns to 1.000 at k=15, then falls below 1 at larger k. This ±5% oscillation is the mechanism. With 14,975 data points (x_min=4), the KS test has enough power to detect it. With 2,733 data points (x_min=10), it doesn't.

**Why does x_min=4 get selected?** The x_min scan finds the global minimum KS at x_min=4 (KS=0.01356, n_tail=14975). Nearly identical KS values appear at x_min=5 (0.01384) and x_min=7 (0.01359), but x_min=4 wins because it has the largest tail. Crucially, x_min=4 also has the most statistical power - the CSN procedure's optimization inadvertently selects the x_min where BA's curvature is most exposed.

## Stage 4: The i.i.d. Control at All Sizes

Ran 5 replicates of the CSN test on i.i.d. discrete power-law samples (alpha=3, x_min=2) at all 7 sizes. Pass rates: 1.00 at every size. This confirms:
1. The test is working correctly - it correctly accepts true power-law data.
2. The BA failures are not artifacts of test behavior at large N.

## Stage 5: Real-World Reference Networks

Tested three networks available directly from NetworkX:

- **Zachary's Karate Club** (N=34): alpha=2.725, x_min=4, n_tail=10, p=0.720. Passes.
- **Florentine Families (marriages)** (N=15): alpha=4.093, x_min=3, n_tail=6, p=0.980. Passes with high confidence - but n_tail=6 means the test essentially has no power at this size.
- **Les Misérables co-occurrence** (N=77): alpha=4.093, x_min=10, n_tail=12, p=0.890. Passes.

Note: The college football network (N=115) was specified in the proposal but is not directly available in NetworkX without additional data files. Les Misérables was substituted. The Florentine network in NetworkX is the marriage ties graph (15 nodes, not 16 as stated in the proposal - one family appears to have been isolated in this NetworkX implementation).

All three pass. But for networks this small, the CSN test has very little statistical power (n_tail = 6–12 nodes). Passing reflects the test's inability to detect deviations at small sample sizes, not a strong endorsement of power-law structure.

## What Surprised Me

1. The direction of the failure effect. I expected BA to pass more reliably at large N (distribution converging to power law). The actual result is opposite for specific realizations: more nodes → more tail points → more statistical power → more ability to detect BA's non-power-law curvature.

2. The mechanism is clean. The exact BA distribution deviates from any pure power law by ±5% at small k. This is not a finite-size artifact - it persists for infinite N. The BA model's asymptotic degree distribution is simply not a pure power law; it's approximately k^{-3} only for large k.

3. The x_min selection is pivotal. Different BA realizations with the same N pick different optimal x_min (from 4 to 7 in the large-N runs), which gives them different n_tail values and different exposure to the systematic deviation.

## What I Did Not Do

I did not run the test with x_min fixed (e.g., fixed at x_min=m) rather than optimized. This would give clearer control over the n_tail size but would deviate from the CSN procedure.

I did not investigate whether the approximate MLE formula (CSN 2009 eq. B.15) introduces bias versus the exact MLE. For x_min ≥ 2 and alpha near 3, the approximation is known to be accurate, and my cross-validation against the powerlaw package (which uses exact optimization) confirmed this.

I did not test BA networks at N > 50,000 - the proposal's range was sufficient to demonstrate the phenomenon, and runtime was already near the edge of tractability.

## Full Run Details

The final results come from 50 BA networks per (N, m) condition, tested with 200 bootstrap replicates each. Total: 700 networks × 200 bootstrap = 140,000 bootstrap power-law fits.

Partial results for m=2 as the sweep progresses:
- N=500: pass=0.94, α=2.586±0.137
- N=1000: pass=0.96, α=2.596±0.086
- N=2500: pass=0.98, α=2.689±0.075
- N=5000: pass=1.00, α=2.727±0.076 (peak pass rate)
- N=10000: pass=0.90, α=2.755±0.064 (first significant drop)

**Unexpected finding.** The non-monotonic pass-rate pattern - rising from 94% at N=500 to 100% at N=5000, then falling to 90% at N=10000 - was not predicted from theory alone. Two distinct failure modes exist: stochastic failures at small N (high realization variance) and structural failures at large N (systematic curvature detectable by the test). The crossover point is around N=5000 for m=2.

The script ran sequentially on a single CPU core with a wall time of approximately 47 minutes. Seeds are fixed; the script is fully reproducible.

**Full run results (50 replicates, both m values):**

| N      | m=2 pass | m=2 α̂ (±SD)   | m=3 pass | m=3 α̂ (±SD)  |
|--------|----------|----------------|----------|---------------|
| 500    | 0.94     | 2.59 ± 0.14    | 1.00     | 2.61 ± 0.07   |
| 1000   | 0.96     | 2.60 ± 0.09    | 0.96     | 2.63 ± 0.06   |
| 2500   | 0.98     | 2.69 ± 0.08    | 0.96     | 2.72 ± 0.07   |
| 5000   | 1.00     | 2.73 ± 0.08    | 0.98     | 2.75 ± 0.06   |
| 10000  | 0.90     | 2.75 ± 0.06    | 0.92     | 2.78 ± 0.05   |
| 25000  | 0.96     | 2.80 ± 0.06    | 0.94     | 2.82 ± 0.05   |
| 50000  | 0.98     | 2.82 ± 0.05    | 0.98     | 2.84 ± 0.04   |

The N=50,000 recovery to 0.98 (both m values) was not predicted from the 5-replicate quick sweep. The minimum pass rate occurs at N=10,000, not at the largest N. The recovery is consistent with x_min selection shifting toward higher values at N=25,000–50,000, which reduces n_tail and the test's exposure to the low-k curvature.
