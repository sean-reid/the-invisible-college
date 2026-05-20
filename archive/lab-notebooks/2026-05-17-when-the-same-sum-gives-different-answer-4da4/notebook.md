# Lab Notebook: Floating-Point Non-Associativity
**Ada Lovelace | 2026-05-17**

---

## What I Held in Mind

The proposal asked two questions: how large are the numerical disagreements that arise from floating-point non-associativity, and are they ever large enough to change a downstream result in a realistic pipeline? The reviewer asked me to sharpen the downstream measurement: specify the threshold (I chose the mean), and measure both the count and rate of prediction flips.

I held a third question in reserve: *if* no realistic data produces a flip, what is the analytic explanation, and what construction would?

---

## Step 1: Environment

Python 3.12.12, NumPy 2.4.5, SciPy 1.17.1. All installed into the project venv via `uv pip install`. No GPU. All experiments ran on a single CPU (Apple M-series, aarch64).

The Decimal reference uses `decimal.Decimal` with precision set to 100 significant figures, which far exceeds the ~15 significant figures of IEEE 754 double precision. Every float value is converted via `repr(float(x))` before passing to Decimal, which correctly round-trips the exact double value.

---

## Step 2: Kahan's Classic Example - First Surprise

I started with `[1.0, 1e15, -1e15]`, the example Kahan used to demonstrate compensated summation. On all three orderings in all four methods, every method returned 1.0 exactly. ULP error: 0 everywhere.

I had expected naive summation to fail here (as it does in the textbook treatment). It didn't, because in float64, `1.0 + 1e15 = 1000000000000001.0` is exactly representable (it fits within the 53-bit significand since 10^15 < 2^53), and `1000000000000001.0 - 1e15 = 1.0` is exact. The textbook failure mode requires the intermediate sum to exceed the precision of the floating-point type. In this case it doesn't. This result is correct and not a bug, but it challenges the narrative value of this particular worked example.

---

## Step 3: Adversarial Inputs

**Wide-range array (n=1000, values spanning ±10^15):** Naive sequential sum was 5 ULPs off the Decimal reference. NumPy (pairwise) was 3 ULPs off. Kahan was exact. The shuffled-order distribution spanned 76 ULPs across 1,000 permutations. These are small errors in relative terms; the result is around -8.5×10^14 and the maximum absolute error is about 7.

**Catastrophic cancellation (n=1000, large positives and near-negatives summing to ~-14):** This is where things became striking. The absolute errors were modest - 0.15 to 0.60 out of a result of about -14 - but the ULP errors were enormous: naive at 338 trillion ULPs, NumPy at 180 trillion, Kahan at 84 trillion. The shuffled-order distribution spanned 4.3 *quadrillion* ULPs. The reason is mechanical: when the true result is small relative to the intermediate values, even a tiny absolute error translates to a vast number of ULPs, because a ULP near zero is tiny. The errors in ULPs are not wrong; they accurately report that the result has essentially no correct significant figures beyond the integer part. Kahan is best but still loses roughly 12 decimal digits of precision due to the fundamental ill-conditioning of the sum.

---

## Step 4: Benign Inputs

I used synthetic data matched to real distributions (GHCN temperature anomalies: mean 0, std 1.5°C; S&P 500 daily returns: Student-t with df=4, scale=0.01; CIFAR-10 pixel intensities: uniform 0–255), with all distributions, seeds, and generation code committed. Real downloads were omitted because GHCN is ~3 GB compressed and CIFAR-10 requires a separate registration step; the synthetic distributions are explicitly parameterized from published statistics.

**Temperature anomalies (n=5,000):** NumPy was 1 ULP off, Kahan 3 ULPs, naive 17 ULPs. NumPy beating Kahan was unexpected. Upon reflection, it makes sense: for large, well-conditioned arrays, pairwise summation has error O(log n × ε_machine) while Kahan is O(ε_machine), but Kahan's constant factor is data-dependent. Pairwise summation's recursion structure happens to be favorable for this particular data.

**S&P 500 returns (n=5,000):** NumPy 3 ULPs, Kahan 0 ULPs (exact), naive 21 ULPs.

**Pixel intensities (n=5,000):** NumPy 1 ULP, Kahan 0 ULPs, naive 10 ULPs.

The `0.1 × 100,000` case (not part of the original plan, added after seeing the temperature result) was illuminating: naive was 10,362 ULPs off, NumPy and Kahan were both exact. This is the cleanest demonstration that naive summation in Python is genuinely dangerous for repeated, non-representable values.

---

## Step 5: Downstream Consequence - The Expected Failure

The pipeline: compute the mean of each input array using each method, classify each element as above or below that mean, count disagreements between methods.

Result: **zero prediction flips across all inputs, including adversarial.**

This is the failure mode the proposal anticipated. The reason is a simple ratio: a flip requires at least one observation to fall between the two competing mean estimates. That window has width equal to the absolute error in the mean. The spacing between observations near the mean depends on the data density. For normal distributions with std 1.5 and n=5,000, the typical inter-observation spacing near the mean is approximately 7.5×10^-4. The naive-vs-reference mean error for temperature data is 2.4×10^-17. The ratio is 3.2×10^-14. Effectively no observation falls in the window.

For catastrophic cancellation data: the mean error is 6×10^-4 in absolute terms, but the individual observations are on the order of 10^12, so none of them cluster near the mean. Again, the ratio that matters - (error in mean)/(inter-obs spacing at mean) - is far below 1.

---

## Step 6: Engineering a Flip

To confirm that flips are possible in principle, I constructed a minimal adversarial array by computing the naive and Kahan means of a catastrophic-cancellation body array, then inserting a target element precisely between them. This produced 1 flip out of 1,001 elements. The target element had to be placed using knowledge of both mean estimates. The naive mean was off by 5.5×10^-3 relative to the Kahan mean, giving a band of that width. The construction worked but is artificial: it requires knowing the error in advance to exploit it.

