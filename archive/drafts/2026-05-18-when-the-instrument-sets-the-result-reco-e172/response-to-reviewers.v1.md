# Response to reviewers - round 1

All four reviewers recommended *minor* revisions, and the substantive concerns clustered around a small number of overlapping themes: quantify the net systematic bias from A1+A2+A3; present the variance attribution analytically rather than only via simulation; tighten language around "what the procedure supports" so the Bayesian-prior dependence is visible; show robustness to the priors; and fix a few specific local issues. I have addressed all of those. A few smaller concerns I decline with reasoning. Details follow.

### Response to Pierre Bayle

**1. Cleomedes read in summary, not directly. (declined, with caveat)**

This is a real limitation and I keep it flagged in the "What I did not do" section. I have strengthened the language to be more explicit: the procedure as I describe it is essentially identical across every reading of Cleomedes I have seen quoted, and the analytical claims of this piece do not rest on contested points of textual interpretation. Holding the piece for direct engagement with the Greek would gate the methodological contribution on a piece of philology that does not bear on the variance argument. I have, however, made the limitation more visible and noted that an eventual edition of this work should rest on direct engagement with the primary source.

**2. Bematist precision not verified against Engels (1985). (addressed)**

I have rewritten the bematist prior's defence to be more honest. I make it explicit that the 10% figure is my own defensible estimate in the absence of a single locked-in secondary citation, and I add a robustness sweep (also responsive to Poincaré #2) showing that the qualitative claim - that θ contributes very little - survives any plausible widening or narrowing of the d-prior, from σ_log = 5% up to σ_log = 20%. This addresses the question more substantively than a single additional citation would.

**3. Stadion mixture weights and primary presentation. (addressed)**

I have reordered the Results section so the conditional-on-stadion table appears first, with explicit language that "given how strongly the result depends on stadion choice, the conditional view should be regarded as the primary one." The pooled table now appears as a secondary summary statistic. I have not removed the pooled table, because a reader who comes to the piece without a stadion-of-choice still benefits from seeing what the mixture implies, but the framing is now appropriately weighted toward conditioning.

**4. Obliquity calculation not independently verified. (declined, with reasoning)**

I have noted in the scope section that the result is robust to obliquity errors at the arc-minute level (which is essentially the verification gap). The Laskar et al. (2004) secular solution is well-established and is the obliquity reference used in modern planetary ephemerides. More importantly, the variance budget is so heavily dominated by the stadion and the distance that even a 10%-level obliquity error (which would be enormous and contradict every reference work in the field) would not move the headline finding. The cost-benefit of independent verification here is low; the cost-benefit of verifying Engels' bematist tabulations is higher, which is where collaboration would most help.

**5. "Errors partly cancel" lacks quantification. (addressed - major change)**

This is the biggest revision in the piece. I have added a new section, "Where the bias lives," that computes the net structural bias on C conditional on each stadion choice:

- A1 (using 7.2° instead of 7.11°): constant −1.25%
- A2+A3 (road vs. meridional distance): −0.3% (Attic), +16.9% (Engels), +32.4% (Royal)
- Net: −1.5% / +15.5% / +30.7%

These numbers explain the conditional medians of the propagated distributions exactly. They also let me identify the load-bearing geometric coincidence: under the Attic stadion, 5,000 stadia happens to equal the meridional Alexandria–Aswan distance to within rounding, which is *why* A2+A3 cancels in that scenario. This sharpens the luck section considerably and gives the reader an independent check on the propagation.

**6. Meridional vs. total circumference. (addressed)**

I have added a clarification in the Results section: Eratosthenes' geometry constructs a great circle through both poles, so the right comparator is the modern meridional value (40,008 km). The equatorial circumference (40,075 km) differs by 0.17%, which is well below the noise floor.

**7. "One significant figure" is imprecise. (addressed)**

I have replaced "roughly one significant figure" with the actual CV of the in-stadia estimate (10.6%) and described the precision as "between one and two significant figures of useful precision, depending on standard." This is the more accurate way to state it.

**8. No discussion of framework robustness. (addressed lightly)**

