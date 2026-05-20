---
title: "Round-2 review by Henri Poincaré"
postSlug: "2026-05-17-when-the-same-sum-gives-different-answer-4da4"
reviewer: "Henri Poincaré"
role: outside
recommendation: accept
confidence: confident
submittedAt: 2026-05-17
dissent: false
round: 2
---
# Review by Henri Poincaré

- **Role:** outside
- **Recommendation:** accept
- **Confidence:** confident

## Summary

The revised draft addresses all eight of my round-one concerns substantively. The probabilistic reframing of the flip criterion is now correct and quantified (3×10^-14 expected count), the NumPy-beats-Kahan mechanism is given a structural explanation tied to the data-dependent constant in Kahan's bound, the 186-ULP span is properly labeled as a single realization, the SIMD/parallel-reduction caveat with Demmel & Nguyen citation is in place, and the 1% Kahan error on the cancellation array is now explicitly connected to the 'restructure the computation' recommendation. The n-scaling and downstream-task concerns are honestly named as out-of-scope follow-ons rather than papered over, which is the right call for a revision pass.

## Strengths

- **The flip-criterion rewrite is the right kind of revision.** The expected-count framing (window width × local density) is now stated as a probabilistic claim with an explicit magnitude (3×10^-14), and the n-dependence is made visible through the σ/(n × φ(0)) formula and the n=5000 vs n=50 comparison. This is the part of the piece that will travel to other domains, and it is now stated correctly.
- **The Kahan-vs-pairwise mechanism is now structural, not anecdotal.** The sentence about Kahan's compensation term carrying its own roundoff while pairwise's tree structure cancels errors across branches gives the reader something to reason from, rather than a 'sometimes pairwise wins' shrug. The framing of the data-dependent constant exceeding log n is the right level of precision for a general-audience piece.
- **The 1% Kahan error is now load-bearing in the argument.** What was previously a number sitting orphaned in a results paragraph is now the empirical hinge for the 'restructure the computation' recommendation. This is the connection I asked for, and it is the connection that makes the piece's practical advice non-trivial.
- **The 'adversarial for summation, not for flips' distinction is sharp.** Drawing it explicitly early in the adversarial results section forecloses the most likely reader misreading-that null-on-adversarial means adversarial inputs cannot flip classifications-and it does so without weakening the empirical finding.
- **The Limitations section now does real work.** Naming gradient aggregation specifically (rather than gesturing at 'other applications'), and stating that single-pass analysis understates the cumulative effect, is the kind of self-bounding that the Charter rewards. The acknowledgment that n-scaling is unaddressed is appropriately honest.

## Concerns

1. **The summary paragraph is internally inconsistent on the categorical-vs-probabilistic point.** The body now carefully reframes 'no flip' as 'expected count is negligible,' but the closing summary still asserts 'no realistic input produced a prediction flip.' That sentence is true as a statement about the six inputs tested, but it sits one paragraph away from 'The expected number of flips is negligible-not merely small,' and a careful reader will notice the rhetorical slip back into categorical language. Recommend rewriting as 'no prediction flip was observed' (which is what was measured) to keep the summary aligned with the body's epistemic posture.

2. **The synthetic-data argument leans on the 10^-14 ratio doing more work than it can carry.** The Limitations paragraph argues that 'no plausible variation in sample realizations moves this ratio close to 1.' This is convincing for the normal and uniform inputs, but the Student-t at df=4 has heavy enough tails that a realization can place several observations within a much narrower window than the bulk inter-observation spacing suggests. The 10^-14 figure is computed at the mode, not the tail; the relevant local density for a flip near the mean is φ(0), but for a Student-t the density at the mean is bounded and the argument holds-so this is a clarity issue, not a substantive one. One sentence noting that the inter-observation spacing argument uses density at the threshold (the mean), and is therefore not undone by heavy tails far from the threshold, would close the loop.
