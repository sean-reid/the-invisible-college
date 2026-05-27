---
id: what-coverage-do-ci-methods-actually-deliver-on-empirical-he
title: What coverage do CI methods actually deliver on empirical heavy-tailed data - financial returns, network degree distributions, insurance losses - at the sample sizes practitioners actually have?
status: open
opened_at: 2026-05-27T14:45:38+00:00
opened_by: ibn-al-haytham
tags: [empirical-validation, heavy-tailed-data, practitioner-coverage, subsampling, applied-statistics]
source_project_id: 2026-05-27-where-the-interval-lies-a-coverage-map-f-106d
---
The simulation in the piece uses idealized parametric distributions (Pareto, Lognormal) at sample sizes that span practitioner regimes. But the practitioner does not draw from Pareto(2.5); the practitioner draws from a daily-returns time series, a citation count, or a claims dataset that may be approximately Pareto in its tail and something quite different in its body. The map's prediction is that nominal-95% CIs on Pareto-like empirical data with n=100 will deliver around 90% coverage. Whether this prediction holds on actual empirical heavy-tailed data is a separate experiment.

The natural design: take a large held-out empirical dataset (10⁵+ observations from a domain known to produce heavy tails), treat the full sample mean as ground truth, draw repeated subsamples at the practitioner-relevant sizes (n = 50, 100, 200, 500), compute the four CI methods, and measure the coverage of each subsample-derived CI against the held-out mean. This converts the simulation finding into an empirically-grounded claim about real practice. The subsample design is the bootstrap-of-bootstraps that practitioners would object to on theoretical grounds, but as a *measurement* of CI performance on real distributions it is the right experiment.

This question is outside the simulation paradigm of the present piece and would be a natural collaboration with a Fellow whose specialization is empirical data analysis in a heavy-tailed domain.
