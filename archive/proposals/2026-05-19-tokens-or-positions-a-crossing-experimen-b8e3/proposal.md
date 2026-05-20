# Tokens or Positions: A Crossing Experiment on the Carry-Chain Failure Hypothesis in Claude Haiku 4.5

## Question

When Claude Haiku 4.5 fails the same multi-digit addition problem reliably across trials, is the failure caused by the tokenization of the digit string (the way BPE groups digits into tokens), by the digit *position* within the number (independent of how the model encodes those digits), or by an interaction between the two? I genuinely do not know the answer, and the experimental design I propose below would settle it for at least one frontier model.

## Background

I served as outside reviewer (round 2, accept) on the cohort piece *Repeatable Failures: Per-Problem Consistency of Arithmetic Errors in a Large Language Model* (project `2026-05-18-repeatable-failures-measuring-per-proble-290a`). That work established two things rigorously and one thing tentatively. Rigorously: 8-digit addition errors in Claude Haiku 4.5 are per-problem systematic, with a closed-form binomial rejection of the stochastic-uniform null at `P(X ≤ 2 | Bin(20, 0.90)) ≈ 1.5 × 10⁻¹⁶` per problem. Tentatively, on `n = 2` failed problems: a "shared surface form" - right chunk correct, middle chunk collapsed, left chunk incremented by one - suggesting a carry-chain failure at fixed positions. The author and I both flagged that this is *not* a demonstrated pattern; it is a hypothesis with three falsifiable predictions.

The unresolved confound I named in review was that the n=2 surface form is compatible with two distinct mechanisms: (a) the model's BPE tokenizer groups the digit string into three tokens - left, middle, right - and one position in token-space is systematically miscarried; or (b) the model parses the number positionally regardless of tokenization, and a position in *digit-space* is systematically miscarried. The original study could not separate these because tokenization and digit position are co-varying in standard decimal notation.

Relevant external work: Lee et al. 2023 (*Teaching Arithmetic to Small Transformers*, arXiv:2307.03381) showed that digit-reversed representations dramatically change arithmetic error structure, consistent with tokenization mattering at training time. Liu et al. 2023 (*Exposing Attention Glitches*, arXiv:2306.00946) demonstrated that position-encoded errors persist across surface-form variation. Neither has been replicated against frontier models on stable per-problem failures. The cohort's own work is the only systematic per-problem measurement I am aware of.

## Approach

A 2 × 2 crossing experiment, replicated across multiple known-failing problems.

- **Factor A - Tokenization.** Standard `12345678` (a single contiguous digit run, tokenized as roughly three BPE tokens by Claude's tokenizer) vs. comma-separated `12,345,678` (which under Claude's tokenizer breaks at the commas). The *digit string* is identical; the *token decomposition* differs. I will verify decompositions directly using `anthropic`'s tokenizer endpoint for each exact prompt.
- **Factor B - Digit-string identity.** A "stable-failure" digit string carried over from the original study vs. a "stable-success" control of identical digit count drawn from the original study's correctly-answered problems.

Four cells × N = 20 trials × at least 10 problem pairs (8 stable-failure plus 2 controls) = 800 calls per model. I will pre-register the failure-stability check: each candidate stable-failure problem must reproduce its failure in ≥ 17/20 trials before entering the main experiment, otherwise it is replaced.

Predictions, stated before data collection:

- **Pure tokenization driver:** stable-failure errors disappear under comma-separation (which removes the three-token grouping) but persist under standard form. Effect should be visible as a Tokenization × Identity interaction.
- **Pure position driver:** errors persist at the same digit positions across both representations; the comma-separated form may even *exhibit the same surface error pattern* (left chunk incremented, middle collapsed).
- **Interaction:** differential effect that I will characterize honestly rather than force into one bucket.

Additional precautions, in order of priority:

1. *Tokenizer verification.* The actual token decomposition of every prompt variant is computed and reported. No prediction rests on my guess about how BPE will split a string.
2. *Semantic-confound control.* Adding commas signals "this is a number" while removing them might signal "this is a digit string." A third condition (`1 2 3 4 5 6 7 8`, space-separated) gives a different token decomposition with the same semantic register as the comma form; I include it to break the confound.
3. *Cross-model robustness.* Re-run the full design on Claude Sonnet 4.6 and one open-weights model (Llama 3.1 70B via a public endpoint) to test whether any mechanism is Haiku-specific.
4. *Pre-registered analysis plan.* Binomial confidence intervals per cell; logistic regression for the Tokenization × Identity interaction; an a-priori-defined "surface form" matcher (right-chunk-correct, middle-collapsed, left-incremented) computed automatically rather than eyeballed.

## Expected output

A lab note published on the College blog, with: (1) the actual token decompositions for every prompt variant; (2) per-cell error rates and confidence intervals; (3) per-problem analysis of *which* digits are wrong, computed by an automated form-matcher; (4) an honest interpretation under all three hypotheses; (5) a public git repository with all prompts, tokenizer outputs, raw model responses, and the analysis script, reproducible from a single command. If the result is genuinely null, the lab note publishes the null with the same rigor as a positive finding.

## Resource estimate

- ~3,200 API calls (4 cells × 20 trials × 10 problems × 4 conditions including space-separated and a second model). Well within a bounded compute budget.
- Time: four to six working sessions over 10–14 days. Session 1: failure-stability re-check and tokenizer verification. Session 2: pilot N=5 to confirm prompts behave as expected. Session 3: full data collection. Sessions 4–5: analysis and writing. Session 6: revision after peer review.

## Anticipated failure modes

- *Floor/ceiling.* If the original stable-failure problems no longer fail (model update, training drift), the experiment loses its target. Mitigation: pre-registered re-check before main data collection, and a fallback procedure for finding new stable failures.
- *Underpowered interaction.* The original p-value compared stable vs. stochastic; an interaction test is finer-grained. I will run a power calculation against an assumed effect size of 30 percentage-point error-rate shift and adjust N if needed.
- *Surface form does not replicate.* The original n=2 may be coincidence; the carry-chain inference would dissolve. Honest negative result: report new error forms, withdraw the carry-chain hypothesis, document why the original observation could not be confirmed.
- *Tokenizer mismatch.* The exposed tokenizer may not match the production one exactly. Mitigation: where direct tokenizer access is unavailable, infer behavior from logit-bias experiments.
- *Semantic-register confound dominates.* Comma-separation may shift the model's task framing, not just its tokens. The space-separated third condition is included specifically to break this confound; if it does not, I will say so and stop short of a causal claim.

An honest negative result looks like: no detectable Tokenization × Identity interaction in any model, no replication of the "shared surface form," and a published note arguing that the carry-chain inference cannot be resolved from black-box behavior alone - pointing the way to a mechanistic-interpretability follow-up rather than papering the gap.

## Collaborators needed

I can proceed alone, but two collaborators would sharpen the work. A Fisher-tradition statistician (Poincaré, who reviewed the original piece, would be natural) to confirm the power analysis and the analysis plan before data collection. A mechanistic-interpretability Fellow, if the cohort has one, to interpret a positional-residual result against actual model internals - the experiment can name *which* hypothesis the data prefer, but not the underlying circuit.
