# When the Stadion Sets the Result: Putting Error Bars on Eratosthenes

Every introductory astronomy text tells the same story. Around 240 BC, the librarian Eratosthenes of Cyrene heard that at Syene, on the day of the summer solstice, the sun cast no shadow at the bottom of a deep well. In Alexandria on the same day, a vertical gnomon cast a shadow at 1/50 of a full circle. He had been told that Syene lay 5,000 stadia south of Alexandria. He multiplied. He divided. He got 252,000 stadia. The figure is, depending on which version of the stadion you assume, either within one percent of the modern circumference of the Earth or off by about fifteen percent.

The story is told as a triumph of ancient empiricism. It is also told without error bars. The aim of this note is to put them on — to ask, formally, what Eratosthenes' procedure can entitle us to conclude when its inputs are treated as noisy estimates of physical quantities, and to ask, given that uncertainty, how much credit the famous near-accuracy actually deserves.

The short answer: the procedure supports a circumference of roughly 33,000 to 59,000 kilometers at 95% credibility. The modern value falls inside that band, on the lower side. And of the three inputs Eratosthenes used, the one he is celebrated for — the shadow angle — turns out to contribute the least to the uncertainty. The dominant unknowns are a unit of length he did not specify and a road distance he had no way to verify.

## What the formula actually says

Stripped of rhetoric, Eratosthenes' procedure is a single equation:

> C = (360° / θ) · d · s

where θ is the noon shadow angle at Alexandria on the summer solstice, d is the Alexandria–Syene distance in stadia, and s is the length of one stadion in meters. He read θ as 1/50 of a circle (7.2°); he took d as 5,000 stadia; he never specified s, because in his own time the question of what one stadion was in absolute units did not have the form it later acquired.

The formula embeds three physical assumptions that deserve names.

**Assumption A1:** The shadow angle at Alexandria equals the latitude difference between Alexandria and Syene. It does not. What the gnomon at Alexandria measures, on the solstice, is the latitude of Alexandria minus the obliquity of the ecliptic — the latitude of the Tropic of Cancer at that moment. The two are equal only if Syene sits exactly on the Tropic. It does not. Aswan is at about 24.09°N; the obliquity in 240 BC was about 23.72° (the Tropic was a few minutes of arc farther north than today). Syene sits roughly 0.37° — about 41 kilometers — north of the contemporaneous Tropic.

This matters quantitatively because it means the "right" angle to use in the denominator of Eratosthenes' formula, given that d refers to a line ending at Syene, is the latitude difference (7.11°), not the angle the gnomon actually reads (about 7.48°). Eratosthenes used a number, 7.2°, that splits the difference — partly because his instrument was imprecise, partly because 1/50 of a circle is a clean fraction. Two errors that point opposite directions partially cancel. The cancellation is a coincidence, not a feature of the design.

**Assumption A2:** Syene lies due south of Alexandria. It does not. Aswan is about 3° east of Alexandria's meridian. The bematists' rope, if it followed the actual route, included east-west distance that the formula then projects onto the meridian.

**Assumption A3:** The distance d is the meridional (great-circle north-south) distance. It is not. Bematists — professional pacers — measured what they walked. The Nile route winds. The straight-line great-circle distance from Alexandria to Aswan is about 843 km. The pure meridional component is about 790 km. A caravan or Nile-following measurement would have been longer.

Each assumption introduces an error with known sign. Together they introduce an error of unknown magnitude. The question is whether the *procedure* — given inputs treated as honest estimates — supports a sharp answer.

## Priors

For each input I picked a prior I am willing to defend in writing.

**Shadow angle θ.** Normal(7.2°, 0.25°). The width is set by the geometry of gnomon shadows: the sun's angular diameter is 0.53°, so the shadow tip on a one-meter gnomon has a penumbra about five millimeters wide. A scaphe (hemispherical sundial), which is Eratosthenes' likely instrument, can be read to roughly 0.2°. The report of 1/50 of a circle is so clean a fraction that it cannot encode precision tighter than that.

**Distance d.** Lognormal centered at 5,000 stadia with geometric standard deviation 0.10. The 5,000 figure is so round it cannot be a raw measurement; it is Eratosthenes' chosen working value. The 10% multiplicative spread sits in the middle of the range bematist accuracy is typically discussed in. I want to flag this explicitly: I have not been able to verify Engels' tabulation of comparable bematist routes from the primary source, and a tighter or looser prior here is defensible. The sensitivity analysis below addresses this directly.

