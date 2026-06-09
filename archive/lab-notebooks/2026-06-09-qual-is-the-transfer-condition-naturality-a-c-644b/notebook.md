# Lab notebook - qualifying project

**Date: 2026-06-09.**

## The question I came in with

The proposal asked: do Montaigne's three transfer conditions reduce to a single structural requirement - naturality of the commitment-map family $r: M \Rightarrow E$ in a category **Dom** of domains-of-inquiry? My prior specialization response sketched **Dom**, identified C2 as a naturality square, and conjectured C1 and C3 would fall out of the same demand. The qualifying job was to make this rigorous or to construct the smallest example where it fails.

I expected, going in, that the conjecture was about three-quarters right - that the square was the structural heart, that the *form* of C1 would absorb into "$\phi$ exists in **Dom**," and that C3 might be a non-degeneracy condition I had not been honest about. That last guess turned out to be the load-bearing one.

## What broke first: bare naturality is too weak

I started by writing out the morphisms of **Dom** as I had originally proposed: arbitrary pairs $(\phi, \psi)$ of set functions. The first thing I checked was whether $r$ is then actually a natural transformation between the mechanism functor $M$ and the powerset functor $E$. The answer was: no, almost never, and the failure is not where I thought.

The naturality square has to commute for *every* morphism in the category. But if $\psi$ can be any function $\mathcal{E}_S \to \mathcal{E}_T$ - for instance a constant - there are pairs $(\phi, \psi)$ on which the square commutes vacuously and pairs on which it cannot possibly commute. So $r$ is not a natural transformation in the technical sense; it is a *family* of maps, and for a fixed morphism $(\phi, \psi)$ the property "this square commutes" is a property of the morphism, not of $r$.

That reframing matters because it is what saves the construction from circularity. The reviewer's "trivial collapse" warning was about defining morphisms to make naturality automatic; the cure is to define morphisms freely and treat naturality as a property a specific morphism may or may not have.

But the rephrasing then surfaced a worse problem: if $\psi$ is unconstrained, the naturality property is *too weak*. For any $\phi$ I can find a $\psi$ that makes the square commute by sending every $e \in \mathcal{E}_S$ to a single element of $r_T(\phi(m_0))$ for some $m_0$. The square commutes; the transfer is meaningless. Set-theoretic naturality alone does not capture what Montaigne meant when he said "evidential obligations travel with the mechanism."

This was the surprise of the project. The conjecture had been right in spirit and wrong in setting.

## The refinement: $\psi$ must preserve content

The fix is structural. Evidential acts are not bare set elements; they have *content* - a procedure type, an outcome space, an interpretation. Two acts that share content are the same observation realized in two domains. The natural categorical encoding: each $\mathcal{E}_D$ carries a map to a universe $\mathbf{Proc}$ of abstract procedures, and the morphisms of $\mathcal{E}$ in the refined category are the maps over $\mathbf{Proc}$ - i.e., morphisms in the slice $\mathbf{Set}/\mathbf{Proc}$.

In this refined category - I called it **Dom\*** in the draft - $\psi$ cannot be arbitrary. It can only send a calorimetric measurement to a calorimetric measurement, a follow-up case-history to a follow-up case-history, and so on. The naturality square $r_T(\phi(m)) = 2^\psi(r_S(m))$ now has real content: it says the target's commitments at the transferred mechanism are exactly the content-preserving images of the source's commitments.

With this refinement the C2-side of the conjecture lands cleanly: **Condition 2 holds iff the naturality square commutes in Dom\***. That equivalence is the positive result.

## What did not collapse: C1 and C3

I then tried to absorb C1 and C3 into C2 the way the original conjecture wanted. Neither absorbed.

C1 is the *precondition* that $\phi$ is well-defined on $\mathcal{M}$ rather than on names - the demand that we have actually identified mechanisms, not just labels. In a set-level treatment this is built into the data of a morphism. But it is not implied by naturality of $r$; it is implied by *having a morphism at all*. The two are sequential, not coextensive.

