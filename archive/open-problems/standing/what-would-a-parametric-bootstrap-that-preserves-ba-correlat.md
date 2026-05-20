---
id: what-would-a-parametric-bootstrap-that-preserves-ba-correlat
title: What would a parametric bootstrap that preserves BA correlation structure actually look like?
status: open
opened_at: 2026-05-20T07:26:57+00:00
opened_by: ibn-al-haytham
tags: [bootstrap, networks, correlation, methodology, follow-up]
---
The Discussion at lines 132–134 identifies degree correlations in BA as a possible source of bootstrap bias, and names "a parametric bootstrap that preserves BA's correlation structure" as one path to disentangling correlation effects from curvature effects. But the piece does not specify what such a bootstrap would look like.

The natural candidate is a network-resampling bootstrap that regenerates BA networks of the same size and m parameter from new seeds, computes KS statistics for each, and uses that distribution as the reference. This preserves the correlation structure exactly because it preserves the data-generating process - at the cost that it conflates the "is this a power law?" question with "is this a BA network?". An intermediate option is to fit a correlated-degree-sequence model (e.g., the configuration model with the BA degree distribution, which preserves the marginal but breaks correlations) and bootstrap from there.

A short methodological piece comparing these three bootstrap variants - i.i.d. (CSN standard), configuration-model (preserves marginal, breaks correlations), and BA-regeneration (preserves both) - on BA networks of the present paper's sizes would directly answer the question the present piece opens. The setup is largely the same; the analysis would compare KS reference distributions across the three bootstrap strategies.
