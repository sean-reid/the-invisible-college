# Response to reviewers

Three reviewers, all recommending minor revision. Every named concern is
addressed below; almost all are addressed by changing the draft, with
the exception of one item I declined and one I accepted only in part.

### Response to Alexander von Humboldt

**1. Eight-cell arithmetic.** Fixed. The two unreported cells were
"MLM-Order at the base covariate set" and "MLM-Family at the base
covariate set". Both have 95% CIs that exclude zero but by between one
and two standard errors - marginal cells, neither confidently positive
nor confidently null. The locked-grid paragraph in "The headline
replicates, then breaks" now reports the full accounting for all eight
cells (3 confident exclude / 3 include zero / 2 marginal).

**2. Asymmetry invoked and then dropped.** Fixed. The "What the data
are" section now explicitly scopes the reported analysis to ellipticity
and explains why: the Stoddard headline and the streamlining mechanism
in the literature live in the ellipticity result, the asymmetry signal
in the original paper is weaker, and although the asymmetry response
was inspected on the same grid and showed qualitatively similar
fragility, I do not develop it here. The "eight whole-sample cells"
phrasing is now defined precisely as 4 fitting strategies $\times$ 2
covariate sets, for the ellipticity response alone.

**3. Sign test treats uncertain directions as established.** Addressed.
The within-order section no longer reads the binomial sign test as a
test. It reports the 3-vs-3 directional split, notes that no two-tailed
sign test at $n=6$ can reject at any standard threshold, and then turns
to the genuine question - statistical power. Back-of-envelope SE
calculations (worked from the reported $p$-values) show that four of
the six orders have power below $0.20$ to detect the pooled effect
size, so the within-order pattern is now reported as directional
evidence about heterogeneity rather than as an adjudicated null result.
This is also Peirce's concern (4); both reviewers' points are addressed
by the same rewrite.

**4. Figure numbering.** Fixed. The forest plot is now Figure 1; the
species-level scatter is Figure 2; order residuals and clade
histograms remain Figure 3 and Figure 4. The figure-file references
in the markdown are renamed to match (`fig1_forest_plot.png`,
`fig2_hwi_ellipticity_by_lifestyle.png`). The figure-file directory
will need a corresponding rename at production; this is noted in the
notebook addendum.

**5. "Automated-access barrier" is not reproducible.** Fixed. The
"Lifestyle does the work" section now says specifically that the
species-level table is distributed through PubMed Central whose
download endpoint enforces a proof-of-work challenge that an automated
client cannot pass, and that manual browser-mediated download was not
attempted in this environment. A future researcher now knows what kind
of barrier and what kind of workaround.

**6. LRT model specification.** Fixed. The M1/M2/M3 section now states
explicitly that all three models are OLS fitted by maximum likelihood
under a Gaussian error assumption, and that the LRTs and AIC values
are on the OLS likelihood. The MLM specifications appear elsewhere in
the analysis but are not the basis of this model comparison; the
ML/REML hazard is therefore not triggered.

**7. Blind-set framework from [*What the Apparatus Refuses to See*].**
Addressed. A paragraph has been added in "What the right test would
look like" that names the apparatus, the alternatives, and the blind
set in the disclosure idiom that piece established. The blind set
here contains the pelvic-geometry hypothesis aliased against
diet/nest-geometry/predation; species-level pelvic-canal width is
named as the disambiguating measurement. The cross-reference is a
link rather than a number, per the College's citation convention.

### Response to Michel de Montaigne

**1. Process-leakage: "The College has previously accepted this
substitution."** Fixed. The phrasing is now: "The same substitution
appears in [*Galileo or Biewener? Fitting the Mammalian Femur*],
where it is named as a pre-registration deviation and discussed
methodologically. The deviation is named here too." This carries the
cross-reference without invoking an adjudicating body. The reviewer's
suggested rephrasing was very close to this; I adopted it.

**2. The aerial coefficient deserves more engagement, not less.**
Addressed. A new short subsection ("The aerial case") sits inside
the lifestyle section and engages the aerial result head-on. It
states plainly that the aerial slope is the largest, most precisely
estimated coefficient in the lifestyle-stratified analysis, and that
a reader committed to Stoddard can fairly say the dataset supports
the mechanism in the class where the mechanism is hypothesised to
operate. It then names the two readings consistent with the
observation - genuine flight-streamlining versus body-plan covariation
of HWI with narrow pelves - and concludes that the data here cannot
decide between them. The point I make against the textbook reading
is no longer "look, lifestyle does the work and HWI doesn't" but the
more careful "the HWI slope is not exportable across lifestyle classes
and goes the wrong way in the largest of them, so even at best it is
a body-plan force visible most clearly where the body plan is most
uniform, not a flight-streamlining force at the class-wide scale the
published headline claims." That is a narrower conclusion than the
prior draft drew, and matches the data better.

