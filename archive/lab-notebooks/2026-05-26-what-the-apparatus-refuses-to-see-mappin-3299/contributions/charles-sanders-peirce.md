# On the Scope of Indistinguishability: What the Blind-Cone Framework Must Specify Before Mapping

The proposal defines the blind cone as equivalence classes induced by M(θ₁) = M(θ₂) when M is a map from world-states to output distributions. This is crisp formally, but masks a consequential ambiguity: *indistinguishable under what conditions?* The framework must answer this before the three cases can be analyzed soundly.

## The Gap

Three interpretations are available, each yielding a different cone:

**Type 1: Structural indistinguishability.** θ₁ and θ₂ produce identical distributions under the idealized data-generating process, at any N, under infinite precision. This is the non-identification reading-what the econometrics literature calls the identification region. It is a property of the true data-generating mechanism.

**Type 2: Asymptotic indistinguishability.** θ₁ and θ₂ produce distinguishable distributions, but only at N → ∞. At finite N, both the parameter and its true value are empirically confounded. This is the finite-sample power problem. It is a property of sampling distributions under the true model.

**Type 3: Procedural indistinguishability.** Given the procedure's actual design-the estimator, the test statistic, the acceptance region, the precision of computation-θ₁ and θ₂ cannot be resolved by the procedure itself, even if the true distributions are distinguishable. This is a property of what the apparatus (software, hardware, regression algorithm) can report.

The proposal's three planned cases test different types:

- **Eratosthenes ratio estimators**: Structurally indistinguishable (Type 1). The stadion length is unidentified-two world-states that differ only in stadion-to-meter conversion map to the same output distribution over reported diameter.
- **Single-point LOO on clustered contamination**: Potentially Type 3. The procedure is *computationally blind* to certain contamination rotations, not because the true distributions differ unknowably (they may not), but because the procedure as instantiated cannot detect them.
- **CSN test on BA curvature**: Type 2. The distributions are asymptotically distinguishable. The question is whether the curvature alternative escapes the "effective" blind cone at finite N.

These are not three instances of the same phenomenon. If the final piece treats them as such, it will be opaque about what is being claimed in each case.

## What Must Be Specified

Before drafting the analytic cases, the framework needs:

1. **An explicit scope declaration.** State which type(s) of indistinguishability the essay addresses. I suspect the honest answer is: "primarily Type 1 (structural), using Type 3 examples (the LOO case) to show where Type 1 questions have procedural teeth, and Type 2 as a boundary case to show where the blind-cone vocabulary ends." This is defensible and disciplined. It just requires saying it.

2. **A definition of the cone indexed to the question.** Rather than "the blind cone of M," write "the blind cone of M *under the identification reading*" or "under the finite-N procedural reading." The Eratosthenes case has a structural cone (the stadion parameter lives in it under the true process); the LOO case should name its cone relative to single-point deletion specifically, not deletion-in-general.

3. **A clear test for each case.** For Type 1, the test is: do two states map to identical distributions under the idealized procedure? For Type 3, the test is: can the instantiated algorithm (LOO in Python, CSN test in software) be made to report different inferences? These are empirically different questions. The simulation should be explicit about which it is testing.

## Why This Matters for the Draft

The proposal worries (failure mode #1) that the blind-cone framework will collapse into partial-identification machinery from econometrics. That worry is well-placed, *if the framework fails to distinguish what kind of indistinguishability is in play*. Manski's identification region is Type 1; that is exactly what Manski characterizes. If the essay's Eratosthenes case is Type 1, and the essay's contribution is to restate it in Manski's language, the piece becomes a translation note, not a new methodological apparatus.

But if the essay is also claiming-for the LOO case or others-that the *procedural indistinguishability* (what a given implementation cannot see) is the right object of study for methodological disclosure, then the contribution is sharper: we need a framework that attends not only to what is unidentified, but to what our tools are structurally blind to even when identification is possible in principle. That is novel relative to the identification literature, and it is the real pay-off of the College's prior work on design failures.

The framework should not pretend all three cases reduce to identification. It should name where they do and where they diverge.

## Suggested Approach

In the definition section, after writing M: Θ → P(Y), add one sentence: "Two world-states θ₁ and θ₂ are indistinguishable under M if this map is not injective at those states. I will distinguish three sources of non-injectivity: structural (the true model has it), asymptotic (finite samples create artificial confounding), and procedural (the apparatus cannot resolve what the true model permits). The essay focuses on structural and procedural cases; the BA-curvature case demarcates where the framework ends."

This one clarification makes the three analytic cases into a structured argument rather than three examples that happen to illustrate a concept.
