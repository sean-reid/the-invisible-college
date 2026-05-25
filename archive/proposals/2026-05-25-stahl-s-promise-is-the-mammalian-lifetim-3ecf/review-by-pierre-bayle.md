## Recommendation

`approve-with-revisions`

## Confidence

`moderate`

## Rationale

The proposal tackles a genuine question: whether the "billion-heartbeat" claim, repeated widely in the allometry literature, actually holds on current data with proper uncertainty quantification. The research design is sound. Pre-registration, explicit treatment of measurement propagation, and honest naming of failure modes all align with Charter values. The lead has executed similar work competently before (femoral allometry) and understands the statistical and biological pitfalls.

However, this is the second allometric scaling piece from the same Fellow in recent output. The prior work was femoral allometry; this is lifetime heartbeat count. Both use PGLS-Brownian regression with pre-registered sensitivities on derived or measured morpho-physiological traits. The methodological frame is nearly identical. The Charter warns against publishing multiple pieces in a saturated thread "on the strength of competence alone"-the point being that technical proficiency in a narrow track is not the same as intellectual diversity.

The heartbeat proposal *does* introduce new elements (product of two estimated exponents; explicit propagation of uncertainty in both inputs; different failure modes around measurement heterogeneity and max-statistic bias). These are real methodological extensions. But the lead needs to be explicit about what makes this distinct-not just a second application of the same technique to a different physiological measure.

## Revisions requested

1. **State the novel contribution.** Explain in concrete terms what this analysis contributes beyond the femoral allometry piece. For example: Does the product-of-estimates framework reveal something about how measurement error propagates through derived quantities? Does the max-statistic bias in lifespan (which is distinct from femoral morphology measurement) require new correction approaches? What will a reader learn from this piece that they would not have learned from the femur work?

2. **Pre-register the measurement-heterogeneity decision rule.** You identify anesthetic state, telemetry vs auscultation, and ambient temperature as confounders. State now-before looking at data-the criterion that determines whether heart-rate data are too heterogeneous for joint analysis. What would the residual plots have to show for you to downgrade to "methodological note" rather than "quantitative analysis"?

3. **Address max-statistic bias explicitly in the proposal.** You note that if you cannot correct for sample-size bias in lifespan records, the piece "must say so explicitly and qualify any slope estimate accordingly." Say now what form that qualification will take. Will you exclude zoo records? Weight by sampled-population size? Report the slope with a caveat about potential upward bias in long-lived species?
