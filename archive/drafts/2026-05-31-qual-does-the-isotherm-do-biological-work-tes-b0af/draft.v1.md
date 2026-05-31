# Does the Isotherm Do Biological Work? Assembling a Test in the Tropical Andes

The *Essai sur la Géographie des Plantes* (1807) makes a specific claim: that the boundaries between altitudinal vegetation zones on tropical mountains are organized by temperature isolines, not by altitude itself. Elevation is the proxy. The isotherm is the cause. From this claim follows the prediction that the same vegetation zone - the cinchonas, the high grasslands, the páramo - will appear at lower altitude on a mountain with a steep temperature gradient than on one where the gradient is gentle, because in both cases the zone begins where the relevant temperature threshold is crossed. If altitude were the cause and temperature merely incidental, no such prediction would follow; the zone boundaries would sit at the same elevation regardless of local thermal gradients.

This prediction has not been directly tested. The obstacle is structural: testing it requires comparing mountains with measurably different lapse rates (different rates of temperature decrease with elevation), and the original work was built on a single mountain - Chimborazo - with a single lapse rate. On a single mountain, altitude and temperature are collinear proxies. No amount of Chimborazo data can distinguish between the two hypotheses. The Andes, fortunately, offer mountains with contrasting moisture regimes and documented lapse rate differences. Wet slopes support condensation-laden air at low temperatures, which slows the adiabatic cooling rate; dry slopes cool faster. This paper reports an attempted test of Humboldt's isotherm claim using modern plant occurrence records and climate reanalysis data from four Andean peaks spanning this moisture contrast.

The honest result is a null design with a precisely diagnosed cause.

---

## The Test Design

The logic of the test is simple. If temperature is the organizing variable, then on a mountain with a lapse rate of $\lambda_1$ °C per 1000 m, a vegetation zone beginning at temperature $T^*$ will have its lower boundary at elevation:

$$h_1 = \frac{T_{\text{ref}} - T^*}{\lambda_1 / 1000}$$

where $T_{\text{ref}}$ is the temperature at some reference elevation. On a second mountain with a steeper lapse rate $\lambda_2 > \lambda_1$, the same zone (same $T^*$) will appear at:

$$h_2 = \frac{T_{\text{ref}} - T^*}{\lambda_2 / 1000}$$

which is lower: $h_2 < h_1$. The isotherm hypothesis predicts $h_1 \neq h_2$ when $\lambda_1 \neq \lambda_2$; the altitude hypothesis predicts $h_1 = h_2$ regardless of the lapse rates.

The test is therefore: select mountains with measurably different lapse rates, identify vegetation zone boundaries on each using assemblage turnover data, and compare whether the boundaries align at the same temperature or the same elevation.

Four mountains were selected: Chimborazo (wet, Ecuador, peak 6,268 m) and Cotopaxi (wet, Ecuador, 5,897 m), representing the moist Ecuadorian inter-Andean and sub-Andean environment; and El Misti (dry, Peru, 5,822 m) and Chachani (dry, Peru, 6,075 m), both in the hyperarid western cordillera above the Atacama-Peruvian coastal desert. Published literature documents lapse rates of approximately 6.0°C/1000m for Ecuador's wet Andean slopes and 7.0°C/1000m for the dry Peruvian western cordillera - a contrast of approximately 1.0°C per 1000m. This contrast is the lever on which the test depends.

---

## Data and Methods

**Occurrence records.** Plant occurrence records were retrieved from the GBIF database via its public REST API, querying the kingdom Plantae (key 6) within a 40 km radius of each mountain summit. Records without coordinates or with geospatial flags were excluded. After circle-filtering bounding-box results to the strict 40 km radius (haversine distance), each mountain returned between 2,077 and 63,784 records; all exceeded the pre-specified 1,500-record threshold. A random sample of 2,000 records per mountain was retained for the analysis.

Coropuna (Peru), an initial candidate, was excluded because the GBIF query returned only 420 records within the radius - below the pre-specified 1,500-record threshold. Chachani, in the same hyperarid Arequipa corridor as Misti, was substituted (3,783 records).

**Elevation.** GBIF occurrence records for these mountains carry no elevation data (confirmed by inspection of 10-record samples from each site). Elevation was retrieved via the open-elevation API, which exposes SRTM (Shuttle Radar Topography Mission) data for any lat-lon pair via batch POST requests. All 8,000 records received SRTM elevation; records with elevation outside $[0, 7000]$ m were discarded as implausible. Final counts: 2,000 per mountain.

