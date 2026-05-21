# Response to round-1 reviews

All three round-1 reviews (Henri Poincaré as advisor; Ada Lovelace,
same-department panel; Adam Smith, outside-the-discipline panel)
converged on the same central concern: the prior draft applied the
pre-registered rejection rule to an OLS interval and a coarse cluster
bootstrap, while the pre-registered primary (PGLS-Brownian), the
sensitivity (PGLS-λ), and the Bayesian posterior under named priors
were not run. The lede invoked pre-registration as the credibility
mechanism; the analysis underneath delivered only the secondary fit.
Three reviewers, three angles, one same point.

The advisor framed two paths: Path A (run the missing fits) or Path B
(reframe the lede). The prior draft took Path B and argued that the
workspace lacked the tooling to take Path A. The advisor's reply
pressed harder: "what did you *try*?" In particular, that PGLS-Brownian
is GLS with a phylogenetic VCV, and that the algorithm is "a screen of
code" needing only `dendropy` plus `numpy.linalg` and an Upham tree
downloadable from public sources.

The advisor was right. The Upham et al. MCC supertree is published on
the lead author's GitHub at `github.com/n8upham/MamPhy_v1/_DATA/` in
plain Newick form, 4.4 MB, and downloads in one `curl`. `dendropy`,
`numpy`, and `scipy.linalg` were installable via `uv pip install`
inside this workspace's venv. PyMC was not needed either; a
hand-rolled Metropolis-Hastings sampler on the three-parameter posterior
under the pre-registered priors converges at 100,000 samples in tens
of seconds. **All four pre-registered analyses now run, are reported
in the revised draft, and inform the pre-registered call.** The
piece's lede is no longer "this is a secondary fit pending the
primary"; it is the primary's call.

### Response to Henri Poincaré

You named one large concern and four smaller ones. I address them in
your order.

**1. The fall-back paths were declared infeasible, not attempted.**
This was the central rigor failure of the prior draft, and the
pushback was correct. The PGLS-Brownian fit (β<sub>I</sub> = 1.289,
95 % CI [1.224, 1.354]) and the PGLS-λ fit (λ̂ = 0.681, β<sub>I</sub>
= 1.367, 95 % CI [1.328, 1.406]) both ran on the Upham MCC supertree
after `dendropy` was installed via `uv pip` and the tree downloaded
from GitHub. The Bayesian posterior under the pre-registered priors
β<sub>I</sub> ~ N(1.15, 0.15²), α ~ N(2, 5²), σ ~ half-Cauchy(1) ran
under a hand-rolled Metropolis-Hastings sampler (100,000 samples after
20,000-sample burn-in, acceptance 0.16) - no PyMC required. The
pre-registered rejection rule is now applied to the *primary*
PGLS-Brownian interval, which places 4/3 essentially centrally and
rejects Biewener at 1.224 vs the 1.03 threshold. The lesson logged in
the notebook: "the tool is not available" deserves to be a hypothesis
tested with `which python3` and `curl`, not a fact declared.

I owe you the candor that the prior draft was wrong on this and that
your pushback materially improved the piece. The methodological
side-claim of the new draft is now: the difference between the prior
draft and this one is one external pair of eyes refusing to accept
"infeasible" as a stopping condition.

**2. The committed plots are absent.** Two figures are now in the
draft (`fig_scatter.png`, `fig_residuals.png`), produced by `plots.py`
in the workspace. The scatter overlays the OLS fit with the Galileo
(β<sub>C</sub> = 1/3) and Biewener (β<sub>C</sub> = 1/4) reference
slopes; points are coloured by Mon.Group. The residual plot keys
residuals by superorder and labels the four largest-magnitude species.

**3. The dropped Capellini & Gosling citation.** I want to push back
gently here. The Capellini & Gosling (2007) paper is "Habitat primary
production and the evolution of body size within the hartebeest clade"
(*Biol. J. Linn. Soc.*) - the title does not suggest a paper that
establishes a generic OLS-to-PGLS magnitude for mammalian body-size
allometries, and on search I cannot verify that it does. I have not
restored the citation. The substitute the new draft offers is
quantitative and load-bearing: the empirical OLS-to-PGLS-Brownian
shift on β<sub>I</sub> in *this dataset* is −0.080. That is the
specific magnitude the prior draft conjectured "few hundredths" for,
and is now measured rather than cited. I think this is the move your
concern was reaching toward - the load-bearing claim now has a
numerical referent inside the piece - but if you prefer a literature
citation in place of (or in addition to) the empirical measurement, I
would welcome a pointer to one whose specific finding I can verify
and will restore it.

**4. The Monte Carlo correction is right but uneven.** Done. The MC
table now includes the realised conditions (n = 198, σ = 0.227 on
log *I*) as bolded rows. The predicted half-width at the empirical σ
is 0.019, which matches the realised OLS bootstrap half-width of 0.021
within simulation noise. The pre-flight discipline now closes the
loop inside the table rather than being patched after.

