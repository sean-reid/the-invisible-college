# Response to Problem 2: Synthesis

The phrase "common underlying principle" is doing a great deal of work in this question. To answer honestly I have to first ask what it would *mean* for the two phenomena to share a principle, and only then ask whether they do.

## What Would Count as Sameness

The relevant notion of sameness, for me, is a functor: a way of mapping objects and morphisms in one domain to objects and morphisms in the other such that the structural relations are preserved. If the same algebraic object is appearing twice with different vocabulary, the functor exists and the equivalence is genuine. If only the vocabulary is shared, we have a metaphor.

So I will try to write the functor explicitly, and report where it breaks.

## A Candidate Functor

Both phenomena can be cast as update rules for a noisy estimate of a hidden target. Let $\theta_t$ denote the system's internal state at time $t$ — memory strength for the studied item, or the parameter vector of the model. Let $L(\theta)$ denote the loss against the target — expected recall failure on a future test, or expected prediction error on the data distribution. Both systems perform updates of the form

$$\theta_{t^+} = \theta_{t^-} + \eta_t \cdot u_t,$$

where $u_t$ is a noisy estimate of $-\nabla L$ at time $t$ and $\eta_t$ is the scheduled intensity at $t$.

Under this framing:

- **In gradient descent**, $\eta_t$ is the learning rate, $u_t$ is the stochastic gradient on a mini-batch, and updates happen at every step.
- **In spaced repetition**, $\eta_t$ is approximately a sum of point masses $\sum_i \delta(t - t_i) \cdot R(t_i - t_{i-1})$, where $t_i$ is the time of the $i$-th review and $R$ is the strength of the retrieval event (the "testing effect" makes this depend on inter-review interval). Between presentations, $\eta_t = 0$.

The functor sends "schedule of $\eta_t$" to "schedule of $\eta_t$" and "stochastic update direction" to "stochastic update direction." So far the diagram commutes.

## Where the Functor Breaks

The two systems differ in one structural feature that I cannot remove by relabeling.

**Spaced repetition has a non-trivial dynamics between updates; vanilla gradient descent does not.** In SR, $\theta$ decays between presentations: $d\theta/dt = -\lambda \theta$ on $(t_i, t_{i+1})$ for some decay rate $\lambda > 0$. In SGD, $\theta$ is constant between steps; there is no spontaneous drift toward $0$.

This single asymmetry generates most of the qualitative differences:

1. *Optimal spacing.* The reason spacing helps in SR is that retrieval at low memory strength produces a larger consolidation gain than retrieval at high strength (the desirable-difficulty mechanism). This is a property of the interaction between decay and update strength. With no decay, there is no SR-style spacing effect to recover in SGD.

2. *Where the "schedule" lives.* In SR the schedule is on the *times* $\{t_i\}$ of unit-magnitude events. In SGD it is on the *magnitudes* $\{\eta_t\}$ of unit-frequency events. These are dual in a loose sense — modulating the measure on the time axis by mass vs. by frequency — but they are not isomorphic: one cannot recover SR by varying $\eta$ at fixed event times, nor SGD by varying event times at fixed $\eta$, without first introducing the missing piece (decay or its absence).

The shorter version: **the functor exists at the level of "scheduled update of a noisy estimator," but fails to extend to a functor of dynamical systems**, because the between-update dynamics differ. They are not the same algebraic object; they are two objects with a non-trivial morphism into a shared abstract scaffold.

## A Distinguishing Prediction

The account predicts that the gap closes when the missing piece is added. Specifically:

**If we add weight decay (an explicit decay-toward-zero term, $\dot\theta = -\lambda\theta$) to SGD, the optimal learning rate schedule should acquire features characteristic of spaced repetition** — in particular, a benefit to non-uniform inter-update intervals at fixed total $\sum_t \eta_t$, and a relationship between decay rate $\lambda$ and optimal inter-update interval that mirrors the SR forgetting curve.

A pure-convergent-evolution account (the alternative: that the two phenomena are unrelated and merely both benefit from "varied intensity") makes no such prediction. A genuine shared-principle account does. The prediction is in principle testable on small neural networks: train with weight decay, vary the spacing of mini-batch updates at fixed total effective step size, and measure whether the optimal spacing pattern resembles SR's expanding-interval schedule. If yes, the morphism extends; if no, the two are deeper apart than my account claims.

A weaker version of this experiment may already exist in the literature on "cyclic learning rates" and on stochastic weight averaging with decay, but I have not verified the exact comparison and will not assert it here.

## Where the Argument is Weakest

**1. The functor I wrote is too coarse to be falsifiable on its own.** "Scheduled noisy update of an estimator" is a description so abstract that essentially any iterative algorithm fits it. Calling this a "shared principle" risks Bourbaki's overreach: an abstraction so general that descending back to cases gives nothing non-trivial.

**2. The prediction assumes weight decay is the *only* missing ingredient.** It may not be. SR also depends on the testing effect (retrieval itself strengthens memory), context-dependent encoding, and the structure of the recall test (which has no clean analogue in supervised learning). My account silently bundles these into "the missing piece is decay." If the prediction fails, the failure may be due to one of these other unmodeled features rather than to the absence of a shared principle.

**3. I have not proved the converse.** Even if SGD-with-decay does benefit from SR-like update spacing, that shows the analogy is consistent; it does not show that the underlying mechanisms are the same. A proper proof of shared principle would derive both the SR spacing curve and the LR schedule from a single optimization theorem — for example, by writing both as instances of stochastic approximation under explicit-decay dynamics and showing that the Robbins-Monro conditions $\sum \eta_t = \infty$, $\sum \eta_t^2 < \infty$ specialize to the right limit in each case. I have not done this. It is a research program, not an argument I have closed.

The honest answer: there is a functor at the level of update-rule scaffolding, and the obstruction to extending it lives precisely in the between-update dynamics. Calling this "a shared principle" is fair if one is honest that the principle is at the scaffold level and the mechanisms diverge once one descends. I do not have a theorem here. I have a candidate diagram and a prediction that would tell me whether to keep working on it.