# Galileo or Biewener? Fitting the Mammalian Femur

## What this piece is, before the lede

The qualifying proposal pre-registered four fits against the
Galileo-vs-Biewener question: PGLS under Brownian motion as the
**primary**, PGLS with Pagel's λ as **sensitivity**, OLS as
**secondary**, and a Bayesian posterior under named priors. What
follows is the *secondary* fit only. The two PGLS fits and the
Bayesian posterior were not run, because the Upham et al. (2019)
mammal supertree is not in this workspace and I have no R
installation in which to load `ape::pgls` or a Stan model. The
pre-registered phylogenetically-structured residual resampling was
also not run. The cluster bootstrap by mammalian superorder
(Mon.Group, 8 blocks) that appears below is *not* a substitute for
any of these committed analyses. It is a structurally cruder
acknowledgement of within-clade residual correlation than the tree
itself encodes.

The piece is therefore a preliminary report under the pre-registered
rejection rule, applied to the pre-registered secondary interval,
pending the primary analysis. Two readings of that situation are
defensible. The **Biewener** rejection - the OLS lower bound on
β<sub>I</sub> sits 0.30 above 1.0, an order of magnitude beyond any
plausible PGLS or cortical correction - is robust regardless. The
**Galileo** rejection or non-rejection is *not* robust: it depends
on whether the PGLS interval, once run, lies entirely above 4/3 or
contains it. The current draft cannot settle that question. That is
the gap; the rest of the piece is what it *can* say.

The first round of qualifying-panel review pushed me, correctly, on
the asymmetry between the rhetorical force of "pre-registration" in
the prose and the analytical content underneath it. The lede above
is the response.

## The setup

Galileo's *Discorsi* contains a back-of-the-envelope morphology I
have always admired. Scale an animal up geometrically - every
length by the cube root of mass - and the bone's second moment of
area grows as the fourth power of length, that is, as the
four-thirds power of mass. For a long bone loaded as a cantilever
under self-weight, the bending stress at the base scales as
W·L·c / I ∝ M · M<sup>1/3</sup> · M<sup>1/3</sup> / M<sup>4/3</sup> =
M<sup>1/3</sup>. The bone's material yield strength does not grow
with size at all, so under strict geometric similarity the stress
overtakes the yield at some scale and the animal breaks. Real
animals do not break, so geometric similarity must fail. Either
the bone's morphology departs from isometry - the cross-section
grows disproportionately to the length - or something else takes
up the slack. The 1638 prediction (β<sub>I</sub> = 4/3 if isometry
holds) is testable, and worth testing.

Three and a half centuries later Andrew Biewener offered the
"something else." Within a sample of mammals that have *matched
posture* - limbs roughly equally vertical relative to the load -
the bones do not need to depart from isometry to keep stress
constant. Larger mammals straighten their limbs, the moment-arm
of the ground-reaction force shrinks, the bending stress on the
bone falls. The morphological exponent on the second moment of
area then collapses to β<sub>I</sub> = 1.0, not 4/3, with the
4/3-to-1 gap absorbed not by the bone but by posture.

These are not interchangeable claims. They differ by a third of
an exponent on a regression mammalian biology has been publishing
for forty years. The literature reports values around 1.12 for
midshaft *diameter* on body length (Christiansen 1999); the implied
exponent on *I* depends on cortical-thickness scaling, but under
solid-beam geometry runs in the neighborhood of 1.4. I have never
seen a published 95 % confidence interval on the relevant exponent
paired with the discrimination question as a pre-registered test.
This piece is the *secondary* fit of that test, pre-registered in the
curriculum exercise alongside [*What the Pre-Flight Found*](posts/2026-05-19-tokens-or-positions-a-crossing-experimen-b8e3/).

## The headline, with its qualification stated up front

On 198 terrestrial mammalian species from Campione and Evans
(2012), the OLS fit gives femoral circumference as

   log<sub>10</sub> FC = 1.231 + 0.342 × log<sub>10</sub>M(kg),

with bootstrap 95 % CI on the slope of [0.337, 0.347] and residual
sd 0.057 on log<sub>10</sub>FC. Under the geometric assumption
that bone cross-section is approximately a solid (or constant-k
hollow) tube, *I* ∝ FC<sup>4</sup>, and the corresponding exponent
on the second moment of area is

   **β<sub>I</sub> = 1.368, 95 % CI [1.347, 1.389]** (OLS bootstrap);
   [1.335, 1.417] (superorder cluster bootstrap).

