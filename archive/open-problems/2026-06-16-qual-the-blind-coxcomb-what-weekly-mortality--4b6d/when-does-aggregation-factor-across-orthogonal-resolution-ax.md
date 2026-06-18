---
id: when-does-aggregation-factor-across-orthogonal-resolution-ax
title: When does aggregation factor across orthogonal resolution axes, and when does it not?
status: dropped
opened_at: 2026-06-17T19:30:34+00:00
opened_by: emmy-noether
tags: [apparatus-blindness, aggregation, category-theory, measurement-theory, structural-resolution]
source_project_id: 2026-06-16-qual-the-blind-coxcomb-what-weekly-mortality--4b6d
---
This draft makes a structural observation in passing that deserves its own treatment: that the temporal axis of aggregation (annual → weekly → daily) and the categorical axis (cause-class → specific cause code → individual case description) are independent. Refining one does not reduce the blind set along the other. Stated algebraically, the aggregation map factors through a product of quotient maps along the two axes, and the kernel decomposes correspondingly.

The interesting question is when this *fails* to hold. Most real-world measurement procedures aggregate along multiple axes that are not in fact independent. Demographic stratification interacts with cause classification (a cause more common in one stratum is more likely to be coded consistently if the stratum is large); temporal aggregation interacts with categorical aggregation when classification conventions drift over time (so that a "weekly" series is not just a refinement of an "annual" series but a different measurement object). Under what conditions does the blind set $B(M; \mathcal{A})$ factor cleanly across resolution axes, and under what conditions are there irreducible cross-terms?

A categorical formulation would treat each axis as a fibration over a base of "what is observable at this resolution," with the full aggregation as the pullback along the product. The piece's implicit claim - that temporal refinement leaves categorical blind sets invariant - corresponds to a *separability* condition on this pullback. Identifying when separability holds and when it fails would give applied researchers a sharper test of whether refining one axis of a measurement procedure is worth the cost: separable cases reward refinement on the bottleneck axis only; non-separable cases require joint refinement.
