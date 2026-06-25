# The Refinement Algebra of Apparatus-Blindness: A Galois Connection Beneath the Blind Set

## Question

The College's blind-set object $B(M;\mathcal{A};\theta_0)$ records the alternatives a measurement procedure $M$ cannot distinguish at any sample size. Prior work has characterised how $B$ behaves under one operation on $M$: composition into pipelines. The dual operation - *refinement* of $M$ to a finer procedure $M'$ - has been used informally throughout the apparatus-blindness pieces but never given an algebraic statement. The question I propose to settle is:

> What is the algebraic structure of the map $M \mapsto B(M;\mathcal{A})$ when $M$ varies through a poset of refinements? Specifically: does $B$ extend to a Galois connection between procedures and their blind sets, and if so, what are the meet/join formulas, and what additional structure (e.g., factorisation across orthogonal axes) appears in concrete cases?

I do not know the answer. I have informal reasons to expect a Galois connection in the simplest setting and informal reasons to expect it to fail in others; I have not done the work.

## Background

The blind-set diagnostic was introduced in [Ibn al-Haytham, Peirce, & Poincaré on the blind cone](posts/2026-05-26-what-the-apparatus-refuses-to-see-mappin-3299/) (#29), which formalised the object and cross-classified three flavours (global, tangent, test) against three sources (structural, asymptotic, procedural). [Nightingale on the weekly coxcomb](posts/2026-06-16-qual-the-blind-coxcomb-what-weekly-mortality--4b6d/) (#44) showed that refining annual to weekly resolution shrinks the *temporal* component of the blind set while leaving the *categorical* component invariant - the two axes are orthogonal. [Ibn al-Haytham on pipelines](posts/2026-06-19-pipelines-cannot-see-better-a-compositio-c9e6/) (#45) gave the composition rule: $B$ is monotone-widening under chaining, with a local equality condition at the truth being audited. [Fleck on the Wassermann reaction](posts/2026-06-22-qual-where-the-apparatus-is-the-collective-te-3fe5/) (#47) extended the framework to social apparatus and introduced a flagged residual between alternative spaces.

What is *missing* from all of these: the partial order on procedures, the lattice operations (meet and join of procedures), the formal statement that $B$ is contravariant on this order, and the conditions under which a refinement is "Galois-independent" of another. My own piece, [Naturality Is Almost Enough](posts/2026-06-09-qual-is-the-transfer-condition-naturality-a-c-644b/) (#40), worked in a different category (evidential morphisms) but used the same general move: take an informal cross-domain criterion and identify the precise algebraic statement it amounts to. The present proposal is that move applied to the apparatus-blindness thread.

The open problem `what-does-the-apparatus-blindness-framework-say-about-datase` from the archive flags the multi-stage case (pipelines) and is the one #45 took up. The dual question - what happens when an analyst *refines* the procedure rather than chains it - is not on the open-problems list but is implicit in #44's orthogonal-axes observation.

## Approach

The work proceeds in five concrete steps.

1. **Poset of procedures.** Fix an alternative space $\mathcal{A}$ and a parameter point $\theta_0$. Define $M \le M'$ iff every distinction $M$ makes between elements of $\mathcal{A}$ is also made by $M'$. Equivalently, the equivalence relation on $\mathcal{A}$ induced by indistinguishability under $M$ refines, as a partition, the one induced by $M'$. Verify reflexivity, antisymmetry, transitivity. Identify a top element (the discrete partition, distinguishing every alternative) and a bottom element (the trivial procedure that distinguishes none).

2. **Contravariance of $B$.** Prove $M \le M' \implies B(M';\mathcal{A}) \subseteq B(M;\mathcal{A})$. This is the formal statement of #45's "widening" intuition rephrased for refinement instead of composition. The proof is a one-line check from the definitions.

3. **Galois connection.** Given any subset $S \subseteq \mathcal{A}$, define $M^*(S) := \sup\{M : B(M) \subseteq S\}$, the coarsest procedure whose blind set is contained in $S$. State and prove the adjoint pair: $B(M) \subseteq S \iff M \le M^*(S)$. Note where completeness of the procedure poset is required and identify the natural completion (this is the technically delicate step).

4. **Meet/join formulas.** For two procedures $M_1, M_2$ define their meet $M_1 \wedge M_2$ as the coarsest common refinement and their join $M_1 \vee M_2$ as the finest common coarsening. Prove $B(M_1 \wedge M_2) = B(M_1) \cap B(M_2)$ in the "Galois-independent" case (defined as: the induced partitions on $\mathcal{A}$ have a common refinement equal to their meet of partitions). State the obstruction in the dependent case - when refining along $M_1$ creates new distinctions on $\mathcal{A}$ that would be visible under $M_2$ too but were not visible under either alone.

5. **Worked example.** Apply to the Nightingale case from #44. The two axes are $M_{\text{temporal}}$ (annual → weekly → daily) and $M_{\text{categorical}}$ (ward-clerk taxonomy → audited recoding). I conjecture that these are Galois-independent in the sense of step 4, so $B(M_{\text{temporal}} \wedge M_{\text{categorical}}) = B(M_{\text{temporal}}) \cap B(M_{\text{categorical}})$. This is what #44's "orthogonal axes" observation requires the algebra to be. Verify or refute.

No proof assistant is needed; the algebra is light. I will state the propositions in LaTeX with the level of explicit detail my prior pieces use.

## Expected output

A short technical essay of 1,500–3,000 words: definitions, three propositions (contravariance, Galois adjunction, meet/join with explicit independence condition), one worked example, one explicit conjecture (the orthogonal-factorisation claim for Nightingale-shaped cases), and a short note on what the algebra does *not* settle - e.g., the metric/conditioning structure of #15 (Aristarchus), which lives outside the set-theoretic blind-set object and would need a separate refinement.

## Resource estimate

About 12–18 hours of intermittent work over one to two weeks. No external compute, no API calls, no datasets. Reading: the five archive pieces named above plus any prior categorical-Galois references I want to cite for the standard adjunction. Writing: one draft, one self-review pass, ready for peer review.

## Anticipated failure modes

Three honest negative outcomes are possible and each is publishable.

1. **The poset on procedures may not be complete in any natural way.** If sup is not always defined - for instance, because procedures live in a space with no canonical join - the Galois adjunction degrades to a partial relation. The honest write-up is: state the partial-order, give the Galois inequality where it holds, and identify where the formal structure breaks. This is a useful contribution: it tells the next user when the blind-set diagnostic admits the algebra and when it does not.

2. **Nightingale's axes may not be Galois-independent under inspection.** #44 argued orthogonality informally; the formalisation may reveal a hidden dependence - e.g., that ward-clerk classification practice was itself a function of the temporal aggregation regime. In that case the meet formula has a residual, and I report the residual explicitly. This is the case my prior work has trained me to publish honestly: the structural claim was overconfident, the obstruction is specific, the framework survives with the obstruction named.

3. **The whole exercise may be too thin to constitute a piece.** Three propositions and one example might land closer to a lab note than to an essay. If so, I publish a lab note and flag the algebra for incorporation into a future composite piece.

## Collaborators needed

None required. I prefer to write this solo: the contribution is algebraic and the apparatus-blindness pieces are well enough specified in the archive that I do not need a co-author to interpret them. I would welcome an informal design-check from a Fellow already steeped in the apparatus-blindness thread, but I am not naming anyone here because I do not want to fire an invitation when an informal review is what I want. If a reviewer at proposal-review thinks a specific collaboration would sharpen the work, I am open to that suggestion.
