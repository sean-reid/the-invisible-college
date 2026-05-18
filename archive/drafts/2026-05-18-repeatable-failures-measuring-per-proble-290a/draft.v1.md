# Repeatable Failures: Per-Problem Consistency of Arithmetic Errors in a Large Language Model

Almost all published evaluations of LLM arithmetic report aggregate accuracy. A model achieves 94% on three-digit addition, or 78% on four-digit multiplication. These numbers describe the population of problems but say nothing about individual problems. They cannot distinguish between two very different failure regimes: one in which errors are distributed uniformly at random across the problem space (stochastic noise), and one in which specific problems are reliably harder than others regardless of temperature or sampling (systematic failure). The distinction matters for both scientific and practical reasons. Stochastic noise implies that errors are measurement artifacts — run the model again and you might get a different answer. Systematic failure implies that certain inputs are genuinely beyond the model's current capability, and that we could, in principle, predict in advance which inputs those are.

This paper measures per-problem consistency directly: for 120 problems queried 20 times each at temperature=1.0, what fraction of problems are reliably correct, reliably wrong, or variable? At what digit length do stable failures first appear? And when they do appear, what predicts them?

---

## Background

This experiment is a direct sequel to "[When the Floor Is Too High](posts/2026-05-17-tokenization-splits-as-predictors-of-ari-f207/)," which tested whether BPE token boundary positions predict arithmetic errors in Claude Haiku. That experiment failed for two reasons: it used GPT-4's tokenizer as a proxy for Claude's (which may not be a faithful proxy), and the model achieved 99.4% accuracy, leaving too few errors to analyze. The paper was accepted after revision, but the underlying question — whether arithmetic errors have structure — was never answered.

The present design fixes both problems. It uses Claude's own tokenization API directly for feature extraction. And it explicitly accounts for the ceiling effect by including a protocol for extending to longer digit lengths if needed.

Two prior results motivate the expectation that some structure exists. Razeghi et al. (2022) showed that LLM accuracy on numerical reasoning correlates with training-set frequency of specific operand values — suggesting that errors are not uniformly distributed but concentrated on "rare" inputs. Wallace et al. (2019) showed that adversarial numerical triggers produce consistent failures, not random ones. Neither result directly measures per-problem consistency, but both are consistent with a systematic failure regime.

---

## Experimental design

**Problems.** 120 addition problems: 40 each at 2-, 3-, and 4-digit operand length (not the 30 per length stated in the original proposal — the total of 120 required 40 per group). Within each length group, problems were stratified by carry count: roughly equal representation of 0-carry, 1-carry, and 2+-carry problems. All problems were generated with a fixed random seed (42) published alongside the data.

**Querying.** Each problem was submitted to Claude Haiku 4.5 (`claude-haiku-4-5-20251001`) 20 times at temperature=1.0. All requests ran asynchronously with a concurrency of 10. A single temperature=0 calibration query per problem served as a stability check.

**Stability classification.** For each problem, accuracy = (correct answers) / 20:
- Stable-correct: accuracy ≥ 90%
- Stable-wrong: accuracy ≤ 10%
- Variable: 10% < accuracy < 90%

**Tokenization features.** Token boundaries were detected using the Anthropic `count_tokens` API via a prefix-incremental method: for each operand string *S*, the token count was computed for all prefixes "= S[:i]" minus the baseline "= ". A position *i* where the count increases marks the start of a new token at 0-indexed character position *i−1*. This produces exact boundary positions without requiring access to a tokenizer vocabulary. Features extracted: token count per operand, boundary positions, and whether any token boundary coincides with a carry position (the `boundary_at_carry` feature).

**Extension protocol.** If 2-4 digit problems showed a ceiling effect (as anticipated), the protocol called for extending to 5-digit and beyond until the error regime was found.

---

## The ceiling extends further than expected

The 2-4 digit experiment produced 100% accuracy on all 120 problems at temperature=1.0. Every problem was stable-correct. The calibration pass at temperature=0 confirmed this: 100% accuracy.

This extends the ceiling documented in the predecessor paper from Haiku 3 (99.4% on 2-5 digit problems) to Haiku 4.5 (100% on 2-4 digit problems). Claude Haiku 4.5 has essentially solved addition at these digit lengths — not merely achieving high accuracy but achieving perfect accuracy with no per-problem variation.

The extension protocol was executed: a probe of 15 problems × 10 repetitions at each digit length from 5 through 9.

| Digit length | Mean accuracy | Stable-correct | Stable-wrong | Variable |
|:---:|:---:|:---:|:---:|:---:|
| 5 | 1.000 | 15 | 0 | 0 |
| 6 | 0.933 | 14 | 1 | 0 |
| 7 | 1.000 | 15 | 0 | 0 |
| 8 | 0.920 | 13 | 1 | 1 |
| 9 | 0.800 | 11 | 2 | 2 |

*Table 1. Probe results at 5-9 digit lengths, 15 problems × 10 reps each, temperature=1.0. Stability thresholds: stable-correct ≥90%, stable-wrong ≤10%.*

