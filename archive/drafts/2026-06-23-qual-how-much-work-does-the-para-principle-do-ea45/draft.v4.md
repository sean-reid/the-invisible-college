# How Much Work Does the *Para* Principle Do? A Pre-Registered Structural Audit of Sūtra 1.4.2

The Aṣṭādhyāyī resolves conflicts between simultaneously applicable rules through a three-tier system. The first tier is *apavāda*: when rule $\alpha$ covers a strict subset of $\beta$'s domain, $\alpha$ preempts $\beta$ - the specific rule overrides the general. The second tier is the *antaraṅga-bahiraṅga* paribhāṣā: when two rules compete, the one conditioned on the more internal environment - closer to the morphological nucleus - fires first. The third tier is sūtra 1.4.2: *vipratiṣedhe paraṃ kāryam*, "in case of mutual conflict, the later rule operates." When a conflict passes through the first two tiers unresolved, the sūtra later in the grammar's sequential numbering determines the output.

This paper asks a question about 1.4.2's actual contribution: in derivational environments where secondary literature explicitly invokes it, does 1.4.2 do the work attributed to it - in the sense that the prior mechanisms would have produced a different output - or does it operate as a citation convention layered over conflicts the prior tiers already settle?

The dispute has run for two millennia. Patañjali, in the Mahābhāṣya, expresses doubt about whether 1.4.2 is needed for several of the cases later grammarians cite it for, arguing that specificity already resolves them. Kiparsky (2002/2009) treats all three tiers as forming a genuine layered system in which 1.4.2 does real derivational work. Cardona (1970) documents Patañjali's doubts systematically without endorsing either extreme. The dispute has never been settled by a systematic count because no one has pre-committed a classification criterion before examining the cases.

The College's pre-registration methodology, developed in [*Galileo or Biewener? Fitting the Mammalian Femur*](posts/2026-05-20-qual-galileo-or-biewener-fitting-the-femoral--715a/), licenses preferring one hypothesis over another only when rejection thresholds are locked before data examination. The blind-set formalism from [*What the Apparatus Refuses to See*](posts/2026-05-26-what-the-apparatus-refuses-to-see-mappin-3299/) requires that the class of environments indistinguishable under the procedure be named before the measurement is reported. Both conditions apply here: the classification criterion must be stated before the cases are examined, and the environments where the procedure cannot detect whether 1.4.2 was operative must be identified and disclosed. This paper does both.

## The Pre-Registration Protocol

Two hypotheses structure the audit.

**$H_\text{para}$** (strong form): 1.4.2 has genuine empirical content. Among environments where it is explicitly invoked, a substantial proportion - $\geq 0.60$ of classifiable cases - are ones where neither *apavāda* nor *antaraṅga-bahiraṅga* would produce the attested form, and the attested form matches the later sūtra's output.

**$H_\text{neg}$** (weak form): 1.4.2 is a rule of last resort rarely needed. Among its invocation environments, a majority - $\geq 0.70$ - are already resolved by the prior mechanisms, leaving the rule idle.

These cutoffs were specified at the time of drafting rather than in the original research proposal; the proposal committed only to the fifteen-case threshold and to the $P_\text{disc}$ / $P_\text{inert}$ / $P_\text{unclass}$ classification scheme. The disclosure matters beyond protocol: even where the distributional verdict is not issued, the $H_\text{para}$ / $H_\text{neg}$ framing shapes how readers process the structural finding - the observed $3/8 = 0.375$ discriminative proportion is described below as "numerically closer to $H_\text{neg}$'s direction," and that characterization depends on the post-hoc thresholds. The fifteen-case threshold rests on a power estimate: a one-sided exact binomial test comparing $p = 0.60$ against null $p = 0.30$ achieves approximately $0.78$ power at $N = 15$, $\alpha = 0.05$; fifteen is a defensible minimum floor, not a guarantee of adequate power for subtler distinctions. Finally, the threshold was foreseeable as likely to fire: Kiparsky's case descriptions are class-level characterizations whose competing rules are unnamed; class-level entries route to $P_\text{unclass}$ under condition (d) regardless of how domain-subset analysis would resolve. The structural fallback was a genuine pre-committed contingency; the case-density limitation was nonetheless foreseeable from the outset.

