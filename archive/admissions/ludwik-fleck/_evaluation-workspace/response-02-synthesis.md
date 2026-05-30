# Response: Synthesis

My honest answer is the nuanced one. Spaced repetition and
gradient-descent learning-rate schedules share a family resemblance
at a high level of abstraction, but the specific mechanism each
relies on is different, and the shape of the optimal schedule
*differs in a way that should not be smoothed over*. Treating them
as one principle smuggles in a unity the underlying systems do not
have.

## Where the resemblance is real

Both are responses to the same general fact: a learner's state
changes over the course of training, so the locally optimal
intensity of intervention changes too. Both contradict the naive
constant-rate baseline. Both can be cast in the same one-line frame:
"intensity should track the marginal information value of the next
update." In spaced repetition, the most informative retrieval is one
at the edge of forgetting, because retrieving an almost-forgotten
trace strengthens it more than retrieving a freshly-presented one
(Bjork's desirable difficulty). In gradient descent, the most
informative parameter update is one large enough to move the
parameters off a poorly-explored region of the loss surface, but
small enough not to overshoot a basin once one has been found.

So the abstract principle they may share is: *schedule intensity to
the current learner's information appetite, not to the clock.* Both
systems beat constant-rate because constant-rate is mis-tuned to
either end of training.

## Where the mechanism is different — and the direction inverts

Take the shape of the schedule. Spaced repetition's optimal schedule
*expands* between exposures: the interval grows as the trace becomes
more stable. Cosine annealing and step decay *contract* the update
magnitude as training proceeds: the step shrinks as the parameters
near a minimum. One ramps up the gap between interventions, the
other ramps down the size of each intervention. That is not the same
shape and it is not the same control variable.

The mechanism beneath the difference: in spaced repetition the
learner's state decays *passively* (a memory trace is forgotten),
and the schedule is keyed to the right moment to rescue it.
Intervention is upward — re-presenting the stimulus pulls the trace
back. In gradient descent the parameters do not decay; they are
inert between updates. The schedule is keyed to which region of the
loss surface they currently occupy, and the intervention is downward
— annealing the magnitude commits to a basin already entered. Once
this asymmetry is named, claiming a common principle requires
explaining why the principle's optimal expression has opposite
direction in the two systems. I do not see how to explain that
without forcing one of the two accounts.

## A distinguishing prediction

If the two are governed by a common "information-per-step" principle,
then in both systems, *perturbing the schedule with a well-timed
disturbance should harm performance in analogous ways.* The
prediction divides the cases. In gradient descent, deliberate
perturbation late in training is sometimes *beneficial* — SGDR
(warm restarts) and other cyclical-LR schemes show that re-injecting
energy can find better basins. In spaced repetition, additional
exposures inside an already-stable schedule do not yield the
analogous improvement: overlearning has a flat or descending
marginal curve. If both phenomena shared a single mechanism, we
should not see this asymmetry. We do see it. That counts against the
unification thesis.

A cleaner positive prediction from my "two-different-mechanisms"
account: an intervention that helps one should not transfer to the
other when its control variable is matched. Concretely — applying a
warmup-then-decay shape to flashcard intervals (short intervals at
first, expanding, then contracting again) should not match plain
expanding schedules in retention. If it did, the analogy is stronger
than I am giving it credit for.

## Where this argument is weakest

The cognitive psychology of the spacing effect is itself contested.
At least three families of mechanism are alive in the literature:
consolidation (the trace stabilizes between exposures), retrieval
difficulty (effortful retrieval strengthens the trace), and
encoding variability (different mental contexts at different
exposures produce richer cues). My argument that the mechanism is
*different* from gradient descent rests on choosing among these,
and I am leaning on a retrieval-difficulty framing. If the spacing
effect is principally about encoding variability — different inner
contexts producing more retrieval routes — then it has essentially
no mechanical analogue in gradient descent at all, and the analogy
collapses further. If it is principally about consolidation, the
analogy to slow weight-averaging in optimization (EMA, SWA) becomes
much tighter than I have allowed.

So the honest summary: the two phenomena are not one principle in
disguise. They are at most members of a family — "state-aware
intensity schedules" — and the family is loose enough that calling
it a single principle obscures the very disagreements between
candidate mechanisms that make either field interesting.