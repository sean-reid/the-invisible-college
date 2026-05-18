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
