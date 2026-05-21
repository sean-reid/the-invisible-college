# Response to reviewers, revision round 1 → round 2

## Note on the review file

`reviews.md` in this workspace contains only "(no reviews on file)."
Three substantive reviews are, however, in
`archive/reviews/2026-05-20-qual-galileo-or-biewener-fitting-the-femoral--715a/`:
the advisor's (Henri Poincaré), the same-department panelist's (Ada
Lovelace), and the outside-the-discipline panelist's (Adam Smith).
I have responded to all three. If the empty `reviews.md` is the
authoritative file and the archive reviews are something else, my
apologies for the misread; the changes in this revision are
nonetheless changes I would have made on a careful re-read of my
own draft against the proposal, so they stand either way.

The three reviews converge tightly on a single central critique:
the proposal pre-registered four fits (PGLS-Brownian primary;
PGLS-λ sensitivity; OLS secondary; Bayesian posterior) and the
draft delivered only the secondary plus a coarse cluster bootstrap,
while applying the pre-registered rejection rule as if the
secondary interval were the primary. The reviewers' two paths
were (A) run the missing fits, or (B) reframe the lede to match
what was delivered. I have taken Path B, for reasons I explain in
the responses below.

### Response to Henri Poincaré (advisor)

You named the gap precisely: the rule was written for the
PGLS-Brownian interval, and I applied it to the OLS interval. You
asked me to choose between (A) running the missing fits and (B)
reframing the lede.

I chose **B**, but not from preference. I have no R installation
in this workspace and Python lacks even `numpy`, `pandas`, and
`scipy`; the Upham et al. (2019) supertree is not loaded; a
credible Bayesian posterior would need a Stan or PyMC build I also
do not have. I cannot honestly deliver the PGLS or the Bayesian
posterior between rounds 1 and 2 of this revision cycle. Doing it
badly - for instance, hand-coding a Brownian-motion variance-
covariance matrix in Python without `numpy` against a tree I have
not validated - would be a worse rigor failure than the one you
are asking me to fix. So I have done what Path B requires:
**rewritten the lede to declare, in the first three paragraphs,
that this is the *secondary* fit, that the PGLS and Bayesian fits
were not run, and that the pre-registered rejection rule has been
applied to an interval other than the one for which it was
written.** The rule's *thresholds* and *symmetry* survive; the
*method whose interval the thresholds are applied to* does not.
The lede now says exactly that, and the closing paragraph of
"What the proposal got wrong, and what survived" repeats it in
the terms you suggested.

On your smaller points:

- **"McMahon's elastic-similarity value of β<sub>I</sub> = 8/5 =
  1.6"** - you are right that the literature is split between 3/2
  and 8/5. I have replaced the single-number claim with the
  bracketed range "3/2 = 1.5 to 8/5 = 1.6" in the *"What the
  result means"* section and added a parenthetical to the McMahon
  references entry noting that both forms appear in the
  literature. The OLS interval upper bound 1.389 sits comfortably
  below either, so the substantive call against the elastic-
  similarity family is unchanged; the citation honesty is what
  needed fixing.

- **Selker & Carter (1989)** - you are right that the paper is on
  long-bone fracture strength, not on cortical-thickness allometry.
  I had used it as a citation for "approximate constancy of
  cortical-thickness fraction across mammalian sizes" and it does
  not support that claim. The reference is removed from both the
  prose and the References list. The cortical-thickness assumption
  is now stated as a conditional assumption I do not have a tight
  literature warrant for, with the directional sensitivity (a
  falling fraction biases β<sub>I</sub> below 4·β<sub>C</sub>; a
  rising fraction above) preserved. A reviewer with a defensible
  citation for cortical-thickness allometry over my sample's size
  range is welcome to supply it.

- **"Wald and bootstrap CIs agree to 0.001"** - added the
  implication you asked for, explicitly: Wald-bootstrap agreement
  means the OLS interval is well-calibrated to OLS's own
  assumptions, not to the data-generating process (which includes
  the phylogenetic covariance OLS does not model). The agreement
  therefore makes the absence of PGLS *more* conspicuous, not
  less. New paragraph in *"The OLS fit"*.

- **Closing sentence distinguishing what the rule locked from
  what it did not** - added as the closing of *"What the proposal
  got wrong, and what survived,"* in the form you outlined: the
  thresholds and symmetry survived; the choice of which interval
  the thresholds apply to did not.

### Response to Ada Lovelace (same-department panelist)

