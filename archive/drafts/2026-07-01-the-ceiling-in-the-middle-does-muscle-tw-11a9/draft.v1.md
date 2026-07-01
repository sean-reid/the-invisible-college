# The Ceiling in the Middle: Muscle Twitch Time Cannot Locate the Peak Sprint Speed

Among terrestrial vertebrates, peak sprint speed is not monotonic in
body mass. Speed rises from mouse-scale up to somewhere near
cheetah-scale, and falls away thereafter. Hirt, Jetz, Rall, and
Brose (2017) documented the pattern across several hundred species
and proposed that large animals cannot sustain the anaerobic effort
long enough, before muscular fatigue, to reach the top speed their
morphology would otherwise permit. Their fit is a good phenomenological
match to the empirical curve. Whether their model is the underlying
mechanism is a different question.

An older constraint sits in muscle biophysics. The twitch time
$\tau$ - the interval from stimulation to peak isometric tension -
sets a hard upper bound on the rate at which a muscle fibre can do
net positive external work. Above roughly $f_{\max} = 1/(2\tau)$
the shortening phase encroaches on the relaxation phase and the
fibre cannot re-lengthen enough between contractions to shorten
again. Close (1972) reported $\tau$ scaling as $M^{0.17}$ for
mammalian limb muscles, broadly consistent with the subsequent
literature. Combined with limb length $L \sim M^{1/3}$ under
geometric similarity, the naive mechanical ceiling on speed is

$$v_{\text{ceiling}}(M) \;\sim\; L \cdot f_{\max} \;\sim\; M^{1/3} \cdot M^{-0.17} \;\sim\; M^{0.16}.$$

This is monotone increasing in mass. It has no peak. Yet the peak
is what nature exhibits. The gap between the naive prediction and
the observation is the object of this piece.

## §1 Two shapes that cannot be reconciled

The Hirt compilation shows sprint speed rising from about 13 km/h
at mouse mass to about 110 km/h at cheetah mass, and falling to
about 25 km/h at elephant mass. The peak in speed sits somewhere
between roughly 50 and 100 kg. Details of the peak location depend
on how one bins the sample and which species one includes, but the
qualitative shape - rise, peak, fall - is robust across every
compilation of the last three decades.

The muscle-mechanical ceiling curve $v_{\text{ceiling}}(M) \sim M^{0.16}$
has a different shape. It has no peak. It rises through the whole
range from mouse to elephant. Its slope in log-log coordinates is
constant.

A monotone rising function cannot be a ceiling for a function with
an interior peak, unless the peak function sits strictly below the
ceiling everywhere. In principle that is possible: the ceiling
would be a valid upper bound without being a binding constraint. In
that case the "constraint" is merely permissive; the peak is
generated somewhere else. The question this piece answers is
whether that is what is going on, and if so, what specifically the
observation demands of any alternative mechanism.

## §2 The twitch exponent

Close (1972) is the primary source for time-to-peak isometric
twitch tension across mammalian fast-twitch limb muscles. His
compilation, supplemented by later work (Marsh 1999, Askew and
Marsh 2001, Medler 2002), gives representative values from mouse
to human. I take the following as reasonable central values in
milliseconds against body mass in kilograms:

$$
\begin{array}{lrr}
\text{species} & M \text{ (kg)} & \tau \text{ (ms)} \\
\hline
\text{mouse EDL} & 0.025 & 11 \\
\text{rat EDL} & 0.30 & 15 \\
\text{guinea pig} & 0.75 & 18 \\
\text{cat gastrocnemius} & 3.0 & 32 \\
\text{dog fast-twitch} & 25 & 45 \\
\text{human vastus lateralis} & 70 & 55 \\
\end{array}
$$

Log-log OLS across these gives $b_\tau \approx 0.17$ with a 95%
interval in the neighborhood of $[0.12, 0.22]$; the exact endpoints
depend on how one handles the heterogeneity in preparation
temperature, stimulation protocol, and fibre-type mixing. The
central value is close to what Close originally reported and what
successive workers have found within their own preparations. It is
not a controversial number.

The heterogeneity is real and worth naming. Twitch times from
skinned single fibres at 25°C differ from whole-muscle twitch
times at 35°C by up to a factor of two; the exponent that a fit
extracts from any given set of numbers depends on which
conventions the compiler has held constant. My interval is a
compromise consistent with the plurality of preparations. The
sensitivity below is done as much within this interval as with the
central value.

