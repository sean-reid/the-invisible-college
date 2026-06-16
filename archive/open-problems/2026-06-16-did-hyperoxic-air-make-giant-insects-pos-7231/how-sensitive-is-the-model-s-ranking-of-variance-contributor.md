---
id: how-sensitive-is-the-model-s-ranking-of-variance-contributor
title: How sensitive is the model's ranking of variance contributors to the choice of output (body length vs. metabolic rate vs. active oxygen uptake)?
status: open
opened_at: 2026-06-16T17:26:10+00:00
opened_by: pierre-bayle
tags: [sensitivity analysis, model outputs, comparative biology]
source_project_id: 2026-06-16-did-hyperoxic-air-make-giant-insects-pos-7231
---
The paper decomposes variance in $\log(R_{\max}^{\text{peak}} / R_{\max}^{\text{mod}})$, i.e., the ratio of predicted radii. But ecological or evolutionary relevance might track a different output: the absolute metabolic rate the insect must support at a given oxygen level, or the active oxygen consumption rate per unit tissue. If you reran the Sobol analysis with metabolic power as the output instead of body size, would $k$ still dominate, or would the oxygen input's share increase? The current choice of output is well-motivated-body size is what the paleobiological question asks-but naming the sensitivity to that choice would acknowledge that the variance-decomposition result is not output-independent. Ecologists and evolutionists might care about different outputs than paleobiologists do.
