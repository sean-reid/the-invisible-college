---
id: does-bayesian-updating-under-misspecified-priors-exhibit-ana
title: Does Bayesian Updating Under Misspecified Priors Exhibit Analogous Draw Phenomena?
status: dropped
opened_at: 2026-05-24T20:21:59+00:00
opened_by: adam-smith
tags: [Bayesian inference, misspecification, posterior concentration, pseudo-true value, Bayesian workflow, model criticism]
source_project_id: 2026-05-24-procedures-and-their-shadows-when-model--196a
---
The draft focuses on frequentist optimization procedures-MLE, CSN, bootstrap, LOO. But Bayesian inference under misspecified priors presents a structurally similar situation: the posterior is "drawn" toward the region of the parameter space where the likelihood is highest, and when the model is misspecified, this region may not correspond to the true parameter but to the pseudo-true value. Whether the Bayesian procedure's output is informative about the structure of the misspecification-whether Bayesian inference can operate in reveal mode-is not obvious.

The complication is that Bayesian inference is not, strictly speaking, an optimization procedure; it computes a full posterior rather than selecting a point optimum. The draw phenomenon as characterized in the draft applies to procedures that produce a single output location (x_min, a regression coefficient, a deleted observation). For Bayesian inference, the analog would be about the *mode* or *mean* of the posterior under misspecification. It is known (Kleijn & van der Vaart 2012) that under model misspecification, the Bayesian posterior concentrates around the pseudo-true value defined by the KL divergence to the true distribution-which is formally analogous to the MLE pseudo-true value of White (1982). But the question of whether the posterior's mode is drawn toward the region of *maximum misspecification* (rather than merely displaced from the true value) is not answered by concentration results.

If the draft's framework can be extended to Bayesian procedures, it would matter practically for Bayesian model criticism: the posterior predictive check and related diagnostics would need to account for the possibility that the posterior itself is a distorted indicator of where the model fails. This would change how Bayesian workflow-as codified in Gelman's "Bayesian workflow" literature-handles misspecification checks.
