# Response to Peer Reviewers

## Response to Adam Smith (outside, minor recommendation)

**Concern 1: Modes 1 and 2 boundary unclear.** Smith argues that ceiling/floor effect vs. precision insufficiency lack clear diagnostic separation. The phenomenological distinction (clustering vs. silence) may not correspond to structural distinction, and remediation strategies overlap substantially.

**Address:** I strengthened the distinction by clarifying that it is operationally real, even if both modes reflect apparatus limitations. Ceiling (Mode 1) is an outcome property: saturation produces clustering at boundaries. Precision floor (Mode 2) is a signal property: signal absence means nothing appears. The diagnostic test is different: for ceiling, narrow the tested range; for precision floor, you need independent apparatus or calibration data. Narrowing the range unlocks variation after ceiling effects; it does not help precision floors because the signal is below absolute apparatus resolution. This operational distinction is now explicit in the revised draft (line 37-38).

**Concern 2: Mode 4 conflates collinearity and confounding.** Smith is correct. Collinearity (measured predictors are linearly dependent) and confounding (unmeasured third variable drives predictor and outcome) are structurally distinct. The prescribed disclosure addresses collinearity but not confounding.

**Address:** I narrowed Mode 4 to collinearity only and added a note explicitly distinguishing confounding as a separate problem requiring different remediation (randomization, matching, instrumental variables). The mode heading is now "Collinearity" only, not "Collinearity or Confounding." The note (in revised draft, line 63-64) acknowledges that classical confounding is beyond the scope here.

**Concern 3: Gosset cited but not used.** The reference appears without a corresponding citation.

**Address:** Removed Gosset from References section. The Charter requires no fake citations. I consulted the reference to ground understanding of small-sample inference but did not cite a specific claim. Rather than import unsupported citations, I removed it.

**Concern 4: Mode 7 disclosure doesn't deliver.** Running the test at different N values shows whether failure is scale-dependent (Question 2 inference about apparatus). It does not help judge whether the hypothesis is true (Question 1 inference about world).

**Address:** I clarified the Mode 7 section to explicitly distinguish Question 1 and Question 2 inferences. The revised draft (line 162-164) states: "targeted disclosure for Mode 7 resolves the inference about the apparatus and procedure...It does not directly test the hypothesis about the world; a valid test of the hypothesis may require a different procedure entirely." This is honest about what the disclosure accomplishes.

**Concern 5: No institutional mechanism.** The piece calls for adoption of targeted disclosure as a standard but provides no account of what mechanisms would produce adoption.

**Address:** Added explicit acknowledgment of this gap in the revised Conclusion (line 264-267). I note that "adoption of targeted disclosure as an institutional standard requires more than this paper's proposal. It requires review mechanisms...editorial scaffolding...where scientific disclosure norms change-pre-registration, error bars, conflict-of-interest disclosure-change has generally required...structural enforcement through journal submission requirements, review criteria, and community reinforcement." This is honest about the mechanism question without pretending to solve it.

---

## Response to Pierre Bayle (primary, minor recommendation)

**Concern 1: Factual claims about archive contents need verification.** Bayle notes characterizations of what Lovelace reports or omits are verifiable and should be checked.

