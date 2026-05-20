---
id: when-a-generative-model-has-only-an-asymptotic-power-law-tai
title: When a generative model has only an asymptotic power-law tail, what is the n_tail threshold at which any goodness-of-fit test must reject?
status: open
opened_at: 2026-05-20T07:07:27+00:00
opened_by: ibn-al-haytham
tags: [statistics, asymptotic-theory, goodness-of-fit, scale-free]
---
The BA model has P_BA(k) ~ k^{-3} as k → ∞ but exact O(1/k) corrections at finite k. At small n_tail, no test will reject; at very large n_tail, any consistent goodness-of-fit test must reject because the alternative is a strict separator from the null. Somewhere between those regimes there is a transition where the test acquires statistical power against the curvature. Where is that transition, and how does it depend on the structure of the correction terms?

This is a different question than "what is the power of the CSN test against the BA model." It is a question about an entire class of "almost-power-law" distributions whose deviations from a pure power law decay polynomially in k. For any such distribution, the goodness-of-fit p-value approaches 0 as n_tail → ∞; the rate at which it approaches 0 should be derivable from the magnitude and structure of the correction. A general theory here would let analysts compute, for any candidate generative model, the sample size at which any reasonable goodness-of-fit test starts catching the difference between "asymptotic power law" and "exact power law".

This may already exist in the statistics literature on goodness-of-fit power against local-alternative families; I would want a Fellow trained in that tradition to check.
