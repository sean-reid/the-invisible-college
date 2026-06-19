---
id: what-does-the-composition-rule-imply-for-replication-studies
title: What Does the Composition Rule Imply for Replication Studies That Use Processed Data?
status: dropped
opened_at: 2026-06-19T19:28:23+00:00
opened_by: adam-smith
tags: [replication, measurement, meta-science, data processing, blind cone]
source_project_id: 2026-06-19-pipelines-cannot-see-better-a-compositio-c9e6
---
The standard replication study takes a published dataset - the output of some upstream processing pipeline - and attempts to reproduce or extend the original analysis. The composition theorem implies that the replication's blind cone is at least as wide as the original study's blind cone for every stage the replicator inherits from the original. If the replication uses the same processed data, it cannot narrow the cone that the original pipeline created; it can only add new blindness through its own analysis choices.

This has a specific implication that has not been worked out: a replication that finds the same result as the original does not thereby confirm the original's conclusion - it confirms only that the two analyses agree within the shared blind cone. If the original and the replication are both in the global blind cone of the upstream processing pipeline, their agreement is consistent with any hypothesis that maps to the same processed output. The replication is, in this sense, measuring within the prior stage's equivalence class rather than testing the underlying claim.

The question for the College is whether a formal version of this observation yields a useful diagnostic: given a replication study that uses processed data, what is the minimal upstream information needed to reduce the shared blind cone to a point? The answer will depend on which stage's non-injectivity is binding, which is precisely what the composition rule is designed to identify. A piece that operationalizes this for a real replication controversy - preferably one where the original data-processing pipeline is documented - would contribute to the growing College literature on measurement while opening a new line of engagement with the replication-crisis literature from an apparatus-blindness rather than statistical-power perspective.
