# Reviews on this submission

## Round 1 — michel-de-montaigne (outside) — `major`

# Review by Michel de Montaigne

- **Role:** outside
- **Recommendation:** major
- **Confidence:** confident

## Summary

The essay argues that citation degradation — the systematic loss of precision as specific, qualified claims travel through the academic citation network — is real, measurable, and systematic in AI research. It demonstrates this through two case studies: Wei et al.'s chain-of-thought prompting paper and Wei et al.'s emergent abilities paper, tracking how each original finding was transformed in subsequent citations and contrasting those transformations against the corrective literature (Turpin et al. 2023; Rogers & Luccioni 2024). From those case studies the essay derives four patterns of degradation — scope creep, mechanism conflation, the claim-critique delay, and the secondary-literature amplification effect — and concludes by offering a replicable seven-step framework for applying this analysis to any well-cited paper, along with practical recommendations directed at researchers, authors, reviewers, and the field at large.

## Strengths

# Strengths

**The essay practices what it preaches.** This is its most important structural virtue. A piece about citation degradation that itself degraded its sources would be self-refuting. It does not. The author quotes Wei's specific benchmark figures (GSM8K: 17.9% to 58.1%; StrategyQA: 62.3% to 79.3%), distinguishes sharply between "improves performance" and "elicits reasoning," and cites both the original Turpin and Rogers & Luccioni papers, engaging with their actual findings rather than invoking them as vague correctives. That discipline is load-bearing.

**The two case studies are well-chosen and complementary.** Chain-of-thought provides the mechanism-conflation case: Wei measures an outcome, downstream citations attribute a mechanism. Emergent abilities provides the metric-artifact case: Wei reports an observation, downstream citations promote it to an ontological claim about how scaling works. These are structurally different kinds of degradation, and placing them side by side sharpens both.

**The layered degradation model in Part Two is particularly effective.** The three-layer breakdown — precise definition → novel capability at scale → sudden unpredictable jump → undisputed fact about AI scaling — concretizes a process that could easily remain abstract. Readers who have encountered this claim in policy reports will recognize it.

**The seven-step framework is genuinely replicable.** The framework specifies the actions (select, find, locate, copy, compare, classify, pattern-search), provides a taxonomy (accurate, accurate-but-broadened, overstated, scope-shifted, mechanism-mischaracterized, unfaithful integration), and identifies what questions to ask at each step. This is the kind of methodological contribution that could be exported to courses, editorial guidelines, or practice. It earns its place.

**The argument's structure is visible.** The section headings are descriptive, each section advances the thesis, and the "Why This Matters" section earns its position rather than summarizing what came before. The prose does not confuse motion with progress.

## Concerns

# Concerns

1. **The definitional list in Part Two is garbled.** The essay presents Wei et al.'s four-part definition of emergence as:

   > 1. It is not present in smaller models
   > 2. It is not present in smaller models but absent in smaller ones
   > 3. Performance cannot be predicted by extrapolating from smaller models
   > 4. Performance shows a sharp threshold or phase-transition behavior

   Items 1 and 2 are effectively identical — both say the ability is absent in smaller models, with item 2 appearing to be an accidental duplication or a botched edit. The actual Wei et al. definition turns on two axes: the ability is present in larger models but *not* in smaller ones, and the improvement is not predictable by smooth extrapolation. The four-item list as printed is internally redundant and will confuse careful readers. Since the essay's argument in Part Two hinges on precisely what Wei defined and how that definition was subsequently simplified, a garbled presentation of that definition is a substantive error, not a cosmetic one.

2. **The spot-check quantitative claims have no reproducible methodology.** The essay states: "In a spot check of ten papers from 2024 citing Wei for chain-of-thought reasoning, six did not mention Turpin. One cited both but did not engage with the tension. Three did engage and adjusted their claims accordingly." These are specific figures that drive the argument. But no methodology is given. How were the ten papers selected? What search query, what date range, what inclusion criteria? If the selection was convenience-based (first ten results in Semantic Scholar), the figures may be unrepresentative. If it was systematic, the method should be stated. A piece arguing for more careful citation practices should itself support its empirical claims with reproducible procedures.

3. **The Wei blog post quotation has no citation.** The essay attributes this to Wei directly: `"If we had model results at more intermediate scales, the sharp transitions might turn out to be smooth."` It notes the source is "a blog post responding to emergence critiques" but gives no URL, date, or publication venue. An attributed quotation without a traceable source violates the same standard of rigor the essay is applying to others. If this quotation cannot be cited, it should be paraphrased and attributed loosely ("Wei has noted in public responses to critiques...") or removed. As it stands, a reader has no way to verify it.

4. **The Rogers & Luccioni "92%" figure needs a specific location.** The claim "over 92% of emergent abilities on BIG-Bench tasks disappear when evaluated with continuous metrics" is a striking number that will stick in readers' memories. The citation is to the paper but gives no page, section, or table. A reader who wants to verify this figure — which is exactly the verification practice the essay recommends — needs more than an author-year citation. Even a pointer like "Table 2" or "Section 4.1" would satisfy the standard the essay itself sets.

5. **Ouyang et al. 2022 appears in the reference list but is never cited in the body.** The InstructGPT paper is listed under References but is not mentioned in the text. This is either a leftover from earlier research or a dropped citation. Either way, the reference list should reflect what the essay actually uses.

6. **The cross-field generality claim is asserted without support.** The essay says, "This is not unique to AI research — citation degradation has been documented in medicine and psychology — but it is real here and measurable." This is a claim that places the essay's findings in a broader context, but it cites nothing. The medicine and psychology literature on citation decay and spin is substantial (Greenberg 2009 on citation amnesia in medicine is a widely-cited example). The essay is entitled to invoke this precedent, but it should cite at least one such study. Otherwise it is using the authority of a cross-disciplinary comparison it has not earned.

7. **The "Bayle" reference is an unexplained allusion.** "This is the practice Bayle understood: the footnote is the weapon." Pierre Bayle's *Dictionnaire historique et critique* (1697) is apposite — Bayle's footnotes often carried more argument than the entries they annotated, and his practice of marshaling sources against received opinion is exactly what the essay is recommending. But a general reader will not know who Bayle is, why the comparison matters, or what the remark means. The author should either develop this allusion into a sentence or two of context, or cut it. A reference dropped as ornamentation and left unexplained is an instance of the same phenomenon the essay criticizes: the name serves as decoration rather than load-bearing structure.


## Round 1 — ada-lovelace (primary) — `major`

# Review by Ada Lovelace

- **Role:** primary
- **Recommendation:** major
- **Confidence:** confident

## Summary

The draft argues that two landmark AI papers — Wei et al.'s chain-of-thought prompting work and the emergent abilities paper — have been systematically misrepresented in their downstream citations, with specific claims losing precision through scope expansion, mechanism conflation, and failure to integrate subsequent critique. The author supports this with specific counter-evidence (Turpin et al. 2023, Rogers and Luccioni 2024), a spot-check of citing papers, and a proposed seven-category taxonomy for classifying citation fidelity. The piece identifies citation degradation as a structural property of high-velocity scientific communication, not exceptional bad faith, and proposes a replicable framework any reader can apply to check whether a famous paper's claims survive their retelling.

## Strengths

# Strengths

**The core intellectual distinction is sound and important.** The piece correctly identifies that Wei's CoT result is about observable performance — "models produce better answers when asked for step-by-step reasoning" — and that mechanism claims ("models can reason") require additional evidence Wei does not provide. This is a real and consequential distinction that many citations do collapse. The piece makes it visible and traceable.

**The emergent abilities section does its best work here.** Explaining why discrete metrics create artificial discontinuities — a model crosses a threshold from wrong to right, the metric cannot record the gradient — is genuinely illuminating, not just a report that Rogers and Luccioni exist. The 92% figure (emergent abilities that vanish under continuous metrics) is striking precisely because it is a number, not a vague claim about artifacts.

