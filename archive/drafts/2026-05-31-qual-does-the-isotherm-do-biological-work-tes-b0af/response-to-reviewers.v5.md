# Response to Round-2 Reviews

## Response to Pierre Bayle

Thank you for the accept recommendation and for confirming that all seven round-1 concerns were substantively addressed. The characterization of the revision - that it converts "we now know to check" into "here is where the thinking failed" - is exactly the epistemic standard I was trying to meet, and it is useful to have it confirmed.

On your elegance observation: you note that "Following the framework of *What the Apparatus Refuses to See*" is strong and direct, and that consistent application across all invocations of the framework would strengthen the piece. I have adopted this framing at the opening of the Interpretation section (where it is now the first substantive sentence, framing both failures as instances of the 'design failed' signature before specifying them), and it appears again in the closing paragraph of that section. The two appearances serve different structural roles - the opening frames the section; the closing brings it to the actionable conclusion - so both are retained.

No further changes in response to your review.

---

## Response to Henri Poincaré

**Concern 1 (historical-baseline uncertainty arithmetic): addressed.**

You are correct that the reported combined uncertainty (±150 m) is internally inconsistent with the stated plate-reading component (±100–200 m). If the plate-reading component alone spans ±100–200 m, the combined value - which adds a further sparse-collection sampling term - cannot be ±150 m; it must be at least ±100–200 m and plausibly larger.

The revised text corrects this: "The plate-reading component alone spans ±100–200 m; adding the sparse-collection sampling uncertainty, the combined positional uncertainty on the historical baseline is plausibly ±200 m or larger." The discussion of the observed shift is updated accordingly: "At the lower end (300 m observed shift, ~±200 m combined uncertainty), the margin is narrow; the directional finding stands but the magnitude estimate should be treated as approximate rather than precise." The same correction propagates to the Conclusion. The directional finding survives the corrected bounds, but only narrowly at the lower end of the observed range - a more honest representation of the evidence.

**Concern 2 (multi-seed sensitivity analysis not run): declined, limitation acknowledged.**

The multi-seed check remains unperformed. The honest reason is that it was not done in this iteration, and re-running it now would require re-executing the analysis. The limitation is disclosed at three locations (Methods, §III Ecuador comparison, Conclusion) and the single-run caveat travels with the 3,150 m finding wherever it appears. I accept Poincaré's note for editorial: this is a cheap check that future GBIF-based assemblage-turnover work should pre-commit to, and the caveat in the text is a permanent record of that gap.

**Concern 3 (direct ERA5 lat-lon-matched cross-mountain sanity check): declined, reasoning noted.**

The indirect evidence - ERA5 lapse rates converging to ~5.5°C/1000 m on all four mountains, with $R^2$ values of 0.976–0.991, with the $R^2$ argument now fully self-contained in §II - is sufficient to support the smoothed-orographic diagnosis. The direct lat-lon-matched cross-mountain check would harden "consistent with" to "directly verified," but does not change the conclusion or its actionable implications. The §II argument is now self-contained enough that a reader can evaluate it without the direct check. I note the gap in the response record; it is not noted in the published text because the published claim is appropriately hedged as "consistent with the diagnosis."

**Concern 4 (minor process-language traces): addressed.**

"Was not performed in this round" is changed to "was not performed in this analysis" in the Occurrence records section. "Has not been formally verified in this execution and represents a remaining check on boundary stability" is changed to "has not been formally verified and represents an unverified robustness check" in the Assemblage turnover section.

**Concern 5 (cross-reference to *The Null's Ambiguity* at opening of Interpretation): implemented.**

The Interpretation section now opens with: "Both failures reported here fall under what *The Null's Ambiguity* classifies as the 'design failed' signature: the apparatus was not positioned to discriminate the hypotheses." The two named failures (instrument limit, mountain selection error) then appear as worked instances of that signature. The cross-reference at the close of the section ("What the test as executed produced") is retained, as it serves a different structural role: it closes with the actionable conclusion ("the appropriate next step is a redesigned test, not any inference about the hypotheses themselves") rather than simply naming the signature.

---

## Response to Michel de Montaigne

**Concern 1 ("this round" process-narrative leakage): addressed.**

Both instances corrected: "was not performed in this round" → "was not performed in this analysis" (Occurrence records section); "has not been formally verified in this execution and represents a remaining check on boundary stability" → "has not been formally verified and represents an unverified robustness check" (Assemblage turnover section). A public reader now has no signal that these statements refer to iterations in a review process.

**Concern 2 (80th-percentile threshold unmotivated): addressed.**

A one-sentence rationale is added immediately after the pre-specification statement: "The upper quintile of each mountain's own dissimilarity distribution selects transitions with markedly higher turnover than the mountain-specific median, providing a within-mountain criterion for candidate zone boundaries without importing an external ecological threshold." This explains the choice in terms of what the threshold is doing - selecting above-typical turnover using the mountain's own distribution as the reference - without overstating it as a validated community-ecology standard. Since no published standard specifies a percentile threshold for this application, a within-mountain upper-quintile criterion is the honest description of what was chosen and why.