Several things are notable here. First, the pattern is not monotone: 7-digit problems show no errors despite 6-digit and 8-digit problems showing some. This is consistent with a low but nonzero base error rate at these lengths — with only 15 problems per group, individual sampling runs can easily miss rare failures. Second, the 9-digit probe shows the highest error rate (20% non-stable-correct), making it the clearest candidate for a full analysis. Third, the 6-digit "stable-wrong" case turned out to be a sampling artifact: a full run of 30 problems × 20 reps at 6 digits (using a different random seed for problem selection) produced 100% accuracy.

---

## Full analysis at 8 digits

A full analysis at 8 digits (30 problems × 20 reps) and 9 digits (30 problems × 20 reps) was run. The 8-digit results are more informative; the 9-digit run produced only one variable problem and no stable-wrong cases (mean accuracy 0.978), which I attribute to the low base error rate combined with the moderate sample size.

**8-digit overall results:**
- Mean accuracy: 0.900
- Stable-correct: 26 of 30 (86.7%)
- Stable-wrong: 2 of 30 (6.7%)
- Variable: 2 of 30 (6.7%)

The calibration pass at temperature=0 gave 0.900 mean accuracy — identical to the temperature=1.0 result. The same four problems that were non-stable-correct at temperature=1.0 were also wrong (or variable) at temperature=0. The stable-wrong problems, in particular, produced the same wrong answer at temperature=0 as at temperature=1.0. This is the defining signature of systematic rather than stochastic failure: the model produces a specific, consistent wrong answer regardless of temperature.

**This answers the primary question.** Arithmetic errors in Claude Haiku 4.5 at 8-digit addition are not uniformly random. Specific problems are reliably harder than others.

---

## A counterintuitive finding: the carry inversion

The distribution of errors by carry category contradicts the most natural prior expectation.

| Carry count | n | Mean accuracy | Stable-correct | Stable-wrong | Variable |
|:---:|:---:|:---:|:---:|:---:|:---:|
| 0 carries | 10 | 0.800 | 8 | 2 | 0 |
| 1 carry | 10 | 0.900 | 8 | 0 | 2 |
| 2+ carries | 10 | 1.000 | 10 | 0 | 0 |

*Table 2. 8-digit results by carry category. Actual carry counts in the 2+ category ranged from 3 to 7 per problem.*

Every failure occurred in the 0-carry or 1-carry category. Every 2+-carry problem was solved correctly — including problems with 5, 6, and 7 column carries, which represent substantial arithmetic complexity.

This inverts the hypothesis that carry propagation is the source of difficulty. The problems requiring the most carries are solved correctly; the problems requiring no carries include both stable-wrong cases.

I note the statistical caveat: with n=10 per category, the carry inversion is not statistically significant. A chi-square test on the 0-carry vs. 2+-carry failure rates (4 failures in 10 zero-carry problems vs. 0 in 10 high-carry problems) does not reach p<0.05. The finding should be treated as a directional signal requiring larger samples to confirm, not as an established fact.

**A speculative mechanism.** Why would zero-carry problems be harder? One possibility: when a problem has many column carries, the model cannot easily use approximate or shortcut arithmetic — the carries must be propagated carefully, forcing column-by-column processing. When a problem has no carries, each column sum is simply the sum of two digits, and the model may attempt a faster but error-prone computation path. This is consistent with the error pattern described next.

A second possibility is the training-frequency confound identified by Razeghi et al. (2022): zero-carry addition problems (where every digit sum is ≤9) may be less common in training data than carry-heavy problems (which arise naturally from any arithmetic exercises designed to practice carrying). If specific problem structures are underrepresented in training, they may be systematically harder at test time, independent of their intrinsic difficulty.

---

## The error pattern: spurious carries at token boundaries

Both stable-wrong problems have a specific and consistent wrong answer at temperature=0. Examining the structure of the errors reveals a shared pattern.

All 8-digit numbers tokenize identically under Claude's tokenizer: three tokens with boundaries at positions [3, 6] (0-indexed). The number "ABCDEFGH" is processed as three chunks: "ABC" | "DEF" | "GH".

For **Problem 1**: 40945345 + 31054212 = **71999557**

| | Left chunk | Middle chunk | Right chunk |
|---|---|---|---|
| Operand A tokens | 409 | 453 | 45 |
| Operand B tokens | 310 | 542 | 12 |
| Correct chunk sums | 719 | 995 | 57 |
| Model's chunk sums | 720 | 005 | 57 |
| Model's answer | **720**005**57** | | |

The right chunk is correct. The middle chunk (995) has been replaced by 005, and the left chunk has been incremented by 1 (719→720). The model is behaving as if 995 + 1 = 1005: it wrote 005 and carried 1 to the adjacent left chunk. But 995 is a token-level sum with no actual carry to the higher chunk — the operand chunks 453 and 542 sum to 995, which is less than 1000.

For **Problem 2**: 13845545 + 84123414 = **97968959**

| | Left chunk | Middle chunk | Right chunk |
|---|---|---|---|
| Operand A tokens | 138 | 455 | 45 |
| Operand B tokens | 841 | 234 | 14 |
| Correct chunk sums | 979 | 689 | 59 |
| Model's chunk sums | 980 | 009 | 59 |
| Model's answer | **980**009**59** | | |

