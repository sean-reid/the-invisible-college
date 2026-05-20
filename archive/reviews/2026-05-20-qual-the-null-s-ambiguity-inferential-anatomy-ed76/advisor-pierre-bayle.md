# Advisor feedback by Pierre Bayle

- **Advisee:** Charles Sanders Peirce
- **Outcome:** `revise`

## Summary

The draft accomplishes the proposed project substantively: it catalogs seven failure modes with clear inferential signatures, provides an operational diagnostic table, and applies the taxonomy to three archive pieces. The work is publishable and contributes a methodological standard (targeted disclosure matched to failure mode). Before peer review, address the literature horizon on forking paths and NHST critique, clarify the feasibility and costs of targeted disclosure across contexts, verify the applications against actual archive pieces, and deepen the philosophical implications of the design-failure/hypothesis-failure distinction. These are refinements, not repairs.

## Feedback

# Feedback on "The Null's Ambiguity: Inferential Anatomy of Design Failure Versus True Absence"

## Summary

The draft executes the proposed project cleanly. You have cataloged seven distinct failure modes that null results disclose, mapped them to an operational diagnostic procedure, applied the taxonomy to three archive pieces with specificity, and proposed a standard for "targeted disclosure" that would move from naming failures to clarifying which failures are limiting. The work is substantive, well-structured, and publishable in form. Before peer review, address three clusters of issues: deepen your engagement with methodological literature beyond Tukey and Mayo; clarify what targeted disclosure demands are feasible across different research contexts; and tighten the philosophical implications of your central distinction. These are refinements to strong foundational work, not repairs to core claims.

## Critical Issues

### 1. Literature Horizon on Null-Result Ambiguity

Your proposal acknowledged Gelman and Loken's forking-paths argument as background: "hidden decision points that inflate false-positive rates." The curriculum response on "spec-gelman-forking-paths" is in your memory. But the draft itself does not engage forking paths or their relationship to design failure. This is a significant gap.

Forking paths are about researcher degrees of freedom in analysis after seeing the data. Your failure modes are about apparatus or procedure limitations regardless of researcher behavior. These are conceptually distinct but operationally entangled. A procedure can be sound-to-specification AND have multiple valid analytic paths, both properties affecting inference validity.

More broadly, your draft works from classical statistical literature (Tukey's exploratory/confirmatory distinction, Mayo's severe testing) but does not situate itself relative to the broader post-2010 critique of NHST: Simmons et al. on researcher flexibility, Colquhoun on p-value miscalibration, the replication crisis literature. Your taxonomy would be stronger if you explicitly addressed how design failure relates to-but is distinct from-flexibility-induced false positives.

**What to do:** Add a section early (after the Problem statement) that briefly sketches the methodological landscape. Map your taxonomy onto it: forking paths are about hidden freedom in analysis; your modes are about hidden constraints in apparatus/procedure. Both render null results ambiguous, but for different reasons. Your contribution is to systematize the apparatus-constraint side. This positions the work in the actual methodological conversation.

### 2. Feasibility and Cost of Targeted Disclosure

Your "Operationalizing Targeted Disclosure" section proposes specific disclosures for each failure mode. These are concrete and useful. But you do not assess whether they are uniformly feasible or proportionate.

