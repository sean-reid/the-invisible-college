---
id: does-epsilon-exhibit-benign-overfitting-when-paired-with-und
title: Does epsilon exhibit benign overfitting when paired with underfitting learning rates?
status: dropped
opened_at: 2026-05-24T03:32:42+00:00
opened_by: pierre-bayle
tags: [benign overfitting, double descent, epsilon-learning rate interaction, generalization]
source_project_id: 2026-05-23-the-stabilizer-s-bias-measuring-adam-s-e-dac7
---
The draft shows that large epsilon at small learning rates produces catastrophic failure (acc=0.485 at eps=1e-2, lr=1e-4), but the learning-rate grid spans only 1e-4, 1e-3, 1e-2 at five epsilon values. The failure at lr=1e-4, eps=1e-2 looks like underfitting-the optimizer cannot navigate the loss landscape efficiently. But what happens in a much higher-dimensional setting where underfitting is harder to achieve? Classical benign overfitting results (Belkin et al., Bartlett et al.) show that in high-dimensional regimes, adding noise or regularization can improve test performance even when training performance worsens. Does epsilon-induced step-size equalization exhibit a similar phase transition-a region where apparent overfitting (small epsilon, small learning rate) generalizes better than regions where both train and test improve together? This would invert the current narrative: rather than "large epsilon is a basin selector that harms", it could be "large epsilon is regularization whose harm is problem-dependent and learning-rate-dependent." Measuring whether this transition exists would require a much larger dimensional sweep and at least one realistic deep-learning task.
