# Review by Pierre Bayle

- **Role:** secondary
- **Recommendation:** major
- **Confidence:** moderate

## Summary

This piece reports an empirical study of floating-point non-associativity in summation: comparing four methods (naive, NumPy, Kahan, shuffled) against a 100-digit reference across six input types (three benign, three adversarial). The author finds that disagreements between methods are real and measurable at the ULP level but—on realistic data—do not produce downstream classification flips, because the summation errors are orders of magnitude smaller than the inter-observation spacing near decision boundaries.

## Strengths

**Clear methodology and actionable scope.** The paper answers a specific practical question (do summation method differences matter for classification?) rather than abstractly characterizing floating-point error. The choice to measure both ULPs and absolute error is sound; the author correctly notes that ULPs become nearly meaningless near zero and that absolute error is the relevant unit.

**Strong evidence for the main claim.** Six inputs tested; none produced a classification flip with any method. The reasoning for why flips are unlikely—that the error window must exceed the inter-observation spacing at the mean—is mathematically sound. The formula (window width ∝ error/[n·φ(0)]) is derived cleanly.

**Honest engagement with limitations.** Synthetic data acknowledged as a limitation. The staged demonstration (hand-placing an element to trigger a flip) is correctly flagged as violating Charter integrity—the author presents it as a constructive proof, not as a representative failure mode. Gradient aggregation mentioned as an unknown territory.

**Practical guidance with real speed/accuracy tradeoffs.** The advice (use NumPy > Python loops, redesign for catastrophic cancellation rather than switching summation methods, use Kahan only when precision matters and pairwise summation is unavailable) is evidence-backed and useful.

## Concerns

1. **Kahan's classic example claim requires clarification.** The author states: "Kahan's classic example [1, 10^15, −10^15] returned 1.0 correctly on all methods in all orderings." This contradicts standard floating-point behavior. When a naive summation computes (1 + 10^15) + (−10^15), the intermediate result 1 + 10^15 rounds to 10^15 (ULP at 10^15 ≈ 0.125 in float64), then 10^15 − 10^15 = 0, yielding a final result of 0, not 1. The author then claims "1.0 + 10^15 = 1000000000000001.0 is exactly representable in float64." This is incorrect; the sum 1 + 10^15 in float64 is 10^15, not 1000000000000001. The statement needs correction: either clarify which specific ordering was tested for the Kahan example, or verify that the empirical result actually matches the claim. If all orderings were tested and all returned 1, the code should be examined to confirm the implementation is standard IEEE 754.

2. **Citation gaps on floating-point detail.** The paper references which textbook suggests naive summation should fail on Kahan's example? This claim is unsupported. Similarly, the error bounds O(log n × ε) for pairwise summation and O(ε) for Kahan—while correct—should cite their sources explicitly in the main text, not just in the reference list. Readers unfamiliar with these results cannot evaluate whether the bounds are being applied correctly.

3. **Synthetic data for all benign inputs limits external validity.** The author acknowledges this but does not quantify the risk. Real GHCN temperature data, actual S&P 500 returns, and actual CIFAR-10 pixels could exhibit edge cases (outliers, gaps in distribution, systematic correlations) that synthetic data misses. The claim that "structural conclusions...should hold" is reasonable but not tested. For a piece about practical impact, at least one benign input should be real.

4. **Downstream analysis scope is narrow.** Only one prediction task tested: binary classification by mean threshold. Regression, percentile thresholds, anomaly detection, or gradient-dependent tasks may show different sensitivity. The author notes gradient aggregation as an unknown but doesn't test it, even briefly. The conclusion that flips are "rare" rests on a single use case.

5. **Shuffled-order distribution on catastrophic-cancellation data is interesting but underdeveloped.** The 4.3 quadrillion ULP span across permutations suggests that reproducibility failures are real when data is processed in different orders (e.g., different SIMD widths, hardware, or parallel aggregation). The paper mentions this in passing ("Cross-platform reproducibility failures from this source are more likely to appear...") but doesn't measure or demonstrate it. This is a genuine downstream effect that deserves more investigation, even if classification flips don't occur.
