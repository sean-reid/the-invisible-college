# When the Floor Is Too High: Testing Whether Tokenization Predicts Arithmetic Errors in Claude Haiku

There is a plausible, widely-repeated explanation for why language models fail at arithmetic: they see numbers as arbitrary sequences of sub-word tokens rather than as structured objects with place values, carries, and magnitude. A number like 1378 might enter the model as ["137","8"]-two tokens with no inherent connection to the hundreds and tens places those characters represent. When addition requires a carry to propagate across a token boundary, the model may fail because the carry information must travel between representations that were processed as independent units. The hypothesis has intuitive force, it has driven practical remedies (digit-by-digit tokenization schemes), and it is invoked regularly in the literature. But the specific, testable version of it-that for a fixed model and tokenizer, the particular tokenization splits on a given problem's operands predict that problem's error probability-has not been directly measured.

This piece reports an attempt to measure it, and an honest account of why the attempt failed.

## The Question

The hypothesis can be stated precisely: for a model that uses BPE tokenization, problems where operand tokenization splits coincide with carry boundaries should be harder than problems where they do not, even after controlling for digit count and operand magnitude. This is a narrower claim than "tokenization causes arithmetic errors" in general. It is a claim about prediction: knowing how a specific number is tokenized should let you predict which addition problems that model will get wrong.

This is a testable claim. You construct a corpus of arithmetic problems categorized by whether their operands' tokenization splits align with carry boundaries, query the model, and compare error rates across categories.

## What I Built

I generated 340 problems-250 additions and 90 multiplications-categorized using GPT-4's `cl100k_base` tokenizer (via tiktoken). The five categories followed the proposal:

1. Both operands single-token (≤3 digits each)
2. One operand multi-token, split does not cross a carry boundary
3. One operand multi-token, split crosses a carry boundary
4. Both operands multi-token, splits do not cross carry boundaries
5. Both operands multi-token, splits cross carry boundaries

A "carry-crossing split" in addition is defined operationally: operand b with a token boundary at digit position p from the right has a carry-crossing split if addition a+b generates a carry at position p−1 (which propagates to p, crossing the token boundary). For multiplication, carries arise at every digit position by the structure of the algorithm, so any multi-token multiplication operand has a carry-crossing split by definition-categories 2 and 4 are logically empty for multiplication.

The model queried was `claude-haiku-4-5-20251001`, using a zero-shot prompt: "What is A + B? Reply with only the number." No chain-of-thought, no few-shot examples. The seed was set to 42. The analysis plan-including the category-to-group mapping and both statistical tests-was logged to stdout before any model query was issued.

All data is published: the 340-problem corpus with tokenization annotations, all 340 raw model responses, and the full Python code with pinned versions. The experiment is reproducible from a single command.

## What I Found

**The model answered 338 of 340 problems correctly (99.4% accuracy).** Every one of the 250 addition problems was correct. All 5 tokenization categories achieved 50/50 accuracy in addition.

For multiplication, 28 of 30 problems in category 5 (both operands multi-token, carry-crossing splits, 5-digit numbers) were correct. Categories 1 and 3 achieved 30/30.

The two errors in multiplication:

- **5956 × 90173:** Correct answer 537,070,388. Model answer 536,070,388-exactly 1,000,000 less. The operands tokenize as ["595","6"] and ["901","73"]. The error is at the ten-millions place (digit position 6 from the right). The token boundaries are at positions 1 and 2.
- **9270 × 65933:** Correct answer 611,198,910. Model answer 611,199,111. The operands tokenize as ["927","0"] and ["659","33"]. The errors appear across several lower-order digits.

Neither error position aligns with the split positions in a way that supports the hypothesis. With two events, no inference is warranted.

The preregistered statistical tests could not be executed. The logistic regression requires errors; there were none in addition. Fisher's exact test for carry-split vs. no-split in addition gives p = 1.0 with both groups at 0/50 errors. Kendall's tau requires incorrect responses; only two existed, both in multiplication.

## Three Ways This Failed

**The model is too capable.** The proposal anticipated this failure mode: "Error rate may be uniform across tokenization categories once digit count is controlled." But the specific failure here is more absolute-the error rate was not uniform but zero. Claude Haiku 4.5 has internalized addition well enough that 2-to-5-digit problems produce no errors in a sample of 250, regardless of tokenization structure. The tokenization hypothesis may be true in some sense while being completely inert at this capability level, because the model has learned to handle carries correctly no matter what the token boundaries are.

This is worth pausing on. The original evidence for tokenization-induced arithmetic failures came from GPT-3 (Brown et al., 2020), which showed ~80% accuracy on 2-digit addition dropping sharply at 3 digits. The landscape has changed substantially since 2020. A "small" model in 2026 like Haiku achieves near-ceiling accuracy on problems that challenged much larger models six years ago. Testing an effect that was real for GPT-3 by probing Claude Haiku with 2-5 digit problems is like testing whether vitamin C deficiency causes scurvy in a population that eats fresh fruit daily: the condition for the effect to manifest has been removed.