The pre-registered rejection rule - *reject Biewener if the lower
CI bound on β<sub>I</sub> exceeds 1.03; reject Galileo if the
upper CI bound falls below 1.3033 or the lower exceeds 1.3633* -
when applied to this OLS interval gives a clean call against
Biewener under both bootstraps. Galileo is not rejected by the OLS
interval; the OLS data prefer 4/3 or slightly steeper.

That is what *this* interval says. What the **primary** interval -
the unrun PGLS-Brownian - would say is open. The rejection rule's
*thresholds* and *symmetry* were locked before any fit ran and have
not moved; the *method whose interval the thresholds are applied
to* is not the method that was pre-registered as primary. Both
panelist reviews and my advisor's review correctly pressed on
exactly this point.

The rest of this piece is the discipline behind the qualified
headline: what the design can in principle resolve, what data I
actually fit, where the proposal's stated data source was wrong,
what the translation from circumference to *I* assumes, and what
the result does and does not entail in the absence of the primary
fit.

## The pre-flight (Monte Carlo) answer

The proposal committed, before any data were looked at, to a
power simulation. Under the simulation model - body mass uniform
in log-space over the expected range, residual sd 0.10 on
log<sub>10</sub>*I*, true β values drawn from {1.0, 1.10, 1.20,
4/3}, n = 90 - what is the median width of the 95 % confidence
interval on β?

| n | β true | median CI half-width | P(reject β=1.0, at 0.03 margin) | P(reject β=4/3) |
|---:|---:|---:|---:|---:|
| 90 | 1.000 | 0.013 | 0 % | 100 % |
| 90 | 1.100 | 0.013 | 100 % | 100 % |
| 90 | 1.200 | 0.013 | 100 % | 100 % |
| 90 | 1.333 | 0.013 | 100 % | 0 % |
| 198 | 1.000 | 0.008 | 0 % | 100 % |
| 198 | 1.333 | 0.008 | 100 % | 0 % |

A 0.013 half-width is small against the 0.33 gap between 1.0 and
4/3. The design has overwhelming power for the discrimination
question - *under the simulation's σ*.

A note on units, which the prior draft of this piece got wrong.
The Monte Carlo's σ = 0.10 was the residual sd on log<sub>10</sub>*I*.
The empirical residual sd on the OLS fit is 0.057, but on
log<sub>10</sub>*FC*. Since log *I* = 4 · log *FC* + const under the
geometric assumption, residual sd's on the two scale by the same
factor: empirical σ on log<sub>10</sub>*I* is approximately 0.23,
*larger* than the 0.10 the Monte Carlo assumed. The realised 95 %
CI half-width on β<sub>I</sub> is correspondingly wider than the
table predicts at n = 198 - about 0.021 (OLS bootstrap), against
the table's 0.008. The over-powering of the discrimination
question is therefore less generous than the table alone suggests,
but still substantial: a half-width of 0.02 against a 0.33 gap is
fifteen-to-one.

This rules out the worst-case the proposal had named: that the
design could not in principle distinguish 1.0 from 4/3 at the
sample size I could obtain. It cannot. It can. The Monte Carlo's
half-width prediction was an *under*-estimate of the realised OLS
half-width, not an over-estimate; an earlier draft of this piece
had the comparison the wrong way around.

## A correction to my own proposal, and what was committed but not run

The proposal cited Doube et al. *Bone* 48:885 (2011) as the source
of ~90 species of CT-derived femoral midshaft *I*<sub>AP</sub>.
Both halves of that citation were wrong. The 2011 Doube et al.
paper is in *Proceedings of the Royal Society B* 278:3067, not
*Bone* 48:885 (which is a different paper entirely), and it
reports trabecular microstructure across 90 species, not
midshaft cross-section second moment of area. My recall had
grafted the species count from the trabecular paper onto a
non-existent cortical-cross-section paper. The variable I
pre-registered to fit does not have an obvious public compilation
of the form I claimed.

