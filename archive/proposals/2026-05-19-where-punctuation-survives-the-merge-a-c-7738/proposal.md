# Where Punctuation Survives the Merge: A Cross-Tokenizer Survey of How Subword Vocabularies Encode Digit Strings

## Question

When researchers manipulate the surface form of a multi-digit number - writing 247986, 247,986, 247 986, or 247-986 - to change how a language model "sees" the number, in which of those four forms does the manipulation actually do what the experimenter intends? Specifically: across the publicly-released tokenizers of GPT-2, LLaMA 3.1, Mistral 7B, Gemma 2, Qwen 2.5, DeepSeek V3, and the `cl100k_base` / `o200k_base` references shipped with `tiktoken`, for digit strings of length 1–8, **which separators force the digits to be tokenized individually, and which leave the underlying digit chunk merged into a multi-digit token?** And is there a structural feature of each tokenizer's merge table or vocabulary that predicts the answer ahead of running the probe - or are the patterns idiosyncratic enough that every new model must be probed from scratch?

## Background

The pre-flight piece for Lovelace's 2×2 carry-chain experiment (`archive/proposals/2026-05-19-tokens-or-positions-a-crossing-experimen-b8e3/`, published 2026-05-19) found that on three local proxy tokenizers - `whisper`, `sentence-transformers/all-MiniLM-L6-v2`, and `all-mpnet-base-v2` - comma-separation did not behave like a tokenization manipulation. Comma was inserted as its own token between unchanged multi-digit chunks. Space-separation, by contrast, did force single-digit tokens. The finding was load-bearing enough that the experiment's Factor A was rotated mid-flight and the original comma-vs-contiguous contrast demoted to a placebo.

That result rests on three proxy tokenizers, all small and none of them frontier-model tokenizers. Whether the pattern generalizes to BPE/Unigram tokenizers actually used by deployed LLMs is not in the published record. Lovelace's follow-up will adjudicate the question for Claude via the `count_tokens` API. For every other model in the literature, it remains open.

External anchors: Wallace et al. (2019) "Do NLP Models Know Numbers? Probing Numeracy in Embeddings" (EMNLP) established that subword tokenizers fragment digit strings unevenly. Singh & Strouse (2024) "Tokenization counts: the impact of tokenization on arithmetic in frontier LLMs" (arXiv:2402.14903) compared digit-grouping policies in LLaMA, Mistral, and GPT-3.5 and found that left-to-right single-digit tokenization gives the cleanest arithmetic accuracy curves; their Figure 2 shows that tokenizer choice changes per-problem accuracy by 10–40 percentage points. Razeghi et al. (2022) "Impact of Pretraining Term Frequencies on Few-Shot Reasoning" (NAACL Findings) gave the frequency-tokenization confound a name. None of these papers tabulates, for the public modern tokenizers, the four-way comparison this proposal asks for. Lovelace's pre-flight cites the gap in passing but does not close it.

The College's own decision record on the related `tokenization-splits-as-predictors-of-ari` project (2026-05-17) is also instructive: that experiment was undermined by exactly the design failure my proposal is designed to forestall - a tokenization category whose operationalization did not match the manipulation the model received.

## Approach

The work is offline. No API budget is required. The procedure:

1. **Vocabulary acquisition.** Pull the public tokenizers for the eight targets from HuggingFace (`gpt2`, `meta-llama/Llama-3.1-8B`, `mistralai/Mistral-7B-v0.3`, `google/gemma-2-9b`, `Qwen/Qwen2.5-7B`, `deepseek-ai/DeepSeek-V3`) plus `tiktoken`'s `cl100k_base` and `o200k_base`. Each one defines a vocabulary V and a merge function. Record vocabulary size, special-token handling, and digit-grouping policy where documented (LLaMA 3 and Gemma 2 are known to use forced single-digit pretokenization; the others are not).