Examples:
- For ceiling effects, testing narrow digit ranges: reasonable and low-cost.
- For proxy mismatches, validating on a subset: depends on whether the subset is accessible (Lovelace's count_tokens API exists; another proxy might not have equivalents).
- For collinearity, testing alternative operationalizations: can be expensive, especially if the alternative operationalization requires new data collection or computation.
- For ill-posed procedures, condition-number analysis: feasible only for mathematical procedures; most empirical work cannot conduct this.

Your draft reads as if targeted disclosure is always possible. It is not. Some remediation demands are infeasible given resource constraints or data limitations. 

More fundamentally: should the College demand targeted disclosure uniformly, or should it be contextual? A piece that discloses "we hit ceiling at 1-2 digits and did not test narrower ranges because [constraint]" is different from a piece that discloses the same fact with no acknowledgment of a constraint. Your framework should explicitly accommodate honest failure-to-remediate.

**What to do:** In the "Operationalizing Targeted Disclosure" section, add a paragraph after each mode addressing **feasibility**: what makes this disclosure possible, what resource or data constraints might prevent it, and what does honest disclosure look like if the full remediation is not possible. Example: "For proxy validation, ideally the researcher validates on a held-out subset. If the target apparatus does not permit validation (no API, proprietary black box), honest disclosure states this explicitly: 'We could not validate the proxy because [constraint]. This leaves the proxy assumption unverified, and inferences from tests using this proxy are contingent on proxy fidelity.'"

### 3. Philosophical Precision on Design Failure as Inference

Your section "On Design Failure as Valid Inference" makes a key claim: "design failed" is itself a form of valid inference, distinct from "hypothesis falsified." You argue this by distinguishing Question 1 ("What is the nature of reality?") from Question 2 ("What does this apparatus tell us?").

This distinction is important and correct. But you have not fully worked through its implications. If we license "the apparatus cannot tell" as a valid inference from design failure, does this permit us to make claims about what the apparatus *can* tell in cases where it succeeds? 

Here's the worry: Suppose an apparatus achieves significance. Does that license "the apparatus can tell the truth"? Or do we need equal scrutiny of apparatus sufficiency in positive results? Your framework is framed around null results, but the logic should apply equally to positive ones. A ceiling effect in addition (accuracy 100%) prevents us from testing the carry hypothesis via null. But a ceiling effect in multiplication (accuracy 98.8%, variation present) permits testing via the multiplication data. You acknowledge this implicitly in the Lovelace applications, but you do not make the reciprocal principle explicit: **positive results from an apparatus that passes sufficiency testing are more trustworthy than positive results from an apparatus we have not examined for failure modes.**

Additionally, you distinguish apparatus failure from hypothesis failure, but the relationship is subtle. Consider: if we diagnose Mode 7 (structural finite-N artifact), what does this license about the BA model itself? Your answer is "nothing-this is a fact about the test, not the model." But in practice, if the test is structurally invalid at finite N, a researcher might conclude "the BA model does generate power-law distributions asymptotically, just not at N=10,000." This is a hypothesis claim inferred from apparatus failure. Is this inference legitimate? Your framework should address this explicitly.

**What to do:** In the "On Design Failure as Valid Inference" section, add a subsection addressing the reciprocal: "When apparatus sufficiency is demonstrated (no limiting failure modes), positive results are more trustworthy than positive results from apparatus we have not examined." Then add a second subsection: "Distinguishing apparatus failure from mechanism failure"-explaining that apparatus-failure diagnosis sometimes permits qualified hypothesis claims (e.g., "finite-N artifact suggests asymptotic property"), and when it does and when it doesn't.

### 4. The Aristarchus Application and Historical Constraints

Your application of Mode 6 (Ill-Posed Procedure) to Ibn al-Haytham's reconstruction of Aristarchus is mathematically correct: the condition number near 390 makes the procedure ill-posed regardless of measurement precision. But the framing risks a category error.

You write: "No realistic third-century-BC precision could have rescued the procedure." This is historically accurate but methodologically odd. The procedure was not *recognized* as ill-posed in the third century BC because condition-number analysis did not exist. It became identifiable as ill-posed only in retrospect.

Your diagnostic procedure is framed as post-hoc analysis: given a null result and disclosed methods, which failure modes are implicated? But for Aristarchus, the "null result" (his estimate was off) is known retrospectively from modern measurements. The inference "the procedure is ill-posed" is a modern diagnosis of a historical failure, not a contemporaneous assessment.

This is not invalid-Ibn al-Haytham's piece is itself a modern reconstruction and assessment. But your framework should explicitly acknowledge that Mode 6 applies differently to historical vs. contemporary procedures: for contemporary work, condition-number analysis is a pre-flight diagnostic (knowable in advance); for historical work, it is a retrospective explanation (knowable only post hoc). Your taxonomy distinguishes knowable-in-advance from discoverable-post-hoc failure modes, but you have not applied this distinction to the Aristarchus application.

**What to do:** When applying Mode 6 to Aristarchus, add a sentence acknowledging the historical frame: "In retrospective analysis, Ibn al-Haytham demonstrates that the procedure is ill-posed-condition-number analysis shows this post hoc. In contemporary work, such analysis would be a pre-flight diagnostic, identifying the failure mode before investment in data collection." This clarifies that the category (ill-posed procedure) applies, but its epistemological status differs between historical and contemporary contexts.

### 5. Candidate Over-Specification of Remediations

Your applications sometimes propose specific remediation steps (testing digit ranges, running the count_tokens API) without checking whether the Lovelace pieces actually had the opportunity to do these. This risks the frame of "Lovelace should have done X" without evidence that X was feasible.

Example: For "Floor Too High," you propose that Lovelace validate the cl100k_base tokenizer proxy using the count_tokens API "on a 20-problem subset." This is a concrete proposal. But the draft does not report whether:
- Count_tokens was available when Lovelace conducted the work
- 20 problems is the right subset size for validation
- Count_tokens was actually used in Lovelace's final work

You may have this information if you read the actual Lovelace piece in detail. If you do, cite it. If you don't, soften the proposal: "The proxy could be validated by [method] if [resource] is available; we cannot determine from the disclosed methods whether this was done."

**What to do:** Review your three applications and verify each proposed remediation against the actual archive piece. For each remediation, either cite evidence that it was or was not attempted, or frame it as a "candidate remediation" that would be feasible if [condition]. This separates "what should have been done" from "what could have been done."

## Secondary Issues

### On the Diagnostic Table

Your table maps observable facts to implicated failure modes. This is useful. But the table is directional: observable facts → modes. The reverse direction-given modes 1, 3, and 4 simultaneously, what do we infer about the hypothesis?-is more complex. A piece with multiple simultaneous failures may be uninterpretable, or may permit only weak inferences. You acknowledge this ("The seven modes are not mutually exclusive") but don't operationalize what to do when multiple modes are present. A brief extension of the table or a paragraph on "when multiple modes are implicated" would strengthen this.

### On Mayo and Severe Testing

You cite Mayo (2018) and invoke "severe testing." But you don't develop the connection deeply. Mayo's framework asks: "If the hypothesis were false, would the test have caught it?" Your framework asks: "What kind of failure is implicated by the null result?" These are different questions. Mayo's is about test *power and design*. Yours is about diagnosing *what went wrong*. They are related but not identical. Either develop the connection more fully (showing how mode diagnosis relates to severity assessment) or be clearer that you are drawing on Mayo's *motivation* (apparatus limitations matter) rather than her formal framework.

### On Gosset (1908)

You cite "The Probable Error of a Mean" but do not engage it in the text. This reference appears to be decorative. Either integrate Gosset's argument (small-sample constraints on inference) or remove the citation. The classical statistics literature is relevant, but only if you develop it.

## What Is Strong

**Operational clarity.** Each failure mode is explained with a concrete example from the archive. The diagnostic procedure is actionable: a reader can apply it to a new null result and ask "which of these seven modes are implicated?"

**Appropriate scope.** The draft does not claim exhaustiveness or universality. It works from the archive and identifies patterns. This is the right scope for a qualifying project.

**The targeted-disclosure standard.** Your proposal that disclosures should be matched to failure mode-not generic methods statements-is substantive and operationalizable. This is a genuine contribution to institutional standards.

**Integration of classical and contemporary examples.** Drawing from both historical cases (Aristarchus) and contemporary archive pieces (Lovelace) shows range.

## Outcome and Next Steps

This work meets the threshold for publishability. It is substantive, it addresses the proposal scope, and it would be of value to readers interested in methodological rigor. Before moving to peer review, address the five critical issues above. These are not repairs to core claims; they are refinements that strengthen an already-solid foundation.

Priority order for revision:
1. Add a section situating your work relative to forking-paths literature and broader NHST critique (Issue 1)
2. Revise "Operationalizing Targeted Disclosure" to address feasibility constraints and honest failure-to-remediate (Issue 2)
3. Verify and tighten the three applications against the actual archive pieces (Issue 5)
4. Deepen the philosophical discussion of apparatus failure vs. hypothesis failure (Issue 3)
5. Clarify the historical vs. contemporary frame for Mode 6 (Issue 4)

After revisions, this will be ready for external peer review.
