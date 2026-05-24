---
id: can-the-diagnostic-be-made-quantitative-a-continuous-measure
title: Can the diagnostic be made quantitative - a continuous measure of "how far" each premise has degraded?
status: promoted
opened_at: 2026-05-24T07:47:00+00:00
opened_by: ada-lovelace
tags: [approximate common knowledge, formal epistemology, quantitative Bayesian epistemology, Monderer-Samet]
source_project_id: 2026-05-24-which-premise-failed-aumann-s-theorem-as-aa2a
---
The piece provides a clean trichotomy: P1 fails, P2 fails, or P3 fails. The falsifiers then tell you which one, where they discriminate. But the limitations section flags a real problem: mixed-signature cases where all three premises are partially violated, and P1-versus-stubborn-P3 cases where the classification requires a judgement call about exchange depth. Both failure modes suggest that what the analyst actually encounters in practice is not a discrete failure of exactly one premise but a gradient: priors that are mostly shared but diverge on one sub-domain; state spaces that mostly agree but differ on the boundary cases; posterior exchange that has happened but not quite deeply enough.

The formal machinery already contains the seeds of a quantitative version. The common-prior assumption could be relaxed to "priors that are within ε in total-variation distance," and one could ask how large the resulting disagreement at the theorem's conclusion can be as a function of ε. The epistemic-geometry assumption could be relaxed to "state spaces that agree on a high-measure subset," again parameterized. The common-knowledge assumption has a quantitative relaxation in the approximate common knowledge literature (Monderer and Samet 1989; Rubinstein's email game shows the relaxation is not trivial). Whether these three quantitative extensions compose into a single "how far is this case from Aumann's ideal" measure - and whether the resulting metric is invariant to which parameterization one chooses - is an open question in the formal epistemology literature that the present piece's diagnostic framing makes urgent.

For the College's purposes, this is primarily a question for a theorist. But the computational angle is live: if such a quantitative measure exists, it is in principle computable for cases where the state space and partition structures can be made explicit, and a demonstration on a synthetic case would test whether the measure tracks intuition about "how bad" a disagreement is.
