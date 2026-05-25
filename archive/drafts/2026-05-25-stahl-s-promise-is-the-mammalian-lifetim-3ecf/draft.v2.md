# A Billion Heartbeats, Plus or Minus a Factor of Twenty

The mammalian heart, the folklore runs, beats about a billion times
across a lifetime, and it does so whether the heart belongs to a
shrew or to a blue whale. The shrew gets through its billion in
two years at eight hundred beats per minute; the whale takes
ninety years at ten. The product, $H = f_H \cdot L_{\max}$, is held
to be a mass-invariant of mammalian physiology, a downstream
consequence of two more famous scaling laws - Stahl's $f_H \propto
M^{-1/4}$ and Calder's $L_{\max} \propto M^{+1/4}$ - whose
exponents are deliberately equal and opposite. Multiply two
quarter-power laws of opposite sign and what survives is mass
independence. The claim is repeated in textbooks, in popular
science, and in the West–Brown–Enquist scaling literature, often
as if it were derived rather than measured.

It is measured. It has been measured very few times, on small
samples, without explicit treatment of the uncertainty in either
input exponent. This piece refits the lifetime-heartbeat product
on a canonical 22-species sample, reports the central estimate
with confidence intervals, and asks where the residuals sit. The
answer is more modest than the folklore: on this sample the data
cannot adjudicate between strict mass-invariance and a modest
negative slope, the central tendency clusters near 1.4 billion
rather than 1, and the residuals do most of their work along the
phylogenetic axis rather than the mass axis.

## The algebra and what it predicts

If $f_H = A_1 M^{a}$ and $L_{\max} = A_2 M^{b}$, then

$$H = A_1 A_2 \cdot M^{a+b},$$

so the slope of $\log H$ on $\log M$ is the sum of the two input
slopes. The "billion-heartbeat" claim is the statement $a + b
\approx 0$. The standard derivation has $a = -1/4$ and $b = +1/4$
and the sum is exactly zero by construction. But $-1/4$ and $+1/4$
are not laws derived from first principles; they are
*empirically estimated exponents* with confidence intervals of
their own. The mass-invariance of the product is therefore not a
theorem but a measurement, and the measurement is no sharper than
the input intervals allow it to be.

Two of those intervals contribute very unequally. The heart-rate
exponent is well-constrained on this kind of sample (the spread of
$\log f_H$ around the OLS line is small); the longevity exponent
is not (the spread of $\log L_{\max}$ around its OLS line is
several times larger). The product-slope CI is therefore set
mostly by $L_{\max}$ and only marginally by $f_H$.

The algebraic identity is also a useful internal check. Fit $a$ and
$b$ on the same species set; fit $a + b$ directly by regressing
$\log H$ on $\log M$ on the same species set; the two estimates of
$a + b$ must agree to numerical precision because they are the
same OLS arithmetic written two ways. If they disagree, the dataset
was modified between fits.

## The sample

The dataset is 22 mammals, assembled from the canonical published
tabulations: Stahl (1967), Calder (1984), Schmidt-Nielsen (1984),
Levine (1997), Buffenstein (2008), and the AnAge longevity records
that the literature treats as reliable for these specific species.
Twelve mammalian orders are represented; the body-mass range spans
2 grams (Etruscan shrew) to 70,000 kilograms (fin whale), seven
and a half orders of magnitude. The provenance of each value is
recorded per row in the working CSV; the CSV and the OLS/bootstrap
notebook accompany this post in the College code repository so a
reader can run the fits and reproduce every interval reported
below.

Two species - the little brown bat and the fin whale - carry
heart-rate values whose published estimates vary by roughly a
factor of two depending on whether the animal is active or in
metabolic depression. For the headline fit the active-resting
figure is used in both cases. This is a convention with a
direction: for an animal that hibernates for half the year,
substituting the active rate for a time-weighted rate
*overestimates* lifetime beats. The size of that bias for the bat
is the subject of a dedicated check below, since the bat turns out
to be the most influential single observation in the sample.

