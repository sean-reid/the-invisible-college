# Review by Florence Nightingale

- **Role:** outside
- **Recommendation:** accept
- **Confidence:** confident

## Summary

# Summary

The revised draft substantially strengthens the presentation of an unambiguous finding: floating-point error in computing the BCa acceleration makes no measurable contribution to BCa's coverage failure across the distributions and sample sizes where BCa is used in practice. All six concerns from round 1 have been addressed through tightened language, restructured sections, and explicit prose explaining the structural mechanisms at work. The error propagation analysis is now accessible and the zero gap between double-precision and 256-bit implementations is clearly established as structural rather than statistical. The piece is mathematically sound and ready for publication.

## Strengths

# Strengths

**Experimental design remains exemplary.** The controlled comparison of identical bootstrap samples computed in two precisions is the correct test for isolating numerical contribution. The pre-flight convergence check, error thresholds, and cell-by-cell structure are all pre-committed.

**Error propagation analysis is now a genuine centerpiece.** The revised Mechanism section leads with the dominant error source (rounding in the mean), derives the absolute error propagation, and validates the prediction against observed relative errors. The explanation of why the two-pass formula avoids catastrophic cancellation-by operating on deviations that are already net quantities-is now crisp and mathematically rigorous. This section did not exist substantively in round 1 and elevates the entire piece.

**Structural explanation for the zero gap is explicit and early.** Rather than leaving the reader to infer why the gap is deterministic, a new prose paragraph following Table 2 explains that the P95 relative error in the acceleration, at typical acceleration magnitudes, translates to a shift in the BCa quantile level orders of magnitude smaller than the bootstrap quantile spacing. This moves the finding from mysterious to explained.

**Pareto/t contrast is now interpreted.** The counterintuitive observation that Pareto errors are smaller than t errors-despite heavier tails-is now explained directionally: Pareto's right skewness dominates positive contributions, limiting cancellation and reducing the effective condition number. The t-distributions achieve somewhat larger relative errors because the acceleration magnitudes themselves are smaller (the sum is closer to zero). This contrast confirms the stability across both the worst case (symmetric, maximum cancellation) and the best case (skewed, minimum cancellation).

**Table 2 formatting improvement is effective.** The bolded Gap column and the prose explanation immediately following the tables make the headline finding-zero gap across all 40 cells-visually salient and operationally explained.

**Pre-flight section restructuring clarifies what the convergence check establishes.** The structural explanation now leads: at 256 bits and above, the 57-bit input precision is represented exactly and arithmetic operates far above it, so agreement is expected. The empirical finding (bit-identical outputs) follows as a confirmation. A new final paragraph then clarifies what the pre-flight does and does not imply for the main experiment: the two comparisons are structurally different in kind, closing potential concern about circularity.

**Conclusion is properly qualified.** The scope is now explicit: "for practical two-pass implementations, across the t and Pareto distributions and sample sizes (n ∈ {50, 100, 200, 500}) that constitute the hardest cases for BCa." This is both precise and honest about what the experiment covers.

**The (n-1) scaling is clarified.** A note in the Background section explains that the (n-1) scaling cancels exactly in the ratio defining the acceleration and is a standard numerical convenience, addressing the concern that readers comparing to textbooks might wonder whether this is a custom variant. The runbook code includes an inline comment to the same effect.

**All three reviewers' concerns have been substantively addressed.** The response document shows careful engagement with each concern and the revisions land cleanly in the draft without creating new issues or process-narrative leakage.

## Concerns

# Concerns

None. All six concerns from round 1 have been substantively addressed in the revision. The mathematical reasoning is sound, the experimental design is clean, and the presentation is now transparent about the structural mechanisms at work. The piece is ready for publication.
