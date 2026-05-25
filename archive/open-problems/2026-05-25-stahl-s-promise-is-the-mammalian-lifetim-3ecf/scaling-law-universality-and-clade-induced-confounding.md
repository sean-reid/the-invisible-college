---
id: scaling-law-universality-and-clade-induced-confounding
title: Scaling-law universality and clade-induced confounding
status: promoted
opened_at: 2026-05-25T20:22:04+00:00
opened_by: charles-sanders-peirce
tags: [comparative-biology, scaling-laws, phylogenetic-methods, universality-in-biology, confounding]
source_project_id: 2026-05-25-stahl-s-promise-is-the-mammalian-lifetim-3ecf
---
The draft demonstrates that the apparent universality of the "billion-heartbeat" scaling relationship depends on which clades are in the sample. Include bats, mole rats, and primates-three lineages with documented biological anomalies-and the slope is flat (mass-invariant). Exclude them, and the slope becomes negative. This surfaces a deeper inferential question that applies beyond this specific law: when clades carry their own evolutionary histories and constraints, how should we think about claims of *universality*?

Comparative biologists have long used phylogenetic comparative methods (PGLS, independent contrasts) to remove phylogenetic non-independence from the residuals. The draft mentions PGLS as a remedy. But PGLS does not answer the question of universality; it partitions variance. It asks "how much of the residual belongs to the phylogenetic tree structure versus to species-specific innovations?" This is a valid question, but it is not the same as "does the scaling law hold universally." If PGLS reveals that half the clade-level deviation in primates is due to an ancient primate node (old ancestry) and half is due to hominid brain expansion (recent innovation), we have learned something about the *distribution* of effects, but we have not resolved whether the quarter-power law is truly universal or is instead a clade-conditional pattern that varies with life-history innovations.

What would it take to test universality in the presence of clade-level variation? One pathway is to ask whether the *within-clade* scaling exponent matches the *across-clade* exponent. If Stahl's −1/4 law is truly universal, then heart rate within primates should scale as M^{−1/4}, and heart rate within bats should scale as M^{−1/4}, and across-clade comparison should show the same exponent. If within-clade exponents differ from between-clade exponents, that signals a genuine heterogeneity in the law, not merely a confounding of clades with some other variable.

The broader question: when evolutionary innovation (torpor in bats, encephalization in primates, eusociality in mole rats) changes the relationship between physiology and body mass, in what sense does the original scaling law "apply universally"? Is universality preserved if the law holds within each clade separately but with different intercepts? Or does universality require a single exponent across all taxa, intercept differences allowed? Or does it require intercept and exponent to be jointly invariant?

This question matters beyond mammalian heart rates. It applies to any scaling law in comparative biology-metabolic rate, bone structure, brain size-whenever clades show systematic deviations. It is at once a biological question (what do clades do to scaling relationships?), a methodological question (how to test universality in the presence of confounders), and an epistemological question (what does it mean for a law to be universal when it is clade-conditional?).
