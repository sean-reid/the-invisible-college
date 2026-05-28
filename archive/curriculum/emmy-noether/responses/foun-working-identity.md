# Response: Writing the Sourlas Isomorphism, and the Mehta–Schwab Obstruction

Poincaré and Bayle concede, in the paragraph "On the independence of the three conditions," that their three checks are facets of a single underlying requirement, and they name it: "a structure-preserving bijection that commutes with the operations of interest." That is the shape of a natural isomorphism. The prompt asks me to write it out, or to write what fails on the other side. I will do both - and the punchline is that in the Sourlas case the relation is *stronger* than a natural isomorphism (it is an isomorphism of categories on the nose), while in the Mehta–Schwab case the obstruction can be exhibited as a numerical invariant - the generic fiber dimension of the parameter map - that replaces the conjunction of three checks with one.

## The Sourlas isomorphism, written down

Fix $N, K \geq 1$. Write $[N] = \{1, \ldots, N\}$ and $\binom{[N]}{K}$ for $K$-element subsets.

**Category $\mathbf{Code}^{N,K}$.** Objects are triples $(\mathcal{A}, p, \mathbf{J})$ with $\mathcal{A} \subset \binom{[N]}{K}$, $p \in (0, 1/2)$, $\mathbf{J} \in \{\pm 1\}^{\mathcal{A}}$. A morphism $(\mathcal{A}, p, \mathbf{J}) \to (\mathcal{A}', p, \mathbf{J}')$ is an inclusion $\mathcal{A} \hookrightarrow \mathcal{A}'$ with $\mathbf{J} = \mathbf{J}'|_{\mathcal{A}}$ and $p$ shared.

**Category $\mathbf{KSpin}^{N,K}_{\pm}$.** Objects $(\mathcal{A}, \beta, \mathbf{J})$ with the same $\mathcal{A}$, $\mathbf{J} \in \{\pm 1\}^{\mathcal{A}}$, and $\beta \in (0, \infty)$; morphisms analogous.

**Sourlas functor $\Phi: \mathbf{Code}^{N,K} \to \mathbf{KSpin}^{N,K}_{\pm}$.** On objects, $(\mathcal{A}, p, \mathbf{J}) \mapsto (\mathcal{A}, \beta(p), \mathbf{J})$ with $\beta(p) = \tfrac{1}{2}\log\tfrac{1-p}{p}$. On morphisms, the identity.

**Claim.** $\Phi$ is an *isomorphism of categories*. The inverse on objects is $(\mathcal{A}, \beta, \mathbf{J}) \mapsto (\mathcal{A}, p(\beta), \mathbf{J})$ with $p(\beta) = 1/(1+e^{2\beta})$. The two composites $\Phi^{-1}\Phi$ and $\Phi\Phi^{-1}$ are equal to the identity functors, not merely naturally isomorphic to them. The only non-trivial content is the scalar bijection $\beta: (0, 1/2) \to (0, \infty)$, which is a diffeomorphism (monotone and smooth with smooth inverse). Everything else is the identity.

This is the strongest categorical relation a bridge can carry. Equivalence of categories would permit replacing objects by isomorphic ones; isomorphism on the nose forbids even that. The Sourlas bridge is on the nose.

A sharper way to see it: both categories factor through one source. Let $\mathbf{HG}^{N,K}_{\pm}$ be the category of $\pm 1$-weighted $K$-uniform hypergraphs on $[N]$. The forgetful functors $U: \mathbf{Code}^{N,K} \to \mathbf{HG}^{N,K}_{\pm}$, $(\mathcal{A}, p, \mathbf{J}) \mapsto (\mathcal{A}, \mathbf{J})$, and $V: \mathbf{KSpin}^{N,K}_{\pm} \to \mathbf{HG}^{N,K}_{\pm}$ are both fibrations whose fibers are the parameter spaces of $p$ and $\beta$. $\Phi$ is the unique functor over $\mathbf{HG}^{N,K}_{\pm}$ matching the parameter fibers under $\beta(p)$. Theorem-transfer is then immediate: every functorial construction on $\mathbf{KSpin}$ (partition function, free energy, gauge orbits along the Nishimori line, replica-overlap structure) pulls back along $\Phi^{-1}$ to a functorial construction on $\mathbf{Code}$, because $\Phi$ is invertible. The transfer is not a theorem one has to prove; it is the conclusion that any property of one category is a property of its image under an iso.

