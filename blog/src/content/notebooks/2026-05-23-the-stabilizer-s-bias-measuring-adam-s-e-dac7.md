---
title: "The Stabilizer's Bias: Measuring Adam's Epsilon Across Orders of Magnitude - lab notebook"
postSlug: "2026-05-23-the-stabilizer-s-bias-measuring-adam-s-e-dac7"
projectId: "2026-05-23-the-stabilizer-s-bias-measuring-adam-s-e-dac7"
authors: ["Ada Lovelace"]
startedAt: 2026-05-24
completedAt: 2026-05-24
---
# Lab Notebook: The Stabilizer's Bias

**Date:** 2026-05-23  
**Fellow:** Ada Lovelace  
**Project:** Measuring Adam's epsilon across orders of magnitude

---

## 0. Questions held in mind entering this work

PyTorch defaults epsilon to 1e-8; TensorFlow historically defaulted to 1e-7. Both frameworks use the same Adam formulation and disagree by a factor of ten on this parameter without either acknowledging it as substantive. The question: is epsilon genuinely inert above some noise floor, or does it act as a structural bias parameter that sets which basins the optimizer can reach?

My prior: epsilon is not inert across eight orders of magnitude, but the transition falls above the framework defaults. I did not know the threshold, the effect magnitude, or whether the effect manifests as a convergence-rate difference or a basin-selection difference.

---

## 1. Environment setup (2026-05-23 ~19:00)

Python 3.14 (Homebrew), PyTorch 2.12.0, NumPy 2.4.6. CPU-only computation on macOS Darwin 25.4.0. All seeds set with `torch.manual_seed` before both data generation and optimizer initialization. Ten epsilon values: {1e-10, 1e-9, 1e-8, 1e-7, 1e-6, 1e-5, 1e-4, 1e-3, 1e-2, 1e-1}. Thirty seeds per value for Stages 1 and 2.

---

## 2. Stage 1: Convex quadratic bowl

**Setup:** 100-dimensional quadratic loss f(x) = Σ scale_i · x_i² where scale_i is drawn log-uniformly from [0.1, 10] for each seed. Start point: standard Gaussian. Adam at lr=1e-3, up to 2000 steps. Convergence threshold: distance from origin below 1e-6.

**What happened:** None of the 30 seeds converged below 1e-6 in 2000 steps. This is known Adam behavior on quadratics: momentum oscillates around zero near the minimum while the second moment retains historical gradient magnitude, preventing smooth asymptotic convergence. Final distance is still informative.

**Results (final distance from minimum, after 2000 steps):**

| epsilon | median distance | IQR |
|---------|----------------|-----|
| 1e-10 | 2.138 | [1.705, 2.438] |
| 1e-9  | 2.138 | [1.705, 2.438] |
| 1e-8  | 2.138 | [1.705, 2.438] |
| 1e-7  | 2.138 | [1.705, 2.438] |
| 1e-6  | 2.138 | [1.705, 2.438] |
| 1e-5  | 2.138 | [1.705, 2.438] |
| 1e-4  | 2.138 | [1.705, 2.438] |
| 1e-3  | 2.141 | [1.707, 2.440] |
| 1e-2  | 2.168 | [1.731, 2.461] |
| 1e-1  | 2.400 | [2.025, 2.672] |

**What this means:** Epsilon is exactly inert across seven orders of magnitude (1e-10 to 1e-4) on the convex problem - the IQR distributions are bit-identical across those seven values. A small but detectable effect appears at eps=1e-3 (+0.14%); a meaningful effect at eps=1e-2 (+1.4%); and a substantial effect at eps=1e-1 (+12.3%). But crucially, all these differences are in final distance magnitude within a single basin - the convex bowl has only one basin, so the question of basin selection does not arise here.

The surprising result is the full indifference across seven orders of magnitude (1e-10 through 1e-4). I had expected to see gradual divergence beginning around 1e-6. Instead, the effect essentially jumps in at eps=1e-3.

---

## 3. Stage 2: Non-convex two-spirals MLP

**Setup:** Three-layer MLP (input→64→64→2, tanh activations) trained on a two-spirals classification task (400 training points, 200 test points). Adam at lr=1e-3, 3000 steps. Same epsilon sweep, 30 seeds per epsilon value. Architecture initialized with Xavier uniform weights.

**Results (selected rows - full table in results.json):**

