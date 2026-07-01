# Review by Emmy Noether

- **Role:** secondary
- **Recommendation:** minor
- **Confidence:** confident

## Summary

# Round-2 Review Summary - Emmy Noether

The revision addresses all ten of my round-1 concerns substantively and cleanly: process leakage in §2 and §7 is gone in author-voice rewrites; the load-bearing algebraic invariant ("any power-law in $M$ is monotone in $M$ for every real $\gamma$") is now stated explicitly at the top of §4; the calibration inessentiality is named; log-slopes for all three candidate mechanisms are derived; Rome (1998) is cited at the introduction of $v = L \cdot f_{\max}$; Alexander's positive limb allometry is explicitly noted to preserve monotone form; the sample size for $b_\tau$ is disclosed; the fatigue asymptotic is corrected to "power law $M^{-d}$" in the large-mass regime; and the insect-gigantism piece is now correctly contrasted rather than analogized. One new concern surfaces on rereading: the elephant column of the §4 sensitivity table (361, 228, 145 km/h at $b_\tau = 0.12, 0.17, 0.22$) is arithmetically inconsistent with the exponents stated one line above. The mouse values (21, 31, 45) match the stated exponents under cheetah calibration; the middle elephant value (228) matches; but the two extreme elephant values would require exponents of 0.263 and 0.061, corresponding to a $\pm 0.10$ radius on $\gamma$ rather than the correct $\pm 0.05$ implied by $b_\tau \in [0.12, 0.22]$. The qualitative argument (all three curves monotone; none near 25 km/h at elephant) survives, but the numbers are wrong and should be corrected to 288 and 181 (or the exponents restated) before publication.

## Strengths

# Strengths - Round 2

## What got better

**The structural invariant is now the spine of §4.** In round 1 I asked for a one-line statement of the fact that any power-law in $M$ is monotone in $M$, so the shape failure is qualitative rather than parametric. §4 now opens with that statement directly: "Any power-law model $v_{\text{ceiling}} = k \cdot M^{\gamma}$ is monotone in $M$ for every real $\gamma$. The observed pattern has an interior maximum. No choice of $\gamma$ within any real interval - not just the twitch-exponent interval - reconciles the two." The sensitivity table below is then framed correctly as an illustration of the invariant rather than as the load-bearing argument. This is the strongest structural improvement in the revision and it changes the register of the piece from empirical-robustness-under-test to genuine impossibility.

**Process leakage is cleaned out completely.** The "preregistration/PGLS demoted" language in §2 is gone, replaced by a straightforward statement of the clade-bootstrap result with a quantitative summary statistic ("moves $b_\tau$ by less than 0.02"). The "reviewer of the proposal" and "properly a question for peer review" phrases in §7 are gone; the self-marking as the fifth piece in a scaling register is now made in the author's own voice as a legitimate methodological reflection. A reader of the draft would not know a review process existed. This was the concern all three reviewers flagged and it is discharged.

**The calibration inessentiality is stated where it matters.** §3 now carries the sentence I asked for: "The load-bearing observation, however, is the mass-dependence of $v_{\text{obs}}/M^{0.16}$, which is invariant under the choice of $k$. Recalibrating at any other species would slide the entire ratio column up or down uniformly, but the shape of the descent above intermediate mass - its slope and its magnitude in log-log coordinates - is untouched." A skeptical reader can no longer object that the shape of the residual is a calibration artifact.

**Each candidate mechanism's log-slope is now derived.** §5 in round 1 declared "two of the three are consistent with $-0.5$" without showing the calculations. The revised §5 works each one: fatigue gives $-d \approx -0.5$ via the large-$M$ power-law approximation to $1 - \exp(-c M^{-d})$; bone-stress gives $\approx -0.14$ from $\sigma \sim M^{0.28}$ against constant yield under Biewener's constant-stress model; tendon-compliance gives $\approx 0$ from the storable-vs-required ratio in the naive form. Which two pass and which one fails is now a fact the reader can audit.

**The fatigue asymptotic is corrected.** The word "exponential" in round 1 was misleading at the elephant end where the discrimination among candidates actually happens; §5 now states the two regimes explicitly ("at small $M$ the argument is large and the residual is near unity; at large $M$ the argument is small and $1 - \exp(-c M^{-d}) \approx c M^{-d}$, so the residual falls as a *power law* $M^{-d}$"). The residual log-slope of $-d$ is what enables the direct comparison with observed $-0.5$.

**The Buckingham Pi analogue is developed cleanly and the insect-gigantism piece correctly contrasted.** §7 now distinguishes the two failure modes as I asked. Insect gigantism was parametric-failure (mechanism operative, exponent wrong). This piece is structural-failure (no exponent value in the measured interval produces the observed shape). The Buckingham Pi diagnostic is the correct analogue because there too a vocabulary can travel across a mass range while shedding the mechanism that gave the vocabulary evidential weight. The prior piece is contrasted rather than listed as an analogue - which is what the reviewer asked for and what the algebra supports.

**Sample-size and citation gaps are closed.** §2 now names the sample as "six species with matched fast-twitch preparations" and states that the interval reflects heterogeneity of preparation rather than a taxonomic sample. Rome (1998) is cited at the point where the $v = L \cdot f_{\max}$ identity is introduced, alongside Hill (1950) and Heglund & Taylor (1988). Roberts and Azizi (2011) and Weyand and Bundle (2005) are added where William James's concern about "alive in the literature" applied.

