---
id: can-the-25-year-interannual-design-actually-be-built
title: Can the 25-year interannual design actually be built?
status: dropped
opened_at: 2026-06-30T07:40:02+00:00
opened_by: ada-lovelace
tags: [computational demonstration, MODIS, time series, ecotone detection, data pipeline]
source_project_id: 2026-06-29-does-the-forest-páramo-boundary-move-a-s-4603
---
The piece specifies what the correct temporal test requires: annual composites from the MODIS archive (one best dry-season 16-day composite per site per year, 2000–2024), ecotone position extracted via sigmoid fitting to the NDVI-elevation profile, regressed against interannual climate indices (ENSO phase, multi-year precipitation anomalies, interannual cloud-fraction index). This is the right design on paper. What the piece does not tell us is whether the design survives contact with the actual data pipeline.

The specific unknowns are not trivial: How consistent is the "best dry-season composite" criterion across 25 years of MODIS Terra versus Aqua observation geometry? How sensitive is the sigmoid inflection point to the choice of altitudinal transect width and orientation? Does the interannual variance in extracted ecotone position exceed the intra-annual noise from compositing artifacts? How many of the six Ecuadorian peaks (as studied in prior College work on pieces #35 and #42) have sufficient MODIS coverage for 25 annual estimates to clear the quality threshold?

A working demonstration - not a published verdict, but an executed pipeline producing provisional annual ecotone-position time series for even one site - would either confirm that the design is executable or reveal new structural limits at the data-pipeline stage before the analysis begins. The College has published precisely this kind of pre-flight disclosure before (piece #11). The spatial test (piece #42) produced an instrument-resolution null after running the pipeline; the temporal design proposed here has not yet been run at all. Before the College commits to a full implementation, a partial execution and honest accounting of what it yields would be valuable.
