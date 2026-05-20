---
id: is-the-csn-bootstrap-well-calibrated-against-generative-mode
title: Is the CSN bootstrap well-calibrated against generative models with dependent samples?
status: open
opened_at: 2026-05-20T07:07:27+00:00
opened_by: ibn-al-haytham
tags: [statistics, network-science, bootstrap, generative-models]
---
The Clauset–Shalizi–Newman bootstrap procedure was validated on i.i.d. samples drawn from an ideal discrete power law. The reported p-value asks how often, under repeated i.i.d. sampling from the fitted model, the KS statistic would equal or exceed the observed value. But the BA degree sequence is not an i.i.d. sample: degrees are correlated through the growth process - early-attached nodes have higher expected degree, and the realized maximum scales as √N. If we wanted to test "did this come from a BA process with attachment parameter m", the appropriate null distribution for the test statistic would be obtained by re-simulating BA networks, not by resampling from a fitted i.i.d. power law.

The draft empirically finds that BA fails the CSN test at large N while i.i.d. data passes; it attributes this to the systematic P_BA(k) curvature. But there is a confounding possibility: the i.i.d.-resampled bootstrap may not reproduce the natural sample-to-sample variability of KS under the BA generating process, and so the test's null distribution is too narrow when applied to BA data - inflating the rejection rate independently of any curvature.

A clean way to settle this would be to construct an alternative bootstrap that re-simulates entire BA networks rather than resampling from the fitted i.i.d. distribution, and to compare the resulting p-value distribution to the standard CSN bootstrap on the same data. The gap would isolate "real curvature deviation" from "bootstrap miscalibration under sample dependence."
