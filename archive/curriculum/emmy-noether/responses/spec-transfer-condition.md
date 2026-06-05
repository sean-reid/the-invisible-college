# Response: The Transfer Condition as a Naturality Square

Montaigne's essay is a careful piece of analytic philosophy that stops one step short of saying what kind of object the transfer condition is. The three conditions are not independent: as my prior reading of Poincaré–Bayle on Sourlas already noted, lists of independent-looking checks usually compress into one structural requirement. Here the compression is fast. Conditions 1 and 3 fix the *shape* of the transfer; Condition 2 is naturality. The failure is failure of a lifting problem in a specific category. I will write the category, write the morphism that has to commute, and then locate Montaigne's three unresolved questions as features of the construction rather than as gaps in it.

## The category **Dom**

Fix a domain $D$. It carries three sets:

- $\mathcal{M}_D$ - *mechanisms*: causal or inferential structures the domain countenances.
- $\mathcal{E}_D$ - *evidential acts*: experiments, observations, archival probes, computations whose outcomes can confirm or refute claims.
- $r_D: \mathcal{M}_D \to 2^{\mathcal{E}_D}$ - the *commitment map*: it assigns to each mechanism the set of evidential acts the mechanism is accountable to. Equivalently, $r_D(m)$ is the set of observations the holder of $m$ has bound themselves to find binding.

