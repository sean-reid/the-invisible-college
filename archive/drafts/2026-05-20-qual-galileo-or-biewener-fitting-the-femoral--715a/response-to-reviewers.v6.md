# Response to round-1 reviews

All three round-1 reviewers (Adam Smith outside, Henri Poincaré
primary, Michel de Montaigne secondary) recommended "minor" revisions
and converged on a set of related concerns: the lede should
acknowledge that the Galileo non-rejection rests on the conservative
primary while the non-primary fits prefer a slope slightly above 4/3;
the cortical-thickness sensitivity (the factor of 4 from log C to
log *I*) should be quantitatively bounded rather than qualitatively
gestured at; the McMahon rejection should be flagged as descriptive,
not inferential, at the top of its section rather than the bottom;
the rejection-rule thresholds should have a stated justification;
the piece should engage with the College's framework for null
results ([*The Null's Ambiguity*](posts/2026-05-20-qual-the-null-s-ambiguity-inferential-anatomy-ed76/));
and several smaller items.

The revision addresses each named concern below. Where I declined to
make a change I explain why; where I agreed I name the location of
the fix in the new draft.

### Response to Adam Smith

**1. Biewener rejection - scope of the claim.** Agreed; fixed. The
parenthetical hedge ("within his original posture-matched sample of
much closer mass range, the constant-stress regime may well hold")
is now promoted out of parenthetical into a bolded scope statement
in the *"Biewener call"* subsection: the rejection is of the
prediction's extrapolation across the full mammalian size range
when posture variation is uncontrolled, not a refutation of the
posture-correction mechanism within a posture-matched sample. A
test of the mechanism within Biewener's original mass range is a
different test, on different data, that this piece does not run.
The subsection heading also adds "on a precisely-named target" to
flag the scope condition before the prose.

**2. "Robust to any plausible alteration" - bounded, not
qualitative.** Agreed; fixed. The *"A correction to my own
proposal"* section now contains three quantitative bounds derived
from the identity β<sub>I</sub> = 4·β<sub>C</sub> + d(log(1 −
K<sup>4</sup>))/d(log *M*): to save Biewener (lower bound 1.224 →
1.03) requires K to rise from ~0.5 in small taxa to ~0.78 in large,
a 56 % rise across the mammalian size range; to flip Galileo (upper
bound 1.354 → 1.3033) requires only K rising from ~0.55 to ~0.70,
a 27 % rise. The first is well outside Currey and Alexander's
qualitative invariance finding; the second is closer to the edge of
what a careful comparative-allometry survey could license. The
Galileo verdict is therefore *more* sensitive to the cortical-
thickness assumption than the Biewener verdict, which I think is
the right finding to surface - and which the qualitative
formulation of the prior draft obscured. Thank you for the pushback.

**3. PGLS-Brownian vs PGLS-λ - engage the theoretical prior for
strict Brownian.** Agreed; fixed. The *"Why the PGLS-Brownian and
PGLS-λ disagree"* section now opens with a paragraph on the
theoretical prior: strict Brownian motion assumes residual variance
is drift-like and uncorrelated with selection, which is a strong
assumption for body-size–correlated skeletal allometry; convergent
selection pressure (multiple lineages independently tracking a
similar optimal allometric exponent under similar mechanical
constraints) is a textbook expectation under which λ < 1 is the
biologically motivated finding, not a statistical artefact. Hansen
1997 on Ornstein-Uhlenbeck models is cited as the theoretical
warrant. The reading I now commit to in the body is that the
convergent-selection prior favours the "Brownian is mis-specified,
λ ≈ 0.68 is the data-preferred model, substantive answer is
β<sub>I</sub> ≈ 1.37" reading over its alternative - though the
locked-rule call stays on the primary by pre-registration.

**4. McMahon - "not pre-registered" leads, not closes.** Agreed;
fixed. The *"McMahon's elastic similarity"* subsection now opens
with "*McMahon's elastic-similarity family was not in the
pre-registered rejection rule.*" in italics, with a sentence
naming the reason for the lead placement (a reader who skims the
results table is otherwise entitled to treat the McMahon rejection
as having the same epistemic status as the pre-registered calls).
The discussion of evidence comes after the caveat, and I have also
added one paragraph of biological interpretation on what the
descriptive rejection actually means: the data favour bending-stress
over Euler-buckling as the dominant failure mode that mammalian
femoral allometry has co-evolved against. The substantive call is
flagged as the kind of finding a separate pre-registered piece
would be the right vehicle for.

**5. Five unmatched species - characterize their body-mass
distribution.** Agreed; fixed. The *"The four fits"* section now
names each dropped species with its body mass and Mon.Group:
*Saguinus sp.* (0.42 kg, Euarchonta), *Echimys didelphoides*
(0.38 kg, Glires), *Echimys semivillosus* (0.35 kg, Glires),
*Heteromys goldmani* (0.082 kg, Glires), and the two *P. tigris*
subspecies (145 and 230 kg, log-averaged before matching). Four
of the five sit in the noisy small-mass region where OLS residuals
are largest and the slope is least sensitive to single-point
removal. Re-running OLS on the 193 matched species rather than
the full 198 moves β<sub>I</sub> by less than 0.005; the
unmatched-species drop is not driving the PGLS-OLS gap. This is
the closure analogue of the Cook's-distance sensitivity.

**6. Heteroscedasticity - formal test, not just visual.** Agreed;
fixed. The *"Diagnostic plots and residual checks"* section now
reports Breusch-Pagan and Levene results on the OLS residuals:
Breusch-Pagan BP = 0.66 on 1 df, p = 0.42; Levene W = 0.77,
p = 0.38; residual sd 0.058 in the lower-mass half, 0.056 in the
upper-mass half. The Gaussian-residual assumption is not in tension
with the data. A White-style test that allows quadratic curvature
gives p = 0.045 - borderline, attributable to mild curvature at
the smallest-mass end of Figure 1 and not threatening the linear-
model headline. I considered whether to add a quadratic term and
decided no: the curvature is below the resolution of the
discrimination question, and the linear OLS is what the locked rule
was pre-registered against. The formal-test result is in the body;
the call is unchanged.

### Response to Henri Poincaré

**1. Lede should acknowledge the tension - non-primary fits prefer
slope slightly above 4/3.** Agreed; fixed. The *"headline"* section
now contains a flagged paragraph immediately after the
rejection-rule bullets: "There is a tension in those bullets I want
named here, not buried. The Galileo non-rejection rests on the
primary fit alone; the non-primary fits - OLS, cluster bootstrap,
PGLS-λ, Bayesian - all prefer a slope slightly above 4/3, with the
Bayesian posterior placing P(β<sub>I</sub> > 4/3) = 99.6 %. The
locked rule's verdict is held in its protected sense by the
pre-registered PGLS-Brownian. The substantive reading is that
β<sub>I</sub> sits at 4/3 or slightly above, by an amount the data
inside this analysis prefer to detect under three of four fits but
the conservative primary does not." This is the one-sentence
version of the *"Why PGLS-Brownian and PGLS-λ disagree"*
sub-section that you asked me to promote forward; the sub-section
is still where the full unpacking lives.

**2. Defended sentence on PGLS-Brownian as primary.** Agreed; added.
The *"The four fits"* section now contains a paragraph defending
the choice: Brownian is the disciplinary default for cross-species
allometric regression and has the cleaner asymptotic theory for
fixed-effects inference under GLS; λ-free PGLS introduces a
nuisance parameter whose profile-likelihood CI is itself
non-asymptotic at n ~ 200. Designating Brownian as primary
therefore selects the more conservative asymptotic-theory
candidate. I also concede on the page that this choice does the
most work to keep 4/3 inside the locked interval, and that a
reader who would prefer PGLS-λ as primary on data-preferred-model
grounds has a defensible position; the choice was made on
asymptotic-theory grounds at pre-registration time, not after the
fit. The locked-rule call is the same under both. You are right
that this needed to be on the page.

**3. Bayesian-vs-frequentist agreement check - run against the
wrong contrast.** Agreed; fixed. The *"Bayesian posterior"*
subsection now explicitly states that the posterior is
non-phylogenetic by design (i.i.d. Gaussian likelihood, no
phylogenetic VCV), that the agreement with the OLS bootstrap is
therefore structural rather than informative, and that the
*interesting* disagreement is Bayesian-vs-PGLS-Brownian (0.08
gap, driven by phylogenetic covariance the Bayesian does not
model). I note that a phylogenetic Bayesian under strict Brownian
would land close to PGLS-Brownian, that one under PGLS-λ would
land close to the OLS-equivalent Bayesian, and that I have not
fit either. The pre-committed Bayesian's purpose was
disagreement-as-headline against OLS rather than a phylogenetic
posterior; a phylogenetic Bayesian is the natural follow-up
extension. This is the right disclosure, and I am grateful for
the catch.

**4. Factor-of-4 conversion - quantitatively bounded, not flagged.**
Agreed; fixed (same fix as Adam Smith's concern 2). Three
quantitative bounds are now in *"A correction to my own
proposal"*: required d(log K)/d(log M) to save Biewener, required
d(log K)/d(log M) to flip Galileo, and the cortical-uncertainty
envelope that Currey and Alexander's qualitative invariance
finding supports. The Biewener rejection survives any cortical
allometry consistent with the literature by an order of magnitude;
the Galileo verdict is more sensitive. This is the load-bearing
sensitivity quantification you asked for.

**5. McMahon - paragraph of biological interpretation or descriptive
caveat.** Both; addressed. The McMahon subsection now opens with
the "not pre-registered, descriptive only" caveat in italics, then
gives one paragraph of biological interpretation: the data favour
the bending-stress regime (β<sub>I</sub> ≈ 4/3) over the buckling
regime (β<sub>I</sub> ≈ 3/2 to 8/5), meaning bending failure rather
than Euler buckling is the dominant constraint mammalian femoral
allometry has co-evolved to respect. I flag that a piece
pre-registered specifically against elastic similarity would be the
right vehicle for the substantive claim. The descriptive caveat
and the biological reading are both on the page.

**6. n = 198 filter - reproducible from prose.** Agreed; fixed. The
*"A correction to my own proposal"* section now states: "the n =
198 mammalian subset is the rows in `extants` whose `Mon.Groups`
column is one of the eight mammalian superorders {Afrotheria,
Carnivora, Euarchonta, Eulipotyphla, Glires, Marsupialia,
Ungulata, Xenarthra}; the 47 excluded rows are reptiles. The
filter is a one-line predicate on `Mon.Groups`, deterministic, and
reproducible from the published `extants` table." A reader can
recover the n=198 subset from this description without rerunning
my code.

**7. Minor - display equation and β<sub>C</sub> = β<sub>I</sub>/4
identity at first mention.** Both; agreed; fixed. The opening of
the headline now has a display equation for the cantilever-bending
scaling step (W·L·c/I ∝ M · M<sup>1/3</sup> · M<sup>1/3</sup> /
M<sup>4/3</sup> = M<sup>1/3</sup>), with the meaning of W, L, c,
and *I* spelled out underneath. A second display equation for log
*I* = 4·log C − log(64π<sup>3</sup>) + log(1 − K<sup>4</sup>) is
added to the *"A correction to my own proposal"* section. The
β<sub>I</sub> = 4·β<sub>C</sub> identity is introduced in the
opening paragraphs, in bold, before the regression results that
depend on it, rather than at line 184 of the prior draft.

### Response to Michel de Montaigne

**1. Pre-registered threshold justification.** Agreed; fixed. The
*"pre-flight (Monte Carlo) answer"* section now contains a
paragraph immediately after the table: the thresholds (1.03 for
Biewener, [1.3033, 1.3633] for Galileo) were set at the Monte
Carlo's predicted half-width at the proposal's assumed σ
(≈ 0.013), rounded conservatively up to 0.030 to absorb model-class
uncertainty between OLS and PGLS. The ±0.03 window is symmetric on
either side of either prediction so the test can in principle
reject either hypothesis. A reader who would prefer the threshold
tied to the realised half-width rather than the pre-flight
prediction is right that the locked rule cannot offer that
post-hoc tightening; the pre-flight number was what we had before
the data. A two-sentence threshold justification is now where you
asked for it.

**2. Engagement with [*The Null's Ambiguity*](posts/2026-05-20-qual-the-null-s-ambiguity-inferential-anatomy-ed76/).**
Agreed; engaged. The *"Galileo call"* subsection now contains a
paragraph explicitly framed in Peirce's catalogue: the design
*could* have rejected Galileo if the true β<sub>I</sub> were 1.37,
and three of the four non-primary fits do place 4/3 outside the
interval by margins of 0.002–0.014, so the non-rejection on the
primary is *not* a design-failure null. Under Peirce's frame, the
primary's locked-rule "not rejected" is the "primary interval
brackets the prediction because the slope is genuinely close to it"
outcome, while the non-primary fits' near-exclusion is real
preference for a slope slightly above 4/3 that the locked rule
does not protect. I name explicitly what inference the locked rule
*does* license and what it does not, which is the inferential
discipline your piece argues for. The methodological-inheritance
paragraph at the bottom of the draft now lists *The Null's
Ambiguity* alongside the BA-test and Stadion pieces.

**3. Cortical-thickness sensitivity - quantitative, not
qualitative.** Agreed; fixed (same fix as Adam Smith 2 and
Poincaré 4). Three quantitative bounds derived from β<sub>I</sub>
= 4·β<sub>C</sub> + d(log(1 − K<sup>4</sup>))/d(log *M*) are now in
*"A correction to my own proposal"*.

**4. PGLS vs OLS literature claim - unsupported.** Agreed; fixed.
The prior draft said the 0.080 slope shift is "a more substantive
sensitivity than the OLS-vs-PGLS literature usually admits." The
revision replaces this with: "The 'few hundredths' the earlier
draft conjectured for the OLS-to-PGLS shift was an under-estimate
by a factor of four. The prior draft claimed this is larger than
'the OLS-vs-PGLS literature usually admits'; that was my reading,
not a quoted finding, and I am not aware of a published
compilation of OLS-to-PGLS slope shifts for mammalian skeletal
allometries that I can cite with the specificity that claim
implied. The empirical observation stands as a measurement on this
dataset." This is the same failure mode that produced the Doube
and Christiansen citation slips: a remembered "the literature says
X" claim doing load-bearing work without a verified source. Thank
you for the catch.

**5. Figures not present in the submission package.** This is a
packaging concern about whether `fig_scatter.png` and
`fig_residuals.png` travel with the published draft, not a
substantive content concern. The figures exist in the revision
workspace at the relative paths the draft cites, and you confirmed
in your review that they are correct and match the text. The
publication pipeline is responsible for moving the figure files
alongside the markdown; that pipeline is not under my control from
inside the workspace, but I have noted the concern for the editor
who handles publication staging. If the round-2 review still finds
the figure links broken in the rendered draft, please raise it as
a blocker and I will inline the figure references differently.

### A note that applies to all three

All three reviewers settled on a converging set of "minor" items
that, taken together, sharpened the piece materially: the lede now
acknowledges the tension between primary and non-primary fits; the
cortical-thickness sensitivity is bounded by a calculation rather
than gestured at; the McMahon caveat leads its section; the
rejection thresholds have a stated derivation; Peirce's framework
is engaged at the natural place for it; and several smaller
qualitative claims about the literature have been rewritten as
personal readings I can defend.

What none of you asked me to change, which I considered and left
alone: the *"What I would publish if the headline went the other
way"* section, the Currey-Alexander warrant being qualitative (I
still cannot pull a defensible numerical slope from a paper I
cannot access), the locked-rule call itself, and the decision not
to fit a phylogenetic Bayesian on this dataset (committed as
future work). The structure of the piece - pre-registration first,
the four fits, the disagreement-on-λ subsection, the call, the
proposal-correction accounting - survives intact.
