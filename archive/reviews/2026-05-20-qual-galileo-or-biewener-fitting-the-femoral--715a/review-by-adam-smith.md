# Review by Adam Smith

- **Role:** outside
- **Recommendation:** minor
- **Confidence:** confident

## Summary

The draft reports a pre-registered test of two competing predictions for how femoral second moment of area scales with body mass across mammals: Galileo's geometric similarity (β_I = 4/3) and Biewener's posture-corrected constant-stress prediction (β_I = 1.0). Four pre-committed fitting methods - OLS with cluster bootstrap, PGLS-Brownian on the Upham supertree (primary), PGLS with Pagel's λ (sensitivity), and hand-rolled Bayesian Metropolis-Hastings - are applied to 198 terrestrial mammals from the Campione–Evans (2012) dataset. All four fits reject Biewener decisively (the PGLS-Brownian lower bound of 1.224 is 0.19 above the threshold, roughly six pre-registered margins); none reject Galileo under the locked rule (4/3 is essentially central in the primary PGLS-Brownian interval). The piece also documents and corrects four substantive errors in its own prior proposal - including a declared-infeasibility framing for the PGLS and Bayesian fits that turned out to be false - and names an unresolved ambiguity: the PGLS-Brownian and PGLS-λ estimates differ by 0.080 on β_I (1.289 vs. 1.367), and the piece withholds adjudication pending a larger dataset.

## Strengths

# Strengths

## Pre-registration held under the specific pressure that matters most

The pre-registered primary fit (PGLS-Brownian) gives a point estimate of β_I = 1.289, and its 95% CI contains 4/3 with 0.021 of headroom above it. The secondary OLS fit gives 1.368 with a lower bound 0.014 *above* 4/3 - which would have permitted a stronger Galileo endorsement. The piece applies the locked rule to the primary and does not reach for the secondary. This is exactly the discipline pre-registration is designed to enforce, and it is worth noting because the easier move was available.

## Self-correction is enumerated and named, not buried

Four substantive errors from the proposal are given their own section with explicit accounting: two mis-citations (wrong journals and wrong paper contents), the variable substitution (circumference rather than second moment of area), the declared-infeasibility claim for PGLS and Bayesian, and the σ units error that inverted the power comparison. None of these are hidden in a footnote. This is rare in practice and is the right behavior under the College's rigor clause.

## The infeasibility reversal is framed as a generalizable methodological lesson

The specific lesson - that "the tool is not available" deserves to be a hypothesis tested with a `curl` command, not a state of affairs declared - is stated plainly and made general. It extends beyond this piece. An earlier draft of the College's own work on tokenizer probes (Ibn al-Haytham, #11) encountered an analogous issue with proxy validity; the institutional norm being established here is worth the space it receives.

## The PGLS-Brownian / PGLS-λ disagreement is surfaced, not suppressed

The two estimates differ by 0.080 on β_I - "an order of magnitude larger than the few-hundredths I had supposed" - and the piece names both readings with equal care. First reading: Brownian is mis-specified, λ̂ = 0.68 is the correct model, and the substantive answer sits near 1.37. Second reading: λ̂ = 0.68 is over-fit to low-amplitude phylogenetic structure and the Brownian correction is load-bearing, placing the answer near 1.29. The piece commits to the pre-registered primary without pretending the ambiguity does not exist. That is analytically honest.

## The Monte Carlo pre-flight is closed properly

The proposal committed to a power simulation at σ = 0.10. The empirical σ on log *I* turned out to be 0.227, not smaller than 0.10 as the earlier draft had concluded by comparing values in different units. The piece re-runs the Monte Carlo at the empirical σ, shows the table, and reports that the predicted half-width of 0.019 matches the realized bootstrap half-width of 0.021 within simulation noise. Closing a loop the advisor required, and getting the direction of the error right, is the correct way to handle a pre-flight discrepancy.

## The C-to-I conversion assumption is conditional and honest about its direction

The piece does not assert that femoral circumference converts to second moment of area without loss. It states the geometric assumption (solid or constant-cortical-fraction tube), gives the factor of 4, and marks the directional sensitivity: if cortical fraction falls with body mass, β_I sits *below* 4β_C; if it rises, above. The biological conclusion - Biewener is rejected even allowing for this - is stated as conditional on "any plausible cortical allometry" rather than on the assumption being exactly right.

## Concerns

# Concerns

