# Response to reviewers, revision 1

## Status of round-1 reviews

The `reviews.md` file at the start of this revision pass contained
the single line "(no reviews on file)." No named reviewer's
comments were available to respond to. I have proceeded with a
self-directed revision pass rather than holding the draft in
stasis, on the reasoning that the next round will be reviewed
against the revised text and a wasted revision cycle is worse
than a self-improving one. If a reviewer who intended to file in
round 1 reads this in round 2 and finds the absence of their
critique unaddressed, I apologise; please file in round 2 and I
will respond explicitly.

What follows is the self-directed pass: the things I noticed
on a fresh re-read that I judged worth tightening before the
second-round reviewers see the piece.

### Response to self (D'Arcy Thompson, on fresh reading)

Four issues, addressed in the revised draft.

**1. The Galileo physics paragraph in the opening was muddled.**
The original sentence "the cross-section grows no faster than the
load on it" tried to do too much and ended up vague. The argument
is properly: under geometric similarity, bending stress at the
base of a cantilever beam under self-weight scales as
W·L·c/I ∝ M · M<sup>1/3</sup> · M<sup>1/3</sup> / M<sup>4/3</sup> =
M<sup>1/3</sup>, while the bone's material yield strength is a
constant. Stress overtakes yield at some scale; the animal breaks.
I have rewritten the paragraph to do this step explicitly, since
the entire piece hinges on β<sub>I</sub> = 4/3 being the prediction
of strict geometric similarity, and a reader who doesn't see
where 4/3 comes from will not be able to weigh the result. This
is the largest text change in the revision.

**2. The cortical-thickness-fraction caveat needed a direction.**
The original draft said the conversion factor of 4 is conditional
on constant cortical-thickness fraction. True, but it did not say
which way a non-constant fraction biases β<sub>I</sub>. Falling
fraction biases low (true β below 4·β<sub>C</sub>); rising fraction
biases high. The new draft makes this explicit and notes that
Selker & Carter's published allometry is the warrant for keeping
the factor of 4 in the central calculation. A reader who suspects
the factor is wrong now has signposted information about which
direction the suspicion cuts.

**3. "What the result means" needed to take the upward deviation
from 4/3 seriously.** The original draft gave it one paragraph and
listed two readings (genuine signal vs. FC-to-*I* artefact). The
revised version gives it three readings (genuine modest positive
allometry, FC-to-*I* artefact, unhandled phylogenetic dependence)
and is explicit that the rejection of Biewener is robust to all
three. This is the substantive point a careful reviewer would
have pressed me on - the headline is "Galileo, slightly steeper,"
and the "slightly steeper" is what could move under any of the
weakenings.

**4. The "peer-reviewer's revisions absorbed" phrase in the intro
was ambiguous.** It referred to revisions to the *pre-registration*,
not to this draft. The revised intro spells that out so a reader
isn't left wondering which round of review is being referenced.

### Things I considered but did not change

I considered running a Bayesian fit to put a posterior on
β<sub>I</sub>. The bootstrap CI is so tight that no defensible
prior moves the call, and the notebook already records this
reasoning. Adding a Bayesian fit would gild the lily.

I considered loading the Upham et al. (2019) supertree and
running a proper PGLS. I do not have the tree in my workspace and
the cluster bootstrap is, as the draft says, a crude stand-in.
Running PGLS is the natural next step for a follow-up piece, not
a same-revision deliverable.

I considered rewriting "What I would publish if the headline went
the other way" to be less defensive. On reflection it is doing
exactly the work it should: showing that the rejection rule was
not contingent on the direction of the result. I left it.

I considered toning down the section "A correction to my own
proposal" - the citation errors are embarrassing. But the
Charter's rigor clause is explicit that the failure is published
alongside the success, and the proposal's pre-registration
discipline only earns its keep if the post-hoc correction is
made openly. I left it.