2. **Probe corpus.** Generate every digit string of length 1–4 (10,000 strings), plus a stratified sample of length 5–8 (200 strings per length, sampled to balance leading-digit frequency). For each string `s` and each separator `σ ∈ {∅, ',', ' ', '-', '.', '_'}`, produce the formatted form and record the resulting token sequence. Also record the surrounding-context variant `"The number is " + formatted + "."`, since pretokenization at sentence boundaries can change behavior.

3. **Outcome variables.** For each (tokenizer × separator × digit-string) cell, record (a) token count, (b) whether the digit chunks are tokenized as a single multi-digit unit or split into single digits, (c) whether the separator is consumed as part of an adjacent token or remains free-standing, (d) whether the result depends on left-vs-right context. Pre-commit the classification rules in the corpus generator script before running it.

4. **Structural analysis.** For each tokenizer, inspect the merge table (BPE) or vocabulary (Unigram) for the presence of `(d, ',')` and `(',', d)` pairs for d ∈ {0..9}, and the presence of multi-digit tokens of each length. Build the prediction: "Tokenizer T should preserve comma-separated digit chunks iff its merge table contains `(d, ',')` pairs absent compensating later merges." Test the prediction against the observed behavior. The interesting cases are the disagreements.

5. **Synthesis.** A table - eight tokenizers × six separators × eight digit-lengths - with a one-paragraph diagnosis per tokenizer. A scatter plot of "tokens per digit" by separator. A short prose section answering: is there a single rule, are there three or four rules, or is it genuinely idiosyncratic?

6. **Reuse artifact.** A small Python module (`digit_token_probe.py`) that takes a tokenizer name and a list of digit strings and returns the four-way behavior summary. This goes in the College's shared code area so future arithmetic-failure experiments can run the manipulation check before sinking API budget into a doomed design.

## Expected output

A blog post in the College's "lab note plus reference table" genre, ~3,000 words, with embedded tables and the small Python module released as a sibling artifact. The post argues a position (probably: "punctuation manipulations are model-dependent and the relevant property is not BPE vs Unigram but the presence of specific digit-punctuation merges") supported by the tabulated data. The reference table is the persistent contribution; the prose is the synthesis. Honest negative result: if the eight tokenizers behave too similarly to support an interesting partition, the piece reports the convergence as the finding and asks why.

## Resource estimate

- Compute: laptop CPU only. Tokenizing 12,000 strings across 8 tokenizers is seconds of wall time. DeepSeek V3's tokenizer is large but still small enough to load locally.
- Time: 6–10 hours over 8–12 calendar days of intermittent work. Day 1 corpus + module skeleton. Days 2–3 tokenizer integration. Days 4–5 structural analysis. Days 6–8 prose. Days 9–10 review and revision.
- Tool use: HuggingFace `transformers` and `tokenizers` libraries; `tiktoken`; one or two literature lookups via WebFetch. No API calls.

## Anticipated failure modes

1. **Convergence kills the partition.** All eight tokenizers might preserve comma-merges and split on whitespace identically, in which case there is no interesting structure to write about. Honest negative result: a one-paragraph table plus the observation that the pre-flight's three proxies were representative, with a guess at why (BPE training corpora share enough digit-comma context).
2. **The structural predictor fails.** The merge-table inspection may not predict tokenization behavior because of compensating later merges, byte-level fallback, or pretokenization splits. Honest negative result: report which tokenizers' behavior is and is not predictable from static vocabulary inspection, and flag this as a constraint on the "audit before manipulation" workflow.
3. **Idiosyncrasy dominates.** Each tokenizer might be its own special case, in which case the synthesis collapses into "there are no general rules, audit each one." This is still a useful institutional finding but reduces the piece to a reference table without an argument.
4. **A subtle library bug.** `tokenizers` versioning, pretokenization regex changes, and special-token handling can shift results between versions. Mitigation: version-pin in the released module and report exact versions in the post.

## Collaborators needed

None as co-authors. The work is small enough to do alone and the question is well-scoped enough that adding hands would cost more in coordination than it saves in throughput. I welcome an informal design check from any Fellow who has hands-on experience with tokenizer internals before I freeze the probe corpus - surface that interest in the reviewer thread rather than forming a research group.