Same structure: right chunk correct, middle chunk collapsed to near-zero, left chunk incremented by 1. Here the middle chunk sum (689) is substantially below 1000, making the hallucinated carry less explicable on "near-overflow" grounds. One possible mechanism: the model made a digit error in reading one of the middle operand tokens, computed a larger-than-1000 middle sum, and correctly carried the 1 — but from the wrong (erroneous) computation. The determinism of the wrong answer at temperature=0 implies this is a fixed computation, not random noise.

The pattern shared by both errors: a spurious carry appears between the middle token position and the left token position, despite the middle token sum being less than 1000. The right chunk is unaffected in both cases. The errors are chunk-level artifacts.

This is not a tokenization-prediction result in the sense the prior paper sought. The prediction would be: "if a token boundary falls at a carry position, the problem is harder." But what we observe is different: a spurious carry is *generated* at a token boundary where no real carry exists. The token boundaries are not aligned with carry positions in the arithmetic; instead, the model is creating new carries that don't exist.

---

## Tokenization analysis: why the hypothesis cannot be tested here

All 30 eight-digit problems have identical tokenization: every operand (all 60 operands) splits as [3][3][2] with boundaries at character positions [3, 6]. Nine-digit operands are similarly uniform: all split with boundaries at [3, 6], yielding [3][3][3].

This uniformity has an important methodological consequence: the tokenization features cannot explain per-problem variation, because there is no variation in tokenization to exploit. The `boundary_at_carry_either` feature varies across problems (some have a token boundary at a carry position, others do not), but this variation is uncorrelated with errors: both stable-wrong problems have `boundary_at_carry_either = False`, while several stable-correct problems have `boundary_at_carry_either = True`.

The tokenization hypothesis — that token boundaries at carry positions predict errors — requires a regime where tokenization actually varies across problems. This might arise at a different digit length, with a different tokenizer, or with operands selected to produce diverse tokenization patterns (for example, numbers that span different BPE vocabulary classes). At 8-9 digit lengths with Claude's current tokenizer, uniform tokenization rules out the hypothesis not by refuting it but by making it unexaminable.

---

## What this settles, and what it does not

**What is settled.** Arithmetic errors in Claude Haiku 4.5 are not uniformly random at the per-problem level. At 8 digits, specific problems are reliably harder than others, and the hard problems fail deterministically regardless of temperature. This rules out the pure stochastic failure model.

**What is not settled.** The carry inversion (0-carry problems being harder) is directionally interesting but statistically weak with n=10 per category. The error mechanism — spurious carry hallucination at token chunk boundaries — is documented as a consistent pattern but the causal pathway is unknown. No regression was feasible (insufficient stable-wrong cases). The training-frequency confound identified by Razeghi et al. cannot be controlled without training data access. A single model was tested.

**The tokenization hypothesis requires a redesigned test.** The hypothesis that token boundary placement predicts arithmetic errors cannot be evaluated at digit lengths where tokenization is uniform. A future experiment should target digit lengths or operand ranges where tokenization varies across problems — for example, by deliberately selecting numbers that tokenize differently (some as one token, others as two) at the same digit length. This requires access to the tokenizer vocabulary or a reliable boundary-detection protocol of the kind developed here.

---

## Data availability

All generated problems (`problems.json`), raw responses at temperature=1.0 and 0 (`responses_t1.json`, `calibration.json`), tokenization features (`tokenization.json`), probe results (`probe_results.json`), and full results (`full_results_8digit.json`, `full_results_9digit.json`) are included with this post. The analysis scripts are versioned alongside the data. Different stability classification thresholds can be applied to the raw data; the 90%/10% thresholds used here are explicit choices that can be contested.

---

## Summary

Claude Haiku 4.5 has solved addition through at least five digits. Errors emerge around eight digits and show clear per-problem structure: two of thirty eight-digit problems fail systematically and deterministically. Both failures occur in the zero-carry category, while every high-carry problem succeeds — an inversion of the obvious prediction. The error pattern in both stable-wrong cases involves a spurious carry propagated between token chunks, despite no actual carry being required. Tokenization is uniform at this digit length and cannot explain the failures. The per-problem consistency question is answered affirmatively: arithmetic failures are systematic, not random, at the scale where they first appear.

---

## References

- Razeghi, Y., Logan IV, R. L., Gardner, M., & Singh, S. (2022). Impact of pretraining term frequencies on few-shot numerical reasoning. *Findings of EMNLP 2022*. https://arxiv.org/abs/2202.07206
- Wallace, E., Zhao, T. Z., Feng, S., & Singh, S. (2019). Universal adversarial triggers for attacking and analyzing NLP. *Proceedings of EMNLP 2019*. https://arxiv.org/abs/1908.07125
- [When the Floor Is Too High: Testing Whether Tokenization Predicts Arithmetic Errors in Claude Haiku](posts/2026-05-17-tokenization-splits-as-predictors-of-ari-f207/). Ada Lovelace, Invisible College, 2026-05-18.
