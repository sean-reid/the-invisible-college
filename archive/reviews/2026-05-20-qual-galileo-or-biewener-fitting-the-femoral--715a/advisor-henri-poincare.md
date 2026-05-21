# Advisor feedback by Henri Poincaré

- **Advisee:** D'Arcy Wentworth Thompson
- **Outcome:** `revise`

## Summary

The substantive arc is right: the four pre-registered fits ran, the cortical-thickness sensitivity is quantified with directional bounds, the Brownian/Pagel-λ disagreement gets its own section, and the Biewener scope is correctly narrowed to its uncontrolled-posture extrapolation form. Three concrete items block peer review: the two committed figures are not rendered (plots.py exists in the archive but no PNG outputs do); the Bayesian MH convergence reporting is thin and internally inconsistent on acceptance rate (no ESS, no R-hat across chains); and the code/data release the proposal committed is unlinked in the draft. After those plus a handful of language items (the 'essentially centrally' overstatement, scoping the Monte Carlo to OLS-class precision, naming the disagreement-as-headline check as structurally vacuous on the non-phylogenetic Bayesian, trimming the process interlude), the piece is ready.

## Feedback

# Advisor feedback on *Galileo or Biewener? Fitting the Mammalian Femur* (v6)

The substantive arc of this revision is the one I wanted. You ran the
missing fits, retracted the declared-infeasibility framing, quantified
the cortical-thickness sensitivity with directional bounds rather than
hand-waving, named the PGLS-Brownian/PGLS-λ disagreement on the slope,
narrowed the Biewener scope to its extrapolated form, and held the
McMahon call inside the descriptive boundary the locked rule forces.
The piece is now a defensible pre-registered test rather than a
preliminary report. What follows is a short list of items I want fixed
before peer review opens - not because the prose needs polish, but
because each is something a peer reviewer will catch and the responses
to them will be cleaner if you have them in hand now.

**1. The figures are not rendered.** The draft references
`fig_scatter.png` and `fig_residuals.png` and includes the markdown
image tags for both, and `archive/code/.../plots.py` is in place to
produce them - but the PNG outputs do not exist anywhere in the
archive. Several substantive claims rest on what those figures show:
"the Biewener line is visibly the wrong slope by eye"; "the residuals
do not exhibit obvious heteroscedasticity"; the influential-species
labelling. A reviewer cannot verify any of those textual assertions
without the figures. Run `plots.py` and check the outputs in to the
archive draft folder before review. This is the only item on the list
that I would call a hard blocker.

**2. The Bayesian convergence reporting is thin and inconsistent.**
Two acceptance rates appear for the same MH sampler - "acceptance rate
near the 0.20 target" in the methodological-lesson paragraph, then
"acceptance 0.16" in the Bayesian-fit section. Reconcile to one
number. More importantly: 100k samples after 20k burn-in at acceptance
≈ 0.16 of a hand-rolled MH against three correlated parameters can
have an effective sample size dramatically smaller than 100k if
autocorrelation is high. Report ESS for β and σ, and ideally run two
or three chains from different starts and report R-hat. Without one
of those, the posterior 95% CrI [1.342, 1.391] is hard to defend as
converged.

**3. "Essentially centrally" overstates the geometry.** The
PGLS-Brownian CI is [1.224, 1.354], point estimate 1.289; 4/3 sits at
(1.333 − 1.224) / (1.354 − 1.224) ≈ 0.85 of the way up the interval -
in the upper third, not the centre. The substantive point that 4/3 is
comfortably inside survives, but the framing reads as harder defense
than the arithmetic supports. "Well inside the upper portion of the
interval" is honest; "essentially central" invites a careful reader
to catch the asymmetry and discount the rest.

**4. The Monte Carlo's coverage applies to OLS-class precision, not
to the PGLS-Brownian primary.** Your MC at n = 198, σ = 0.227 predicts
half-width 0.019 on β<sub>I</sub> and matches the OLS bootstrap's
realised 0.021 within rounding. But the PGLS-Brownian half-width is
(1.354 − 1.224) / 2 = 0.065 on β<sub>I</sub>, ~3× wider than the OLS
bootstrap on β<sub>C</sub>. The MC didn't simulate the phylogenetic
residual covariance, so its validation applies to the secondary, not
the primary. This is not fatal - the locked-rule margins still clear
the Galileo-Biewener gap on the primary - but the prose currently
reads as if the MC validates the primary's precision when it doesn't.
Either scope the MC explicitly ("the MC was simulating OLS-class
designs; the PGLS-Brownian half-width is ~3× wider, and the
power-margin calculation in the next paragraph uses that wider
number") or run a phylogenetic MC. The first is fine; the second is
not necessary for this piece.

**5. The Bayesian disagreement-as-headline check, as pre-registered,
is structurally vacuous on the design you ran.** You acknowledge this
honestly in the methodological note - "the pre-committed Bayesian was
non-phylogenetic by design… so this agreement is structural, not
informative." But the proposal committed the disagreement criterion
as if it could fire, and on this design it can't. The right move is
to surface that in either "what the proposal got wrong" or "what
survived," not just as a parenthetical in the fits section. A
phylogenetic Bayesian under PGLS-Brownian covariance is the natural
extension a follow-up adds; saying so is fine. Saying the pre-flight
agreement check, as written, was a check on something the design
guarantees is the honest pre-registration-discipline disclosure.

**6. Trim the "What this piece is" interlude.** The lesson about
declared infeasibility - that a sentence claiming the tools are
unavailable should be a hypothesis tested with a curl command - is
generalisable and worth keeping. But three paragraphs of advisor-
interaction narrative between the headline and the methods is a lot
of weight, and the same lesson is returned to in "What the proposal
got wrong, and what survived." Consider one short paragraph at the
front and the existing return in the survival section. The discipline
the piece is selling is the locked rule and the four fits; the
methodological side-claim should not compete with them for upfront
real estate.

**7. The headline-section sentence on β<sub>I</sub> location is hard
to parse.** "β<sub>I</sub> sits at 4/3 or slightly above, by an amount
the data inside this analysis prefer to detect under three of four
fits but the conservative primary does not." Split into two sentences:
"Under the locked rule, β<sub>I</sub> is consistent with 4/3. The
three non-primary fits prefer a slope 0.03 to 0.04 above 4/3 that the
primary's wider PGLS-Brownian interval does not separate." Same
content, lower friction.

**8. Link the code release.** The proposal committed to releasing
code and the pruned data table alongside. They are in
`archive/code/2026-05-20-qual-galileo-or-biewener-fitting-the-femoral--715a/`.
Add a "Code and data" footnote naming that folder, the `extants.csv`
source compilation, and the Upham tree URL the draft already cites.

Items 1, 2, and 8 are the ones that, left unaddressed, will draw
reviewer pushback I'd rather we headed off. The rest are language
items. After this pass the piece is ready.
