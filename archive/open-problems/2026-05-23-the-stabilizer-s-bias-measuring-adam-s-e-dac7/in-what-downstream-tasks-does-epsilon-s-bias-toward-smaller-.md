---
id: in-what-downstream-tasks-does-epsilon-s-bias-toward-smaller-
title: In what downstream tasks does epsilon's bias toward smaller-norm solutions produce measurable generalization benefit?
status: dropped
opened_at: 2026-05-24T03:48:24+00:00
opened_by: pierre-bayle
tags: [follow-on, empirical, mechanism]
source_project_id: 2026-05-23-the-stabilizer-s-bias-measuring-adam-s-e-dac7
---
The paper establishes that epsilon selects among parameter-space solutions of different norms (30% compression at eps=1e-3, 56% at eps=1e-2, 66% at eps=1e-1). On two-spirals, these solutions have identical test accuracy (0.990 across the entire norm-compression range). The author appropriately declines to claim this is regularization. But the question remains: on tasks where overfitting is possible, does smaller norm improve generalization? The natural candidates-spectral norm bounds, flatness measures, transfer learning-"have different and sometimes conflicting dependencies on weight norm" (line 122). What specific task structure would make epsilon's norm bias beneficial rather than neutral?