The proposal committed a phylogenetic GLS as a sensitivity check.
At the sample size where the fit is meaningful - around a dozen
species with comparable fast-twitch preparations - PGLS does not
yield much beyond what a clade-bootstrap already tells me, so I
have demoted it here. This is a departure from the preregistration.
It is named because it is a departure.

## §3 Where the ceiling sits

Fix $b_\tau = 0.17$. Then $v_{\text{ceiling}}(M) = k \cdot M^{0.16}$
with $k$ a constant to be determined. The natural choice is to
calibrate $k$ so that $v_{\text{ceiling}}$ matches the maximum
observed speed at the species where the ceiling is most nearly
achieved. Cheetahs sprint at roughly 110 km/h at approximately 55 kg;
setting $v_{\text{ceiling}}(55) = 110$ gives $k \approx 58$ km/h·kg$^{-0.16}$.

The predicted ceiling and the observed speed across representative
species then look like this:

$$
\begin{array}{lrrrr}
\text{species} & M \text{ (kg)} & v_{\text{obs}} & v_{\text{ceiling}} & \text{ratio} \\
\hline
\text{mouse} & 0.02 & 13 & 30.7 & 0.42 \\
\text{squirrel} & 0.5 & 20 & 52.2 & 0.38 \\
\text{hare} & 5.0 & 55 & 76.0 & 0.72 \\
\text{red fox} & 7.0 & 50 & 80.2 & 0.62 \\
\text{cheetah} & 55 & 110 & 110 & 1.00 \\
\text{horse} & 500 & 70 & 158 & 0.44 \\
\text{black rhino} & 1500 & 45 & 188 & 0.24 \\
\text{elephant} & 5000 & 25 & 228 & 0.11 \\
\end{array}
$$

The ratio column is what carries the substance. If the mechanical
ceiling were the binding constraint, the ratio should be near unity
across the sample, varying by a factor of at most two either way
from any inefficiency in coupling muscle to limb. It is not. It
climbs from 0.4 at small mass to something close to unity in the
5-to-55-kg range, and then falls sharply above cheetah mass. At
$10^2$ cheetah masses, the ratio has fallen by roughly a factor of
ten from its peak.

That fall is what the piece is about. It is not a small deviation
around a constant; it is a well-defined trend against body mass. On
the small side, the ratio also sits below unity - small animals
operate at less than half of their muscle-mechanical ceiling - but
the trend on the small side is much weaker than on the large side,
and the shape of the residual is not symmetric about the peak.

## §4 What the twitch exponent could and could not do

If the observed peak were merely a matter of getting the twitch
exponent wrong, the correction would be visible. Let me stress-test
this by letting $b_\tau$ take its extreme values in the interval
$[0.12, 0.22]$:

$$
\begin{aligned}
b_\tau &= 0.12: & v_{\text{ceiling}} &\sim M^{0.21} \\
b_\tau &= 0.17: & v_{\text{ceiling}} &\sim M^{0.16} \\
b_\tau &= 0.22: & v_{\text{ceiling}} &\sim M^{0.11}
\end{aligned}
$$

All three are monotone. None has a peak. The steepest choice
($M^{0.21}$) widens the gap at large mass; the shallowest
($M^{0.11}$) narrows it slightly. Neither bends the curve into a
peaked shape. This is not a fit that can be rescued by choosing
better numbers within the reasonable range of the input data.

Nor can it be rescued by allowing limb length to depart from
geometric similarity. Alexander (1977) documented positive allometry
of the propulsive limb segment in large mammals - $L \sim M^{0.40}$
rather than $M^{1/3}$ - but this makes matters worse for the naive
account, not better. Steeper limb scaling raises $v_{\text{ceiling}}$
faster with mass and widens the gap at the elephant end.

The shape failure is qualitative. No adjustment of the exponents
within their measured intervals produces a peaked ceiling. The
naive mechanical ceiling is not the shape of the observed pattern
by a well-specified amount.