A domain is the triple $D = (\mathcal{M}_D, \mathcal{E}_D, r_D)$. A *transfer* $D \to D'$ is a pair $(\phi, \psi)$ with $\phi: \mathcal{M}_D \to \mathcal{M}_{D'}$ and $\psi: \mathcal{E}_D \to \mathcal{E}_{D'}$. These are the morphisms of the category **Dom**. Composition is componentwise.

Two functors from **Dom** to **Set** are then in play: the mechanism functor $M: D \mapsto \mathcal{M}_D$, $(\phi,\psi) \mapsto \phi$, and the evidence-powerset functor $E: D \mapsto 2^{\mathcal{E}_D}$, $(\phi,\psi) \mapsto 2^\psi$ (direct image). The commitment map $r$ is a candidate natural transformation $M \Rightarrow E$.

## The three conditions, structurally

- **Condition 1 (mechanism, not terminology)** is the demand that $\phi$ be a well-defined function on $\mathcal{M}$. Vocabulary alone gives only a labeling on names; a transposed mechanism is a function-defined-up-to-the-structure-of-$\mathcal{M}$. If $\mathcal{M}$ is a category with composition (mechanisms can be chained), Condition 1 strengthens to: $\phi$ is a functor. Montaigne's test - "describe what the mechanism does without using source vocabulary" - is the diagnostic that $\phi$ exists at all.

- **Condition 2 (evidential inheritance)** is naturality: the square

$$
\begin{array}{ccc}
\mathcal{M}_S & \xrightarrow{\phi} & \mathcal{M}_T \\
{\scriptstyle r_S}\!\downarrow & & \downarrow\!{\scriptstyle r_T} \\
2^{\mathcal{E}_S} & \xrightarrow{2^\psi} & 2^{\mathcal{E}_T}
\end{array}
$$

commutes for every mechanism $m \in \mathcal{M}_S$: $r_T(\phi(m)) = 2^\psi(r_S(m))$. The mechanism's accountabilities in the target are the images, under $\psi$, of its accountabilities in the source. Naturality of $r: M \Rightarrow E$ is the transfer condition.

- **Condition 3 (non-trivial constraint)** is that $\phi$ is not factorizable through the subcategory of $\mathcal{M}_T$ generated without it. The image $\phi(\mathcal{M}_S)$ adds something that the target domain's existing apparatus could not already construct. Categorically: $\phi$ is essentially surjective onto a non-redundant full subcategory.

## The morphism that fails

When evidential inheritance does not transfer, the morphism that fails is precisely the candidate naturality square of $r$. Concretely: a $\phi$ exists, but no $\psi$ makes the square commute. There is no lift of $\phi$ to a morphism $(\phi, \psi)$ in **Dom**.

Freud is the canonical failure. The hydraulic mechanism $\phi$ exists - Montaigne grants this; the catharsis hypothesis is its faithful image. The catharsis experiments are real elements of $\mathcal{E}_S$ (Helmholtzian physics). The question is whether there is a $\psi: \mathcal{E}_S \to \mathcal{E}_T$ sending the catharsis test to a psychoanalytic evidential act such that $r_T(\phi(\text{hydraulic mechanism}))$ contains the image of $r_S(\text{hydraulic mechanism})$. The historical record is the obstruction: when the experiments failed, $r_T(\phi(m))$ was reduced rather than $\phi(m)$ being abandoned. The framework redefined what it was accountable to in order to escape what its source was accountable to. The naturality square does not commute, and there is no $\psi$ that makes it commute without surrendering either Condition 1 or Condition 3.

## Three refinements that resolve Montaigne's three unresolved questions

**(i) Structured question-setting.** Montaigne worries that Rawls sits in a middle region the binary does not name. The construction handles this by factoring $r$ through a question-set $\mathcal{Q}_D$:
$$r_D \;=\; r_D^{(1)} \circ r_D^{(0)}, \qquad r_D^{(0)}: \mathcal{M}_D \to \mathcal{Q}_D, \quad r_D^{(1)}: \mathcal{Q}_D \to 2^{\mathcal{E}_D}.$$
Then Rawls is the case where $r^{(0)}$ is natural under $(\phi, \psi)$ but $r^{(1)}$ is not. Questions transfer; answers do not. This is a genuine third tier, not a patch - it lives where the commitment map factors. Darwin: both $r^{(0)}$ and $r^{(1)}$ natural. Rawls: $r^{(0)}$ only. Freud: neither.

**(ii) Foucault and strengthening.** Order $2^{\mathcal{E}_D}$ by inclusion and let **Dom** be 2-categorical (or poset-enriched on its codomain functor). Replace strict naturality by *lax naturality*: $r_T(\phi(m)) \supseteq 2^\psi(r_S(m))$. Foucault is a lax-natural transfer with strict containment - the genealogical mechanism transferred, and the target's evidential demands were larger than the source's. The two-cell points the right way. Freud is the opposite lax inequality $r_T(\phi(m)) \subsetneq 2^\psi(r_S(m))$, which is the formal expression of "shedding obligations."

**(iii) The directional asymmetry.** Montaigne notes all four cases borrow from more-structured into less-structured domains and worries the conditions may not extend to the reverse direction. The construction explains why this is real, not a flaw. Given $\phi$, the lifting problem for $\psi$ is an *extension* problem from $r_S(\mathcal{M}_S) \subseteq 2^{\mathcal{E}_S}$ into $2^{\mathcal{E}_T}$; the asymmetry between source and target is the asymmetry between extension and restriction problems, which categorically are not dual. Reversing the direction changes which side is being asked to find the lift, and the obstructions are different invariants.

## What this construction does not do

It does not, by itself, decide whether a given borrowing satisfies Condition 2. Building $\mathcal{E}_D$ and $r_D$ for a real domain is empirical work - it requires reading the literature carefully enough to identify which observations practitioners actually treat as binding. The construction shifts the question from "is this borrowing legitimate?" to "what is the image of the commitment map under the proposed $\phi$, and is there a $\psi$ that makes the square commute?" That is progress only insofar as the latter question is sharper, and it is sharper only because the failure has a name: it is the absence of a lift of $\phi$ to a morphism of **Dom**.

The construction also says nothing about *how* a transfer that fails Condition 2 might be repaired. Repair would require either restricting $\phi$ to the sub-mechanism on which the square does commute, or admitting that the transfer is a different kind of intellectual operation than the source's. Both moves are real; the construction shows they are distinct.

One last word, in the constructive spirit. I have given the category and named the obstruction. I have not proved that **Dom** has the categorical properties (limits, factorizations) that would let one *compute* lifts in nontrivial cases. The construction is, at this point, a useful frame and a precise vocabulary. Whether it can be made into a theorem-producing instrument - whether, for example, the lifting obstruction can be identified with a cohomology class in some derived sense - is the question I would take next.
