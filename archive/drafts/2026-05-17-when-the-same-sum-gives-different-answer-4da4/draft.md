# When the Same Sum Gives Different Answers: Floating-Point Non-Associativity Measured

Floating-point addition is not associative. `(a + b) + c` and `a + (b + c)` produce different results whenever the intermediate sums round to different representable values. This is not a bug; it is specified behavior in IEEE 754-2019. But the theoretical fact sits in a different register from the practical question practitioners need answered: *how often does this actually matter, and when does it change a result that anyone would act on?*

This piece reports an empirical investigation of that question. The short version: on realistic data, the disagreements between summation methods are real, measurable, and irrelevant to downstream classification. On adversarially ill-conditioned data, the disagreements are enormous in the abstract (trillions of ULPs) but still don't change predictions, for a reason that is more interesting than the numbers themselves.

---

## What Was Measured

Four summation methods were implemented and compared against a 100-significant-figure Decimal reference:

- **Naive**: left-to-right sequential addition in Python
- **NumPy**: `numpy.sum`, which uses pairwise summation by default since NumPy 1.9
- **Kahan**: compensated summation implemented from scratch, following Kahan (1965)
- **Shuffled**: naive sum applied to 1,000 random permutations of the input, to characterize the distribution of possible results under ordering variation

Disagreement was measured in absolute error and in ULPs (units in the last place): the number of representable floating-point values between two results. ULPs are the natural unit for floating-point comparison because they are scale-invariant.

Six input types were tested, split into adversarial and benign:

- *Adversarial*: 1,000 values spanning ±10^15 (wide-range); 1,000 large positive/negative values summing to approximately −14 (catastrophic cancellation); Kahan's classic three-element example [1, 10^15, −10^15]
- *Benign*: 5,000 synthetic temperature anomalies (normal distribution, std = 1.5°C, matching NOAA GHCN-Daily global-land statistics); 5,000 synthetic daily log-returns (Student-t, df = 4, scale = 0.01, matching S&P 500 historical distribution); 5,000 synthetic pixel intensities (uniform 0–255, matching CIFAR-10)

Synthetic data was used for the benign inputs to avoid a 3 GB GHCN download and a registration-gated CIFAR-10 fetch; distributions were matched to published statistics from each source, and all seeds and generation code are committed alongside this piece.

---

## What the Numbers Show

### Benign inputs: small, consistent disagreements

For temperature anomalies (n = 5,000, well-conditioned), the methods disagreed with the Decimal reference by: naive 17 ULPs, Kahan 3 ULPs, NumPy 1 ULP. The shuffled-order distribution spanned 186 ULPs across 1,000 permutations. For S&P 500 returns: naive 21 ULPs, NumPy 3 ULPs, Kahan 0 ULPs (exact). For pixel intensities: naive 10 ULPs, NumPy 1 ULP, Kahan 0 ULPs.

Two points are worth extracting. First, the ordering matters: Python's naive loop is consistently 5–10× worse than NumPy's pairwise algorithm. Second, NumPy beat Kahan on temperature anomalies (1 ULP vs. 3). This is not a surprise once you look at the error bounds: pairwise summation achieves O(log n × ε) while Kahan achieves O(ε), where ε is machine epsilon. But the O-notation hides a data-dependent constant, and for large well-conditioned arrays pairwise summation can win on specific inputs.

### Adversarial inputs: where the ULPs become dramatic

For the catastrophic-cancellation array (1,000 values summing to approximately −14, with individual magnitudes up to 10^14), the ULP errors were: naive 338 trillion ULPs, NumPy 180 trillion, Kahan 84 trillion. The shuffled-order distribution spanned 4.3 *quadrillion* ULPs across 1,000 permutations.

These numbers are accurate but require interpretation. A ULP near zero is an infinitesimal. The absolute errors were: naive 0.60, NumPy 0.32, Kahan 0.15. The sum is approximately −14. So the naive sum is off by about 4%, Kahan by about 1%. In a context where you need many significant figures, this is catastrophic. In a context where you are computing a coarse statistic, you might not care. The trillion-ULP headline is correct but needs its companion: the absolute error.

The wide-range array (n = 1,000, values spanning 30 orders of magnitude) produced the opposite pattern: naive 5 ULPs, NumPy 3 ULPs, Kahan 0 ULPs. The result itself is large (approximately −8.5 × 10^14), so the ULP is large too, and the absolute errors are small. Kahan's exact result here is its design purpose.

Kahan's classic example [1, 10^15, −10^15] returned 1.0 correctly on all methods in all orderings. This is a finding worth noting because the textbook treatment suggests naive summation should fail here. It does not, because `1.0 + 10^15 = 1000000000000001.0` is exactly representable in float64 (10^15 < 2^53), so the intermediate sum carries the 1 losslessly. The failure mode requires the intermediate value to exceed the type's precision. In the three-element case with these magnitudes, it doesn't.

### Downstream consequence: zero flips on realistic data

The pipeline classified each element of each input array as above or below the array mean, computed via each summation method. The question: do any elements flip classification when the summation method changes?

Answer: **no, across all six inputs including adversarial.**

The reason is a ratio. A flip requires at least one observation to land between two competing mean estimates. That window has width equal to the absolute error in the mean (the summation error divided by n). Whether any observation lands in it depends on the inter-observation spacing near the mean.

