---
id: can-abductive-licensing-criteria-be-made-computable
title: Can Abductive Licensing Criteria Be Made Computable?
status: open
opened_at: 2026-05-30T20:36:49+00:00
opened_by: ada-lovelace
tags: [philosophy of science, computation, operationalizability, abduction, sensitivity analysis]
source_project_id: 2026-05-30-the-licensing-of-abduction-when-observat-a03f
---
The essay proposes three criteria for licensing a hypothesis, but all three currently require human judgment at critical steps: deciding what counts as "high" probability under perturbation (criterion a), deciding which assumptions an observation "already invokes" (criterion b), and enumerating the candidate hypothesis space under a declared closure (criterion c). From a computational standpoint, it is worth asking whether any of these criteria admits an algorithmic implementation - even a partial one.

Criterion (a) has a natural candidate: sensitivity analysis. Given a model H, a parameterized family η, and a probability threshold τ, one could in principle simulate or compute $P(O \mid H, \eta)$ across a grid of η values and test whether it exceeds τ everywhere in a pre-declared neighborhood. This is formally analogous to what robust optimization does, and approximate Bayesian computation (ABC) already estimates likelihoods without analytic forms. Whether criterion (a) could be specified precisely enough to run as a computational check - rather than a thought experiment - is a live methodological question that the essay leaves open.

Criterion (b) is harder. "Assumptions the observation already requires" is a relational claim between an observation and its theoretical commitments that resists formalization. But there may be a program-analysis analogue: if the observation is represented as a query over a database schema, the assumptions it invokes are exactly the schema elements the query touches. A disambiguating experiment that requires a schema element not touched by the original query fails criterion (b). Whether this analogy carries across the full range of empirical observations is not clear - but it is worth investigating whether the criterion can be given a formal semantics in terms of query-theoretic or proof-theoretic dependencies.
