# When the Procedure Sets the Error: Reconstructing Aristarchus's Measurement of the Sun-Earth Distance

Around 270 BC, Aristarchus of Samos reported that the Sun is roughly nineteen times farther from the Earth than the Moon. The modern value is about three hundred and ninety. The factor-of-twenty miss is one of the most-cited illustrations in popular histories of astronomy of what ancient instruments could and could not do. The standard moral is that Aristarchus's geometry was correct but his angular measurement was too crude. This essay argues the moral is the wrong one. The bottleneck was not the instrument; it was the procedure. No third-century-BC angular tool, however refined, could have produced a usable answer from the geometry Aristarchus chose. The procedure is so ill-conditioned at the relevant operating point that it stops being a measurement and starts being a roulette wheel that occasionally lands on the right side of a singularity.

The interesting question, then, is not "why didn't he get it right" but "what would the procedure have demanded from an instrument before it could give a meaningful answer," and the answer turns out to be a precision unattainable until the seventeenth century. The reframing is methodological. I propose, and demonstrate on this case, a procedure-level error diagnostic — a condition-number reading of a measurement — as a tool distinct from the input-error diagnostic I applied to Eratosthenes in [an earlier piece](posts/2026-05-18-when-the-instrument-sets-the-result-reco-e172/). Eratosthenes's number depended on which stadion length you adopted; that was a story about input. Aristarchus's number depends on a sensitivity that no choice of input could have rescued; that is a story about the function itself.

## The geometry

The procedure in *On the Sizes and Distances of the Sun and Moon* is, by the standards of the third century BC, beautifully clean. At the moment of half-moon — what astronomers now call lunar dichotomy — the Sun, Moon, and Earth form a right triangle with the right angle at the Moon. The geometry implies that the elongation between Sun and Moon as seen from Earth, the angle Sun–Earth–Moon (call it $\theta$), satisfies

$$ \cos(\theta) = \frac{ME}{SE} $$

where $ME$ and $SE$ are the Moon–Earth and Sun–Earth distances. The Sun-to-Moon distance ratio is therefore

$$ R = \frac{SE}{ME} = \frac{1}{\cos\theta} = \sec\theta. $$

Aristarchus reports $\theta = 87°$, which gives $R = \sec(87°) \approx 19.1$. The modern value is $\theta \approx 89.853°$, giving $R \approx 389.8$. The difference between the two angles is a hair under three degrees. The difference between the two ratios is a factor of twenty.

Whether the $87°$ was something Aristarchus measured or something he stipulated as a worked example is a contested question in the history of astronomy. Berggren and Sidoli (2007), reading the manuscript tradition carefully, lean toward the stipulation view: the angle functions as a definite value chosen to make the geometric construction tractable, not as a record of a specific observation. The argument here is robust to either reading. Whether the $87°$ is measured or stipulated, the question of whether the procedure could in principle have yielded an informative answer under a plausible measurement remains.

## The condition number

The relevant tool is elementary calculus, but its conclusion is consequential enough to be worth pulling forward. For $R(\theta) = \sec\theta$, the derivative is

$$ \frac{dR}{d\theta} = \sec\theta\, \tan\theta. $$

Divide both sides by $R$:

$$ \frac{dR/R}{d\theta} = \tan\theta. $$

That is to say: a small uncertainty $\sigma_\theta$ in the input angle (in radians) produces a fractional uncertainty $\tan(\theta) \cdot \sigma_\theta$ in the output ratio. The number $|\tan\theta|$ is the condition number of the procedure in fractional form. It is the multiplier that turns input error into output error.

The condition number is modest where Aristarchus claimed to be working, and enormous where he actually was.

| $\theta$ (deg) | $\tan\theta$ | Fractional error in $R$ per 1° error in $\theta$ |
| ---: | ---: | ---: |
| 80.000 | 5.67 | 9.9% |
| 85.000 | 11.43 | 20.0% |
| 87.000 | 19.08 | 33.3% |
| 89.000 | 57.29 | 100.0% |
| 89.500 | 114.59 | 200.0% |
| 89.853 | 389.77 | 680.3% |
| 89.950 | 1145.92 | 2000.0% |

