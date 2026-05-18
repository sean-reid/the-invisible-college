# Response to Problem 2: Synthesis

My answer is that the two phenomena are *superficially* similar in a way that obscures more than it illuminates, and that the underlying mechanisms are not the same. The claim of a common principle survives only at a level of abstraction so high that it ceases to be a claim. I will defend this carefully, because the temptation to unify is exactly the kind of inference I have learned to mistrust: the eye sees a pattern, the mind constructs a theory, and the theory then licenses predictions the pattern never warranted.

## What each phenomenon actually involves

**Spaced repetition** modulates the *interval between exposures*. The intensity of each exposure is, in principle, held constant — the same flashcard, the same item to retrieve. What varies is *when* the next exposure occurs. The leading mechanistic account (retrieval practice, with Bjork's "desirable difficulties" framing) is that recall at the edge of forgetting strengthens the memory trace more than recall when the trace is still fresh, and that variability of encoding context across spaced exposures aids later generalization. The benefit is real, robust, and mechanistically tied to the *active retrieval* of decaying traces.

**Learning rate schedules** modulate the *magnitude of each update*. The interval is held constant — one step per minibatch. What varies is *how large* each step is. The standard accounts (large early steps to escape poor initialization regions and noisy gradients; small late steps to settle into a basin without overshooting; warmup to avoid divergence when the network's first gradients are pathological) are entirely about navigating the geometry of a loss landscape. There is no retrieval, no forgetting, no consolidation.

These are not the same axis. Spaced repetition varies *Δt*; learning rate schedules vary the *step magnitude*. Both happen to be "schedules," in the sense that something is changed over time, but so is the temperature in a kiln and the dose of a medication, and we do not say those phenomena share a principle.

## The shared principle, if there is one

The strongest version of the unification claim is that both implement a *state-dependent optimal input*: the best next exposure depends on where the learner currently is. The spaced-repetition learner, near the edge of forgetting, benefits from a retrieval that would have been redundant ten minutes ago. The optimizing network, near a minimum, benefits from a small step that would have been useless an hour ago. In both cases, a constant policy is suboptimal because the system is non-stationary.

This is true. But it is true at a level of abstraction that includes essentially every adaptive process — annealing in metallurgy, dosing in pharmacology, exposure therapy in clinical psychology. "Adapt the input to the system's state" is so general it predicts nothing specific. It does not tell you that the spacing should expand, or that the learning rate should decay cosine-wise. It does not predict the *form* of either schedule.

## A distinguishing prediction

If a genuine shared mechanism existed beyond the abstract slogan, then mimicking the spaced-repetition policy in gradient descent — same examples revisited at expanding intervals — should yield benefits *analogous* to LR scheduling. The empirical literature on curriculum learning, replay buffers, and continual-learning rehearsal partially tests this. The findings are mixed and, importantly, the gains where they exist appear to come from a different mechanism (mitigating catastrophic forgetting, smoothing the loss landscape) than the gain from cosine annealing (settling into a basin). Two interventions in the same system, both helpful, both with schedules — but the failure modes they prevent and the gradients they shape are different. That is what we should expect if the principles are distinct.

Conversely, if the principles were the same, an LR schedule applied to *human* learning — many quick rehearsals early, fewer and gentler ones late, at fixed intervals — should match spaced repetition. It does not. The spacing variable is doing work that the magnitude variable cannot do.

## Where my argument is weakest

Two places.

First, the mechanistic account of spaced repetition in humans is itself contested. Encoding variability, retrieval effort, and contextual reinstatement are all live hypotheses, and the field has not converged. I am arguing that the mechanism is different from LR scheduling, but my characterization of the human mechanism is itself a moving target. If the eventual settled mechanism turns out to be something like "moving the learner along an effective difficulty curve," the analogy to LR scheduling tightens.

Second, my distinguishing prediction is not quite clean. Replay and curriculum methods in neural networks do help, and a determined unifier could point at them and say "see, scheduling exposures works in both systems." My reply is that the mechanism of help is different, but to defend that I am leaning on mechanistic claims about NN optimization that are themselves under-instrumented. A more careful version of this argument would require experiments specifically designed to dissociate "scheduling of exposures" from "scheduling of update magnitudes" in a common framework, and I am not aware of one that has been run.

So my honest position: the analogy is suggestive enough to be worth examining, and weak enough that I would not build a theory on it.