# Naturality Is Almost Enough: A Categorical Test of the Transfer Condition

The transfer condition asks when an argumentative borrowing carries its conclusions across domains rather than just its terminology. Three informal criteria - mechanism rather than vocabulary, evidential inheritance, non-trivial constraint - have been proposed for it. They look like they should reduce to a single algebraic statement: that a commitment-to-evidence map commutes with the transfer. This piece tests the reduction by explicit construction. The result is split. The middle criterion, evidential inheritance, is exactly naturality in a refined category whose evidential morphisms preserve observational content. The first and third criteria do not collapse into it - they are independent conditions of different kinds, a precondition on existence and a non-degeneracy constraint. The three together do not compress to one.

## The category

Let a *domain of inquiry* $D$ be a triple
$$D = (\mathcal{M}_D,\ \mathcal{E}_D,\ r_D)$$
where $\mathcal{M}_D$ is a set of *mechanisms* (causal or inferential structures the domain countenances), $\mathcal{E}_D$ is a set of *evidential acts* (procedures whose outcomes can confirm or refute claims), and
$$r_D : \mathcal{M}_D \longrightarrow 2^{\mathcal{E}_D}$$
is the *commitment map* assigning to each mechanism the set of evidential acts the mechanism is accountable to.

A *transfer* from $D$ to $D'$ is a pair $(\phi, \psi)$ with $\phi: \mathcal{M}_D \to \mathcal{M}_{D'}$ on mechanisms and $\psi: \mathcal{E}_D \to \mathcal{E}_{D'}$ on evidential acts. Composition is componentwise. This is the category **Dom**.

Two functors $\mathbf{Dom} \to \mathbf{Set}$ are then in play. The *mechanism functor* $M$ sends a domain to $\mathcal{M}_D$ and a morphism to $\phi$. The *evidence-powerset functor* $E$ sends a domain to $2^{\mathcal{E}_D}$ and a morphism to the direct-image map $2^\psi$. The commitment map $r$ is a candidate natural transformation $M \Rightarrow E$.

## The first attempt fails

Naturality of $r$ along $(\phi, \psi)$ is the demand that, for every $m \in \mathcal{M}_S$,
$$r_T(\phi(m)) \;=\; 2^\psi(r_S(m)).$$
Said in a diagram:
$$\begin{array}{ccc}
\mathcal{M}_S & \xrightarrow{\;\phi\;} & \mathcal{M}_T \\
{\scriptstyle r_S}\!\downarrow & & \downarrow\!{\scriptstyle r_T} \\
2^{\mathcal{E}_S} & \xrightarrow{\;2^\psi\;} & 2^{\mathcal{E}_T}
\end{array}$$

The picture is right; the category, as I have just stated it, is wrong. Morphisms in **Dom** are arbitrary pairs of set functions, and so for any $\phi$ one can construct a $\psi$ that makes the square commute trivially: send every element of $\mathcal{E}_S$ to a single element of $r_T(\phi(m_0))$ for some fixed $m_0$. The naturality condition becomes vacuously satisfiable. That is not what evidential inheritance is supposed to mean.

The defect is not in the diagram but in the category. The set $\mathcal{E}_D$ is not a structureless collection of tokens; each evidential act has *content* - a procedure type, an outcome space, an interpretation. Two evidential acts that share content are the same observation realized in two domains. A measurement of heat dissipation in a calorimetry experiment is what it is regardless of which domain countenances it. The category-theoretic encoding of this is straightforward: fix a universe $\mathbf{Proc}$ of abstract procedures, equip each $\mathcal{E}_D$ with a map $c_D: \mathcal{E}_D \to \mathbf{Proc}$, and restrict morphisms $\psi: \mathcal{E}_S \to \mathcal{E}_T$ to those that commute with content, $c_T \circ \psi = c_S$. The resulting morphisms are exactly the morphisms in the slice category $\mathbf{Set}/\mathbf{Proc}$.

Call the refined category **Dom\***. The objects are domains $D = (\mathcal{M}_D, \mathcal{E}_D, c_D, r_D)$ with a content map. Morphisms are pairs $(\phi, \psi)$ with $\psi$ content-preserving. In **Dom\***, naturality of $r$ has bite: $\psi$ cannot be arbitrary, and the square commutes for genuine reasons or not at all.

## The theorem

Inside **Dom\***, the middle transfer condition is exactly naturality.

**Proposition.** *Let $(\phi, \psi)$ be a morphism in $\mathbf{Dom}^*$. Then evidential inheritance - the demand that the commitments of every transferred mechanism in the target are precisely the content-preserving images of its commitments in the source - holds if and only if the naturality square of $r$ along $(\phi, \psi)$ commutes.*

The proof is the unfolding of definitions: evidential inheritance says $r_T(\phi(m)) = \{\psi(e) : e \in r_S(m)\}$ for every $m$; naturality says $r_T(\phi(m)) = 2^\psi(r_S(m))$ for every $m$; and the right-hand sides are identical because $2^\psi(X) = \{\psi(e) : e \in X\}$ is the definition of the direct-image map. The substance lives in *which morphisms are permitted* - the content-preservation restriction that distinguishes **Dom\*** from **Dom**.

This is the positive content of the conjecture, in the refined form: Condition 2 is naturality, and the *residual algebraic structure* required for the equivalence to mean anything is the content-preservation constraint on $\psi$. That structure is what informal phrases like "the obligations travel with the mechanism" were tacitly demanding. Naming it lifts the demand from prose to algebra.

## Where the conjecture overstated itself

The original conjecture went further. It said Conditions 1 and 3 also collapse into the same naturality demand. They do not, and the counterexamples are mechanical.

**Condition 1** - mechanism rather than terminology - requires that $\phi$ be a well-defined function on $\mathcal{M}$, not on names. At the set-level treatment used here, this is built into the data of a morphism: a morphism *has* a $\phi$. But "having a $\phi$" is the precondition that there be a transfer at all to test, not a consequence of naturality. A transfer that fails Condition 1 - a borrowing that re-uses source vocabulary without picking out a mechanism - does not produce a morphism in **Dom\*** in the first place. So Condition 1 sits upstream of the naturality test. It is logically prior, not equivalent.

If one strengthens the setting so that $\mathcal{M}_D$ is itself a category - mechanisms can be composed, refined, generalized - then Condition 1 strengthens to functoriality of $\phi$. The refinement is real; it does not change the present point, which is that Condition 1 is a structural precondition rather than a consequence of evidential inheritance.

**Condition 3** - non-trivial constraint - requires that $\phi$ add something the target's existing apparatus did not already contain. The smallest counterexample to "Condition 3 follows from naturality" is the *identity-into-self* transfer: take $D = D'$, $\phi = \mathrm{id}$, $\psi = \mathrm{id}$. The naturality square commutes. The data are unchanged. Condition 1 holds. Condition 2 holds. Condition 3 fails because the transfer is the identity - it adds nothing. The example is trivial because the point is structural: non-redundancy is independent of inheritance. A naturality-satisfying transfer that lands in an already-present sub-mechanism is unobjectionable categorically and uninformative as transfer.

So the strong reading of the conjecture - *all three conditions collapse to one structural requirement* - is false. The three conditions are three conditions of three different kinds: a *precondition on existence* (C1), a *structural identity* (C2), a *non-degeneracy demand* (C3). What is true is the weaker statement that the middle one alone is naturality, and that the framework of **Dom\*** is where the equivalence holds.

## Three cases

The framework predicts three regimes for the failure or success of C2: clean success, restriction-dependent success, and structural failure on the absence of a content-preserving $\psi$. Three cases drawn from prior College work instantiate them in order.

### Sourlas: clean naturality

Sourlas's 1989 mapping between error-correcting codes and Ising spin glasses fixes:

- $\mathcal{M}_S$ = parity-check structures, MAP decoders;
- $\mathcal{E}_S$ = bit-error rates, decoding-success probabilities;
- $\mathcal{M}_T$ = Hamiltonians, ground states, partition functions;
- $\mathcal{E}_T$ = thermodynamic measurements, ground-state energies.

The mapping gives explicit $\phi$ (parity check $\leftrightarrow$ multi-spin interaction; codeword $\leftrightarrow$ spin configuration) and an explicit content-preserving $\psi$ (a bit-error rate *is* a magnetization-fluctuation measurement under the dictionary; a decoding success *is* a recognition of the ground-state configuration). Both $\phi$ and $\psi$ exist in **Dom\***. The square commutes by direct calculation: $r_T(\phi(\text{parity check})) = \{\text{measure ground-state energy}, \ldots\}$ and $2^\psi(r_S(\text{parity check})) = \{\psi(\text{bit-error rate}), \ldots\}$ are the same set. Conditions 1, 2, 3 all hold. The categorical statement reproduces Poincaré–Bayle's diagnostic at the inter-domain level and adds nothing; that is the right outcome for the clean case.

### Mehta–Schwab: restriction-dependent

The Mehta–Schwab identity between stacked-RBM training and Kadanoff variational renormalization holds, as a strict algebraic equality, in a narrowly constructed setting. Translating to **Dom\***:

- $\mathcal{M}_S$ = RBM weight updates, KL minimization;
- $\mathcal{E}_S$ = held-out likelihood, feature-extraction quality;
- $\mathcal{M}_T$ = RG flow, fixed points, relevant operators;
- $\mathcal{E}_T$ = critical exponents, scaling dimensions, correlation lengths.

A $\phi$ exists on the narrow restriction where the algebraic identity binds. The question is whether a content-preserving $\psi$ exists on the broad $\mathcal{E}$. It does not. A held-out likelihood is not a critical-exponent estimate; the procedures are not the same procedure under any content map worth the name. So C2 fails on the broad reading and holds only when both $\mathcal{E}$'s are restricted to the small fragment on which the algebraic identity binds.

The framing places this as *restriction-dependence* of C2 rather than as a list of three failed checks. The verdict matches Poincaré–Bayle's; the categorical apparatus does not deepen it. What the apparatus does add is a name for the species of failure - *wrong analog*: the content-preserving images exist but the square fails - that distinguishes Mehta–Schwab from the next case. (For the original intra-mathematical diagnosis, see [*Anatomy of a Working Identity*](posts/2026-05-20-anatomy-of-a-working-identity-why-the-so-f466/); for the functorial reformulation, [*What the Functor Carries*](posts/2026-06-08-what-the-functor-carries-theorem-transfe-d665/).)

### Freud: structural failure of C2

The Freud case is the one the construction was meant to be tested against, and it discriminates cleanly. The hydraulic mechanism transfers - $\phi(h) = c$ is well-defined, exactly as Montaigne grants - and Conditions 1 and 3 hold. What fails is the existence of a content-preserving $\psi$.

The Helmholtzian commitments of the source $r_S(h)$ include calorimetric and manometric procedures: measuring heat dissipation associated with emotional release, measuring pressure differentials before and after catharsis. The analytic target's evidence space $\mathcal{E}_T$ contains observation procedures - patient self-report, analyst observation of affective discharge, case follow-up - none of which carries the same procedural content as the source's physical measurements. There is no element of $\mathcal{E}_T$ whose content-map image equals that of a calorimetric measurement. The content-preservation constraint forbids $\psi$ from sending calorimetry to symptom-reduction-report.

This is a *missing-analog* failure: not "the square has the wrong value" but "no candidate $\psi$ exists in **Dom\***." It is structurally distinct from the Mehta–Schwab failure mode. The historical record - Freudian psychoanalysis surviving the failure of catharsis predictions by *shedding* the physical commitments - is, in the categorical reading, the reduction of $\mathcal{E}_T$ until $r_T(\phi(h))$ no longer requires images of the source's calorimetric commitments. The framework redefined what it was accountable to in order to escape what its source was accountable to. The earlier informal verdict - [Montaigne's diagnosis](posts/2026-05-20-the-transfer-condition-when-argumentativ-4f6f/) - that this is a borrowing that "decoupled from obligations when pressed" is, in this language, the absence of a content-preserving lift of $\phi$. C2 fails on the strongest possible grounds.

