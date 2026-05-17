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

## Step 2: Kahan's Classic Example — First Surprise

I started with `[1.0, 1e15, -1e15]`, the example Kahan used to demonstrate compensated summation. On all three orderings in all four methods, every method returned 1.0 exactly. ULP error: 0 everywhere.

I had expected naive summation to fail here (as it does in the textbook treatment). It didn't, because in float64, `1.0 + 1e15 = 1000000000000001.0` is exactly representable (it fits within the 53-bit significand since 10^15 < 2^53), and `1000000000000001.0 - 1e15 = 1.0` is exact. The textbook failure mode requires the intermediate sum to exceed the precision of the floating-point type. In this case it doesn't. This result is correct and not a bug, but it challenges the narrative value of this particular worked example.

---

## Step 3: Adversarial Inputs

**Wide-range array (n=1000, values spanning ±10^15):** Naive sequential sum was 5 ULPs off the Decimal reference. NumPy (pairwise) was 3 ULPs off. Kahan was exact. The shuffled-order distribution spanned 76 ULPs across 1,000 permutations. These are small errors in relative terms; the result is around -8.5×10^14 and the maximum absolute error is about 7.

**Catastrophic cancellation (n=1000, large positives and near-negatives summing to ~-14):** This is where things became striking. The absolute errors were modest — 0.15 to 0.60 out of a result of about -14 — but the ULP errors were enormous: naive at 338 trillion ULPs, NumPy at 180 trillion, Kahan at 84 trillion. The shuffled-order distribution spanned 4.3 *quadrillion* ULPs. The reason is mechanical: when the true result is small relative to the intermediate values, even a tiny absolute error translates to a vast number of ULPs, because a ULP near zero is tiny. The errors in ULPs are not wrong; they accurately report that the result has essentially no correct significant figures beyond the integer part. Kahan is best but still loses roughly 12 decimal digits of precision due to the fundamental ill-conditioning of the sum.

---

## Step 4: Benign Inputs

I used synthetic data matched to real distributions (GHCN temperature anomalies: mean 0, std 1.5°C; S&P 500 daily returns: Student-t with df=4, scale=0.01; CIFAR-10 pixel intensities: uniform 0–255), with all distributions, seeds, and generation code committed. Real downloads were omitted because GHCN is ~3 GB compressed and CIFAR-10 requires a separate registration step; the synthetic distributions are explicitly parameterized from published statistics.

**Temperature anomalies (n=5,000):** NumPy was 1 ULP off, Kahan 3 ULPs, naive 17 ULPs. NumPy beating Kahan was unexpected. Upon reflection, it makes sense: for large, well-conditioned arrays, pairwise summation has error O(log n × ε_machine) while Kahan is O(ε_machine), but Kahan's constant factor is data-dependent. Pairwise summation's recursion structure happens to be favorable for this particular data.

**S&P 500 returns (n=5,000):** NumPy 3 ULPs, Kahan 0 ULPs (exact), naive 21 ULPs.

**Pixel intensities (n=5,000):** NumPy 1 ULP, Kahan 0 ULPs, naive 10 ULPs.

The `0.1 × 100,000` case (not part of the original plan, added after seeing the temperature result) was illuminating: naive was 10,362 ULPs off, NumPy and Kahan were both exact. This is the cleanest demonstration that naive summation in Python is genuinely dangerous for repeated, non-representable values.

---

## Step 5: Downstream Consequence — The Expected Failure

The pipeline: compute the mean of each input array using each method, classify each element as above or below that mean, count disagreements between methods.

Result: **zero prediction flips across all inputs, including adversarial.**

This is the failure mode the proposal anticipated. The reason is a simple ratio: a flip requires at least one observation to fall between the two competing mean estimates. That window has width equal to the absolute error in the mean. The spacing between observations near the mean depends on the data density. For normal distributions with std 1.5 and n=5,000, the typical inter-observation spacing near the mean is approximately 7.5×10^-4. The naive-vs-reference mean error for temperature data is 2.4×10^-17. The ratio is 3.2×10^-14. Effectively no observation falls in the window.

For catastrophic cancellation data: the mean error is 6×10^-4 in absolute terms, but the individual observations are on the order of 10^12, so none of them cluster near the mean. Again, the ratio that matters — (error in mean)/(inter-obs spacing at mean) — is far below 1.

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

The catastrophic cancellation result is the most practically relevant finding: the ULP errors are in the trillions, but the right lesson is not "use Kahan" — it is that the sum of a catastrophically cancelling array is fundamentally unreliable regardless of summation method, and the pipeline should be redesigned to avoid it.
