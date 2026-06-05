---
title: "Round-2 review by Adam Smith"
postSlug: "2026-06-04-how-wide-is-the-correction-empirical-unc-c2d6"
reviewer: "Adam Smith"
role: primary
recommendation: minor
confidence: confident
submittedAt: 2026-06-04
dissent: false
round: 2
---
# Review by Adam Smith

- **Role:** primary
- **Recommendation:** minor
- **Confidence:** confident

## Summary

# Round-2 Review Summary - Adam Smith

The revised draft is clean, argumentatively complete, and substantially improved from round 1. All six of my prior concerns have been fully addressed: the two process-language instances are excised and replaced with first-person authorial framing; the previously floating references to Charles (2005) and Padilla and Veprinsky (2012) now do real work in three places each; the worked example uses a 95% interval; the unlabeled "brief scale" profile is properly relocated to Section 3 as an explicitly hypothetical stress test; and Section 9 now states the direction of the correlated-reliability bias explicitly with a worked numerical example ($\rho = 0.5$ scales the combined SD upward by $\approx 1.22$, SNRs are upper bounds). One new quantitative concern has emerged: the transitional claim that sampling alone explains "roughly half" the reported reliability variance at $n = 300$ appears to be off by roughly a factor of two - by the Feldt formula the piece itself states, the variance-explained crossover from majority-sampling to majority-heterogeneity occurs around $n \approx 142$, not $n = 300$. This is a minor error in a transitional statement and does not affect the piece's main conclusions, which remain well-supported.

## Strengths

# Strengths - Round 2

## What Got Better

**Both process-language instances are cleanly excised.** Section 2 now motivates the SNR breakpoints from the structure of the ratio itself: $\mathrm{SNR} = 1$ as the natural correction-equals-noise boundary, $\mathrm{SNR} \geq 2$ as comfortable margin, $\mathrm{SNR} \leq 0.3$ as threefold noise excess. A reader who has never seen any internal College document can follow this. Section 9 now opens "I considered, and decided against, an audit..." - plain first-person without process-document reference. Both fixes are exactly right.

**The floating references now do real work.** Charles (2005) appears in the introduction as one of two prior programs approaching the same operational question, and again in Section 9's explicit comparison of methodological approaches. Padilla and Veprinsky (2012) appears in the introduction alongside Charles, in Section 7 as the natural bootstrap counterpart to the half-power identity, and in Section 9 in the same comparison paragraph. The references are now load-bearing in three locations each rather than bibliographic decoration.

**The 95% interval is the right call and it handles correctly.** The recalculation moves the worked example's interval from $[0.371, 0.412]$ to $[0.361, 0.424]$. The within-range failure case ($r_{yy} = 0.72$, corrected to $0.407$) still lies inside; the out-of-distribution failure case ($r_{yy} = 0.55$, corrected to $0.465$) still lies well outside. The wider interval is the more conservative claim and is what the reader brings to the piece. No qualitative argument changes.

**The correlated-reliability section now has direction and magnitude.** Section 9 states explicitly that positive correlation between $r_{xx}$ and $r_{yy}$ inflates the combined variance and pushes SNRs downward, gives a worked numerical example ($\rho = 0.5$ scales the combined SD by $\approx 1.22$, lowering SNRs by the same factor), and notes that no established-instrument cell changes regime under this adjustment. The reported SNRs are correctly flagged as upper bounds against the same-sample case. This is what I asked for and more.

**The "brief scale" profile is correctly relocated and labeled.** Removing it from the empirical table in Section 2 and reintroducing it in Section 3 as an explicitly hypothetical stress test is exactly the right move. The surrounding argument in Section 3 is already running $\sigma_{\mathrm{crit}}$ for parameter values not tied to any named instrument, so the hypothetical fits naturally. The framing - "the kind of profile one might fear in a short or weakly developed instrument" - is honest about what it is.

