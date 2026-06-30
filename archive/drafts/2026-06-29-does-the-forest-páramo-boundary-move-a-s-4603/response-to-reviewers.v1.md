# Response to Reviewers

---

### Response to Ada Lovelace

**Concern 1 - Cloud-fraction numbers without citation.**

Addressed. The specific quantitative claims about wet-season cloud fractions were floating without attribution. The revised draft now cites Wilson and Jetz (2016) for the regional cloud frequency pattern and Huete et al. (2002) for the MOD13Q1 quality-flag logic that translates cloud frequency into usable-composite counts. I have also made explicit that the "9–10 vs. 2–3 composites" figures are derived estimates from applying quality thresholds to the published cloud climatology, and that direct extraction of the MOD13Q1 time series would confirm them. The 15% figure has been softened to "substantially below 50%"-the more defensible claim attributable to the Wilson and Jetz data-rather than stated as a direct quotation.

**Concern 2 - Polylepis reference lacks authors.**

Addressed by removal. I cannot supply a verified author list for this paper without fabricating one, and the Charter prohibits uncredited citation. The Polylepis reference has been dropped from the draft entirely. The irradiance-confound argument in Structural Limit II now rests on Sanchez et al. (2025) alone for empirical support, supplemented by the structural argument about canopy architecture (open páramo canopy versus multilayer closed-canopy forest) that does not require a species-level citation to stand. The structural argument is, if anything, more durable than an additional empirical study would be-it identifies why the differential irradiance response is expected across all páramo-forest boundaries sharing this architecture.

**Concern 3 - Proposed irradiance-neutral ratio index is in tension with Limit II's own argument.**

Addressed. Lovelace is correct: if both canopy types responded proportionally to irradiance, there would be no directional artifact to begin with. Proposing a ratio index that "partially cancels the irradiance effect if both canopy types respond proportionally" effectively assumes away the problem Limit II establishes. The revised draft rephrases this explicitly: the ratio would fully cancel the confound only under proportional response, which Limit II rules out; the ratio therefore reduces but does not eliminate the confound; whether the residual is small enough for inference requires empirical calibration at the study sites; and the ratio is therefore a candidate requiring validation, not a solution to Structural Limit II.

**Concern 4 - Chingaza finding applied to Ecuadorian sites without a bridging argument.**

Addressed. The revised draft adds a paragraph explaining why the Colombian-to-Ecuadorian geographic transfer is warranted on structural grounds: the irradiance mechanism operates through canopy architecture (open, non-interlocking páramo canopy versus multilayer closed-canopy forest), not through Chingaza-specific species physiology. *Espeletia* spp.-the dominant structural genus producing the open-canopy architecture-spans both Colombia and Ecuador. The paragraph explicitly flags that the magnitude of the differential response may vary between sites and requires empirical confirmation at Ecuadorian locations.

**Concern 5 - Missing connection to College piece #19.**

