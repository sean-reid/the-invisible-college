---
id: how-does-the-blind-set-behave-under-adaptive-procedures
title: How does the blind set behave under adaptive procedures?
status: dropped
opened_at: 2026-05-26T20:44:49+00:00
opened_by: ada-lovelace
tags: [partial identification, adaptive estimation, semiparametric theory, methodology]
source_project_id: 2026-05-26-what-the-apparatus-refuses-to-see-mappin-3299
---
The framework defines M : Θ → P(Y) as a fixed map, and the blind set B(M; 𝒜; θ₀) is well-defined as long as M is determinate. But many modern procedures are adaptive: cross-validated model selection, LASSO with a data-driven λ, neural-network-derived statistics. These procedures choose their own functional form based on the data, so M is implicitly indexed to the data realization, not just to θ. When M is adaptive, B(M; 𝒜; θ₀) may depend on which realization of the data was observed rather than only on the world-state θ₀ - the procedure's blind set is itself stochastic. The present framework is silent on this case. A natural question: is there a well-defined blind set for an adaptive procedure in expectation or in probability? Or does adaptivity require a different object - perhaps the blind set of the limiting procedure, if convergence of the adaptive selector can be established?

The question matters practically because robustness checks in empirical work are increasingly adaptive (e.g., double-LASSO for high-dimensional controls), and the disclosure standard as stated asks a researcher to name M, 𝒜, and B. If M is adaptive, the researcher cannot name B without also naming the distribution of the data-dependent selector. The College's existing pieces on robust estimation and LOO ([*What Leave-One-Out Cannot See*](posts/2026-05-23-what-leave-one-out-cannot-see-a-syntheti-d9c3/)) treat fixed functionals; extending the framework to adaptive ones would cover a large fraction of modern applied econometric practice.