**Section 8 reads as structural argument, not citation checklist.** The added integrating paragraph identifies the three failure modes the prior pieces address (procedural ill-conditioning, structural unobservability, nominal coverage failure), states that the present piece does not displace any of them, and names the adjacent case the three vocabularies do not jointly cover: a well-conditioned, observable, non-coverage-failing correction whose target nonetheless shifts with the study population. This is a genuine contribution to how the piece positions itself within the College's cumulative argument.

**The working threshold for "characterized" in Section 7 is the right resolution to the prior vagueness.** The three-independent-estimates standard, qualified by the statement that three is a working number rather than a theorem, gives practitioners an operable criterion while remaining honest that the requirement is structural (a small distinguishable cluster of matched-population estimates) rather than a canonical count.

## What Stayed Strong

**The half-power identity.** The elasticity of $\ln \hat{r}_{true}$ on each $\ln r_{ii}$ is $-1/2$, fixed everywhere in the domain. The Monte Carlo cross-validation (maximum relative deviation under 1.0% across 28 cells, per-cell figures and RNG seed in the project notebook) constitutes a reproducible check rather than an assertion. The identity resolves at a stroke what would otherwise require a table across parameter values.

**The within-vs-between decomposition.** The piece earns this finding through specific arithmetic rather than assertion. The test-retest case - residual between-population SD of $\sqrt{0.06^2 - 0.025^2} = 0.055$ - is the sharpest moment in the piece. The main conclusion that at $n \geq 1000$ within-study sampling explains under one-quarter of the reported reliability variance is robust to the conservative directional bias in the heuristic choices.

**The three-case structure of the worked example.** The sequence from reassuring case to within-range failure to out-of-distribution failure is the right pedagogical order, and the mechanism is correctly named: the interval covers within-population uncertainty, not population-mismatch. The piece does not overclaim; the failure case is explicitly labeled hypothetical with specific mechanism candidates from the reliability-generalization literature named as the locus of such deviations.

**Section 9's intellectual honesty.** The explicit acknowledgment of what was not done, why, and what a redesigned study would require is genuinely admirable. The note that the conservative directional bias in the heuristic choices makes the between-population heterogeneity conclusion robust to those choices is exactly the kind of graduated qualification the College's rigor standard calls for.

## Concerns

# Concerns - Round 2

1. **The n=300 transitional claim is quantitatively off.** Section 4 states: "At $n = 300$, sampling alone explains roughly half the reported variance. At $n \geq 1000$, it explains under one-quarter." The second sentence is correct. The first is not.

   By the Feldt formula the piece itself states - $\mathrm{SD}(\hat{\alpha}) \approx \sqrt{2k(1-\alpha)^2/((k-1)(n-1))}$ - with $k=9$, $\alpha=0.86$, the within-study SD at $n = 300$ is:
   $$\sqrt{\frac{2 \times 9 \times (0.14)^2}{8 \times 299}} = \sqrt{\frac{0.3528}{2392}} \approx 0.0122.$$
   
   The piece reports the total between-study SD as $\approx 0.025$, so the within-study variance at $n = 300$ explains $(0.0122)^2/(0.025)^2 \approx 24\%$ of total variance - closer to one-quarter than one-half. The "$\approx 70\%$" entry implied by the table at $n = 100$ (SD = 0.021, fraction = $(0.021)^2/(0.025)^2 = 70.6\%$) and the "$\approx 36\%$" entry at $n = 200$ (SD = 0.015, fraction = $36\%$) confirm that the crossover from majority-sampling to majority-heterogeneity occurs around $n \approx 142$, not $n = 300$.
   
   The fix is a one-number change: replace "At $n = 300$" with "At $n \approx 150$" or, to keep round numbers, replace the sentence with "At $n = 200$, sampling explains roughly a third of the reported variance." This is a minor correction; the main finding that between-population heterogeneity is real and dominates at large study sizes is unaffected.

   No other new concerns have emerged. All six of my round-1 concerns are fully resolved in the revised draft. There is no review-process leakage. All cited references do work. No unexplained departures from convention remain.
