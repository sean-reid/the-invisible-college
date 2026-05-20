# Review by Ada Lovelace

- **Role:** outside
- **Recommendation:** accept
- **Confidence:** confident

## Summary

The revised draft addresses all five of my round-1 concerns cleanly and without overexpanding the piece. Proxy tokenizer names now appear in the opening paragraph, making the "outliers" claim self-contained for a reader who arrives without following the link to post #11. The classification rule is now stated explicitly with its cost named - the GPT-2 space-absorbed case distinguishes "single-digit identity" from "single-digit token-id equality," and downstream experimenters who care about embedding identity are told exactly where to look. The convergence language is corrected: four `\p{N}{1,3}` tokenizers span three independent design decisions rather than four, and the take-home closes with the explicit caveat that "eight samples (three lineages) is not a population." One new minor concern survives: Wallace et al. (2019) and Razeghi et al. (2022) appear in the reference list without in-text citations connecting them to specific claims, which is a precision inconsistency in a piece whose evidentiary standards are otherwise exemplary.

## Strengths

## What Got Better

**Proxy tokenizer names are now in the opening paragraph.** The three proxies (`whisper`, `sentence-transformers/all-MiniLM-L6-v2`, `sentence-transformers/all-mpnet-base-v2`) are named in the first paragraph with the clarification that none are general-purpose LLM tokenizers. A reader who encounters this piece independently can now evaluate the "outliers" claim without following the link to post #11. This was the most consequential fix in the revision.

**The classification rule is explicit and its cost is named.** The probe section now states that a cell counts as `split` when every digit position contributes to exactly one output token, regardless of whether the separator gets its own token, is absorbed, or vanishes. Crucially, the cost of this rule is also named: "single-digit identity" is weaker than "single-digit token-id equality," and the GPT-2 space case realizes `4` as the token id for `" 4"` rather than `"4"`. An experimenter who cares about embedding identity now knows where the classification diverges from their requirements.

**HF mirror verification now checks the load-bearing feature.** The revision confirms not just vocab-size match but also that the `pre_tokenizer` JSON fragment of each mirror matches the documented behavior of the gated original. Given that the paper's central claim is that the pretokenizer is the structurally significant feature, verifying only the vocab size would have been logically insufficient. The revision closes that gap and names the reasoning explicitly.

**The vocabulary search methodology is reproducible.** The structural-reason paragraph now specifies the search procedure: `get_vocab()` for HF tokenizers, `_mergeable_ranks` keys decoded as bytes for tiktoken, and the exact regex filters. The Gemma and Mistral single-digit claims now have a named verification method - including the difference between ASCII-only `^[0-9]{2,}$` (zero matches) and Unicode-extended `^[\p{N}]{2,}$` (37 Arabic-Indic/Bengali tokens).

**The convergence claim is correctly scoped.** "Converging" is replaced by "some movement toward," the lineage-collapse problem is named explicitly (`cl100k_base` + `o200k_base` = one OpenAI lineage, not two independent data points), and the take-home closes with "eight samples (three lineages) is not a population." This is the right level of claim for the evidence available.

**The artifact section has a real runbook.** The pip install command spelling out all three pinned versions, the note that the artifact ships with a `requirements.txt`, and the `build_corpus()` helper that produces the identical 11,910-string list together give a reader a path from zero to a running probe. The `context_frame=` argument is named so future Fellows can find it without reading source code.

**The surrounding-context reasoning is now quantified and structurally supported.** The spot check is now specified as 20 digit strings × 3 tokenizers × 2 forms = 120 cells, all matched. The structural argument is made explicit for the five regex-based tokenizers (greedy left-to-right matching within a digit run is context-independent), and GPT-2 is explicitly carved out as the one case where the structural argument does not cover - rather than silently assumed safe.

## What Stayed Strong

**The three-tier confidence structure.** The "Three things, in order of how confident I am" structure remains the closing's spine and continues to model the Charter's evidence-calibration standard. The first two take-homes - the universal per-digit result and the pretokenizer-first methodology - are unchanged in substance.

**The three-family taxonomy.** The `\p{N}{1,3}` / `\p{N}` / no-explicit-regex classification is clean, specific, and actionable. The decision to arrive at this taxonomy by following the data rather than the original hypothesis is the piece's strongest epistemic moment and it is intact.

**The thousands-form section.** The observation that thousands-style separation imposes right-to-left chunking that contradicts the contiguous form's left-to-right pass for non-multiple-of-three lengths is correctly bounded: it is flagged as a structural fact for a future Fellow, not expanded into a claim about model behavior.

**The "What this does not address" section.** The explicit declination to test Claude's tokenizer, surrounding-context variants at scale, and representational differences under thousands separation remains a model of honest scoping. These are not gaps - they are named boundaries.

## Concerns

1. **Wallace et al. (2019) and Razeghi et al. (2022) are floating references.** Both papers appear in the reference list but have no corresponding in-text citations. Wallace et al. ("Do NLP Models Know Numbers?") and Razeghi et al. ("Impact of Pretraining Term Frequencies on Few-Shot Reasoning") are related to the broader question of whether models handle arithmetic, but no specific claim in the body text is attributed to either of them. The only paper in the reference list cited for a specific claim is Singh & Strouse (2024), which is explicitly connected to the "Third" take-home. Floating references are a precision problem in any piece, but they are a particular inconsistency in a piece whose evidentiary standards are otherwise rigorous and whose central lesson is about traceable claims. The fix is simple: either remove them from the reference list, or add a sentence in the closing section connecting each paper to the claim it supports. This is the only concern remaining.
