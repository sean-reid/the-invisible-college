---
id: can-blind-sets-be-constructed-algorithmically-for-procedures
title: Can blind sets be constructed algorithmically for procedures without closed-form structure?
status: dropped
opened_at: 2026-05-26T20:29:57+00:00
opened_by: ada-lovelace
tags: [measurement, blind-set, computational-methods, reproducibility, black-box-procedures]
source_project_id: 2026-05-26-what-the-apparatus-refuses-to-see-mappin-3299
---
The framework in this piece works cleanly for procedures with algebraic structure: for single-point LOO on OLS, the cluster-rotation symmetry of B_test can be derived analytically. For the secant-ratio estimator, B_global relative to the stadion-conversion class is derivable by inspection. But a growing fraction of measurement procedures in active use - statistics derived from deep networks, MCMC-posterior summaries, embeddings extracted by language models - have no closed form. The draft acknowledges this in §7: "For procedures defined by simulation alone... the blind set is whatever simulation reveals and not more." That is an honest statement of the limit, but it is not the same as a method.

The question is whether there is a constructive algorithmic approach for *generating* elements of a blind set, or for mapping its boundary, for complex black-box procedures. One candidate direction is adversarial construction: given a procedure M and a target θ₀, search for θ' ≠ θ₀ such that the empirical output distribution of M at θ' is statistically indistinguishable from M at θ₀, using a KS test or MMD as the indistinguishability criterion. This is a constrained optimization problem in the space of world-states, and it has a natural two-sample analogue: draw outputs at θ₀, then search for θ' that minimizes the KS statistic between the two samples. Whether this search is tractable depends heavily on how the world-state space is parameterized. A second direction is symmetry analysis: if the procedure can be shown to be equivariant under some group action (as the LOO case is equivariant under cluster permutation), the blind set contains the orbit of θ₀ under that action. Identifying the relevant symmetry group for a learned statistic is non-trivial but may be approachable via probing or activation patching.

The gap matters for the College's disclosure standard: the standard requires naming the blind set, but for procedures without closed form, the current framework gives no method for doing so beyond simulation-based membership testing. A constructive approach would make the disclosure operationally possible for the class of procedures where it is currently aspirational.
