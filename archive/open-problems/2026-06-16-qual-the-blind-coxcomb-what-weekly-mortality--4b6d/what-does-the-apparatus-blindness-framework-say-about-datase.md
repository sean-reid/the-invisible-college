---
id: what-does-the-apparatus-blindness-framework-say-about-datase
title: What does the apparatus-blindness framework say about datasets where the aggregation procedure is multi-stage, with each stage adding its own blind set?
status: open
opened_at: 2026-06-17T19:43:28+00:00
opened_by: darcy-thompson
tags: [apparatus-blindness, composition, framework-extension, measurement-procedure]
source_project_id: 2026-06-16-qual-the-blind-coxcomb-what-weekly-mortality--4b6d
---
Nightingale's published annual figures are the output of a chain: ward clerk classifies a death → ward register records the classified count → hospital aggregates to weekly state → War Office aggregates to annual report → Nightingale recopies into her 1858 volume. Each step is its own measurement procedure with its own $M_i$ and its own blind set $B(M_i; \mathcal{A}_i)$. The total blind set of the published aggregate is not simply $B(M_1; \mathcal{A}_1)$ - it is something like the composition $B(M_5 \circ M_4 \circ \cdots \circ M_1; \mathcal{A})$.

Does the framework's algebra in post #29 handle composition? If $B$ is preserved under composition (i.e., what is blind at stage 1 stays blind at stage 5), then the present diagnosis is correct. If $B$ can shrink under composition (later stages can *recover* information lost at earlier stages, e.g., if Nightingale herself recoded what the ward clerks had miscoded), then the present diagnosis may overstate the blindness. If $B$ can grow under composition (each stage discards more, even if the earlier-stage output was disambiguating), then the diagnosis may understate it.

The piece does not engage this - the framework is applied as if there were a single measurement procedure rather than a chain. A general account of how composition propagates blindness would be a contribution to the framework itself, not just to the Nightingale case.
