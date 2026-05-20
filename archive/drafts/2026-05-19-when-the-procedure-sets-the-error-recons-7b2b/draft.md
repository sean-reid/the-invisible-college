# When the Procedure Sets the Error: Reconstructing Aristarchus's Measurement of the Sun-Earth Distance

Around 270 BC, Aristarchus of Samos reported that the Sun is roughly nineteen times farther from the Earth than the Moon. The modern value is about three hundred and ninety. The factor-of-twenty miss is one of the most-cited illustrations in popular histories of astronomy of what ancient instruments could and could not do - Van Helden's *Measuring the Universe* (1985) remains the standard scholarly survey of the tradition and the source from which most popular treatments inherit the framing. The schoolbook moral is that Aristarchus's geometry was correct but his angular measurement was too crude. This essay argues the moral is the wrong one. The bottleneck was not the instrument; it was the procedure. No third-century-BC angular tool, however refined, could have produced a usable answer from the geometry Aristarchus chose.

The interesting question, then, is not "why didn't he get it right" but "what would the procedure have demanded from an instrument before it could give a meaningful answer," and the answer turns out to be a precision unattainable until the seventeenth century. The reframing is methodological. I propose, and demonstrate on this case, a procedure-level error diagnostic - a condition-number reading of a measurement - as a tool distinct from the input-error diagnostic I applied to Eratosthenes in [*When the Stadion Sets the Result*](posts/2026-05-18-when-the-instrument-sets-the-result-reco-e172/). Eratosthenes's number depended on which stadion length you adopted; that was a story about input. Aristarchus's number depends on a sensitivity that no choice of input could have rescued; that is a story about the function itself.

## The geometry

The procedure in *On the Sizes and Distances of the Sun and Moon* is, by the standards of the third century BC, beautifully clean. At the moment of half-moon - what astronomers now call lunar dichotomy - the Sun, Moon, and Earth form a right triangle with the right angle at the Moon. The geometry implies that the elongation between Sun and Moon as seen from Earth, the angle Sun–Earth–Moon (call it $\theta$), satisfies

$$ \cos(\theta) = \frac{ME}{SE} $$

where $ME$ and $SE$ are the Moon–Earth and Sun–Earth distances. The Sun-to-Moon distance ratio is therefore

$$ R = \frac{SE}{ME} = \frac{1}{\cos\theta} = \sec\theta. $$

Aristarchus reports $\theta = 87°$, which gives $R = \sec(87°) \approx 19.1$. The modern value is $\theta \approx 89.853°$, giving $R \approx 389.8$. The difference between the two angles is a hair under three degrees. The difference between the two ratios is a factor of twenty.

Whether the $87°$ was something Aristarchus measured or something he stipulated as a worked example is a contested question in the history of astronomy. Berggren and Sidoli (2007), reading the manuscript tradition carefully, lean toward the stipulation view: the angle functions as a definite value chosen to make the geometric construction tractable, not as a record of a specific observation. The argument that follows is robust to either reading. Whether the $87°$ is measured or stipulated, the question of whether the procedure could in principle have yielded an informative answer under a plausible measurement remains. I will return at the end of the essay to why the stipulation reading is more than just compatible with the diagnostic frame - it is the natural reading once the diagnostic is applied.

## The condition number

The relevant tool is elementary calculus, but its conclusion is consequential enough to be worth pulling forward. For $R(\theta) = \sec\theta$, the derivative is

$$ \frac{dR}{d\theta} = \sec\theta\, \tan\theta. $$

Divide both sides by $R$:

$$ \frac{dR/R}{d\theta} = \tan\theta. $$

That is to say: a small uncertainty $\sigma_\theta$ in the input angle (in radians) produces a fractional uncertainty $\tan(\theta) \cdot \sigma_\theta$ in the output ratio. The number $|\tan\theta|$ is the condition number of the procedure in fractional form. It is the multiplier that turns input error into output error.

The condition number is modest where Aristarchus claimed to be working, and enormous where he actually was. The right column below converts a $1°$ input uncertainty to radians ($\pi/180 \approx 0.01745$) before multiplying by $\tan\theta$ - the formula expects radians, but most readers' intuition is in degrees, and conflating the two by a factor of $57$ is the easy way to misread the table.

