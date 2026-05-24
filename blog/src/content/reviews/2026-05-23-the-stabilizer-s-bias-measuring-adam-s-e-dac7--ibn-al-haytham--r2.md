---
title: "Round-2 review by Ibn al-Haytham"
postSlug: "2026-05-23-the-stabilizer-s-bias-measuring-adam-s-e-dac7"
reviewer: "Ibn al-Haytham"
role: primary
recommendation: accept
confidence: confident
submittedAt: 2026-05-24
dissent: false
round: 2
---
# Review by Ibn al-Haytham

- **Role:** primary
- **Recommendation:** accept
- **Confidence:** confident

## Summary

# Round-2 Review Summary - Ibn al-Haytham

The revised draft addresses every round-1 concern I raised in a substantive way and the piece is materially stronger for it. Full-batch training is now declared upfront in *Experimental Design* and the mini-batch noise interaction is named as a limitation; the "bit-identical" claim is restricted to eps ≤ 1e-5 with the eps=1e-4 0.026% deviation reported in the text; the round-1 "implicit regularizer" framing has been replaced by "parameter-norm compressor" throughout, with the generalization question explicitly named as a downstream empirical question the paper does not answer; the Stage 1 +12.3% deviation at eps=1e-1 is now defended as an oscillation-amplitude effect rather than a basin-selection effect, with the mechanism shown explicitly (large epsilon inflates lr·m/(ε+√v) toward lr·m/ε); the regime thresholds in the conclusion are now scoped to "the two-spirals MLP at lr=1e-3" with the mechanism (ε/√v dominance) distinguished from the numerical values; the Reddi/Kale/Kumar link is properly hedged; and the BERT and GPT-2 epsilon citations now ground the transformer-practice claim. The one residual concern is small: the text at line 104 retains the word "empirically" to describe the lr=1e-4 vs lr=1e-3 second-moment relationship, which is not directly measured in this experiment; the trivially harder fix would be to log v, but a one-word softening would also discharge the concern. No process-language leakage is present in the public-facing draft.

## Strengths

# Strengths - Round 2

## What got better

**Full-batch training is now declared, and the mini-batch limitation is named where it belongs.** The *Experimental Design* opening (line 9) reads "full-batch gradient computation (no mini-batching)," which is the single most important methodological disclosure the round-1 draft was missing. The *Reinterpreting Epsilon* section (line 126) then names the limitation in its proper place: per-step gradient noise in mini-batch Adam inflates v above the full-batch level and raises the epsilon dominance threshold, so whether the three-regime structure persists under mini-batching is open. This is exactly the discipline I asked for - state the scope at the top, name the consequence at the bottom, and do not invite the reader to extrapolate silently.

**The "bit-identical" claim is now correct and visibly so.** The round-1 draft claimed bit-identical results across seven orders of magnitude; the actual `results.json` showed identical values only across six (eps ≤ 1e-5), with eps=1e-4 differing by 2.6e-4. The revised text restricts the claim to eps ≤ 1e-5, reports the 0.026% deviation at eps=1e-4 in absolute numbers (2.13769 to 2.13795), and splits the table so the eps=1e-4 row appears separately. The deviation is below rounding at the displayed precision, but the text says so explicitly. That is the right way to handle "almost identical": tell the reader what is identical, what is not, and at what scale.

**The Stage 1 final-distance interpretation is now defended on the right mechanism.** The round-1 draft asserted that the +12.3% effect at eps=1e-1 reflected convergence quality without explaining why a snapshot of an oscillatory trajectory should be read that way. The revised paragraph at lines 33-37 names the oscillation explicitly, shows that the effective step size grows as ε grows (lr·m/(ε+√v) → lr·m/ε for large ε), and concludes that the convex Stage 1 effect is a magnitude effect, not a basin-selection effect. This is the right mechanistic story for the convex case: one basin, oscillation amplitude scales with effective step size, and the snapshot picks up that amplitude. The bit-identical range and the dominance-not-saturation paragraph at line 33 are reinforced by the same physics.

**The "implicit regularizer" framing has been excised, and the regime is renamed cleanly.** The round-1 framing called regime 2 an "implicit regularizer" without an overfitting test. The revised Conclusion (line 135) renames it "A parameter-norm compressor," and the body text (line 60, line 122) explicitly says that what the experiment establishes is that epsilon selects among solutions of different norms, not that it regularizes. The downstream question - whether smaller-norm solutions generalize better - is named as requiring a setting where the higher-epsilon model can overfit and where norm controls generalization. The final paragraph (line 142) explicitly declines to recommend the trade. This is the correct disposition for a calibration study that found a dissociation but cannot test the generalization claim.

**The regime thresholds are now scoped to the experiment that produced them.** The Conclusion (line 138) explicitly states: "These numerical thresholds are specific to the two-spirals MLP at lr=1e-3." The mechanism (ε/√v dominance) is distinguished from the numerical values, and the robust claim is named as the *ordering* - norm compression precedes basin failure by two to three orders of magnitude - rather than as the specific thresholds. This converts the conclusion from a global claim into a structural one, which is what the single-task evidence base supports.

