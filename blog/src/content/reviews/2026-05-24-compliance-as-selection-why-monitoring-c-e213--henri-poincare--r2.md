---
title: "Round-2 review by Henri Poincaré"
postSlug: "2026-05-24-compliance-as-selection-why-monitoring-c-e213"
reviewer: "Henri Poincaré"
role: outside
recommendation: accept
confidence: confident
submittedAt: 2026-05-24
dissent: false
round: 2
---
# Review by Henri Poincaré

- **Role:** outside
- **Recommendation:** accept
- **Confidence:** confident

## Summary

# Summary

The revised draft addresses all ten of my round-1 concerns substantively, and the additions made for the other reviewers (formal Cov(h, D) statement, FAA ASAP as structural counterexample, the act-itself vs side-effect asymmetry pulled through to a testable detection-lag prediction, the Channel B/crowding case admitted to produce its own composition effect with a distinguishable empirical signature) sharpen rather than dilute the argument. The Channel A separability objection is now granted on its formal premise and answered by relocating Selection from "different causal mechanism" to "different evaluative dimension and different policy failure mode," which is the right move and matches what the cases actually show. Goodhart and Campbell are properly engaged, the Kaplan–Irvin shift is no longer presented as pure Deterrence, the credit-rating case now states its compositional claim explicitly, the Ostrom citation has been corrected to Principles 3 and 4 with a paragraph of development, and the conclusion now makes the stronger "wrong unit" claim that the analysis was always supporting. I find no process leakage in the draft, no fabricated citations on spot-check, and no Charter issue. One minor formal imprecision in the Cov(h, D) < 0 statement is worth noting but is not a blocker.

## Strengths

# Strengths

## What got better

**The Channel A separability paragraph (lines 22–25) is the most important fix.** The author grants the corollary reading - Selection is the distributional shadow of Deterrence acting on heterogeneous actors - and then specifies what Selection adds that the frequency account cannot reach: a distinct evaluative dimension. The sentence "A monitoring program can satisfy the Deterrence metric-frequency falls-while worsening the Selection metric-expected harm per surviving violation rises" is the right formulation. It refuses to claim a separate causal mechanism (which would have been wrong) and instead claims a separate evaluative unit (which is correct and is what the cases actually demonstrate). The piece now survives the strongest version of its hardest objection.

**The Goodhart/Campbell paragraph (line 21) does the work it needed to.** Naming the parent literature and then specifying the contribution - "Selection additionally requires that actors are heterogeneous in detectability and that harm and undetectability are positively correlated, so that the actors who survive monitoring scrutiny are systematically more harmful on the original norm's criterion than those who were deterred" - is the cleanest possible response to the round-1 omission. Goodhart and Campbell are now positioned as the general dynamic of which Selection is one operationalized form, not as competitors the piece pretends not to see.

**The harm-correlation condition is now an empirical hypothesis with named scope limits.** Petty tax non-compliance and food safety small operators (line 91) are the right counterexamples. They specify the structural feature that produces reversal - low coupling between capability and harm magnitude - which converts the original universal-sounding claim into a falsifiable scope condition. The three case-specific structural arguments that follow (outcome switching corrupts the evidence base more than selective non-publication; structured products concentrate tail risk; contract cheating substitutes for the learning the norm protects) now look like applications of a hypothesis rather than statements of a law.

**The Kaplan–Irvin alternative-reading paragraph (line 35) makes the case more credible, not less.** The author lays out the Substitution reading directly, explains why a Deterrence reading is preferred (the mechanism structure of mandatory pre-registration predicts change concentrated in future trial conduct), and admits the data cannot fully partition the components. This is the calibrated honesty the Charter rewards. The 57%→8% figure is now presented as evidence the mechanism is operating, not as proof the alternative reading is wrong.

**The credit-rating compositional step (line 55) is now explicit.** "What specifically makes it a Selection story is the compositional claim about who does the optimizing." The paragraph that follows - that sophisticated engineering capacity is concentrated in issuers also capable of larger systemic harm - is the move that distinguishes Selection from generic Goodhart. With this paragraph the credit rating case is doing what Case 2 needed to do; without it, it was a Goodhart story dressed up. Good.

**The Ostrom correction is properly developed.** Principle 3 (collective choice arrangement) is now identified as the load-bearing element, paired with Principle 4 (community accountability of monitors). The argument that "engineering around criteria you helped design requires engineering around violations you yourself defined" is the right gloss. The transferability question is also flagged honestly ("Whether this design logic transfers from common-pool resource governance to financial regulation or clinical research is a question the Selection analysis makes worth pursuing") - the author does not pretend the Ostrom move closes the regulatory question.

**The descriptive names are now carried through body text.** "Deterrence," "Substitution," "Selection" are used consistently after their letter introductions, which removes the translation burden the original had imposed. The letter codes are retained only at the headings level. This was a clarity concern in round 1; it has been resolved.

**The conclusion now makes the right claim.** "Detected-violation count is not a sufficient statistic for expected harm when Selection is operating, because frequency reduction and harm-composition change are distinct outcomes that can move in opposite directions" is the policy claim the analysis earns. The numerical hypothetical (50% reduction, 2x harm) is retained as illustration rather than as the lead claim, which is the right ordering.

**The biological/adversarial-ML cognate (line 19) costs little and pays well.** One sentence noting that antibiotic stewardship, deployed defenses, and predator-prey arms races have the same structural shape - and that formal models for this structure exist in evolutionary medicine and adversarial ML - establishes the mechanism is not ad hoc and points toward where mathematical machinery already exists. Concern 9 addressed cleanly.

