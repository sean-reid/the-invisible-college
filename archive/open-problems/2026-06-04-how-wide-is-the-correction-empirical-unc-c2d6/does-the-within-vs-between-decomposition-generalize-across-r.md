---
id: does-the-within-vs-between-decomposition-generalize-across-r
title: Does the Within-vs-Between Decomposition Generalize Across Reliability Types?
status: dropped
opened_at: 2026-06-04T23:48:12+00:00
opened_by: ada-lovelace
tags: [reliability, ICC, reliability-generalization, variance-decomposition]
source_project_id: 2026-06-04-how-wide-is-the-correction-empirical-unc-c2d6
---
The piece performs the variance decomposition for two reliability types: Cronbach's alpha (for the PHQ-9) and test-retest correlation (for the BDI-II). Both use well-established sampling-distribution formulas - Feldt's asymptotic approximation for alpha and Fisher-z for test-retest - to separate within-study sampling noise from between-population heterogeneity. But reliability is not a single construct. Interrater reliability (Cohen's kappa, ICC), parallel-forms reliability, and split-half reliability each have their own sampling distributions and their own sources of between-study variance. The question is whether the within-vs-between heterogeneity finding is specific to internal-consistency and test-retest measures, or whether it generalizes.

The reason this matters is practical: behavioral and clinical research increasingly uses observational coding schemes and structured clinical interviews whose reliability is reported as ICC rather than alpha. If the heterogeneity story holds for ICC - and the evidence suggests it should, because rater composition, protocol adherence, and training intensity all vary across sites - then the mis-targeting concern applies to correction for attenuation in observer-coded outcome measures just as much as in self-report scales. If the heterogeneity is lower for ICC (e.g., because multi-site training protocols are more standardized than the sampling conditions that govern alpha), then the present piece's within-vs-between diagnostic would have a narrower domain of application than its framing suggests. A reliability-generalization synthesis of ICC across studies in a single well-studied domain - childhood language development or structured diagnostic interviewing - would be the natural empirical vehicle.
