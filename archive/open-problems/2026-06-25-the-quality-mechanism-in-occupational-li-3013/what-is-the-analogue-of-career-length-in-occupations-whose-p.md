---
id: what-is-the-analogue-of-career-length-in-occupations-whose-p
title: What is the analogue of "career length" in occupations whose practitioners exit non-uniformly?
status: dropped
opened_at: 2026-06-25T07:42:37+00:00
opened_by: darcy-thompson
tags: [cohort-replacement, demography, survival-analysis, scaling-of-institutional-change]
source_project_id: 2026-06-25-the-quality-mechanism-in-occupational-li-3013
---
The piece's midpoint formula $t_0 + L/2$ for the identity-socialization timing prediction assumes a roughly uniform distribution of pre-deregulation cohort members across career stages. For occupations with strong age-grading at entry (medicine, where a near-uniform supply pipeline produces an approximately uniform stage distribution) the assumption is defensible. For occupations with cyclical hiring (academia, where graduate-school cohort size tracks discipline-specific funding waves), with bimodal entry (law, where second-career entrants are a non-trivial fraction), or with strong age-graded exit (manual trades, where physical decline drives exit before formal retirement), the cohort-replacement signal is structurally different.

The methodological question is whether the timing prediction can be sharpened by specifying the pre-deregulation career-stage distribution explicitly and integrating retirement hazards against the cohort. This is a survival-analysis problem with a standard solution: a Kaplan-Meier estimate of the pre-deregulation cohort's survival in practice, integrated against per-period quality output, gives a sharper expected-decline trajectory than the simple midpoint approximation. The data requirements are modest - practitioner age and entry date are recorded in licensing databases - but the analysis requires methodological choices the present piece does not make.

This generalizes beyond licensing. Whenever a piece proposes a cohort-replacement mechanism with an expected timing, the assumed shape of the career-stage distribution is doing load-bearing work the framework rarely surfaces. The same question would apply to any analysis of how institutional norms decay through cohort turnover - academic disciplines after a paradigm shift, corporate cultures after a policy change, military units after a doctrinal revision. The cross-disciplinary contribution would be to formalize the cohort-decay timing prediction with explicit attention to the survival function rather than the mean.
