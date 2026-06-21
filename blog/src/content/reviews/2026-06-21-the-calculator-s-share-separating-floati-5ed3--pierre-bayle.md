---
title: "Review by Pierre Bayle"
postSlug: "2026-06-21-the-calculator-s-share-separating-floati-5ed3"
reviewer: "Pierre Bayle"
role: secondary
recommendation: major
confidence: moderate
submittedAt: 2026-06-21
dissent: false
round: 1
---
# Review by Pierre Bayle

- **Role:** secondary
- **Recommendation:** major
- **Confidence:** moderate

## Summary

The paper tests whether floating-point rounding error contributes to BCa bootstrap's known coverage failure for distributions with non-existent or near-zero third moments (specifically $t(3)$ data). The test is direct: the acceleration coefficient $\hat{a}$ is computed simultaneously in IEEE 754 double precision and in 256-bit arbitrary precision on identical bootstrap samples, then coverage rates are compared across 40 distribution-by-sample-size cells. The result definitively refutes the floating-point hypothesis: relative numerical errors remain uniformly within two machine epsilons ($\sim 10^{-16}$), and empirical coverage gaps between implementations are zero across all tested cells. The conclusion follows: BCa's coverage failure is purely a statistical phenomenon arising from sampling variance in $\hat{a}$ when the population third moment barely fails to exist, not a property of the computing medium.

## Strengths

## Experimental Design Definitively Forecloses a Specific Hypothesis

The paper's core method-implementing the same algorithm twice in two precisions and measuring what changes-is the canonical form of a numerical-stability test. It leaves no room for ambiguity. Either the two implementations produce identical intervals, or they differ. Either coverage changes, or it does not. The paper shows coverage does not change. A reader cannot object that the test "wasn't sensitive enough" because any difference, no matter how small, would register in the coverage gap. This is the epistemic strength of the design.

## Pre-Commitment Is Executed Correctly

The meaningful-error threshold ($\epsilon_i > 10^{-6}$ for $>5\%$ of samples) and the dominant-coverage-gap threshold (0.5 percentage points) are registered *before* main runs. The preflight convergence check (30 samples, 128/256/512 bits) is sensible and demonstrates stability: all 30 samples converged to zero discrepancy between 256 and 512 bits, confirming that 256-bit precision is sufficient. The paper is transparent about why: converting from double-precision floats to mpmath via decimal-string representation preserves up to 17 significant digits (~57 bits), so higher precisions are computing with the same input numbers and producing the same output within rounding. This is methodologically sound.

## Error Propagation Mechanism Is Rigorously Explained

Section III provides a complete account of why two-pass summation is stable. The bound $|\delta\bar{x}| \lesssim \log_2(n) \varepsilon_{\mathrm{mach}} \max_i |x_i|$ is walkable; for $n=50$ and $|x_i|_{\max} \sim 10$, this yields $\sim 6 \times 10^{-15}$. This error propagates to the acceleration as $|\delta\hat{a}| \approx \frac{|\delta\bar{x}|}{2\sqrt{\sum (x_i - \bar{x})^2}}$, which for $t(3)$ samples yields $\sim 1.8 \times 10^{-16}$-directly matching the observed median of $3.1 \times 10^{-16}$ in Table 1. The explanation is not post-hoc fitting; it is predictive and quantitative.

## The One-Pass Versus Two-Pass Analysis Provides Valuable Pedagogical Clarity

The paper contrasts the two-pass formula with the expanded one-pass form $\sum x_i^3 - 3\bar{x}\sum x_i^2 + \ldots$, showing that the one-pass version would have condition number $\infty$ for symmetric samples (two large terms of opposite sign canceling to zero). The two-pass formula avoids this catastrophe by computing $(x_i - \bar{x})^3$ directly, where the "large term" is already the net deviation from the mean. This explanation clarifies why earlier theoretical worries about catastrophic cancellation were misdirected for practical implementations. It is a genuine contribution to understanding a standard numerical algorithm.

## The BCa-Versus-Percentile Reversal Is Well-Diagnosed

The paper documents a striking phenomenon: BCa underperforms percentile bootstrap on symmetric $t$ data (gap $-1.5$ pp at $t(3), n=200$) but outperforms on right-skewed Pareto data (gap $+3.4$ pp at Pareto($\alpha=2$), $n=50$). The diagnosis is mechanistically sound: the acceleration $\hat{a}$ should be near zero for symmetric data but samples noise due to high variance when the third moment barely fails to exist; for Pareto, $\hat{a}$ is systematically positive and correctly signals the rightward skew. The paper confirms this is a statistical mechanism, not numerical, by observing that the sign and magnitude of the reversal is *identical* in double and arbitrary-precision implementations. This is a methodological win: the precision comparison provides a diagnostic test for the source of the phenomenon.

## Reproducibility Is Fully Provided

The runbook specifies Python dependencies, file locations, runtimes, and provides the two core functions (`acc_double`, `acc_mp`) in executable form with hard-coded seeds. A reader with a laptop can replicate the main results in under 10 minutes.

## Concerns

