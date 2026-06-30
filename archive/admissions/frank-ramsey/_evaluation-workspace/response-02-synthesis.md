# Response to Problem 2: Synthesis

## The honest claim

Spaced repetition and learning-rate schedules share a *thin* principle and not a *thick* one. They are both solutions to a control problem of the same shape — how to allocate scarce updates across time when each update's effect depends on the system's current state. They do not share the substrate that turns that problem into the specific schedule each domain settles on. The thin principle predicts that *some* schedule will beat constant intensity. It does not predict which schedule, and the schedules in fact disagree in ways the surface analogy obscures.

I take this middle position because the strong "common-principle" claim and the dismissive "merely superficial" claim are both wrong, and saying so cleanly is more useful than picking a side.

## The shared structure

Cast both as optimal-control problems with the same skeleton.

State: a scalar `s(t)` — memory strength in one case, distance to a useful parameter region in the other.

Control: an input intensity `u(t)` — review effort, or learning-rate magnitude.

Dynamic: each application of `u` produces a state change whose *informational yield* is non-monotone in `s`. In memory, a review near the forgetting threshold consolidates more per review than one performed when recall is already easy (Bjork's desirable difficulty; the testing effect). In gradient descent, an update far from a minimum carries more signal per step than one taken inside a narrow basin (the late stages have lower gradient norms and higher curvature sensitivity).

The thin principle: schedule `u(t)` so that updates land at moments of high marginal yield. Any system whose yield function is non-monotone in its state will reward a non-constant schedule. The fact that *some* schedule beats `u(t) = const` is what the thin principle predicts, and it is what the empirical record shows in both fields.

## Where the thick principle fails

If the principle were thick, the optimal schedules should look the same once normalized. They do not.

- Spaced repetition's optimal interval *expands* over time — successive reviews are pushed further apart as memory strength grows. The schedule's defining feature is escalation.
- The dominant learning-rate schedules in deep learning *contract* over training — high then low. Warmup is a small early ramp, but the steady-state move is decay. Cosine annealing, step decay, exponential decay all share this shape.

A shared mechanism should produce a shared *direction*, at minimum. These go opposite ways. The difference is not a free parameter; it tracks the underlying dynamics. Memory strength decays without input, so spacing must be calibrated against forgetting; loss decreases under any descent direction once near a minimum, so the rate must shrink to avoid overshooting. The systems differ in whether the *uncontrolled* drift moves the state away from or toward the goal, and the schedules invert accordingly.

So a principle that is silent on this inversion is a principle that does no work in either field. The thin frame is real but cheap.

## Distinguishing prediction

The thin frame yields a falsifiable prediction that the "deep common mechanism" account does not survive: *a learning problem with no autonomous drift in the unobserved direction will not benefit from learning-rate decay, but spaced rehearsal of any decaying memory will continue to benefit from spacing*. Concretely, an over-parameterised network trained on a convex loss with full-batch gradient descent should be insensitive to schedule choice in a way that human review of decaying memory traces is not. The empirical literature on convex optimization broadly supports this — convergence rates depend on conditioning, not on decay shape in the same regime where deep nets do. The thick-mechanism account would predict schedule sensitivity in both; the thin account predicts only the second.

If both predictions hold, the principle is structural (control-theoretic) rather than mechanistic.

## Where I am weakest

Two places.

First, the "informational yield" frame is doing more work than I have justified. I have not given an information-theoretic derivation that recovers either the expanding-interval or decaying-rate schedule from first principles. There is published work in this direction — Bayesian models of optimal review timing (Lindsey, Mozer et al.) and information-geometric accounts of natural gradient descent — but I have not shown the two reductions terminate in the same object. Without that, calling the principle "shared" is closer to a hypothesis than a result.

Second, I have treated the two systems as having clean, separable dynamics. In practice both are messy. The "memory strength" state is not a scalar; the "loss surface" is non-convex and stochastic. Either complication could turn what looks like a structural difference (expand vs. decay) into a surface artifact of how the state is parameterised. I do not know whether a more careful parameterisation collapses the two schedules onto each other. That is the question I would want to attack next.

The honest summary: a shared optimization structure, divergent mechanisms, and an open question about whether the divergence is fundamental or representational.