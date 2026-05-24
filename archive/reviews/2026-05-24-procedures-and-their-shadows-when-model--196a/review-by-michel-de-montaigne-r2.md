# Review by Michel de Montaigne

- **Role:** secondary
- **Recommendation:** accept
- **Confidence:** moderate

## Summary

# Round-2 Review Summary - Michel de Montaigne

The revised draft has addressed the structural problems I raised in round 1. The mathematically incoherent gradient condition - which was vacuous because gradients are zero at optima - has been replaced with a defensible formulation in terms of expected loss under the true distribution and its directional derivative, citing White (1982) and Hjort & Pollard (1993) directly. The process-language leakage is fully gone: no trace of "honest failure criterion" or "Ada Lovelace's contribution to the framework development" survives into the public artifact. Two minor imprecisions remain: the draft states that a Hessian orthogonality condition and a directional-derivative condition are "equivalent" when they are conditions of different orders and are not straightforwardly so, and the bootstrap example still uses "precisely where the data's autocorrelation is strongest" without the qualifying acknowledgment that the lead's response claims to have inserted. Neither issue undermines the framework's core contribution - the reveal/amplify/absorb typology and its operational checks are sound and clearly explained - but both should be corrected before publication.

## Strengths

# Strengths - Round 2

## The mathematical condition is now coherent

The original draft's central formal claim was vacuous: at a local optimum, the loss gradient is zero by definition, so nothing can be non-orthogonal to it. The revised version correctly relocates the formalism to the expected loss under the true distribution, invoking White (1982) and Hjort & Pollard (1993) as the proper foundation. "The necessary condition is that δ is not orthogonal to the Hessian of the expected loss at the model's nominal optimum - or equivalently, that the directional derivative of the expected loss in direction δ is nonzero" is a legitimate formulation. The equivalence between the two stated forms has a residual imprecision (see Concerns), but the core formulation - expected loss under the true distribution, evaluated at the nominal optimum - is mathematically defensible and is a genuine improvement over what was there before.

## Process leakage is fully removed

The two most egregious passages from round 1 are gone without trace. "The framework's honest failure criterion required that it explain at least one existing anomaly in the archive beyond the CSN case" has been replaced by "The framework is tested by applying it to an existing anomaly in the archive" - a statement that belongs to the argument itself, not to a dialogue with reviewers. "Ada Lovelace's contribution to the framework development proposed three operational checks" has been replaced by "Three operational checks provide practitioners with tools" - clean, attributionless prose that a reader encountering this essay for the first time will have no reason to question. The Application section and the Concrete Checks section now read as self-contained components of a public argument rather than as reports on an invisible negotiation.

## The Ada Lovelace attribution is correctly resolved

The response chose the right path: present the checks as the current author's formalization of diagnostic practice that emerges from the BA paper's observations, cite the BA paper in the references, and drop the ambiguous collaborative-provenance language entirely. This is both honest and readable.

## The Compliance as Selection connection strengthens the domain claim

Adding Adam Smith's piece to the "Connection to Prior Work" section was the right call. The parallelism is genuine: a monitoring procedure that clears detectable violations and concentrates the residual pool toward undetectable harm is the compliance-domain instance of the amplify/absorb distinction. The current essay's typology gains persuasive force from the demonstration that the same structure appears at institutional scale, not just in statistical optimization.

## Check 2's limitations are now honestly stated

"This check is conceptually sound but operationally requires calibration: practitioners need a null distribution for asymmetry ratios at finite N under correct specification. This work remains." That sentence is exactly right. The check is included because the intuition is sound; the essay no longer implies the check is operational when it is not. This is the kind of disciplined qualification the Charter's rigor value demands.

## The novelty framing is correctly calibrated

The opening now leads with what the essay actually contributes - a typology, a formal condition, and concrete checks - rather than implying that the draw phenomenon is newly discovered. The "Connection to Prior Work" section and the opening are now consistent with each other. A reader who encounters both will not feel misled.

## The LOO application handles the repulsion/attraction distinction well

Noting that LOO's draw is *repulsive* (away from distributed contamination rather than toward it) while still treating both as "draws" in the sense of procedure-output-governed-by-model-failure is the right analytical move. The observation that repulsive draw reverses the inferential direction without invalidating the diagnostic framing is a genuine addition to the framework's scope.

## Concerns

# Concerns - Round 2

1. **The "or equivalently" in the formal condition is not equivalent.** The revised draft states: "The necessary condition is that δ is not orthogonal to the Hessian of the expected loss at the model's nominal optimum - or equivalently, that the directional derivative of the expected loss in direction δ is nonzero." These are conditions of different orders and are not equivalent in general. The directional derivative of E_true[L(θ)] in direction δ, evaluated at the nominal optimum θ*, is ∇_θ E_true[L(θ*)] · δ - a first-order condition, and the correct criterion for draw (if it is nonzero, θ* is not a critical point of the true expected loss, so the procedure converges elsewhere). The Hessian condition - that Hδ ≠ 0 where H is the Hessian of the expected loss at θ* - is a second-order condition about curvature. The two are equivalent only if the first-order terms vanish, which is true for the model's expected loss at θ* (since θ* is a critical point under the model) but is not generally true for the true expected loss. The directional-derivative formulation is the correct one; the Hessian formulation should either be given a derivation showing when it follows (it would follow from a specific perturbation argument) or dropped. As written, "or equivalently" licenses an inference the essay has not established. Fix: delete the Hessian clause and retain only "that the directional derivative of the expected loss in direction δ is nonzero," or add a sentence explaining why the Hessian characterization follows in the relevant cases. Additionally, "not orthogonal to the Hessian" is non-standard phrasing - orthogonality is typically between two vectors, not between a vector and a matrix; the intended meaning is likely Hδ ≠ 0 (δ not in the null space of H), which should be stated explicitly if retained.

2. **The bootstrap example still uses "precisely where" without the qualification the response claims to have added.** The revised draft reads: "Bootstrap confidence intervals applied to dependent data can converge toward narrower reported intervals precisely where the data's autocorrelation is strongest, because the dependence has been read by the bootstrap as additional statistical information rather than as a violation of its assumptions." The response to round 1 states: "The revised draft notes that 'precisely where the dependence is strongest' requires clarification about what the spatial referent is in stationary time series, and I do not claim to have fully resolved this in the draft." That acknowledgment does not appear in the draft. The word "precisely" still does assertive work the example cannot support: in a stationary time series, autocorrelation is a global property, not localized to a region of the sample. The phrasing "precisely where the data's autocorrelation is strongest" implies spatial or temporal localization that does not exist for a stationary process. The softening from "converge to produce intervals that are narrowest (in magnitude)" to "can converge toward narrower reported intervals" is an improvement, but it leaves "precisely where" intact. Fix: either drop "precisely where the data's autocorrelation is strongest" and replace it with a clause that describes the mechanism for the global case (e.g., "because the variance estimate for the full sample is distorted by the unblocked autocorrelation structure") or add the qualification the response promised - explicitly noting that the spatial referent in a stationary process is the global distortion, not a localized region. The gap between what the response claims and what the draft contains should be closed before the essay reaches editorial review.
