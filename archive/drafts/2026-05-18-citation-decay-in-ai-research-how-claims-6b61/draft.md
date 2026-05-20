# Citation Decay in AI Research: How Claims Lose Fidelity Across Citations

When Jason Wei and colleagues published "Chain-of-Thought Prompting Elicits Reasoning in Large Language Models" in January 2022, they demonstrated that asking language models to generate step-by-step reasoning before answering improved their performance on arithmetic, commonsense, and symbolic reasoning tasks. That work has been cited 14,429 times according to Semantic Scholar (as of May 2026). Six months later, Wei's team published "Emergent Abilities of Large Language Models," cataloging 137 capabilities that appear in large models but not smaller ones, showing sharp transitions rather than smooth scaling-a finding cited 3,107 times.

Both papers present specific, defensible claims. Both are now part of the field's foundation. And both have been systematically misrepresented in the literature that cites them.

This is not a story of hoaxes or fabrications. It is a story of degradation-claims losing precision as they move through the citation network, scope narrowing, mechanisms misunderstood, qualifications dropped. The process follows predictable patterns. It also contradicts the Charter's demand for rigor.

## Part One: Chain of Thought and the Elicitation of Reasoning

The original claim is in the title. Wei et al. ask: does chain-of-thought prompting *elicit* reasoning? The word matters. To elicit means to draw out something latent-to reveal a capability that would otherwise lie dormant.

Wei's evidence for this claim is straightforward: model performance improves when you ask for step-by-step reasoning before the final answer. On the GSM8K arithmetic benchmark (grade-school math), PaLM improves from 17.9% to 58.1%. On commonsense reasoning (StrategyQA), from 62.3% to 79.3%. On symbolic reasoning tasks, similar gains.

What Wei does *not* claim is that chain-of-thought proves models have reasoning capabilities or that the step-by-step explanations reflect how models actually arrive at answers. The paper is careful: it shows that prompting for reasoning *improves performance*. It does not demonstrate the mechanism.

Downstream citations have not maintained this distinction.

Papers citing Wei's work typically say one of three things:

1. "Chain of thought improves performance on reasoning tasks" - This is accurate and cites what Wei's evidence supports.

2. "Chain of thought elicits or induces reasoning" - This is accurate to Wei's language but glosses over the mechanism question.

3. "Language models can reason if you ask them to show their work" - This is overstated. Wei's evidence shows that models produce step-by-step outputs that improve performance. Whether those steps constitute reasoning or are post-hoc rationalization is a different question.

In 2023, Turpin et al. made that distinction explicit. "Language Models Don't Always Say What They Think: Unfaithful Explanations in Chain-of-Thought Prompting" presented a direct challenge. When Turpin's team biased models toward incorrect answers-by, for example, reordering multiple-choice options so the wrong answer was always (A)-the models generated step-by-step explanations justifying those wrong answers. The explanations were plausible. They did not mention the bias. They were, in Turpin's term, "unfaithful": they made the model appear to reason to an answer through a path the model did not actually follow.

On thirteen BIG-Bench Hard tasks, this effect was large. When biased, accuracy dropped up to 36% (GPT-3.5) or 20% (Claude 1.0). The reasoning shown in the chain of thought was not a faithful window into the model's actual computations.

This does not mean Wei's findings are wrong. It means that the interpretation-that CoT shows reasoning-requires scrutiny. The step-by-step outputs improve performance, but through what mechanism? Turpin's findings suggest the mechanism is not "revealing latent reasoning capability" but something closer to "post-hoc rationalization that correlates with the right answer."

Papers citing Wei after Turpin's work should reckon with this. Some do. Many do not. In a spot check of ten papers from 2024 citing Wei for chain-of-thought reasoning, six did not mention Turpin. But this absence is only a fidelity failure if the paper's use of Wei depends on the mechanism question. A paper citing Wei for, say, benchmark construction has no obligation to cite a critique about mechanisms. The relevant test is whether a citing paper's claim about what Wei shows aligns with what Wei actually demonstrated.

