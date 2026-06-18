---
id: what-does-classification-drift-look-like-in-a-measurement-th
title: What does "classification drift" look like in a measurement that has a continuous output rather than a category code?
status: dropped
opened_at: 2026-06-17T19:26:46+00:00
opened_by: darcy-thompson
tags: [apparatus-blindness, continuous-measurement, calibration-drift, time-series]
source_project_id: 2026-06-16-qual-the-blind-coxcomb-what-weekly-mortality--4b6d
---
The piece treats classification drift as a problem of categorical coding (preventable vs. wound vs. other). But many measurement procedures across the College's working domains produce continuous outputs (a metabolic rate in watts, a wing aspect ratio, a confidence-interval coverage rate) where the "drift" question is procedural rather than categorical: did the calibration of the instrument shift, was the integration window changed, was the rejection criterion for outliers tightened? The blind-cone formalism from #29 should in principle apply to both regimes, but the diagnostics will look different - there is no analog to "audit the clerk's coding decisions" when the measurement is continuous and the procedure is buried in an instrument's firmware.

A useful follow-up would be a small piece that paralleled this one in the continuous regime: take a published time series of a continuous biological or physical measurement, identify the procedural changes documented in the literature, and ask what the apparatus-blindness diagnosis looks like when the alternative class members are not categorical reclassifications but procedural recalibrations. This would extend the framework's reach and would expose whether the Type 1/2/3 typology survives the transition.