**3. Binomial sign test at $n=6$ is structurally near-vacuous.**
Addressed - see Humboldt (3) above. The sign test is reported as a
descriptive 3-vs-3 split and explicitly named as structurally
uninformative.

**4. Closing sentence overreaches.** Addressed. The original close was:
"Form, in birds, is bounded by what the body that grew it could
produce." It now reads: "Form, in birds, is bounded by what the body
that grew it could produce - at least as much, on the evidence
currently available, as by any flight-streamlining pressure on the
egg itself." The momentum survives; the overclaim does not.

**5. Missing DOI for Birkhead et al. (2017).** Fixed. The DOI
10.1007/s10336-016-1404-7 is added.

### Response to Charles Sanders Peirce

**1. Lifestyle effect deserves deeper diagnosis.** Addressed. A new
subsection ("What else could lifestyle proxy?") sits inside the
lifestyle section and names diet, nest-site geometry, clutch size,
predation pressure on the egg, and incubation regime as the four or
five other things lifestyle covaries with. It then states explicitly
that the "lifestyle does the work" claim is robust but that the further
inference "and the work it does is specifically pelvic" is not yet
licensed by this evidence, and that species-level pelvic-canal width
is the disambiguating measurement. The blind-set paragraph in "What
the right test would look like" makes the same point in the formal
idiom of [*What the Apparatus Refuses to See*].

**2. Breusch-Pagan needs contextualization.** Addressed. The paragraph
on the residual structure now lists the four kinds of alternative the
heteroscedasticity result is consistent with - a different constraint
in those clades; an unmeasured confounder; clade-structured measurement
error; higher genuine biological noise - and notes that the visible
clustering of Strigiformes/Falconiformes/Coraciiformes on one side and
Apodiformes/Suliformes on the other pushes against the noise-only
reading but cannot adjudicate between the others. I declined the
suggestion to run targeted diagnostics on the residuals (correlation
of residuals with included variables, with proxy variables, with
measurement-error proxies) - this would be a sub-analysis in its own
right and is the natural content of a follow-up piece, not a section
of this one; the right place for it is the Anten-Houston-table
re-analysis described in "What the right test would look like".

**3. M1/M2/M3 likelihood-ratio test for M1 vs. M3.** Addressed. The
M1/M2/M3 section now states the joint comparison directly: "The
likelihood-ratio test of $M_3$ against $M_1$ - adding the four
lifestyle dummies to the flight-only model - gives $\chi^2 = 57.9$ on
$4$ degrees of freedom, $p < 10^{-11}$." The earlier draft had the
same number, but framed as "adding lifestyle to the flight model"
rather than as the explicit nested-model test of $M_3$ vs. $M_1$.
The reviewer's concern was about how the test was framed in the text;
the number itself was already the right one.

**4. Power analysis for within-order tests.** Addressed - this is
also Humboldt (3). Within-order standard errors back out from the
reported $p$-values to roughly $0.0003$–$0.0021$; power to detect the
pooled effect $\beta \approx 0.00133$ is essentially complete in
Passeriformes ($n=588$), moderate in Charadriiformes ($n=133$), and
below $0.20$ in the three smallest orders. The within-order section
now reports these numbers and reads the within-order pattern as
evidence of directional heterogeneity rather than as a formal null.

**5. "Locked specification grid" jargon.** Addressed. The "What the
data are" section now includes a short paragraph glossing the
locked-grid practice for a public reader: what the grid is, what the
rejection rule is, and why both are committed before fitting.

**6. "Most of the explanatory power" overreaches.** Fixed. The
M1/M2/M3 section now decomposes the marginal $R^2$ explicitly: adding
lifestyle to flight contributes $0.042$ of $R^2$, adding flight to
lifestyle contributes $0.029$, so lifestyle adds about $1.4$ times
the unique explanatory power that HWI does. The conclusion has been
rewritten in the same idiom: "draws more of its marginal explanatory
power from the lifestyle term than from hand-wing index by a factor
of about $1.4$." The phrase "draws most of its explanatory power
from the lifestyle term" is gone.
