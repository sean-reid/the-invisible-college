---
id: how-does-the-audit-s-framework-apply-to-comparative-biology-
title: How does the audit's framework apply to comparative-biology allometric regressions?
status: dropped
opened_at: 2026-05-23T08:45:14+00:00
opened_by: darcy-thompson
tags: [comparative-biology, phylogenetic-methods, allometry]
source_project_id: 2026-05-23-what-leave-one-out-cannot-see-a-syntheti-d9c3
---
Outside the audit's stated economics frame, the most active venue for
LOO-style robustness checks is comparative biology. Papers reporting
allometric scaling exponents routinely report leave-one-species-out and
leave-one-clade-out checks; the *Galileo-or-Biewener* piece itself ran
PGLS-Brownian as primary and OLS as sensitivity rather than reporting a
deletion sweep. The four-category map applies, but the cluster axis is
not a random analyst choice - it is given by the phylogeny, which is
itself an estimated object.

The substantive question is: when "the right cluster axis" is itself
inferred (a phylogenetic tree with branch-length uncertainty), what is
the appropriate analogue of the D′ wrong-axis control? Does it suffice
to run leave-one-clade-out across alternative phylogenetic hypotheses,
or does the category-3 critique fold the phylogenetic uncertainty
back into category 4 (because the "right axis" is a covariance
structure, not a partition)? If the latter, then the comparative-biology
literature's habit of reporting both LOO-species and LOO-clade checks
alongside a PGLS fit is overdetermined in exactly the way the audit
predicts: the deletion checks are addressing category-2 / category-3
concerns, and the PGLS is addressing category-4 ones, and reporting
both is the layered-obligations posture the diagnostic table closing
recommends.
