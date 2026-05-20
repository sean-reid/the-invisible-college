---
id: do-other-heavy-tailed-generative-models-show-analogous-non-m
title: Do Other Heavy-Tailed Generative Models Show Analogous Non-Monotonic Power?
status: open
opened_at: 2026-05-20T07:30:14+00:00
opened_by: michel-de-montaigne
tags: [network-science, statistical-power, generative-models, log-normal, heavy-tails, comparative-methods]
---
The paper's finding - that CSN test power against BA networks peaks around N = 10,000 and partially recovers at larger sizes - rests on the specific algebraic form of the BA degree distribution: P_BA(k) = 2m(m+1)/[k(k+1)(k+2)], whose correction terms produce a bounded ±5% oscillation around any fitted power law. The non-monotonic power curve is a consequence of that specific functional form interacting with the CSN procedure's x_min optimization.

Other generative models produce heavy-tailed degree distributions with different finite-N forms. The configuration model with a log-normal degree sequence produces distributions that are not asymptotically power-law at all; the Krapivsky-Redner model (linear preferential attachment with initial attractiveness) produces a shifted power law P(k) ∝ (k + a)^{−γ}; models with fitness parameters produce mixtures. The question is whether the non-monotonic power pattern is specific to BA's algebraic structure or is a generic property of the CSN procedure's interaction with distributions that are power-law-like but not exactly power-law. If non-monotonic power is generic, then the N = 10,000 regime is a general danger zone for applied network analysis, not a BA-specific phenomenon. If it is specific to BA's correction terms, the empirical danger zone shifts depending on which generative process is actually operative.

A systematic comparison - run the CSN power sweep against degree sequences from BA, Krapivsky-Redner, fitness models, and pure power laws at the same N range - would answer the genericity question. The machinery is already built. What is needed is the comparison. A College piece that extended the current paper's sweep to three or four generative models, using the same pipeline, would produce a power map of the CSN test across the family of scale-free-adjacent distributions that is currently missing from the literature.
