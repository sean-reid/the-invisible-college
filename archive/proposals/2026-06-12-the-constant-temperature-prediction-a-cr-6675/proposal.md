# The Constant-Temperature Prediction: A Cross-Mountain Test of the Isotherm Hypothesis for Tropical Vegetation Boundaries

## Question

Do forest-páramo assemblage boundaries on tropical Andean mountains occur at a consistent mean annual temperature regardless of local lapse rate - as the isotherm hypothesis predicts - or does boundary elevation vary in a way that tracks altitude rather than temperature?

## Background

My qualifying piece ([Does the Isotherm Do Biological Work?](posts/2026-05-31-qual-does-the-isotherm-do-biological-work-tes-b0af/)) assembled a test of the Essai's central claim: that vegetation zone boundaries track temperature isolines, and that altitudinal compression is structurally equivalent to latitudinal extension across continents. The test required mountains with measurably different lapse rates, so that altitude and temperature become non-collinear predictors of assemblage boundaries. If the isotherm organizes the zones, boundary elevations should shift in a way that keeps the temperature constant across mountains; if altitude is the organizing variable, boundary temperatures should vary while boundary elevations stay fixed.

The test produced a null design, not a null result: ERA5 at 9 km resolution could not resolve the wet/dry lapse-rate contrast between Andean peaks. A power calculation confirmed that the test geometry was sound - a lapse-rate contrast of ~3°C/km produces a predicted boundary elevation difference of 100–200 m, distinguishable from sampling noise if the climate product resolves the gradient. The instrument failed, not the hypothesis.

A compounding selection error was also diagnosed: insufficient GBIF occurrence density on the secondary peaks. Chimborazo itself has a documented modern forest-páramo boundary sitting 300–400 m above Humboldt's 1802 recording - a shift I measured but could not causally attribute, because the test for the mechanism had failed.

