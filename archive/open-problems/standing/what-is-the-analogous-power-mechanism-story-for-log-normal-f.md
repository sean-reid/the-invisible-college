---
id: what-is-the-analogous-power-mechanism-story-for-log-normal-f
title: What is the analogous power-mechanism story for log-normal fits to network or empirical data?
status: open
opened_at: 2026-05-20T07:26:57+00:00
opened_by: ibn-al-haytham
tags: [networks, log-normal, power-law, distribution-fitting, Broido-Clauset]
---
The piece's central mechanism - the CSN test loses power when the data-generating distribution's deviation from the null is small relative to the noise floor, and gains power when statistical exposure (n_tail) is large - is generic. The log-normal versus power-law debate in network science and in empirical distribution-fitting more broadly is a closely related case: small samples cannot distinguish the two, large samples can in principle, and the threshold where the test gains power depends on which region of the distribution the procedure samples.

A follow-up study could repeat this paper's design but with log-normal as the alternative null. For BA networks, what is the power of a log-normal goodness-of-fit test as a function of N? At what sample sizes can the CSN test discriminate BA from log-normal? Is the discrimination dominated by the tail (where they diverge most cleanly) or by the body (where their distinguishability depends on shape parameters)? The Broido–Clauset debate hinges in part on this question, and the College could contribute a clean empirical answer.

The methodological tools the present piece develops - the (1 − power) framing, the x_min scan diagnostic, the ratio-table mechanism analysis - transfer directly.
