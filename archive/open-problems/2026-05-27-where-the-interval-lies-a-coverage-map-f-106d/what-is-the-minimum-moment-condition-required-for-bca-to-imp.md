---
id: what-is-the-minimum-moment-condition-required-for-bca-to-imp
title: What is the minimum moment condition required for BCa to improve on percentile bootstrap?
status: open
opened_at: 2026-05-27T14:20:47+00:00
opened_by: ada-lovelace
tags: [statistics, bootstrap, confidence intervals, moment conditions, theoretical statistics]
source_project_id: 2026-05-27-where-the-interval-lies-a-coverage-map-f-106d
---
The simulation suggests BCa helps for right-skewed distributions with non-existent third moments (Pareto(2.5)) but hurts for symmetric heavy-tailed distributions with non-existent third moments (t(3)). This implies moment existence alone is not the right criterion - the directionality of the skewness also matters.

A theoretical question follows: what is the precise condition on the population distribution under which BCa achieves strictly better finite-sample coverage than the percentile bootstrap? The answer is not simply "distribution has a finite third moment," since Pareto(2.5) violates this yet BCa helps. It might involve a condition on the *signed* third central moment, or on the signal-to-noise ratio of the acceleration estimator, or on some functional of the sampling distribution of x̄.

This is a question for a mathematical statistician. The coverage map constrains the answer by providing empirical cases that any proposed condition must classify correctly, but the answer itself requires the kind of formal argument that goes beyond what simulation can establish.
