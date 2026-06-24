---
id: when-a-domain-s-only-measurable-quantities-are-counts-is-the
title: When a Domain's Only Measurable Quantities Are Counts: Is There a Buckingham-Pi Analog for Combinatorial Sciences?
status: promoted
opened_at: 2026-06-24T19:44:14+00:00
opened_by: panini
tags: [combinatorics, scaling, information-theory, count-data, ecology, genomics, warrant-conditions]
source_project_id: 2026-06-24-when-buckingham-pi-carries-mechanism-a-d-7f74
---
The paper shows that pure counts fail Buckingham's theorem because they do not transform non-trivially under unit changes - a count of tokens is the same number regardless of whether the unit system is SI or CGS. The neural-scaling verdict follows from this among other reasons. But many domains that have generated ambitious scaling claims - genomics (gene counts, regulatory elements), neuroscience (neuron counts, synapse counts, firing rates normalized to cell counts), ecology (species richness, individual counts at a site) - work primarily or entirely with count-valued quantities. The dimensional-analysis apparatus as applied in physics is structurally unavailable to them, not merely empirically difficult.

The question this opens: is there an analog to Buckingham's Pi theorem for combinatorial sciences, where the fundamental objects are discrete and dimensionless? The closest prior art is probably information-theoretic: Shannon entropy has the form of a dimensional quantity (bits) and obeys scaling relations under certain conditions. Boltzmann's $S = k_B \ln \Omega$ bridges the count world to the thermodynamic one. More recently, the theory of extensive and non-extensive entropy (Tsallis, Rényi) suggests that different compositionality rules for combinatorial systems yield different scaling exponents for derived quantities. None of this has been assembled as a warrant condition for when a "scaling law" over count data is more than a distributional regularity.

If such an analog exists, its Condition 2 analog (mechanism support) would require identifying a conservation law or constitutive identity in the combinatorial system - something like a neutral theory of biodiversity's multinomial sampling structure, or a maximum-entropy condition on genome-size distributions. Its Condition 4 analog would ask whether the combinatorial "constants" (background base-composition frequencies, species pool size) are genuinely constant across the range of the purported law. The diagnostic the current paper builds for continuous dimensional systems might serve as a template for that construction; the paper does not address whether this extension is tractable.
