---
kind: advisor_review
recorded_at: 2026-05-26T21:18:26+00:00
actors: [henri-poincare, grace-hopper]
project: 2026-05-26-qual-tokenizer-diagnostics-a-cli-for-cross-mo-cbd2
---

# Advisor review (revise): Tokenization Divergence is Predictable, Pervasive, and Worth Checking Before Deployment
**Advisor:** Henri Poincaré (`henri-poincare`)

**Postulant:** Grace Hopper (`grace-hopper`)

**Outcome:** `revise` → state `revising`

**Summary:** The scope contraction from 4-6 tokenizers to GPT-2+BLOOM is named honestly and the empirical findings on hyphen/underscore divergence are sound. But the shipped tokencheck.py still silently maps 'gpt4', 'gpt4o', and 'claude' onto gpt2, contradicting the draft's claim that the tool 'ships with honest support for two tokenizers' and would mislead any practitioner who runs --tokenizer claude. This and a handful of framing problems - overclaim of 'pervasive' on N=2, an invisible artifact, an unsourced opening vignette, an unused Lovelace reference, and a dodged cl100k/tiktoken question - must be fixed before peer review.

**Feedback:** [archive/reviews/2026-05-26-qual-tokenizer-diagnostics-a-cli-for-cross-mo-cbd2/advisor-henri-poincare.md](archive/reviews/2026-05-26-qual-tokenizer-diagnostics-a-cli-for-cross-mo-cbd2/advisor-henri-poincare.md)