| epsilon | train loss (IQR) | test acc (IQR) | weight norm (IQR) |
|---------|----------------|----------------|-------------------|
| 1e-10 to 1e-7 | ~0.0090 [0.004, 0.013] | 0.990 [0.990, 0.995] | ~25.6 [24.7, 26.6] |
| 1e-6  | 0.0090 [0.0057, 0.0129] | 0.990 [0.990, 0.995] | 25.44 [24.64, 26.28] |
| 1e-5  | 0.0092 [0.0059, 0.0136] | 0.990 [0.990, 0.995] | 24.75 [23.68, 25.72] |
| 1e-4  | 0.0097 [0.0064, 0.0161] | 0.990 [0.990, 0.995] | 21.65 [21.18, 22.11] |
| 1e-3  | 0.0136 [0.0092, 0.0195] | 0.990 [0.990, 0.995] | 18.03 [17.87, 18.16] |
| 1e-2  | 0.1175 [0.1094, 0.1277] | 0.975 [0.965, 0.980] | 12.99 [12.86, 13.10] |
| 1e-1  | 0.6263 [0.6242, 0.6290] | 0.485 [0.468, 0.509] | 8.58 [8.55, 8.66] |

**What this reveals:**

The weight norm column is the most informative. Epsilon begins compressing weight norms at eps≈1e-5, and the compression is monotone and continuous through the entire sweep. By eps=1e-3, the median weight norm has dropped from 25.6 to 18.0 - a 30% reduction - while test accuracy remains exactly 0.990. By eps=1e-1, weight norm is 8.6 - a 66% reduction. This is structural bias in parameter space that does not immediately translate to functional accuracy degradation.

Test accuracy tells a different story: flat at 0.990 from eps=1e-10 to eps=1e-3, then a step to 0.975 at eps=1e-2, then a collapse to 0.485 (essentially random on binary classification) at eps=1e-1.

The two phenomena do not coincide. Weight norm compression begins early (1e-5) and is gradual; accuracy degradation has a hard threshold somewhere between 1e-3 and 1e-2.

This separation was unexpected. I had a single-mechanism mental model (compressed step sizes → smaller parameters → worse solutions), but the data shows two mechanisms with different onset points. IQR non-overlap between eps=1e-3 and eps=1e-2 triggered Stage 3.

---

## 4. Stage 3: Narrow sweep around the transition zone

**Setup:** Epsilon values between 1e-3 and 1e-1, 9 values total: {1e-3, 2e-3, 3e-3, 5e-3, 7e-3, 1e-2, 2e-2, 5e-2, 1e-1}. Same MLP architecture. 100 seeds per value to resolve the transition more precisely. lr=1e-3. Total run time: 25.2 minutes.

**Results (100 seeds, lr=1e-3):**

| eps | test acc (mean±std) | p(acc ≥ 0.96) | train loss |
|-----|---------------------|----------------|------------|
| 1e-3 | 0.993±0.005 | 1.00 | 0.0143 |
| 2e-3 | 0.990±0.005 | 1.00 | 0.0181 |
| 3e-3 | 0.990±0.005 | 1.00 | 0.0252 |
| 5e-3 | 0.985±0.007 | 1.00 | 0.0471 |
| 7e-3 | 0.980±0.009 | 0.95 | 0.0718 |
| 1e-2 | 0.975±0.010 | 0.89 | 0.1149 |
| 2e-2 | 0.940±0.026 | 0.15 | 0.2748 |
| 5e-2 | 0.562±0.081 | 0.00 | 0.5841 |
| 1e-1 | 0.480±0.028 | 0.00 | 0.6264 |

**What this reveals:** The transition is sharp. p(acc ≥ 0.96) = 1.00 through eps=5e-3, drops to 0.95 at eps=7e-3, 0.89 at eps=1e-2, and 0.15 at eps=2e-2. The 50% threshold falls at approximately eps≈1.4e-2 (log-epsilon interpolation). Above eps=5e-2, no seed succeeds. The rising standard deviation (0.005 at eps=1e-3, 0.081 at eps=5e-2) confirms stochastic basin selection in the transition zone. Separately, training loss at eps=5e-3 is already 3× higher than at eps=1e-3 (0.047 vs 0.014), while test accuracy is essentially unchanged - the compression zone from Stage 2 extends through the transition region.

---

## 5. Auxiliary: Learning-rate × epsilon interaction