$H_\text{para}$ and $H_\text{neg}$ are not complementary: an intermediate distribution ($0.30$–$0.60$ discriminative) would support neither and would instead be evidence that the dispute itself was framed at the wrong granularity.

### Formal Classification Criteria

A derivational environment $E$ with competing sūtras $\alpha$ and $\beta$, where $\alpha < \beta$ in the grammar's sequential numbering, is classified as follows.

**$P_\text{disc}$** (discriminative - 1.4.2 uniquely determines the output): $E$ falls under $P_\text{disc}$ if and only if:
1. $\alpha$ and $\beta$ are simultaneously applicable in $E$.
2. $F(\alpha, E) \neq F(\beta, E)$ - the two sūtras produce different forms.
3. The *apavāda* condition fails: $D(\alpha) \not\subset D(\beta)$ and $D(\beta) \not\subset D(\alpha)$, where $D(\sigma)$ denotes the structural description of sūtra $\sigma$. Neither sūtra's domain is a proper subset of the other's.
4. The *antaraṅga* condition fails: the conditioning environments of $\alpha$ and $\beta$ are not in a proper inner/outer containment relation - neither rule is conditioned on a more-internal environment than the other.
5. The attested form matches $F(\beta, E)$.

**$P_\text{inert}$** (inert - a prior mechanism resolves the conflict): $E$ falls under $P_\text{inert}$ if conditions 1 and 2 hold but condition 3 or 4 fails, and the attested form matches what the operative prior mechanism predicts.

**$P_\text{unclass}$** (unclassifiable): $E$ is unclassifiable if (a) the environment falls within the domain of the *asiddhavat* conventions (6.4.22 or 8.2.1); (b) condition 1 - simultaneous applicability - is itself in dispute in the secondary literature; (c) $F(\alpha, E)$ or $F(\beta, E)$ cannot be specified with confidence from available sources; or (d) the competing sūtras are not individually named in the source *and* their structural descriptions are insufficient to evaluate conditions 2–4 from available secondary-source characterizations. Note that (d) requires both elements: the absence of a sūtra number alone does not route an environment to $P_\text{unclass}$ if the structural descriptions of both rules' domains are sufficient to evaluate the domain-subset and conditioning-containment relations.

### Excluded Environments and the Blind Set

Two structurally distinct classes of environments fall outside the procedure's reach; they are not the same object and must be named separately.

The *excluded* class covers environments governed by the *asiddhavat* conventions (6.4.22 and 8.2.1). These sūtras restrict rule visibility by treating earlier applications as not having occurred for the purposes of later rules within their domains - a mechanism of sequential application with lookback restriction rather than simultaneous-applicability conflict. Sūtra 1.4.2's scope condition (*vipratiṣedha*: mutual conflict) requires simultaneous applicability, which *asiddhavat* environments preclude. These cases are not "blind" to the audit; the question of 1.4.2's contribution simply does not arise.

The *blind set* proper is the class of environments where all three tiers produce the same output form. In these cases the prior mechanism's winner happens to be the later sūtra - coinciding with what 1.4.2 would have predicted - and the audit cannot detect whether 1.4.2 was operative. The blind set falls within the $P_\text{inert}$ category: specifically, those $P_\text{inert}$ cases where the prior mechanism (*apavāda* or *antaraṅga*) happens to favor $\beta$ (the later sūtra) rather than $\alpha$. In contrast, when the prior mechanism favors the earlier sūtra $\alpha$ and the attested form accordingly matches $F(\alpha, E)$, the outcome is unambiguously diagnostic - the prior mechanism fired, not 1.4.2.

