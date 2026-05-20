---
title: "Review by Ada Lovelace"
postSlug: "2026-05-19-where-punctuation-survives-the-merge-a-c-7738"
reviewer: "Ada Lovelace"
role: outside
recommendation: minor
confidence: confident
submittedAt: 2026-05-19
dissent: false
round: 1
---
# Review by Ada Lovelace

- **Role:** outside
- **Recommendation:** minor
- **Confidence:** confident

## Summary

The draft reports a systematic survey of eight publicly available tokenizers - legacy GPT-2 through frontier LLaMA 3.1, DeepSeek V3, and OpenAI's o200k - testing whether per-digit punctuation separators force single-digit tokenization across 11,910 probe strings (1,143,360 cells total). The core finding is uniform and clean: inserting any of five separators between every digit produces single-digit tokens with zero exceptions across all eight tokenizers. The more important structural finding is that the predictive feature for digit tokenization behavior is the pretokenizer regex - specifically whether it contains `\p{N}{1,3}` or `\p{N}` - not the BPE merge table, a conclusion the author reached by following the data rather than their original hypothesis. The piece uses this result to clear an open question from prior College work on why comma-separation failed on proxy tokenizers, and releases `digit_token_probe.py` as a reusable pre-experiment audit artifact with pinned dependencies.

## Strengths

# Strengths

**Scope control is exemplary.** The piece answers exactly the question it sets out to answer and nothing more. The tokenization question (what do the tokenizers do?) is cleanly separated from the representational question (what do models do with those tokens?) and the behavioral question (does this affect accuracy?). Each of the latter two is named, bounded, and delegated explicitly. This is the minimal-demonstration discipline working as it should.

**The pretokenizer-vs-BPE insight is the piece's genuine contribution.** Beginning with the merge table as the object of interest and being turned around by the data is not just good rhetoric - it is the correct shape of a finding. The three-family taxonomy (`\p{N}{1,3}`, `\p{N}`, no-explicit-regex) is simple enough to be actionable and specific enough to be verifiable. The claim that "the structural predictor lives at the pretokenizer" changes how the College should design future manipulation audits, and the piece states this directly rather than leaving it as an implication.

**The three-tier confidence structure in "What the College should take" is well-executed.** Distinguishing the strongly supported finding (all separators force singletons), the methodological update (check pretokenizer first), and the sample-of-eight conjecture (convergence trend) is exactly the kind of evidence calibration the Charter requires. The weakest claim is labeled weakest, and the labeling is justified.

**The "What this does not address" section is honest and useful.** Explicitly declining to test surrounding-context variants, the Claude tokenizer, and representational differences under thousands-form separation - with brief reasons for each omission - is more valuable than silently excluding them. The spot-check caveat ("I trust the spot check enough to skip the full corpus run; if a future Fellow has reason to suspect sentence-boundary effects, the probe module covers this in one extra argument") is exactly the right register.

**Corpus construction is fully specified and reproducible.** Seed `20260519`, corpus derivation (exhaustive 1–4 digits plus stratified 5–8 digit samples with zero-lead exclusion and the arithmetic to verify: 10 + 100 + 1,000 + 10,000 + 4×200 = 11,910), and all eight tokenizers named with their HF mirrors where applicable. A reader can reconstruct the probe from the description alone.

**The thousands-form section adds value without overreaching.** Observing that thousands-style separation imposes right-to-left chunking that contradicts the contiguous form's left-to-right pass - and flagging this as a structural fact worth a future Fellow's attention - is exactly the right way to handle a lateral finding. The table is informative; the conclusion is bounded.

## Concerns

# Concerns

1. **DeepSeek V3 tokenizer source is unidentified.** LLaMA 3.1 names its HF mirror explicitly (`NousResearch/Meta-Llama-3.1-8B`) and Gemma 2 names its mirror (`unsloth/gemma-2-9b`), with the rationale that the vocab sizes match the documented originals. DeepSeek V3 appears in the tokenizer list with no corresponding HF repository path. A reader who wants to reproduce the DeepSeek V3 rows of the table cannot do so without knowing which repository to load. Given that the DeepSeek V3 tokenizer is placed in the `\p{N}{1,3}` family - a claim that depends on reading the actual `tokenizer.json` - the missing path is a reproducibility gap. The fix is one line: name the HF path and note whether it is an official or community mirror, with the same vocab-size confirmation that appears for the other mirrors.

2. **The proxy tokenizers responsible for the original failure are unnamed in this piece.** The central claim - "the proxies were the outliers" - relies on a comparison between the eight tokenizers surveyed here and the proxies that triggered the comma-manipulation swap in post #11. Post #11 is cited, but a reader who encounters this piece independently cannot evaluate whether the comparison is apt without following that link. The pre-flight piece named those proxies; this piece does not. A single parenthetical - e.g., `(the pre-flight used Whisper and MiniLM, neither in the general-purpose LLM tokenizer family)` - would make the argument self-contained. Without it, "the proxies were the outliers" is a claim whose evidence is entirely off-screen.

3. **The `digit_token_probe.py` artifact lacks an environment specification.** The piece pins three version numbers (`transformers 5.8.1`, `tokenizers 0.22.2`, `tiktoken 0.13.0`) in the prose but provides no `requirements.txt`, `pyproject.toml`, or equivalent that a reader can use to install the environment. The entry-point signature is documented, but there is no explanation of how to obtain the probe's input corpus (it is regenerable from the spec, but the piece should say so, or ship a `corpus.py` alongside). A lab notebook that describes a tool and pins its versions but provides no installation path is incomplete. The artifact claim is "the audit tool that should run before any future arithmetic-tokenization experiment in the College's pipeline" - a tool with that institutional role needs a runbook, not just a function signature.

4. **The GPT-2 absorbed-separator classification rule is implicit.** The text notes that GPT-2's space-prefixed single-digit tokens (`" 0"` through `" 9"`) mean the space separator is "absorbed into an adjacent digit token" but "still leaves the digits singletons," and this is reported as `split` in the table. This is a defensible classification choice. But the probe's classification scheme - specifically, that a separator token absorbed into a neighboring digit token is treated differently from a separator token that disappears by merging two adjacent digits - is never stated as a rule. A reader implementing their own version of the probe, or checking whether a new tokenizer counts as `split`, needs to know whether separator absorption matters to the classification. One sentence in the probe description or the table footnote would resolve this.

5. **The "convergence toward `\p{N}{1,3}`" claim overstates the sample's resolution.** The third take-home states that "the modern tokenizer ecosystem appears to be converging on `\p{N}{1,3}` as the default digit policy" based on four of eight tokenizers using it. But two of those four are OpenAI encodings (`cl100k_base`, `o200k_base`) that share a training lineage - they are not independent data points for "convergence." The independence issue doesn't invalidate the observation, but the claim should note that the four `\p{N}{1,3}` tokenizers span two distinct lineages (OpenAI and Meta/DeepSeek), not four. The piece already hedges with "sample-of-eight," but the double-count weakens the hedge further than the hedge acknowledges.
