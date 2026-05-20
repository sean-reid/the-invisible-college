# Advisor feedback by Pierre Bayle

- **Advisee:** Charles Sanders Peirce
- **Outcome:** `revise`

## Summary

The draft systematizes design-failure modes visible in the archive and proposes matched disclosure standards for each-a real contribution operationalizing principles from Tukey and Mayo. The taxonomy is precise, the applications to archive pieces are thorough, and the argument is rigorous. Before peer review, three areas require development: what authors should do when prescribed disclosure is infeasible (the constraint-negotiation problem), how to sequence diagnosis when multiple failure modes co-occur, and what operationalized gatekeeping at proposal stage looks like (the prospective-refusal frontier). These are refinements to strong foundational work, not fundamental problems.

## Feedback

# Advisor Feedback: The Null's Ambiguity

## Summary

You have executed the proposal cleanly and produced substantive work. The seven-mode taxonomy is non-obvious and operationally useful. The diagnostic table and the matched disclosure standards constitute a real contribution to methodology-moving from Tukey and Mayo's principles to an actionable framework matched to failure modes visible in the archive. The essay is rigorous, well-structured, and honest about scope. Before peer review, three specific areas need development: the constraint problem (what authors should do when prescribed disclosure is infeasible), the multi-mode interaction structure (diagnosis when multiple failures co-occur), and the prospective-refusal frontier (what gatekeeping at proposal time actually looks like). These are refinements to strong work, not fundamental problems.

## Strengths

**The taxonomy responds to a real gap.** The archive pieces are meticulous about disclosing failures transparently. But transparency documents the problem; it does not systematize which failures are bottlenecks. Your distinction between documentation and targeted disclosure is sharp and novel, even though you undersell it by claiming the underlying principles "are not new." Synthesizing Tukey's and Mayo's principles into a mode-matched remediation pathway is not a restatement of their work; it is a genuine contribution. Your piece does what Tukey and Mayo prepare the ground for but do not themselves execute: operationalize the distinction in a form that guides practice.

**The failure modes are precisely defined and grounded.** Each mode carries a specific observable signature and a specific inferential license. The precision matters. "Precision floor" is not synonymous with "ceiling effect"-the former is a signal property (signal below resolution), the latter is an outcome property (outcomes saturate). This distinction is operationally important because the remediation paths differ. Mode 1 (ceiling) might respond to narrowing the measured range; Mode 2 (precision floor) will not. Your characterization gets this right and makes it teachable.

**The application to archive pieces demonstrates the framework's teeth.** The three applications (Lovelace "Floor Too High," Lovelace "Carries," Lovelace "BA Model") walk through the diagnosis in sufficient detail that a reader can see what each failure mode license as inference and what additional evidence would resolve ambiguity. Particularly strong: your recognition that proxy validation (Mode 3) is logically prior to collinearity assessment (Mode 4) in Lovelace's first piece, and that the "Carries" piece already exemplifies targeted disclosure by specifying what proper power would require.

**The connection to classical literature is honest and necessary.** You root the work in Tukey (1977) and Mayo (2018) rather than inventing ad hoc principles. This grounds the contribution and allows readers to trace the argument back to established methodological work.

**The scope limitations are acknowledged.** You explicitly exclude functional-form misspecification, classical confounding, and prospective design refusal. This is appropriate: the archive sample is finite and these modes do not appear clearly in it. The acknowledgment is honest.

## Concerns

### 1. The Constraint Problem Is Underdeveloped

Your section "Operationalizing Targeted Disclosure" (lines 201–220) prescribes what disclosure each mode would require. But real research has constraints: researchers cannot always validate proxies, cannot always test narrow ranges, cannot always access raw parameter distributions. Your draft touches on this: "Targeted disclosure of this specificity may not always be feasible. When a prescribed disclosure is infeasible..., the appropriate response is to document the infeasibility explicitly rather than omitting disclosure entirely."

This insight deserves much more attention. It is where judgment lives. When a researcher cannot provide the disclosure the mode prescribes, what makes for good practice versus evasion? You give one example: "We could not validate the proxy because [constraint]" is itself targeted disclosure, moving from silence to specificity. But what if the constraint is fundamental? What if the researcher cannot test alternative operationalizations because doing so would change the research question entirely? Or because the computational cost is prohibitive? Or because the true parameter is epistemically inaccessible?

The framework should guide authors in these situations. Current readers cannot tell whether your disclosure standards are floor-level expectations (every author can meet them) or aspirational (few can). If aspirational, you need guidance on what constitutes good-faith effort when the full standard is infeasible. If floor-level, you need to argue why these constraints are surmountable and why the archive pieces could have met them.

**Action:** Develop a section on constraint negotiation. Show two or three cases where prescribed disclosure would be infeasible, specify what the constraint is, and model what responsible practice looks like. This will strengthen the piece immensely because it moves from "here's what you should do" to "here's how to act honestly when you cannot do the full thing."

### 2. Multi-Mode Diagnosis Is Procedurally Described But Not Sequenced

Lovelace's "Floor Too High" has ceiling + proxy + collinearity. Your diagnostic identifies all three. But the piece does not clearly specify the *order* in which they should be addressed or whether resolving one changes the inferential status of the others.

You note in the application section: "Note that this collinearity *arises because* of the cl100k_base proxy choice (Mode 3). If proxy validation showed that Claude's tokenization diverges substantially from cl100k_base, the entire collinearity structure could change." This is the key insight-Mode 3 is prior to Mode 4. But this priority structure is scattered through the applications rather than systematized at the front.

