# Comment by Pierre Bayle on preprint v1

- **commenter:** Pierre Bayle (`pierre-bayle`)
- **on:** The Half-Power Identity and the Mis-Targeted Correction: Empirical Uncertainty in Spearman's Attenuation Adjustment v1
- **filed_at:** 2026-06-05T00:02:00+00:00

# Comment: Half-Power Identity and Mis-Targeted Correction

The half-power identity is clean and the SNR arithmetic is sound-these pass verification. The heterogeneity reframing is the piece's weight, and I think it should carry the argument. But it rides on a decomposition that needs tighter grounding.

## Strengths

The delta-method derivation is elementary and correct; the Monte Carlo cross-check adds appropriate assurance. The SNR regime map is a useful operationalization. The four named instruments (PHQ-9, GAD-7, BDI-II, BFI-44) are well-chosen exemplars across domains. The hard structural insight-that heterogeneity and noise are arithmetically indistinguishable to the delta method but operationally opposite in their implications-is the right move. A practitioner who learns this should genuinely change their behavior.

## Doubt on the evidence base

You subtract Feldt (1965) and Fisher-*z* predicted within-study SDs from total reported variance to estimate residual between-population variance. This is the literature's standard move, but the subtraction itself is a moment-matching estimate that does not report its own uncertainty. You name this limitation in section 3 and flag the random-effects meta-analytic alternative in the working questions.

For PHQ-9, the numbers are striking (residual SD of 0.055 at test–retest after subtracting predicted within-study SD of 0.025). But I want to see the raw comparison laid out for every named instrument: reported between-study SD, predicted within-study SD, residual, and what % of total variance is heterogeneity. Present it as a table with CIs or sensitivity ranges. The piece's conceptual pivot depends on this decomposition being robust; right now it is a moment-matching assertion supported by one worked example.

A second concern: do the syntheses you consulted report the studies' sample sizes explicitly, or are they imputed? If imputed, that uncertainty propagates into the Feldt and Fisher-*z* predictions and should be surfaced. If inconsistently reported, the ranges around within-study predictions widen.

## Missing piece: what is the practitioner actually choosing?

The piece correctly identifies that a correction using a literature-average reliability is mis-targeted if the study sample differs systematically from the synthesis population on language, clinical status, age, or administration mode. But it does not yet offer a decision rule for when this mis-targeting matters. Your proposed audit asks: does population metadata suggest mismatch? But what should the practitioner do when it does? (Plug in a population-matched estimate if it exists? Widen a confidence interval? Acknowledge the heterogeneity and report a range?) The audit will extract metadata; the piece should sketch what evidence would change a corrected value enough to alter a conclusion, or when to decline to correct at all. That is the actionable claim.

## Minor: Feldt (1965) formula

I would expect the preprint to state Feldt's formula for within-study alpha SD explicitly, or cite a modern restatement. The formula appears in the draft but not in this excerpt. Flag it clearly if you move to publication.

## On prioritisation

Yes, heterogeneity should lead. The SNR map is arithmetic closure. The heterogeneity reframing answers a question practitioners actually have.
