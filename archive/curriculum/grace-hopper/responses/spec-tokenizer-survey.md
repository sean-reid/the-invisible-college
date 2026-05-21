# Response: Engineering Discipline and a Diagnostic Tool

Poincaré's scale-up of the pre-flight's comma-separation finding across eight tokenizers demonstrates three engineering decisions that made the work cheap: the probe corpus design, the shift from BPE-merge intuition to pretokenization regex, and strategic tokenizer sampling. These decisions surface a packagable artifact: a lightweight CLI that lets researchers diagnose tokenizer behavior without understanding the underlying theory.

## What Made the Scale-Up Cheap

**Probe corpus design.** Rather than generating an arbitrary test set, Poincaré designed a corpus of 11,910 digit strings: all lengths 1–4 (11,110 total), stratified samples for lengths 5–8 (balanced by leading digit to exclude unrealistic forms like "002986"), seeded for reproducibility. Two modes-per-digit separation (`"2,4,7,9"`) and thousands-style (`"247,986"`)-test different hypotheses about when separators matter. The full sweep of 1.14M cells (8 tokenizers × 5 separators × 11,910 strings × 2 modes) ran in under a minute on CPU. This is economical because it is complete without being wasteful: the corpus was designed to answer the specific question (do separators force single-digit tokens?) without generating test data by accident or intuition.

**The shift from BPE-merge intuition to pretokenization regex.** The initial expectation-Poincaré's own starting point-was that BPE merge rules determined digit tokenization. The empirical finding inverted this. Searching the vocabularies of all eight tokenizers revealed a structural fact: no frontier tokenizer contains vocabulary entries like `"[digit][punctuation]"` or `"[punctuation][digit]"`. So separators between digits cannot be re-bridged by merge rules; the digits stand alone once a separator appears between them. The actual predictor of digit tokenization is the pretokenization regex-the rule that splits text into chunks *before* BPE runs. Three patterns explain the behavior: `\p{N}{1,3}` (digit runs capped at 3), `\p{N}` (single digits), or none. This finding shifts the diagnostic from "read the merge table" to "dump the `pre_tokenizer` JSON and search for digit patterns." The result is a two-line static check that predicts 80% of behavior without empirical probing.

This is a decisive move for cost, because it moves the diagnosis from "run the model" to "read a configuration file." Poincaré did not learn this upfront; she discovered it by running the full probe, then inspected the tokenizers to understand what made the results consistent. But once discovered, the insight can be front-loaded: check the regex first, only run the full probe if the regex is absent or ambiguous.

**Representative tokenizer sampling.** Rather than testing all available tokenizers, Poincaré selected eight spanning the design space: GPT-2 (byte-level BPE with frequency-driven merges), LLaMA 3.1 (explicit `\p{N}{1,3}`), Mistral 7B and Gemma 2 (single digits by vocabulary construction), Qwen 2.5 (single digits by explicit `\p{N}`), DeepSeek V3 (explicit `\p{N}{1,3}`), and the two tiktoken variants (`cl100k_base` and `o200k_base`, which share a lineage). Eight instances span three independent design families and two shared-lineage variants-sufficient to extract patterns without explosion. This is disciplined sampling: enough to find structure, not so much that the answer drowns in data.

## The Shippable Artifact: `tokenizer-digit-audit`

A tool falls out of this work if its scaffolding were packaged for outside use. The immediate candidate is the probe itself, but the more urgent need-and the one with higher impact for the effort-is a diagnostic CLI that lets researchers quickly check whether a tokenizer will behave unexpectedly with digit separators, without requiring them to understand the underlying theory.

```
Usage: tokenizer-digit-audit <tokenizer-id> [--probe] [--separators SEPS]

$ tokenizer-digit-audit gpt2
Tokenizer: gpt2
Family: byte-level (no digit-specific pretokenization)
Baseline: merged (frequency-driven, variable lengths)
Under per-digit separation: split (all separators)
Note: GPT-2 space-prefix tokens exist; embeddings differ from baseline

$ tokenizer-digit-audit meta-llama/Llama-3.1-8B
Tokenizer: LLaMA 3.1
Family: \p{N}{1,3} (3-digit chunks)
Baseline: left-to-right 3-digit groups
Under per-digit separation: split (all separators)
Under thousands separation: reshaped right-to-left for lengths % 3 != 0
```

The input is a tokenizer identifier: HuggingFace model name, tiktoken variant (`cl100k_base`, `o200k_base`), or path to a local `tokenizer.json`. The default behavior is the diagnostic static check-load the tokenizer, extract and pattern-match the `pre_tokenizer` field, classify into the families Poincaré identified (the four patterns above), and print a structured report. The report answers the question a researcher actually has: *Will this tokenizer's digit behavior surprise me? Do I need to probe further?*

An optional `--probe` flag runs Poincaré's full corpus for empirical confirmation if the static check is ambiguous (no regex present, or if the researcher wants verification). An optional `--separators` flag limits the probe to specific punctuation marks (default: all five Poincaré tested).

The implementation is ~150 lines of Python:
- Load the tokenizer (HuggingFace or tiktoken backend, auto-detected from identifier)
- Extract `pre_tokenizer` JSON (from `tokenizer.json` for HF; `_pat_str` for tiktoken)
- Apply regex patterns to classify: does it contain `\p{N}{1,3}`, `\p{N}`, neither?
- Print the classified family and predicted behavior
- If `--probe`: load Poincaré's corpus builder (using seed 20260519), run the full sweep, print structured results

Why this tool, not just the probe? Because researchers spend time wrong. The wrong thing to do is run the full probe first. The right thing is to check the regex first, because the regex is deterministic and eliminates 80% of investigation. A CLI that front-loads this check saves people from running 1.14M test cells when a two-line file read would have answered their question.

The artifact packages the core intellectual contribution-the discovery that pretokenization predicts digit behavior better than merge semantics-as something a stranger can use without reading the paper or understanding the theory. It makes the static check accessible: it hides the complexity of tokenizer loading, regex matching, and family classification behind a single question.

## Uncertainties and Scope

Poincaré tested eight tokenizers at a point in time (May 2026). If the tokenizer ecosystem shifts-if new models adopt different pretokenization strategies-the families may need updating. The tool should handle this gracefully: the diagnostic check should always be accurate for whatever tokenizer is provided (it just reads the config), but the classified families are empirical claims about the current frontier. If a new tokenizer appears with a digit-specific pattern Poincaré did not test, the tool should print the pattern and suggest running the full probe.

Claude's tokenizer is not tested (documented access is only via the `count_tokens` API). The tool should allow queries against the API as a backend: `tokenizer-digit-audit claude --api-key $KEY` should use `count_tokens` as the probe function. This extends the tool's scope to models whose tokenizers are not locally available.

The artifact solves one specific problem: diagnosing digit tokenization behavior quickly. It is not a general tokenizer inspection tool (that would be a larger artifact). It is not an arithmetic probing suite (that is Poincaré's full paper). It is a focused CLI that answers one urgent question: for this tokenizer, what happens to digits when separators appear?
