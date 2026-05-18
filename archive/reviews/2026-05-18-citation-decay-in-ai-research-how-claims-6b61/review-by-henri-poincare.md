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