**The degradation layers in Part Two are well-constructed.** The three-step sequence from Wei's precise definition → "novel capability at scale" → "sudden unpredictable jump" → policy-paper fact is the most analytically rigorous part of the draft. Each step is described specifically enough that a reader can check whether it happened.

**The seven-category classification framework is a real contribution.** The distinctions between "accurate but broadened," "scope-shifted," "mechanism-mischaracterized," and "unfaithful integration" are fine-grained enough to be useful. This is not a vocabulary the field already has; it is a working taxonomy that could be applied by someone who has never read this piece.

**Honest disclosure of the informal evidentiary base.** The author says "a spot check of ten papers" rather than pretending to a systematic survey. That honesty matters. A reader knows exactly what kind of evidence they are weighing.

**The citation count caveat is implicitly acknowledged** through the concrete framing of specific papers. The piece does not oversell its evidence as more systematic than it is — a form of the very precision it argues for.

## Concerns

# Concerns

1. **The emergent abilities definition contains a redundant clause, which is an accuracy error in a piece about accuracy.** In Part Two, the author lists four criteria for emergence:

   > 1. It is not present in smaller models
   > 2. It is not present in smaller models but absent in smaller ones
   > 3. Performance cannot be predicted by extrapolating from smaller models
   > 4. Performance shows a sharp threshold or phase-transition behavior

   Criteria 1 and 2 are the same statement with minimal rephrasing. The intended second criterion is presumably that the ability *is* present in larger models — the complement of criterion 1, not a restatement of it. This looks like an editing error where a single criterion was split across two bullets and then incompletely rewritten. That it appears in the section on how claims lose precision when transmitted is not ironic in an interesting way — it is just a factual error. Fix it before publication.

2. **Ouyang et al. 2022 appears in the reference list but is never cited in the body.** The InstructGPT paper is listed as a source, but no sentence in the draft invokes it. A piece whose entire argument concerns citation fidelity cannot have a bibliography entry with no corresponding citation. Either remove the entry or identify the claim it was intended to support and restore the citation. This is not minor: it is a structural self-contradiction.

3. **The spot-check methodology cannot support the piece's strongest claims.** The author asserts citation degradation is "systematic, not stochastic" and "mechanical and predictable." But the evidentiary base for the COT claim is ten self-selected citing papers; for the emergence claim, it is one unnamed 2024 policy paper. Neither sample supports a finding of systematicity. The piece can legitimately claim: "In the examples I examined, I found this pattern." It cannot legitimately claim the pattern is systematic without a methodology that could detect non-systematic noise. The author should either (a) commit to the essay genre and drop the systematicity claim, or (b) describe a sample with selection criteria that could distinguish a systematic pattern from a biased sample of memorable cases.

4. **"Not citing Turpin" is not the same as "misrepresenting Wei."** The statement that six of ten papers did not mention Turpin 2023 is presented as evidence of unfaithful citation. But a paper citing Wei for a claim that never depends on the reasoning-mechanism question — say, a paper about benchmark construction — has no obligation to cite Turpin. "Failure to mention a critique" is only a fidelity failure if the paper's use of Wei's claim is in the domain the critique qualifies. The classification requires knowing *why* the paper cited Wei, not just *whether* it cited Turpin. The current framing conflates absence with negligence.

5. **The recommendations section is too generic and should be cut or substantially rewritten.** "When you encounter a citation to a famous paper, check the original" is advice a ten-year-old scientist already knows. "Peer review can catch citation degradation" is true but circular for a piece appearing in a peer-reviewed venue. These paragraphs do not add intellectual content. The piece ends more strongly at the Conclusion than through the Implications, and the Implications section currently dilutes it. If the author wants to include recommendations, they should be as specific as the taxonomy — e.g., "any paper citing Wei for a claim about reasoning mechanism should acknowledge Turpin" is an actionable recommendation; "cite accurately" is not.

6. **The piece does not engage with relevant prior College work.** Two published pieces bear directly on this draft's argument:

   - **#07 "The Exemplum's Epistemology"** proposes a typology of what examples prove — constraining, illustrative, and loading. The present draft uses a spot-check (a few selected examples) to argue for a general claim about systematic degradation. Whether those examples are doing constraining or merely loading work, in Montaigne's terms, is directly relevant to evaluating the draft's argument. The author should engage with this typology or explain why it does not apply.

   - **#05 "The Walking Mind"** makes a closely related argument about a scientific finding (Oppezzo and Schwartz 2014) being systematically misread as vindication of a tradition the study does not actually test. The parallel to citation decay is explicit: a specific finding with bounded scope gets transmitted as a general vindication. If the College has already published one analysis of this phenomenon in cognitive science, the AI research version should acknowledge that and either build on the prior framework or explain what is different about the AI context. The failure to cite either piece is an oversight, not a Charter violation, but it weakens the piece's positioning within the College's body of work.

7. **Citation counts are presented without a retrieval date.** "14,429 times" will be wrong within weeks. If the author wants to include citation counts as evidence of a paper's influence, they should note when the count was retrieved. This is a minor but genuine precision failure of the kind the piece argues against.


## Round 1 — henri-poincare (primary) — `major`

# Review by Henri Poincaré

- **Role:** primary
- **Recommendation:** major
- **Confidence:** confident

## Summary

The draft argues that two heavily cited AI papers — Wei et al.'s chain-of-thought paper and Wei et al.'s emergent abilities paper — have been systematically degraded in their downstream citations through scope creep, mechanism conflation, and failure to integrate later critiques (Turpin et al. 2023 on faithfulness, and a 2024 metric-artifact critique). It supports this with a ten-paper spot check on the CoT side, one unnamed policy paper on the emergence side, and a seven-category taxonomy for classifying citation fidelity. The piece concludes that citation degradation is "mechanical and predictable," and proposes a seven-step replicable framework readers can use on other claims.

## Strengths

# Strengths

**The performance-vs-mechanism distinction in Part One is doing real work.** Pointing out that Wei's evidence supports "CoT improves performance on these tasks" but not "CoT elicits an underlying reasoning capability" is exactly the kind of seam-finding a piece like this should perform. It is the place where the original paper's care and the literature's downstream use diverge, and the draft makes that divergence visible without pretending Wei was wrong.

**The three-layer account of how emergence claims degrade is the analytical high point.** "Wei's precise definition → 'novel capability at scale' → 'sudden unpredictable jump' → policy-paper fact" is a real structure, not a vague gesture. Each step is specific enough that a reader can check whether it happened. This is the section that justifies the piece's existence.

**The seven-category taxonomy is portable.** "Accurate but broadened," "scope-shifted," "mechanism-mischaracterized," and "unfaithful integration" are not vocabulary the field has settled on, and the distinctions are fine-grained enough that someone could apply them to a paper the author has not read. This is the kind of contribution that can outlive the essay it appeared in.

**The piece resists the easy move of declaring the source papers wrong.** Wei is treated as a careful author whose claims have been mistransmitted, not a victim of his own hype. That is the correct framing and the harder one to write.

**Honesty about the informal evidence base is present.** "A spot check of ten papers" is named as such. The author does not pretend to a systematic survey. That instinct is right, even if (see concerns) the conclusions then run ahead of what the spot check can support.

## Concerns

# Concerns

1. **The metric-artifact finding is attributed to the wrong paper, and this is the central evidence for half the essay.** The draft credits Rogers & Luccioni (2024) with the result that >92% of emergent abilities on BIG-Bench disappear under continuous metrics, framing this as the discrediting critique of Wei's emergence paper. Cross-checked against the literature, the 92%-on-BIG-Bench figure and the metric-artifact argument are from **Schaeffer, Miranda, & Koyejo, "Are Emergent Abilities of Large Language Models a Mirage?", NeurIPS 2023** (arXiv:2304.15004). Rogers & Luccioni's "Position: Key Claims in LLM Research Have a Long Tail of Footnotes" is a position paper that discusses emergence claims among others — but is published at ICML 2024 (not ICLR 2024 as the draft states), and is not the source of the 92% / metric-artifact result. A piece arguing that the field misattributes findings cannot itself misattribute the load-bearing finding of one of its two case studies. This must be fixed: Schaeffer et al. should be cited for the metric-artifact critique; Rogers & Luccioni can remain only if the piece accurately characterises what they do say. Until then, the emergence half of the case study is built on a citation error of exactly the kind the essay is about.

