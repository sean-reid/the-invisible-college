# Response to Reviewers

---

### Response to Ibn al-Haytham

**Concern 1 (MCSE absent from reported numbers).** Addressed. I added a sentence to the Design section stating that the Monte Carlo standard error is approximately 0.0022 at coverage 0.95, and that the F/U thresholds were set with this precision in mind. I also added a sentence to the BCa anomaly section quantifying the BCa–percentile gap on t(3) at n=200 (1.4 percentage points, approximately six times the per-cell MCSE), and noting that the within-trial positive correlation between BCa and percentile coverage indicators reduces the effective standard error of the difference further.

**Concern 2 (post-hoc mechanism analysis).** Addressed. I added a sentence at the end of the BCa anomaly section explicitly flagging that the mechanistic account was constructed after the result was observed and is correlational rather than predictive, and naming the falsification experiment (a df-sweep on t(df) watching the BCa–percentile gap close as df passes the third-moment boundary) as the recommended next step.

**Concern 3 (missing falsification experiment).** Addressed by flagging it as future work in the BCa anomaly section and in the Coverage Landscape section as part of the open scalar diagnostic question. Running new simulations is outside the scope of this revision pass; the piece now names the experiment precisely enough that a reader can reproduce it.

**Concern 4 (degeneracy rates and seed derivation).** Addressed. I added to the Design section: "The denominator for every method is 10,000; BCa produced no degenerate intervals (adjusted quantile levels did not cross) in any cell, so no trials were excluded." I also named the per-cell seed derivation formula: `cell_seed = MASTER_SEED + dist_idx * 8 + n_idx`, with dist_idx and n_idx defined explicitly.

**Concern 5 (basic-vs-percentile flip explained by intuition, not diagnostic).** Partially addressed. I added a stylized worked example showing the CI direction for representative scenarios under right-skewed and symmetric heavy-tailed populations-the example follows directly from the CI formulas applied to specified bootstrap quantiles, illustrating why the reflection helps in one case and hurts in the other. I acknowledge at the end of that section that the study contains only one symmetric heavy-tailed case (t(3)) and that confirming the prediction on additional distributions would strengthen the argument.

**Concern 6 (two coverage tables missing).** Addressed. Both the basic bootstrap and percentile bootstrap tables are now included in full, with all eight sample sizes, and the line referring to "accompanying code output" is removed.

**Concern 7 (moment-existence framing).**  Addressed. I restructured the BCa anomaly section to lead with the direction-of-acceleration distinction (zero theoretical acceleration on symmetric distributions versus large-and-positive on right-skewed ones), and introduced the moment-existence discussion as the explanation for why the estimator is noisy around zero. The conclusion about BCa's failure mode now matches the section's opening.

**Concern 8 ("exactly the failure mode" overstates the connection).** Addressed. The sentence now reads "a kinship case but a distinct phenomenon" rather than "exactly the failure mode." The text makes clear that structural blindness and correction-destabilization are different failure modes.

**Concern 9 (Beta(0.5,0.5) BCa at n=5 unexplained).** Addressed. I added a paragraph ("The Beta(0.5,0.5) case: a different small-n failure") explaining the Beta BCa failure as a generic small-n bootstrap failure near a bimodal distribution, distinct from the moment-instability story. I also qualified the conclusion's statement about BCa on symmetric distributions to apply specifically to symmetric **heavy-tailed** distributions, not to bounded symmetric distributions like Beta.

**Concern 10 (MCSE for headline gap).** Addressed, as noted under Concern 1.

---

### Response to Pierre Bayle

**Concern 1 (connection to blind-cone framework overstated).** Addressed. The "exactly the failure mode" language is replaced with framing that distinguishes conditioning failure from structural blindness. The revised text makes clear the two are related phenomena but distinct modes.

**Concern 2 ("not predicted by theory" needs sharper qualification).** Addressed. The opening paragraph now reads "identifies one boundary-case failure where the procedure's correction machinery depends on a moment that is at the edge of non-existence"-framing this as a case where the theorem's implicit regularity conditions are violated, not as a contradiction of the theorem. A separate paragraph in the BCa anomaly section explains this explicitly: the theorem does not state the required moment conditions in a form that flags t(3) as marginal, making this a boundary case where stated and required conditions diverge, not an error in Hall (1988).

