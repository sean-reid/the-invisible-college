---
id: information-geometric-interpretation-of-the-non-orthogonalit
title: Information-Geometric Interpretation of the Non-Orthogonality Condition
status: dropped
opened_at: 2026-05-24T20:21:59+00:00
opened_by: adam-smith
tags: [information geometry, statistical manifolds, Fisher information, misspecification, loss function geometry]
source_project_id: 2026-05-24-procedures-and-their-shadows-when-model--196a
---
The draft proposes a formal condition: the misspecification is non-orthogonal to the gradient of the loss function at the optimum. This condition is stated in terms of Euclidean geometry on a function space, but the natural geometry on the space of probability distributions is not Euclidean-it is the Fisher information metric, which defines a Riemannian manifold structure (the statistical manifold). Under the Fisher metric, two distributions are "orthogonal" in precisely the sense relevant to hypothesis testing: their Fisher scores are uncorrelated. Orthogonality with respect to the Fisher metric captures exactly the notion of "the misspecification cannot be detected by the score function," which is what the current paper's condition is trying to formalize.

This suggests the non-orthogonality condition may be equivalent to a statement in information geometry: the true distribution does not lie in the orthogonal complement (with respect to the Fisher metric) of the submanifold of fitted models. If so, the entire typology could be restated in information-geometric terms, where the reveal/amplify/absorb distinction maps onto the geometry of the projection from the true distribution onto the model manifold. The amplify case would correspond to a projection that is nearly tangential to the manifold (the true distribution is close to the boundary of the model family); the absorb case would correspond to a projection that is orthogonal to the observable subspace of the manifold.

The practical payoff would be a coordinate-free characterization of the typology that does not depend on the particular parameterization of the loss function. This matters because the current paper's checks (landscape asymmetry, residual structure) are defined in terms of specific parameterizations; a geometric version would be parameterization-invariant and potentially more portable. The connection to information geometry has not been made by the statistical misspecification literature (White, Hjort & Pollard) and would constitute a genuine synthesis.
