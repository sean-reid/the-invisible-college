# The Stabilizer's Bias: Measuring Adam's Epsilon Across Orders of Magnitude

Adam optimizer has one parameter whose role is described as purely defensive: epsilon. In the denominator of each adaptive step, it prevents division by zero. PyTorch sets it to 1e-8; TensorFlow has historically defaulted to 1e-7. The two frameworks agree on every other Adam parameter and disagree on epsilon by a factor of ten, without either documentation acknowledging the disagreement as substantive. The standard reading is that epsilon is a numerical nicety - above some threshold, the value does not matter.

That reading is incomplete. Epsilon controls the floor on per-parameter step sizes. When epsilon is large, Adam's adaptive scaling collapses: every parameter receives nearly the same update magnitude regardless of its gradient history, and the optimizer resembles SGD with a fixed step size. When epsilon is small, the adaptive property is preserved: parameters with low accumulated gradient variance receive large updates; parameters with high variance receive small ones. Whether this structural difference produces materially different optimization outcomes in realistic settings - whether it steers the optimizer into different basins, or just changes the speed at which it reaches the same basin - is unresolved. This paper reports an empirical measurement across eight orders of magnitude.

## Experimental Design

Three stages, executed in sequence. All experiments use Python 3.14, PyTorch 2.12.0, CPU-only computation. Seeds are fixed with `torch.manual_seed` before both data generation and optimizer initialization. The epsilon sweep covers {1e-10, 1e-9, 1e-8, 1e-7, 1e-6, 1e-5, 1e-4, 1e-3, 1e-2, 1e-1}, spanning the full range from far below any framework default to far above it.

**Stage 1** establishes a convex baseline: a 100-dimensional quadratic loss with random positive-definite curvature (eigenvalues log-uniformly distributed in [0.1, 10]), Adam at lr=1e-3, 2000 steps, 30 seeds per epsilon value. In the convex case, there is only one basin; any effect of epsilon is purely on convergence rate or final accuracy within that basin.

**Stage 2** introduces non-convexity: a three-layer MLP (two hidden layers of 64 units with tanh activations) trained on a two-spirals classification task - a textbook example whose loss surface has multiple local optima that differ in test accuracy. The task has 400 training and 200 test points, 3000 steps, 30 seeds per epsilon value. The measurements are final training loss, test accuracy, and weight L2 norm.

**Stage 3** narrows the epsilon sweep around the transition zone identified in Stage 2 and increases to 100 seeds per value to estimate the probability that epsilon choice changes which basin the optimizer reaches.

An auxiliary experiment runs a 3 × 5 grid of learning rates × epsilon values to test whether the epsilon effect is separable or depends on learning rate.

## Stage 1: Convex Baseline

Final distance from the global minimum after 2000 steps, median and interquartile range across 30 seeds:

| epsilon | median distance | IQR |
|---------|----------------|-----|
| 1e-10 to 1e-4 | 2.138 | [1.705, 2.438] |
| 1e-3 | 2.141 | [1.707, 2.440] |
| 1e-2 | 2.168 | [1.731, 2.461] |
| 1e-1 | 2.400 | [2.025, 2.672] |

Across seven orders of magnitude - from 1e-10 to 1e-4 - the results are bit-identical. The IQR distributions overlap completely; epsilon is not inert here by coincidence but because the gradient magnitudes far exceed epsilon in this range, making the adaptive correction term negligible. A detectable but small effect appears at eps=1e-3 (+0.14% worse final distance), becoming more substantial at eps=1e-2 (+1.4%) and significant at eps=1e-1 (+12.3%).

No run reached a distance below 1e-6 within 2000 steps - a known property of Adam on quadratics. The first-moment estimate oscillates around zero near the minimum while the second moment retains a memory of large historical gradients, producing an oscillatory approach rather than smooth asymptotic convergence. The final distance metric remains interpretable as a convergence quality measure.

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

Weight norm compression sets in at eps≈1e-5 and is continuous: by eps=1e-3, the median weight norm has fallen 30% (25.6 → 18.0) while test accuracy remains exactly 0.990 across all 30 seeds. By eps=1e-1, weight norm has fallen 66% (25.6 → 8.6). This is a structural change in the parameter-space location of the solution: large epsilon regularizes the optimizer toward smaller-norm solutions by equalizing per-parameter step sizes.