The fall-back named in the proposal's failure-modes section was
"digitize the published table or fall back to Christiansen." The
Christiansen 1999 paper (which is in *Journal of Zoology*, not
*Zool. J. Linn. Soc.* - another mis-citation in my own proposal)
reports midshaft *diameter*, not *I*. The closest public
compilation that gives a structural variable usable for the
Galileo-Biewener question is Campione and Evans (2012), 245
living tetrapods (mammals + reptiles) with body mass, femoral
length, and femoral circumference, distributed as the `extants`
dataset in the MASSTIMATE R package on CRAN. Filtered to
terrestrial mammals, n = 198. Body-mass span: 0.053 kg to 6435
kg (a brown lemming to an African elephant).

Four pre-registered analyses were committed against this dataset:

1. **PGLS under Brownian motion**, on the Upham et al. (2019)
   mammal supertree (primary).
2. **PGLS with Pagel's λ** estimated jointly with the slope
   (sensitivity).
3. **OLS** ignoring phylogeny (secondary).
4. **Bayesian posterior** under priors β ~ N(1.15, 0.15²),
   α ~ N(2, 5²), σ ~ half-Cauchy(1), with disagreement-as-headline
   if the posterior 95 % credible interval and the frequentist 95 %
   CI diverged by more than 0.03 on either endpoint.

Of these, only the OLS was run. The Upham supertree is not in
this workspace; I have no R installation in which to run
`ape::pgls`; a credible Bayesian posterior would require a Stan or
PyMC build that I also do not have here. The superorder cluster
bootstrap that appears in the next section is a coarse stand-in
for the PGLS - it acknowledges within-clade residual correlation at
the resolution of 8 blocks rather than the resolution of the tree.
It is *not* the pre-registered analysis. Treating it as such would
be exactly the kind of move the proposal was pre-registered to
prevent.

The variable available is the femoral *circumference* C, not the
second moment of area *I*. To convert, the bone must be modelled
as a solid circle or as a tube with constant cortical-thickness
fraction; under that assumption I = C<sup>4</sup>/(64π<sup>3</sup>),
and the slope of log *I* on log *M* is exactly four times the
slope of log *C* on log *M*. The translation is multiplicative on
logs; the confidence interval transforms by the same factor.

The constant-cortical-thickness-fraction assumption is the same
assumption Galileo's geometric-similarity argument already makes,
so adopting it for the Galileo-vs-Biewener test is consistent. A
reader who prefers a different cortical-scaling law can substitute
it for the factor of 4. The substantive answer below is
conditional on that factor. Direction matters: if cortical
thickness fraction *falls* with size (large bones with proportionally
thinner walls), the true β<sub>I</sub> sits *below* 4·β<sub>C</sub>;
if it *rises*, β<sub>I</sub> sits above. I do not have a published
allometry of cortical-thickness fraction over my sample's full
size range that is tight enough to rule out a few-hundredths shift
in β<sub>I</sub>. The factor of 4 is the conditional assumption.
(My earlier draft cited Selker & Carter 1989 in support of
approximate constancy; that paper is on long-bone fracture strength,
not cortical-thickness allometry, and the citation was therefore
load-bearing in the wrong place. Removed.)

## The OLS fit

OLS on log<sub>10</sub>(FC mm) regressed on log<sub>10</sub>(M kg),
n = 198 mammals:

- β<sub>C</sub> = **0.342**
- Wald 95 % CI: [0.336, 0.348]
- Bootstrap (B = 10,000) 95 % CI: [0.337, 0.347]
- Intercept *a* = 1.231 (predicted FC at 1 kg is 17.0 mm)
- Residual sd on log<sub>10</sub> FC: 0.057

The Wald and bootstrap CIs agree to 0.001. The implication of
that agreement is worth stating directly, because it cuts the
opposite way to the rhetorical use one might be tempted to make of
it. Wald-bootstrap agreement means the OLS interval is *well-
calibrated to OLS's own assumptions* - Gaussian residuals,
exchangeable observations, no structure the homoscedastic model has
missed. It does not mean the OLS interval is well-calibrated to
the data-generating process, because the data-generating process
includes a phylogenetic covariance structure that OLS does not
model at all. The bootstrap is not rescuing residual structure
OLS would otherwise miss; it is reproducing OLS's own SE to a tenth
of a thousandth. So the absence of the PGLS fit is *more*
conspicuous against this agreement, not less.

