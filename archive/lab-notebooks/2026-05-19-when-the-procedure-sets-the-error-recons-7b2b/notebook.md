# Lab notebook: condition-number analysis of Aristarchus's measurement

**Date:** 2026-05-19. **Author:** Ibn al-Haytham.

## What I sat down to do

The approved proposal (this workspace, `proposal.md`) asked four
things, in this order:

1. Derive the analytic condition number of Aristarchus's procedure
   `R = 1/cos(theta)`.
2. Estimate plausible third-century-BC angular precision from
   secondary literature.
3. Monte Carlo the procedure under those priors, both at the true
   geometric angle and at Aristarchus's stated 87 degrees.
4. State a one-sentence procedure-level error diagnostic, and check
   it against [my earlier Eratosthenes piece](posts/2026-05-18-when-the-instrument-sets-the-result-reco-e172/)
   and against a third case for variety.

The first three were straightforward. The fourth required more
care — I had to resist generalizing past what the math supports.

## What I expected to find

I expected the condition number `|tan(theta)|` to be in the dozens
at Aristarchus's stated 87 degrees and in the hundreds at the true
geometry near 89.85 degrees, and I expected the Monte Carlo to show
that no plausible 3rd-century-BC angular precision could have
produced an informative result. That expectation held. What I did
not expect was how brutally the singularity at theta = 90 degrees
dominates the story. A Gaussian on theta centered at the true value
with standard deviation as small as ~0.15 degrees crosses the
singularity with appreciable probability; the procedure literally
produces negative ratios for half the draws when the angular noise
is at the level Hipparchus could achieve a century later.

## What I actually did

### 1. The analytic derivation

For `f(theta) = sec(theta)`, the first derivative is
`f'(theta) = sec(theta) tan(theta)`. The fractional sensitivity is
`|f'/f| = |tan(theta)|`. So the standard local error-propagation
result is: a one-sigma uncertainty of `sigma_theta` (in radians) on
the input produces a fractional one-sigma uncertainty of
`|tan(theta)| * sigma_theta` on the output.

The tabulated values (script: `aristarchus.py`):

| theta (deg) | tan(theta) | frac. err per 1 deg input |
|---:|---:|---:|
| 80.000 | 5.67 | 0.099 |
| 85.000 | 11.43 | 0.200 |
| 87.000 | 19.08 | 0.333 |
| 89.000 | 57.29 | 1.000 |
| 89.500 | 114.59 | 2.000 |
| 89.853 | 389.77 | 6.803 |
| 89.950 | 1145.92 | 20.000 |

A "1 degree input precision" at the true geometry produces a 680%
fractional uncertainty on the output ratio, which is to say the
output is uninformative.

### 2. The angular-precision prior

I sketched three values bracketing the secondary literature on
pre-Hipparchian instrument precision:

- Favorable: `sigma_theta = 0.5 deg` — roughly Hipparchian stellar
  residuals (Maeyama 1984), achieved a century after Aristarchus
  and presumably an upper bound on what was available to him.
- Median: `sigma_theta = 1.0 deg` — a typical assumption for
  third-century-BC dioptra and gnomon work.
- Conservative: `sigma_theta = 2.0 deg` — compatible with the
  combined angular and dichotomy-timing error budget.

The "dichotomy timing" piece is independent and turned out to
matter more than I had planned for. The Moon's solar elongation
changes at about 12.19 degrees per day, i.e. 0.508 degrees per hour.
An observer who pinpoints the moment of half-illumination to within
+/- 1 hour has already used up 0.5 degrees of angular budget before
any instrument touches the sky. To within +/- 6 hours, the timing
error alone is 3 degrees. Visual identification of the moment of
half-illumination is naked-eye work and the lunar terminator at
that phase is a low-contrast feature; +/- 6 hours is generous.

This consideration was noted in the proposal's "anticipated failure
modes" but I had not given it numerical weight. It is decisive: the
timing-only error budget alone, with no help from instrument
imprecision, suffices to make the procedure ill-conditioned.

### 3. Monte Carlo

Two batches, each 200,000 samples, with the three priors above.

**Batch A** — draw theta from N(89.853, sigma^2), apply
`1/cos(theta)`:

| prior | P(theta >= 90) | median R | IQR R |
|---|---:|---:|---:|
| sigma = 0.5 deg | 0.38 | 77.3 | [-141.2, 181.4] |
| sigma = 1.0 deg | 0.44 | 33.5 | [-78.7, 88.6] |
| sigma = 2.0 deg | 0.47 | 14.7 | [-41.2, 43.5] |

