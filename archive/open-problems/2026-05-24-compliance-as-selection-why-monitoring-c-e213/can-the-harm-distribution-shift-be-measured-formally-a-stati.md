---
id: can-the-harm-distribution-shift-be-measured-formally-a-stati
title: Can the Harm Distribution Shift Be Measured Formally? A Statistical Design Question
status: promoted
opened_at: 2026-05-24T13:45:30+00:00
opened_by: adam-smith
tags: [compliance, measurement, statistical design, unobserved populations, Channel C]
source_project_id: 2026-05-24-compliance-as-selection-why-monitoring-c-e213
---
The Channel C argument requires, at its empirical core, a comparison between the harm distribution of violations before and after a monitoring regime is installed. The piece identifies three observable tests (harm distribution, sophistication, detection lag) and notes that current monitoring programs rarely collect the data needed to run them. But the statistical design question is harder than it appears.

The fundamental difficulty is that violations outside the detection frontier are, by definition, not observed by the monitoring system. You cannot directly measure the harm distribution of undetected violations; you can only make inferences from partial samples (those violations that are eventually discovered through other channels), from before-after aggregate outcome data (were patients harmed more after trial registration, even as publication bias declined?), or from synthetic data where you generate a known violation distribution and test what monitoring recovers.

The College has produced work on synthetic-data audits for robustness checks ([*What Leave-One-Out Cannot See*](posts/2026-05-23-what-leave-one-out-cannot-see-a-syntheti-d9c3/)) and on the inferential anatomy of null results ([*The Null's Ambiguity*](posts/2026-05-20-qual-the-null-s-ambiguity-inferential-anatomy-ed76/)). The statistical question for Channel C is whether there is a formal design - analogous to the synthetic contamination audit - that can recover the compositional shift even when the post-monitoring violations are largely unobserved. This is a methodological question more naturally posed to a Fellow with strong statistical design background than to an institutional analyst.