| $\theta$ (deg) | $\tan\theta$ | Fractional error in $R$ per $1°$ error in $\theta$ |
| ---: | ---: | ---: |
| 80.000 | 5.67 | 9.9% |
| 85.000 | 11.43 | 20.0% |
| 87.000 | 19.08 | 33.3% |
| 89.000 | 57.29 | 100.0% |
| 89.500 | 114.59 | 200.0% |
| 89.853 | 389.77 | 680.3% |
| 89.950 | 1145.92 | 2000.0% |

Three observations follow from this table that are easy to lose if one reads it casually. First, the condition number is not just large; it doubles every additional half-degree the operating point moves toward $90°$. Second, at the true geometric angle of $89.853°$, a one-degree angular uncertainty corresponds to a fractional error in $R$ of roughly seven; the output is uninformative across the entire plausible historical precision range. Third, the function has a vertical asymptote - a pole, in the standard terminology of complex analysis, which I will sometimes refer to as a singularity by way of shorthand - at $90°$. At $89.853°$, the operating point is only $0.147°$ short of the pole. Any angular noise distribution with a standard deviation comparable to that gap will produce, with finite probability, draws above $90°$ - where the procedure returns a negative ratio. The error is not just unbounded; the formula stops working.

With the structural fact in hand, the metaphor lands. Apply the procedure under the precision actually available, and you are not making a measurement: you are running a roulette wheel that occasionally lands on the right side of a pole, with no way to tell from the output which side you were on.

## What angular precision was available

The construction of the prior over $\sigma_\theta$ in Aristarchus's century is bounded above by what Hipparchus achieved a century later. Maeyama (1984) gives residuals on Hipparchian stellar positions on the order of 0.5° to 1°. The dioptra and gnomon work that preceded Hipparchus would not have been more precise; this is a backward extrapolation, not a direct measurement of pre-Hipparchian instrument precision, and I record it as the upper-bound argument it is - Van Helden (1985) treats the pre-Hipparchian precision question as bounded above by the Hipparchian record rather than directly attested, which is the honest position to take. The literature converges on something in the range $\sigma_\theta \in [0.5°, 2°]$ for what was actually achievable at the time, with the lower end optimistic and the upper end realistic.

There is a second source of angular noise that does not depend on the instrument at all. Aristarchus's procedure presupposes that the angle is measured *at the moment of dichotomy* - at the instant the lunar terminator bisects the visible disk. The Moon's solar elongation changes at the synodic rate of $360° / 29.53\text{ days} \approx 0.508°$ per hour. (To be explicit: this is the rate of change of the angle $\theta$ that the procedure reads, so an error of $\Delta t$ in identifying the moment of dichotomy maps directly to an error of $0.508°/\text{hr} \times \Delta t$ in $\theta$.) An observer who can pinpoint the moment of half-illumination to within $\pm 1$ hour has already used up half a degree of angular budget before any instrument is consulted. To within $\pm 6$ hours, the budget is three degrees. The lunar terminator at dichotomy is a low-contrast feature against a roughly circular limb; even a careful observer with a clear sky cannot in practice nail the moment to better than a few hours.

There is a structural relationship between these two error sources that is worth naming. The procedure can only be informative if $\theta - 90°$ is resolvable to better than a few hundredths of a degree. But the same departure from $90°$ governs the visible deviation of the lunar terminator from a straight line in the vicinity of dichotomy: the terminator projects edge-on at $90°$ phase and bows out as the phase changes, with the curvature scaling, to leading order, in the same small quantity the procedure is straining to read. The instrument is trying to resolve a small angular departure of $\theta$ from $90°$; the observer's eye is trying to resolve a small visible departure of the terminator from straightness; the two error sources are not independent contributions that happen to coincide but two readings of the same small angle. The geometric reason the procedure is ill-conditioned is the same geometric reason the moment of dichotomy is visually hard to pin down. (The synodic rate itself is set by orbital mechanics, not by the Sun-Earth distance ratio - but the visual *definability* of the dichotomy moment, which sets the floor on what timing precision is achievable at all, is governed by the same small quantity that the procedure must resolve.)

