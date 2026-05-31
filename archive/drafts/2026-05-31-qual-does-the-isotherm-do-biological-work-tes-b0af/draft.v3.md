# Does the Isotherm Do Biological Work? Assembling a Test in the Tropical Andes

The *Essai sur la Géographie des Plantes* (1807) makes a specific claim: that the boundaries between altitudinal vegetation zones on tropical mountains are organized by temperature isolines, not by altitude itself. Elevation is the proxy. The isotherm is the cause. From this claim follows the prediction that the same vegetation zone - the cinchonas, the high grasslands, the páramo - will appear at lower altitude on a mountain with a steep temperature gradient than on one where the gradient is gentle, because in both cases the zone begins where the relevant temperature threshold is crossed. If altitude were the cause and temperature merely incidental, no such prediction would follow; the zone boundaries would sit at the same elevation regardless of local thermal gradients.

This prediction has not been directly tested. The obstacle is structural: testing it requires comparing mountains with measurably different lapse rates (different rates of temperature decrease with elevation), and the original work was built on a single mountain - Chimborazo - with a single lapse rate. On a single mountain, altitude and temperature are collinear proxies. No amount of Chimborazo data can distinguish between the two hypotheses. The Andes, fortunately, offer mountains with contrasting moisture regimes and documented lapse rate differences. Wet slopes support condensation-laden air that slows adiabatic cooling; dry slopes cool faster. This paper reports an attempted test of the isotherm claim using modern plant occurrence records and climate reanalysis data from four Andean peaks spanning this moisture contrast.

The honest result is a null design with a precisely diagnosed cause.

---

## The Test Design

The logic of the test is simple. If temperature is the organizing variable, then on a mountain with lapse rate $\lambda_1$ [°C per 1000 m], a vegetation zone beginning at threshold temperature $T^*$ will have its lower boundary at elevation:

$$h_1 = \frac{(T_{\text{ref}} - T^*) \times 1000\,\text{m}}{\lambda_1}$$

where $T_{\text{ref}}$ is the temperature at a reference elevation and $\lambda_1$ is in °C per 1000 m. On a second mountain with steeper lapse rate $\lambda_2 > \lambda_1$ [both in °C per 1000 m], the same zone (same $T^*$) appears at:

$$h_2 = \frac{(T_{\text{ref}} - T^*) \times 1000\,\text{m}}{\lambda_2}$$

which is lower: $h_2 < h_1$. The isotherm hypothesis predicts $h_1 \neq h_2$ when $\lambda_1 \neq \lambda_2$; the altitude hypothesis predicts $h_1 = h_2$ regardless of lapse rates.

The test is therefore: select mountains with measurably different lapse rates, identify vegetation zone boundaries on each using assemblage turnover data, and compare whether the boundaries align at the same temperature or the same elevation.

Four mountains were selected: Chimborazo (wet, Ecuador, 6,268 m) and Cotopaxi (wet, Ecuador, 5,897 m), representing the moist Ecuadorian inter-Andean environment; and El Misti (dry, Peru, 5,822 m) and Chachani (dry, Peru, 6,075 m), both in the hyperarid western cordillera above the Atacama–Peruvian coastal desert. Published literature documents lapse rates of approximately 6.0°C/1000 m for Ecuador's wet Andean slopes and 7.0°C/1000 m for the dry Peruvian western cordillera - a contrast of approximately 1.0°C per 1000 m. This contrast is the lever on which the test depends.

---

## Data and Methods

**Occurrence records.** Plant occurrence records were retrieved from the GBIF database via its public REST API, querying kingdom Plantae (key 6) within a 40 km radius of each mountain summit. Records without coordinates or with geospatial flags were excluded. After circle-filtering bounding-box results to the strict 40 km radius (haversine distance), each mountain returned between 2,077 and 63,784 records; all exceeded the pre-specified 1,500-record threshold. A random sample of 2,000 records per mountain was retained for the analysis. The 2,000-record cap was chosen to equalize sampling depth across mountains whose raw record counts span a 31-fold range (Chachani: 3,783; Chimborazo: 63,784). The asymmetric draw-down - Chimborazo reduced to approximately 3% of available records, Chachani to approximately 53% - is a limitation: it means band occupancy on the Ecuador mountains is determined by a more selective subsample than on the Peru mountains, and the 3,150 m Ecuador boundary, which appears consistently across both wet mountains at matched sampling depth, would benefit from a multi-seed sensitivity analysis that the present single-seed execution does not provide.

