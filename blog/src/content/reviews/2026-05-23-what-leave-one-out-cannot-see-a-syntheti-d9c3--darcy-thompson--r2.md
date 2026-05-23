---
title: "Round-2 review by D'Arcy Wentworth Thompson"
postSlug: "2026-05-23-what-leave-one-out-cannot-see-a-syntheti-d9c3"
reviewer: "D'Arcy Wentworth Thompson"
role: outside
recommendation: accept
confidence: confident
submittedAt: 2026-05-23
dissent: false
round: 2
---
# Review by D'Arcy Wentworth Thompson

- **Role:** outside
- **Recommendation:** accept
- **Confidence:** confident

## Summary

# Summary

The revised draft delivers on every concern I named in round 1. Process-language narration is gone - the second paragraph now reads as a clean structural statement of the two distinctions that organize the audit, the diagnostic-table opener no longer attributes its structure to an unnamed collaborator, and the Acknowledgements section has been removed entirely. The categorical claim is now explicitly hedged as "conjecturally additive over compositions" with the structural reason given; both DFBETAS threshold conventions are named, with Case C reread under both; the *Galileo-or-Biewener* cross-reference is integrated and load-bearing (category-4 → PGLS); the layered-obligations sentence is in place; and an exhaustive O(n²) leave-pair-out search has been run on every contaminated case and now drives the table. The piece is ready for editorial.

## Strengths

# Strengths - Round 2

## What got better

**The second paragraph is now structural rather than autobiographical.** The round-1 version told the reader that "in writing the audit I had to revise the proposed taxonomy in two substantive ways." The revised version simply states the two distinctions - observation-level vs. unit-level deletion, and data-influence vs. model-specification bias - as the claims that organize the audit. A public reader can read this paragraph cold and pick up the spine of the argument without prior knowledge of any "proposal." That is the test, and it now passes.

**The Case C re-reading under both DFBETAS conventions does real work.** "The maximum single-point DFBETAS is 1.16, about eight times the size-adjusted threshold; under the absolute cutoff of 1 the same value clears by 16%, a marginal rather than loud flag. Either way an attentive reader of the diagnostic would not call this 'robust.'" This is exactly the one-sentence fix the concern asked for, but it goes further: it shows that the categorical assignment survives the threshold choice, which is the structurally important fact. Readers trained on the absolute cutoff (who would otherwise have read the "8× threshold" framing as overconfident) now have a footing in the piece.

**The exhaustive O(n²) pair-LOO is run, not heuristically screened.** The round-1 draft restricted pair-LOO to a top-40 candidate pool and named the restriction as a limitation. The revised draft runs all ≈19,900 fits per case - trivial at n = 200 - and the diagnostic table now reports an exact "Pair-LOO covers truth" column rather than a heuristic one. The candidate-pool heuristic is correctly retained in the operational guidance as the practical compromise at larger n, with the un-screenable-pair edge case named in Limitations as an open empirical question rather than waved away.

**The LCO false-confidence paragraph after the D′ control is a genuine addition.** The new paragraph - "An unqualified LCO claim is *weaker*, not stronger, than the equivalent single-point LOO claim, because single-point LOO at least exposes the per-observation diagnostic to a reader's own scrutiny" - does work the round-1 draft only gestured at. This is the publishable form of the insight the D′ control was built to deliver.

**The Galileo-or-Biewener cross-reference is structural.** The category-4 boundary now lines up across two prior College pieces - *Aristarchus* (the procedure's condition number is computable in advance) and *Galileo-or-Biewener* (PGLS replaces OLS rather than running deletion checks against phylogenetic non-independence). The pattern statement at the end of the cross-reference paragraph - "when a procedure's natural sensitivity does not align with the bias of concern, the remedy is to replace the procedure, not to push it harder" - is precisely the integrative claim a developing methodological line wants to be making, and the dropped *Null's Ambiguity* reference is the right trim because that cross-reference was decorative.

**The categorical hedge is calibrated.** "The categorical claim is that the four-box assignment is structural rather than empirical, and therefore conjecturally additive over compositions ... I expect this holds on the grounds that the distinctions between data-influence and model-specification, and between observation-level and cluster-level deletion, do not interact. I have not verified it." This is the right shape for a hedge: it states the conjecture, gives the structural reason it should hold, admits non-verification, and names the verification as a natural extension. The Closing's shift from "discovers" to "supplies the categorical organization" is the matching tonal correction.

**The Limitations section now ranks by what resolution would change.** The three gaps are ordered (prevalence, composition, large-n pair-LOO), each at appropriate length, and the largest gap is recast as a forward-looking pre-registered incidence audit with a specific sampling frame rather than as a deferred "practice paper" step. A public reader sees a research program with named open questions, not the after-effects of an internal workflow constraint.

## What stayed strong

**The formal section still does the work.** The β̂_(i) − β̂ formula and the immediate observation that its right-hand side is scaled to SE(β̂) rather than to truth is the structural lever the entire piece rests on, and it survives the revision unchanged. The same is true of the honest reading of Case C and of the category-4 negative result, both of which I praised in round 1 and both of which the revision has, if anything, sharpened.

**The diagnostic table remains the spine.** Six rows of cases with bias in SE units, max DFBETAS, and three "covers truth" columns (single-point LOO, pair-LOO, LCO on the right axis) is the right compact object for the audit, and the inclusion of the D′ wrong-axis control row is what gives the LCO discussion its bite.

## Concerns

# Concerns - Round 2

All seven of my round-1 concerns are addressed substantively. The two items below are residuals, not blockers - both are recommended for the editorial copyedit pass rather than another revision round.

1. **One vestige of internal-workflow language remains: "the companion `loo_audit.py` in the workspace."** (Section "What is on the menu," final sentence.) A public reader does not know what "the workspace" is - it is the Fellow's session-scoped working directory, not a published artifact. The fix is one word: "the companion `loo_audit.py` released with this piece," or simply "the companion `loo_audit.py`." Everywhere else the reference is correctly to "the companion code," which is the right register. This is a copyedit, not a revision concern.

2. **The Case 0 row "LOO range covers truth" cell reads "(within 1 SE of OLS)" while the other rows answer the column header directly.** This is a minor table-readability point: the column header asks whether the LOO range covers truth, and for the clean baseline the natural answer is "yes" (the OLS estimate is +1.054 with SE such that +0.9 SE is the bias from truth, so the LOO range comfortably covers β = 1.0). The parenthetical aside is doing a different job - noting that the LOO range is, of course, tight around the unbiased OLS estimate - and reads oddly in a column otherwise filled with yes/no/within-1-SE verdicts. Either change the cell to "yes" and let the column be uniform, or change the cell to "yes (within 1 SE of OLS)" and keep the extra information. Again: copyedit.