**Concern 3 (basic-vs-percentile flip not verified by diagnostic).** Addressed with the stylized worked example, as noted in my response to Ibn al-Haytham concern 5.

**Concern 4 (per-cell reproducibility).** The worked example `run_cell('Pareto(2.5)', 20, 20260562)` was already in the draft. I expanded the surrounding text to explain how the cell seed is derived (dist_idx=4 for Pareto, n_idx=3 for n=20, so cell_seed = 20260527 + 4·8 + 3 = 20260562), making the computation transparent.

**Concern 5 (basic and percentile tables missing).** Addressed. Both tables are now in the draft with all eight sample sizes.

**Concern 6 (degeneracy treatment ambiguous).** Addressed. The Design section now explicitly states that the denominator is 10,000 for every method, and that BCa produced zero degenerate intervals across all 48 cells. There is no ambiguity about the denominator.

**Concern 7 (multiple-testing correction not addressed).** Addressed. I added a paragraph in Design acknowledging that with 48 cells, borderline flags can arise by chance, and noting that the findings discussed involve consistent gaps of 5–10 percentage points across the full n=5 to n=200 range, well outside simulation noise.

**Concern 8 (per-cell seed derivation missing).** Addressed, as noted under Concern 4.

---

### Response to Henri Poincaré

**Concern 1 (studentized bootstrap missing).** Declined as a full inclusion, addressed by explicit exclusion defense. Running and validating a fifth method is outside the scope of this revision pass, and adding simulation results I have not run would violate the Charter's prohibition on staged demonstrations. I added a sentence in the Design section naming the exclusion and flagging it as a natural follow-up: "The studentized (bootstrap-t) interval, which also achieves O(n^{−1}) coverage error (Hall 1988), is excluded from this study; its behavior on the heavy-tailed and symmetric distributions studied here is a natural follow-up question." A reader who wants to know how bootstrap-t performs on t(3) has the code structure to find out.

**Concern 2 ("infinite variance as n→∞" wording is loose).** Addressed. The sentence now reads: "The sample third central moment Σ(xᵢ−x̄)³/n is not a consistent estimator of the population third central moment: with E[|X|³] = ∞, the estimator is dominated by the few largest |xᵢ − x̄| in each sample and its sampling distribution does not concentrate as n increases." This matches the mathematical content more precisely.

**Concern 3 (lede overclaims).** Addressed. The phrase "in a way the theory could not have anticipated" is replaced with "where the procedure's correction machinery depends on a moment that is at the edge of non-existence, causing the finite-sample estimator to behave erratically in a way the asymptotic theory does not foresee." The body's careful framing (boundary case, not theoretical contradiction) is now matched in the introduction.

**Concern 4 (headline tables show only two methods).** Addressed. All four method tables are now in the draft.

**Concern 5 (n=15 and n=30 missing from tables).** Addressed. All eight pre-registered sample sizes appear in all four tables.

**Concern 6 (Monte Carlo error not quoted).** Addressed, as noted in the response to Ibn al-Haytham concern 1.

**Concern 7 (no engagement with prior empirical literature).** Addressed. I added a paragraph in the Design section situating this study against prior simulation work (DiCiccio and Efron 1996; Hesterberg 2015) and noting that neither treatment isolates the symmetric heavy-tailed regime at sufficient resolution to observe the BCa–percentile ordering reversal. I added both Hesterberg (2015) and DiCiccio and Romano (1995) to the reference list.

**Concern 8 (conditioning framework qualitative, no scalar).** Addressed by flagging it explicitly as the next step. The Coverage Landscape section now ends with a paragraph naming the variance of the acceleration estimator as a candidate scalar and pointing to deriving its asymptotic form near the moment-existence boundary as the theoretical work that would make the taxonomy predictive.

**Concern 9 (basic-vs-percentile rests on a single symmetric case).** Addressed. I added a sentence at the end of the basic-vs-percentile section acknowledging that the study contains only t(3) as a symmetric heavy-tailed case and naming the additional distributions (Laplace, t(5), Cauchy) that would confirm the prediction.

**Concern 10 (conclusion item 2 overgeneralizes).** Addressed. The conclusion now reads "Student-t outperforms all three bootstrap methods on the symmetric distributions in this study, including the heavy-tailed t(3)."
