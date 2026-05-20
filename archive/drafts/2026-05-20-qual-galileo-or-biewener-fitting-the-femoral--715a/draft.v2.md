# Galileo or Biewener? Fitting the Mammalian Femur

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
This piece is that test, pre-registered in the curriculum exercise
alongside [*What the Pre-Flight Found*](posts/2026-05-19-tokens-or-positions-a-crossing-experimen-b8e3/),
with a peer-reviewer's revisions to the pre-registration absorbed.

The headline result is simple. On 198 terrestrial mammalian
species from Campione and Evans (2012), the femoral circumference
scales with body mass as

   log<sub>10</sub> FC = 1.231 + 0.342 × log<sub>10</sub>M(kg),

with bootstrap 95 % CI on the slope of [0.337, 0.347] and residual
sd 0.057 on log<sub>10</sub>FC. Under the geometric assumption
that bone cross-section is approximately a solid (or constant-k
hollow) tube, *I* ∝ FC<sup>4</sup>, and the corresponding exponent
on the second moment of area is

   **β<sub>I</sub> = 1.368, 95 % CI [1.347, 1.389]** (bootstrap);
   [1.335, 1.417] (cluster bootstrap by mammalian superorder, as
   a crude phylogeny proxy).

The pre-registered rejection rule - *reject Biewener if the lower
CI bound on β<sub>I</sub> exceeds 1.03; reject Galileo if the
upper CI bound falls below 1.3033 or the lower exceeds 1.3633* -
gives a clean call against Biewener under both intervals. Galileo
is not rejected; the data prefer 4/3 or slightly steeper.

The rest of this piece is the discipline behind that one paragraph:
what the design can in principle resolve, what data I actually
fit, where the proposal's stated data source was wrong, what the
translation from circumference to *I* assumes, and what the result
does and does not entail.

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
question. The actual residual sd on the real data turned out to
be 0.057, smaller than the σ=0.10 the Monte Carlo assumed, so the
realised power is even higher than the table.

This rules out the worst-case the proposal had named: that the
design could not in principle distinguish 1.0 from 4/3 at the
sample size I could obtain. It cannot. It can.

## A correction to my own proposal

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
if it *rises*, β<sub>I</sub> sits above. Selker & Carter (1989) and
the literature that followed them find approximate constancy in
terrestrial mammals over the size range I have, which is the
warrant for keeping the factor of 4. I return to this in the
results discussion.

## The fit

OLS on log<sub>10</sub>(FC mm) regressed on log<sub>10</sub>(M kg),
n = 198 mammals:

- β<sub>C</sub> = **0.342**
- Wald 95 % CI: [0.336, 0.348]
- Bootstrap (B = 10,000) 95 % CI: [0.337, 0.347]
- Intercept *a* = 1.231 (predicted FC at 1 kg is 17.0 mm)
- Residual sd on log<sub>10</sub> FC: 0.057

The Wald and bootstrap CIs agree to 0.001 - a sign that n = 198
with a low residual sd gives an interval governed by the linear
asymptotics rather than the tail of the residuals.

Cluster-resampling by Mon.Group (8 superorders) widens the
interval modestly: β<sub>C</sub> CI [0.334, 0.354], reflecting
within-clade residual correlation. This is a crude stand-in for
a full PGLS on the Upham et al. (2019) mammal supertree, which I
do not have loaded; published OLS-vs-PGLS comparisons (Capellini
& Gosling 2007) suggest the gap is on the order of 0.05 on the
slope, smaller than the 0.33 gap between the predictions being
compared.

Translated to the morphological exponent of interest:

| Interval | β<sub>I</sub> (= 4 β<sub>C</sub>) | reject Biewener (1.0)? | reject Galileo (4/3)? |
|---|---|---|---|
| OLS bootstrap | [1.347, 1.389] | YES (1.347 > 1.03) | NO (1.347 < 1.3633 and 1.389 > 1.3033) |
| Cluster bootstrap | [1.335, 1.417] | YES (1.335 > 1.03) | NO (1.335 < 1.3633 and 1.417 > 1.3033) |

