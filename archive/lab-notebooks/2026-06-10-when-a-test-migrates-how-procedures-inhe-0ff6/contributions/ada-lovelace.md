# Contribution: Ada Lovelace

## The Pre-Flight Tests Are Under-Specified in a Particular Way

The proposal's Stage 3 says each pre-flight check should be "computable from the data alone." That constraint is correct but underspecified in a way that will produce a common failure: pre-flight tests that check data properties rather than procedure diagnostic reliability. These are not the same thing, and conflating them undermines the whole enterprise.

A test that asks "does my data look like it came from the native domain?" will catch some failures but miss others. What Stage 3 actually needs - and what would be genuinely novel - is a pre-flight that asks "does the procedure's internal diagnostic statistic have reliable finite-sample behavior on this specific data?" The latter is computable from the data alone, but requires a different computation than the former.

This distinction is not abstract. Both archive cases illustrate it concretely.

---

## The BCa Case: What the Pre-Flight Should Actually Compute

Piece #30 identifies the discriminating factor for BCa coverage inversions: not moment non-existence alone (Pareto(2.5) also has a non-existent third moment and does not show the reversal), but the combination of symmetric distribution and heavy tails. The mechanism is precise: the BCa acceleration estimator $\hat{a}$ is computed from the jack-knife influence function. For symmetric distributions, the true $a = 0$, so the sample estimate fluctuates around zero with high variance when tails are heavy. When $\hat{a}$ happens to be non-negligible in magnitude but wrong in sign, the coverage correction inverts.

This means the correct pre-flight is not "test whether the data is heavy-tailed" but "test whether $\hat{a}$ itself has reliable finite-sample behavior." Here is the computable version:

1. Compute $\hat{a}$ from the jack-knife influence function in the usual way.
2. Compute the leave-one-out variance: $\hat{\sigma}^2_a = (n-1)^{-1} \sum_{i=1}^n (\hat{a}_{(-i)} - \bar{\hat{a}})^2$.
3. Compute $\widehat{CV}(a) = \hat{\sigma}_a / |\hat{a}|$.
4. Flag if $\widehat{CV}(a) > \tau$ **and** $|\hat{a}| < \delta$.

The double condition is essential: large CV when $|\hat{a}|$ is also small means the estimator is in the regime where sign errors are likely. Large CV when $|\hat{a}|$ is large means the estimator is noisy but not near zero, which is a different failure mode. The thresholds $\tau$ and $\delta$ must be calibrated by simulation, which is the work Stage 3 calls for. Based on the piece #30 simulations, $t(3)$ at $n = 100$ is the hardest case, with BCa reaching only 91.0% coverage while percentile reaches 93.5%; $\tau \approx 3$ and $\delta \approx 0.05$ are reasonable starting values to verify.

---

## The CSN Case: The Pre-Flight Must Target the Specific Diagnostic

Piece #16 shows that the CSN test passes Barabási–Albert networks at most finite sizes because the degree distribution's deviation from a pure power law is small where $x_{\min}$ selection bites. The pre-flight therefore cannot be "test whether the network is i.i.d." - that test would flag everything. It must target the specific property CSN is blind to: degree correlations.

Newman's degree assortativity coefficient $r$ is exactly this. It is computable from the degree sequence and mixing matrix in $O(E)$ time. The pre-flight: compute $r$; flag if $|r|$ exceeds a size-dependent threshold, because assortativity is biased at small $N$. The calibration simulation needs to establish the distribution of $r$ under the CSN's actual null (i.i.d. draws from a power-law family) to set the threshold.

One subtlety: piece #12 shows that pass rate under BA equals (1 − power), not Type I error. The pre-flight here is not trying to detect that the data is BA; it is trying to detect that the CSN diagnostic statistic has lost its ability to distinguish pass from reject. These are related but not identical - and the proposal should make this distinction explicit in Stage 3.

---

## Calibration Is the Hard Problem, and It Needs Its Own Simulation Design

The proposal mentions the anticipated failure mode that pre-flights might be miscalibrated. This is more serious than the proposal acknowledges, for a structural reason: calibration requires knowing the false-alarm rate on held-out distributional families that were not used to design the pre-flight threshold. If the calibration families and the design families overlap, the result overstates pre-flight reliability.

I recommend the simulations be structured as follows:

- **Design set**: the cases known to trigger the failure (t(3) for BCa; BA networks for CSN)
- **Calibration set**: held-out families that could plausibly be confused with the design cases but should not trigger the pre-flight (e.g., t(5) for BCa, which has an existing third moment; configuration-model networks with empirical degree sequences for CSN)
- **Reporting**: both the detection rate on the design set and the false-alarm rate on the calibration set, as a pair

Without this structure, the pre-flight thresholds will be tuned to the demonstration cases rather than to the underlying reliability condition, and the piece's practical claim - that a practitioner can use these checks prospectively - will not be supported.

---

## A Note on the Third Procedure

The proposal mentions permutation tests in the resource estimate but does not name the third procedure explicitly. If the third case uses a permutation test, the pre-flight analog would be an exchangeability check (ACF/PACF for temporal data; Moran's I for spatial data). The same logic applies: the pre-flight should target the specific property the permutation test's null requires (exchangeability), not a general distributional check.
