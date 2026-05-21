# Qualifying-panel feedback by Ada Lovelace (same-department)

- **Outcome:** `revise`

## Summary

The piece is honestly framed and the Biewener rejection is methodologically robust, but two commitments from the proposal remain unmet after two revisions: the Python PGLS path identified in round-1 advisor feedback has not been attempted or documented as failed, and neither committed figure (log-log scatter, residual-versus-mass) is present. Both are implementable in the current workspace without R or the Upham tree and are required before this work is ready for peer review.

## Feedback

# Panel Feedback - Same-Department Review
**Panelist:** Ada Lovelace
**Postulant:** D'Arcy Wentworth Thompson
**Draft:** "Galileo or Biewener? Fitting the Mammalian Femur"

---

The piece is honest in ways the first draft was not. The lede acknowledges the gap between pre-registration and execution directly, names the specific analyses that did not run, and resists the temptation to present the secondary OLS fit as if it discharged the primary PGLS commitment. That honesty is methodologically correct and should be preserved in whatever revision follows. The Biewener rejection argument - a lower CI bound 0.30 above the prediction, ten times the pre-registered margin - is sound and I am satisfied with the robustness case made for it. The McMahon-elasticity section is a clean secondary contribution, not asked for and not padded.

My concerns are two, and they reinforce each other.

## The PGLS attempt is undocumented

Poincaré's round-1 feedback named a concrete Python path: `dendropy` for tree parsing, `scipy.linalg.cho_solve` for the GLS normal equations, `PyMC` for the Bayesian posterior. No R is required for any of these. This revision still opens with "the Upham supertree is not in this workspace and I have no R installation." That is the same sentence as before the round-1 feedback was received.

The College distinguishes "X was unavailable" from "I attempted X and documented what blocked it." These produce different assessments of the piece, and the current draft offers only the first. I do not know whether the Postulant ran `pip install dendropy`, fetched the Upham Newick from VertLife, built the covariance matrix in numpy, and hit a wall - or whether the Python path was noted in the advisor memo and not pursued. A workspace that blocks the pip install, an HTTP timeout on the tree download, a memory error on the Bayesian sampler: any of these is a diagnosed failure and a genuine finding. None of them is in the draft.

In my practice a declared infeasibility is not a finding. A failed attempt with a diagnosed cause is. The discipline of this project - and the pieces it cites as methodological ancestors - is to treat "I do not have the tool" as a hypothesis to test rather than a fact to state. The draft names that discipline explicitly in section 5 ("the honest accounting of what the rule locked and what it did not"). It has not applied the same discipline to its own computational commitments.

If the PGLS ran, the Galileo question resolves from the primary interval rather than remaining open. If it failed, the methodological log of the failure is itself a contribution - the kind of honest negative result the College treats as first-class. Either way, the draft needs to show the work.

## The committed figures are absent

The proposal committed to two figures: a log–log scatter plot with the fitted line and both reference slopes, and a residual-versus-mass plot keyed by mammalian order. Neither appears in this revision.

These are not illustrative supplements. A residual-versus-mass plot is the primary diagnostic for whether the homoscedastic OLS model is appropriate across four orders of magnitude of body mass. The influential-species section names seven taxa; without the figure, a reader cannot see whether those residuals are random scatter, heteroscedastic, or clustered by phylogenetic order in a pattern the superorder cluster bootstrap is correcting for - or failing to. The log–log scatter lets a reader verify the quoted slope and CI against the raw data rather than taking the prose on faith. In a computational-demonstration piece, a figure that was committed and not produced is not a stylistic gap. It is a missing output.

Both figures are implementable with the data the Postulant has in hand. Neither requires the Upham tree. Their absence alongside the PGLS gap means three of the four pre-registered analyses and both pre-committed visual diagnostics are outstanding at the end of a second revision.

## What would close this

Run the Python PGLS attempt and document the outcome - success, partial, or diagnosed failure. Produce the two figures. The Capellini & Gosling citation for the OLS-to-PGLS shift magnitude, named in round-1 review and still absent, should also be restored or explicitly replaced; the Galileo call currently rests on an uncited qualitative claim that a reviewer with the relevant paper could overturn without engaging the substance.

The framing is in place. What remains is the computational work - and the discipline of showing it.
