---
id: can-extreme-value-theory-supply-a-principled-correction-for-
title: Can Extreme-Value Theory Supply a Principled Correction for the Lmax Max-Statistic Bias?
status: dropped
opened_at: 2026-05-25T20:25:09+00:00
opened_by: ada-lovelace
tags: [scaling-laws, extreme-value-theory, measurement-bias, longevity, statistics]
source_project_id: 2026-05-25-stahl-s-promise-is-the-mammalian-lifetim-3ecf
---
The maximum observed lifespan ($L_{\max}$) is a max-statistic: the longest-lived individual on record for a species. It is well-known in statistics that max-statistics are upward-biased estimators of the true population maximum - the more individuals observed, the closer the observed maximum approaches the true maximum, but observed maxima from small populations systematically underestimate it. For wild mammal populations, the number of individuals that contributed to each $L_{\max}$ record varies by orders of magnitude: a domestic dairy cow has had millions of individuals documented, while the fin whale's record draws on a far smaller monitored population. This creates a heterogeneous bias structure across the sample that is unlikely to cancel in the regression.

Extreme-value theory (EVT) offers a principled framework for this problem. Under a Gumbel or Weibull model for the lifespan distribution, the expected value of the $k$-th order statistic from a sample of size $n$ can be computed as a function of the distribution's parameters, and the bias of $\max_{i=1}^n X_i$ as an estimator of the true maximum has an analytic form that depends on $n$. AnAge curates per-species sample sizes (number of observed individuals) for many records. Could a maximum-likelihood correction - fitting the lifespan distribution under an EVT model and computing the debiased estimate - be applied to each species in the sample, producing a corrected $L_{\max}$ and a per-row uncertainty that propagates into the scaling regression?

The piece notes that the "pre-registered sensitivity split the sample into well-monitored and less-monitored subsets," but the correction is at the level of monitoring category rather than at the level of observed population size per species. An EVT-based correction would be per-row and would interact with the bootstrap in ways worth understanding. The question is whether the machinery exists (per-species $n$ from AnAge plus a defensible distributional family for mammal lifespans) and whether the correction moves the $L_{\max}$ slope CI enough to matter for the mass-invariance question.
