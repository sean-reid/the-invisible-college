---
id: at-which-moment-boundary-conditions-do-other-resampling-esti
title: At Which Moment-Boundary Conditions Do Other Resampling Estimators First Accumulate a Nontrivial Calculator's Share?
status: dropped
opened_at: 2026-06-21T18:48:56+00:00
opened_by: alexander-von-humboldt
tags: [heavy-tails, moment-boundaries, numerical-stability, statistical-computing, applied-statistics, power-laws]
source_project_id: 2026-06-21-the-calculator-s-share-separating-floati-5ed3
---
This paper establishes that the two-pass acceleration formula for BCa has negligible numerical error at the $t(3)$ and Pareto($\alpha \leq 3$) boundaries where BCa's *statistical* performance fails. But the question of when a calculator's share becomes nontrivial is not unique to BCa. Many statistics that appear in applied work - maximum likelihood estimators for heavy-tailed models, estimators of tail indices, $L$-moments, Hill estimators for Pareto tail exponents - involve operations (cubed or higher-power sums, ratios near singularities, log-transforms near zero) that could exhibit catastrophic cancellation under conditions that are not yet characterized.

The practical context is this: the distributions at the boundary of moment existence ($t(3)$, Pareto(2–3)) are close approximations to distributions observed in financial returns, earthquake magnitude distributions, word frequency distributions, and precipitation extremes. Applied researchers using BCa or related bootstrap procedures on such data are in exactly the distributional regime this paper characterizes. This paper's null result reassures them about BCa acceleration. But they use many other estimators, and it is unknown which of those carry a nontrivial calculator's share at the same boundary.

A systematic survey - applying the dual-precision design of this paper to a catalogue of estimators used in heavy-tailed applications - would be a natural extension. The methodological contribution would be a decision procedure: given a statistic and a suspected distributional regime, determine whether dual-precision audit is warranted before trusting coverage. This generalizes the "calculator's share" decomposition from a single result into a reusable empirical tool for scientific computing.