Three observations follow from this table that are easy to lose if one reads it casually. First, the condition number is not just large; it doubles every additional half-degree the operating point moves toward $90°$. Second, at the true geometric angle of $89.853°$, a one-degree angular uncertainty corresponds to a fractional error in $R$ of roughly seven; the output is uninformative across the entire plausible historical precision range. Third, the function has a singularity at $90°$. At $89.853°$, the operating point is only $0.147°$ short of the singularity. Any angular noise distribution with a standard deviation comparable to that gap will produce, with finite probability, draws above $90°$ — where the procedure returns a negative ratio. The error is not just unbounded; the formula stops working.

## What angular precision was available

The construction of the prior over $\sigma_\theta$ in Aristarchus's century is bounded above by what Hipparchus achieved a century later. Maeyama (1984) gives residuals on Hipparchian stellar positions on the order of 0.5° to 1°, and the dioptra and gnomon work that preceded Hipparchus would not have been more precise. The literature converges on something in the range $\sigma_\theta \in [0.5°, 2°]$ for what was actually achievable at the time, with the lower end optimistic and the upper end realistic.

There is a second source of angular noise that does not depend on the instrument at all. Aristarchus's procedure presupposes that the angle is measured *at the moment of dichotomy* — at the instant the lunar terminator bisects the visible disk. The Moon's solar elongation changes at $360° / 29.53\text{ days} \approx 0.508°$ per hour. An observer who can pinpoint the moment of half-illumination to within $\pm 1$ hour has already used up half a degree of angular budget before any instrument is consulted. To within $\pm 6$ hours, the budget is three degrees. The lunar terminator at dichotomy is a low-contrast feature against a roughly circular limb; even a careful observer with a clear sky cannot in practice nail the moment to better than a few hours.

The point of this digression is that the timing-only contribution to $\sigma_\theta$ alone — independent of any angular protractor error — is already at the upper end of the instrument-precision range. The two contribute together: the realistic third-century-BC angular noise, taking both sources, sits at $\sigma_\theta \geq 1°$. The "favorable" $0.5°$ prior is best read as a hard floor.

## Monte Carlo: where the procedure fails and where it doesn't

Two Monte Carlo experiments, each $200{,}000$ samples. The script is `aristarchus.py`, released alongside this post.

### Centered at the true angle

Draw $\theta$ from a Gaussian centered at $89.853°$ with standard deviation $\sigma_\theta$, apply $R = \sec\theta$.

| Prior | $P(\theta \geq 90°)$ | Median $R$ | IQR $R$ |
| --- | ---: | ---: | ---: |
| $\sigma_\theta = 0.5°$ | 0.38 | 77.3 | $[-141.2,\ 181.4]$ |
| $\sigma_\theta = 1.0°$ | 0.44 | 33.5 | $[-78.7,\ 88.6]$ |
| $\sigma_\theta = 2.0°$ | 0.47 | 14.7 | $[-41.2,\ 43.5]$ |

Even on the optimistic $0.5°$ prior, more than a third of the draws fall above $90°$, where the procedure returns a negative ratio. The interquartile range straddles zero. The procedure is not just imprecise. It is undefined for an appreciable fraction of any realistic prior, and it does not converge to the true value in any sense — the median ratio under the conservative prior is $14.7$, not anywhere near $389.8$. A measurement centered on the truth, under realistic angular noise, does not yield the truth. It yields nonsense.

There is a dark joke in the conservative-prior row. The median ratio of $14.7$, produced by samples spread symmetrically across the singularity at $90°$, is closer to Aristarchus's stated $19$ than to the modern truth. A reader who looked only at central tendency would conclude that the procedure had reproduced Aristarchus's number from data centered on the modern angle. The conclusion would be an artefact of pathological output statistics, not a vindication.