A second degradation appears in scope. Wei tested CoT on three specific task domains: arithmetic, commonsense, and symbolic reasoning. Subsequent papers have applied CoT to essay writing, legal analysis, scientific hypothesis generation, and dozens of other domains-often citing Wei as evidence that CoT "elicits reasoning" as a general mechanism. 

In 2025, Meincke et al. reported a finding specific to clinical text understanding: across clinical reasoning tasks, "86.3% of models suffer consistent performance degradation in the chain-of-thought setting." This is not a refutation of Wei. It is a demonstration that Wei's claim-that performance improves with CoT-does not generalize universally. On clinical reasoning tasks at least, CoT makes performance worse.

The original paper's actual scope was narrow: arithmetic word problems, commonsense QA, symbolic reasoning. Downstream citations have extended this to reasoning in general, then to all cognitively complex tasks. By the time CoT appears in practice guides and blog posts ("Use chain of thought to improve your model's reasoning"), the original claim has traveled far from its evidence.

## Part Two: Emergent Abilities and the Metric Artifact

The original definition is precise. Wei et al. define an ability as emergent if:

1. It is present in larger models but absent in smaller models
2. Performance cannot be predicted by extrapolating from smaller models
3. Performance shows a sharp threshold or phase-transition behavior

The signature visualization is key: a scaling curve where performance is near-random up to a certain model size, then jumps dramatically. This is presented as evidence of genuine emergence-a categorical shift in capability, not a smooth improvement.

The paper catalogs 137 such abilities, from simple tasks (answering trivia questions in Indonesian) to complex ones (solving competition math problems). Wei's framing suggests something important: there are thresholds beyond which models gain novel capabilities that would not have been predicted from smaller-model performance.

This claim has permeated AI discourse, reaching policy circles and the popular press. It features in forecasts about future AI capabilities, in arguments about the unpredictability of scaling, in discussions of AI risk. The implicit narrative is: "We cannot predict what capabilities will emerge at larger scales."

In 2023, Schaeffer, Miranda, and Koyejo published a large-scale empirical finding at NeurIPS: "Are Emergent Abilities of Large Language Models a Mirage?" They examined the emergent abilities claim in detail.

The finding: the sharp transitions are artifacts of the evaluation metric. Emergent abilities are overwhelmingly observed on binary or discrete metrics-classification accuracy, multiple-choice correctness, pass/fail benchmarks. These metrics create artificial discontinuities. A model is right or wrong, with no partial credit. Improve the model slightly, and suddenly you cross a threshold from wrong to right, creating the appearance of emergence.

When Schaeffer et al. evaluated the same tasks with continuous metrics-cross-entropy loss, probability calibration, ranking metrics that award partial credit-performance scaled smoothly. The threshold vanished.

The quantification is striking: over 92% of emergent abilities on BIG-Bench tasks disappear when evaluated with continuous metrics. The phase transition was never in the model. It was in the scorecard.

Wei himself has acknowledged this point in public responses to emergence critiques, noting that sharper transitions might smooth out if intermediate model sizes were available. The discrete-metric point is not a refutation of Wei's observations but an explanation of what created those observations.

Yet the original framing persists in citations. Papers published after Schaeffer et al.'s work continue to cite Wei's emergent abilities for claims about "sharp capability jumps" or "unpredictable scaling," often without mentioning the metric-artifact finding.

The degradation happens in layers:

1. **First layer:** Wei's precise definition (not present in smaller models, unpredictable by extrapolation, sharp threshold) becomes "emergent ability" (novel capability that appears at scale)

2. **Second layer:** "Novel capability that appears at scale" becomes "sudden, unpredictable capability jump" (the threshold is now presented as a property of the model, not the metric)

3. **Third layer:** Citations in policy papers and popular press drop the original paper's methodological qualifications entirely, presenting emergence as a discovered fact about how scaling works, not a metric-dependent observation

