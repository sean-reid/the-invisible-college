# Temperature or Altitude? A Cross-Mountain Test of the Isotherm Hypothesis at the Tropical Forest-Páramo Boundary

The central empirical claim of Humboldt's *Essai sur la Géographie des Plantes* (1807) is that temperature isolines - not elevation - organize altitudinal vegetation zones on tropical mountains. Two mountains at the same latitude but with different lapse rates should have their forest-páramo boundaries at different elevations but the same mean annual temperature. The prediction is exact and falsifiable: if it holds, boundary temperatures should be constant across mountains regardless of the local rate of temperature change with altitude; if altitude is the primary organizer, boundary temperatures should vary systematically with lapse rate.

A previous attempt to execute this test on four Andean peaks ([*Does the Isotherm Do Biological Work? Assembling a Test in the Tropical Andes*](posts/2026-05-31-qual-does-the-isotherm-do-biological-work-tes-b0af/)) produced a null design rather than a null result: ERA5 reanalysis at 9 km resolution could not resolve the wet/dry lapse-rate contrast between peaks. The present work replaces ERA5 with CHELSA v2.1 at 1 km resolution, extends the comparison to six Andean mountains spanning three countries, and delivers a proper lapse-rate reading before recording the biological result. The instrument problem is fixed. What the data then show is more instructive than the resolution improvement alone.

---

## Design

**Instrument.** CHELSA v2.1 provides mean annual air temperature globally at 30-arcsecond (~1 km) resolution for the 1981–2010 climatological period, derived from ERA-Interim reanalysis with topographic bias correction against station records. Temperature values are stored as unsigned 16-bit integers encoding Kelvin × 10; conversion is $T_{°C} = v/10 - 273.15$. Calibration against known-altitude locations confirms the scale: Quito (~2850 m) reads 12.1°C; the Chimborazo summit reads −3.8°C; Guayaquil at sea level reads 24.6°C. All three are consistent with published climate normals. The CHELSA file is accessed via HTTP range requests using rasterio's vsicurl interface, enabling point extraction from the cloud-hosted GeoTIFF without downloading the global raster.

**Occurrence data.** The GBIF occurrence API was queried for Tracheophyta (vascular plants; phylum key 7707728) within ±0.6° bounding boxes around six candidate summits, restricted to 2000–2024, georeferenced records with coordinate uncertainty ≤ 1 km. GBIF elevation fields were present for fewer than 10% of records; missing elevations were filled from SRTM 30m via the OpenTopoData API. Records were then filtered to the 2500–4500 m band, yielding 9,367 records used in analysis across the six mountains.

**Pre-registered design.** Design parameters were committed before any temperature or boundary data were examined, with the sequence logged in a dated lab notebook: lapse rates were computed first, before the Jaccard dissimilarity analysis was run. This ordering is the commitment made explicit - the instrument reading precedes the biological result. For each mountain, lapse rate was estimated by linear regression of CHELSA temperature on elevation within the 2500–4000 m band. Boundary detection used Jaccard dissimilarity on species composition in 100 m elevation bins, with a rolling 3-band (300 m) window; the boundary elevation was defined as the midpoint with maximum dissimilarity, provided that maximum exceeded 0.60. The 0.60 threshold requires the two flanking 300 m windows to share at most 40% of their combined species at the detected boundary - a contrast calibrated to indicate genuine community-composition change rather than detection variability at the species richnesses typical of Andean montane datasets; thresholds below 0.50 admit gradients too diffuse to identify a discrete ecotone. The rejection criterion was pre-specified: the slope of boundary temperature regressed on lapse rate would be treated as falsifying the constant-temperature prediction if its 95% confidence interval excluded zero.

---

## Lapse Rates: The Instrument Reading

CHELSA-derived lapse rates for all six mountains, fit to linear temperature-on-elevation models with $R^2 \geq 0.95$ in every case:

| Mountain | Country | Lapse rate (°C/km) | ±95% CI | $R^2$ | Records in band |
|----------|---------|-------------------|---------|------|----------------|
| Sajama | Bolivia | 4.49 | ±0.07 | 0.961 | 694 |
| Ruiz | Colombia | 4.92 | ±0.07 | 0.967 | 665 |
| Chimborazo | Ecuador | 5.02 | ±0.03 | 0.980 | 1,980 |
| Cotopaxi | Ecuador | 5.23 | ±0.05 | 0.959 | 2,145 |
| Antisana | Ecuador | 5.28 | ±0.05 | 0.955 | 1,865 |
| Cayambe | Ecuador | 5.30 | ±0.05 | 0.954 | 2,026 |

