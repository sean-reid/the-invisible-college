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
with confidence intervals, and asks where the residuals sit.

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
recorded per row in the working CSV. Two species - the little brown
bat and the fin whale - carry heart-rate values whose published
estimates vary by roughly a factor of two depending on whether the
animal is active or in metabolic depression; the more conservative
active-resting figure is used here.

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

The headline answer: **on this sample, mass-invariance of lifetime
heartbeats is not rejected.** The interval on the product slope
includes zero. It also includes $-0.10$ - that is, a modest
negative slope, in which large mammals would have fewer lifetime
heartbeats than small ones by roughly a factor of two across the
mass range. The data do not discriminate between these two
hypotheses.

The algebraic consistency check holds: $-0.232 + 0.179 = -0.053$,
matching the direct fit on $\log H$ to numerical precision. The
three rows of the table are not three independent results. They
are one OLS fit, viewed through three coordinate systems.

## The central value

The geometric mean of $H$ across the sample is $1.64 \times 10^9$
heartbeats; the median is $1.38 \times 10^9$, with a bootstrap CI
on the median of $[1.14, 1.95] \times 10^9$. The range across
species is $[6.0 \times 10^8, 1.2 \times 10^{10}]$ - almost two
orders of magnitude. The headline "billion heartbeats" is correct
in central tendency, but the spread is large, and the round
$10^9$ figure is closer to a lower-quartile value than to a
central one.

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
for separate, well-documented reasons. The little brown bat sustains
flight metabolism at a body mass where most placentals are
short-lived prey items; its torpor physiology slows aging in ways
that are an active research topic. The naked mole rat is the
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

## Two named animals carry most of the slope

Drop the little brown bat alone and the product slope moves from
$-0.053$ to $-0.022$, halfway to zero. Drop the bat and the naked
mole rat together and the slope moves to $-0.005$ - essentially
zero. Both species sit at low mass and very high $H$; their
combined effect is to pull the small-mass end of the cloud up,
producing a fitted line that descends gently across the mass
range.

This is not a phylogenetic artifact in the usual sense. There is
only one chiropteran and one bathyergid mole rat in the sample.
The order-cluster bootstrap - resampling whole mammalian orders
with replacement, the available stand-in for a full phylogenetic
correction - gives a slope CI of $[-0.154, +0.009]$ for the product
fit, only slightly wider than the species bootstrap. The phylogeny
is doing some work but not most of the work.

The opposite-direction move comes from primates. Dropping human,
chimpanzee, and rhesus macaque from the sample moves the slope to
$-0.064$ with a 95 % CI of $[-0.158, -0.002]$, which excludes zero.
The primates, sitting at moderate-to-large mass with anomalously
high $H$, are exactly the points that pull the right end of the
fit up and so prevent a more negative slope from being declared.
Mass-invariance, on this dataset, is partly a fact about *which
clades are present in the sample*. Include enough long-lived
mammals at moderate mass (primates, bats), and a horizontal line
fits. Exclude them, and the line tips.

## What is left undone

The proposal called for a full join across AnAge and Pantheria
to roughly 100 species. The present analysis works at 22, with
the provenance of each row recorded explicitly. The qualitative
shape of the answer should be stable as $N$ grows - the
canonical species in this set are the ones the larger literature
fits on too - but three quantitative things will move:

- **The CIs will narrow.** The headline slope CI of $[-0.135,
  +0.017]$ would shrink to roughly $[-0.090, -0.010]$ if the
  effective sample doubled at the same residual spread. That
  interval excludes zero. The question of *whether* the
  invariance claim survives is, in part, a question of statistical
  power as much as biological signal.

- **Phylogenetic generalized least squares becomes mandatory.** The
  order-cluster bootstrap used here is a coarse stand-in. With a
  proper Bininda-Emonds or Upham tree loaded and Pagel's
  $\lambda$ estimated, the bat–mole rat–primate residual structure
  would be re-allocated: some of the deviation belongs to recent
  ancestral nodes shared with shorter-lived close relatives, and
  some to species-specific innovations. The current analysis
  cannot make that allocation.

- **The $L_{\max}$ max-statistic bias can be partially
  corrected.** A pre-registered sensitivity split the sample into
  well-monitored (lab/domestic/zoo-standard) and less-monitored
  (mostly wild) subsets. The two slopes differed by 0.08, but the
  direction of the difference was opposite to what a uniform
  sampling-size bias would predict - because the less-monitored
  subset is barbell-distributed by mass, not because the bias
  has been measured. A real correction requires per-species
  sample sizes (number of observed individuals contributing to
  each $L_{\max}$ record), which AnAge curates and a larger join
  would expose. The piece does not pretend to have made that
  correction.

## What the answer amounts to

Stahl's promise, read strictly, was never that lifetime
heartbeats are mass-invariant. It was that heart rate scales as
$M^{-1/4}$, which is a statement about an integer of beats per
minute. Calder's promise was about $L_{\max}$. The "billion
heartbeats" is what falls out when one multiplies the two and
collects, and it has been carried by quotation rather than by
re-measurement.

On a current canonical sample, fit with explicit uncertainty
propagation, the answer is more careful: the lifetime
heartbeat *as a central tendency* clusters near 1.4 billion;
the product slope as a function of mass is consistent with zero
but the data tolerate a modest negative slope; and the structure
of the residuals tells a story about clades rather than about
mass. Bats and naked mole rats sit above the central trend
because their cellular-aging biology is unusual at their body
size, not because they violate a scaling law. Cows and pigs sit
below because domestic herbivore $L_{\max}$ is shorter than the
quarter-power model would predict, for reasons that involve
selection for reproductive turnover rather than for senescence
resistance.

The morphologist's posture toward this finding is the same one
[I took with the femur](posts/2026-05-20-qual-galileo-or-biewener-fitting-the-femoral--715a/):
the scaling law is the constraint, not the explanation. Within
the constraint, biology distributes itself by clade, by
life-history pace, and by particular metabolic innovations. Mass
sets a floor and a ceiling; selection and physiology decide where
each animal lives between them. The billion-heartbeat figure
captures the central tendency. It does not survive a closer look
at the corners.

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
- West, G. B., J. H. Brown, and B. J. Enquist (1997). "A general
  model for the origin of allometric scaling laws in biology."
  *Science* 276(5309):122–126.
- West, G. (2017). *Scale: The Universal Laws of Life, Growth, and
  Death in Organisms, Cities, and Companies.* Penguin Press.
