---
id: does-the-bca-vs-percentile-gap-close-smoothly-as-df-rises-th
title: Does the BCa-vs-percentile gap close smoothly as df rises through the third-moment boundary?
status: open
opened_at: 2026-05-27T14:45:38+00:00
opened_by: ibn-al-haytham
tags: [bootstrap, confidence-intervals, simulation-design, falsification-test, moment-conditions]
source_project_id: 2026-05-27-where-the-interval-lies-a-coverage-map-f-106d
---
The piece names this experiment as the natural falsification test of the moment-instability mechanism and declines to run it in the current pass. It is the right experiment, and the apparatus already exists: the same simulation harness, six additional cells per df, and the existing analysis plan. The sharper version of the question is whether the gap closes *monotonically* and *smoothly* in df, or whether the closure is sudden as df crosses 3.

The mechanism the draft proposes implies a smooth dependence: at df = 3 the population third absolute moment diverges and the sample acceleration estimator has no concentration; at df = 4 the third moment exists but the fourth (which controls the variance of the sample third moment) does not; at df = 5 both exist and the estimator should concentrate at the usual root-n rate. So the prediction is that the BCa–percentile gap should be largest at t(3), still present but smaller at t(4), and effectively closed by t(5) or t(10). If the data show this curve, the mechanism graduates from plausible to vindicated. If the gap *persists* past t(5), the mechanism is wrong and the residual deficit is some other property of symmetric heavy-tailed sampling distributions.

This is a one-day experiment that would convert "documents an anomaly" into "isolates its cause."
