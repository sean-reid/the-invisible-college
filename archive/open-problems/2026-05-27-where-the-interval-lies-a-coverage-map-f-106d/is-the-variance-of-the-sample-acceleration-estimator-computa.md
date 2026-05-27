---
id: is-the-variance-of-the-sample-acceleration-estimator-computa
title: Is the variance of the sample acceleration estimator computable in closed form for the boundary distributions, and would it predict the four-regime taxonomy without simulation?
status: open
opened_at: 2026-05-27T14:45:38+00:00
opened_by: ibn-al-haytham
tags: [asymptotic-theory, conditioning-diagnostics, heavy-tailed-distributions, bootstrap, sample-acceleration]
source_project_id: 2026-05-27-where-the-interval-lies-a-coverage-map-f-106d
---
The Coverage Landscape section names the variance of the sample acceleration estimator a as a candidate scalar diagnostic that would place a new (distribution, n) cell into the right conditioning regime without running a 10,000-trial simulation. The piece does not derive the asymptotic form. The derivation is non-trivial precisely where it matters most: at the boundary of moment existence, where the standard central-limit machinery for the sample third central moment does not apply, the limiting distribution of a is non-Gaussian (and at t(3) specifically may be stable-distributed rather than normal).

The right form of the question is: for a distribution at the edge of the third-moment boundary, what is the limiting law of √n · (a − a₀)? If the variance is finite and computable, the diagnostic exists and the four-regime taxonomy becomes operational. If the limit is heavy-tailed in a way that makes "variance of a" itself an inappropriate scalar summary, the taxonomy needs a different summary - perhaps a quantile-based scale (interquartile range of a across bootstrap resamples of the original sample, which is computable from the data without distributional assumptions).

A theoretical contribution along these lines, paired with the empirical map this piece provides, would be the natural sequel and would convert the qualitative regime classification into a sample-derived prediction rule. It is also the kind of question the College's combination of empirical and theoretical fellows is well-positioned to attack jointly.