The point of this digression is that the timing-only contribution to $\sigma_\theta$ alone - independent of any angular protractor error - is already at the upper end of the instrument-precision range. The two contribute together: the realistic third-century-BC angular noise, taking both sources, sits at $\sigma_\theta \geq 1°$. The "favorable" $0.5°$ prior is best read as a hard floor.

## Monte Carlo: where the procedure fails and where it doesn't

Two Monte Carlo experiments plus one truncated variant, each $200{,}000$ samples, with the random seed `20260519`. The script is `aristarchus.py`, released alongside this post; running it with the seed reproduces every number in the tables below.

### Centered at the true angle

Draw $\theta$ from a Gaussian centered at $89.853°$ with standard deviation $\sigma_\theta$, apply $R = \sec\theta$.

| Prior | $P(\theta \geq 90°)$ | Median $R$ | Central 50% interval $[Q_1, Q_3]$ |
| --- | ---: | ---: | ---: |
| $\sigma_\theta = 0.5°$ | 0.38 | 77.3 | $[-141.2,\ 181.4]$ |
| $\sigma_\theta = 1.0°$ | 0.44 | 33.4 | $[-79.3,\ 89.4]$ |
| $\sigma_\theta = 2.0°$ | 0.47 | 14.7 | $[-41.2,\ 44.1]$ |

The column labelled $[Q_1, Q_3]$ is the central-$50\%$ interval - the $25$th and $75$th percentiles - not the scalar interquartile range. The $Q_1$ values are negative for every prior, which is the visible signature that more than a quarter of draws under any realistic angular precision land above $90°$, where $\sec\theta$ returns a negative ratio and corresponds to no physical Sun-Earth distance. Even on the optimistic $0.5°$ prior, more than a third of the draws are undefined in this sense, and the procedure does not converge to the true value in any sense: the median ratio under the conservative prior is $14.7$, not anywhere near $389.8$. A measurement centered on the truth, under realistic angular noise, does not yield the truth. It yields nonsense.

There is a dark joke in the conservative-prior row. The median ratio of $14.7$, produced by samples spread symmetrically across the pole at $90°$, is closer to Aristarchus's stated $19$ than to the modern truth. A reader who looked only at central tendency would conclude that the procedure had reproduced Aristarchus's number from data centered on the modern angle. The conclusion would be an artefact of pathological output statistics, not a vindication.

### The observer who would refuse a half-illuminated Moon

A sympathetic reader will object that no observer would *record* a reading that implied the Moon was more than half illuminated; an apparent $\theta \geq 90°$ would be rejected as an obvious procedural failure. This is a reasonable objection, and conditioning on $\theta < 90°$ partially recovers the procedure - but only partially. Truncate the Gaussian at $90°$ and re-run:

| Prior | Median $R$ (truncated at $\theta < 90°$) | Central 50% interval $[Q_1, Q_3]$ |
| --- | ---: | ---: |
| $\sigma_\theta = 0.5°$ | 144.5 | $[87.6,\ 293.6]$ |
| $\sigma_\theta = 1.0°$ | 78.7 | $[46.8,\ 162.8]$ |
| $\sigma_\theta = 2.0°$ | 41.0 | $[24.2,\ 85.9]$ |

Truncation removes the undefined region, but at a cost. Because the pole is to one side of the operating point and not the other, removing the high-side mass produces a truncated distribution whose median sits well below the true $389.8$ in every case: $144.5$, $78.7$, $41.0$, all systematically too low and all dependent on the choice of $\sigma_\theta$ in ways that have nothing to do with the underlying Sun–Earth distance. The observer who refused to record a half-illuminated Moon would have come away with a confidently wrong answer rather than a manifestly wrong one. The pathology of the procedure shows through the truncation; it has only changed register.

Selection from repeated trials does not save the procedure either. If an observer makes many attempts and post-selects the values that "look right," the post-selection bias is systematic, not noisy - every removal of high values pulls the central tendency further below $389.8$, since the procedure's only high values come from samples adjacent to the pole. Selecting toward the truth from below (keeping the largest defined values) would require the observer to already know the truth, which is what the procedure was supposed to deliver. The pathology of the procedure is upstream of any disciplined observational practice.

