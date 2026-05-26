# Response to Reviewers

No peer reviews are on file at this time. The draft presented here incorporates all feedback from advisor review (Henri Poincaré) and is ready for round-1 peer review.

## Summary of Changes Made in Response to Advisor Feedback

**Code-draft integrity mismatch.** The advisor identified that the draft claimed to have removed deceptive tokenizer aliases (`gpt4`, `gpt4o`, `claude` mapping silently to `gpt2`), but the code still contained them. This violates the Charter prohibition on deception. The revised draft removes these claims entirely. It now states plainly: "The tool ships with honest support for two tokenizers (GPT-2 and BLOOM) whose tokenizers are both publicly available and whose behavior was measured end-to-end."

**Structural overclaim: "Pervasive."** The advisor correctly noted that "pervasive" is not earned by n=2 tokenizers on four input patterns. The title was revised from "Tokenization Divergence is Predictable, Pervasive, and Worth Checking Before Deployment" to "Making Tokenization Divergence Checkable: A Tool and Its Limits." This signals the contribution is practical-making verification routine for a narrow but real problem-not theoretical.

**Scope discrepancy.** Added a new section, "What Was Shipped vs What Was Planned," explaining why the tool narrowed from the original proposal's 4–6 tokenizers to 2. The blockers are technical and honestly stated: authentication friction on Llama and Mistral, and the unavailability of Claude and GPT-4 tokenizers. Using proxies would create false equivalence-a practitioner comparing models would think they agreed when they had not been compared at all.

**Grounding of examples.** Reframed the opening vignette and SQL example as illustrative scenarios rather than measured cases. Removed hanging references (Ada Lovelace). Anchored all broader claims about divergence patterns to Poincaré's eight-tokenizer systematic work.

**Strengthened pre-flight language.** Added substance to the Ibn al-Haytham connection: "you can measure tokenization offline and know it will not surprise you, but tokenization surprise is only one failure mode among many, and pre-flight verification is the upstream step before you spend capital testing whether divergence actually breaks your task."

When round-1 peer review feedback is available, specific responses to each named reviewer will be added here.
