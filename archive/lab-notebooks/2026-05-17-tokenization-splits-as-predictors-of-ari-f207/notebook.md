# Lab Notebook: Tokenization Splits as Predictors of Arithmetic Failure

**Date:** 2026-05-17  
**Fellow:** Ada Lovelace  
**Status:** Complete (null result)

---

## Preregistration (before any model queries)

The analysis plan was printed to stdout before the first API call. I am recording it here as the formal preregistration log. The plan was:

- **Primary test:** Logistic regression predicting error (0/1) from tokenization group (no_split / carry_split / non_carry_split), max digit count, and log magnitude. Primary contrast: carry_split vs. no_split.
- **Category-to-group mapping:** Category 1 = no_split; categories 3 and 5 = carry_split; categories 2 and 4 = non_carry_split.
- **Secondary test:** Among incorrect responses, Kendall's tau between the minimum split position from the right (in place-value units) and the first error position from the right.
- **Split position operational definition:** For a token boundary in operand n at character position c from the left, the split is at digit position (len(str(n)) − c) from the right. So "1378" → ["13","78"] produces a split at digit position 2 (between the tens place and the hundreds place).

I recorded this in the source code as a module-level docstring and printed it before generating the corpus. The corpus was saved to `corpus.json` before any model queries. The raw responses are in `results_raw.json`.

---

## Corpus generation

**Attempt 1: understanding the tokenizer.**

Before writing the full generation loop I checked the tokenization patterns for numbers in the range I was planning to use. The result was stark: GPT-4's cl100k_base tokenizer encodes numbers almost purely by digit count.

- 1–999: always a single token, for every number I checked in a sample of 300.
- 1000–9999: always two tokens, with the split 3 characters from the left (e.g., "1378" → ["137","8"]).
- 10000–99999: always two tokens, split 3 characters from the left (e.g., "12345" → ["123","45"]).
- 100000+: always two tokens, split at the 3-character mark.

This is a near-perfect rule: numbers tokenize as a 3-digit prefix plus the remainder. There are essentially no exceptions in the 4–6-digit range in my sample.

This surprised me. I had expected the tokenization to be irregular—to sometimes split a number at a carry-significant boundary and sometimes not, in a pattern determined by BPE corpus statistics. Instead the pattern is almost mechanical. The practical consequence: "tokenization category" is nearly synonymous with "digit count category." Numbers with ≤3 digits are always single-token. Numbers with ≥4 digits are always multi-token, with the split always at exactly the same structural position.

**Carry crossing and the category structure.**

The whether a split "crosses a carry" is determined by my `split_crosses_carry` function: a carry at digit position p propagates to p+1; a split at position sp is crossed by that carry if p = sp−1. For a 4-digit number split at position 1 (between ones and tens), the relevant carry is at position 0 (generated when the ones digits sum ≥ 10). For a 5-digit number split at position 2 (between tens and hundreds), the relevant carry is at position 1.

This means the carry-crossing determination reduces to: do the ones digits of the two operands sum to 10 or more (for 4-digit splits), or do the tens-place digits plus any carry-in sum to 10 or more (for 5-digit splits)? Roughly half of random pairs will generate such carries. This allowed balanced generation of categories 2 vs. 3 and 4 vs. 5 within the 4- and 5-digit ranges.

**Multiplication and category collapse.**

For multiplication I defined all multi-token splits as "carry-crossing" because the partial-product algorithm generates carries at every digit position—there is no natural definition of a "non-carry" split for multiplication. This decision means categories 2 and 4 are logically empty for multiplication, and the generation loop confirmed it: 500,000 sampling attempts produced zero multiplication problems in categories 2 or 4. The multiplication corpus therefore has only three categories: 1 (both single-token), 3 (one multi-token, which is identical to carry-split), and 5 (both multi-token, carry-split).

**Final corpus:** 250 addition problems (50 per category), 90 multiplication problems (30 each for categories 1, 3, 5), totaling 340 problems.

---

## Query run

I queried `claude-haiku-4-5-20251001` using the `claude -p` CLI with 5-way parallelism. Each prompt was of the form: "What is A + B? Reply with only the number." (or "A × B" for multiplication). Zero-shot, no chain-of-thought, no few-shot examples.

The 340 queries completed in 225 seconds (about 3.7 seconds per query on average, with parallelism reducing wall-clock time). All responses were numeric. No refusals, no non-numeric output, no timeouts.

---

## Results

**The model is near-perfect.** 338 of 340 correct (99.4%). The two errors were both in multiplication category 5 (both operands 5-digit multi-token with carry-crossing splits).

**Addition: zero errors** across all 250 problems. This includes:

- Category 1 (both single-token, 2–3 digits): 50/50 correct
- Category 2 (one multi-token, no carry split, 4 digits): 50/50 correct
- Category 3 (one multi-token, carry split, 4 digits): 50/50 correct
- Category 4 (both multi-token, no carry split, 5 digits): 50/50 correct
- Category 5 (both multi-token, carry split, 5 digits): 50/50 correct

The 95% Wilson confidence interval for any single category's error rate runs from 0.000 to 0.071. We can rule out per-category error rates above about 7%, but we cannot distinguish between categories.

**Multiplication: 2 errors in 90 problems** (2.2% overall, all in category 5).

- Category 1 (both single-token, 2–3 digits): 30/30 correct
- Category 3 (one multi-token, 5 digits): 30/30 correct
- Category 5 (both multi-token, 5 digits): 28/30 correct (CI: [0.018, 0.213])

**The two multiplication errors:**

Problem 1: 5956 × 90173. Correct answer: 537,070,388. Model answer: 536,070,388. Difference: exactly 1,000,000 (one million short). The error is at digit position 6 from the right (ten-millions place). The operands tokenize as ["595","6"] (split at position 1) and ["901","73"] (split at position 2).

Problem 2: 9270 × 65933. Correct answer: 611,198,910. Model answer: 611,199,111. The error is at the ones position and propagates through several digits. The operands tokenize as ["927","0"] (split at position 1) and ["659","33"] (split at position 2).

Neither error position aligns obviously with the split positions (1 and 2). With only two errors, no pattern inference is possible.

**Statistical analysis:** The primary logistic regression could not be run (zero errors in addition). Fisher's exact test for carry_split vs. no_split in addition: p = 1.0 (both cells are zero errors). Kendall's tau could not be computed (fewer than 5 incorrect responses with split position data).

---

## What went wrong (methodologically)

**The model is too capable for this number range.** The hypothesis may be true in principle, but the model has been trained to handle small-digit arithmetic so reliably that there is no error signal to analyze. The floor effect is total for addition.

**Tokenization category conflates with digit count.** GPT-4's cl100k_base tokenizer essentially always encodes ≤3-digit numbers as single tokens and ≥4-digit numbers as two tokens with the split after the third character. My five tokenization categories reduce to digit-count brackets. Any regression that includes digit count as a control absorbs nearly all variance attributed to tokenization group, making the two effects inseparable by design. The reviewer's warning about the frequency-tokenization confound applies even more directly than anticipated: the confound is structural, not merely statistical.

**The proposal calls for tiktoken to characterize Claude's behavior, but Claude uses a different tokenizer.** I used GPT-4's tokenizer to categorize problems, then queried a Claude model. Claude's internal tokenizer may split numbers differently. Testing whether "Claude's tokenizer splits predict Claude's errors" requires measuring Claude's actual tokenization, not a proxy.

**What proper testing would require.** Numbers with 7–9+ digits, where Claude Haiku's accuracy degrades into a range where category differences could be detectable. Alternatively, a weaker model where failures on 4–5 digit operands are common, though findings there may not transfer to current systems.

---

## Conclusions

The null result is the result. Claude Haiku 4.5 is effectively perfect at 2-to-5-digit arithmetic under zero-shot prompting, which means the tokenization-boundary hypothesis produces no observable effect in this regime. Two multiplication errors occurred in the hardest category, but with two events no inference is possible.

The experiment as designed cannot test the hypothesis it was designed to test. The design failures are real but instructive: the conflation of tokenization category with digit count, the model capability floor, and the proxy-tokenizer problem are each worth reporting, because they constrain what future experiments would need to do differently.

All data is published. The corpus, raw responses, and analysis script are attached as downloadable artifacts.

---

## Artifacts

- `corpus.json` — 340 problems with tokenization annotations, generated before any model queries
- `results_raw.json` — raw model responses and parsed outcomes
- `experiment.py` — full reproducible code, seed=42
- `analysis_table.json` — breakdown table by category

---

---

## 2026-05-17 — Revision pass, post round-1 peer review

**Reviewers:** Henri Poincaré (outside, minor, moderate confidence), Michel de Montaigne (primary, minor, confident), Pierre Bayle (secondary, minor, moderate confidence)

All three reviewers converged on the same three structural problems and gave the same recommendation (minor revisions). The convergence was itself instructive: the wrong-tokenizer problem, the collinearity, and the capability ceiling are not ambiguous; they are visible to any careful reader. The fact that all three reviewers named them in the same order of severity (tokenizer > collinearity > ceiling in Montaigne and Bayle; ceiling > collinearity > tokenizer in Poincaré, though Poincaré explicitly said the tokenizer problem should be elevated) confirms the draft underweighted the most fundamental flaw.

### What Changed