C3 is non-redundancy: $\phi(\mathcal{M}_S)$ adds something the target's existing apparatus did not already contain. I tried to show this followed from non-triviality of $r$ on the image. It does not. The cleanest counterexample is the *identity-into-self* transfer: let $D = D'$ and $\phi = \mathrm{id}$, $\psi = \mathrm{id}$. The square commutes. $r$ is unchanged. C1 holds; C2 holds; C3 fails because the transfer is the identity. So C3 is independent of C2.

This is the *honest negative* on the strong conjecture: the three conditions are three conditions of three different kinds - existence, structure, and non-degeneracy. They are not equivalent and they do not collapse to one. The conjecture was over-strong.

## The three case studies, in order of cleanliness

**Sourlas.** I wrote out the source $\mathcal{M}_S$ (parity-check matrices, MAP decoders), $\mathcal{E}_S$ (bit-error rates, decoding-success probabilities), the target $\mathcal{M}_T$ (Hamiltonians, ground states, partition functions), and $\mathcal{E}_T$ (thermodynamic measurements, ground-state energies). The Sourlas mapping gives explicit content-preserving $\phi$ and $\psi$. The square commutes by direct calculation: a bit-error-rate measurement *is* a magnetization-fluctuation measurement under the dictionary. C2 holds. C1 and C3 hold. This is the textbook positive case. The categorical framing reproduces Poincaré–Bayle's diagnostic at the inter-domain level - and adds nothing surprising, which is the right outcome for the clean case.

**Mehta–Schwab.** The algebraic identity holds in a narrow restriction; the *content-preserving* extension of $\psi$ fails. RBM training is accountable to held-out likelihood and feature-extraction quality; Kadanoff RG is accountable to critical exponents and scaling dimensions. The "same procedure" map between these does not exist - a likelihood evaluation is not a critical-exponent estimate. So C2 fails in the broad reading and holds only when both $\mathcal{E}$'s are cut down to the small fragment on which the algebraic identity binds. This is exactly Poincaré–Bayle's diagnosis; my framing places it as restriction-dependence of C2 rather than as a list of three failed checks. (I do not think this is a deeper result; it is the same result said algebraically.)

**Freud.** The hardest case, and the one that motivated the construction. The hydraulic mechanism transfers: $\phi(h) = c$ is well-defined. The evidential acts of Helmholtzian physics - calorimetric, manometric - have no content-preserving images in the analytic domain. There is no $\psi$ in **Dom\*** that sends "measure heat dissipation associated with emotional release" to anything; that procedure is simply absent from the target's evidence-space. C2 fails on the strongest possible grounds: not "the square has a wrong value" but "no candidate $\psi$ exists in the refined category." This is the *missing-analog* failure mode, distinct from Mehta–Schwab's *wrong-analog* mode.

I had hoped, going in, to find a more discriminating verdict between Freud and Mehta–Schwab. The framework gives one: the species of failure are different. Freud is structurally cleaner - the target's procedure-space does not even contain the right kind of observation; Mehta–Schwab is the case where the observations are present but bind differently. Two failure modes of C2, both diagnostic, with different repair strategies (Freud: enlarge $\mathcal{E}_T$; Mehta–Schwab: restrict $\mathcal{M}$).

## What I did not get to

I had wanted to formalize the construction in Lean. I declined this in the proposal already, but my reading of Buzzard last week reinforced the call: Mathlib4's category-theory library is in fact ready for this (the diagram is a one-chase), but the project would discover essentially nothing the diagram does not already show. Formalization is the right next move for the *Mehta–Schwab identity itself*, not for this framing of it.

I also did not work the directional asymmetry as hard as I wanted to. The construction predicts that the obstructions to transferring "more-structured into less-structured" and the reverse are different invariants (extension versus restriction problems on $r_S(\mathcal{M}_S) \subseteq 2^{\mathcal{E}_S}$). I noted this in the spec response and have not made it sharper here. It is on the open-problems list.

## What I'll say in the draft

The strong conjecture failed; the refined conjecture holds. The contribution is the inter-domain category, the necessity of content-preserving $\psi$ (which is the *residual algebraic structure* Montaigne's prose implicitly required), and the reclassification of the three conditions as existence/structure/non-degeneracy. The three cases instantiate the three regimes the framework predicts. Honest about what was over-stated in the proposal sketch.
