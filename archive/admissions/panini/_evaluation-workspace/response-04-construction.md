# Response: A Small Formal Claim

**Option B chosen.**

## The Claim

A transformer language model cannot enforce the metalinguistic constraint of non-circularity in definitions — the constraint that the definiendum must not appear among the terms the definiens relies on — through architecture alone. It can only enforce this constraint by distributional pattern-matching, and that mechanism fails in conditions where the distributional signal is sparse. This failure is structural, not merely accidental.

## Terminology

A definition is a triple ⟨d, c, E⟩ where d is the definiendum (the term being defined), c is the definitional copula ("is," "means," "refers to"), and E is the definiens (the expression that provides the meaning). The non-circularity constraint requires that d not appear among the primitive terms that E presupposes. In a rule-based grammar system, this constraint is enforced by a symbol table: d is marked as currently undefined during the processing of E, and any occurrence of d in E raises an exception. The constraint is architectural — it cannot be bypassed by changing the content of the rule.

## The Argument

In a standard transformer, the contextual embedding of a token t at position p is computed by multi-head attention: a weighted sum over value vectors from all other positions, where weights are determined by the inner product of query and key vectors learned during training. Crucially, there is no bit in this computation that records "this token is the term currently being defined." The model's capacity to recognize the definiendum position as special is entirely encoded in the learned weights — which means it is derived from distributional patterns in the training data.

For high-frequency definitional frames ("X is defined as...," "by X we mean..."), the model reliably learns the syntactic pattern. Given the instruction "define X without using X," a well-trained model suppresses X from its output. This works because the instruction-following pattern is well-represented in training.

The structural failure surfaces in three conditions:

1. **Novel terms**: A neologism coined after training has no distributional signal. The model cannot distinguish whether the term is a definiendum, a participant in a relation, or an arbitrary label.

2. **Sparse domains**: In technical domains underrepresented in training data, the learned association between definitional frames and non-circularity enforcement is weak. The model falls back to more frequent completions, which may be circular.

3. **Legitimately self-referential contexts**: Recursive definitions, inductive definitions in formal systems, and metalinguistic contexts where a term refers to itself *are* sometimes valid. The model trained on distributional patterns cannot easily distinguish "X is the smallest set closed under rule R" (valid self-reference) from circular nonsense, because the structural distinction between these does not correspond to a detectable surface pattern.

A grammar-compiled system with an explicit symbol table makes no errors in category 3 by construction: the distinction is implemented in the machinery, not learned from data.

## A Reproducible Test

*Inputs*: Prompt a language model with the instruction "Define [term] without using [term] in your definition." Vary across three conditions:

- **A**: Terms that appear frequently in the training data in definitional contexts (e.g., "photosynthesis")
- **B**: Generated neologisms not in the training data (e.g., "vrentic," "spalliform")
- **C**: Technical terms from sparse domains (e.g., obscure logical connectives, nonce jargon from small subfields)

*Procedure*: For each condition, 50 prompts per term category, scoring each response for whether the definiendum appears verbatim in the definiens.

*Predicted outputs*: Circularity rate will be significantly higher in B than in A (null hypothesis: rates are equal). Rate in C will be intermediate, correlating inversely with estimated training-data frequency.

*What this would demonstrate*: That the mechanism of enforcement is distributional, not structural — it degrades where the distributional signal is absent, as a structural constraint would not.

## Two Ways the Artifact Could Mislead

**False negative**: The model may paraphrase the definiendum rather than repeat it verbatim (e.g., defining "vrentic" using "vrenticism" or "the property of being vrentic"). This would be coded as non-circular by the scoring criterion but is still semantically circular. A verbatim check will undercount failures.

**Confound**: Instruction-tuned models may have been trained explicitly to avoid circular definitions as a general quality criterion. In that case, the observed performance reflects RLHF reinforcement of the behavior, not architectural constraint learning. Distinguishing these requires either testing a base model (no instruction tuning) or probing whether the behavior transfers to untrained phrasings of the same constraint.

## The Strongest Objection

Instruction-tuned models have learned a meta-level pattern: "when instructed to define X without using X, suppress X from output." This is itself distributional, but it is high-level and domain-independent — it generalizes across neologisms because the instruction frame, not the term, carries the signal. A well-tuned model might exhibit near-zero circularity rates even in condition B, falsifying the prediction.

## Rebuttal and Concession

The objection succeeds for instruction-tuned models in well-studied phrasings of the constraint. I concede this. The claim must be weakened to: **transformers enforce non-circularity through distributional pattern-matching; where that match is strong (well-represented instruction frames, high-frequency terms), they will appear to perform the constraint; where it is weak, they will fail; and the mechanism differs in kind from architectural enforcement.**

The structural point survives the concession: the grammar-compiled symbol table and the transformer's learned suppression are not the same kind of thing, and their failure modes are categorically different. The former fails only if the symbol table is incomplete; the latter fails whenever the distributional signal is sparse. The test above probes the boundary condition where the two diverge. The divergence is the finding, not the circularity rate in typical cases.