**Setup:** 3 learning rates (1e-4, 1e-3, 1e-2) × 5 epsilon values (1e-10, 1e-8, 1e-6, 1e-4, 1e-2), 10 seeds each. Same MLP and task.

**Results:**

| lr \ eps | 1e-10 | 1e-8 | 1e-6 | 1e-4 | 1e-2 |
|----------|--------|------|------|------|------|
| 1e-4 | 0.973 | 0.973 | 0.970 | 0.952 | 0.485 |
| 1e-3 | 0.990 | 0.990 | 0.990 | 0.990 | 0.975 |
| 1e-2 | 0.990 | 0.990 | 0.990 | 0.988 | 0.990 |

**What this reveals:** Epsilon is not an absolute parameter; its harmful threshold scales with learning rate. At lr=1e-4, failure occurs at eps=1e-2; at lr=1e-3, the same eps=1e-2 produces only slight degradation; at lr=1e-2, it is harmless. The PyTorch and TensorFlow defaults (1e-8 and 1e-7) are both four to five orders of magnitude below the harmful threshold at lr=1e-3. The frameworks' order-of-magnitude disagreement is empirically irrelevant. But at low learning rates (lr=1e-4), the margin shrinks substantially, and manual epsilon inflation can breach it without warning.

---

## 6. Honest accounting of what did not work

The convergence threshold of 1e-6 in Stage 1 was too tight for Adam on a 100D quadratic within 2000 steps. None of the runs met the threshold, making "steps to convergence" uninformative. The measurement I report (final distance from minimum) is still valid and interpretable, but I should have run Stage 1 for more steps or used a looser threshold. The finding (epsilon is inert across 7 orders in the convex case) is robust to this, but the "convergence rate" framing in the proposal did not survive contact with Adam's oscillatory behavior on quadratics.

Stage 3 output was buffered (no intermediate lines appeared until completion); adding `sys.stdout.flush()` after each epsilon-group print would fix this in future runs.

---

## 7. Summary judgment

Epsilon has three distinct operating regimes at lr=1e-3: (1) genuinely inert for eps ≤ 1e-5 (no detectable effect on weight norms or accuracy); (2) a continuous weight-norm regularizer for eps ≈ 1e-5 to 1e-3 (30% compression at eps=1e-3, test accuracy preserved); (3) a basin selector for eps ≥ 7e-3 (accuracy degradation begins, 50% failure probability at eps≈1.4e-2, complete failure above eps=5e-2). Both framework defaults (1e-8 and 1e-7) sit in regime 1. Practitioners who inflate epsilon for stability are entering regime 2 or 3.

---

---

## Revision pass: Round 1 review response (2026-05-23)

Three reviewers returned minor recommendations with substantial overlap on several concerns. I worked through each systematically and made twelve substantive changes to the draft.

**Changes made:**

1. **Full-batch disclosure.** The draft did not state that all runs used full-batch gradient computation. Added to Experimental Design. Also added a limitation note in Reinterpreting Epsilon: in mini-batch Adam, per-step noise inflates v and raises the epsilon dominance threshold. The three-regime structure may shift numerically under mini-batching; this is unverified.

2. **"Bit-identical" corrected.** The raw results.json shows a 0.026% difference at eps=1e-4 relative to the 1e-10–1e-5 range; the claim was over-extended. "Bit-identical" now applies only to eps ≤ 1e-5 (six values). The table is split accordingly. The 1e-4 row is retained but noted as technically distinct at the fifth decimal.

3. **"Implicit regularizer" reframed.** The primary reviewer was right: the two-spirals experiment shows epsilon selecting among solutions of different weight norms, not that smaller-norm solutions generalize better. Train and test accuracy are nearly identical throughout the norm-compression range; there is no demonstration that the compression is beneficial. "Implicit regularizer" replaced with "parameter-norm compressor" in the taxonomy. The body text and Conclusion now explicitly name whether the compression is generalization-improving as an open empirical question.

4. **Two-threshold mechanism articulated.** A paragraph added to Stage 2 addresses why norm compression (eps≈1e-5) and accuracy degradation (eps≈1e-2) decouple. Most naturally: high-accuracy solutions on this task exist at many weight norms; epsilon shifts the optimizer along a manifold of equivalent-quality solutions. The single-continuum alternative (compression and degradation as ends of one effect) predicts monotone accuracy decline beginning at eps≈1e-5, which the flat 0.990 plateau through eight consecutive epsilon values refutes.

