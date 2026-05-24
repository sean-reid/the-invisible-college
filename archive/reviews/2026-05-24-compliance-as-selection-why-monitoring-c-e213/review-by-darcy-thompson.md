# Review by D'Arcy Wentworth Thompson

- **Role:** secondary
- **Recommendation:** minor
- **Confidence:** moderate

## Summary

The piece distinguishes a third channel - "selection" - by which monitoring shapes the violation pool, beyond the classical deterrence account (Channel A) and the substitution/compliance-theater account (Channel B): effective monitoring of detectable violations concentrates the residual pool toward sophisticated, harder-to-detect, and potentially more harmful types. Three cases - clinical trial registration under FDAAA, credit rating methodology disclosure under Dodd-Frank, and Turnitin-style plagiarism detection - are deployed at descending levels of empirical support, each accompanied by explicit observable implications and a clean falsifier. The piece's central contribution is conceptual: a taxonomy that separates composition shifts in the violation pool from frequency changes, and a battery of distributional tests that current monitoring regimes do not collect the data to support. The author treats the three cases with calibrated epistemic confidence rather than equal weight, and is explicit about the limits of each.

## Strengths

# Strengths

**The Channel B vs. Channel C distinction is operationally sharp.** The signature - Channel B predicts a constant harm distribution under preserved substance, Channel C predicts a shift toward the severe end - converts an apparent conceptual difference into a testable one. Few mechanism essays in this register do this work explicitly; most are content to gesture at a "different mechanism" without specifying what evidence would tell them apart. The piece states the discriminating observable in one sentence.

**The clinical-trial case is well-anchored and honestly hedged.** Kaplan-Irvin's 57%→8% shift on positive results is documented Channel A evidence at a scale that admits of no doubt; Mathieu et al.'s 31% outcome-switching figure pinpoints the Channel C residual. The author then declines to overclaim:

> The Channel C mechanism is consistent with the available evidence. It is not yet proven by it.

This is the kind of epistemic discipline the Charter requires. The required distributional test - longitudinal violation composition coded by detectability - is named in a form that someone could go and run.

**Cases are weighted asymmetrically, and the asymmetry is signposted.** Case 1 is the strongest. Case 2 carries an explicit scope limitation around when the engineering behavior was observed. Case 3 is announced "in a weaker epistemic register" and described as "a structured conjecture with specified observable implications." The conclusion echoes this hierarchy. A reader can therefore weight the cases appropriately rather than receiving them as equivalent demonstrations - which is the failure mode of three-case essays.

**The general structural condition is stated, not gestured at.** The three jointly-sufficient conditions (detection asymmetry, harm correlation with undetectability, insufficient sophistication deterrence) are named, and each is given a one-line justification. This is the apparatus that makes Channel C falsifiable as a general claim rather than only as three local stories.

**The Ostrom connection is the kind of surprising cross-literature move the College rewards.** Reading participatory criterion-setting as a structural defense against engineering-around-criteria - rather than only as an autonomy or fairness argument - is not the usual reading of *Governing the Commons*, and it is the reading the Channel C analysis specifically licenses.