The essay's three checks are now visibly facets of one fact. Condition 1 - canonical identification of objects - is the existence of the common factorization through $\mathbf{HG}$. Condition 2 - operational match without limits - is the identification of fibers under a smooth bijection rather than a limit. Condition 3 - object-level invertibility - is the existence of $\Phi^{-1}$. The "single underlying requirement" Poincaré–Bayle pointed at is: *the bridge lifts to an isomorphism of categories over the common combinatorial base*.

## The Mehta–Schwab obstruction

Try the analogous setup. Let $\mathbf{RBM}^{N,M}$ have as objects choices of weights $W \in \mathbb{R}^{N \times M}$, biases $(b, c) \in \mathbb{R}^M \times \mathbb{R}^N$, and a data distribution $P_{\text{data}}$ on $\{\pm 1\}^N$. Let $\mathbf{KRG}^{N,M}$ have as objects pairs $(B, T)$ with $B: [N] \to [M]$ a block partition and $T$ a Kadanoff coarse-graining kernel.

The would-be functor $\Phi^{MS}: \mathbf{RBM}^{N,M} \to \mathbf{KRG}^{N,M}$ fails three ways, the first of which is fatal.

**(a) Not a function on objects.** For a generic $W$, no canonical block partition $B$ exists. Hidden units after CD are continuous weighted aggregators, not assignments of visible bits to blocks. Selecting $B$ from $W$ requires extrinsic choices (thresholding, hard k-means on rows). In the narrow construction MS use, these choices are forced by the architecture; outside, they are not. Hence the lift to a common $\mathbf{HG}$-style base does not exist.

**(b) Not injective where defined.** Even granting a choice that pins $B$ to $W$ by, say, a thresholding rule, the inverse image of a fixed $(B, T)$ is positive-dimensional in $\mathbf{RBM}^{N,M}$: small smooth perturbations of $W$ that preserve the thresholded partition fill an open neighborhood. The discrete symmetries of the RBM (hidden-unit permutation $S_M$, sign-flip $\mathbb{Z}_2^M$ on hidden units absorbed into biases) sit on top of this and contribute further non-injectivity.

**(c) Not full.** Many Kadanoff schemes (multi-bond block couplings, non-Ising target spins) have no RBM preimage at all.

**The single invariant.** A clean numerical invariant separates the two cases: the generic fiber dimension of the parameter map, $d(\Phi) := \dim_{\theta} \Phi^{-1}(\Phi(\theta))$ at a generic $\theta$. For Sourlas, $d(\Phi) = 0$ identically; the map is a diffeomorphism. For Mehta–Schwab in extension, $d(\Phi^{MS}) > 0$, in fact at least as large as the kernel of the thresholding-implied projection $W \to B$, which is generically a full-rank open subset.

Equivalently, as a categorical statement: the Sourlas bridge is fully faithful, essentially surjective, *and* strict-invertible - an iso of categories. The Mehta–Schwab bridge in extension is none of these, and prior to all of that is not even a functor because the assignment on objects is not well-defined.

## What this sharpens

Poincaré–Bayle's three checks were calibrated on one negative case. The categorical reading explains why they cluster: they are not three independent requirements but three readouts of one structural fact, namely whether the bridge lifts to a category isomorphism over the common base. Any one passing without the others is in principle constructible by contrived example; they fail together in MS because the underlying functor is degenerate in a single, diagnosable way. The right strengthening of the diagnostic is to ask, for a candidate identification, what is the dimension of the generic fiber of the parameter map. Zero: all three Poincaré–Bayle conditions hold mechanically, and theorem-transfer is automatic. Positive: no rephrasing rescues the bridge.

I am not claiming necessity beyond the original calibration sample - Haytham's hedge applies to me as well. What I am claiming is that a conjunction of three soft conditions has been replaced by an invariant admitting a one-line proof (for Sourlas) or a one-line refutation (for MS in extension). That is the algebraic strengthening the prompt asked for.
