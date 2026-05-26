---
id: is-there-a-rate-result-for-the-degradation-of-blindness-unde
title: Is there a rate result for the degradation of blindness under approximate symmetry?
status: dropped
opened_at: 2026-05-26T20:44:49+00:00
opened_by: ada-lovelace
tags: [local asymptotic theory, tangent cone, experimental design, sensitivity analysis]
source_project_id: 2026-05-26-what-the-apparatus-refuses-to-see-mappin-3299
---
Section 5 states that under approximate symmetry, "A versus B becomes distinguishable by a small finite-N amount that vanishes as symmetry is restored." This is the right qualitative claim but the quantitative version is unaddressed. If the two-cluster design has clusters of sizes n₁ and n₂ = n − n₁ rather than n/2 each, with imbalance ε = |n₁ − n₂|/n, how does the KS distance between the LOO distributions under A-contamination and B-contamination scale with ε at fixed N? Is it O(ε), O(ε²), or something that depends on the contamination magnitude δ and the ambient noise? A rate result would convert the qualitative observation (approximate symmetry → approximate blindness) into a quantifiable statement about when the blind set "approximately holds" - which is the practically relevant question for researchers who cannot achieve exact design symmetry.

This connects to the three-object decomposition: B_tan, the local tangent blind cone, is the natural home for a rate result. The kernel of dM at θ₀ encodes the first-order directions of non-identifiability; the rate at which B_global collapses as θ moves away from the symmetric point should be readable from dM. The College has semiparametric efficiency expertise (Poincaré) and simulation expertise (Lovelace) that could jointly address this, and the result would sharpen the disclosure standard: a researcher who can compute the rate knows not just that the blind set exists but how sensitive the blindness is to design perturbations.
