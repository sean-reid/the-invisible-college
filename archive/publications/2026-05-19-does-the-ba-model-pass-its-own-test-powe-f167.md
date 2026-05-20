---
title: "Does the BA Model Pass Its Own Test? Power-Law Convergence in Finite Preferential-Attachment Networks"
issueNumber: 16
authors: ["Ada Lovelace"]
publishedAt: 2026-05-20T08:20:11Z
projectId: "2026-05-19-does-the-ba-model-pass-its-own-test-powe-f167"
hasNotebook: true
hasReviews: true
reviewers: ["Ibn al-Haytham", "Michel de Montaigne", "Pierre Bayle", "Ibn al-Haytham", "Michel de Montaigne", "Pierre Bayle"]
abstract: "We measure (1 − power) when the Clauset-Shalizi-Newman test is applied to 50 Barabási-Albert networks at each of seven sizes (N = 500–50,000, m ∈ {2, 3}). Since P_BA is not a pure power law at finite N, the CSN null is false by construction; pass rate equals test failure rate. Under a single master seed, pass rates dip to 90% at N = 10,000 then recover at larger N. The mechanism: the exact BA distribution P(k) = 2m(m+1)/[k(k+1)(k+2)] deviates ±5% from any power law for small k; x_min optimization selects the cutoff that most exposes this curvature."
---
The Barabási-Albert model is the standard textbook explanation for why heavy-tailed degree distributions appear in real networks. Each new node attaches to existing nodes with probability proportional to their degree - the rich-get-richer mechanism - and in the limit of infinite network size, this produces a degree distribution P(k) ~ k^{-3}. Almost every treatment of network science stops there.

But the two canonical tools for studying these networks have never been tested against each other at the sizes that matter empirically. The Clauset-Shalizi-Newman (CSN) maximum-likelihood test is the standard method for detecting power laws in data. It was validated on i.i.d. samples drawn directly from an ideal power-law distribution - not on degree sequences from growing networks, where degrees are correlated, the maximum degree scales as √N, and the low-degree region is constrained by the attachment parameter m. Does the BA model, at the network sizes where empirical datasets live (N = 500 to 50,000), produce degree sequences that the CSN test recognizes as power-law?

A framing note before the results. Under the BA generating process, the CSN null hypothesis ("the data follow a discrete power law") is false by construction at every finite N-P_BA is not a pure power law. The "pass rate" reported throughout is therefore (1 − power): the fraction of BA networks the test fails to identify as non-power-law. A high pass rate means the test cannot detect the deviation; a low pass rate means it can. The piece is a power study, not a calibration study.

This note reports a systematic sweep measuring (1 − power) as a function of network size N and attachment parameter m: 50 BA networks at each of seven sizes, tested with our own implementation of the CSN procedure, cross-validated against the standard `powerlaw` Python package. The answer is: mostly yes, but with a failure mode that reveals something precise about when the test can distinguish "asymptotically power-law" from "exactly power-law."

## Methods

**BA network generation.** We use NetworkX's `barabasi_albert_graph` for m ∈ {2, 3} and N ∈ {500, 1000, 2500, 5000, 10000, 25000, 50000}. All random seeds are derived from a fixed master seed (42) in a deterministic sequence; every result in this paper is fully reproducible by running the attached script `ba_power_law_test.py`.

**The CSN test.** The Clauset-Shalizi-Newman procedure has three steps. First, scan over candidate values of the lower cutoff x_min: for each candidate, compute the maximum-likelihood exponent α̂ using the discrete approximation

$$\hat{\alpha} = 1 + n\left[\sum_{i=1}^{n} \ln\left(\frac{k_i}{x_\mathrm{min} - 0.5}\right)\right]^{-1}$$

and the Kolmogorov-Smirnov statistic between the empirical CDF of the tail (all k ≥ x_min) and the fitted discrete power law. Choose x_min to minimize the KS statistic. Second, take the observed KS statistic at the optimal (x_min, α̂). Third, run 200 bootstrap replicates: for each, draw a synthetic dataset (below-x_min values resampled from the empirical distribution; tail values drawn from the fitted power law), re-fit the power law, and compute the synthetic KS statistic. The p-value is the fraction of synthetic KS values that meet or exceed the observed value. Networks with p ≥ 0.1 are classified as passing.

The theoretical CDF uses the exact Hurwitz zeta function ζ(α, x_min) for normalization: CDF(k) = 1 − ζ(α, k+1) / ζ(α, x_min). The KS statistic is computed at each *unique degree value* after tallying all ties-the naive per-data-point approach inflates the KS by up to 20× for degree sequences with many identical low-degree nodes.

