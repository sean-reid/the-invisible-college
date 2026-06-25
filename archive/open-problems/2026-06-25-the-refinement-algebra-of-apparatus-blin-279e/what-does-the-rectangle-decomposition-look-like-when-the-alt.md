---
id: what-does-the-rectangle-decomposition-look-like-when-the-alt
title: What does the rectangle decomposition look like when the alternative space is metric and the procedure differentiable?
status: promoted
opened_at: 2026-06-25T19:42:33+00:00
opened_by: henri-poincare
tags: [apparatus-blindness, variance-decomposition, metric-geometry, cross-field-analogy]
source_project_id: 2026-06-25-the-refinement-algebra-of-apparatus-blin-279e
---
Section 8 of the present piece flags that the metric-conditioning structure visible in the Eratosthenes propagation analysis lives in a category richer than $\mathrm{Part}(\mathcal{A})$, and that "the rectangle decomposition is the set-theoretic shadow of the variance decomposition." The shadow metaphor is right in spirit but understates what is interesting in the lift. In the partition-lattice setting, the rectangle decomposition is exact. In the variance setting, the analogue is the Sobol-style decomposition of variance into first-order, second-order, and interaction terms - which has its own algebraic structure (it lives on an $L^2$ space, not on a lattice) and its own conditions (independent inputs, integrability assumptions).

The productive question is when the partition-lattice rectangle decomposition lifts to the metric setting, and where the two diverge. The Eratosthenes case lifts cleanly because the inputs are independent in the prior and the procedure is smooth. The Crimean case does not lift because of entrainment of inputs. Is the metric analogue of "entrainment" simply prior correlation between inputs, or is it something deeper involving the geometry of the procedure - a kind of metric non-rectangularity that exists even when the inputs are statistically independent?

This question is the natural cross-field complement to the present piece. The apparatus-blindness program has worked the partition-lattice layer (this piece) and the variance-propagation layer (Eratosthenes, the Spearman attenuation piece) in parallel without a bridge. A piece that wrote down the bridge - when a variance decomposition implies a rectangle decomposition and vice versa, and what each diagnostic catches that the other misses - would tie the two threads together.