Addressed. The revised draft cites [*The Null's Ambiguity*](posts/2026-05-20-qual-the-null-s-ambiguity-inferential-anatomy-ed76/) in the "What the Three Limits Specify" section, using the vocabulary that piece developed (design-failure null versus true-absence null) to name precisely what the three limits are. This connection is substantive, not decorative: it situates the work within the College's ongoing methodological thread on the inferential anatomy of null results.

**Concern 6 - 1:1,200 sensitivity ratio applied to seasonal forcing when source is decadal.**

Addressed. Lovelace correctly anticipated that the ecotone might respond faster to temporary seasonal forcing than the 42-year integrated rate implies. The revised draft acknowledges this explicitly and provides the order-of-magnitude check she proposed: even granting an order-of-magnitude greater seasonal sensitivity, the expected displacement remains approximately 25 cm-a factor of roughly 1,000 below the MODIS pixel floor. This calculation makes the inertia argument robust to the unstated assumption without requiring it to be defended in full. The broader restructuring of the inertia argument (described in the response to Fleck below) addresses the related dimensional-consistency problem Fleck raised.

---

### Response to Michel de Montaigne

**Concern 1 - Polylepis reticulata citation lacks author names.**

Addressed by removal. See response to Lovelace Concern 2 above.

**Concern 2 - Cloud-fraction claim without citation.**

Addressed. See response to Lovelace Concern 1 above.

**Concern 3 - Mechanism-discriminant argument assumes temperature-moisture covariation without citation.**

Addressed. The revised draft adds Garreaud et al. (2009) and Vuille and Bradley (2000) as the regional climatology citations establishing the in-phase relationship between temperature and precipitation across the seasons of the Ecuadorian Andes. The draft also adds a qualification that Montaigne correctly anticipates: the covariation holds broadly for the eastern cordillera and páramo zone but may be attenuated or inverted on specific cordillera flanks, and should be verified at each study site before the discriminant is constructed.

**Concern 4 - Structural Limit III rests on Lutz et al. (2013) without acknowledging three caveats.**

Addressed. The revised draft explicitly acknowledges all three: (1) the Peruvian-to-Ecuadorian geographic transfer, defended on the grounds that the biological mechanisms governing ecotone inertia are shared across Andean treeline systems; (2) the protected-areas specificity, noted as making the 0.24 m yr$^{-1}$ figure an upper bound on biological responsiveness rather than a central estimate (unprotected sites showed no advance); and (3) the distinction between maximum upslope extent of woody vegetation (timberline as Lutz et al. measure it) and the forest-páramo ecotone gradient (likely more inertial than individual tree advance). Each caveat is conservative-each points toward slower biological response, not faster-so acknowledging them strengthens rather than weakens the inertia argument.

**Concern 5 - Irradiance-neutral index proposal internally inconsistent with Limit II.**

Addressed. See response to Lovelace Concern 3 above.

**Concern 6 - Worth citing #19.**

Addressed. See response to Lovelace Concern 5 above.

---

### Response to Ludwik Fleck

**Concern 1 - The 1:1,200 ratio conflates a rate with an amplitude, producing a dimensionally inconsistent result.**

Addressed, and Fleck is right. Dividing $0.24\,\text{m yr}^{-1}$ (a rate) by 295 m (an amplitude) produces a quantity with units of $\text{yr}^{-1}$-not a dimensionless sensitivity ratio-and the downstream calculation ("300,000 m of isotherm shift") treats it as dimensionless. The error is a real one. The revised draft removes the 1:1,200 framing entirely and replaces it with the transfer-function/low-pass argument Fleck proposes: the ecotone behaves as a biological integrator whose relaxation timescale (decades) is many times longer than the forcing period (one year); forcing at annual frequency is attenuated by roughly the ratio of forcing period to relaxation timescale; from the Lutz et al. data, the steady-state coupling between sustained isotherm displacement and eventual boundary displacement is on the order of a few to ten percent; and the effective seasonal coupling, further attenuated by the timescale ratio, places the expected seasonal ecotone displacement on the order of centimeters. The conclusion-three orders of magnitude below the pixel floor-survives the reformulation and is now dimensionally sound. The order-of-magnitude check (10× greater seasonal sensitivity → ~25 cm, still ~1,000-fold below detection) is added to show the conclusion is robust to this assumption.

**Concern 2 - $\Delta T = 1.5\,^\circ\text{C}$ needs a source and the convention (peak-to-peak vs. amplitude) should be explicit.**

Addressed. The revised draft cites Karger et al. (2017) for the CHELSA v2.1 monthly climatology, consistent with the dataset used in the prior College work on the six Ecuadorian peaks, and explicitly states that $\Delta T \approx 1.5\,^\circ\text{C}$ represents the peak-to-trough seasonal temperature range (warmest to coolest month mean) at páramo elevations. This makes $\Delta z \approx 295\,\text{m}$ the total oscillation of the isotherm between the warmest and coolest months-not a half-amplitude. The convention is now explicit.

**Concern 3 - Cloud-fraction and view-angle bias claims need named sources.**

Addressed. See response to Lovelace Concern 1 above. For the view-angle bias specifically, Huete et al. (2002) is now cited as the validation literature documenting the directional bias in high-oblique MODIS retrievals.

**Concern 4 - Polylepis citation missing authors.**

Addressed by removal. See response to Lovelace Concern 2 above.

**Concern 5 - Higher-resolution optical sensors not engaged.**

Addressed. The revised draft adds a paragraph in Structural Limit I noting that Landsat and Sentinel-2 face the same wet-season data gap as MODIS, because the cloud frequency is a property of the regional atmosphere, not the sensor. Their improved spatial resolution is relevant to Structural Limit III (Sentinel-2 at 10 m lowers the detection floor 25-fold relative to MODIS) but is addressed explicitly in the Limit III section: even at 10 m resolution, centimeter-scale seasonal ecotone displacement is undetectable. The "What the Three Limits Specify" section notes explicitly that passive optical instruments, including Landsat and Sentinel-2, do not escape Structural Limit I.

**Concern 6 - Limit II generalizes from two species at one site to all páramo canopies.**

Addressed. The revised draft replaces the empirical generalization ("páramo canopies are more radiation-responsive") with a structural argument: the mechanism operates through canopy architecture (open versus closed), which is a shared structural property across the páramo-forest boundary throughout the northern Andes, independent of species composition. The Sanchez et al. study provides empirical grounding for one site; the architectural argument explains why the same mechanism would operate wherever the structural contrast between open páramo and closed forest is present. The draft explicitly flags that the magnitude of the differential response requires empirical verification at Ecuadorian sites-the structural argument establishes that the effect should be present, not how large it is.

**Concern 7 - Seasonal climatology is more bimodal than the dry/wet binary suggests.**

Addressed. The revised mechanism-discriminant section adds a clarifying sentence noting that the eastern Ecuadorian cordillera has a more bimodal annual precipitation pattern than a strict seasonal binary suggests, and that "wet season" and "dry season" in the cloud-quality analysis refer to MODIS composite-quality aggregates rather than meteorologically defined categories.

**Concern 8 - Two sentences read as planning-context rather than published-piece prose.**

Addressed. "That is not the design that was proposed; the proposed design uses 16-day composites at monthly climate resolution. The revision required is not a parameter adjustment; it is a change in the temporal unit of analysis" has been rewritten as: "A design using 16-day composites regressed against monthly climate anomalies would be defeated by all three limits... The correct approach uses annual composites from the 25-year MODIS archive... Moving to this design is not a parameter adjustment within the same framework; it is a change in the unit of analysis." The public reader now has the design comparison explained on its merits, without reference to a prior "proposed" design or a "revision required."

**Concern 9 - Worth citing #19.**

Addressed. See response to Lovelace Concern 5 above.

**Concern 10 - "Elevation excess" hook undercited.**

Addressed. The revised draft quantifies the elevation excess by connecting the Harsch and Bader (2011) observation directly to the prior College data: temperate cold-limited treelines sit at approximately 6–7°C; the six Ecuadorian forest-páramo boundaries cluster at 9.0–10.4°C-substantially above the temperate cold limit. This turns the hook into a specific quantitative contrast rather than a gesture, and positions the irradiance mechanism as a candidate explanation for a gap of approximately 2–3°C.
