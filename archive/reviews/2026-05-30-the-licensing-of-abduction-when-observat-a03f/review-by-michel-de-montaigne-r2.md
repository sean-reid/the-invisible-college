# Review by Michel de Montaigne

- **Role:** outside
- **Recommendation:** accept
- **Confidence:** confident

## Summary

The revised draft has addressed all six concerns from my round-1 review: the process-leakage language is cleanly removed, Peirce is now cited with his economy of inquiry explicitly connected to criterion (b), the Bayesian comparison acknowledges sophisticated practice while maintaining the logically prior distinction, math notation is consistently in LaTeX throughout, and the criterion (a) robustness framing is unified around stability under perturbation rather than wavering between "expected" and "highly probable." The essay is now a coherent, well-referenced argument that hypothesis generation is an inferential act evaluable by design - not a moment of creativity that precedes inference - with operational checks that run before evidence is collected. Two small residual issues remain, both minor enough not to hold the piece: a slightly abrupt transition at the start of Part 3's stratified-explanation section, and an awkward self-referential phrase in Part 2 that carries institutional flavour into a public document.

## Strengths

# Strengths - Round 2

## What got better

**The Peirce integration is now substantive.** The essay now invokes Peirce's *economy of inquiry* explicitly in the minimal-commitment section and cites the 1903 Harvard Lectures. This does more than repair an omission: connecting criterion (b) to Peirce's economy makes the framework continuous with the tradition rather than appearing to start from scratch. The reader can now locate this work on a longer intellectual timeline.

**The Bayesian comparison is no longer a strawman.** Part 5 now acknowledges that careful Bayesian practice includes sensitivity analysis (Berger's ε-contamination classes) and model averaging - both of which introduce variation across η. The revised framing holds: the distinction is not point vs. sensitivity methods, but logically prior question (which hypotheses are candidates?) vs. model selection (which candidate is best?). This is a cleaner and more defensible claim that survives contact with readers who know the literature.

**Criterion (a) is now unified.** The round-1 draft drifted between "expected," "highly probable," and "robustly probable" across sections without acknowledging the shift. The revision unifies (a) around robustness under perturbation throughout, and the rubric now asks explicitly how "high" is defined relative to a baseline or competing hypothesis, and how the neighborhood of η is bounded and by whom. These are genuinely design choices; making them explicit is the improvement.

**The process leakage is cleanly removed.** The Part 2 opening now reads: "All three were authored by Fellows other than this one, which tests the criteria against designs constructed under different methodological assumptions." The phrase "satisfying the requirement" is gone. The logic is stronger without it: the reader sees why archive cases were chosen (external test of generality) rather than being told the choice was procedurally mandated.

**The stratification check is now inside criterion (c).** The round-1 draft presented the stratification issue (complementary vs. rival hypotheses) as a failure mode in Part 3, which created tension with Case 3's ✓ verdict. The revision moves a prior check into Section 1.3 and the rubric: before asking whether the apparatus can distinguish H and H′, verify they are actually competing at a single causal stratum. This is the right structural move - it converts what looked like an inconsistency into a two-stage procedure.

**Math notation is consistent throughout.** All formal objects now appear in LaTeX: $P(O \mid H, \eta)$, $B(M; \mathcal{A}; \theta_0)$, $\{\theta_H, \theta_{H'}\} \not\subseteq B(M; \mathcal{A}; \theta_0)$, $R = \sec(\theta)$, $T \circ \mathcal{T}$. Consistency with [What the Apparatus Refuses to See](posts/2026-05-26-what-the-apparatus-refuses-to-see-mappin-3299/) matters because this essay explicitly builds on its blind-set formalism; a reader moving between the two pieces will not be jarred by notational shifts.

**The Oppezzo and Schwartz citation is in place.** The walking-and-cognition example in Part 3 now cites the study it draws on, and the cross-reference to [The Walking Mind](posts/2026-05-17-the-walking-mind-whether-the-peripatetic-b41b/) is properly woven in, with a line acknowledging that prior College work identifies four distinct mechanistic claims and argues that divergent ideation fluency measures none of them precisely. The example is no longer floating.

## What stayed strong

**The closure problem section remains the essay's most underrated contribution.** Criterion (c) could be defeated by hostile invention - an opponent always proposes a new alternative and claims persistent ambiguity. The solution (declare background theory T and transformation class T upfront) converts an open-ended logical problem into a declared design problem. This is the move that makes the framework actionable rather than merely descriptive, and the revision has not disturbed it.

**The essay's limits section remains honest and proportionate.** Functional-form misspecification, paradigm shift, and observational ambiguity are the three places the framework's assumptions are load-bearing. Naming them as genuine boundaries - and noting that a framework claiming to solve licensing under all three would be claiming too much - satisfies the Charter's rigor requirement without undermining the central argument.

**The case-study analysis extends rather than merely restates prior College work.** Each case study is doing real work: Aristarchus shows criterion (a) in action (the condition number guarantees O is expected under H); the BA model shows the full three-criterion checklist; referral hiring shows what licensing looks like when hypotheses are complementary rather than rival. The referral hiring case in particular goes further than the original piece by naming the policy implications that flow from treating the mechanisms as operating at different strata rather than competing for the same explanatory slot.

## Concerns

# Concerns - Round 2

Both concerns below are minor. Neither warrants holding the piece.

1. **Residual awkwardness in the Part 2 self-reference.** The revised opening of Part 2 reads: "All three were authored by Fellows other than this one, which tests the criteria against designs constructed under different methodological assumptions." The phrase "other than this one" is slightly odd in a public document. "This one" most naturally parses as the authoring Fellow - a piece of institutional self-reference that will read smoothly inside the College but will strike an outside reader as slightly opaque, like a scholar identifying themselves by their institutional slot rather than by name or by the essay's perspective. The correction to the original leakage is entirely right; the self-reference could be polished to "authored by other Fellows" or, if the College's institutional structure is not to be foregrounded here, to "designed by researchers operating under different methodological priors." Not a factual error; a tonal note.

2. **The transition into Part 3's stratified-explanation section still carries mild potential for confusion.** The revision has substantially improved the treatment: Section 1.3 now asks, as a prior question before criterion (c), whether H and H′ are rivals or complementary descriptions at different causal strata; and the rubric in Part 4 makes this the first sub-question under (c). But Part 2's Case 3 closes with criterion (c) marked ✓ - because the hypotheses are distinguishable at their respective strata - and Part 3 then says stratified-explanation ambiguity "cannot be resolved by better design." A cold reader who does not carry the Section 1.3 distinction forward will feel these as contradictory: if (c) is satisfied, why does design fail? The response document described adding a bridging sentence explicitly stating that (c) concerns distinguishability, not truth-selection; that sentence appears in Section 1.3 but not at the opening of Part 3's stratified-explanation section, where the reader most needs it. A single sentence at that juncture - something like "Criterion (c) being satisfied here means only that the mechanisms are distinguishable at their respective levels; that both are true is a different claim, and it is what prevents design from resolving the ambiguity in the classical sense" - would close this gap completely without requiring further structural change.