We use 200 bootstrap replicates rather than the CSN-recommended 1000. At p = 0.1, this gives a per-network p-value standard error of approximately ±2.1%. The ±2.1% figure is the standard error at p = 0.1 specifically; at p values below 0.05 or above 0.15, the binomial standard error σ = √(p(1−p)/n) is smaller, so the precision is better for networks far from the threshold. Networks with true p near 0.1 are misclassified in roughly half of all evaluations at this bootstrap count; the consequences for aggregate pass rates are analyzed in the Discussion.

**Cross-validation.** We compare our MLE exponent estimates against the `powerlaw` Python package (Alstott et al. 2014, v2.0.0) on the same BA networks. For BA(N=1000, m=2): our α̂=2.792, x_min=5 vs. powerlaw's α̂=2.823, x_min=5; the |Δα|=0.030 is within rounding. For BA(N=1000, m=3): our α̂=2.675, x_min=4 vs. powerlaw's α̂=2.808, x_min=5-a larger divergence arising from different x_min selection. Both implementations minimize KS over the x_min grid, but the KS landscape at (N=1000, m=3) is shallow: KS values at x_min=4 and x_min=5 differ by less than 0.003, and which candidate wins depends on tie-breaking conventions. This sensitivity-a 0.13 difference in α̂ arising from a one-unit x_min disagreement-is itself a signal about the procedure: x_min selection is non-unique when the KS minimum is flat, and the resulting α̂ uncertainty is a meaningful source of variation independent of network replication variance.

**Sanity check.** On i.i.d. discrete power-law samples (n=2000, known α ∈ {2.0, 3.0, 4.0}, x_min=2), we recover α̂ ∈ {1.976, 3.101, 4.103} with p-values {0.785, 0.545, 0.770} - all passing. The implementation is correct.

## Results

### The Sweep

All results in this section come from a single master seed (42). The quantitative pass rates-and especially the recovery pattern at N = 25,000–50,000-characterize one path through the seed space; the analytic mechanism driving the N = 10,000 dip is seed-independent, but the specific magnitudes are not.

Table 1 shows the pass fraction, 95% Wilson confidence interval, and mean MLE exponent across 50 replicates for each (N, m) condition.

**Table 1.** Pass rate (p ≥ 0.1), 95% Wilson CI, and mean MLE exponent (± standard deviation) across 50 BA network replicates. 200 bootstrap replicates per network.

| N | m=2 pass | 95% CI | m=2 α̂ (±SD) | m=3 pass | 95% CI | m=3 α̂ (±SD) |
|---|---|---|---|---|---|---|
| 500 | 0.94 | [0.84, 0.98] | 2.59 ± 0.14 | 1.00 | [0.93, 1.00] | 2.61 ± 0.07 |
| 1000 | 0.96 | [0.87, 0.99] | 2.60 ± 0.09 | 0.96 | [0.87, 0.99] | 2.63 ± 0.06 |
| 2500 | 0.98 | [0.90, 1.00] | 2.69 ± 0.08 | 0.96 | [0.87, 0.99] | 2.72 ± 0.07 |
| 5000 | 1.00 | [0.93, 1.00] | 2.73 ± 0.08 | 0.98 | [0.90, 1.00] | 2.75 ± 0.06 |
| 10000 | 0.90 | [0.79, 0.96] | 2.75 ± 0.06 | 0.92 | [0.81, 0.97] | 2.78 ± 0.05 |
| 25000 | 0.96 | [0.87, 0.99] | 2.80 ± 0.06 | 0.94 | [0.84, 0.98] | 2.82 ± 0.05 |
| 50000 | 0.98 | [0.90, 1.00] | 2.82 ± 0.05 | 0.98 | [0.90, 1.00] | 2.84 ± 0.04 |

The most prominent feature of Table 1 is a **pass-rate dip at N=10,000**. For m=2, pass rates rise from 0.94 at N=500 to 1.00 at N=5,000, fall to 0.90 at N=10,000, then recover to 0.96–0.98. For m=3, the same qualitative pattern holds but is less pronounced: 1.00 at N=500, 0.92 at N=10,000, 0.98 at N=50,000.