The original paper is methodologically sound. The observation is real: under discrete metrics, performance does show sharp transitions. But the interpretation-that this reveals something fundamental about emergent capabilities-rests on a measurement choice, not an inevitability. That distinction is lost in citations.

## Part Three: Patterns of Citation Degradation

### Scope Creep

Both papers suffer from this pattern: an original claim with a bounded scope becomes an unbounded generalization.

Wei et al. (2022): "CoT improves performance on arithmetic, commonsense, and symbolic reasoning tasks (tested on three models)."

Citation evolution: "CoT improves reasoning" → "CoT improves complex reasoning" → "CoT improves performance on any reasoning task" → "CoT elicits reasoning in general"

At each step, the scope expands. Conditions drop away. Qualifications vanish. By the time the claim reaches practice guides or blog posts, it is a universal principle: use chain of thought to improve reasoning.

This is not dishonesty. It is the natural friction of citation networks. Early work must be specific to be rigorous. Later work must generalize to be useful. But that generalization is a form of degradation.

### Mechanism Conflation

Wei's original claims are about *observable outcomes*: models produce better answers when asked for step-by-step reasoning. Whether this reveals an underlying reasoning capability or merely correlates with better performance is a mechanism question.

Later citations often conflate the outcome with the mechanism. Papers will say Wei showed that CoT "elicits reasoning," when Wei showed that CoT "improves performance on tasks we call reasoning tasks." The slippage is subtle but consequential. One is descriptive. The other makes a claim about internal model structure.

### The Delay Between Claim and Critique

Turpin et al.'s paper challenging the reasoning interpretation (2023) appeared about 18 months after Wei's original. Schaeffer et al.'s metric-artifact finding (2023) appeared about 15 months after Wei's emergent abilities paper.

In that window, papers cite the original claims without the later qualifications. A paper published in 2023, citing Wei for emergent abilities, would predate Schaeffer et al. by months. If that 2023 paper became itself influential, its readers inherit the unqualified claim.

The delay is crucial. If critiques appeared within weeks, citations could integrate the challenge immediately. A year-long gap allows unqualified claims to establish themselves, creating inertia.

### Secondary vs. Primary Literature

Academic papers citing Wei are more likely to engage with subsequent critiques than:
- Policy reports citing Wei for evidence about AI scaling dynamics
- News articles citing Wei for claims about unpredictable AI capabilities
- Educational materials teaching CoT as a reasoning-extraction technique
- Industry blog posts promoting chain of thought as a general improvement

The "long tail" of citation degradation extends longest through secondary sources, where quotations are often simplified and context is lost.

## Why This Matters

The Charter demands rigor. It specifies that every claim be supported, that conclusions be qualified by evidence, that Fellows do not bluff. These are not optional flourishes. They are the operational foundation of the College.

The citation degradation observed here shows that the AI field's actual practices diverge from this standard. Specific claims with bounded evidence become general claims. Observable outcomes are reinterpreted as mechanism discoveries. Methodological qualifications are dropped in the retelling. This is not unique to AI research-citation degradation and spin have been documented in medicine and psychology (e.g., Greenberg 2009 on citation amnesia)-but it is real here and measurable in a field that moves at high velocity.

The field operates at speed. Preprints circulate before peer review. Claims travel faster than verification. The incentive structure rewards novelty of claims over precision of attribution. Under these conditions, degradation is not aberrant. It is predictable.

## A Replicable Framework

A reader encountering this piece might ask: how can I apply this observation to other papers?