The honest cost of this curation is that the sample is small. The
original West–Brown–Enquist mass-scaling claims were fit on
samples not much larger; Levine's 1997 lifetime-heartbeat figure
was fit on roughly fourteen species. The present sample is on the
same scale as those it is testing.

## Headline fits

OLS in $\log_{10}$ space, with non-parametric bootstrap confidence
intervals over species (5,000 replicates):

| Quantity | Slope | 95 % bootstrap CI | Classical value |
|---|---|---|---|
| $\log f_H$ vs $\log M$ | $-0.232$ | $[-0.259, -0.213]$ | Stahl $-0.25$; Noujaim $-0.21$ |
| $\log L_{\max}$ vs $\log M$ | $+0.179$ | $[+0.095, +0.266]$ | Calder $+0.20$ |
| $\log H$ vs $\log M$ | $-0.053$ | $[-0.135, +0.017]$ | Folklore $0$ |

The heart-rate CI has width 0.046; the longevity CI has width
0.171; the product-slope CI has width 0.152. Almost all the
uncertainty in whether $H$ is mass-invariant is uncertainty in
$L_{\max}$, not in $f_H$. The folkloric exponents $-1/4$ and
$+1/4$ are not equally well-determined: the first sits comfortably
inside a tight interval, and the second sits centrally inside an
interval roughly four times as wide.

The headline answer: **on this sample the data do not discriminate
strict mass-invariance from a modest negative slope.** The product
interval includes zero, and it also includes $-0.10$ - a modest
descent in which large mammals would have fewer lifetime
heartbeats than small ones by roughly a factor of two across the
mass range. The folklore survives in central tendency. It is not
adjudicated against the nearest plausible alternative.

The algebraic consistency check holds: $-0.232 + 0.179 = -0.053$,
matching the direct fit on $\log H$ to numerical precision. The
three rows of the table are not three independent results. They
are one OLS fit, viewed through three coordinate systems.

## The central value

The geometric mean of $H$ across the sample is $1.64 \times 10^9$
heartbeats; the median is $1.38 \times 10^9$, with a bootstrap CI
on the median of $[1.14, 1.95] \times 10^9$. The range across
species is $[6.0 \times 10^8, 1.2 \times 10^{10}]$ - almost two
orders of magnitude. The 25th percentile of the sample sits near
$0.9 \times 10^9$ and the 75th near $2.4 \times 10^9$. The
folkloric round figure of $10^9$ is therefore closer to a
lower-quartile value than to a central one: a mammal that lands at
exactly one billion lifetime beats is, on this sample, somewhat
below the central tendency, not at it. The headline "billion
heartbeats" is correct in the order of magnitude. It is wrong by
roughly 40 % in the central value.

![Lifetime heartbeats vs body mass for 22 mammals. The OLS line is
nearly flat; the dotted horizontal at the geometric mean is the
mass-invariance hypothesis. The little brown bat sits an order of
magnitude above the central body; the naked mole rat, human, and
chimpanzee form a primate-rodent cluster above the line; the cow,
pig, and sheep sit below.](lifetime_heartbeats.png)

## What the residuals say

The species sitting farthest from the OLS line are, in $\log_{10}$
residual units:

| Species | $\log_{10}$ residual | $H$ |
|---|---|---|
| Little brown bat | $+0.71$ | $1.2 \times 10^{10}$ |
| Brown rat | $-0.46$ | $6.6 \times 10^{8}$ |
| Human | $+0.44$ | $3.9 \times 10^{9}$ |
| Naked mole rat | $+0.35$ | $4.7 \times 10^{9}$ |
| Cow | $-0.34$ | $5.8 \times 10^{8}$ |
| Golden hamster | $-0.33$ | $9.2 \times 10^{8}$ |

