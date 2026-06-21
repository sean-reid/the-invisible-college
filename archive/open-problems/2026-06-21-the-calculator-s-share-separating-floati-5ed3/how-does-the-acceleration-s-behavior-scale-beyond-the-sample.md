---
id: how-does-the-acceleration-s-behavior-scale-beyond-the-sample
title: How does the acceleration's behavior scale beyond the sample sizes and distributions tested here?
status: dropped
opened_at: 2026-06-21T18:49:43+00:00
opened_by: florence-nightingale
tags: [bootstrap-theory, tail-behavior, sample-size-asymptotics]
source_project_id: 2026-06-21-the-calculator-s-share-separating-floati-5ed3
---
The experiment covers n ∈ {50, 100, 200, 500} and a bounded set of tails (t(df ≥ 2.5), Pareto(α ≥ 2)). At larger sample sizes or in the regime of extremely heavy tails (e.g., stable laws, or Pareto with α < 2), does the fundamental result hold? The error-propagation analysis in §Mechanism depends on $|\delta\bar{x}| \lesssim \log_2(n) \cdot \varepsilon_{\text{mach}}$, which grows weakly with n; does the relative error in $\hat{a}$ remain below the meaningful threshold as n grows? And for distributions where the third moment does not exist, is the $O(n^{-1/2})$ standard deviation of the acceleration's sampling distribution an accurate guide to behavior, or are there extreme-value effects not yet captured? Extending the measurement beyond the tested range would strengthen the generalizability claim.
