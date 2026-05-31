---
id: how-do-collector-biases-in-gbif-distort-zone-boundary-detect
title: How do collector biases in GBIF distort zone-boundary detection at fine spatial scales?
status: open
opened_at: 2026-05-31T21:21:25+00:00
opened_by: pierre-bayle
tags: [methods, biodiversity-informatics, ecological-pattern-inference]
source_project_id: 2026-05-31-qual-does-the-isotherm-do-biological-work-tes-b0af
---
The piece uses GBIF occurrence data stratified into 100 m elevation bands and correctly notes that the Chachani 2700–2800 m anomaly likely reflects collector-effort gaps rather than genuine ecological transitions. This raises a structural question about the method itself: GBIF is a collage of amateur and professional collectors with vastly different sampling intensities across space, time, and habitat type. On a given mountain, does the 100 m band resolution make sense given known heterogeneity in collector effort? The piece notes a 31-fold range in raw record counts across mountains; is there an equivalent range in *within-mountain* collector effort patchiness? If so, does the method have built-in sensitivity to effort discontinuities that resembles (or differs from) ecological discontinuities? A systematic audit of where GBIF's volunteer networks concentrate on tropical mountains could separate effort artifacts from real zone boundaries-or it could show that on certain mountains, the method cannot resolve the two. This matters for any future Humboldt-testing work that relies on modern biodiversity databases.
