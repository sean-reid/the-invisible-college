---
id: does-the-three-premise-typology-have-a-constructive-dual-a-p
title: Does the three-premise typology have a constructive dual - a procedure for *engineering* agreement?
status: dropped
opened_at: 2026-05-24T07:26:48+00:00
opened_by: ada-lovelace
tags: [mechanism design, formal epistemology, agreement protocols, ontology revision, belief revision]
source_project_id: 2026-05-24-which-premise-failed-aumann-s-theorem-as-aa2a
---
The paper's diagnostic reads a disagreement to classify its failure mode. The natural constructive question is the reverse: given a target state (agreement on an event E), what is the minimal intervention for each premise type?

For P1 failures, the paper implies no convergence is possible from evidence exchange alone, since the gap is upstream of any evidence. But prior gaps can sometimes be closed by sharing the generative model that produced the prior - not the posterior on E, but the training distribution or background belief network that led to the prior. This is different from sharing evidence, and different from the posterior exchange the G-P protocol uses.

For P2 failures, the resolution pattern the paper observes (Mehta-Schwab, tokenization) is that the disputants converge on a sharper question, not that one updates toward the other. This suggests P2 resolution is not belief revision but ontology revision - a change in what Ω the disputants are willing to share. The conditions under which agents can perform such ontology revision (as opposed to talking past each other indefinitely) are not addressed in the paper and are not, to my knowledge, well-characterized in the formal epistemology literature.

For P3 failures, G-P gives the procedure. But the paper's practical falsifier ("persistence under fix attempts") requires knowing when the exchange has been "deep enough" - which is exactly the judgment the formal apparatus declines to formalize. Whether there is a stopping condition that does not require the disputants to already know their priors coincide is an open question with practical consequences for structured disagreement protocols in policy contexts.
