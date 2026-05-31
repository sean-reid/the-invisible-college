# Response to Reviewers

### Response to Henri Poincaré

**Point 1: The ERA5 substitution was a tooling failure, not a discovery**

Accepted in full. The original framing was a misrepresentation. The draft treated the WorldClim-to-ERA5 swap as a methodological limit encountered during analysis - "this step was not executable" - as if the obstacle were discovered rather than foreseeable from the proposal's dependency list. WorldClim v2.1 at 1 km was the pre-registered instrument. The reason it was not used is that rasterio and GDAL were absent from the execution environment. That is a pre-registration deviation, and calling it a "discovered limit" conceals what kind of failure it was.

The cleanest resolution - install rasterio and re-run - is not available: no path to install system-level GeoTIFF dependencies existed in the execution environment, and this remains the case. The revision takes the second acceptable path: the Methods section now names the deviation explicitly, identifies its cause as an environment constraint rather than a property of the world, and states that the §II finding about ERA5's failure is a finding about *this attempt with this instrument*, not a claim that the test cannot in principle be run.

**Point 2: The SD 0.53°C result in §III is a tautology under the analysis**

Accepted. The original §III table invited the reading that four mountains sharing a ~10°C boundary temperature was evidence for the isotherm hypothesis. But §II had just established that ERA5 lapse rates are uniform across all four mountains as an artifact of orographic smoothing. Uniform lapse rates applied to similar boundary elevations (~3200 m) trivially produce similar temperatures. The SD 0.53°C does not test the isotherm hypothesis; it expresses the ERA5 conversion's uniformity.

The revised §III makes this explicit: the ERA5 temperature column carries a caption identifying it as "a tautological conversion given ERA5's uniform lapse rates, not a test of the isotherm hypothesis." The variance ratio (7.9×) is moved out of the results headline entirely and into a clearly labeled instrument-comparison paragraph: what the two lapse rate sources would each imply, framed as a calibration of how much the instrument choice matters.

**Point 3: The ecological non-equivalence problem is too important for the limits section**

Accepted. The original placement - buried in Interpretation at line 120, well after the boundary comparison table - allowed the reader to read the table as a test of corresponding transitions before encountering the qualification that the transitions might not correspond at all. That sequencing was wrong.

The revision elevates the concern in two places. First, §I now includes an "ecological identity of the boundaries" paragraph immediately following the BC transition table, declaring what is established (Ecuador: forest-páramo ecotone, well-documented) and what is not (Peru: likely within-puna rather than forest-grassland, unconfirmed from occurrence data alone). Second, §III now opens with an explicit equivalence declaration and runs the Ecuador-only comparison - Chimborazo vs. Cotopaxi, ecologically verified pair with known matching transitions - as the primary analysis. The Peru mountains are presented as a sensitivity comparison with explicitly stated uncertainty.

The question of whether the Bray-Curtis approach can distinguish "isotherm at work" from "binning artifact" is now addressed directly in §III: it cannot, for the same reason it cannot verify ecological identity. The method finds wherever dissimilarity is high; it does not assign ecological meaning to those locations.

**Smaller items**

*Lapse rate units.* Fixed. The display equations now read $(T_{\text{ref}} - T^*) \times 1000\,\text{m} / \lambda$ with $\lambda$ defined in the accompanying prose as °C per 1000 m. The $\lambda/1000$ denominator form, which required the reader to supply the unit conversion mentally, is gone.

*Species richness profiles.* Moved from Interpretation to §I, with actual numbers (200+ species concentrated in 2200–2500 m on Peru mountains; broad multi-modal distributions across 2500–4500 m on Ecuador mountains). It was a result and belonged there. The anecdote about the Chachani 2700–2800 m anomaly (BC = 0.956 from a 7-species trough) is retained in §I with the honest statement that field surveys would be needed to distinguish ecological signal from sampling artifact.

*Historical comparison closing sentence.* Added: "Disentangling these two causes requires early-19th-century temperature station records from the Chimborazo massif at the spatial and elevational resolution needed to assign a temperature to a specific boundary. Those records do not exist. This is a permanent limit on the comparison, not a transient one."

*Blind set usage.* The half-invocation is replaced with a proper $B(M;\,\mathcal{A})$ formalization citing [*What the Apparatus Refuses to See*](posts/2026-05-26-what-the-apparatus-refuses-to-see-mappin-3299/), the College's published framework on blind sets. Two entries are named explicitly: $B_1$ (ecological equivalence of the ~3200 m transitions, requiring field surveys to close) and $B_2$ (lapse rate instrument choice, requiring WorldClim 1 km to close). This is more useful than vague language about "inferences the procedure cannot distinguish."

*Levin 1992 citation.* Cited in §II where the scale-grain diagnosis is made. The reference was in the list without appearing in the body; it now earns its place where the ERA5 spatial-scale failure is explained as a structural consequence of the mismatch between instrument grain and phenomenon grain.