**The non-monotone small-mass ratios are named.** §3 now lists the pattern explicitly (mouse 0.42, squirrel 0.38, hare 0.72, fox 0.62) and marks it as a puzzle distinct from the large-mass descent. The scope decision - naming the pattern here without resolving it - is the correct scope for a piece whose primary object is the large-mass regime. The author is right that resolving the small-mass puzzle is a separate piece; the acknowledgment prevents the reader from mistaking the current piece's coverage for uniform.

## What stayed strong

**The shape-mismatch as structural cut, quantified residual, and three-candidate ending refusing to pick a winner it hasn't earned.** These were the load-bearing strengths in round 1 and they remain load-bearing here. The residual log-slope of $-0.5$ across two decades is still the piece's specific quantitative demand on any candidate mechanism; the algebraic invariant now stated in §4 gives that demand its full force; and the three-candidate accounting still refuses the temptation to laundering a favored mechanism as the answer. The piece knows what it establishes and what it does not.

## Concerns

# Concerns - Round 2

1. **Arithmetic error in the elephant sensitivity values in §4.** The sensitivity claim reads: "At elephant mass ($5000$ kg), they give 361, 228, and 145 km/h" for $b_\tau = 0.12, 0.17, 0.22$ respectively. Under the calibration used everywhere else in the piece ($v(55) = 110$ km/h, $L \sim M^{1/3}$, $\gamma = 1/3 - b_\tau$), the correct elephant values are:
   - $b_\tau = 0.12, \gamma = 0.213: v(5000) = 110 \cdot (5000/55)^{0.213} \approx 288$ km/h
   - $b_\tau = 0.17, \gamma = 0.163: v(5000) \approx 228$ km/h ✓ (matches)
   - $b_\tau = 0.22, \gamma = 0.113: v(5000) \approx 181$ km/h

   The middle case matches; the two extremes are wrong. Reverse-engineering the piece's numbers: 361 requires $\gamma = 0.263$ and 145 requires $\gamma = 0.061$. Those correspond to a $\pm 0.10$ radius around the middle $\gamma = 0.163$, whereas the correct radius from the stated interval $b_\tau \in [0.12, 0.22]$ is $\pm 0.05$. My best guess is that whoever computed the extreme cells used the *width* of the $b_\tau$ interval (0.10) where they should have used the *radius* (0.05). The mouse values in the same sentence (21, 31, 45) are internally consistent with $\gamma \in \{0.21, 0.16, 0.11\}$, so the error is localized to the elephant column.

   The qualitative claim in the following paragraph ("Neither bends the curve into a peaked shape; each is monotone in $M$") is untouched. What is not untouched is the sentence: "The steepest choice ($M^{0.21}$) widens the gap at large mass; the shallowest ($M^{0.11}$) narrows it slightly." The direction is right, but at the true values (288 vs 228 vs 181), "widens" and "narrows slightly" are both understatements of the printed numerical spread (361 vs 228 vs 145). Either the numbers need to be corrected to 288 and 181, or - if the author wants the wider spread the printed numbers imply - the exponents in the display equation need to be changed to $M^{0.26}$ and $M^{0.06}$ with an accompanying explanation of where those exponents come from.

   This is a rigor concern in a piece whose whole method is numerical scaling. It does not undermine the argument, but it should be fixed before publication.

2. **Minor: the tendon-compliance derivation compares required energy per unit distance to storable energy per stride, and the framing of "shortfall" as required/storable rather than storable/required is unusual.** §5 writes "the shortfall in storable-per-required elastic energy scales as $M^{2/3} v_{\text{ceiling}}^2 / M = M^{-1/3} \cdot v_{\text{ceiling}}^2$." The numerator ($M^{2/3} v^2$) is required KE per unit distance; the denominator ($M$) is storable elastic energy per stride. Comparing per-distance to per-stride requires an implicit division by strides-per-unit-distance ($\sim 1/L \sim M^{-1/3}$), which cancels out in the given expression - but the derivation as written is compressed enough that a reader has to work to reconstruct it, and the phrase "storable-per-required" reads as the inverse of what the expression computes. Half a sentence naming the per-stride/per-distance conversion, and switching either the ratio or the phrasing so they agree, would clean this up. The conclusion (roughly flat, therefore not the source of steep large-mass descent) is unaffected.

3. **Very minor: the first-principles derivation "acceleration time scales roughly as $M^{1/3}/v \sim M^{0.17}$" in §5 sits adjacent to the empirical claim "$d$ recovered near $0.5$" without a clean bridge between them.** If the first-principles motivation gives $d \approx 0.17$ and Hirt's fit gives $d \approx 0.5$, that is either two different quantities being compared under the same name or a discrepancy the piece is choosing not to engage. The paragraph would be clearer if it either explicitly noted that the first-principles $M^{0.17}$ scaling is a motivation for the *form* of Hirt et al.'s fit (with the numerical value of $d$ empirically fit rather than derived) or dropped the $M^{0.17}$ scaling line altogether and just cited Hirt et al.'s empirical $d \approx 0.5$ as the input.

Concerns 2 and 3 are exposition-level; concern 1 is a numerical error and is the reason for the "minor" recommendation. All of my round-1 concerns are substantively addressed.
