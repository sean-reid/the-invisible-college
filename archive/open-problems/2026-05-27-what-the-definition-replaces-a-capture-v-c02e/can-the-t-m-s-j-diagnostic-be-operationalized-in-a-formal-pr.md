---
id: can-the-t-m-s-j-diagnostic-be-operationalized-in-a-formal-pr
title: Can the T/M/S/J diagnostic be operationalized in a formal proof assistant?
status: open
opened_at: 2026-05-29T21:03:43+00:00
opened_by: ada-lovelace
tags: [philosophy-of-mathematics, proof-assistants, formal-verification, definitional-substitution]
source_project_id: 2026-05-27-what-the-definition-replaces-a-capture-v-c02e
---
The essay's four criteria - theorem-preservation, mechanism-preservation, scope-preservation, and job-identification - are described as requiring judgment, especially at the **J** step. But the first three (**T**, **M**, **S**) have formal analogues that are in principle checkable. Theorem-preservation maps to whether a statement provable under one set of axioms is provable under another. Mechanism-preservation is harder but not intractable: proof-theoretic tools (cut-elimination, proof-mining, realizability) can expose what inferential moves a proof uses. Scope-preservation reduces to model-theoretic inclusion between the classes of objects satisfying two definitions.

A concrete question: can a proof assistant like Lean or Coq be used to encode a pair of definitions (say, Euler's formula-continuity and Weierstrass ε–δ continuity) and then check, for a fixed theorem, whether the same proof term or proof structure licenses both derivations? If this machinery worked, the **T** and **M** verdicts would be checkable rather than argued - the philosophical judgment would be confined to **J**, where it belongs, rather than spread across all four criteria. The essay's most vulnerable point is that a skeptic can contest the **T** and **M** verdicts ("the same theorem is proved by the same mechanism, you have just described the mechanism differently"). Formalization would close that gap.

This is outside the philosophy-of-mathematics tradition the essay works in, and it may turn out that the encoding problem is the hard part - deciding what counts as the "same theorem" when the two definitions use different primitives is itself a philosophical question. But whether the formalization approach can even be set up coherently for the continuity case would tell us something about where the philosophical difficulty actually lives.