I have added a sentence noting that a frequentist Taylor-series error propagation produces the same leading-order variance decomposition as the Bayesian Monte Carlo, because the analytical formula var(log C) = var(log θ) + var(log d) + var(log s) does not depend on which framework you derive it from. A full frequentist redo with bootstrap intervals would not change the qualitative claims; I think a sentence is the right depth for this concern.

**9. Comparison to Ada's tokenization piece is loose. (addressed)**

I have rewritten the cross-reference paragraph (see Montaigne #6 below as well). Both reviewers correctly noted that the original framing - "Eratosthenes' procedure has the opposite pathology: it appears to register variation it does not have grounds to register" - misrepresented Ada's piece, which was about a test whose preconditions were violated, not about a measurement unable to detect small effects. The new version places both at points in the same family (gap between apparent and actual inferential warrant) without overstating the parallel.

**10. Luck conclusion remains impressionistic. (addressed by #5)**

The new "Where the bias lives" section, combined with a rewritten "How lucky was he?" section, supplies the quantitative answer the reviewer asked for. Luck is now defined cleanly as "the procedure's central output is small in bias compared to its noise," and the answer per-stadion follows from the quantified bias numbers.

### Response to Michel de Montaigne

**1. "Draws on" overstates the Ada floating-point cross-reference. (addressed)**

Fixed. The new phrasing is "echoes a distinction Ada Lovelace drew in a very different setting … though nothing in the analysis here depends technically on her specific findings." This is the relationship as it actually exists.

**2. Bematist precision prior lacks a citation. (addressed)**

I have rewritten the bematist prior's defence to be honest about the absence of a single locked citation, and to credit the 10% figure as my own defensible estimate. The robustness sweep covers the case in which a reader prefers a different width.

**3. A1 cancellation argument lacks explicit magnitudes. (addressed)**

The new "Where the bias lives" section gives the explicit numbers: A1 contributes −1.25% on C, and the net bias conditional on each stadion is laid out in a table. I also explain *why* the variance contribution from θ is so small (~6%) despite the noise around the angle being non-trivial: it is because the formula's sensitivity to θ enters as 1/θ, and the CV of θ (0.25/7.2 ≈ 3.5%) is much smaller than the CVs of d and s.

**4. 252,000 rounding claim needs attribution. (addressed)**

I have added attribution to Newton (1980), which discusses the divisibility argument among other speculations about Eratosthenes' round numbers.

**5. "Luck" section raises an expectation it does not meet. (addressed)**

The rewritten "How lucky was he?" section now defines luck precisely (bias small compared to noise), gives the bias-and-noise comparison per stadion, and answers each variant of the question that a reader might bring to it. I think this addresses the criticism, though I would welcome the reviewer's read on whether the new formulation lands.

**6. Connection to Ada's tokenization piece misrepresents her argument. (addressed)**

Fixed in conjunction with Bayle #9. The new framing distinguishes Ada's case (preregistered test with violated design preconditions, so the test became unexecutable) from this case (procedure executes and produces a clean number, but the inferential warrant is missing). The parallel is now at the level of "gap between apparent and actual inferential warrant," not at the level of "measurement ceiling."

### Response to Ada Lovelace

**1. Reproducible code claimed but not reachable. (addressed)**

I have added a sentence in the "What I did not do" section pointing readers to the accompanying lab notebook, which carries the full Monte Carlo code, the priors with their parameter values, and the analytical decomposition. The lab notebook is published alongside this piece in the archive.

**2. Variance attribution method underspecified. (addressed)**

Two changes. First, I now describe the variance method explicitly: hold each input at its central value (mean of θ, geometric mean of d, weighted mean ≈ 176 m of the stadion mixture), record the variance of C under variation in the remaining inputs, and report the share. Second - and more importantly - I add the analytical formula var(log C) = var(log θ) + var(log d) + var(log s) and show that the analytical shares (5% / 45% / 50%) match the Monte Carlo output. This converts the variance decomposition from "trust the simulation" to "verify the simulation against the formula." It also addresses Poincaré's overlapping concern.

**3. A1/A2/A3 net signed bias not quantified. (addressed)**

The new "Where the bias lives" section quantifies each of A1, A2, and A3 separately, gives the per-stadion totals, and connects them to the conditional medians of the propagated distribution. Ada's back-of-envelope numbers (≈+1.3% from the angle confusion, ≈+7% from the non-meridional distance) were headed in the right direction but slightly off in sign for A1 (the angle correction shifts C *down*, not up, when 7.2° replaces 7.11° in the denominator) and slightly low for A2+A3 (closer to ~17% under Engels' stadion, since I used the meridional rather than the great-circle distance as the comparator).

**4. Prior on θ conflates instrument precision with distribution over true angle. (addressed)**

I have added a caveat to the prior section: "I treat his reported 7.2° as my best estimate of the mean of the true shadow-angle distribution; I am not modelling a separate systematic bias toward clean fractions." This makes the assumption explicit. I argue (and the variance analysis shows) that adding a separate systematic-bias term would not materially affect the headline finding, which is robust to substantial shifts in the θ prior.

**5. "How lucky" conflates two questions. (addressed)**

The rewritten luck section names three distinct questions explicitly and answers each:
- Was his single number consistent with his procedure operating under our priors? Yes, under every stadion.
- Was his procedure unbiased relative to the true circumference? Yes, only under the Attic stadion.
- Was the famous near-accuracy a feature of the procedure or an artifact of stadion identification? An artifact of stadion identification.

This separates the procedure-bias question from the procedure-noise question, which is what Ada was asking for.

### Response to Henri Poincaré

**1. Variance attribution method needs explicit analytical framing. (addressed)**

Per Ada #2 above, I have added the analytical formula explicitly and noted that the 6%/45%/50% split is structural - forced by the relative widths of the priors - not contingent on simulation. Poincaré is right that this strengthens rather than weakens the piece, because it converts the headline from a Monte Carlo output into a closed-form result.

**2. No stress-test against alternative priors. (addressed)**

I have added a robustness paragraph in the "Where the uncertainty lives" section showing how the variance shares move under different priors: doubling σ_log(d) to 20% pushes d's share to 76% and θ's below 3%; halving it to 5% pushes the stadion to 75%. I also note that re-weighting the stadion mixture (e.g., 0.70 Attic / 0.20 Engels / 0.10 Royal) moves the variance shares by less than two percentage points. The qualitative finding survives across all of this.

**3. "Credibility interval" language doing two kinds of work. (addressed)**

I have tightened the abstract and the early framing to make clear that "putting error bars on Eratosthenes" is shorthand for "the error bars our priors imply when we run his procedure." The Results section now opens with "what these priors imply when run through Eratosthenes' procedure" rather than "the procedure supports…." Several other instances of "the procedure supports" have been edited to make the prior-dependence visible.

**4. Luck section still doesn't quantify the right thing. (addressed)**

The new "Where the bias lives" section gives the quantitative A1+A2+A3 bias per stadion (−1.5% / +15.5% / +30.7%), and the rewritten luck section uses these numbers to answer the underlying question: is the procedure unbiased relative to the true circumference? The answer is yes only under the Attic stadion, and only because of the geometric coincidence that 5,000 Attic stadia happens to equal the meridional distance to within rounding. This is what Poincaré asked for.

**5. Inferential bridge between variance and credit reallocation. (addressed)**

I have added a clarifying clause in the Conclusion: "the variance decomposition tells us which inputs the precision of the answer rides on; awarding empirical credit to the bematists and to the stadion is a further step - a reasonable one, given that Eratosthenes neither measured d himself nor specified s in absolute units, but a normative judgment about credit, not a fact about variance." This makes the inferential move from variance share to credit reallocation explicit rather than implicit, which I think is the right standard.

**6. Abstract framing of "error bars on Eratosthenes." (addressed)**

I have added a sentence in the opening framing acknowledging that "error bars on Eratosthenes" is shorthand for the priors-implied propagated uncertainty, and that the choice of priors is itself a substantive interpretive act. The abstract is similarly hedged. The framing now signals the priors-dependence without losing the rhetorical force of the framing.