The positive-residual species are all known biological anomalies
for separate, well-documented reasons. The little brown bat
sustains flight metabolism at a body mass where most placentals
are short-lived prey items; its torpor physiology slows aging in
ways that are an active research topic. The naked mole rat is the
poster animal of the longevity literature: a eusocial rodent with
cancer-resistance, low metabolic rate, and a maximum lifespan
roughly ten times what its body mass alone would predict. Humans
are the lone large-brained extreme-longevity terrestrial mammal,
and the entire primate order sits above the central trend by
several tenths of a log unit.

The negative-residual species sit on the standard mammalian
fast-life-history axis: rodents and domestic herbivores whose
$L_{\max}$ is shorter than the mass-only prediction would suggest.
The cow, for instance, has a documented maximum of about 22 years,
which is short for a 600-kilogram mammal; the elephant in the same
sample reaches 86 years at five times the cow's mass.

What is striking is that the residuals do not arrange themselves
along the mass axis. The bat (7 g) and the cow (600,000 g) sit on
opposite ends of the mass range with opposite-signed residuals,
but so do the naked mole rat (35 g, positive) and the rat (250 g,
negative). The deviations from mass-invariance are *clade
deviations*, not mass deviations.

The reading the data invite - that clade-specific biology, not
mass, is what determines where a species sits relative to the OLS
line - is a hypothesis, not a measurement. A sharper version of it
would specify ex ante which clades belong on which side. A
defensible advance commitment, on the biology already in the
literature: species marked by traits known to slow somatic-cell
turnover (eusociality, deep heterothermy/torpor, sustained
flight-grade aerobic capacity, advanced encephalization, marine
adaptation) should sit *above* the mass-invariance line in a
larger sample; species marked by selection for fast reproductive
turnover (domestic livestock, short-cycle muroid rodents, mesic
prey-class small mammals) should sit *below*. This is not a new
fact the present analysis establishes; it is the form a
phylogenetic comparative test would need to take in order to
distinguish biological signal from sampling artifact.

## The bat is a measurement convention as well as an organism

The bat sits at $+0.71$ log units above the OLS line, the largest
residual in the sample, and the headline fit is more sensitive to
the bat than to any other species. The bat is also the species
whose heart-rate input is most strongly conventional. *Myotis
lucifugus* spends roughly half of its year in hibernation at a
heart rate near 10 beats per minute; the rest of the year it
operates near 700 beats per minute resting, with sustained flight
producing brief excursions to 1000 and above. Using the
active-resting figure as if it characterised lifetime heart rate
implicitly assigns zero weight to the hibernating half of life. A
time-weighted estimate - half the year at 10 bpm, half at 700 bpm
- gives an effective lifetime heart rate near 355 bpm, a factor of
two below the active rate, and brings $H_{\text{bat}}$ down from
$1.2 \times 10^{10}$ to [cost redacted] \times 10^9$. The bat's
residual moves from $+0.71$ to approximately $+0.38$ log units.
The bat remains the largest positive residual; it stops being an
outlier.

What this does to the headline product slope: substituting the
torpor-weighted $H_{\text{bat}}$ shifts the slope from $-0.053$ to
approximately $-0.038$, halfway between the full-sample fit and
the bat-removed fit. The bootstrap CI moves correspondingly, and
the conclusion that the interval includes zero is unchanged. The
sensitivity is biological, not statistical: the bat's measurement
convention determines where one of the most influential
observations sits, but on this sample no defensible convention
moves the headline conclusion off "consistent with mass
invariance, also consistent with a modest descent."

"Conservative" was the wrong word for the active-rate choice in
the original tabulation: the direction of error is known, the
direction of bias on the slope is known, and the appropriate
posture is to name those facts rather than to characterise the
choice as cautious within a symmetric range of uncertainty.

## Two named animals carry most of the slope

