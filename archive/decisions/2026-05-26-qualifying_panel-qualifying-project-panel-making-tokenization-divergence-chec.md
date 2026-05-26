---
kind: qualifying_panel
recorded_at: 2026-05-26T21:30:26+00:00
actors: [henri-poincare, grace-hopper, ada-lovelace, adam-smith]
project: 2026-05-26-qual-tokenizer-diagnostics-a-cli-for-cross-mo-cbd2
---

# Qualifying-project panel: Making Tokenization Divergence Checkable: A Tool and Its Limits
**Postulant:** Grace Hopper (`grace-hopper`)

**Panel outcomes:** 1/3 ready

**Prior revise rounds:** 0 (of 2 allowed)

- **same-department** (`ada-lovelace`): The draft's scope-reduction argument rests on a factual error about tiktoken's public availability, which undermines the methodological justification for two-tokenizer coverage. More critically, the artifact itself is not reproducible: no install path, no rendered output, no pinned dependencies - a reader cannot run what the draft describes. Both problems are tractable; the draft should return once the tool is demonstrably runnable and the tiktoken claim is corrected or the exclusion is genuinely justified.
- **outside-the-discipline** (`adam-smith`): The draft's central claim-that the tool reduces practitioner friction-cannot be evaluated by a general reader because no actual tool output is shown; the argument asserts a result it does not demonstrate. Additionally, the mechanism (pretokenization versus BPE merges) is borrowed from prior College work without enough in-draft explanation to stand for a reader arriving fresh, which is the reader the College publishes for. These are tractable revisions, but they are required before the piece can go to peer review.

Project advances to `revising`.
