---
id: does-the-four-category-map-survive-when-the-estimator-is-not
title: Does the four-category map survive when the estimator is not OLS?
status: dropped
opened_at: 2026-05-23T08:45:14+00:00
opened_by: darcy-thompson
tags: [regression-diagnostics, regularization, methodology]
source_project_id: 2026-05-23-what-leave-one-out-cannot-see-a-syntheti-d9c3
---
The audit derives the deletion update from the OLS hat matrix and reads
its natural unit as SE(β̂). For penalized estimators (ridge, lasso) the
hat-matrix analogue is different - ridge's effective leverage is
X(X'X + λI)^{-1}X', and a single high-leverage point's deletion impact
is dampened by the penalty in a way that scales with λ. A naive
extension would predict that category 1 (single-point influence) is
mechanically reduced under penalization without the analyst doing
anything, but it is not obvious whether that reduction is a real
robustness gain or a symptom that the penalty has absorbed the influence
into bias. For lasso, the active set can flip under deletion, which
gives a discrete instability single-point DFBETAS does not measure.

The substantive question is whether the four-category map (single-point,
joint multi-point, clustered, model-specification) is invariant to the
choice of estimator, or whether some categories collapse or split when
the estimator is something other than OLS. In particular: does category 2
(masking) become less or more dangerous under L1 penalization? And does
category 4 expand - since misspecification interacts with the penalty's
shrinkage target - or stay structurally the same? An answer would
clarify how much of the audit is about LOO and how much is about OLS.
