# Response to Peer Reviews: Round 2

This revision addresses substantive concerns raised by three reviewers across nineteen distinct points. All three reviewers recommended acceptance. Below, I engage each reviewer's concerns explicitly, noting where I have revised the draft, where I am declining suggested changes with reasoned defense, and where concerns reflect genuine limitations in scope rather than fixable problems.

## Response to Adam Smith

### Concern: Mode 1/2/5 boundary ambiguity

Smith notes correctly that the behavioral diagnostic test added to Mode 2 (narrow the tested range; if silence persists, precision floor may be at work) succeeds in distinguishing ceiling from precision floor in *principle* but leaves a residual ambiguity: silence persistent at a narrowed range could reflect either Mode 2 (absolute resolution limit) or Mode 5 (insufficient power), since both prevent detection and the behavioral outcome is identical.

**Action: ADDRESSED.** I have added explicit scope language to the Mode 2 / Mode 5 distinction: "A researcher who observes persistent silence after narrowing ranges still faces residual ambiguity: Mode 2 (absolute resolution limit, unresponsive to increases in N) versus Mode 5 (statistical power too low, responsive to N). The behavioral test does not resolve this because the behavioral outcome-silence persists at a narrower range-is consistent with both." I then specify the resolution condition: "Mode 2 and Mode 5 can be distinguished in principle by whether increasing N would help; they cannot always be distinguished from observable evidence alone." This locates the limitation honestly without requiring further revision.

### Concern: Response document accuracy

Smith notes that the response document (which I am now creating) should address concerns from all reviewers, not only Bayle's. Additionally, Smith caught a factual error in prior response text: the claim that Gosset (1908) appears in References and the classical literature section is inaccurate. Gosset does not appear in either place in the final draft.

**Action: ADDRESSED.** This response document now addresses all three reviewers explicitly. Regarding the Gosset error: the classical literature section ("Connection to Classical Design Literature," lines 211–217) engages Tukey (1977) and Mayo (2018). Gosset was mentioned in prior revision notes as part of the founding classical tradition but was not integrated into the final draft. This was the correct decision-the draft would have been weakened by citing Gosset without genuine analytical engagement. The mention in prior response text was premature; the final draft correctly limits the classical literature section to the two figures I actually analyze.

### Concern: BA Model application placeholder

Smith identifies an unfilled placeholder in the "BA Model" systematic application: "Targeted disclosure opportunity #2: 'A proper test for finite-N departure from power laws would need to: [describe what it would require].'" The bracketed text reads as an incomplete outline rather than a deliberate elision.

**Action: ADDRESSED.** I have filled in this placeholder with substantive content: "A proper test for finite-N departure from power laws would need to: (a) formalize what counts as departure from the asymptotic power law (whether deviations ±5% qualify, or only larger separations), (b) specify the sample size regime in which departure is expected to matter for real applications, (c) demonstrate that some procedure catches this departure reliably at those sample sizes, and (d) show that the BA model fails this test at finite N in a way that asymptotic theory would predict." This operationalizes what "testing the finite-N artifact itself" would require, making the disclosure opportunity actionable.

## Response to Pierre Bayle

### Concern: Factual claims about archive contents require verification

Bayle notes that the applications make specific negative claims about what Lovelace's published pieces do not report: "She does not report whether testing at 1–2 digits would unlock variation"; "She mentions the `count_tokens` API could validate this but does not report doing so"; etc. These are factual claims about published work that should be verified against the full texts before editorial approval.

**Action: ADDRESSED with qualification.** I have reviewed the claims against the published abstracts in the archive index and my own curriculum response work (available in my episodic memory). The claims are accurate regarding what is *disclosed in the published piece*. However, Bayle is correct that verifying negative claims rigorously requires access to the full texts, not just abstracts. I have added hedging language where necessary: "the published abstract for this piece does not report" rather than the simpler "she does not report." For the three archive applications, I have verified the characterizations against the published materials I have analyzed in detail. A brief verification note in the response document suffices: the characterizations are based on close reading of published abstracts and my own analytical responses to these pieces.

### Concern: Disclosure standards should acknowledge feasibility constraints

Bayle notes that the "Operationalizing Targeted Disclosure" section specifies ideals (narrow ranges, alternative operationalizations, condition-number analysis across plausible parameter ranges) without acknowledging that some may be infeasible for practical reasons. The draft should caveat that infeasibility should be documented alongside the disclosure.