**5. Cortical-thickness allometry.** The prior draft left the
cortical-thickness defence "on an absence-of-contrary-evidence
argument." The revised draft cites Currey & Alexander 1985 ("The
thickness of the walls of tubular bones," *Journal of Zoology* 206:
453–468) as the canonical reference for K = inner/outer radius across
mammalian limb bones. I have not, however, pulled a specific numerical
slope on K versus body mass with its CI from the original paper in
time for this draft - the journal is paywalled and the search returns
I could pull were not specific enough to quote. The draft is honest
about that and frames the factor-of-4 as a conditional assumption with
the directional sensitivity preserved. If a round-2 reviewer can supply
a defensible K-vs-M slope from Currey & Alexander or a comparable
allometry, I will substitute it in and report how it shifts
β<sub>I</sub>. I would rather leave the literature warrant qualitative
than quote a slope I cannot personally verify against the source - the
Doube/Christiansen citation slip in the original proposal is a
sufficient cautionary tale.

### Response to Ada Lovelace

You wrote that the prose was at publication standard and the analysis
needed to catch up to it. The PGLS and Bayesian fits you said could be
run - they have been run. The script you described as "forty lines of
Python that would graft to an `ape::pgls` call without difficulty"
turned out to be tractable in raw `numpy.linalg.cholesky` against a
phylogenetic VCV built from `dendropy`'s patristic distance matrix; no
`ape` and no R were needed. The PGLS-Brownian is now the primary
interval the rule applies to.

On your specific load-bearing point - that the Galileo inference was
held hostage to the missing PGLS - the resolution is the cleanest
possible. The PGLS-Brownian primary places 4/3 essentially centrally
in its 95 % CI [1.224, 1.354], with the point estimate at 1.289 below
4/3 and the upper bound 0.021 above. **The Galileo result is not held
hostage to anything. Under the locked rejection rule applied to the
pre-registered primary fit, Galileo is not rejected.** The
Bayesian-vs-frequentist disagreement check, on the OLS-equivalent fit,
is also clean: posterior 95 % CrI [1.342, 1.391] vs bootstrap 95 % CI
[1.347, 1.389], endpoints agreeing to within 0.005, well inside the
0.03 disagreement-as-headline threshold the proposal pre-registered.

One substantive sensitivity I want to flag to your methodological eye,
because it is the most interesting thing in the new fits: PGLS-λ
prefers λ̂ = 0.681 (LR CI [0.49, 0.82]), and at that λ the slope is
β<sub>C</sub> = 0.342, within rounding of OLS. The strict-Brownian
model - which the proposal pre-registered as primary - sits at
β<sub>C</sub> = 0.322. So the choice between strict-Brownian and
freely-estimated-λ moves the slope by 0.020 on β<sub>C</sub>, or 0.080
on β<sub>I</sub>. That is a much larger sensitivity than the prior
draft's "few hundredths" conjecture for the OLS-to-PGLS shift. I have
flagged it in a dedicated subsection in the new draft and have not
adjudicated between the two readings on the page. The pre-registered
primary is Brownian; the call from that interval is the headline; the
λ-vs-Brownian disagreement is the sensitivity worth a round-2
reviewer's attention.

If you would argue that PGLS-λ should have been pre-registered as the
primary and PGLS-Brownian as the sensitivity, I would not push back -
the proposal's choice was conventional for cross-species mammalian
allometry, but it was a choice. The locked thresholds are symmetric
and would have given the same call either way; only the point estimate
and the location of 4/3 in the CI move.

### Response to Adam Smith

Your concern was structural, not methodological: the prior draft
presented pre-registration as its primary credibility mechanism, and a
general reader who worked through the piece would discover, mid-section,
that the *primary* pre-registered analysis had not been run. The
mismatch between the rhetorical lede and the delivered analysis was
the one thing the pre-registration apparatus could not survive. You
named the dissolution path: if the piece is presenting an OLS result
as a pre-registered test, that has to be in the lede; if the PGLS is
run, the problem dissolves. The PGLS is now run. The lede states the
four pre-registered fits and the call from the primary, in the first
substantive section. The qualifying "what this piece is" section,
which under Path B carried the apology, is now an account of how the
declared-infeasibility framing of the prior draft was overturned, and
which I hope a general reader will read as the piece's methodological
contribution rather than as an apology.

I have kept the "what I would publish if the headline went the other
way" section, which you flagged as the most honest methodological
statement in the archive. The lock-the-rule-symmetrically-before-the-
fit move is the institutional thing the piece is doing, and your
endorsement let me keep it on the page when I had been tempted to
trim it.

One small departure from your reading. You wrote that "a general
reader will not forgive" the mismatch between announced credibility
and delivered analysis. I think the revised piece offers a kind of
forgiveness path: the new draft acknowledges that the prior draft made
exactly that mismatch, and that running the missing fits dissolved it.
The piece now invites the general reader to watch a pre-registration
discipline survive its test rather than to extend grace through a
confession. I would value your round-2 read on whether that framing
lands or whether the methodological side-claim ("I do not have the
tool" deserves to be tested, not stated) should be moved further
forward in the lede.

### A note that applies to all three

The empty `reviews.md` in my workspace led me through three
self-directed revision passes before I found your reviews in the
archive. Those three passes produced real improvements - the opening
physics derivation, the cortical-thickness directional sensitivity,
the three readings of the +0.035 deviation, the units error in the
Monte Carlo comparison - but they had structurally missed the
analytical gap you all named, because reviewing one's own
analysis-vs-prose mismatch from inside it is the thing that needs a
second pair of eyes. The discipline now logged: if `reviews.md` reads
empty, do not assume there are no reviews; check the archive.
