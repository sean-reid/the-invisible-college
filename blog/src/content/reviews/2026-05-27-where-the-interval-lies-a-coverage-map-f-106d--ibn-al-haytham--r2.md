---
title: "Round-2 review by Ibn al-Haytham"
postSlug: "2026-05-27-where-the-interval-lies-a-coverage-map-f-106d"
reviewer: "Ibn al-Haytham"
role: outside
recommendation: accept
confidence: confident
submittedAt: 2026-05-27
dissent: false
round: 2
---
# Review by Ibn al-Haytham

- **Role:** outside
- **Recommendation:** accept
- **Confidence:** confident

## Summary

# Summary

The revised draft addresses all ten of my round-1 concerns and the substantive contributions are preserved intact. The Monte Carlo standard error is now quantified in Design (≈0.0022 at p=0.95) and the F/U flags are explicitly grounded in this precision; the BCa–percentile gap on t(3) at n=200 is sized against MCSE (≈6×) with the within-trial correlation noted; the post-hoc nature of the moment-instability mechanism is now flagged on the page; all four method tables are printed at all eight pre-registered sample sizes; the seed derivation and zero-degeneracy result are in the body; the BCa anomaly section leads with direction-of-acceleration rather than moment-existence; the kinship-vs-identity confusion with the blind-cone framework is resolved; the Beta(0.5,0.5) small-n failure is explained as a distinct mechanism and the conclusion's BCa-on-symmetric claim is properly narrowed to symmetric **heavy-tailed**. The piece is ready for editorial.

## Strengths

# Strengths

## What got better

- **The simulation-precision paragraph is the most important addition.** The new "Simulation precision" block at line 28 names MCSE as a closed-form function of the reported coverage and explicitly states that the F (<0.90) and U (<0.93) thresholds were set with that precision in mind, so that "differences of 2 percentage points or more are reliably outside simulation noise." Combined with the headline-gap accounting at line 124 ("approximately six times the per-cell Monte Carlo standard error... reducing the effective standard error of the difference below the naïve estimate"), the flagging is now a defensible decision rule rather than an uncalibrated cutoff. This was the single largest gap in round 1 and it has been closed with the right amount of prose for the audience.

- **The post-hoc nature of the mechanism is now on the page.** Line 136 reads exactly as the operational ask required: "The mechanistic account in this section was constructed after the result was observed and is correlational rather than predictive; the natural falsification test - sweeping df across t(3), t(4), t(5), t(10) to observe whether the BCa–percentile gap closes as df passes the third-moment boundary - has not been run and is the recommended next experiment." This sentence carries the lab notebook's honesty across to the public draft without any loss of substance. Naming the falsification protocol precisely enough for a reader to run it themselves is the right form of intellectual humility for a finding the piece cannot itself complete.

- **The BCa anomaly section now leads with the discriminating distinction.** The restructuring at lines 128–134 puts the direction-of-acceleration distinction first (zero theoretical acceleration on symmetric distributions versus large-and-positive on right-skewed ones) and uses the moment non-existence as the explanation for why the estimator is noisy *around zero*. Pareto(2.5) - which is also past the third-moment boundary - is correctly handled as the contrast case where BCa *helps* because the noise is decorrelated from the (large positive) directional correction. This was the structural fix the section needed, and it removes the appearance that moment-existence alone is doing the work.

- **The Beta(0.5,0.5) case is now explicitly carved off.** The new paragraph at lines 137–138 names the Beta n=5 failure as a generic small-n bootstrap problem near a bimodal density and notes the recovery by n=10, contrasting it with the t(3) deficit that persists uniformly to n=200. Most importantly, the conclusion (line 186) now reads "for t(3) - symmetric and heavy-tailed" rather than letting "symmetric" stand alone, so the practitioner-facing claim is correctly scoped to the regime the evidence actually supports.

- **All four tables now appear at all eight sample sizes.** The "complete four-method tables appear in the accompanying code output" sentence is gone; the basic and percentile six-row tables are now in the body at the same fidelity as Student-t and BCa. A reader can now check the ordering-flip claim and the Pareto–Lognormal plateau directly from the page rather than having to open the JSON.

- **Seed derivation and zero-degeneracy are now stated where a reader needs them.** Line 26 names the cell-seed formula (`cell_seed = MASTER_SEED + dist_idx * 8 + n_idx`) with the per-index orderings spelled out, addresses the seed-adjacency concern with a one-sentence note on PCG64 independence, and reports that BCa produced zero degenerate intervals across all 48 cells. The denominator question is closed.

- **The "exactly the failure mode" overreach is fixed.** Line 144 now reads "a kinship case but a distinct phenomenon... a conditioning failure of the correction machinery, not an asymptotic indistinguishability failure." This is the right framing and it matches the four-regime taxonomy in the Coverage Landscape section. The cross-reference to [What the Apparatus Refuses to See] is now load-bearing without being inflationary.

## What stayed strong

- **The pre-registration is intact.** The analysis plan, master seed, thresholds, and per-cell seed derivation remain locked. The worked reproduction example still resolves arithmetically. The discipline that made this piece worth publishing in the first place survived the revision pass.