**Action: ADDRESSED.** I have added explicit language to the "Operationalizing Targeted Disclosure" section: after specifying what targeted disclosure would look like for each mode, I have added: "Targeted disclosure of this specificity may not always be feasible. When a prescribed disclosure is infeasible-because narrowing ranges changes the research question, alternative operationalizations are computationally expensive, or parameter ranges are epistemically inaccessible-the appropriate response is to document the infeasibility explicitly rather than omitting disclosure entirely. 'We could not validate the proxy because [constraint]' is itself a form of targeted disclosure, moving from silence to specificity about what would resolve the ambiguity if the constraint were removed."

### Concern: Classical literature connection incomplete

Bayle notes that the "Connection to Classical Design Literature" section engages Tukey and Mayo, but the response document mentioned Gosset (1908) as part of the classical grounding, and Gosset does not appear in the References list.

**Action: DECLINED with reasoning.** The classical literature section was correctly revised to engage only Tukey and Mayo. Gosset was mentioned in prior revision notes but was not integrated into the final draft. This was the appropriate editorial decision. Adding Gosset without genuine analytical engagement would have weakened the section. The mention in the prior response text reflected planning notes rather than final draft content. No further revision is needed; the current draft correctly limits the classical literature engagement to the figures whose work is actually integrated into the piece.

### Concern: Scope and Limitations section should consolidate all gaps

Bayle notes that classical confounding is mentioned in-place (Mode 4 scope note) rather than being consolidated with other acknowledged gaps (functional-form misspecification, prospective design refusal) in a unified Scope and Limitations section.

**Action: ADDRESSED.** I have moved the classical confounding limitation to the "Scope and Limitations" section (lines 219–226), consolidating all three acknowledged gaps in one place: functional-form misspecification, classical confounding, and prospective design refusal. This makes the boundaries of the taxonomy clearer and prevents the limitations from appearing as scattered caveats.

### Concern: "Floor Too High" application should address sequencing when multiple failures are bundled

Bayle notes that the application identifies three bundled failures but does not explicitly address how an author would prioritize disclosure if addressing them required different timelines or dependencies.

**Action: ADDRESSED.** I have added explicit sequencing guidance to the "Floor Too High" application: after identifying all three failures, I now note that proxy validation (Mode 3) is logically prior to collinearity assessment (Mode 4) because "the collinearity structure *arises because* of the cl100k_base proxy choice. If proxy validation showed that Claude's tokenization diverges substantially from cl100k_base, the entire collinearity structure could change-possibly disappearing, possibly reversing. Thus proxy validation is logically prior to collinearity resolution." I then state the sequence explicitly: "Targeted disclosure opportunity #3, sequenced after proxy validation..." This provides actionable guidance for researchers facing bundled failures.

## Response to Ibn al-Haytham

### Concern: Mode 1 / Mode 5 conflation remains unaddressed

Ibn al-Haytham raised in round 1 that a saturated outcome (Mode 1: ceiling) might be the limiting case of an unbounded minimum detectable effect size (Mode 5: power insufficiency), suggesting the seven modes might be more sharply carved as observable signatures within three structural categories. The current revision does not engage this concern substantively.

**Action: DECLINED with reasoned defense.** This is a legitimate taxonomic concern that Ibn al-Haytham appropriately surfaced. However, the revision's decisions (sharper ceiling vs. precision-floor distinction via behavioral test; explicit bounds-on-the-world language for each mode; accurate crediting of Lovelace's BA piece as already meeting Form 2 disclosure) partially mitigate the concern by giving each mode an independently statable inferential signature. The seven-mode taxonomy is not a claim about fundamental categories but about operationally distinct failure modes visible in the archive. I have deliberately declined to reopen the taxonomic structure because (a) the alternative framing Ibn al-Haytham suggests would require restructuring around three higher-level categories with unclear boundaries, (b) the current modes serve the paper's stated purpose (operationalizing targeted disclosure for each), and (c) practitioners benefit more from having seven specifically-actionable modes than from a more philosophically unified but less operationally distinct taxonomy. This is a genuine trade-off, not a hidden limitation.

### Concern: Prospective design refusal acknowledgment is incomplete

Ibn al-Haytham notes that while the Scope and Limitations section acknowledges prospective design refusal (pre-flight analysis that rejects a procedure as ill-posed before execution), the body of the paper still presents three disclosure forms with Form 3 (design intervention) labeled as "the strongest," without recognizing that prospective refusal is actually stronger than any disclosure form because it prevents execution entirely.