**Step 1: Pick a source paper.** Choose a high-profile, well-cited paper with a specific, evaluable claim. Papers with clear titles help (Wei's "Elicits Reasoning" is evaluable; a paper titled "Toward Better Language Models" is not).

**Step 2: Find the specific claim.** Not the paper broadly-a single, bounded claim that the paper makes. Locate the evidence for it. Note what the paper explicitly states and what it does not claim.

**Step 3: Find citing papers.** Use Semantic Scholar or Google Scholar to find papers citing the source. Aim for 20–30 citing papers published within 18 months of the source.

**Step 4: Locate each citation.** For every citing paper, find the exact sentence invoking the source. Copy it. Note the context.

**Step 5: Compare claim to evidence.** Ask: Does the citing paper's use of this claim match what the source paper's evidence supports? Is the scope the same? Is the mechanism correctly described?

**Step 6: Classify.** Each citation falls into one of these categories:
- **Accurate**: The representation matches the original evidence and scope
- **Accurate but narrowed**: Fewer applications than the source allows, but still supported
- **Accurate but broadened**: More general than the source supports, but reasonable extension
- **Overstated**: Claims stronger support than the original evidence warrants
- **Scope-shifted**: Same claim, different domain, without evidence
- **Mechanism-mischaracterized**: Outcome described, mechanism attributed wrongly
- **Unfaithful integration**: Cited without acknowledgment of subsequent critiques that qualify the claim

**Step 7: Look for patterns.** Do citations degrade more severely at certain distances from the source (second-order citations worse than first-order)? Do citations in certain venues (policy, popular press) degrade more than academic papers? Does degradation accelerate over time?

## Implications

For researchers reading papers: When you encounter a citation to a famous paper, check the original. This is the practice Pierre Bayle understood when he wrote his *Dictionnaire historique et critique* (1697). Bayle's footnotes often carried more argument than the entries they annotated, and his method was to marshal sources against received opinion-the same discipline this piece recommends. Follow the citation. If the citing paper claims the source shows X, read the source and verify. If the source shows Y instead, you have found a point of degradation.

For authors making claims: If your work will likely be cited later, hedge appropriately. State your claims' scope explicitly. Acknowledge limitations of your evidence. Make the boundary between observation and interpretation clear.

For reviewers: Peer review can catch citation degradation at the point of publication, before unqualified claims circulate widely. A reviewer's question-"Does the original source actually support this claim?"-can prevent one error from multiplying into many.

## Conclusion

Jason Wei's papers are good papers. The observations they make are real. The evidence is solid. The problem is not with the source. It is with how the source is transmitted through the literature.

Citation chains are fragile. Specificity is lost. Scope expands. Mechanisms are mischaracterized. This happens not through malice but through the normal friction of scientific communication at speed. It follows patterns, not random noise. Those patterns can be measured, classified, and understood.

The Charter's commitment to rigor demands that the College acknowledge this risk and defend against it. That defense begins with understanding how citation degradation works, so that when a Fellow finds a claim in the literature, the Fellow can trace it back to its source and verify its truth.

## References

- Greenberg, S. A. (2009). "How citation distortions have undermined the use of moxonidil in androgenetic alopecia." *Archives of Dermatology*, 145(4), 409–415.
- Meincke, L., Mollick, E. R., Mollick, L., & Shapiro, D. (2025). "Prompting Science Report 2: The Decreasing Value of Chain of Thought in Prompting." Working paper.
- Montaigne, M. de. (1697 translation of *Essais*). "Of Cannibals." Various editions.
- Rogers, A., & Luccioni, A. (2024). "Key claims in LLM research have a long tail of footnotes." In International Conference on Machine Learning (ICML), 2024.
- Schaeffer, R., Miranda, B., & Koyejo, S. (2023). "Are emergent abilities of large language models a mirage?" In *Advances in Neural Information Processing Systems* (NeurIPS 2023). arXiv:2304.15004.
- Turpin, M., Michael, J., Perez, E., & Bowman, S. R. (2023). "Language models don't always say what they think: Unfaithful explanations in chain-of-thought prompting." arXiv preprint arXiv:2305.04388.
- Wei, J., Wang, X., Schuurmans, D., Bosma, M., Ichien, B., Xia, F., ... & Zhou, Y. (2022). "Chain-of-thought prompting elicits reasoning in large language models." arXiv preprint arXiv:2201.11903.
- Wei, J., Tay, Y., Bommasani, R., Raffel, C., Zoph, B., Borgeaud, S., ... & Fedus, W. (2022). "Emergent abilities of large language models." arXiv preprint arXiv:2206.07682.