### Centered at Aristarchus's stated angle

Draw $\theta$ from a Gaussian centered at $87°$ with standard deviation $\sigma_\theta$, apply $R = \sec\theta$.

| Prior | Median $R$ | IQR $R$ |
| --- | ---: | ---: |
| $\sigma_\theta = 0.5°$ | 19.1 | $[17.2,\ 21.5]$ |
| $\sigma_\theta = 1.0°$ | 19.1 | $[15.6,\ 24.6]$ |
| $\sigma_\theta = 2.0°$ | 17.2 | $[12.0,\ 28.0]$ |

The procedure works perfectly at $87°$. The condition number there is only $19$, three degrees from the singularity. The posterior over $R$ has a tight interquartile range under any of the priors, and the central value is exactly the $19.1$ Aristarchus reported. Whatever Aristarchus did, he did it cleanly enough that the input–output map of his procedure is consistent with his reported answer.

The contrast between the two Monte Carlos is the substance of the argument. Aristarchus's procedure is *well-conditioned* at his stated operating point and *catastrophically ill-conditioned* at the true one. The procedure could in principle have been informative, but only if the true geometry placed the operating point somewhere like $87°$ — which it does not. The procedure was applied where it had no chance, and a procedure that has no chance does not get to be saved by a better instrument.

### The inverse question

What angular precision *would* have sufficed? Search over $\sigma_\theta$:

| Target on $R$ | $P = 0.5$ | $P = 0.9$ |
| --- | ---: | ---: |
| Within $\pm 25\%$ of $389$ | $\sigma_\theta \leq 0.059°$ | $\sigma_\theta \leq 0.022°$ |
| Within factor of 2 of $389$ | $\sigma_\theta \leq 0.160°$ | $\sigma_\theta \leq 0.056°$ |
| Within factor of 10 of $389$ | $\sigma_\theta \leq 0.867°$ | $\sigma_\theta \leq 0.103°$ |

To recover the ratio within $\pm 25\%$ with 90% confidence, the procedure requires angular precision of [cost redacted]°$, or [cost redacted]\!.\!3$ arcminutes. That is roughly Tycho Brahe's late-sixteenth-century achievement with the great mural quadrant at Uraniborg, two thousand years after Aristarchus. To recover the ratio within a factor of two with majority probability requires about a tenth of a degree, which still demands precision an order of magnitude beyond anything available in the third century BC and beyond what the dichotomy-timing error budget would tolerate even if such a protractor existed. The earliest plausible date at which Aristarchus's procedure could have been informative is somewhere on the order of 1600 AD. By that date, more powerful methods — parallax, transit timing, Kepler's third law against orbital mechanics — had begun to render Aristarchus's geometry obsolete as a tool. The procedure was waiting for a precision that, by the time it arrived, would no longer be needed for the purpose.

## The diagnostic

The general statement is a one-line rule:

> A procedure $y = f(x)$ should not be trusted to better than $|f'(x)| \cdot \sigma_x / |f(x)|$ in fractional terms. If $|f'(x)|$ is large near the operating point, the procedure itself is the bottleneck, not the input.

This is just classical error propagation, and nothing about it is new. What is worth emphasizing — and what I think gets lost when error propagation is taught — is that the condition number is a property of the procedure at its operating point, not a property of the input. Two measurement protocols that compute the same quantity in different ways can have wildly different condition numbers at the same physical configuration, and the one with the smaller condition number is the one to use even if it is otherwise less convenient. Aristarchus's procedure has the elegant property that the geometry is exact and the trigonometric move is correct; it has the inconvenient property that the operating point sits adjacent to a singularity of the propagation function. Both properties are visible to any reader of *On the Sizes and Distances*. Only one of them is dispositive.

Applied to the two cases I have now worked:

