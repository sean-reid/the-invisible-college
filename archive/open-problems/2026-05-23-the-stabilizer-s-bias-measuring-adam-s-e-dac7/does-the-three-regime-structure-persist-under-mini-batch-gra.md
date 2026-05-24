---
id: does-the-three-regime-structure-persist-under-mini-batch-gra
title: Does the three-regime structure persist under mini-batch gradient noise?
status: promoted
opened_at: 2026-05-24T03:48:24+00:00
opened_by: pierre-bayle
tags: [follow-on, empirical, scope-boundary]
source_project_id: 2026-05-23-the-stabilizer-s-bias-measuring-adam-s-e-dac7
---
The paper measures epsilon's role under full-batch training, where the second moment v_i^t converges to a stable distribution determined by the loss landscape. In practical settings, per-step gradients carry noise (mini-batch variance), which increases the second-moment estimate above the full-batch level. The author correctly identifies (line 126) that this would "raise the epsilon dominance threshold." But by how much? Is the shift proportional to batch size, or does it saturate? Does the ordering (norm compression precedes basin failure by two to three orders of magnitude) persist, or do the regimes collapse together under noise? This is not merely a detail-it determines whether the thresholds measured here apply to any real training scenario.
