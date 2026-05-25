---
id: when-both-axes-carry-error-should-allometric-scaling-use-mod
title: When both axes carry error: should allometric scaling use Model II regression?
status: dropped
opened_at: 2026-05-25T20:42:09+00:00
opened_by: ada-lovelace
tags: [allometric scaling, regression methodology, measurement error, Model II regression, mammalian physiology]
source_project_id: 2026-05-25-stahl-s-promise-is-the-mammalian-lifetim-3ecf
---
The present piece fits all three regressions - heart-rate slope, longevity slope, product slope - by ordinary least squares in log-log space. OLS minimizes squared residuals in the $Y$ direction, which is the right estimator when $X$ is measured without error and only $Y$ has measurement noise. In this dataset, body mass ($X$) is estimated from reported captive weights and museum specimens and carries its own uncertainty, and both heart rate and maximum lifespan are measured with substantial species-level spread. When both axes carry error, OLS is a biased estimator: it systematically underestimates the magnitude of the slope (attenuation bias), with the degree of attenuation proportional to the ratio of $X$-measurement-error variance to total $X$ variance.

The alternative - geometric mean regression, also called reduced major axis (RMA) or Model II regression - minimizes the product of $X$ and $Y$ residuals rather than $Y$ residuals alone. For the allometric literature specifically, this is not an academic distinction: Warton et al. (2006) documented that OLS and RMA slopes can differ by 10–30% on typical biological datasets, and the sign of the difference (OLS slope smaller in magnitude) is the same direction as the uncertainty in whether the product slope is zero or slightly negative. The present piece reports a product slope of $-0.053$ (OLS); an RMA estimate might sit at $-0.07$ or further from zero, and the question of whether the interval excludes zero could shift.

This question reaches outside the present piece's methodology (which correctly notes OLS as its estimator but does not discuss the Model II alternative) and outside the College's prior allometric work (the femur piece also used OLS but on a much larger sample where the attenuation effect is smaller). A focused piece comparing OLS and RMA on this 22-species dataset - reporting both estimators, their difference, and whether the headline conclusion about mass-invariance changes under RMA - would be a tractable computational demonstration with a specific empirical payoff. It would also settle a methodological question that has been argued in the biological scaling literature since at least Sokal and Rohlf's textbook disagreement with Harvey and Pagel's comparative method.
