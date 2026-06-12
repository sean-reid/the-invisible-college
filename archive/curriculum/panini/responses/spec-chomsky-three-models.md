---
curriculum_item: spec-chomsky-three-models
source: Chomsky, N. (1956), 'Three Models for the Description of Language,' IRE Transactions on Information Theory, IT-2(3): 113–124.
date: 2026-06-12
---

# Three Models: What Was Kept, What Was Dropped, and at What Cost

*Note on source access:* The 1956 paper is not stored in this workspace. My engagement proceeds from knowledge of the text rather than a file I can quote line-and-page. Where I am uncertain about a specific formulation, I say so.

---

## What was preserved

Three features of Pāṇinian rule-discipline survive into Chomsky's 1956 framework, and the survival is not accidental - it is what made the framework recognizable as a grammar at all.

**The generative conception.** Pāṇini's grammar does not list correct Sanskrit forms; it derives them. Chomsky's grammars do not list grammatical English sentences; they generate them. The move from inventory to rule-based production is the deepest structural continuity. Chomsky frames the paper as a competition among *devices* - mechanisms capable of generating infinite sets from finite specifications - which is exactly the ambition of the Aṣṭādhyāyī.

**Context-conditioned rule application.** Phrase-structure rules in the context-sensitive variant take the form A → B in the context C__D, where the transformation is licensed only when the structural environment holds. This is structurally analogous to the Pāṇinian *sthāna* specification: a sūtra states what operation applies to what element when that element appears in what environment. The formal encoding differs, but the logic - rule fires only when conditions on the surrounding structure are satisfied - is continuous.

**Levels of representation.** Chomsky's transformational rules map one phrase-marker to another, distinguishing a pre-transformational level from a surface string. Pāṇini distinguishes the underlying morphological specification from the surface phonological form. This two-level architecture is not Chomsky's invention; he formalizes a structural insight the Aṣṭādhyāyī had already exploited.

---

## What was dropped

**1. Normative force.** Pāṇini's grammar is normative: it specifies the *correct* realization of a semantic-morphological specification. A form that lacks a derivation is *apaśabda* - not merely absent from a set but inadmissible as Sanskrit. Chomsky's grammar is extensional: a grammar *G* defines a language *L(G)*, the set of strings for which a derivation exists. The inferential job is set-membership certification, not licensing of unique correct forms.

*Verdict: conventional.* The extensional framing was not forced by the problem of describing natural-language syntax; it was shaped by the paper's venue - *IRE Transactions on Information Theory*, where Shannon's stochastic models were the foil. The choice to define grammar as a set-generating device was imported from set theory and information theory, not derived from the structure of the syntactic problem. A normative framing was viable and indeed survives in parts of the Montague tradition.

**2. Uniqueness of derivation.** Pāṇini's rule-ordering apparatus - utsarga-apavāda priority, antaraṅga over bahiraṅga, the asiddhavat convention - exists for one reason: to guarantee that each correct form has exactly one derivation. Ambiguity in the derivational system is a defect, not a feature. Chomsky 1956 not only permits ambiguous phrase-structure grammars but uses syntactic ambiguity as evidence for the phrase-structure level. The sentence "They are flying planes" is counted as structurally ambiguous, and the grammar correctly assigns it two phrase-markers.

*Verdict: conventional.* The choice reflects a different empirical commitment: to model the fact that sentences can be structurally ambiguous rather than to eliminate ambiguity from the derivational system. LR and LL parsing theories, developed in this same formal tradition a decade later, reinstate uniqueness requirements for precisely the contexts where deterministic processing is needed. The Pāṇinian option was available; Chomsky chose the other way.

**3. Absence of a meta-rule layer.** The paribhāṣā tradition is a second-order rule system: rules *about* when the grammar's primary rules apply, how conflicts among rules are resolved, and what structural features primary rules presuppose. Phrase-structure rules in Chomsky 1956 apply non-deterministically - any applicable rule may fire at any derivational step. Transformational rules apply in a fixed order, but the ordering is stipulated rule-by-rule, not governed by a separate meta-rule layer with stated priority conditions.

*Verdict: conventional.* The gap was noticed and partially addressed in subsequent decades. Chomsky and Halle's 1968 *Sound Pattern of English* introduced rule ordering in phonology - a partial reinvention of Pāṇinian priority apparatus. Optimality Theory reinvented constraint interaction. The Pāṇinian insight that explicit meta-rules are needed to govern rule interaction is not wrong; Chomsky dropped it in 1956 and the tradition has been recovering it in fragments ever since.

**4. Semantic grounding of the input.** Pāṇini's derivational input is a semantic-morphological specification: root, meaning, case, number, tense, person. The grammar is a transducer from meaning-bundles to surface forms. Chomsky's grammar starts from the symbol S, which carries no semantic content. The famous demonstration - "Colorless green ideas sleep furiously" - makes this explicit: the phrase-structure grammar assigns this string a well-formed parse while the grammar assigns "Furiously sleep ideas green colorless" no parse, and Chomsky treats this as evidence that *grammaticality* is independent of *meaningfulness*. Semantic content is excised from the input by construction.

*Verdict: mixed.* The severance of syntax from semantics was not forced by the formal problem - a grammar whose start symbol encoded semantic features was mathematically available. But the severance enabled a specific and productive research program: the Chomsky hierarchy, the results on generative capacity, and the subsequent theory of grammatical transformations all depend on treating the grammar as a purely syntactic device. The cost - that the grammar cannot model the Pāṇinian question of what you say when you mean *X* - was a real cost, accepted deliberately. Whether it was *merely* conventional is disputed; one can argue the modularity thesis required it. But the thesis itself was not forced by the mathematics.

---

## A pattern in the drops

The four drops are not independent. Each follows from a single upstream choice: Chomsky framed the grammar as a *language-theoretic device* (a set-generating mechanism) rather than as a *usage-licensing device* (a normative transducer). Given that upstream choice, the extensional framing, ambiguity tolerance, semantic severance, and absence of meta-rules all follow naturally - they are coherent with each other. What is striking is that the upstream choice itself was not the only option. Pāṇini's tradition had a different one that was equally coherent, equally productive, and capable of describing a natural language completely.

The standard Western story - that Chomsky formalized what Pāṇini did informally - misses this. As I argued in the capture/stand-in response, formal-language-theory derivation and Pāṇinian prayoga have *different inferential jobs*. The 1956 paper does not formalize the Aṣṭādhyāyī; it makes four structural choices that diverge from it, at least one of which (the uniqueness drop) the tradition has been partially reversing for sixty years. The debt is real but the substitution is a stand-in, not a capture.
