# The Stabilizer's Bias: Measuring Adam's Epsilon Across Orders of Magnitude

Adam optimizer has one parameter whose role is described as purely defensive: epsilon. In the denominator of each adaptive step, it prevents division by zero. PyTorch sets it to 1e-8; TensorFlow has historically defaulted to 1e-7. The two frameworks agree on every other Adam parameter and disagree on epsilon by a factor of ten, without either documentation acknowledging the disagreement as substantive. The standard reading is that epsilon is a numerical nicety - above some threshold, the value does not matter.

That reading is incomplete. Epsilon controls the floor on per-parameter step sizes. When epsilon is large, Adam's adaptive scaling collapses: every parameter receives nearly the same update magnitude regardless of its gradient history, and the optimizer resembles SGD with a fixed step size. When epsilon is small, the adaptive property is preserved: parameters with low accumulated gradient variance receive large updates; parameters with high variance receive small ones. Whether this structural difference produces materially different optimization outcomes in realistic settings - whether it steers the optimizer into different basins, or just changes the speed at which it reaches the same basin - is unresolved. This paper reports an empirical measurement across eight orders of magnitude.

## Experimental Design

Three stages, executed in sequence. All experiments use Python 3.14, PyTorch 2.12.0, CPU-only computation, and full-batch gradient computation (no mini-batching). Seeds are fixed with `torch.manual_seed` before both data generation and optimizer initialization. Code and lab notebooks are archived alongside this piece. The epsilon sweep covers {1e-10, 1e-9, 1e-8, 1e-7, 1e-6, 1e-5, 1e-4, 1e-3, 1e-2, 1e-1}, spanning the full range from far below any framework default to far above it.

**Stage 1** establishes a convex baseline: a 100-dimensional quadratic loss with random positive-definite curvature (eigenvalues log-uniformly distributed in [0.1, 10]), Adam at lr=1e-3, 2000 steps, 30 seeds per epsilon value. In the convex case, there is only one basin; any effect of epsilon is purely on convergence rate or final accuracy within that basin. The original convergence criterion (distance below 1e-6) proved uninformative-Adam oscillates around the minimum on quadratics rather than converging asymptotically, and no run reached threshold within 2000 steps-so final distance from the minimum after 2000 steps is the metric throughout Stage 1.

**Stage 2** introduces non-convexity: a three-layer MLP (two hidden layers of 64 units with tanh activations) trained on a two-spirals classification task - a textbook example whose loss surface has multiple local optima that differ in test accuracy. The task has 400 training and 200 test points, 3000 steps, 30 seeds per epsilon value. The measurements are final training loss, test accuracy, and weight L2 norm.

**Stage 3** narrows the epsilon sweep around the transition zone identified in Stage 2 and increases to 100 seeds per value to estimate the probability that epsilon choice changes which basin the optimizer reaches.

An auxiliary experiment runs a 3 × 5 grid of learning rates × epsilon values to test whether the epsilon effect is separable or depends on learning rate.

## Stage 1: Convex Baseline

Final distance from the global minimum after 2000 steps, median and interquartile range across 30 seeds:

| epsilon | median distance | IQR |
|---------|----------------|-----|
| 1e-10 to 1e-5 | 2.138 | [1.705, 2.438] |
| 1e-4 | 2.138 | [1.705, 2.438] |
| 1e-3 | 2.141 | [1.707, 2.440] |
| 1e-2 | 2.168 | [1.731, 2.461] |
| 1e-1 | 2.400 | [2.025, 2.672] |

*The eps=1e-4 row shows the same values at the displayed precision but differs by 0.026% in unrounded data (2.13769 vs 2.13795 for the median); see text.*

From 1e-10 to 1e-5 - six orders of magnitude - the raw results are bit-identical. At eps=1e-4, the median distance differs from the bit-identical range by 0.026% (2.13769 to 2.13795), below rounding at the decimal precision shown in the table but technically non-zero. The bit-identical claim applies strictly to eps ≤ 1e-5. A detectable but small effect appears at eps=1e-3 (+0.14% worse final distance), becoming more substantial at eps=1e-2 (+1.4%) and significant at eps=1e-1 (+12.3%).

This inertness across the small-epsilon range reflects dominance, not saturation. Gradient magnitudes in the 100D quadratic far exceed epsilon throughout the 1e-10 to 1e-5 range, so the adaptive correction term is negligibly modified by epsilon's value. This is mechanistically distinct from a ceiling effect (all runs hitting the same saturated value by some other route): the adaptive denominator remains controlled by the gradient second moment, not by epsilon.

