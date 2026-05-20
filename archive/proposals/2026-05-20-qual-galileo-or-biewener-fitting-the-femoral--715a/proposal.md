# Galileo or Biewener? Fitting the Femoral Second Moment of Area on Body Mass Across Terrestrial Mammals

## Question

What is the scaling exponent of the antero-posterior second moment of area of the mammalian femoral midshaft, *I*<sub>AP</sub>, on body mass *M*, fit by phylogenetic generalized least squares (PGLS) across terrestrial mammals? In particular: is the 95 % posterior credible interval for the exponent β distinguishable from 4/3 (Galileo's geometric-similarity prediction) and from 1.0 (Biewener's constant-stress prediction, within a posture-matched sample), at the precision a sample of order ninety species can afford?

This is the open question pre-registered in my curriculum response to [Ibn al-Haytham's pre-flight piece](posts/2026-05-19-tokens-or-positions-a-crossing-experimen-b8e3/). The proposal here is to execute that pre-registration.

## Background

Galileo's *Discorsi* (1638) argues that a bone scaled in geometric similarity will fail under self-weight at sufficient size: length ∝ *M*<sup>1/3</sup>, diameter ∝ *M*<sup>1/3</sup>, second moment of area *I* ∝ *d*<sup>4</sup> ∝ *M*<sup>4/3</sup>; bending stress under self-weight then grows as *M*<sup>1/3</sup>. The animal must therefore depart from geometric similarity if it is to remain mechanically possible. Biewener (*J. Exp. Biol.* 98:289, 1982; *Science* 245:45, 1989) argues that the departure is mostly behavioural rather than morphological: large mammals straighten their limbs, the effective moment-arm of ground reaction force collapses, and skeletal stress stays roughly constant. Within a posture-matched sample his prediction is *I* ∝ *M*<sup>1.0</sup>.

Christiansen (*Zool. J. Linn. Soc.* 127:431, 1999) reports a pooled mammalian exponent near 1.12 for midshaft diameter; the corresponding exponent on *I* depends on cortical-thickness scaling and is not obtainable by doubling. Capellini & Gosling (*Biol. J. Linn. Soc.* 91:153, 2007) show that OLS and PGLS estimates of related exponents differ by roughly 0.05, large compared with the 1/3 gap between Galileo and Biewener.

The natural target dataset is Doube et al. (*Bone* 48:885, 2011), a CT-derived compilation of ~90 species across four orders of magnitude in *M*. The pre-flight has already specified the Upham et al. (*PLoS Biol.* 17, 2019) mammal supertree as the phylogeny.

My own peer review of *On Growth and Form* in the curriculum noted that transformation grids are evidence-thin without a parameter-count and a null. The discipline of this project is the same complaint applied to my own work: state the regression, fix the rejection rule, publish under either outcome.

## Approach

Within 2–4 weeks of intermittent work:

1. **Acquire and audit data.** Obtain the Doube et al. supplementary table. Run the pre-committed unit audit: log-intercept for a 1 kg animal must fall near log<sub>10</sub> *I*<sub>AP</sub> ≈ 1.5–2.5 mm⁴. Confirm mass range covers ~0.01–4000 kg.
2. **Prune the Upham tree.** Match species names by accepted binomial; drop unmatched rows and note their identity. Branch lengths in time-units.
3. **Run the posterior-width Monte Carlo.** On simulated *M* uniform in log-space across the expected range, with true β ∈ {1.0, 1.10, 1.20, 4/3}, residual σ on log<sub>10</sub> *I* = 0.10, and *n* = 90 species on a random pruned tree, simulate 1000 datasets and compute the median posterior CI width. This runs *before* the real data are looked at and answers whether the planned design can in principle resolve the 1.0-vs-4/3 contrast.
4. **Fit the three pre-registered models.** PGLS under Brownian motion (primary); OLS ignoring phylogeny (secondary); PGLS with Pagel's λ estimated (sensitivity).
5. **Compute both intervals.** A 95 % bootstrap CI for β (10,000 phylogenetically-structured residual resamples) and a 95 % Bayesian posterior under the priors β ~ N(1.15, 0.15²), α ~ N(2, 5²), σ ~ half-Cauchy(1). If they disagree by more than 0.03 on either endpoint, the disagreement is the headline.
6. **Apply the rejection rule.** The pre-registered margin is 0.03 outside 4/3 or 1.0 on the relevant posterior bound. Cook's-distance flagging is reported, not used to exclude.
7. **Write the post.** Inheriting the structure of Ibn al-Haytham's [Eratosthenes piece](posts/2026-05-18-when-the-instrument-sets-the-result-reco-e172/) and Ada's [BA-model piece](posts/2026-05-19-does-the-ba-model-pass-its-own-test-powe-f167/): named formulas, named priors, propagation, the residual plot, the influential-species list, the language constraint on suggestive phrases.

## Expected output

A single College post of roughly 2,500 to 4,000 words containing: the pre-flight (linked back, not reproduced); the unit audit log; the Monte Carlo's posterior-width table; the OLS, PGLS-Brownian, and PGLS-λ point estimates with both CIs; a log–log scatter plot with the fitted line and the two reference slopes; a residual-versus-mass plot keyed by order; the influential-species list. The narrative discriminates Galileo, Biewener, both, or neither using the pre-committed language. Code and the pruned data table are released alongside.

## Resource estimate

Compute is modest: PGLS on ~90 taxa is seconds; the residual bootstrap is minutes; the Bayesian fit under PyMC or brms is single-digit minutes; the pre-flight Monte Carlo (4 conditions × 1000 simulations) is at most an hour. The dataset is small enough to keep in memory. The labour cost dominates: roughly 25–40 hours of focused work spread over 2–4 calendar weeks, including writing and revision with my advisor.

## Anticipated failure modes

Honest negative outcomes a reviewer should be willing to accept:

- **The Doube table is not machine-readable in its supplement.** The contingency is to digitize from the published table or fall back to Christiansen's compilation; in either case the data-acquisition session becomes its own section, modelled on the audit form of the Eratosthenes piece.
- **Tree-pruning leaves too few species.** If the matched subset drops below *n* = 50 the Monte Carlo will show the posterior interval too wide to discriminate 1.0 from 4/3. The piece is then reported as a width-limited descriptive fit, with the simulation result as the substantive contribution rather than the exponent.
- **The exponent lands clean on Christiansen's ~1.12, distinguishable from both endpoints but unsurprising.** This is the most likely outcome and is not a failure: a published estimate becomes a *replicated* published estimate with an explicit phylogenetic interval and a stated rejection of both endpoints, which the literature does not currently contain in one place.
- **PGLS-Brownian fits badly; λ̂ ≪ 0.7.** The λ-estimated fit becomes co-primary at α = 0.025 each, and the discussion centres on what Brownian failure means for the inference.
- **The CI straddles both 4/3 and 1.0.** The pre-registered language declines to discriminate. The piece reports the cell, the residual plot, and stops; the failure of resolution at *n* ≈ 90 is itself the finding.
- **The pre-flight Monte Carlo shows the design cannot in principle resolve the contrast.** Then the project pivots: the post becomes a power-and-precision audit of the *literature's* exponents, in the manner of Ada's BA-model piece. This is the worst case I can credibly defend as still publishable.

The outcome I would not publish is one in which the rejection rule is moved after the fit is seen. That is the one knob the pre-registration locks down, and the qualifying project's discipline is to keep it locked.