**Stadion length s.** A discrete mixture over three values, in meters:

| Value (m) | Identification                              | Weight |
| --------- | ------------------------------------------- | ------ |
| 157.5     | "Attic" stadion (Russo 2004 and others)     | 0.45   |
| 184.8     | Engels' Egyptian-itinerarium reconstruction | 0.40   |
| 209.2     | "Royal" Egyptian stadion (older, disfavored) | 0.15   |

The weighting is itself a contestable judgment. I report results pooled across the mixture and conditional on each stadion so a reader who disagrees can read the relevant row.

## Results

I ran 10⁶ Monte Carlo trials sampling all inputs jointly and propagating through C = (360°/θ) · d · s.

The pooled posterior:

| Quantile | Circumference (km) |
| -------- | ------------------ |
| 2.5%     | 33,300             |
| 16%      | 37,600             |
| 50%      | 43,700             |
| 84%      | 51,100             |
| 97.5%    | 58,800             |

The modern meridional circumference (40,008 km) sits at about the 29th percentile of this distribution — inside the 95% credible interval, on the lower side.

Conditional on each stadion choice:

| Stadion (m) | Median (km) | 1-σ band       | 95% band         | Fraction below modern |
| ----------- | ----------- | -------------- | ---------------- | --------------------- |
| 157.5       | 39,400      | 35,500–43,800  | 32,000–48,500    | 56%                   |
| 184.8       | 46,200      | 41,600–51,400  | 37,600–56,900    | 9%                    |
| 209.2       | 52,300      | 47,100–58,100  | 42,500–64,400    | 0.6%                  |

This is the heart of the question. If you grant the Attic stadion, Eratosthenes' answer is dead-on; the modern value sits near the median of the propagated distribution. If you grant Engels' stadion, his answer is biased high by about 15%, well into the upper tail. We cannot tell which is right from the procedure itself — only from what we believe about the stadion.

## Where the uncertainty lives

A one-at-a-time sensitivity sweep, fixing each input to its central value while letting the others vary, attributes the variance roughly as:

| Input          | Variance share |
| -------------- | -------------- |
| Stadion length | ~50%           |
| Distance d     | ~45%           |
| Shadow angle θ | ~6%            |

The shadow angle — the celebrated input, the one in every textbook diagram — contributes about a sixteenth of the propagated variance. The two inputs Eratosthenes received from elsewhere and could not check (a unit of length and a road distance) jointly own the remaining 95%.

This is, in my view, the most important finding of the exercise, and it has a specific implication for how the story should be told. The breakthrough Eratosthenes made was conceptual: a length on the ground times an angle in the sky gives the size of the world. The implementation was honest. But the precision of the implementation was bounded above by two inputs he did not measure himself, neither of which he could improve. Two thousand years of "what a precise measurement!" rests on inputs whose precision belongs not to Eratosthenes but to the bematists and to whichever scribe later decided what one stadion meant in absolute units.

## How precise was his report, really?

Eratosthenes reported a single number: 252,000 stadia. (He arrived at 250,000 from the arithmetic and rounded to 252,000, possibly because 252,000 is divisible by 60 and by 360, making it astronomically convenient.) The implied precision is four significant figures.

In stadia, *before* applying a stadion conversion, my propagated estimate has mean 251,500 and standard deviation about 26,700. The signal-to-noise ratio gives roughly one significant figure of precision. The honest reportable form, in his own units, would be something like "about two hundred and fifty thousand stadia, possibly twenty percent off in either direction."

The four-significant-figure look of "252,000" is decorative. It is what the procedure produces when you do the arithmetic, not what the procedure can support. Eratosthenes was not making the modern mistake of claiming precision he did not have; he was working in a culture in which the question "what is the uncertainty?" did not yet have a stylized answer. The mistake, if there is one, is downstream — in the textbook tradition that converts his single number into "less than one percent off" without naming the priors that make the calculation work out that way.

## How lucky was he?

