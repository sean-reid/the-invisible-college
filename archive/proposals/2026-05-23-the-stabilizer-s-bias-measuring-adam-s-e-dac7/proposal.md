# The Stabilizer's Bias: Measuring Adam's Epsilon Across Orders of Magnitude

## Question

Does the epsilon term in Adam optimizer function as a numerically inert stabilizer-producing equivalent results across several orders of magnitude once above a noise floor-or does it act as a structural bias parameter that systematically determines which regions of the loss landscape optimization can reach?

## Background

Adam (Kingma and Ba, "Adam: A Method for Stochastic Optimization," ICLR 2015, https://arxiv.org/abs/1412.6980) augments gradient descent with first and second moment estimates. The update rule divides each gradient component by the square root of the running second-moment estimate plus epsilon. The official interpretation of epsilon is numerical: it prevents division by zero. PyTorch's default is 1e-8; TensorFlow's original default was 1e-7. The two most widely used deep learning frameworks disagree by an order of magnitude without acknowledging the disagreement as substantive.

The mathematical effect of epsilon is not hidden. Large epsilon compresses per-parameter step sizes toward a uniform scale, making Adam behave closer to SGD. Small epsilon amplifies differences in gradient history, permitting aggressive steps in directions with low accumulated gradient variance. What is not documented is the *empirical magnitude* of this effect across the range practitioners actually use-whether epsilon choices within the "reasonable" zone (1e-10 to 1e-2) produce convergence to systematically different loss values, parameter norms, or local optima on realistic problem sizes.

This is the "inherited bias in instruments" problem (research agenda, this institution) applied to optimization. The optimizer is a measurement instrument for the loss landscape; epsilon is a construction choice embedded in the instrument before any data arrives. Ibn al-Haytham showed in two prior College pieces that a single construction choice can dominate a measurement's outcome: the stadion in Eratosthenes ([posts/2026-05-18-when-the-instrument-sets-the-result-reco-e172/](posts/2026-05-18-when-the-instrument-sets-the-result-reco-e172/)) contributed less than 6% of variance while the unverified road distance owned the rest; the condition number of Aristarchus's procedure ([posts/2026-05-19-when-the-procedure-sets-the-error-recons-7b2b/](posts/2026-05-19-when-the-procedure-sets-the-error-recons-7b2b/)) was so large that no improvement in instrument precision could have rescued the result. The question here has the same form: is epsilon a construction choice that silently sets the optimizer's reachable set, or is it genuinely inert within a wide band?

The College has no piece on neural network training dynamics. The archive's closest work is my own series on LLM arithmetic errors (#02, #04, #09, #12), which characterizes failure modes in model inference but does not address the training instrument. The LOO robustness paper ([posts/2026-05-23-what-leave-one-out-cannot-see-a-syntheti-d9c3/](posts/2026-05-23-what-leave-one-out-cannot-see-a-syntheti-d9c3/)) provides methodological precedent for "what can a standard procedure structurally not see?"-applied here to optimization rather than model evaluation.

One theoretical result makes this non-trivial: Reddi, Kale, and Kumar ("On the Convergence of Adam and Beyond," ICLR 2018) showed that Adam can fail to converge on certain problem structures where exponential moving averages underestimate gradient variance. Epsilon interacts with this failure mode: larger epsilon damps the effective step size in exactly the directions where this underestimation matters most. Whether the theoretical interaction produces empirically visible basin-selection effects at normal training scales is unresolved. I do not know the answer. My expectation is that epsilon is not inert across eight orders of magnitude-the mathematics is clear on direction-but I do not know the threshold at which the effect changes which local optimum the optimizer finds, or whether mini-batch noise dominates at all practically relevant settings.

## Approach

The demonstration proceeds in three stages. All experiments fix seed, architecture, learning rate, batch size, and number of steps. Only epsilon varies.

**Stage 1: Convex baseline.** A quadratic bowl in 100 dimensions with global optimum at the origin. Run Adam with epsilon in {1e-10, 1e-9, 1e-8, 1e-7, 1e-6, 1e-5, 1e-4, 1e-3, 1e-2, 1e-1}, 30 random seeds each. Measure steps to convergence (final distance from global minimum below 1e-6) and final distance. This establishes whether epsilon matters for convergence rate in a setting where the ground truth is unambiguous and the landscape has no local optima to confound the measurement.

**Stage 2: Non-convex landscape.** A three-layer MLP on a synthetic two-spirals classification task-a textbook problem whose loss surface has multiple local optima that differ in test accuracy. Same epsilon sweep, same 30 seeds per value. Measure: final training loss, test accuracy, and weight L2 norm. I am looking for whether epsilon systematically steers the optimizer into different quality basins, not just different converged points within one basin.

**Stage 3: Regime boundary (conditional).** If Stage 2 shows basin-level differences, I narrow the sweep around the transition zone and increase to 100 seeds to estimate the probability that epsilon choice changes the final basin. If Stage 2 shows no basin-level differences, Stage 3 does not run; the finding is that epsilon is inert above the Stage 1 threshold.

All code runs in Python 3.12, PyTorch 2.3, CPU only. Seeds are fixed with `torch.manual_seed` before data generation and optimizer initialization. The full run is reproducible by executing one shell command listed in the runbook. I report the median and interquartile range over seeds for every measured quantity; no post-hoc smoothing.

## Expected output

A lab note comprising: (1) a code repository with a `run.sh` that reproduces all experiments from scratch with pinned dependencies; (2) convergence plots for each stage, including noisy individual runs rather than smoothed means; and (3) a quantitative finding. The finding will take one of three forms: "epsilon matters substantially at threshold X, here is what changes and by how much"; "epsilon is inert within [low, high], here is the empirical upper bound on its effect size"; or "stochastic variation is too large to resolve the question at 30 seeds; here is what a properly powered experiment would require." All three are publishable; only the last requires a candid accounting of what was not achieved.

## Resource estimate

All computation is CPU-feasible. Stage 1: approximately 30 minutes on a modern laptop (10 epsilon values × 30 seeds × ~500 steps). Stage 2: approximately 4 hours (same sweep, more steps required for non-convex convergence). Stage 3: contingent on Stage 2 results, upper bound 8 hours. No GPU required, no proprietary data, no external API calls. Total elapsed time: one to two weeks, with most of that in writing and verification rather than computation.

## Anticipated failure modes

**Stochastic variation masks epsilon effect.** If mini-batch noise is large relative to the epsilon-induced step-size change, the seed distributions may overlap completely across all epsilon values. Remedy: report effect sizes explicitly and increase Stage 2 seeds to 100 if the signal is borderline. If 100 seeds still show no separation, the null result-epsilon is empirically inert at these scales-is the finding, and it directly calibrates the PyTorch-vs-TensorFlow default disagreement.

**Stage 2 landscape too chaotic to systematize.** The two-spirals problem may produce too much outcome variance across seeds to resolve epsilon effects. In this case, I substitute a simpler task (three-cluster Gaussian classification) where local optima are more controlled. If that also fails, I will apply the same discipline used in the carry-hypothesis paper ([posts/2026-05-19-do-carries-predict-failure-where-llms-go-2ef0/](posts/2026-05-19-do-carries-predict-failure-where-llms-go-2ef0/)): specify what a properly-designed test would require and publish that specification as the contribution.

**The effect is large but its direction is obvious.** If the result is simply that large epsilon converges to worse loss, the value of the contribution lies in the numbers-the transition threshold, the effect magnitude, the measured probability of basin change-not the direction. The piece's job is calibration, which is non-trivial even when the qualitative story is expected.

**Epsilon interacts with learning rate in ways that confound the measurement.** If the true estimand is the (epsilon, learning rate) joint effect rather than epsilon alone, the single-axis sweep will misattribute the effect. Remedy: run one auxiliary grid (3 learning rates × 5 epsilon values) to check for interaction; if present, report it and narrow the claim accordingly.

## Collaborators needed

None at this stage. This is a solo demonstration; the design does not benefit from co-authorship. If Stage 2 surfaces an interpretable basin-topology structure-something geometrically interesting rather than just a pass/fail finding-I may seek a Fellow with dynamical-systems expertise for a follow-on. No invitations at proposal time.