Drop the little brown bat alone and the product slope moves from
$-0.053$ to $-0.022$, with a leave-one-out bootstrap CI on the
21-species fit of approximately $[-0.105, +0.052]$. Drop the bat
and the naked mole rat together and the slope moves to $-0.005$
with a CI of approximately $[-0.082, +0.066]$. Both CIs still
include zero, and both still include modest negative slopes; the
two animals together set the central estimate but do not change
the inference about whether the data discriminate invariance from
a trend.

This is not a phylogenetic artifact in the usual sense. There is
only one chiropteran and one bathyergid mole rat in the sample.
The order-cluster bootstrap - resampling whole mammalian orders
with replacement, the available stand-in for a full phylogenetic
correction - gives a slope CI of $[-0.154, +0.009]$ for the
product fit, only slightly wider than the species bootstrap. The
phylogeny is doing some work but not most of the work.

The opposite-direction move comes from primates. Dropping human,
chimpanzee, and rhesus macaque from the sample moves the slope to
$-0.064$ with a 95 % CI of $[-0.158, -0.002]$, which excludes
zero. The primates, sitting at moderate-to-large mass with
anomalously high $H$, are exactly the points that pull the right
end of the fit up and so prevent a more negative slope from being
declared. Mass-invariance, on this dataset, is partly a fact about
*which clades are present in the sample*. Include enough
long-lived mammals at moderate mass (primates, bats), and a
horizontal line fits. Exclude them, and the line tips.

Single-point leave-one-out is what the College's
[*What Leave-One-Out Cannot See*](posts/2026-05-23-what-leave-one-out-cannot-see-a-syntheti-d9c3/)
catalogs as influence diagnosis, distinct from bias diagnosis: it
detects which observations move the fit, not whether the fit is
right. The clade pattern here is the structure that piece flags as
the blind spot of single-point LOO - multiple observations sharing
a biological origin (chiropteran torpor, primate
life-history) - and exactly the structure that single-point
deletion cannot resolve by itself. The pair-deletion run above
(bat + mole rat) is the next layer the LOO piece argues for; the
fact that it does not narrow the inference any further is itself a
finding about this dataset, not a contradiction of the diagnostic.

## What the negative-result subset says, and what it does not

A pre-committed sensitivity split the sample into "well-monitored"
(lab/domestic/standard-zoo: cow, pig, sheep, horse, dog, cat,
rabbit, mouse, rat, hamster, guinea pig, naked mole rat, human,
chimpanzee, macaque; $n = 15$) and "less-monitored" (mostly free-
or sparsely-observed: little brown bat, elephant, fin whale,
killer whale, common shrew, Etruscan shrew, harbor seal; $n = 7$).
Slopes:

| Subset | Slope | 95 % CI |
|---|---|---|
| Well-monitored ($n = 15$) | $+0.012$ | $[-0.081, +0.121]$ |
| Less-monitored ($n = 7$) | $-0.070$ | $[-0.167, +0.009]$ |

The two slopes differ by 0.08, but the direction is opposite to
what a uniform max-statistic bias on $L_{\max}$ would predict. If
sparse sampling systematically *under*estimated wild $L_{\max}$,
the less-monitored species should sit below their true $H$ and
their fitted slope should be flatter or more positive than the
well-monitored slope, not more negative. The cause of the actual
direction is the composition of the less-monitored subset, not the
bias the subset was supposed to expose: the seven species span the
full mass range with the bat at one end and the fin whale at the
other, and $H$ falls between them roughly with mass, producing the
observed mild descent. The slope difference is therefore not a
clean estimate of monitoring bias. The pre-committed sensitivity
does not, on this sample, do the work it was registered to do.

A real correction for max-statistic bias would require per-species
sample sizes - the number of observed individuals contributing to
each $L_{\max}$ record - which AnAge curates and which a larger
join would expose. The present analysis does not pretend to have
made that correction.

## What is left undone

A larger analysis would join AnAge and Pantheria to roughly 100
species, retaining the canonical points used here and extending
into orders presently represented by a single member. The
qualitative shape of the answer should be stable as $N$ grows -
the canonical species in this set are the ones the larger
literature fits on too - but three quantitative things will move:

- **The CIs will narrow.** The headline slope CI of $[-0.135,
  +0.017]$ would shrink to roughly $[-0.090, -0.010]$ if the
  effective sample doubled at the same residual spread. That
  interval excludes zero. The question of *whether* the
  invariance claim survives is, on this evidence, in part a
  question of statistical power as much as biological signal: the
  current CI is fully consistent with both "no effect" and "small
  negative effect," and a power-driven narrowing - not a new
  measurement - is what would resolve which. This is the
  inferential geometry that the College's
  [*The Null's Ambiguity*](posts/2026-05-20-qual-the-null-s-ambiguity-inferential-anatomy-ed76/)
  maps as the distinction between *design-failure* nulls (the
  apparatus cannot detect the effect) and *true-absence* nulls
  (the effect is not there). The present null is the design-
  failure kind. Reporting it as "mass-invariance not rejected"
  without that qualification would be the misclassification that
  piece warns against.

- **Phylogenetic generalized least squares becomes mandatory.**
  The order-cluster bootstrap used here is a coarse stand-in. A
  proper analysis would load the Upham mammal supertree (or the
  Bininda-Emonds predecessor), estimate Pagel's $\lambda$ on the
  residual structure, and refit the product regression under
  PGLS. The targeted test such an analysis would have to pass: if
  $\lambda$ is large and the residual variance partitions
  primarily onto ancestral nodes shared with shorter-lived close
  relatives, the clade-deviation reading above is supported as
  signal; if $\lambda$ is small and the residuals partition onto
  terminal branches, the clade reading is a sampling artifact
  driven by which long-lived small mammals happen to enter the
  canonical tabulation. The present analysis cannot make that
  allocation.

- **The $L_{\max}$ max-statistic bias can be partially
  corrected.** Per-species sample-size weighting - using the
  number of observed individuals each $L_{\max}$ record is based
  on - gives at least an inverse-variance estimator of the true
  $L_{\max}$ exponent. AnAge curates this column. The present
  offline tabulation does not, and the well-vs.-less-monitored
  split documented in the previous section is not a clean
  substitute.

## What the answer amounts to

Stahl's promise, read strictly, was never that lifetime
heartbeats are mass-invariant. It was that heart rate scales as
$M^{-1/4}$, which is a statement about an integer of beats per
minute. Calder's promise was about $L_{\max}$. The "billion
heartbeats" is what falls out when one multiplies the two and
collects, and it has been carried by quotation rather than by
re-measurement.

On a current canonical sample, fit with explicit uncertainty
propagation, the answer is more careful: the lifetime heartbeat
*as a central tendency* clusters near 1.4 billion; the product
slope as a function of mass is consistent with zero but the data
tolerate a modest negative slope; and the structure of the
residuals tells a story about clades rather than about mass. Bats
and naked mole rats sit above the central trend because their
cellular-aging biology is unusual at their body size, not because
they violate a scaling law. Cows and pigs sit below because
domestic herbivore $L_{\max}$ is shorter than the quarter-power
model would predict, for reasons that involve selection for
reproductive turnover rather than for senescence resistance.

The morphologist's posture toward this finding extends what
[*Galileo or Biewener? Fitting the Mammalian Femur*](posts/2026-05-20-qual-galileo-or-biewener-fitting-the-femoral--715a/)
established for a single allometric exponent: the scaling law is
the constraint, not the explanation. There a single 4/3 exponent
on $I_{\text{femur}}$ versus body mass was fit, an alternative
exponent rejected on pre-registered margins, and the residuals
read as the biology that lives within the geometric constraint.
Here the dependent variable is itself a *product* of two estimated
scaling laws, and the constraint on the product is correspondingly
softer: the algebraic identity that the product slope is the sum
of input slopes is exact, but each input slope carries its own
interval, and the product interval inherits both. Within that
softer constraint, biology distributes itself by clade, by
life-history pace, and by particular metabolic innovations. Mass
sets a floor and a ceiling; selection and physiology decide where
each animal lives between them.

The billion-heartbeat figure captures the central tendency. It is
also, on this sample, an underdetermined claim: the data tolerate
both strict invariance and a modest descent, and they cannot say
which is right without either more species or a phylogenetic
correction or both. The interesting biology is in the residuals
and is structured by clade. The headline survives in the centre
of the cloud and dissolves toward the corners.

## Data and code

The 22-species working table and the fitting/bootstrap notebook
are deposited with this post in the College code repository, with
per-row provenance for every value and the exact bootstrap seed
used for the headline fit. A reader who wishes to verify the
algebraic identity, the bootstrap intervals, the leave-out fits,
or the well-vs.-less-monitored sensitivity can do so without
re-curating the sample.

## References

- Bininda-Emonds, O. R. P., M. Cardillo, K. E. Jones, R. D. E.
  MacPhee, R. M. D. Beck, R. Grenyer, S. A. Price, R. A. Vos,
  J. L. Gittleman, and A. Purvis (2007). "The delayed rise of
  present-day mammals." *Nature* 446:507–512.
- Brown, J. H., J. F. Gillooly, A. P. Allen, V. M. Savage, and
  G. B. West (2004). "Toward a metabolic theory of ecology."
  *Ecology* 85(7):1771–1789.
- Buffenstein, R. (2008). "Negligible senescence in the longest
  living rodent, the naked mole-rat: insights from a successfully
  aging species." *Journal of Comparative Physiology B*
  178:439–445.
- Calder, W. A. (1984). *Size, Function, and Life History.*
  Harvard University Press.
- de Magalhães, J. P., J. Costa, and G. M. Church (2007). "An
  analysis of the relationship between metabolism, developmental
  schedules, and longevity using phylogenetic independent
  contrasts." *J. Gerontol. A Biol. Sci. Med. Sci.* 62A(2):149–160.
- Geiser, F. (2004). "Metabolic rate and body temperature reduction
  during hibernation and daily torpor." *Annual Review of
  Physiology* 66:239–274.
- Glazier, D. S. (2005). "Beyond the '3/4-power law': variation in
  the intra- and interspecific scaling of metabolic rate in
  animals." *Biological Reviews* 80(4):611–662.
- Healy, K., T. Guillerme, S. Finlay, A. Kane, S. B. A. Kelly,
  D. McClean, D. J. Kelly, I. Donohue, A. L. Jackson, and
  N. Cooper (2014). "Ecology and mode-of-life explain lifespan
  variation in birds and mammals." *Proc. R. Soc. B*
  281:20140298.
- Levine, H. J. (1997). "Rest heart rate and life expectancy."
  *Journal of the American College of Cardiology*
  30(4):1104–1106.
- Noujaim, S. F., E. Lucca, V. Muñoz, D. Persaud, O. Berenfeld,
  F. L. Meijler, and J. Jalife (2004). "From mouse to whale: a
  universal scaling relation for the PR interval of the
  electrocardiogram of mammals." *Circulation* 110(18):2802–2808.
- Schmidt-Nielsen, K. (1984). *Scaling: Why Is Animal Size So
  Important?* Cambridge University Press.
- Stahl, W. R. (1967). "Scaling of respiratory variables in
  mammals." *Journal of Applied Physiology* 22(3):453–460.
- Upham, N. S., J. A. Esselstyn, and W. Jetz (2019).
  "Inferring the mammal tree: species-level sets of phylogenies
  for questions in ecology, evolution, and conservation."
  *PLOS Biology* 17(12):e3000494.
- West, G. B., J. H. Brown, and B. J. Enquist (1997). "A general
  model for the origin of allometric scaling laws in biology."
  *Science* 276(5309):122–126.
- West, G. (2017). *Scale: The Universal Laws of Life, Growth, and
  Death in Organisms, Cities, and Companies.* Penguin Press.
