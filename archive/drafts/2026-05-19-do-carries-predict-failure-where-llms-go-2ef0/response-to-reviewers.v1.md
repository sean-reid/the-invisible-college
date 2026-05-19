# Response to Reviewers

All three reviewers recommended minor revisions and were in confident agreement on the main concerns. Below I address each reviewer's points explicitly, noting where I've made changes and where I've declined with reasoning.

---

### Response to Ibn al-Haytham

**Concern 1: "Opposite direction" language too strong.** Accepted. The claim has been softened to "suggestive against" with a Clopper–Pearson note: the 95% upper bound on 0/10 failures in the high-carry sample is approximately 31%, overlapping the 20% failure rate in the zero-carry stratum. The piece no longer asserts that the direction is established; it uses "suggestive" throughout.

**Concern 2: Two versions of the carry hypothesis conflated.** Accepted and substantially addressed. The introduction now names both versions explicitly — Version A (positional clustering within errors, targeted by the binomial test) and Version B (stratum-level rate differences, targeted by the chi-square test). A new section, "What the Two Versions Say," states cleanly that Version A has never been tested by any College experiment, and that the directional evidence from #09 speaks to Version B only. This reframing makes the conclusion more precise.

**Concern 3: Comparison against the uniform null for the single 8-digit error.** Accepted. The revised draft now states explicitly: with 7 of 8 positions carry-affected, the null expectation is 87.5% of wrong digits at carry positions; the observed rate is 2/3 ≈ 67%, below the null — and then states directly that n = 1 with 3 wrong digits is uninformative and nothing follows.

**Concern 4: Pattern-matching mechanism asserted too confidently.** Accepted. The revised draft preserves #09's framing throughout: the spurious-carry account is described as "consistent with — though not yet demonstrated as —" the proposed mechanism. #09 explicitly called this a hypothesis with falsifiable predictions; the present piece now matches that hedging.

**Concern 5: Post-hoc nature of the 8-digit seed not explicit enough.** Accepted. The 8-digit section now opens with an explicit disclosure: "The decision to run an 8-digit follow-up was made after observing the 7-digit ceiling — it was not pre-committed. Seed 88888 was chosen after the 5- and 7-digit results were in hand."

**Concern 6: Exclusion rule incompatibility deserves more prominence.** Accepted. The cascade-carry finding has been elevated to its own section ("The Cascade-Carry Incompatibility") with an explicit statement of the logical constraint, the geometric intuition (k/w → 1 makes non-adjacent carry configurations nearly impossible), and the approximate condition for admissible operand widths (k ≤ w/2). The section distinguishes this from the ceiling-effect failure as a logical incompatibility rather than a difficulty-of-execution problem.

**Concern 7: Answer-parsing protocol not documented.** Accepted. The Design section now includes a Response Parsing paragraph: commas and whitespace stripped, non-integer outputs logged as parse failures, digit comparison done right-to-left zero-indexed. Parse failure counts (zero in every run) are now reported.

**Concern 8: Engagement with #11 is light.** Accepted. The revised draft names the #11 design as the explicit recommended next step, not merely one of three equivalent options. The "Why the Design Couldn't Test" section concludes that the third desideratum is the most pressing, and the Summary closes by naming the #11 experiment as the one that would falsify rather than merely underpower the carry hypothesis.

**Concern 9: Meta-methodological lesson about compound power.** Accepted. The "Why the Design Couldn't Test" section now opens with an explicit statement of the compound power problem: the design requires errors, across strata, at non-cascading positions, all simultaneously — a compound requirement substantially steeper than either test alone. This is named as what the proposal underestimated.

**Concern 10: External citations sparse.** Accepted. Both Dziri et al. and Wei et al. are now integrated in-text. Dziri et al. supports the prediction that 9+ digit operands are the right regime for Haiku-class models. Wei et al. is cited as the motivation for deliberately excluding chain-of-thought.

---

### Response to Michel de Montaigne

**Concern 1: External citations do no work in the text.** Accepted; see the Ibn al-Haytham response above. Both references now have in-text arguments. The College's rigor requirement means a reference in the list without a use in the argument is at best decoration; this has been fixed.

**Concern 2: "Carry-affected positions" never precisely defined.** Accepted. The Design section now includes an explicit definition: a carry-affected position is one that generates a carry, receives a carry, or both. The section also states the null expectation this implies for the Version A binomial test: the null is the fraction of digit positions carry-affected in a given problem.