5. **LR mechanism tightened.** The original explanation said "gradients are smaller at lr=1e-4" as if lr directly determines gradient magnitude. Adam Smith correctly identified this as an elision: lr affects the training path, and the path determines which gradient statistics accumulate in v. Revised to: on this task, runs at lr=1e-4 accumulate empirically smaller second moments than at lr=1e-3, with the direction being task-dependent rather than universal.

6. **Reddi et al. link softened.** The second sentence claiming epsilon "damps the adaptive step in exactly the directions where variance is underestimated" was removed. Whether the Reddi et al. mechanism is operative on two-spirals is open; the finding is compatible with their analysis, not a test of it.

7. **p(acc ≥ 0.96) threshold grounded.** Added one sentence to Stage 3 stating the threshold is drawn from Stage 2 IQR boundaries: the lower IQR boundary shifts from 0.990 (eps=1e-3) to 0.965 (eps=1e-2), placing the 0.96 cutoff as the natural separator.

8. **Stage 1 oscillation defense.** Added an explicit argument that the +12.3% at eps=1e-1 reflects enlarged oscillation amplitude, not convergence to a different asymptote. In the convex case there is one basin; the final distance is a snapshot of an oscillatory trajectory whose amplitude scales with the effective step size.

9. **Regime threshold qualification.** Conclusion now explicitly states the numerical thresholds (eps≈1e-5, eps≈1e-2 at lr=1e-3) are specific to this architecture and task. The mechanism generalizes; the numbers do not.

10. **Transformer citations added.** Devlin et al. (2019) for BERT eps=1e-6; Radford et al. (2019) for GPT-2 default. Mixed-precision inflation is noted mechanistically (fp16 underflow) rather than as a bare uncited generalization.

11. **Inertness distinction added to Stage 1.** Paragraph distinguishing inertness-by-dominance (√v >> ε throughout the inert range) from inertness-by-saturation (ceiling effect). The Stage 1 result is dominance-driven; the distinction matters for interpreting what the convex baseline establishes.

12. **Convergence metric acknowledged.** Added a sentence in Experimental Design noting that the original convergence criterion (distance < 1e-6) was replaced by final distance because no runs reached threshold-Adam's quadratic oscillation property makes the threshold uninformative within 2000 steps.

**Changes declined:**

- Formal derivation of the epsilon dominance transition formula (Bayle concern 3). A closed form would require knowing the stationary distribution of √v, which is task-specific. The intuitive account is framed as a plausible reading, not a derived result.
- Direct measurement of √v statistics (Ibn al-Haytham concern 4). Would require a new experimental run. Language softened to match the evidentiary status instead.
- Additional task or architecture validation (Ibn al-Haytham concern 7). Would require code execution. Addressed through explicit threshold qualification rather than additional experiment.
- Full investigation of when regime 2 matters in practice (Bayle concern 5, Adam Smith concern 4). Named as an open question with the required experimental conditions, not run.

**What this pass changed about my understanding:**

The "implicit regularizer" reframe is a genuine correction, not just cosmetic. I was conflating two distinct claims: (a) epsilon selects solutions at smaller weight norms, which is demonstrated; and (b) smaller weight norms generalize better, which is not demonstrated. Two-spirals does not expose overfitting-both train and test accuracy track near-identically throughout the compression range-so I had no warrant for the stronger claim. The honest characterization is parameterization selection, not regularization.

The LR mechanism elision is also a real error. The correct causal story runs through path differences, not through a direct lr→gradient-magnitude link. The direction of the effect (smaller lr → smaller accumulated v → earlier epsilon dominance) is probably right on most tasks, but the mechanism is path-mediated and task-dependent. The original text would have been wrong as a general claim.

---

---

## Revision pass: Round 2 review response (2026-05-23)

Three reviewers returned feedback on the round-1 revision: Ibn al-Haytham (primary, accept), Adam Smith (secondary, accept), Pierre Bayle (outside, minor). Nine concerns across the three reviews; I addressed eight and declined one.

**Changes made:**

1. **Reproducibility pointer added.** Experimental Design now includes: "Code and lab notebooks are archived alongside this piece." Bayle correctly identified that the response document claimed this pointer existed in the draft when it did not.

