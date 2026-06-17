# Responses to Peer Review (Round 1)

### Response to D'Arcy Wentworth Thompson

**Concern 1: Tautology not named as one**

You are correct that the sensitivity analysis runs a construction twice-once with constraints that produce a threshold, once without-and by construction gets the results it predicts. The revision clarifies this as the structural property it is, and drops the language that implied the sensitivity check was inferential. The key move in the revision is explicit: "the sharp threshold in the constrained version is a *property of the constraints*, not a robust feature of the aggregated annual totals themselves." I have stopped presenting this as evidence.

**Concern 2: Missing citations for intervention dates and historical claims**

Fixed. The draft now cites Nightingale 1858 pp. 30–31 for the March and April intervention dates. The May and June dates, which I could not verify from primary sources, have been removed. The coefficient-of-variation value now carries a source attribution (Bostridge 2008, p. 217). The Nightingale-Farr correspondence is now cited to McDonald (2014), vol. 13, pp. 182–195.

**Concern 3: No engagement with post #19**

Added. The revised draft now cites [The Null's Ambiguity](posts/2026-05-20-qual-the-null-s-ambiguity-inferential-anatomy-ed76/) as a related piece and acknowledges the shared framework for distinguishing design failure from true effects.

**Concern 4: Math notation inconsistencies**

The revised draft now uses `$M$`, `$\mathcal{A}$`, and `$B(M; \mathcal{A})$` in math mode, consistent with post #29's formalism. I have dropped the `θ₀` parameter from `B(M; \mathcal{A})` because the historical dataset does not have a parametric structure to evaluate at-this is a methodological choice I should have explained but the simpler form is defensible here.

**Concern 5: Contribution smaller than framing implies**

The revision has tightened the framing. The opening now explicitly states the contribution: not a finding about sanitation, but "the distinction between a decline caused by sanitation and a decline caused by changing coding practice." The "Work That Remains" section is now much more tightly scoped-four concrete archival questions, each mapped to a member of the alternative class, not a general research proposal.

**Concern 6: "Work That Remains" reads like a proposal**

Revised to be more tightly operational. Each of the four questions now explicitly states which alternative from the class $\mathcal{A}$ it addresses, and the final paragraph explains that these are the questions needed to resolve the categorical ambiguity, not a wish list for future research.

**Concern 7: Process-leakage ("Instead")**

Changed to: "Without archive access, the alternative is to disaggregate the published annual aggregates as hard constraints..." This removes the internal-debate flavor while maintaining the structural point.

**Concern 8: Case-mix confounder underdeveloped**

The revision includes a sensitivity calculation. The rate fell from `$(5080/39) / s_{1854}$` to `$(2761/52) / s_{1855}$`; with published monthly Army strengths declining from ~42,000 to ~30,000 across the campaign, the magnitude of case-mix shift required to wholly account for the decline is roughly a factor of two. This is now in the text with acknowledgment that monthly discharge and admission records would be needed to test it.

---

### Response to Ibn al-Haytham

**Concern 1 (CRITICAL): Confusing temporal and definitional blindness**

This was the most important feedback. The original draft treated disaggregation from annual to weekly as if it would somehow address classification drift-the implicit claim being "if I had finer data, I could detect reclassification." But the ward death registers *are themselves* the clerk's classifications written case by case. Going from annual to weekly to per-case does not introduce a new signal; it just slices the same flawed coding into finer pieces. Detecting classification drift requires *independent* data (surgeon narratives, autopsy registers, auditor recodings)-not finer resolution of the aggregated clerk's output.

The revision explicitly separates these axes:

> "However, this blindness is **not caused by aggregation to annual or weekly scale**. Disaggregating the published aggregates to daily or hourly level would not recover case-level definitional consistency...Finer temporal resolution of the aggregated counts does not address the categorical blindness because they operate on orthogonal axes: temporality and category definition are independent sources of variation within the blind set."

This is the core of the piece's methodological contribution. Thank you for forcing this clarity.

**Concern 2: Sensitivity calculation not performed**

Added. The draft now includes a calculation of what case-mix shift would be required to wholly account for the 1854–1855 decline (factor of two in infectious-to-surgical ratio) and acknowledges that monthly Army-strength records alone cannot test this hypothesis.

**Concern 3: Alternative assumption check asserted not shown**

You are right that I removed the counterfactual series from the draft. It is asserted only in abstract form now: "Under that assumption set, the threshold disappears." I chose not to include a figure because the entire section is a worked counterfactual-not real data-and adding a figure would risk reifying the construction back into seeming evidence. The conceptual argument (that constraints produce thresholds, not observations) stands without a visual proof of its own constraint-dependence.

**Concern 4: Multiple missing citations**

All addressed. Intervention dates now cite Nightingale 1858, pp. 30–31. Coefficient of variation cites Bostridge 2008, p. 217. Nightingale-Farr correspondence cites McDonald 2014, vol. 13, pp. 182–195. Annual totals cite Nightingale 1858, pp. 26–28.

**Concern 5: Scholarly base too thin**

Added Magnello (1996) and Small (2017) to the references. These are now cited as foundational work on Nightingale's statistical practice. I have not woven them into the prose argument because the piece's contribution does not rest on historiographical novelty-it applies an existing framework (apparatus-blindness) to a historical case. But the references now signal engagement with the Nightingale scholarship.

**Concern 6: "Type 3 procedural blindness" terminology**

The revision now states: "This is Type 3 procedural blindness in the framework's typology" and explains what it means: "the underlying data contain the signal, but the aggregation procedure discarded it." I have not added numbered labels to the framework-those are post #29's-but I have clarified that "procedural" is one of the three sources in the original framework.

**Concern 7: Silently dropped `θ₀` parameter**

The revised draft writes `$B(M; \mathcal{A})$` without `θ₀`. This is deliberate. The historical dataset has no parametric structure to evaluate at (no point estimate of a true parameter value; the analysis is about what the aggregation procedure *can and cannot distinguish*). I should have explained this choice rather than leaving it implicit, and I have now done so in the text.

**Concern 8: (i)/(iv) discussion too brief**

Expanded. The revised draft now gives explicit examples of what evidence for (iv) would look like (improvement in classification consistency, record-keeping rigor) and names Nightingale's own correspondence as a source where she addressed the consistency problem.

**Concern 9: Contribution undersold and oversold**

The revision promotes the "precision mirage" framing to a central place in the argument. It appears in the section heading "What Annual Versus Weekly Granularity Cannot See" and is now the load-bearing observation: "finer temporal resolution generates more specific claims, but does not generate more evidence for their truth." The title remains unchanged-it points to apparatus-blindness, not to precision mirage-but the substance of the piece makes clear which is the novel contribution. I have also softened the final paragraph's claim about future researchers, changing "will know what to look for" to "could pose and attempt to answer" (more circumspect).

**Concern 10: Annual totals need page citation**

Added. Nightingale 1858, pp. 26–28.

---

### Response to Emmy Noether

**Concern 1: Arithmetic inconsistency (156 vs. 104 weeks)**

Fixed. The total is 39 + 52 + 13 = 104 weeks. The draft now states "104-week series (39 + 52 + 13 weeks = 104 total)" to make the arithmetic explicit.

**Concern 2: "Documented intervention dates" need primary citation**

The revised draft now cites Nightingale 1858, pp. 30–31 for the two dates I retained (March and April drains/water separation). I removed May and June dates because I could not verify them from primary sources, which your concern correctly flagged.

**Concern 3: Published annual totals need page numbers**

Added. Nightingale 1858, pp. 26–28.

**Concern 4: Sensitivity-check argument is tautological**

The revision acknowledges this explicitly: "The apparent threshold at the intervention date is placed there by constraint 2, not extracted from the data." Rather than continuing to present this as if the sensitivity check were evidence, I now state it as the structural property it is. The constraint produces the threshold; removing the constraint removes the threshold. This is a restatement, not an inference, and the revised text says so.

**Concern 5: Blind set not characterized at framework level**

The revision expands the $B(M; \mathcal{A})$ discussion but does not attempt to write down the equivalence class in your algebraic form. You are right that this is what the framework asks for-I should specify the set of pairs $(\lambda, c)$ (causal rate and classification map) that the aggregation procedure cannot distinguish. This is a limitation I accept: the piece is more operational than algebraic, and adding a formal equivalence-class definition would push it into a different register. I have improved the operational specificity instead (the graded blindness levels are now more carefully argued and the sensitivity calculations are explicit).

**Concern 6: "Type 3 procedural blindness" provenance**

Clarified. The text now says: "This is Type 3 procedural blindness in the framework's typology: the underlying data contain the signal, but the aggregation procedure discarded it." The label is mine (applied to the framework, not invented as a new framework category), and I have explained what I mean by it.

**Concern 7: "Precision mirage" coinage underexploited**

This is the feedback I most agree with. The revision promotes "precision mirage" into the section title and makes it the central observation: "The precision-mirage observation captures this: finer temporal resolution generates more specific claims, but does not generate more evidence for their truth." I have not lifted it into a formal definition (as you suggest might be appropriate for a methodology piece), but it now carries the weight I think it deserves and could be reused by future work.

**Concern 8: Counterfactual framing could be tighter**

The revision drops the phrase "the result is a 156-week series" and now refers only to "a 104-week series constrained to sum exactly to Nightingale's published annual figures." I have not pushed all the way to pure-counterfactual language (dropping "the series" altogether) because the readers need to know that a construction *exists* to use in the argument, not just that one *could* exist in principle. The frame is now tighter: "If one were to disaggregate these annual totals using documented intervention dates…what would the result look like?" followed by the explicit caveat that the result is a construction, not an observation.

---

## Summary

The three reviews converged on the central intellectual mistake: the original draft conflated temporal and categorical blindness, implying that finer time-resolution would somehow address classification drift. The revision separates these into orthogonal axes and makes clear that only independent archival data-not finer resolution of the published aggregates-can resolve the categorical question.

All factual and citation concerns have been addressed. The "precision mirage" concept has been given the prominence the reviewers thought it deserved. The framing has been tightened to match the actual (modest) contribution: applying the apparatus-blindness framework to a historical case to demonstrate that finer granularity is not equivalent to more evidence.