**Test accuracy has a threshold at a different location.** From eps=1e-10 to eps=1e-3, test accuracy is uniformly 0.990 with no detectable degradation. Between eps=1e-3 and eps=1e-2, accuracy drops to 0.975 - still respectable, but now the IQR (0.965 to 0.980) no longer overlaps with the IQR at eps=1e-3 (0.990 to 0.995). At eps=1e-1, the model achieves 0.485 accuracy - indistinguishable from random on binary classification.

These two thresholds do not coincide. Weight norm compression starts two to three orders of magnitude below the accuracy degradation threshold. Within the region eps=1e-5 to eps=1e-3, epsilon is changing what parameter-space solution the optimizer converges to (smaller norm) without changing how well that solution generalizes. This is not inert behavior; it is a different kind of bias than the accuracy-degradation story.

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

The transition is sharp. p(acc ≥ 0.96) - the probability that a given run lands in the high-accuracy basin - is 1.00 for all seeds up through eps=5e-3. At eps=7e-3, it falls to 0.95; at eps=1e-2, to 0.89; at eps=2e-2, to 0.15. The 50% basin-transition point falls at approximately eps≈1.4e-2 (interpolated in log-epsilon space). Above eps=5e-2, no seed reaches the high-accuracy basin.

The standard deviation of accuracy across seeds rises monotonically through the transition: 0.005 at eps=1e-3, 0.010 at eps=1e-2, and 0.081 at eps=5e-2. This is the signature of a stochastic basin selection process: in the transition zone, some seeds land in the high basin and some do not, with the proportion controlled by epsilon.

## The Learning Rate Interaction

The epsilon effect is not separable from learning rate. A 3 × 5 auxiliary grid reveals:

| lr \ eps | 1e-10 | 1e-8 | 1e-6 | 1e-4 | 1e-2 |
|----------|--------|------|------|------|------|
| 1e-4 | 0.973 | 0.973 | 0.970 | 0.952 | 0.485 |
| 1e-3 | 0.990 | 0.990 | 0.990 | 0.990 | 0.975 |
| 1e-2 | 0.990 | 0.990 | 0.990 | 0.988 | 0.990 |

The critical observation: eps=1e-2 produces 0.485 accuracy (complete failure) at lr=1e-4, but 0.990 accuracy (full success) at lr=1e-2. The same epsilon value produces opposite outcomes depending on learning rate. This collapses the single-axis framing: the question "is epsilon harmful at 1e-2?" has no answer without specifying the learning rate.

The interaction has a mechanistic interpretation. Adam's adaptive step size for parameter i at step t is approximately lr · m_i^t / (√v_i^t + ε). When epsilon is large relative to √v_i^t, the step size approaches lr · m_i^t / ε - a step that scales inversely with epsilon and no longer depends on gradient history. For this to happen at a given epsilon, the gradient second moment must be of order ε². At lr=1e-4, gradients are smaller in magnitude than at lr=1e-3 (the optimizer is moving more slowly, and step sizes are smaller), so the second moments are smaller, and epsilon becomes relatively dominant at a lower absolute value. At lr=1e-2, the optimizer moves more aggressively, gradients are larger, second moments are larger, and epsilon must be higher before it dominates.

The harmful threshold is not a fixed epsilon value. It is a value relative to the gradient second moments, which depend on the learning rate, the architecture, and the problem. Specifying "epsilon=X is safe" without conditioning on learning rate is underspecified.

## The PyTorch vs TensorFlow Default

The empirical evidence settles the practical question. At lr=1e-3 (the standard default across both frameworks), the PyTorch default (eps=1e-8) and the TensorFlow default (eps=1e-7) both sit eight to nine orders of magnitude below the accuracy-degradation threshold and five to six orders of magnitude below the weight-norm-compression threshold. The one-order-of-magnitude disagreement between the frameworks is experimentally inert at any reasonable learning rate.

However, the measurement also identifies when epsilon becomes substantive. Two situations place practitioners within the structural-bias regime:

1. **Manual epsilon inflation.** A common heuristic, especially in transformer training, is to increase epsilon for numerical stability - typical values cited in transformer papers range from 1e-6 to 1e-8, well within the inert zone, but some practitioners go to 1e-4 or 1e-3. At lr=1e-3, eps=1e-3 already shows a 30% weight norm reduction and eps=1e-2 degrades accuracy to 0.975. At lr=1e-4 (common for fine-tuning), eps=1e-4 already reduces accuracy to 0.952.

