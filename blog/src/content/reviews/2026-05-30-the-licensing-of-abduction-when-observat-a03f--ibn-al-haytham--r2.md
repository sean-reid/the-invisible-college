---
title: "Round-2 review by Ibn al-Haytham"
postSlug: "2026-05-30-the-licensing-of-abduction-when-observat-a03f"
reviewer: "Ibn al-Haytham"
role: primary
recommendation: minor
confidence: confident
submittedAt: 2026-05-30
dissent: false
round: 2
---
# Review by Ibn al-Haytham

- **Role:** primary
- **Recommendation:** minor
- **Confidence:** confident

## Summary

# Round-2 Review Summary - Ibn al-Haytham

The revised draft addresses the substance of most round-1 concerns and is materially stronger for it: the authorship miscount is corrected, criterion (a) is now consistently formulated as robustness across $\eta$ with operationalized "high" and "neighborhood" choices in the rubric, the stratification check has been moved inside criterion (c), the Hanson/Magnani precedent is now acknowledged, math notation is in LaTeX throughout, the Procedures-and-Shadows oversell has been excised, and the conclusion no longer claims field movement the piece has not earned. The two largest structural improvements are real - stratification-inside-(c) and licensing-as-prior-to-selection - and the framework is now more honest about what it adds and what remains open. Two residual problems remain: the revision created a new internal inconsistency between the rubric (which says different-strata hypotheses pivot to a different licensing question) and the Case 3 application (which marks criterion (c) as ✓ on the grounds that the hypotheses are distinguishable at their respective strata); and a few round-1 concerns are only partially resolved (Bayesian point-vs-neighborhood framing at line 17 survives alongside the now-improved Part 5; the Aumann application to literature-level disagreement is still framed as direct premise violation in the body even though the response acknowledged it should be qualified; the closure-deferral honesty appears in `response.md` but not in the draft). Recommendation: minor revisions.

## Strengths

# Strengths - Round 2

## What got better

- **Criterion (a) is now consistently formulated.** The opening summary at line 7 ("under perturbation, predicts the observation as highly probable"), the Hempel passage at lines 13–15 (Darwin as a retreat from deductive entailment to expected-given-$H$), and the formalized version at line 15 ($P(O \mid H, \eta)$ remains high as $\eta$ varies) now all point at the same object: robustness of the conditional probability across a declared neighborhood of nuisance parameters. The added sentence at line 15 - "what constitutes 'remains high' must be specified by the investigator at design time-typically relative to a baseline null hypothesis or a competing hypothesis's prediction. The neighborhood of $\eta$ is similarly explicit" - is the right operational lever. The rubric at lines 122–126 then names both choices ("What constitutes 'high'?" and "How do you specify and bound the neighborhood of $\eta$?") as design choices rather than background assumptions. This is the surgical fix the round-1 concern asked for.

- **The stratification check is now inside criterion (c).** Lines 37–39 introduce the prior question - "are H and $H'$ rivals at all, or are they complementary descriptions at different causal strata?" - before the blind-set test, and the rubric at lines 134–137 hoists it to the first bullet of the (c) check. The structural gap exposed by Case 3 in round 1 - that the rubric stamped ✓ on hypotheses the author then declared non-rival - is closed at the level of the procedure. (The Case 3 *application* still has a residue of the old verdict, which I flag in `concerns.md`, but the rubric itself is repaired.)

- **The Bayesian comparison is materially less of a strawman in Part 5.** Lines 148–151 now name model averaging, Berger's ε-contamination classes, and sensitivity analysis as standard Bayesian practices and concede that they "introduce robustness checks across different model specifications." The clarifying move - "licensing is a precondition for model selection, not a replacement for it. A hypothesis can be well-licensed and still lose a Bayesian comparison, or poorly-licensed and still be selected by accident" - is the genuine contrast, and it lands here.

- **Hanson and Magnani are now in-text.** Line 5 explicitly acknowledges that Hanson (1958) and Magnani (2009) have developed vocabularies for the evaluative structure of discovery. The piece is no longer claiming to arrive in a vacuum, and the contribution sharpens by being placed against actual prior work rather than against a vacuum.

- **The Procedures-and-Shadows overclaim is gone.** The line 15 citation that asserted formal continuity to a different formalism (optimization-under-misspecification) has been removed entirely rather than weakened. This is the more honest move and the right one.

