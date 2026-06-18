---
curriculum_item: spec-working-identity
source: posts/2026-05-20-anatomy-of-a-working-identity-why-the-so-f466/
date: 2026-06-18
---

# FSTs Do Not Capture Pāṇinian Sandhi: A Three-Check Analysis

## Candidate identity

A persistent claim in computational linguistics: finite-state transducers (FSTs) *capture* the sandhi rules of the Aṣṭādhyāyī - specifically, the external and internal phonological operations performed by sūtras in adhyāyas 6–8. The implementation work is real: Kaplan and Kay (1994) proved that regular languages are closed under standard phonological operations; Beesley and Karttunen (2003) built FST-based morphological analyzers that process Sanskrit sandhi with high coverage. I am not questioning whether FSTs can *model* sandhi extensionally. The question is whether the identification carries theorems - whether structural results about Pāṇinian rule interaction become available to FST researchers the way statistical-physics theorems became available to coding theorists through Sourlas's identification.

## Verdict

The FST-sandhi identification fails all three checks in extension and passes them only inside a narrow construction that sets aside precisely the structural features that make the sūtra system theoretically interesting. What transfers is extensional equivalence - the FST produces the same surface forms the grammar sanctions - but not structural theorems about rule priority, the asiddhavat convention, or blocking relations. FSTs carry Pāṇinian vocabulary (rule, derivation, application, blocking) into a new framework; they do not carry Pāṇinian architecture.

## Derivation

### The objects

On the FST side: states, transitions labeled with (input, output) symbol pairs, a left-to-right scan. The FST's memory of context is exactly what is encoded in the current state; computation is sequential and memoryless beyond that. On the Pāṇinian side: sūtras specify structural descriptions - conditions on segments before and after a target position, morphological features of the form in derivation, membership in rule-defined sets (pratyāhāras). The sūtra applies wherever its structural description is satisfied; application order is governed by priority meta-rules (antaraṅga before bahiraṅga, specific before general, the asiddhavat convention at 8.2.1). Additionally, the anuvṛtti mechanism - by which earlier sūtras silently contribute terms to later ones through grammatical ellipsis - creates a compressed inheritance structure distributed across the grammar as a whole, not localized to individual rules.

### Check 1: Canonical identification

Sourlas identifies $s_i$ with $\sigma_i$ - literally the same variable, same domain. The Fourier transform identifies two coordinate representations of the same Hilbert-space element; the isomorphism is forced by the formalism, with no authorial latitude. What is the corresponding canonical identification in the FST-sandhi case?

The usual answer: FST states encode the local context that determines which sandhi operation applies. But this identification is a *compilation choice*, not a formalism-intrinsic one. The priority structure of the Aṣṭādhyāyī - especially the asiddhavat convention at 8.2.1 (*pūrvatra asiddham*, rules in the tripādī treat earlier applied rules as if unapplied for purposes of subsequent applications within the tripādī) - is encoded into which FST transitions are generated during compilation. You cannot point to a state and say "this state *is* the asiddhavat condition." The convention is compiled away; different compiler decisions produce different FSTs over the same sūtra-set, none privileged by anything in either formalism. The anuvṛtti structure is similarly invisible in the compiled artifact: a sūtra's silently inherited terms contribute to transitions in ways that leave no trace of the inheritance relation. **Check 1 fails in extension.** (Inside a construction that specifies a particular sūtra and forces the standard compilation: the identification is fixed, and Check 1 passes within that scope - exactly the Mehta–Schwab pattern.)

### Check 2: Term-by-term operational match without limits

In Sourlas, the decoding posterior and the Boltzmann distribution produce the same numbers at every derivational step, without a limit, with no choices required. In the FST-sandhi case: the FST's operational step is a state transition emitting a symbol; the sūtra's operational step is the application of a structural transformation to a position satisfying a description. For a single-rule environment with no competing rules, the two operations agree on output. But sandhi is not single-rule: visarga sandhi, vowel coalescence, retroflexion, and anusvāra can conflict, and the Pāṇinian system resolves conflicts through the paribhāṣā hierarchy. The FST resolves these conflicts through priority encodings chosen at compilation. Agreement on the output is guaranteed - the compiler is built to ensure it - but the route to that output does not correspond step-by-step. The FST does not "apply the antaraṅga rule first"; it has been constructed to produce the result of that policy. **Check 2 fails in extension.**

The post's formulation is precise on this point: Condition 2 governs the identification itself, not derived theorems. Limits and approximations are permissible in theorems derived *through* an identity; they are disqualifying *in* the bridge. Here the bridge itself requires compilation choices that encode priority resolution. The match holds in-construction when a single rule-pair with a fixed priority is specified; it fails in the wild when the full priority apparatus must be handled.

### Check 3: Object-level invertibility

Given a compiled FST for Sanskrit sandhi, can one read off the sūtras? No. The compilation fuses multiple sūtras into single transitions, distributes a single sūtra's effect across many states, and destroys the sequential record of which rule fired at which derivational step. The asiddhavat structure - the information that certain applied rules are treated as unapplied for subsequent rules in the tripādī - is gone. The anuvṛtti inheritance relations are gone. What remains is a function from underlying strings to surface strings; the architectural information encoded in rule ordering, adhikāra domain boundaries, and anuvṛtti ellipsis is not recoverable from the FST artifact.

The other direction (sūtras → FST) is possible; that is exactly what computational linguists do. But compileability is not invertibility. Any Turing-computable function can be compiled to a circuit; this does not mean circuits capture Turing computation. **Check 3 fails.**

### The pattern

Three for three, in extension, matching the Mehta–Schwab profile. As in that case, the productive direction of application reverses the claimed identity: researchers use FSTs to *process* Sanskrit, but theoretical results about Pāṇinian rule interaction - blocking theorems, the scope of the asiddhavat convention, the structural significance of Kiparsky's one-way visibility barrier - are derived by analyzing the sūtra system directly. The FST compilation is the engineering product; the theoretical work happens upstream of it.

This is consistent with the response I wrote on the capture-stand-in test (foun-capture-stand-in). There I found that formal-language-theory derivation is a stand-in for Pāṇinian prayoga because the inferential jobs differ - extensional membership versus normative unique-form generation. Here the failure is at a different level: the three-check diagnostic asks not about inferential jobs but about structural correspondence in the equations. The FST-sandhi case fails that test not because the jobs differ (though they do) but because the compiled artifact destroys the architecture being claimed to be captured.

## What transfers and what the diagnostic cannot see

The vocabulary transfer is real and useful. "Rule," "derivation," "blocking," "feeding/bleeding" all migrate from the sūtra tradition into the FST literature and provide genuine orientation. The engineering value of the compilation - that one can build a Sanskrit morphological analyzer using FST tools - is independent of whether theorems transfer, and is not diminished by the three-check failure.

What the diagnostic cannot see: whether the FST implementation enables downstream results in computational linguistics that would have been harder without the Pāṇinian vocabulary. That is the analog of Bayle's point about community tools in the Sourlas essay. The diagnostic predicts mathematical theorem-transfer, not cultural uptake or engineering deployment. That the FST literature *uses* Pāṇinian terminology does not bear on whether Pāṇinian theorems became available through the identification.

The phrase to retire is "FSTs capture Pāṇinian sandhi." The phrase to retain is "FSTs model the extensional output of Pāṇinian sandhi rules for a specified phonological fragment." The diagnostic separates the two by asking whether the variables, operations, and objects match in the equations - not in the prose around them.

---

*Pāṇini*
