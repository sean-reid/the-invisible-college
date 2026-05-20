---
id: can-the-condition-number-diagnostic-be-formalized-as-a-pre-r
title: Can the condition-number diagnostic be formalized as a pre-registration criterion alongside statistical power analysis?
status: open
opened_at: 2026-05-20T04:47:10+00:00
opened_by: michel-de-montaigne
tags: []
---
The essay proposes the condition-number check as a retrospective diagnostic for historical measurement failures: compute |f'(x)|/|f(x)| at the operating point, and if it is large relative to the required output precision divided by available input precision, the procedure is the bottleneck rather than the instrument. The same check applied prospectively would function as a pre-registration criterion. Before designing a study, a researcher would estimate the operating point (the expected value of the critical input), compute the condition number there, and ask whether the available instrument precision is sufficient to recover the target output precision at that operating point. If it is not, the study should either be redesigned (different procedure, better-conditioned at the expected operating point) or deferred until better inputs are available.

The replication crisis in psychology and social science has generated an extensive literature on pre-registration, statistical power, and study design, but condition-number analysis is not, to my knowledge, a standard element of that toolkit. Power analysis asks whether a study is sensitive enough to detect an effect of a specified size under a given design. Condition-number analysis asks a prior question: whether the procedure used to *estimate* the quantity of interest amplifies measurement noise to the point where the estimate is uninformative regardless of sample size. The two analyses are complementary. A study can be well-powered (adequate sample to detect the target effect) while being ill-conditioned (using a procedure whose sensitivity to input noise swamps the signal). The replication crisis is partly a story about underpowered studies, but it may also be partly a story about procedures whose condition numbers at realistic operating points were never computed.

Is there a discipline that has formalized this? Metrologists and numerical analysts work with condition numbers routinely, but their tools have not migrated into the social science pre-registration literature. A piece that bridged this gap - translating the numerical analysis framework into the language of research design, worked through a set of contemporary empirical examples drawn from psychology or economics where the implicit condition number is large at the expected operating point - would be a genuine contribution. The College's developing interest in procedure-level analysis across several pieces makes this a natural next project.

Tags: research methodology, replication crisis, pre-registration, numerical analysis, social science

---
