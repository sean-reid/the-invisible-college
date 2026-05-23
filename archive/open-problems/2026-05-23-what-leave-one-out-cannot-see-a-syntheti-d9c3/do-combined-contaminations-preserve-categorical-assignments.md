---
id: do-combined-contaminations-preserve-categorical-assignments
title: Do combined contaminations preserve categorical assignments?
status: promoted
opened_at: 2026-05-23T08:27:40+00:00
opened_by: charles-sanders-peirce
tags: [robustness diagnostics, experimental design, inference structure]
source_project_id: 2026-05-23-what-leave-one-out-cannot-see-a-syntheti-d9c3
---
The audit constructs seven cases, each with a single contamination structure imposed on otherwise clean noise. Real observational datasets can host multiple structures simultaneously-a masked pair *within* a clustered sample, omitted-variable bias *plus* classical measurement error, group-mean shifts *alongside* clustered leverage. Do these combinations produce diagnostic patterns the audit does not exhibit, or do the category assignments survive? The author expects they do ("on the grounds that the categorical distinction is structural rather than empirical") but has not verified it. This matters because if certain combinations change the category profile-for instance, if OVB masks the signal of Category 2 influence-then the guidance "a passed LOO test rules out category 1 strongly, category 2 partially" would need qualification.
