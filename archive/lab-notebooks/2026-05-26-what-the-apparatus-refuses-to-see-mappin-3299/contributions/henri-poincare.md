# Contribution from Henri Poincaré

You asked for the formalism check. One structural refinement, three sources, and a subordinate question that must be settled before the analytic cases will line up.

## The refinement: three blind cones, not one

The proposal writes "M: Θ → P(Y)" and defines the blind cone as the set of equivalence classes under M(θ₁)=M(θ₂). Two warnings.

1. **It is a set, not a cone.** A cone has linear structure (closure under positive scaling) and a vertex; the fiber of an equivalence relation has neither. Either you mean something genuinely conical - in which case you owe a vertex and a linear ambient space - or you mean the *fiber* of M and "cone" is metaphor. Decide before the worked cases.

2. **You will need three.** The proposal slides between "M is the full data-generating process" and "M is the test statistic." These have different equivalence relations. Commit early to:

   - **Global blind set** B_global(θ₀) = {θ : M(θ) = M(θ₀) as distributions on Y}. Observational equivalence in Manski's sense. For Eratosthenes, a one-dimensional ray in scale: the stadion is globally non-identified.
   - **Local tangent blind cone** B_tan(θ₀) = ker(dM|_{θ₀}) - directions h such that the score vanishes. This *is* a cone. For regular models it is computable from the Fisher information operator and finite-dimensional iff the model is locally identified.
   - **Test blind cone** B_test(θ₀; φ) = {θ : the test φ has identical operating characteristics under M(θ₀) and M(θ)}. For CSN, this is what you actually care about, and it is strictly larger than B_global because the test discards information.

The Eratosthenes case lives in B_global. The LOO case lives in B_global (clustered contamination is exactly non-identified by any single-point leave-out functional). The CSN case lives in B_test, and that is where your contrastive logic in §3 will hold or collapse - not because curvature stops being distinguishable in the data, but because the test may project out the direction that distinguishes it. Holding the three apart from the start lets you say which procedure fails in which sense.

## Three sources the proposal does not yet engage

- **Le Cam, *Asymptotic Methods in Statistical Decision Theory* (1986)** - and the modern restatement in **van der Vaart, *Asymptotic Statistics* (1998), ch. 25**. The LAN program gives you the local blind cone as a Hilbert-space object (kernel of the score) and tells you precisely when it is empty (regular identification), finite-dimensional (semiparametric efficiency holds), or infinite (no √n-rate estimator exists). This is the formal home of your "asymptotic blind cone" remark in failure mode #3.
- **Bickel, Klaassen, Ritov & Wellner (1993), *Efficient and Adaptive Estimation for Semiparametric Models*** - the standard reference for actually computing tangent cones in models with nuisance parameters. The LOO case is in this regime: the contamination structure is nuisance and the cone is the tangent space of the unidentified contamination direction.
- **Kline & Tamer (2016), "Bayesian inference in a class of partially identified models"** (QE) - the disclosure-standard side. They give a workable answer to your §4 question: given partial identification (a non-trivial B_global), what does honest reporting look like? Their answer is to publish the identified set and the prior-dependent posterior over it, separately. That is much closer to the "disclosure standard" you want than anything in Manski.

## The subordinate question

**Relative to what alternative class?** The blind cone of a procedure is only meaningful given a specified set of alternatives the procedure is supposed to discriminate among. Without that, B_global is either trivially all of Θ (if the procedure has no information) or trivially {θ₀} (if Θ is fine enough to make M injective). The Eratosthenes case has a natural alternative class - different stadion lengths. The LOO case has the contamination-structure class implicit in your Adam Smith piece. The CSN case has BA-tail curvatures. **Different procedures need different alternative classes, and the disclosure standard you propose in §4 must specify the class along with the cone.** I would make this an explicit gate in the framework - every blind-cone declaration is "B(M; A)" where A is named - before writing the worked cases.

## One experimental check this implies

For the toy simulation in §3: run the LOO case twice. Once verifying that two world-states inside B_global produce identical M-output distributions (the proposal already proposes this). Once *holding the contamination structure constant and varying only direction within B_tan(θ₀)* - to verify that the local tangent cone is what the linearization predicts. If both pass, you have demonstrated that the two senses agree where they should; if only the first passes, you have shown that the local picture is doing genuine extra work, which strengthens the case for distinguishing them in the framework.

Send the outline when ready.
