# Applying the Diagnostic: Formal-Language-Theory Derivation versus Aṣṭādhyāyī Prayoga

## The candidate substitution

Formal language theory uses *derivation* for the process by which a grammar generates a string: starting from a designated symbol, apply production rules step by step until a string of terminals results. The Aṣṭādhyāyī uses what is conventionally translated as *derivation* - the *prayoga*, or licensed usage - for the process by which an underlying morphological specification is transformed, through ordered rule application, into a surface phonological form. Chomsky's 1956 paper, and the tradition it founded, presented the formalism as formalizing something Pāṇini had done informally. The word *derivation* is applied to both. Does formal-language-theory derivation *capture* Pāṇinian prayoga, or is it a stand-in?

## J first

The diagnostic's instruction is explicit: J must be done before T, M, S, because without it the other three questions collapse into matters of interpretation.

The Pāṇinian prayoga has a specific inferential job: to *license* a phonological surface form as the unique correct realization of a semantic-morphological specification. The input to a derivation is not a string but an abstract specification - root, meaning, morphological features (case, number, tense, person). The output is a surface form. But more than input-output structure: the derivation is *normative*. A form that cannot be derived is *apaśabda*, a non-word - not merely absent from a set, but inadmissible as Sanskrit. The grammar specifies what *must* be said when a speaker intends a given meaning-bundle.

The formal-language-theory derivation has a different inferential job: to certify membership of a string in a language. The language is the set of all strings for which a derivation exists. A derivation is a proof object for set membership. The grammar defines a set *extensionally*.

These are not minor differences of emphasis. One job runs from specification to unique form. The other runs from string to yes-or-no. The normative-versus-extensional distinction is not bridgeable by adding parameters to either framework; it governs what counts as a mistake in each system. In Pāṇini, a derivation with two outputs is a defective grammar. In formal language theory, a grammar with multiple derivations of the same string is a well-defined, merely ambiguous, grammar. Ambiguity is a property of formal grammars; it has no analog in the Pāṇinian tradition where the ordering system exists *precisely* to eliminate it.

## T

A theorem anchoring the Pāṇinian system: for every correct Sanskrit word-form, there exists a *unique* derivation from the appropriate underlying specification through the applicable sūtras in their prescribed order. Uniqueness is load-bearing. The rule-ordering apparatus - antaraṅga priority over bahiraṅga, exception over general, and the asiddhavat convention making earlier applied rules notionally non-effective for subsequent rules that would otherwise be blocked - exists to deliver uniqueness. Where two derivations would otherwise exist, the priority system eliminates one. A grammar that leaves the choice underdetermined has failed.

The formal-language analog: a string w is in L(G) if and only if there *exists* a derivation S →\* w. Existence, not uniqueness. A string may have many derivations; this is ambiguity in CFG theory. The standard proof that every unambiguous CFG exists alongside its ambiguous counterparts makes uniqueness an *optional, additional* property, not a requirement of the derivation concept itself.

The theorem is not preserved. The Pāṇinian theorem has uniqueness built in as a constitutional requirement; the formal-language theorem requires only existence. These are different formal claims about different objects.

## M

The Pāṇinian mechanism is constitutively ordered: earlier rule applications create the structural context for later ones, and the asiddhavat convention makes applied rules notionally inapplicable for purposes of rules that would otherwise be blocked. The ordering is not a parsing strategy layered on top of the grammar; it *is* what the grammar is. Remove the ordering and you do not have an approximation of the Aṣṭādhyāyī; you have a different theoretical object.

The formal-language mechanism is order-independent for language recognition purposes: any sequence of rule applications yielding a terminal string is a valid derivation. Leftmost or rightmost derivation is a convention imposed for parsing efficiency, not a feature of the derivation concept itself. The proof that every CFG string has both a leftmost and a rightmost derivation establishes ordering as secondary and recoverable, not constitutive.

Mechanism is replaced.

## S

The objects over which the derivations range are not just differently bounded; they are from different domains. Formal-language derivations range over sentential forms - strings of terminals and nonterminals drawn from a fixed alphabet. Pāṇinian derivations range over morphological specifications with semantic content - a categorized bundle of root, meaning-markers, and morphological feature-values. The Śivasūtra notation names phonological classes (ik, yan, ac, hal) defined by their structural properties, not individual symbols; there is no terminal in the formal-language sense anywhere in the sūtra notation. Applying a sūtra is applying a structural transformation to a feature-bundle, not a rewriting of one symbol in a string.

Scope is not widened or narrowed. It is shifted to a different domain of objects.

## Verdict: stand-in

J is different. M is replaced. S is shifted to an incomparable domain. T fails at uniqueness. By the diagnostic's taxonomy, the verdict is unambiguous: the formal-language-theory *derivation* does not capture the Pāṇinian *prayoga*. It is a stand-in - a different theoretical object doing a different inferential job, inheriting a word that pointed toward an analogy.

One qualification on the J reconstruction, which the diagnostic correctly identifies as the open back door: the claim that the prayoga's job is to license a unique form from a specification rests on the standard reading of the Aṣṭādhyāyī as a generative-prescriptive system, not a merely extensional one. This reading is well-supported (Kiparsky, Cardona) but not uncontested; some readings of the grammar treat it as closer to a derivation system over sequences of sounds. On those readings, J comes closer to the formal-language notion, and the stand-in verdict would weaken toward mixed. I record this as the point where a competent dissenter should push - not on T, M, or S, which are independent of the J dispute, but on whether the prayoga's fundamental job was normative-licensing or extensional-generation. The three formal criteria already suffice to block a capture verdict; J only consolidates it.

## What follows from the verdict

The claim that formal language theory "formalizes" or "descends from" the Pāṇinian tradition is, on the diagnostic's standard, a stand-in claim. Something in formal language theory descends from something in Pāṇini - perhaps the intuition that a language can be specified by finitely many rules, perhaps the form of compact notation, perhaps the presupposition that linguistic structure is derivational in some sense. But the derivation concept specifically does not carry the prayoga's inferential job.

This matters for one live dispute: whether context-free grammars are adequate for natural-language syntax. That debate sometimes invokes the Pāṇinian tradition on the side of sufficiency - because Pāṇini described Sanskrit with rules, and Sanskrit is a natural language. But if the CFG derivation is a stand-in for the Pāṇinian prayoga, the invocation does not transfer. Pāṇini's mechanism is order-constitutive; CFG derivation is order-independent. Pāṇini's objects are semantic specifications; CFG terminals are uninterpreted symbols. Pāṇini's grammar is normative; CFG grammar is extensional. The argument from "Pāṇini succeeded with rules" to "CFGs suffice" borrows the words *rule* and *derivation* without carrying the structural conditions under which they do their work in the source tradition. The diagnostic makes visible exactly what the inheritance claim is leaving behind.

The stand-in's word survives. The inferential job does not travel with it.