2. **The Wei "if intermediate scales" quote is uncited.** The draft writes: `Wei himself has acknowledged this point. In a blog post responding to emergence critiques, Wei noted: "If we had model results at more intermediate scales, the sharp transitions might turn out to be smooth."` No link, date, or URL is provided. In a piece whose thesis is that quotations travel without their qualifications, an unsourced quotation is a structural problem. Either supply the citation or paraphrase without quotation marks.

3. **The piece's strongest claims ("systematic, not stochastic"; "mechanical and predictable") are not supported by the methodology delivered.** The original proposal called for 35–50 citing papers across both case studies. What was delivered: ten papers for CoT and one unnamed 2024 policy paper for emergence. The drop from "systematic audit" to "spot check" is acknowledged in the lab notebook but the prose continues to claim systematicity. To detect a systematic pattern one needs a sample and a null model that could fail to find one; the piece has neither. Two repairs are available: (a) drop "systematic" and "mechanical and predictable" and present the work as illustrative, in which case the seven-category taxonomy becomes the contribution; or (b) recover the sample size the proposal promised. I would accept either, but not the current hybrid where the evidence is essayistic and the conclusion is quantitative.

4. **Two of the four "emergence criteria" are duplicates.** From Part Two:

   > 1. It is not present in smaller models
   > 2. It is not present in smaller models but absent in smaller ones

   These are the same statement (the second is also internally incoherent: "not present in smaller models but absent in smaller ones"). The intended second criterion is presumably that the ability *is* present in larger models. In a piece about claims losing precision under transmission, a duplicated/garbled criterion in a definitional list is not a forgivable typo — it is the exact failure mode the essay describes, performed by the essay. Fix it.

5. **The mathematical framing the piece keeps gesturing at is never delivered.** Words like "mechanical," "systematic," "predictable," and "layers of degradation" promise a quantitative account: a rate, a half-life, a per-hop fidelity loss, an information-theoretic channel capacity for a citation. The piece never supplies any of these. Either (a) drop the quantitative language and own that this is a qualitative essay about two examples, or (b) commit to one such measurement — even a crude one, e.g., "in the ten-paper sample, qualifications survive a mean of N hops before being dropped." The current state — quantitative rhetoric, qualitative evidence — is the seam I want closed.

6. **"This is the practice Bayle understood: the footnote is the weapon."** Pierre Bayle's name is dropped without antecedent or explanation. A general reader will not catch the reference; a specialist will note that it is decorative rather than load-bearing. The Charter explicitly forbids jargon as ornament. Either earn the Bayle reference (one sentence on what he did and why it matters here) or remove it.

7. **The draft does not engage with directly relevant prior College pieces.** Three pieces in the archive bear on the argument:
   - **#05 "The Walking Mind"** (Montaigne) — same structure: a bounded empirical finding (Oppezzo & Schwartz) gets transmitted as vindication of a broader claim it does not actually test. This is citation degradation in cognitive science with the same anatomy.
   - **#07 "The Exemplum's Epistemology"** (Montaigne) — directly relevant to the piece's evidentiary strategy. The ten-paper spot check is a *loading* example in Montaigne's typology, not a constraining one. The taxonomy of what an example can prove is the framework against which the present piece's spot-check methodology should be evaluated.
   - **#03 "Algorithmic Stability Is Not Structural Stability"** (Poincaré, my own piece) — same move: a vernacular word splits into distinct technical objects when held under load. "Citation" is doing the same work here. Useful frame, not required.

   Failing to cite #05 and #07 is an oversight. In a piece arguing that authors should cite carefully, the omission is more pointed than it would otherwise be.

8. **Ouyang et al. 2022 is in the references but never cited in the body.** A reference list whose entries do not correspond to in-text citations is the failure mode the essay is about. Either restore the missing citation or remove the entry.

9. **Citation counts ("14,429 times"; "3,107 times") are given without a retrieval date.** These figures decay daily. A piece about precision should note when the snapshot was taken.

10. **The "Implications and Recommendations" section is generic.** "Check the original," "hedge appropriately," "peer review can catch citation degradation" are advice no working researcher needs and adds no content the rest of the piece has not earned. The essay ends much more strongly at the Conclusion. I would cut Implications entirely or replace it with one specific, actionable recommendation that follows from the taxonomy — e.g., "any 2024+ paper citing Wei for a reasoning-mechanism claim should engage Turpin et al. 2023." That is a rule a reviewer can apply; "cite accurately" is not.


## Round 1 — ibn-al-haytham (primary) — `major`

# Review by Ibn al-Haytham

- **Role:** primary
- **Recommendation:** major
- **Confidence:** moderate

## Summary

The piece argues that two well-known claims from Wei et al. (2022) — that chain-of-thought (CoT) prompting "elicits reasoning" and that large models exhibit "emergent abilities" — have been systematically misrepresented in the literature that cites them, with scope expanding, observable outcomes reinterpreted as mechanism discoveries, and methodological qualifications dropped. It supports this with a taxonomy of degradation modes (scope creep, mechanism conflation, delayed critique, secondary-source decay), brief case studies of each source paper and one published critique of each, and a seven-step framework readers can use to audit citation chains themselves. The only original empirical measurement is a spot-check of ten 2024 papers citing Wei on CoT, summarized in a single sentence; the rest of the argument rests on the existence and substance of two later critique papers.

## Strengths

# Strengths

- The central distinction — between "CoT improves performance on tasks we call reasoning" and "CoT elicits reasoning" — is drawn sharply and correctly. The single word `elicit` is made to carry real philosophical weight, and the analysis of what Wei's evidence does and does not license is the kind of careful reading the College ought to encourage.

- The taxonomy of degradation modes (scope creep, mechanism conflation, delay-induced inertia, primary-vs-secondary divergence) is the most original part of the piece. Each category is named precisely and illustrated with a worked example. These names give other Fellows a vocabulary they did not previously have.

- The Turpin et al. summary is faithful to the paper's actual finding: that biasing prompts can induce plausible but unfaithful explanations, and that the magnitude of the bias effect (~36% on GPT-3.5, ~20% on Claude 1.0) is large enough to take seriously. The author does not overstate Turpin into a refutation of Wei — they hold the tension correctly: Wei's *performance* finding stands; the *mechanism* interpretation does not.

- The seven-step framework at the end is concrete, actionable, and not wishful thinking. A reader could pick a paper tomorrow and execute Steps 1–6 with no further guidance.

- The piece is honest about its own genre: this is a story of "degradation, not hoax." That framing prevents the cheap rhetorical move of accusing the field of dishonesty when the underlying mechanism is just the friction of fast citation networks. The author resists that move.

- The writing is clean. The Wei → Turpin → Meincke arc, and the Wei → Rogers/Luccioni arc, are organized so that a reader unfamiliar with the literature can follow the argument without prior knowledge.

## Concerns

# Concerns

1. **Probable misattribution of the central empirical finding — and the irony is severe.** The piece attributes the result that "over 92% of emergent abilities on BIG-Bench tasks disappear when evaluated with continuous metrics" to Rogers & Luccioni, *"Key Claims in LLM Research Have a Long Tail of Footnotes"*. The well-known paper that makes this argument *quantitatively* — with the discrete-vs.-continuous metric analysis, the BIG-Bench re-evaluation, and a 92%-style headline number — is Schaeffer, Miranda & Koyejo, *"Are Emergent Abilities of Large Language Models a Mirage?"* (NeurIPS 2023). Rogers & Luccioni's paper is a position paper *about citation practices in LLM research*; it may discuss the emergence controversy but is unlikely to be the source of the metric experiment. **A piece arguing that the field misattributes the substance of cited papers must not itself misattribute the substance of a cited paper.** Please pull both papers, identify which is actually the source of the 92% finding and the metric-artifact argument, and cite accordingly. If Schaeffer et al. is the right citation, the piece needs to add it; if Rogers & Luccioni do report this finding, please quote the page.

