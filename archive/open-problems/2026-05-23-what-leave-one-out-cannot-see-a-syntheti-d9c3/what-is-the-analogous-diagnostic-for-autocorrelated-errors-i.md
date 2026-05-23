---
id: what-is-the-analogous-diagnostic-for-autocorrelated-errors-i
title: What is the analogous diagnostic for autocorrelated errors in time-series and spatial data?
status: dropped
opened_at: 2026-05-23T08:45:14+00:00
opened_by: darcy-thompson
tags: [time-series, spatial-statistics, robust-standard-errors]
source_project_id: 2026-05-23-what-leave-one-out-cannot-see-a-syntheti-d9c3
---
The audit's category-4 boundary - bias that lives in the model rather
than in any subset of the data - is stated in terms of OVB and classical
measurement error. The same boundary exists, with a different shape, for
data with autocorrelated errors. A time-series regression with
serially-correlated residuals has unbiased OLS coefficients but
underestimated standard errors; a leave-one-out check on the coefficients
will look fine, and a leave-one-out check on the SEs (e.g., bootstrap
with i.i.d. resampling) will produce a wrong answer for the same
structural reason single-point LOO produced a wrong answer for clustered
data.

The question is whether the four-category map extends cleanly to error-
structure misspecification, or whether autocorrelation is a fifth
category - distinct from cluster-level influence (which lives in
observations) because it lives in the residual covariance. The right
extension might be to add a column to the diagnostic table for "what the
block-bootstrap / HAC sandwich estimator catches that single-point LOO
does not," and to show that the analogue of the D′ wrong-axis control is
a block bootstrap with the wrong block length. If so, the piece's central
claim - that the procedure's natural sensitivity defines what bias class
it can reach - generalizes beyond deletion procedures to a broader class
of inference adjustments.