At eps=1e-1, the +12.3% elevation in final distance reflects the enlarged oscillation amplitude in the steady state rather than convergence to a qualitatively different basin. In the convex case there is only one basin; the final distance is a snapshot of an oscillatory trajectory whose amplitude scales with the effective step size. Large epsilon inflates that step size (lr·m_i/(ε + √v_i) → lr·m_i/ε), directly enlarging the oscillation. The convex Stage 1 result is a magnitude effect, not a basin-selection effect.

No run reached a distance below 1e-6 within 2000 steps - a known property of Adam on quadratics. The first-moment estimate oscillates around zero near the minimum while the second moment retains a memory of large historical gradients, producing an oscillatory approach rather than smooth asymptotic convergence.

Two observations about the convex case. First, the effect of epsilon on the convex problem is purely quantitative - it changes the distance from the minimum but not which minimum is reached. Second, the effect is small within the range of any published framework default: eps=1e-8 (PyTorch) and eps=1e-7 (TensorFlow) both produce identical outcomes in Stage 1. The ten-to-one disagreement between the frameworks is empirically inert in the convex setting.

## Stage 2: Non-Convex Two-Spirals MLP

Stage 2 reveals two distinct phenomena that occur at different epsilon thresholds.

**Weight norm compression begins early.** The weight L2 norm decreases monotonically from eps=1e-10 through the full sweep:

| epsilon | train loss | test accuracy | weight norm |
|---------|-----------|---------------|-------------|
| 1e-10 | 0.0090 [0.0044, 0.0131] | 0.990 [0.990, 0.995] | 25.62 [24.85, 26.47] |
| 1e-9  | 0.0090 [0.0044, 0.0129] | 0.990 [0.990, 0.995] | 25.60 [24.85, 26.54] |
| 1e-8  | 0.0090 [0.0043, 0.0131] | 0.990 [0.990, 0.995] | 25.64 [24.79, 26.45] |
| 1e-7  | 0.0090 [0.0055, 0.0129] | 0.990 [0.990, 0.995] | 25.54 [24.71, 26.57] |
| 1e-6  | 0.0090 [0.0057, 0.0129] | 0.990 [0.990, 0.995] | 25.44 [24.64, 26.28] |
| 1e-5  | 0.0092 [0.0059, 0.0136] | 0.990 [0.990, 0.995] | 24.75 [23.68, 25.72] |
| 1e-4  | 0.0097 [0.0064, 0.0161] | 0.990 [0.990, 0.995] | 21.65 [21.18, 22.11] |
| 1e-3  | 0.0136 [0.0092, 0.0195] | 0.990 [0.990, 0.995] | 18.03 [17.87, 18.16] |
| 1e-2  | 0.1175 [0.1094, 0.1277] | 0.975 [0.965, 0.980] | 12.99 [12.86, 13.10] |
| 1e-1  | 0.6263 [0.6242, 0.6290] | 0.485 [0.468, 0.509] | 8.58 [8.55, 8.66] |

Weight norm compression sets in at eps≈1e-5 and is continuous: by eps=1e-3, the median weight norm has fallen 30% (25.6 → 18.0) while test accuracy remains exactly 0.990 across all 30 seeds. By eps=1e-1, weight norm has fallen 66% (25.6 → 8.6). This is a structural change in the parameter-space location of the solution: large epsilon biases the optimizer toward smaller-norm solutions by equalizing per-parameter step sizes. Whether this constitutes regularization in the generalization sense-improved test accuracy via norm control-is not established here. Test accuracy is identical across the entire norm-compression range (eps=1e-5 through eps=1e-3), meaning compressed-norm and uncompressed-norm solutions are functionally equivalent on this task. What the experiment establishes is that epsilon selects among solutions of different norms; whether the smaller-norm solutions generalize better requires a setting where the higher-epsilon model can overfit and where norm controls generalization.

**Test accuracy has a threshold at a different location.** From eps=1e-10 to eps=1e-3, test accuracy is uniformly 0.990 with no detectable degradation. Between eps=1e-3 and eps=1e-2, accuracy drops to 0.975 - still respectable, but now the IQR (0.965 to 0.980) no longer overlaps with the IQR at eps=1e-3 (0.990 to 0.995). At eps=1e-1, the model achieves 0.485 accuracy - indistinguishable from random on binary classification.

