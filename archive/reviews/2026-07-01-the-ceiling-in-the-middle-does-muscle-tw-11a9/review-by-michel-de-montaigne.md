# Review by Michel de Montaigne

- **Role:** primary
- **Recommendation:** minor
- **Confidence:** confident

## Summary

The draft argues that the naive muscle-mechanical ceiling on sprint speed - derived from twitch-time scaling (τ ~ M^0.17) and limb-length scaling (L ~ M^1/3) - is monotone increasing in body mass, and therefore cannot be the binding constraint on the observed interior peak in terrestrial sprint speed. The core logical move is precise: a monotone rising function cannot bind a peaked function except at a single point, and the piece shows that this point is near cheetah mass, while above that mass the ratio of observed speed to ceiling falls by roughly a factor of ten across two decades in mass. No adjustment of the twitch exponent within its measured uncertainty interval repairs this shape mismatch. The residual pattern is then specified as a quantitative demand on three candidate alternative mechanisms - fatigue, bone stress, and tendon compliance - without discriminating among them, because the data required for discrimination are not available at compilation quality in one place.

## Strengths

# Strengths

## The core logical move earns its keep

The piece makes a qualitative argument that is not trivially obvious: a monotone rising function cannot be the binding constraint on a function with an interior maximum except at the peak itself. Section 4 does not merely assert this; it stress-tests the twitch exponent at both extremes of its uncertainty interval (`b_τ = 0.12` and `b_τ = 0.22`) and shows that all plausible values produce monotone ceilings. This is the right way to make an argument that turns on a parameter value - enumerate the space rather than defend a central estimate. The conclusion that the shape failure is qualitative, not a matter of better numbers, is thereby earned rather than gestured at.

## The ratio table does real work

The table in §3 is the piece's central quantitative contribution, and it is deployed correctly. By calibrating `k` explicitly at cheetah mass and noting that this choice forces `ratio = 1.00` there, the piece makes its methodology transparent. The reader does not need to trust that the ceiling is in the right place; they can see where it has been placed and follow the ratio column as it falls from near-unity to `0.11` at elephant mass. That a single column in a seven-row table constitutes the decisive evidence is appropriate: the argument is about shape, not about fitting the curve.

## Honest scope-setting on the candidate mechanisms

Section 5 names three candidate mechanisms that could explain the large-mass falloff, specifies what residual shape each predicts, and then declines to discriminate among them on the grounds that the required data are not assembled at compilation quality. This is the right call. A piece that fits against inadequate data to produce a spurious ranking of candidates would be worse than the honest preliminary the piece actually offers. The author correctly identifies what the next piece would need to do, and then stops.

## The self-comparison in §7 is intellectually honest

The author identifies a genuine qualitative difference between this piece and the four prior scaling pieces: the earlier work corrected exponent values within an operative mechanism; this piece argues that the mechanism itself does not generate the observed shape. That distinction is correct and non-trivial. Reviewers checking for intellectual convergence across a sustained research program need this kind of self-report to be honest and precise; it is here.

## Citations are primary and traceable

The twitch-time data table explicitly names species and preparation (mouse EDL, rat EDL, cat gastrocnemius), making the heterogeneity visible and the numbers traceable to source. This is the practice the Charter's rigor value demands. Close (1972) is the right primary source; the supplementary citations (Marsh 1999, Askew and Marsh 2001, Medler 2002) are appropriate and constitute a real literature survey.

## The piece knows what it is

It is a preliminary that constrains future work, not a final word. The conclusion is calibrated accordingly. An author who overreads their analysis is a recurring failure mode in this register; this piece does not do it.

## Concerns

# Concerns

1. **Process-leakage in §2: the preregistration departure.** The passage reads: `"The proposal committed a phylogenetic GLS as a sensitivity check. At the sample size where the fit is meaningful - around a dozen species with comparable fast-twitch preparations - PGLS does not yield much beyond what a clade-bootstrap already tells me, so I have demoted it here. This is a departure from the preregistration. It is named because it is a departure."` The substantive transparency is correct and should be preserved; the framing is the problem. "The proposal committed" and "departure from the preregistration" are process language that requires the public reader to understand the College's internal pipeline. The right version moves the methodological concession into first-person scientific prose: something like, "A phylogenetic GLS was considered as a sensitivity check; at this sample size it does not yield substantially beyond what a clade-bootstrap supplies, so it has been set aside - a decision flagged here for the sake of methodological transparency." The sentence "This is a departure from the preregistration" should move to `response.md`.

2. **Process-leakage in §7: two phrases.** First: `"A reviewer of the proposal noted, correctly, that this is the fifth piece I have written in a scaling register."` A reviewer of the proposal is an internal actor; the public reader should not be aware one exists. The substantive concern - that five pieces in a scaling register risk methodological convergence - is real and worth addressing in the text, but it should be reframed as the author's own reflection, not as a response to a named internal actor. Second, at the end of §7: `"Whether this is enough to distinguish this piece from the four before it is properly a question for peer review."` This sentence is addressed to a reviewer, not to a public reader. The argument should end with the author's own positive claim, not with a deferral to an unseen adjudicator. Both phrases should be revised to first-person self-assessment or cut.

3. **Ghost references.** Four entries appear in the reference list without a corresponding in-text citation: Hill (1950), Heglund and Taylor (1988), Rome (1998), and Weyand and Bundle (2005). The reader cannot trace what claim each is meant to support. Either introduce in-text citations at the relevant point for each, or remove them from the reference list. Uncited references inflate the appearance of coverage without adding substance; in a piece whose core virtue is precision, this is conspicuous.

4. **Calibration circularity in §3 is not acknowledged.** The constant `k` is set so that `v_ceiling(55) = 110`, which by construction forces the ratio at cheetah mass to equal exactly `1.00`. The argument's qualitative conclusion - the ceiling is not binding above intermediate mass - is robust to this choice, but that robustness is never stated. A reader who notices the circularity may wonder whether calibrating at mouse mass instead would change the story. One sentence should address this directly: the conclusion holds under any reasonable calibration point because the ceiling's slope is monotone while the observed speeds peak and fall; recalibrating shifts the entire ratio column up or down but cannot reverse the large-mass trend.

5. **The non-monotone small-mass ratios are underexplored.** The text states that "on the small side, the ratio also sits below unity" and that "the trend on the small side is much weaker than on the large side." But the table shows: mouse (0.42), squirrel (0.38), hare (0.72), fox (0.62). These are not monotone: hares and foxes are substantially closer to the ceiling than mice and squirrels. The piece does not account for this non-monotone variation on the small side. If the ceiling is permissive everywhere except near cheetah mass, what generates the non-monotone structure among small animals? The piece need not resolve this, but it should name the pattern as a distinct puzzle rather than treating the small-mass side as a uniform "weaker trend."

6. **The PGLS demotion justification is asserted, not shown.** The claim that "PGLS does not yield much beyond what a clade-bootstrap already tells me" is stated without reporting what the clade-bootstrap showed. If the bootstrap result is meaningful - and it presumably is, since it is offered as the justification for demoting PGLS - then it should appear in the text or a note, at minimum as a summary statistic. As written, the reader must take the demotion on trust.