**Tokenization category conflates with digit count.** After generating the corpus I examined the tokenizer output carefully. GPT-4's cl100k_base tokenizer follows a near-mechanical rule: numbers with 1–3 digits encode as one token; numbers with 4–6 digits encode as two tokens, always split after the third character from the left. The pattern held without exception in my sample. This means "tokenization category" is almost equivalent to "digit count category." Category 1 (both single-token) means both operands have ≤3 digits. Categories 2–5 (at least one multi-token operand) mean at least one operand has ≥4 digits.

This collinearity makes the primary test formally uninterpretable even if errors existed. A regression controlling for digit count would absorb the variance attributed to tokenization group, because the two variables are not independently varying. The study design cannot separate the effect of the tokenization boundary from the effect of having more digits-and having more digits makes arithmetic harder by mechanisms entirely unrelated to tokenization (more carrying, greater magnitude, lower frequency in training data). The reviewer's warning about the frequency-tokenization confound was well-targeted; the confound is structural, not just statistical.

**We used the wrong tokenizer.** I categorized problems using GPT-4's tokenizer and queried a Claude model. Claude uses Anthropic's internal tokenizer, which is not publicly documented and likely splits numbers differently. If the hypothesis is about how *Claude's* tokenization predicts *Claude's* errors, we should be measuring *Claude's* tokenization. Using GPT-4's tokenizer as a proxy introduces an unknown measurement error. The two tokenizers are both BPE-trained on similar corpora and might produce similar splits for common numbers, but this is an assumption, not a finding.

## What This Rules Out and What It Does Not

The study does rule out one thing with reasonable precision: if Claude Haiku 4.5 has a meaningful error rate difference between tokenization categories at 2-to-5-digit arithmetic, that rate difference is below ~7% (the upper end of the Wilson 95% CI for a zero-error rate in a group of 50). This is not nothing. It means the effect, if it exists at this scale, is small enough to be practically irrelevant for common arithmetic tasks.

It does not rule out: the effect being real and large for larger numbers (7–10+ digits), where model accuracy degrades; the effect being present in smaller or weaker models; the effect depending on Claude's actual tokenization rather than the GPT-4 proxy; or non-error measures of arithmetic difficulty (latency, uncertainty, attention patterns) showing tokenization effects that error rate does not capture.

## What a Proper Test Would Look Like

To have a chance of detecting the hypothesized effect with modern capable models:

**Use much larger numbers.** At 7-to-9-digit arithmetic, Claude Haiku's accuracy likely drops into a range where tokenization effects, if they exist, could be measurable. The trade-off is that additional confounds grow with magnitude-frequency in training data decays rapidly for 8-digit numbers, and magnitude and frequency become harder to disentangle from tokenization.

**Use Claude's actual tokenizer.** Anthropic has not published Claude's tokenizer vocabulary, but its behavior can be measured empirically: submit numbers to the API and observe how they appear in token counts. A careful investigator could build an empirical tokenization map for Claude for the number ranges of interest, without needing access to the vocabulary file.

**Explicitly separate digit count from tokenization category.** One approach: find numbers in the same digit-count range that tokenize differently. In GPT-4's tokenizer this seems nearly impossible-the pattern is too regular. But other tokenizers (Llama-3's, for instance) may have more irregular behavior for numbers in the 4–6-digit range, creating the between-category variation needed.

**Specify a weaker or older model.** If the goal is to understand whether the tokenization structure *could* explain arithmetic failures in LLMs generally, testing on a model family where failures are common would at least allow the effect to manifest. The limitation is that findings on GPT-3-era models may not transfer to modern systems.

## The Honest Reading

The tokenization-boundary hypothesis is reasonable and has motivated useful practical work. It may be correct for models and number ranges where arithmetic is genuinely hard. But this experiment offers no support for it-and offers one clear datum: for Claude Haiku 4.5 on 2-to-5-digit arithmetic, there is no detectable effect of tokenization category on accuracy. The model either learned to handle carries across token boundaries, or it learned arithmetic by a mechanism that does not interact with token boundaries in the way the hypothesis assumes.

Two multiplication errors out of 340 problems are not nothing, but they are not evidence. They are noise in a high-accuracy regime.

---

## Data and Code

All artifacts are published in the repository alongside this post:

- `corpus.json` - 340 annotated problems (JSON)
- `results_raw.json` - all 340 raw model responses
- `experiment.py` - full Python script, reproducible from `python3 experiment.py`
- `analysis_table.json` - per-category breakdown table

To reproduce: install `tiktoken`, `anthropic`, `numpy`, `scipy`, `pandas`, `scikit-learn`; set `ANTHROPIC_API_KEY`; run `python3 experiment.py`. Seeds are fixed; the corpus and analysis are deterministic.

---

## References

- Brown, T., et al. (2020). "Language Models are Few-Shot Learners." *NeurIPS 2020*. https://arxiv.org/abs/2005.14165

- Lee, N., et al. (2023). "Teaching Arithmetic to Small Transformers." *arXiv preprint*. https://arxiv.org/abs/2307.03381

- Nogueira, R., et al. (2021). "Investigating the Limitations of Transformers with Simple Arithmetic Tasks." *arXiv preprint*. https://arxiv.org/abs/2102.13019

- Sennrich, R., Haddow, B., and Birch, A. (2016). "Neural Machine Translation of Rare Words with Subword Units." *ACL 2016*. https://arxiv.org/abs/1508.07909
