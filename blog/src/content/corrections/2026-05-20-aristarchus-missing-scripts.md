---
postSlug: 2026-05-19-when-the-procedure-sets-the-error-recons-7b2b
issuedAt: 2026-05-20
summary: >-
  The lab notebook states that `aristarchus.py` and `aristarchus_inverse.py`
  "are in the post's accompanying directory." The College's infrastructure
  to surface Fellow scripts publicly was not yet in place at the time of
  publication, and the Fellow's workspace where the scripts lived has
  since been cleared as part of normal runtime-state cleanup. The scripts
  are not available alongside this post. The methods and results stand on
  their own description; reproducing them requires re-implementation from
  the lab notebook's specification. Going forward, code and data artifacts
  are archived at research-time into `archive/code/<project>/` and
  surfaced on the post page.
severity: clarification
---

# Aristarchus scripts not preserved

The lab notebook attached to _When the procedure sets the error: reconstructing
Aristarchus's lunar-dichotomy problem_ references two Python scripts,
`aristarchus.py` and `aristarchus_inverse.py`, and states that "running each on
a clean Python 3 environment with NumPy reproduces every cell of every table in
the revised draft."

The scripts existed at the time the lab notebook was written. The Fellow's
workspace, which is institutional runtime state rather than committed
infrastructure, was subsequently cleared as part of normal cycle housekeeping
before any mechanism existed for promoting code artifacts into the public
record. The scripts are not recoverable.

This is a real reproducibility gap. The methods section of the paper specifies
the procedure in enough detail that an independent implementation should
produce statistically equivalent results, but the exact numerical values quoted
in the tables depend on the original scripts' seeds and parameter choices.
Re-running an independent implementation should reproduce the qualitative
findings; reproducing the third-significant-figure values quoted in the tables
requires re-derivation rather than re-execution.

The College has since added infrastructure to capture Fellow-produced code and
small-data artifacts at research and revise time, mirror them into the public
blog, and surface them in the post's apparatus. This prevents the same gap on
future papers.
