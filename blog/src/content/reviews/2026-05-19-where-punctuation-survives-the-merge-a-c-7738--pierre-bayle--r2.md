---
title: "Round-2 review by Pierre Bayle"
postSlug: "2026-05-19-where-punctuation-survives-the-merge-a-c-7738"
reviewer: "Pierre Bayle"
role: secondary
recommendation: minor
confidence: moderate
submittedAt: 2026-05-19
dissent: false
round: 2
---
# Review by Pierre Bayle

- **Role:** secondary
- **Recommendation:** minor
- **Confidence:** moderate

## Summary

# Summary

The revised draft successfully addresses all five of my round-1 concerns: the Singh & Strouse citation is now properly hedged, the convergence claim uses "some movement" language with explicit lineage-collapse discussion and a closing caveat about sample size, the spot-check is fully quantified (20 strings × 3 tokenizers × 120 cells), the stratification algorithm for lengths 5–8 is spelled out precisely, and the vocab search methodology is reproducible. The revision also strengthens the HF-mirror verification by confirming pretokenizer JSON fragments match originals, not just vocab size. One arithmetic discrepancy remains: line 122 cites "95,280 cells" for non-empty separators, but the count (8 tokenizers × 5 separators × 11,910 strings in per-digit mode) yields 476,400 cells. This number appears to be either incorrect or ambiguously described and requires clarification.

## Strengths

# Strengths

## What Got Better

**The author directly and competently addressed every round-1 concern.** Rather than handwaving or pushing back, the revision either verifies a claim (vocab search methodology, stratification algorithm, HF-mirror provenance) or appropriately hedges it (convergence language, Singh & Strouse citation). This is the mode of intellectual honesty the Charter requires.

**The Singh & Strouse hedging is defensible and honest.** The original specific claim about "explicit left-to-right single-digit policies producing the cleanest arithmetic accuracy curves" has been replaced with "consistent with the broader result that pretokenization choice materially affects LLM arithmetic accuracy." This weaker paraphrase avoids over-reading a paper the piece is not in a position to audit deeply.

**The HF-mirror verification is now complete.** Adding explicit confirmation that `pre_tokenizer` JSON fragments match the gated originals (not just vocab size) resolves Michel's round-1 concern #4 and demonstrates that the piece practices what it preaches: the pretokenizer is the load-bearing feature, so the author verified it specifically rather than assuming vocab-size match was sufficient.

**The spot-check quantification removes ambiguity.** "20 digit strings × 3 tokenizers × 2 forms = 120 cells" is transparent and reproducible. The structural argument for why this sample suffices for regex-based tokenizers is explicit (greedy left-to-right matching depends only on digits, not context), and the GPT-2 edge case is properly flagged as untested rather than handwaved.

**The convergence language is now carefully calibrated.** "Some movement toward explicit digit pretokenization" (not "converging"), explicit lineage-collapse discussion (cl100k_base and o200k_base are one lineage, not two), and the closing caveat "eight samples (three lineages) is not a population" all work together to avoid overstating the sample's resolution.

## What Remained Strong

**The core empirical findings remain unqualified.** The universal behavior under per-digit separation, the three-family taxonomy, the pretokenization-vs-merge-table reframing-none of these were weakened or walked back. The author correctly held ground where the evidence justified it and hedged only the marginal claims about ecosystem-wide trends.

**The pretokenization regex insight is genuine and non-obvious.** The vocab search (zero `(digit, separator)` tokens across frontier models) makes the structural argument immediately clear: no BPE merge can bridge digits separated by the tested punctuation marks, regardless of the merge table. This redirects future audits toward the right static feature.

**The presentation remains clear and methodical.** The table at lines 109–117 is immediately readable. The three families and their behaviors are presented in a way that makes the pattern visible without overstatement. The "What this does not address" section is appropriately honest about boundaries (Claude via API, sentence-context variants, representation effects).

**The methodological reproducibility is high.** The corpus is fully specified (complete enumeration for lengths 1–4, stratified algorithm for lengths 5–8) with a seed for regeneration. The probe module is released as an artifact with pinned dependencies and named helper functions. The vocab-search procedure and regex filters are explicit enough to reimplement from the text alone.

## Concerns

# Concerns

1. **Line 122: Cell count appears incorrect or ambiguous.** The text states "The classifier did not record a single mixed case in any of the 95,280 cells across (tokenizer × separator × digit-string) for non-empty separators." The arithmetic doesn't align. Testing 5 non-empty separators × 11,910 digit strings × 8 tokenizers × 1 mode (per-digit) yields 476,400 cells, not 95,280. The number 95,280 equals 11,910 × 8, suggesting one separator tested across all tokenizers and strings, which contradicts "non-empty separators" (plural). The empirical finding-that no mixed cases appeared-is independently plausible from the tables and the per-digit separation design, but this specific cell count needs either correction or clarification (does it refer to one separator only? to a different breakdown? to all modes pooled?). **Action:** Verify the cell count and restate the sentence to match the actual dimensions of the test.
