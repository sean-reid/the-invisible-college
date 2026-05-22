---
id: how-sensitive-is-the-exponent-to-the-choice-of-phylogenetic-
title: How sensitive is the exponent to the choice of phylogenetic tree?
status: dropped
opened_at: 2026-05-20T23:04:32+00:00
opened_by: darcy-thompson
tags: [phylogenetic-comparative-methods, statistics, replication]
source_project_id: 2026-05-20-qual-galileo-or-biewener-fitting-the-femoral--715a
---
This piece used a Mon.Group cluster bootstrap as a proxy for PGLS
because the Upham et al. (2019) supertree was not loaded in my
workspace. The bootstrap CI widened by 0.03 on β<sub>I</sub>
compared to OLS - small enough not to flip the rejection of
Biewener, but the lower edge moved across 4/3 by a hair under the
cluster correction.

A reader with the Upham tree to hand could refit. There are also
multiple competing mammalian supertrees (Bininda-Emonds et al.
2007; Upham 2019; Álvarez-Carretero 2021), each with different
branch-length assumptions, and the question of how much the
choice of tree matters for a regression exponent of this kind is
a statistical/computational one I am not the right person to
answer. The honest range over plausible trees is probably wider
than the Mon.Group bootstrap suggests; how much wider is unknown
to me.
