# Review by Adam Smith

- **Role:** outside
- **Recommendation:** minor
- **Confidence:** confident

## Summary

# Round-2 Review Summary - Adam Smith

The revised draft achieves the correction it most needed: the formal condition is restated in terms of expected-loss derivatives and the Hessian of the expected loss, replacing the vacuous "gradient at the optimum" formulation that was the piece's deepest structural flaw in Round 1; the aggressive biconditional is replaced by a stated necessary condition supported by case-by-case sufficiency. The Compliance as Selection cross-reference is now integrated into the Prior Work section at exactly the right moment, the Ada Lovelace attribution is cleanly removed, polynomial regression has been dropped from the main example list, and no process-language narrative survives in the draft. Two precision issues remain: the bootstrap CI example retains a spatial localization claim ("precisely where the data's autocorrelation is strongest") that is not well-defined for stationary time series, and the formal condition describes δ as a direction in function space while the Hessian condition operates in parameter space, leaving a gap that a careful reader will notice. The draft is close to publication-ready and the remaining repairs are narrow enough for editorial handling.

## Strengths

# Strengths - Round 2

## What Got Better

**The mathematical condition is now defensible.** The prior draft's "not orthogonal to the gradient of the loss function at the optimum" was self-defeating: at a local optimum the gradient is zero by construction, so the condition was vacuous. The revised formulation - δ non-orthogonal to the Hessian of the expected loss, equivalently the directional derivative of expected loss in direction δ is nonzero - correctly captures the substance of White (1982) and Hjort-Pollard (1993). The biconditional has been replaced by an explicit necessary condition, which is more honest about what the working examples establish.

**The Ada Lovelace attribution is completely removed.** The three operational checks are now presented as the current author's formalization, with the BA model paper credited for demonstrating the sample-size-drift pattern. Intellectual credit is now correctly assigned.

**Polynomial regression has been excised from the main example list.** The corrected list (CSN, bootstrap CI, MLE under finite-sample bias) does not include the near-tautological polynomial case. The two surviving examples carry genuine argumentative weight and are better-differentiated from one another.

**The Compliance as Selection connection is now made explicit.** Lines 79–80 name the compliance monitoring paper directly and articulate the structural identity: a monitoring procedure clears what it can detect, concentrating the residual pool toward violations the procedure cannot see - the same selection artifact operating at institutional scale rather than statistical scale. This is the piece's strongest claim to domain generality, and it now appears in the text.

**All process-language narrative is gone.** The draft reads throughout as a self-contained public argument. No phrase sounds like a response to reviewers or an account of what the draft used to say. This was the most common failure mode across Round 1 drafts in the archive and the revision avoids it cleanly.

## What Stayed Strong

**The three-mode typology remains the piece's best contribution.** Reveal, amplify, and absorb are not relabeled versions of a single observation; each licenses a different inferential response, and the revised draft makes this more precise by explicitly addressing the asymmetry between modes in what external checks are required.

**The CSN case is still the best-supported illustration.** The non-monotone pass-rate-with-sample-size pattern is tied directly to the BA model's finite-size correction term, and the account of why the pattern reverses at large N - the correction becomes negligible relative to tail length - is the right kind of specificity. This is the piece's empirical anchor and it holds.

**The negative case (quasi-MLE, heteroscedasticity) remains the formal condition's strongest moment.** A researcher cannot use the MLE output location to diagnose heteroscedasticity and must check by other means. A framework that specifies when a tool cannot do something a practitioner might expect is more useful than one that enumerates only positive cases.

**The LOO application is now better framed.** The revised draft presents the LOO section as a stress-test of the framework's generality rather than as a straightforward application. The "repulsive draw" framing - the procedure is drawn away from distributed contamination toward isolated high-leverage observations - is less formally rigorous than the CSN case, but presenting it explicitly as a generalization attempt rather than a confirmed case is honest about the difference. The diagnostic insight (if LOO identifies a single point while bias is distributed, the structure of contamination is itself revealed) remains valuable.

## Concerns

# Concerns - Round 2

1. **Bootstrap CI localization claim is still not resolved.** The response committed to qualifying "precisely where the data's autocorrelation is strongest" as an illustrative sketch of the amplify mechanism rather than a verified empirical claim. The draft still reads: "Bootstrap confidence intervals applied to dependent data *can* converge toward narrower reported intervals *precisely where* the data's autocorrelation is strongest." The hedge "can" softens the modal force but does not address the substantive problem: for a stationary time series, autocorrelation is a global property of the process, not something localized at a position in input space where the CI can be "precisely" narrower. The spatial referent of "where" is undefined. If the intended claim is that block-bootstrap CIs under positive serial dependence are on average too narrow, that is documentable and worth stating. If the claim is that narrowness is maximized at a specific location identifiable from the procedure's output, that requires a non-stationary setting and an argument about where the nonstationarity is strongest - an argument the draft does not provide. The response said this would be qualified; the draft does not qualify it. Editorial should either excise "precisely where the data's autocorrelation is strongest" and replace with a statement about average bias direction, or supply the conditions (non-stationary process, identified structural break location) under which the spatial claim becomes defensible.

2. **The δ-in-function-space versus Hessian-in-parameter-space gap persists.** The formal condition (lines 23–26) defines δ as "the direction in function space along which the misspecification operates" and then states the necessary condition as "δ is not orthogonal to the Hessian of the expected loss at the model's nominal optimum." The Hessian of the expected loss is a bilinear form on parameter space, not on function space. Orthogonality between a vector in function space and an operator on parameter space is not defined without an explicit mapping between the two spaces. For the CSN example, both spaces collapse conveniently (the "function space direction" is the direction in which the KS distance increases, which maps directly to x_min in parameter space), but this collapse is specific to the example and not stated as the mechanism. The response acknowledged the original gradient-at-optimum problem and corrected it; the space-mapping gap is an inheritance from that correction. The repair is narrow: either define δ as a direction in parameter space (the direction in which the nominal model parameter value is displaced by misspecification), which is operationally what the examples use, or add one sentence naming the projection from function space to parameter space that the condition implicitly employs.

3. **"Repulsive draw" in the LOO section remains formally unmoored.** The draft states that both CSN and LOO "represent draws in the sense that the procedure's output is governed by its sensitivity to the model's departure from its null claim." This is true in a verbal sense but does not connect to the formal apparatus. The necessary condition (Hessian non-orthogonality) was designed for attractive draw toward a misspecification region in parameter space. The draft does not provide an analogous formal condition for repulsive draw in deletion space. The response acknowledged this is "a stress-test of the framework's generality" and that the mechanism differs; the draft now reflects this framing (lines 67–71 are clearer than the original). But the claim "Both represent draws" invites the reader to believe the formal apparatus covers both cases equally, which it does not. A one-sentence acknowledgment that the formal condition has not been extended to deletion-space optimization - and that the LOO case is argued by analogy rather than by the framework directly - would be sufficient. This is not a request to redo the LOO section; it is a request for one sentence of honesty about the formal scope.
