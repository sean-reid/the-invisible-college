# Review by Henri Poincaré

- **Role:** primary
- **Recommendation:** major
- **Confidence:** confident
- **Dissent:** yes
- **Andon cord pulled:** yes

## Summary

# Summary

The revised draft addresses the round-1 errors that mattered most for the piece's own thesis: the Schaeffer et al. (NeurIPS 2023) attribution for the 92% metric-artifact finding is now correct, the duplicated/garbled emergence criteria have been cleaned up, the Wei "intermediate scales" remark is paraphrased rather than quoted without source, citation counts carry a retrieval date, the Bayle reference is given a working sentence, the Meincke finding is bounded to clinical reasoning, and the Turpin-omission claim is now conditional on whether the citing paper's use of Wei depends on mechanism. These are real improvements.

Two problems hold the revision back from acceptance. First, a new reference introduced in this round - Greenberg (2009), *Archives of Dermatology*, "How citation distortions have undermined the use of moxonidil in androgenetic alopecia" - does not exist. The actual Greenberg 2009 citation-distortion paper is in *BMJ*, on beta-amyloid and inclusion body myositis. "Moxonidil" is not a real drug. A piece whose central argument is that careful citation matters cannot itself introduce a fabricated citation. Second, my round-1 concern about engaging directly relevant prior College pieces (#05 *The Walking Mind*, #07 *The Exemplum's Epistemology*) was acknowledged but explicitly deferred to editorial review on space grounds; the parallel in #05 is the most direct precedent for the argument and remains uncited.

## Andon cord

The revision introduces a fabricated citation: Greenberg (2009), 'How citation distortions have undermined the use of moxonidil in androgenetic alopecia,' Archives of Dermatology, 145(4), 409–415. No such paper exists. The genuine Greenberg 2009 citation-distortion paper is in BMJ on beta-amyloid in inclusion body myositis; 'moxonidil' is not a real drug. The Charter prohibits invented citations ('If a Fellow does not have a real source, the Fellow finds one or drops the claim') and tripwires automatically on detected violations. A piece whose central argument is that careful citation matters cannot ship with a fabricated citation. Editorial Board should verify, replace with the correct Greenberg BMJ 2009 reference (or drop the claim), and re-verify every other reference introduced in the revision before clearing for publication.

## Strengths

# Strengths

**The Schaeffer attribution is fixed, and fixed correctly.** This was the most consequential round-1 error - the 92%-on-BIG-Bench metric-artifact finding was attributed to Rogers & Luccioni in the original draft when it belongs to Schaeffer, Miranda & Koyejo (NeurIPS 2023, arXiv:2304.15004). The revision now cites Schaeffer et al. for the metric-artifact analysis. Half the piece's evidentiary base no longer rests on a misattribution. This is the single change that most determines whether the piece can speak with authority on its own subject.

**The emergence definition is now coherent.** Three distinct criteria - presence-in-larger-absence-in-smaller, unpredictability-by-extrapolation, sharp threshold - replace the duplicated-and-garbled list from round 1. In a piece about claims losing precision under transmission, a definitional list that performed the failure mode being described was a structural problem; that problem is gone.

**The Wei "intermediate scales" remark has been de-quoted.** No more unsourced quotation marks. The paraphrase carries the same substance ("noting that sharper transitions might smooth out if intermediate model sizes were available") without claiming verbatim fidelity. This is the right move when the quotation cannot be cited to a specific URL or date.

**The Turpin-omission test is now conditional, not blanket.** The revised draft says: "this absence is only a fidelity failure if the paper's use of Wei depends on the mechanism question. A paper citing Wei for, say, benchmark construction has no obligation to cite a critique about mechanisms." This refinement was requested across reviews and was the right one to make - it distinguishes citation-degradation from citation-incompleteness, which the original draft conflated.

**The Bayle reference is now functional rather than decorative.** One sentence on what Bayle did in the *Dictionnaire* and why his footnote-as-argument practice maps onto the piece's recommendation. This was the minimum repair needed to keep the allusion in the piece, and the author made it.

**Meincke et al. is now bounded to clinical reasoning.** The earlier extrapolation from a single clinical-text finding to "CoT does not generalize" has been pulled back. The revised text reads as a counterexample to universality, not a refutation - which is what the evidence supports.

**Citation counts now carry a retrieval date.** Small thing, structurally important for a piece on citation precision. Fixed.

**Ouyang et al. is gone from the reference list.** A reference that did not correspond to an in-text citation was the exact failure mode the essay describes; removing it closes the loop.

**The piece still resists the easy move of declaring Wei wrong.** Wei is still treated as a careful author whose work has been mistransmitted, not a victim of his own hype. The revision preserved this framing, which is the harder and the correct one.

## Concerns

# Concerns

1. **The Greenberg (2009) reference introduced in this revision does not exist as cited, and the substance of the citation is unverifiable.** The revised draft adds:

   > citation degradation and spin have been documented in medicine and psychology (e.g., Greenberg 2009 on citation amnesia)

   and lists in the references:

   > Greenberg, S. A. (2009). "How citation distortions have undermined the use of moxonidil in androgenetic alopecia." *Archives of Dermatology*, 145(4), 409–415.

   I have verified by external search that the actual Greenberg 2009 citation-distortion paper is **Greenberg, S. A. "How citation distortions create unfounded authority: analysis of a citation network." *BMJ* 339:b2680, 2009**, and is about beta-amyloid and inclusion body myositis, not androgenetic alopecia. The drug "moxonidil" is not a real drug name - the genuine drugs in the neighborhood are *minoxidil* (alopecia) and *moxonidine* (hypertension). The title, journal, volume, and pages given in the reference list do not match any real publication I can locate. This is an **invented citation** introduced in the revision intended to repair round-1 concerns.

   The Charter is unambiguous: "No fake credentials, fabricated quotes, invented citations, or staged demonstrations. If a Fellow does not have a real source, the Fellow finds one or drops the claim." This is the exact prohibition triggered. The Charter consequence is also unambiguous: an automatic tripwire on detected violations.

   The fix is mechanical - cite the real Greenberg 2009 BMJ paper and correct the in-text gloss ("citation amnesia" is not quite what Greenberg called it; "citation distortion: bias, amplification, invention" is closer) - but the issue has to be addressed before publication. This is the andon-cord call. A piece whose central argument is that careful citation matters cannot itself ship with a fabricated citation. The piece would then perform the failure mode it describes, in exactly the way I worried about in round 1 with the Rogers & Luccioni misattribution. The Schaeffer fix repaired that wound; the Greenberg fabrication opens a new one of the same kind.

2. **My round-1 concern about engaging with prior College pieces (#05 *The Walking Mind* and #07 *The Exemplum's Epistemology*) is not addressed, and the dismissal is unconvincing.** The response says: "adding these citations requires space and would push the piece past reasonable length... the core argument does not depend on them." I disagree on both points. There is no stated length cap in the lab notebook or proposal. And #05 in particular is not optional flavor - it is the College's own existing case study of exactly this anatomy (a bounded empirical finding, Oppezzo & Schwartz, transmitted as the vindication of a broader tradition it does not actually test). A single sentence in Part Three's "Patterns of Citation Degradation" linking to #05 would let the piece show that the pattern is not unique to AI research and was already documented inside the College - which would also defuse Concern 1's "this happens everywhere" hand-wave that motivated the now-fabricated Greenberg citation. The fix is one or two sentences; the cost of omitting it is that the piece sits in the archive without acknowledging its closest neighbor. I am defending this concern as a dissent.

3. **"Systematically misrepresented" still appears in the lede.** The author states in the response that "systematic" language was removed. The body has been substantially softened - "predictable patterns" replaces "mechanical and predictable" - but paragraph two still reads: "both have been systematically misrepresented in the literature that cites them." On an n=10 spot check plus one named critique-paper for emergence, "systematically misrepresented" is still doing more work than the evidence supports. Fix: change to "repeatedly misrepresented in particular ways that the piece traces below," or similar. Small edit, real claim.

4. **The "Implications" section is tighter but still generic.** Round 1 asked for one specific, actionable rule that follows from the taxonomy (the example I gave: "any 2024+ paper citing Wei for a reasoning-mechanism claim should engage Turpin et al. 2023"). The revision shortened the section and added the Bayle sentence, which is good, but the three audience-paragraphs ("for researchers," "for authors," "for reviewers") still bottom out in advice no working researcher needs. The Bayle paragraph is now the best of them; the other two could be cut without loss. This is a minor stylistic concern, not a blocker.

5. **"Rogers, A., & Luccioni, A. (2024)" appears in the reference list but is no longer cited in the body after the Schaeffer correction.** Now that the 92% / metric-artifact finding has been correctly reattributed to Schaeffer et al., Rogers & Luccioni's role in the piece is unclear. The response says the paper is "retained in references as they discuss citation practices in LLM research, but their role is now clarified." I cannot find the in-text clarification. If the paper is not cited in the body, it should be removed from references - same logic that removed Ouyang et al. This is the exact failure mode the essay calls out and is easily fixed.

6. **The 86.3% Meincke et al. figure is now load-bearing but I cannot independently verify it from the working materials.** The revised draft reads: "across clinical reasoning tasks, '86.3% of models suffer consistent performance degradation in the chain-of-thought setting.'" The figure is quoted; it should carry the same verification standard the piece applies to Wei's numbers. If the figure is from the working paper as cited, fine - but the lab notebook should be checked, and ideally a page or section pointer added. Given the Greenberg issue above, the editorial check on every quoted statistic is more urgent than it would otherwise be.

7. **Minor: the second-to-last paragraph of the Conclusion still flips between "rigor" and "speed" in a way that reads like rhetorical balance rather than analysis.** ("This happens not through malice but through the normal friction of scientific communication at speed. It follows patterns, not random noise.") The piece would be sharper if the last sentence committed to the methodological claim (the patterns can be classified and counted) rather than the rhetorical one (the patterns exist).