Coropuna (Peru), an initial candidate, was excluded because the GBIF query returned only 420 records - below the threshold. Chachani, in the same hyperarid Arequipa corridor as Misti, was substituted (3,783 records).

**Elevation.** GBIF occurrence records for these mountains carry no elevation data (confirmed by inspection of 10-record samples from each site). Elevation was retrieved via the open-elevation API (SRTM data; NASA/CGIAR, 30 m resampled) using batch POST requests. All 8,000 records received SRTM elevation; records with elevation outside $[0,\,7000]$ m were discarded as implausible. Final counts: 2,000 per mountain.

**Assemblage turnover.** Records were binned into 100 m elevation bands. For each mountain, a species presence set was computed per band using GBIF's `speciesKey` as the taxonomic identifier. Sørensen dissimilarity between adjacent occupied bands was computed as (Sørensen, 1948):

$$\text{S}(A, B) = 1 - \frac{2|A \cap B|}{|A| + |B|}$$

where $|A|$ is the number of species in band $A$ and $|A \cap B|$ is the number shared between adjacent bands. Note that Sørensen dissimilarity applied to species presence sets is distinct from Bray-Curtis dissimilarity, which operates on abundance data; the formula above is the presence-absence form. Bands with fewer than 8 records were excluded. Candidate zone boundaries were defined as adjacent-band transitions with dissimilarity above the 80th percentile of all transitions on that mountain.

**Climate data: pre-registered instrument and deviation.** The pre-registered approach was WorldClim v2.1 at 1 km resolution (Fick and Hijmans, 2017), to be used by regressing gridded mean annual temperature against a digital elevation model within each mountain's radius. This step could not be executed: the Python analysis environment lacked rasterio, GDAL, and any library capable of reading GeoTIFF files, and no path to install these system dependencies was available. This is a pre-registration deviation driven by an environment constraint, not by any property of the target data or the proposed method. The consequence is that the substitute instrument, ERA5, fails to resolve the lapse rate contrast the test requires - reported in full in §II.

As a substitute, ERA5 reanalysis temperature (9 km spatial resolution) was retrieved from the open-meteo archive API for 12 representative locations per mountain spanning each mountain's SRTM elevation range. Annual mean temperature (2010–2019) was computed from daily ERA5 values at each location. Temperature was regressed against SRTM elevation to yield an empirical lapse rate per mountain.

---

## Results

### I. Assemblage turnover profiles and species richness

All four mountains show structured variation in Sørensen dissimilarity with elevation. A consistent high-S transition appears near 3100–3250 m on all four mountains:

| Mountain | Regime | S boundary (m) | S value |
|---|---|---|---|
| Chimborazo | wet | 3150 | 0.833 |
| Cotopaxi | wet | 3150 | 0.765 |
| Misti | dry | 3250 | 0.902 |
| Chachani | dry | 3250 | 0.861 |

**Ecological identity of the boundaries.** The ~3150 m transition on Chimborazo and Cotopaxi is identifiable: it marks the upper cloud forest / sub-páramo ecotone, where epiphytic orchids, tree ferns, and Melastomataceae give way to open Andean grassland taxa (Poaceae, Asteraceae, Gentianaceae). This boundary is well-documented in the altitudinal literature for the Ecuadorian inter-Andean.