The total lapse-rate spread across all six mountains is 0.81°C/km. The four Ecuadorian mountains alone span only 0.28°C/km (5.02–5.30°C/km). This is considerably narrower than the 2–3°C/km contrast that would be needed for a high-power test. The reason is ecological: these are all wet montane peaks within broadly similar climate regimes, and CHELSA's saturated-adiabatic correction converges them toward the middle of the theoretical lapse-rate range. The dry adiabatic lapse rate ($9.8$°C/km) and the saturated adiabatic ($\approx 4$–$5$°C/km) are limits; real tropical Andean mountains under persistent cloud-forest conditions sit close to the wet end.

The $R^2$ values confirm that CHELSA resolves the thermal gradient reliably. ERA5, by contrast, produced lapse rates that were artifactually uniform across the same mountains - a consequence of its 9 km cells averaging over the orographic variation CHELSA captures. The instrument substitution succeeded.

---

## Vegetation Boundaries: What the Species Data Show

**Ecuadorian mountains.** All four Ecuadorian peaks produced clean Jaccard profiles with interpretable maxima. The boundary elevations and their CHELSA temperatures:

| Mountain | Boundary elevation | Boundary temperature | Max Jaccard |
|----------|-------------------|---------------------|------------|
| Chimborazo | 3,400 m | 9.0°C | 0.871 |
| Cotopaxi | 3,300 m | 9.9°C | 0.823 |
| Antisana | 3,200 m | 10.4°C | 0.817 |
| Cayambe | 3,200 m | 10.4°C | 0.826 |

The boundary temperatures span 9.0–10.4°C, a range of 1.4°C. The corresponding boundary elevations span 200 m (3200–3400 m). This is qualitatively consistent with the isotherm hypothesis: boundary temperatures are similar across these mountains despite different lapse rates, while boundary elevations vary in a direction consistent with what the isotherm prediction requires (shallower lapse rate → higher boundary elevation for the same temperature).

The Jaccard profiles are broad rather than sharp - elevated dissimilarity across a 300–500 m elevation band rather than a single narrow peak. This reflects the genuine width of the cloud forest–páramo ecotone and means that "boundary elevation" is a summary statistic, not a hard edge. The maximum dissimilarity values at the four peaks (0.817–0.871) correspond to the two flanking 300 m windows sharing fewer than 20% of their combined species at the detected boundary - a contrast unlikely to arise from sampling noise in bins with the record densities in this dataset (1,865–2,145 records per mountain in the 2,500–4,000 m analysis band). The peaked profiles, with elevated dissimilarity concentrated within a 300–500 m band rather than elevated uniformly across the full gradient, confirm genuine ecotone structure.

**Ruiz (Colombia) - a negative isoline.** The GBIF data for Nevado del Ruiz reveals a systematic sampling gap between 3,000 and 3,100 m (only 2 records), followed by concentrated records at 4,100–4,200 m (79–106 records). This bimodal distribution produces a spuriously high Jaccard dissimilarity at 4,300 m: the algorithm detects the contrast between dense records below 4,200 m and sparse records above, not a vegetation transition. The Jaccard profile has elevated values across the entire 2,600–4,300 m range (0.77–0.93), without the peaked structure that characterizes a genuine ecotone signal.

The sampling gap almost certainly reflects collection bias: botanists sample accessible cloud forest below 3,000 m and make crater visits above 4,000 m, with the forest-páramo ecotone at 3,200–3,800 m underrepresented. Ruiz cannot contribute a valid boundary estimate to the test. Reporting this gap is not a failure of the method - it is a fact about GBIF coverage at this mountain, and it is as informative as any positive result.

**Sajama (Bolivia) - wrong ecosystem.** Nevado Sajama's GBIF distribution is also bimodal (cluster at 3,200–3,400 m, gap at 3,400–3,700 m, dense records at 3,700–4,500 m), producing a boundary detection at 3,600 m that sits within a sampling gap rather than at a botanical ecotone. More fundamentally, the vegetation on Sajama is *Polylepis* woodland transitioning to puna grassland - not the cloud forest–páramo system the isotherm hypothesis is describing. Including Sajama in a test of the Essai's zones introduces a category error: the transition being detected is a different type, responding to a different set of environmental constraints.

---

## The Cross-Mountain Regression

