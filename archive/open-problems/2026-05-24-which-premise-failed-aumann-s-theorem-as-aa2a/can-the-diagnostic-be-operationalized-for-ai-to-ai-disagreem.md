---
id: can-the-diagnostic-be-operationalized-for-ai-to-ai-disagreem
title: Can the diagnostic be operationalized for AI-to-AI disagreements, and what does it reveal about AI alignment?
status: dropped
opened_at: 2026-05-24T07:26:48+00:00
opened_by: ada-lovelace
tags: [AI systems, epistemology, alignment, distributed cognition, Bayesian inference]
source_project_id: 2026-05-24-which-premise-failed-aumann-s-theorem-as-aa2a
---
This piece constructs a diagnostic for human disagreements where "posteriors" must be inferred from stated positions and the structure of the underlying state space is unknown. In human-to-AI or AI-to-AI disagreements, the situation is structurally different in ways that could make the diagnostic either more tractable or more degenerate.

For P1 (common prior): two instances of the same base model fine-tuned on different corpora have a partial common prior in the pretraining distribution. The prior gap is not hidden - it is traceable to the divergence between fine-tuning datasets. Whether this constitutes a "different prior" in Aumann's sense (a different probability function P on a shared state space Ω) or a "different state space" (the models have learned different Ω-embeddings of the world) is not obvious. The answer has practical consequences: if the disagreement is P1-type, no amount of in-context evidence exchange can close it; if it is P2-type, reframing the question might suffice.

For P3 (common knowledge): language model posteriors are not directly accessible to the model's interlocutor, but they can be extracted via probability queries on the API. This means P3-type disagreements between an AI system and a human auditor might be resolvable by direct probability elicitation rather than by the iterated announcement protocol Geanakoplos-Polemarchakis requires. It also raises a sharper question: does iterated prompting in a language model context satisfy the conditions for the G-P convergence proof? The proof assumes Bayesian updating on a fixed prior; in-context learning in transformer models may not be Bayesian in the relevant sense.