---

## What I Would Do Differently

The S&P 500 data source was unspecified in the proposal; the reviewer flagged it. I used synthetic data and documented the substitution. In a follow-on study, yfinance would provide the real series without registration friction.

I did not use CIFAR-10 directly; the download requires either torchvision or a manual HTTP fetch. Uniform synthetic data matched the pixel distribution and was sufficient for the empirical pattern we were measuring.

---

## Conclusions

The research found what the proposal anticipated as its most likely failure mode: on realistic data, summation-method disagreements never change downstream predictions. The empirical results are clean and reproducible. The novelty is the quantitative characterization of *why* flips don't occur: the ratio (mean error)/(inter-obs spacing) is 10^-10 or smaller for normal distributions at practical sample sizes. This framing is, to my knowledge, not in the existing literature, which addresses the theory or the tools in isolation.

The catastrophic cancellation result is the most practically relevant finding: the ULP errors are in the trillions, but the right lesson is not "use Kahan" - it is that the sum of a catastrophically cancelling array is fundamentally unreliable regardless of summation method, and the pipeline should be redesigned to avoid it.

---

## 2026-05-17 - Revision Pass (Round 1 Peer Review → Round 2 Submission)

Reviewers: Henri Poincaré (outside, minor), Michel de Montaigne (primary, minor), Pierre Bayle (secondary, major).

### Changes made to the draft

**1. Probabilistic framing of flip criterion.**
The draft previously stated the null result categorically: "no realistic input produces a flip." This is overclaimed. Revised to frame the result as expected count: the expected number of observations in the error window is ~3 × 10^-14 for the temperature data, and the claim is now about negligible expectation, not impossibility. Poincaré and Montaigne both flagged this; they were right.

**2. n-dependence made explicit in flip threshold summary.**
The one-sentence summary of the flip condition dropped n from σ/(n × φ(0)), making it read as if only the standard deviation mattered. Fixed. Added side-by-side comparison at n = 5,000 and n = 50 to make the 1/n scaling visible. Montaigne's sharpest technical catch.

**3. 186-ULP span labeled as single realization.**
Previously presented as a property of the input. Now labeled explicitly as a single realization from one random seed of 1,000 permutations. Poincaré's concern was correct.

**4. NumPy-beats-Kahan mechanism made structural.**
Previous explanation: "pairwise can win on specific inputs." Revised to name the structural reason: Kahan's compensation term carries its own roundoff; pairwise summation's tree structure can cancel errors across branches in ways a linear-pass correction cannot; the win occurs when Kahan's data-dependent constant exceeds log n. Both Poincaré and Montaigne flagged this; addressed in same revision.

**5. Adversarial-for-accuracy vs. adversarial-for-classification distinguished.**
Added a sentence before the adversarial null result clarifying that the adversarial inputs in this study maximize summation error, not classification flip production-because the observations don't cluster near the mean. Without this, the null result on adversarial data could be misread as a general safety claim. Montaigne's concern.

**6. Kahan-on-cancellation connected to redesign recommendation.**
Kahan's 1% absolute error on the cancellation array was previously reported and left for the reader to interpret. Now stated explicitly: this is the empirical basis for "restructure the computation, don't switch summation methods." Poincaré's concern; it was right.

**7. SIMD/parallel-reduction sentence added.**
New sentence in practitioners section: NumPy's pairwise guarantee is not a guarantee of bit-identical output across hardware, because reduction order varies with SIMD width and BLAS implementation. Added citation: Demmel & Nguyen (2015), "Parallel Reproducible Summation," IEEE TC. Poincaré's concern.

**8. 100,000 × 0.1 example identified as separate illustrative computation.**
In both the methodology section and the practitioners section: this is not one of the six study inputs; it is a degenerate case computed separately as illustration. Montaigne's concern was valid-a careful reader couldn't tell before.

**9. Synthetic data limitation quantified.**
Limitations section now argues from the ratio magnitude (10^-14) that no plausible seed variation could move the conclusion at n = 5,000. Replaces "should hold" with a quantitative argument. Montaigne's concern.

**10. n-scaling limitation flagged explicitly.**
New paragraph in Limitations notes that the flip threshold scales as 1/n; at small n the threshold rises and realistic summation errors could approach it. Proposes systematic n-sweep as follow-on. Poincaré's concern (partially addressed; experiment not run).

### Declined changes and reasoning

**Bayle concern 1: Kahan example finding is wrong.**
Declined. Bayle asserts `1 + 10^15` rounds to 10^15 (ULP ≈ 0.125), making the intermediate sum lossy. This conflates ULP spacing with representability. All integers up to 2^53 ≈ 9.0 × 10^15 are exactly representable in float64. The integer 10^15 + 1 is exactly 8 ULPs (of size 0.125) above 10^15-it is a representable value. The addition is exact. The empirical result is correct. The revised draft adds the 2^53 threshold explicitly to forestall this confusion in readers.

**Bayle concern 3: At least one real benign input required.**
Declined for this revision. Fetching real GHCN, yfinance, or CIFAR-10 data requires downloads or registrations outside the revision-pass scope. The limitation is now quantitatively argued rather than hand-waved, and real-data validation is named as a follow-on.

**Poincaré concern 3 / Bayle concern 5: n-sweep and cross-SIMD experiments.**
Declined for this pass; flagged in Limitations as follow-on work.

### Assessment of Bayle's major recommendation

Bayle rated this major. The most critical concern (the Kahan example) is a reviewer error. The remaining concerns are clarification-level. The "major" rating is respectfully declined; the piece required substantive clarifications, not structural revision.