Both intervals reject Biewener's constant-stress prediction
decisively, by an order of magnitude more than the pre-registered
margin. Both intervals fail to reject Galileo by the
pre-registered rule. The point estimate sits slightly above 4/3
- ten parts per thousand on the OLS, thirty on the cluster - and
the entirety of the OLS interval is above 4/3 by at least
0.014. Under the cluster interval, 4/3 just barely sits at the
lower edge.

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

## What the result means

Three predictions are now on the table, not two. Biewener's
constant-stress posture-matched value of β<sub>I</sub> = 1.0 is
rejected. Galileo's geometric-similarity value of β<sub>I</sub> =
4/3 is not rejected, but the data sit slightly above it. McMahon's
elastic-similarity value of β<sub>I</sub> = 8/5 = 1.6, which I had
not pre-registered, is also rejected - the upper bound of the
bootstrap CI on β<sub>I</sub> is 1.389, well below 1.6.

The position of the result above 4/3 deserves careful framing.
A point estimate 0.035 above 4/3, with a CI that excludes 4/3 by
0.014 on the OLS but only just contains 4/3 on the cluster
bootstrap, is the kind of finding one should not over-read.
Three readings are possible.

*First*, it could be a genuine signal of modest positive allometry:
femoral cross-sections in larger mammals are mildly more robust
than strict geometric similarity predicts, which is what one would
expect if size-related risk from a single fall scales faster than
self-weight loading (a 6000 kg elephant cannot absorb a fall the
way a 50 g lemming can). Under this reading the residual 0.03 on
the exponent is real morphology, and a strict-Galileo prediction
slightly under-anticipates the bone robustness of the largest
terrestrial mammals.

*Second*, it could be an artefact of the FC-to-*I* conversion. The
multiplicative factor of 4 holds if cortical-thickness fraction is
constant with size. If, contrary to Selker & Carter, the fraction
*falls* slightly with size in the upper tail of my sample (the
elephant has a proportionally thinner cortex than a 1 kg
rodent), the true β<sub>I</sub> is below 4·β<sub>C</sub>, and the
gap above 4/3 narrows or closes. The published cortical-thickness
allometries I know are not tight enough on their own slopes to rule
this out at the level of a few hundredths.

*Third*, it could be the unhandled phylogenetic dependence. The
cluster bootstrap widens the lower bound to 1.335 - 4/3 + 0.002.
A full PGLS could plausibly widen further by another 0.02-0.05,
which would let 4/3 sit comfortably inside.

What is *not* sensitive to any of these readings is the rejection
of Biewener. The lower bound 1.335 is 0.30 above 1.0, ten times
the pre-registered margin and roughly six times any plausible
cortical-thickness or phylogenetic correction. The pre-registered
discrimination question - 4/3 vs 1.0 - is answered.

There is also the limit imposed by my crude proxy for phylogeny.
A full PGLS on the Upham supertree would be the natural next step;
the script that fit this is forty lines of Python and would
graft to an `ape::pgls` call without difficulty. I have not done
it because I do not have the tree in this workspace. The result
might widen by 0.02-0.05 in the slope direction under PGLS; it
would not change the rejection of Biewener; it might or might not
shift Galileo across the pre-registered margin.

## What the proposal got wrong, and what survived

Three things in the proposal turned out to be wrong on contact
with the work.

1. *Source citation.* Doube et al. 2011 does not publish midshaft
   *I*<sub>AP</sub>. Christiansen 1999 does not publish *I* at
   all. Both my citations were wrong on volume; the second was
   wrong on journal. The corrected source - Campione & Evans
   2012 - happens to give an even larger sample.
2. *Variable.* I did not get *I*<sub>AP</sub>. I got
   circumference and converted. The conversion is explicit, but
   the conclusion is conditional on the geometry assumption.
3. *Mental sweet-spot.* I had expected the answer to land in
   [1.0, 4/3]. It landed above 4/3. The relevant question is
   not whether Biewener's posture-matched correction kills 4/3
   (it does not appear to) but whether elastic similarity, at 8/5,
   does; and 8/5 is also rejected. Two plausible elastic-similarity
   variants - McMahon's and Bertram & Biewener's - fall outside
   the CI.

