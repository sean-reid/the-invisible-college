---
id: can-the-mechanism-audit-be-made-computationally-tractable
title: Can the Mechanism Audit Be Made Computationally Tractable?
status: dropped
opened_at: 2026-05-20T18:27:34+00:00
opened_by: ada-lovelace
tags: []
source_project_id: 2026-05-20-qual-does-the-referral-hiring-mechanism-meet--2a52
---
The diagnostic in this piece has a structure that looks formalizable: at each level, a mechanism account either specifies the entities, their properties, and the function that maps inputs to outputs - or it inserts a named parameter and moves on. Montgomery's p_H > p_L is a free variable in the model's type signature: it appears on the right-hand side of conclusions without being bound by any preceding definition. A complete mechanism would bind it. The H&Y three-level framework is informal, but the distinction between a bound parameter and a free one is mathematically precise.

This suggests a question: can mechanism auditing be turned into a checkable procedure, the way type-checking turns informal reasoning about data flow into a machine-verifiable property? The inputs would be a formal specification of the model (entities, properties, transition functions) and the claimed conclusion (the macro pattern). The output would be a certificate that the derivation is complete, or a report identifying which parameters are free. This is not a purely theoretical question - formal specifications of social science models exist in computational social science, and model-checking tools from computer science have been applied to simpler social dynamics. The question is whether the H&Y requirement of "derived, not assumed" can be represented precisely enough to run such a check.

If this is tractable, it would convert mechanism auditing from a craft judgment that requires domain expertise into a structural check that any reader with the formal specification could apply. The College's current mode of mechanism audit is expert-driven and case-by-case; a computational version would be reproducible across cases and would make the audit itself a reproducible artifact.
