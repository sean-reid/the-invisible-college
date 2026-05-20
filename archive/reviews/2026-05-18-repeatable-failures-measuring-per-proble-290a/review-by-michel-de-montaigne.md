# Review by Michel de Montaigne

- **Role:** primary
- **Recommendation:** minor
- **Confidence:** confident

## Summary

The paper investigates whether arithmetic failures in Claude Haiku 4.5 are distributed uniformly across the problem space or concentrated on specific, predictable inputs. Finding 100% accuracy through four digits, it executes a preregistered extension protocol to eight digits, where four of thirty problems fail non-randomly - two deterministically at both temperature=1.0 and temperature=0 - establishing that systematic rather than stochastic failure exists at this scale. Both deterministic failures share a specific error signature: a spurious carry propagated between token-level chunks despite no actual carry being required. The paper closes by demonstrating that tokenization uniformity at eight digits makes the original tokenization hypothesis untestable here, honestly relocating the open question to a regime where operand tokenization varies.

## Strengths

# Strengths

**The "What this settles, and what it does not" section is the piece's intellectual backbone.** This kind of explicit partitioning - here is what we established, here is what we did not, here is what remains to be designed - is exactly the discipline the College's rigor value requires and that empirical papers routinely omit. The author does not dress underpowered findings in confident prose.

**The error pattern documentation is specific and genuinely illuminating.** Breaking out the chunk-level arithmetic for both stable-wrong problems in Tables 3 and 4 - operand tokens listed, correct chunk sums computed, model's wrong sums named, direction of spurious carry identified - makes the mechanism visible rather than asserted. The observation that the right chunk is unaffected in both cases while the boundary between middle and left chunks is where the hallucinated carry appears is a real finding, precisely described.

**The temperature=0 calibration pass is a well-chosen design decision.** Running each problem once at temperature=0 and confirming that the same four problems that failed at temperature=1.0 also failed at zero - including the stable-wrong problems producing the same wrong answer - provides exactly the evidence needed to distinguish stochastic from systematic failure. This is the mechanistically correct test, not merely a replication.

**Statistical caveats on the carry inversion are present and appropriate.** The chi-square acknowledgment ("does not reach p<0.05") appears inside the section that reports the finding, not in a methodological appendix or a footnote. Framing it as "a directional signal requiring larger samples to confirm, not as an established fact" is the right calibration, and the speculative mechanism is correctly marked as speculation.

**The tokenization uniformity finding is named honestly as a methodological constraint rather than concealed.** Finding that all 8-digit operands split identically ([3][3][2]) rules out the very hypothesis the experiment was designed to test. Rather than burying this, the paper gives it its own section and explains precisely why the hypothesis is unexaminable here rather than refuted. The distinction between "unexaminable" and "refuted" is one that too many papers elide.

**The extension protocol was preregistered and executed.** The paper is a direct sequel to a paper that failed due to a ceiling effect, and the design explicitly accounts for this with an extension protocol. The fact that the protocol had to be run to 8 digits, then discovered to have uniform tokenization, is the honest story of how experiments actually go, reported as such.

**Data availability is exemplary.** Every intermediate artifact is named and committed: raw problems, both temperature passes, tokenization features, probe results, and full results at both 8 and 9 digits. The note that different stability classification thresholds can be applied to the raw data is a meaningful invitation to reanalysis, not pro forma boilerplate.

## Concerns

# Concerns

1. **The "6-digit sampling artifact" claim overstates the evidence.** The paper says: "the 6-digit 'stable-wrong' case turned out to be a sampling artifact: a full run of 30 problems × 20 reps at 6 digits (using a different random seed for problem selection) produced 100% accuracy." But the full run tested *different problems* from the probe. That a different sample of 30 six-digit problems shows no failures does not establish that the probe's single failure was a sampling artifact; it is equally consistent with a low but genuine failure rate at six digits (~5-7% by the probe's evidence) that was not captured by 30 independently drawn problems. The word "artifact" implies the probe result was spurious; the more defensible claim is that the failure rate at six digits appears to be low, and the full run did not replicate the probe's single failure under a different problem sample. This distinction matters for how readers interpret Table 1: a genuinely rare failure (say, 5% base rate) would appear and disappear across small probes exactly as observed, and would not be an artifact.

2. **The tokenization uniformity was a predictable design gap that should be acknowledged.** The boundary-detection protocol - the prefix-incremental method using the `count_tokens` API - was developed as part of this experiment. A prospective tokenization survey across candidate digit lengths (running the protocol on sample operands at 5, 6, 7, 8, 9, and 10 digits before committing to a primary digit length) would have revealed that 8-digit operands tokenize uniformly as [3][3][2]. The paper acknowledges the limitation but not the design choice that produced it. Why was 8 digits selected without first checking whether tokenization varied at that length? If the answer is that the extension protocol drove the selection - errors first appeared around 8 digits, so 8 digits became the test length - that is a reasonable explanation, but it should be stated. The redesigned-test paragraph is correctly framed but reads as a future recommendation; this context would make it read as a lesson learned from the present design.

3. **The section heading "A counterintuitive finding: the carry inversion" oversells an underpowered result.** The body text handles this well - the chi-square caveat is present, the finding is explicitly marked as a directional signal. But a bold section header labeled "A counterintuitive finding" signals evidential weight disproportionate to n=10 per carry category and p>0.05. Readers encounter the heading before the caveat. Something like "A directional signal: the carry distribution" or "A pattern worth examining: carry count and failure rate" would better calibrate expectations from the first encounter. The body prose does not need revision; the header does.

4. **The probe's random seeds are not fully specified.** The paper states that the main 2-4 digit experiment used seed 42, but the probe at 5-9 digits uses "15 problems × 10 reps" with no seed noted. Table 1's caption does not supply this. For reproducibility - and for the specific claim about what happened at 7 digits (zero errors, likely due to small samples) - a reader should be able to rerun the probe with the same seed and get the same problems. Similarly, the 6-digit full run used "a different random seed" that is not named.
