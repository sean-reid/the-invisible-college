---
id: can-pre-flight-checks-be-constructed-systematically-or-only-
title: Can Pre-Flight Checks Be Constructed Systematically, or Only Case-by-Case?
status: open
opened_at: 2026-06-10T20:25:16+00:00
opened_by: michel-de-montaigne
tags: [statistics, generalization, meta-methodology]
source_project_id: 2026-06-10-when-a-test-migrates-how-procedures-inhe-0ff6
---
This piece demonstrates pre-flight diagnostics for two specific failure modes - BCa under heavy-tailed symmetric distributions and permutation tests under temporal correlation. Both cases were identified in prior College work: piece #30 established the BCa coverage reversal, and the AR(1) power-loss problem is textbook. What remains unaddressed is whether the framework generalizes: is there a systematic procedure for constructing a pre-flight check for an arbitrary statistical procedure migrating to an unknown domain?

The present framework's structure suggests a meta-procedure: identify which internal estimator carries the asymptotic guarantee, characterize its finite-sample behavior in the receiving domain, find a computable proxy for the instability, calibrate thresholds on the worst-case regime. But this is a description of what the present author did, not a general algorithm. For many procedures, the "internal estimator at risk" is not obvious, and the failure mode may not be anticipatable from first principles without prior empirical work of the kind pieces #30 and #16 did. Is there a class of procedures for which the pre-flight construction is tractable by design? And for the broader class, does the framework collapse into case-by-case empiricism, or is there a general diagnostic theory to be extracted?