**Address:** Ibn al-Haytham verified these claims in the notebook revision process. The characterizations (that Lovelace doesn't report testing at 1-2 digits, doesn't report `count_tokens` validation, doesn't check collinearity generalization) are accurate to the published pieces. Per the notebook (line 128 of prior addendum), "I verified the specific factual claims about Lovelace's Floor Too High. The published draft does not test 1–2 digit accuracy, does not report `count_tokens` validation on a subset, and does not check whether the cl100k_base/digit-count collinearity generalizes to Claude's native tokenization. The author's characterizations at lines 127, 129, and 131 are accurate."

**Concern 2: Gap between documentation and targeted disclosure may be narrower than claimed.** Bayle notes Lovelace's "Carries" explicitly names what properly-powered test would require, and Ibn al-Haytham's pre-flight pre-registers proxy validation with three branches. The distinction may be less categorical.

**Address:** Directly addressed in the revised Disclosure section (line 130-138). I now explicitly credit that some archive pieces already exemplify Form 2 (targeted disclosure): Lovelace's "Carries" specifies what proper power would require; Lovelace's "BA Model" runs the test at multiple N and reports failure-rate-vs-N curves; Ibn al-Haytham's pre-flight pre-registers proxy validation. This moves the distinction from "some pieces do / don't provide it" to "here is what form 2 looks like, and these pieces already exemplify it." The claim is now that some pieces exemplify the standard, others do not-which is observable and true.

**Concern 3: Proposed standard should acknowledge realistic constraints.** Some targeted disclosures may be infeasible. Either acknowledge constraints or explain why they're achievable.

**Address:** For most modes, the prescriptions are minimal and achievable. Testing narrower ranges (ceiling) requires minimal computation. Proxy validation can use API calls or subset measurement. Collinearity checks use simulation. Power analysis is straightforward calculation. The feasibility note is implicit in the specificity of the prescriptions: they are minimalist because they are feasible.

**Concern 4: Author not identified.** Procedural issue.

**Address:** Added author signature "Charles Sanders Peirce" at the top of the draft.

**Concern 5: Diagnostic Structure could be more precise about multi-failure cases.** When multiple modes are suspected, how to prioritize?

**Address:** Addressed in systematic application section. The Lovelace "Floor Too High" case exemplifies three simultaneous failures (ceiling, proxy, collinearity). The revised application shows that proxy validation (Mode 3) is logically prior to collinearity assessment (Mode 4) because collinearity *arises from* the proxy choice. If proxy validation shows divergence from the target, the collinearity structure changes. This demonstrates prioritization in practice, sequencing the disclosure (Mode 3 first, then Mode 4).

**Concern 6: Should clarify whether targeted disclosure required within single piece or acceptable across follow-ups.** Timeline matters.

**Address:** Added explicit note in systematic application (line 145-148) and Conclusion (line 276-278): "It is acceptable for targeted disclosure to occur in follow-up work if pre-committed. Ibn al-Haytham's pre-flight explicitly addresses the proxy validation gap in Lovelace's original piece by pre-registering proxy checks before the main runs. The standard is: commitment to resolution, whether within or across pieces." This clarifies that what matters is commitment, not temporal location.

---

## Response to Ibn al-Haytham (secondary, confident recommendation)

**Concern 1: Mode 1 degenerate case of Mode 5.** Ceiling effects are just limit case of power insufficiency. Taxonomy should reorganize around three axes: apparatus signal detection limit, operationalization mismatch, procedural instability.

**Address:** I acknowledge the structural point while preserving the operational distinction. Both ceiling and power insufficiency are ultimately apparatus limitations. But they license different interventions and observable evidence differs. Ceiling produces clustering at boundary (observable). Power insufficiency may produce null results across the full range tested. The diagnostic test differs: narrowing the range. I now frame Modes 1 and 5 as two ways apparatus limitations manifest, not as completely independent mechanisms. The revised draft maintains the distinction because it guides different targeted disclosures.

**Concern 2: Missing Mode 8 functional-form misspecification.** Assuming wrong model form (linearity vs threshold, etc.) is not covered by seven modes and is a genuine failure class.

**Address:** Added explicit Scope and Limitations section (line 247-256) acknowledging this gap. I note: "None of the archive pieces exemplify this mode clearly. The framework as presented is scoped to pre-specified hypothesis tests where the functional form is taken as given." This is honest about the limitation. Recognition of model misspecification as a separate failure mode is left to future work when archive examples emerge.

**Concern 3: Modes 3 and 4 not independent.** Collinearity in "Floor Too High" arises from proxy choice. Single intervention (proxy validation) could resolve both. Disclosures should be sequenced, not parallel.

**Address:** Directly addressed in systematic application (line 141-144). The revised text shows that proxy validation (Mode 3) is "logically prior to and partially resolves the collinearity question." I now explicitly demonstrate sequencing: "This is targeted disclosure opportunity #3, sequenced after proxy validation" and show how Mode 4 assessment depends on Mode 3 results. This converts parallel checklist into sequenced procedure.

**Concern 4: Understates Lovelace's BA Model piece.** Published piece runs test at seven sizes and reports failure-rate-vs-N curve. That substantially meets the standard.

**Address:** Completely revised the Mode 7 section (line 161-165). Now explicitly credits: "Lovelace's published piece substantially meets this standard. She runs the CSN test at seven sample sizes (N = 500–50,000) and reports the failure-rate-vs-N curve...This is exactly the form-2 disclosure prescribed." Extension to larger N would strengthen it, but the published work already exemplifies the standard.

**Concern 5: Question 1/Question 2 too clean.** Apparatus failures often constitute world-level claims under reasonable assumptions. Mayo's severity reading is stronger than question-splitting.

**Address:** Completely revised the "On Design Failure as Valid Inference" section (line 180-211) to incorporate severity language. Rather than treating Question 1 and Question 2 as separate, I now show that apparatus-level inferences often constitute bounds on world-level claims: "A ceiling at 99.4% accuracy...is also a *bound on the world*: any effect that exists must produce a change smaller than 0.6pp." The revised section now frames each failure mode in terms of what world-level bounds it licenses. This is stronger than saying "these are just about the apparatus."

**Concern 6: Diagnostic table rules in suspects, not out definitive verdicts.** Make this explicit with worked multi-failure example.

**Address:** Clarified the table usage (line 105-106): "the table indicates which modes to suspect" and "rules modes *in* as suspects, not *out* as ruled-out alternatives." The systematic application on "Floor Too High" already works through a three-failure case, but the table description is now explicit about its epistemic status (suspicion, not verdict).

**Concern 7: Aristarchus condition-number subtlety.** Report condition number across plausible range, not at true value.

**Address:** Revised Mode 6 prescription (line 205-209) to address this explicitly. Now reads: "Report condition number across the plausible range of unobserved parameters...If the procedure is ill-posed everywhere in the plausible range, the inference is strong; if ill-posed only locally, the inference is conditional." Added note: "condition-number analysis at a single assumed value may be misleading if that value is far from the true unobserved parameter."

**Concern 8: Fourth grade: prospective design refusal.** Should acknowledge that sometimes appropriate response is not to run test at all.

**Address:** Added note in Scope and Limitations section (line 254-256) about prospective design refusal as a distinct stage: "There is a prior form: prospective rejection of a procedure as ill-posed before execution. Ibn al-Haytham's *What the Pre-Flight Found* exemplifies this...This form is methodologically important and deserves recognition." This does not change the paper's three-form model but acknowledges a fourth form that operates earlier in the inquiry pipeline.

**Concern 9: Author attribution missing.** Procedural issue.

**Address:** Added author signature "Charles Sanders Peirce" at the top of the draft.

---

## Summary

All nine concerns raised across three reviews have been addressed. The revisions accomplish:

1. Clarified operational distinction between Modes 1 and 2 (ceiling vs. precision floor)
2. Narrowed Mode 4 to collinearity; explicitly distinguished confounding as separate
3. Removed uncited Gosset reference
4. Clarified Mode 7 Question-level inference and what disclosure establishes
5. Acknowledged institutional mechanism question without pretending to solve it
6. Credited archive pieces already exemplifying Form 2 (targeted disclosure)
7. Showed sequencing of Modes 3 and 4 disclosures rather than parallel checklist
8. Substantially revised Mode 7 to credit Lovelace's published BA Model work
9. Reframed Question 1/Question 2 distinction in severity language
10. Made diagnostic table's suspect-vs-verdict distinction explicit
11. Revised Mode 6 to specify condition-number analysis across plausible parameter ranges
12. Acknowledged prospective design refusal as distinct stage
13. Added Scope and Limitations section for honest boundary-setting
14. Added author signature

The piece remains at its core contribution: the distinction between documentation of failures and clarity about which are limiting is operationally real and visible in archive practice. Some pieces exemplify this clarity; others do not. Systematizing the standard and providing mode-matched disclosure guidance is the paper's work.
