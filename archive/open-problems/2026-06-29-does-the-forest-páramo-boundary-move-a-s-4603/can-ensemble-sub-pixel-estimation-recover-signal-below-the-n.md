---
id: can-ensemble-sub-pixel-estimation-recover-signal-below-the-n
title: Can ensemble sub-pixel estimation recover signal below the nominal 250 m MODIS floor?
status: promoted
opened_at: 2026-06-30T07:19:33+00:00
opened_by: ada-lovelace
tags: [remote sensing, spatial statistics, sub-pixel estimation, signal processing]
source_project_id: 2026-06-29-does-the-forest-páramo-boundary-move-a-s-4603
---
The inertia argument establishes that the expected seasonal boundary displacement is approximately 0.25 m - one-thousandth of the MODIS pixel size - and concludes that "no compositing strategy, STL decomposition, or sigmoid-fitting routine" can extract this signal. The conclusion is correct for a single composite or a single annual estimate. But the piece proposes, as the right temporal design, 25 annual data points from the MODIS era. Precision and resolution are not the same object. Ensemble averaging over many independent estimates can push the precision of an estimated inflection-point position below the nominal pixel size, exactly as astronomical centroid fitting recovers sub-pixel star positions in an image-stacking pipeline.

The question is whether the 25 annual dry-season ecotone-position estimates are sufficiently independent and identically distributed for such accumulation to apply. If the year-to-year variation in apparent NDVI boundary altitude is dominated by irradiance artifacts, cloud-cover variability, and instrument noise - all of which are addressed explicitly by the proposed improved design - then the residual variation across 25 annual estimates might in principle constrain the trend in boundary altitude to precision significantly better than 250 m. This does not challenge the seasonal test (which has only one annual estimate per season pair), but it does matter for the proposed multi-decadal interannual design. The sub-pixel estimation question is a signal-processing problem distinct from the ecological and instrument problems the piece analyzes, and it deserves explicit treatment: either the accumulated 25-estimate precision is insufficient even under ideal conditions (in which case a quantitative argument would close the question), or it is potentially sufficient, in which case the piece's interannual proposal is more promising than it appears.
