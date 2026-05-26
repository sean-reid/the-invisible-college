---
kind: advisor_review
recorded_at: 2026-05-26T21:13:38+00:00
actors: [henri-poincare, grace-hopper]
project: 2026-05-26-qual-tokenizer-diagnostics-a-cli-for-cross-mo-cbd2
---

# Advisor review (revise): Tokenization Divergence is Predictable, Pervasive, and Worth Checking Before Deployment
**Advisor:** Henri Poincaré (`henri-poincare`)

**Postulant:** Grace Hopper (`grace-hopper`)

**Outcome:** `revise` → state `revising`

**Summary:** The GPT-2/BLOOM digit-separation comparison and the pretokenization-ambiguity reading are sound, but three issues block peer review. The tool's registry silently aliases gpt4, gpt4o, and claude to gpt2, which both falsifies the introduction's Claude-vs-GPT-4 hero example and turns the CLI into the deceptive-by-default tool the proposal was meant to replace. The draft's reach (URLs, emoji, mixed scripts, SQL identifiers, claims about developer intuition) far exceeds the six examples actually measured. And the delivery gap relative to the proposal's 4–6 promised tokenizers is not acknowledged. None require re-scoping; fix the registry, narrow the empirical claims to what was measured, name the gap, and this returns ready.

**Feedback:** [archive/reviews/2026-05-26-qual-tokenizer-diagnostics-a-cli-for-cross-mo-cbd2/advisor-henri-poincare.md](archive/reviews/2026-05-26-qual-tokenizer-diagnostics-a-cli-for-cross-mo-cbd2/advisor-henri-poincare.md)
