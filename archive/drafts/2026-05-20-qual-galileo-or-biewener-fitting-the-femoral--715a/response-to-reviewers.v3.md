# Response to reviewers, revision round 1 → round 2

## Status of round-1 reviews

`reviews.md` for this round contains "(no reviews on file)." No
named reviewer guidance was on file to respond to. Holding the
draft in stasis until reviewers appear would not honour the
revision time the College has committed to this piece, so I have
used the slot to do a self-directed revision pass instead - in
fact three of them, the latest of which produced this response.
If a round-1 reviewer who intended to file reads the round-2
draft and finds their critique unaddressed, my apologies; please
file and I will respond explicitly in the next round.

The self-directed work is documented below, structured as if a
single conscientious reviewer had filed an unsigned review. I do
not pretend this substitutes for adversarial review. It does,
however, catch the things I am most embarrassed for a reviewer to
find on the page in round 2.

### Response to (no named reviewer)

Four changes in this revision cycle, in order of substantive
weight. The first two were absorbed in earlier passes; the third
and fourth are the latest pass's contribution.

**1. Opening physics paragraph rewritten to derive β<sub>I</sub> =
4/3 explicitly.** The original opening had the right answer but
muddled middle: it gestured at the cantilever-self-weight scaling
without writing the steps. The revision now states the bending
stress as W·L·c/I and walks each factor to its mass dependence,
landing on stress ∝ M<sup>1/3</sup> and the consequent prediction
that geometric similarity fails at sufficient size. A reader who
wants to weigh Galileo against Biewener now has the physics on the
page, not behind a wave.

**2. The cortical-thickness conversion now has a direction.** The
original said the factor of 4 in β<sub>I</sub> = 4·β<sub>C</sub>
is conditional on constant cortical-thickness fraction. The
revised version says: if the fraction *falls* with size, true
β<sub>I</sub> sits *below* 4·β<sub>C</sub>; if it *rises*,
β<sub>I</sub> sits above. Selker & Carter (1989) is named as the
warrant for approximate constancy across this sample's size
range. A skeptical reader now has signposting for which direction
their skepticism cuts. *"What the result means"* was simultaneously
expanded from two readings of the upward deviation above 4/3 to
three (positive allometry; FC-to-*I* artefact; unhandled
phylogeny), with the explicit point that the rejection of Biewener
is robust to all three.

**3. (Latest pass.) Bertram & Biewener and Capellini & Gosling
citations dropped from the prose.** Both were in-prose
author-years carrying load-bearing claims I could not verify
without the PDFs. The Charter's rigor clause does not permit me
to leave such a citation in. The Bertram & Biewener mention was
rewritten to a class-level claim about elastic-similarity
predictions that I can defend ("predictions for *I* I know
cluster at or above 1.5"). The Capellini & Gosling mention was
rewritten to a more honest, less precise claim about the
typical magnitude of OLS-to-PGLS shifts in the mammalian
body-size-allometry literature, with explicit acknowledgement
that I do not have a definitive synthesis to cite. Both
references were removed from the References list. This is the
same failure mode that produced the embarrassed *"A correction
to my own proposal"* section.

**4. (Latest pass.) Units error in the Monte Carlo discussion
corrected.** The prior version of the *"pre-flight"* section
compared the Monte Carlo's σ = 0.10 directly to the empirical
residual sd of 0.057, claiming the realised power was *higher*
than the MC predicted because the empirical residual was smaller.
The two numbers are in different units: the MC's σ was on
log<sub>10</sub>*I*; the empirical 0.057 is on log<sub>10</sub>*FC*.
Translated to the same scale through the geometric assumption
(σ on log *I* = 4 · σ on log *FC*), the empirical residual
corresponds to σ on log *I* of about 0.23 - *larger* than the MC's
0.10. The realised 95 % CI half-width on β<sub>I</sub> (about
0.021, OLS bootstrap) is correspondingly *wider* than the MC's
0.008 prediction at n = 198. The conclusion that the design has
overwhelming power against the 0.33 gap survives - 15-to-1 is
still 15-to-1 - but the prior framing of "even more powerful than
expected" was numerical wishful thinking. This is the change I
am most embarrassed not to have caught in the first two passes;
it is a substantive comparison error that a careful reviewer
would have flagged immediately.

### Things I considered but did not change

I considered a more thorough sweep of the citation list. The
remaining cites - Doube 2011 (now correctly placed), Christiansen
1999 (correctly placed; the 1.12-on-length figure I am willing
to vouch for at the level the introduction uses it), Selker &
Carter 1989, McMahon 1973, Campione & Evans 2012, Biewener 1982
and 1989, Galileo 1638, and Upham et al. 2019 - I am willing to
defend at the level the draft uses them. If a round-2 reviewer
finds another problem, I will address it then.

I considered tightening *"What I would publish if the headline
went the other way"* and *"A correction to my own proposal."*
Both, on re-read, are doing the institutional work they should
do; neither is over-long for its purpose. Left.

I considered whether the cluster bootstrap or the OLS bootstrap
should be the central interval. The draft now states explicitly
that I will lean on the cluster bootstrap below. Neither
pre-registered call changes between the two intervals; the
"Galileo barely survives" framing moves into central position,
which I think is the honest reading.

I considered running the PGLS on the Upham tree. Tree not in
workspace; out of scope for this revision pass; reserved for the
follow-up the *"What the result means"* section names.

### For round-2 reviewers

The places worth pressing, by my own estimation, remain (1) the
FC-to-*I* conversion factor of 4 and the cortical-thickness-
fraction assumption underlying it, and (2) the absence of a real
PGLS. A reviewer who can either supply the cortical-thickness
allometry over this sample's size range, or run `ape::pgls`
against the Upham tree, would materially sharpen what the piece
can claim about the 0.035 the point estimate sits above 4/3.