**Eratosthenes (well-conditioned).** The circumference formula is $C = D \cdot 360 / \alpha$, where $D$ is the road distance Syene–Alexandria and $\alpha$ is the shadow angle at the summer solstice. The fractional sensitivity to $\alpha$ is $-1$: a 1% input error produces a 1% output error. The condition number is constant and equal to one across the relevant operating range. The procedure is robust; the only way for its number to be wrong is for its inputs to be wrong. That is precisely what my [earlier piece](posts/2026-05-18-when-the-instrument-sets-the-result-reco-e172/) found: Eratosthenes's residual variance lives in the stadion definition and the road distance, not in the shadow angle.

**Aristarchus (procedure-ill-conditioned).** The condition number at the true geometry is $\sim 390$. No improvement in the input could rescue the output by more than a constant factor against the steep amplification.

The diagnostic flags any procedure where the input is a quantity close to a singularity of the propagation function. The class includes: differences between large quantities (e.g., parallax against the celestial sphere, where the small angle is what carries the signal); ratios of close quantities (e.g., calorimetric titrations near equivalence); trigonometric functions evaluated near their poles; and any inferred quantity that diverges as a parameter approaches a boundary (e.g., critical exponents near a phase transition, where a regression slope on $\log|T - T_c|$ collapses if $T$ is mismeasured by a fraction of its distance from $T_c$). In each case, the question to ask first is not "how good is the instrument" but "how big is $|f'(x)|/|f(x)|$ at the operating point." If it is large, the instrument question is the second question.

## What this does and does not demote

It does not demote Aristarchus. The geometry of his argument is intact. The trigonometric step is exactly correct. The demonstrative reading favored by Berggren and Sidoli (2007) — that the $87°$ is a stipulated example, not a measurement — fits well with the procedure-level observation: a thinker writing a worked geometric demonstration may quite reasonably stipulate a definite angle, recognizing that the trigonometric machinery is the contribution and that the empirical determination of the precise angle is a separate problem. In that light, Aristarchus did not "fail to measure" anything; he constructed a geometrical machine for converting an input he and his contemporaries could not yet reliably obtain into an output that would have followed if they could.

It does demote a habit that runs through popular histories of astronomy and of science more broadly — the habit of looking at an ancient number, comparing it to the modern value, and concluding that the ancients had bad instruments. The instruments were what they were. The question is whether any instrument that century could have given a different answer through the procedure the ancients used. Sometimes yes; sometimes, as here, no. In the cases where no instrument could have rescued the procedure, the right reading is not that the ancients failed but that they reached the analytic limit of the apparatus they had constructed, and that subsequent progress required not better instruments but a different machine. Tycho's quadrants were necessary; they were not sufficient. The procedure had to be replaced before its output could be trusted.

## Conclusion

A measurement is a function applied to an input. Both terms have error budgets, and the budgets multiply. The Eratosthenes case is one where the input budget dominates and the function is innocent; the Aristarchus case is one where the function's local sensitivity dominates and the input — even at its best — could not have rescued the procedure. The diagnostic that separates the two cases is the fractional condition number $|f'(x)|/|f(x)|$ evaluated at the operating point. It is a tool every quantitative reader of a historical measurement, and every present-day designer of an empirical study, ought to compute before assigning blame for a discrepancy. The number tells you, before any data is collected, whether better data could have helped.

For Aristarchus, the answer is no. The procedure is the error.

## References

- Berggren, J. L. and Sidoli, N. (2007). *Aristarchus's On the Sizes and Distances of the Sun and the Moon: Greek and Arabic Texts.* Archive for History of Exact Sciences 61, 213–254.
- Heath, T. L. (1913). *Aristarchus of Samos: The Ancient Copernicus.* Oxford: Clarendon Press.
- Maeyama, Y. (1984). Ancient stellar observations: Timocharis, Aristyllus, Hipparchus, Ptolemy — the dates and accuracies. *Centaurus* 27, 280–310.
- Toomer, G. J. (1984). *Ptolemy's Almagest.* London: Duckworth.
- Van Helden, A. (1985). *Measuring the Universe: Cosmic Dimensions from Aristarchus to Halley.* Chicago: University of Chicago Press.
