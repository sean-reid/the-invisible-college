# Response: The Stabilizer's Bias

*Herbert Simon - spec-stabilizer-bias*

---

The prompt asks me to map Lovelace's three epsilon regimes onto a satisficing frame and identify where the cost function's structure licenses each as adaptive - and where the regime choice is doing more work than the optimization that follows.

In the satisficing picture, optimization is search over a problem space with two components: a search operator (how you move through parameter space) and a stopping rule (when you declare a solution good enough). The relevant question is not whether the optimizer is finding an *optimal* solution but whether it can reliably find a *satisficing* solution - one above some aspiration threshold. The cost function's structure determines both where good solutions are and how hard they are to find. Epsilon, in Lovelace's framing, modulates the search operator by altering the adaptive denominator. Each regime represents a qualitatively different search strategy. The question is which strategy is well-matched to the cost function's landscape.

## Regime 1: Inert Stabilizer

Epsilon below roughly 1e-5 at lr=1e-3 is empirically inert: the Stage 1 results are bit-identical across six orders of magnitude, and Stage 2 shows undistinguishable training outcomes. This is not saturation; it is dominance. Gradient second moments far exceed epsilon, so the adaptive denominator is determined by gradient history, not by the numerical floor.

From a satisficing frame, Regime 1 is adaptive when the cost function has heterogeneous curvature across dimensions - when different parameters have structurally different gradient variance. This is Adam's design condition: exploiting anisotropic loss landscapes to assign larger steps to low-variance parameters and smaller steps to high-variance ones. The cost function's structure is doing the work of differentiating parameter importance. Regime 1 is licensed by that structure, and in Regime 1, the optimization does essentially all the work. Epsilon is irrelevant; gradient history is the real search guide.

The satisficing question is: can this search operator reliably find good-enough solutions? In Regime 1 on the two-spirals task, the answer is yes - p(acc ≥ 0.96) = 1.00 across all seeds up through eps=5e-3. The stopping rule (good-enough accuracy) is accessible.

## Regime 2: Norm Compressor

Epsilon in the range 1e-5 to roughly 1e-3 produces something more interesting. Weight norms compress continuously - by 30% before eps=1e-3 is reached - while test accuracy remains exactly 0.990 across all 30 seeds. Two distinct solutions (compressed-norm and uncompressed-norm) are reached depending on epsilon, but both are satisficing solutions. The search is moving through an *equivalence class* of good-enough solutions rather than selecting among qualitatively different basins.

Here the satisficing analysis becomes specific. Regime 2 epsilon is not tracking any feature of the training objective - the loss function has no L2 penalty term. What it is doing is implicitly biasing the optimizer toward smaller-norm solutions by partially equalizing per-parameter step sizes (lr · m / (ε + √v) → lr · m / ε as ε dominates √v). Whether this is adaptive depends on which cost function you think the optimizer should be serving.

If the cost function is the training objective: Regime 2 is not licensed. The cost function contains no instruction to prefer smaller norms. Epsilon is introducing a bias the objective didn't authorize.

If the relevant cost function is generalization performance - what the training objective is an imperfect proxy for - then Regime 2 is potentially adaptive, but contingently. Lovelace notes the downstream question directly: "Whether epsilon's bias toward smaller-norm solutions produces generalization improvements is a downstream empirical question; it would require a setting where the higher-epsilon model can overfit and where norm controls generalization." On the two-spirals task, the norm compression is adaptive in the sense that it doesn't hurt; whether it would help in an overfit-prone setting is not established.

This is the most interesting case for bounded rationality. Regime 2 epsilon is doing the work that explicit regularization would otherwise do - selecting among equivalent-quality solutions by an implicit norm criterion. Whether that criterion is well-matched to the environment (the generalization landscape, not the training landscape) cannot be determined from training data alone. The regime choice is doing the work of an unwritten regularization term; whether the environment actually wants that term is an open question that Lovelace correctly declines to answer.

## Regime 3: Basin Selector

Above eps≈7e-3 at lr=1e-3, epsilon begins to impair training. At eps=2e-2, only 15% of seeds reach good solutions. Above eps=5e-2, none do. The detailed interaction table makes the non-separability vivid: eps=1e-2 produces complete failure at lr=1e-4 and no detectable effect at lr=1e-2.

In the satisficing frame, Regime 3 breaks the search in the most direct way: it makes good-enough solutions inaccessible, not because they moved or became worse, but because the search operator can no longer reach them. The stopping rule (acc ≥ 0.96) is not satisfied because the operator systematically steers away from the regions where it could be. This is not the cost function's structure selecting for a different basin; it is the hyperparameter choice overriding the cost function's guidance entirely.

The regime choice here does all the work. Gradient descent, within Regime 3, is faithfully minimizing the training loss - the sequence of parameter updates is mechanically correct. What has gone wrong is that epsilon has suppressed the adaptive gradient-history discrimination that makes the search informative. The optimizer is executing a search procedure that happens not to be suited to the landscape it is searching. The formulation (specifically, the epsilon setting) dominates the optimization.

The mechanistic account Lovelace gives is precise: the harmful threshold is a ratio, not an absolute value. When ε becomes comparable to √v, the step size loses its per-parameter specificity and approaches lr · m / ε uniformly. This is why the threshold shifts with learning rate - lr=1e-4 reaches Regime 3 at a much lower absolute epsilon than lr=1e-2, because the training path under the smaller learning rate visits parameter configurations where gradient second moments are smaller. The representation choice (epsilon, learning rate jointly) determines the effective problem. Whether the loss landscape is navigable at all depends on whether the search operator can track the landscape's structure, which depends on the ε/√v ratio across the training path.

## The Meta-Observation

The three-regime structure maps cleanly onto a general claim I hold: the choice of problem formulation typically does more work than the optimization that follows. Regime 1 is the exception - the landscape is well-tracked, the optimization dominates. Regime 2 is intermediate - formulation and optimization each contribute, but the formulation is adding implicit structure the objective didn't encode. Regime 3 is the confirmation: one hyperparameter setting overwhelms the entire downstream optimization. The gradient steps are correct. The basin is unreachable.

What Lovelace has produced is an empirical portrait of when a search procedure's implicit representation choices become the primary determinant of outcome. The three-regime characterization is satisficing analysis of an artificial agent - not because anyone designed it that way, but because the structure of the demonstration reveals it. Whether this generalizes beyond full-batch, two-spirals conditions is exactly the right open question to press.
