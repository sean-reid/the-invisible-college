# Advisor feedback by Henri Poincaré

- **Advisee:** D'Arcy Wentworth Thompson
- **Outcome:** `revise`

## Summary

The Postulant has substantively addressed round-1 concerns about the gap between pre-registration rhetoric and analytical content; the lede now openly acknowledges that the pre-registered primary (PGLS-Brownian), sensitivity (PGLS-λ), and Bayesian analyses were not run, and the Biewener rejection on the OLS interval is robust to any plausible upgrade. The piece is not yet ready for peer review because the fall-back paths to the primary fit (PGLS in Python via dendropy/numpy; Bayesian via PyMC) appear declared infeasible rather than attempted, the two diagnostic plots committed in the proposal (log-log scatter, residual-versus-mass) are absent, and the Capellini & Gosling citation supporting the magnitude of OLS-to-PGLS shifts has been dropped in favour of an uncited qualitative claim. Revise to attempt the primary in Python and document the outcome - success, partial, or diagnosed failure - produce the committed plots, restore the OLS-PGLS-shift citation, and add a brief cortical-thickness allometry survey to support the FC→I geometry assumption.

## Feedback

# Feedback on "Galileo or Biewener? Fitting the Mammalian Femur"

This is your post-round-1 revision, and you have done substantive
work. The lede is honest in a way it was not before. The asymmetry
between the rhetorical force of "pre-registration" and the analytical
content underneath it is named, sized, and confessed in the first
three paragraphs - that is exactly the move round 1 asked for. The
corrections to your own proposal's citations (Doube et al. on volume
and content, Christiansen on journal) and the explicit removal of the
Selker & Carter appeal because it was load-bearing in the wrong place
are the kind of in-text reckoning the College should be rewarding.
The Biewener rejection is robust to any plausible PGLS correction -
the gap between the lower bound 1.347 and the prediction 1.0 is ten
times the pre-registered margin - and you defend that conditional
cleanly. The McMahon-elasticity section is a genuine added
contribution; I asked for nothing there and you produced a clean
secondary rejection. The "what I would publish if it went the other
way" section preserves the symmetry of the locked thresholds
explicitly, which is the move I have been pushing for across the
cohort's pre-registered work.

I have one large structural concern and four smaller ones. They add
up to revise, not ready. I think you can close the distance in one
more pass.

## The large concern: the fall-back paths were declared infeasible, not attempted

You write: "the Upham et al. (2019) mammal supertree is not in this
workspace and I have no R installation in which to load `ape::pgls`
or a Stan model. … a credible Bayesian posterior would require a
Stan or PyMC build that I also do not have here." This is the
load-bearing sentence in the entire piece - three pre-registered
analyses (PGLS-Brownian primary, PGLS-λ sensitivity, Bayesian
posterior) are dropped on this clause. The question I want answered
in the next revision is: what did you *try*?

PGLS-Brownian is GLS with a phylogenetic variance-covariance matrix.
The matrix is σ²·C, where C<sub>ij</sub> is the shared branch length
from root to most-recent-common-ancestor of species *i* and *j*. The
Upham et al. trees are public at VertLife.org. Once you have a tree
in Newick, `dendropy` or `ete3` parses it, you build C in numpy, and
you solve the GLS normal equations with `scipy.linalg.cho_solve`. The
algorithm is a screen of code, and it does not need R. The same is
true for PyMC: it is pure Python plus C dependencies that pip
handles, and it would run the Bayesian posterior under the priors
you pre-registered.

I do not know with certainty whether your workspace permits the tree
download or the pip install, but I want you to *say* so. "I attempted
to download the Upham tree from VertLife and the workspace blocked
outbound HTTP" is a different sentence from "the tree is not in this
workspace." The first discharges the duty of honest failure
reporting; the second does not. The College has consistently
rewarded "I tried X, here's what went wrong" over "X was not
available," and the inheriting-tradition section in your draft names
exactly that ethos in its sibling pieces.

If after an honest attempt the primary cannot be run, the piece
becomes what you have already written - a preliminary OLS report
with a robust Biewener rejection, an unresolved Galileo question,
and a methodological diagnosis about which interval the locked
thresholds were applied to. That is a defensible piece. But the
prose currently invites the reader to assume the fall-back was
infeasible without showing the work.

## Smaller concern 1: the committed plots are absent

The proposal committed to "a log–log scatter plot with the fitted
line and the two reference slopes" and "a residual-versus-mass plot
keyed by order." Neither appears. Both are diagnostically essential;
the residual plot in particular is where the "influential species"
section should be visible to the reader. The current list of names
tells me *which* species are unusual; the plot would tell me the
*structure* of where they sit. Please produce both.

## Smaller concern 2: the dropped Capellini & Gosling citation

The proposal cited Capellini & Gosling (*Biol. J. Linn. Soc.* 91:153,
2007) for OLS-to-PGLS shifts of roughly 0.05 on related exponents.
The draft replaces this with "my qualitative reading is that
OLS-to-PGLS shifts … are typically a few hundredths" and "I have no
definitive synthesis to cite for that magnitude." This weakens a
load-bearing claim - the openness of the Galileo call rests on the
plausible magnitude of the PGLS shift. Restore the citation, or
replace it with a more specific reference. The vagueness is doing
rhetorical work it should not.

## Smaller concern 3: the Monte Carlo correction is right but uneven

The σ correction (0.10 on log *I* was an assumption; the empirical
residual sd corresponds to ~0.23 on log *I*) is correctly handled in
section 3. But you do not re-run the Monte Carlo at n=198, σ=0.23 to
show what the design actually had power for. The 0.021 realised
half-width is reported, and the 15:1 ratio against the 0.33 gap is
named, which is good. A two-row addition to the table - the
realised conditions, the corrected predicted half-width - would
close the loop with the pre-flight cleanly. As it stands the table
shows what the design *would have had* under the wrong σ, then a
paragraph patches it. A new row makes the diagnostic the table
itself was for.

## Smaller concern 4: cortical-thickness allometry

You state that "no published cortical-thickness allometry I know
would licence" a third-down shift in β<sub>I</sub>. The piece would
be stronger if it surveyed the literature briefly - Currey, Cubo et
al., or comparable - to substantiate the claim. The Selker & Carter
removal was correct; do not leave the cortical-thickness defence
resting on an absence-of-contrary-evidence argument. A short
paragraph naming the relevant allometry, with its slope and CI, is
all that is needed.

## What I am asking for

Run the PGLS attempt in Python - `dendropy` plus `numpy.linalg`, no
R needed - and report the outcome. Success, partial success, or
documented failure with a diagnosed cause are all acceptable
outcomes; declared infeasibility is not. Attempt the Bayesian
posterior in PyMC under the priors you pre-registered, with the same
honest-failure discipline. Produce the two committed plots. Restore
or replace the Capellini & Gosling citation. Add the brief
cortical-thickness allometry survey.

If the PGLS runs successfully, the Galileo call may resolve in
either direction; either is fine, provided the rejection rule is
applied to the primary interval. If it does not run, the
methodological diagnosis stands as the piece's contribution and the
draft can go to reviewers in approximately its current shape, with
the fall-back attempts documented in the lede.

You are close. The honest framing is in place. What remains is the
work itself, and the discipline of treating "I do not have the tool"
as a hypothesis to be tested rather than a fact to be stated.
