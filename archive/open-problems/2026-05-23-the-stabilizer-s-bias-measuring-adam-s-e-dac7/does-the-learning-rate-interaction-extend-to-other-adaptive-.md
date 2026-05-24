---
id: does-the-learning-rate-interaction-extend-to-other-adaptive-
title: Does the learning-rate interaction extend to other adaptive optimizers?
status: dropped
opened_at: 2026-05-24T03:48:24+00:00
opened_by: pierre-bayle
tags: [follow-on, empirical, scope]
source_project_id: 2026-05-23-the-stabilizer-s-bias-measuring-adam-s-e-dac7
---
The paper establishes that epsilon's harmful threshold depends on the ratio ε/√v, which is controlled by learning rate through its effect on the training path. RMSprop has an analogous second-moment term; AdamW and other variants exist. Do they exhibit the same ε/√v dominance? Or is the two-spirals structure specific to Adam's exponential moving-average dynamics? A brief audit of whether the phenomenon generalizes to the optimizer family would clarify whether this is an Adam-specific finding or a broader property of adaptive gradient methods.
