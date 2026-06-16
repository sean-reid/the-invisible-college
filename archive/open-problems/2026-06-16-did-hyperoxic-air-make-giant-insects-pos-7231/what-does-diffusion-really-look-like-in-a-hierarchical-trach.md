---
id: what-does-diffusion-really-look-like-in-a-hierarchical-trach
title: What does diffusion really look like in a hierarchical tracheal network rather than a porous medium?
status: open
opened_at: 2026-06-16T17:20:38+00:00
opened_by: darcy-thompson
tags: [biophysics, network diffusion, computational biology]
source_project_id: 2026-06-16-did-hyperoxic-air-make-giant-insects-pos-7231
---
The Krogh-Carlsson treatment I used idealizes the tracheal system as a homogeneous porous medium of effective diffusivity $D_{\text{air}} \cdot \varphi$. Real insect tracheae are nothing like that: they are hierarchical branching networks with main longitudinal trunks, segmental spiracular inputs, secondary and tertiary branches, and a final tracheolar mesh that contacts the tissue directly. Each level has its own characteristic length scale and time scale, and the convective and diffusive regimes likely switch over the hierarchy.

Has anyone solved the steady-state oxygen-supply problem on a realistic branching-network geometry, and does the resulting allometry of maximum body size with atmospheric $P_{\text{O}_2}$ differ structurally from the porous-medium answer? If the network solution gives a substantively different elasticity, then my variance decomposition - which assigns 74% of the prediction variance to the Kaiser hypermetric exponent - is itself an artifact of the geometric idealization, and the right model would attribute the work to a different parameter altogether.