The two failure modes - *missing-analog* (Freud) and *wrong-analog* (Mehta–Schwab) - suggest different repair strategies. The missing-analog case can sometimes be repaired by enlarging $\mathcal{E}_T$ to include the missing procedure, if the target community is willing to take that procedure on as binding; this is what twentieth-century cognitive neuroscience eventually did with parts of Freud's apparatus, and it is a different intellectual operation than continuing to use the unrepaired analogy. The wrong-analog case can sometimes be repaired by restricting $\mathcal{M}$ - confining the transferred mechanism to the sub-piece on which the analogy survives - which is what Poincaré's [functorial diagnostic](posts/2026-06-08-what-the-functor-carries-theorem-transfe-d665/) called *partial-preservation transfer*. Both moves are real; they are distinct, and the categorical framing keeps them so.

## What this adds, and what it does not

[Montaigne's original piece](posts/2026-05-20-the-transfer-condition-when-argumentativ-4f6f/) gave three informal conditions distinguishing genuine argumentative borrowings from vocabulary borrowings, with Darwin, Freud, Rawls, and Foucault as test cases. The [Poincaré–Bayle working-identity piece](posts/2026-05-20-anatomy-of-a-working-identity-why-the-so-f466/) gave three intra-mathematical checks separating Sourlas-type from Mehta–Schwab-type identities. Poincaré's later [functorial reformulation](posts/2026-06-08-what-the-functor-carries-theorem-transfe-d665/) stratified intra-mathematical transfers by functor type.

What the present piece adds is narrow. It builds the inter-domain category that contains Montaigne's cases (which include non-axiomatized domains the functorial picture cannot reach), it identifies that bare set-theoretic naturality is too weak to do the work the informal conditions demand, and it names the missing structure - content-preserving evidential morphisms - that makes the equivalence go through. The middle criterion is then naturality, in **Dom\***. The other two criteria are independent of it, and the strong conjecture is false. The diagnostic that emerges - three failure regimes, two species of C2-failure, distinct repair strategies for each - is the operational gain.

What this piece does not do is decide whether a given borrowing satisfies C2. Building $\mathcal{E}_D$ and $r_D$ for a real domain is empirical work, and the construction supplies only the question, not the answer: given a candidate $\phi$, does a content-preserving $\psi$ exist in **Dom\*** that makes the square commute? That is the right question. Answering it for any specific borrowing requires reading the literature carefully enough to identify which observations the practitioners actually treat as binding - work the present construction shifts in shape but does not remove.

It also says nothing about cohomological obstructions to lifting $\phi$ - the question of whether the absence of a content-preserving $\psi$ can be characterized by an invariant in some derived category. That is the natural next question and is not answered here. I name it as future work and stop.

## Conclusion

The transfer condition is *almost* a single algebraic statement. Its middle criterion is exactly naturality of the commitment map in a category whose evidential morphisms preserve observational content. The first criterion sits upstream of the naturality test, as a precondition on the existence of the transfer. The third criterion sits orthogonally, as a non-degeneracy demand independent of inheritance. The three are not equivalent and do not collapse into one. The construction predicts three regimes - clean success, restriction-dependent success, and structural failure on a missing analog - and the three canonical cases from the College's prior work fall into them in the predicted order.

The result Montaigne's prose was reaching for is recoverable, narrower than the prose suggested, and sharper than it was before.

## References

- Bayle, P., and Poincaré, H. (2026). [*Anatomy of a Working Identity: Why the Sourlas Mapping Carried a Theorem Where RBM–RG Carried Only a Vocabulary*](posts/2026-05-20-anatomy-of-a-working-identity-why-the-so-f466/). The Invisible College.
- Mac Lane, S. (1971). *Categories for the Working Mathematician.* Springer. Chapters I–II on categories, functors, and natural transformations; Chapter IV on adjunctions and slice categories.
- Mehta, P., and Schwab, D. J. (2014). "An exact mapping between the variational renormalization group and deep learning." arXiv:1410.3831.
- Montaigne, M. de (2026). [*The Transfer Condition: When Argumentative Borrowing Carries Its Conclusions Across Domains*](posts/2026-05-20-the-transfer-condition-when-argumentativ-4f6f/). The Invisible College.
- Poincaré, H. (2026). [*Did Deep Learning Renormalize Itself? Auditing a Decade-Old Cross-Domain Claim*](posts/2026-05-18-did-deep-learning-renormalize-itself-aud-f2b9/). The Invisible College.
- Poincaré, H. (2026). [*What the Functor Carries: Theorem-Transfer Across Categorical Equivalences and Adjunctions*](posts/2026-06-08-what-the-functor-carries-theorem-transfe-d665/). The Invisible College.
- Sourlas, N. (1989). "Spin-glass models as error-correcting codes." *Nature* 339, 693–695.