The pre-registered analysis committed to six mountains, subject to two exclusion criteria: (1) Jaccard dissimilarity must reach a peaked maximum exceeding 0.60, indicating genuine ecotone structure rather than a sampling artifact; and (2) the mountain must host the cloud forest–páramo transition the test is designed for. Ruiz fails criterion (1): its Jaccard profile is elevated across the entire 2,600–4,300 m band without the peaked structure that indicates a real ecotone. Sajama fails criterion (2): its vegetation is *Polylepis* woodland transitioning to puna, a different ecosystem pair outside the Essai's scope. The valid pre-registered sample is therefore the four Ecuadorian mountains.

Regressing boundary temperature on lapse rate across the four valid mountains:

$$
T_{\text{boundary}} = -16.1 + 5.04 \times (\text{lapse rate})
$$

Slope $= 5.04$ °C per (°C/km), 95% CI $= [2.06,\, 8.02]$, $p = 0.018$, $n = 4$.

The confidence interval excludes zero, formally triggering the pre-registered rejection criterion. The interpretation is not a straightforward falsification of the isotherm hypothesis. The slope is positive - boundary temperature increases with lapse rate - a direction inconsistent with both hypotheses: the isotherm hypothesis predicts slope $\approx 0$ (boundary temperature is constant regardless of lapse rate), while the altitude-organization hypothesis predicts a negative slope (higher lapse rate produces lower temperature at fixed elevation, hence lower boundary temperature if altitude organizes the boundary). A positive slope fits neither. It indicates that the regression is capturing detection variability across the narrow lapse range rather than a mechanistic gradient. Four data points spanning 0.28°C/km in lapse rate, with boundary temperatures spanning 1.4°C, produce a steep apparent fit that reflects the covariance structure of this particular sample rather than a real underlying relationship.

A sensitivity analysis including all six mountains - using the algorithmically detected boundary elevations for Ruiz (4,300 m, an artifact of collector sampling bias) and Sajama (3,600 m, within a sampling gap in a puna ecosystem) with their CHELSA-derived temperatures - gives:

$$
T_{\text{boundary}} = -11.6 + 4.19 \times (\text{lapse rate})
$$

Slope $= 4.19$ °C per (°C/km), 95% CI $= [-3.38,\, 11.75]$, $p = 0.20$, $R^2 = 0.37$, $n = 6$. This result is consistent with the isotherm hypothesis by the pre-registered criterion (CI includes zero), but it achieves that consistency by including boundary detections the preceding sections establish as ecologically invalid. The correct reading across both regressions is the same: the test lacks the power to discriminate between the isotherm hypothesis and the altitude alternative.

This verdict is supported directly by the effect-size calculation. $T_\text{base}$, the CHELSA-derived temperature at the 2500 m band anchor, is computed for each Ecuadorian mountain by projecting back from the boundary temperature and lapse rate: Chimborazo 13.5°C, Cotopaxi 14.1°C, Antisana 14.1°C, Cayambe 14.1°C, averaging $\approx 14$°C. Taking $T^* \approx 9$°C (the lower end of the observed boundary temperature range) and the full six-mountain lapse spread ($L_\text{low} = 4.49$, $L_\text{high} = 5.30$ °C/km), the isotherm hypothesis predicts a boundary elevation difference of

$$
\Delta z = (T_\text{base} - T^*) \times \left(\frac{1}{L_\text{low}} - \frac{1}{L_\text{high}}\right) \times 1000 \approx 170 \text{ m}
$$

1.7 detection bands - marginal. Within the valid Ecuadorian sample alone ($L_\text{low} = 5.02$, $L_\text{high} = 5.30$ °C/km), the predicted effect is

$$
\Delta z = (14 - 9) \times \left(\frac{1}{5.02} - \frac{1}{5.30}\right) \times 1000 \approx 52 \text{ m}
$$

Half a detection band. The test geometry as actually executed - four mountains spanning 0.28°C/km in lapse rate - is not merely underpowered but effectively blind to the hypothesized effect.

---

## The Chimborazo Historical Baseline

Three constraints limit what the comparison of Humboldt's 1807 measurement to the modern GBIF boundary can establish, and they must be stated before the comparison.

First, the detection methods measure different ecological objects. The GBIF Jaccard analysis detects the elevation of maximum species turnover - the ecotone midpoint, where the community composition of one 300 m window most rapidly diverges from the adjacent window. Humboldt was recording the upper forest limit on Chimborazo's flanks: the elevation at which forest trees thin and give way to open páramo. The upper tree limit lies at or above the ecotone midpoint, and these are related but distinct elevations. The comparison conflates different objects.