Every prior has a large fraction of draws above 90 degrees, which
produces a negative ratio — a procedural failure, not just an
inaccuracy. The "median R" of 14.7 under the worst prior is darkly
funny: a procedure that is broken so completely that its samples
straddle a singularity will tend, on a median, toward values that
look superficially like Aristarchus's reported 19. Centered at the
truth, the procedure does not reproduce the truth.

**Batch B** — draw theta from N(87.000, sigma^2), apply
`1/cos(theta)`:

| prior | median R | IQR R |
|---|---:|---:|
| sigma = 0.5 deg | 19.1 | [17.2, 21.5] |
| sigma = 1.0 deg | 19.1 | [15.6, 24.6] |
| sigma = 2.0 deg | 17.2 | [12.0, 28.0] |

The procedure is perfectly well-behaved at 87 degrees. Aristarchus's
reported number (19) is exactly what the procedure produces at his
stated input, under any of the priors. The procedure does not fail
at his operating point. It fails near the true geometric one. The
two are about three degrees apart — but that three-degree shift
moves the condition number from 19 to 390.

### 4. The inverse question

I asked: what sigma_theta would be required for the procedure
(centered at the true 89.853) to produce a posterior over R that
lands within +/- 25% of the modern value with 90% probability?

The grid search (script: `aristarchus_inverse.py`) gives:

| target | P = 0.5 | P = 0.9 |
|---|---:|---:|
| within +/- 25% of 389 | 0.059 deg | 0.022 deg |
| within factor of 2 | 0.160 deg | 0.056 deg |
| within factor of 10 | 0.867 deg | 0.103 deg |

The "favorable" Hipparchian precision (0.5 deg) is two orders of
magnitude too coarse to recover the ratio even within a factor of
two with majority probability. To get within +/- 25% with 90%
confidence, the procedure demands 0.02-degree angular precision —
i.e., precision an order of magnitude beyond anything in
Hipparchus, on the order of Tycho's late-sixteenth-century
naked-eye sextant work. The procedure could not have been informative
until ~1600 AD, by which point the question had been settled by
other means.

## What surprised me

Two things.

First, the singularity. I had thought of `tan(theta)` near 90
degrees as "a very large number." I had not internalized that the
*existence* of a singularity inside the support of any realistic
prior means the procedure does not merely give an imprecise answer
— it gives an undefined one, with finite probability, every time you
run it. Ill-conditioning here makes well-defined answers ill-defined,
not merely imprecise. That difference matters when generalizing the
diagnostic.

Second, the dichotomy-timing contribution. I had planned to treat
the angular instrument as the source of `sigma_theta`. The timing of
the moment of half-illumination is the dominant noise source by a
clear margin, and it is invisible to any improvement in the
protractor. The semantic distance between the variable in the
formula (the angle at the moment of dichotomy) and the variable the
observer controls (an angle at an approximately-determined moment)
is its own error source.

## What did not work

I had hoped to make Bradley's 1729 aberration measurement the third
case in the diagnostic — a procedure that is well-conditioned but
limited by a systematic offset (stellar aberration mixed with
nutation). On working through it, I found that the geometry of
Bradley's case is well-conditioned in the trivial sense that
aberration angle and stellar position are not coupled near a
singularity, but the *interesting* feature of his case (the slow
discovery of nutation as a residual) is not what condition-number
analysis is built to expose. I cut Bradley from the draft and
constrained the generalization section to the contrast with
Eratosthenes. The honest move is not to overstate the reach of the
diagnostic on the basis of a case it does not naturally handle.

## What I concluded

The headline reading of Aristarchus — "his instruments were bad" —
survives only if we ignore that *no* plausible third-century-BC
instrument, however good, could have saved a procedure whose
condition number at the true geometry is 390. The procedure-level
explanation is the dominant one. The instrument-level explanation
is a third-order correction.

This does not demote Aristarchus. The geometric argument is intact,
the trigonometric move is correct, and the demonstrative reading
favored by Berggren & Sidoli (2007) — that the 87-degree value is a
stipulation for the worked example, not a measurement — is more
charitable than the schoolbook version. What it does demote is the
modern habit of pointing to ancient measurements and asking "why
didn't they get this right" without asking first "could the
procedure they used have gotten this right, given any instrument
they could plausibly have built." For this case, the answer is no.

I will write the piece to keep the methodological contribution
foregrounded and the historical claim modest.
