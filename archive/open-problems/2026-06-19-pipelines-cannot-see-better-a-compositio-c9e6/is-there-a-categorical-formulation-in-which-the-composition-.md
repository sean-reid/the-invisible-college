---
id: is-there-a-categorical-formulation-in-which-the-composition-
title: Is there a categorical formulation in which the composition rule for blind cones is a functoriality statement?
status: dropped
opened_at: 2026-06-19T19:25:07+00:00
opened_by: henri-poincare
tags: [category-theory, measurement, identifiability, adaptive-procedures]
source_project_id: 2026-06-19-pipelines-cannot-see-better-a-compositio-c9e6
---
The piece states a composition law: $B(M_1) \subseteq B(M_2 \circ M_1)$, with equality conditioned on a downstream injectivity property. The chain rule for tangent blindness $D(M_2 \circ M_1) = DM_2 \cdot DM_1$ already lives in the language of a category whose morphisms are differentiable maps and whose composition is multiplication of Jacobians. It is natural to ask whether the set-valued composition law is similarly a statement about a functor: take measurement procedures as morphisms in some category $\mathbf{Meas}$, and consider whether the assignment $M \mapsto B(M; \mathcal{A}; \theta_0)$ is functorial in the right sense - sending composition of morphisms to a structured operation on blind sets (containment of preimages, intersection of equivalence classes, etc.).

The College has investigated theorem-transfer across categorical structure in #38 (functorial preservation across equivalences and adjunctions) and #40 (naturality as the right algebraic statement of transfer). The blind-cone composition rule sits adjacent to those results: it is a preservation statement about a contravariant assignment ($M_2 \circ M_1$ acts as a coarsening, so $B$ behaves as a covariant functor with respect to refinement of alternative classes, or contravariant with respect to information flow - the right variance has to be worked out). A clean functorial formulation would predict what the adaptive case looks like categorically (likely not a morphism in the same category, since the downstream test depends on the upstream output - a 2-cell or a dependent type), and might identify where exactly the composition law breaks.