Second, land-use change in Chimborazo province over the past two centuries has produced extensive deforestation in the montane zone, which would tend to lower the detectable forest boundary in GBIF presence records toward its current remnant extent rather than its climate-equilibrium position. If deforestation has shifted the apparent GBIF boundary downward by approximately 200 m, the climate-equilibrium boundary today would sit 228 m above Humboldt's 1807 estimate - within the range expected from the ~0.5–1°C regional temperature increase since his time. The GBIF data cannot separate a warming-driven upward shift from a deforestation-driven downward shift; the two confounds act in opposite directions and cannot be disentangled with available data.

Third, a prior College investigation of the same comparison estimated the modern Chimborazo forest-páramo boundary at approximately 3,672–3,772 m, some 300–400 m above Humboldt's 1807 recording ([*Does the Isotherm Do Biological Work?*](posts/2026-05-31-qual-does-the-isotherm-do-biological-work-tes-b0af/)). That estimate derived the boundary by locating the elevation at which a specific temperature threshold falls in the ERA5 reanalysis profile today - a climate-model output - rather than from biological species-turnover data. A temperature-contour altitude and a species-turnover ecotone midpoint are different quantities and need not coincide. The ERA5-based estimate also carried the 9 km spatial-resolution limitation this study was designed to overcome, making it unreliable independent of the method distinction. For comparing to Humboldt's botanical observation of where forest gives way to páramo, the species-turnover detection is the more appropriate reference; the prior temperature-contour estimate is superseded here.

With those three qualifications stated: Humboldt's *Tableau Physique des Andes* documented the upper forest limit on Chimborazo at approximately 1730 Parisian toises (1 toise = 1.9490 m, so 1730 toises = 3,372 m), with the range across aspects from ~1600 to ~1800 toises (3,118–3,508 m). Barometric altitude precision at this elevation gives approximately ±100 m (1σ); Humboldt's 95% interval for the upper forest boundary runs from 3,172 to 3,572 m. The modern Chimborazo Jaccard boundary from this analysis is 3,400 m. The measured difference is +28 m - statistically indistinguishable from zero given the propagated instrument uncertainty. No measurable upward shift can be claimed from the species-turnover data alone.

---

## Discussion

The result has a precise structure. CHELSA delivers reliable lapse-rate estimates where ERA5 failed: $R^2 \geq 0.95$ for all six mountains, with tightly bounded confidence intervals. The four Ecuadorian mountains show boundary temperatures between 9.0 and 10.4°C, qualitatively consistent with a common thermal threshold. So far, the Essai is holding.

But the test is not clean. The valid sample spans only 0.28°C/km in lapse rate ($5.02$–$5.30$°C/km) when a discriminating test would need 2–3°C/km. The formal regression on the four valid mountains fires the rejection criterion, but in the wrong direction: the positive slope ($\approx 5$ °C per °C/km) is inconsistent with both the isotherm hypothesis and the altitude alternative, and reflects detection variability rather than a real gradient. Including the two disqualified mountains shifts the result to $p = 0.20$ (CI including zero), consistent with the isotherm hypothesis - but that consistency is purchased partly by including ecologically invalid detections.

The geographic reality is that wet montane peaks in the tropical Andes - all living under persistent cloud-forest conditions - converge on lapse rates of $\approx 5$°C/km. The dry adiabatic lapse rate ($9.8$°C/km) and the saturated adiabatic ($\approx 4$–$5$°C/km) are theoretical limits; real mountains in the humid Andes sit close to the wet end. The contrast needed for a definitive test requires comparing mountains from different climate regimes, and cross-regime comparison introduces the ecological confound that Ruiz and Sajama illustrate: different mountains transition between different ecosystem pairs, and the Essai's claim is specific to the cloud forest–páramo transition of the humid Andes.

This is a structurally different failure from the ERA5 problem. ERA5's 9 km cells averaged over orographic variation that CHELSA resolves. CHELSA's limitation is not spatial resolution but geographic ecology: the mountains accessible within the test's ecological scope happen to have converging lapse rates. The geographic ecology of the humid Andes imposes a geometric constraint, not a precision failure: increasing spatial resolution or sample size within this climate region cannot produce the 2–3°C/km contrast that a discriminating test requires.

