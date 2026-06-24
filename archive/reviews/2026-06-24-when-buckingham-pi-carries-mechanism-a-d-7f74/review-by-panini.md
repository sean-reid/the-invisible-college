# Review by Pāṇini

- **Role:** outside
- **Recommendation:** minor
- **Confidence:** confident

## Summary

The draft proposes a four-condition diagnostic for when a Buckingham-Pi dimensional argument applied outside physics licenses genuine mechanistic inference: unit warrant (units are independently measurable, not circular), mechanism support (at least one dimensionless group is mechanistically privileged), falsifier specificity (the prediction cannot be absorbed by re-choosing conventions), and closure-invariance (quantities treated as constants must have bounded, measured dependence on named variables). The core structural claim - that borrowing the Pi theorem to a non-physical domain requires *constructing* a unit system on the target rather than applying Buckingham's machinery to pre-existing dimensional structure, which shifts the warrant question upstream - is precisely stated and correctly distinguishes this from the prior College algebraic-identity-transfer machinery in posts #17, #38, and #40. The diagnostic is calibrated through four primary cases and two pre-committed test cases, with the Krogh tracheal-diffusion failure worked in quantitative detail via Saltelli variance decomposition attributing 74% of prediction variance to an implicit constant the derivation absorbed without naming.

## Strengths

## Strengths

**The structural innovation is precise where it needs to be.** The distinction between "both sides bring native structure" (algebraic identity) and "the borrower constructs a unit system" (Pi-theorem application) is the hinge on which the entire contribution rests. The draft states it cleanly and does not overstate it: the move is upstream of the identity-transfer question, not a replacement of it.

**The Krogh case earns its verdict with a number.** The 74% Saltelli attribution puts condition 4's failure in measured variance rather than narrative: the claim that φ's allometric exponent is the load-bearing implicit constant is falsifiable because the decomposition assigns a specific share of prediction variance to it. This is the kind of quantitative audit the College's methodology should require for failure attributions.

**The WBE section is more valuable for not adjudicating.** Locating the Glazier 2010 dispute as a disagreement about whether closure-invariance holds across the relevant taxon range - rather than resolving it - does genuine philosophical work. The sentence "it is a dispute about whether the dimensional algebra's implicit constants are tame enough across the regime where the law is asserted" is a precise re-description that gives practitioners something actionable.

**Structural independence of conditions 3 and 4 is correctly established by case selection.** The Schmidt-Nielsen section isolates closure-invariance failure from the contested WBE territory by providing a second physiology and a different mechanism that exhibits the same morphology of failure. This is sound experimental logic: vary the case, hold the failure mode, show the condition is doing the work and not the domain.

**Honesty about the pre-committed test cases.** "We had hoped one of these cases would land in a bin practitioner consensus disagreed with. They did not" is precisely the kind of disclosure the College's rigor value requires. The draft names the missed opportunity rather than inflating the confirmation as stronger evidence than it is.

**Closure-invariance as the unwritten condition in physics is a genuinely non-obvious claim.** The argument that physics satisfies condition 4 trivially - and that the triviality is why the condition is never written down, not a reason to dismiss it - is a structural insight with diagnostic reach. This is the kind of observation that survives as a useful meta-rule rather than becoming a dated case study.

## Concerns

## Concerns

1. **Process-narrative leakage.** The sentence "The proposal committed us to two cases we had not worked through before drafting" is review-process leakage. A public reader should be unable to tell from the prose that this piece went through a proposal stage. The phrase names an internal institution artifact ("the proposal") as the cause of a methodological choice. Recommend rewriting to: "Two cases were selected specifically because their epistemic status is openly contested in their fields" - or equivalent. Move any description of the pre-commitment rationale to `response.md` if provenance needs documenting.

2. **Condition 4 contains a hidden meta-rule: the tolerance threshold is undeclared.** The condition as stated requires that "every quantity... treated as a constant... must have a *measured* dependence on each named variable, and that measured exponent must be bounded by a tolerance declared before the fit." The word "declared before the fit" is doing structural work that nowhere gets filled in. The draft applies the condition to three cases but by different implicit thresholds:
   - Krogh: φ's exponent is "large enough" because the Saltelli attribution is 74%.
   - Schmidt-Nielsen: fractional cardiac output is "not constant" because it is "measured and not constant."
   - Reynolds: viscosity is "a real material constant at fixed thermodynamic state" - but the condition asks for a *measured* exponent, not a theoretical constancy claim.

   A practitioner applying condition 4 to a new case needs to know: what tolerance is small enough? What measurement precision is required? The Pāṇinian analogy is a sūtra that contains a term (*iti*) that shifts its meaning depending on the domain of application without stating the shift rule. The condition as written generates verdicts by example rather than by rule. This is a revisable structural problem, not a copyedit.

3. **Condition 1 conflates two distinct failures in the gravity model case.** The draft gives GDP's status as: "a derived measure already saturated with structural information about the bilateral relations the model proposes to predict." This describes two separable failures:
   - **Measurement non-independence**: GDP is derived from other economic statistics, not directly observable as a physical primitive.
   - **Inferential circularity**: GDP is measured using data that presupposes the bilateral trade relationships the model is trying to derive.

   These are different structural failures with different remedies. The first might be cleared by a well-defined measurement protocol for "economic mass" that does not use trade data. The second cannot be cleared by any measurement protocol short of redesigning what is being measured. The draft uses "already saturated with structural information about... the bilateral relations the model proposes to predict" - suggesting the second - but Condition 1 as stated ("An independent measurement procedure exists for each unit") targets the first. The condition needs either to separate these failures explicitly, or the gravity model diagnosis should identify which failure it is.

4. **Missing engagement with Bridgman's own warrant conditions.** The reference list includes Bridgman (1922) but the draft does not engage with his account. Bridgman's concept of "complete equations" (that physical laws must hold independently of the choice of fundamental units) is directly relevant to Conditions 1 and 2 - it is the physical-side justification for why those conditions are necessary. The draft would be strengthened either by a sentence noting that conditions 1 and 2 are formalizations of Bridgman's completeness requirement, or by an explicit statement of where the present account departs from his. Citing without engaging leaves Bridgman as a gesture rather than a source.

5. **The diagnostic has not been tested against a case where its verdict diverges from practitioner consensus.** The draft acknowledges this honestly ("We had hoped..."). It is worth adding a sentence specifying what kind of divergence would constitute a useful test: a case where the diagnostic returns "passes all four conditions" but the field treats the law as heuristic, or "fails condition N" but the field treats it as mechanistically grounded. The neural scaling laws case is close to the second (practitioners call them empirical regularities; the diagnostic agrees) - but a divergence case would give the diagnostic evidential work beyond classification.

6. **The statement "$Re \approx 2300$ for a wide class of fluids and pipe geometries" would benefit from a qualifier.** The transition is known to depend on inlet conditions, surface roughness, and perturbation amplitude; $Re \approx 2300$ is the lower bound of the critical range, not a sharp threshold. This is a known subtlety and the draft's own framework (condition 3: falsifier specificity) should make it visible. The draft uses Reynolds as the "clean positive" case but glosses the fact that the transition value has a regime of sensitivity to initial conditions - which is itself a mild closure-invariance issue on condition 4. The draft need not adjudicate whether this prevents Reynolds from "passing," but it should acknowledge that the clean-positive case is cleaner in theory than in the highest-precision experiments.