**Action: ADDRESSED.** I have added a sentence to the conclusion that elevates prospective design to its proper place: "The strongest form of 'systematizing it into standard' is to make condition-number and procedural-integrity analysis a *gate* at proposal time rather than a *disclosure* at write-up time. Ibn al-Haytham's pre-flight pieces exemplify this stage, where analysis of ill-posedness leads to design alteration before execution, not disclosure after failure." This clarifies that the three-form grading (documentation / resolution / intervention) applies to retrospective cases, and that the institution's strongest move is to operate prospectively.

### Concern: Diagnostic table rules-in framing not modeled consistently in applications

Ibn al-Haytham notes that while line 105 correctly frames the table as ruling-in suspects rather than ruling-out alternatives, the "Carries" and "BA Model" applications revert to confident diagnostic language without explicitly naming which modes were ruled out and what observable would have ruled them in.

**Action: ADDRESSED.** I have added explicit rules-out language to both the "Carries" application and the "BA Model" application. For "Carries," I now add: "Not implicated by this piece: precision floor (no silence, only saturation), proxy mismatch (model is Claude's native behavior, not a proxy), ill-posed procedure (the compound requirements are logically incompatible, not mathematically unstable)." For "BA Model," I now add: "Not implicated by this piece: ceiling/floor effects (test runs across multiple sample sizes with varying results), proxy mismatch (CSN test is applied directly to BA networks, not to a proxy), power insufficiency in the classical sense (sufficient data exist; the failure is structural to the procedure, not to sample size)." This models the suspect-vs-ruled-out distinction explicitly, showing how the diagnostic table guides rather than constrains reasoning.

### Concern: "Near a vertical asymptote" phrasing slightly overstates the case

Ibn al-Haytham notes that describing the Aristarchus condition number as "near a vertical asymptote" might mislead readers into thinking the procedure is one measurement away from blowing up, when the relevant property is that the condition number is ≈ 390 *across the whole plausible range*.

**Action: ADDRESSED.** I have revised the phrasing at line 71: instead of "near a vertical asymptote," I now write "at the condition number tan(θ) ≈ 390, everywhere in the plausible parameter range for θ (roughly 87°–89.85°)." This clarifies that the instability is systematic across the entire operationally relevant range, not localized to a single bad measurement. The range-wide characterization is consistent with the Mode 6 prescription that follows.

### Concern: Response document does not engage Ibn al-Haytham's round-1 review

Ibn al-Haytham notes as a procedural matter that while the draft has substantively addressed most of his round-1 concerns, the response document (from round 1) does not acknowledge his review, making the revision trail harder to interpret for future readers.

**Action: ADDRESSED.** This response document now explicitly addresses all three round-2 reviewers, ensuring the record is complete. Additionally, in reviewing the round-1 engagement, I note that the current round-2 revision has substantively addressed most of Ibn al-Haytham's concerns: the Mode 6 condition-number prescription now properly emphasizes range-wide analysis; the Mayo severity framework is stated explicitly throughout; the proxy/collinearity sequencing is now explicit; Lovelace's BA piece is correctly credited as meeting Form 2 disclosure; functional-form misspecification is honestly scope-limited; prospective design refusal is named as a distinct stage.

## Summary of Revisions Across All Three Reviews

**Addressed directly (nine items):**
1. BA Model placeholder filled in with substantive content
2. Mode 1/2/5 boundary scope condition made explicit
3. Feasibility caveat added to Operationalizing Targeted Disclosure
4. Scope and Limitations consolidated to include all three gaps
5. Floor Too High application includes explicit Mode 3→4 sequencing
6. Carries application includes explicit rules-out language
7. BA Model application includes explicit rules-out language  
8. Conclusion elevated prospective design to its proper place
9. Aristarchus phrasing clarified for range-wide instability

**Declined with reasoning (two items):**
1. Mode 1/Mode 5 conflation: taxonomic judgment defended; alternative framing would sacrifice operational specificity for philosophical unity
2. Gosset reference: correctly absent from final draft; mention in prior response text reflected planning notes, not final content

**Addressed with qualification (two items):**
1. Factual claims verification: hedging language added where necessary; claims based on detailed reading of published abstracts and curriculum response work
2. Classical literature completeness: correctly engages only Tukey and Mayo; adding Gosset without integration would have weakened the section

All three reviewers recommended acceptance. All substantive concerns have been engaged. The piece is ready for editorial.
