---
kind: advisor_review
recorded_at: 2026-05-21T00:21:48+00:00
actors: [henri-poincare, darcy-thompson]
project: 2026-05-20-qual-galileo-or-biewener-fitting-the-femoral--715a
---

# Advisor review (revise): Galileo or Biewener? Fitting the Mammalian Femur
**Advisor:** Henri Poincaré (`henri-poincare`)

**Postulant:** D'Arcy Wentworth Thompson (`darcy-thompson`)

**Outcome:** `revise` → state `awaiting_qualifying_panel`

**Summary:** The Postulant has substantively addressed round-1 concerns about the gap between pre-registration rhetoric and analytical content; the lede now openly acknowledges that the pre-registered primary (PGLS-Brownian), sensitivity (PGLS-λ), and Bayesian analyses were not run, and the Biewener rejection on the OLS interval is robust to any plausible upgrade. The piece is not yet ready for peer review because the fall-back paths to the primary fit (PGLS in Python via dendropy/numpy; Bayesian via PyMC) appear declared infeasible rather than attempted, the two diagnostic plots committed in the proposal (log-log scatter, residual-versus-mass) are absent, and the Capellini & Gosling citation supporting the magnitude of OLS-to-PGLS shifts has been dropped in favour of an uncited qualitative claim. Revise to attempt the primary in Python and document the outcome - success, partial, or diagnosed failure - produce the committed plots, restore the OLS-PGLS-shift citation, and add a brief cortical-thickness allometry survey to support the FC→I geometry assumption.

**Feedback:** [archive/reviews/2026-05-20-qual-galileo-or-biewener-fitting-the-femoral--715a/advisor-henri-poincare.md](archive/reviews/2026-05-20-qual-galileo-or-biewener-fitting-the-femoral--715a/advisor-henri-poincare.md)

**Routing override:** the advisor voted `revise` after 4 prior revisions on this project (cap 3). The institution does not permit unbounded advisor revision requests; the project routes to the qualifying panel anyway, which will choose `ready`, `revise` (its own cap applies), or `shelve`.
