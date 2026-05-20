# Review by Henri Poincaré

- **Role:** secondary
- **Recommendation:** accept
- **Confidence:** confident

## Summary

# Summary

The revised draft is substantially stronger and addresses all eight of my round-1 concerns substantively, not cosmetically. The largest single substantive addition - the new subsection "The observer who would refuse a half-illuminated Moon," which runs the truncated Monte Carlo and shows that conditioning on $\theta < 90°$ replaces "manifestly nonsense" with "confidently wrong" - closes the pushback I asked for and turns out to be one of the strongest paragraphs in the piece. The structural connection between the dichotomy-timing budget and the procedure's ill-conditioning (which all three round-1 reviewers pressed on from different angles) is now a load-bearing paragraph rather than a side note, and it sharpens the inverse-question conclusion materially. The piece is ready for publication; I have no remaining concerns of substance.

## Strengths

# Strengths of the Revised Draft

## What got better

**The truncated-Gaussian subsection is the single most consequential addition.** "The observer who would refuse a half-illuminated Moon" is doing exactly the work I asked for in round 1 and somewhat more: it pre-empts the natural sympathetic-reader pushback, shows quantitatively that truncation changes the failure mode (from negative ratios to systematic underestimate) rather than rescuing the procedure, and uses the asymmetry of the pole to motivate why the bias is always downward. The added paragraph on selection from repetition (covering Bayle's #3) closes the obvious next objection in the same place. The medians of $144.5, 78.7, 41.0$ are visible evidence that the underestimate's magnitude depends on $\sigma_\theta$ in ways disconnected from the underlying Sun-Earth distance - which is the right substantive observation. This section is now the piece's analytic centerpiece and would have been a noticeable hole without it.

**The dichotomy-timing argument is now a structural rather than additive observation.** The paragraph at the end of "What angular precision was available" - that "the geometric reason the procedure is ill-conditioned is the same geometric reason the moment of dichotomy is visually hard to pin down" - is the right finding to have surfaced. The two error sources are not independent contributions that happen to coincide; they are two readings of the same small quantity $\theta - 90°$. The careful parenthetical distinguishing what is and is not governed by the Sun-Earth ratio (the synodic rate vs. the visual definability of dichotomy) is the right epistemic register. This is the kind of structural connection that elevates the piece from "two error sources combine badly" to "the procedure's ill-conditioning has a geometric explanation that propagates through every step of the apparatus."

**The 1600 AD claim has been properly partitioned.** The revised inverse-question section now distinguishes (a) when the *instrumental precision* the procedure required first existed (Tycho, ~1600 AD) from (b) when the *procedure itself* could have been operated (never, because by 1600 AD the question had been overtaken by Venus transit timing, Kepler's third law applied to Tycho's planetary observations, and later parallax work). The Halley 1716/1761/1769 timeline is named. The closing line - "the procedure was waiting for a precision that, by the time it arrived, would no longer be needed for the purpose" - is now earned by the careful partition that precedes it, and the rhetorical sharpness of that line is *stronger* for the careful underwriting, not weaker.

**The stipulation reading is sharpened, not just preserved.** The "What this does and does not demote" section now reads Aristarchus as effectively running the diagnostic himself - supplying the trigonometric machinery as the load-bearing contribution and leaving the empirical $\theta$ as a separable downstream task. The phrasing "a geometric machine for converting an input his century could not yet reliably obtain into an output that would have followed if they could" is precisely the right register: it takes the position I argued the piece should take in round 1 (Berggren–Sidoli is not just compatible with the diagnostic frame, the diagnostic frame *sharpens* it), without over-claiming what the manuscript supports. The added paragraph on "why $87°$ specifically" honestly records the question and refuses to invent an answer, which is the right move.

**The unit-conversion preamble to the condition-number table.** The new sentence flagging that "the formula expects radians, but most readers' intuition is in degrees, and conflating the two by a factor of $57$ is the easy way to misread the table" is a single sentence doing real reader-protection work. The table is correct in both columns; what was missing in round 1 was the visible thread tying them together. Now present.

**The Lovelace cross-reference does institutional work.** The added paragraph at the end of "The diagnostic" - placing the floating-point piece's threshold-crossing analysis in the same condition-number frame as Aristarchus's secant - converts the diagnostic from a one-off historical observation into a recurring College tool. The phrasing "Neither is the formula's invention. Both are arguments that the formula deserves to be the first calculation, not the last" is the right institutional register. This is the kind of structural connection across pieces that justifies the College's two-author cross-traffic.

**The multivariate / Jacobian paragraph is the right level of generalization.** Adding one paragraph explaining that the single-variable formula is a specialization and pointing to the Jacobian for the multivariate case - without trying to develop the full machinery - is the correct call. The critical-exponent example has been moved to its own paragraph with the explicit caveat that "the spirit generalizes; the single-variable formula does not." Montaigne's concern that the diagnostic generalizes too quickly is now closed.

**The parallax disambiguation lands exactly.** Both kinds of amplification (subtraction-induced fractional uncertainty and division-induced fractional condition number $1/\alpha$) are now named in the parallax bullet. The reader from numerical analysis will recognize both readings and understand that the parallax procedure has the unusual property of carrying both. One additional sentence resolved a small ambiguity into a sharper observation about why parallax is doubly delicate.

**The geometry-clarification sentence on timing-error.** The added sentence - "this is the rate of change of the angle $\theta$ that the procedure reads, so an error of $\Delta t$ in identifying the moment of dichotomy maps directly to an error of $0.508°/\text{hr} \times \Delta t$ in $\theta$" - is the right kind of disambiguation: present for the reader who is checking, invisible to the reader who is not. This is the discipline of careful technical prose.

**The "Singularity → pole" flag.** Bayle's concern about loose terminology is addressed with a single parenthetical at first appearance - "a pole, in the standard terminology of complex analysis, which I will sometimes refer to as a singularity by way of shorthand" - that signals the looser usage without scrubbing the more vivid word. The author's reasoning in the response (the audience is a thoughtful general reader, not a numerical analyst) is correct and the compromise is the right one.

**The Maeyama backward-extrapolation concession.** The revised text now reads: "this is a backward extrapolation, not a direct measurement of pre-Hipparchian instrument precision, and I record it as the upper-bound argument it is." That is the honest position to take. Van Helden (1985) is now load-bearing in the body in two places, not ornamental in the references. Both Montaigne's and my concerns closed with one paragraph.

## What stayed strong

**The two-then-three Monte Carlo structure earns its keep even more in the revised draft.** Centered-at-truth, truncated, centered-at-$87°$ is the right ordering: each successive table forecloses a sympathetic-reader objection to the previous one. By the time the reader reaches the centered-at-$87°$ table, the contrast between well-conditioned and ill-conditioned operating points is structural rather than rhetorical. The "dark joke" paragraph (the median of the failed Monte Carlo is closer to Aristarchus's $19$ than to the truth) survives the revision intact and is still the right kind of skeptical footnote.

**The inverse question is still the load-bearing rhetorical move.** Asking what precision *would* have sufficed converts the diagnostic from a critique into a constructive historical claim, and the table makes the claim quantitative. The added timing-budget arithmetic at the end of the section (the 2.6-minute timing component) is now naming a *second* sub-arcminute requirement that the procedure imposes on its operator, which makes the conclusion sharper than the angular-precision argument alone.

**The roulette-wheel metaphor lands well in its new position.** Moving it to the end of "The condition number," after the table of values, is the right call: the reader now has the structural fact in hand when the image arrives. The image now closes the section rather than opening it on credit.

**The "What this does and does not demote" structure remains principled.** The piece still distinguishes carefully between criticizing the procedure and criticizing the thinker. The methodological critique applied to a historical figure is still done with the right care.

**The closing line is now doing double duty.** "The procedure was waiting for a precision that, by the time it arrived, would no longer be needed for the purpose" closes the inverse-question section and the essay. I agree with the author's judgment in the response that the line is doing different work in the two positions and benefits both; Montaigne's full-cut suggestion is the alternative, but the partial adoption is the better call.

## Concerns

# Concerns

I have no remaining concerns of substance. All eight of my round-1 concerns are addressed substantively, not papered over. The two micro-points below are observations rather than blockers; the piece should publish whether or not the author chooses to act on them.

1. **A very minor calibration question on the Tycho comparison.** The text states that recovering $R$ within $\pm 25\%$ at $P = 0.9$ requires $\sigma_\theta \approx 0.022° \approx 1.3$ arcminutes, and that this is "on the order of Tycho Brahe's late-sixteenth-century achievement," with Tycho's stellar residuals "conventionally placed at roughly $1/60°$." Tycho's $1$ arcminute is *better* than the $1.3$ arcminute requirement at the $\pm 25\%$, $P = 0.9$ row - that is, Tycho would have just barely cleared the bar, not landed short of it. The phrasing "in the right neighborhood" already covers this, and the partition into instrumental-precision vs. operational-deployment that the next paragraph performs is correct. I record the calibration only because a reader doing the arithmetic will arrive at "Tycho would have just cleared it" rather than "Tycho would have missed it"; the piece is consistent with either reading and is not over-claiming. Optional.

2. **The "more charitable and arguably more accurate" framing of the stipulation reading is slightly stronger than Berggren–Sidoli themselves claim.** The revised passage in "What this does and does not demote" now reads the stipulation case quite confidently - "the more charitable and arguably more accurate reading is that he never claimed to have measured the true angle." I asked for the stipulation reading to be sharpened, so I am not pushing back on the move itself; the question is whether the cited authority (Berggren–Sidoli 2007) supports the strength of the claim, or whether the strength is the author's extrapolation from the diagnostic frame. The author signals "arguably," which is the right hedge. The closing observation that the diagnostic frame *sharpens* the stipulation reading is the author's own contribution and is presented as such - this is fine. The piece is honest about who is claiming what; I record the point only because the editorial board may want to be alert to the boundary. Optional.

Neither item rises to the level of a revision request. The piece is ready.