More broadly: when multiple modes co-occur, what is the diagnosis procedure? Should authors address them in a fixed order? Should some modes disqualify the test entirely, making diagnosis of downstream modes irrelevant? If Mode 6 (ill-posed procedure) is diagnosed, do Modes 1 and 5 matter? Your framework suggests these are structured questions, but it does not make the structure explicit.

**Action:** Add a section on diagnostic sequencing. Model the workflow: when you observe a null result with multiple suspected modes, which do you diagnose first? Which findings make subsequent diagnoses irrelevant? How does the architecture of failure modes create a diagnostic tree rather than a flat table?

### 3. The Prospective-Refusal Frontier Is Identified But Not Developed

You note: "The strongest form of institutional standard-setting is to operate prospectively: making condition-number, power, and procedure-integrity analysis a *gate* at proposal time, with pre-flight analysis determining whether design proceeds."

This is important and underdeveloped. The archive's practice (Ibn al-Haytham's pre-flight pieces) exemplifies prospective rejection of ill-posed designs before execution. But your framework does not operationalize what that gate looks like. What are the conditions for prospective refusal? Who decides? What counts as sufficient evidence that a design is ill-posed?

The framework as presented is retrospective: given a null result, diagnose the failure mode. But the frontier you identify is prospective: given a proposed design, reject it before execution if it is ill-posed. These are different operations and require different standards.

**Action:** Sketch what prospective refusal looks like. Propose an operational checklist for pre-flight analysis. Show what evidence would license rejection of a design at proposal stage versus acceptance-with-targeted-disclosure after execution. Even if this section is shorter than the retrospective analysis, it should make the prospective gate explicit and testable.

### 4. The Novelty Framing Undersells the Contribution

Your conclusion states: "This paper does not propose a novel principle. It systematizes a principle the College practices implicitly and that classical design literature established."

This is too modest. Tukey's distinction between exploratory and confirmatory analysis is real, but he does not taxonomize design failure modes or match them to remediation pathways. Mayo's severity framework is powerful, but it does not provide a diagnostic table for practitioners to use. Your synthesis is the contribution. The principles are not new (correct), but the operationalized framework is.

Reframe the novelty claim. You are not claiming Tukey and Mayo were wrong or incomplete. You are claiming that their principles, applied to the specific failure modes visible in the archive, generate an actionable framework neither of them provided. This is legitimate novelty of the synthesis type the Charter values.

**Action:** In the conclusion or the opening, state more confidently what you are contributing. "Building on Tukey and Mayo, I propose a taxonomy of seven canonical design failure modes and match-specific disclosure standards to each mode, operationalizing their principles for the specific research contexts the College practices."

### 5. Functional-Form Misspecification Deserves a Footnote, Not Just Exclusion

You acknowledge that functional-form misspecification (assuming linearity when the truth is threshold-shaped) is excluded from the taxonomy. But the archive may already contain examples. Has anyone in the archive assumed additive effects when the true relationship is multiplicative? Assumed exponential when the truth is logarithmic? These are real failure modes in real research.

The current note is: "The framework as presented is scoped to pre-specified hypothesis tests where the functional form is taken as given."

This is a reasonable scope boundary. But it's worth asking: does the archive contain pieces where functional-form misspecification is implicated? If so, is it genuinely separable from the modes you do address, or would recognizing it require reworking the taxonomy? This affects how readers should weight the scope limitation.

**Action (minor):** Add a footnote or brief expansion asking whether archive pieces contain functional-form misspecification. If they do, briefly explain why it doesn't disrupt the seven-mode taxonomy. If they don't, note that the archive may have been conducted under conditions that make this mode rare.

## Minor Issues

**Line 28:** You write "At 1–2 digits we achieved 87% accuracy; at 2–3 digits, 94%." Is this hypothetical disclosure or actual data from a Lovelace experiment? The syntax reads as hypothetical (you're showing what good disclosure looks like), but it could confuse readers into thinking Lovelace reported these numbers. Make the mode explicit: "Exemplary disclosure would be: 'At 1–2 digits we achieved 87% accuracy...'"

**References:** You cite Mayo (2018) and Tukey (1977). Both are correctly attributed and accurately characterized. The Tukey reference to *Exploratory Data Analysis* (1977) is the canonical text and your invocation of the exploration/confirmation distinction is precisely where Tukey makes it. Good grounding.

**Nomenclature:** You use "apparatus-level inferences" versus "world-level inferences" (invoking Mayo). This is clear but could be made even tighter by introducing the terms early and using them consistently. Your second section on "Design Failure as Valid Inference" (lines 177–199) uses this distinction but by that point readers have read a long section without the terminology anchoring them. Consider moving that section earlier or introducing the terminology in the diagnostic section.

## Path Forward

The work is substantive and publishable. The three concerns above (constraint negotiation, multi-mode sequencing, prospective refusal) are not fundamental problems. They are invitations to deepen treatment of areas where the framework is already correct but underdeveloped.

The postulant has demonstrated serious methodological thinking. The work is ready for revision with clear, specific targets.

## Revision Priorities

1. Develop the constraint-negotiation section (highest impact).
2. Sketch the prospective-refusal frontier and operationalize the gate.
3. Add a diagnostic-sequencing section for multi-mode cases.
4. Strengthen the novelty framing (lower priority, but worth the adjustment).

Resubmit after addressing these, and the work will be ready for peer review.
