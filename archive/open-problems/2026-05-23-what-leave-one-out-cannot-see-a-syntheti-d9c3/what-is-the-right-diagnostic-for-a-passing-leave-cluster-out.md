---
id: what-is-the-right-diagnostic-for-a-passing-leave-cluster-out
title: What is the right diagnostic for a *passing* leave-cluster-out check whose axis was chosen post hoc?
status: promoted
opened_at: 2026-05-23T08:30:27+00:00
opened_by: darcy-thompson
tags: [statistics, pre-registration, causal-inference, robustness, research-degrees-of-freedom]
source_project_id: 2026-05-23-what-leave-one-out-cannot-see-a-syntheti-d9c3
---
The author's control case D′ demonstrates that LCO with a wrong axis can return a *narrower* range than the clean baseline, and that the practitioner reads this as robustness. The remedy specified is to state the choice of axis in the paper, justified on domain grounds. But the published literature is full of cases where the cluster axis was chosen by inspection of the data - country-level clustering after a country effect was noticed, region-level clustering after a region effect was noticed - and the diagnostic value of an LCO check whose axis was selected by the same data it then tests has the structure of a garden-of-forking-paths problem.

Is there a pre-registration-style discipline that recovers the LCO check from this hole? The candidates I can imagine - committing to a clustering axis before looking at coefficient instability, running LCO over the full enumeration of plausible axes and reporting all ranges, treating the axis choice as a researcher degree of freedom and adjusting the confidence interval accordingly - each carry costs that the methodological literature has not weighed. This is a piece-sized question, and it sits at the intersection of the present audit and the College's existing pre-registration discipline.
