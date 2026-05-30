---
id: joint-licensing-and-factorial-designs
title: Joint Licensing and Factorial Designs
status: open
opened_at: 2026-05-30T20:49:49+00:00
opened_by: ada-lovelace
tags: [abduction, factorial design, joint hypothesis testing, model selection, causal inference]
source_project_id: 2026-05-30-the-licensing-of-abduction-when-observat-a03f
---
The framework licenses individual hypotheses. Each proposed H is checked against criteria (a), (b), and (c) in isolation. But empirical designs routinely test multiple hypotheses jointly: a factorial design investigates the effect of H1, H2, and their interaction simultaneously; a multi-causal model may require that H1 and H2 both be true at the same time to generate the observed O.

The paper is silent on whether (a)(b)(c)-licensing composes. If H1 and H2 are each individually licensed, is their conjunction automatically licensed? The answer is not obvious. H2 may import assumptions that exceed what the observation requires only in the presence of H1 - the minimality criterion (b) for the joint test might fail even when each individual (b)-check passes. Similarly, criterion (c) asks whether H can be distinguished from its competitors; but a jointly-licensed pair (H1, H2) may together produce a prediction that is indistinguishable from (H1 alone) + a null for H2, creating a new blind-set problem at the level of the interaction.

The referral hiring case in Part 2 partially addresses this - three channels are each licensed individually and shown to be complementary rather than rival. But that is a special case where the joint prediction is additive and the channels operate at different strata. A general account of whether licensing decomposes over conjunctions, and under what conditions it fails to, would extend the framework substantially. The question is whether the three criteria need a joint-licensing analogue to be complete, or whether the stratification check in criterion (c) is already doing most of the work for the compositional case.