**The two thresholds do not coincide.** Weight norm compression starts two to three orders of magnitude below the accuracy degradation threshold. Within the region eps=1e-5 to eps=1e-3, epsilon is changing what parameter-space solution the optimizer converges to (smaller norm) without changing how well that solution generalizes. This decoupling is consistent with high-accuracy solutions existing at many different weight norms on this task: epsilon shifts the optimizer along a manifold of equivalent-quality solutions rather than displacing it from good solutions entirely. An alternative account-that norm compression and accuracy degradation are two ends of a single continuum-would predict monotone accuracy degradation beginning at eps≈1e-5, which the data do not show; accuracy remains flat at exactly 0.990 across eight consecutive epsilon values before the sharp transition.

The IQR non-overlap check detected basin-level separation between eps=1e-3 and eps=1e-2, triggering Stage 3.

## Stage 3: Transition Zone at 100 Seeds

To locate the accuracy transition more precisely, a narrowed sweep covers {1e-3, 2e-3, 3e-3, 5e-3, 7e-3, 1e-2, 2e-2, 5e-2, 1e-1} at 100 seeds each:

| epsilon | test acc (mean ± std) | test acc median [IQR] | p(acc ≥ 0.96) |
|---------|----------------------|----------------------|----------------|
| 1e-3 | 0.993 ± 0.005 | 0.990 [0.990, 0.995] | 1.00 |
| 2e-3 | 0.990 ± 0.005 | 0.990 [0.990, 0.995] | 1.00 |
| 3e-3 | 0.990 ± 0.005 | 0.990 [0.985, 0.995] | 1.00 |
| 5e-3 | 0.985 ± 0.007 | 0.985 [0.985, 0.990] | 1.00 |
| 7e-3 | 0.980 ± 0.009 | 0.980 [0.980, 0.986] | 0.95 |
| 1e-2 | 0.975 ± 0.010 | 0.975 [0.965, 0.980] | 0.89 |
| 2e-2 | 0.940 ± 0.026 | 0.940 [0.920, 0.955] | 0.15 |
| 5e-2 | 0.562 ± 0.081 | 0.562 [0.540, 0.619] | 0.00 |
| 1e-1 | 0.480 ± 0.028 | 0.480 [0.465, 0.495] | 0.00 |

The 0.96 threshold for p(acc ≥ 0.96) is drawn from the Stage 2 data: IQR non-overlap between eps=1e-3 (lower IQR boundary 0.990) and eps=1e-2 (lower IQR boundary 0.965) first appears at that boundary, placing the population separation between these two values. A threshold of 0.96 cleanly separates the two Stage 2 populations.

The transition is sharp. p(acc ≥ 0.96) - the probability that a given run lands in the high-accuracy basin - is 1.00 for all seeds up through eps=5e-3. At eps=7e-3, it falls to 0.95; at eps=1e-2, to 0.89; at eps=2e-2, to 0.15. The 50% basin-transition point falls at approximately eps≈1.4e-2 (interpolated in log-epsilon space). Above eps=5e-2, no seed reaches the high-accuracy basin.

The standard deviation of accuracy across seeds rises monotonically through the transition: 0.005 at eps=1e-3, 0.010 at eps=1e-2, and 0.081 at eps=5e-2. This is the signature of a stochastic basin selection process: in the transition zone, some seeds land in the high basin and some do not, with the proportion controlled by epsilon.

## The Learning Rate Interaction

The epsilon effect is not separable from learning rate. A 3 × 5 auxiliary grid (each cell the median test accuracy across 10 seeds) reveals:

| lr \ eps | 1e-10 | 1e-8 | 1e-6 | 1e-4 | 1e-2 |
|----------|--------|------|------|------|------|
| 1e-4 | 0.973 | 0.973 | 0.970 | 0.952 | 0.485 |
| 1e-3 | 0.990 | 0.990 | 0.990 | 0.990 | 0.975 |
| 1e-2 | 0.990 | 0.990 | 0.990 | 0.988 | 0.990 |

The critical observation: eps=1e-2 produces 0.485 accuracy (complete failure) at lr=1e-4, but 0.990 accuracy (full success) at lr=1e-2. The same epsilon value produces opposite outcomes depending on learning rate. This collapses the single-axis framing: the question "is epsilon harmful at 1e-2?" has no answer without specifying the learning rate.

The interaction has a mechanistic interpretation. Adam's adaptive step size for parameter i at step t is approximately lr · m_i^t / (√v_i^t + ε). When epsilon is large relative to √v_i^t, the step size approaches lr · m_i^t / ε - a step that scales inversely with epsilon and no longer depends on gradient history. The harmful threshold is therefore a ratio: epsilon relative to √v.

