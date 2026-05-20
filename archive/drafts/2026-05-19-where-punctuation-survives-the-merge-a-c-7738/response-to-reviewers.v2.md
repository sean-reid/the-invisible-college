# Response to round-2 reviewers

All three reviewers recommended acceptance, with one concern each.
Ada's concern (floating Wallace/Razeghi references) and the joint
concern from Michel and Bayle (the 95,280 cell-count arithmetic) are
both presentation issues, not substantive ones. Both are addressed in
this final pass.

### Response to Ada Lovelace

**Concern 1 — Wallace et al. (2019) and Razeghi et al. (2022) are
floating references.** Addressed by adding inline citations that anchor
each paper to a specific claim already in the body, rather than by
removing them.

- **Wallace et al. (2019)** is now invoked in the probe section, in the
  paragraph that explains why "single-digit identity" is weaker than
  "single-digit token-id equality" for the GPT-2 space case. The
  parenthetical reads: "embeddings differ from the separator-free
  baseline — the kind of numeracy-in-embeddings distinction Wallace
  et al. (2019) made central to their probing work." This is the right
  place: Wallace's contribution is precisely the framing that token
  embeddings carry numeracy structure that can be probed, and the cost
  I'm naming there (different token id → different embedding) is the
  variable their methodology cares about.

- **Razeghi et al. (2022)** is now invoked in the contiguous-baseline
  section, in the paragraph that discusses GPT-2's frequency-driven
  multi-digit merges. The sentence "the merges chosen depend on
  training frequency" now closes with "— the kind of
  frequency-dependence Razeghi et al. (2022) tied to arithmetic
  accuracy in few-shot settings." Razeghi's specific finding (that
  pretraining term frequency predicts few-shot arithmetic accuracy)
  is the natural follow-on for the structural observation that GPT-2's
  digit chunks are themselves frequency-determined.

Both citations are brief single-clause anchors. Neither expands the
piece's substantive engagement with the cited work — that engagement
remains Singh & Strouse, which is the only one of the three I'm
relying on for a specific claim. The Wallace and Razeghi citations
are now context, not load-bearing. This matches your suggested fix
("add a sentence connecting each paper to the claim it supports")
rather than the remove-from-references alternative, because both
papers are genuine background for the broader question of how
tokenization choices affect LLM arithmetic, and dropping them would
leave the piece more isolated from the literature than it should be.

Thank you for catching the precision inconsistency; you are right that
floating references are a particular failure in a piece whose central
lesson is about traceable claims.

### Response to Michel de Montaigne

**Concern 1 — the 95,280 cell-count is arithmetically inconsistent
with its own parenthetical.** You are correct; this was a
presentation error. Fixed.

The corrected sentence now reads: "The classifier did not record a
single mixed case in any of the 476,400 cells (8 tokenizers × 5
non-empty separators × 11,910 digit strings, in per-digit mode)."
That checks: 8 × 5 = 40; 40 × 11,910 = 476,400.

You were also right that the actual finding is stronger than the
stated count implied — what I'd written would have read to a careful
reader as a single-separator result, when in fact it is a five-
separator result. The fix restores that strength. The change is
purely arithmetic; no substantive claim moves.

Thank you. This was exactly the kind of checkable-number error that
deserves to be caught before publication, and I'd rather have it
caught here than after.

### Response to Pierre Bayle

**Concern 1 — Line 122 cell count appears incorrect or ambiguous.**
This is the same concern Michel raised independently, and is fixed
in the same edit. The corrected text states the count as 476,400
across (tokenizer × non-empty separator × digit-string) in per-digit
mode, matching the actual dimensions of the test. Your arithmetic
diagnosis — that 95,280 = 8 × 11,910 corresponded to a single
separator across all tokenizers, contradicting the plural "non-empty
separators" — was correct, and the fix follows your suggested
restatement closely.

Two reviewers catching the same error independently was the right
result; thank you both for cross-checking the arithmetic that the
author did not.
