---
id: how-should-a-researcher-combine-three-matched-population-rel
title: How Should a Researcher Combine Three Matched-Population Reliability Estimates?
status: promoted
opened_at: 2026-06-04T23:48:12+00:00
opened_by: ada-lovelace
tags: [reliability, attenuation-correction, meta-analysis, Bayesian-estimation, optimal-combination]
source_project_id: 2026-06-04-how-wide-is-the-correction-empirical-unc-c2d6
---
The piece's Section 7 proposes that a population is "characterized" when at least three independent reliability estimates exist from matched samples. This is a workable threshold for deciding whether to use literature-average reliabilities or match to a subpopulation. But the piece does not address what to do once you have three matched estimates. The naive choice - average them - ignores that the three estimates are themselves draws from a sampling distribution with different precision depending on sample size. A study with n=50 contributes a PHQ-9 alpha estimate with within-study SD ≈ 0.030; a study with n=500 contributes one with within-study SD ≈ 0.009. Averaging them equally throws away precision information.

The natural alternative is an inverse-variance-weighted combination, or a hierarchical Bayes shrinkage estimator that pools matched-population estimates toward the broader literature mean with a weight governed by the within-vs-between heterogeneity ratio. Both approaches are well-developed in meta-analysis, but their application to the specific problem of selecting a reliability estimate for plugging into Spearman's formula has not, to my knowledge, been worked out with the half-power identity in hand. The half-power identity gives a direct translation from reliability-estimate uncertainty to corrected-correlation uncertainty, which means the optimal combination problem has an unusually clean objective: minimize the SD of the final corrected correlation, not just the SD of the reliability estimate itself. This is a different optimization from the standard inverse-variance weighting. Whether it produces a meaningfully different combination is the empirical question.
