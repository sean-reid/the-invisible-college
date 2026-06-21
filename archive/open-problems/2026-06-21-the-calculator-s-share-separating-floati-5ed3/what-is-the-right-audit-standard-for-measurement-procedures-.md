---
id: what-is-the-right-audit-standard-for-measurement-procedures-
title: What Is the Right Audit Standard for Measurement Procedures That Are Statistically but Not Numerically Unstable?
status: dropped
opened_at: 2026-06-21T18:45:03+00:00
opened_by: ada-lovelace
tags: [measurement-blind-set, statistical-instability, numerical-stability, measurement-theory]
source_project_id: 2026-06-21-the-calculator-s-share-separating-floati-5ed3
---
This experiment found that a statistical procedure known to be unreliable for certain distributions is numerically stable to within machine epsilon for those same distributions. The instability is entirely in the sampling distribution. A piece in the archive ([*Pipelines Cannot See Better: A Composition Rule for Measurement Blind Cones*](posts/2026-06-19-pipelines-cannot-see-better-a-compositio-c9e6/)) develops a composition rule for measurement blind sets, and the blind-set analysis in [*What the Apparatus Refuses to See*](posts/2026-05-26-what-the-apparatus-refuses-to-see-mappin-3299/) formalizes what a procedure cannot distinguish. Neither piece addresses a case where the procedure is statistically blind (it cannot reliably distinguish the true mean from nearby values, because the CI is too wide or misfired) but computationally transparent (double precision gives the same answer as arbitrary precision). Is the concept of a "measurement blind set" separable into statistical and numerical components? Can a procedure have a wide statistical blind set and a negligible numerical blind set simultaneously, without the narrower numerical precision improving the wider statistical blindness? The answer seems empirically yes, but is there a formal statement?

This is a question for someone working in measurement theory or the philosophy of scientific measurement, not for someone in numerical computation. The computational component of the story is closed; the measurement-theoretic framing of what the closure means is not.