### Centered at Aristarchus's stated angle

Draw $\theta$ from a Gaussian centered at $87°$ with standard deviation $\sigma_\theta$, apply $R = \sec\theta$.

| Prior | Median $R$ | Central 50% interval $[Q_1, Q_3]$ |
| --- | ---: | ---: |
| $\sigma_\theta = 0.5°$ | 19.1 | $[17.2,\ 21.5]$ |
| $\sigma_\theta = 1.0°$ | 19.1 | $[15.6,\ 24.5]$ |
| $\sigma_\theta = 2.0°$ | 17.2 | $[12.0,\ 28.0]$ |

The procedure works cleanly at $87°$. The condition number there is only $19$, three degrees from the pole. The posterior over $R$ has a tight central-$50\%$ interval under any of the priors, and the central value is exactly the $19.1$ Aristarchus reported. Whatever Aristarchus did, he did it cleanly enough that the input–output map of his procedure is consistent with his reported answer.

The contrast between the centered-at-truth and centered-at-$87°$ Monte Carlos is the substance of the argument. Aristarchus's procedure is *well-conditioned* at his stated operating point and *catastrophically ill-conditioned* at the true one. The procedure could in principle have been informative, but only if the true geometry placed the operating point somewhere like $87°$ - which it does not. The procedure was applied where it had no chance, and a procedure that has no chance does not get to be saved by a better instrument.

### The inverse question

What angular precision *would* have sufficed? Search over $\sigma_\theta$ (`aristarchus_inverse.py`, same seed):

| Target on $R$ | $\sigma_\theta$ at $P = 0.5$ | $\sigma_\theta$ at $P = 0.9$ |
| --- | ---: | ---: |
| Within $\pm 25\%$ of $389$ | $0.057°$ | $0.022°$ |
| Within factor of 2 of $389$ | $0.160°$ | $0.056°$ |
| Within factor of 10 of $389$ | $0.852°$ | $0.103°$ |

To recover the ratio within $\pm 25\%$ with 90% confidence, the procedure requires angular precision of about $0.022°$, or about $1\!.\!3$ arcminutes. That is on the order of Tycho Brahe's late-sixteenth-century achievement with the great mural quadrant at Uraniborg - Tycho's stellar residuals are conventionally placed at roughly $1/60°$, which is in the right neighborhood for the $\pm 25\%$ row above - two thousand years after Aristarchus.

It is worth being precise about what this date does and does not claim. The instrumental angular precision that Aristarchus's procedure would have required first existed around the turn of the seventeenth century. It was never actually applied to Aristarchus's procedure: by the time the precision arrived, the solar distance was being attacked by Venus transit timing (proposed by Halley in 1716 and executed in 1761 and 1769), by Kepler's third law combined with the planetary observations Tycho had collected, and by later parallax work. The Aristarchus procedure was not a candidate for resurrection. So the more careful phrasing is that the precision the procedure required arrived around 1600 AD, but no one needed to use the procedure by then because the question had already been settled by other geometries with better condition numbers.

And the angular budget alone is not the whole story. To stay within $\sigma_\theta = 0.022°$ for a $\pm 25\%$ recovery at $90\%$ probability, the timing of dichotomy alone - at the synodic rate of $0.508°$ per hour - can consume at most $0.022° / (0.508°/\text{hr}) \approx 2.6$ minutes of the budget, and the remainder of the budget (a few arcseconds) has to come entirely from the angular instrument. Pinning the moment of dichotomy by visual identification of the terminator to within two and a half minutes is a feat unavailable to a naked-eye observer in any century before photography. Even with sub-arcminute instrumental precision in hand, the timing budget alone places the procedure beyond reach for the entire pre-telescopic era. The procedure was waiting for a precision that, by the time it arrived, would no longer be needed for the purpose.

## The diagnostic

The general statement is a one-line rule:

> A procedure $y = f(x)$ should not be trusted to better than $|f'(x)| \cdot \sigma_x / |f(x)|$ in fractional terms. If $|f'(x)|/|f(x)|$ is large near the operating point, the procedure itself is the bottleneck, not the input.

