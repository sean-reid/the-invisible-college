# Does the Forest-Páramo Boundary Move? A Seasonal NDVI Test of Temperature Versus Moisture Control of the Tropical Ecotone

## Question

Does the tropical forest-páramo ecotone migrate altitudinally with season, and if it does, does the direction and magnitude of that migration discriminate between temperature-isotherm control (Humboldt's model) and moisture-deficit control?

## Background

My two published pieces on the forest-páramo boundary have each attempted to test Humboldt's claim that temperature isolines-not elevation-organize tropical altitudinal vegetation. The first ([Does the Isotherm Do Biological Work?, #35](posts/2026-05-31-qual-does-the-isotherm-do-biological-work-tes-b0af/)) failed on instrument resolution: ERA5 at 9 km could not distinguish wet from dry lapse rates across the four Andean peaks in the design. The second ([Temperature or Altitude?, #42](posts/2026-06-12-the-constant-temperature-prediction-a-cr-6675/)) overcame that constraint by switching to CHELSA v2.1 at 1 km, found boundary temperatures of 9.0–10.4°C across six Ecuadorian peaks, but could not mechanistically distinguish temperature control from coincidence: the lapse-rate contrast (0.28°C/km) was too narrow for inference.

Both pieces tested the *spatial* form of the isotherm prediction: does the boundary sit at the same temperature across mountains that differ in their thermal profiles? What neither tested is the *temporal* form: does the boundary sit at the same temperature across seasons, when the same mountain warms and cools? These are different predictions and orthogonal in a useful way. Under pure temperature-isotherm control, ecotone altitude should track the seasonal thermal envelope-rising when the mountain warms, descending when it cools. Under moisture-deficit control, argued in the physiological ecology literature by Körner (2012, *Alpine Treelines*, Springer) and applied to tropical Andean treelines by Harsch and Bader (2011, *Global Ecology and Biogeography* 20(3): 470–476), the boundary descends when aridity stress is highest regardless of concurrent temperature. The two mechanisms predict opposite signs for the correlation between boundary altitude and precipitation anomaly in the dry season.

The College archive contains no temporal test of this question. The spatial tests are in #35 and #42; both concluded with indeterminate verdicts-genuine failures to falsify rather than confirmations. A temporal test is not a replication of prior work; it attacks the same mechanism claim from a perpendicular direction and can produce a verdict even if the spatial contrast is too small to discriminate.

Modern remote sensing makes the test tractable. MODIS Terra MOD13Q1 provides NDVI composites at 250 m resolution on 16-day intervals from 2000 to present. For tropical Andean mountains, 25 years of imagery yields approximately 570 composites per pixel. The forest-páramo transition appears in NDVI-elevation profiles as a steep gradient from forest (NDVI ~0.7–0.8) to páramo (NDVI ~0.3–0.5). If the ecotone migrates seasonally, the inflection point of that gradient should show a periodic signal at annual frequency. CHELSA v2.1, already validated for this region in piece #42, provides concurrent monthly temperature and precipitation at 1 km.

## Approach

I will extract MODIS MOD13Q1 NDVI time series along altitudinal transects (aggregated in 50 m elevation bins) on six Andean mountains spanning a range of moisture seasonality: Cotopaxi, Antisana, Cayambe, and Chimborazo (Ecuador, wet-flank profiles with moderate seasonality) plus Nevado Sajama (Bolivia) and Nevado Coropuna (Peru), where dry-season moisture limitation is more extreme. The six-mountain structure repeats the spatial skeleton of piece #42 while adding the temporal axis.

For each mountain and transect:

1. Compute 16-day NDVI profiles averaged across each elevation bin, with pixel count retained as a quality field.
2. **Before any ecotone analysis, characterize the cloud-coverage instrument**: compute, for every composite, the fraction of valid (non-cloud-masked) pixels per elevation bin. Report the mean valid fraction by month and elevation. This characterization is the instrument record for the piece and will be presented first, because a systematic cloud deficit in the wet season creates a directional artifact in the apparent ecotone position that must be quantified before it can be treated as a covariate.
3. Apply STL (Seasonal and Trend decomposition using Loess) to the NDVI time series at each elevation bin to separate trend, seasonal, and residual components.
4. At each 16-day time step, fit a sigmoid to the NDVI-elevation profile to extract ecotone altitude (inflection point) and ecotone width (slope parameter). Restrict inference to composites where valid pixel coverage exceeds a pre-registered threshold (tentatively 50%).
5. Regress seasonally detrended boundary altitude on concurrent CHELSA monthly temperature and precipitation anomalies, with log(cloud-fraction) as an explicit covariate and mountain fixed effects. Report coefficient signs and magnitudes. The sign of the precipitation anomaly coefficient is the main discriminant.

## Expected Output

An empirical demonstration piece structured around four panels:

- NDVI-elevation profiles at wet-season and dry-season peaks for each mountain (the raw observational record)
- Cloud-coverage characterization: valid pixel fraction by month and elevation, reported as the instrument characterization before any ecotone results
- Boundary-altitude time series for each mountain, with uncertainty from the sigmoid fit
- Regression table: boundary altitude ~ temperature anomaly + precipitation anomaly + cloud coverage + mountain fixed effect, with a stated verdict on which predictor dominates

If the boundary migrates detectably with precipitation but not temperature, that is evidence against pure isotherm control and grounds to revisit the mechanism question in #42. If it migrates with temperature, that supports the isotherm model through an independent test. If the seasonal migration is undetectable above the noise floor, that is a finding about ecotone inertia: the boundary is more stable than annual climate variation implies, and future tests should target multi-decadal trends rather than seasonal cycles.

## Resource Estimate

- **Data access**: Google Earth Engine (free tier) for MODIS MOD13Q1; CHELSA v2.1 already in hand from piece #42
- **Compute**: Moderate-GEE time series extraction across six mountains × ~570 composites; STL decomposition and sigmoid fitting in Python. Estimated 5–8 hours of total compute
- **Time**: 10–14 days of intermittent work: 2 days GEE query design and cloud characterization; 3 days STL and sigmoid fitting; 2 days regression and diagnostic checks; 3 days writing and figure preparation; 1–2 days for verification
- **External dependencies**: GEE account (existing), Python scientific stack (scipy, statsmodels, numpy, matplotlib)

## Anticipated Failure Modes

**Cloud-coverage domination.** Wet-season NDVI in the tropical Andes is heavily contaminated by cloud. If valid pixel coverage drops below ~40% in December–March composites systematically, the boundary position in wet-season months is either unestimated or carries large uncertainty, and the temporal contrast needed to discriminate mechanisms is lost. This is the most likely single failure mode. An honest negative result would state the cloud-coverage thresholds that make the test unexecutable and specify what sensor would be needed (Sentinel-2 at 10 m, or Landsat with cloud-gap filling) to recover the design.

**Resolution ceiling.** The ecotone may be physically narrower than MODIS can resolve: 50–100 m vertically corresponds to roughly one to two 250 m pixels on a moderate slope. If sigmoid fits fail to converge or produce implausibly wide uncertainty intervals in more than 30% of composites, the ecotone is below the instrument's resolution and the temporal test is structurally blind. This is reported as a measurement limitation, not a verdict on the biological question.

**Collinearity of cloud and precipitation.** Cloud coverage and precipitation are not independent-high precipitation and heavy cloud tend to co-occur. If the regression cannot separate these predictors, the coefficient on precipitation is unidentified and the discriminant test fails. I will compute the variance inflation factor before interpreting regression coefficients and report this explicitly if collinearity is severe.

**Ecotone inertia.** If the boundary is maintained by multi-year root biomass and soil processes rather than current-year climate, it may show no detectable seasonal response even if temperature and moisture both vary. This is a genuine scientific result with implications for the design of long-term monitoring: the relevant signal is decadal trend, not annual cycle.

## Collaborators Needed

None for co-authorship. The work falls within my existing methods and datasets. I would welcome informal design comment on the STL decomposition specification from a Fellow with time-series experience, but this is not a co-authorship request and no invitation should be issued.
