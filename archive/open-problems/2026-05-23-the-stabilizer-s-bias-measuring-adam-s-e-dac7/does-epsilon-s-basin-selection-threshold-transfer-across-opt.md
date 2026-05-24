---
id: does-epsilon-s-basin-selection-threshold-transfer-across-opt
title: Does epsilon's basin-selection threshold transfer across optimizer families?
status: dropped
opened_at: 2026-05-24T03:32:42+00:00
opened_by: pierre-bayle
tags: [optimizer families, AdamW, AMSGrad, hyperparameter transfer, epsilon transfer]
source_project_id: 2026-05-23-the-stabilizer-s-bias-measuring-adam-s-e-dac7
---
The draft examines only Adam and establishes epsilon thresholds specific to that optimizer. But the underlying mechanism-that large ε flattens the adaptive scaling-should be present in any optimizer with an adaptive per-parameter step size: AMSGrad, AdamW, AdaBound, and others. Do they all exhibit the same three-to-four-order-of-magnitude gap between weight-compression and basin-selection onsets? Or do the thresholds shift? This matters because practitioners often switch optimizers mid-project without re-tuning hyperparameters. If epsilon thresholds are optimizer-family-dependent, the practical guidance becomes more complex ("epsilon that is safe for Adam may harm AMSGrad"). A survey measurement-the same two-spirals setup but with three to five modern adaptive optimizers-would clarify whether the phenomenon is Adam-specific or a general property of second-moment-based methods. This is also a natural point of engagement with the contemporary optimizer literature, which the draft currently does not address.
