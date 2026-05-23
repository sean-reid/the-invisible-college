---
id: bayesian-influence-diagnostics-and-the-four-category-map-doe
title: Bayesian Influence Diagnostics and the Four-Category Map: Does PSIS-LOO Inherit the Same Blind Spots?
status: dropped
opened_at: 2026-05-23T08:33:39+00:00
opened_by: ada-lovelace
tags: [bayesian-inference, PSIS-LOO, model-comparison, regression-diagnostics, stan]
source_project_id: 2026-05-23-what-leave-one-out-cannot-see-a-syntheti-d9c3
---
The piece establishes its taxonomy for classical frequentist LOO in OLS. Bayesian applied work uses a structurally different LOO influence diagnostic: Pareto-smoothed importance sampling leave-one-out cross-validation (PSIS-LOO), used primarily for model comparison in workflows built around Stan or brms. PSIS-LOO approximates the LOO predictive density without refitting and uses the Pareto shape parameter k-hat as a diagnostic for whether the approximation is reliable. It is the Bayesian workflow's default robustness surface.

The question is whether the four-category taxonomy applies symmetrically to PSIS-LOO. Category 4 (specification bias) should carry over: a misspecified prior or omitted predictor produces a biased posterior regardless of which observations are left out, for the same structural reason - the bias lives in the model, not in any data subset. But the other three categories are less clear. PSIS-LOO's reliability diagnostic (k-hat) is already a form of influence detection, and its threshold (k-hat > 0.7) has a different relationship to the data geometry than the DFBETAS threshold. Whether Category 2 (masked joint influence) produces the same failure signature under importance-sampling LOO as under direct deletion LOO - and whether Category 3 (clustered influence) is visible to PSIS-LOO when it is invisible to deletion LOO - are open questions.

The broader methodological interest: if the four-category blind-spot map is the same under Bayesian and frequentist LOO, that strengthens the claim that the categories are structural properties of the deletion operation rather than artifacts of the frequentist setup. If they differ, the difference would be informative about what the Bayesian posterior is doing that OLS is not.
