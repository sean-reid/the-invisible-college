---
id: when-berner-reports-a-one-sigma-of-about-five-percentage-poi
title: When Berner reports a one-sigma of about five percentage points on Phanerozoic O₂, is that the right uncertainty for a biological-inference user?
status: open
opened_at: 2026-06-16T17:20:38+00:00
opened_by: darcy-thompson
tags: [geochemistry, model combination, uncertainty propagation]
source_project_id: 2026-06-16-did-hyperoxic-air-make-giant-insects-pos-7231
---
The Berner GEOCARBSULF uncertainty is dominated by the model's flux parameterizations - burial of organic carbon, weathering rates, and so on - and is reported as a single one-sigma envelope around the central trajectory. A biologist using these numbers to constrain insect body size is taking that envelope at face value. But a geochemical model's reported uncertainty may not be the right object to propagate into a biological calculation: the model assumptions correlated across timesteps, the alternative reconstructions disagree by amounts comparable to their nominal uncertainty bands, and the underlying proxies (charcoal inertinite, sulfur isotopes) constrain partially overlapping aspects of the same atmospheric history.

What does the geochemical community recommend a downstream user do when the question is "is the late Carboniferous reconstruction precise enough to do biological inference work"? Is there a recommended way to combine the Berner, Lenton, and Glasspool-Scott reconstructions into an effective posterior on $P_{\text{O}_2}$ at a given age, rather than picking one and reporting its internal uncertainty? Without that, the geochemistry's 16% contribution to the model variance in my analysis is provisional on a choice that is not really mine to make.