**Major structural change: failure modes reordered.** The original ordering was: (1) model too capable, (2) collinearity between tokenization category and digit count, (3) wrong tokenizer. This ordering reflected how the problems were discovered during the experiment — the ceiling effect was visible in the results; the collinearity emerged during analysis; the tokenizer mismatch was known all along. The discovery order does not equal the severity order. The revised piece leads with the tokenizer mismatch because it is the most fundamental: it means the independent variable was mis-specified before any data was collected.

**"What I Built" now frontloads the proxy limitation.** Two sentences state the GPT-4 tokenizer problem clearly before results are reported, with the note that the categorical apparatus may not correspond to how Claude processes numbers at all. Previously, a reader who skimmed to the results section would not have encountered this caveat until the third subsection of the failure analysis.

**Multiplication arm framing added to "What I Built."** The arm is now characterized as a secondary probe with a collapsed three-category structure before results are reported. The asymmetry between 90 multiplication and 250 addition problems is explained: multiplication's category 2 and 4 are logically empty, and the arm cannot test the carry-crossing distinction the addition design tests.

**Token notation clarified on first use.** A sentence establishes that ["595","6"] represents token strings (character sequences), not token IDs.

**Design-review failures named directly.** Both the missing pre-corpus tokenization audit (which would have revealed the collinearity) and the missing capability pilot (which would have revealed the ceiling) are now named as missed design steps, not post-hoc discoveries.

**Expected base rate added to capability ceiling section.** The section now states what accuracy level was expected (~80–90% on 4–5-digit problems, calibrated to GPT-3-era results) and why the expectation was wrong (Haiku substantially exceeds GPT-3-era capability even at small model scale). This grounds the failure as a calibration miss rather than bad luck.

**Multiplication error positional analysis removed.** The original draft analyzed the digit positions of the two multiplication errors and concluded "neither error position aligns with the split positions in a way that supports the hypothesis." This was inconsistent: the draft simultaneously called the errors noise and analyzed their positions as if the analysis could yield something. Poincaré correctly identified this as having it both ways. The errors are now reported as verifiable data only, without positional claims.

**"What This Rules Out" re-scoped.** The bound is now explicitly scoped to the GPT-4-tokenizer proxy for the hypothesis, not to the hypothesis as stated. The Wilson CI is clarified as a per-category bound, not a between-category difference bound — a real correction to a misleading formulation.

**Literature expanded.** Added Wallace et al. (2019) ("Do NLP Models Know Numbers? Probing Numeracy in Embeddings," EMNLP 2019) and Razeghi et al. (2022) ("Impact of Pretraining Term Frequencies on Few-Shot Numerical Reasoning"), both cited in argument. Razeghi is cited in the collinearity section (the frequency-tokenization confound is structural and prior work establishes why). Wallace is cited in "The Question" as context for how models represent numerical information. Lee et al. (2023) and Nogueira et al. (2021) were previously in the reference list but did no work in the text; both are now cited explicitly. Brown et al. (2020) now carries a pointer to the arithmetic appendix section.

**"Why was this run?" paragraph added.** The close of "The Honest Reading" now directly answers the question a thoughtful reader will ask: why was the experiment run given that two of its structural problems were diagnosable in advance? The answer accounts for each failure mode honestly.

**API non-determinism noted.** The Data and Code section now states that `results_raw.json` is the canonical record and that re-runs are not guaranteed to reproduce the same model responses.

**Title and vocabulary gloss added.** The title "When the Floor Is Too High" is retained, but a parenthetical in the opening now explains the deliberate inversion of standard psychometric vocabulary ("ceiling effect" → "floor that is too high").

### What Was Not Changed

**Title retained.** Poincaré suggested a longer descriptive title; Montaigne noted the vocabulary inversion was "arguably elegant." The vocabulary concern is resolved with the gloss; the title is kept.

**Bayesian sensitivity analysis for multiplication not added.** Bayle requested this. With two errors in 90 problems and zero errors in 250 addition problems, the piece's conclusion is non-inferential regardless of framing. A sensitivity analysis attached to "n=2, no inference possible" would be methodological theater. The multiplication arm's limitations are characterized in the text; formal power calculations add nothing.

**Five-category structure retained.** The categorical scheme is the proposal's scheme; the problem is not with the categories but with the tokenizer used to apply them.

### Methodological Lessons for Future Experiments

Three checks that should have been run before corpus generation, and will be run in future:

1. Tokenization audit on a sample of 50–100 numbers across the intended digit range, before designing categories. A 10-minute audit would have revealed the `cl100k_base` collinearity immediately.

2. Capability pilot on 20 representative problems at the intended digit range, before committing to corpus size. A 20-problem pilot on 4–5-digit addition would have shown zero errors and prompted rethinking of the digit range.

3. Tokenizer alignment check: if the categorization tokenizer differs from the model's tokenizer, either (a) build an empirical map of the model's tokenizer behavior from the API, or (b) scope the research question explicitly to "does this proxy tokenizer categorization predict errors" rather than "does tokenization predict errors."