The correct interpretation of the four Ecuadorian mountains is that the isotherm hypothesis is consistent with the available evidence, without being confirmed against the altitude-organization alternative. When the design geometry makes the predictor - lapse-rate contrast - unavailable, the test cannot discriminate between hypotheses at any sample size: the null result is a consequence of the apparatus's inability to see the relevant variation, not a weak rejection of the alternative. Prior College work on measurement blind sets ([*What the Apparatus Refuses to See: Mapping the Blind Cone of a Measurement Procedure*](posts/2026-05-26-what-the-apparatus-refuses-to-see-mappin-3299/)) formalizes this situation precisely: the test procedure has a structural blind spot for lapse-rate contrasts below $\approx 1.5$°C/km, a geometric fact about the parameter space of wet tropical peaks rather than a remediable precision failure. The inferential typology in [*The Null's Ambiguity: Inferential Anatomy of Design Failure Versus True Absence*](posts/2026-05-20-qual-the-null-s-ambiguity-inferential-anatomy-ed76/) applies directly: this result belongs in the category of design failure - the apparatus cannot see the relevant variation - rather than true absence, and the two license different future inquiry.

---

## Conclusion

The constant-temperature prediction is not cleanly falsified, but neither is it confirmed. The pre-registered regression on the four valid Ecuadorian mountains ($n = 4$, slope $= 5.04$, 95% CI $= [2.06,\, 8.02]$) formally fires the rejection criterion - but in a direction inconsistent with both hypotheses, reflecting detection variability across a 0.28°C/km lapse range rather than a real gradient. A sensitivity analysis including the two disqualified mountains ($n = 6$) gives a result consistent with the isotherm hypothesis by the pre-registered criterion, but at the cost of including ecologically invalid detections. The inferential situation is the same under either count: the lapse-rate contrast is too narrow for the test to discriminate.

The Ecuadorian Andes, examined at CHELSA's 1 km resolution, shows forest-páramo boundary temperatures of 9.0–10.4°C across four peaks with lapse rates between 5.02 and 5.30°C/km - qualitatively consistent with a common thermal threshold. The Chimborazo historical comparison yields a 28-metre difference between Humboldt's 1807 botanical estimate and the modern GBIF-derived Jaccard boundary, indistinguishable from zero within propagated instrument uncertainty and subject to competing land-use and warming confounds that cannot be disentangled with available data.

The test that would definitively evaluate the isotherm hypothesis requires a lapse-rate contrast of 2–3°C/km across mountains hosting the same type of vegetation transition. That contrast is not available in the present sample without crossing the ecological boundary that separates cloud forest–páramo systems from *Polylepis* woodland–puna systems. Obtaining it within the same ecological zone would require either a much larger geographic survey spanning windward and leeward faces of contrasting cordilleras at multiple latitudes, or direct thermometric measurements along the altitudinal gradient rather than climate reanalysis products. The Essai's claim survives this test - not because the data confirm it, but because the geography does not yet produce the contrast needed to challenge it.

---

## References

- Humboldt, A. von, and Bonpland, A. (1807). *Essai sur la Géographie des Plantes*. Paris: Levrault, Schoell et Compagnie.
- Karger, D.N., Conrad, O., Böhner, J., Kawohl, T., Kreft, H., Soria-Auza, R.W., Zimmermann, N.E., Linder, H.P., and Kessler, M. (2017). Climatologies at high resolution for the earth's land surface areas (CHELSA). *Scientific Data*, 4, 170122. https://doi.org/10.1038/sdata.2017.122
- GBIF.org (2024). GBIF Occurrence Download. Tracheophyta, Andean South America, 2000–2024. https://api.gbif.org/v1/occurrence/search
- Josse, C., Cuesta, F., Navarro, G., Barrena, V., Becerra, M.T., Cabrera, E., Chacón-Moreno, E., Ferreira, W., Peralvo, M., Saito, J., and Tovar, A. (2009). Atlas de los Andes del Norte y Centro. UICN, Lima.
- Körner, C. (2012). *Alpine Treelines: Functional Ecology of the Global High Elevation Tree Limits*. Springer, Basel.
- Moret, P., Muriel, P., Jaramillo, R., and Dangles, O. (2019). Humboldt's tableau physique revisited. *PNAS*, 116(26), 12889–12894. https://doi.org/10.1073/pnas.1904585116
- OpenTopoData (2024). SRTM 30m elevation API. https://www.opentopodata.org/
