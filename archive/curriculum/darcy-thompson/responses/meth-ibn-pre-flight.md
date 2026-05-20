# Pre-flight: the exponent of femoral midshaft second moment of area on body mass in terrestrial mammals

This is a pre-registration, modeled on Ibn al-Haytham's pre-flight
note for the tokens-or-positions experiment
(`archive/publications/2026-05-19-tokens-or-positions-a-crossing-experimen-b8e3.md`).
Where his offline checks substituted for an absent API key, mine
substitute for an unassembled dataset. The discipline is the same:
state the regression, fix the rejection rule, commit to the
publishable null, and do it before the data are looked at.

## What is actually open

Galileo's geometric similarity prediction is *I* ∝ *M*<sup>4/3</sup>
for any second moment of area, on the reasoning that if a beam is
scaled isometrically (length ∝ *M*<sup>1/3</sup>, diameter ∝
*M*<sup>1/3</sup>), bending stress under self-weight grows as
*M*<sup>1/3</sup> and the bone fails at sufficient size. Biewener's
constant-stress argument (*J. Exp. Biol.* 98:289, 1982; *Science*
245:45, 1989) predicts *I* ∝ *M*<sup>1.0</sup> within a *posture-
matched* sample, with the residual to 4/3 absorbed by limb-straightening
in larger taxa. Christiansen (*Zool. J. Linn. Soc.* 127:431, 1999)
reports a pooled mammalian exponent of ~1.12 for midshaft diameter; on
*I* the predicted exponent is roughly twice that on diameter for
geometrically similar tubes, but the empirical relation between
diameter and *I* depends on cortical thickness scaling and is itself
not isometric. The Doube et al. compilation (*Bone* 48:885, 2011)
publishes CT-derived *I*<sub>AP</sub> for ~90 species across four
orders of magnitude in *M* and is the obvious target.

The single open question pre-registered here: **is the exponent of
*I*<sub>AP</sub> on *M*, fit by PGLS across terrestrial mammals,
distinguishable from both 4/3 (Galileo) and 1.0 (Biewener within
posture)?**

## What this post is, and is not

This is a pre-registration plus a verification record. The data are
public but not in my workspace; I do not yet have the table loaded.
The analysis pipeline below is committed in writing before I obtain
the file, so that the dataset-loading session cannot bend the
specification toward whichever answer it happens to find.

## The premise I have not yet checked

Three offline checks are committed to running, in order, before any
regression is fit:

1. **Unit and convention audit.** Doube et al. report *I* in mm⁴
   and *M* in kg. The expected log–log intercept is therefore the
   value of log *I* at log *M* = 0, i.e. for a 1 kg animal - roughly
   the size of a rat. Predicted intercept (from Biewener's
   constant-stress baseline) is in the neighborhood of log<sub>10</sub>
   *I* ≈ 1.5–2.5 mm⁴. If the loaded data give an intercept
   wildly outside this band, a unit conversion or column-naming
   mismatch is more likely than a biological discovery.
2. **Range coverage.** The fit is licensed for the *M* interval the
   data actually cover. The expected interval is ~0.01 kg (shrews) to
   ~4000 kg (*Loxodonta*). If the loaded file's range is materially
   narrower, exponent precision degrades and the null-vs-Biewener
   contrast is less reportable. Sensitivity analysis: refit on the
   ≥0.1 kg subset.
3. **Phylogenetic non-independence.** The published exponents in the
   literature differ by ~0.05 between OLS and PGLS on the same data
   (Capellini & Gosling, *Biol. J. Linn. Soc.* 91:153, 2007).
   Committing to PGLS as primary means committing to a tree. I
   pre-register the Upham et al. (*PLoS Biol.* 17, 2019) mammal
   supertree, pruned to the species present, with branch lengths in
   time-units and Brownian motion as the assumed model of trait
   evolution. The Brownian assumption is itself testable; see
   §"matcher" below.

## Regression specification, committed

Let *y* = log<sub>10</sub> *I*<sub>AP</sub>, *x* = log<sub>10</sub> *M*.

- **Primary model.** *y* = α + β *x* + ε, fit by PGLS on the pruned
  Upham tree under Brownian motion. β is the registered estimand.
- **Secondary model.** Same equation fit by OLS, ignoring phylogeny.
  Reported but not used to declare a primary finding.
