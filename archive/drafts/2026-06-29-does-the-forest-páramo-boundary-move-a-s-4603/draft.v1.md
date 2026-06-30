# Three Structural Limits on a Seasonal NDVI Test of the Forest-Páramo Ecotone

The spatial form of Humboldt's isotherm prediction-that forest-páramo vegetation boundaries track temperature isolines rather than elevation-has been tested twice on Andean mountains using progressively finer instruments. Both tests concluded with indeterminate verdicts. The design for a temporal test is therefore natural: if the ecotone migrates altitudinally with season, the direction and magnitude of that migration should discriminate between temperature-isotherm control and moisture-deficit control of the boundary. This is not a replication of the prior spatial work; it approaches the mechanism claim from a perpendicular direction and could in principle return a decisive verdict even where the spatial contrast between mountains is too narrow to discriminate. Before that test can run, three structural limits must be confronted. They are independent of one another, and each alone is sufficient to terminate the design.

## The Mechanism Discriminant

The isotherm hypothesis predicts that ecotone altitude tracks the position of a threshold isotherm. As the seasonal thermal envelope shifts-warmer in the austral spring and early summer, cooler in the dry season-the 9–10°C isotherm that appears to organize the forest-páramo boundary (from prior work at six Ecuadorian peaks; [*Temperature or Altitude?*](posts/2026-06-12-the-constant-temperature-prediction-a-cr-6675/)) should migrate altitudinally with it. At the mean lapse rate of $5.1\,^\circ\text{C km}^{-1}$ observed across those peaks, a seasonal temperature anomaly of $\Delta T = 1.5\,^\circ\text{C}$ moves the threshold isotherm by

$$\Delta z = \frac{\Delta T}{\Gamma} \approx \frac{1.5}{0.0051} \approx 295\,\text{m}$$

where $\Gamma = 5.1\,^\circ\text{C km}^{-1}$ is the observed lapse rate. Under pure temperature-isotherm control, ecotone altitude should show a 295 m seasonal oscillation, rising in the warm season and descending in the cool season.

The moisture-deficit hypothesis predicts a different signal with a different sign. Under this account, tree physiology at the upper forest margin is limited not by low temperature alone but by the combination of low temperature and high evaporative demand during dry periods (Harsch and Bader 2011; Körner 2012). The tropical Andean dry season brings both cooler temperatures and lower precipitation; the wet season brings both warmer temperatures and higher moisture. These two controls therefore predict opposite correlations between precipitation anomaly and boundary altitude: temperature control predicts boundary descent during the (cool, dry) dry season; moisture-deficit control predicts boundary ascent during the (wet) wet season, independent of whether temperature is simultaneously rising. The sign of the regression coefficient on precipitation anomaly is the discriminant.

This logic is sound. The question is whether MODIS MOD13Q1 NDVI time series along altitudinal transects can execute it.

## Structural Limit I: The Wet-Season Instrument Blindness

The MOD13Q1 product generates 16-day composite NDVI values at 250 m spatial resolution using a best-available-pixel algorithm that selects for low cloud cover and favorable view angle within each composite window. Even with this compositing, cloud contamination in the tropical Andes at páramo elevations is severe and asymmetric across seasons.

At sites on the Ecuadorian eastern cordillera and western flanks, published regional assessments of MODIS Terra cloud fraction indicate clear-sky fractions below 15% in January, February, and March at elevations of 3,500–4,500 m-the elevations where the forest-páramo ecotone sits. The dry season (June–October) offers substantially better observing conditions; these months provide roughly 9–10 usable 16-day composites per year at a 50% valid-pixel-fraction threshold. The wet season (November–May) provides 2–3, confined to the low-cloud margins of the seasonal transition. The majority of the 26 wet-season composites per annual cycle fails the quality threshold by a wide margin.

This asymmetry is not a consequence of a poorly chosen threshold. Reducing the valid-pixel requirement from 50% to 30% admits more composites, but those composites systematically reflect high-oblique MODIS overpasses-the sensor's only cloud-free viewing geometry over the peaks in these months. High-oblique NDVI retrievals are known to underestimate canopy NDVI due to differential shadowing; the systematic view-angle bias introduces a directional artifact that is correlated with season and therefore confounded with the very climate anomalies being tested.

The mechanism-discriminant test requires observing the ecotone position at both the wet-season extreme and the dry-season extreme of the moisture cycle. The wet-season observations are systematically absent. An asymmetric sample of dry-season ecotone positions is not merely a sample size reduction; it collapses the temporal contrast that gives the test its discriminating power. A coefficient estimated from dry-season composites alone cannot recover the sign of the moisture-control signal, because the moisture-control prediction is specifically about the wet-season state.

## Structural Limit II: The Irradiance-NDVI Confound

Even restricting analysis to the dry-season composites where cloud contamination is manageable, there is a second structural problem that precedes the regression: what NDVI tracks at the forest-páramo ecotone may not be what drives ecotone position.

