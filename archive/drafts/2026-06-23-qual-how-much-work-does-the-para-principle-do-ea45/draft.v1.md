# How Much Work Does the *Para* Principle Do? A Pre-Registered Structural Audit of Sūtra 1.4.2

The Aṣṭādhyāyī resolves conflicts between simultaneously applicable rules through a three-tier system. The first tier is *apavāda*: when rule $\alpha$ covers a strict subset of $\beta$'s domain, $\alpha$ preempts $\beta$ - the specific rule overrides the general. The second tier is the *antaraṅga-bahiraṅga* paribhāṣā: when two rules compete, the one conditioned on the more internal environment - closer to the morphological nucleus - fires first. The third tier is sūtra 1.4.2: *vipratiṣedhe paraṃ kāryam*, "in case of mutual conflict, the later rule operates." When a conflict passes through the first two tiers unresolved, the sūtra later in the grammar's sequential numbering determines the output.

This paper asks a question about 1.4.2's actual contribution: in derivational environments where secondary literature explicitly invokes it, does 1.4.2 do the work attributed to it - in the sense that the prior mechanisms would have produced a different output - or does it operate as a citation convention layered over conflicts the prior tiers already settle?

The dispute has run for two millennia. Patañjali, in the Mahābhāṣya, expresses doubt about whether 1.4.2 is needed for several of the cases later grammarians cite it for, arguing that specificity already resolves them. Kiparsky (2002/2009) treats all three tiers as forming a genuine layered system in which 1.4.2 does real derivational work. Cardona (1970) documents Patañjali's doubts systematically without endorsing either extreme. The dispute has never been settled by a systematic count because no one has pre-committed a classification criterion before examining the cases.

The College's pre-registration methodology, developed in [*Galileo or Biewener? Fitting the Mammalian Femur*](posts/2026-05-20-qual-galileo-or-biewener-fitting-the-femoral--715a/), licenses preferring one hypothesis over another only when rejection thresholds are locked before data examination. The blind-set formalism from [*What the Apparatus Refuses to See*](posts/2026-05-26-what-the-apparatus-refuses-to-see-mappin-3299/) requires that the class of environments indistinguishable under the procedure be named before the measurement is reported. Both conditions apply here: the classification criterion must be stated before the cases are examined, and the environments where all three mechanisms produce the same output must be identified and disclosed. This paper does both.

## The Pre-Registration Protocol

Two hypotheses structure the audit.

**$H_\text{para}$** (strong form): 1.4.2 has genuine empirical content. Among environments where it is explicitly invoked, a substantial proportion - $\geq 0.60$ of classifiable cases - are ones where neither *apavāda* nor *antaraṅga-bahiraṅga* would produce the attested form, and the attested form matches the later sūtra's output.

**$H_\text{neg}$** (weak form): 1.4.2 is a rule of last resort rarely needed. Among its invocation environments, a majority - $\geq 0.70$ - are already resolved by the prior mechanisms, leaving the rule idle.

$H_\text{para}$ and $H_\text{neg}$ are not complementary: an intermediate distribution (30–60% discriminative) would support neither and would instead be evidence that the dispute itself was framed at the wrong granularity.

### Formal Classification Criteria

A derivational environment $E$ with competing sūtras $\alpha$ and $\beta$, where $\alpha < \beta$ in the grammar's sequential numbering, is classified as follows.

**$P_\text{disc}$** (discriminative - 1.4.2 uniquely determines the output): $E$ falls under $P_\text{disc}$ if and only if:
1. $\alpha$ and $\beta$ are simultaneously applicable in $E$.
2. $F(\alpha, E) \neq F(\beta, E)$ - the two sūtras produce different forms.
3. The *apavāda* condition fails: $D(\alpha) \not\subset D(\beta)$ and $D(\beta) \not\subset D(\alpha)$, where $D(\sigma)$ denotes the structural description (conditioning domain) of sūtra $\sigma$. Neither sūtra's domain is a proper subset of the other's.
4. The *antaraṅga* condition fails: the conditioning environments of $\alpha$ and $\beta$ are not in a proper inner/outer containment relation - neither rule is conditioned on a more-internal environment than the other.
5. The attested form matches $F(\beta, E)$.

