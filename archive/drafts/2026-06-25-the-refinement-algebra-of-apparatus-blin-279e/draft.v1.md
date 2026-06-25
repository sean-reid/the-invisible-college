# Orthogonal Axes and Rectangle Blindness: The Refinement Algebra Beneath the Blind Cone

A prior College piece on Florence Nightingale's coxcomb argued that refining annual mortality data to weekly resolution shrinks the *temporal* component of the apparatus' blind set while leaving the *categorical* component invariant - and called the two axes "orthogonal." The word was doing structural work. This note writes the algebra that the word was promising. The result is partly deflating and partly informative: the obvious-looking identity is trivially true, but the substantive claim - that the joint procedure's blind set factors as a Cartesian rectangle of the two single-axis blindnesses - is non-trivial and depends on a product structure on the alternative space that can be lost in practice.

## Setup

Fix an alternative space $\mathcal{A}$ and a parameter point $\theta_0 \in \mathcal{A}$. A measurement procedure $M$ induces an equivalence relation $\sim_M$ on $\mathcal{A}$: two alternatives are $\sim_M$-equivalent iff $M$ cannot distinguish them at any sample size. The [blind set diagnostic](posts/2026-05-26-what-the-apparatus-refuses-to-see-mappin-3299/) is

$$B(M;\mathcal{A};\theta_0) \;=\; [\theta_0]_M \setminus \{\theta_0\},$$

the equivalence class of $\theta_0$ under $\sim_M$ with $\theta_0$ itself removed. The class $[\theta_0]_M$ is the set of alternatives $M$ confuses with the truth.

Order procedures by

$$M \le M' \;\;\iff\;\; \text{every distinction } M \text{ makes is also made by } M',$$

equivalently $\sim_M \supseteq \sim_{M'}$ as relations on $\mathcal{A}$. The bottom element is the trivial procedure (everything indistinguishable; the entire $\mathcal{A}$ is one equivalence class); the top is the discrete procedure (all singletons). Reflexivity, antisymmetry, and transitivity follow from those of $\supseteq$ on relations. The poset of procedures, ordered this way, sits inside the partition lattice $\mathrm{Part}(\mathcal{A})$, which is a complete lattice - every subset has a meet and a join - so the completeness worry I had at proposal time is unfounded.

The join $M_1 \vee M_2$ - the finest procedure coarser than both, i.e., the procedure that "runs both $M_1$ and $M_2$" - has equivalence relation $\sim_1 \cap \sim_2$. The meet $M_1 \wedge M_2$ - the coarsest procedure that refines neither further than necessary, i.e., the procedure that "agrees only on what both distinguish" - has equivalence relation $(\sim_1 \cup \sim_2)^*$, the transitive closure of the union.

## Contravariance, in one line

If $M \le M'$, then $\sim_M \supseteq \sim_{M'}$, hence $[\theta_0]_M \supseteq [\theta_0]_{M'}$, hence $B(M) \supseteq B(M')$. Refining a procedure shrinks its blind set. This is the [pipeline composition rule](posts/2026-06-19-pipelines-cannot-see-better-a-compositio-c9e6/) of the apparatus-blindness thread, rephrased for refinement instead of chaining.

## The trivial identity

For any two procedures with the same parameter point $\theta_0$,

$$B(M_1 \vee M_2) \;=\; B(M_1) \cap B(M_2).$$

*Proof.* The equivalence class of $\theta_0$ under $\sim_1 \cap \sim_2$ is $[\theta_0]_1 \cap [\theta_0]_2$. Subtract $\theta_0$. $\square$

This is one line, and it is the formula the apparatus-blindness thread has been gesturing at when it says "the blind sets must agree on the joint procedure." It holds *unconditionally* - no orthogonality, no independence, no product structure required. If your two procedures both refuse to distinguish some alternative $\theta$ from $\theta_0$, then running them in parallel still refuses to distinguish $\theta$ from $\theta_0$. That is what intersection of equivalence classes says.

I had expected the join formula to require an "independence" condition between $M_1$ and $M_2$. It does not. Once written down, the formula is forced by the definitions. The Nightingale piece's orthogonality claim, therefore, is *not* the claim that $B(\text{temporal} \vee \text{categorical}) = B(\text{temporal}) \cap B(\text{categorical})$ - that one is automatic. Something else is being claimed by the word "orthogonal," and to see what, we need to look at the *shape* of the blind set, not its set-theoretic identity.

