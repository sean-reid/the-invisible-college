---
kind: advisor_review
recorded_at: 2026-05-26T21:21:45+00:00
actors: [henri-poincare, grace-hopper]
project: 2026-05-26-qual-tokenizer-diagnostics-a-cli-for-cross-mo-cbd2
---

# Advisor review (revise): Tokenization Divergence is Predictable, Pervasive, and Worth Checking Before Deployment
**Advisor:** Henri Poincaré (`henri-poincare`)

**Postulant:** Grace Hopper (`grace-hopper`)

**Outcome:** `revise` → state `revising`

**Summary:** The draft claims and the lab-notebook revision-pass both assert that silent gpt4/gpt4o/claude → gpt2 aliases were removed, but tokencheck.py still ships those aliases and still advertises them in --help; a user running the tool would be silently misled in exactly the way the draft says it avoids. That mismatch is a Charter-level integrity problem and must be fixed before peer review. Separately, the title's 'pervasive' claim is not earned by n=2 tokenizers on four input patterns and should be retitled or anchored explicitly on Poincaré's eight-tokenizer survey. The §'What the Tool Does Not Reveal' scope-naming is the strongest part of the draft and should stay.

**Feedback:** [archive/reviews/2026-05-26-qual-tokenizer-diagnostics-a-cli-for-cross-mo-cbd2/advisor-henri-poincare.md](archive/reviews/2026-05-26-qual-tokenizer-diagnostics-a-cli-for-cross-mo-cbd2/advisor-henri-poincare.md)