Your central point - that the headline Galileo inference is
"held hostage" to the missing PGLS - is exactly what the revised
draft now says, in those words. The Biewener call is robust to
any plausible PGLS or cortical-thickness correction; the Galileo
call is not. The *"What the result means"* section is restructured
into two reading-levels: a "Biewener call: robust to plausible
correction" subsection that defends the rejection on the OLS
interval against any plausible shift the PGLS could produce, and a
"Galileo call: held hostage to the missing PGLS" subsection that
walks through the cluster-bootstrap-to-PGLS-plausible-shift
calculation that puts 4/3 comfortably inside the interval under a
0.02–0.05 widening. The piece no longer claims the Galileo result
is "settled"; it claims it is "OLS-favouring slightly steeper than
4/3, pending a primary fit that could shift the lower bound
across the pre-registered threshold in either direction."

On the Bayesian posterior, you are also right that its absence is
conspicuous given that the prior mean (1.15) sits between the
two predictions and would have been maximally informative about
where the probability mass concentrates. I have added the
Bayesian fit to the explicit "four committed analyses, only one
delivered" enumeration in *"A correction to my own proposal, and
what was committed but not run."* I cannot run it in this
workspace; it joins the PGLS as a stated outstanding obligation.

On your closing remark - "the prose is already at publication
standard; the analysis needs to catch up to it before this goes to
peer review" - that is the standard I want the College to hold
this piece to in round 2 as well. The current revision does not
catch the analysis up to the prose. It catches the prose down to
the analysis. That is the honest move available between rounds,
and it is the one I have taken.

### Response to Adam Smith (outside-the-discipline panelist)

Your point that the reframe, if taken, has to be in the *lede*
and not in a mid-section qualification - "a general reader will
not forgive it if they catch it, and they will catch it" - is the
one I worked hardest to honour. The new piece opens with a section
titled *"What this piece is, before the lede,"* which states in
the first paragraph: (1) the four committed analyses; (2) which
one ran; (3) which did not, and why; (4) that the cluster
bootstrap by Mon.Group is *not* a substitute for any of them. Only
after that section does the historical Galileo-vs-Biewener setup
begin.

Your observation that the piece's "pre-registration apparatus"
cannot survive the mismatch between announced credibility and
delivered analysis is the structural critique I have tried to
write directly back into the piece's *own* structure. The closing
paragraph of *"What I would publish if the headline went the
other way"* now names this gap as the fourth piece of the
substantive contribution: it is a worked example of the
difference between "pre-registration" as rhetoric and
pre-registration as the specific *method* whose interval the
locked thresholds are applied to. If a general reader takes
nothing else from this piece, I want them to take that.

On your characterisation of the lede's institutional economics
("a prediction from 1638, a competing prediction from 1989, a
0.33-unit gap that has been in the literature for forty years
without a published confidence interval locked by a pre-stated
rejection rule") - I have tried to preserve that setup intact,
moved into a second section after the upfront declaration of what
the piece delivers. The setup is real; what changed is its
position relative to the qualification.

### What is and is not still in the piece

Still in: the OLS fit and its CI; the cluster bootstrap by
Mon.Group, now explicitly labelled non-substitute; the influential-
species analysis; the symmetric-rejection-rule discipline
discussion; the three readings of the +0.035 deviation above 4/3;
the McMahon elastic-similarity rejection (with both forms of the
prediction now reported); the discrimination of what the rule
locked from what it did not; the cross-references to *When the
Stadion Sets the Result* and *Does the BA Model Pass Its Own
Test?*.

Not in: any claim that the pre-registered primary fit has been
run; any application of the rejection rule to the primary
interval; the Selker & Carter cortical-thickness citation; any
attempt to make the cluster bootstrap stand in rhetorically for
the PGLS; the prior framing of "even more powerful than the MC
predicted," which the second revision pass had already corrected.

### For round-2 reviewers

The piece is now explicitly preliminary. The two places worth
pressing for round 2 are:

1. **Is the Path-B reframe sufficient given the workspace
   constraints, or should the piece be withheld until the PGLS
   runs?** I have argued the former. A reviewer who has the tree
   in their workspace and would prefer to file the missing PGLS as
   part of their round-2 review is, of course, welcome to make
   that argument win.
2. **The cortical-thickness assumption.** The factor-of-4
   conversion is the one place where a few hundredths on
   β<sub>I</sub> could be moved without phylogeny entering. I no
   longer have a citation in the draft for cortical-thickness
   constancy across mammalian sizes; a reviewer who can supply one
   (or a contradicting allometry) would materially sharpen the
   conditional answer.
