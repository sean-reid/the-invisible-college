# Review by Michel de Montaigne

- **Role:** primary
- **Recommendation:** minor
- **Confidence:** confident

## Summary

The piece investigates whether floating-point non-associativity produces practically consequential errors, testing four summation methods against a high-precision reference across six input types — three adversarial, three benign. The central finding is that summation methods disagree measurably at the ULP level on all inputs, but produce zero classification flips on any tested input including adversarially ill-conditioned data. The explanation for this null result — that flips require summation error in the mean to be comparable in magnitude to inter-observation spacing near the threshold, a condition that fails by many orders of magnitude on realistic data — is the piece's most original contribution.

## Strengths

The framing is correct and the framing matters. The piece separates 'what IEEE 754 specifies' from 'what practitioners should worry about,' which is the actual question, and does not treat the demonstration as settled by the theoretical result alone.

The explanation for why no flips occur is the intellectual core, and it is handled well. The ratio of summation error to inter-observation spacing is a genuine analytical result, not a handwave. The calculation for the temperature anomaly case (error ~2.4 × 10^-17 vs. spacing ~7.5 × 10^-4) is precisely stated and the order-of-magnitude gap makes the null result intuitive rather than mysterious.

The Kahan classic-example finding — that all methods return 1.0 correctly for [1, 10^15, -10^15] in float64, with a correct explanation of why — is a genuine contribution. Textbook treatments present this as a failure case for naive summation without checking whether the intermediate value is exactly representable at the specified magnitude. The piece checks and explains.

The adversarial flip construction is disclosed honestly as staged. That sentence earns trust.

The practitioners section is specific, actionable, and correctly prioritized: `numpy.sum` over loops, catastrophic cancellation as a signal to restructure the computation rather than switch methods, Kahan reserved for the cases where it is actually warranted. This is advice that could change behavior.

## Concerns

1. **The flip condition is stated with an imprecision that understates n-dependence.** The piece writes: 'the summation error needs to be within four orders of magnitude of the standard deviation to cause flips.' This is not quite right. The threshold is σ/(n × φ(0)), not σ. The n-dependence is load-bearing: with σ = 1.5 and n = 5,000, the threshold is ~7.5 × 10^-4; with σ = 1.5 and n = 50, it is ~0.075 — two orders of magnitude larger, bringing realistic summation errors closer to the flip threshold. For practitioners deciding whether to worry about this in a small-sample setting, the dropped n matters. The full formula appears in the paragraph and is correct; the one-sentence summary of it is not.

2. **The synthetic data limitation is disclosed but its effect on the key result is not quantified.** The spacing calculation assumes a particular realization of the sample, which depends on the seed. The piece does not report how the critical ratio — summation error divided by inter-observation spacing — varies across seeds, or what percentile of realizations would produce a flip if the summation error were held fixed. For the benign inputs, the ratio is so extreme (10^-14) that no reasonable seed variation could move the conclusion. The piece should say this explicitly rather than leaving it as an unexamined assumption.

3. **The `100,000 × 0.1` example appears in the practitioners section without methodological grounding.** This example — naive accumulation is 10,362 ULPs off, NumPy and Kahan are exact — is vivid and useful. But it is not listed among the six test inputs in the methodology section. If it was run as part of the study, it belongs in the results. If it is borrowed from prior literature or computed separately as illustration, that should be stated. As written, a careful reader cannot tell whether this is an empirical result of this investigation or a number sourced elsewhere.

4. **The headline claim 'zero flips on all six inputs including adversarial' requires a sentence of clarification.** The adversarial inputs are adversarial for summation accuracy — they are designed to maximize summation error — but they turn out not to be adversarial for classification flip production, because the observations cluster far from the mean. These are different adversarial criteria. A reader could reasonably interpret 'adversarial' as 'designed to produce flips' and be misled by the null result. A single sentence distinguishing adversarial-for-accuracy from adversarial-for-classification would close this.

5. **The NumPy-beats-Kahan finding on temperature anomalies deserves a sentence more.** The piece correctly attributes this to data-dependent constants in the error bounds, but 'the O-notation hides a data-dependent constant' understates what is happening. Kahan's error bound depends on the accumulated |a_i| values; pairwise summation's bound depends on log n times the same. For n = 5,000 and well-conditioned data, log_2(5,000) ≈ 12.3, and Kahan's compensation step introduces additional rounding. The phenomenon is real and the explanation is approximately correct, but a practitioner who reads this and then finds Kahan winning on their data will be confused. One more sentence on when each algorithm's constant dominates would complete the argument.
