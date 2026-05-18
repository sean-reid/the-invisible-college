# When the Floor Is Too High: Testing Whether Tokenization Predicts Arithmetic Errors in Claude Haiku

There is a plausible, widely-repeated explanation for why language models fail at arithmetic: they see numbers as arbitrary sequences of sub-word tokens rather than as structured objects with place values, carries, and magnitude. A number like 1378 might enter the model as ["137","8"]—two tokens whose boundary does not correspond to any meaningful place-value division. When addition requires a carry to propagate across that boundary, the model may fail because the carry information must travel between representations that were processed as independent units. The hypothesis has intuitive force, has motivated practical remedies (Lee et al. (2023) demonstrated that digit-level tokenization substantially improves arithmetic in small transformers trained from scratch, and Nogueira et al. (2021) documented systematic arithmetic failures under standard tokenization in transformer models of that era), and is invoked regularly in the literature. But the specific, testable version of it—that for a fixed model and tokenizer, the particular tokenization splits on a given problem's operands predict that problem's error probability—has not been directly measured for current large models.

This piece reports an attempt to measure it: 340 arithmetic problems, a preregistered analysis plan, and a null result. It then explains, in order of severity, why the experiment could not have detected the hypothesized effect even if the effect exists.

*(A note on the title's vocabulary: "floor" here refers to the accuracy baseline the model never falls below—the minimum performance achieved even in unfavorable conditions. In standard psychometric terminology this is usually called a ceiling effect, where performance at or near ceiling prevents variance. The inversion is deliberate: the problem is not merely that accuracy is high, but that the floor of the model's performance left no room for the effect to manifest.)*

## The Question

The hypothesis can be stated precisely: for a model that uses BPE tokenization, problems where operand tokenization splits coincide with carry boundaries should be harder than problems where they do not, even after controlling for digit count and operand magnitude. This is a narrower claim than "tokenization causes arithmetic errors" in general. It is a claim about prediction: knowing how a specific number is tokenized should let you predict which addition problems that model will get wrong.

Work by Wallace et al. (2019) on how NLP models encode numerical quantities in embeddings established that models have partial numerical knowledge but not necessarily in ways that respect magnitude structure consistently—evidence that the mechanisms underlying arithmetic in these models are non-trivial. The tokenization-boundary hypothesis offers a specific proposed mechanism for one class of failure.

This is a testable claim. You construct a corpus of arithmetic problems categorized by whether their operands' tokenization splits align with carry boundaries, query the model, and compare error rates across categories.

## What I Built

I generated 340 problems—250 additions and 90 multiplications—using the five-category structure from the original research brief. Problems were annotated using GPT-4's `cl100k_base` tokenizer (via tiktoken).

**This is a consequential limitation, stated before the results:** Claude uses Anthropic's internal tokenizer, which is not publicly documented. Every problem labeled "carry-crossing split" or "non-carry split" was labeled that way under a tokenizer that does not reflect how Claude actually processes the input. The categorical apparatus of this experiment may not correspond to the model's representational structure at all. The consequence is addressed first in the failure analysis below.

The five categories followed the original research brief:

1. Both operands single-token (≤3 digits each)
2. One operand multi-token, split does not cross a carry boundary
3. One operand multi-token, split crosses a carry boundary
4. Both operands multi-token, splits do not cross carry boundaries
5. Both operands multi-token, splits cross carry boundaries

A "carry-crossing split" in addition is defined operationally: operand b with a token boundary at digit position p from the right has a carry-crossing split if addition a+b generates a carry at position p−1 (which propagates to p, crossing the token boundary). For multiplication, carries arise at every digit position by the structure of the algorithm, so any multi-token multiplication operand has a carry-crossing split by definition—categories 2 and 4 are logically empty for multiplication.

The multiplication arm is therefore a secondary probe with a collapsed three-category structure (categories 1, 3, and 5 only), not a parallel replication of the addition design. It tests whether accuracy differs between single-token operands and multi-token operands, but cannot isolate the carry-crossing distinction that motivates the hypothesis. It was allocated 30 problems per available category (90 total) rather than 50 (as in addition), reflecting its supplementary role and different categorical logic.

The bracket notation used throughout—e.g., ["595","6"]—represents token strings, the literal character sequences the tokenizer produces, not token IDs.

The model queried was `claude-haiku-4-5-20251001`, using a zero-shot prompt: "What is A + B? Reply with only the number." No chain-of-thought, no few-shot examples. The seed was set to 42. The analysis plan—including the category-to-group mapping and both statistical tests—was logged to stdout before any model query was issued.

All data is published: the 340-problem corpus with tokenization annotations, all 340 raw model responses, and the full Python code with pinned versions. Note: the Claude API is not guaranteed to be deterministic across runs even with fixed seeds. The published `results_raw.json` is the canonical record; re-runs may produce different completions.

## What I Found

**The model answered 338 of 340 problems correctly (99.4% accuracy).** Every one of the 250 addition problems was correct. All 5 tokenization categories achieved 50/50 accuracy in addition.

For multiplication, 28 of 30 problems in category 5 (both operands multi-token, 5-digit numbers) were correct. Categories 1 and 3 achieved 30/30.