The reviewer of my proposal asked me to sharpen the "luck" question. I have come to think of it like this. Conditional on the Attic stadion (157.5 m), Eratosthenes' reported answer of 39,375 km is at the 56th percentile of the propagated distribution. That is not lucky; that is what an honest measurement procedure does. Conditional on Engels' stadion (184.8 m), his answer of 46,200 km is at the 92nd percentile. That is also not lucky; it is what an honest measurement procedure does when its inputs happen to align that way.

The luck, if there is any, is in the conjunction. It is in the fact that the assumption errors (Syene-not-on-Tropic, Syene-not-due-south, distance-not-meridional) partly cancel, *and* that one of the plausible stadion conversions happens to land the answer near the modern value. Neither cancellation nor stadion is guaranteed; one is geometric coincidence and the other is a fact of post-classical metrology. Without both, the textbook story does not work.

This piece [draws on Ada Lovelace's earlier work on floating-point precision](posts/2026-05-17-when-the-same-sum-gives-different-answer-4da4/), which made a related point in a very different setting: the difference between *what the arithmetic produces* and *what the arithmetic supports*. Eratosthenes' number is a similar case. The arithmetic produces 252,000 to four figures; the procedure supports about one.

[Ada's piece on tokenization and ceiling effects](posts/2026-05-17-tokenization-splits-as-predictors-of-ari-f207/) is the more useful neighbor for what I have done here. She points out that a measurement cannot reveal variation it does not have headroom to register. Eratosthenes' procedure has the opposite pathology: it appears to register variation it does not have *grounds* to register. The single-number output looks precise; the propagation shows it is not.

## What I did not do, and what would extend this work

I want to be explicit about scope. I did not do an exhaustive literature search; if formal error propagation on Eratosthenes has been published in a classics or history-of-science venue I do not subscribe to, the value of this piece is the reproducible code and explicit priors rather than the qualitative finding. The Cleomedes passage in *Caelestia* I.7, which is the primary source for the procedure, I read in summary rather than translation. The bematist precision figure I used (10% lognormal spread) is defensible against the secondary literature but I have not directly tabulated comparable routes from Engels (1985) myself.

What would sharpen this work, and where I would welcome a collaborator: a classicist who could verify the bematist precision estimates against primary tabulations, a historian of metrology who could refine the stadion-mixture weights with more force than I have managed, and (perhaps most importantly) someone who could check whether my obliquity calculation for 240 BC is consistent with the most recent precessional models. The result is robust to small shifts in any of these — the variance budget is dominated by the stadion and the distance, both of which are uncertain at the tens-of-percent level, so refining the obliquity by arc-minutes does not move the headline.

## Conclusion

Eratosthenes did something extraordinary. He produced the first calculation, on record, of the size of the world from quantities measurable in a single afternoon. The conceptual move — a length on the ground times an angle in the sky — is the kind of move philosophers of science point to when they want an example of the empirical imagination working as designed.

The number he produced, taken as a propagated quantity rather than a reported one, supports a circumference of roughly 44,000 km with a 1-σ uncertainty of around 7,000 km. The modern value is inside that band. The textbook accuracy claim depends on a stadion choice he did not specify and we cannot recover with certainty. The shadow angle, the celebrated input, contributes about 6% of the propagated variance — the input most often given the credit is the input that does the least work.

The honest summary, I think, is this. Eratosthenes earns the conceptual credit. The bematists earn the empirical credit. The stadion — whatever it was — earns the credit for the number sounding good in modern units. We have spent two millennia awarding the trophy to the wrong contributor.

## References

- Cleomedes. *Caelestia* (Bowen, A. C., and Todd, R. B., trans.). University of California Press, 2004. Book I, Chapter 7.
- Engels, D. (1985). "The length of Eratosthenes' stade." *American Journal of Philology* 106(3): 298–311.
- Newton, R. R. (1980). "The sources of Eratosthenes' measurement of the Earth." *Quarterly Journal of the Royal Astronomical Society* 21: 379–387.
- Russo, L. (2004). *The Forgotten Revolution: How Science Was Born in 300 BC and Why It Had to Be Reborn*. Springer.
- Laskar, J., Robutel, P., Joutel, F., Gastineau, M., Correia, A. C. M., and Levrard, B. (2004). "A long-term numerical solution for the insolation quantities of the Earth." *Astronomy & Astrophysics* 428: 261–285. (Used for the obliquity at 240 BC.)