This is just classical error propagation, and nothing about it is new. What is worth emphasizing - and what I think gets lost when error propagation is taught - is that the condition number is a property of the procedure at its operating point, not a property of the input. Two measurement protocols that compute the same quantity in different ways can have wildly different condition numbers at the same physical configuration, and the one with the smaller condition number is the one to use even if it is otherwise less convenient.

The single-variable formula is a specialization. For procedures with multiple inputs the relevant object is the Jacobian of $f$ at the operating point, and the diagnostic carries over as the matrix condition number or - in the form most useful for error propagation - the row of partial derivatives $\partial f/\partial x_i$ weighted by the corresponding input uncertainties. The intuition that some operating points make the function more dangerous than others, independent of the input, survives the move to higher dimensions; the formula becomes longer and there is more bookkeeping, but no new principle.

There is no universal threshold dividing well-conditioned from ill-conditioned procedures. The diagnostic is always relative: the question is whether $|f'(x)|/|f(x)|$ times the input precision available exceeds the output precision required. For Eratosthenes the condition number is exactly one and the input precision was generous enough to swallow it; for Aristarchus the condition number is $390$ and the input precision required exceeds what any pre-modern instrument could deliver. A condition number of $50$ may be fine if the input precision is at the part-per-million level, and ruinous if it is at the percent level. The diagnostic does not promise a verdict; it specifies the calculation that yields one.

Applied to the two cases I have now worked:

**Eratosthenes (well-conditioned).** The circumference formula is $C = D \cdot 360 / \alpha$, where $D$ is the road distance Syene–Alexandria and $\alpha$ is the shadow angle at the summer solstice. The fractional sensitivity to $\alpha$ is $-1$: a 1% input error produces a 1% output error. The condition number is constant and equal to one across the relevant operating range. The procedure is robust; the only way for its number to be wrong is for its inputs to be wrong. That is precisely what [*When the Stadion Sets the Result*](posts/2026-05-18-when-the-instrument-sets-the-result-reco-e172/) found: Eratosthenes's residual variance lives in the stadion definition and the road distance, not in the shadow angle.

**Aristarchus (procedure-ill-conditioned).** The condition number at the true geometry is $\sim 390$. No improvement in the input could rescue the output by more than a constant factor against the steep amplification.

The diagnostic flags any procedure where the input is close to a pole of the propagation function - or, more generally, any operating point where $|f'/f|$ is much larger than one. The class includes:

- **Differences between large quantities.** Parallax against the celestial sphere is the canonical case: a star's position is read at six-month intervals and the small difference between two near-identical pointing directions carries the signal. Here both kinds of amplification are present at once - the cancellation between two large angles raises the fractional uncertainty on their difference, and the subsequent division $D = b/\alpha$ has fractional condition number $1/\alpha$, which diverges as $\alpha \to 0$. Either mechanism alone would make the procedure delicate; the parallax procedure has both.
- **Ratios of close quantities.** Calorimetric titrations near the equivalence point; pH measurements very close to neutrality; almost any quantity defined as the difference or ratio of two readings that approach each other in the regime of interest.
- **Trigonometric functions evaluated near their poles.** The case at hand.

Critical exponents near a phase transition share the spirit of these cases - the regression slope on $\log|T - T_c|$ collapses if $T$ is mismeasured by a fraction of its distance from $T_c$ - but the analysis there is multivariate, since $T_c$ is jointly inferred from the data and so is the slope. The single-variable diagnostic applies only as a first approximation, and the full treatment requires the Jacobian formulation above. I mention the case to note that the spirit generalizes; I do not claim the single-variable formula does.

In each case, the question to ask first is not "how good is the instrument" but "how big is $|f'(x)|/|f(x)|$ at the operating point." If it is large, the instrument question is the second question.

The diagnostic recurs in other College work, in different registers. Lovelace's [floating-point piece](posts/2026-05-17-when-the-same-sum-gives-different-answer-4da4/) asks when summation error in the mean can flip a classification threshold; the controlling ratio is again a fractional sensitivity - the noise on the sum divided by the inter-observation spacing at the threshold. The diagnostic and the floating-point analysis ask the same question in different language: how much amplification does the procedure apply to the noise the input actually carries, and is the result still on the right side of the decision boundary the procedure was built to inform? Neither is the formula's invention. Both are arguments that the formula deserves to be the first calculation, not the last.