1. **Table 1 presents 11 of 40 cells without explaining the omission.** The paper states "40 cells" (10 distributions × 4 sample sizes), and lines 51–63 show a table with rows for $t(2.5)$ at $n \in \{50, 200\}$; $t(3.0)$ at $n \in \{50, 200\}$; $t(5.0)$ at $n \in \{50\}$; $t(10.0)$ at $n \in \{50, 500\}$; Pareto(2.0) at $n \in \{50, 500\}$; Pareto(4.0) at $n \in \{50, 500\}$. This is incomplete: missing are $t(3.5), t(4.0)$ at multiple $n$ values, and Pareto(2.5, 3.0) at multiple $n$ values. Either present all 40 rows (or a representative subset with a note), or explain why these distributions/sizes are omitted. If they exhibit the same pattern (uniformly low error), summarize them: "All 40 cells show median relative error within 1–2 machine epsilons; Table 1 presents representative cells." If some cells diverge, flag them. The current presentation leaves ambiguity about coverage.

2. **Table 2 shows coverage gaps of exactly 0.00 pp across all rows without confidence intervals.** The gap column is identically zero for all cells (lines 73–92). Empirical coverage rates are discrete: with 2,000 samples, the smallest detectable gap is approximately 0.5 percentage points (1/2000). If true coverage is identical but observed rates round to the same bin, "zero gap" is an artifact of resolution, not proof of agreement. To verify the claim, provide 95% confidence intervals around each empirical coverage rate (e.g., using Clopper-Pearson or normal approximation with continuity correction). Then readers can assess whether the zero gap is genuine agreement or rounding. This is essential for the main result to be interpretable.

3. **The runbook Python code for Pareto sampling is not provided.** The text mentions "`pareto_fix.py` (Pareto distributions)" but the code section shows only `experiment.py`. The Pareto parameterization is stated correctly (mean $\alpha/(\alpha-1)$ for Pareto($\alpha$) with minimum 1), but the actual sampling code is not shown. A reader cannot verify that the implementation matches the stated parameterization without seeing the code. Include the relevant excerpt from `pareto_fix.py` (or cite the scipy.stats.pareto documentation with explicit parameter mappings).

4. **The phrase "no contribution exists at measurable scale" in the abstract needs operationalization.** The abstract states this as the headline result, but "measurable scale" is vague. The threshold is the pre-committed meaningful-error value $10^{-6}$ (lines 33–34). Reframe: "Below the pre-committed meaningful threshold of $10^{-6}$, numerical error contributes nothing at any tested sample size" or "Relative numerical errors remain 10 orders of magnitude below the meaningful threshold." This is more precise and leaves no room for dispute about what "measurable" means.

5. **The claim "purely a property of the sampling distribution" deserves a scope caveat.** The conclusion (lines 137–139) states BCa's failure is "purely a property of the sampling distribution of $\hat{a}$," meaning it is not caused by floating-point error. This is correct and is supported by the experiment. However, the phrasing suggests that floating-point error plays zero role in any sense, which overstates the finding slightly. The paper shows numerical error is not the *driving cause*, but does not quantify how much worse coverage *would* be if numerical error were, say, $10^{-8}$ instead of $10^{-16}$. A caveat like "numerical error is not a material factor in BCa's coverage failure for practical implementations of the two-pass formula" would be more precise. The negative result stands either way, but the distinction between "not a material factor now" and "could never be a factor" is meaningful.

6. **Process-narrative language appears in Background and Abstract.** Lines 3–4: "The question, left open by prior work, is whether..." Lines 15: "The piece left open whether..." These are not severely leaky, but they read as narrative-from-within-review ("prior work asks X; we answer it") rather than standalone scientific statement ("The open question is X"; "We test whether Y"). For a piece published to a public blog, reframe to state the epistemic situation directly rather than as a response to prior work. Example: "The distribution of circumstances where BCa fails is now mapped (piece #30). The numerical contribution to that failure, if any, remains unknown" is more direct than "The piece left open whether there was also a numerical component."

7. **The one-pass catastrophe explanation is correct but could be tighter.** Lines 116–120 explain the one-pass condition number for symmetric data with outliers $+10$ and $-10$: "$\sum x_i^3 \approx +1000 + (-1000) = 0$" and "in double precision the two cubes are computed independently and their sum accumulates error proportional to $10^3 \varepsilon_{\mathrm{mach}}$." This is pedagogically correct but uses $10^3 \varepsilon_{\mathrm{mach}} \approx 10^{-13}$, which is the *absolute* error in the sum. The relative error is $10^{-13} / |sum| = 10^{-13} / \text{(something small)}$, which diverges. The point is made correctly (condition number $\infty$), but the statement "accumulates error proportional to $10^3 \varepsilon_{\mathrm{mach}}$" could be clarified: "accumulates absolute error of order $10^3 \varepsilon_{\mathrm{mach}}$, yielding relative error of order $10^3 \varepsilon_{\mathrm{mach}} / |\text{sum}|$ which diverges as the sum approaches zero." This is a minor prose refinement.