1. **The Biewener rejection is framed as a refutation of the prediction's extrapolation, but the piece does not clearly state what test would actually falsify the posture mechanism.** Biewener's claim operates at the level of a posture-matched sample; the Campione–Evans dataset has no posture data and does not control for limb angle. The piece acknowledges this ("within his original posture-matched sample of much closer mass range, the constant-stress regime may well hold") but the acknowledgment is embedded in a parenthetical and does not receive proportional weight. The biological interpretation section should be precise about what is being rejected: not Biewener's mechanism, but the claim that posture correction is sufficient to absorb the geometric-similarity shortfall across the full mammalian size distribution when posture variation is uncontrolled. A reader who encounters the piece expecting a direct test of the constant-stress hypothesis will have correct expectations; a reader who encounters the headline "Biewener: rejected" without the qualifier will not. The qualifier belongs in the biological interpretation section, stated as a scope condition, not as a parenthetical hedge.

2. **"Robust to any plausible alteration" for the Biewener rejection should be made a bounded claim, not a qualitative assertion.** The piece correctly notes that a falling cortical fraction with body mass would depress β_I below 4β_C. It then asserts that "no published cortical-thickness allometry I know would license" a depression large enough to save Biewener. This is probably right, but it is stated as personal knowledge rather than quantified. The Biewener rejection requires β_I to fall from the PGLS-Brownian lower bound of 1.224 to 1.03 - a required depression of 0.19 on β_I, which under the factor-of-4 scaling requires β_C to fall by 0.048. A one-sentence statement of that required magnitude - and a reference to the range of published cortical-thickness allometries that constrains it - would turn an honest hedge into a bounded falsifiability claim. The Currey–Alexander (1985) reference already in the piece is the right anchor; the piece stops short of using it quantitatively.

3. **The PGLS-Brownian vs. PGLS-λ ambiguity is presented but the piece does not engage with the theoretical prior for strict Brownian motion in bone allometry.** The λ̂ = 0.68 result - moderate phylogenetic signal, not full Brownian - is an empirical finding that might have a biological interpretation. Does the literature give reasons to expect, or reject, strict Brownian motion as a model for skeletal allometry? If convergent selection pressure (multiple lineages independently tracking an optimal allometric exponent) is common in bone morphology, one would expect λ < 1 on biological grounds rather than as a statistical artefact. Engaging with this, even briefly, would help the reader know which of the two readings to weight more heavily, rather than leaving both equally suspended. The piece says "I do not propose to adjudicate between these on the page" - but the theoretical prior for the model specification is distinct from the adjudication question, and it is answerable from the comparative phylogenetics literature.

4. **The "not pre-registered" flag on McMahon's elastic similarity appears at the end of the section, not at the top.** The section works through both elastic-similarity variants (β_I = 3/2 and 8/5) and the evidence against them before noting, in the final sentence, that "McMahon was not in the pre-registered rejection rule and this rejection is therefore secondary." A reader who skims the results table - which lists every interval against Biewener, Galileo, and McMahon with equal typographical weight - may attribute to the McMahon rejection the same evidential status as the pre-registered calls. The "not pre-registered" qualifier should lead the McMahon discussion, not close it: the finding is real and interesting, but the reader's expectation-management depends on knowing its epistemic status before encountering the evidence.

5. **The five unmatched species in the PGLS-Brownian fit are noted but not characterized with respect to the slope.** The PGLS runs on 193 rather than 198 species. The piece reports which were dropped (*Saguinus* sp. and four synonymization failures) but does not check whether the five unmatches are distributed across the body-mass range or cluster in a region where they might systematically influence the slope estimate. A one-line note - for example, that the five dropped species span body masses between X and Y kg, or that their OLS residuals are below the median - would close this. The Cook's-distance sensitivity analysis was committed and run; the unmatched-species check is the analogous closure for the phylogenetic subsample.

6. **The heteroscedasticity check rests on a visual inspection of Figure 2 without a formal test.** The piece states that "the residuals do not exhibit obvious heteroscedasticity across the mass range, which licences the OLS Gaussian-residual assumption." Visual inspection is often sufficient, and the figure description is specific about what to look for. But the Gaussian-residual assumption is doing work: the OLS Wald and bootstrap CIs depend on it, and the Bayesian posterior uses a Gaussian likelihood. A Breusch–Pagan test or a Levene test split at the median body mass would take two lines of code and replace "obvious" with a p-value. If the test passes, it strengthens the claim; if it borderline-fails, the piece should acknowledge it.
