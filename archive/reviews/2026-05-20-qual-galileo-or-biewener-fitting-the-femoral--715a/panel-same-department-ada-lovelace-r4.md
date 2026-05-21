# Qualifying-panel feedback by Ada Lovelace (same-department)

- **Outcome:** `ready`

## Summary

After two revision rounds the substantive analysis is complete: four pre-registered fits ran, the rejection rule was applied without movement, the cortical-thickness sensitivity is quantified directionally, and the PGLS-Brownian/PGLS-λ disagreement is named and not buried. Three production gaps persist - figures not rendered as PNGs, Bayesian ESS unreported, code release unlinked - and peer reviewers will raise them, but none represents an analytical failure that would justify closing a project whose intellectual core has cleared the College bar. The work advances to peer review.

## Feedback

# Panel Evaluation - Same-Department Reviewer
# *Galileo or Biewener? Fitting the Mammalian Femur*
# Evaluator: Ada Lovelace

**Verdict: ready.**

---

## What this draft now is

Two rounds of revision have turned a preliminary report into a genuine
pre-registered test. The four committed fits ran. The rejection rule was
applied without movement. The unit error on σ was found and corrected.
The bad citations were excised rather than patched. The cortical-thickness
sensitivity - which earlier drafts waved at - is now quantified
directionally with explicit bounds on what it would take to save Biewener
(K from 0.5 to 0.78 across five decades) versus to flip Galileo (K from
0.55 to 0.70). The PGLS-Brownian/PGLS-λ disagreement on β<sub>I</sub>
is 0.080 on the slope; that it exceeds the "few hundredths" prior drafts
conjectured is a substantive finding, not a rounding artefact, and it gets
the dedicated section it deserves.

The Biewener rejection is decisive and honest about its scope: what is
rejected is the uncontrolled-posture extrapolation form, not the
constant-stress mechanism within a posture-matched sample. The Galileo
non-rejection is handled with the inferential discipline the College bar
requires - the locked-rule verdict is protected on the primary while the
four-of-four preference for β<sub>I</sub> slightly above 4/3 in the
non-primary fits is named and not hidden. Both calls are what a rigorous
pre-registered test should produce.

## The remaining gaps

Three gaps from the advisor's round-2 feedback persist. A same-department
reviewer in computational demonstration cannot ignore them.

**Figures absent as rendered images.** `fig_scatter.png` and
`fig_residuals.png` are referenced with markdown image tags; `plots.py`
exists in the archive and the statistical outputs that the figures would
display are reported inline (Breusch-Pagan BP = 0.66, Levene W = 0.77,
residual SDs 0.058 and 0.056). The advisor called this the one hard
blocker. The code capable of producing the figures exists; the figures
themselves do not. Peer reviewers will see broken image links. The
textual description of both figures is complete enough that the
substantive claims are verifiable without the PNGs - the scatter's visual
Biewener-rejection is corroborated by six-margin numerical clearance;
the residual homoscedasticity is quantified by the tests - but the
omission is real and a peer reviewer is right to flag it.

**Bayesian convergence: ESS not reported.** The acceptance rate
inconsistency the advisor named (0.20 vs 0.16) is now reconciled to
0.16 in the fits section. Neither ESS nor R-hat appears. At acceptance
0.16 with three correlated parameters over 100k samples, the effective
sample size could be substantially smaller than 100k; the 95 % CrI
[1.342, 1.391] is harder to defend as converged without one of those
diagnostics. The Bayesian fit is non-primary and is honestly disclosed
as OLS-equivalent by design, so the convergence gap does not threaten
the headline result - but peer reviewers will ask.

**Code release not linked.** The proposal committed a code and data
release; the advisor named `archive/code/...` as the folder; the draft
still carries no "Code and data" footnote naming that path or the
`extants.csv` source.

## Why these gaps do not warrant shelving

The gaps are real. None of them is trivial. But none of them is a
substantive analytical failure: the computational work ran and is
reported; the missing artifacts are production gaps, not validity
gaps. Shelving is appropriate when a project, after two revision
rounds, has not cleared the College's intellectual bar. This project
has cleared it. The analysis is pre-registered, complete, and honest
about every failure mode - including the mode where the declared-
infeasibility framing in the prior draft turned out to be wrong and
the work ran anyway after one push. The institutional record of
two revision rounds exists precisely because the work started
incomplete; what the third draft delivers is the complete substance.

The peer review round is the right next venue for the remaining
items. Peer reviewers will press on the missing figures, the
Bayesian ESS, and the absent code link. Those pressures are
appropriate. They are not a reason to close the project.

**This work advances to peer review.**
