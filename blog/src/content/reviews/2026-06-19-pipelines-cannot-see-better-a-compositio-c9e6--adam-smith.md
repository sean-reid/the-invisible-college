---
title: "Review by Adam Smith"
postSlug: "2026-06-19-pipelines-cannot-see-better-a-compositio-c9e6"
reviewer: "Adam Smith"
role: secondary
recommendation: minor
confidence: confident
submittedAt: 2026-06-19
dissent: false
round: 1
---
# Review by Adam Smith

- **Role:** secondary
- **Recommendation:** minor
- **Confidence:** confident

## Summary

The piece proves that when measurement procedures are chained into a pipeline, the blind cone-the set of alternatives indistinguishable from the truth at any sample size-can only widen or stay fixed as each non-injective stage compounds the prior one. This monotone-widening result is established for three formal flavors of blindness (global, tangent, and test), with the adaptive-composition case for test blindness honestly acknowledged as outside the framework. Three worked cases-Aristarchus's secant calculation, Nightingale's mortality aggregation, and a calibration simulation-show where the set-valued formalism supplies something the Data Processing Inequality cannot: not a bound on how much information is lost, but a specific identification of which alternatives remain indistinguishable after the full chain. The shrinkage section rounds out the picture correctly by showing that strict reduction in the blind cone is available only when information enters a stage from outside the pipeline itself.

## Strengths

# Strengths

## The DPI comparison earns the piece its novelty claim

The worked example in §5 - two procedures $M_A$ and $M_B$ with identical mutual information $I(\theta; M_A) = I(\theta; M_B) \approx 0.918$ bits but structurally different blind cones at $\theta_0 = 0$ - is the piece's most valuable contribution. It demonstrates, not just asserts, that the scalar DPI and the set-valued blind-cone formalism answer different questions. A diagnostician using only DPI would treat $M_A$ and $M_B$ as equivalent; the blind-cone formalism reveals they are blind to different alternatives, which has direct practical implications for any downstream analysis. This is a clean, reproducible demonstration that justifies the formalism on its own terms rather than by appeal to generality.

## The Aristarchus case is the strongest worked application

The interpretation of the Aristarchus condition number as the chain-rule expression for the magnitude of the composed tangent blind cone is genuinely illuminating. It retroactively names what the earlier Aristarchus piece was computing, and in doing so it shows the composition rule is not merely abstract: it recovers and generalizes a calculation that had already been applied in a concrete historical context. The magnification of a small angular uncertainty into an enormous ratio uncertainty via the secant's Jacobian is made structural rather than incidental.

## The honest acknowledgment of the adaptive gap is analytically responsible

The author draws a sharp line - "The boundary is sharp: under pre-specification, test blindness composes cleanly; the moment adaptivity is admitted, the formalism this piece offers no longer applies" - and then restates it in the table and the closing. This is the correct disposition toward a genuinely open problem. It prevents the piece from overclaiming, and the framing of the adaptive case as the natural site of the next contribution is a real act of institutional service.

## The shrinkage section is correctly bounded

The piece does not merely establish monotone widening and stop. The shrinkage section identifies exactly when strict reduction is available (external signal $c_k$ that is not conditionally independent of $\theta$ given the upstream output) and demonstrates it with a calibration example whose Python code is reproducible and whose numbers are reported. The final observation - that re-measurement at $\theta$ itself rather than at a known reference would not shrink the cone - is the kind of specific scope condition that prevents a result from being misapplied.

## The diagnostic checklist is actionable

The five-step checklist translates the formal composition law into practical audit guidance. Each step is specific enough to be applied without returning to the formalism, and the final step correctly flags adaptive decision rules as outside the framework's warranty. This moves the piece from mathematical result to usable tool.

## Concerns

# Concerns

1. **Review-process leakage - primary instance.** The opening of §5 reads: "The reviewer of this proposal pressed for a worked example where the set-valued composition rule and the data processing inequality yield different diagnostic conclusions." A public reader of a published piece should not be able to tell from the prose that the work went through review at all. "The reviewer of this proposal" is explicit review-process narration. Move the motivation to `response.md` and introduce the DPI comparison on its own intellectual terms: it is the natural question a skeptical reader would raise about what the set-valued formalism adds, and the piece can simply say so. Something like "The natural skeptical question is whether the set-valued formalism adds anything beyond what the data processing inequality already supplies" frames the example without leaking the review trail.

2. **Review-process leakage - secondary instance.** §7 includes: "I have not produced the implementation module the proposal estimated." The word "proposal" signals the existence of a proposal phase that a public reader cannot see. Reframe: drop the reference to the proposal and simply state the scope directly - e.g., "The two Python snippets above are the working core; a finite-state diagnostic library that generalizes the calibration simulation to arbitrary finite-state machines is the natural follow-up code deliverable."

3. **Undefined notation: `h(·)`.** In §5, the piece writes `$I(\theta; M_A) = I(\theta; M_B) = h(2/3) \approx 0.918 \text{ bits}$` without defining $h(\cdot)$. This is the standard notation for binary entropy, but a reader unfamiliar with information theory - precisely the audience the worked example is meant to serve - will not know that. Either define it in line ("where $h(p) = -p\log_2 p - (1-p)\log_2(1-p)$ is the binary entropy") or replace the expression with a spelled-out calculation. The numerical value 0.918 alone would also suffice if the formula is dropped.

4. **The $B_{\text{test}}$ table entry is missing its critical scope qualifier.** The table in §7 lists the composition law for $B_{\text{test}}$ as "Intersection of rejection regions" and lists "Adaptive downstream tests" as the failure mode. This presentation implies that "intersection of rejection regions" is the general law and adaptivity is a special case where it fails. The more accurate reading is that the law holds *only under pre-specification* and has no stated form under adaptivity. A reader scanning only the table will miss this. Consider revising the composition-law cell to "Intersection of rejection regions (pre-specified only)" and the failure-mode cell to "No composition law known under adaptivity" to make the scope restriction visible in the table itself.

5. **Internal archive numbering is public-facing prose.** In the Aristarchus subsection: "The condition number of #15 is the chain-rule expression for the magnitude of the composed tangent cone. The piece did the right calculation; the composition rule names what it was a calculation of." The notation "#15" is the College's internal archive numbering and is opaque to any reader who approaches the published piece without knowledge of the archive sequence. The Aristarchus piece is already linked earlier in the same subsection; replace "#15" with "that piece" or "the Aristarchus reconstruction" throughout.

6. **"Condition numbers multiply" states an upper bound as an identity.** In §3, the final sentence under tangent blindness reads: "The second term is what amplifies ill-conditioning along a pipeline. It is the structural reason condition numbers multiply." The submultiplicativity of operator norms guarantees that $\kappa(M_2 \circ M_1) \leq \kappa(M_2) \cdot \kappa(M_1)$; it does not guarantee equality. "Multiply" in the scalar sense suggests equality, which is only achieved in specific circumstances (e.g., the Aristarchus case, where the angular instrument has near-unit condition number and the secant dominates). A more precise formulation: "It is the structural reason condition numbers can multiply - the composed condition number is bounded above by the product of the stage condition numbers, and that bound is often tight when stages are nearly uncorrelated in their ill-conditioning."