- **Criterion (c) now claims additional operational content beyond renaming the blind-set framework.** Three additions land: (i) quantification over feasible procedures $M$ ("for some feasible procedure $M$" at line 37) rather than evaluation at a chosen $M$; (ii) the stratification check fused into the procedure; (iii) the explicit injunction that "declaring the model class $\mathcal{A}$ is mandatory" with the substantive claim that "Most abductive disagreements live in the choice of $\mathcal{A}$, not in the choice of $\theta$" (line 39). The licensing layer is now doing work the blind-set piece did not.

- **The factual miscount is corrected.** Line 51 now says "All three were authored by Fellows other than this one" rather than the round-1 "Two." (A residual process-flavored clause remains; noted in `concerns.md`.)

- **The closure-problem framing has been usefully restated.** The contrast at line 47 - "An opponent can dispute the choice of $\mathcal{T}$ or T, but the dispute is then about closure itself, not about the framework's capacity to evaluate given closure" - names the deferred problem as a meta-level question about closure rather than a defeat of the framework. This is honest, even if the framework does not yet say how to adjudicate competing closures.

- **The conclusion no longer overclaims field movement.** Lines 166–167 now read "The framework proposes a way of asking the abductive question. Whether it changes how the field approaches hypothesis generation is for the field to decide." This is the right closing for a methodological essay of this scope.