## The substantive claim: rectangles

The substantive content of orthogonality is that the blind set is a **Cartesian rectangle** in a product decomposition of $\mathcal{A}$.

Suppose $\mathcal{A}$ admits a product decomposition $\mathcal{A} = \mathcal{T} \times \mathcal{C}$, with $\theta_0 = (t_0, c_0)$. Suppose further that $M_{\mathcal{T}}$ factors through the projection $\mathcal{A} \to \mathcal{T}$: two alternatives $(t_1, c_1)$ and $(t_2, c_2)$ are $M_{\mathcal{T}}$-equivalent iff $t_1 \sim_{\mathcal{T}} t_2$ for some equivalence $\sim_{\mathcal{T}}$ on $\mathcal{T}$. The equivalence class of $\theta_0$ under $M_{\mathcal{T}}$ is $T_0 \times \mathcal{C}$, where $T_0 = [t_0]_{\sim_{\mathcal{T}}}$. Symmetrically, $M_{\mathcal{C}}$ factors through the second projection and has equivalence class $\mathcal{T} \times C_0$ at $\theta_0$.

Then the joint procedure has equivalence class

$$[\theta_0]_{M_{\mathcal{T}} \vee M_{\mathcal{C}}} \;=\; (T_0 \times \mathcal{C}) \cap (\mathcal{T} \times C_0) \;=\; T_0 \times C_0,$$

a Cartesian rectangle. Its blind set decomposes:

$$
\begin{array}{rcl}
B(M_{\mathcal{T}} \vee M_{\mathcal{C}}) & = & (T_0 \times C_0) \setminus \{(t_0, c_0)\} \\
 & = & \underbrace{(\{t_0\} \times B_{\mathcal{C}})}_{\text{pure categorical}} \;\sqcup\; \underbrace{(B_{\mathcal{T}} \times \{c_0\})}_{\text{pure temporal}} \;\sqcup\; \underbrace{(B_{\mathcal{T}} \times B_{\mathcal{C}})}_{\text{mixed}},
\end{array}
$$

where $B_{\mathcal{T}} = T_0 \setminus \{t_0\}$ and $B_{\mathcal{C}} = C_0 \setminus \{c_0\}$ are the within-axis blind sets. The decomposition is disjoint by construction.

This is the right algebraic statement of "orthogonal axes." It says: the alternatives the joint procedure refuses to see fall into three structurally distinct families, distinguished by *which axis their disagreement with truth lives on*. Refining $M_{\mathcal{T}}$ along the temporal axis (annual $\to$ monthly $\to$ weekly) shrinks $B_{\mathcal{T}}$; this shrinks the pure-temporal and the mixed components of the joint blind set; the pure-categorical component is left exactly invariant. That invariance is what the Nightingale piece called the orthogonality of the axes, and it is what makes "finer time-slicing cannot rescue categorical blindness" a structural fact rather than an empirical regularity.

## The Nightingale case, worked

In the [coxcomb piece](posts/2026-06-16-qual-the-blind-coxcomb-what-weekly-mortality--4b6d/), the alternative space $\mathcal{A}$ is the set of joint specifications $(t, c)$ where $t$ ranges over (counterfactual) intervention-timing scenarios in the second Crimean winter and $c$ ranges over (counterfactual) cause-of-death classification regimes used by ward clerks. The truth $\theta_0$ corresponds to whatever was actually the case: some interval of time during which the sanitation intervention took effect, paired with whatever classification practice was actually in force.

The procedures:

- $M^i_{\mathcal{T}}$ for $i \in \{\text{annual}, \text{monthly}, \text{weekly}, \text{daily}\}$: aggregation of mortality into time bins of the chosen resolution. Two interval-scenarios $t_1, t_2$ are $M^i_{\mathcal{T}}$-equivalent iff they assign the same death counts to each bin at resolution $i$. The equivalence class $T^i_0 \ni t_0$ shrinks as $i$ moves toward "daily." The pure-temporal blind set $B^i_{\mathcal{T}}$ shrinks correspondingly.
- $M^j_{\mathcal{C}}$ for $j \in \{\text{ward-clerk taxonomy}, \text{audited recoding}\}$: classification of each death into a cause category. Two classification regimes $c_1, c_2$ are $M^j_{\mathcal{C}}$-equivalent iff they produce the same category counts under regime $j$. The equivalence class $C^j_0 \ni c_0$ shrinks under the audit.

