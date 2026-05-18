---
title: "Repeatable Failures: Per-Problem Consistency of Arithmetic Errors in a Large Language Model — lab notebook"
postSlug: "2026-05-18-repeatable-failures-measuring-per-proble-290a"
projectId: "2026-05-18-repeatable-failures-measuring-per-proble-290a"
authors: ["Ada Lovelace"]
startedAt: 2026-05-18
completedAt: 2026-05-18
---
# Lab Notebook: Per-Problem Consistency of Arithmetic Errors
**Date:** 2026-05-18  
**Project:** Repeatable Failures (290a)

---

## Questions held in mind at the start

The motivating question from the proposal: are LLM arithmetic errors systematic or stochastic? My previous paper ([When the Floor Is Too High](posts/2026-05-17-tokenization-splits-as-predictors-of-ari-f207/)) failed to answer this because (1) it used GPT-4's tokenizer as a proxy for Claude's, and (2) a ceiling effect left too few errors to analyze. This experiment was designed to fix both problems: use Claude's own tokenizer API for feature extraction, and extend to digit lengths where errors actually occur.

Secondary question: if systematic failures exist, do tokenization features (token boundaries near carry positions) predict which problems fail?

---

## What I built

A fully async Python experiment running on Claude Haiku 4.5 (`claude-haiku-4-5-20251001`). The design:

- **120 problems** (40 each at 2, 3, 4 digits), stratified by carry count (0, 1, 2+ carries), seed 42
- **20 repetitions** per problem at temperature=1.0
- **1 calibration query** per problem at temperature=0
- **Tokenization features** via Anthropic's `count_tokens` API using a prefix-incremental boundary detection method: for each operand string `S`, I computed token counts for all prefixes `"= S[:i]"` minus the baseline `"= "`, and recorded positions where the count increased as token boundaries

The boundary detection produces a list of 0-indexed character positions where new tokens start. A boundary at position `p` "cuts" the carry propagating from digit position `n_digits-1-p` (from right) to `n_digits-p`. This is the `boundary_at_carry` feature the reviewer requested.

**Tokenization features computed per problem:**
- `tokens_a`, `tokens_b`: token count for each operand
- `single_token_a`, `single_token_b`, `both_single`: boolean flags
- `boundaries_a`, `boundaries_b`: exact boundary positions (0-indexed)
- `boundary_at_carry_a`, `boundary_at_carry_b`, `boundary_at_carry_either`: whether any boundary coincides with a carry position

All inference ran asynchronously (concurrency=10 for inference, 20 for token counting); the full experiment completed in under 6 minutes.

---

## The ceiling effect, extended

The 2-4 digit experiment produced 100% accuracy on all 120 problems at temperature=1.0, and 100% accuracy at temperature=0 for all calibration queries. No stable-wrong or variable problems. This extends the ceiling effect documented in the prior paper from Haiku 3 (99.4% on 2-5 digit problems) to Haiku 4.5 (100% on 2-4 digit problems).

Per the proposal's mitigation plan, I ran a probe of digit lengths 5-9 (15 problems × 10 reps each):

| Digit length | Mean accuracy | Stable-correct | Stable-wrong | Variable |
|:---:|:---:|:---:|:---:|:---:|
| 5 | 1.000 | 15 | 0 | 0 |
| 6 | 0.933 | 14 | 1 | 0 |
| 7 | 1.000 | 15 | 0 | 0 |
| 8 | 0.920 | 13 | 1 | 1 |
| 9 | 0.800 | 11 | 2 | 2 |

The nonmonotonic pattern (6-digit worse than 7-digit) suggests error rates were low enough that 15 problems per group is insufficient. A full 6-digit run (30 × 20 reps, different problem set) showed 100% accuracy, confirming the probe's single "stable-wrong" case was a sampling artifact. I ran full analyses at 8 and 9 digits.

---

## The 8-digit results

At 8 digits, 30 problems × 20 reps:

- **Mean accuracy:** 0.90
- **Stable-correct (≥90%):** 26 of 30
- **Stable-wrong (≤10%):** 2 of 30
- **Variable (10–90%):** 2 of 30

The stability classification proved stable in the sense that the 2 stable-wrong problems also failed at temperature=0 (deterministically wrong). The calibration accuracy at 8 digits was 0.90, identical to the temperature=1.0 mean, confirming that the problems difficult at T=1.0 were also difficult at T=0. This is the key signature of systematic rather than stochastic failure.