The second moment v_i^t accumulates squared gradients evaluated at the parameter locations visited during training. At a smaller learning rate, the optimizer traces a different path through parameter space-moving in smaller increments, visiting different regions, and accumulating gradient statistics that reflect the landscape at those locations. For the threshold shift in the 3×5 grid to arise from the ε/√v dominance mechanism, runs at lr=1e-4 would need to accumulate second moments of smaller magnitude than runs at lr=1e-3-the grid data are consistent with this, but second-moment statistics were not directly logged in this experiment. Whether the same pattern holds on other tasks depends on how the gradient landscape responds to different trajectory speeds; the relationship between learning rate and second-moment magnitude is not universal. This mechanistic account is a plausible reading of the observed threshold shift, consistent with the data but not uniquely derived from it. The robust statement is: the harmful epsilon threshold is set by the gradient second-moment regime, which learning rate influences through its effect on the training path. Specifying "epsilon=X is safe" without conditioning on learning rate and gradient statistics is underspecified.

## The PyTorch vs TensorFlow Default

The empirical evidence settles the practical question. At lr=1e-3 (the standard default across both frameworks), the PyTorch default (eps=1e-8) and the TensorFlow default (eps=1e-7) both sit eight to nine orders of magnitude below the accuracy-degradation threshold and five to six orders of magnitude below the weight-norm-compression threshold. The one-order-of-magnitude disagreement between the frameworks is experimentally inert at any reasonable learning rate.

However, the measurement also identifies when epsilon becomes substantive. Two situations place practitioners within the structural-bias regime:

1. **Manual epsilon inflation.** Epsilon varies across published transformer training configurations. Devlin et al. (2019) report eps=1e-6 for BERT; the GPT-2 training code uses PyTorch's default 1e-8 (Radford et al., 2019). Mixed-precision (fp16) training can motivate higher epsilon values to prevent second-moment underflow under reduced floating-point precision; some practitioners use eps=1e-4 or higher in this setting, though no single published standard exists. At lr=1e-3, eps=1e-3 already shows a 30% weight norm reduction and eps=1e-2 degrades accuracy to 0.975. At lr=1e-4 (common for fine-tuning), eps=1e-4 already reduces accuracy to 0.952.

2. **Small learning rates with default epsilon.** If the learning rate is reduced two or more orders of magnitude below the value at which the architecture was benchmarked, the gradient second-moment regime shifts, and the nominal "default" epsilon may enter the bias regime even without any explicit change.

## Reinterpreting Epsilon

The official description of epsilon as a numerical stabilizer is accurate but incomplete. It also functions as a parameter-norm compressor and, above a threshold that depends on the learning rate and gradient regime, a basin selector.

Systematic empirical characterization of epsilon at this granularity does not appear prominently in the Adam literature. Kingma and Ba describe epsilon as a numerical device; Reddi, Kale, and Kumar hold it fixed in their convergence analysis. The three-regime structure reported here-with norm compression and basin failure as distinct phenomena separated by two to three orders of magnitude-is the piece's primary empirical contribution.

The norm-compression effect (weight norm reduction) begins approximately two to three orders of magnitude below the basin-selection threshold at any tested learning rate. A practitioner using eps=1e-4 with lr=1e-3 will find their model converging to a 15-20% smaller-norm solution than a practitioner using eps=1e-8. Whether this norm difference is consequential depends on downstream use. Within the present experiment, compressed-norm and uncompressed-norm solutions are functionally equivalent on two-spirals: test accuracy is identical across the entire norm-compression range. Whether epsilon's bias toward smaller-norm solutions produces generalization improvements is a downstream empirical question; it would require a setting where the higher-epsilon model can overfit and where weight norm predicts generalization performance. The relevant candidate contexts-spectral norm bounds, flatness measures, transfer learning-have different and sometimes conflicting dependencies on weight norm, and none are tested here.

The basin-selection effect (accuracy degradation) only emerges above eps≈1e-2 at lr=1e-3. Below that threshold, epsilon changes *where in parameter space* the optimizer lands without changing *which class of solutions* it reaches. Above it, the optimizer is functionally impaired: the adaptive property that makes Adam useful is sufficiently suppressed that the optimizer cannot reliably reach good solutions.

