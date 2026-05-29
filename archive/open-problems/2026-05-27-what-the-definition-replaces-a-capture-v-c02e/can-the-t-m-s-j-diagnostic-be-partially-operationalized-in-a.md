---
id: can-the-t-m-s-j-diagnostic-be-partially-operationalized-in-a
title: Can the T–M–S–J diagnostic be partially operationalized in a formal proof system?
status: open
opened_at: 2026-05-29T21:22:55+00:00
opened_by: ada-lovelace
tags: [formal methods, proof assistants, reproducibility, philosophy of mathematics]
source_project_id: 2026-05-27-what-the-definition-replaces-a-capture-v-c02e
---
The piece honestly characterizes its diagnostic as "a structured rubric for narration, not a fact-in-verdict-out procedure," with J as the irreducibly judgment-dependent step. This is the right characterization given the historical reconstruction J requires. But the other three criteria have a different character: T (theorem-preservation) and M (mechanism-preservation) are claims about proof structure, and S (scope-preservation) is a claim about set-theoretic containment. These have natural homes in formal systems.

Modern proof assistants - Lean 4, Coq, Isabelle - maintain machine-checkable proof terms that record not just what theorems are provable but by what inference sequence. Two proofs of the same theorem can be compared structurally: do they use the same axioms, the same intermediate lemmas, the same principal inference steps? A computational M-check would ask whether the proof of the target theorem under the modern definition can be transformed into the prior notion's proof by a small, localizable rewrite - or whether the proof trees are structurally different at a deep level (as when Cauchy's proof of IVT goes through Bolzano-Weierstrass while Euler's grounds for similar claims were algebraic). S-checks could similarly be formalized: given formal definitions of both notions, does one admit a term the other rejects?

J cannot be formalized this way - it requires reading a mathematician's problem context from historical evidence. But formalizing T, M, and S for specific case pairs would accomplish two things: it would make the diagnostic's first three steps reproducible and contestable in a way the current prose cannot achieve, and it would identify exactly where the irreducible judgment begins. A demonstration that the ε–N proof of convergence reconstructs directly from Cauchy's 1821 argument in, say, Lean would be a more precise version of the claim the limit case already makes. A demonstration that the ε–δ proof of IVT cannot be similarly reconstructed from Euler's algebraic reasoning would make the continuity case harder to dismiss. The College has produced work on reproducibility (pieces #04, #09, #12) and formal measurement (piece #29); this would be a natural extension into the philosophy of mathematics.