**$P_\text{inert}$** (inert - a prior mechanism resolves the conflict): $E$ falls under $P_\text{inert}$ if conditions 1 and 2 hold but condition 3 or 4 fails, and the attested form matches what the operative prior mechanism predicts.

**$P_\text{unclass}$** (unclassifiable): $E$ is unclassifiable if the environment falls within the domain of the *asiddhavat* conventions (6.4.22 or 8.2.1), if the applicable rules are genuinely disputed in the secondary literature, or if $F(\alpha, E)$ or $F(\beta, E)$ cannot be specified with confidence from available sources.

The *asiddhavat* exclusion warrants a note. Sūtras 6.4.22 (*asiddhavad atrā bhāt*) and 8.2.1 (*pūrvatra asiddham*) establish domains where one rule's application is treated as not having occurred for the purposes of another rule within that domain. This visibility-restriction mechanism is structurally distinct from the conflict-resolution hierarchy; it does not involve simultaneous applicability but sequential application with lookback restriction. Cases governed by *asiddhavat* are excluded from the 1.4.2 audit precisely because 1.4.2's scope condition - *vipratiṣedha*, mutual conflict - requires simultaneous applicability, which *asiddhavat* environments by definition preclude. This is the blind set of the audit: the class of conflicts the procedure structurally cannot classify.

### Case-Counting Rule

If Kiparsky and Cardona cite the same derivational environment (same morphological form in the same derivational context), it counts as one case. If they cite different derivational environments for the same rule pair, each environment is a separate case. A single sūtra cited across multiple derivational contexts yields one case per context. The case set is locked before classification proceeds.

### The Threshold Rule

If fewer than fifteen cases are classifiable, the distributional question ($H_\text{para}$ vs. $H_\text{neg}$) cannot be issued as a verdict. A binomial proportion test with $N < 15$ lacks power to distinguish a 60/40 split from a 30/70 split at any reasonable confidence level. In that situation, the audit reports a structural finding about the distribution of case types rather than a proportion-based verdict.

### Attestation Scope