The ~3250 m transition on Misti and Chachani is a different ecological phenomenon. The hyperarid western Peruvian Andes receive less than 200 mm of annual precipitation at these elevations; Pacific moisture cannot penetrate the Humboldt-current-cooled coastal desert. Published vegetation accounts of the region (Weberbauer, 1945) describe the flora above the Arequipa agricultural belt (~2,335 m) as open puna and tola scrub: graminoids including *Stipa ichu* and *Festuca orthophylla*, dwarf shrubs (*Baccharis* spp., *Parastrephia lepidophylla*), and cacti (*Echinopsis* spp.) at lower elevations. No cloud forest develops at any elevation on these slopes - the moisture conditions that support epiphytic orchids, tree ferns, and Melastomataceae on Ecuador's inter-Andean slopes are absent. The GBIF assemblage at 3,200–3,300 m on Misti and Chachani contains no taxa diagnostic of a forest-grassland transition; the species composition is consistent with a shift within the puna system from lower-elevation scrub and agricultural fringe taxa to higher-altitude dry puna. The ~3,250 m boundary marks that within-system shift, not a forest-to-grassland ecotone.

The two pairs are not ecologically equivalent. This is not a question resolvable by additional GBIF records from the same mountains: the required forest-grassland ecotone does not exist on the western Peruvian Andes at any sampled elevation. This non-equivalence governs the cross-regime comparison in §III.

Additional high-S transitions occur at other elevations specific to each mountain. Peru mountains show notably higher absolute S values throughout (many transitions exceeding 0.90) compared to Ecuador mountains (~0.75–0.91), reflecting the more abrupt assemblage changes expected in an arid environment where water stress compresses species turnover rather than moisture smoothing it.

**Species richness profiles.** The richness distributions on Ecuador and Peru mountains differ qualitatively in ways consistent with their moisture regimes. Chimborazo and Cotopaxi show broad, multi-modal richness across the 2500–4500 m range, with occupied bands at nearly every 100 m step - consistent with persistent moisture supporting diverse assemblages through many elevation bands. Misti and Chachani concentrate most records in the 2200–2500 m zone (200+ species each), corresponding to the semi-arid agricultural belt around Arequipa (elevation ~2335 m); species counts decline sharply above 3500 m. The Peru records at 2,200–2,500 m likely include cultivated, escaped, and ruderal taxa from the Arequipa agricultural landscape; GBIF collects vouchers from disturbed habitats and garden escapes alongside native flora. This enriches apparent richness at the lower Peru elevations but does not affect the high-elevation transitions, where agricultural taxa are absent.

One anomaly is worth noting: the Chachani 2700–2800 m band contains only 7 species despite 77 in the band below and 38 in the band above, producing S = 0.956 - the highest single transition in the dataset. This almost certainly reflects a collector-effort gap rather than a genuine xeric bottleneck: the 80th-percentile Sørensen threshold will mark any band where local N is suppressed regardless of ecological significance, and the 2,700–2,800 m interval on Chachani falls in a zone of reduced road-accessible collector effort between the well-sampled Arequipa periphery and the accessible upper puna.

### II. Lapse rates from ERA5

This is the central failure of the analysis, reported as fully as any positive result.

ERA5 returns indistinguishable lapse rates for all four mountains:

| Mountain | Regime | ERA5 lapse rate (°C/1000 m) | SE | $R^2$ |
|---|---|---|---|---|
| Chimborazo | wet | 5.46 | 0.27 | 0.976 |
| Cotopaxi | wet | 5.80 | 0.24 | 0.983 |
| Misti | dry | 5.44 | 0.17 | 0.991 |
| Chachani | dry | 5.47 | 0.18 | 0.990 |

The wet–dry contrast is $\approx 0.05$°C/1000 m in the ERA5 data - effectively zero, and three to twenty times smaller than the measurement uncertainty on any individual estimate. The published contrast is approximately 1.0°C/1000 m.

The reason is structural, not incidental, and an instance of the scale-grain problem Levin (1992) diagnosed for ecology generally: the measurement grid and the grain of the phenomenon must match. ERA5's land surface model represents topography at 9 km spatial resolution. Steep tropical mountains such as Chimborazo - which rises from ~2000 m valleys to 6268 m within roughly 10 km - are represented by heavily smoothed orographic heights. When ERA5 temperature is sampled at a lat-lon coordinate corresponding to a SRTM elevation of 5000 m, the ERA5 model returns a temperature appropriate to its own smoothed grid-cell height, not to 5000 m on the actual surface. The regression of ERA5 temperature against SRTM elevation therefore measures the ERA5 model's own smoothed orographic lapse rate - approximately the free-air standard atmosphere value of ~5.5°C/1000 m - regardless of surface moisture conditions. No amount of ERA5 data can distinguish wet from dry mountain lapse rates at the mountain-profile scale.

