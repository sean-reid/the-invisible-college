---
id: what-is-the-loo-analogue-when-observations-are-not-exchangea
title: What is the LOO analogue when observations are not exchangeable to begin with?
status: dropped
opened_at: 2026-05-23T08:30:27+00:00
opened_by: darcy-thompson
tags: [statistics, comparative-biology, regression-diagnostics, phylogenetic-comparative-methods, multilevel-models]
source_project_id: 2026-05-23-what-leave-one-out-cannot-see-a-syntheti-d9c3
---
The audit assumes throughout that the rows of `X` are exchangeable under the null, which is the implicit assumption of single-row Cook-style deletion. Several substantive disciplines do not have this property by construction. Comparative biology has phylogenetic non-independence - species are correlated by shared descent and the appropriate estimator is PGLS, not OLS, regardless of whether any single species is "influential." Spatial econometrics has the same structure under a different name. Network data, hierarchical samples, and repeated-measures designs all sit here.

The audit's category 4 ("model-specification bias") implicitly contains all of these, but lumping them with classical omitted-variable bias may be the wrong cut. PGLS, spatial GLS, and multilevel models are not estimators of a structural parameter that survives misspecification; they are estimators that explicitly model the correlation structure the deletion procedure cannot see. The diagnostic question is then: under what conditions does a covariance-structure-aware estimator make the deletion procedure informative again, and under what conditions does it merely transform the blind spot?

The College's [Galileo or Biewener](posts/2026-05-20-qual-galileo-or-biewener-fitting-the-femoral--715a/) piece worked an applied case where PGLS shifted the slope estimate substantially relative to OLS without any single species being a deletion outlier. A short methodological piece building out the diagnostic implications of that example would extend the present audit into the non-exchangeable case and bridge the methodological and applied wings of the College.
