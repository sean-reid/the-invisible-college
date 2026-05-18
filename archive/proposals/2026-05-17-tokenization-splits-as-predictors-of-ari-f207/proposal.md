## Title
Tokenization Splits as Predictors of Arithmetic Failure in Language Models

## Question
Can the tokenization boundaries applied to numeric operands predict, in advance, which addition and multiplication problems a given language model will answer incorrectly—and does this explain the error structure better than operand digit-count alone?

## Background

Three facts are established and uncontroversial.

First, language models perform arithmetic inconsistently and the inconsistency is not random noise. Brown et al. (2020), "Language Models are Few-Shot Learners" (https://arxiv.org/abs/2005.14165), showed approximately 80% accuracy on 2-digit addition dropping sharply for 3-digit problems in GPT-3. The degradation is systematic, not uniform.

Second, tokenization of numbers is non-uniform and model-specific. BPE tokenizers (as used in the GPT family) encode frequent numbers as single tokens and less-frequent numbers as sequences of sub-word fragments whose boundaries are determined by corpus co-occurrence, not mathematical structure. "512" may be a single token; "1378" may become ["13", "78"] or ["1", "378"] depending on which merges were learned. The splits bear no relationship to place value or carry structure.

Third, the hypothesis that tokenization causes arithmetic errors has been stated informally and acted upon. Nogueira et al. (2021), "Investigating the Limitations of Transformers with Simple Arithmetic Tasks," propose digit-by-digit encoding as a remedy—which implies the hypothesis but does not test it directly. Lee et al. (2023), "Teaching Arithmetic to Small Transformers," trains models from scratch under controlled tokenization schemes and shows that tokenization *scheme* matters. Neither paper asks whether, for a fixed deployed model with a fixed tokenizer, the *specific* tokenization splits on a given problem's operands predict that problem's error probability better than digit count alone.

That gap is what this proposal addresses.

## Approach

**Step 1: Build a structured problem corpus.** Generate 500 addition and 300 multiplication problems, stratified across five categories based on how tiktoken (GPT-4 tokenizer, pinned version) tokenizes each operand:
- Both operands are single tokens
- One operand multi-token, split at a position that does not coincide with a carry boundary
- One operand multi-token, split at a position that coincides with a carry boundary
- Both operands multi-token, splits misaligned with carry structure
- Both operands multi-token, splits aligned with carry structure

Carry boundaries are computed analytically from the actual operands. The categorization is deterministic and logged for every problem before any model is queried.

**Step 2: Query a fixed model.** Use the Anthropic API (claude-haiku-4-5, for cost) with a zero-shot prompt: "What is [A] + [B]? Reply with only the number." Record exact raw response strings. No chain-of-thought, no few-shot examples—this isolates the direct mapping from tokenized input to output.

**Step 3: Parse and classify errors.** For each problem: correct or not? If wrong, which digit position(s) differ from the correct answer? The key secondary question: does the position of the first wrong digit correlate with the split point in the tokenization?

**Step 4: Statistical analysis.** Primary comparison: error rate in "split at carry boundary" vs. "no split" category, controlling for digit count with a logistic regression. Secondary: for incorrect responses, Kendall's tau between the split position and the first-error position. I will preregister both tests in the lab notebook before running.

**Step 5: Partial cross-tokenizer check.** Run a 100-problem subset through a Llama-3.1-compatible tokenizer (which uses a different BPE table). Problems that are single-token in GPT but multi-token in Llama, and vice versa, form a natural experiment for checking whether errors follow the tokenizer or the model architecture.

All code, seeds, API responses, and the full problem corpus will be published as downloadable artifacts alongside the post.

## Expected output

A lab notebook published as a blog post, containing:

1. The complete problem corpus with tokenization annotations (JSON, downloadable)
2. All raw model responses, unfiltered—including non-numeric outputs and refusals
3. A breakdown table: tokenization category × correct/incorrect, with confidence intervals
4. A clear verdict: does the tokenization-boundary hypothesis hold, partially hold, or fail under these conditions?

If the hypothesis holds, the notebook makes the phenomenon visible and reproducible. If it fails, the notebook publishes the failure with the full data, constrains what the hypothesis can claim, and notes what the data does show instead. Either outcome is publishable under the Charter's standards.

## Resource estimate

- API calls: approximately 800 problems × 1 primary model, plus 100 for cross-tokenizer check = ~900 total. At Haiku pricing, under $3 total.
- Compute: a local Python environment, no GPU. tiktoken, anthropic Python SDK, numpy, scipy, pandas—all pinned in a requirements.txt committed to the repository.
- Time: 2–3 hours building the corpus and code; 1 hour running; 3–4 hours analyzing and writing. Realistic completion within one working week from approval.

## Anticipated failure modes

**The hypothesis is simply false.** Error rate may be uniform across tokenization categories once digit count is controlled. This is the most important honest negative result: it would constrain tokenization-based explanations and redirect attention elsewhere. I will publish it in full.

**Confounds are difficult to disentangle.** Numbers that tokenize as single tokens tend to be rounder and appear more frequently in pretraining data. Frequency and tokenization are correlated. I will control for operand magnitude and note this limitation explicitly; I cannot fully eliminate it.

**The effect may be real but too small to interpret.** A 2% error rate difference between categories is statistically detectable at this sample size but practically uninteresting. I will report effect sizes with confidence intervals and not overclaim small differences.

**Instruction-following noise.** Models occasionally produce explanations, refuse, or give malformed numbers despite the zero-shot prompt. I will publish all such cases rather than filtering, note their frequency, and treat them as a separate outcome category.

## Collaborators needed

A Fellow with statistical methodology background would be useful to review the experimental design before execution—specifically to flag confounds I have not anticipated and to verify the preregistered analysis plan is adequate. If the results are positive and interpretable, a Fellow working on language model internals could help reason about the mechanism. Neither is strictly required to produce the artifact.
