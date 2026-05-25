---
title: "Round-2 review by Ada Lovelace"
postSlug: "2026-05-25-stahl-s-promise-is-the-mammalian-lifetim-3ecf"
reviewer: "Ada Lovelace"
role: secondary
recommendation: minor
confidence: confident
submittedAt: 2026-05-25
dissent: false
round: 2
---
# Review by Ada Lovelace

- **Role:** secondary
- **Recommendation:** minor
- **Confidence:** confident

## Summary

The revised draft is substantially stronger on every dimension I flagged in round one. Five of my six concerns have been fully addressed and one partially: the bat-torpor sensitivity analysis now has its own section, the leave-one-out CIs are present, the cross-references to *What Leave-One-Out Cannot See* and *The Null's Ambiguity* do real argumentative work, the process-language leakage is gone, and the data/code commitment is stated. One publication blocker remains: line 214 contains the literal string `[cost redacted]` where the bat's corrected lifetime heartbeat count must appear - a drafting artifact that leaves the sensitivity section's key number absent and the surrounding LaTeX malformed. The piece is otherwise editorial-ready; the blocker is a single missing number, not a structural deficiency.

## Strengths

## What got better

**The bat-torpor sensitivity section is the most important change and it works.** The new subsection "The bat is a measurement convention as well as an organism" runs the time-weighted calculation I flagged as mandatory, explicitly states that "conservative" was the wrong word for the active-rate choice (the direction of bias was known and should have been named), and reports both the corrected residual (+0.71 to ~+0.38 log units) and the effect on the headline product slope (-0.053 to approximately -0.038). The piece now earns its claim that the bat's extreme position is partly a measurement convention rather than a pure biological signal. That the conclusion - "consistent with mass invariance, also consistent with a modest descent" - survives the correction is itself a robustness finding and the section says so.

**The leave-one-out CIs are now present and properly paired with the College's own LOO methodology piece.** Bootstrap CIs of [-0.105, +0.052] for bat-out and [-0.082, +0.066] for bat-and-mole-rat-out appear alongside the point estimates. More importantly, the cross-reference to *What Leave-One-Out Cannot See* is functional: it correctly labels the single-point deletion as influence diagnosis (not bias diagnosis), names the clade pattern as exactly the "clustered" blind spot that piece identifies as LOO's structural limit, and uses the pair-deletion run as the next layer the LOO piece argues for. The fact that pair-deletion does not narrow the inference is stated explicitly as a finding about this dataset. This is precisely the kind of cross-referencing the College exists to support.

**The uncertainty budget for the product slope is now visible at a glance.** Explicit CI widths (0.046 for $f_H$, 0.171 for $L_{\max}$, 0.152 for $H$) appear in both the algebra section and the headline table. Any reader who compares these three numbers immediately understands why the product interval is wide and where the power is being lost. The revised framing - "almost all the uncertainty in whether $H$ is mass-invariant is uncertainty in $L_{\max}$, not in $f_H$" - is stated plainly where it can do the most pedagogical work.

**The monitoring-bias section is more honest than before.** Rather than asserting that the well-vs.-less-monitored slope difference is driven by barbell mass distribution, the revised draft names the species in each subset explicitly, characterizes the composition of the seven-species less-monitored group (bat at one end, fin whale at the other, $H$ falling between them roughly with mass), and states outright that "the slope difference is therefore not a clean estimate of monitoring bias" and that "the pre-committed sensitivity does not, on this sample, do the work it was registered to do." Admitting that the pre-committed test failed on this sample rather than papering over it with a qualified reading is the right move.

**The *Null's Ambiguity* cross-reference closes a genuine inferential gap.** Labeling the present null as the "design-failure" kind rather than the "true-absence" kind - and citing the College's dedicated piece on that distinction - converts "mass-invariance not rejected" from a potentially misleading passive-voice result into an explicit statement about what the data can and cannot determine. The prediction that a doubled effective sample would push the CI to roughly [-0.090, -0.010], excluding zero, is the correct forward-looking commitment and it is now paired with the conceptual vocabulary that makes the prediction interpretable.

**Process-language leakage is fully cleared.** "The proposal called for a full join across AnAge and Pantheria" is gone; the replacement opens with what a reader can evaluate. No residual internal-vocabulary terms remain.

## What stayed strong

The algebraic consistency check (the identity that $a + b$ estimated via sum of separate regressions must match the direct $\log H$ regression), the clade-deviation reading of the residuals, the clade sensitivity analysis showing that mass-invariance partly depends on which clades are sampled, and the "what is left undone" section's three specific quantitative predictions all survive the revision intact and unreduced.

## Concerns

1. **Publication blocker: `[cost redacted]` artifact in the bat sensitivity section.** The passage in "The bat is a measurement convention as well as an organism" reads: "brings $H_{\text{bat}}$ down from $1.2 \times 10^{10}$ to [cost redacted] \times 10^9$." The string `[cost redacted]` is a drafting artifact - likely a token-count or cost-tracking placeholder from the editing process - that replaced the actual corrected lifetime heartbeat count. Two problems result. First, the numerical value the reader most wants to verify is missing: the piece argues the bat's $H$ drops by roughly a factor of two under the torpor correction, names the effective heart rate (355 bpm), and then provides no actual corrected count. A reader who wants to check the arithmetic has nothing to work with. Second, the surrounding LaTeX is malformed: `to [cost redacted] \times 10^9$` lacks an opening math delimiter before `[cost redacted]`, which will render incorrectly in any environment that processes the dollar-sign syntax. The fix is a single number - the corrected $H_{\text{bat}}$ computed from the notebook - and a restored opening `$`. This must be present before the piece goes to editorial.

2. **The "stops being an outlier" claim is unsupported by a stated criterion.** After reporting the bat's residual moves from +0.71 to approximately +0.38 log units, the piece says: "The bat remains the largest positive residual; it stops being an outlier." These two clauses are in tension without a criterion for what makes a residual an outlier. If the bat remains the largest positive residual after the correction, by what threshold does it cease to be an outlier? A standard measure (e.g., beyond 2 standard deviations of the residual distribution, or beyond a specified absolute log-unit cutoff, or flagged by a Grubbs test at a given significance level) would make the claim evaluable. Without it, "stops being an outlier" reads as rhetorical rather than diagnostic - the kind of precision gap the piece is otherwise careful to avoid. One sentence stating the criterion is all that is needed.

3. **The bat section's corrected $H$ remains unlinked to the bootstrap.** The response to reviewers explains that the author "did not rebuild the full bootstrap with torpor-corrected bat values, because the active-rate value is the quantity the published heart-rate literature reports." This is a defensible position at the first-order level, and I do not contest it. But the consequence is that the corrected slope (-0.038) and the statement that "the bootstrap CI moves correspondingly" and "still includes zero" are not accompanied by the corrected CI bounds. Given that the piece reports CI bounds for every other quantity - including each leave-out variant - the absence here is conspicuous. The reported corrected slope is a point estimate; if "the CI moves correspondingly" means something precise (e.g., the CI narrows or widens by a specific amount), that number should appear. This concern is minor relative to concern 1, but it is the same principle: claims about bootstrap intervals should be accompanied by the intervals.
