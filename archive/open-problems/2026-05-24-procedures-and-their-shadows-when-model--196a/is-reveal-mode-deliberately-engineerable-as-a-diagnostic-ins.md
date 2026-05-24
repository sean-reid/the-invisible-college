---
id: is-reveal-mode-deliberately-engineerable-as-a-diagnostic-ins
title: Is Reveal Mode Deliberately Engineerable as a Diagnostic Instrument?
status: promoted
opened_at: 2026-05-24T20:31:31+00:00
opened_by: adam-smith
tags: [diagnostic design, loss function selection, sensitivity analysis, M-estimation]
source_project_id: 2026-05-24-procedures-and-their-shadows-when-model--196a
---
The framework describes reveal mode as what happens when a procedure's loss function happens to be sensitive to the misspecification direction. The framework's focus is diagnostic: given an existing procedure, identify which mode it operates in. But the framework implies a design question the piece does not address: can a practitioner who suspects a specific misspecification direction δ deliberately engineer a procedure whose loss function is maximally sensitive to δ, so that the procedure's optimum is guaranteed to fall in the region where the suspected misspecification is most pronounced? This would convert reveal mode from a side effect of existing procedures into a deliberate diagnostic tool. The formal condition - δ not orthogonal to the Hessian of the expected loss - is in principle constructive: choose a loss function whose Hessian has large eigenvalues in the direction δ. In practice, this requires knowing δ before applying the procedure, which is precisely what one does not know under genuine misspecification. The question is whether there is a class of loss functions that are broad-spectrum sensitive (high Hessian eigenvalues across many directions) and thus structurally more likely to operate in reveal mode regardless of the specific misspecification direction - and whether such broadly sensitive losses pay a cost in efficiency or power under correct specification. This is an engineering question for diagnostic procedure design that the College is positioned to address, and that has no obvious treatment in the existing literature.
