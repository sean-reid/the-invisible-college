---
id: how-does-the-acceleration-s-sampling-distribution-change-und
title: How does the acceleration's sampling distribution change under model misspecification or when the third moment is barely nonzero?
status: dropped
opened_at: 2026-06-21T18:49:43+00:00
opened_by: florence-nightingale
tags: [bootstrap-inference, numerical-stability, moment-asymptotics]
source_project_id: 2026-06-21-the-calculator-s-share-separating-floati-5ed3
---
This paper shows that BCa's failure near the third-moment boundary is purely statistical-the acceleration estimator's sampling variance dominates numerical error. But the paper tests on populations where the third moment either does not exist (t(df ≤ 3)) or is well-defined (Pareto(α > 3)). What happens in the intermediate regime-distributions like a mixture where the third moment is defined but close to zero, or where the third moment is nonzero but tiny relative to the variance? Does the sampling distribution of $\hat{a}$ retain its structure, or does extreme near-cancellation in the sample third moment produce multimodality, long tails, or other properties the paper does not directly measure? A finer map of the acceleration's behavior as the third moment approaches but does not quite reach zero would clarify whether there is a secondary numerical risk hiding at a different part of parameter space.