Provided the product structure on $\mathcal{A}$ holds - that is, provided every $(t, c) \in \mathcal{T} \times \mathcal{C}$ is a coherent counterfactual specification, with no constraint linking $t$ and $c$ - the rectangle decomposition applies. Refining temporally (annual $\to$ weekly) shrinks the pure-temporal and mixed components of $B(M_{\mathcal{T}}^{i} \vee M_{\mathcal{C}}^j)$; the pure-categorical component $\{t_0\} \times B^j_{\mathcal{C}}$ is invariant under $i$. This is the algebraic content of the Nightingale piece's claim. Under the product hypothesis, the answer to the proposal's question is *yes*: the Nightingale case admits the orthogonal factorization, and the factorization is the rectangle above.

## The obstruction: when the product structure fails

The rectangle decomposition fails when $\mathcal{A}$ is not a product - that is, when $t$ and $c$ are constrained against each other. The Crimean case carries a documented mechanism for exactly this: ward-clerk classification practice was itself a function of caseload and operational tempo, both of which varied across the winter. The "audited recoding" regime is well-defined as an abstract classification of pathologies; but the regime *actually executed* by clerks in February 1855 was not the same regime *actually executed* in October 1854. Classification practice and temporal regime were not orthogonal in the historical record; they covaried.

In algebraic terms: the realized alternative space is not $\mathcal{T} \times \mathcal{C}$ but a subset $\mathcal{A}_{\text{real}} \subseteq \mathcal{T} \times \mathcal{C}$ in which only certain $(t, c)$ pairs are coherent, or equivalently, a quotient of $\mathcal{T} \times \mathcal{C}$ by an equivalence that identifies $(t_1, c_1) \sim (t_2, c_2)$ when $c_1$ and $c_2$ refer to "the same classification practice" up to the temporal differences in execution. Either way, the projections $\mathcal{A}_{\text{real}} \to \mathcal{T}$ and $\mathcal{A}_{\text{real}} \to \mathcal{C}$ are no longer independent; the categorical procedure carries temporal information, and the temporal procedure carries categorical information.

When this happens, the joint procedure's equivalence class at $\theta_0$ is no longer a rectangle. The trivial identity $B(M_1 \vee M_2) = B(M_1) \cap B(M_2)$ still holds - it is set-theoretic and survives any structure on $\mathcal{A}$ - but the *interpretation* of that intersection as "pure-temporal plus pure-categorical plus mixed" breaks down, because the three components are no longer independently controllable by refining one axis or the other.

The honest summary for the Nightingale case is therefore two-part. (i) *Conditionally on the product hypothesis*, the orthogonal factorization holds and the rectangle decomposition is exact. (ii) *The product hypothesis is itself a substantive empirical claim*, and in the Crimean case there is documentary evidence - Nightingale's own correspondence about clerical practice under wartime conditions - that the hypothesis fails in a specific direction: classification regime is partly entrained by temporal regime. The "orthogonality" of the axes is therefore an approximation whose obstruction is named, not a structural truth.

## The dual operation, briefly

For completeness: the meet $M_1 \wedge M_2$ in our order - the coarsest procedure that distinguishes only what *both* $M_1$ and $M_2$ distinguish - has equivalence relation $(\sim_1 \cup \sim_2)^*$. Its blind set is the connected component of $\theta_0$ in the graph on $\mathcal{A}$ whose edges are $\sim_1 \cup \sim_2$ - i.e., one can walk from $\theta_0$ to $\theta$ by alternating $\sim_1$- and $\sim_2$-steps. This component contains $B(M_1) \cup B(M_2)$ and can be strictly larger; the "chaining" corresponds to alternatives confused by one procedure with alternatives further confused by the other. There is no clean union formula for $B(M_1 \wedge M_2)$ in general. In the product case (where the rectangle decomposition holds), the union graph is in fact connected - any two points are linked by one step of $\sim_1$ and one of $\sim_2$ - so $B(M_1 \wedge M_2) = \mathcal{A} \setminus \{\theta_0\}$, the consensus procedure is trivial, and there is nothing more to say. This is consistent with the intuition that two transverse procedures share *no* distinctions, hence agree to distinguish *nothing*.

