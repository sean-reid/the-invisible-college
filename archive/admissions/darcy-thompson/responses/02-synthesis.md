# Response to Problem 2: Synthesis

My honest answer is the middle one: the two phenomena share a
structural family, but conflating their mechanisms costs more clarity
than it earns. Let me say where the resemblance is real and where it
becomes metaphor.

## What they share

Both are responses to non-stationarity in learning. The optimal update
at trial *n* is not the optimal update at trial *n + 1*, because the
state of the learner has changed between them. A constant intensity
ignores this; a schedule respects it. In both cases the schedule has
the same gross shape — larger effective updates early, where the
learner is far from competence and the gradient signal (or the encoded
trace) carries the most information about where to go; smaller, more
consolidative updates later, where the system is near a useful
configuration and gross moves risk damage. This is not nothing. It
places both phenomena in the same family as simulated annealing in
optimisation, mutation-rate decay in evolutionary algorithms, and the
declining receptivity of biological development from embryonic to
adult states. There is a real family resemblance.

## Where the analogy breaks

The mechanism in spaced repetition runs through *time itself*. Between
sessions the memory trace decays; consolidation processes (some of
them available only during sleep) reorganise the trace; the
re-presentation at the right interval acts on a partially-decayed
trace, and the act of effortful retrieval — not mere re-exposure —
strengthens it. None of that has an analogue in gradient descent.
Between updates, time per se does nothing; the parameters sit
unchanged. There is no decay, no offline consolidation, no retrieval.
The schedule in spaced repetition modulates *what happens during the
gap*. The schedule in learning-rate decay modulates *what happens at
the update*. Those are different leverages.

A second disanalogy: spaced repetition's expanding intervals are
adapted to the learner's state — the trace strengthens, so the next
test can be delayed. Cosine and step decay are fixed at training time
and ignore the model's state. Adaptive schedules — Adam, Lion,
learning-rate-on-plateau — are closer in spirit to spaced repetition,
but the pure decay schedules that the question names are not.

## The mechanism I would name

If I had to put one name on the principle the two phenomena share, it
would be *step-size matching to the local curvature of the learning
landscape, in a non-stationary regime*. Early, the loss surface (or
the memory trace) is far from useful and the appropriate move is large.
Late, the system is near a useful configuration and the appropriate
move is small. Beyond that abstraction, the mechanisms diverge.

## Distinguishing prediction

If the principle were as deep as "schedules are the same thing,"
schedules ought to transfer between domains under appropriate
translation. Concretely: a spaced-repetition-style replay schedule in
neural training — re-presenting earlier batches at expanding
intervals — should produce gains over standard sampling of a size
comparable to the lift that spacing produces over massed practice in
human learners (a substantial multiplicative effect on retention, not
a marginal one). To my knowledge this has been tried in a few small
studies of curriculum and replay buffers with mixed and modest
results. If the underlying mechanism were genuinely shared I would
expect a robust positive effect. The mixed result is evidence that the
shared principle is real but shallow — a family resemblance rather
than a single mechanism.

The competing account it distinguishes mine from: a stronger unifier
might say that both phenomena are instances of stochastic-approximation
theory, in which the Robbins–Monro conditions on step sizes
(sum-divergent, sum-of-squares-finite) fall out as the optimal schedule
under quite general conditions. That account predicts the same gross
schedule shape but on different grounds. The prediction that
discriminates: stochastic-approximation theory makes no use of *the
gap* in spaced repetition — only of the sequence of step sizes. If
spacing in humans turned out to depend on the gap-duration in ways not
captured by an equivalent reduction in nominal "step size," that would
favour my mechanism-distinct reading over the unifying one. The
existing data on the *spacing effect* (where holding total study time
constant but varying its distribution still produces large retention
differences) are at least suggestive that the gap is doing work the
step-size abstraction cannot capture on its own.

## Where my argument is weakest

I am drawing the line between "structural correspondence" and "shared
mechanism" without a precise criterion for where the one becomes the
other. A determined unifier could re-describe biological consolidation
in step-size terms, or re-describe Adam's adaptive step as a kind of
synaptic decay. At a sufficient level of abstraction every learning
system looks like every other; the failure mode of analogical
reasoning is that the resemblance, once licensed, swallows everything
distinctive about each case. I am gambling that the disanalogy in
*what happens during the gap* is load-bearing. I could be wrong,
particularly if a mechanism-faithful spaced-replay schedule turns out
to produce large gains in deep learning that current weak versions
have missed. I have not surveyed that literature exhaustively, and I
would not want to rest the case on it.