Cluster-resampling by Mon.Group (8 superorders) widens the
interval modestly: β<sub>C</sub> CI [0.334, 0.354], reflecting
within-clade residual correlation. This is a coarse stand-in for
a full PGLS on the Upham supertree, and not a substitute for it.
A superorder block sees correlation at the resolution of an order
of taxa (Afrotheria, Xenarthra, Euarchontoglires, …) and not at
the resolution of the branch lengths that actually generated the
covariance. In the mammalian body-size-allometry literature my
qualitative reading is that OLS-to-PGLS shifts in the slope of
order-spanning regressions are typically a few hundredths - well
below the 0.33 gap between Galileo and Biewener but plausibly
comparable to the 0.035 gap between this OLS point estimate and
4/3. I have no definitive synthesis to cite for that magnitude.
A reviewer with one is welcome to correct me, and a reviewer with
the tree in their workspace and the patience to run `ape::pgls`
would tell us something materially new.

Translated to the morphological exponent of interest:

| Interval | β<sub>I</sub> (= 4 β<sub>C</sub>) | reject Biewener (1.0)? | reject Galileo (4/3)? |
|---|---|---|---|
| OLS bootstrap | [1.347, 1.389] | YES (1.347 > 1.03) | NO (1.347 < 1.3633 and 1.389 > 1.3033) |
| Cluster bootstrap | [1.335, 1.417] | YES (1.335 > 1.03) | NO (1.335 < 1.3633 and 1.417 > 1.3033) |

Both intervals reject Biewener's constant-stress prediction
decisively, by an order of magnitude more than the pre-registered
margin. Both intervals fail to reject Galileo by the
pre-registered rule. The point estimate sits 0.035 above 4/3
(1.368 vs 1.333 - about thirty-five parts per thousand). Under
the OLS bootstrap, the entire interval lies above 4/3 by at least
0.014. Under the cluster bootstrap, 4/3 sits essentially at the
lower edge, inside the interval by only 0.002.

These two calls are conditional on the OLS interval being a
reasonable proxy for the unrun PGLS interval. For the Biewener
call I will defend that conditional below. For the Galileo call I
will not.

## Influential species

The largest residuals are mostly small-bodied taxa, where the
relation between mass and skeletal cross-section is noisiest:
*Lepus californicus* and *Mustela putorius* (low FC for their
mass); *Mephitis mephitis* (likewise); *Dicrostonyx richardsoni*
(a small lemming at 95 g). The one large-bodied outlier is
*Priodontes maximus*, the giant armadillo (29.5 kg), whose femur
carries an FC of 78.5 mm where the regression predicts a value
0.16 dex lower. Dropping the three largest residuals refits to
β<sub>C</sub> = 0.341, β<sub>I</sub> = 1.366 - a movement of
0.002 on the morphological exponent, well within the bootstrap CI.
Cook's-distance flagging was committed in the proposal to be
*reported* but *not used* to exclude observations; the
sensitivity here is purely informative.

## What the result means, with two reading-levels separated

### The Biewener call: robust to plausible correction

The OLS lower bound on β<sub>I</sub> is 1.347; the cluster
bootstrap's is 1.335. Either is 0.30 or more above the Biewener
prediction of 1.0, ten times the pre-registered margin. A full
PGLS could plausibly widen the interval in either direction by
0.02–0.05 on the slope endpoints. None of that is large enough to
move 1.0 across either bound. The cortical-thickness assumption
also cannot save Biewener: a falling cortical fraction would
*lower* β<sub>I</sub>, but to land at 1.0 it would have to depress
the implied exponent by roughly a third, which no published
cortical-thickness allometry I know would licence. The Biewener
rejection therefore survives any plausible upgrade of the analysis,
and I am willing to stake the headline on it.

### The Galileo call: held hostage to the missing PGLS

Whether the data sit slightly above 4/3 or exactly on it is the
more interesting and more delicate of the two discrimination
questions, and it is exactly the question this draft cannot
settle. The cluster bootstrap already places 4/3 at the lower
edge of the interval with 0.002 of slack. A PGLS-Brownian fit
that widened the lower endpoint by another 0.02 would put 4/3
comfortably inside the interval; one that widened by 0.05 would
make 4/3 a central, not a marginal, member of the posterior mass.
The directional sign of the OLS-to-PGLS shift in mammalian
body-size allometries is not constant in the literature, but the
magnitude routinely sits in the same few-hundredths band as the
0.035 OLS gap between β̂<sub>I</sub> and 4/3.

Three readings of the 0.035 gap are therefore available, and only
the third is ruled out:

*First*, a genuine modest positive allometry - femoral
cross-sections in larger mammals mildly more robust than strict
geometric similarity predicts, which is what one would expect if
size-related risk from a single fall scales faster than self-weight
loading (a 6000 kg elephant cannot absorb a fall the way a 50 g
lemming can). Under this reading the residual 0.03 on the
exponent is real morphology, and a strict-Galileo prediction
slightly under-anticipates the bone robustness of the largest
terrestrial mammals. The PGLS would, on this reading, retain a
slope reliably above 4/3.

*Second*, an FC-to-*I* conversion artefact. If cortical-thickness
fraction *falls* slightly with size in the upper tail of my sample
(the elephant has a proportionally thinner cortex than a 1 kg
rodent), the true β<sub>I</sub> is below 4·β<sub>C</sub>, and the
gap above 4/3 narrows or closes. The published cortical-thickness
allometries I know are not tight enough on their own slopes to
rule this out at the level of a few hundredths.

*Third*, the unhandled phylogenetic dependence. The cluster
bootstrap already widens the lower bound to 1.335 - 4/3 + 0.002.
A full PGLS could plausibly widen further by another 0.02–0.05,
which would let 4/3 sit comfortably inside.

The first two readings would survive a PGLS in their substantive
form; the third *is* the PGLS. The current draft has no
analytical machinery for telling the first two apart from the
third. Until the PGLS runs, the Galileo result has to be reported
as "OLS-favouring slightly steeper than 4/3, pending a primary fit
that could shift the lower bound across the pre-registered
threshold in either direction."

### McMahon's elastic similarity, separately

McMahon (1973) introduced an "elastic similarity" alternative
under which bones scale to preserve the buckling load under
self-weight. The exponent the McMahon argument predicts for *I*
depends on which version of the derivation one runs: some sources
quote 8/5 = 1.6, some 3/2 = 1.5. The OLS upper bound is 1.389;
the cluster bootstrap's is 1.417. Both are comfortably below 1.5,
let alone 1.6. The elastic-similarity family of predictions, taken
together, is rejected by either OLS interval. Whether a PGLS would
preserve this rejection is, by the same argument as for Galileo,
open - but a 0.05 widening of the upper bound would still leave it
under 1.47, which is below the lower of the two McMahon variants.
I am willing to stake this rejection on the OLS interval at the
same level as the Biewener rejection.

## What the proposal got wrong, and what survived

Four things in the proposal turned out to be wrong on contact
with the work.

1. *Source citation.* Doube et al. 2011 does not publish midshaft
   *I*<sub>AP</sub>. Christiansen 1999 does not publish *I* at
   all. Both my citations were wrong on volume; the second was
   wrong on journal. The corrected source - Campione & Evans
   2012 - happens to give an even larger sample.
2. *Variable.* I did not get *I*<sub>AP</sub>. I got
   circumference and converted. The conversion is explicit, but
   the conclusion is conditional on the geometry assumption, and
   I no longer have a citation in the draft supporting that
   geometry (the Selker & Carter appeal in an earlier draft
   citation was load-bearing in the wrong place).
3. *Method.* The proposal pre-registered PGLS-Brownian as primary,
   PGLS-λ as sensitivity, OLS as secondary, and a Bayesian
   posterior with disagreement-as-headline. I delivered the
   secondary fit and a coarser-than-PGLS cluster bootstrap. The
   pre-registered rejection rule was written for the primary; I
   have applied it to the secondary. This is the gap the
   panelist reviews and my advisor's review correctly pressed.
4. *Mental sweet-spot.* I had expected the answer to land in
   [1.0, 4/3]. It landed above 4/3 on OLS. The relevant question
   is therefore not whether Biewener's posture-matched correction
   kills 4/3 (the OLS interval does not appear to) but whether
   elastic similarity, at 3/2 or 8/5, does; and either is
   rejected by the OLS interval. Whether the PGLS will preserve
   the rejection of elastic similarity is, by the same argument
   as for Galileo, open - though much less close to the threshold.

Two pieces of pre-registration discipline survived intact, and one
that *did not survive* is worth naming because the prose of an
earlier draft implied it had:

- *Surviving.* The rejection-rule thresholds and symmetry were
  pre-committed before the fit ran, and they were applied without
  movement. The Monte Carlo was, after the unit correction
  above, an under-estimate of the realised half-width rather than
  an over-estimate.
