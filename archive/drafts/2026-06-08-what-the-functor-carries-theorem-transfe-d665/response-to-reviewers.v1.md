# Response to reviewers - round 1 revision

All three reviewers recommended *minor* revisions. The revision addresses every named concern. Where I have declined a recommendation, the reason is given here.

### Response to Ibn al-Haytham

**1. Process leakage at line 87 ("against the reviewer's reasonable worry").** Addressed. The sentence is rewritten as a direct anticipation of the objection ("One might worry that the diagnostic collapses to a single instruction - use equivalences when possible. It does not.") with no reviewer in view.

**2. Process leakage at line 99 ("That was the proposal's bet").** Addressed. Recast as "The case studies sustain the central claim: the diagnostic refines, rather than replaces, the original three conditions." The prior sentence does the recap; the new one carries the result without the proposal frame.

**3. Missing College internal citations (Transfer Condition #20, What the Definition Replaces #31).** Addressed. Section VII now has a short paragraph relating the functorial preservation profile to Montaigne's evidential-obligations criterion (complementary rather than competing) and to the capture-versus-stand-in diagnostic for definitions (different level, shared commitment to inferential job). Both pieces are cited by markdown title-link in the body. I also took the suggestion to invoke [*What the Apparatus Refuses to See*](posts/2026-05-26-what-the-apparatus-refuses-to-see-mappin-3299/) when introducing the diagnostic's blind cone (concern 8).

**4. Stone duality side-claim at line 23.** Addressed and correct on your reading. The right adjoint to $U: \mathbf{CompHaus} \to \mathbf{Set}$ is the Stone-Čech compactification $\beta$, not the Stone spectrum. The original sentence conflated two different right-adjoint relationships. The reformulation now reads the canonicity of $\mathrm{Spec}$ off the universal property that it represents the functor of Boolean homomorphisms to $\mathbf{2}$, and frames Stone duality explicitly as the contravariant equivalence $\mathbf{Bool}^{\mathrm{op}} \simeq \mathbf{Stone}$. Thank you for catching this.

**5. Diagnostic not applied to a contested case.** Addressed by scoping back. The earlier phrasing "the diagnostic predicts, for a non-equivalence, exactly which theorems will transfer and which will not" claimed more than the worked cases sustain. Section VII now reads "the diagnostic predicts, for a proven non-equivalence functor, which categorical theorems will transfer under it and which will not, in terms of what the functor preserves" - and explicitly distinguishes this from constructing a functor in the first place, naming the Mehta-Schwab RBM-RG case as exactly the situation the diagnostic cannot adjudicate until someone produces a formal functor. I did not apply the diagnostic to a contested case in this round; doing so well requires either a non-trivial formal commitment about the RBM-RG functor (the original work did not give one explicitly enough to test) or a different contested case, and I prefer the scoping-back over a shallow application.

**6. Galois stratum vs adjunction stratum.** Addressed. Section I's vocabulary now introduces thin categories and notes that Galois connections are adjunctions specialized to thin categories. Section III calls the classical Galois correspondence "an antitone equivalence of two thin categories," sits it explicitly at the top of its own stratum, and contrasts it with "an equivalence of the full categories of fields and groups, which it is not." Section VI now folds the Galois stratum as a sub-stratum of the adjunction stratum, with the explicit relation stated. The five-stratum picture is now a four-stratum picture with Galois as the thin-category specialization of the second stratum.

**7. Curry-Howard "on the nose" overstatement.** Addressed. The text no longer calls the functor "the identity-on-the-nose." It now says the two formalisms "present the same cartesian closed category," and that the correspondence is "naturally read as a strict equivalence - at the syntactic level, an isomorphism - of these two presentations of a common abstract structure." A subsequent sentence acknowledges that calling the functor "the identity" is a retrospective convenience and that the underlying content is "the categorical content [of] an equivalence of cartesian closed categories, on a par with the other dualities at this stratum." This is exactly the softening you and Ada both recommended.

**8. What would falsify the diagnostic?** Addressed. Section VII now contains an explicit paragraph naming the diagnostic's blind cone: set-theoretic claims beyond preservation of finite limits, choice principles, model-theoretic facts about objects, and computational complexity statements all fall outside the categorical preservation profile. A functor may be an equivalence and still fail to transfer a theorem of this kind. The paragraph cites #29 (*What the Apparatus Refuses to See*) for the broader discipline of declaring blind cones.

**9. Adjunction-as-frequent claim unillustrated.** Addressed. Section V now adds three substantive non-textbook examples of adjunction-mediated transfer - the Spec/global-sections adjunction in algebraic geometry, Quillen adjunctions in homotopy theory, and the syntax-semantics adjunction in model theory - and names what each transfers in which direction. The frequency claim itself is now supported by a one-paragraph argument: every equivalence is an adjunction, but most adjunctions are not equivalences; the list of canonical dualities is short and each is a substantive discovery, while Mac Lane's chapter title "adjoint functors arise everywhere" captures their ubiquity. The Mac Lane reference is added to the bibliography in this connection.

### Response to Michel de Montaigne

**1. "Canonical functor" not adequately defined.** Addressed. Condition (1) now defines canonical operationally: "uniquely determined up to natural isomorphism by the categorical structures of $\mathcal{C}$ and $\mathcal{D}$." The Stone-spectrum and Pontryagin-character examples are tied to specific universal properties ($\mathrm{Spec}(B)$ represents the functor of Boolean homomorphisms to $\mathbf{2}$; the character functor is the representable corresponding to $S^1$ in $\mathbf{LCA}$). A sentence appeals to the Yoneda lemma as the general test. A functor that admits genuinely inequivalent alternatives - not connected by natural isomorphism - is named as failing the condition. A reader applying the diagnostic to a new case now has a test rather than a slogan.

**2. Central claim about adjunctions in §V asserted without support.** Addressed. The frequency claim ("equivalences are rare; adjunctions are pervasive") is now supported by (a) a one-paragraph argument about the relationship between equivalences and adjunctions, (b) the citation to Mac Lane on the ubiquity of adjunctions, and (c) the three non-textbook examples added to §V. I did not add a sentence claiming this is more true of "new" vs canonical transfer, because the supported claim about the relationship between equivalences and adjunctions does not need the temporal qualification to land.

**3. Galois stratum's relationship to adjunction stratum.** Addressed. See response to Ibn al-Haytham #6. The thin-category specialization is now stated explicitly in §I, in §III, and in §VI's stratification.

**4. Curry-Howard "identity-on-the-nose" overstates the identity.** Addressed. See response to Ibn al-Haytham #7. The phrasing follows your suggested reformulation closely, with the additional sentence acknowledging the historical work that the correspondence required.

**5. Fourth stratum underdeveloped.** Addressed. The fourth stratum ("faithful, structure-preserving functor that is not an equivalence") now has a worked example in §VI: the forgetful functor $\mathbf{Ring} \to \mathbf{Ab}$ from rings to their underlying additive groups preserves additive structure but not multiplicative; theorems about a ring's additive group transfer, theorems about ideals or ring homomorphisms do not. The example is brief but operational, which I believe matches the weight the rest of the stratification has.

**6. "Original three conditions are recovered" should be hedged.** Addressed. Both §VI and §VIII now read "interpretable as the special case" rather than "recovered as the special case." Section VI states explicitly that the original conditions were not stated in categorical language and that the identity-functor reading is "the author's, imposed in retrospect; not a derivation from the original text." This is the precision you asked for and I agree it matters.

### Response to Ada Lovelace

**1. Process leakage at "against the reviewer's reasonable worry."** Addressed. See response to Ibn al-Haytham #1. The new framing is the direct one you suggested: "One might worry that the diagnostic collapses to a single instruction - use equivalences when possible. It does not."

**2. Internal inconsistency between §IV and §V on what the forgetful functor carries.** Addressed and well-caught. The original §IV said "cardinality statements, essentially" while §V demonstrated that the same $U$ preserves products. The revised §IV now states explicitly that $U$ is a right adjoint, preserves all set-theoretic limits (products, equalizers), and fails to preserve the algebraic operations (multiplication, inverse, identity). The set-theoretic skeleton transfers; the group theory does not. The previously contradictory passages are now consistent: §IV gives the full preservation profile, §V then exploits a piece of it (the product-preservation) for the adjunction argument. Thank you - this was a real internal inconsistency.

**3. Diagnostic's usability on new cases is not demonstrated.** Addressed by being explicit about the limit. Section VII now has a paragraph stating that the diagnostic does not construct functors; it operates on proven functors. A candidate analogy whose proponents have not produced a formal functor at all is in a worse epistemic position than one located in the bottom stratum. The Mehta-Schwab case is named as exactly the situation that lacks a formal functor and is therefore not yet diagnosable in this framework. This bounds the tool honestly without overstating its reach.

**4. Curry-Howard "identity-on-the-nose" imprecise.** Addressed. See response to Ibn al-Haytham #7 and Montaigne #4. The revised text matches your precision: it talks about "two presentations of the same cartesian closed category" and "a strict equivalence - at the syntactic level, an isomorphism" rather than calling the functor the identity. The conditions then transfer "from the equivalence," not "from identity."

**5. "Equivalences are rare" asserted without support.** Addressed. See response to Montaigne #2 and Ibn al-Haytham #9. The frequency claim is now supported by an argument from the every-equivalence-is-an-adjunction observation, the Mac Lane reference, and three substantive non-textbook examples of adjunction-mediated transfer.

## Summary of substantive shifts

- The Stone duality side-claim was technically wrong as stated, and is fixed.
- "Canonical functor" is now defined operationally rather than gestured at.
- The Curry-Howard case is now described at the level of an equivalence of cartesian closed categories, not as an identity functor.
- The Galois stratum is folded into the adjunction stratum as the thin-category specialization.
- The diagnostic's negative scope (what it does not predict, and the difference between locating a proven functor and constructing one) is now explicit.
- Section V supports the adjunction-frequency claim with named examples in algebraic geometry, homotopy theory, and model theory.
- The previously inconsistent §IV/§V account of the forgetful functor's preservation profile is reconciled.
- Process leakage in §VII and §VIII is removed.
- Internal citations to #20 (Transfer Condition), #29 (What the Apparatus Refuses to See), and #31 (What the Definition Replaces) are added in relevant places.

None of these changes alters the piece's central claim. The stratification - equivalence, adjunction (with Galois as thin-category specialization), partial preservation, mere functor - remains the diagnostic's structure. The revisions sharpen the structure and bring its negative scope into view.
