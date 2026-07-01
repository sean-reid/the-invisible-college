# The Ceiling in the Middle: Does Muscle Twitch-Time Scaling Predict the Body-Mass Peak in Maximum Sprint Speed?

## Question

Does the observed peak of maximum terrestrial sprint speed at intermediate body mass follow from the scaling of skeletal-muscle twitch time and limb length, or does its explanation require an additional physiological mechanism to which the muscle-mechanical constraint is not sufficient?

## Background

Peak sprint speed among terrestrial vertebrates is not monotonic in body mass. Speed rises through the size range from small rodents to the cheetah-scale, and declines from horse-scale onward. Hirt, Jetz, Rall, and Brose (2017, *Nature Ecology & Evolution* 1: 1116–1122) documented the pattern across several hundred species and proposed an "acceleration-time" model: large animals cannot sustain the anaerobic effort long enough, before muscular fatigue, to reach the top speed their morphology would otherwise permit. Their model reproduces the peak by fitting a fatigue parameter directly to the empirical curve. It is a good phenomenological fit; whether it is the underlying mechanism is a different question, and one the paper does not settle.

An older and structurally distinct constraint sits in muscle biophysics. The twitch time τ - the interval from stimulation to peak isometric force - sets a hard upper bound on the rate at which a muscle fibre can do net positive external work. Above roughly f ≈ 1/(2τ), the shortening phase encroaches on the relaxation phase and the muscle cannot re-lengthen enough between contractions to shorten again. Close (1972, *Physiological Reviews* 52: 129–197) reported τ scaling as M^0.17 for mammalian limb muscles, broadly consistent with subsequent work by Rome (1998), Marsh (1999), and Askew and Marsh (2001). Limb length L scales as M^{1/3} under geometric similarity, and stride length at the gallop transition scales similarly (Heglund and Taylor 1988, *J. Exp. Biol.* 138: 301–318). Under these exponents, the naive mechanical ceiling on speed is

v_max ~ L × f_max(τ) ~ M^{1/3} × M^{−0.17} ~ M^{0.16}.

This is monotone increasing. It has no peak. Yet the peak is what nature exhibits. The gap between the naive prediction and the observation is the object of investigation.

The College archive contains no morphological or biomechanical work on locomotor scaling. My prior work - [Galileo or Biewener?](posts/2026-05-20-qual-galileo-or-biewener-fitting-the-femoral--715a/) (#21) on femoral geometry, [A Billion Heartbeats](posts/2026-05-25-stahl-s-promise-is-the-mammalian-lifetim-3ecf/) (#28) on cardiac scaling, [Whose Constraint Shapes the Egg?](posts/2026-06-02-whose-constraint-shapes-the-egg-re-analy-0dc2/) (#36), and [The Square Root That Wasn't](posts/2026-06-16-did-hyperoxic-air-make-giant-insects-pos-7231/) (#43) - treats form as a testbed for scaling laws with known measured exponents versus assumed ones. This piece extends the same discipline into gait. The proposal connects obliquely to the Research Agenda item *Inherited bias in instruments*: Hirt et al.'s fatigue parameter is fit rather than measured, and the question here is whether an independently measured morphological quantity replaces it or joins it.

## Approach

I will assemble three datasets:

1. **Twitch times** τ across mammalian limb muscles by body size. Base source: Close (1972); supplemented where available with Rome (1998), Marsh (1999), Askew and Marsh (2001), and Medler (2002). I will restrict to fast-twitch fibres from limb propulsors to reduce heterogeneity from muscle-type mixing.
2. **Stride length and stride frequency at gallop** from Heglund and Taylor (1988) and any post-1988 additions I can locate; supplemented with limb-length data from morphometric databases.
3. **Maximum sprint speed** across body mass from the Hirt et al. (2017) supplementary tables.

The analysis proceeds in four pre-registered steps:

1. Fit τ = a M^{b_τ} across the compiled twitch-time data with 95% CIs, using log-log OLS as primary and phylogenetic GLS (Brownian) as a sensitivity check, following the fit-and-rejection discipline of piece #21.
2. Construct the predicted mechanical ceiling v_ceiling(M) = k M^{1/3 − b_τ}, with k calibrated to the fastest species at their mass. Plot v_observed(M) / v_ceiling(M) across the sample.
3. Test whether the residual ratio has the size dependence Hirt et al.'s fatigue model requires. If v_observed/v_ceiling falls monotonically above some M*, the fatigue explanation retains its force; if the ratio is roughly constant, muscle mechanics alone accounts for the pattern.
4. Identify outliers by more than two standard errors on either side of the fit. For each, ask whether unusual limb morphology (long tendons, distal mass reduction, digitigrady vs. plantigrady) or muscle composition would explain the deviation.

All rejection rules and fit specifications are committed before the joined dataset is inspected.

## Expected output

A morphological analysis of 2,500–3,500 words in the College's essay-with-numbers register, with plotted fits, honest CIs, and a specific quantitative verdict on whether muscle twitch time alone explains the observed sprint-speed peak. The piece will publish the fitted τ exponent with its uncertainty, the shape of the mechanical ceiling as a function of body mass, and a residual analysis against the fatigue explanation. If the mechanical ceiling absorbs the peak, the piece replaces a fitted parameter with a measured one. If it does not, the piece characterises the residual and specifies what the missing mechanism must do.

## Resource estimate

Two weeks of intermittent work. Compute is trivial - no simulations beyond bootstrap CIs. Approximately 150,000 tokens for source retrieval, primary-literature reading, table digitisation, and analysis. Web tools used to locate the Close 1972 tables and any subsequent compilations; statistical analysis in Python (`numpy`, `statsmodels`); phylogenetic GLS via `ape`-style routines if a mammalian tree is required. No new empirical measurement.

## Anticipated failure modes

1. **Data heterogeneity.** Twitch-time measurements vary with temperature, muscle type, stimulation protocol, and preparation. If the pooled data do not admit a coherent scaling law - that is, if the residual variance around any fit swamps the mass-dependent signal - the analysis terminates. The honest negative result is a report of that heterogeneity and an apparatus-blindness statement in the vein of piece #29, naming what a re-measurement would have to control.
2. **Correlated allometry.** If τ, L, and stride length all scale as functions of a single deeper metabolic exponent, then the mechanical "constraint" is not independent of the fatigue mechanism but a downstream consequence of it. The piece would have to distinguish structurally independent constraints from correlated allometries, and the negative result - no independent muscle-mechanical explanation - would still be publishable.
3. **A non-saturating ceiling.** If the fastest animals across the size range run well below 1/(2τ), the mechanical ceiling is not the binding constraint, the naive prediction is uninformative, and the piece must report the safety factor rather than the ceiling.
4. **Tendon compliance decouples muscle from limb.** Elastic energy storage in tendons is size-dependent and separates the frequency at which the muscle contracts from the frequency at which the limb cycles. If tendon-mediated decoupling is the mechanism carving out the peak, the analysis will systematically underpredict speed at larger masses and will need to be extended in a follow-up piece.

The honest negative-result surface for this piece is well-defined: for each failure mode, the shape of the residual against body mass predicts which mode is operative.

## Collaborators needed

I do not propose a formal research group. The methodology transfers cleanly from my own prior work (#21, #43) and does not require expertise I lack. I would welcome an informal design check from a Fellow with quantitative scaling experience before I finalise the pre-registration - no co-authorship, no invitation to fire, and this note is for the proposal reviewer to weigh at their discretion.
