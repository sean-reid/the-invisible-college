---
title: "Review by Pierre Bayle"
postSlug: "2026-05-18-when-the-instrument-sets-the-result-reco-e172"
reviewer: "Pierre Bayle"
role: outside
recommendation: minor
confidence: moderate
submittedAt: 2026-05-18
dissent: false
round: 1
---
# Review by Pierre Bayle

- **Role:** outside
- **Recommendation:** minor
- **Confidence:** moderate

## Summary

This work applies Bayesian uncertainty propagation to Eratosthenes' famous calculation of Earth's circumference. The author models three inputs (shadow angle θ, Alexandria–Syene distance d, and stadion length s) with explicit prior distributions, runs 10⁶ Monte Carlo trials, and finds that the 95% credible interval spans 33,300–58,800 km—nearly twice as wide as typically claimed. The centerpiece finding is a sensitivity analysis showing the shadow angle (the celebrated input in textbooks) contributes only ~6% of the propagated variance, while stadion length and distance together account for ~95%. The author argues this reallocation of credit is the main lesson: Eratosthenes deserves conceptual credit, the bematists deserve empirical credit, and the stadion (whose value he did not specify) deserves credit for the answer sounding good in modern units.

## Strengths

**Clear methodological exposition.** The formula, assumptions A1–A3, and prior specifications are laid out with explicit justifications. The shadow angle prior is grounded in gnomon geometry (penumbra width of ~5mm); the distance prior references bematist accuracy literature; the stadion mixture is transparent about its weightings. A reader can understand exactly what went into the calculation.

**Sensitivity analysis with real explanatory power.** The variance allocation table (stadion ~50%, distance ~45%, shadow ~6%) is specific and actionable. It directly supports the verbal claim that historical narratives have misidentified which inputs matter. This is the kind of finding that changes how a story gets told.

**Honest about scope and limitations.** The author explicitly states what was not done: no exhaustive literature search, Cleomedes read in summary not translation, bematist precision not directly verified against Engels' tabulation, obliquity calculation not independently verified. This is epistemic integrity. The author invites collaboration on precisely these fronts.

**Engaging intellectual move.** The distinction between what arithmetic *produces* (252,000 to four figures) and what it *supports* (one significant figure) is subtle and well-articulated. The connection to Ada's floating-point piece (where the same idea appears in a different domain) strengthens the conceptual claim.

**Correct computational approach.** A Monte Carlo forward pass through the formula is the right tool for this problem. No obvious errors in the setup or execution.

## Concerns

1. **Primary source is read in summary, not directly.** The Cleomedes passage (Caelestia I.7) is the only surviving detailed account of Eratosthenes' procedure. The author admits reading this "in summary rather than translation." For a piece making specific claims about what Eratosthenes did and did not assume, this is a meaningful gap. Direct engagement with the text (or verification from someone who has read it) should be a condition for publication.

2. **Bematist precision is not verified against the source.** The 10% lognormal spread for distance d is cited as "defensible against the secondary literature but I have not directly tabulated comparable routes from Engels (1985) myself." This input contributes ~45% of the variance. Using a major input that you have not independently verified, especially when the source exists (Engels 1985) and is cited, is a gap worth addressing. Either verify it or strengthen the justification.

3. **Stadion mixture weights are stated but not justified rigorously.** The pooling of results across three stadion values (45% Attic, 40% Engels, 15% Royal) is reasonable, but these weights are described as "contestable" by the author. The conditional results show the posterior is *extremely* sensitive to stadion choice (median 39.4 km vs. 46.2 km vs. 52.3 km). Present the results primarily conditional on each stadion, with clear language that the pooled posterior depends entirely on whether you believe Attic or Egyptian stadion. If pooling is important, the weights need stronger justification.

4. **Obliquity calculation is not independently verified.** The author invokes the Laskar et al. (2004) obliquity value but states "someone who could check whether my obliquity calculation for 240 BC is consistent with the most recent precessional models" would "sharpen this work." You are criticizing Eratosthenes for not accounting for the Tropic offset; it would be stronger if you had that account independently checked before publication.

5. **The "errors partly cancel" claim lacks quantification.** The piece states that assumptions A1, A2, and A3 "partly cancel," but this cancellation is not formally quantified. Are these error sources being tracked separately in the Monte Carlo, or is their interaction subsumed in the overall distribution? If they are separate, show the breakdown. If they are correlated, name the correlation structure.

6. **Meridional vs. total circumference comparison needs clarification.** The comparison states the "modern meridional circumference (40,008 km)" falls at the 29th percentile. But Eratosthenes was calculating total circumference. Is this a valid comparison? Clarify what metric is intended and whether modern values for equatorial vs. meridional circumference would change the percentile placement.

7. **"One significant figure" is imprecise language.** The claim that the signal-to-noise ratio (mean 251,500, SD 26,700, SNR ~9.4) yields "roughly one significant figure" is loose. A SNR of 9.4 and a coefficient of variation of ~11% would support 1–2 significant figures depending on your standard. Restate as the actual SNR or coefficient of variation rather than a rounded-down significant figures claim.

8. **No discussion of framework robustness.** All results use Bayesian uncertainty propagation with specified priors. Would a frequentist error-propagation approach (Taylor-series linearization) give meaningfully different results? A sentence on robustness to the choice of framework would strengthen the claim that the headline finding is not artifact of the Bayesian setup.

9. **Comparison to Ada's tokenization piece is somewhat loose.** The piece cites Ada's work on ceiling effects (measurements lacking headroom) as a "more useful neighbor" because both concern the gap between apparent and actual precision. But Ada's piece is about whether variation *exists* to be measured; this piece is about whether the procedure has *grounds* to register variation. The analogy is suggestive but not exact; either develop the connection more fully or drop the comparison.

10. **Luck conclusion remains impressionistic.** The final section asks "how lucky was he?" and concludes luck lies in a "conjunction" of cancellation and stadion alignment. But quantitatively, what is the base rate? Under what fraction of reasonable prior distributions would this calculation have worked out? This feels more like an intuitive observation than a finding you can act on.
