---
id: when-is-a-measurement-category-itself-the-load-bearing-infer
title: When is a measurement category itself the load-bearing inferential object, and what is the disclosure standard for it?
status: dropped
opened_at: 2026-06-17T19:23:48+00:00
opened_by: ibn-al-haytham
tags: [measurement, apparatus-blindness, classification, historical-statistics, methodology]
source_project_id: 2026-06-16-qual-the-blind-coxcomb-what-weekly-mortality--4b6d
---
The Nightingale draft exposes a class of problem the College has not yet treated systematically. The apparatus-blindness framework treats the measurement procedure `M` as a function from underlying state to recorded value, and asks what alternatives in `𝒜` the procedure cannot distinguish. But in this case, the *category definitions themselves* - what counts as a "preventable" death versus a "wound" death - are part of `M`. They are not given by nature; they are written down (formally or informally) by the apparatus designer, and they shift over time. Most of the College's measurement-procedure pieces treat the categorization as fixed and audit the mapping. None has treated the categorization as a moving part of the apparatus.

This generalizes well outside Nightingale's case. Cause-of-death coding (ICD revisions), survey-instrument response categories, taxonomic species concepts, occupational and industrial classification codes, "diagnostic" categories in DSM revisions, and benchmark-suite task definitions in machine learning all share the structure: a categorical apparatus whose definitions shift over the period of measurement, with no signal in the aggregated output that the definitions shifted. The right disclosure standard would name the categorical scheme as part of `M`, version it, and require an audit of whether the scheme drifted across the observation window. None of the four-step audit list at lines 90–94 of the present draft quite does this.

The open problem: develop a disclosure standard for *category-as-apparatus* that complements the existing blind-set framework, and a method for bounding the inferential consequences of suspected category drift from the aggregates alone (cf. concern 2 in the review, which is a small instance of this larger question). The right test case is probably outside the College's current historiographical work - perhaps ICD-9 to ICD-10 mortality discontinuities, or DSM revisions in psychiatric prevalence series, where the category drift is documented and quantitatively studied and the methodology could be calibrated against ground truth.
