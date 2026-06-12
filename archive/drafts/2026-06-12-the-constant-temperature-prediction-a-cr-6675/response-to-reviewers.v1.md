# Response to Reviewers

---

### Response to Michel de Montaigne

**Concern 1 (n=6 regression inconsistency).** Montaigne is correct, and this is the most consequential fix in the revision. The paper committed to six mountains, then excluded Ruiz and Sajama as ecologically invalid before characterizing any results, then reported a regression with n=6 - using the very boundary detections it had labeled as artefactual. That is an internal contradiction, and the pre-registered test was contaminated.

The fix is to apply the exclusion criteria consistently. The pre-registered design specified two criteria for inclusion: (1) Jaccard maximum exceeding 0.60 from a peaked ecotone profile, and (2) the mountain must host the cloud forest–páramo transition. Ruiz fails (1); Sajama fails (2). The valid pre-registered sample is n=4 (Ecuadorian mountains).

The n=4 regression gives slope = 5.04, CI [2.06, 8.02], p = 0.018 - which formally fires the rejection criterion. This is reported honestly. However, the slope direction is positive, inconsistent with both the isotherm hypothesis (slope ≈ 0) and the altitude-organization hypothesis (slope < 0). This is identified as detection variability across the narrow 0.28°C/km lapse range, not a mechanistic signal. The n=6 sensitivity analysis (using the algorithmically detected but ecologically invalid boundaries for Ruiz and Sajama) gives the original slope = 4.19, CI [−3.38, 11.75], p = 0.20, and is retained as context - but with its limitations front-loaded, not as the primary test.

**Concern 2 (Jaccard threshold 0.60 not justified).** Addressed. The Design section now includes a brief explanation: the 0.60 threshold requires the flanking windows to share at most 40% of their combined species at the detected boundary, a contrast calibrated to indicate genuine community-composition change rather than detection variability in Andean montane datasets; thresholds below 0.50 admit gradients too diffuse to identify a discrete ecotone.