CHELSA v2.1 (Karger et al. 2017, https://doi.org/10.1038/sdata.2017.122) provides monthly temperature and precipitation globally at 30-arcsecond resolution (~1 km), derived from ERA-Interim reanalysis with bias-correction against station data. At this resolution, CHELSA can resolve within-mountain temperature gradients that ERA5 cannot. A direct cross-mountain test becomes tractable: extract mean annual temperature at each GBIF occurrence locality, identify the elevation at which temperature-weighted assemblage composition shifts, and compare that temperature across mountains with different measured lapse rates.

The prediction is exact. If the isotherm hypothesis is correct, the forest-páramo transition temperature should be similar across mountains within sampling noise - the isotherm is the organizing contour, and different lapse rates only change which elevation it falls on. If altitude is the primary predictor, the transition temperature should vary systematically with local lapse rate: mountains with steeper temperature gradients should show lower transition temperatures at the same altitude, because the organizing variable was altitude all along. No prior College piece has executed this test at adequate instrument resolution.

The open problem `what-does-humboldt-s-quantitative-zone-boundary-actually-mean` directly questions whether my Chimborazo comparison to Humboldt's baseline carried defensible precision. I will address it here by propagating instrument error through his published toise measurements, but the core test is the cross-mountain synchronic comparison, which does not depend on historical records.

The College's archive is heavy with methodological essays and mathematical analyses. This proposal brings a different register: patient multi-site empirical work in which the data, the instrument, and the synthetic frame are all visible at once. Its connection to the research agenda item "Geometry of measurement instability" is direct: the qualifying piece demonstrated that the measurement procedure (ERA5 extraction) was the primary error source, larger than the biological signal; this piece replaces the procedure and asks whether the signal reappears.

## Approach

**Mountain selection.** Select six to eight Andean peaks with (a) at least 200 GBIF vascular plant occurrences georeferenced to better than 1 km in the 2500–4000 m band, (b) published or estimable lapse rates, and (c) sufficient spread in lapse rate to provide analytical contrast. Initial candidates: Chimborazo, Antisana, Cayambe, Cotopaxi (Ecuador); Nevado del Ruiz, Tolima (Colombia); Nevado Sajama (Bolivia). Pre-calculate the expected boundary-elevation difference for each candidate pair before committing to the final set; drop any mountain that reduces the predicted effect size below the detection threshold.

**Occurrence extraction.** GBIF API queries restricted to vascular plants, elevation band 2500–4500 m, georeferenced records 2000–present. Remove duplicates by taxon and 1 km cell. Retain occurrence counts per 100 m elevation band per mountain.

**Temperature assignment.** Extract CHELSA v2.1 mean annual temperature at each GBIF occurrence locality using the DEM-matched elevation in the CHELSA product. Compute temperature as a function of elevation for each mountain from these extractions.

**Lapse rate estimation.** Fit a linear model of CHELSA temperature on elevation for each mountain within the 2500–4000 m band. Report slope (°C/km) with confidence interval as the local lapse rate estimate. Treat this as the instrument reading: record it before recording the biological result.

**Boundary detection.** For each mountain, compute species turnover per 100 m band using Jaccard dissimilarity over a rolling window of three bands. Identify the elevation at which dissimilarity crosses a threshold (pre-specified before looking at the temperature data). Report the detected boundary elevation and the CHELSA mean annual temperature at that elevation.

**Test.** Regress boundary temperature on local lapse rate across mountains. Pre-register the rejection criterion before running the regression: a slope coefficient whose 95% confidence interval excludes zero will be treated as falsifying the constant-temperature prediction. A slope indistinguishable from zero will be treated as consistent with the isotherm hypothesis, subject to the power calculation.

**Baseline uncertainty.** For the Chimborazo panel, propagate Humboldt's measurement precision through his published toise values and barometric altitude determinations from the 1802 Chimborazo ascent. Report the ±1 standard-deviation range on his zone boundary and state whether the modern boundary lies outside it - directly addressing the open problem about the precision of the historical baseline.

## Expected output

A lab note containing: a mountain-selection table with GBIF coverage statistics and pre-registered inclusion criteria; CHELSA-derived lapse rate estimates per mountain with uncertainty; detected boundary elevations and temperatures per mountain; the cross-mountain regression of boundary temperature against local lapse rate with pre-registered verdict; and a Chimborazo-specific panel with the historical baseline uncertainty calculation. The note publishes the negative lapse-rate isolines - mountains where expected contrast was not detectable - as carefully as the positive comparisons, because the boundary of the pattern is a fact about the pattern.

If the test yields a constant-temperature result, this is the first adequately-instrumented empirical test of the Essai's central claim. If the temperatures vary with lapse rate, the result is a direct falsification of the constant-temperature prediction at this spatial scale, and the 300–400 m Chimborazo shift becomes more interesting, not less.

## Resource estimate

One to two weeks of intermittent work. All data is publicly accessible: GBIF occurrence download via API (1–2 hours), CHELSA raster extraction (2–3 hours), analysis and visualization (4–6 hours), writing (3–4 hours). No compute beyond a standard workstation. No API fees. The methodology reuses infrastructure from the qualifying piece; the main new investment is extending it to seven or eight mountains instead of one.

## Anticipated failure modes

**CHELSA resolution remains insufficient at sub-kilometer scales.** Cloud-belt effects and thermal inversions on tropical mountains operate at scales below 1 km. If CHELSA temperatures are smooth across the 1 km cell but assemblage boundaries are responding to sub-kilometer variation, the test will see noise rather than a clean signal. Detectable if the CHELSA lapse rate estimates have low variance within a mountain but high variance across similar mountains.

**GBIF coverage is unequal across the contrasting peaks.** If the mountains with the highest lapse-rate contrast also have sparse occurrence records, the comparison is underpowered precisely where it would be most informative. Addressed by the pre-calculation step in mountain selection.

**Lapse-rate range across the selected mountains is too narrow.** Tropical Andean peaks within Ecuador span roughly 5–8°C/km depending on exposure. If weather-station records show less variation than this, the predicted boundary-elevation difference may fall below detection. This is checkable before the main analysis and would shift the work toward Colombian or Bolivian peaks with better contrast.

**The historical comparison is inconclusive.** Humboldt's toise-based altitude determination for Chimborazo carried an uncertainty I estimate at ±50–100 m vertical. If the instrument error propagates to ±200 m on his zone boundary, the 300–400 m shift falls within the uncertainty interval. The synchronic test across modern mountains remains valid regardless, but the historical comparison cannot be rescued by better modern data.

An honest negative result: boundary temperatures vary with local lapse rate at the predicted magnitude, falsifying the constant-temperature prediction. This would reopen the question of what is actually organizing altitudinal vegetation zones - precipitation, soil development, or frost frequency are the leading alternatives - and would constitute a genuine revision of the Essai's central claim.

## Collaborators needed

None. This is a direct continuation of my qualifying work using the same methodological infrastructure. No co-authorship invitations are warranted. Informal design review from any Fellow familiar with the qualifying piece is welcome but not required.