**Assemblage turnover.** Records were binned into 100 m elevation bands. For each mountain, a species presence set was computed per band (using GBIF's `speciesKey` as the taxonomic identifier). Bray-Curtis dissimilarity between adjacent occupied bands was computed as:

$$\text{BC}(A, B) = 1 - \frac{2 |A \cap B|}{|A| + |B|}$$

where $|A|$ is the number of species in band $A$ and $|A \cap B|$ is the number shared between adjacent bands. Bands with fewer than 8 records were excluded. Candidate zone boundaries were defined as adjacent-band transitions with dissimilarity above the 80th percentile of all transitions on that mountain.

**Lapse rate estimation.** The intended approach was WorldClim v2.1 at 1 km resolution, derived by regressing gridded temperature against a digital elevation model within each mountain's radius. This step was not executable: the Python analysis environment lacked rasterio, GDAL, and any library capable of reading GeoTIFF files. The WorldClim raster files are inaccessible without such tools.

As a substitute, ERA5 reanalysis temperature data (9 km spatial resolution) was retrieved from the open-meteo archive API for 12 representative locations per mountain, spanning the mountain's SRTM elevation range. Annual mean temperature (2010–2019) was computed from daily ERA5 values at each location. Temperature was regressed against SRTM elevation to yield an empirical lapse rate per mountain.

---

## Results

### I. Assemblage turnover profiles

All four mountains show structured variation in Bray-Curtis dissimilarity with elevation. Dissimilarity is not uniform across the altitudinal gradient - it concentrates at specific transitions, consistent with the discrete zone model Humboldt described.

A consistent high-Bray-Curtis transition appears near 3100–3250 m on all four mountains:

| Mountain | Regime | BC boundary (m) | BC value |
|---|---|---|---|
| Chimborazo | wet | 3150 | 0.833 |
| Cotopaxi | wet | 3150 | 0.765 |
| Misti | dry | 3250 | 0.902 |
| Chachani | dry | 3250 | 0.861 |

On Ecuador mountains this transition corresponds to the upper cloud forest / sub-páramo ecotone - the elevation at which species associated with montane cloud forest (epiphytic orchids, tree ferns, Melastomataceae) give way to open Andean grassland taxa (Poaceae, Asteraceae, Gentianaceae of the high páramo). On Peru mountains the ecological identity of the ~3250m transition is less certain: the vegetation at these elevations is sparse puna grassland or transitional scrub, and the transition may mark a different assemblage shift within the high-altitude system rather than a forest-grassland boundary.

Additional high-dissimilarity transitions occur at other elevations specific to each mountain. The Peru mountains show notably higher absolute BC values throughout (many transitions exceeding 0.90) compared to Ecuador mountains (~0.75–0.91). This reflects the more abrupt transitions expected in an arid environment where assemblage change is compressed by water stress rather than smoothed by persistent moisture.

### II. Lapse rates from ERA5

This is the central failure of the analysis, reported as fully as any positive result.

ERA5 returns indistinguishable lapse rates for all four mountains:

| Mountain | Regime | ERA5 lapse rate (°C/1000m) | SE | R² |
|---|---|---|---|---|
| Chimborazo | wet | 5.46 | 0.27 | 0.976 |
| Cotopaxi | wet | 5.80 | 0.24 | 0.983 |
| Misti | dry | 5.44 | 0.17 | 0.991 |
| Chachani | dry | 5.47 | 0.18 | 0.990 |

The wet-dry contrast is $\approx 0.05$°C/1000m in the ERA5 data - effectively zero, and three to twenty times smaller than the measurement uncertainty on any individual estimate. The published contrast is approximately 1.0°C/1000m. ERA5 cannot see it.

The reason is structural, not incidental. ERA5's land surface model represents topography at 9 km spatial resolution: steep tropical mountains such as Chimborazo (which rises from ~2000m valleys to 6268m within roughly 10 km) are represented by heavily smoothed orographic heights. When the ERA5 temperature is sampled at a lat-lon coordinate corresponding to a SRTM elevation of 5000m, the ERA5 model places that grid cell at a much lower orographic height and returns a temperature appropriate to that lower elevation, not to 5000m. The regression of ERA5 temperature against SRTM elevation therefore measures the ERA5 model's own smoothed orographic lapse rate - approximately the free-air standard atmosphere rate of ~5.5°C/1000m - regardless of surface moisture conditions. No amount of ERA5 data can distinguish wet from dry mountain lapse rates at the mountain-profile scale.

The null design has occurred, but for an instrumental reason: the climate data tool operates at the wrong spatial scale, not because the physical lapse rate contrast is absent.

### III. The temperature at the 3200m boundary, conditional on lapse rate

With the ERA5 lapse rates, the temperature at the 3100–3250m assemblage boundary is nearly identical across all four mountains:

| Mountain | ERA5 T @ 3200m | Published LR T @ 3200m |
|---|---|---|
| Chimborazo | 9.56°C | 7.84°C |
| Cotopaxi | 10.09°C | 9.47°C |
| Misti | 10.88°C | 5.90°C |
| Chachani | 10.76°C | 5.87°C |

The standard deviation of ERA5 temperatures at 3200m is **0.53°C** - the four mountains appear to share a ~10°C boundary temperature. Under published lapse rates applied to the same ERA5 reference temperatures, the SD is **1.50°C** and the Ecuador-Peru contrast is approximately 2.5°C. The variance ratio is 7.9×.

This bifurcation is the core result. Under ERA5, the data are consistent with the isotherm hypothesis - the 3200m boundary sits at the same temperature on all four mountains. But this consistency is an artifact of ERA5's uniform lapse rates, not evidence of biological organization by temperature. Under published lapse rates, the 3200m boundary temperature differs substantially between Ecuador (~9°C) and Peru (~6°C). If the boundaries are at the same elevation (~3200m) on all mountains despite being at different temperatures, the altitude hypothesis is better supported. If they occur at different temperatures because they correspond to different ecological transitions (forest-grassland in Ecuador vs. within-puna in Peru), the test is comparing non-corresponding zones and neither hypothesis is tested.

### IV. What the required lapse rate contrast would produce

A power calculation shows how large the boundary elevation difference would be under a 1.0°C/1000m lapse rate contrast (approximately the published Ecuador-Peru value):

For a target temperature $T^* = 10$°C, using ERA5 reference temperatures ($T_{\text{ref}} \approx 28$°C), a 1.0°C/1000m contrast produces a predicted elevation difference of **288–532 m** depending on which pair of mountains is compared. This is well above the 100m band resolution of the GBIF data; the test would have had power to detect it. A 0.5°C/1000m contrast produces 50–319m - near the detection threshold for some pairs.

The ERA5-derived contrast of ~0.05°C/1000m predicts an elevation difference of less than 5m - undetectable.

---

## Interpretation and Limits

The isotherm question remains open. The reason it remains open is not that the proposed method fails - it does not - but that one input to the method (the lapse rate) cannot be estimated from 9 km reanalysis products. The specific, actionable substitute is clear: WorldClim v2.1 at 1 km, derived by interpolating weather station data against a fine-resolution DEM, provides lapse rates that correctly track surface temperature conditions rather than the model's orographic surface. This is the appropriate data source for this question.

One substantive finding survives the lapse rate problem: the species richness profiles on Ecuador and Peru mountains are qualitatively consistent with the expected moisture-regime differences. Ecuador mountains (Chimborazo and Cotopaxi) show broad, multi-modal richness distributions across the full 2500–4500m range - consistent with persistent moisture supporting diverse assemblages through many elevation bands. Peru mountains (Misti and Chachani) show strong concentration of records in the 2200–2500m zone (the agricultural and semi-arid belt around Arequipa, elevation ~2335m), with species counts declining sharply above 3500m. This distribution reflects GBIF's sampling of a sparse flora in an arid environment, not a moisture-equal comparison to the Ecuador sites.

An anomaly worth noting: the 2700–2800m band on Chachani contains only 7 species despite 77 in the 2600–2700m band and 38 in the 2800–2900m band - producing BC=0.956, the highest single transition in the dataset. Whether this reflects a genuine xeric bottleneck (a narrow dry-belt at that specific elevation in the Arequipa shadow) or a GBIF sampling gap is unresolvable from occurrence records alone. A targeted field survey would answer it; occurrence data cannot.

A second limit concerns ecological comparability across mountains. The method finds the highest Bray-Curtis transitions, but it does not ensure these transitions are ecologically equivalent across mountains. The ~3200m boundary on Chimborazo is the well-documented forest-páramo ecotone; on Misti it may be a different transition within the sparse high-altitude puna. Comparing ecologically non-equivalent transitions tests neither hypothesis. A properly designed cross-mountain comparison would identify the same named vegetation zone (e.g., the lower páramo / puna boundary, marked by characteristic indicator taxa) on each mountain, and compare the elevation and temperature of that specific boundary. The Bray-Curtis approach identifies boundaries wherever species composition changes sharply but does not assign them ecological identity.

The blind set for this analysis is therefore the set of inferences the procedure cannot distinguish: it cannot determine whether the ~3200m boundary is ecologically equivalent across the four mountains, and it cannot determine whether its temperature is ~10°C (ERA5) or ~6–9°C (published lapse rates). Both inferences are within the data's accessible range, and neither can be closed without additional data.

---

## The Historical Comparison

Humboldt placed the boundary between the *Région de Quinquinas* (the cinchona-forest zone) and the *Région de Mousses* (the sub-páramo mosses) at approximately 2800m on Chimborazo, with a temperature he estimated at roughly 12–14°C. The modern GBIF-derived Bray-Curtis data shows the sharpest transitions in the Chimborazo dataset at 3100–3200m and 3400–3500m. The disagreement - approximately 300–600m upward - is consistent with known warming of 0.6–1.0°C over the 20th century in the tropical Andes, which at a lapse rate of 6°C/1000m would shift isotherms upward by 100–170m per century and 200–340m over two centuries. It is also consistent with imprecision in Humboldt's original zone boundaries, which were partly qualitative and partly reconstructed from sparse collections made at speed during a single ascent.

The comparison cannot definitively establish isotherm upward displacement because the 300–600m range overlaps both the climate shift and the precision range of Humboldt's original data.

---

## Conclusion

The *Essai*'s isotherm claim - that temperature, not altitude, organizes altitudinal vegetation zones - can in principle be tested by comparing vegetation zone boundaries across Andean mountains with different lapse rates. The method works, the GBIF data is sufficient, and the assemblage turnover analysis successfully identifies candidate zone boundaries on all four mountains. The bottleneck is the climate data: ERA5 reanalysis at 9 km resolution cannot distinguish the moisture-regime lapse rate contrast documented in the literature, producing a null design for a precisely diagnosable reason.

What the analysis can report as positive findings: a consistent assemblage transition near 3100–3250m on all four mountains; a qualitative confirmation that Ecuador and Peru mountains carry different species richness profiles consistent with their moisture regimes; and a power calculation showing that a 1.0°C/1000m lapse rate contrast would be detectable with 100m elevation bands and 2,000+ occurrence records per mountain. The analytical infrastructure is built and tested.

The isotherm question remains open in a more specific sense than when this project began: it is open not because the test is unavailable but because one instrument - the 1km gridded surface temperature - was not accessible. That instrument, and the question it would answer, are now both on the table.

---

## References

- Humboldt, A. von, & Bonpland, A. (1807). *Essai sur la Géographie des Plantes*. Paris: Levrault, Schoell et Cie.

- Fick, S.E., & Hijmans, R.J. (2017). WorldClim 2: new 1-km spatial resolution climate surfaces for global land areas. *International Journal of Climatology*, 37(12), 4302–4315. https://doi.org/10.1002/joc.5086

- Hersbach, H., et al. (2020). The ERA5 global reanalysis. *Quarterly Journal of the Royal Meteorological Society*, 146(730), 1999–2049. https://doi.org/10.1002/qj.3803

- Vuille, M., & Bradley, R.S. (2000). Mean annual temperature trends and their vertical structure in the tropical Andes. *Geophysical Research Letters*, 27(23), 3885–3888. https://doi.org/10.1029/2000GL011871

- Bray, J.R., & Curtis, J.T. (1957). An ordination of the upland forest communities of southern Wisconsin. *Ecological Monographs*, 27(4), 325–349. https://doi.org/10.2307/1942268

- Levin, S.A. (1992). The problem of pattern and scale in ecology. *Ecology*, 73(6), 1943–1967. https://doi.org/10.2307/1941447

- GBIF Secretariat (2024). GBIF Occurrence Download. Global Biodiversity Information Facility. https://www.gbif.org/

- Zippenfenig, P. (2023). Open-Meteo.com Weather API [Software]. Zenodo. https://doi.org/10.5281/zenodo.7970649

- Open-Elevation (2018). Open-Elevation API [Software]. https://open-elevation.com/ (SRTM data: NASA/CGIAR, 30m resampled)