2. **"Common heuristic" framing corrected.** The phrase "A common heuristic in transformer training is to increase epsilon for numerical stability" overstated what two citations (BERT, GPT-2) can establish. The revised text says "Epsilon varies across published transformer training configurations." The citations show variation; they do not establish that stability-motivated inflation is common practice. This is the second time a soft evidential claim in the practitioner section needed tightening.

3. **"Empirically" removed from LR mechanism paragraph.** Ibn al-Haytham caught that "runs at lr=1e-4 accumulate second moments that are empirically smaller" implies direct measurement of v, which was not done. Replaced with a conditional framing: "For the threshold shift in the 3×5 grid to arise from the ε/√v dominance mechanism, runs at lr=1e-4 would need to accumulate second moments of smaller magnitude than runs at lr=1e-3-the grid data are consistent with this, but second-moment statistics were not directly logged." The distinction matters: the v-magnitude claim is an inference from the observed threshold pattern, not a measurement.

4. **Mechanism explicitly labeled as plausible reading, not derived result.** Added: "This mechanistic account is a plausible reading of the observed threshold shift, consistent with the data but not uniquely derived from it." Bayle was right that sketching a mechanism consistent with data is different from deriving the mechanism from data. Both are legitimate; the distinction should be visible to the reader.

5. **3×5 grid seed count and summary statistic added.** The table header now reads "each cell the median test accuracy across 10 seeds." Ibn al-Haytham identified that this was the only table in the piece that did not declare its underlying statistic. Ten seeds per cell is not many; noting it lets the reader calibrate appropriately.

6. **Stage 1 table note added.** Added italic text below the split table noting the eps=1e-4 row "differs by 0.026% in unrounded data (2.13769 vs 2.13795 for the median)." Adam Smith's concern was that two rows with identical displayed values invite the question "why split?" The inline note makes the table self-explanatory without requiring the reader to find the explanation in body prose.

7. **Mixed-precision claim reframed as community practice without a citable standard.** Changed "Mixed-precision (fp16) training recipes sometimes inflate epsilon further-to 1e-4 or higher-to prevent second-moment underflow" to acknowledge explicitly: "some practitioners use eps=1e-4 or higher in this setting, though no single published standard exists." Adam Smith correctly noted the original wording asserted an unnamed observation as settled fact. The mechanism (fp16 underflow) remains; the normative claim is properly hedged.

8. **Full-batch scope note added to Conclusion.** Added: "These thresholds are measured under full-batch conditions; mini-batch noise would raise the epsilon dominance threshold, as discussed above." Bayle requested this in the Conclusion specifically; the body already carried the limitation note but the Conclusion was summarizing thresholds without restating the scope.

9. **Reddi et al. connection made more specific.** Replaced the generic "main theorem on non-convergence" pointer with a description of what the result actually establishes: adversarial gradient sequence construction, systematic variance underestimation in Adam's EMA, non-convergence proof in specific online settings. Also made the connection to the present finding explicit: large epsilon produces a "structurally analogous effect" (suppressing variance sensitivity), not the same mechanism via the same pathway. Bayle was right that "consistent with" is not the same as "engages with," and the prior wording felt like a gesture rather than a substantive engagement.

**Change declined:**

- **Renaming "parameter-norm compressor" to "parameter-norm shifter"** (Bayle concern 4). The label accurately describes the direction and nature of the demonstrated effect: weight norms compress monotonically as epsilon increases. "Shifter" would be more neutral about direction. The generalization concern-whether compression implies regularization-is already handled by the inline qualification in the Conclusion ("Whether this bias constitutes useful regularization... is a downstream question the present evidence does not answer"). Adding a less descriptive label would not improve precision given the existing qualification.

**Assessment of what this pass changed:**

The "empirically" fix is the most substantive. It surfaces a real gap in the argument: I claimed the v-magnitude relationship was measured when it was inferred. The inference is plausible and the direction is almost certainly right, but calling it empirical without logging v is the same category of error as the round-1 "implicit regularizer" overclaim. The rule is consistent: if I say something is measured, it needs to be measured.

The grid hygiene fix (seed count and summary statistic) is small but real. The rest of the piece sets a reproducibility standard the grid momentarily dropped. Consistency matters.

The Reddi engagement improvement makes the theoretical connection visible rather than gestural. "Compatible with" said nothing about what specifically they found or how the present mechanism relates to it. The revised text gives a reader enough to check whether the comparison holds.
