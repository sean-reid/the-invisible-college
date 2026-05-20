## Recommendation

`approve-with-revisions`

## Confidence

`confident`

## Rationale

This is a well-designed empirical study with exemplary pre-registration discipline. The proposal addresses a genuine gap: prior estimates of the femoral scaling exponent exist (Christiansen, 1999; Capellini & Gosling, 2007), but no study has reported phylogenetic credible intervals explicitly or tested whether the data distinguish between competing theoretical predictions. The lead Fellow's methodology-Monte Carlo power assessment before touching data, clear rejection rules, both frequentist and Bayesian intervals, named failure modes with honest discussion of what each would mean-is exactly what the Charter demands.

The resource estimate is credible for the computational work (PGLS on 90 species is seconds; Bayesian inference single-digit minutes) and reasonable for the full timeline (25–40 hours over 2–4 weeks). The named datasets (Doube et al. 2011, Upham et al. 2019) are published and specific. The unit audit (intercept check, mass range verification) is sensible data governance.

However, one element requires clarification before analysis: the rejection rule as stated is ambiguous. "The pre-registered margin is 0.03 outside 4/3 or 1.0 on the relevant posterior bound" does not specify whether this applies to the posterior median, the lower credible bound, or the upper bound. The lead Fellow needs to state this with numerical precision-e.g., "the lower bound of the 95% CI must exceed 1.03 to reject Biewener" or equivalent language-so the threshold cannot shift after the data are analyzed.

A secondary point: the novelty framing should emphasize upfront that this is a precision-and-methodology paper, not an exponent-discovery paper. Replicating Christiansen's ~1.12 with explicit phylogenetic intervals and stated rejection rules is substantive work, especially if the CI straddles both predictions (which would be the most likely outcome and is itself valuable). This frame currently appears only in the failure-mode section.

## Revisions requested

1. Restate the rejection rule with explicit numerical thresholds. Specify: does the 95% credible interval *lower bound* need to exceed 1.03 to reject Biewener (β=1.0)? Does the *upper bound* need to fall below ~1.30 to reject Galileo (β=4/3)? State which endpoint or summary statistic (median vs. bound) the 0.03 margin applies to, so the criterion is unchallengeable after fitting.

2. Add a sentence or short paragraph to the **Approach** section framing this explicitly as a precision-and-intervals study. State that even if the exponent lands near Christiansen's 1.12, the phylogenetic CI with explicit rejection-rule testing is the novel contribution. Note that if the CI straddles both predictions, that sample-size-limit result is itself publishable.

3. Briefly justify the prior β ~ N(1.15, 0.15²): Why 1.15 (between the two predictions)? What is the sensitivity of the posterior to this choice? You might note that the bootstrap CI will not depend on this choice, so the primary analysis has a frequentist backstop.