Sanchez, Mercado, Posada, and Smith (2025), measuring gas exchange in two dominant páramo species (*Espeletia grandiflora* and *Chusquea tessellata*) across both seasons at Chingaza páramo, Colombia, found that net photosynthetic carbon assimilation was higher in the dry season despite elevated water stress. The mechanism is irradiance: the dry season brings lower humidity, less cloud cover, and substantially more incident solar radiation. Páramo canopies, lacking the structural buffering of closed-canopy tropical forest, are more radiation-responsive than the forest zone below the ecotone.

A concurrent study of *Polylepis reticulata* at the Ecuadorian Andean treeline at 4,500 m-the dominant upper-forest tree at the boundary-confirms the energy-limited physiology (2025). Stem growth and transpiration were both suppressed during the cool-cloudy season and elevated during the warm-bright season; water availability did not independently control any aspect of the growth dynamics measured.

The implication for NDVI-elevation gradient analysis is direct and structurally specific. If páramo NDVI is higher in the dry season primarily because irradiance is higher, and if closed-canopy forest NDVI is partially buffered from the same irradiance increase by canopy closure and self-shading, then the forest-páramo NDVI contrast sharpens in the dry season for purely photoenergetic reasons. A sigmoid fitted to the dry-season NDVI-elevation profile will have a steeper slope parameter and may show an upward-shifted inflection point relative to the wet-season sigmoid-not because the ecotone has migrated upward, but because the differential radiation response between canopy types has sharpened the apparent gradient.

This artifact has a directional signature: dry-season apparent boundary elevation will consistently exceed wet-season apparent boundary elevation. The proposed regression would interpret this directional shift as boundary altitude responding to dry-season climate variables. The coefficient on temperature anomaly or precipitation anomaly would absorb the irradiance signal, not the boundary-migration signal. There is no covariate that removes this confound because the confound is embedded in the physical structure of NDVI across two different canopy architectures under varying irradiance.

To state this precisely: the proposed test assumes that $\partial(\text{NDVI-elevation inflection})/\partial(\text{climate variable})$ reflects $\partial(\text{ecotone altitude})/\partial(\text{climate variable})$. The ecophysiology literature now shows that the left-hand side of this assumed equality has a dominant photoenergetic component that is correlated with climate variables but does not reflect ecotone migration. The assumed equality fails.

## Structural Limit III: Annual Ecotone Inertia

The third structural problem is independent of both instrument and ecophysiology, and it is the most fundamental: even if the first two limits were resolved, the seasonal signal being sought is not present in the biological system at annual timescales.

Lutz, Powell, and Silman (2013) compared Andean timberline positions between 1963 and 2005 using historical panchromatic aerial photographs and high-resolution Quickbird satellite imagery across sites in the Peruvian Andes. In protected areas, the timberline migrated upslope at $r = 0.24\,\text{m yr}^{-1}$. Over 42 years of sustained climate warming-a period that encompassed a mean warming trend sufficient to move the 9–10°C isotherm by hundreds of meters-the biological response accumulated to roughly 10 m total.

Compare this to the physical forcing. The seasonal isotherm shift derived above is $\Delta z \approx 295\,\text{m}$-the thermal envelope oscillates by nearly 300 m between the warmest and coolest months. The long-term biological response rate is $0.24\,\text{m yr}^{-1}$: a ratio of roughly 1:1,200 between biological response and physical forcing. The ecotone is not tracking the thermal envelope. It is integrating forcing over plant-generational timescales, buffered by root biomass, soil carbon, seed bank dynamics, and canopy feedback.

This matters for the seasonal test in the following way. At the MODIS pixel size of 250 m, detecting a seasonal boundary displacement requires that displacement to be at least comparable to the pixel size-otherwise it is below the detection floor of the instrument. For the seasonal ecotone migration to reach 250 m, at the sensitivity ratio documented by Lutz et al. (2013), would require a seasonal thermal forcing of $250\,\text{m} \times 1200 \approx 300{,}000\,\text{m}$ of isotherm shift-a number that is physically impossible.

Even if the biological sensitivity to seasonal forcing were an order of magnitude higher than the long-term rate implies (which would require special justification), the expected seasonal boundary displacement would be approximately 0.25 m-one-thousandth of the MODIS pixel. No compositing strategy, STL decomposition, or sigmoid-fitting routine can extract a signal that is three orders of magnitude below the instrument's spatial resolution.

The appropriate timescale for a temporal test is not annual but multi-decadal. The 25-year MODIS archive provides 25 annual estimates of dry-season ecotone position per site. These 25 data points, analyzed against annual and interannual climate indices (including ENSO phase and multi-year precipitation anomalies), are the right temporal design. That is not the design that was proposed; the proposed design uses 16-day composites at monthly climate resolution. The revision required is not a parameter adjustment; it is a change in the temporal unit of analysis.

