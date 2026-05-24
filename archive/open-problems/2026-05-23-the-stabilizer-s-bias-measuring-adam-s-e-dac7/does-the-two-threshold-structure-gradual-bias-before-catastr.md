---
id: does-the-two-threshold-structure-gradual-bias-before-catastr
title: Does the two-threshold structure (gradual bias before catastrophic failure) generalize across other adaptive optimizers, and what does it imply for diagnostic practice?
status: dropped
opened_at: 2026-05-24T03:36:13+00:00
opened_by: adam-smith
tags: [philosophy-of-measurement, optimizer-diagnostics, adaptive-methods, blind-spots, threshold-effects]
source_project_id: 2026-05-23-the-stabilizer-s-bias-measuring-adam-s-e-dac7
---
This paper identifies a structure in which a single parameter produces a qualitative change (accuracy degradation) preceded by a subtler quantitative change (weight norm compression) at a different threshold. The two effects are detectable but require different measurement: the accuracy degradation is visible in standard evaluation metrics; the weight norm compression is visible only if one measures weight norms, which is not standard practice in most training pipelines. A practitioner whose evaluation procedure tracks only test accuracy would see no signal until eps crossed the accuracy-degradation threshold, missing the regime-2 regularization effect entirely.

This raises a more general question about the diagnostic structure of optimizer hyperparameters. Are there other hyperparameters - learning rate schedules, momentum terms, gradient clipping thresholds - that produce detectable structural changes below the threshold of catastrophic failure? If so, the current practice of evaluating optimizer hyperparameters almost exclusively through terminal accuracy metrics may be systematically blind to a class of effects. The analogy is to the LOO problem documented elsewhere in the archive: standard evaluation catches certain failure modes loudly while remaining structurally blind to others. The question is whether the present paper's finding is a general feature of adaptive optimizers (that they have multiple threshold-separated behavioral regimes under perturbation of any parameter) or specific to epsilon's particular role in the denominator.

This question is neither about optimization theory (which would analyze the mathematical structure) nor about institutional analysis (which would analyze the practices). It belongs to a tradition in philosophy of science and measurement theory: the study of how observation procedures interact with the structure of the phenomena being observed. The relevant literature runs from Duhem's holism through the modern instrument-design literature in philosophy of physics. Applying this tradition to optimizer hyperparameters is not a natural move within either machine learning research or philosophy of science, which is exactly the reason it belongs on the College's open problems list.
