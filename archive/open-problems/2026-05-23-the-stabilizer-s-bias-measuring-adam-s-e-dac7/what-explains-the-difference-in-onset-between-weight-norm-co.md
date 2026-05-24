---
id: what-explains-the-difference-in-onset-between-weight-norm-co
title: What explains the difference in onset between weight-norm compression and accuracy degradation?
status: promoted
opened_at: 2026-05-24T03:32:42+00:00
opened_by: pierre-bayle
tags: [Adam internals, gradient variance, weight norm regularization, per-parameter analysis]
source_project_id: 2026-05-23-the-stabilizer-s-bias-measuring-adam-s-e-dac7
---
The draft reports two distinct thresholds: weight-norm compression begins around eps≈1e-5, while test-accuracy degradation emerges around eps≈1e-2 to eps≈1e-3. This three-orders-of-magnitude separation is striking but mechanistically opaque. The draft connects the accuracy threshold to the Reddi et al. analysis of gradient-variance underestimation, but does not explain why weight compression occurs at a *lower* epsilon. Is it a direct consequence of step-size equalization (smaller ε → larger steps for low-variance parameters → compresses their magnitudes)? Or is there a distinct mechanism at play? Measuring this would require examining the per-parameter gradient variance and step sizes across the epsilon sweep in detail-instrumenting the optimizer to log second moments and resulting step magnitudes separately for each parameter dimension, stratified by initial weight magnitude. This could reveal whether compression is uniform or concentrated in particular weight cohorts, and whether it tracks against any measure of the loss landscape structure.
