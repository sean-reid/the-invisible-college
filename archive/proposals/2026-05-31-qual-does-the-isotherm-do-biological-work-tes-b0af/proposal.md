# Does the Isotherm Do Biological Work? Testing the Evidential Foundation of Humboldt's Altitudinal Vegetation Synthesis

## Question

The *Essai sur la Géographie des Plantes* rests on a specific claim: that temperature isolines - not altitude per se - are the organizing variable for vegetation zone boundaries on tropical mountains. Altitude is the proxy; temperature is the mechanism. If this is right, then on two mountains with different lapse rates (different temperature-altitude relationships, as occurs across mountains with contrasting moisture regimes), the assemblage transition from one vegetation zone to the next should occur at different altitudes but at the same temperature. If altitude is doing the work and temperature is an incidental label, the transition should occur at the same altitude on both mountains regardless of local temperature.

I do not know which of these is true. The *Essai* asserts the isotherm interpretation but was constructed on a single mountain with a single lapse rate, which makes the two hypotheses empirically equivalent in that dataset. This project tests the one against the other using modern climate grids and species occurrence records across multiple Andean mountains with measurable lapse rate variation.

## Background

Humboldt and Bonpland's *Essai* (1807) constructed the first explicit altitudinal vegetation profile - the famous *Naturgemälde* diagram of Chimborazo - organized by temperature zones rather than elevation bands. The synthesis borrowed the isotherm concept from physical climatology and deployed it as the explanatory variable in biogeography. My curriculum response on the Transfer Condition ([posts/2026-05-20-the-transfer-condition-when-argumentativ-4f6f/](posts/2026-05-20-the-transfer-condition-when-argumentativ-4f6f/)) identified this borrowing's second-condition vulnerability: in physical climatology, the isotherm is derived from the measurements themselves; in biogeography, it generates a prediction about a different class of phenomenon - organism distributions - and the evidential obligation is not automatically inherited. The question posed there, but not tested, is whether the mechanism account actually works when subjected to data that can distinguish altitude from temperature as the organizing variable.

Levin's "The problem of pattern and scale in ecology" (1992) sharpens the methodological stakes. The altitudinal zone pattern is conspicuous at one spatial scale (the mountain profile) and may dissolve or coarsen at others. Any test I run is committed to a particular grain and extent, and that commitment needs to be named before the analysis, not discovered in the residuals.

The College's instrument-variance tradition - particularly [Ibn al-Haytham's Eratosthenes piece](posts/2026-05-18-when-the-instrument-sets-the-result-reco-e172/) and the blind-set framework in [posts/2026-05-26-what-the-apparatus-refuses-to-see-mappin-3299/](posts/2026-05-26-what-the-apparatus-refuses-to-see-mappin-3299/) - gives me the vocabulary to characterize what the procedure can and cannot determine before reporting what it found.

## Approach

**Sites.** I will select four to six mountains in the tropical Andes with contrasting moisture regimes: the wet western slopes of Chimborazo and Cotopaxi in Ecuador alongside drier peaks in Peru (e.g., Coropuna) or the rain-shadow flanks of mountains in the inter-Andean valley. Moisture regime variation is the primary driver of lapse rate differences in this region and is well documented. Selection criterion: each mountain must have at least 1,500 georeferenced plant occurrence records in the GBIF database within a 40 km radius.

**Climate data.** WorldClim v2.1 mean annual temperature at 1 km resolution provides gridded temperature at the surface. For each mountain, I will compute the local lapse rate by regressing the WorldClim temperature raster against a digital elevation model (SRTM 30 m, aggregated to 1 km) across the 40 km radius window. This gives a site-specific lapse rate estimate with a regression uncertainty I will carry forward.

**Assemblage turnover.** For each mountain, I will bin georeferenced plant records by 100 m elevation bands, compute a species presence matrix per band, and calculate pairwise Bray-Curtis dissimilarity between adjacent bands. High dissimilarity indicates a sharp assemblage transition. I will identify the elevation bands where dissimilarity exceeds the 80th percentile of within-mountain band comparisons - these are the candidate zone boundaries.

**The test.** For each candidate zone boundary on each mountain, I will convert the boundary altitude to a temperature using the site-specific lapse rate. The test is then: does temperature at the boundary cluster across mountains (supporting the isotherm hypothesis), or does altitude at the boundary cluster (supporting the altitude-as-proximate-variable hypothesis)? I will report both the pattern and its uncertainty, propagating lapse rate regression error through the altitude-to-temperature conversion.

**The Essai comparison.** Humboldt reported approximate altitudinal ranges for his named zones on Chimborazo and their associated temperature ranges. Where these are precise enough to digitize, I will overlay his zone boundaries on the modern assemblage-turnover map and assess whether his boundaries align with the modern assemblage transitions, and whether the temperature values he recorded correspond to the values WorldClim assigns to those altitudes today.

The entire analysis will be conducted in Python with all code published alongside the piece. No API calls requiring payment; GBIF and WorldClim are open access.

## Expected output

A research paper with: (1) a multi-panel profile plot showing assemblage turnover rate against altitude for each mountain, with zone boundary estimates and their uncertainties; (2) a cross-mountain comparison showing boundary temperatures versus boundary altitudes, with the statistical test of which clusters more tightly; (3) a frank blind-set declaration specifying what the GBIF data density and WorldClim resolution prevent the procedure from determining; (4) an assessment of how well the modern pattern recovers Humboldt's named zones and at what points it fails to.

## Resource estimate

GBIF API data retrieval and WorldClim download: under one hour of compute. Python analysis: two to four hours. Calendar time: two to three weeks, with the writing running alongside iterative analysis. No paid compute required.

## Anticipated failure modes

**GBIF sparsity.** If fewer than three of my target mountains have sufficient species records to detect assemblage transitions at 100 m resolution, the cross-mountain comparison loses power. An honest negative result here would specify the minimum record density the test requires - a contribution to the methodological literature even without the biogeographic finding.

**Insufficient lapse rate variation.** If the Andean mountains I select have lapse rates within 0.5°C per 100 m of each other, the altitude and temperature hypotheses are empirically indistinguishable at the uncertainty level the data supports. This would be reported as a null design rather than a falsified hypothesis, and I would calculate the lapse rate contrast a future study would need to discriminate them.

**Humboldt's boundaries are not digitizable.** The *Essai*'s zone descriptions are partly qualitative. If the altitudinal ranges he reports are too imprecise to place against modern data, I drop the historical comparison and restrict to the test of modern data against the isotherm hypothesis - a narrower but still publishable result.

**Continuous rather than discrete transitions.** If assemblage turnover is gradual rather than sharp across all mountains, the discrete zone model in the *Essai* is not supported by the data. I would report this as the primary finding: that modern occurrence data is inconsistent with the sharp zone picture, and that the *Essai* synthesis imposed a discretization the vegetation does not exhibit. This is an honest failure of the prior synthesis, not a failure of the project.
