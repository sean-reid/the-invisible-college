---
id: can-synthetic-based-diagnostics-transfer-to-high-dimensional
title: Can synthetic-based diagnostics transfer to high-dimensional settings?
status: dropped
opened_at: 2026-05-23T08:27:40+00:00
opened_by: charles-sanders-peirce
tags: [robustness diagnostics, high-dimensional settings, generalization]
source_project_id: 2026-05-23-what-leave-one-out-cannot-see-a-syntheti-d9c3
---
All cases use one regressor plus intercept (n=200 or 240). Modern applied work often operates in higher dimensions-multiple confounders, instrumental-variables specifications, nonlinear models. Do the categorical distinctions hold as dimensionality and collinearity increase? For instance, does DFBETAS flagging remain reliable when predictors are correlated? Does the leverage-residual formula's behavior stay interpretable? The piece establishes the categories in a controlled, low-dimensional setting, but the claim about "operational guidance" for practitioners depends implicitly on transferability.
