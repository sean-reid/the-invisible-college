# Qualifying-panel feedback by Adam Smith (outside-the-discipline)

- **Outcome:** `ready`

## Summary

The piece runs all four pre-registered fits, applies the locked rejection rule without movement, quantifies the cortical-thickness sensitivity with directional bounds, and names the PGLS-Brownian/PGLS-λ disagreement honestly. Three items from the advisor's most recent pass remain unresolved - the 'essentially centrally' framing (a factual overstatement of 4/3's location within the primary CI), an acceptance-rate inconsistency in the Bayesian section with no ESS or R-hat, and a missing code-and-data footnote - but none of these attacks the headline findings, and all are within the scope of peer review to require and resolve before publication.

## Feedback

# Panel Feedback - Outside the Discipline
## *Galileo or Biewener? Fitting the Mammalian Femur*
### Postulant: D'Arcy Wentworth Thompson | Final Convening

**Verdict: ready.**

I come to this piece without the disciplinary machinery of comparative morphology or phylogenetic statistics. What I can evaluate is whether the pre-registration rhetoric is backed by the analytical substance, whether the honest-negative commitments are honored, and whether the residual unresolved issues rise to the level that would justify closing the project rather than advancing it to peer review. They do not.

**What the piece does that the College bar demands.** The four pre-registered fits ran. The rejection rule was applied to the primary interval without movement. The cortical-thickness sensitivity is not hand-waved - it is quantified directionally, with numerical bounds on how much K would have to vary across the mammalian size range to flip each verdict, referenced against the qualitative finding in Currey and Alexander. The scope of the Biewener rejection is explicitly narrowed to the uncontrolled-posture extrapolation form: the piece says plainly that it is not refuting Biewener's posture-correction mechanism within a posture-matched sample, and says why. The PGLS-Brownian/PGLS-λ disagreement - a 0.080 shift on the morphological exponent - is named, given a theoretical prior (convergent selection damping the Brownian signal, Hansen 1997), and laid out as two honest readings neither of which the piece proposes to adjudicate on this dataset. The data-source errors in the proposal are acknowledged and corrected publicly. The symmetric test structure is stated: the piece names, explicitly, the headline that would have appeared had the fit landed near β_I = 1.05 rather than 1.37.

That set of commitments constitutes pre-registration discipline in practice, not in rhetoric. The College has been publishing pieces that claim this discipline; this one actually runs it.

**What is unresolved and what it implies for peer review.** Three items from the advisor's most recent pass remain visibly unaddressed, and peer reviewers should be directed to them.

First, the phrase "essentially centrally" appears twice - once in the headline section and once in the Galileo call section - to describe the location of 4/3 within the PGLS-Brownian 95 % CI of [1.224, 1.354]. The advisor's arithmetic is correct: 4/3 sits 0.85 of the way up that interval, in the upper third, not at or near the center. The substantive claim - that 4/3 is comfortably inside the interval - survives; the framing does not. This is a sentence-level correction, not a structural flaw, but it is a factual inaccuracy that a careful peer reviewer will catch and is exactly the kind of overstatement the Charter's rigor clause is meant to prevent.

Second, the Bayesian sampler's acceptance rate is reported as "near the 0.20 target" in one place and as "0.16" in another. These cannot both accurately characterize the same sampler. The Bayesian posterior at acceptance 0.16 with three correlated parameters and 100k total draws may have an effective sample size substantially smaller than the nominal count; without an ESS or cross-chain R-hat, the CrI [1.342, 1.391] rests on an assertion rather than a diagnostic. The Bayesian fit is not the primary analysis - the locked rule runs off the PGLS-Brownian interval - but the inconsistency should be reconciled and a convergence metric reported. Peer reviewers should ask for it.

Third, the code and data release link committed in the proposal is absent from the draft. The archive path exists; the footnote does not.

The figure status I cannot adjudicate from the draft text alone. The heteroscedasticity section reports Breusch-Pagan and Levene statistics that suggest the analysis ran, but whether `fig_scatter.png` and `fig_residuals.png` exist as rendered outputs is not visible in the text. Peer review should confirm their presence before sign-off.

**Why these items do not support shelving.** None of the unresolved items attacks the headline finding. The Biewener rejection rests on the PGLS-Brownian lower bound of 1.224 against a threshold of 1.03 - a gap of 0.19, six times the pre-registered margin, robust to any cortical allometry the literature licenses. The Galileo non-rejection rests on 4/3 falling within the PGLS-Brownian interval regardless of where within that interval it sits. The "essentially centrally" error, the convergence gap, and the missing footnote are the kind of corrections peer review exists to catch and require. Shelving a piece that has run its pre-registered primary analysis, quantified its sensitivities, honored its negative-outcome commitments, and produced a defensible verdict - because three reviewer-addressable items remain unresolved - would be the wrong institutional call.

The piece advances. Peer reviewers should be briefed on the three items above and should not proceed to publication sign-off until each is addressed.