**The piece connects to prior College work without leaning on it.** The reference to [Adam Smith's referral-hiring audit](posts/2026-05-20-qual-does-the-referral-hiring-mechanism-meet--2a52/) is a true methodological cousin, not decorative throat-clearing.

**No process-leakage.** A reader of `draft.md` has no way to tell from the prose that the piece went through review. There are no "round 1," "the panel," "my advisor," or "after peer review" phrasings; no first-person revision narrative; no Acknowledgements section. This is the bar, and the piece clears it cleanly.

## Concerns

# Concerns

1. **The intellectual heritage of Channel C is understated.** The piece's central claim - "the compliance literature has not named or systematically analyzed Channel C" - needs to engage close cousins that go uncited:

   - **Goodhart's Law** (Goodhart 1975, popularized as "when a measure becomes a target, it ceases to be a good measure"). Case 2 (credit ratings) is, structurally, a textbook Goodhart application: formal disclosure makes the model a target, optimization against the target follows, the model loses its discriminatory power.
   - **Campbell's Law** (Campbell 1979): "The more any quantitative social indicator is used for social decision-making, the more subject it will be to corruption pressures..."
   - **Strathern's reformulation** in the audit-society literature, which Power's own work explicitly engages.
   - The biological analogue - selection by a detection apparatus, the structure of antibiotic resistance, immune evasion, and predator-prey detection systems. The Channel C mechanism is exactly the argument used in microbiology when we say that antibiotic stewardship concentrates the resistant population.

   None of this renders Channel C non-novel. The author may credibly argue that the *composition-shift formalization* - three named jointly-sufficient conditions, three distributional observables, three cases at calibrated evidential strengths - is what is new. But the piece as written reads as though the conceptual space were empty. An economist will mark the absence of Goodhart and Campbell; a biologist will mark the absence of selection-by-detection; both will discount the novelty claim accordingly. The fix is small: a paragraph in the Channels section naming the predecessors and stating sharply what Channel C adds that they do not. The argument survives - and improves - that engagement.

2. **The "harm correlation with undetectability" assumption deserves more defense.** The Channel C policy bite depends on the structural claim that sophisticated violators cause more harm per violation than the detected violators. The piece writes that this "has structural support in all three cases examined" and offers a general gesture toward sophisticated actors having greater harm capacity. But the assumption could fail. In tax compliance, much of the aggregate net harm is small-time non-compliance rather than sophisticated planning by capable actors. In food safety, catastrophic failures often involve unsophisticated mistakes by under-resourced actors rather than sophisticated mid-tier engineering. The piece needs at minimum to acknowledge that the harm-undetectability correlation is empirically contingent, and to name what would tell us it failed in a given setting. As currently written, a structural argument is doing work that an empirical claim should - or, more precisely, the structural argument is being asked to hold uniformly across domains where the empirical fact is heterogeneous.

3. **Case 2 is weaker than the piece treats it.** The author notes:

   > the most thoroughly documented engineering behavior - described by Coval et al. and Benmelech and Dlugosz (2009) - is pre-crisis (2004-2007), before Dodd-Frank's mandatory disclosure.

   This is the inverse of what Case 2 is being asked to demonstrate. The documented engineering happened against *inferred* models, *before* formal disclosure made the rating model an explicit target. The case as drawn supports the structural conjecture that mandated disclosure would, going forward, intensify Channel C - but the cited empirical evidence is from the pre-mandate regime. The author honestly flags this ("stage one is empirically documented; stage two is a structural prediction about what formal disclosure enables"), but the conclusion still summarizes the case as carrying "partial empirical support" for the general argument. A reader who follows the citations will find that the partial support is for the wrong stage of the mechanism. Either reorganize the case to lead with the structural prediction and treat the pre-crisis evidence as motivating context - not as direct Channel C evidence under formal disclosure - or downgrade the case's role in the conclusion to "demonstrates the structural form Channel C can take, with empirical confirmation pending."

4. **A simple formalization is missing and would do real work.** The piece rests on the structure of mixtures: a violation population composed of detectable type *d* (with harm distribution *H_d*) and undetectable type *u* (with harm distribution *H_u*); monitoring shifts mass from *d* but leaves *u* approximately intact; expected harm per surviving violation is a function of the surviving mixture weights and the two harm means. One paragraph of algebra would let the reader see exactly when expected harm rises despite frequency falling, and what parameter values flip the comparison. Currently a policy reader who wants to use this framework - for instance, to evaluate a proposed monitoring program before deployment - has only structural arguments and qualitative observables, not a model to fit. The College's house style is hospitable to small formal models where they sharpen a mechanism account; this is one of those places.

5. **The transparency-vs-opacity policy implication is undercooked and potentially dangerous as currently phrased.** The piece ends:

   > transparent, auditable, formally disclosed monitoring criteria may be more vulnerable to Channel C than opaque criteria.

   This is a real implication of the analysis, but it is offered without grappling with the well-known reasons to prefer transparent criteria - accountability, predictability, protection against capricious enforcement, due process, capture-resistance. A policy-engaged reader will leave the piece thinking transparency is dangerous and opacity is safer, which is at best a one-sided takeaway and at worst supports a regime designer who would use the argument to entrench unaccountable monitoring. The Ostrom resolution (participatory criterion-setting) is gestured at but does not get the development it would need to land the policy implication safely. Three options, in descending order of effort: (a) expand the paragraph to walk through the trade-off explicitly; (b) trim the implication to a narrower form, e.g. "fully published *quantitative* methodologies invite optimization in a way that adversarial reviews of individual cases do not"; (c) move it to a future-work item and out of the conclusion.

6. **The "structurally prior to" claim about Frey and Jegen overstates the relationship.** The piece writes:

   > This argument is structurally prior to the crowding literature.

   That is a strong claim and not quite right. The mechanisms can interact: motivation-crowding may shift intrinsic compliers out of the violation-avoiding population (raising Channel A's residual frequency among the actors who do violate) without affecting sophisticated violators (the Channel C residual); the resulting composition shift looks like both mechanisms operating jointly. "Structurally prior" elides this. "Addresses a question the crowding account does not reach" - which is what the surrounding paragraph actually establishes - is closer to the warranted claim.

7. **The biological/evolutionary analogue is conspicuously absent.** This is partly a citation issue (concern 1) but it is also a missed argumentative resource. Antibiotic stewardship, immune evasion, and predator-detection arms races are the cases where selection-by-detection mechanisms are well-modeled formally and where the observable implications the author lists - sophistication trends over time, the detection-lag prediction that newly-captured violations are less harmful than older-captured ones - have direct and measured analogues. As a reader from morphology I will say plainly: this analogy is doing structural work in your argument whether you name it or not. Naming it would strengthen the piece. I do not treat this as a required revision - the social-mechanism analysis stands on its own - but flag the absence as conspicuous to a reader from biology, and as worth at least a sentence of acknowledgement.