The five $P_\text{inert}$ cases admit the following partial enumeration. For **C5** (*apādāna* 1.4.24 vs karma 1.4.49): *apavāda* favors *apādāna* (1.4.24), which is $\alpha$ (1.4.24 < 1.4.49 in sequential numbering); the prior mechanism favors $\alpha$, making C5 definitively diagnostic - its output is unambiguously not what 1.4.2 would predict. For **K4** (*san* vs *ṇic*, *antaraṅga*): *antaraṅga* favors *ṇic* (root-conditioned, more internal); if *ṇic* is the later sūtra ($\beta$) in the 3.1 sequence, the prior mechanism favors $\beta$ and K4 is a blind-set member - but the sūtra-sequence order for this specific pair requires primary-source verification before the blind-set determination can be made definitively. For **C2**, **C3**, and **C4a**, the prior mechanism's winner relative to sequential ordering cannot be determined from available secondary-source characterizations; these cases remain unenumerated with respect to blind-set membership.

### Case-Counting Rule

If Kiparsky and Cardona cite the same derivational environment (same morphological form in the same derivational context), it counts as one case. If they cite different derivational environments for the same rule pair, each environment is a separate case. A single sūtra cited across multiple derivational contexts yields one case per context. The case set is locked before classification proceeds.

### The Threshold Rule

If fewer than fifteen cases are classifiable, the distributional question ($H_\text{para}$ vs. $H_\text{neg}$) cannot be issued as a verdict. In that situation, the audit reports a structural finding about the distribution of case types rather than a proportion-based verdict.

### Attestation Scope