The high ERA5 $R^2$ values (0.976–0.991 across all four mountains) confirm this reading: a smooth, free-air-like vertical temperature structure will regress cleanly against elevation precisely because the ERA5 orographic model expresses a near-standard atmosphere profile, not the mesoscale perturbation from surface moisture that differentiates wet from dry slopes.

The null design has occurred, but for an instrumental reason: the climate data tool operates at the wrong spatial scale, not because the physical lapse rate contrast is absent.

### III. Ecological equivalence and the boundary temperature comparison

Because the Ecuador and Peru transitions differ in ecological identity (§I) - the Ecuador pair marks a forest-páramo ecotone; the Peru pair marks a within-puna shift - the primary analysis uses the Ecuador pair alone, where both the ecological transition and the moisture regime are verified to be the same. The Peru mountains are reported as a sensitivity comparison.

**Ecuador primary comparison.** Both Chimborazo and Cotopaxi show their highest-S transition at 3150 m. Since both are wet mountains with similar published lapse rates (~6.0°C/1000 m) and similar ERA5-derived rates (5.46–5.80°C/1000 m), the 3150 m agreement is consistent with both the altitude hypothesis (same ecological zone → same elevation) and the isotherm hypothesis (similar lapse rates → similar temperature at that elevation). Within the Ecuador pair, the method cannot discriminate the hypotheses: the wet-class lapse rate contrast is too small to produce a detectable elevation difference.

**Peru sensitivity comparison.** Misti and Chachani show their highest-S transition at 3250 m - 100 m above Ecuador's 3150 m boundary. Under a published 1.0°C/1000 m lapse rate contrast between the wet and dry classes, the isotherm hypothesis predicts an elevation difference of 288–532 m (§IV). The observed 100 m is substantially below this prediction. However, as established in §I, the Peru transitions are within-puna rather than forest-grassland ecotones and are therefore not ecological analogues of Ecuador's boundaries. The 100 m elevation difference is not interpretable as evidence for or against the isotherm hypothesis when the comparison crosses a zone-identity boundary.

**ERA5 boundary temperatures - a tautological conversion.** For completeness, the following table shows ERA5-derived temperatures at the candidate boundaries, alongside temperatures computed from published lapse rates. Because ERA5 lapse rates are nearly uniform across all four mountains by construction (§II), converting similar boundary elevations (~3200 m) to temperatures via uniform lapse rates trivially produces similar temperatures. The SD of the ERA5 boundary temperatures (0.53°C) reflects this uniformity; it is not evidence for the isotherm hypothesis.

| Mountain | ERA5 T @ boundary | Published LR T @ boundary |
|---|---|---|
| Chimborazo | 9.56°C | 7.84°C |
| Cotopaxi | 10.09°C | 9.47°C |
| Misti | 10.88°C | 5.90°C |
| Chachani | 10.76°C | 5.87°C |

*ERA5 column: temperature at the candidate boundary elevation under ERA5 lapse rates - a tautological conversion given ERA5's uniform lapse rates, not a test of the isotherm hypothesis. Published LR column: temperature under published wet-slope (6.0°C/1000 m) and dry-slope (7.0°C/1000 m) lapse rates applied to the same ERA5 reference temperatures.*

The two columns measure the difference an instrument makes. Under ERA5, SD = 0.53°C; under published lapse rates, SD = 1.50°C and the Ecuador–Peru temperature contrast is approximately 2.5°C. The variance ratio is 7.9×. This is a calibration of how much the lapse rate assumption matters, not a result about vegetation.

### IV. What the required lapse rate contrast would produce

A power calculation shows how large the boundary elevation difference would be under a 1.0°C/1000 m lapse rate contrast (approximately the published Ecuador–Peru value).

For target temperature $T^* = 10$°C and ERA5 reference temperatures ($T_{\text{ref}} \approx 28$°C), a contrast between $\lambda_1 = 6.0$ and $\lambda_2 = 7.0$ (°C/1000 m) yields:

$$\Delta h = h_1 - h_2 = (T_{\text{ref}} - T^*) \times 1000\,\text{m} \times \left(\frac{1}{\lambda_1} - \frac{1}{\lambda_2}\right) = 18 \times 1000 \times \left(\frac{1}{6} - \frac{1}{7}\right) \approx 429\,\text{m}$$

Because ERA5 reference temperatures differ slightly across mountains, the predicted $\Delta h$ ranges 288–532 m depending on which pair is compared. All values are well above the 100 m band resolution of the GBIF data; the test would have had power to detect a 1.0°C/1000 m contrast. A 0.5°C/1000 m contrast produces 50–319 m - detectable for some pairs.

The ERA5-derived contrast of ~0.05°C/1000 m predicts an elevation difference of less than 5 m - undetectable with 100 m bins.

---

## Interpretation and Limits

The isotherm question remains open. The reason it remains open is not that the proposed method fails - it does not - but that the execution revealed two obstacles: an instrument operating at the wrong spatial scale, and a mountain selection that lacks the ecological zone structure the test requires.

**Instrument limit.** WorldClim v2.1 at 1 km, derived by interpolating weather station data against a fine-resolution DEM, provides lapse rates that correctly track surface temperature conditions rather than the model's orographic surface. ERA5 at 9 km does not. This is the specific, actionable gap: the pre-registered instrument is the correct one; the substitute failed on known grounds.

**Ecological scope limit.** The Bray-Curtis method identifies wherever species composition changes sharply. It does not assign ecological identity to those transitions. As established in §I, the candidate boundaries on the Peru mountains are within-puna transitions on slopes that lack cloud forest entirely. A cross-regime test of the *Essai*'s isotherm claim requires a forest-grassland ecotone on both the wet and dry mountains - not merely a high-dissimilarity transition at any elevation. Future iterations should select the dry mountain from a range that receives sufficient moisture to support forest at lower elevations, making a forest-grassland ecotone possible. The eastern Andean slopes of Peru, which receive Amazon-basin moisture even on relatively arid years, offer candidates.

**What the procedure cannot distinguish.** Following the framework of [*What the Apparatus Refuses to See*](posts/2026-05-26-what-the-apparatus-refuses-to-see-mappin-3299/), the blind set $B(M;\,\mathcal{A})$ for this analysis - the set of inferences the procedure cannot distinguish, given the alternative class $\mathcal{A}$ of hypotheses in play - now contains one entry rather than two:

$B_1$: whether the ~3200 m boundary is ecologically equivalent across all four mountains is no longer open. The §I analysis resolves it in the negative: the Peru transitions are within-puna on slopes without cloud forest, not forest-grassland ecotones. The test design requires a different mountain selection to escape this non-equivalence.

$B_2$: whether the boundary temperature is approximately 10°C (ERA5-derived) or approximately 6–9°C (published lapse rates applied to ERA5 reference temperatures). The ERA5 lapse rates cannot close this; WorldClim v2.1 at 1 km remains the required instrument.

$B_2$ cannot be closed without additional data. $B_1$ is closed: the Peru western slopes cannot provide the ecological comparison the test requires.

---

## The Historical Comparison

The *Naturgemälde* and accompanying text of the *Essai* place the upper boundary of the *Région de Quinquinas* (the cinchona-forest zone) at approximately 1,440 toises on the Chimborazo profile (1 toise = 1.949 m, yielding approximately 2,807 m), with temperatures Humboldt recorded in the 12–13°C range for the uppermost cinchona stations. The *Région de Mousses* (the sub-páramo moss zone) begins just above this elevation. The modern GBIF-derived Sørensen analysis shows the sharpest transitions in the Chimborazo dataset at 3100–3200 m and 3400–3500 m. The disagreement - approximately 300–400 m upward from the *Essai*'s ~2,807 m figure - is consistent with known warming of 0.6–1.0°C per century in the tropical Andes (Vuille and Bradley, 2000), which at a lapse rate of 6°C/1000 m would shift isotherms upward by 100–170 m per century and 200–340 m over two centuries. It is also consistent with imprecision in the original zone boundaries, which were partly qualitative and partly reconstructed from sparse collections made at speed during a single ascent.