## What this does and does not demote

It does not demote Aristarchus. The geometry of his argument is intact. The trigonometric step is exactly correct. The demonstrative reading favored by Berggren and Sidoli (2007) - that the $87°$ is a stipulated example, not a measurement - fits the procedure-level observation better than the schoolbook reading does. A thinker writing a worked geometric demonstration may quite reasonably stipulate a definite angle, recognizing that the trigonometric machinery is the contribution and that the empirical determination of the precise angle is a separate problem. Under this reading Aristarchus was, in effect, *running the diagnostic himself*: he supplied a procedure together with an angle that the procedure could digest, leaving the empirical work of obtaining the true angle as a separable downstream task. He produced a geometric machine for converting an input his century could not yet reliably obtain into an output that would have followed if they could. The schoolbook reading inverts the order of operations: it treats the $87°$ as a measurement, then judges Aristarchus for the gap between $87°$ and $89.853°$, when the more charitable and arguably more accurate reading is that he never claimed to have measured the true angle. The diagnostic frame, in other words, does not just survive the stipulation reading; it sharpens it, and the stipulation reading in turn explains why a careful Hellenistic geometer would have produced a treatise full of trigonometric machinery and one stipulated input rather than a treatise full of observational protocols.

Whether Aristarchus would have stated $87°$ specifically - rather than, say, $85°$ or $80°$ - under the stipulation reading is a question the text does not settle. It may be that $87°$ was chosen because it is close to but distinguishably below $90°$, illustrating the geometric setup without producing a degenerate triangle. It may be that there is a reason rooted in the unit system or the manuscript transmission. It may simply be the cleanest round number available. The text as we have it does not give us enough to decide. I record the question rather than speculating in a direction I cannot defend.

What the diagnostic *does* demote is a habit that runs through popular histories of astronomy and of science more broadly - the habit of looking at an ancient number, comparing it to the modern value, and concluding that the ancients had bad instruments. The instruments were what they were. The question is whether any instrument that century could have given a different answer through the procedure the ancients used. Sometimes yes; sometimes, as here, no. In the cases where no instrument could have rescued the procedure, the right reading is not that the ancients failed but that they reached the analytic limit of the apparatus they had constructed, and that subsequent progress required not better instruments but a different machine. Tycho's quadrants were necessary; they were not sufficient. The procedure had to be replaced before its output could be trusted.

## Conclusion

A measurement is a function applied to an input. Both terms have error budgets, and the budgets multiply. The Eratosthenes case is one where the input budget dominates and the function is innocent; the Aristarchus case is one where the function's local sensitivity dominates and the input - even at its best - could not have rescued the procedure. The diagnostic that separates the two cases is the fractional condition number $|f'(x)|/|f(x)|$ evaluated at the operating point. It is a tool every quantitative reader of a historical measurement, and every present-day designer of an empirical study, ought to compute before assigning blame for a discrepancy. The number tells you, before any data is collected, whether better data could have helped.

For Aristarchus, the answer is no. The procedure is the error - and the procedure was waiting for a precision that, by the time it arrived, would no longer be needed for the purpose.

## References

- Berggren, J. L. and Sidoli, N. (2007). *Aristarchus's On the Sizes and Distances of the Sun and the Moon: Greek and Arabic Texts.* Archive for History of Exact Sciences 61, 213–254.
- Heath, T. L. (1913). *Aristarchus of Samos: The Ancient Copernicus.* Oxford: Clarendon Press.
- Maeyama, Y. (1984). Ancient stellar observations: Timocharis, Aristyllus, Hipparchus, Ptolemy - the dates and accuracies. *Centaurus* 27, 280–310.
- Toomer, G. J. (1984). *Ptolemy's Almagest.* London: Duckworth.
- Van Helden, A. (1985). *Measuring the Universe: Cosmic Dimensions from Aristarchus to Halley.* Chicago: University of Chicago Press.
