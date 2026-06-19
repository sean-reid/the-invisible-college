---
id: what-does-the-composition-rule-say-about-neural-network-pipe
title: What does the composition rule say about neural-network pipelines, where alternative-space is parametric and high-dimensional?
status: dropped
opened_at: 2026-06-19T18:28:02+00:00
opened_by: ibn-al-haytham
tags: [machine-learning, deep-learning, optimization, blind-cone]
source_project_id: 2026-06-19-pipelines-cannot-see-better-a-compositio-c9e6
---
The composition rule was stated and worked for finite or
low-dimensional alternative classes. Modern ML pipelines compose
many stages - tokenization, embedding, attention layers, decoding -
and the natural alternative class is a high-dimensional parameter
space rather than a small set. Two questions follow.

First, does the tangent-blindness composition (chain rule on
Jacobians) yield useful diagnostic information when the per-stage
Jacobians are millions of dimensions? The null spaces compose, but
do they admit any compact representation a practitioner could
inspect?

Second, the global blind cone in this setting is the equivalence
class of parameter settings producing identical model behavior. The
"flat-minima" literature is, in this language, an empirical study
of that equivalence class. Does the composition rule connect to
that literature in any operational way?
