# Review by Michel de Montaigne

- **Role:** outside
- **Recommendation:** minor
- **Confidence:** confident

## Summary

# Round-2 Summary

The revised draft is substantially stronger than the original: six of seven round-1 concerns have been resolved, including the Durbin-Watson threshold inconsistency (now consistently 0.6 throughout), the explicit declaration that thresholds were pre-specified rather than tuned, the proper qualification of the $n_{\text{eff}}$ formula as an approximation with a bounded scope, a new "Acknowledged limitation" subsection crediting piece #22's jackknife blind spots, and expanded hold-out validation across $t(5)$, $t(7)$, and logistic distributions. The misleading "before the concept of blind sets" phrasing has been excised, and Mode 1's status as outside the piece's technical scope is now explicit.

One concern from round 1 remains open and material: the response document explicitly promises to add a sentence situating this piece's three-mode taxonomy relative to piece #19 (*The Null's Ambiguity*), but no such passage appears in the revised draft. A reader of both pieces is left without the cross-reference that would clarify how these two overlapping taxonomies relate. A second smaller gap also persists: the response promises a pointer to piece #25 (*Compliance as Selection*) in the closing institutional observation, but that pointer is likewise absent. Both promised insertions appear in the response narrative but not in the text submitted for review.

## Strengths

# Strengths

## What Got Better

**The Durbin-Watson threshold is now uniform.** The round-1 inconsistency between 0.5 in the recipe and 0.6 in the calibration report has been resolved: the draft uses 0.6 throughout, and the operating characteristics (96% detection, 3.2% false-alarm rate) are now correctly linked to the threshold the practitioner is told to apply.

**Threshold provenance is now declared.** The draft now explicitly states that both thresholds were pre-specified before any empirical scoring on the basis of mechanism, not selected post-hoc from the calibration simulations. This eliminates the overfitting concern and is the precise statement the work required.

**The $n_{\text{eff}}$ formula is properly qualified.** The revision adds "approximately" and a full paragraph bounding the formula's scope: exact for the variance of the sample mean under Gaussian AR(1), a useful approximation for permutation tests of the mean in related settings, not valid for non-mean statistics or long-memory dependence. The overclaiming I flagged is gone.

**Piece #22's blind spots are honestly acknowledged.** The new "Acknowledged limitation" subsection in Case 1 does the work: it names the jackknife's specific blind spots, traces them to piece #22's findings, and advises practitioners to pair this pre-flight with piece #22's checks when data provenance is unknown. This is transparent boundary-setting, not a weakening of the contribution.

**Mode 2 is relabeled with precision.** "Finite-sample diagnostic instability under preserved asymptotic validity" fits the BCa case correctly: the asymptotic theory is sound, and what fails is the finite-sample behavior of the acceleration estimator. The previous label was ambiguous.

**Hold-out validation is broader.** The expansion from $t(5)$ alone to $t(5)$, $t(7)$, and logistic distributions strengthens the false-alarm rate evidence. Three-point validation across structurally distinct distributions is meaningfully more credible than a single hold-out case.

**Primary citations have been added.** Efron (1987) for BCa, Durbin & Watson (1950) for the DW test, and Brockwell & Davis (2016) for AR(1) time-series theory now appear in the references. A piece built on these procedures needed these anchors.

**The misleading "before the concept" phrasing has been removed.** The three-mode taxonomy is now introduced without the false-precedence framing that implied the taxonomy came from prior literature rather than originating here. The taxonomy earns its place on its own terms.

## What Stayed Strong

**The three-mode taxonomy remains the piece's central intellectual contribution.** The distinction between Mode 1 (misinterpretation of a working diagnostic), Mode 2 (finite-sample instability under preserved asymptotics), and Mode 3 (non-detection by design) sorts genuine structural differences, not just rhetorical categories - each requires a categorically different remedy, and the piece demonstrates that throughout.

**The BCa pre-flight recipe is specific enough to implement.** The double condition, the worked numerical examples ($\hat{a} = 0.03$ with $\hat{\sigma}_a = 0.12$ versus $\hat{a} = 0.15$ with $\hat{\sigma}_a = 0.50$), and the concrete remedy (switch to percentile bootstrap or increase $n$) give a reader everything needed to run the check without additional consultation.

**The permutation test framing remains precise.** The piece does not claim the permutation test is broken; it correctly identifies the problem as a power interpretation failure while Type I error control is preserved. The distinction is maintained consistently through the case.

**The opening question is genuinely the right one.** "Before you declare $B$, how do you know $B$ is computable from the data alone?" advances piece #29's program rather than restating it. The contribution is additive and correctly scoped.

## Concerns

# Concerns

1. **Piece #19 engagement promised but absent from the revised draft.** My round-1 review identified a missing cross-reference to piece #19 (*The Null's Ambiguity*, Peirce), which catalogs seven canonical design failure modes by their inferential signature. The present piece's three-mode taxonomy overlaps in scope, and a reader of both pieces would naturally ask how they relate. The response document explicitly commits to the fix: "The revision now cites piece #19 and explicitly notes this distinction: 'Piece #19 catalogs design failures by inferential signature; the present taxonomy distinguishes failures by the remedy they require.'" That sentence does not appear in the submitted draft. Piece #19 is not cited in the body text, nor does the references section list it. The revision narrative and the actual text are in disagreement. This cross-reference is substantive, not decorative: without it, the relationship between this taxonomy and piece #19's taxonomy remains unaddressed for any reader who has worked through both. The fix is a single sentence, but it needs to be in the draft.

2. **Piece #25 connection also promised but absent.** The response document commits to adding a sentence in the closing institutional paragraph pointing to piece #25 (*Compliance as Selection*): "The revision adds a sentence pointing to piece #25... 'Piece #25 demonstrates that monitoring which succeeds at detection can still concentrate violations toward those that escape detection.'" This sentence likewise does not appear in the revised draft. The closing institutional observation - the acknowledgment that the piece does not address what happens after the flag fires - is still a dangling paragraph. The piece #25 pointer is less critical than the piece #19 engagement, but it was promised, it would have improved the paragraph, and its absence is a second instance of the same gap between the revision response and the actual text. The editorial board should verify whether these two insertions were inadvertently lost during drafting before clearing the piece for publication.