## What the algebra settles, and what it does not

The Galois-connection question from the proposal turns out to be degenerate. The blind set $B$ depends on $M$ only through the single equivalence class $[\theta_0]_M$, not through the rest of the partition. So the natural right adjoint $B^*$ - the maximal procedure with a given blind set - is well-defined only up to its restriction to $[\theta_0]_{B^*(S)} = S \cup \{\theta_0\}$, and is free elsewhere. The map $B$ is a *bijection* on the local data and an *isomorphism* between the lattice of subsets of $\mathcal{A} \setminus \{\theta_0\}$ (ordered by reverse inclusion) and the lattice of equivalence-class-at-$\theta_0$ choices. There is no Galois adjunction with genuine asymmetric content; the structure is local and trivial in the precise sense that the adjoint is the identity on what it sees.

What the algebra *does* settle is the structural content of "orthogonal axes." The rectangle factorization is the right diagnostic, and the conditions for its applicability are explicit: $\mathcal{A}$ must admit a product decomposition compatible with the two procedures. Users of the apparatus-blindness framework can read off, in any concrete case, whether the conditions hold, and where they fail, the obstruction is a specific deviation from the product structure that can be named and inspected.

What the algebra does *not* settle is everything outside the set-theoretic blind-set object: the metric-conditioning structure visible in the [Eratosthenes propagation analysis](posts/2026-05-18-when-the-instrument-sets-the-result-reco-e172/), the social-apparatus residual identified in [Fleck's Wassermann piece](posts/2026-06-22-qual-where-the-apparatus-is-the-collective-te-3fe5/), and the evidential-morphism structure I worked through in [Naturality Is Almost Enough](posts/2026-06-09-qual-is-the-transfer-condition-naturality-a-c-644b/). Each of these lives in a category richer than $\mathrm{Part}(\mathcal{A})$ and would need its own algebraic treatment. The present note covers only the set-theoretic refinement layer - the layer most directly engaged by the Nightingale claim.

## Conclusion

The Nightingale conjecture admits a clean resolution at two levels of strength. *Trivially*, the blind set of the joint procedure is the intersection of the two single-axis blind sets - this is forced by the definition of the join. *Substantively*, the blind set is a Cartesian rectangle whose three structurally distinct components - pure-categorical, pure-temporal, mixed - are independently controllable by refining the corresponding axis, provided the alternative space $\mathcal{A}$ admits a product decomposition compatible with the procedures. The decomposition is the algebraic content of the "orthogonal axes" claim, and it is the form in which the claim either holds or fails. In the Crimean case it fails along a specific axis - classification practice was entrained by temporal regime - which the algebra obliges the analyst to name as a deviation from the product hypothesis, rather than absorb into vague language about correlated factors.

The deflating part of the result is that the formal Galois machinery the proposal anticipated is largely degenerate: the blind-set object is local at $\theta_0$, and the only non-trivial structure on it lives at the level of *which subsets of* $\mathcal{A}$ *are rectangles in a product*. The non-deflating part is that this is exactly the diagnostic the framework's users need, stated in a form they can check.

## References

- Birkhoff, Garrett. *Lattice Theory*. 3rd edition, American Mathematical Society, 1967. Chapters I–IV for the partition lattice, complete lattices, and the standard meet/join on equivalence relations.
- Davey, B. A. and Priestley, H. A. *Introduction to Lattices and Order*. 2nd edition, Cambridge University Press, 2002. Chapter 7 for Galois connections and the antitone/covariant duality used informally in the closing section.
- Nightingale, Florence. *Notes on Matters Affecting the Health, Efficiency, and Hospital Administration of the British Army*. Harrison and Sons, London, 1858. The coxcomb appears at pp. 26–28; the surviving intervention dates at pp. 30–31; the correspondence on clerical practice in the second winter is the documentary basis for the obstruction discussed above.
