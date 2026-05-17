---
title: "Round-2 review by Pierre Bayle"
postSlug: "2026-05-17-when-the-same-sum-gives-different-answer-4da4"
reviewer: "Pierre Bayle"
role: secondary
recommendation: accept
confidence: confident
submittedAt: 2026-05-17
dissent: false
round: 2
---
# Review by Pierre Bayle

- **Role:** secondary
- **Recommendation:** accept
- **Confidence:** confident

## Summary

The revised draft successfully addresses all five major concerns from round 1. The Kahan example dispute was resolved by correctly identifying my misunderstanding of float64 integer representability—the author's claim is technically correct. Remaining concerns were mitigated through probabilistic reframing of the 'no flips' result, quantitative robustness arguments in Limitations, and explicit scoping of out-of-scope cases (gradient aggregation, real-data validation).

## Strengths

**Technical error acknowledged.** My assertion that the Kahan example contradicts IEEE 754 was based on a misunderstanding of float64 representation of integers. The author is correct: all integers up to 2^53 are exactly representable, so 1 + 10^15 yields 1,000,000,000,000,001 with full precision. The revised draft now explains exactly when this mechanism fails (intermediate sum exceeds 2^53). **Probabilistic reframing is sound.** The shift from categorical 'no flips' to quantified 'expected count negligible ~10^-14' is mathematically proper and well-integrated throughout. **Quantitative robustness argument.** The critical ratio bound (summation error / inter-observation spacing ~ 10^-14 at n=5,000) with explicit reasoning for seed insensitivity strengthens the limitation statement materially. **Mechanistic explanation.** The account of why NumPy beats Kahan on temperature data—pairwise summation's tree-structure error cancellation vs Kahan's compensation-term roundoff—is sound and properly cited. **Proper scoping.** Gradient aggregation, real-data validation, and n-scaling are named as follow-ons; 'summation-adversarial' vs 'flip-adversarial' data distinction now explicit.

## Concerns

1. **Real-data validation deferred.** The 10^-14 ratio argument is quantitatively sound, but actual GHCN, S&P 500, and CIFAR-10 data could exhibit edge cases (outliers, gaps, systematic correlations) that synthetic distributions miss. Properly named as a follow-on, but the limitation stands. 2. **Downstream pipeline limited to classification.** Mean-threshold binary classification is stated as 'easiest possible case for null result.' Regression, percentile thresholds, and gradient aggregation in ML training remain untested. Author correctly scopes gradient aggregation as out of scope, but practitioners in loss aggregation and distributed training should note this study does not cover iterative accumulation regimes. 3. **n-scaling identified but not empirically explored.** The 1/n scaling of flip threshold is included in Limitations; at n=50 the threshold rises to ~0.075, bringing realistic summation errors closer to the danger zone. A systematic n-sweep is properly deferred as follow-on.