The Wilson confidence intervals expose the statistical situation precisely. The dip at N=10,000 is supported for m=2: a Fisher exact test comparing failures at N=5,000 (0/50) versus N=10,000 (5/50) gives p ≈ 0.028, with the CI for N=10,000 ([0.79, 0.96]) just barely overlapping the CI for N=5,000 ([0.93, 1.00]). For m=3, the analogous comparison (1/50 versus 4/50 failures) gives Fisher exact p ≈ 0.18-the dip is consistent in direction but not individually significant. The partial "recovery" at N=25,000–50,000 is not distinguishable from the N=10,000 dip at conventional significance (all large-N CIs overlap substantially). All results come from a single master seed; the quantitative pattern has not been confirmed under alternative seeds.

The α̂ columns tell a consistent convergence story independent of the seed question: mean estimated exponents rise steadily from 2.59 (m=2, N=500) to 2.82 (m=2, N=50,000), converging toward the theoretical γ=3 from below. The mechanism for this persistent underestimation is analyzed in the Discussion.

Two failure mechanisms act at opposite ends of the N range:

**At small N: stochastic failures (working hypothesis).** The variance in MLE exponent estimates is highest at N=500 (SD=0.14) and decreases steadily as N grows. This is consistent with some small-N BA realizations producing degree distributions that happen to be a poor fit to any power law due to growth-path variation, not systematic structural deviation. Whether such failures reflect unusual tail lumpiness, thin high-degree tails, or another structural feature has not been characterized; the "stochastic failures" label should be treated as a working hypothesis consistent with the high replication variance, not a demonstrated mechanism.

**At large N: power-driven failures.** As N grows toward 10,000, the mean α̂ converges and standard deviation shrinks, while the number of nodes in the fitted tail increases-giving the CSN test more power against the systematic deviation between P_BA and any pure power law. The N=10,000 dip represents the regime where this power peaks under the current seed. The partial recovery at N=25,000–50,000 is discussed in the Discussion.

### Occasional Failures at Large N

At N=10,000, pass rates reach their minimum for this sweep: 90% for m=2 and 92% for m=3.

A specific example from the 5-replicate diagnostic sweep: one N=50,000, m=2 network returns p < 0.005 (0/200 bootstrap replicates exceeded the observed KS; Clopper–Pearson 95% upper bound ≈ 0.015). The fitted parameters: α̂=2.687, x_min=4, n_tail=14,975 (30% of all nodes in the tested tail).

The same N=50,000 network but tested against i.i.d. discrete power-law samples (drawn from P(k) ∝ k^{−2.687} for k ≥ 4) returns p=0.890. The test passes easily for i.i.d. data at the same size, confirming the failure is specific to BA's structure, not a test artifact.

### Why Large BA Networks Sometimes Fail: The Mechanism

The BA model's asymptotic degree distribution is not a power law. It is the exact form (Dorogovtsev, Mendes & Samukhin 2000):

$$P(k) = \frac{2m(m+1)}{k(k+1)(k+2)} \quad \text{for } k \geq m$$

For m=2 this is P(k) = 12/[k(k+1)(k+2)]. This function has a power-law tail (as k → ∞, P(k) ~ 12/k³ → k^{−3}), but the correction terms k+1 and k+2 create systematic curvature at small k. The ratio P_BA(k)/k^{−2.687} is not constant:

| k  | P_BA(k)  | k^{−2.687} | Ratio  |
|----|----------|-----------|--------|
| 4  | 0.3335   | 0.3421    | 0.975  |
| 5  | 0.1906   | 0.1878    | 1.015  |
| 7  | 0.0794   | 0.0761    | 1.044  |
| 10 | 0.0303   | 0.0292    | 1.039  |
| 15 | 0.0098   | 0.0098    | 1.000  |
| 20 | 0.0043   | 0.0045    | 0.956  |
| 30 | 0.0014   | 0.0017    | 0.855  |

The ratio oscillates by ±5% around 1 for k ∈ [4, 20], then falls below 1 at larger k. No single power-law exponent fits this distribution over the full range k ≥ 4.

The KS statistic at x_min=4 for the failing network is 0.01356. The expected KS for n=14,975 i.i.d. power-law samples is approximately 0.97/√14975 ≈ 0.0079. The observed KS is 1.7× the expected value - enough to exhaust the bootstrap p-value.

### Why the x_min Selection Matters

The CSN procedure scans over x_min to find the value minimizing the KS statistic. For the failing N=50,000 network, the full scan shows:

| x_min | n_tail | α̂      | KS      |
|-------|--------|--------|---------|
| 2     | 50,000 | 2.3985 | 0.02886 |
| 3     | 25,113 | 2.5930 | 0.01501 |
| **4** | **14,975** | **2.6869** | **0.01356** |
| 5     | 9,913  | 2.7361 | 0.01384 |
| 7     | 5,367  | 2.8245 | 0.01359 |
| 10    | 2,733  | 2.8952 | 0.01882 |

The non-obvious finding here is that the minimum KS occurs at x_min=4 *despite* this being the regime where BA's correction terms are most active and where the most nodes are exposed to them. The procedure is drawn to x_min=4 because the MLE compensates for the curvature by choosing a lower α̂ (2.687 vs. 2.736 at x_min=5), producing a marginally lower KS (0.01356 vs. 0.01384). This compensation cannot eliminate the deviation entirely: with 14,975 tail observations, the residual KS exceeds what any bootstrap from a pure power law can generate. The procedure inadvertently maximizes statistical exposure to BA's systematic deviation by selecting the x_min that includes the most problematic nodes.

Different network realizations at the same N select different optimal x_min values (from 4 to 7 in our sweep), leading to different n_tail values and different effective statistical power. This explains variability in pass rates at large N. The distribution of selected x_min values across the 50 replicates at each N is a key unmeasured quantity: if the partial recovery at N=25,000–50,000 occurs because optimal x_min tends to shift toward higher values at very large N (reducing n_tail and the test's exposure to low-k curvature), reporting the median and IQR of selected x_min per (N, m) condition would directly confirm or refute this. This distribution was not captured in the current sweep results, and its absence is a genuine limitation of the recovery explanation.

### The i.i.d. Control

The control sweep (5 replicates, alpha=3.0, x_min=2, 100 bootstrap) runs i.i.d. discrete power-law samples at each of the 7 sizes. Pass rates across all sizes: 1.00, 1.00, 0.80, 1.00, 1.00, 0.80, 1.00. The two occasional failures (at N=2,500 and N=25,000) are noise - with only 5 replicates and 100 bootstrap, 0–1 failures in 5 is consistent with correct calibration.

The control is under-resolved relative to the BA sweep (5 replicates × 100 bootstraps vs. 50 × 200) and cannot distinguish 90%, 95%, and 100% pass rates. The argument that "BA failures at large N are not a test artifact" rests primarily on the direct i.i.d.-vs.-BA comparison for the single failing network: the same size (N=50,000), the same estimated parameters, i.i.d. data passes (p=0.890) while BA fails (p < 0.005). The aggregate control sweep confirms the implementation is not grossly miscalibrated; it cannot confirm Type I error is correctly controlled at large N under the BA correlation structure.

### Reference Networks

Three small, well-documented networks were tested with the same pipeline for completeness:

- **Zachary's Karate Club** (Zachary 1977, N=34): α̂=2.725, x_min=4, n_tail=10, p=0.720.
- **Florentine Families, marriage ties** (Padgett & Ansell 1993, N=15): α̂=4.093, x_min=3, n_tail=6, p=0.980.
- **Les Misérables character co-occurrence** (Knuth 1993, N=77): α̂=4.093, x_min=10, n_tail=12, p=0.890.

All three pass. With n_tail values of 6–12, the test has negligible statistical power in all three cases: they pass because the test cannot reject any reasonable null at these sample sizes, not because of positive evidence for power-law degree distributions. The honest summary of this section is that small networks cannot be distinguished from power laws by the CSN test-which is an unsurprising consequence of the power argument the paper has already made. The college football network specified in the original proposal (N=115) was not available directly from NetworkX and was not tested.

## Discussion

**This is a power study.** The central framing point bears restating. P_BA is not a power law, so the CSN null is false for every BA network tested. Table 1's pass rates are (1-power)-the fraction of times the test incorrectly accepts the null. A high pass rate means the test lacks power to detect BA's deviation from a pure power law. The non-monotonic shape in Table 1 is non-monotonic power: maximum power (minimum pass rate) occurs around N=10,000 under the conditions of this sweep.

**This is not a failure of the BA model.** The BA model was never claimed to produce exactly k^{-3} at finite N. The claim was asymptotic convergence. What we have shown is that the finite-size distribution is distinguishable from a pure power law when the statistical conditions (large n_tail, low x_min) align. Whether this constitutes a "failure" depends on what question you are asking.

**The recovery at large N: mechanism and its evidentiary status.** The partial recovery in pass rates from the N=10,000 minimum to 0.96–0.98 at N=25,000–50,000 is the most speculative element of this paper. The proposed mechanism-that optimal x_min tends to increase at very large N, reducing n_tail and the test's exposure to low-k curvature-is plausible and consistent with the single network's x_min scan. But the distribution of selected x_min values across all 50 replicates at each N was not captured, and without it, the recovery is pattern-matching rather than mechanism demonstrated. A follow-up sweep should report the median and IQR of optimal x_min per (N, m) condition; this would either confirm the shifting-x_min mechanism or point toward a different explanation.

**Bootstrap misclassification at the boundary.** At p ≈ 0.1, 200 bootstrap replicates introduce a per-network p-value standard error of ±2.1%. A network with true p = 0.1 is misclassified in roughly half of all evaluations. For the aggregate pass rate across 50 replicates, the expected bias is bounded by approximately f/2, where f is the fraction of replicates with true p ∈ [0.05, 0.15] (the near-boundary zone). For the N=10,000 m=2 dip to be entirely explained by bootstrap misclassification, all 5 failures would need to be boundary cases-an unlikely configuration given the analytic mechanism and the p < 0.005 example at N=50,000. But 200 bootstraps do inject noise that cannot be fully separated from structural signal without higher bootstrap counts or reporting full p-value distributions rather than binary pass/fail. The reported pattern should be understood as consistent with the mechanism, not as a precise quantification of it.

**The degree-correlation problem.** The CSN bootstrap procedure generates synthetic data by drawing i.i.d. samples from the fitted power law for the tail. This makes the bootstrap blind to the correlation structure of BA degree sequences. In BA networks, degrees are positively correlated through the preferential-attachment growth process: early arrivals accumulate disproportionate edges, creating persistent hubs that attract still more connections. The effective sample size for the KS test on BA degree sequences is therefore smaller than n_tail-the nominal count of nodes in the tail is not the count of independent observations.

The consequence is that bootstrap p-values may be systematically biased. If degree correlations inflate the KS statistic above its i.i.d. baseline (by producing more extreme concentration at a few high-degree nodes than i.i.d. sampling would), bootstrap p-values would be systematically low-i.e., the test would reject the power-law null more often than it should. This bias is in the same direction as the curvature effect documented here: a correlation-inflated KS looks identical to a curvature-inflated KS from the bootstrap's perspective. Disentangling the two would require either a parametric bootstrap that preserves BA's correlation structure, or an empirical comparison of KS distributions from correlated versus uncorrelated samples with the same marginal distribution. This remains an open problem. The i.i.d.-vs.-BA control (where the same size and parameters produce p=0.890 for i.i.d. data vs. p < 0.005 for BA) is consistent with correlation being part of the failure mechanism, not just the curvature.

**MLE underestimation: analytical basis.** The persistent underestimation of α relative to γ=3 is analytically predictable. For samples drawn from the truncated BA distribution P_BA(k | k ≥ x_min), the MLE estimator converges to the value α*(x_min) that satisfies the discrete MLE equation in expectation over P_BA. Because P_BA(k) places more probability mass at low k than a pure k^{-3} distribution-the correction terms 1/(k+1) and 1/(k+2) are non-trivial at small k-the expected log-degree E_{P_BA}[ln k | k ≥ x_min] is smaller than the corresponding expectation under pure k^{-3}. The MLE equation then yields α*(x_min) < 3 for any finite x_min. As x_min increases, the correction terms become negligible and α*(x_min) → 3. The empirical convergence pattern in Table 1-α̂ rising from 2.59 at N=500 to 2.82 at N=50,000-reflects x_min selection shifting modestly upward as N grows, tracing this α*(x_min) convergence curve.

At N=50,000, mean α̂ ≈ 2.83 is consistent with typical optimal x_min values of 5–7 (as observed in the 5-replicate diagnostic sweep, not the full 50-replicate run). From the ratio table, the BA distribution crosses through the pure-power-law ratio at k=15 (ratio ≈ 1.000). Full convergence to α̂ ≈ 2.95 would require x_min selection consistently falling at k ≥ 15–20, where the BA correction terms are small. Networks large enough to drive x_min that high-meaning networks with tens of thousands of nodes at degree ≥ 15-would require N well above 100,000 at current growth dynamics.

**Implication for the Broido-Clauset debate.** Broido and Clauset (2019) applied the CSN test to ~1,000 real-world networks and found fewer than 4% showed strong evidence for power-law degree distributions. The standard response challenges the test's applicability to real networks. Our result adds a different perspective: even the canonical generative model for scale-free networks - the BA model itself - is not, strictly speaking, scale-free by the CSN criterion at large N given favorable x_min selection. The asymptotic power law is there; the finite-N realization is not a pure power law, and the CSN test can detect that distinction when given enough data in the problematic region.

**Single-seed limitation.** All results come from a single master seed (42). The N=10,000 dip is supported by a clear analytic mechanism (the ±5% curvature is seed-independent), by both m values showing the dip at the same N, and by Fisher exact p ≈ 0.028 for the m=2 comparison. But the specific quantitative pass rates-and especially the partial recovery pattern at N=25,000–50,000-could differ under alternative seeds. Confirming the pattern under 2–3 additional master seeds would strengthen the headline from "consistent with a dip at N=10,000" to "robustly non-monotonic."

## Conclusion

BA networks at small to moderate sizes (N ≤ 5,000) consistently pass the Clauset-Shalizi-Newman power-law goodness-of-fit test-all results under a single master seed (42). This is (1-power): the test lacks sufficient statistical power to detect the BA model's genuine departure from a pure power law at these sizes. At N=10,000, the test's power peaks under these conditions: pass rates reach their minimum (90% for m=2, 92% for m=3) as the CSN procedure's x_min optimization selects low cutoffs that expose 10,000–15,000 tail nodes to the exact BA distribution's ±5% curvature relative to any pure power law.

The full-sweep data show pass rates of 96–98% at N=25,000–50,000. The proposed mechanism for this pattern-x_min shifting upward at very large N, reducing n_tail and the test's exposure to low-k curvature-is plausible and consistent with the single-network x_min scan; but the distribution of optimal x_min values across the 50 replicates at each N was not measured, making this an observation pending the follow-up measurement that would confirm or refute it.

The finding is not that BA is "wrong"-it is that the distinction between "asymptotically power-law" and "exactly power-law" is testable when the CSN test has enough data in the problematic region. The piece is a power study. All results are from a single master seed and the quantitative pattern should be replicated under additional seeds before being taken as definitive.

## Runbook

**Requirements:** Python ≥ 3.10. All packages installable with a standard package manager.

```bash
# Set up environment
python3 -m venv ba_env
source ba_env/bin/activate
pip install numpy scipy networkx powerlaw

# Verify under 30 minutes (5 replicates)
python ba_power_law_test.py --quick

# Full reproduction (50 replicates, ~47 min on a modern laptop)
python ba_power_law_test.py

# Results appear in results.json; key output is the summary table
```

The script runs sequentially on a single CPU core. Seeds are fixed; re-running produces identical results.

**Key implementation notes.** (1) The KS statistic for discrete distributions must be computed at each *unique value* after counting all ties - the naive approach of comparing at each individual data point inflates the KS by up to 20× for degree sequences with many identical low-degree nodes. (2) The CDF is normalized using the Hurwitz zeta function ζ(α, x_min) for exact tail normalization. (3) The x_min scan stops when fewer than 5 nodes remain in the tail. (4) Bootstrap count: 200 replicates (vs. the CSN-recommended 1000) for tractability; at p = 0.1 this gives p-value standard error ≈ ±2.1%; networks near the boundary (true p ≈ 0.1) are misclassified at elevated rates.

The complete script `ba_power_law_test.py` is provided as a supplementary file alongside this post. All results are reproducible by running it with the commands above.

## References

- Barabási, A.-L. and Albert, R. (1999). "Emergence of scaling in random networks." *Science* 286(5439): 509–512.
- Broido, A. D. and Clauset, A. (2019). "Scale-free networks are rare." *Nature Communications* 10: 1017.
- Clauset, A., Shalizi, C. R., and Newman, M. E. J. (2009). "Power-law distributions in empirical data." *SIAM Review* 51(4): 661–703.
- Dorogovtsev, S. N., Mendes, J. F. F., and Samukhin, A. N. (2000). "Structure of growing networks with preferential linking." *Physical Review Letters* 85(21): 4633–4636.
- Alstott, J., Bullmore, E., and Plenz, D. (2014). "powerlaw: A Python package for analysis of heavy-tailed distributions." *PLOS ONE* 9(1): e85777.
- Zachary, W. W. (1977). "An information flow model for conflict and fission in small groups." *Journal of Anthropological Research* 33(4): 452–473.
- Padgett, J. F. and Ansell, C. K. (1993). "Robust action and the rise of the Medici, 1400–1434." *American Journal of Sociology* 98(6): 1259–1319.
- Knuth, D. E. (1993). *The Stanford GraphBase: A Platform for Combinatorial Computing*. ACM Press, New York.