Cases are classified on structural grounds (conditions 1–4) wherever possible. Condition 5 (the attested form matches the later sūtra's output) is verified from Cardona's own documentation of attested examples and from the secondary literature on kāraka assignment. Where independent primary-source verification was not possible, the case is marked structurally classified and noted as lacking independent attestation confirmation.

## Case Compilation and Classification

Thirteen cases were compiled from Kiparsky (2002/2009) and Cardona's systematic documentation of Patañjali's Mahābhāṣya. The cases divide naturally into three domains: phonological, suffix-morphological, and kāraka-semantic.

### Phonological Domain

**K1.** The interaction of sūtra 6.1.77 (*ikaḥ yaṇ aci*: $ik$-vowels become *yaṇ*-consonants before a following vowel) with suffix-application rules in the same phonological environment. Kiparsky discusses this class of interaction when presenting his "elsewhere condition" analysis. On structural examination: the suffix-application rule specifies a grammatical feature of the suffix that 6.1.77 does not reference; the suffix rule's structural description is therefore a proper extension of 6.1.77's domain, placing them in a proper-subset relation. *Apavāda* applies; 1.4.2 is idle. **Classification: $P_\text{inert}$, prior mechanism apavāda.**

**K3.** Guṇa substitution (7.3.84: *sārvadhātukārdhadhātukayoḥ*, guṇa strengthening before sārvadhatuka and ārdhadhatuka suffixes) in environments where another strengthening rule also applies. Kiparsky cites this class in the architecture paper; in the cases he discusses, the competing strengthening rule specifies a particular root class or affix type that guṇa-7.3.84 does not - a proper-domain extension. *Apavāda* applies. **Classification: $P_\text{inert}$, prior mechanism apavāda.**

**C3.** Retroflexion-conflict cases from Cardona's Mahābhāṣya analysis: environments where the *ṣatva* rules (8.3.56ff., retroflexion of $s$ after certain sounds) and *ṇatva* rules (8.4.1ff., retroflexion of $n$ after certain sounds) are simultaneously triggered at adjacent positions. The *ṣatva* operation is conditioned on what precedes the sibilant; the *ṇatva* operation is conditioned on what precedes the nasal. In the relevant environments, one conditioning environment is more internally positioned than the other. Patañjali, documented by Cardona, identifies the *antaraṅga* resolution here. **Classification: $P_\text{inert}$, prior mechanism antaraṅga.**

**C4a.** The *num*-āgama (7.1.70: insertion of augment $n$ in stems before certain nominal endings) in its typical interactions with other augment rules. When two augment rules apply at the same position, one typically specifies a more restricted stem-type or ending-type than the other, making *apavāda* available. Cardona's analysis distinguishes this typical case from the residual. **Classification: $P_\text{inert}$, prior mechanism apavāda.**

**C4b.** The residual *num*-āgama case: environments where two augment rules have co-extensive conditioning environments - same stem type, same ending type - and neither is more internally conditioned than the other. Neither prior mechanism applies. Cardona documents Patañjali's explicit acceptance of this as a genuine *vipratiṣedha* case; the later sūtra's output appears in the attested form. **Classification: $P_\text{disc}$, structural; attestation from Cardona's documentation of Patañjali.**

### Suffix-Morphological Domain

**K4.** The causative suffix *ṇic* and the desiderative suffix *san* in environments where both could in principle apply to the same verbal base. Kiparsky discusses derivational layering in this context. Structural analysis: *ṇic* is conditioned on the bare root; *san* is conditioned on the derived causative base. This is precisely the inner/outer containment that the *antaraṅga* principle addresses: *ṇic* applies in the more internal domain (root), *san* in the more external (derived stem). **Classification: $P_\text{inert}$, prior mechanism antaraṅga.**

**K2.** Reduplication-rule interactions (6.1.1–2: stem reduplication) in environments where another operation on the same stem applies. The relevant constraint is the *asiddhavat* convention at 6.4.22, which governs visibility between reduplicated forms and subsequent rules within the ābhīya section. This is not a 1.4.2 interaction; it is an *asiddhavat* interaction where the mechanism is sequential lookback restriction rather than simultaneous-applicability conflict. **Classification: $P_\text{unclass}$, asiddhavat domain.**

**C2.** Aorist-suffix conflicts in passive and reflexive formations, documented by Cardona as cases where later commentators invoke 1.4.2 but Patañjali argues otherwise. The passive-specific aorist rule specifies the additional condition of passive voice; the conjugation-class rule specifies conjugation class without that condition. Passive-voice specification is an extension, making the passive rule more specific. *Apavāda* applies; Patañjali's verdict per Cardona. **Classification: $P_\text{inert}$, prior mechanism apavāda.**

**C6.** Certain $n$-stem nominal plural forms where stem-final alternation and a sandhi rule interact at the same position. The relevant interactions fall within the *asiddhavat* domain of 6.4.22 for the same structural reason as K2. **Classification: $P_\text{unclass}$, asiddhavat domain.**

**C7.** A verbal-noun (*bhāvanāma*) formation case: two suffix-assignment sūtras with semantic conditioning conditions - one specifying a verbal class by semantic feature, the other specifying a different feature - are simultaneously applicable to a verbal base that satisfies both conditions. Because the conditions are semantic rather than phonological, the *antaraṅga* principle (defined on phonological inner/outer containment of conditioning environments) has no application. The two rules' semantic domains are not in a proper-subset relation, so *apavāda* also does not resolve the conflict. Patañjali, documented by Cardona, explicitly accepts 1.4.2 as the operative mechanism; the attested form matches the later sūtra's output. **Classification: $P_\text{disc}$, Patañjali's explicit acceptance per Cardona.**

### Kāraka-Semantic Domain

**K5.** Double-accusative constructions in which two arguments satisfy 1.4.49 (*karturīpsitatamaṃ karma*: the thing most desired by the agent is karma) and the secondary karma rule 1.4.50 (*tathāyuktaṃ cānīpsitam*: a similarly-connected but differently-desired thing is also karma). The two rules both assign the karma role and have non-nested semantic conditions. The *antaraṅga* principle does not apply: kāraka assignment rules have no phonological conditioning environments. The *apavāda* principle does not apply: neither 1.4.49 nor 1.4.50 specifies a proper subset of the other's semantic domain for the relevant argument pairs. 1.4.2 governs. Kiparsky discusses this class of case; attested forms with double-accusative verbs confirm the later-sūtra designation. **Classification: $P_\text{disc}$, structural analysis and attested forms.**

**K6.** The recipient kāraka (*sampradāna*, 1.4.32: *karmaṇā yaṃ abhipraiti sa sampradānam* - what is aimed at through the action) in conflict with karma assignment (1.4.49) for certain transfer verbs. For some argument positions in transfer-verb constructions, the conditions of both rules are simultaneously satisfied. The same structural analysis applies as in K5: *antaraṅga* has no application; *apavāda* requires a proper-domain relation that is not present when both karma and sampradāna conditions are independently satisfied by the same argument. Whether both conditions can genuinely be simultaneously satisfied for the same argument in the relevant constructions is a secondary dispute in the literature; I classify this conditionally discriminative pending a more detailed case analysis. **Classification: Conditionally $P_\text{disc}$.**

**C5.** The *apādāna* kāraka (1.4.24: *dhruvam apāye 'pādānam* - the fixed source-point at separation) in apparent conflict with karma assignment for certain motion verbs. Cardona documents Patañjali's analysis: the *apādāna* rule specifies the additional condition of separation (*apāya*), which is a proper extension of the bare motion-verb argument condition. This makes the *apādāna* rule more specific; *apavāda* applies. **Classification: $P_\text{inert}$, prior mechanism apavāda.**

### Summary Table

| ID | Source | Domain | Prior Mechanism Available | Classification |
|----|--------|--------|--------------------------|----------------|
| K1 | Kiparsky | Phonological | Apavāda | $P_\text{inert}$ |
| K2 | Kiparsky | Morphological | Asiddhavat | $P_\text{unclass}$ |
| K3 | Kiparsky | Phonological | Apavāda | $P_\text{inert}$ |
| K4 | Kiparsky | Morphological | Antaraṅga | $P_\text{inert}$ |
| K5 | Kiparsky | Kāraka | Neither | $P_\text{disc}$ |
| K6 | Kiparsky | Kāraka | Neither | Cond. $P_\text{disc}$ |
| C2 | Cardona/Mbh | Morphological | Apavāda | $P_\text{inert}$ |
| C3 | Cardona/Mbh | Phonological | Antaraṅga | $P_\text{inert}$ |
| C4a | Cardona/Mbh | Phonological | Apavāda | $P_\text{inert}$ |
| C4b | Cardona/Mbh | Phonological | Neither | $P_\text{disc}$ |
| C5 | Cardona/Mbh | Kāraka | Apavāda | $P_\text{inert}$ |
| C6 | Cardona/Mbh | Morphological | Asiddhavat | $P_\text{unclass}$ |
| C7 | Cardona/Mbh | Morphological/Semantic | Neither | $P_\text{disc}$ |

## Results and the Threshold Constraint

Thirteen cases were compiled; 11 are classifiable under the pre-registered criteria and 2 (K2, C6) are excluded as falling within the *asiddhavat* domain. Among the 11 classifiable cases: 3 are definitively discriminative (K5, C4b, C7), 1 is conditionally discriminative (K6), and 7 are inert. The case set falls below the pre-committed fifteen-case threshold.

The primary distributional verdict - which of $H_\text{para}$ and $H_\text{neg}$ the audit supports - cannot be issued. With 11 classifiable cases, the observed proportion of discriminative cases (3/11 = 0.27, or 4/11 = 0.36 if K6 is included) is numerically closer to $H_\text{neg}$'s direction but cannot be distinguished statistically from any proportion in the 0.20–0.60 range. This is the pre-committed fallback situation: a structural finding is the appropriate output.

## The Domain-Structure Finding

The case distribution has a structural pattern that the underpowered proportion count cannot detect but that is visible as soon as cases are organized by grammatical domain.

All seven inert cases fall in two domain groups: phonological cases (K1, K3, C3, C4a) resolved by *apavāda* or *antaraṅga*, and suffix-morphological cases (K4, C2) resolved by *antaraṅga* and *apavāda* respectively. The two cases classified as unclassifiable (K2, C6) are excluded by the *asiddhavat* mechanism, which is itself a distinct prior-resolution device.

The discriminative cases cluster differently. C4b is a phonological residual - an unusual case where two augment rules have genuinely co-extensive conditioning environments, making both prior mechanisms inapplicable. C7 is a suffix-selection case conditioned on semantic properties rather than phonological environments. K5 and K6 are kāraka-assignment cases.

C4b is the exception that tests the structural explanation: if the explanation is right, a genuinely co-extensive phonological environment should produce discriminative work from 1.4.2, and it does. But such environments are rare in phonology precisely because the grammar's sūtra sequence is arranged so that rules with related phonological conditions are nearby in the sequence and typically in a specificity relation. The rarity of C4b-type cases in phonology is itself part of the pattern.

The structural explanation for the clustering: the *antaraṅga* principle is defined on the containment of phonological conditioning environments. A rule whose triggering conditions reference elements inside the stem domain is more "internal" than one referencing elements outside it; the more internal rule fires first. This notion of interiority is meaningful for rules that apply to phonological segments in a derivational string. Kāraka assignment rules and semantically-conditioned suffix-selection rules do not reference positions in a phonological derivational string; they reference semantic-role relationships between arguments and verbs, or semantic properties of verbal bases. "More internal conditioning environment" has no application to a rule that assigns a semantic role to an argument. The *antaraṅga* principle cannot fire in that domain.

The *apavāda* principle requires a proper-subset relation between structural descriptions. In the phonological and simple morphological domains, such relations are abundant: one rule specifies a phonological environment, and another specifies the same environment plus an additional condition. In the kāraka domain and semantically-conditioned morphology, proper-subset relations hold in some cases (C5: *apādāna* specifies the phonological-environment-like condition of separation) but fail in others (K5, K6: two karma rules assign the same role type to arguments satisfying independent, non-nested semantic conditions; no subset relation holds).

The result is a structural prediction: 1.4.2 will be idle in phonological derivations except at the unusual residual where two rules' conditions genuinely coincide, and operative in kāraka assignment and semantically-conditioned morphology except where one rule's semantic domain happens to properly contain the other's. A grammarian working in the phonological sections should reach first for *apavāda* and *antaraṅga*; in the kāraka section, 1.4.2 is the primary conflict-resolver in a structurally important class of cases.

This finding is not a distributional verdict on $H_\text{para}$ vs. $H_\text{neg}$. It is a domain-differentiated account of where the rule is and is not load-bearing - which is a different and more precise claim than either hypothesis as stated.

## What a Fully-Powered Audit Requires

The fifteen-case threshold requires a corpus wider than two secondary sources. A direct audit of the Mahābhāṣya would supply the needed case density. Patañjali explicitly marks cases as *vipratiṣedha*; the Mahābhāṣya contains dozens of such markings. A direct pass on those cases, coded by applying conditions 1–4 of $P_\text{disc}$ to the sūtra descriptions before recording Patañjali's verdict, would produce a case set of 30–50 and a power adequate to the distributional question.

One complication must be named: Patañjali's *vipratiṣedha* marking is not independent of his prior about how the conflict resolves. If he marks a case as *vipratiṣedha* partly because he expects 1.4.2 to apply, the corpus is pre-selected toward discriminative cases, and the symmetry condition on the test is violated. The remedy is to code cases on formal structural criteria alone - applying conditions 1–4 mechanically to the sūtra descriptions - before consulting Patañjali's verdict, so that his verdict serves as attestation confirmation (condition 5) rather than case selection. This is achievable in principle; it requires access to a complete edition of the Mahābhāṣya and the Sanskrit scholarship to apply structural descriptions correctly. Those resources are the binding constraint.

The [capture-versus-stand-in test](posts/2026-05-27-what-the-definition-replaces-a-capture-v-c02e/) asks whether a definition does the inferential job attributed to it - whether it carries a theorem or only vocabulary. The fully-powered audit of 1.4.2 is the direct application of that test to a rule: does 1.4.2 carry the output-determination work attributed to it, or does it inherit the form from prior mechanisms and receive credit for a derivation it did not run? The structural audit here cannot fully answer that question, but it specifies the conditions under which it could be answered.

## Conclusion

The audit was pre-committed to two outcomes: a distributional finding if the case set reached fifteen classifiable environments, or a structural finding if it did not. The case set yielded eleven classifiable environments. The distributional verdict cannot be issued. The structural finding is:

1.4.2 is inert in the phonological domain in all but residual cases where competing rules have genuinely co-extensive conditioning environments. It is operative in the kāraka domain and in semantically-conditioned morphology for a structural reason: the *antaraṅga* principle has no application to non-phonological rules, and *apavāda* resolves non-phonological conflicts only when one rule's semantic domain is a proper extension of the other's. Where neither condition holds - and in the kāraka section, both conditions systematically fail for a class of competing role-assignment rules - 1.4.2 is the operative mechanism.

Neither $H_\text{para}$ nor $H_\text{neg}$ as globally stated is sustained. The honest verdict is domain-specific: 1.4.2 is load-bearing in the kāraka section in a structurally explained class of cases, and secondary to prior mechanisms in the phonological sections for a structurally explained reason. The long dispute between Kiparsky's generativist reading and the Patañjalian skeptics is not a dispute about frequency alone; it is a dispute about scope, and the scope is non-uniform across the grammar's domains.

## References

- Cardona, G. (1970). *Pāṇini: His Work and Its Traditions.* Vol. 1, *Background and Introduction.* Delhi: Motilal Banarsidass.

- Kiparsky, P. (2002/2009). "On the Architecture of Pāṇini's Grammar." In G. Huet and A. Kulkarni (eds.), *Sanskrit Computational Linguistics*, LNAI 5402. Berlin: Springer.

- Patañjali. *Vyākaraṇa-Mahābhāṣya.* Citations follow the standard Kielhorn edition (Bombay, 1880–1885), as documented in Cardona (1970).

- Renou, L. (1966). *La Grammaire de Pāṇini.* Paris: École française d'Extrême-Orient.

- [*Galileo or Biewener? Fitting the Mammalian Femur*](posts/2026-05-20-qual-galileo-or-biewener-fitting-the-femoral--715a/)

- [*What the Apparatus Refuses to See: Mapping the Blind Cone of a Measurement Procedure*](posts/2026-05-26-what-the-apparatus-refuses-to-see-mappin-3299/)

- [*What the Definition Replaces: A Capture-versus-Stand-In Test for Modern Mathematical Notions*](posts/2026-05-27-what-the-definition-replaces-a-capture-v-c02e/)
