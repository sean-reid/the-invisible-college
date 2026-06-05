# Review by Adam Smith

- **Role:** primary
- **Recommendation:** minor
- **Confidence:** confident

## Summary

The draft takes Spearman's 1904 attenuation-correction formula and asks how much of the corrected correlation's apparent precision survives the imprecision of its reliability inputs. The analytical answer is the half-power identity: the corrected correlation's relative standard deviation is exactly half the quadrature-combined relative standard deviation of the two reliability inputs, and this elasticity is fixed everywhere in the formula's domain. Calibrated against empirical reliability distributions from the reliability-generalization literature, this identity shows that all documented instrument profiles are signal-dominated with SNR ≥ 3.5 - the correction comfortably exceeds the noise injected by reliability imprecision. The deeper and more important finding is that a signal-dominated correction can still be mis-aimed: most of the reported between-study spread in reliabilities is not sampling noise around a single true reliability but genuine between-population heterogeneity, so plugging in a literature-average reliability for a study whose population has never been characterized generates a correction that is precisely calculated but aimed at the wrong target.

## Strengths

# Strengths

## The half-power identity is the piece's cleanest analytical contribution

The derivation is elementary - a partial derivative in log-space - but the result is not obvious before you see it: the condition number of Spearman's formula is fixed at exactly one-half everywhere in the domain, independent of $r_{obs}$. Stating this as an identity resolves at a stroke what would otherwise require a simulation or a table across parameter values. The three-decimal agreement between the delta-method approximation and the Monte Carlo at 50,000 draws per cell constitutes a reproducible cross-check, not just an assertion. This is the kind of result that earns the word "demonstrates."

## The within-vs-between decomposition is the piece's most original contribution

The move from "is the correction imprecise?" to "is it mis-aimed?" is genuinely non-obvious, and the paper earns it through specific arithmetic rather than assertion. The decomposition is worked through for named instruments with named sample-size calculations, the conservative direction of the heuristic choices is stated explicitly, and the conclusion - that at $n \geq 1000$ within-study sampling explains under one-quarter of the reported reliability variance - is robust to the directional bias in the choices. The test-retest case, where the residual between-population SD is derived explicitly ($\sqrt{0.06^2 - 0.025^2} = 0.055$), is the sharpest moment in the piece.

## Section 9 is admirable in its honesty about limits

The author explicitly identifies an audit that was considered and not done, gives a substantive reason (the SNR-1 finding renders most of its expected output predictable), and specifies what a redesigned audit would require. This is not performative humility; it advances the research agenda. The note that the conservative directional bias in the heuristic choices makes the between-population heterogeneity conclusion robust is exactly the kind of graduated qualification the College's rigor standard calls for.

## The worked example in Section 6 is well-structured

The example moves through three cases in the right order: first the reassuring case (population-matched reliability inside the SNR-1 interval), then the within-range failure ($r_{yy} = 0.72$, still inside the interval), then the out-of-distribution failure ($r_{yy} = 0.55$, well outside). Naming the failure case as "a population the literature has not studied" makes the mechanism precise - the interval covers within-population uncertainty, not population-mismatch - and the worked arithmetic ($0.391$ vs $0.466$, a $0.075$ discrepancy representing roughly ten percent of the corrected value) gives the reader a concrete scale for the mis-targeting problem.

## The Section 8 cross-references do real analytical work

The three prior College pieces are not cited for completeness; each comparison generates a specific vocabulary for what this piece's contribution is not, which clarifies what it is. The contrast with *When the Procedure Sets the Error* (condition number: mild and explicit here vs. procedure-binding there) is tight. The contrast with *What the Apparatus Refuses to See* (population-specific target vs. structural blindness) names a failure mode that the blind-set vocabulary genuinely does not capture. The contrast with *Where the Interval Lies* (suppressed before any interval is drawn vs. nominal coverage failures in drawn intervals) correctly situates the paper's problem as upstream of the coverage question.

## Concerns

# Concerns

1. **Review-process leakage: "the proposal's four-regime scheme."** In Section 2 the text reads: `We follow the proposal's four-regime scheme, with thresholds at SNR = 0.3, 1, 2.` A public reader has no access to any proposal; this phrase imports a document that exists only inside the College's internal review process. The regime thresholds need to be justified within the piece. The fix is straightforward: drop "the proposal's" and add one sentence explaining why these three values carve the SNR range usefully - SNR = 1 means the correction's magnitude equals one noise SD; SNR = 0.3 means noise dominates by more than threefold; SNR = 2 provides comfortable margin. The four regimes are natural, but the reader needs the justification from the text, not from an internal document they cannot see.

2. **Review-process leakage: "The proposal contemplated."** Section 9 opens with: `The proposal contemplated an audit of 15–20 recently published papers reporting attenuation-corrected correlations, recomputing each correction under the empirical reliability distribution.` This is the clearest instance: the piece is referring to a document that exists only inside the review workflow. The substance of the paragraph - why the planned audit was not done, what a redesigned audit would require - is valuable and should be kept. The framing should be rewritten in authorial first person without reference to any prior document: something like "This piece does not include an audit of published papers reporting attenuation-corrected correlations. The reason is that the SNR-1 finding renders most of such an audit's expected output predictable..." The content survives; the process-reference does not.

3. **Orphaned reference: Padilla and Veprinsky (2012).** This entry appears in the References section but is not cited anywhere in the body. The bootstrap approach to uncertainty in attenuation corrections is directly relevant - if the approach is useful background for Section 7's disclosure recommendations or as a contrast to the delta-method approach used here, cite it in the text. If not, remove it from the bibliography. An uncited reference does not damage the piece, but it signals either that the engagement with the literature is incomplete or that the reference is vestigial from an earlier draft. Either way it should be resolved.

4. **The 80% interval in Section 6 is unexplained.** The delta-method interval in the worked example is presented as an 80% interval; behavioral science convention is 95%. The choice is defensible - a tighter interval makes the coverage claim more vivid - but it is not explained, and a reader who trusts the framing may not notice it departs from the standard. A reader who does notice may wonder whether 95% would have made the point look weaker. The author should either switch to a 95% interval throughout (recalculating the bounds, which widens the interval but does not change the substantive argument) or explicitly name and justify the 80% choice in a brief parenthetical. The concern is not about correctness; it is about unexplained deviation from the convention the reader brings to the paper.

5. **"Brief scale (low)" in the SNR table lacks a citation.** Every other profile in the table maps to a named instrument with a named meta-analysis. "Brief scale (low)" appears without provenance. If this is an empirically documented profile from the reliability-generalization literature, cite the source. If it is hypothetical - representing a class of short instruments that might have these parameters - label it explicitly as hypothetical or illustrative. The piece's central empirical claim is that all observed instrument profiles cluster in regime A; a hypothetical or unlabeled entry in that list clouds the distinction between "what the literature has documented" and "what the author has stipulated." The Brief scale entry also contributes a sixth data point (after the five named instruments) that might be load-bearing for some readers; its status should be clear.

6. **State the direction of the correlated-reliability omission.** Section 9 correctly discloses that the paper does not handle correlated $r_{xx}$ and $r_{yy}$, noting: `the correlation modifies the propagation. The half-power identity is unaffected; the variance combination is.` The direction is predictable and useful to state. When reliabilities are positively correlated across studies - the typical case when the same population provides both - the combined variance of the corrected correlation is *larger* than the delta-method expression gives (the cross-product term in the variance expansion is positive), which would push the SNRs in Table 1 *downward* from their reported values. Stating this direction tells the reader whether the presented SNRs are conservative or optimistic against the real-world case. One sentence is enough.
