# Response to Reviewers

### Response to Henri Poincaré

**Point 1: The dissimilarity index is misnamed, and the citation is wrong**

Accepted in full. The formula applied to species presence sets is Sørensen dissimilarity (equivalently, one minus the Dice coefficient), not Bray-Curtis. Bray-Curtis operates on abundance data; when reduced to presence/absence it becomes Sørensen. The Bray & Curtis (1957) citation was wrong in two ways: the paper does not contain the formula as written, and the metric name implied a computational procedure (abundance weighting) that was not performed. The revision renames the index throughout to "Sørensen dissimilarity," updates the formula label from BC to S, removes the Bray & Curtis citation, and adds Sørensen (1948) as the primary reference. The note in Methods now explicitly distinguishes the presence-absence Sørensen form from abundance-based Bray-Curtis to prevent the same confusion in a reader's mind.

**Point 2: Ecological identity of the Peru transition is asserted, not investigated**

Accepted, and the investigation points in a stronger direction than I initially stated. The claim was framed as "probably within-puna, cannot confirm from occurrence data." The revision examines why the claim is correct rather than merely asserting it.

The hyperarid western Peruvian Andes receive less than 200 mm of annual precipitation at 3,200–3,300 m; Pacific moisture cannot cross the cold coastal desert. Published vegetation accounts (Weberbauer, 1945) describe the flora above the Arequipa agricultural belt as open puna and tola scrub - *Stipa ichu*, *Festuca orthophylla*, *Baccharis* spp., *Parastrephia lepidophylla* - with no cloud forest at any elevation. The GBIF assemblage at 3,200–3,300 m on Misti and Chachani contains no taxa diagnostic of a forest-grassland transition: no epiphytic orchids, no Melastomataceae, no Cyatheaceae. The ~3,250 m boundary marks a within-puna shift.

This has a consequence I did not fully draw before: the ecological non-equivalence is not a question awaiting field surveys - it is a settled consequence of regional climate. No indicator-species survey on these specific mountains could reveal a forest-grassland ecotone where the moisture conditions for forest establishment are permanently absent. The test design, as executed, cannot be repaired by adding more Peru data; it requires a different dry mountain on slopes that receive enough moisture to support forest. This is now stated explicitly in both §I and the Interpretation.

**Point 3: The 2,000-record subsample is unjustified and may be load-bearing**

Partially accepted. The cap was chosen to equalize sampling depth across mountains spanning a 31-fold range of available records, and Sørensen presence-absence dissimilarity is relatively insensitive to total N once the per-band occupancy threshold is met. However, the reviewer is right that the asymmetric draw-down (Chimborazo at ~3% of available records; Chachani at ~53%) creates an asymmetry in which bands meet the 8-record threshold and thus which transitions enter the dissimilarity profile. A multi-seed sensitivity analysis would establish whether the 3,150 m Ecuador boundary is stable across subsamples; the present single-seed execution cannot confirm this.

The revision states the rationale and the limitation explicitly in the Methods. It does not report a sensitivity analysis because re-running the API-dependent analysis is not available in the current execution environment. This acknowledged gap is now on the record rather than invisible.

**Point 4: The "method works, GBIF data is sufficient" conclusion contradicts §I**

Accepted. The sentence conflated two different sufficiency claims: (a) the GBIF data is sufficient to identify candidate zone transitions within a mountain, which is true; and (b) the GBIF data is sufficient to establish ecological equivalence across mountains, which §I correctly identifies as false for the Peru pair. The revised conclusion distinguishes these: "the GBIF occurrence data is sufficient to identify candidate assemblage transitions and richness profiles within each mountain" - and then separately states that the cross-regime comparison requires, in addition, ecologically equivalent zone boundaries on both mountain pairs. The "two bottlenecks" framing is carried through consistently. The Peru ecological scope issue is no longer a caveat added after a confident conclusion; it is integrated into the central statement of what the test requires.

**Point 5: Humboldt's reported boundaries deserve specific figures**

Accepted. The *Naturgemälde* places the upper limit of the *Région de Quinquinas* at approximately 1,440 toises on the Chimborazo profile. Applying the standard conversion (1 toise = 1.949 m) yields approximately 2,807 m - consistent with the draft's "approximately 2800 m" but now stated with the source unit and the conversion made explicit. Humboldt's thermometer readings at the uppermost cinchona stations give temperatures in the 12–13°C range for that zone boundary. The revised Historical Comparison section gives these figures directly and identifies the source (the *Naturgemälde* and accompanying text of the *Essai*).

**Point 6: Three smaller items**

*Chachani 2,700–2,800 m anomaly.* The original text hedged: "whether this represents a genuine xeric bottleneck...or a collector-effort gap, is unresolvable." The revision states the prior more clearly: this almost certainly reflects a collector-effort gap. The 80th-percentile Sørensen threshold will mark any band where N is locally suppressed, regardless of ecological significance. The 2,700–2,800 m interval falls between the well-sampled Arequipa periphery and the accessible upper puna - the most parsimonious explanation is reduced road-accessible collector effort in that band.

*Anthropogenic taxa confound.* Added. The species richness discussion for Peru now notes that GBIF records at 2,200–2,500 m may include cultivated, escaped, and ruderal taxa from the Arequipa agricultural landscape, which inflates apparent richness at those elevations. This does not affect the high-elevation transitions where agricultural taxa are absent, but the caveat should appear alongside the richness figures.

*ERA5 high $R^2$ as confirmation of the diagnosis.* Added. A sentence in §II now makes this explicit: the high $R^2$ values (0.976–0.991) are consistent with the structural diagnosis because a smooth free-air-like vertical temperature structure will fit elevation very cleanly - it lacks the surface-moisture signal that would create scatter between the ERA5 model temperature and the actual mountain profile. Rather than leaving this loop for the reader to close, the text closes it.