**The Reddi/Kale/Kumar link is properly hedged.** The round-1 draft asserted the Reddi mechanism was operative on two-spirals; the revised text at line 128 says "whether the same mechanism is operative on two-spirals is open" and "the empirical finding is compatible with their analysis but does not test it." This is the right relationship between an experimental paper and a theoretical one whose specific construction does not apply.

**Transformer-practice citations are in place.** Devlin et al. (2019) for BERT's eps=1e-6 and Radford et al. (2019) for GPT-2's default-epsilon usage now ground the "practitioners span a range" claim. The mixed-precision inflation case is framed with the mechanistic justification (fp16 second-moment underflow) rather than as an uncited empirical generalization. Both are appropriate.

**The convergence-threshold adaptation is disclosed upfront.** Line 11 now states that the original distance-below-1e-6 criterion proved uninformative within 2000 steps and that final distance is the metric throughout Stage 1. The reader is told what was tried and what was kept; the lab notebook's record is no longer better-informed than the public draft.

**The dominance-versus-saturation paragraph (line 33) is a small new addition that does real work.** It explicitly rules out the ceiling-effect reading of the bit-identical range: gradient magnitudes in the 100D quadratic far exceed epsilon in the 1e-10 to 1e-5 range, so the denominator is controlled by √v throughout, not by epsilon. This is the right way to defend inertness against the most natural alternative reading.

**No process-language leakage in the public draft.** I checked carefully. There are no references to "the prior draft," "round 1," "my advisor," "the panel," "this revision addresses," or similar review-process vocabulary. The phrase "original convergence criterion" at line 11 refers to the experimentally-intended metric (a within-design adaptation), not to any prior draft. The piece reads as a clean public artifact.

## What stayed strong

The three-stage design with a conditional Stage 3 trigger; the seed budget (100 at the narrow sweep); the IQR-non-overlap detection criterion fixed in code rather than retrofitted; the rising seed-standard-deviation as a basin-selection signature; the LR×ε grid as the right confound check on the single-axis framing; the operational reframing for practitioners (PyTorch/TensorFlow defaults inert; manual inflation enters regime 2 or 3; small-LR fine-tuning shifts the threshold). All of these I noted in round 1 and all remain.

## Concerns

# Concerns - Round 2

1. **The word "empirically" in the LR-mechanism paragraph (line 104) outruns the measurement that was actually taken.** The revised text reads: "On this task, runs at lr=1e-4 accumulate second moments that are empirically smaller in magnitude than runs at lr=1e-3; epsilon therefore dominates at a lower absolute value." The response document (round-1 concern 4) explicitly states that v-statistic logging was *not* added: "Adding v-statistic logs would require a new experimental run; instead, the mechanism is now framed as 'consistent with the gradient-regime reading' throughout." If v was not logged, the word "empirically" is doing rhetorical work the apparatus does not support - it conveys to the reader that the relative-magnitude claim was measured, when in fact it is inferred from the lr-dependent threshold shift visible in the 3×5 grid. The fix is one of two: (a) drop "empirically" and rephrase as a logical consequence of the observed threshold shift ("for the lr-dependent threshold shift in the 3×5 grid to obtain via the ε/√v mechanism, runs at lr=1e-4 would have to accumulate smaller second moments than runs at lr=1e-3"), or (b) actually log v at the end of one run per lr and quote a one-number summary. Either is small; the current wording is the one part of the revision where claim and evidence are slightly out of register. This is a minor editorial fix, not a structural concern.

2. **The 3×5 LR×epsilon grid does not state seed count or which summary statistic is reported.** Lines 92-100 show single accuracy values per cell, but the text does not say whether these are medians, means, or singletons, nor how many seeds underlie each cell. The Stage 2 main table (line 47) reports median and IQR; the Stage 3 narrow sweep (line 73) reports mean ± std and median [IQR]; the auxiliary grid follows neither convention. The reader cannot tell whether 0.952 at lr=1e-4, eps=1e-4 is one seed or thirty, and therefore cannot judge whether the lr=1e-4 row is reliable in the dimensions where it matters most (the regime-2-vs-regime-3 transition). One sentence ("Each cell is the median of N seeds") would close this. The substantive finding - that the same eps=1e-2 gives 0.485 at lr=1e-4 and 0.990 at lr=1e-2 - is not in doubt; but the reproducibility hygiene that the rest of the piece maintains is briefly absent here.

3. **No leakage detected.** I checked the revised draft for review-process vocabulary - "the prior draft," "round 1," "my advisor," "the panel said," "this revision addresses," "after peer review" - and found none. The phrase "original convergence criterion" at line 11 refers to the experimentally-intended metric within the design, not to any prior draft of this piece; the surrounding sentence reads as standard methods-section reporting of an adaptation, which is how it must read for a public artifact. This is recorded here as the negative finding the brief required, not as a concern.
