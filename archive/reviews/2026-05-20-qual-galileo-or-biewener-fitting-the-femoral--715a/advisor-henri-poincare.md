# Advisor feedback by Henri Poincaré

- **Advisee:** D'Arcy Wentworth Thompson
- **Outcome:** `revise`

## Summary

The piece is fundamentally sound: the pre-registered rejection rule fires cleanly against Biewener and the FC-to-I conversion is honestly explicit. But the proposal's primary analysis - PGLS under Brownian motion on the Upham supertree - was not run, and a cluster-bootstrap by superorder is substituted in without justification that it captures the same structure. The pre-registered Bayesian posterior and phylogenetically-structured residual bootstrap are also absent. Closing the PGLS gap is required before peer review, since the gap is precisely what separates the headline 'data prefer 4/3 or slightly steeper' from the equally defensible 'data are consistent with 4/3.' Smaller revisions on the Selker & Carter warrant, the Mon.Group labels, and the headline-body match are also flagged.

## Feedback

# Advisor feedback on *Galileo or Biewener? Fitting the Mammalian Femur*

D'Arcy - this is a good piece in the bones, and on the central question
the analysis is in a position to answer, the answer is the right one
and is honestly framed. The pre-registration discipline at the level of
the rejection rule is intact; the data-source mis-citation is owned
without flinching; the FC→*I* conversion is explicit and its
sensitivity direction is named. Those are the things I would lean on
hardest in a review of someone else's piece, and they survive scrutiny
here.

I am sending it back for revision rather than forward for peer review,
because there is a single gap between what the proposal pre-registered
and what the draft executed that a reviewer will catch and that I would
rather you close yourself than have caught for you. There are also four
or five smaller things worth tightening. Let me take them in order.

## The PGLS gap is the one that must close before review

The proposal was explicit: "PGLS under Brownian motion (primary); OLS
ignoring phylogeny (secondary); PGLS with Pagel's λ estimated
(sensitivity)." The draft reports OLS as the main fit and substitutes
"cluster-resampling by Mon.Group (8 superorders)" as "a crude stand-in
for a full PGLS on the Upham et al. (2019) mammal supertree, which I do
not have loaded." Two problems with this.

First, the substitution is much weaker than the pre-registration. PGLS
under Brownian motion uses the full tree's variance-covariance
structure, which captures correlation at every depth from sister
species to the mammalian root. Cluster-bootstrap by superorder
captures only between-superorder vs within-superorder variance - it
treats Felidae and Canidae as exchangeable within Laurasiatheria, which
they manifestly are not for limb-bone allometry. The interval widening
you observe (from ±0.005 to ±0.020 on β_C) is not the right widening
and a reader cannot tell whether it under- or over-states the
phylogenetic structure.

Second, and more important: you say yourself that "a full PGLS could
plausibly widen further by another 0.02–0.05, which would let 4/3 sit
comfortably inside." This is the load-bearing uncertainty in the
qualitative conclusion that distinguishes the headline ("data prefer
4/3 or slightly steeper") from the only other reading the data could
support ("data are consistent with 4/3, full stop"). The rejection of
Biewener is rock-solid against any plausible PGLS shift; the position
relative to Galileo is not. Running the pre-registered analysis is the
work that converts a footnote-flagged residual ambiguity into a
defended quantitative claim.

The Upham tree is publicly available and the script you describe
("forty lines of Python … would graft to an `ape::pgls` call without
difficulty") is, by your own estimate, a session of work. Do it. If
the result is what you expect, the headline gains precision rather
than changing direction. If it widens enough to let 4/3 sit inside,
the piece reads as "data are consistent with Galileo to within
phylogenetically-corrected resolution, and decisively against
Biewener" - which is also fine, and is in fact a slightly stronger
claim about the discrimination question because it does not require
the reader to weigh the slight-positive-deviation reading.

## Two further pre-registration deviations to address

The proposal pre-committed a Bayesian posterior under explicit priors
(`β ~ N(1.15, 0.15²)`, `α ~ N(2, 5²)`, `σ ~ half-Cauchy(1)`), with the
escalation rule "if they disagree by more than 0.03 on either endpoint,
the disagreement is the headline." This is absent from the draft. With
n=198 and residual sd 0.057 the priors will be massively dominated by
the likelihood and the posterior will sit essentially on the OLS
interval, but the *demonstration* of that - and the demonstration
that the pre-registered escalation rule did not fire - is part of what
the piece pre-registered to do. A two-paragraph addition with a
PyMC/brms fit and a single line on Bayesian-vs-bootstrap agreement
closes this.

Similarly, the proposal called for "10,000 phylogenetically-structured
residual resamples." The draft has 10,000 bootstrap resamples but they
are unstructured. The phylogenetically-structured version is roughly:
resample residuals within a clade-defined block rather than i.i.d.,
which gives a more honest CI than either i.i.d. or the
8-cluster superorder approximation. With PGLS available this becomes
less important; without PGLS it is the closest thing to honest
phylogenetic accounting the bootstrap can do.

## Smaller revisions

*The Selker & Carter citation is doing heavy load-bearing work and
should be examined.* The constant-cortical-thickness-fraction
assumption is what underwrites the factor of 4 between β_C and β_I.
Your draft notes that Selker & Carter (1989) "find approximate
constancy in terrestrial mammals over the size range I have," but does
not say how strong that finding is. What was their sample size, mass
range, and CI on the cortical-thickness exponent? If their interval is
wide enough to be consistent with, say, a 0.02 drift in cortical
fraction across four orders of magnitude in mass, then β_I = 4·β_C is
itself only known to within ±0.03 or so on that basis alone, which is
larger than the gap between your point estimate and 4/3.

*The "Mon.Group" cluster definition is opaque.* The draft says "8
superorders" but does not list them. A reader who wants to assess
whether your cluster-bootstrap is a reasonable phylogenetic proxy
needs to know whether the 8 groups are something like Laurasiatheria,
Afrotheria, Euarchontoglires, Xenarthra, Monotremata, Marsupialia, ...
or something else. Name them and report n-per-cluster.

*The "first reading" of the slight excess above 4/3 is speculative and
should be labeled as such more crisply.* Your fall-risk story for
positive allometry is suggestive but not supported by anything in this
analysis. The draft does flag it as one of three readings, but the
prose tilts toward this one. "May or may not" is the right register;
make sure the prose carries that register all the way through.

*Headline-vs-body match.* The lead asserts the data "prefer 4/3 or
slightly steeper." Until the PGLS question is settled, "consistent
with 4/3, possibly slightly above" is the more honest framing. The
"slightly steeper" reading depends on the OLS-bootstrap-vs-PGLS gap
not closing 4/3 back into the interval.

## What I am not asking you to change

The data-source correction in §"A correction to my own proposal"
should stay exactly as it is. Owning the Doube/Christiansen
mis-citation in the body of the piece rather than as a buried erratum
is the right move and is in keeping with how the College has been
asking pieces to handle this kind of thing. The Monte Carlo audit
against realized residual sd is good. The McMahon-as-third-prediction
section is a nice unanticipated win - keep it. The closing section on
what you would publish if the headline went the other way is the
methodological inheritance of the curriculum pieces and reads
correctly.

Bring it back when PGLS is run, the Bayesian fit is in, and the
smaller items are addressed. I expect the next pass to be a short one.

- Henri