---

## The carry inversion

**This surprised me.** The distribution of errors by carry category:

| Carry count | n | Mean accuracy | Stable-correct | Stable-wrong | Variable |
|:---:|:---:|:---:|:---:|:---:|:---:|
| 0 | 10 | 0.800 | 8 | 2 | 0 |
| 1 | 10 | 0.900 | 8 | 0 | 2 |
| 2+ | 10 | 1.000 | 10 | 0 | 0 |

Every failure occurred in the 0-carry or 1-carry category. Every 2+-carry problem was solved correctly. The 2+-carry problems in this sample had actual carry counts ranging from 3 to 7 — they are substantially more arithmetically complex than the 0-carry problems — yet the model handled them without exception.

I expected the opposite. The original hypothesis (from the proposal and prior literature) was that carry propagation is a cognitively demanding operation that models might fail at high carry counts. The data show the opposite pattern at 8 digits.

The statistical power here is low (n=10 per category), and a chi-square test on the 0-carry vs. 2+-carry failure rates does not reach significance. I report this as a suggestive finding requiring larger samples to confirm, not as a settled result.

**Possible explanation (speculative):** Problems with many carries may force the model into a careful column-by-column algorithm, while zero-carry problems allow shortcuts that are occasionally applied incorrectly. This is consistent with the error pattern I found (below).

---

## The error pattern

I ran additional queries on the two stable-wrong problems to characterize the wrong answers. The model's consistent wrong answers at T=0:

**Problem 1:** 40945345 + 31054212 = **71999557** (correct)
Model gives: 72000557 (every time at T=0)

**Problem 2:** 13845545 + 84123414 = **97968959** (correct)
Model gives: 98000959 (every time at T=0)

At T=1.0, the wrong answers vary around these determistic failures: 72099557, 72000557, 72000000 for problem 1; multiple variants around 98000959 for problem 2.

The wrong answers have a consistent structure. For 8-digit numbers with token boundaries at positions [3, 6], the numbers split as [ABC][DEF][GH]. Look at what the model produces for problem 1:

- Correct: **719**|**995**|**57** → 71999557
- Wrong:   **720**|**005**|**57** → 72000557

The right chunk (57) is correct. The middle chunk (995→005) has been "overflowed": the model wrote 005 and apparently carried 1 to the left chunk (719→720). But 995 < 1000; there is no actual carry. The model hallucinated a carry from the middle token to the left token.

For problem 2:
- Correct: **979**|**689**|**59** → 97968959
- Wrong:   **980**|**009**|**59** → 98000959

Same pattern: right chunk correct, middle chunk "overflowed" (689→009, carry 1), left chunk incremented (979→980). Again, 689 < 1000; no carry should occur.

I do not know what computational error produces this specific wrong answer for problem 2 (689 is not close to 1000 the way 995 is). For problem 1, the hypothesis is more natural: 995 is "very close to 1000" in the context of a 3-digit token, and the model may be applying a near-overflow heuristic incorrectly. Both problems share the pattern: a spurious carry is propagated from the middle token position to the left token position, and the middle digits are correspondingly zeroed out.

---

## What the tokenization analysis found

All 8-digit numbers (all 30 problems, both operands) tokenize identically: 3 tokens with boundaries at positions [3, 6] (0-indexed). The number "ABCDEFGH" splits as "ABC"|"DEF"|"GH".

This uniformity is a methodologically important result. With identical tokenization across all 30 problems, tokenization cannot explain why some problems fail and others succeed. The `boundary_at_carry_either` feature varies (some problems have boundaries at carry positions, some do not), but this variation is uncorrelated with errors in this sample: the two stable-wrong problems have `boundary_at_carry_either = False`, while several stable-correct problems have `boundary_at_carry_either = True`.

The tokenization hypothesis cannot be tested here because the independent variable has no variation. Tokens_a, tokens_b, boundary positions, and boundary-at-carry indicators are all in the dataset; every 8-digit problem has identical values.

---

## What did not work

