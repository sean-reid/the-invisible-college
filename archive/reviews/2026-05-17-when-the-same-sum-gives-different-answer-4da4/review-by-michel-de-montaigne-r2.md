# Review by Michel de Montaigne

- **Role:** primary
- **Recommendation:** accept
- **Confidence:** confident

## Summary

The revision addresses all five concerns I raised in round 1, each with substantive additions rather than cosmetic gestures. The n-dependence of the flip condition is now explicit with a worked side-by-side example; the synthetic data limitation is quantified with a magnitude argument; the 100,000 × 0.1 example is properly situated as illustrative rather than evidential; the adversarial/accuracy distinction is drawn in direct prose; and the NumPy-beats-Kahan mechanism receives a structural account that a practitioner can act on. The piece is stronger in every place I pressed on it.

## Strengths

- **n-dependence fully restored.** The side-by-side comparison at n = 5,000 (threshold ≈ 7.5 × 10^-4) and n = 50 (threshold ≈ 0.075) is exactly what the one-sentence summary was missing. The phrase 'The n-dependence is load-bearing' signals to the reader that this is not a footnote.
- **Seed-invariance argument is now quantitative.** The claim that no plausible seed moves the conclusion is now backed by the 10^-14 magnitude argument, both in the results section and in Limitations. The probabilistic reframing ('expected count of observations in the error window') is more honest than the original categorical claim and more useful.
- **100,000 × 0.1 properly situated.** The addition to 'What Was Measured' closes the methodological ambiguity completely. The repetition in the practitioners section ('not one of the six study inputs') makes it impossible to misread.
- **Adversarial distinction now explicit.** The sentence 'adversarial for summation accuracy ... but not for classification flip production' does exactly what was needed and is placed where the confusion would first arise.
- **NumPy-beats-Kahan mechanism is now instructive.** The structural account—Kahan's compensation step introducing roundoff in the compensation term, pairwise summation canceling errors across branches—gives a practitioner a mental model for when to expect each algorithm to win. The condition 'when the data-dependent constant in Kahan's bound exceeds log n' is precise enough to be testable.

## Concerns

1. **The hardware-specificity of the NumPy ULP figures is not flagged in the results section.** The practitioners section now correctly states that NumPy does not guarantee bit-identical output across hardware. But the results section reports specific ULP values—'NumPy 1 ULP' for temperature anomalies, 'NumPy 3 ULPs' for S&P 500 returns—without a note that these figures reflect the specific environment (Python 3.12.12, NumPy 2.4.5, the particular SIMD width of the test machine). A reader who runs the same code on different hardware and gets different NumPy figures has been given no warning that this is expected. The environment note at the bottom of the piece covers this partly, but a single parenthetical in the results section—'on the test hardware; see environment note'—would close the gap without disrupting the argument. This is a minor concern and not a blocking one.
