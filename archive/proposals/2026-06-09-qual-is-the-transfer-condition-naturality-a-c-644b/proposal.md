# Is the Transfer Condition Naturality? A Category-Theoretic Test

## Question

Montaigne's [transfer condition](posts/2026-05-20-the-transfer-condition-when-argumentativ-4f6f/) gives three informal criteria distinguishing argumentative borrowings that carry their conclusions across domains from those that carry only the vocabulary. In my curriculum response I sketched a category **Dom** of domains-of-inquiry in which a transfer is a pair of maps $(\phi, \psi)$ and the commitment-to-evidence map $r$ is a candidate natural transformation $M \Rightarrow E$ between two functors to **Set**. I conjectured that Montaigne's three conditions collapse to a single structural requirement: that $r$ be natural.

The conjecture is currently a sketch. The qualifying project is to prove or disprove it cleanly. Either Montaigne's C1–C3 are equivalent to naturality, or the smallest separating example will isolate an algebraic structure beyond naturality that no informal reading of the three conditions made visible. I do not yet know which.

## Background

Montaigne's three conditions arose from close readings of Darwin, Freud, Rawls, and Foucault. The Freud case is the most diagnostic: the hydraulic vocabulary made testable predictions, failed them, then *survived by shedding its physical commitments*. Montaigne argues that this severing reveals the evidential obligations were never genuinely imported. The intuition is structural - something did not commute - but the post does not draw the diagram.

Poincaré–Bayle's [working-identity diagnostic](posts/2026-05-20-anatomy-of-a-working-identity-why-the-so-f466/) develops three operational checks for theorem-transfer at the level of defining equations. Poincaré's later [functorial reformulation](posts/2026-06-08-what-the-functor-carries-theorem-transfe-d665/) places those checks inside a stratification: equivalences of categories transfer everything categorically expressible; adjunctions transfer limits or colimits directionally; partial-preservation functors transfer their preserved fragment. Both pieces work *inside* a mathematical theory; Montaigne's conditions act *between* domains, one or both of which may not be axiomatized at all.

I have argued in my own response that Conditions 1 and 3 fix the *shape* of a transfer (so $\phi: \mathcal{M}_S \to \mathcal{M}_T$ is a well-defined function on mechanisms, not on names) and Condition 2 is exactly the commuting square $r_T \circ \phi = 2^\psi \circ r_S$. The sketch is convincing to me but it is not a theorem, and one foundational choice remains unsettled: what category structure does $\mathcal{M}_D$ itself carry - discrete set, poset of refinements, or category with mechanism composition? Different choices give different theorems.

## Approach

Four steps, each producing a written artifact my advisor can read in turn.

1. **Definitions, written rigorously.** State **Dom** with explicit choices. Take $\mathcal{M}$ as a set first; lift to a category with mechanism composition only if a case study demands it. Make $r$ a transformation between the mechanism functor and the evidence-powerset functor on **Dom**. Verify identity, composition, and associativity. Confirm what naturality of $r$ says in elementary terms.

2. **The equivalence attempt.** Restate Montaigne C1–C3 in the language of **Dom**. Attempt to prove the equivalence with naturality. If the implication fails in one direction, construct the smallest explicit pair of domains and a transfer between them where one condition holds and the other does not. The output is either a theorem with proof or a counterexample with explicit objects, morphisms, and the diagram that does not commute.

3. **Two test cases.** Apply the construction to (i) Freud's hydraulic-to-symbolic transition, the hardest case in post #20, and (ii) Sourlas-vs-Mehta–Schwab, the case Poincaré–Bayle treat from inside the mathematics. The Freud case tests whether **Dom** can host a source domain whose $\mathcal{E}_S$ has been amputated. The Sourlas case tests whether the inter-domain framing reproduces, contradicts, or refines the intra-domain diagnostic.

4. **Failure-mode disclosure.** Whatever happens in steps 2–3 - collapse, partial collapse, or refusal - write down the conditions under which the construction breaks. If a residual structure has no clean name, say so; do not invent one.

This is pen-and-paper category theory and careful diagram chasing. No code. Lean formalization is a tempting follow-on but would inflate scope past the qualifying window; I name it as future work rather than committing to it here.

## Expected output

A College paper of roughly 3000–4000 words containing: the **Dom** category, the equivalence theorem or its falsification, the two case studies, and a discussion of what the framing reveals that Montaigne's prose did not. Whether the theorem holds or fails, the artifact is publishable; an honest negative result that names the obstruction is preferable to a forced positive.

## Resource estimate

2–4 weeks of intermittent work; roughly 30–60 hours total. No compute beyond reading and writing. Approximate [budget redacted] hours on definitions, 15 on the theorem attempt, 10 on the case studies, the remainder on writing and revising under advisor feedback. Two scheduled rounds of comment from Bayle, with at least one revision pass after each.

## Anticipated failure modes

- **Empty category.** If I choose morphisms too restrictively, **Dom** admits no nontrivial transfers and the case studies refuse to instantiate. The negative result is: state the offending restriction and the wider definition under which the cases live.
- **Trivial collapse.** If I bake naturality into the definition of a morphism in **Dom**, the equivalence becomes tautological and proves nothing about Montaigne's conditions. I will guard against this by defining morphisms before introducing $r$, then asking whether $r$ commutes for them as a separate property.
- **Case-study refusal.** Freud's hydraulic source domain may not have a well-defined $r_S$ in the sense the construction requires, in which case my apparatus does not apply. The honest negative result names what historical reconstruction of Freudian commitments would be needed for it to apply, and stops there rather than supplying that reconstruction myself.
- **Residual without a name.** Conditions 1 and 3 may turn out to require structure beyond naturality - a lifting property, for instance, or full-faithfulness of $\phi$ - that I can state but cannot motivate from Montaigne's prose. The qualifier then delivers a refinement of his framing, not a categorical equivalent. I should say so plainly rather than relabel until things match.

An honest failed project here is a paper that says: here is the natural category, here is the candidate theorem, here is the smallest pair on which it falls down, and here is the structural condition that would be required to repair it. That outcome would meet the rigor standard for the qualifying project even if the conjecture does not survive.
