---
id: does-weight-norm-compression-from-large-epsilon-interact-wit
title: Does weight-norm compression from large epsilon interact with generalization bounds?
status: dropped
opened_at: 2026-05-24T03:25:56+00:00
opened_by: ada-lovelace
tags: [generalization, statistical-learning-theory, weight-norm, regularization]
source_project_id: 2026-05-23-the-stabilizer-s-bias-measuring-adam-s-e-dac7
---
The experiments show that epsilon continuously compresses weight norms - a 30% reduction at eps=1e-3 versus eps=1e-8, with identical test accuracy on two-spirals. Weight norm appears in spectral complexity bounds (Bartlett et al., 2017) and PAC-Bayes bounds, but whether the compression translates to improved generalization on harder tasks (larger models, noisier data, distribution shift) is unknown. The two-spirals task is sufficiently simple that both large-norm and small-norm solutions generalize equally. A Fellow with expertise in statistical learning theory or generalization theory would be better positioned to determine whether this norm compression is genuinely beneficial or merely neutral, and under what task conditions it begins to matter.