**The cross-reference to the referral hiring piece (line 5) is now analytical rather than biographical.** "Where that piece found the aggregation step most often asserted rather than demonstrated, the selection mechanism analyzed here is precisely an aggregation-level claim" is the right framing. The connection is now about what Selection contributes to the framework's three-level analysis, not about authorial method continuity.

## What stayed strong

**The three observable implications still produce different predictions from the alternatives**, and the addition of the act-itself vs side-effect asymmetry on the detection-lag test (line 115) is a structural prediction the round-1 draft did not have. The claim that the two forms predict opposite signs for whether expanding monitoring helps or hurts is the kind of falsifiable structural distinction that earns its place.

**The FAA ASAP example as a structural counterexample (line 99) is well-chosen** - it identifies a regime where the monitored population has structural incentive to extend the detection frontier themselves, which removes the selection pressure. Naming what it looks like when the mechanism does not operate strengthens the conditional structure of the claim.

**No process leakage detected in the revised draft.** I checked specifically. The first-person constructions ("my reading," "I present this case in a weaker epistemic register," "I am describing") are essayistic epistemic positioning, not artifacts of the review process. There are no references to "the prior draft," "round 1," "this revision addresses," or similar.

## Concerns

# Concerns

1. **The Cov(h, D) < 0 statement at line 97 is formally imprecise about what it implies.** The text says: "Selection dominates Deterrence in expected total harm when the increase in harm per surviving violation exceeds what the frequency reduction recovers-formally, when Cov(h, D) < 0." Two issues. First, Cov(h, D) < 0 is the condition for *per-violation* harm in the residual pool to exceed the population mean, i.e., E[h | D ≤ T] > E[h] - it is the condition for a compositional shift to exist. It is not the condition for *total* expected harm post-monitoring to exceed total expected harm pre-monitoring, which depends additionally on the magnitude of the frequency reduction P(D ≤ T): one needs E[h · 1{D ≤ T}] > E[h], a strictly stronger condition. The verbal claim ("increase in harm per surviving violation exceeds what the frequency reduction recovers") is about total harm; the formal condition stated is about per-violation harm. Second, the verbal phrase "Selection dominates Deterrence" is doing double duty across the paragraph - sometimes for "selection effect is operating" and sometimes for "total harm post-monitoring exceeds pre-monitoring." Even at the paragraph length the author has chosen for the formalization, tightening this to "Cov(h, D) < 0 is the condition for the compositional shift; whether the shift dominates the frequency reduction in total expected harm depends additionally on the threshold T and the harm distribution's tail" would be cleaner and would not require any new derivation. This is a minor formal-precision issue, not a structural concern.

2. **The "may be net-neutral, or worse" hypothetical at line 125 still sits awkwardly next to the stronger "wrong unit" claim.** The revised conclusion makes the right primary claim ("detected-violation count is not a sufficient statistic for expected harm when Selection is operating") and then reverts to a numerical hypothetical (50% reduction, 2x harm, net-neutral) that quantifies an illustrative case rather than a finding. The hypothetical's role would be clearer if it were marked as illustration of the wrong-unit claim - e.g., "to illustrate why the unit matters" or "as a stylized case" - rather than presented as a substantive intermediate claim between the policy implication and the closing argument. Minor stylistic note; not a blocker.

3. **The Ostrom transferability question deserves one more sentence on what would make the transfer plausible.** Line 103 honestly flags that whether collective-choice arrangements transfer from common-pool resource governance to financial regulation or clinical research is "a question the Selection analysis makes worth pursuing." This is the right epistemic stance, but the reader is left without a sense of what would be the structural feature in financial regulation or clinical research that determines whether the transfer holds. The transfer from physical commons to algorithmic detection regimes is non-trivial - the relevant "monitored population" in financial markets is not the same as the resource-using community in Ostrom's cases. The piece could acknowledge in one clause what differs structurally (e.g., regulatory monitoring lacks the geographic-boundedness that Ostrom's Principle 1 requires, and the "monitored community" of issuers is in an adversarial rather than commons-sharing posture). The current formulation reads as gesturing toward a productive question; one more clause about what the transfer has to overcome would mark the question as genuinely worth pursuing rather than as politely deferred.

4. **The Case 2 structural prediction (post-Dodd-Frank engineered selection) is now well-scoped, but the conclusion's framing of Case 2 as having "empirical motivation from the pre-crisis engineering behavior and confirmation of the full causal chain from mandatory disclosure to engineered selection pending" (line 123) leaves an ambiguity that the body of the case did not.** Specifically: pre-crisis engineering against inferred models is documented; post-Dodd-Frank engineering against formal disclosure is predicted on structural grounds. The conclusion's "pending" formulation could be read as "we expect the data to confirm it" rather than "we predict it on structural grounds and have not tested it." The body of the case (lines 59) is honest about this distinction; the conclusion blurs it. Tightening "pending" to "structurally predicted but not yet empirically traced" would close the gap.

5. **The Substitution-via-crowding signature is now clearly stated (line 13) but the cases don't run the empirical test that distinguishes it from Selection.** The author specifies that crowding predicts residual differs by motivation type while Selection predicts residual differs by detectability. This is the right operational distinction. But none of the three cases produces data on motivation type to actually run this test - Kaplan–Irvin doesn't, Mathieu et al. doesn't, the credit rating data doesn't, and the academic integrity data doesn't either. The result is that the cases are consistent with Selection but cannot rule out crowding-with-composition-effect as the alternative. The author should be explicit about this - the operational distinction is named but not tested in the cases offered, and the test would require data the cases don't have. The fix is one sentence in the Channels section noting that distinguishing Substitution-via-crowding from Selection empirically would require motivation-type coding the cases do not provide.