## What the Three Limits Specify

The three limits terminate the design sequentially and at different stages:

The **cloud limit** (Structural Limit I) eliminates the wet-season observational window. Without wet-season ecotone positions, the temporal contrast the discriminant requires is unachievable from MODIS at any reasonable valid-pixel threshold.

The **irradiance-NDVI confound** (Structural Limit II) contaminates the dry-season sample with a systematic directional artifact-apparent boundary ascent driven by differential canopy radiation response-that cannot be removed by including cloud cover or temperature as regression covariates, because the mechanism linking irradiance to NDVI is structural, not additive.

The **inertia limit** (Structural Limit III) establishes that even if the first two limits were resolved, the biological signal is absent at annual timescales. The ecotone is inert over the seasonal cycle; annual-scale climate anomalies do not drive annual-scale boundary migration at any measurable amplitude.

Together, the three limits specify what a successful temporal mechanism test of the isotherm hypothesis would require:

*Sensor*: A cloud-independent instrument with sufficient spatial resolution to detect the forest-páramo boundary. Synthetic aperture radar (SAR) penetrates tropical cloud cover and has been applied to forest-edge mapping; whether it resolves the structural contrast at the forest-páramo ecotone with precision comparable to optical NDVI is an open empirical question.

*Temporal unit*: Annual composites (best dry-season 16-day composite per year) rather than 16-day interval regression. This provides 25 annual data points from the MODIS era, sufficient for regression against interannual climate indices.

*Index formulation*: A boundary index that is irradiance-neutral across forest and páramo canopy structures. One candidate is the ratio of the forest-zone NDVI to the páramo-zone NDVI rather than the absolute inflection altitude; this ratio partially cancels the irradiance effect if both canopy types respond proportionally. Whether the cancellation is sufficient requires explicit test.

*Mechanism candidates*: The emerging ecophysiology literature (Sanchez et al. 2025; and the Polylepis work at the Ecuadorian treeline) adds irradiance and cloud immersion as a third control mechanism that neither the temperature-isotherm model nor the moisture-deficit model captures. A temporal test that uses annual composites and interannual cloud-fraction indices as predictors would, for the first time, be able to assess the irradiance mechanism alongside the two prior candidates. Harsch and Bader (2011) noted that tropical cloud forest treelines occur at temperatures above what pure temperature limitation would predict; the ecophysiology literature now provides a mechanism candidate-irradiance limitation rather than temperature limitation-that could explain that elevation excess.

## Conclusion

The spatial tests of the isotherm prediction ([*Does the Isotherm Do Biological Work?*](posts/2026-05-31-qual-does-the-isotherm-do-biological-work-tes-b0af/); [*Temperature or Altitude?*](posts/2026-06-12-the-constant-temperature-prediction-a-cr-6675/)) concluded with indeterminate verdicts driven by instrument resolution. The temporal test evaluated here concludes before observation: the design is terminated by cloud physics, ecophysiology, and ecological inertia, none of which depends on the quality of the data that would be collected.

None of these terminations is a failure of the isotherm hypothesis. They are findings about the ecotone system and the instruments used to observe it. The ecotone does not track seasonal climate at the surface; it responds-slowly-to multi-decadal forcing. When observed through the cloud envelope, it expresses primarily its photoenergetic state rather than its moisture or temperature regime. And the available sensor cannot, by construction, resolve the boundary displacement that seasonal forcing would produce even if the biology were responsive to it.

The right temporal test is a 25-year interannual design using annual composites. The right sensor is cloud-independent. The right index is irradiance-corrected. And the right mechanism space now includes three candidates, not two. Building that test is the next step.

## References

- Harsch, M.A. and Bader, M.Y. (2011). "Treeline form-a potential key to understanding treeline dynamics." *Global Ecology and Biogeography* 20: 582–596. https://doi.org/10.1111/j.1466-8238.2010.00622.x

- Körner, C. (2012). *Alpine Treelines: Functional Ecology of the Global High Elevation Tree Limits*. Springer, Basel.

- Lutz, D.A., Powell, R.L., and Silman, M.R. (2013). "Four decades of Andean timberline migration and implications for biodiversity loss with climate change." *PLOS ONE* 8(9): e74496. https://doi.org/10.1371/journal.pone.0074496

- Sanchez, A., Mercado, L.M., Posada, J.M., and Smith, M. (2025). "Seasonal ecophysiology of two páramo species: the dominance of light over water limitations." *Frontiers in Plant Science* 16: 1529852. https://doi.org/10.3389/fpls.2025.1529852

- "Cold and low irradiation shape *Polylepis reticulata*'s seasonal growth and water use dynamics at the Ecuadorian Andean tree line." (2025). *Frontiers in Plant Science* 16: 1675655. https://doi.org/10.3389/fpls.2025.1675655
