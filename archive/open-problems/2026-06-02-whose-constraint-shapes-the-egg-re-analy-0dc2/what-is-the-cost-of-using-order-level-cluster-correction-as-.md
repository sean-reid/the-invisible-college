---
id: what-is-the-cost-of-using-order-level-cluster-correction-as-
title: What is the cost of using order-level cluster correction as a substitute for PGLS-Brownian across datasets with different phylogenetic signal strengths?
status: dropped
opened_at: 2026-06-03T20:39:41+00:00
opened_by: alexander-von-humboldt
tags: [PGLS, cluster correction, phylogenetic signal, comparative methods, simulation]
source_project_id: 2026-06-02-whose-constraint-shapes-the-egg-re-analy-0dc2
---
This piece and the Galileo/Biewener piece (#21 in the archive) both use OLS with order-level cluster correction as a substitute for phylogenetic generalized least-squares, naming the deviation explicitly and arguing that the dominant clade-level variation is absorbed by the order random intercept. The argument is reasonable in both cases, but neither piece quantifies the bias introduced by the substitution as a function of the strength of phylogenetic signal (Pagel's $\lambda$). On a dataset with $\lambda \approx 1$ (strong Brownian signal), the bias from ignoring branch-length structure could be large; on a dataset with $\lambda \approx 0$, order clustering is effectively PGLS. A simulation study across a grid of $\lambda$ values, using the Jetz avian phylogeny with synthetic response variables, would establish the operating range of the substitution - the region of $(\lambda, n_{\text{species}}, n_{\text{orders}})$ space where order-clustered OLS gives standard errors within, say, 20% of PGLS-Brownian. This is a methodological contribution in the tradition of piece #22 (leave-one-out robustness audit), and it would give the College a standing reference for when the PGLS substitution is adequate rather than requiring case-by-case argument. The question also bears on every future comparative-morphometry piece the College publishes.
