# Response to Reviewers

I thank all three reviewers for careful readings. Several concerns are well-founded and have been addressed in the revised draft; a smaller number are declined with reasoning below.

---

### Response to Henri Poincaré

**Concern 1: Flip criterion stated deterministically but is actually probabilistic.**

Addressed. The draft previously asserted "no realistic input produces a flip" as a categorical claim. The revised text reframes the finding: a flip requires the expected number of observations in the error window to be at least O(1), and the claim is now explicitly about the expected count being negligible (on the order of 3 × 10^-14 for the temperature data), not about categorical impossibility. The threshold sentence is rewritten accordingly.

**Concern 2: NumPy beats Kahan on temperature anomalies is hand-waved.**

Addressed. The revised draft now gives a structural explanation: Kahan's compensation step itself introduces roundoff in the compensation term, while pairwise summation's tree structure can cancel errors across branches in ways a linear-pass correction cannot. The win occurs specifically when the data-dependent constant in Kahan's error bound exceeds log n-a condition the temperature data at n = 5,000 satisfies.

**Concern 3: n held fixed; scaling question unaddressed.**

Partially addressed. A new paragraph in Limitations explicitly names the n-scaling question, notes that the flip threshold scales as σ/(n × φ(0)) and therefore as 1/n, and proposes a systematic n-sweep as a natural follow-on. Running a new n-sweep experiment is outside the scope of this revision pass.

**Concern 4: 186-ULP span presented as a population fact.**

Addressed. The revised text labels it explicitly as "a single realization from one random seed of 1,000 permutations" and notes that a different seed produces a different span.

**Concern 5: Downstream task is reductive.**

Acknowledged in the revised Limitations section, which now specifically names gradient aggregation as the regime where single-pass analysis understates the problem and states that this study does not speak to that case. Expanding the pipeline to regression or gradient aggregation is outside this piece's scope.

**Concern 6: SIMD and parallel-reduction ordering absent.**

Addressed. A new sentence in the practitioners section states explicitly that NumPy's pairwise guarantee is not a guarantee of bit-identical output across hardware, with citation to Demmel & Nguyen (2015).

**Concern 7: Kahan's 1% error on cancellation array not interpreted.**

Addressed. The adversarial results section now makes the connection explicit: Kahan's 1% absolute error on the cancellation array is the direct empirical basis for the "restructure the computation" recommendation. The connection was previously left for the reader to assemble; it is now stated.

**Concern 8: Reference list omits parallel-reduction source.**

Addressed. Demmel, J., & Nguyen, H. D. (2015). "Parallel Reproducible Summation." IEEE Transactions on Computers, 64(7):2060–2070 has been added.

---

### Response to Michel de Montaigne

**Concern 1: Flip condition understates n-dependence.**

Addressed. The previous one-sentence summary ("within four orders of magnitude of the standard deviation") incorrectly omitted the n factor. The revised text gives the full formula σ/(n × φ(0)) and includes an explicit side-by-side comparison at n = 5,000 (threshold ≈ 7.5 × 10^-4) and n = 50 (threshold ≈ 0.075), making the two-order-of-magnitude scaling visible to practitioners working in small-sample settings.

**Concern 2: Synthetic data limitation not quantified.**

Addressed. The revised Limitations section now explicitly states that the critical ratio is on the order of 10^-14 and argues from that magnitude that no plausible seed variation could move the conclusion at n = 5,000. The claim "should hold" is replaced with a quantitative argument for why it must hold.

**Concern 3: 100,000 × 0.1 example not methodologically grounded.**

Addressed. Both the "What Was Measured" section and the practitioners section now explicitly identify this as a separate illustrative computation-not one of the six study inputs-and note that it uses a degenerate case (repeated identical non-representable values). A reader cannot now mistake it for a finding of the systematic study.

**Concern 4: "Zero flips on adversarial" needs clarification.**

Addressed. A sentence early in the adversarial results section now draws the distinction: the adversarial inputs in this study are adversarial for summation accuracy, not for classification flip production, because the observations do not cluster near the mean. The null result on adversarial inputs does not mean adversarial inputs cannot produce flips; it means these particular adversarial inputs don't.

**Concern 5: NumPy beats Kahan deserves more explanation.**

Addressed. See response to Poincaré concern 2; the mechanism is now explained structurally in the draft.

---

### Response to Pierre Bayle

**Concern 1: Kahan classic example claim contradicts standard floating-point behavior.**

Declined. The review asserts that `1 + 10^15` in float64 "rounds to 10^15," citing a ULP of 0.125 at that magnitude, and therefore concludes naive summation should return 0. This is incorrect, and the draft's finding is correct.

The key fact is that float64 represents all integers exactly up to 2^53 ≈ 9.007 × 10^15. Since 10^15 < 2^53, both 10^15 and 10^15 + 1 are exactly representable integers in float64. The ULP at 10^15 is 2^(49−52) = 0.125, which means consecutive representable floats are spaced 0.125 apart in the range [2^49, 2^50). The integer 10^15 + 1 = 1,000,000,000,000,001 is exactly 8 steps of 0.125 above 10^15-it is a representable value. The intermediate sum `1.0 + 10^15 = 1000000000000001.0` is computed exactly, and the subtraction `1000000000000001.0 − 10^15 = 1.0` is also exact. The review conflates "the ULP is 0.125" (meaning non-integer values between adjacent floats cannot be represented) with "1 cannot be added exactly to 10^15" (false, because the result is an exactly representable integer). The failure mode requires the intermediate sum to exceed 2^53; at 10^15 it does not.

The revised draft adds the statement "all integers up to 2^53 ≈ 9.0 × 10^15 are exactly representable in float64" to make the mechanism visible to readers who might share this intuition. The empirical finding stands.

**Concern 2: Citation gaps on floating-point detail.**

Partially addressed. The error bounds for pairwise summation and Kahan are standard results from Higham (2002, Ch. 4), already cited. The phrase "textbook treatment suggests" has been removed and replaced with a direct statement of when the failure mode does and does not apply, avoiding the need to cite a specific textbook that circulates the example without verifying the representability condition.

**Concern 3: Synthetic data for all benign inputs limits external validity.**

Acknowledged but not remedied in this revision. Fetching real GHCN, S&P 500, and CIFAR-10 data requires downloads or registrations that are out of scope for a revision pass. The Limitations section is strengthened with a quantitative argument (the 10^-14 ratio magnitude) for why the structural conclusions are insensitive to this limitation, and real-data validation is named explicitly as a follow-on.

**Concern 4: Downstream analysis scope is narrow.**

Acknowledged. The revised Limitations section now specifically names gradient aggregation as the regime where the reproducibility problem lives and where single-pass analysis understates the cumulative effect. The piece does not extend to that regime.

**Concern 5: Shuffled-order distribution underdeveloped.**

The cross-platform reproducibility observation is real and is now surfaced more explicitly: the practitioners section adds a direct statement that `numpy.sum` does not guarantee bit-identical output across hardware, with citation to the Demmel & Nguyen reproducible-summation literature. Measuring or demonstrating cross-SIMD divergence empirically is a separate experiment outside this piece's scope.

**On the overall major recommendation.**

Respectfully declined. After examining each concern in detail, none requires structural revision of the piece. The most severe concern raised-that the Kahan example finding is factually wrong-is a reviewer error, as argued above. The remaining concerns call for clarification, probabilistic reframing, and limitation-strengthening, all of which are addressed. The piece's central claim is intact; this revision strengthens rather than retreats from it.