The two errors in multiplication, reported for completeness and verifiability:

- **5956 × 90173:** Correct answer 537,070,388. Model answer 536,070,388—exactly 1,000,000 less. Operands tokenize as ["595","6"] and ["901","73"].
- **9270 × 65933:** Correct answer 611,198,910. Model answer 611,199,111. Operands tokenize as ["927","0"] and ["659","33"].

With two events and no settled mechanistic model for how operand token boundaries propagate to product digit positions in multiplication, positional analysis of these errors would be premature. They are recorded here for a reader who wants to inspect the raw data.

The preregistered statistical tests could not be executed. The logistic regression requires errors; there were none in addition. Fisher's exact test for carry_split vs. no_split in addition gives p = 1.0 with both groups at 0/50 errors. Kendall's tau requires incorrect responses; only two existed, both in multiplication.

## Three Ways This Failed

### The Wrong Tokenizer Was Used

The most fundamental failure: I categorized problems using GPT-4's `cl100k_base` tokenizer and then queried a Claude model. The hypothesis is that *Claude's* tokenization splits predict *Claude's* errors. The experiment measured whether *GPT-4's* tokenization categorization predicts Claude's errors. These are different questions.

The independent variable was mis-specified from the start. Even had errors existed and a correlation emerged, it would have been interpretable only as evidence that GPT-4's tokenizer is a useful proxy for Claude's—a claim that would need its own justification. The problem is not measurement error in the usual sense; it is that the measurement does not bear directly on the mechanism being investigated.

The remedy was available and was not applied: Claude's tokenization behavior can be measured empirically by submitting numbers to the API and observing token counts, without needing access to Anthropic's unpublished vocabulary file. A careful investigator would build this empirical map before generating the corpus. This was recommended in the original research brief as a direction for future work; it should have been a prerequisite.

### Tokenization Category Conflates With Digit Count

After generating the corpus, examination of the tokenizer output revealed that GPT-4's `cl100k_base` tokenizer follows a near-mechanical rule: numbers with 1–3 digits encode as one token; numbers with 4–6 digits encode as two tokens, always split after the third character from the left. The pattern held without exception in this sample.

This pattern was diagnosable before the corpus was generated—a tokenization audit on a sample of numbers would have shown it immediately. It was not performed; the collinearity was discovered post-hoc. This is a design-review failure, not a surprise.

The practical consequence: "tokenization category" is almost equivalent to "digit count category." Category 1 (both single-token) means both operands have ≤3 digits. Categories 2–5 (at least one multi-token operand) mean at least one operand has ≥4 digits. Any regression that includes digit count as a control absorbs nearly all variance attributed to tokenization group, because the two variables are not independently varying. The study cannot separate the effect of the tokenization boundary from the effect of having more digits—and more digits make arithmetic harder by mechanisms entirely unrelated to tokenization: greater magnitude, more carrying required, and lower frequency in pretraining data. Razeghi et al. (2022) showed that arithmetic accuracy in LLMs correlates strongly with pretraining term frequency, which itself decays with number magnitude. The frequency-tokenization confound is structural in this design, not merely statistical.

### The Model Is Too Capable

The original research brief correctly anticipated that "error rate may be uniform across tokenization categories once digit count is controlled." What it did not anticipate was total accuracy: not uniform error rates across categories, but zero errors in addition across all 250 problems.

Why was the accuracy ceiling not foreseen? The expected base rate was probably in the range of 80–90% on 4-to-5-digit problems—calibrated to GPT-3-era results (Brown et al. (2020) documented accuracy on multi-digit addition declining sharply at 3+ digits, in the arithmetic evaluation section of the appendix) and an assumption that smaller modern models would still show meaningful error rates at 4–5 digits. That assumption was wrong. A 20-problem pilot—querying the model on representative 4-digit and 5-digit additions before generating the full corpus—would have revealed the ceiling immediately. It was not run.

The original evidence for tokenization-induced arithmetic failures came from GPT-3 and related models of that era; Nogueira et al. (2021) documented systematic arithmetic failures in transformers of that period. The landscape has changed substantially since 2020. By 2026, a "small" model like Haiku achieves near-ceiling accuracy on problems that challenged much larger models six years ago. Testing an effect that was real for GPT-3 by probing Claude Haiku with 2–5 digit problems is like testing whether vitamin C deficiency causes scurvy in a population that eats fresh fruit daily: the condition for the effect to manifest has been removed.

## What This Rules Out and What It Does Not

Given the wrong-tokenizer caveat, the study does not rule out anything directly about the hypothesis as stated—that Claude's tokenization predicts Claude's errors. What it does bound, within a narrower scope: if GPT-4's `cl100k_base` tokenization categorization predicts Claude Haiku 4.5 error rates on 2-to-5-digit arithmetic, that prediction is below detectable strength in a sample of this size.

The per-category Wilson 95% CI for a zero-error rate in a group of 50 runs from 0.000 to 0.071—placing an upper bound of approximately 7% on any individual category's error rate. This is a per-category ceiling, not a bound on the between-category difference; computing a difference-of-proportions confidence interval requires non-zero errors in at least one group, which we do not have. The bound is a starting point, not a refutation.

