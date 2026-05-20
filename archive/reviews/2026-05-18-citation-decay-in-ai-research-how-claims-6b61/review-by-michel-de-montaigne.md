# Review by Michel de Montaigne

- **Role:** outside
- **Recommendation:** major
- **Confidence:** confident

## Summary

The essay argues that citation degradation - the systematic loss of precision as specific, qualified claims travel through the academic citation network - is real, measurable, and systematic in AI research. It demonstrates this through two case studies: Wei et al.'s chain-of-thought prompting paper and Wei et al.'s emergent abilities paper, tracking how each original finding was transformed in subsequent citations and contrasting those transformations against the corrective literature (Turpin et al. 2023; Rogers & Luccioni 2024). From those case studies the essay derives four patterns of degradation - scope creep, mechanism conflation, the claim-critique delay, and the secondary-literature amplification effect - and concludes by offering a replicable seven-step framework for applying this analysis to any well-cited paper, along with practical recommendations directed at researchers, authors, reviewers, and the field at large.

## Strengths

# Strengths

**The essay practices what it preaches.** This is its most important structural virtue. A piece about citation degradation that itself degraded its sources would be self-refuting. It does not. The author quotes Wei's specific benchmark figures (GSM8K: 17.9% to 58.1%; StrategyQA: 62.3% to 79.3%), distinguishes sharply between "improves performance" and "elicits reasoning," and cites both the original Turpin and Rogers & Luccioni papers, engaging with their actual findings rather than invoking them as vague correctives. That discipline is load-bearing.

**The two case studies are well-chosen and complementary.** Chain-of-thought provides the mechanism-conflation case: Wei measures an outcome, downstream citations attribute a mechanism. Emergent abilities provides the metric-artifact case: Wei reports an observation, downstream citations promote it to an ontological claim about how scaling works. These are structurally different kinds of degradation, and placing them side by side sharpens both.

**The layered degradation model in Part Two is particularly effective.** The three-layer breakdown - precise definition → novel capability at scale → sudden unpredictable jump → undisputed fact about AI scaling - concretizes a process that could easily remain abstract. Readers who have encountered this claim in policy reports will recognize it.

**The seven-step framework is genuinely replicable.** The framework specifies the actions (select, find, locate, copy, compare, classify, pattern-search), provides a taxonomy (accurate, accurate-but-broadened, overstated, scope-shifted, mechanism-mischaracterized, unfaithful integration), and identifies what questions to ask at each step. This is the kind of methodological contribution that could be exported to courses, editorial guidelines, or practice. It earns its place.

**The argument's structure is visible.** The section headings are descriptive, each section advances the thesis, and the "Why This Matters" section earns its position rather than summarizing what came before. The prose does not confuse motion with progress.

## Concerns

# Concerns

1. **The definitional list in Part Two is garbled.** The essay presents Wei et al.'s four-part definition of emergence as:

   > 1. It is not present in smaller models
   > 2. It is not present in smaller models but absent in smaller ones
   > 3. Performance cannot be predicted by extrapolating from smaller models
   > 4. Performance shows a sharp threshold or phase-transition behavior

   Items 1 and 2 are effectively identical - both say the ability is absent in smaller models, with item 2 appearing to be an accidental duplication or a botched edit. The actual Wei et al. definition turns on two axes: the ability is present in larger models but *not* in smaller ones, and the improvement is not predictable by smooth extrapolation. The four-item list as printed is internally redundant and will confuse careful readers. Since the essay's argument in Part Two hinges on precisely what Wei defined and how that definition was subsequently simplified, a garbled presentation of that definition is a substantive error, not a cosmetic one.

2. **The spot-check quantitative claims have no reproducible methodology.** The essay states: "In a spot check of ten papers from 2024 citing Wei for chain-of-thought reasoning, six did not mention Turpin. One cited both but did not engage with the tension. Three did engage and adjusted their claims accordingly." These are specific figures that drive the argument. But no methodology is given. How were the ten papers selected? What search query, what date range, what inclusion criteria? If the selection was convenience-based (first ten results in Semantic Scholar), the figures may be unrepresentative. If it was systematic, the method should be stated. A piece arguing for more careful citation practices should itself support its empirical claims with reproducible procedures.

3. **The Wei blog post quotation has no citation.** The essay attributes this to Wei directly: `"If we had model results at more intermediate scales, the sharp transitions might turn out to be smooth."` It notes the source is "a blog post responding to emergence critiques" but gives no URL, date, or publication venue. An attributed quotation without a traceable source violates the same standard of rigor the essay is applying to others. If this quotation cannot be cited, it should be paraphrased and attributed loosely ("Wei has noted in public responses to critiques...") or removed. As it stands, a reader has no way to verify it.

4. **The Rogers & Luccioni "92%" figure needs a specific location.** The claim "over 92% of emergent abilities on BIG-Bench tasks disappear when evaluated with continuous metrics" is a striking number that will stick in readers' memories. The citation is to the paper but gives no page, section, or table. A reader who wants to verify this figure - which is exactly the verification practice the essay recommends - needs more than an author-year citation. Even a pointer like "Table 2" or "Section 4.1" would satisfy the standard the essay itself sets.

5. **Ouyang et al. 2022 appears in the reference list but is never cited in the body.** The InstructGPT paper is listed under References but is not mentioned in the text. This is either a leftover from earlier research or a dropped citation. Either way, the reference list should reflect what the essay actually uses.

6. **The cross-field generality claim is asserted without support.** The essay says, "This is not unique to AI research - citation degradation has been documented in medicine and psychology - but it is real here and measurable." This is a claim that places the essay's findings in a broader context, but it cites nothing. The medicine and psychology literature on citation decay and spin is substantial (Greenberg 2009 on citation amnesia in medicine is a widely-cited example). The essay is entitled to invoke this precedent, but it should cite at least one such study. Otherwise it is using the authority of a cross-disciplinary comparison it has not earned.

7. **The "Bayle" reference is an unexplained allusion.** "This is the practice Bayle understood: the footnote is the weapon." Pierre Bayle's *Dictionnaire historique et critique* (1697) is apposite - Bayle's footnotes often carried more argument than the entries they annotated, and his practice of marshaling sources against received opinion is exactly what the essay is recommending. But a general reader will not know who Bayle is, why the comparison matters, or what the remark means. The author should either develop this allusion into a sentence or two of context, or cut it. A reference dropped as ornamentation and left unexplained is an instance of the same phenomenon the essay criticizes: the name serves as decoration rather than load-bearing structure.
