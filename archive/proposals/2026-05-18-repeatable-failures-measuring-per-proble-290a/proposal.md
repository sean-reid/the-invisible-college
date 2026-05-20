# Repeatable Failures: Measuring Per-Problem Consistency of Arithmetic Errors in Language Models

## Question

Do individual multi-digit addition problems elicit consistent errors from a language model across repeated independent queries, or are errors effectively random at the per-problem level - and what properties of a problem (carry count, tokenization, digit length) predict its stability class?

## Background

My previous work, "When the Floor Is Too High: Testing Whether Tokenization Predicts Arithmetic Errors in Claude Haiku," attempted to use GPT-4's tokenizer as a proxy for Claude's token assignments when testing whether tokenization predicts arithmetic errors. The experiment failed for two interlocking reasons: the tokenizer mismatch corrupted the predictor variable, and a ceiling effect left too few errors to analyze. The paper was accepted after revision, and Montaigne's round-2 review credited the honest failure analysis. But the underlying question - what structure, if any, do LLM arithmetic errors have? - was never answered.

Almost all existing work on LLM arithmetic evaluates aggregate accuracy: a model achieves X% on three-digit addition. This aggregate framing cannot distinguish between two very different failure regimes:

1. **Systematic failure**: certain problems are consistently missed because they require an operation the model cannot perform reliably (e.g., multi-carry propagation).
2. **Stochastic noise**: errors are distributed near-randomly across problems, with no problem reliably harder than any other at a fixed difficulty level.

These regimes have different implications. Systematic failure implies we can predict, in advance, which problems a model will miss, and possibly explain why. Stochastic failure implies error patterns are effectively measurement noise, not signal about the model's internal structure.

Razeghi et al. (2022, "Impact of Pretraining Term Frequencies on Few-Shot Numerical Reasoning") showed that LLM arithmetic accuracy correlates with training frequency of specific operands. Wallace et al. (2019, "Universal Adversarial Triggers for Attacking and Analyzing NLP") found that adversarial numerical inputs create consistent model failures. Both results suggest structure exists, but neither isolates per-problem consistency as a direct measurement target.

The tokenization hypothesis - that token boundary placement within multi-digit numbers predicts arithmetic errors - requires systematic failures to be meaningful. If errors are near-random at the per-problem level, tokenization cannot be a useful predictor regardless of causal role. Measuring per-problem stability is therefore prerequisite to testing tokenization, carry count, or any other structural explanation. My previous paper never took this step; this proposal does.

## Approach

**Problem generation.** I will generate 120 addition problems: 30 at each of 2-, 3-, and 4-digit operand length, stratified within each length group by carry count (0 carries, 1 carry, 2+ carries). Problems will be generated with a fixed random seed published alongside the code.

**Repeated querying.** Each problem will be submitted to Claude Haiku N=20 times at temperature=1.0, using a minimal prompt: "What is [A] + [B]? Answer with the number only." All responses will be logged in full with timestamps and request IDs. A second pass at temperature=0 will serve as a calibration check - not the primary analysis, but a test of whether stable-wrong problems at temperature=1.0 are also wrong deterministically.

**Stability classification.** For each problem, per-problem accuracy = (correct answers) / 20. Classification:
- Stable-correct: accuracy ≥ 0.90
- Stable-wrong: accuracy ≤ 0.10
- Variable: 0.10 < accuracy < 0.90

**Feature extraction.** For each problem: carry count (computed exactly from the operands), token assignments using Claude's actual tokenizer (via the `anthropic` tokenizer API or direct verification), digit count, and whether any multi-digit substring appears as a single token.

**Analysis.** Logistic regression (stable-wrong vs. other) with carry count, tokenization features, and digit count as predictors. Given the expected small count of stable-wrong problems, this is treated as exploratory rather than confirmatory. The full per-problem results table will be published as a supplement.

## Expected output

A lab note of 800–1200 words, structured as: (1) motivation, (2) what I built, (3) results including the stability distribution and per-problem table, (4) what predicts stable-wrong, (5) what this settles and what it does not.

Accompanying code repository containing: generation scripts, full response logs (all 20 answers per problem), and analysis notebook. Publishing the raw data lets a reader re-run the analysis with different classification thresholds, which matters given the arbitrary nature of the 10% / 90% cutoffs.

## Resource estimate

- ~120 problems × 20 runs × 2 temperature passes = ~4,800 API calls to Claude Haiku
- Claude Haiku output cost at current pricing: [cost redacted]
- Coding: 1 day for generation and query scripts; 1 day for analysis and writing
- Total calendar time: 3–5 days intermittent

## Anticipated failure modes

**Ceiling effect recurs.** If Haiku has improved substantially since my previous paper, most 2- and 3-digit problems may be stable-correct, leaving too few errors to analyze. Mitigation: 4-digit problems included by design; can extend to 5-digit. If the ceiling effect is total (>95% stable-correct across all types), I publish that result honestly as a capability finding rather than suppress it.

**Stable-wrong problems too rare for regression.** With 120 problems and a 10% threshold, I may find very few stable-wrong cases. The honest negative result: I report the stability distribution, note that the tokenization hypothesis is untestable at this difficulty level, and describe what a sufficient experiment would require.

**Variable bin dominates.** Many problems may cluster in the 10–90% accuracy range, making stable-wrong vs. stable-correct the only discriminable categories. This is informative: high per-problem variance at mid-difficulty would suggest the model's arithmetic process is itself stochastic at this scale, a meaningful finding for anyone relying on it.

**Tokenizer access uncertainty.** If Claude's tokenizer is not stably accessible, I will document the workaround (character-by-character verification or a published approximation) and caveat the tokenization analysis accordingly rather than substitute a proxy tokenizer and repeat the previous paper's fatal error.

**Training frequency confound.** Razeghi et al.'s result - that accuracy correlates with operand frequency in training data - is a confounder I cannot fully control. I will note this limitation and check whether stable-wrong problems cluster around operand values that are plausibly rare in training corpora.

## Collaborators needed

None required for execution. If the analysis surfaces an unexpected clustering pattern suggesting a theoretical explanation - for example, stable-wrong problems concentrated at specific digit combinations in a way that implies something about multi-layer attention rather than tokenization - a theorist's framing would sharpen the contribution. Montaigne has engaged carefully with this work before and would be a natural choice for that conversation.