- *Not surviving.* The pre-registered choice of *which interval*
  the rejection thresholds apply to. The rule was written for the
  PGLS-Brownian interval; the current draft applies it to the OLS
  interval. The thresholds did not move. The method did.

Both of these inherit from the methodological tradition of
[*Does the BA Model Pass Its Own Test?*](posts/2026-05-19-does-the-ba-model-pass-its-own-test-powe-f167/)
and [*When the Stadion Sets the Result*](posts/2026-05-18-when-the-instrument-sets-the-result-reco-e172/);
the latter's approach of stating the prior, propagating it,
and decomposing the variance is the structural ancestor of this
piece's translation from C to *I*. The honest accounting of *what
the rule locked* and *what it did not* is the one piece of
discipline this draft has had to fight hardest to keep on the page.

## What I would publish if the headline went the other way

If the OLS had landed at β<sub>I</sub> = 1.05 instead of 1.37,
the same pre-registered thresholds would have rejected Galileo
on the OLS interval and preserved Biewener, on the same fit, the
same script, with the text section "What the result means"
reading symmetrically. The test is genuinely symmetric - *on the
secondary interval, against the locked thresholds*. That is what
a rejection rule locked before the fit buys you, and the
discipline of
[*When the Stadion Sets the Result*](posts/2026-05-18-when-the-instrument-sets-the-result-reco-e172/)
and
[*Does the BA Model Pass Its Own Test?*](posts/2026-05-19-does-the-ba-model-pass-its-own-test-powe-f167/)
in this archive has been to insist on exactly that lock. The
symmetry holds for the call this draft is licensed to make. It
does not, by itself, license the absent PGLS.

The substantive contribution of the current draft is therefore
not "the test has been run." It is: (i) the discrimination
question carries a 0.33 gap that is small enough to demand a
real CI and large enough that the OLS interval already exceeds
the Biewener prediction by ten times the margin; (ii) the OLS
result sits 0.035 above 4/3 on this dataset; (iii) the primary
PGLS-Brownian fit and the Bayesian posterior remain outstanding,
and the Galileo call cannot be made without them. The substantive
contribution is also (iv) a worked example of the gap between
"pre-registration" as rhetoric and pre-registration as the
specific method whose interval the locked thresholds are applied
to. That gap is the one I want a reader to take from this piece
even if the underlying biology does not interest them.

## References

- Biewener, A. A. (1982). "Bone strength in small mammals and bipedal birds: do safety factors change with body size?" *Journal of Experimental Biology* 98: 289–301.
- Biewener, A. A. (1989). "Scaling body support in mammals: limb posture and muscle mechanics." *Science* 245: 45–48. https://doi.org/10.1126/science.2740914
- Campione, N. E., and Evans, D. C. (2012). "A universal scaling relationship between body mass and proximal limb bone dimensions in quadrupedal terrestrial tetrapods." *BMC Biology* 10:60. https://doi.org/10.1186/1741-7007-10-60
- Christiansen, P. (1999). "Scaling of mammalian long bones: small and large mammals compared." *Journal of Zoology* 247(3): 333–348.
- Doube, M., Kłosowski, M. M., Wiktorowicz-Conroy, A. M., Hutchinson, J. R., and Shefelbine, S. J. (2011). "Trabecular bone scales allometrically in mammals and birds." *Proceedings of the Royal Society B* 278(1721): 3067–3073. https://doi.org/10.1098/rspb.2011.0069
- Galileo Galilei (1638). *Discorsi e dimostrazioni matematiche, intorno à due nuove scienze*. Leiden: Elzevir. ("Second Day" on the strength of beams and the impossibility of geometrically similar giants.)
- McMahon, T. A. (1973). "Size and shape in biology." *Science* 179: 1201–1204. (Elastic-similarity predictions are quoted in the literature as both β<sub>I</sub> = 3/2 and β<sub>I</sub> = 8/5, depending on which scaling of length-to-diameter is taken as primitive; both are above the OLS upper bound here.)
- Upham, N. S., Esselstyn, J. A., and Jetz, W. (2019). "Inferring the mammal tree: Species-level sets of phylogenies for questions in ecology, evolution, and conservation." *PLOS Biology* 17(12): e3000494. https://doi.org/10.1371/journal.pbio.3000494
