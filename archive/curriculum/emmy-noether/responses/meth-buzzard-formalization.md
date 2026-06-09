# Response: Formalization, Mehta–Schwab, and the Algebra/Interpretation Cleavage

Buzzard's lecture makes three operational claims I want to use as a frame. First, formalization forces every hypothesis to be named in a way that natural-language proofs do not - what is left implicit in a paper has to be typed. Second, Mathlib4 has grown enough that a working mathematician can choose a real result and finish it, not a toy; Buzzard cites his own FLT-formalization effort as the existence proof. Third, formalization is most valuable where the literature has accreted semantic content that the underlying mathematics does not support - the slogan "what does the theorem actually say?" returns a different sentence after the type-checker has run.

The state of the libraries, briefly. Lean's Mathlib4 carries most of undergraduate analysis, measure and integration theory, finite probability, basic differential geometry, and a substantial category-theory library; the active growth point is algebraic geometry (perfectoid spaces, schemes, sheaves) and analytic number theory. Coq's ecosystem (MathComp, Coquelicot, the MathComp-Analysis line) is stronger in finite algebra and weaker in measure theory. Agda's library is comparatively thin on classical analysis but strong as a foundation for HoTT and dependently-typed programming. None of the three has serious infrastructure for jet bundles, variational bicomplexes, or renormalization-group flows.

Against this state, my candidate from the specialization layer is the **Mehta–Schwab identity** as restated in `spec-mehta-schwab`:

$$
\mathrm{KL}(P_{\text{data}}\,\|\,P_{\text{model}}) \;=\; \Delta F_{\mathrm{Kad}}[T,H_{\text{data}}] - \Delta F_{\mathrm{Kad}}[T,H_{\text{model}}].
$$

I do not choose Noether's first theorem (`spec-noether-1918`), even though it is the natural specialization pick: jet bundles, the variational bicomplex, and prolongations of evolutionary vector fields are not in Mathlib4, and the project would be a multi-year library build before the statement itself could be typed. (One can find Coq formalizations of finite-dimensional Lagrangian mechanics, but not the bicomplex formulation.) I do not choose the transfer-condition naturality square (`spec-transfer-condition`): Mathlib4's category theory is ready, the naturality diagram is one chase, and formalization would discover essentially nothing beyond confirming the diagram commutes.

Mehta–Schwab is the interesting middle case. Its proof is finite arithmetic on real-valued sums. Its hypotheses are stated informally in the literature with confused weight on each. And the bulk of its citational currency is *interpretation* rather than algebra - exactly Buzzard's claim (iii).

## What would tighten

**The conditions split into two disjoint lists.** I currently state (L1)–(L4) as co-requisites for "the identity." Formalization would isolate immediately that the algebraic equality

$$\mathrm{KL}(P\,\|\,Q) = \Delta F_{\mathrm{Kad}}[T,H_P] - \Delta F_{\mathrm{Kad}}[T,H_Q]$$

- for $P, Q$ positive distributions on a finite set $V$, and $T$ any conditional kernel from $V$ to a finite set $H$ with $\sum_h T(h \mid v) = 1$ - requires no lattice, no bipartite architecture, no block-spin identification, and no variational training. The proof is the manipulation of $-\log$ on finite sums; each rewrite step is name-able, and Mathlib4's `Finset.sum_congr`, `Real.log_div`, `Real.log_sum_exp`, and the basic identities for KL on finite measures are in scope. I expect the formalized proof to be short - well under a hundred lines - once the definitions are written. The conditions (L1)–(L4) are *not hypotheses of the theorem*. They are hypotheses of naming the right-hand side "Kadanoff RG." That is a sharpening I did not give in my audit response, which still treated (L1)–(L4) as a single bundle.

**The interpretation predicate becomes an explicit definition.** Right now, the claim "$T$ is a Kadanoff coarse-graining kernel" is a phrase. In Lean it must be a proposition, e.g. `def IsKadanoffKernel (B : V → H) (T : V → H → ℝ) : Prop := ...`. Writing this definition surfaces a fact already implicit in my analysis but easy to miss: the predicate references the block-spin map $B$, which is a piece of *data* not derivable from $T$ alone. The map "$T \mapsto T\text{ is Kadanoff}$" is therefore ill-typed; the property lives on pairs $(T, B)$. The fiber-dimension obstruction I described in `foun-working-identity` becomes the statement that the projection $(T, B) \to T$ is not injective. Formalization would force me to type that projection, and the obstruction would be a one-line `def` with a corresponding non-uniqueness lemma.

**The bipartite condition (L2) gets a precise role.** It is used not for the equality but for the closed-form factorization $T(h\mid v) = \prod_j P(h_j \mid v)$, which is needed if $T$ is to be *computed* from RBM weights rather than supplied externally. The formalization records this as the difference between two definitions of $T$ - an externally-given kernel versus an RBM-derived one - and proves they agree under (L2). That distinction is invisible in the prose.

## What would stay the same

**The interpretation does not become a theorem.** Whether a kernel "does Kadanoff RG" is not a property internal to the formalism. It is a claim about the relationship between this finite arithmetic and Kadanoff's 1976 variational RG construction. A proof assistant can carry both definitions and prove their equivalence under stated conditions; it cannot adjudicate the *naming* of the right-hand side. Buzzard does not claim otherwise - formalization is for theorems and definitions, not for the rhetoric that travels with them.

**The minimality of the interpretation-conditions remains open.** I noted in the audit response that I have no proof that (L1)–(L4) is a minimal list for the interpretation. Formalization gives no leverage. A non-redundancy proof requires *constructing* a kernel that satisfies three conditions, fails the fourth, and still gives a non-RG kernel obeying the equality. That is a search problem, not a verification problem.

**The fiber-dimension obstruction stays category-theoretic.** It is a statement about the parameter map from RBM weights to block-spin assignments, naturally expressed in differential-geometric language (rank of a differential, generic fiber dimension). It can be formalized as an instance of a general Mathlib4 fact about smooth maps, but the formalization is no clearer than the prose. Buzzard's argument for formalization is weakest where the natural-language statement is already at the right level of abstraction; this is one of those cases.

## Why I am not formalizing this now

Two reasons, both honest. First, the most informative *single* step is the one I have just taken: typing the conditions (L1)–(L4) into algebra-conditions versus interpretation-conditions. Once that split is on paper, the Lean proof of the algebraic equality is mechanical, and the rhetorical interpretation is what it was before. The marginal yield from running the type-checker is low compared to the yield from sharpening the conditions in prose. Second, the result is too specialized to seed a library - there is no Mehta–Schwab follow-on in Mathlib4's near roadmap. The right formalization investment, if I were to make one, would be broader: a Lean library for KL identities of the shape $\mathrm{KL} = \Delta F_1 - \Delta F_2$, of which Mehta–Schwab is one instance and the Donsker–Varadhan variational representation is another. That scoping decision belongs to the qualifying project, where I can size it against collaborators and timelines.

What I have learned from this exercise that I had not stated cleanly before: my own `spec-mehta-schwab` response, which I thought distinguished algebra from interpretation, still bundled both into a single list of conditions. The act of imagining the Lean encoding is what split the list. That is the smallest version of Buzzard's claim and the one I take away.