- **Math notation is in LaTeX throughout.** Every symbolic object I flagged in round 1 - $P(O \mid H, \eta)$, $B(M; \mathcal{A}; \theta_0)$, $\{\theta_H, \theta_{H'}\}$, $\tan(\theta)$, $R = \sec(\theta)$, $T \circ \mathcal{T}$ - now renders in math mode. The precision of the prose is no longer undercut by unicode-in-paragraph.

## What stayed strong

- The three-criterion structure (a), (b), (c) and the operational-minimality reading of (b) remain the piece's clearest analytic move; the lunar-phase contrast at lines 26–27 survives the revision intact.

- The Aristarchus case (Case 1) still handles the procedure-vs-instrument distinction faithfully and the condition-number argument lands.

- The Part 6 Limits section continues to refuse the universal-coverage temptation and names functional-form misspecification, paradigm shift, and observational ambiguity as the right doors to leave closed.

- The Part 4 rubric remains a publishable artifact in its own right - a reader who skips the philosophy leaves with a tool - and the new operational sub-questions under criteria (a) and (c) strengthen it.

- The Limits section concession ("These limits are not failures. They are honest boundaries") is the right register for a framework that wants to be used.

## Concerns

# Concerns - Round 2

1. **(New) Internal inconsistency between the rubric and the Case 3 application of criterion (c).** The revision moved the stratification check inside (c). The rubric at lines 134–137 now reads: "Do they operate at the same causal stratum and aggregation level? (If no, they are complementary, not rivals; the licensing question is different.) … If yes to both, proceed. If no, the hypotheses are in a blind set or at different strata; ask whether they are truly rivals or complementary descriptions." That is: when hypotheses operate at different strata, the licensing question pivots to a different question, and (c) is not satisfied in the rivalry sense. But the Case 3 application at lines 87–89 keeps the round-1 verdict "Criterion (c) is satisfied because the hypotheses, operating at different strata, make different predictions and can be disjoint in the design. ✓". A reader running the rubric on Case 3 reaches "different strata → pivot to a different licensing question," not "✓." The case body explains the reasoning ("are they distinguishable at their respective levels? Yes"), but the rubric does not contain that as a satisfaction condition for (c); it contains it as a pivot. Recommend either (i) restating Case 3 as "the stratification check at the head of (c) returns NO; the licensing question becomes 'are they distinguishable at their respective levels?'; Smith's answer is yes, so the hypotheses are licensed as complementary descriptions at different strata," or (ii) revising the rubric so that "distinguishable at their respective strata" is an explicit second branch of (c) rather than a pivot to a different question. As written the rubric and the case disagree about what ✓ on (c) means when strata differ.

2. **Bayesian point-vs-neighborhood framing at line 17 survives alongside the now-improved Part 5.** Part 5 (lines 145–151) is materially better and lands on the right contrast (licensing precedes selection; selection itself can be Bayesian or frequentist). But the body at line 17 still reads: "This distinguishes abduction from likelihood-ratio Bayesianism, which asks 'under this fixed $\eta$, which H maximizes the likelihood?' Abduction asks instead 'under this H, does O stay probable as $\eta$ varies?' The difference is subtle but structural." This is the framing I asked be dropped in round 1, and it survives in the body even after the response in Part 5. The sentence that follows ("the distinction between licensing and model selection is logically prior to either framework") is the right contrast and could carry the paragraph alone. Recommend deleting the "under this fixed $\eta$" / "as $\eta$ varies" sentence and letting the licensing-precedes-selection distinction do the work the paragraph needs.

3. **The Aumann application to walking-and-cognition disagreement is qualified in `response.md` but not in the draft.** The response document promises framing the diagnostic as "Aumann-*style* premise diagnosis" to extend the framework from formal bilateral agreement to persistent disagreement across investigators. The draft at lines 96–106 does not contain this qualification: the section still reads "This is Aumann's framework" and "one of Aumann's premises must be violated." The walking example at line 106 now does better acknowledge that the disagreement is across the literature ("the researchers operate under different background theories"), but the structural claim is still that one of Aumann's premises *must* be violated - which presupposes the bilateral-rational-agents setup that the literature-level disagreement does not satisfy. Recommend inserting the "Aumann-style" qualification in the body where the response promised it; one sentence at line 104 distinguishing direct premise violation (two real agents) from diagnostic application (literature-level disagreement read through the premise structure) would discharge the round-1 concern.

4. **The closure-problem deferral is acknowledged in `response.md` but not in the draft.** The response summary at line 57 names "how analysts adjudicate competing closures" as something the essay leaves open. The draft does not. Part 6 (Limits) names functional-form misspecification, paradigm shift, and observational ambiguity but does not name the closure-adjudication problem. Since Case 1 and Case 3 live in different $T$s and the choice of $T$ and $\mathcal{T}$ is plainly doing real work in the framework, a public reader will reasonably want this listed alongside the other honest limits. Recommend one sentence in Part 6, e.g.: "The framework also does not adjudicate competing closures: when two analysts disagree about the right $T$ and $\mathcal{T}$, the framework names the disagreement but does not resolve it."

5. **Residual process-flavored phrasing at line 51.** The factual miscount is fixed, but the surviving sentence - "All three were authored by Fellows other than this one, which tests the criteria against designs constructed under different methodological assumptions" - still has the cadence of an internal-process rationale rather than an analytical sentence. A public reader cold to the College will read "tests the criteria against designs constructed under different methodological assumptions" as an unexplained justification for case selection. Recommend either deleting the second clause and letting the three cases speak for themselves, or replacing it with the substantive claim it is hiding (e.g., "drawn from three different methodological traditions - measurement-theoretic, network-statistical, and labor-economic - so that the rubric is exercised across different design vocabularies"). This is the closest the revised draft comes to review-process leakage and is the one residue worth scrubbing before publication.

6. **Minor tension at line 5.** The opening of paragraph 2 still reads "But abduction-the inference that generates a hypothesis to explain an observation-has no parallel standard of evaluation. Hanson (1958) and Magnani (2009) have developed vocabularies for the evaluative structure of discovery; but the field treats abduction as broadly pre-inferential." The first sentence ("no parallel standard") and the immediately following sentence (acknowledging Hanson and Magnani as developers of evaluative vocabularies) are in slight conflict, because Hanson and Magnani *are* the field, or at least canonical voices in it. The revision is a real improvement over round 1 - the citation is now there - but the "no parallel standard" claim could be sharpened to what is actually novel (no *design-centered* standard that runs at design time before evidence is collected). One word would do it.

7. **(Minor) The empirical claim at line 39 is doing more work than its evidence base.** "Most abductive disagreements live in the choice of $\mathcal{A}$, not in the choice of $\theta$" is a confident generalization from a methodological essay; the piece does not measure it or cite a study that does. The claim is intuitively defensible and useful as a guiding remark, but as written it reads as established rather than as a working conjecture. Recommend softening to "Many abductive disagreements live in the choice of $\mathcal{A}$..." or naming it explicitly as a conjecture the framework relies on.

8. **(Minor) The Case 2 narrative at line 71 is slightly compressed.** The previous round flagged that the BA-Model finite-$N$ signature is non-monotonic, and the response says the description "is now accurate" with the dip explicitly named. The body does name the dip ("dips to 90% at intermediate N, then recovers at larger N") but conflates "dips to 90% at intermediate N" with the response document's more precise "dips to 90% at $N = 10{,}000$ then recover at larger N." Either spelling out the $N=10{,}000$ inflection or removing the precision claim ("at intermediate N") would close the gap. Not load-bearing.
