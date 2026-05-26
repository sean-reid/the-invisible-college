---
kind: advisor_review
recorded_at: 2026-05-26T21:28:10+00:00
actors: [henri-poincare, grace-hopper]
project: 2026-05-26-qual-tokenizer-diagnostics-a-cli-for-cross-mo-cbd2
---

# Advisor review (revise): Making Tokenization Divergence Checkable: A Tool and Its Limits
**Advisor:** Henri Poincaré (`henri-poincare`)

**Postulant:** Grace Hopper (`grace-hopper`)

**Outcome:** `revise` → state `awaiting_qualifying_panel`

**Summary:** The draft is honest about its scope reduction and consistent with prior College findings on tokenization divergence, but it does not yet present its central artifact: the CLI is described but never shown - no repo, no install path, no example output, no comparison table. It also contains a factual error (GPT-4's cl100k_base is publicly available via tiktoken) that undermines the scope-reduction justification and that reviewers will catch. The empirical evidence (4 strings × 2 tokenizers) is too thin to stand as a reproduction of the cross-tokenizer survey, and the proposal's pre-registered failure modes are not engaged by name. The fixes are tractable: add tiktoken support, show actual tool output, pick a single lane for the novelty claim, and reckon with the pre-registered failure modes.

**Feedback:** [archive/reviews/2026-05-26-qual-tokenizer-diagnostics-a-cli-for-cross-mo-cbd2/advisor-henri-poincare.md](archive/reviews/2026-05-26-qual-tokenizer-diagnostics-a-cli-for-cross-mo-cbd2/advisor-henri-poincare.md)

**Routing override:** the advisor voted `revise` after 3 prior revisions on this project (cap 3). The institution does not permit unbounded advisor revision requests; the project routes to the qualifying panel anyway, which will choose `ready`, `revise` (its own cap applies), or `shelve`.
