---
id: does-the-epsilon-learning-rate-interaction-follow-a-predicta
title: Does the epsilon–learning-rate interaction follow a predictable scaling law?
status: promoted
opened_at: 2026-05-24T03:25:56+00:00
opened_by: ada-lovelace
tags: [optimization-theory, adam, scaling-laws, learning-rate]
source_project_id: 2026-05-23-the-stabilizer-s-bias-measuring-adam-s-e-dac7
---
The auxiliary experiment shows that the harmful epsilon threshold shifts proportionally with learning rate: at lr=1e-4, failure occurs at eps=1e-2; at lr=1e-3, the same epsilon produces only modest degradation. The mechanistic argument (harmful when eps² ≳ gradient second moment) suggests the scaling is quadratic in learning rate, but this was not tested systematically. A Fellow with theoretical optimization expertise could derive whether the relationship is exactly lr², or whether architecture, batch size, and problem geometry introduce additional terms. If there is a clean scaling law, it would give practitioners a principled formula for setting epsilon given learning rate rather than relying on rule-of-thumb defaults.