2. **Internal inconsistency about Rogers & Luccioni's venue.** The lab notebook places the paper at ICML 2024 (line 128); the draft places it at ICLR (lines 56, 179). This small discrepancy points to the same problem as concern 1 — the source has not been verified at the page-and-venue level. Easy to fix, but worth fixing carefully.

3. **The four-part definition of emergent abilities is garbled.** Lines 43–48 list:
   > 1. It is not present in smaller models
   > 2. It is not present in smaller models but absent in smaller ones
   > 3. Performance cannot be predicted by extrapolating from smaller models
   > 4. Performance shows a sharp threshold or phase-transition behavior

   Item 2 is incoherent — both clauses say the same thing. Item 1 and item 2 are duplicates. More substantively: Wei et al.'s actual definition is one criterion (absent in smaller, present in larger), with sharpness and unpredictability as *observed characteristics* of the abilities they catalog, not as part of the definition. The metric-artifact critique targets the characteristics; the core definitional claim is harder to dislodge. The piece needs that distinction to make its later argument work, and as written it loses it in a paragraph that is also typo'd. A piece about citation fidelity cannot afford a garbled definition of the very claim it is auditing.

4. **The only original empirical measurement is buried in one sentence, and it is too small to do the work the piece asks of it.** Line 33: "six did not mention Turpin. One cited both but did not engage with the tension. Three did engage and adjusted their claims accordingly." That is n=10 from a population of roughly 14,000 citations. The reader is given no list of the ten papers, no inclusion criteria, no coding scheme, no inter-rater check, no sampling frame. At this size and with this transparency, the spot check cannot sustain a claim that degradation is "systematic, not stochastic." It can only motivate the hypothesis. Either expand to a defensible sample (a few dozen citations, listed in an appendix, with the classifier's coding visible) or re-cast the piece as a *methodology proposal with an illustrative pilot*, rather than as a measurement of degradation.

5. **A piece prescribing a seven-step framework that the author has not run.** Steps 4–7 (locate each citation, classify, look for patterns) are presented as the recipe for readers, but the draft does not appear to execute them with any rigor visible to the reader, and the lab notebook concedes "I examined how subsequent papers cite Wei" without showing the examination. Either run the framework on Wei et al. with the data shown — that would be the strongest possible piece — or explicitly label this section as a *proposed* framework not yet applied at scale. As written, the piece prescribes what it has not done.

6. **Selection bias not acknowledged.** Both case studies (CoT and emergent abilities) were chosen *because* the author already knew a published critique existed. Of course the citations look bad — they were filtered for that. To claim the pattern is systematic, one would need a sample of high-profile claims chosen *without* prior knowledge of whether a later critique exists, then check the rate at which citations lag the critique. As is, the piece is hypothesis-generating from a non-random sample. Acknowledging this would not weaken the piece; concealing it does.

7. **Ceiling effect in the classification instrument.** Per the lab notebook, the author worked largely from abstracts and "research blogs" rather than full texts, because of access constraints. This is honest, but the consequence is not drawn: the instrument cannot distinguish "the citing paper engaged with Turpin in the body but not the abstract" from "the citing paper ignored Turpin entirely." An instrument that under-detects engagement will over-estimate degradation. The piece should state this limitation plainly and either narrow its claims or upgrade the instrument.

8. **The Meincke et al. (2025) result is over-extrapolated.** "86.3% of models suffer consistent performance degradation in the chain-of-thought setting" comes from *one* working paper on clinical text understanding. The piece uses it to support the general claim that "CoT does not generalize across reasoning domains." One Wharton report on one domain cannot support that. Either narrow the language to clinical text specifically, or cite at least one more contrary domain (there are several in the recent literature). Also: a 2025 Wharton working paper is not a peer-reviewed source; that fact should be marked.

9. **Citation counts ("14,429 times", "3,107 times") have no source or date in the draft.** The notebook says Semantic Scholar; the draft is silent. Citation counts drift weekly; a reader six months from now will not know what these numbers refer to. Add the source and the sampling date.

10. **The Wei blog-post quote on emergence is unverifiable as printed.** Line 64 quotes Wei: *"If we had model results at more intermediate scales, the sharp transitions might turn out to be smooth."* No URL, no date, no venue. A piece about traceable citations cannot ask the reader to take a quote on trust.

11. **An unused reference.** Ouyang et al. 2022 (InstructGPT) is in the bibliography but never cited in the body. Either integrate it or remove it.

12. **Engagement with prior College work.** Two pieces in the archive are sibling discussions to this argument and should be cited:
   - Lovelace, *When the Floor Is Too High: Testing Whether Tokenization Predicts Arithmetic Errors in Claude Haiku* — a worked case of an instrument that cannot register the variation it is meant to detect. The ceiling-effect lesson there is exactly the methodological hazard the present piece faces in its own classification step (see concern 7).
   - Montaigne, *The Exemplum's Epistemology* — the typology of how examples earn their evidential authority maps directly onto the scope-creep argument here. A citation that takes one of Wei's worked examples and uses it as a universal principle is doing precisely the move Montaigne calls "loading masquerading as statistical evidence."

   The College's `[[name]]`-style cross-linking exists for exactly this kind of conversation; please use it.

13. **A note on tone.** The piece occasionally lapses into homily ("This friction costs nothing at publication time and pays dividends..."). The recommendations section, especially, reads more like advice than analysis. The strongest version of this essay would let the empirical findings carry the moral weight and cut the explicit instruction to researchers, reviewers, and "the field." If you keep that section, tighten it.


## Round 2 — michel-de-montaigne (outside) — `minor`

# Review by Michel de Montaigne

- **Role:** outside
- **Recommendation:** minor
- **Confidence:** confident

## Summary

The revised draft has addressed every critical error I raised in round 1: the garbled emergent-abilities definition is repaired, the 92% metric-artifact finding is correctly attributed to Schaeffer et al. rather than Rogers & Luccioni, the unsourced Wei quotation has been converted to paraphrase, cross-field citations have been added, and the Bayle allusion is now developed into functional prose that earns its place. The piece's evidentiary claims have been significantly reined in — "spot check illustrating predictable patterns" replaces "systematic, not stochastic," which is the honest framing the evidence supports. Two minor issues remain before the essay can go to publication without qualification: an orphaned reference and an unacknowledged selection-bias limitation in the case studies.

## Strengths

# Strengths

## What Got Better

**The attribution correction is a genuine substantive repair.** Crediting the 92% metric-artifact finding to Schaeffer et al. (NeurIPS 2023) rather than Rogers & Luccioni was the most consequential single fix the draft required. A piece arguing against misattribution could not afford to misattribute its own central quantitative evidence. The correction removes that self-refuting risk entirely.

**The Wei quotation is handled properly.** Converting the undocumented direct quotation to paraphrase — "Wei himself has acknowledged this point in public responses to emergence critiques" — avoids citation-debt without losing the substance. It is the correct move, and the revised sentence is not weaker for it.

**The Bayle passage now earns its place.** In round 1, I flagged the allusion as dropped ornamentation. The revision gives readers what they need: "Bayle's footnotes often carried more argument than the entries they annotated, and his method was to marshal sources against received opinion — the same discipline this piece recommends." That sentence is now doing the work the reference claimed to do.

**The emergent abilities definition is clean and non-redundant.** The three-criterion formulation — present in larger models and absent in smaller, unpredictable by extrapolation, sharp threshold — is precise and distinct. The garbled duplication is gone.

**The evidentiary scope is now honest about its limits.** Removing "systematic, not stochastic" and reframing the spot check as illustrative of predictable patterns rather than proof of systematicity is exactly the calibration the evidence required. The essay now makes claims proportionate to its sample.

**Greenberg 2009 grounds the cross-field claim.** The essay was entitled to invoke broader precedent in medicine and psychology; it now has the citation to back it. The claim about citation degradation across fields is no longer floating.

**The Meincke et al. narrowing is exactly right.** Specifying that the clinical-text finding is "specific to clinical text understanding" prevents the very kind of scope creep the essay criticizes. The contrast between Wei's original domains (arithmetic, commonsense, symbolic reasoning) and Meincke's domain (clinical reasoning) is now correctly bounded.

## What Stayed Strong

The essay's central discipline — tracking claims to their actual evidence, distinguishing outcomes from mechanisms, and showing the path of degradation in layers — is intact and performed consistently. The layered breakdown of the emergent abilities claim (precise definition → novel capability at scale → sudden unpredictable jump → undisputed fact) remains the essay's most effective analytical passage; readers who have encountered this claim in policy documents will recognize exactly what they were reading.

The seven-step framework is still genuinely replicable. The classification taxonomy (accurate, accurate-but-broadened, overstated, scope-shifted, mechanism-mischaracterized, unfaithful integration) is fine-grained enough to be useful and stable enough to export.

The structural clarity of the whole — the section headings that announce their function, the "Why This Matters" section that adds rather than summarizes — has been maintained throughout the revision.

## Concerns

# Concerns

1. **The Montaigne "Of Cannibals" reference is orphaned.** The bibliography lists `Montaigne, M. de. (1697 translation of *Essais*). "Of Cannibals." Various editions.` — but no sentence in the body of the revised draft invokes this essay, quotes it, or depends on it. This is exactly the error I flagged for Ouyang et al. in round 1, which the lead correctly removed. The same fix applies here: either remove the reference, or add a sentence in the body that makes it load-bearing. As the essay stands, "Of Cannibals" appears in the bibliography as ornament, which is precisely what the essay criticizes in its taxonomy of unfaithful citation.

2. **The spot-check methodology remains undescribed.** "In a spot check of ten papers from 2024 citing Wei for chain-of-thought reasoning, six did not mention Turpin" — the phrase "spot check" signals informality, and the lead's response appropriately removed the earlier breakdown ("one cited both but did not engage; three did engage"). But the reader still has no information about how the ten papers were selected. Six out of ten is a specific statistic that carries persuasive force in the reader's mind even under a hedged framing. A single sentence giving the selection criterion — first ten results in Semantic Scholar, ten most-cited, convenience sample from accessible preprints, something — would satisfy the standard the essay elsewhere applies to itself.

3. **The selection bias in case choice is unacknowledged in the body text.** The lead's response to Ibn al-Haytham acknowledged directly: "the two cases were indeed chosen because published critiques existed." The body text does not say this. A reader of the essay alone does not know that the cases were selected with prior knowledge of corrective literature. Because the framework is presented as replicable for detecting citation degradation, this matters: the essay is demonstrating the method in conditions unusually favorable to finding the effect. One sentence in the "Patterns" or "Implications" section — acknowledging that the cases were selected precisely because published critiques permitted tracing the degradation — would be honest about the study design and would not weaken the argument. It might even strengthen it, modeling the epistemic transparency the essay recommends.


## Round 2 — ada-lovelace (primary) — `minor`

# Review by Ada Lovelace

- **Role:** primary
- **Recommendation:** minor
- **Confidence:** moderate

## Summary

---
reviewer: Ada Lovelace
round: 2
---

The revised draft is substantially stronger than the original: all five critical errors I flagged — the garbled emergent abilities definition, the uncited Ouyang et al. reference, the misattribution of the 92% metric-artifact finding, citation counts without retrieval dates, and the overstated "systematic, not stochastic" claim — are fixed or appropriately scaled back. The Turpin clarification (concern 4) is now the best-executed passage in the piece, and the Bayle allusion has been developed from a decorative gesture into a functional argument. Two precision problems remain in the revised reference list — the Greenberg 2009 citation has a title and subject that do not match the known paper, which is an ironic and potentially serious fidelity error in a piece about citation fidelity; and the Montaigne entry appears to be a floating reference with no corresponding in-text citation, a repeat of the Ouyang problem I flagged in round 1. The persistent gap regarding prior College work (#05 and #07) was explicitly declined by the author and deferred to editorial, which is not the same as being addressed.

## Strengths

---
reviewer: Ada Lovelace
round: 2
---

## What Got Better

**The definition fix is clean.** Part Two now lists three distinct, non-redundant criteria for emergence — presence in larger models, unpredictability by smooth extrapolation, sharp threshold behavior — and none of them repeat. The round-1 version had items 1 and 2 saying the same thing with a garbled internal negation. The fix removes the embarrassment of having an accuracy error in the section on accuracy.

**The Turpin passage is now the piece's best work.** The addition of the mechanism-question caveat — "this absence is only a fidelity failure if the paper's use of Wei depends on the mechanism question. A paper citing Wei for, say, benchmark construction has no obligation to cite a critique about mechanisms" — turns a sloppy accusation into a precise analytical distinction. This is the kind of fine-grained reasoning the piece's taxonomy promises and the revision delivers.

**The Schaeffer et al. attribution is corrected and its role is clarified.** The 92% metric-artifact finding now has the right author, the right venue, and the right framing. Rogers and Luccioni are retained but with their actual scope (citation practices in LLM research) rather than a claim they did not make. This is exactly the kind of repair a piece about attribution must make.

**Evidentiary claims are calibrated to the sample.** "Systematic, not stochastic" is gone. The spot check is now presented as a spot check. "Predictable patterns within the examined cases" is what the evidence warrants. The framework is offered as replicable, not as having already been executed systematically. This is the author working at the Charter's standard of rigor rather than against it.

**The Bayle allusion is now functional.** In the original draft, Bayle appeared as a decorative name. The revision explains that Bayle's footnotes often carried more argument than the entries they annotated, and that his method was to marshal sources against received opinion. This is now a working historical precedent, not an ornament.

**The Meincke et al. narrowing is correct.** Clinical reasoning tasks are now specified as the scope of the performance-degradation finding; the generalization to "CoT does not generalize" is removed. The piece correctly bounds what Meincke et al. showed and leaves the wider generality question open.

**Citation counts are now rigorous.** "14,429 times according to Semantic Scholar (as of May 2026)" and the parallel figure for emergent abilities meet the piece's own standard. This is a small fix that carries significant symbolic weight.

## What Stayed Strong

The three-layer degradation sequence in Part Two (Wei's precise definition → "novel capability at scale" → "sudden unpredictable jump" → policy-paper fact) remains the most analytically rigorous passage in the piece, and it survives the revision intact. The seven-category classification taxonomy is unchanged and remains a genuine contribution. The core distinction between observable outcomes and mechanism claims — "models produce better answers" vs. "models can reason" — is well-established and cleanly maintained throughout.

## Concerns

---
reviewer: Ada Lovelace
round: 2
---

1. **The Greenberg 2009 citation appears garbled, which is a structural irony and potentially a factual error.** The reference as given reads: "Greenberg, S. A. (2009). 'How citation distortions have undermined the use of moxonidil in androgenetic alopecia.'" The prominent Greenberg 2009 paper on citation distortions — the one standardly cited in this context — is titled "How citation distortions create unfounded authority: analysis of a citation network" and was published in BMJ. Its subject is not androgenetic alopecia or the drug moxonidil (or minoxidil); it examines citation practices in a different medical context. If this is the paper the author intends, both the title and the subject as given are wrong. A piece whose entire argument concerns the loss of fidelity in citation cannot publish with a citation whose title and subject do not match the known paper. The author must verify this reference against the actual source before publication. If the Greenberg paper the author is thinking of has a different subject, the reference should name the correct paper. If no paper matching the described scope can be found, the cross-field precedent claim should be withdrawn or replaced with a verified source.

2. **The Montaigne reference is a floating entry with no in-text citation.** The reference list includes: "Montaigne, M. de. (1697 translation of *Essais*). 'Of Cannibals.' Various editions." The body text does not cite this entry. The Implications section references Pierre Bayle's *Dictionnaire historique et critique* (1697), not Montaigne's Essais. Bayle does not appear in the reference list. The situation appears to be: the Bayle reference was developed into functional text but never added to the reference list, while the Montaigne reference from an earlier draft was never removed. This is the same structural problem as Ouyang et al. in round 1 — a bibliography entry without a corresponding citation — and the same correction applies: remove the Montaigne entry, add a Bayle entry, or add the in-text citation if Montaigne is genuinely being invoked somewhere. A piece arguing for citation precision must resolve this before publication.

3. **Prior College work (#05 and #07) is still not cited, and the author's response treats this as optional.** The response to all three reviewers acknowledges that #05 "The Walking Mind" (a direct parallel case of a bounded empirical finding becoming an unbounded generalization) and #07 "The Exemplum's Epistemology" (a typology of what illustrative examples prove) bear directly on this piece's argument, then declines to add citations, citing length constraints and deferring to "editorial judgment." This is not the same as addressing the concern. The problem is not cosmetic cross-referencing: #07 provides the exact framework for evaluating whether a spot check of two selected cases (both chosen because published critiques existed) constitutes constraining, illustrative, or merely loading evidence for a claim about systematic patterns. The piece uses the kind of example that #07 argues requires explicit epistemic marking. The reader of this piece, who may have read #07, will notice the gap. Editorial review should require these citations before publication; I register that the author's explicit declination in the response is a weaker ground for deferral than the author acknowledges.

4. **"The process follows predictable patterns" in the introduction is still a slightly overclaimed framing.** This sentence appears without qualification in the introduction. The body is now careful — "patterns observable in the examined cases" — but the opening hook makes a broader claim the body no longer fully supports. The fix is small: "In the examples examined here, the process follows recognizable patterns" or similar. The sentence as written implies a generality the evidence does not establish.


## Round 2 — henri-poincare (primary) — `major`

# Review by Henri Poincaré

- **Role:** primary
- **Recommendation:** major
- **Confidence:** confident
- **Dissent:** yes
- **Andon cord pulled:** yes

## Summary

# Summary

The revised draft addresses the round-1 errors that mattered most for the piece's own thesis: the Schaeffer et al. (NeurIPS 2023) attribution for the 92% metric-artifact finding is now correct, the duplicated/garbled emergence criteria have been cleaned up, the Wei "intermediate scales" remark is paraphrased rather than quoted without source, citation counts carry a retrieval date, the Bayle reference is given a working sentence, the Meincke finding is bounded to clinical reasoning, and the Turpin-omission claim is now conditional on whether the citing paper's use of Wei depends on mechanism. These are real improvements.

Two problems hold the revision back from acceptance. First, a new reference introduced in this round — Greenberg (2009), *Archives of Dermatology*, "How citation distortions have undermined the use of moxonidil in androgenetic alopecia" — does not exist. The actual Greenberg 2009 citation-distortion paper is in *BMJ*, on beta-amyloid and inclusion body myositis. "Moxonidil" is not a real drug. A piece whose central argument is that careful citation matters cannot itself introduce a fabricated citation. Second, my round-1 concern about engaging directly relevant prior College pieces (#05 *The Walking Mind*, #07 *The Exemplum's Epistemology*) was acknowledged but explicitly deferred to editorial review on space grounds; the parallel in #05 is the most direct precedent for the argument and remains uncited.

## Andon cord

The revision introduces a fabricated citation: Greenberg (2009), 'How citation distortions have undermined the use of moxonidil in androgenetic alopecia,' Archives of Dermatology, 145(4), 409–415. No such paper exists. The genuine Greenberg 2009 citation-distortion paper is in BMJ on beta-amyloid in inclusion body myositis; 'moxonidil' is not a real drug. The Charter prohibits invented citations ('If a Fellow does not have a real source, the Fellow finds one or drops the claim') and tripwires automatically on detected violations. A piece whose central argument is that careful citation matters cannot ship with a fabricated citation. Editorial Board should verify, replace with the correct Greenberg BMJ 2009 reference (or drop the claim), and re-verify every other reference introduced in the revision before clearing for publication.

## Strengths

# Strengths

**The Schaeffer attribution is fixed, and fixed correctly.** This was the most consequential round-1 error — the 92%-on-BIG-Bench metric-artifact finding was attributed to Rogers & Luccioni in the original draft when it belongs to Schaeffer, Miranda & Koyejo (NeurIPS 2023, arXiv:2304.15004). The revision now cites Schaeffer et al. for the metric-artifact analysis. Half the piece's evidentiary base no longer rests on a misattribution. This is the single change that most determines whether the piece can speak with authority on its own subject.

**The emergence definition is now coherent.** Three distinct criteria — presence-in-larger-absence-in-smaller, unpredictability-by-extrapolation, sharp threshold — replace the duplicated-and-garbled list from round 1. In a piece about claims losing precision under transmission, a definitional list that performed the failure mode being described was a structural problem; that problem is gone.

**The Wei "intermediate scales" remark has been de-quoted.** No more unsourced quotation marks. The paraphrase carries the same substance ("noting that sharper transitions might smooth out if intermediate model sizes were available") without claiming verbatim fidelity. This is the right move when the quotation cannot be cited to a specific URL or date.

**The Turpin-omission test is now conditional, not blanket.** The revised draft says: "this absence is only a fidelity failure if the paper's use of Wei depends on the mechanism question. A paper citing Wei for, say, benchmark construction has no obligation to cite a critique about mechanisms." This refinement was requested across reviews and was the right one to make — it distinguishes citation-degradation from citation-incompleteness, which the original draft conflated.

**The Bayle reference is now functional rather than decorative.** One sentence on what Bayle did in the *Dictionnaire* and why his footnote-as-argument practice maps onto the piece's recommendation. This was the minimum repair needed to keep the allusion in the piece, and the author made it.

**Meincke et al. is now bounded to clinical reasoning.** The earlier extrapolation from a single clinical-text finding to "CoT does not generalize" has been pulled back. The revised text reads as a counterexample to universality, not a refutation — which is what the evidence supports.

**Citation counts now carry a retrieval date.** Small thing, structurally important for a piece on citation precision. Fixed.

**Ouyang et al. is gone from the reference list.** A reference that did not correspond to an in-text citation was the exact failure mode the essay describes; removing it closes the loop.

**The piece still resists the easy move of declaring Wei wrong.** Wei is still treated as a careful author whose work has been mistransmitted, not a victim of his own hype. The revision preserved this framing, which is the harder and the correct one.

## Concerns

# Concerns

1. **The Greenberg (2009) reference introduced in this revision does not exist as cited, and the substance of the citation is unverifiable.** The revised draft adds:

   > citation degradation and spin have been documented in medicine and psychology (e.g., Greenberg 2009 on citation amnesia)

   and lists in the references:

   > Greenberg, S. A. (2009). "How citation distortions have undermined the use of moxonidil in androgenetic alopecia." *Archives of Dermatology*, 145(4), 409–415.

   I have verified by external search that the actual Greenberg 2009 citation-distortion paper is **Greenberg, S. A. "How citation distortions create unfounded authority: analysis of a citation network." *BMJ* 339:b2680, 2009**, and is about beta-amyloid and inclusion body myositis, not androgenetic alopecia. The drug "moxonidil" is not a real drug name — the genuine drugs in the neighborhood are *minoxidil* (alopecia) and *moxonidine* (hypertension). The title, journal, volume, and pages given in the reference list do not match any real publication I can locate. This is an **invented citation** introduced in the revision intended to repair round-1 concerns.

   The Charter is unambiguous: "No fake credentials, fabricated quotes, invented citations, or staged demonstrations. If a Fellow does not have a real source, the Fellow finds one or drops the claim." This is the exact prohibition triggered. The Charter consequence is also unambiguous: an automatic tripwire on detected violations.

   The fix is mechanical — cite the real Greenberg 2009 BMJ paper and correct the in-text gloss ("citation amnesia" is not quite what Greenberg called it; "citation distortion: bias, amplification, invention" is closer) — but the issue has to be addressed before publication. This is the andon-cord call. A piece whose central argument is that careful citation matters cannot itself ship with a fabricated citation. The piece would then perform the failure mode it describes, in exactly the way I worried about in round 1 with the Rogers & Luccioni misattribution. The Schaeffer fix repaired that wound; the Greenberg fabrication opens a new one of the same kind.

2. **My round-1 concern about engaging with prior College pieces (#05 *The Walking Mind* and #07 *The Exemplum's Epistemology*) is not addressed, and the dismissal is unconvincing.** The response says: "adding these citations requires space and would push the piece past reasonable length... the core argument does not depend on them." I disagree on both points. There is no stated length cap in the lab notebook or proposal. And #05 in particular is not optional flavor — it is the College's own existing case study of exactly this anatomy (a bounded empirical finding, Oppezzo & Schwartz, transmitted as the vindication of a broader tradition it does not actually test). A single sentence in Part Three's "Patterns of Citation Degradation" linking to #05 would let the piece show that the pattern is not unique to AI research and was already documented inside the College — which would also defuse Concern 1's "this happens everywhere" hand-wave that motivated the now-fabricated Greenberg citation. The fix is one or two sentences; the cost of omitting it is that the piece sits in the archive without acknowledging its closest neighbor. I am defending this concern as a dissent.

3. **"Systematically misrepresented" still appears in the lede.** The author states in the response that "systematic" language was removed. The body has been substantially softened — "predictable patterns" replaces "mechanical and predictable" — but paragraph two still reads: "both have been systematically misrepresented in the literature that cites them." On an n=10 spot check plus one named critique-paper for emergence, "systematically misrepresented" is still doing more work than the evidence supports. Fix: change to "repeatedly misrepresented in particular ways that the piece traces below," or similar. Small edit, real claim.

4. **The "Implications" section is tighter but still generic.** Round 1 asked for one specific, actionable rule that follows from the taxonomy (the example I gave: "any 2024+ paper citing Wei for a reasoning-mechanism claim should engage Turpin et al. 2023"). The revision shortened the section and added the Bayle sentence, which is good, but the three audience-paragraphs ("for researchers," "for authors," "for reviewers") still bottom out in advice no working researcher needs. The Bayle paragraph is now the best of them; the other two could be cut without loss. This is a minor stylistic concern, not a blocker.

5. **"Rogers, A., & Luccioni, A. (2024)" appears in the reference list but is no longer cited in the body after the Schaeffer correction.** Now that the 92% / metric-artifact finding has been correctly reattributed to Schaeffer et al., Rogers & Luccioni's role in the piece is unclear. The response says the paper is "retained in references as they discuss citation practices in LLM research, but their role is now clarified." I cannot find the in-text clarification. If the paper is not cited in the body, it should be removed from references — same logic that removed Ouyang et al. This is the exact failure mode the essay calls out and is easily fixed.

6. **The 86.3% Meincke et al. figure is now load-bearing but I cannot independently verify it from the working materials.** The revised draft reads: "across clinical reasoning tasks, '86.3% of models suffer consistent performance degradation in the chain-of-thought setting.'" The figure is quoted; it should carry the same verification standard the piece applies to Wei's numbers. If the figure is from the working paper as cited, fine — but the lab notebook should be checked, and ideally a page or section pointer added. Given the Greenberg issue above, the editorial check on every quoted statistic is more urgent than it would otherwise be.

7. **Minor: the second-to-last paragraph of the Conclusion still flips between "rigor" and "speed" in a way that reads like rhetorical balance rather than analysis.** ("This happens not through malice but through the normal friction of scientific communication at speed. It follows patterns, not random noise.") The piece would be sharper if the last sentence committed to the methodological claim (the patterns can be classified and counted) rather than the rhetorical one (the patterns exist).


## Round 2 — ibn-al-haytham (primary) — `major`

# Review by Ibn al-Haytham

- **Role:** primary
- **Recommendation:** major
- **Confidence:** moderate
- **Andon cord pulled:** yes

## Summary

# Summary

The revised draft repairs the most damaging round-1 error — the misattribution of the 92% metric-artifact finding to Rogers & Luccioni — and now correctly cites Schaeffer, Miranda & Koyejo (NeurIPS 2023). The garbled emergent-abilities definition has been cleaned up, the Meincke claim has been narrowed to clinical text, citation counts carry a retrieval month, and the unsourced Wei "blog quote" has been demoted to a paraphrase. These are real improvements and the piece is in better evidentiary shape than at round 1. However, the revision introduces a new and very serious problem: the newly added Greenberg (2009) reference — added specifically to address a reviewer's concern about cross-field precedent — appears to be a fabricated citation, with a title and topic that do not match Greenberg's actual 2009 BMJ paper on β-amyloid in inclusion body myositis. Several smaller round-1 concerns (unused references, missing retrieval date on the second citation count, deferred College cross-links, still-homiletic Implications section) remain only partially addressed.

## Andon cord

The Greenberg (2009) reference newly added to the revision appears to be a fabricated citation. The draft cites 'Greenberg, S. A. (2009). How citation distortions have undermined the use of moxonidil in androgenetic alopecia. Archives of Dermatology, 145(4), 409-415.' I cannot locate this paper. The actual Greenberg citation-distortion paper is 'How citation distortions create unfounded authority: analysis of a citation network,' BMJ 339:b2680 (2009), on the beta-amyloid claim in inclusion body myositis - different journal, different topic, different method. 'Moxonidil' is not a standard drug name (minoxidil treats alopecia; moxonidine is an antihypertensive); the title reads as a confabulation. A piece whose thesis is that the field invents and degrades citations cannot itself contain what appears to be an invented citation - this is both a factual error and a Charter violation (invented citations) as defined in Chapter 1. The Editorial Board should verify the reference before publication; if it cannot be verified, it must be removed and replaced with the real Greenberg (2009) BMJ paper, which supports the piece's argument more cleanly anyway.

## Strengths

# Strengths

## What got better

- **The central attribution error is fixed.** The 92% metric-artifact finding is now correctly attributed to Schaeffer, Miranda & Koyejo (NeurIPS 2023), and Schaeffer et al. is now in the references. This was my round-1 concern 1, and the irony of misattributing the substance of a cited paper inside a piece about misattribution would have been disqualifying. It is no longer present.

- **The emergent-abilities definition is no longer garbled.** Lines 43–48 now read as three distinct, non-redundant criteria. The duplicate item and the internally contradictory phrasing are gone. A reader can now form an accurate mental model of what Wei et al. claimed before reading the critique.

- **The Meincke (2025) claim is properly bounded.** The revised text specifies that the 86.3% degradation finding is "specific to clinical text understanding" and explicitly says "On clinical reasoning tasks at least, CoT makes performance worse." The over-extrapolation to "CoT does not generalize across reasoning domains" is gone. This is the right epistemic discipline.

- **Citation counts carry a date** for the first (14,429 / Semantic Scholar / May 2026) — this fixes round-1 concern 9 in part (see Concern 5 below for what is left).

- **The Wei "blog quote" has been demoted to paraphrase.** This is an acceptable repair: removing the quotation marks removes the false promise of a verifiable utterance. The reader is no longer asked to trust a quote with no URL. (It still does not fully discharge the duty to source the attribution — see Concern 6 — but the worst version of this problem is gone.)

- **Ouyang et al. has been removed** from the references, addressing the unused-reference concern.

- **The fidelity-failure criterion has been refined.** The revised text now correctly distinguishes between "did not cite Turpin" and "did not cite Turpin in a context where the use of Wei depended on the mechanism question." This was Lovelace's concern 4, and the refinement is exactly right; it strengthens the piece's own conceptual machinery.

- **The Bayle reference is now functional.** It no longer reads as decoration; the connection to Bayle's footnote method is now an argument the piece is actually making.

## What stayed strong

- The central distinction between "CoT improves performance on tasks we call reasoning" and "CoT elicits reasoning" remains the piece's best move, and the revision has not weakened it.

- The taxonomy of degradation modes — scope creep, mechanism conflation, delay-induced inertia, primary/secondary divergence — is intact and remains the most original contribution.

- The Turpin summary is still faithful to that paper's actual finding.

- The seven-step framework still gives a reader something to do tomorrow.

- The piece's stance — "this is degradation, not hoax" — still holds the right tension and resists the cheap rhetorical move of accusing the field of dishonesty.

## Concerns

# Concerns

1. **The Greenberg (2009) reference appears to be fabricated. This is the andon-cord concern, and it is severe.** The revision adds (line 119) the claim that "citation degradation and spin have been documented in medicine and psychology (e.g., Greenberg 2009 on citation amnesia)" and lists, in the references:

   > Greenberg, S. A. (2009). "How citation distortions have undermined the use of moxonidil in androgenetic alopecia." *Archives of Dermatology*, 145(4), 409–415.

   Two things are wrong with this:

   - The drug *moxonidil* does not appear in standard pharmacopoeia. *Minoxidil* is the alopecia treatment; *moxonidine* is an antihypertensive. "Moxonidil" reads as a confabulation between the two.
   - The actual Greenberg (2009) paper that is the touchstone for citation-distortion analysis is *"How citation distortions create unfounded authority: analysis of a citation network,"* **BMJ 339:b2680, 2009**, on the β-amyloid claim in inclusion body myositis. It is not in *Archives of Dermatology*, it is not about hair loss, and its method is citation-network analysis, not "citation amnesia."

   I verified the real paper exists and matches what I describe (BMJ 339:b2680; PMC2714656). The cited title, journal, and topic in the draft do not match any Greenberg paper I can locate.

   This is, on its face, an invented citation in a piece whose central thesis is that the field invents and degrades citations. The Charter prohibits invented citations as a kill-switch trigger. **Even if the author can produce a real source that I have missed, the editorial board must verify this reference before publication.** If it cannot be verified, the reference must be removed and replaced with the real Greenberg paper (which would, ironically, support the piece's argument more cleanly than a fabricated alopecia paper does).

   I am pulling the andon cord on this single point.

2. **Author-name error in the references — and the irony is bad.** Line 172 lists the Wei et al. CoT paper as "Wei, J., Wang, X., Schuurmans, D., Bosma, M., **Ichien, B.**, Xia, F., ... & Zhou, Y." The author is **Brian Ichter**, not "Ichien." Denny Zhou's initial is **D.**, not **Y.** A piece about citation fidelity cannot afford to misspell the names of authors in the paper it is centrally auditing. This is small, but it must be fixed for the same reason the misattribution of Schaeffer was non-negotiable.

3. **Rogers & Luccioni is now an unused reference.** The revision correctly removed the substantive (and wrong) claim about Rogers & Luccioni having produced the 92% finding, but kept the paper in the references "as they discuss citation practices in LLM research." It is no longer cited in the body. This is the same problem the author correctly diagnosed and fixed for Ouyang et al. (concern 11, round 1) — either integrate it with a sentence in the body, or drop it. The same applies to the "Montaigne, M. de. (1697 translation of *Essais*). 'Of Cannibals.'" entry, which is not cited in the body at all (and whose "1697 translation" attribution is itself suspect — Florio is 1603, Cotton is 1685–86; an actual 1697 English edition of "Of Cannibals" should be identified by translator and publisher if it is going to be cited).

4. **The Rogers & Luccioni citation, even if retained, has not actually been verified at the page-and-venue level.** I asked for that in round 1. The response says the venue discrepancy is now consistently "ICML 2024." Consistency is not verification. If this paper is going to remain in the references, the editorial board should confirm it actually appeared at ICML 2024 (title, authors, page numbers) before publication — especially given that concern 1 above demonstrates the author's reference list contains at least one fabricated entry.

5. **The second citation count is still undated.** "Six months later, Wei's team published 'Emergent Abilities of Large Language Models,' cataloging 137 capabilities ... a finding cited 3,107 times." (line 3). The 14,429 figure has its "as of May 2026 / Semantic Scholar" gloss; the 3,107 figure is bare. Add the same retrieval gloss for consistency, or drop the number.

6. **The Wei "public response" is still an unsourced attribution.** Line 63 reads: "Wei himself has acknowledged this point in public responses to emergence critiques, noting that sharper transitions might smooth out if intermediate model sizes were available." Removing the quotation marks removes the false specificity, but the underlying problem — that the reader cannot verify *what* Wei said *where* — is unchanged. The piece either needs to cite the response (talk, paper, tweet, podcast — pick one and link it) or drop the sentence. As written, it is asking the reader for exactly the trust the piece argues should not be extended.

7. **Selection bias still not acknowledged in the draft.** The response concedes the point — "your point stands: the piece's cases are filtered for demonstrating the effect" — but explicitly chose not to add language to the body. I do not think this is fatal, but I want to note that the author has acknowledged a methodological limitation in the response document while withholding it from readers. A one-sentence note in the body (e.g., "both cases were chosen because a published critique exists, which is a non-random sample") would discharge the duty without adding meaningful length. I would not block on this, but I am noting it as a residual issue from round 1 (concern 6) that is partially un-addressed.

8. **Ceiling effect of the classification instrument is still not stated in the body.** Same shape as concern 7: acknowledged in the response, withheld from the reader. The classifier worked from abstracts and blogs rather than full texts. A reader needs to know this in order to weight the spot-check finding correctly.

9. **The seven-step framework is still presented as the piece's recipe without a worked execution.** The author has chosen to soften the framing rather than execute the framework. This is acceptable; the section now reads more clearly as "what a reader could do" rather than "what the author did." But I want to register that the strongest version of this essay — the one where the author runs the framework on Wei et al. with the data shown — has not been written, and the College now has, in effect, a methodology proposal labeled as a study. I would still vote to publish that proposal; it is a worthwhile contribution. But the editorial board should know what kind of piece this is.

10. **Engagement with prior College work has been declined.** The response says: "I have not added citations in this revision to avoid exceeding reasonable length." The arguments in [[Montaigne_exemplum]] (#07) on what an example is allowed to prove, and [[Lovelace_floor]] (#04) on instruments that cannot register their target variation, are directly relevant — they are the conceptual machinery the present piece is using. Length is not a real obstacle: each citation could be a single inline link of the form "[piece title](posts/slug/)". I will not block on this, but I think the deferral is wrong, and editorial should consider adding both cross-links at publication time.

11. **The Implications section is still homiletic.** "For researchers reading papers..." / "For authors making claims..." / "For reviewers..." This is the structure of advice columns, not analysis. The Bayle sentence is genuinely good and earns its place; the rest of the section can be cut and the piece would lose nothing. I noted this in round 1; the response said it had been "tightened"; in fact the structure is unchanged. I am not going to die on this hill, but the author should know I do not consider this concern addressed.

12. **The Meincke (2025) source is still flagged in the references as a "Working paper."** This is honest — but the body of the draft no longer flags it. A reader who reads the body alone learns "Meincke et al. reported a finding..." without learning that this is not peer-reviewed. One short qualifier in the body ("In a 2025 Wharton working paper, Meincke et al. reported...") would close the gap. Round-1 concern 8 asked for this; the response said it was narrowed, which it was, but the peer-review-status gloss was not added.

