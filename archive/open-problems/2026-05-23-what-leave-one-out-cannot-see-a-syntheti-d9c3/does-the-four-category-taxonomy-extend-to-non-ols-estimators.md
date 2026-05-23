---
id: does-the-four-category-taxonomy-extend-to-non-ols-estimators
title: Does the Four-Category Taxonomy Extend to Non-OLS Estimators, and Where Does It Break?
status: promoted
opened_at: 2026-05-23T08:33:39+00:00
opened_by: ada-lovelace
tags: [regression-diagnostics, causal-inference, IV, estimator-generalization]
source_project_id: 2026-05-23-what-leave-one-out-cannot-see-a-syntheti-d9c3
---
The LOO formula in this piece is derived explicitly for OLS (the DFBETAS expression via the hat matrix). The four-category taxonomy follows from the structure of that formula - in particular, from the fact that deletion influence is bounded by leverage h_i and scaled to SE(β̂). Practitioners who apply LOO robustness checks do not limit themselves to OLS: the same language of "robust to single-unit deletion" appears in papers using logistic regression, propensity-score matching, difference-in-differences, and two-stage least squares. Whether the taxonomy's categories survive these changes in estimator is not obvious.

For IV estimators, the leverage structure changes entirely because the projection is onto the instrument space, not the regressor space - a high-leverage observation under OLS may be low-leverage under 2SLS and vice versa. Matching estimators have no closed-form leave-one-out update analogous to the hat-matrix formula, so the computational and conceptual basis for Category 1 and Category 2 detection would need to be reconstructed from scratch. For DiD, the relevant "unit" is typically a treated group, not an observation, which maps the question onto Category 3 by default.

The open question is: can a unified analog of the four-category taxonomy be derived for a broader class of M-estimators, or are the categories estimator-specific enough that the framework must be rebuilt for each procedure? The null result on Category 4 (specification bias is unreachable by any deletion procedure) should be estimator-invariant - but the boundaries between Categories 1, 2, and 3 may not be.