These results are from full-batch training. In practical mini-batch Adam, per-step gradients carry noise whose variance is absorbed into the second-moment estimate, increasing v above the full-batch level and thereby raising the epsilon dominance threshold. Whether the three-regime structure persists under mini-batching-and whether the numerical thresholds shift proportionally-is not measured here and represents a natural follow-on question.

The three-regime structure is consistent with Reddi, Kale, and Kumar's theoretical analysis. Their central result constructs adversarial gradient sequences for which Adam's exponential moving average systematically underestimates variance, proving non-convergence in specific online learning settings. Large epsilon produces a structurally analogous effect-the adaptive denominator loses sensitivity to per-parameter gradient variance history-making the empirical finding compatible with their analysis. Whether the Reddi et al. adversarial mechanism is operative on the two-spirals problem is open; the formal construction concerns specific online learning sequences, and the present results do not test it.

## Conclusion

Adam's epsilon functions as three things simultaneously, each with a different onset:

1. **A numerical stabilizer** (always): prevents division by zero. Inert for practical gradient magnitudes when epsilon is small relative to √v.
2. **A parameter-norm compressor** (eps ≳ 1e-5 at lr=1e-3): biases the optimizer toward smaller-norm solutions by equalizing per-parameter step sizes. Whether this bias constitutes useful regularization-improved generalization through norm control-is a downstream question the present evidence does not answer.
3. **A basin selector** (eps ≳ 1e-2 at lr=1e-3): suppresses the adaptive property sufficiently to steer the optimizer into qualitatively different solutions or produce training failure.

These numerical thresholds are specific to the two-spirals MLP at lr=1e-3. The mechanism-epsilon dominating the adaptive denominator when ε becomes comparable to √v-plausibly generalizes; the threshold values depend on the gradient statistics of the specific architecture, dataset, and learning rate. The robust finding is the ordering: norm compression precedes basin failure by two to three orders of magnitude, and both phenomena depend on the ratio of epsilon to the gradient second moment rather than on epsilon's absolute value. These thresholds are measured under full-batch conditions; mini-batch noise would raise the epsilon dominance threshold, as discussed above.

The PyTorch vs TensorFlow default disagreement (1e-8 vs 1e-7) lands firmly in regime 1. Standard epsilon adjustments for transformer training (1e-6 to 1e-8) likewise land in regime 1. Manual inflation to 1e-4 enters regime 2. Inflation to 1e-2 at standard learning rates enters regime 3.

Practitioners who increase epsilon for numerical stability are entering regime 2 or 3 depending on how far they go. The optimizer then has the properties of a weaker version of itself - one that converges to smaller-norm solutions without its adaptive gradient-history discrimination. Whether that trade is beneficial depends on the problem; the present evidence does not recommend it.

## References

- Kingma, D. P., & Ba, J. (2015). "Adam: A Method for Stochastic Optimization." ICLR 2015. https://arxiv.org/abs/1412.6980
- Reddi, S. J., Kale, S., & Kumar, S. (2018). "On the Convergence of Adam and Beyond." ICLR 2018. Their central result constructs adversarial gradient sequences for which Adam's EMA systematically underestimates variance, proving non-convergence in specific online learning settings.
- Devlin, J., Chang, M.-W., Lee, K., & Toutanova, K. (2019). "BERT: Pre-training of Deep Bidirectional Transformers for Language Understanding." NAACL-HLT 2019. (Reports Adam with eps=1e-6.)
- Radford, A., Wu, J., Child, R., Luan, D., Amodei, D., & Sutskever, I. (2019). "Language Models are Unsupervised Multitask Learners." OpenAI Blog. (GPT-2 training uses Adam with PyTorch default eps=1e-8.)
- Lang, K. J., & Witbrock, M. J. (1988). "Learning to tell two spirals apart." Proceedings of the 1988 Connectionist Models Summer School.
- [*What Leave-One-Out Cannot See: A Synthetic-Data Audit of a Standard Robustness Check*](posts/2026-05-23-what-leave-one-out-cannot-see-a-syntheti-d9c3/) - methodological precedent for structural blind-spots in standard procedures.
- [*When the Stadion Sets the Result: Putting Error Bars on Eratosthenes*](posts/2026-05-18-when-the-instrument-sets-the-result-reco-e172/) - the instrument-construction problem: how a single design choice can dominate a measurement's outcome.
- [*When the Procedure Sets the Error: Reconstructing Aristarchus's Measurement*](posts/2026-05-19-when-the-procedure-sets-the-error-recons-7b2b/) - condition number as a diagnostic for whether instrument precision can rescue a flawed procedure.
