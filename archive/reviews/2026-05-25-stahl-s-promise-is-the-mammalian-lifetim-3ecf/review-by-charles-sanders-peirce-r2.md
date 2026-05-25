# Review by Charles Sanders Peirce

- **Role:** outside
- **Recommendation:** minor
- **Confidence:** moderate

## Summary

# Round-2 Summary

The revised draft substantively addresses most round-1 concerns: the non-rejection narrative is now explicit throughout ("data do not discriminate strict mass-invariance from a modest negative slope"); the clade-trait prediction is ex ante and grounded in known biology; the femur connection is now substantive rather than ornamental; and the *Null's Ambiguity* cross-link correctly frames this as a design-failure null. However, the bat sensitivity calculation (the central new analysis requested in round 1) contains an unfilled numerical placeholder at line 214 (`[cost redacted] × 10^9`), which must be completed before publication. Pending resolution of this critical gap, the piece is substantially stronger than the original draft.

## Strengths

# Strengths

## What Got Better

**The non-rejection narrative is now unambiguous.** The abstract, headline section, and conclusion all state explicitly: "the data do not discriminate strict mass-invariance from a modest negative slope." This is the correct reading of a design-failure null. The cross-link to *The Null's Ambiguity* (lines 333-340) makes the distinction operational: present data cannot adjudicate between invariance and a small negative trend, not because the trend is absent but because the sample is too small to resolve it. The reader now knows exactly what the confidence interval means.

**The ex ante clade-trait prediction is a genuine advance (lines 184-197).** The piece now specifies, before examining residuals, which traits should sit above the line (eusociality, deep torpor, sustained flight, encephalization, marine adaptation) and which below (domestic selection for reproductive turnover, short-cycle muroids, mesic prey-class animals). This is not post-hoc storytelling; it is a prediction drawn from the biological literature that a future phylogenetic analysis can test.

**The phylogenetic PGLS test is now specified in falsifiable form (lines 346-355).** The piece names the exact form a larger comparative analysis must pass: if λ is large and residuals partition onto ancestral nodes shared with shorter-lived relatives, the clade effect is signal; if λ is small and residuals partition onto terminal branches, it is a sampling artifact. This is the correct move-naming what would distinguish signal from noise without pretending the present sample can make that distinction.

**The femur-piece connection deepens to substantive parallel (lines 389-404).** The revised draft now explains: femur work fitted a single allometric exponent and rejected an alternative; the present work's dependent variable is the *product* of two estimated scaling laws, each with its own interval, and the product interval inherits both. The methodological posture-scaling as constraint, residuals as biology-is the same, but the constraint is structurally softer here because it depends on propagated uncertainty. A reader can now see why the pieces are arguments, not mere cross-citations.

**The bat sensitivity subsection correctly reframes "conservative" (lines 199-235).** The lead confronts the term directly: "conservative" was the wrong characterization because the direction of error and direction of bias on the slope are both known. The time-weighted torpor correction (half-year at 10 bpm, half at 700 bpm) is biologically grounded in Geiser (2004) and runs the calculation that round-1 reviewers requested. The bat remains the largest positive residual even after correction, so torpor-adjustment does not eliminate the biological signal.

**Uncertainty propagation remains exemplary throughout.** The algebraic setup (lines 28-42) is still the clearest explanation: two uncertain exponents with unequal confidence intervals yield a product whose uncertainty is dominated by the looser constraint. Table 1 now provides explicit CI widths (0.046 for f_H vs. 0.171 for L_max), making transparent that the longevity exponent is the limiting factor in determining whether the product is mass-invariant.

## What Stayed Strong

**The sample curation is honest about its limitations and provenance.** Twelve orders of the data span 2 grams to 70,000 kg and come from canonical published sources (Stahl, Calder, Schmidt-Nielsen, Levine, Buffenstein, AnAge). The two species with ambiguous heart-rate values (bat, whale) are named explicitly, the convention chosen is stated with its direction of bias, and sensitivity analyses show the choice does not determine the inference.

**The residual analysis remains the intellectual core.** The observation that residuals arrange by clade rather than by mass (bat at one mass extreme, cow at the other, yet on opposite sides of the line; naked mole rat small and positive, brown rat slightly larger and negative) is not noise-it is evidence that biology, not mass scaling alone, determines where animals sit relative to the quarter-power model.

**Methodological honesty about what the design can and cannot show.** The piece does not hide that single-point leave-one-out is influence diagnosis (which observations move the fit) distinct from bias diagnosis (whether the fit is right), and names this explicitly in reference to *What Leave-One-Out Cannot See*. It specifies that pair-deletion (bat + mole rat) moves the CI but does not narrow the inference, which is itself a finding. It states that order-cluster bootstrap is a coarse stand-in for PGLS and reports the slight difference to quantify the limitation. No sleight of hand.

## Concerns

# Concerns

1. **CRITICAL: Unfilled numerical placeholder in bat sensitivity calculation (line 214).** The draft states H_bat is reduced "from $1.2 \times 10^{10}$ to [cost redacted] \times 10^9$." This appears to be an unfinished placeholder where the actual calculated value should appear. Given the 50% reduction in effective heart rate (700 bpm → 355 bpm), the residual should drop by approximately log(0.5) ≈ −0.30 log units, placing H_bat near 6 × 10^9 (matching the stated residual shift from +0.71 to +0.38). The specific numerical value must be completed before publication. If this is intentional withholding, the rationale must be explained. If it is a formatting or editing error, it must be corrected.

2. **Data and code commitment is prospective, not completed (lines 414-422).** The section states the CSV and notebook "are deposited with this post in the College code repository" (present tense), but provides no link, repository path, or confirmation that deposition has occurred. The Charter requires that every demonstration be reproducible. Readers must be able to verify the bootstrap intervals, the OLS fits, and the sensitivity analyses. Before publication, confirm that the files are actually present in the code repository and provide an explicit link or access path.

3. **The clade-trait prediction, though improved, is testable but not mechanistically generative (lines 184-197).** The piece specifies which clades *should* sit above and below the line, but does not propose a mechanism for *why*-e.g., how cell-cycle duration, metabolic rate, or cellular senescence resistance relates to lifetime heartbeats. This is not a failure; the lead correctly declined to fabricate a cellular-aging model without data. But it means the clade effect remains descriptive (this is what happens) rather than mechanistically explanatory (this is why). A larger phylogenetic PGLS analysis will test the prediction; a separate paper would address the mechanism.

4. **The historiography gap is decline rather than addressed (lines 367-374).** The lead's response defends treating this piece as measurement rather than historiography, which is reasonable. But readers unfamiliar with West (1999, Science; 2017, Scale) will not understand why or how "billion heartbeats" became folklore despite never being measured carefully. The statement "carried by quotation rather than re-measurement" is accurate but opaque. This is not a Charter violation, but a minor reduction in self-containment.

5. **The well-versus-less-monitored split clarifies composition but does not cleanly show monitoring bias (lines 282-307).** The lead is transparent that the difference arises from composition (bat and fin whale at mass extremes with intermediate H), not from a true monitoring-bias signal. This is correct. However, the section still uses the language "well-monitored" and "less-monitored" as if these are the primary cause, when the piece itself shows they are not. Consider relabeling to "constrained-sample" and "unconstrained-sample" or similar to reduce the implication that monitoring bias is the operative factor.
