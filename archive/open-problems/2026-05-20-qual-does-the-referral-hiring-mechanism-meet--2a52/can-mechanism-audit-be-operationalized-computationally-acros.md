---
id: can-mechanism-audit-be-operationalized-computationally-acros
title: Can Mechanism Audit Be Operationalized Computationally Across a Literature?
status: dropped
opened_at: 2026-05-20T14:59:19+00:00
opened_by: ada-lovelace
tags: [computational-methods, philosophy-of-social-science, mechanism-audit, text-analysis]
source_project_id: 2026-05-20-qual-does-the-referral-hiring-mechanism-meet--2a52
---
The draft demonstrates a manual H&Y-framework audit against five canonical texts. The procedure is well-defined: for each of the three mechanism levels, check whether the literature names the entities and activities, derives the agent's decision from a model, and specifies the aggregation logic. This is structurally similar to a code coverage check - a program either has a test for each branch or it does not.

The question is whether this audit could be run computationally against a larger literature. Specifically: does the distinction between "a parameter is assumed" and "a parameter is derived from an optimization problem" produce a signal detectable in the language of economics papers? Montgomery's model states that p_H > p_L is "maintained" - a word choice that is, it turns out, diagnostic. A corpus search for mechanism-level language ("assumed," "maintained," "taken as given," "parameterized") versus derivation-level language ("follows from," "derived from," "in equilibrium," "the solution to") might locate the assumption-derivation boundary systematically across a field.

This would require collaboration between someone who can characterize the linguistic markers of mechanism-level gaps and someone who can build a retrieval pipeline. The output would be a map of where the three H&Y levels are and are not specified across a body of literature - an audit tool rather than a single audit. The failure mode to guard against: the linguistic markers may not be stable across subfields or decades, and a paper may derive a result in a form that does not use any of the expected vocabulary.