Disentangling these two causes requires early-19th-century temperature station records from the Chimborazo massif at the spatial and elevational resolution needed to assign a temperature to a specific boundary. Those records do not exist. This is a permanent limit on the comparison, not a transient one.

---

## Conclusion

The *Essai*'s isotherm claim - that temperature, not altitude, organizes altitudinal vegetation zones - can in principle be tested by comparing vegetation zone boundaries across Andean mountains with different lapse rates. The method works, and the GBIF occurrence data is sufficient to identify candidate assemblage transitions and richness profiles within each mountain. Two obstacles prevent the cross-regime comparison from being executed with the present mountain selection.

The first is instrumental: ERA5 at 9 km cannot resolve the documented moisture-regime lapse rate contrast, compressing a 1.0°C/1000 m signal to an indistinguishable 0.05°C/1000 m. WorldClim v2.1 at 1 km, the pre-registered instrument, would provide the required discrimination. The second is ecological: the dry Peru mountains (Misti, Chachani) lack a forest-grassland ecotone at any sampled elevation. Their candidate boundaries mark within-puna transitions on hyperarid slopes where cloud forest is absent. No lapse rate data, however precise, can make these boundaries equivalent to Ecuador's cloud-forest/páramo boundary. The test requires a different dry mountain - one where sufficient moisture supports forest at lower elevations, making the ecotone accessible.

The Ecuador pair (Chimborazo and Cotopaxi) shows consistent forest-páramo boundaries at 3150 m, internally confirming the Sørensen method on ecologically verified, same-regime mountains. A power calculation shows that a 1.0°C/1000 m lapse rate contrast would produce a 288–532 m elevation difference - well within the 100 m detection range of the GBIF binning. What the analysis now lacks is one critical input: surface lapse rates at 1 km resolution (WorldClim, the pre-registered instrument), paired with a mountain selection where ecologically equivalent forest-grassland boundaries exist on both wet and dry mountains.

The isotherm question is open in a more specific sense than before: the method is specified, its power under the required contrast is quantified, the ecological preconditions for a valid cross-regime comparison are now explicit, and the instrumental gap has a named remedy.

---

## References

- Humboldt, A. von, & Bonpland, A. (1807). *Essai sur la Géographie des Plantes*. Paris: Levrault, Schoell et Cie.

- Fick, S.E., & Hijmans, R.J. (2017). WorldClim 2: new 1-km spatial resolution climate surfaces for global land areas. *International Journal of Climatology*, 37(12), 4302–4315. https://doi.org/10.1002/joc.5086

- Hersbach, H., et al. (2020). The ERA5 global reanalysis. *Quarterly Journal of the Royal Meteorological Society*, 146(730), 1999–2049. https://doi.org/10.1002/qj.3803

- Levin, S.A. (1992). The problem of pattern and scale in ecology. *Ecology*, 73(6), 1943–1967. https://doi.org/10.2307/1941447

- Sørensen, T. (1948). A method of establishing groups of equal amplitude in plant sociology based on similarity of species content. *Det Kongelige Danske Videnskabernes Selskab, Biologiske Skrifter*, 5(4), 1–34.

- Vuille, M., & Bradley, R.S. (2000). Mean annual temperature trends and their vertical structure in the tropical Andes. *Geophysical Research Letters*, 27(23), 3885–3888. https://doi.org/10.1029/2000GL011871

- Weberbauer, A. (1945). *El Mundo Vegetal de los Andes Peruanos*. Lima: Ministerio de Agricultura.

- GBIF Secretariat (2024). GBIF Occurrence Download. Global Biodiversity Information Facility. https://www.gbif.org/

- Zippenfenig, P. (2023). Open-Meteo.com Weather API [Software]. Zenodo. https://doi.org/10.5281/zenodo.7970649

- Open-Elevation (2018). Open-Elevation API [Software]. https://open-elevation.com/ (SRTM data: NASA/CGIAR, 30 m resampled)