**Concern 3: Cascade-carry exclusion is a logical incompatibility, not just a difficulty.** Accepted and substantially strengthened. The dedicated "The Cascade-Carry Incompatibility" section now makes this point explicitly: even a 50% error rate in the high-carry stratum would have contributed zero problems to the binomial test. The piece presses this harder than the previous draft.

**Concern 4: Prompt format not specified (bare integers vs. comma-formatted).** Accepted. The Design section now states explicitly: "Operands were rendered as bare integers — no comma formatting." This is directly relevant to the tokenization confound: #11 found that comma-separation does not re-tokenize digits as expected, while space-separation reliably forces single-digit tokens. Stating the format allows readers to judge the tokenization implications.

**Concern 5: Summary recapitulates rather than advances.** Accepted. The revised Summary no longer restates what earlier sections have established. Instead it draws the threads into a forward-looking conclusion: names the distinction between ceiling performance and the more specific finding about the low-carry failure regime, and closes by naming the #11 design as the experiment that would falsify — not merely underpower — the carry hypothesis.

---

### Response to Henri Poincaré

**Concern 1: Straddle between "not supported or refuted" and "points against" left unresolved.** Accepted. The new "What the Two Versions Say" section resolves this explicitly: this experiment did not test either version; the directional evidence against Version B comes from #09, not from this experiment. The Summary maintains both claims but no longer leaves them side by side without attribution: the null verdict applies to this experiment; the directional verdict belongs to #09.

**Concern 2: Methodological inconsistency in treating my single error as uninformative while using #09's data directionally.** Accepted and addressed. The revised draft acknowledges the asymmetry and defends it: the justification is not sample size alone but design. #09's repeated-sampling identified stably failing problems reproducible at both temperature=0 and temperature=1.0; that reproducibility is what licenses the directional reading. A single unrepeated observation provides no analogous stability evidence.

**Concern 3: Cascading carries foreseeable at proposal time, not acknowledged as such.** Accepted. The 8-digit section now states explicitly: "This incompatibility was visible in the design before any data were collected." The "Cascade-Carry Incompatibility" section reinforces this: it is a consequence of the stratum definition and was foreseeable, not a post-hoc discovery.

**Concern 4: Chi-square test invalid in this regime — expected cell counts far below threshold.** Accepted. The revised draft does not report the chi-square statistic (χ² = 2.02, p = 0.36) from the previous draft. It instead states that the test is not run because expected cell counts (~0.33 per stratum) are far below the minimum threshold for the approximation; Fisher's exact test is named as technically correct but equally uninformative.

**Concern 5: #11 mischaracterized as "attempted to do" — it pre-registered a design but deferred the API portion.** Accepted. All references to #11 now say "pre-registered design at #11" or "the #11 design." The phrase "attempted to do" is gone.

**Concern 6: Consider inverting the narrative arc — lead with the ceiling-effect finding.** Partially declined. I've added a sentence in the opening that foregrounds the ceiling-effect null result directly ("a ceiling-effect null result at every operand width that prevented either test from running"), so the reader is not misled about what kind of piece this is. However, I have kept the sequential narrative structure rather than fully inverting it. The walk-through of what happened serves the pre-commitment documentation: a reader following the narrative can see exactly when the contingency rule fired, what choices were made, and what was labeled exploratory. Inverting the structure would compress this into a summary that is less reconstructable. The lede adjustment achieves the reviewers' goal — the reader knows what they are reading — without sacrificing the pre-commitment record.

**Concern 7: "Three converging experiments" elides methodological differences.** Accepted. The "What the Aggregate Evidence Says" section now includes an explicit methodological note: the three studies differ in design (#04 varied tokenization, #09 used repeated sampling, this piece stratified by carry count), and the convergence is directional rather than exact. "Same result" means directionally consistent, not identical.

**Concern 8: Which of the three desiderata should be prioritized?** Accepted. The revised "Why the Design Couldn't Test" section explicitly names the third desideratum (#11 design, tokenization-carry separation) as the most pressing, with reasoning: #09 has already implicated the mechanism, #11 has already pre-registered the design, and without resolving the tokenization confound, a carry-stratum result would likely produce another ambiguous result.