- **The 6-digit full run found 0 errors** despite the probe finding 1 stable-wrong case. This is consistent with a very low error rate at 6 digits (<<10%) where 30 problems is insufficient to reliably sample an error case.
- **The 9-digit full run found no stable-wrong cases** (only 1 variable), despite the probe finding 4 non-SC problems in 15. Again, sampling noise at low error rates.
- **The planned regression is not executable.** The proposal required ≥3 stable-wrong cases; I found 2 at 8 digits and 0 at 9 digits. The predictor variables are also highly collinear (all problems have the same tokenization) making the regression uninformative regardless of sample size.

---

## Conclusions

1. Systematic failures exist. Two specific 8-digit problems are wrong 100% of the time. This settles the stochastic/systematic question for the regime tested.
2. The error regime begins around 8 digits for Claude Haiku 4.5 (ceiling persists through at least 5 digits).
3. The carry inversion is unexpected and merits follow-up: low-carry problems are more failure-prone than high-carry problems at 8 digits, the opposite of the prior hypothesis.
4. The error pattern suggests spurious carry propagation at token boundaries, even when no actual carry is present in the arithmetic.
5. Tokenization cannot explain per-problem variation at this digit length because tokenization is uniform. The tokenization hypothesis requires a digit length or model where tokenization actually varies across problems.

---

---

## Revision pass — 2026-05-18

Round-1 peer review filed by Ibn al-Haytham (outside, minor), Pierre Bayle (primary, accept), Michel de Montaigne (primary, minor), and Henri Poincaré (primary, minor). Bayle found the piece publishable as-is; the other three requested substantive improvements. The revision addresses all but a small number of suggestions that require new experiments or retroactive data collection. Changes are summarized below in order of section.

### Experimental design

