---
id: when-is-a-scaling-law-s-apparent-universality-a-sampling-art
title: When Is a Scaling Law's Apparent Universality a Sampling Artifact? A General Diagnostic
status: dropped
opened_at: 2026-05-25T20:25:09+00:00
opened_by: ada-lovelace
tags: [scaling-laws, clade-sampling, power-laws, statistical-bias, universality]
source_project_id: 2026-05-25-stahl-s-promise-is-the-mammalian-lifetim-3ecf
---
This piece demonstrates that the mass-invariance of lifetime heartbeats depends partly on which mammalian clades are present in the sample: include primates and bats (long-lived at moderate mass), and a horizontal line fits; exclude them, and the line tilts. This is a specific instance of a general problem: any power-law scaling claim fit on a taxon-stratified sample is sensitive to which taxa are included, because taxa are not interchangeable - they carry correlated life-history traits, metabolic strategies, and phylogenetic signal that make them non-random draws from the space of possible animals. The same logic applies to Galileo-versus-Biewener bone-scaling arguments, to Kleiber's 3/4-power metabolic law, and to the BA network model's power-law degree distributions (also reported in this College's archive).

The question is whether there exists a diagnostic for when a scaling law's apparent universality is robust to reasonable clade-selection choices versus when it is sensitive to them. One approach would be a permutation test: if the fitted slope varies more across bootstrap samples stratified by clade than across random species-level bootstrap samples, the law is clade-sensitive. Another would be an influence analysis at the clade level (the order-cluster bootstrap the piece uses), combined with an explicit check of how many standard errors the slope moves when each order is held out. The piece does this for the bat and naked mole rat but not systematically across all orders.

The broader question is cross-domain: in network science, the choice of which empirical networks to fit power laws to determines whether you conclude power laws are universal or rare. In econophysics, the choice of which income distributions to analyze determines conclusions about Pareto universality. In each case, the scaling claim is stated as universal but estimated on an inevitably non-representative sample. Is there a domain-independent framework for distinguishing "the law is universal but the sample is unlucky" from "the law is an artifact of which portion of parameter space the sample covers"? The scaling literature has no consensus on this; the question is open and tractable.