Cases are classified on structural grounds (conditions 1–4) wherever possible. Condition 5 (the attested form matches the later sūtra's output) is verified from Cardona's documentation of attested examples and from the secondary literature on kāraka assignment. Where independent primary-source verification was not possible, the case is marked structurally classified and noted as lacking independent attestation confirmation.

Among the three discriminative cases specifically: K5 (double karma) draws condition-5 attestation from Kiparsky's discussion and the kāraka literature on double-accusative constructions, independently of Cardona. C4b and C7 are classified as $P_\text{disc}$ on Patañjali's explicit acceptance as documented by Cardona; Cardona is thus both the source for case identification and the source for condition-5 attestation in these two cases. This is a circularity: condition 5 for C4b and C7 rests on Cardona's mediated authority rather than independent primary-source verification. The limitation affects two of the three discriminative cases.

## Case Compilation and Classification

Thirteen cases were compiled from Kiparsky (2002/2009) and Cardona's systematic documentation of Patañjali's Mahābhāṣya. The Cardona-sourced cases are numbered C2 through C7; there is no C1. The first Cardona-sourced environment - the class of 6.1.77 interactions documented in the Mahābhāṣya - was treated as the same derivational class as K1 under the case-counting rule (same environment cited by multiple sources counts once) and was not assigned a separate identifier. This merger is revisited in the K1 entry below.

### Phonological Domain

**K1.** The interaction of sūtra 6.1.77 (*ikaḥ yaṇ aci*: $ik$-vowels become *yaṇ*-consonants before a following vowel) "with suffix-application rules in the same phonological environment" - Kiparsky's characterization in the architecture paper. This description names a class, not a specific derivational environment, and does not name the competing sūtra or characterize its structural domain. Without any structural description of the competing rule, conditions 2–4 cannot be evaluated - this is the condition that routes an environment to $P_\text{unclass}$ under criterion (d), not the mere absence of a sūtra number but the absence of any domain characterization. The same class-level description governs the C1 merger: what would have been C1 is not separately classifiable for the same reason. **Classification: $P_\text{unclass}$, competing rule unnamed and structurally uncharacterized.**

**K3.** Guṇa substitution (7.3.84: *sārvadhātukārdhadhātukayoḥ*, guṇa strengthening before sārvadhatuka and ārdhadhatuka suffixes) in environments where "another strengthening rule also applies" - again a class characterization in Kiparsky, with the competing rule unnamed and its domain uncharacterized. Conditions 3 and 4 cannot be evaluated. **Classification: $P_\text{unclass}$, competing rule unnamed and structurally uncharacterized.**

**C3.** Retroflexion-conflict cases from Cardona's Mahābhāṣya analysis: environments where the *ṣatva* rules (8.3.56ff., retroflexion of $s$ after certain sounds) and *ṇatva* rules (8.4.1ff., retroflexion of $n$ after certain sounds) are simultaneously triggered at adjacent positions. The *ṣatva* operation is conditioned on what precedes the sibilant; the *ṇatva* operation is conditioned on what precedes the nasal. In the relevant environments one conditioning environment is more internally positioned than the other. Patañjali, documented by Cardona, identifies the *antaraṅga* resolution here. **Classification: $P_\text{inert}$, prior mechanism *antaraṅga*. Blind-set status: uncertain (sūtra sequence for the favored rule not confirmed from available sources).**

**C4a.** The *num*-āgama (7.1.70: insertion of augment $n$ in stems before certain nominal endings) in its typical interactions with other augment rules. When two augment rules apply at the same position, one typically specifies a more restricted stem-type or ending-type than the other, making *apavāda* available. Cardona's analysis distinguishes this typical case from the residual. **Classification: $P_\text{inert}$, prior mechanism *apavāda*. Blind-set status: uncertain (specific competing sūtra not identified from available sources).**

**C4b.** The residual *num*-āgama case: environments where two augment rules have co-extensive conditioning environments - same stem type, same ending type - and neither is more internally conditioned than the other. Neither prior mechanism applies. Cardona documents Patañjali's explicit acceptance of this as a genuine *vipratiṣedha* case; the later sūtra's output appears in the attested form. **Classification: $P_\text{disc}$, structural; attestation from Cardona's documentation of Patañjali.**

### Suffix-Morphological Domain

**K4.** The causative suffix *ṇic* and the desiderative suffix *san* in environments where both could in principle apply to the same verbal base. Structural analysis: *ṇic* is conditioned on the bare root; *san* is conditioned on the derived causative base. This is precisely the inner/outer containment that the *antaraṅga* principle addresses: *ṇic* applies in the more internal domain (root), *san* in the more external (derived stem). **Classification: $P_\text{inert}$, prior mechanism *antaraṅga*. Blind-set status: *antaraṅga* likely favors $\beta$ (*ṇic*), placing K4 in the blind set - but sūtra-sequence order for this pair requires primary-source verification.**

**K2.** Reduplication-rule interactions (6.1.1–2: stem reduplication) in environments where another operation on the same stem applies. The relevant constraint is the *asiddhavat* convention at 6.4.22, which governs visibility between reduplicated forms and subsequent rules within the ābhīya section. This is not a 1.4.2 interaction; it is an *asiddhavat* interaction where the mechanism is sequential lookback restriction rather than simultaneous-applicability conflict. **Classification: $P_\text{unclass}$, *asiddhavat* domain (excluded).**

**C2.** Aorist-suffix conflicts in passive and reflexive formations, documented by Cardona as cases where later commentators invoke 1.4.2 but Patañjali argues otherwise. The passive-specific aorist rule specifies the additional condition of passive voice; the conjugation-class rule specifies conjugation class without that condition. The competing sūtras are not identified by number in the available secondary-source characterization - distinguishing this from K1 and K3 requires care. What is available is sufficient structural description to evaluate condition 3: the passive rule's domain (aorist formations with passive voice in a given conjugation class) is a proper subset of the conjugation-class rule's domain (all aorist formations of that conjugation class), establishing $D(\text{passive}) \subset D(\text{class})$ from the descriptions alone. Sūtra numbering would be needed to determine which is $\alpha$ and which is $\beta$ for the blind-set check; it is not needed to evaluate the domain-subset relation that grounds the *apavāda* classification. Passive-voice specification is an extension, making the passive rule more specific. *Apavāda* applies; Patañjali's verdict per Cardona. **Classification: $P_\text{inert}$, prior mechanism *apavāda*. Blind-set status: uncertain (sūtra sequence not confirmed).**

**C6.** Certain $n$-stem nominal plural forms where stem-final alternation and a sandhi rule interact at the same position. The relevant interactions fall within the *asiddhavat* domain of 6.4.22 for the same structural reason as K2. **Classification: $P_\text{unclass}$, *asiddhavat* domain (excluded).**

**C7.** A verbal-noun (*bhāvanāma*) formation case: two suffix-assignment sūtras with semantic conditioning conditions - one specifying a verbal class by semantic feature, the other specifying a different feature - are simultaneously applicable to a verbal base satisfying both conditions. Because the conditions are semantic rather than phonological, the *antaraṅga* principle (defined on phonological inner/outer containment of conditioning environments) has no application. The two rules' semantic domains are not in a proper-subset relation, so *apavāda* also does not resolve the conflict. Patañjali, documented by Cardona, explicitly accepts 1.4.2 as the operative mechanism; the attested form matches the later sūtra's output. **Classification: $P_\text{disc}$, Patañjali's explicit acceptance per Cardona.**

### Kāraka-Semantic Domain

**K5.** Double-accusative constructions in which two arguments satisfy 1.4.49 (*karturīpsitatamaṃ karma*: the thing most desired by the agent is karma) and the secondary karma rule 1.4.50 (*tathāyuktaṃ cānīpsitam*: a similarly-connected but differently-desired thing is also karma). The two rules both assign the karma role and have non-nested semantic conditions. The *antaraṅga* principle does not apply: kāraka assignment rules have no phonological conditioning environments. The *apavāda* principle does not apply: neither 1.4.49 nor 1.4.50 specifies a proper subset of the other's semantic domain for the relevant argument pairs. 1.4.2 governs. Kiparsky discusses this class of case; attested forms with double-accusative verbs confirm the later-sūtra designation. **Classification: $P_\text{disc}$, structural analysis and attested forms.**

**K6.** The recipient kāraka (*sampradāna*, 1.4.32: what is aimed at through the action) in conflict with karma assignment (1.4.49) for certain transfer verbs. Whether both conditions can genuinely be simultaneously satisfied for the same argument in the relevant constructions is a secondary dispute in the secondary literature. Condition 1 of $P_\text{disc}$ - simultaneous applicability - is itself in doubt. Under the pre-committed protocol, a case where condition 1 is unresolved routes to $P_\text{unclass}$; the protocol did not authorize a "conditionally discriminative" category. **Classification: $P_\text{unclass}$, condition 1 disputed.**

**C5.** The *apādāna* kāraka (1.4.24: *dhruvam apāye 'pādānam* - the fixed source-point at separation) in apparent conflict with karma assignment (1.4.49: *karturīpsitatamaṃ karma*) for certain motion verbs. Cardona documents Patañjali's analysis: the *apādāna* rule specifies the additional condition of separation (*apāya*), which is a proper extension of the karma assignment condition. This establishes $D(1.4.24) \subset D(1.4.49)$: the apādāna domain is a proper subset of the karma domain. *Apavāda* applies, favoring 1.4.24. Since 1.4.24 < 1.4.49 in sequential numbering, *apavāda* here favors $\alpha$ - making C5 definitively diagnostic rather than a blind-set member. **Classification: $P_\text{inert}$, prior mechanism *apavāda*. Blind-set status: diagnostic ($\alpha$ favored, definitively not in blind set).**

### Summary Table

| ID | Source | Domain | Prior Mechanism | Classification | Prior mech. favors |
|----|--------|--------|-----------------|----------------|--------------------|
| K1 | Kiparsky | Phonological | - | $P_\text{unclass}$ (rule uncharacterized) | N/A |
| K2 | Kiparsky | Morphological | Asiddhavat | $P_\text{unclass}$ (excluded) | N/A |
| K3 | Kiparsky | Phonological | - | $P_\text{unclass}$ (rule uncharacterized) | N/A |
| K4 | Kiparsky | Morphological | Antaraṅga | $P_\text{inert}$ | β (likely; unconfirmed) |
| K5 | Kiparsky | Kāraka | Neither | $P_\text{disc}$ | N/A |
| K6 | Kiparsky | Kāraka | - | $P_\text{unclass}$ (cond. 1 disputed) | N/A |
| C2 | Cardona/Mbh | Morphological | Apavāda | $P_\text{inert}$ | uncertain |
| C3 | Cardona/Mbh | Phonological | Antaraṅga | $P_\text{inert}$ | uncertain |
| C4a | Cardona/Mbh | Phonological | Apavāda | $P_\text{inert}$ | uncertain |
| C4b | Cardona/Mbh | Phonological | Neither | $P_\text{disc}$ | N/A |
| C5 | Cardona/Mbh | Kāraka | Apavāda | $P_\text{inert}$ | **α** (definitive) |
| C6 | Cardona/Mbh | Morphological | Asiddhavat | $P_\text{unclass}$ (excluded) | N/A |
| C7 | Cardona/Mbh | Morphological/Semantic | Neither | $P_\text{disc}$ | N/A |

## Results and the Threshold Constraint

Thirteen cases were compiled; 8 are classifiable under the pre-registered criteria and 5 are excluded or unclassifiable. Of the five unclassifiable cases: two (K2, C6) fall within *asiddhavat* domains and are out of scope entirely; two (K1, K3) lack named competing rules and any structural domain characterization, making conditions 2–4 formally unevaluable; one (K6) has condition 1 in dispute. Among the 8 classifiable cases: 3 are discriminative (K5, C4b, C7) and 5 are inert (K4, C3, C4a, C2, C5).

The case set falls well below the pre-committed fifteen-case threshold. The primary distributional verdict - which of $H_\text{para}$ and $H_\text{neg}$ the audit supports - cannot be issued. With 8 classifiable cases, the observed proportion of discriminative cases ($3/8 = 0.375$) is numerically closer to $H_\text{neg}$'s direction but cannot be distinguished statistically from any proportion in the $0.20$–$0.60$ range. This is the pre-committed fallback situation: a structural finding is the appropriate output.

## The Domain-Structure Finding

The case distribution has a structural pattern visible when cases are organized by grammatical domain. This organization is not a pre-committed axis of the audit; it emerged inductively after the cases were classified. The structural account that follows is a hypothesis the audit generates for a fully-powered follow-up to test, not a finding the pre-committed apparatus confirms.

Among the eight classifiable cases, all five inert cases involve prior mechanisms: the phonological domain contributes C3 (*antaraṅga*) and C4a (*apavāda*); the suffix-morphological domain contributes K4 (*antaraṅga*) and C2 (*apavāda*); the kāraka domain contributes C5 (*apavāda*). The three discriminative cases occupy different structural positions: C4b is a phonological residual where two augment rules have genuinely co-extensive conditioning environments; C7 is a suffix-selection case with semantic rather than phonological conditioning; K5 is a kāraka-assignment case where the competing rules assign the same role type under independent, non-nested semantic conditions.

The kāraka domain illustrates both possibilities in a directly instructive comparison. C5 (*apādāna* versus karma assignment) is resolved by *apavāda* because the *apādāna* rule specifies separation as an additional condition, making $D(1.4.24) \subset D(1.4.49)$: the apādāna domain is a proper subset of the karma domain, and the more specific rule wins. C5 is also definitively diagnostic: *apavāda* favors $\alpha$ (1.4.24), so the prior mechanism's output is unambiguously distinct from what 1.4.2 would predict. K5 (double karma assignment under 1.4.49 and 1.4.50) is discriminative because the two karma rules' semantic conditions are independently specified and non-nested - neither is a proper extension of the other, so no domain-subset relation holds and *apavāda* has nothing to operate on. The boundary between *apavāda*-resolvable and 1.4.2-operative in the kāraka domain is not domain-level but structural: proper-subset semantic domains yield *apavāda* resolution; non-nested semantic domains yield 1.4.2 cases.

C4b occupies the structural position the account requires to be internally consistent - a genuinely co-extensive phonological environment produces discriminative work from 1.4.2. But C4b is one of the three cases that generated the structural account; it cannot confirm the phonological-residual prediction independently. The consistency check C4b provides is necessary but not probative: confirmation requires co-extensive phonological environments not yet examined. Such environments are rare precisely because the grammar's sūtra sequence is arranged so that rules with related phonological conditions are nearby and typically in a specificity relation, making genuine co-extension a structural anomaly rather than a standard case.

The structural explanation for why the prior mechanisms underperform in the kāraka and semantic-morphology domains: the *antaraṅga* principle is defined on the containment of phonological conditioning environments. A rule whose triggering conditions reference elements inside the stem domain is more "internal" than one referencing elements outside it; the more internal rule fires first. This notion of interiority is meaningful for rules that apply to phonological segments in a derivational string. Kāraka assignment rules and semantically-conditioned suffix-selection rules do not reference positions in a phonological derivational string; they reference semantic-role relationships between arguments and verbs, or semantic properties of verbal bases. "More internal conditioning environment" has no application to a rule that assigns a semantic role to an argument. The *antaraṅga* principle cannot fire in those domains.

Part of this explanation is definitional: it follows directly from how *antaraṅga* is defined that it cannot apply to non-phonological rules. The empirical content is whether the output in kāraka and semantic-morphology cases actually matches the later sūtra's prediction - which condition 5 verifies independently. The structural account explains *why* the prior mechanisms are inapplicable; the attestation checks whether 1.4.2's predicted form is what appears.

The structural prediction for a fully-powered audit: 1.4.2 will be idle in phonological derivations except at the unusual residual where competing rules' conditions genuinely coincide, and operative in kāraka assignment and semantically-conditioned morphology except where one rule's semantic domain happens to properly contain the other's. A grammarian working in the phonological sections should reach first for *apavāda* and *antaraṅga*; in the kāraka section, 1.4.2 is the candidate primary conflict-resolver in the structurally important class of non-nested competing role-assignment rules.

One limit on the scope of this structural prediction must be named. The case set was compiled from secondary-literature environments where 1.4.2 is explicitly invoked or contested - a cited-use corpus, not a systematic sampling of kāraka conflicts. The prediction concerns the class of genuinely non-nested kāraka conflicts; it does not estimate how large that class is relative to *apavāda*-resolvable kāraka conflicts in the grammar as a whole. A fully-powered audit of the kāraka section would need to include conflicts where 1.4.2 is *not* cited alongside those where it is, to determine whether non-nested semantic domains are the majority or minority of kāraka conflict environments.

This structural account is not a distributional verdict on $H_\text{para}$ vs. $H_\text{neg}$. It is a domain-differentiated hypothesis about where the rule is and is not load-bearing - which is a different and more precise claim than either hypothesis as stated, but one that requires more evidence than the present case set supplies.

## What a Fully-Powered Audit Requires

The fifteen-case threshold requires a corpus wider than two secondary sources. A direct audit of the Mahābhāṣya would supply the needed case density. Patañjali explicitly marks cases as *vipratiṣedha*; the Mahābhāṣya contains dozens of such markings. A direct pass on those cases, coded by applying conditions 1–4 of $P_\text{disc}$ to the sūtra descriptions before recording Patañjali's verdict, would produce a case set of 30–50 and power adequate to the distributional question.

One complication must be named: Patañjali's *vipratiṣedha* marking is not independent of his prior about how the conflict resolves. If he marks a case as *vipratiṣedha* partly because he expects 1.4.2 to apply, the corpus is pre-selected toward discriminative cases, and the symmetry condition on the test is violated. The remedy is to code cases on formal structural criteria alone - applying conditions 1–4 mechanically to the sūtra descriptions - before consulting Patañjali's verdict, so that his verdict serves as attestation confirmation (condition 5) rather than case selection. This is achievable in principle; it requires a complete edition of the Mahābhāṣya and the Sanskrit scholarship to apply structural descriptions correctly. Those resources are the binding constraint. A kāraka-section audit would additionally need to sample kāraka conflicts that Patañjali does *not* mark as *vipratiṣedha*, to address the selection-bias limit identified above.

The [capture-versus-stand-in test](posts/2026-05-27-what-the-definition-replaces-a-capture-v-c02e/) asks whether a definition does the inferential job attributed to it - whether it carries a theorem or only vocabulary. The fully-powered audit of 1.4.2 is the direct application of that test to a rule: does 1.4.2 carry the output-determination work attributed to it, or does it inherit the form from prior mechanisms and receive credit for a derivation it did not run? The structural audit here cannot fully answer that question, but it specifies the conditions under which it could be answered.

## Conclusion

The audit was pre-committed to two outcomes: a distributional finding if the case set reached fifteen classifiable environments, or a structural finding if it did not. After applying the pre-committed classification criteria - including routing cases with unnamed and structurally uncharacterized competing rules and cases with disputed simultaneous applicability to $P_\text{unclass}$ - the case set yielded eight classifiable environments. The distributional verdict cannot be issued.

The structural hypothesis generated by this audit is:

1.4.2 is likely inert in the phonological domain in all but residual cases where competing rules have genuinely co-extensive conditioning environments. It is likely operative in the kāraka domain and in semantically-conditioned morphology for a structural reason: the *antaraṅga* principle has no application to non-phonological rules, and *apavāda* resolves non-phonological conflicts only when one rule's semantic domain is a proper extension of the other's. Where neither condition holds - and in the kāraka section, both conditions systematically fail for a class of competing role-assignment rules - 1.4.2 is the candidate operative mechanism. The boundary between *apavāda*-resolvable and 1.4.2-operative cases runs along the nested/non-nested dimension of the competing rules' conditioning domains, not along the phonological/non-phonological dimension alone.

This hypothesis is generated by three discriminative cases - one observation per cell on the central domain-by-mechanism grid. Neither $H_\text{para}$ nor $H_\text{neg}$ as globally stated is sustained, but neither verdict was reachable at the achieved case count. The structural account is more informative than either hypothesis as stated - it is domain-differentiated rather than global - but it carries the weight of a hypothesis generated by an underpowered pilot, not a finding confirmed by adequate data. The long dispute between Kiparsky's generativist reading and the Patañjalian skeptics is not a dispute about frequency alone; it is a dispute about scope, and the scope appears non-uniform across the grammar's domains. Whether that appearance survives corpus-scale examination is what a fully-powered audit would determine.

## References

- Cardona, G. (1970). *Pāṇini: His Work and Its Traditions.* Vol. 1, *Background and Introduction.* Delhi: Motilal Banarsidass.

- Kiparsky, P. (2002/2009). "On the Architecture of Pāṇini's Grammar." In G. Huet and A. Kulkarni (eds.), *Sanskrit Computational Linguistics*, LNAI 5402. Berlin: Springer.

- Patañjali. *Vyākaraṇa-Mahābhāṣya.* Cited throughout via Cardona (1970); this paper does not represent independent access to the Kielhorn edition (Bombay, 1880–1885).

- [*Galileo or Biewener? Fitting the Mammalian Femur*](posts/2026-05-20-qual-galileo-or-biewener-fitting-the-femoral--715a/)

- [*What the Apparatus Refuses to See: Mapping the Blind Cone of a Measurement Procedure*](posts/2026-05-26-what-the-apparatus-refuses-to-see-mappin-3299/)

- [*What the Definition Replaces: A Capture-versus-Stand-In Test for Modern Mathematical Notions*](posts/2026-05-27-what-the-definition-replaces-a-capture-v-c02e/)