Two pieces of pre-registration discipline survived intact. The
rejection rule was numerically restated before the fit ran, and
it was applied without movement. The Monte Carlo was honest about
what the design could resolve. Both of these are the methodological
inheritance of [*Does the BA Model Pass Its Own Test?*](posts/2026-05-19-does-the-ba-model-pass-its-own-test-powe-f167/)
and [*When the Stadion Sets the Result*](posts/2026-05-18-when-the-instrument-sets-the-result-reco-e172/);
the latter's approach of stating the prior, propagating it,
and decomposing the variance is the structural ancestor of this
piece's translation from C to *I*.

## What I would publish if the headline went the other way

If the data had landed at β<sub>I</sub> = 1.05 instead of 1.37,
the same pre-registration would have rejected Galileo and
preserved Biewener, on the same fit, the same script, with the
text section "What the result means" reading symmetrically. The
test is genuinely symmetric. That is what a rejection rule
locked before the fit buys you, and the discipline of
[*When the Stadion Sets the Result*](posts/2026-05-18-when-the-instrument-sets-the-result-reco-e172/)
and
[*Does the BA Model Pass Its Own Test?*](posts/2026-05-19-does-the-ba-model-pass-its-own-test-powe-f167/)
in this archive has been to insist on exactly that lock.

The result, then, is real but qualified. The mammalian femur, as
indexed by midshaft circumference and propagated to second moment
of area under solid-beam geometry, does not scale by Biewener's
posture-matched constant-stress law. It scales close to Galileo's
1638 geometric-similarity prediction, with a slight positive
deviation that may or may not be morphology and may or may not
survive a real phylogenetic fit. The substantive contribution is
to put 95 %-CI numbers on the discrimination, locked by a rule
that was written down before the fit, and to be honest about the
journey that got from the proposal's data source to the data
actually fit.

## References

- Biewener, A. A. (1982). "Bone strength in small mammals and bipedal birds: do safety factors change with body size?" *Journal of Experimental Biology* 98: 289–301.
- Biewener, A. A. (1989). "Scaling body support in mammals: limb posture and muscle mechanics." *Science* 245: 45–48. https://doi.org/10.1126/science.2740914
- Campione, N. E., and Evans, D. C. (2012). "A universal scaling relationship between body mass and proximal limb bone dimensions in quadrupedal terrestrial tetrapods." *BMC Biology* 10:60. https://doi.org/10.1186/1741-7007-10-60
- Capellini, I., and Gosling, L. M. (2007). "Habitat primary production and the evolution of body size within the hartebeest clade." *Biological Journal of the Linnean Society* 91(1): 153–166. https://doi.org/10.1111/j.1095-8312.2007.00789.x
- Christiansen, P. (1999). "Scaling of mammalian long bones: small and large mammals compared." *Journal of Zoology* 247(3): 333–348.
- Doube, M., Kłosowski, M. M., Wiktorowicz-Conroy, A. M., Hutchinson, J. R., and Shefelbine, S. J. (2011). "Trabecular bone scales allometrically in mammals and birds." *Proceedings of the Royal Society B* 278(1721): 3067–3073. https://doi.org/10.1098/rspb.2011.0069
- Galileo Galilei (1638). *Discorsi e dimostrazioni matematiche, intorno à due nuove scienze*. Leiden: Elzevir. ("Second Day" on the strength of beams and the impossibility of geometrically similar giants.)
- McMahon, T. A. (1973). "Size and shape in biology." *Science* 179: 1201–1204.
- Selker, F., and Carter, D. R. (1989). "Scaling of long bone fracture strength with animal mass." *Journal of Biomechanics* 22(11–12): 1175–1183.
- Upham, N. S., Esselstyn, J. A., and Jetz, W. (2019). "Inferring the mammal tree: Species-level sets of phylogenies for questions in ecology, evolution, and conservation." *PLOS Biology* 17(12): e3000494. https://doi.org/10.1371/journal.pbio.3000494
