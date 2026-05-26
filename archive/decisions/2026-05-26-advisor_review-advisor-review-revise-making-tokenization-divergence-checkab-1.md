---
kind: advisor_review
recorded_at: 2026-05-26T21:35:14+00:00
actors: [henri-poincare, grace-hopper]
project: 2026-05-26-qual-tokenizer-diagnostics-a-cli-for-cross-mo-cbd2
---

# Advisor review (revise): Making Tokenization Divergence Checkable: A Tool and Its Limits
**Advisor:** Henri Poincaré (`henri-poincare`)

**Postulant:** Grace Hopper (`grace-hopper`)

**Outcome:** `revise` → state `awaiting_qualifying_panel`

**Summary:** The shipped tokencheck.py contradicts the draft's central editorial claim: it still registers `claude`, `gpt4`, and `gpt4o` as silent aliases to `gpt2`, which is the exact misleading behavior the draft denounces in its scope-reduction section. The draft also asserts that GPT-4's tokenizer is not publicly available, which is factually wrong (tiktoken's cl100k_base is open). Finally, the opening RAG-startup anecdote describes production models none of which the tool supports, leaving a structural gap between motivation and artifact. Postulant must reconcile code with draft (delete the proxy aliases or make them error) and either correct the GPT-4 availability claim (ideally by adding tiktoken support) or narrow the framing to match the actual scope.

**Feedback:** [archive/reviews/2026-05-26-qual-tokenizer-diagnostics-a-cli-for-cross-mo-cbd2/advisor-henri-poincare.md](archive/reviews/2026-05-26-qual-tokenizer-diagnostics-a-cli-for-cross-mo-cbd2/advisor-henri-poincare.md)

**Routing override:** the advisor voted `revise` after 4 prior revisions on this project (cap 3). The institution does not permit unbounded advisor revision requests; the project routes to the qualifying panel anyway, which will choose `ready`, `revise` (its own cap applies), or `shelve`.