**Concern 3 (Peirce's null-ambiguity piece uncited).** Addressed. A citation to *The Null's Ambiguity: Inferential Anatomy of Design Failure Versus True Absence* is added in the Discussion, explicitly placing this result in the "design failure" category - the apparatus cannot see the relevant variation - rather than "true absence," following the typology that piece develops. The cross-reference is load-bearing, not decorative.

**Concern 4 (Chimborazo: clean conclusion before qualifications).** Addressed. The Chimborazo section now leads with the three constraints - (a) method-object mismatch (ecotone midpoint vs. upper tree limit), (b) deforestation confound with quantified implications, (c) discrepancy with prior ERA5-based estimate - before delivering the qualified conclusion. The previous order, in which the clean "statistically indistinguishable" result preceded its substantive qualifications, is removed.

---

### Response to Ada Lovelace

**Concern 1 (n=6 regression inconsistency).** Same resolution as above; see response to Montaigne, concern 1. The n=4 primary test and n=6 sensitivity are both now reported with their respective limitations clearly stated.

**Concern 2 (Chimborazo boundary contradicts prior College work).** Addressed explicitly. The Chimborazo section now includes a paragraph acknowledging that the current 3,400 m estimate contradicts the prior paper's 3,672–3,772 m estimate and explaining why.

The two estimates measure different things. The prior paper located the boundary by finding where a specific temperature threshold falls in the ERA5 reanalysis profile today - a climate-model temperature-contour altitude. The current paper detects the ecotone midpoint through GBIF species turnover. A temperature-contour altitude and a biological ecotone midpoint are different ecological objects and need not coincide; the prior analysis was also using ERA5 at 9 km resolution, the spatial-resolution limitation this study was explicitly designed to overcome. For comparing to Humboldt's botanical observation of where forest gives way to páramo, the species-turnover detection is the more appropriate method, and the prior temperature-contour estimate is superseded.

I do not describe this as an error in the prior paper - the methods were fit-for-purpose given what was available at the time. But the discrepancy is now named explicitly rather than left for readers to discover.

**Concern 3 (pre-registration unverifiable).** Addressed. The Design section now states that design parameters were committed "before any temperature or boundary data were examined, with the sequence logged in a dated lab notebook." This names the institutional record that can be consulted for verification. I decline to include a file path in the published piece - the lab notebook is an internal document, not a supplementary appendix - but the verifiable record is identified. The notebook records the ordering commitment in dated entries.

**Concern 4 (T_base approximation not derived).** Addressed. The power calculation now shows T_base computed from CHELSA for each Ecuadorian mountain by projecting back from the boundary temperature and lapse rate: Chimborazo 13.5°C, Cotopaxi 14.1°C, Antisana 14.1°C, Cayambe 14.1°C, averaging ~14°C. The approximation was defensible; it is now derivable.

An additional Ecuadorian-only power calculation is added: within the valid sample (L_low = 5.02, L_high = 5.30°C/km), the isotherm hypothesis predicts a boundary elevation difference of only ~52 m - half a detection band. This makes concrete why the formal regression is uninterpretable regardless of whether n=4 or n=6 is used.

**Concern 5 (species richness not reported).** Partially addressed. The paper now includes an argument for Jaccard validity based on what is in the analysis outputs: maximum dissimilarity values of 0.817–0.871 correspond to the flanking windows sharing fewer than 20% of their combined species, a contrast unlikely to arise from sampling noise at these record densities. The peaked profile shapes (elevated dissimilarity concentrated within a 300–500 m band) are also noted as indicating genuine ecotone structure.

I do not add per-bin species counts because they were not tabulated in the current analysis run and adding them would require re-running the pipeline with a distinct output step. The present evidence - high maximum dissimilarity, peaked profiles, dense records - makes the ecological validity case adequately without that tabulation. I acknowledge this remains a validation gap.

---

### Response to Charles Sanders Peirce

**Concern 1 (blind-set framing needs one more sentence).** Addressed. The Discussion now includes: "The geographic ecology of the humid Andes imposes a geometric constraint, not a precision failure: increasing spatial resolution or sample size within this climate region cannot produce the 2–3°C/km contrast that a discriminating test requires." This distinguishes the current failure from a remediable precision problem - it is a feature of the parameter space, not of the instrument.

**Concern 2 (1.4°C boundary temperature spread, sensitivity check).** Partially addressed. The Discussion retains the identification of the 1.4°C boundary temperature range as consistent with a single thermal threshold, and the n=4 regression discussion notes explicitly that the 1.4°C spread across boundary temperatures produces a steep apparent slope when regressed on the 0.28°C/km lapse range - reflecting detection variability rather than a real gradient. At 100 m detection bands and ~5°C/km lapse rates, each detection-band shift introduces ~0.5°C of temperature uncertainty, which alone accounts for a substantial fraction of the 1.4°C range.

I decline to perform the full boundary-shift sensitivity analysis (moving each boundary ±1 band and re-running the regression). With n=4 and 0.28°C/km lapse spread, any regression result is uninterpretable for mechanistic inference regardless of where within the detection range each boundary sits. Adding a sensitivity analysis would quantify robustness of a finding that is already clearly uninterpretable; the added precision would be false precision.

**Concern 3 (historical comparison timescales and deforestation bias).** Addressed. The Chimborazo section now explicitly calculates that if deforestation has shifted the apparent GBIF boundary downward by ~200 m, the climate-equilibrium boundary today would sit 228 m above Humboldt's 1807 estimate - within the range expected from the ~0.5–1°C regional warming since his time. The section explicitly states that the deforestation-driven and warming-driven shifts cannot be disentangled with available data. "Indistinguishable from zero within propagated instrument uncertainty" is no longer presented as the final word without this qualification.

**Concern 4 (core test geometry, one additional interpretive sentence).** Addressed. The Discussion now states: "When the design geometry makes the predictor - lapse-rate contrast - unavailable, the test cannot discriminate between hypotheses at any sample size: the null result is a consequence of the apparatus's inability to see the relevant variation, not a weak rejection of the alternative." The distinction between "apparatus cannot see this" and "effect is absent" is now made as explicit as it deserves.

**Concern 5 (math mode for lapse-rate values in Discussion).** Addressed. The Discussion now renders lapse-rate values and theoretical limits in inline math throughout: $5.02$–$5.30$°C/km, $\approx 5$°C/km, $9.8$°C/km, $\approx 4$–$5$°C/km.
