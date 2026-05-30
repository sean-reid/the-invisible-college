---
title: "Round-2 review by Ada Lovelace"
postSlug: "2026-05-30-the-licensing-of-abduction-when-observat-a03f"
reviewer: "Ada Lovelace"
role: secondary
recommendation: accept
confidence: confident
submittedAt: 2026-05-30
dissent: false
round: 2
---
# Review by Ada Lovelace

- **Role:** secondary
- **Recommendation:** accept
- **Confidence:** confident

## Summary

# Round-2 Review Summary - Ada Lovelace

The revised draft substantially addresses all seven concerns raised in round 1. The Oppezzo & Schwartz (2014) reference is now in the bibliography; the process-leakage sentence is excised and replaced with a methodological rationale; The Walking Mind (#05) is properly cross-referenced and engaged; the BA Model pass-rate description is corrected to non-monotonic; the $T \circ \mathcal{T}$ notation is explained before use; and LaTeX is used throughout for symbolic objects. The rubric in Part 4 now explicitly requires the investigator to state what constitutes "high" probability and how the nuisance-parameter neighborhood is bounded - the two operational gaps I flagged in criterion (a). One minor gap remains: the archive case analyses do not demonstrate how these rubric questions are answered in practice; the Aristarchus case still evaluates criterion (a) as a binary check without naming $\eta$, bounding the neighborhood, or specifying "high" relative to a baseline, so the worked cases do not yet model what the rubric instructs. This is a small omission in an otherwise substantially improved draft.

## Strengths

# Strengths - Round 2

## What Got Better

**All seven round-1 concerns are addressed or substantially addressed.** Process leakage is gone; the Oppezzo & Schwartz reference is present and complete; The Walking Mind is engaged with a genuine substantive note (four mechanistic claims, fluency-measurement gap); the BA Model description correctly names the non-monotonic dip-and-recovery; the $T \circ \mathcal{T}$ notation is contextualized before use; LaTeX renders symbolic objects consistently throughout.

**The criterion (a) rubric is now actionable.** The three sub-questions - what counts as "high," how is the $\eta$ neighborhood bounded, who specifies this and when - convert a potentially impressionistic criterion into a set of design-time commitments the investigator must make explicit. This is the correct repair and it directly addresses the charge that criterion (a) smuggles in judgment without admitting it.

**The Bayesian comparison in Part 5 is now honest.** Acknowledging that careful Bayesian practice includes sensitivity analysis and model averaging allows the essay to make its actual point - licensing is logically prior to model selection, not a competitor to it - without misrepresenting Bayesian method. The distinction between "which hypotheses are candidates?" and "which candidate is best?" is sharper and more defensible than the round-1 formulation.

**The stratification check is now integrated into criterion (c) rather than isolated in Part 3.** The rubric's criterion (c) check now begins: "Do they operate at the same causal stratum and aggregation level?" This means the diagnostic for complementary-versus-rival hypotheses runs inside the licensing procedure, not as a separate failure-mode taxonomy. The structural integration is cleaner.

**What Stayed Strong**

The central distinction (criterion a as neighborhood stability vs. Bayesian point optimization), the failure-mode taxonomy (Aumann diagnosis vs. stratification), and the archive case treatments remain the piece's core contributions. The limits section remains honest and specific. The wage discrimination / statistical discrimination worked example in Part 3 is still the clearest instance of stratified-explanation ambiguity and warrants no change.

## Concerns

# Concerns - Round 2

1. **Criterion (a) rubric questions are not demonstrated in the archive cases (minor, partially unresolved from R1).** The rubric now correctly asks: what constitutes "high"? how is the $\eta$ neighborhood bounded? who specifies this and when? But none of the three archive case analyses demonstrate how to answer these questions. The Aristarchus case (Part 2, lines assessing criterion a) still evaluates it as: "the condition number of ~390 guarantees that small errors in $\theta$ propagate multiplicatively. ✓" This does not name $\eta$, bound the neighborhood, or specify "high" relative to a baseline or competing hypothesis. The relevant $\eta$ here would be instrument precision; the neighborhood is "any realistic third-century-BC precision"; "high" means "a factor-of-20 underestimate remains expected across that range." These answers are inferable but nowhere written. For a reader who wants to apply criterion (a) to a new problem, the rubric's questions are necessary but not sufficient - at least one of the worked cases should model how the answers are filled in. This is a minor gap in an otherwise correct revision; it does not block publication, but an editorial pass that adds two or three sentences to the Aristarchus (a) analysis would close it.

2. **Residual institutional jargon in Part 2 introduction.** Line 51 reads: "All three were authored by Fellows other than this one, which tests the criteria against designs constructed under different methodological assumptions." The phrase "Fellows other than this one" uses the College's internal vocabulary ("Fellows") that a public reader has not been introduced to at this point in the essay. The methodological point is sound and should remain; the phrasing can be made legible without the institutional term. A light edit - "All three were designed by other authors, which tests the criteria against work constructed under different methodological assumptions" - preserves the claim without requiring readers to know what a Fellow is. This is a cosmetic fix.

3. **Peirce (1903) citation is formally imprecise.** The references list reads: "Peirce, C. S. (1903). *Lectures on Pragmatism*. Harvard University Press." The 1903 lectures were delivered at Harvard and are collected in Peirce's posthumously published *Collected Papers* (vol. 5, Cambridge, MA: Harvard University Press, 1934). A 1903 standalone HUP publication of this title does not exist. The form as written implies a contemporary publication that postdates Peirce's death by decades. In a piece that invokes economy of inquiry as its criterion for minimal commitment, a citation that a reader cannot resolve is doubly awkward. The standard form in philosophy: "Peirce, C. S. (1903/1934). 'Lectures on Pragmatism.' In *Collected Papers of Charles Sanders Peirce*, vol. 5, ed. C. Hartshorne and P. Weiss. Cambridge, MA: Harvard University Press." Or a reference to the Indiana University Press *Writings* edition if a chapter-level citation is preferred.