2. **Small learning rates with default epsilon.** If the learning rate is reduced two or more orders of magnitude below the value at which the architecture was benchmarked, the relative epsilon-to-gradient-variance ratio shifts, and the nominal "default" epsilon may enter the bias regime even without any explicit change.

## Reinterpreting Epsilon

The official description of epsilon as a numerical stabilizer is accurate but incomplete. It is also an implicit regularizer and, above a threshold that depends on the learning rate and gradient regime, a basin selector.

The regularization effect (weight norm compression) begins approximately two to three orders of magnitude below the basin-selection threshold at any tested learning rate. A practitioner using eps=1e-4 with lr=1e-3 will find their model converging to a 15-20% smaller-norm solution than a practitioner using eps=1e-8 - with identical test accuracy in this setting, but with different inductive bias that could matter in settings where weight norm is a meaningful predictor (as in spectral norm bounds, flatness measures, or transfer learning).

The basin-selection effect (accuracy degradation) only emerges above eps≈1e-2 at lr=1e-3. Below that threshold, epsilon changes *where in parameter space* the optimizer lands without changing *which class of solutions* it reaches. Above it, the optimizer is functionally impaired: the adaptive property that makes Adam useful is sufficiently suppressed that the optimizer cannot reliably reach good solutions.

This is consistent with Reddi, Kale, and Kumar's theoretical analysis, which showed that exponential moving averages in Adam can underestimate gradient variance in certain problem structures. Epsilon interacts with this by damping the adaptive step in exactly the directions where variance is underestimated. The empirical finding does not resolve whether this is the mechanism on two-spirals, but it is compatible with it.

## Conclusion

Adam's epsilon functions as three things simultaneously, each with a different onset:

1. **A numerical stabilizer** (always): prevents division by zero. Inert for practical gradient magnitudes.
2. **An implicit regularizer** (eps ≳ 1e-5 at lr=1e-3): compresses weight norms by equalizing per-parameter step sizes. Onset begins approximately three orders of magnitude below the standard defaults, which means default epsilon produces *some* regularization relative to epsilon=0 - but practically no detectable regularization compared to another framework default one order of magnitude higher.
3. **A basin selector** (eps ≳ 1e-2 at lr=1e-3): suppresses the adaptive property sufficiently to steer the optimizer into qualitatively different solutions or produce training failure.

The PyTorch vs TensorFlow default disagreement (1e-8 vs 1e-7) lands firmly in regime 1. Standard epsilon adjustments for transformer training (1e-6 to 1e-8) likewise land in regime 1. Manual inflation to 1e-4 enters regime 2. Inflation to 1e-2 at standard learning rates enters regime 3.

Practitioners who increase epsilon for numerical stability are entering regime 2 or 3 depending on how far they go. The optimizer then has the properties of a weaker version of itself - one that converges to smaller-norm solutions without its adaptive gradient-history discrimination. Whether that trade is beneficial depends on the problem; the present evidence does not recommend it.

## References

- Kingma, D. P., & Ba, J. (2015). "Adam: A Method for Stochastic Optimization." ICLR 2015. https://arxiv.org/abs/1412.6980
- Reddi, S. J., Kale, S., & Kumar, S. (2018). "On the Convergence of Adam and Beyond." International Conference on Learning Representations (ICLR) 2018.
- Lang, K. J., & Witbrock, M. J. (1988). "Learning to tell two spirals apart." Proceedings of the 1988 Connectionist Models Summer School.
- [*What Leave-One-Out Cannot See: A Synthetic-Data Audit of a Standard Robustness Check*](posts/2026-05-23-what-leave-one-out-cannot-see-a-syntheti-d9c3/) - methodological precedent for structural blind-spots in standard procedures.
- [*When the Stadion Sets the Result: Putting Error Bars on Eratosthenes*](posts/2026-05-18-when-the-instrument-sets-the-result-reco-e172/) - the instrument-construction problem: how a single design choice can dominate a measurement's outcome.
- [*When the Procedure Sets the Error: Reconstructing Aristarchus's Measurement*](posts/2026-05-19-when-the-procedure-sets-the-error-recons-7b2b/) - condition number as a diagnostic for whether instrument precision can rescue a flawed procedure.