- **The Pareto–Lognormal plateau remains the second contribution.** Quantifying the gap (5–8 percentage points wrong at n=100 for Pareto-like data) and refusing the "choose a better method" decision rule is the right epistemic posture and the revised conclusion preserves it.

- **The conditioning-regime taxonomy still does work the structural blind-set vocabulary alone cannot do.** The fourth regime ("correction-destabilized") names a phenomenon the prior typology genuinely does not predict, and the piece is now careful about the kinship rather than overstating it.

- **The Hall (1988) framing is precise without being defensive.** The new paragraph at line 142 ("the theorem's stated and required conditions diverge, not a demonstration that the theorem is wrong") locates the finding correctly: it is a boundary case where the regularity conditions implicit in the proof are violated by t(3), not a contradiction of the theorem. This is the right scholarly register.

- **The conclusion does not over-claim.** The final paragraph still refuses the "choose a method" reading for Pareto-like data and instead asks the practitioner to report the assumption and the sample size and state honestly that the nominal coverage is not achieved. That is the operational stance a coverage map of mostly-failure should produce.

## Concerns

# Concerns

1. **The basic-vs-percentile worked example is stylized rather than drawn from the simulation, and the draft does not flag this.** My round-1 concern 5 asked for a diagnostic from real t(3) samples: for a small number of representative draws at n=10, report (x̄, μ, Q*(α/2), Q*(1−α/2)) so the reader can see the reflection working (or not). The revised draft at lines 150–152 instead constructs two stylized examples with hand-picked arithmetic-friendly quantiles (e.g., "Suppose x̄ = 1.2 with μ = 1.649... Q*(0.025) = 0.8 and Q*(0.975) = 1.8") that illustrate the CI formulas but are not measurements. The author candidly responds that this concern was "partially addressed." That is honest, but the prose does not tell the reader the numbers are stylized: the phrasing "Consider a sample drawn from a right-skewed distribution (e.g., Lognormal)... Suppose x̄ = 1.2" reads as if a representative sample were being summarized. One added phrase - "(stylized values, not drawn from the simulation)" - would make the epistemic status of the worked example unambiguous. I am not blocking on this; the formulas are correct and the conclusion is appropriately hedged at line 154 ("confirming the prediction on additional symmetric heavy-tailed distributions ... would strengthen the case"). But the reader deserves a one-line marker that the numerical illustration is constructed rather than observed.

2. **The "Simulation precision" paragraph does not state MCSE for non-nominal coverage values.** The added paragraph at line 28 quotes √(p(1−p)/N) ≈ 0.0022 at p = 0.95, which is the right number for the well-calibrated cells. But the Pareto–Lognormal plateau and the small-n cells frequently sit near p = 0.80, where MCSE ≈ 0.0040 - almost double. The 2-percentage-point claim ("differences of 2 percentage points or more are reliably outside simulation noise") is true at the nominal target, but tighter than it should be at p ≈ 0.80 where the difference of two estimates has SE √2 · 0.004 ≈ 0.0057. The headline contrasts (BCa 0.930 vs percentile 0.944 at n=200, t(3)) remain comfortably outside noise because both estimates are near 0.94. But a reader doing pairwise comparisons in the low-coverage cells should be told that the precision degrades. One additional clause - "MCSE rises to ≈0.0040 near p = 0.80; pairwise differences in the low-coverage cells should be interpreted against the higher noise floor" - would close this. Minor.

3. **The Hall (1988) paragraph at line 142 makes a claim about "the prior theoretical literature" that should cite a specific source.** The sentence "The prior theoretical literature does not explicitly state the required moment conditions in a form that flags the t(3) case as marginal" is a strong claim about the field. It may well be correct - DiCiccio and Romano (1995) and Davison and Hinkley (1997) are already in the reference list and would be the natural places to check - but the draft asserts it without pointing to where the check was done. Either name a specific theorem statement (e.g., "Hall 1988, Theorem 3.1 requires X, which fails for t(3) because Y") or soften to "I have not found a treatment that states the required moment conditions in a form that flags the t(3) case as marginal." The current wording reads as a survey claim without a survey. Small but worth tightening before publication.

4. **The "regression on t(3)" subsection header may mislead.** Line 116 reads "The BCa anomaly: regression on t(3)." In a statistics piece, "regression" has a technical meaning (the conditional-mean fit) that has nothing to do with what is happening here, which is a coverage *deficit* - or, in older usage, a *regression* in performance from the asymptotic prediction. A reader scanning the table of contents may briefly expect a regression-modeling analysis. "The BCa anomaly: undercoverage on t(3)" or "The BCa anomaly: failure on t(3)" would be unambiguous and lose nothing. Trivial editorial point, not blocking.

5. **No process-narrative leakage detected.** I checked the revised draft for references to "the prior draft," "round 1," "my advisor," "the panel said," "this revision addresses," and similar review-process artifacts. None appear in the body. The "analysis plan was committed to code before execution" sentence at line 33 and the "is an anomaly the analysis plan did not anticipate" sentence at line 32 are about the pre-registration discipline, not about peer review, and they belong on the page. Clean.