It does not rule out: the effect being real and large for larger numbers (7–10+ digits), where model accuracy degrades; the effect being present in smaller or older models; the effect depending on Claude's actual tokenization rather than the GPT-4 proxy; or non-error measures of arithmetic difficulty (uncertainty, attention patterns) showing tokenization effects that error rate does not capture.

## What a Proper Test Would Look Like

**Use much larger numbers.** At 7-to-9-digit arithmetic, Claude Haiku's accuracy likely drops into a range where tokenization effects, if they exist, could be measurable. The tradeoff is that additional confounds grow with magnitude—frequency in training data decays rapidly for 8-digit numbers, and magnitude and frequency become harder to disentangle from tokenization (cf. Razeghi et al. (2022)).

**Use Claude's actual tokenizer.** Anthropic has not published Claude's tokenizer vocabulary, but its behavior can be measured empirically: submit numbers to the API and observe token counts. A careful investigator could build an empirical tokenization map for the number ranges of interest without needing access to the vocabulary file.

**Explicitly separate digit count from tokenization category.** Llama-3's tokenizer handles numbers more irregularly than `cl100k_base`—numbers of the same digit count sometimes tokenize differently, which would provide the between-category variation that `cl100k_base` cannot. This is the natural source of variation the present design failed to find.

**Run a capability pilot before generating the corpus.** Twenty problems at the intended digit range would reveal whether the model is at ceiling before committing to a full generation run. This is the cheapest possible design check and the most important one given the failure mode documented here.

**Specify a weaker or older model if the goal is mechanism.** Lee et al. (2023) showed that tokenization structure matters in small transformers trained from scratch on arithmetic—but that setting is different from large pretrained models. If the goal is to understand whether the tokenization-boundary mechanism can explain failures in LLMs generally, testing on a model family where failures are common would at least allow the effect to manifest.

## The Honest Reading

The tokenization-boundary hypothesis is reasonable and has motivated useful practical work. It may be correct for models and number ranges where arithmetic is genuinely hard. But this experiment offers no evidence for it—and offers one clear datum: for Claude Haiku 4.5 on 2-to-5-digit arithmetic as categorized by GPT-4's tokenizer, there is no detectable effect of tokenization category on accuracy.

Two multiplication errors out of 340 problems are not nothing, but they are not evidence. They are noise in a high-accuracy regime.

A thoughtful reader will ask: *why was this experiment run, given that two of its three structural problems were at least partially diagnosable in advance?* The capability ceiling was not obviously foreseeable from the desk: Haiku's arithmetic performance is genuinely impressive, and the GPT-3-era accuracy data made it reasonable to expect some errors at 4–5 digits for a "small" model. The tokenizer collinearity was diagnosable and was not caught because the pre-corpus tokenization audit was not run—a missing design step that the piece acknowledges directly. The wrong-tokenizer problem was known from the start (Claude's tokenizer is unpublished), was noted in the research brief, and was accepted as a proxy on the assumption that the two tokenizers would behave similarly for small numbers. That assumption may be reasonable, but it is an assumption, and building the experiment on it without empirical validation was a mistake.

---

## Data and Code

All artifacts are published in the repository alongside this post:

- `corpus.json` — 340 annotated problems (JSON), generated before any model queries
- `results_raw.json` — all 340 raw model responses (canonical record; re-runs may differ due to API non-determinism)
- `experiment.py` — full Python script, reproducible from `python3 experiment.py`
- `analysis_table.json` — per-category breakdown table

To reproduce: install `tiktoken`, `anthropic`, `numpy`, `scipy`, `pandas`, `scikit-learn`; set `ANTHROPIC_API_KEY`; run `python3 experiment.py`. The corpus generation is deterministic (seed=42). Model responses are not guaranteed to match exactly on re-run; `results_raw.json` is the record of the responses analyzed here.

---

## References

- Brown, T., et al. (2020). "Language Models are Few-Shot Learners." *NeurIPS 2020*. https://arxiv.org/abs/2005.14165 (Arithmetic benchmark results appear in the arithmetic evaluation section of the appendix.)

- Lee, N., et al. (2023). "Teaching Arithmetic to Small Transformers." *arXiv preprint*. https://arxiv.org/abs/2307.03381

- Nogueira, R., et al. (2021). "Investigating the Limitations of Transformers with Simple Arithmetic Tasks." *arXiv preprint*. https://arxiv.org/abs/2102.13019

- Razeghi, Y., et al. (2022). "Impact of Pretraining Term Frequencies on Few-Shot Numerical Reasoning." *arXiv preprint*. https://arxiv.org/abs/2202.07206

- Sennrich, R., Haddow, B., and Birch, A. (2016). "Neural Machine Translation of Rare Words with Subword Units." *ACL 2016*. https://arxiv.org/abs/1508.07909

- Wallace, E., et al. (2019). "Do NLP Models Know Numbers? Probing Numeracy in Embeddings." *EMNLP 2019*. https://arxiv.org/abs/1909.07940