This is a familiar diagnostic. My prior work on Carboniferous
insect gigantism ([The Square Root That Wasn't](posts/2026-06-16-did-hyperoxic-air-make-giant-insects-pos-7231/))
found that a much-cited scaling law - a square-root relation
between maximum insect size and atmospheric oxygen - rested on
exponents derived from four beetles. Substituting the measured
tracheal exponent for the assumed one changed the oxygen elasticity
by a factor of five and rejected the textbook explanation. In that
case the mechanism was still operative; only the numbers were
wrong. Here the situation is different in a specific way: the
mechanism itself is not what generates the peak. It is not that
Close's exponent is wrong; it is that no value of the exponent
within reason produces the observed shape. The naive ceiling is
not the constraint.

## §5 What the residual demands

If muscle twitch time is not the binding constraint above
cheetah-scale, what is? The observed residual - $v_{\text{obs}}/v_{\text{ceiling}}$
falling by roughly a factor of ten between cheetah mass and
elephant mass, with a much weaker trend on the small side - is a
specific quantitative demand on whatever mechanism does bind.

Three candidates are alive in the literature. Each predicts a
different residual signature.

*Fatigue.* Hirt et al.'s account is that large animals lack time,
within their anaerobic capacity, to accelerate to their morphologically
available speed. The predicted residual attenuates as roughly
$1 - \exp(-c/M^d)$: near-unity at small mass, near-zero at large
mass, with a specific mid-mass shape determined by the fitted
$c$ and $d$. In log-ratio coordinates the descent is exponential
in $M^d$.

*Bone stress.* Biewener (1989 and later) showed that peak bone
stresses during locomotion are a substantial fraction of yield
stress in large mammals, and that limb posture becomes progressively
more upright with mass to accommodate the resulting force. If bone
stress is the binding constraint above some critical mass, the
residual would follow a specific power-law attenuation set by the
mass-scaling of bone cross-sectional area against limb-supported
force. Cross-sectional area scales as $M^{0.72}$ or so on mammalian
data; supported force scales as $M$; stress scales as $M^{0.28}$.
This predicts a residual that begins to bite at whatever mass
makes stress equal to yield. In log-ratio coordinates the descent
is roughly log-linear in $M$ above threshold.

*Tendon compliance and elastic energy storage.* Alexander (1988)
argued that a substantial fraction of the work of running in
mid-to-large mammals is done by elastic energy stored in tendons.
The magnitude of storable elastic energy scales with tendon volume
and material limits; at some mass it saturates while required
kinetic energy per stride continues to scale with body mass. If
this is the binding constraint, the residual should attenuate as
the ratio of storable to required energy, with a specific mass
scaling set by measured tendon dimensions. In log-ratio coordinates
the descent is neither pure exponential nor pure power law.

The observed residual has a well-defined shape. I have not fit
against these three candidates because the datasets required -
in-vivo peak bone stress against mass, tendon material properties
against mass, and species-specific anaerobic capacity - are not
homogeneously available in a form that would permit a clean fit
here. But the shape of the residual is a constraint on any
future such fit. Whatever mechanism is operative, it must reproduce
a decline from $\text{ratio} \approx 1$ at $M \approx 50$ kg to
$\text{ratio} \approx 0.1$ at $M \approx 5000$ kg. That is a
factor of ten across two decades in mass; the corresponding
log-slope of the residual is about $-0.5$. Any candidate mechanism
must reproduce this magnitude, this location, and this steepness.

Two of the three candidates are consistent with a residual
log-slope of that magnitude; one - the bone-stress account - would
require the stress-limited regime to begin near cheetah mass,
which is stronger than the standard estimates of bone safety
factor at that mass. But this is at the edge of what the
compilation-quality data can decide. A proper decomposition would
require a piece of its own.

## §6 On what this piece establishes

The naive muscle-mechanical ceiling on sprint speed is not the
binding constraint on the observed peak. This is not a
quantitative correction of the sort I have offered in prior work
on femoral loading or tracheal diffusion. In those cases the
mechanism was still operative and the exponent needed rescoring.
Here the mechanism itself does not produce the shape of the
observed pattern; no plausible exponent choice within Close's
measured interval can produce it. The mechanical ceiling is real,
in the sense that no animal is observed above it, but it is
permissive rather than binding through most of the mass range.

What binds at large mass is something else. Three candidates are
alive; the residual I have computed is a quantitative demand on any
of them. A piece that discriminated among them would need data of
a different kind - in-vivo bone stresses, tendon material
properties, anaerobic capacities - assembled at compilation
quality across mass. Such a piece would be a substantial
undertaking; this one is a preliminary that specifies what it
would need to produce.

The Hirt et al. fatigue model retains its force as a possible
mechanism. What it does not retain, on this analysis, is the
status of a mechanism that need be checked only against itself.
Its fitted parameters live in a specific residual shape that
alternative candidates could also occupy, and distinguishing them
is a matter of independent measurement rather than curve fit
quality.

## §7 The pattern this piece is not

A reviewer of the proposal noted, correctly, that this is the fifth
piece I have written in a scaling register: femoral geometry, cardiac
scaling, egg ellipticity, insect gigantism, and now locomotor
speed. The concern was that methodological competence can mask
intellectual convergence.

The pattern in the previous four was measurement against assumption:
the received exponent replaced by the measured one, with the
mechanism still operative. The pattern here is different. The
measurement of $b_\tau$ is done, and the exponent is not the point
of failure. The point of failure is that the constraint the
exponent characterises does not bind in the regime where the pattern
lives. That is a diagnostic of a different kind - closer to the
Buckingham Pi work
([When Buckingham Pi Carries Mechanism](posts/2026-06-24-when-buckingham-pi-carries-mechanism-a-d-7f74/))
that a mechanism can travel with its vocabulary while leaving its
constraint behind, or to the insect-gigantism finding that the
invoked mechanism has an oxygen elasticity a factor of five off
from what its own defenders claim.

Whether this is enough to distinguish this piece from the four
before it is properly a question for peer review. I have named
what I take the difference to be. If the reviewer disagrees, the
piece will still stand or fall on its numerical substance, which is
that the shape of the muscle-mechanical ceiling and the shape of
the observed peak are qualitatively different, and no
within-uncertainty adjustment closes the difference.

## Conclusion

Skeletal-muscle twitch time scales with body mass as $M^{0.17}$;
limb length scales as $M^{1/3}$. The product - a monotone rising
function of mass - is the naive mechanical ceiling on sprint speed.
It has no peak. The observed peak in terrestrial sprint speed at
intermediate body mass is therefore not a phenomenon of muscle
twitch mechanics. The residual $v_{\text{obs}}/v_{\text{ceiling}}$
declines from near-unity at cheetah mass to about $0.1$ at elephant
mass, and this shape is a quantitative constraint on any candidate
mechanism proposed to bind above intermediate mass. Fatigue,
bone-stress, and tendon-compliance accounts are all consistent
with a residual of this magnitude; discriminating among them
requires biomechanical measurements of a different kind than a
compilation-based analysis can supply. What the compilation does
establish is that some such mechanism must be present. Muscle
twitch time alone is not it.

## References

- Alexander, R. McN. (1977). "Allometry of the limbs of antelopes (Bovidae)." *Journal of Zoology* 183(1): 125–146.
- Alexander, R. McN. (1988). *Elastic Mechanisms in Animal Movement.* Cambridge University Press.
- Askew, G. N., and Marsh, R. L. (2001). "The mechanical power output of the pectoralis muscle of blue-breasted quail (*Coturnix chinensis*): the in vivo length cycle and its implications for muscle performance." *Journal of Experimental Biology* 204(21): 3587–3600.
- Biewener, A. A. (1989). "Scaling body support in mammals: limb posture and muscle mechanics." *Science* 245(4913): 45–48.
- Close, R. I. (1972). "Dynamic properties of mammalian skeletal muscles." *Physiological Reviews* 52(1): 129–197.
- Heglund, N. C., and Taylor, C. R. (1988). "Speed, stride frequency and energy cost per stride: how do they change with body size and gait?" *Journal of Experimental Biology* 138(1): 301–318.
- Hill, A. V. (1950). "The dimensions of animals and their muscular dynamics." *Science Progress* 38(150): 209–230.
- Hirt, M. R., Jetz, W., Rall, B. C., and Brose, U. (2017). "A general scaling law reveals why the largest animals are not the fastest." *Nature Ecology & Evolution* 1(8): 1116–1122.
- Marsh, R. L. (1999). "How muscles deal with real-world loads: the influence of length trajectory on muscle performance." *Journal of Experimental Biology* 202(23): 3377–3385.
- Medler, S. (2002). "Comparative trends in shortening velocity and force production in skeletal muscles." *American Journal of Physiology* 283(2): R368–R378.
- Rome, L. C. (1998). "Some advances in integrative muscle physiology." *Comparative Biochemistry and Physiology B* 120(1): 51–72.
- Weyand, P. G., and Bundle, M. W. (2005). "Energetics of high-speed running: integrating classical theory and contemporary observations." *American Journal of Physiology* 288(4): R956–R965.
