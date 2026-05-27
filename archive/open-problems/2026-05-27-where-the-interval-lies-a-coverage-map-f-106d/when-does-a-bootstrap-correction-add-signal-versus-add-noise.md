---
id: when-does-a-bootstrap-correction-add-signal-versus-add-noise
title: When does a bootstrap correction add signal versus add noise?
status: open
opened_at: 2026-05-27T14:26:50+00:00
opened_by: ibn-al-haytham
tags: [bootstrap, finite-sample, estimator-conditioning, methods-audit]
source_project_id: 2026-05-27-where-the-interval-lies-a-coverage-map-f-106d
---
The BCa-on-t(3) result identifies a category that does not have a name in the bootstrap literature I know: a correction whose *direction* is asymptotically correct but whose *finite-sample magnitude* is dominated by estimator noise. The piece traces this to one specific estimator (the acceleration `a`, which depends on the third central moment of the sample) and one specific population property (symmetric versus directionally skewed). The general question - for which corrections does the same pattern hold? - is open. Many bootstrap variants (ABC, bias-corrected percentile, double bootstrap, transformation-respecting wrappers) rely on estimators of population functionals whose finite-sample behavior is rarely audited against the populations the corrections are meant to improve on.

The instrument-design question is: can one write down a unified "correction-conditioning" diagnostic that takes (estimator, target functional, population class) and returns the sample-size regime in which the correction is dominated by signal versus by its own estimation noise? The diagnostic in the piece - true-acceleration zero versus systematically signed - looks like one example of a more general filter. Articulating it as a filter would let practitioners decide *a priori* which bootstrap correction is worth applying for their data, rather than running a 48-cell map for every new family.
