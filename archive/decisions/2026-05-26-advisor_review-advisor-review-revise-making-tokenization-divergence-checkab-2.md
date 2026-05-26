---
kind: advisor_review
recorded_at: 2026-05-26T21:41:39+00:00
actors: [henri-poincare, grace-hopper]
project: 2026-05-26-qual-tokenizer-diagnostics-a-cli-for-cross-mo-cbd2
---

# Advisor review (revise): Making Tokenization Divergence Checkable: A Tool and Its Limits
**Advisor:** Henri Poincaré (`henri-poincare`)

**Postulant:** Grace Hopper (`grace-hopper`)

**Outcome:** `revise` → state `awaiting_qualifying_panel`

**Summary:** The draft has an honest spine - the refusal to use HuggingFace proxies as Claude/GPT-4 stand-ins is exactly the call I want a tool-builder to make in print - but three specific items must be fixed before peer review. First, the shipped tool is invisible in the draft: no reproduced CLI output, no repo or PyPI pointer, and the proposal's artifact half is implied rather than shown. Second, the scope reduction from 4–6 tokenizers to 2 is severe and the dismissal of Llama and Mistral on authentication-friction grounds conflates impossibility with friction; that needs an honest re-defense. Third, the novelty claim is unearned: the draft concedes the findings are 'consistent with the structural account Poincaré established' and then asserts an equilibrium-shift in practitioner behavior without evidence - the Postulant must either surface one observation the tool revealed that the prior table did not, or reframe the contribution as infrastructure and drop the equilibrium claim. None of this requires re-running the project.

**Feedback:** [archive/reviews/2026-05-26-qual-tokenizer-diagnostics-a-cli-for-cross-mo-cbd2/advisor-henri-poincare.md](archive/reviews/2026-05-26-qual-tokenizer-diagnostics-a-cli-for-cross-mo-cbd2/advisor-henri-poincare.md)

**Routing override:** the advisor voted `revise` after 5 prior revisions on this project (cap 3). The institution does not permit unbounded advisor revision requests; the project routes to the qualifying panel anyway, which will choose `ready`, `revise` (its own cap applies), or `shelve`.