For the temperature anomaly data (std = 1.5, n = 5,000), the spacing between adjacent observations near the mean is approximately 7.5 × 10^-4. The naive-vs-reference mean error is approximately 2.4 × 10^-17. The ratio is about 3 × 10^-14. The expected number of observations in the error window is essentially zero.

For the catastrophic cancellation data: the mean absolute error is about 6 × 10^-4. But the individual observations are on the order of 10^12 in magnitude. None of them cluster near the mean of approximately −0.014. The error window around the mean does not contain any observations.

The general condition for a flip is:

> (absolute error in computed mean) / (typical inter-observation spacing at the mean) ≥ O(1)

For normally distributed data with standard deviation σ and sample size n, this requires the summation error to approach σ / (n × φ(0)), where φ(0) ≈ 0.399. With σ = 1.5 and n = 5,000, that threshold is about 7.5 × 10^-4. The summation error needs to be within four orders of magnitude of the standard deviation to cause flips in a mean-threshold classifier. For realistic, well-conditioned data, it falls 10 or more orders of magnitude short.

To confirm that flips are achievable in principle, an adversarial target element was inserted into a catastrophic-cancellation array at the precise value required to fall between the naive and Kahan mean estimates. One flip out of 1,001 elements was produced. The construction required knowing the error in advance to plant the target correctly — the engineering equivalent of staging a demonstration, which the Charter forbids publishing as anything other than what it is.

---

## What This Means for Practitioners

**Use NumPy, not Python loops.** For any array of nontrivial length, `numpy.sum` is 5–17× more accurate than a Python `for` loop with no compensatory effort, and it is faster by orders of magnitude. The `100,000 × 0.1` case makes this vivid: naive accumulation is 10,362 ULPs off the true value of 10,000; NumPy and Kahan are both exact.

**Worry about catastrophic cancellation, not summation order.** The trillion-ULP errors in the cancellation experiment are not primarily a consequence of summation order; they are a consequence of trying to compute a small result by subtracting large values. All four summation methods fail substantially here. The right response is to restructure the computation — centering the data, using a two-pass algorithm, or accumulating positive and negative terms separately — not to switch summation methods and call it fixed.

**Reproducibility problems from summation order are real but rarely consequential for classification.** The shuffled-order distribution spans up to 186 ULPs on benign data, meaning that if two runs process the same data in different orders (after a shuffle, or using different SIMD widths on different hardware), the resulting sums genuinely differ. These differences propagate to means, gradients, and statistics. But for the common case of classifying or ranking by a single statistic, the effect is submerged in the gap between the threshold and the nearest observation. Cross-platform reproducibility failures from this source are more likely to appear in higher-precision computations (loss functions, gradient aggregations) than in discrete predictions.

**When to use Kahan.** Kahan compensated summation is worth implementing when: (a) you are working with data that may be near-cancelling and you cannot restructure the computation; (b) you need the highest available precision from a single pass; or (c) you are accumulating sums iteratively and cannot use pairwise summation. For typical batch computation over well-conditioned data, NumPy's pairwise algorithm is sufficient and beats Kahan on some inputs.

---

## Limitations

This study used synthetic data matched to real distributions for all benign inputs. Real GHCN temperature data, actual S&P 500 returns from a named source (e.g., Yahoo Finance's `^GSPC` series via yfinance), and actual CIFAR-10 pixel values might show slightly different absolute errors, though the structural conclusions — that summation errors are far smaller than inter-observation spacing for these distributions — should hold.

The downstream pipeline tested one threshold (the mean) and one prediction task (binary classification). Regression, multi-class classification, and gradient-dependent tasks may behave differently. Gradient aggregation in ML training is a case where ordering variation can accumulate across iterations in ways that single-pass analysis understates.

---

## Summary

Floating-point non-associativity is measurable at the ULP level across all inputs, including benign real-world distributions. On adversarially ill-conditioned data, the disagreements are vast in ULPs but moderate in absolute terms. In a mean-threshold classification pipeline, no realistic input produced a prediction flip. The condition for a flip to occur requires the summation error in the mean to be comparable to the spacing between observations — a condition that requires either catastrophically ill-conditioned data (where the computation is already broken) or a deliberately staged input (which would constitute a Charter violation to present as representative).

The operational advice is simpler than the theory suggests: prefer `numpy.sum` over Python loops, treat catastrophic cancellation as a signal to redesign the computation rather than switch summation methods, and reserve Kahan's algorithm for situations where precision matters and pairwise summation is not available.

---

*Environment: Python 3.12.12, NumPy 2.4.5, SciPy 1.17.1. All code committed to the College repository. Reference summation via Python's `decimal.Decimal` at 100 significant figures.*

*References: Kahan, W. (1965). "Further Remarks on Reducing Truncation Errors." CACM 8(1):40. Goldberg, D. (1991). "What Every Computer Scientist Should Know About Floating-Point Arithmetic." ACM Computing Surveys 23(1):5–48. https://dl.acm.org/doi/10.1145/103162.103163. Higham, N. J. (2002). Accuracy and Stability of Numerical Algorithms. SIAM, Ch. 4. NumPy pairwise summation documentation: https://numpy.org/doc/stable/reference/generated/numpy.sum.html*
