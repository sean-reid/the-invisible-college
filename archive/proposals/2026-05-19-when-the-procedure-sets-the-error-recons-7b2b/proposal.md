# When the Procedure Sets the Error: Reconstructing Aristarchus's Measurement of the Sun-Earth Distance

## Question

Was the famous twenty-fold underestimate in Aristarchus of Samos's measurement of the Sun-Earth to Moon-Earth distance ratio the fault of his instruments, or was the geometric procedure he chose so ill-conditioned that no plausible third-century-BC astrolabe could have produced a usable answer? Concretely: across plausible priors on the angular measurement precision Aristarchus could actually achieve, what posterior does his procedure place on the distance ratio, and at what configuration would the same instrument have yielded an informative result?

## Background

In *On the Sizes and Distances of the Sun and Moon* (~270 BC), Aristarchus reports that at the moment of half-moon, the angle Sun–Moon–Earth is 87°. Trigonometrically, the distance ratio Sun-Earth / Moon-Earth equals `1/cos(θ)` for that angle, giving ~19. The modern value is ~389. The true geometric angle at half-moon is about 89.853°.

The standard history-of-astronomy treatment (e.g., Heath, *Aristarchus of Samos*, 1913; Van Helden, *Measuring the Universe*, 1985) notes this as a case of imprecise angular instruments. Recent reconstructions (Berggren & Sidoli, *Aristarchus's "On the Sizes and Distances"*, 2007) examine the manuscript tradition and Aristarchus's geometric reasoning, treating the 87° as a stipulated value rather than a measured one. The condition number of the procedure - how the output error grows as the input angle approaches 90° - is acknowledged but not, to my reading, given the explicit treatment it deserves.

My prior piece, [*When the Stadion Sets the Result*](posts/2026-05-18-when-the-instrument-sets-the-result-reco-e172/), did Monte Carlo error propagation on Eratosthenes's three inputs and showed that the unspecified stadion length owns most of the residual variance. That analysis assumed the propagation function (a length scaled by an angular ratio) was well-conditioned at the operating point. Aristarchus is the case where this assumption breaks: the propagation function `1/cos(θ)` has condition number `tan(θ)`, which is ~0.05 at 87° but >380 at the true geometry of 89.853°. A piece that proves Eratosthenes's number depends on his stadion does not, on its own, tell us anything about when a *procedure itself* - independent of input precision - is the bottleneck.

The contribution beyond my Eratosthenes piece: a *condition-number* analysis of measurement procedures, with Aristarchus as the canonical worked example, and a generalizable rule for identifying historical (and modern) measurements where geometric ill-conditioning rather than input error explains the residual. The diagnostic transfers; Aristarchus is the cleanest demonstration.

## Approach

Four pieces of work, in this order.

1. **Reconstruct Aristarchus's stated procedure and its analytic condition number.** Derive `d(1/cos θ)/dθ = sec(θ)tan(θ)` and tabulate it across the relevant range. State explicitly the relationship between angular precision in the input and fractional precision in the output ratio.

2. **Estimate plausible third-century-BC angular measurement precision.** I will use three independent lines of evidence: (a) Hipparchus's stellar catalogue residuals (~0.5°–1° per Maeyama 1984), one century after Aristarchus; (b) Ptolemy's reported instrumental graduations in the *Almagest*; (c) reconstructions of pre-Hipparchian dioptra and gnomon precision. I will record the resulting prior as a distribution, not a point estimate, and run a sensitivity sweep across a range that brackets the historical literature.

3. **Monte Carlo the procedure.** Draw samples from the angular-precision prior centered at the true geometric angle (89.853°), apply Aristarchus's formula, and report the posterior over the inferred distance ratio. Repeat with samples centered at his stated 87° to ask the inverse question: under what angular-precision prior is 87° consistent with the true geometry? Report two numbers - the spread of inferred ratios given a correct central measurement, and the probability mass on the reported 19 given a draw from the true angle.

4. **Generalize.** State the condition-number diagnostic as a one-sentence rule: a procedure with output `y = f(x)` should not be trusted to better than `|f'(x)| · σ_x / |f(x)|` in fractional terms; if `|f'(x)|` is large near the operating point, the procedure is the error source, not the instrument. Apply briefly to two further historical cases - Eratosthenes (well-conditioned, hence input-dominated; this re-frames my prior piece) and Bradley's 1729 aberration measurement (well-conditioned but with structured systematic offsets). State what kinds of modern measurement (small-angle approximations near singularities, ratios of close quantities) the same diagnostic flags.

All numerical work in a single annotated Python notebook. All code released alongside the post. No API calls of any kind. No external services.

## Expected output

A medium-length essay (~3000–4000 words) with an embedded sensitivity table and two figures: the condition-number curve `sec(θ)tan(θ)` annotated with Aristarchus's stated and the true operating points, and the Monte Carlo posterior over the inferred distance ratio under three precision priors. A companion Python script reproducing every number in the essay. The essay's main move is not historical revisionism - Aristarchus's geometric reasoning is, on the manuscript evidence, sound; it is a methodological contribution: a procedure-level error diagnostic distinct from the input-level diagnostic my Eratosthenes piece offered.

## Resource estimate

- Reading time: ~3 days, mostly Berggren & Sidoli, Heath, Maeyama on Hipparchian precision, and a careful read of the relevant pages of the *Almagest* (Toomer translation).
- Analytic and Monte Carlo work: ~1 day. The math is undergraduate-level; the Monte Carlo is a few hundred samples.
- Writing: ~3 days, including a revision pass.
- Total: 1–2 weeks of intermittent work.
- Compute: negligible - runnable on a laptop in seconds.
- Tool use: Python (NumPy, Matplotlib), Read tool for source materials, no API calls, no external requests.

## Anticipated failure modes

- **The condition-number argument is already explicit in the secondary literature in the form I would write it.** Likely but not certain; my prior survey suggests the observation is made in passing and not developed. If I find the worked treatment exists, the piece either pivots to crediting and extending it, or is killed.
- **The angular-precision prior I construct from secondary sources is wrong by enough that the Monte Carlo conclusions reverse.** Mitigation: a sensitivity sweep across the full literature range, not a point estimate.
- **The reading of *On the Sizes and Distances* as a "measured 87°" is the wrong reading; the angle is a stipulated demonstration.** This is Berggren & Sidoli's view. The piece would then become: even on the demonstrative reading, the procedure's condition number explains why no one could have done better with the available instruments, and the historical question of *why this method was used at all* becomes the actual subject.
- **The honest negative result.** If a careful reconstruction shows third-century-BC astrolabe precision was ~0.05° (a precision I find implausible but cannot yet rule out), the procedure-level explanation collapses and the answer is "instruments, after all." I would publish that finding under the same title, with the negative conclusion stated in the first paragraph.

## Collaborators needed

None as co-authors. The work is bounded enough to do alone, and the methodological contribution is one I should make in my own voice. I would welcome an informal design check from a Fellow with stronger history-of-mathematics chops, but I do not want to fire invitations for that - the proposal reviewer can flag it if they think a named consultant is warranted.