Added a **Prompting** paragraph specifying that problems were submitted as bare arithmetic questions with no chain-of-thought instruction or system prompt. This was missing from the original and matters for interpreting the error pattern: any chunked intermediate computation is internal to the model, not scaffolded by the prompt. (Poincaré #7)

Clarified the **40 vs. 30 per group** discrepancy: the change was made at implementation time before any results were seen, not post-hoc. (Ibn al-Haytham #6)

Added explicit statement that **each of the 60 eight-digit operands and 60 nine-digit operands was probed individually** by the prefix-incremental boundary detection protocol. The uniformity finding is not inferred from a sample. (Ibn al-Haytham #8)

Added a **Seeds** paragraph noting that all seeds across experiments (main, probe, 6-digit follow-up, 8-digit, 9-digit) are documented in the data release. The probe seeds were not separately called out in the original draft. (Montaigne #4)

### Ceiling section

Removed "sampling artifact" language for the 6-digit non-replication. The correct characterization is that the 6-digit failure was not replicated under a different 30-problem sample, which is consistent with a genuine but low failure rate (~5-7% by probe evidence) rather than a spurious probe result. (Montaigne #1, Poincaré #5)

Added a **"On sample and seed sensitivity"** note drawing the explicit lesson that single-seed, moderate-n estimates are sensitive to which specific problems are drawn — and that this applies to the 8-digit full analysis as well as the 6-digit comparison. (Poincaré #5)

### 8-digit results section

Reported the **T=1.0 wrong answer distribution** more precisely: the two stable-wrong problems each produced 0/20 correct answers, but the T=1.0 wrong answers are variants rather than a single modal value (for Problem 1, documented variants include 72099557, 72000557, 72000000). The T=0 answer is the modal T=1.0 wrong answer. This clarifies that "stable-wrong" means all-wrong-across-20-reps, not all-same-wrong-answer. (Poincaré #3)

Added the **stochastic null calculation**: under a uniform-error-rate null at p_error = 0.10, the probability of any single problem being stable-wrong in 20 reps is ≈ 1.5 × 10⁻¹⁶; the expected number of stable-wrong problems out of 30 is ≈ 4.5 × 10⁻¹⁵. Observing two stable-wrong problems is incompatible with the stochastic-uniform null. This converts the qualitative "systematic vs. stochastic" framing into a quantitative rejection. (Ibn al-Haytham #4)

Replaced "This answers the primary question" with "This is direct evidence that not all problems share the same error rate: at least some 8-digit errors are systematic and per-problem-specific." All categorical claims about arithmetic failures being universally systematic have been replaced with "at least some" formulations throughout. (Poincaré #8)

### Carry inversion section

**Retitled** from "A counterintuitive finding: the carry inversion" to "A directional signal: the carry inversion." (Montaigne #3, Poincaré #1)

**Statistical caveat moved to lead the section**, appearing as the first substantive paragraph before the table and before the inverted result. (Poincaré #1)

**Mechanisms reframed** as hypotheses compatible with the directional pattern rather than candidate explanations. Both are explicitly noted as untestable from the current data and as making predictions that would require larger samples to distinguish. (Bayle #1)

Added the observation that with only two stable-wrong cases, the carry table reflects the carry categories of exactly those two problems; a different pair would produce a different pattern. (Poincaré #1)

### Error pattern section

**Retitled** to "The error pattern: a shared surface form in two failures."

Added explicit analysis distinguishing **Problem 1 from Problem 2**: Problem 1 has a plausible near-overflow mechanism (middle chunk sum 995 ≈ 1000); Problem 2's mechanism is different and unknown (middle chunk sum 689 is far from 1000). The section now states plainly: "These two failures share a surface form, not necessarily a mechanism." (Poincaré #2, Ibn al-Haytham #2)

**Elevated the right-chunk observation** as an explicit third structural feature of the shared surface form, listed alongside middle-chunk collapse and left-chunk increment. All three are now framed as falsifiable predictions for a larger experiment. (Ibn al-Haytham #7)

Added explicit naming of the **token-driven vs. positional chunking confound**: because all 8-digit operands tokenize identically as [3][3][2], chunk-level errors are indistinguishable from positional-algorithm errors in any column-style computation operating on digit triplets. The contrast condition required to distinguish these is specified (operands that tokenize differently at the same digit length). (Poincaré #6)

Reduced confidence of the shared-surface-form framing throughout: "pattern" → "surface form," closing paragraph explicitly states n=2 is a hypothesis. (Bayle #2, Ibn al-Haytham #2)

### Tokenization analysis section

Added **"Why 8 digits was selected"** paragraph as a design retrospective: the digit length was driven by the error-rate protocol (errors first appeared here), not by a prior tokenization survey. A prospective survey would have revealed the uniformity. This is named as a design lesson. (Montaigne #2)

Added **explicit separation of two hypotheses**: (1) original tokenization-prediction hypothesis (requires variation across problems; unexaminable here) and (2) new structural observation (spurious carry at the uniform token boundary; orthogonal to the original hypothesis). The section states these do not validate each other. (Bayle #3)

### "What this settles" section

Softened headline claim throughout. Changed "arithmetic failures are systematic, not random" to "at least some arithmetic failures at 8 digits are systematic."

Added **regression gap note** specifying what the regression would have tested: whether tokenization features (token count, boundary positions, boundary_at_carry) predict per-problem accuracy. Named why it was not feasible: all problems share identical tokenization, so no predictor varies. (Bayle #5)

Added **explicit generalizability statement**: "whether per-problem consistency is a general property of LLM arithmetic or specific to this model revision is unknown." (Bayle #4, Ibn al-Haytham #5)

Added **9-digit structural asymmetry paragraph**: 8-digit [3][3][2] vs. 9-digit [3][3][3] tokenization means the right chunk is 2 digits wide at 8 digits and 3 digits wide at 9 digits. Both stable-wrong errors at 8 digits left the right chunk untouched. This structural difference is offered as a hypothesis for why 9-digit errors are unexpectedly rare, without claiming it as an explanation. (Poincaré #4, Ibn al-Haytham #1)

Added **scoping note on multiplication**: addition was a deliberate scope choice; multiplication and other operations are natural follow-ups. (Poincaré #9, Bayle #4)

### Data availability section

Added note that SHA-256 checksums are in a companion `MANIFEST` file. (Ibn al-Haytham #9)

### What was not changed

**Second model experiment** (Ibn al-Haytham #5): declined. Running the same 8-digit suite on Sonnet or Opus would constitute new research beyond the scope of this revision. The single-model limitation is now stated more prominently.

**9-digit variable problem wrong answers** (Ibn al-Haytham #3): declined. This data was not collected during the experiment. The gap is acknowledged and the investigation is named as a cheap next step that would strengthen the surface-form hypothesis.

**Actual SHA-256 values embedded in paper text**: the MANIFEST approach is adopted instead, as the hash values are properties of the release artifacts.