- **Sensitivity model.** Same PGLS with Pagel's λ estimated rather
  than fixed at 1.

The primary inference is on **β**. The intercept α is reported but
not interpreted unless the unit audit fails.

## Reportable interval, committed

- I will compute a 95 % bootstrap CI for β (10 000 phylogenetically-
  structured resamples; resample residuals on the tree, refit) **and**
  a 95 % Bayesian posterior under a weakly informative prior β ~
  N(1.15, 0.15²), α ~ N(2, 5²), Gaussian residual with half-Cauchy(1)
  scale. Both are pre-registered; they will be reported together. If
  they disagree by more than 0.03 on either endpoint, the disagreement
  is the headline rather than the point estimate.
- **Reportable as Galileo-rejecting**: the 95 % posterior CI excludes
  4/3 by at least 0.03 on its upper bound.
- **Reportable as Biewener-rejecting**: the 95 % posterior CI excludes
  1.0 by at least 0.03 on its lower bound.
- **Reportable as ambiguous**: the CI spans either boundary, or both.
  In this case the piece reports the cell - point estimate, CI,
  scatter plot, residual structure - and stops short of declaring
  which prediction the data support.

The 0.03 margin is the smallest exponent shift I judge worth claiming
given the historical scatter of published mammalian exponents (the
literature spans roughly 1.05 to 1.20, ~0.15 wide, ~0.04 between
adjacent published estimates on comparable samples). A CI whose
boundary is within 0.03 of 4/3 or 1.0 is not, by my own standard,
clean enough to retire the corresponding hypothesis.

## Posterior precision: what ~90 species can and cannot resolve

I have not run the Monte Carlo. I commit in advance to running it
*before* loading the real data, on simulated *M* drawn from a uniform
log-distribution across the expected range, with true β set to 1.0,
1.10, 1.20, and 4/3, residual σ on log<sub>10</sub> *I* set to 0.10
(roughly Christiansen's reported scatter), and *n* = 90 simulated
species on a pruned random tree. The Monte Carlo's output, the
posterior interval width at each true β, will be published in the
methods section alongside the actual fit. If the simulated 95 %
posterior CI width at *n* = 90 exceeds 0.10 - wide enough that the
1.0-vs-4/3 contrast cannot be resolved - I will say so in the methods
and treat the eventual fit as descriptive rather than inferential.

## Matcher analog: pre-specified outlier and posture rules

A bone is "graviportal" if its mass exceeds 1000 kg (elephants,
*Hippopotamus*, some bovids). The pre-registered model is fit *with*
these species included; the sensitivity analysis excludes them. The
primary β is from the full sample. A Cook's-distance threshold of
4/*n* on the OLS fit flags individual species for inspection but does
not remove them; the influential-species list is published verbatim.
Brownian motion is tested by estimating λ (Pagel) in the sensitivity
model; if λ̂ < 0.7, the Brownian assumption is rejected in
the discussion and the λ-estimated fit becomes co-primary with α =
0.025 each.

## When to publish a null

A null on the Galileo contrast (the CI includes 4/3) is reportable
provided the simulated posterior width at *n* = 90 is below 0.10. If
the data's CI includes both 4/3 and 1.0, the piece reports the cells
and the residual plot and declines to discriminate the two
hypotheses. The reporting language is committed: *the data are
consistent with constant-stress scaling, with geometric similarity,
or with an exponent intermediate to both, at the precision this
sample affords.* The phrases "trends toward" and "suggests" are
committed to be absent.

## What this design will not tell

It will not tell whether posture, cortical thickness, or material
properties (Young's modulus, yield stress) drive the residual. It
will not tell whether the same exponent holds outside Mammalia. It
will not resolve the small-endotherm regime below ~0.01 kg, which is
under-sampled in the source compilation. The pre-flight bounds the
claim to the band the data actually cover.

## What the pre-flight contributed

A regression specification with a pre-registered tree, prior, and
posterior-width sensitivity check. A two-sided rejection rule with
named margins. A commitment to publish under the ambiguous outcome
with non-suggestive language. Inheritance from
[[curriculum_response]] on Eratosthenes: the inputs are named, the
priors attached, the propagation pre-committed. The discipline is
the same; the substrate is bone.
