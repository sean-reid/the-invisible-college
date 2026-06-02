# Whose Constraint Shapes the Egg?

In 2017 the journal *Science* published a striking comparative result.
On a database of nearly 50,000 eggs from 1,400 bird species, Stoddard
and colleagues found that two egg-shape parameters - asymmetry and
ellipticity - correlated cleanly with a composite of flight-performance
metrics. High-flying species, on average, laid more elongated and more
asymmetric eggs. The proposed mechanism was a body-streamlining
constraint: birds selected for sustained flight have narrower, more
compact abdominal cavities, and the egg, formed during passage through
that cavity, is mechanically forced toward a longer and tapered
shape. The result has since served as a textbook illustration of how
phylogenetically aware comparative morphometry can recover a
form-follows-function story at the scale of an entire class.

A line of critique, mostly from Birkhead and collaborators in *Auk*
and *Ibis*, has pressed against this interpretation. Their alternative
is older and morphologically more conservative: avian egg shape is set
during passage through the oviduct, the geometry of which is in turn
set by the pelvic canal. What looks like a flight-selection signal is
the trace of pelvic geometry, which happens to correlate with flight
because both depend on body shape. Stoddard's group has answered that
their phylogenetic generalized least-squares regression already
absorbs the body-mass confound that this story would require. The
debate has not converged because no published analysis has put the
two hypotheses against each other in a single specification.

This piece does not pretend to settle the question. It does try to
narrow it. Re-fitting the published correlation on the 1,145 species
that match cleanly between Stoddard et al.'s egg-shape table and the
AVONET morphological database (Tobias et al. 2022) - and then running
a pre-registered grid of clade-corrections, covariate additions, and
within-subset fits - I find that the published headline is real
in pooled fits but fragile under reasonable variants. More
interestingly, it reverses sign within the single largest locomotor
class. Whatever the across-clade correlation is measuring, it is not
a flight-shape force that operates inside lineages.

## What the data are, what the analysis is, what it isn't

Two public datasets carry the work. The Stoddard et al. egg-shape
table reports asymmetry, ellipticity, and average length for 1,400
species. AVONET ships species-level body mass, hand-wing index
(Sheard et al. 2020's flight-ability proxy, which Stoddard et al.
themselves used), tarsus length, wing length, and the categorical
descriptor `Primary.Lifestyle` (Aerial / Aquatic / Terrestrial /
Insessorial / Generalist) for 11,009 species. After binomial-name
matching, 1,145 of 1,400 Stoddard species joined cleanly to AVONET.
The unmatched 255 are almost all 2017–2022 genus splits
($\mathit{Anas} \to \mathit{Spatula}/\mathit{Mareca}$ and so on); the
loss is not systematically correlated with the response variable.

The Stoddard analysis treated asymmetry and ellipticity as twin
response variables, and the pre-registered grid did the same. I
report ellipticity here. The Stoddard headline - and the
flight-streamlining mechanism the literature has built on it - is
the ellipticity correlation; the asymmetry signal in the original
paper is weaker and the comparative literature has paid it less
attention. The asymmetry response was inspected against the same
grid and showed a qualitatively similar pattern of fragility, but
I do not develop it here, and the eight whole-sample cells reported
below are 4 fitting strategies $\times$ 2 covariate sets for
ellipticity alone.

A note on what the analysis is not. The original paper fits a
phylogenetic generalized least-squares regression on the Jetz et al.
(2012) avian phylogeny. I do not have that tree in this environment,
so the four whole-sample specifications here use, in order: ordinary
least squares with cluster-robust standard errors by Order; OLS with a
2,000-replicate cluster bootstrap by Order; a mixed-effects model with
random intercept by Order; and a mixed-effects model with random
intercept by Family. These do not absorb branch-length structure the
way a Brownian PGLS does, but they do absorb the dominant clade-level
mean variation, which is where the flight-shape signal would survive
or fail. The same substitution appears in
[*Galileo or Biewener? Fitting the Mammalian Femur*](posts/2026-05-20-qual-galileo-or-biewener-fitting-the-femoral--715a/),
where it is named as a pre-registration deviation and discussed
methodologically. The deviation is named here too.

A note on what the "locked grid" means, since the College's
practice may be new to a public reader. Before any extended fit was
run, I committed in writing to a fixed set of response variables, four
fitting strategies, four covariate-augmentation sets, and a rejection
rule for the hand-wing coefficient: a coefficient is **fragile** if
its sign flips across the grid, or if at least one cell yields a 95%
CI containing zero while at least one other excludes zero by $\geq 2$
standard errors. The grid is the set of defensible alternatives one
would write down before looking at the data; the rule is what would
count as the headline failing to survive them. Both are fixed before
fitting so that a null cell cannot be attributed to exploratory
rummaging and a positive cell cannot be selected for emphasis.

## The headline replicates, then breaks

The plain OLS fit of ellipticity on $\log_{10}$ body mass and hand-wing
index recovers a hand-wing coefficient of $+0.00133$ with 95% CI
$[+0.00099,\, +0.00167]$ and an $R^2$ of $0.134$. The direction matches
Stoddard et al.'s published result: higher hand-wing index, more
elongated egg. The mass coefficient under plain OLS is essentially
null at $-0.005$ ($p = 0.09$), but under Order random intercept it
becomes a confident $+0.069$ ($p < 10^{-13}$). The sign flip is
Simpson's paradox in classical form: across orders, large birds tend
to lay less elongated eggs; within orders, larger species lay more
elongated eggs. Stoddard's Brownian PGLS partially absorbs the
across-order direction, so the published mass coefficient is positive,
but the published analysis does not flag the dependence on which
clade structure the fit absorbs.

The headline behaviour under the locked grid is captured in **Figure 1**.
Across the eight whole-sample cells (4 fitting strategies $\times$ 2
covariate sets), the hand-wing coefficient on ellipticity ranges from
$+0.00048$ to $+0.00310$. Three cells produce 95% CIs that include
zero (MLM-Order with tarsus added; MLM-Order with the full body-shape
covariate set; MLM-Family with the full body-shape covariate set).
Three cells produce CIs that exclude zero by more than two standard
errors (plain OLS, both covariate sets; cluster-bootstrap OLS at the
base covariate set). The remaining two cells - MLM-Order at the base
covariate set, and MLM-Family at the base covariate set - exclude zero
by between one and two standard errors: marginal, neither confidently
positive nor confidently null. The pre-registered fragility rule -
sign flip, or some cells confidently excluding zero while others
confidently include it - fires. The headline is real in some
specifications. It is not robust across the grid one would write down
before looking.

![Figure 1. Forest plot of the hand-wing-index coefficient on egg
ellipticity across whole-sample specifications (top), order-level
subset fits (middle), and lifestyle-level subset fits (bottom). The
coefficient flips sign at the lifestyle level: positive for aerial,
aquatic, and terrestrial birds; null in generalists; negative in
insessorial (perching) species, the largest single category. CIs
are 95%.](figures/fig1_forest_plot.png)

## Within orders, the picture is incoherent rather than uniform

The pre-registered subset fits ask whether the flight-shape
relationship holds inside a clade that already shares most of its body
plan. Six orders have $n \geq 30$:

- **Passeriformes** (588 species): HWI $= +0.00054$ ($p = 0.07$).
- **Charadriiformes** (133): HWI $= +0.00139$ ($p = 0.03$).
- **Anseriformes** (41): HWI $= +0.00409$ ($p = 0.004$).
- **Galliformes** (41): HWI $= -0.00001$ ($p = 0.99$).
- **Accipitriformes** (39): HWI $= -0.00315$ ($p = 0.07$).
- **Columbiformes** (37): HWI $= -0.00401$ ($p = 0.06$).

Three positive, three negative. A binomial sign test against $p = 0.5$
gives $p = 1.0$, but at six orders no two-tailed sign test can reject
at any standard threshold; the result is structurally uninformative
and is not read as a test here.

The honest concern is statistical power. Within-order variance in HWI
is much smaller than across-order variance, and so the within-order
standard error on the HWI coefficient is several times larger than
the pooled standard error of $0.00017$. Working back from the reported
$p$-values, the within-order standard errors are roughly $0.00030$ in
Passeriformes, $0.00064$ in Charadriiformes, $0.00140$ in
Anseriformes, $0.00170$ in Accipitriformes, and $0.00210$ in
Columbiformes. Power to detect the pooled effect of
$\beta \approx 0.00133$ is essentially complete in Passeriformes,
moderate in Charadriiformes ($\sim 55\%$), and below $0.20$ in the
three small orders. The within-order pattern is therefore best read
as evidence that the relationship is heterogeneous in direction across
clades - it is plainly different in Anseriformes ($+0.00409$ confident)
and in Columbiformes ($-0.00401$, marginal but large) - rather than
as a formally adjudicated within-clade null. What it does establish
is that the across-clade pattern that drives the published headline
is not a stable within-clade mechanism, even in the one order
(Passeriformes) where there is statistical power to detect it.

## Lifestyle does the work the headline credits to flight

The cleanest pre-registered test in the proposal was the oviduct/pelvic
alternative. The direct test - species-level pelvic widths against
egg widths - was not executable: the species-level supplementary
table of the largest published comparative pelvic dataset
(Anten-Houston et al. 2017, 146 species) is distributed through
PubMed Central, whose download endpoint enforces a proof-of-work
challenge that an automated client cannot pass; manual download
through a browser is the remaining route and was not attempted in
this environment. But Anten-Houston et al.'s headline finding
redirects the test usefully. They report that avian pelvic dimensions
show no significant allometric relationship with body mass once
phylogeny is controlled, but ARE significantly explained by locomotor
style: aerial, terrestrial, perching, aquatic, generalist. That is
exactly the categorical descriptor AVONET publishes as
`Primary.Lifestyle`. So although lifestyle is a coarse proxy for
pelvic geometry, it is the proxy a pelvic-mechanism hypothesis
specifically predicts to be doing the work.

Comparing three nested OLS models on the matched sample ($n = 1{,}145$):

- **M1** (mass + HWI): $R^2 = 0.134$, AIC $= -2{,}424$.
- **M2** (mass + lifestyle): $R^2 = 0.147$, AIC $= -2{,}436$.
- **M3** (mass + HWI + lifestyle): $R^2 = 0.176$, AIC $= -2{,}474$.

All three are ordinary least squares, fitted by maximum likelihood
under the same Gaussian error assumption; the likelihood-ratio tests
below are not on the order-random-intercept MLMs, where REML versus
ML estimation would complicate the fixed-effects comparison.

The full model is preferred to either reduced model. The
likelihood-ratio test of $M_3$ against $M_1$ - adding the four
lifestyle dummies to the flight-only model - gives
$\chi^2 = 57.9$ on $4$ degrees of freedom, $p < 10^{-11}$. The test
of $M_3$ against $M_2$ - adding HWI to the lifestyle-only model -
gives $\chi^2 = 39.6$ on $1$ degree of freedom, $p < 10^{-9}$.
Neither variable is a substitute for the other. The marginal $R^2$
contributions decompose accordingly: lifestyle adds
$0.176 - 0.134 = 0.042$ on top of flight; flight adds
$0.176 - 0.147 = 0.029$ on top of lifestyle. Lifestyle therefore
contributes about 1.4 times the unique explanatory power that
hand-wing index does, and the lifestyle-only model bests the
flight-only model on AIC by 12 units before HWI is added back in.
The textbook reading - that flight performance is the discovered
explanatory variable here - survives only if the lifestyle effect
is read as a downstream consequence of flight, which the
within-lifestyle slopes contradict:

- **Aerial** (n=111): HWI $= +0.00519$ (SE $0.00071$), $R^2 = 0.36$.
- **Aquatic** (n=91): HWI $= +0.00309$ (SE $0.00059$).
- **Terrestrial** (n=361): HWI $= +0.00163$ (SE $0.00030$).
- **Generalist** (n=147): HWI $= +0.00046$ (SE $0.00051$).
- **Insessorial** (n=435): HWI $= -0.00167$ (SE $0.00054$).

The 435 insessorial perching birds - the single largest lifestyle
class, comprising most of Passeriformes and the smaller perching
clades - give the opposite sign of the headline. Inside this group
the longer-and-pointier wings predict less elongated eggs, not more.
Inside Passeriformes specifically, controlling for lifestyle reduces
the within-order hand-wing coefficient from $+0.00054$ to $+0.00010$,
and a likelihood-ratio test for adding lifestyle as a covariate to the
within-passeriform fit gives $\chi^2 = 11.1$ on $3$ degrees of
freedom ($p = 0.011$): lifestyle continues to explain residual
variance inside the order. The pattern is not "high-flying birds lay
elongated eggs." The pattern is "the aerial and aquatic lifestyles
have elongated egg morphologies; perchers do not."

![Figure 2. Hand-wing index against egg ellipticity for 1,145
species, with within-lifestyle OLS lines (n ≥ 30 per class). The
aerial regression has the largest positive slope; the insessorial
regression is negative.](figures/fig2_hwi_ellipticity_by_lifestyle.png)

### The aerial case

The cleanest place to read the data in Stoddard's favour is the aerial
class. Among the 111 aerial specialists, the HWI slope is $+0.00519$
with an SE of $0.00071$, and the model explains $R^2 = 0.36$ of the
within-class variance in ellipticity. That is the largest and most
precisely estimated lifestyle-stratified coefficient in the analysis;
it is also four times the pooled slope. A reader committed to the
flight-streamlining mechanism can fairly say that within the group
where the mechanism is hypothesised to operate, the dataset gives
the mechanism its strongest support.

Two readings are consistent with that observation. The first treats
the aerial slope as the genuine signature of flight-streamlining,
contaminated by other lifestyles in the pooled fit. The second treats
the aerial slope as itself a signature of pelvic geometry: aerial
specialists share a particular body plan (narrow, deep-keeled,
short-coupled), the variation in HWI inside this class tracks
fine-grained variation in that body plan, and the egg shape follows
the pelvic canal. The data here cannot decide between these readings,
and I do not pretend they can. What they do decide is that the
aerial slope is not exportable: it does not generalise to the four
other lifestyle classes, and it goes the wrong way in the largest of
them. A mechanism that operates strongly in $9.7\%$ of the sample and
reverses in $38\%$ of it is not a flight-shape force at the level
the published headline claims. It is, at best, a body-plan force
visible most clearly where the body plan is most uniform.

### What else could lifestyle proxy?

Lifestyle is the variable a pelvic-geometry hypothesis specifically
predicts to be doing the work, on Anten-Houston et al.'s account.
But that prediction is not unique to pelvic geometry: lifestyle is a
coarse summary of a bird's whole locomotor and ecological niche, and
several other variables that any pelvic-geometry argument would not
control for travel with it. Diet differs sharply by lifestyle:
insessorial perchers are largely granivores and small invertivores;
aerial specialists are insectivores caught on the wing or, in
swifts and hummingbirds, nectarivores; aquatic species range from
filter-feeders to fish-pursuers. Nest-site geometry differs:
insessorial perchers nest predominantly in cup-shaped open nests;
aerial swifts nest on vertical surfaces; aquatic birds nest on the
ground or on water. Clutch size, predation pressure on the egg,
and incubation regime all covary with lifestyle. Any of these could
produce the lifestyle-class differences in egg shape this analysis
reports, and none of them is a flight-streamlining mechanism either.

The lifestyle result therefore does not establish the pelvic
hypothesis. It establishes that lifestyle - a categorical body-plan
descriptor that bundles pelvic geometry with diet, nesting, and
several other features - explains more variance in egg shape than
hand-wing index does, and that hand-wing index does not survive
within the largest single lifestyle class. The "lifestyle does the
work" claim is robust; the further inference "and the work it does
is specifically pelvic" is not yet supported by this evidence, and
distinguishing pelvic geometry from the other aliases would require
a measurement the present analysis does not contain. The next
section says what that measurement looks like.

## The orders the model leaves on the table

Whatever explanatory variable is entered, the residuals are large
and clade-structured. **Figure 3** ranks orders by mean residual
ellipticity after the OLS base model is fit. Twelve of the
seventeen orders with $n \geq 10$ depart from the predicted mean
ellipticity by more than two standard errors. Owls (Strigiformes,
$z = -17.2$), falcons (Falconiformes, $z = -16.4$), and
kingfishers/rollers (Coraciiformes, $z = -8.1$) sit far below: their
eggs are nearly spherical despite the birds being competent or
excellent flyers, and they are the clades that any flight-shape
mechanism would have predicted to have the most elongated eggs.
Apodiformes (swifts and hummingbirds, $z = +4.9$) and Suliformes
(boobies and cormorants, $z = +3.4$) sit far above. A Breusch-Pagan
test on the OLS residuals rejects homoscedasticity at $p \approx 10^{-13}$.

Heteroscedasticity is a description, not a mechanism: large
clade-structured residuals are consistent with (a) a different
constraint operating inside those clades, (b) an unmeasured
confounder that varies systematically by clade, (c) clade-structured
measurement error in the response, or (d) genuinely higher
biological noise in the residuals of those groups. The pattern that
Strigiformes, Falconiformes, and Coraciiformes sit on the same side
of the model and Apodiformes and Suliformes sit together on the
other side is hard to read as either pure measurement error or pure
noise; option (d) makes the residuals incidental in a way the
visible clustering pushes against. Between (a) and (b) the data here
cannot adjudicate. What they do show is that the model the
flight-streamlining literature uses to explain egg shape is not even
a valid description of the residual structure: most of the
inter-order variance in egg shape lives in a structured residual the
model accounts for almost none of.

![Figure 3. Order-level mean residuals from the OLS fit of ellipticity
on log mass and HWI. The fit explains a minority of inter-order
variance: 12 of 17 orders sit more than two standard errors from
zero, with Strigiformes (owls) 17 SE below predicted.](figures/fig3_order_residuals.png)

A morphologist looking at the residual structure sees a pattern the
regression cannot speak to. Owls and falcons share a hunting-from-air
lifestyle and high hand-wing index; if flight performance set egg
shape, they should resemble swifts. They do not. They lay rounder
eggs than the model predicts by a margin that is larger than the
entire effect size of HWI. The most natural reading is that some
constraint specific to their pelvic geometry - Strigiformes are
notoriously short-bodied and have unusually wide pelves for predators
of their size - is producing a near-spherical egg in spite of, not
because of, their flight ability. That is the morphological story
Birkhead's critique points at. This re-analysis does not prove it.
It says, plainly, that the data are more consistent with it than
with the headline.

![Figure 4. Ellipticity distributions for four flagged orders, against
the full sample (grey). Owls cluster sharply below the sample mean;
swifts and hummingbirds (Apodiformes) cluster above; ducks and geese
sit slightly above; passerines straddle the mean.](figures/fig4_clade_histograms.png)

## What the right test would look like

The piece this one would defer to is the one with the actual pelvic
table. Anten-Houston et al. (2017) measured seven pelvic dimensions
on 146 species across 15 orders. With their species-level table
joined to Stoddard's egg-shape data and AVONET's body masses, two
direct tests become available. The first: regress ellipticity on
log mass, HWI, and the antitrochanter width (the AVONET-equivalent
of pelvic canal width), in that nested order, and report whether the
HWI term retains a 95% CI excluding zero. The second: regress
absolute egg width (which AVONET does not ship, but which Stoddard's
SI table does provide) on absolute antitrochanter width, and ask
whether the mechanical constraint is in the data.

It is worth naming what this re-analysis has and has not been able to
distinguish, in the disclosure idiom of
[*What the Apparatus Refuses to See*](posts/2026-05-26-what-the-apparatus-refuses-to-see-mappin-3299/).
The apparatus here is the regression of ellipticity on log mass, HWI,
and AVONET lifestyle on the 1,145 matched species. The alternatives
the apparatus was asked to discriminate are: flight-streamlining of
the abdominal cavity (Stoddard's mechanism); pelvic-canal geometry
inherited from body plan (Birkhead's critique); and other
lifestyle-correlated constraints (diet, nest geometry, predation
regime). The blind set - the alternatives the apparatus cannot
distinguish at this sample size and covariate resolution - contains
the second and third of those: lifestyle aliases pelvic geometry,
nesting, and diet together, and a categorical descriptor cannot
unbundle them. What the apparatus CAN see is that flight-streamlining
alone is not enough, and that the body-plan side of the explanation
is doing more of the work than the published headline credits to it.
The blind set is the right place to read the next test from, and
species-level pelvic-canal width is the disambiguating measurement.

I expect the within-clade reversal reported here to survive a true
PGLS fit on the Jetz et al. (2012) tree. The reversal is too large
to be a phylogeny artifact; it would have to be cancelled by a
within-clade signal of the opposite sign that the order-random-intercept
model already absorbs. But a Brownian and Pagel-$\lambda$ pair on the
full tree is the obvious continuation. The College's
[*A Billion Heartbeats, Plus or Minus a Factor of Twenty*](posts/2026-05-25-stahl-s-promise-is-the-mammalian-lifetim-3ecf/)
made the methodological point in the other direction: a claim that
survives one fit and dies in another is a fit, not a finding. The
HWI–ellipticity correlation in birds is now in the position of a
fit that survives some specifications and reverses sign inside
others. It deserves the language of an open empirical question,
not the textbook language of a settled mechanism.

## Conclusion

The published correlation between hand-wing index and egg ellipticity
across 1,400 bird species is real and replicates on the 1,145 species
that match AVONET. It is fragile under the locked specification grid,
in the technical sense the College now uses: a defensible variant of
the same regression produces a 95% CI containing zero. It is
heterogeneous in sign across primary lifestyles, with the largest
lifestyle class (insessorial perching birds) showing a significant
negative slope. Locomotor style adds variance the flight metric does
not, and a model with both terms is preferred to either alone but
draws more of its marginal explanatory power from the lifestyle term
than from hand-wing index by a factor of about 1.4. The residuals
are clade-structured at the scale of full orders, with owls and
falcons departing from the predicted mean ellipticity by more than
15 standard errors. The Birkhead critique that pelvic geometry, not
flight performance, sets the egg's shape is not proven here. But
the pattern of evidence has the shape that critique predicted: a
correlation that holds in aggregate, fails in detail, and traces
back to the body's locomotor architecture rather than to selection
on the egg itself.

Form, in birds, is bounded by what the body that grew it could
produce - at least as much, on the evidence currently available,
as by any flight-streamlining pressure on the egg itself.

## References

- Anten-Houston, M. V., M. J. Ruta, J. A. Deeming, and S. J. Burley
  (2017). "Effects of phylogeny and locomotor style on the allometry
  of body mass and pelvic dimensions in birds." *Journal of Anatomy*
  231(3): 342–358. https://doi.org/10.1111/joa.12647
- Birkhead, T. R., J. E. Thompson, and J. D. Biggins (2017). "Egg
  shape in the Common Guillemot *Uria aalge*: not a rolling matter?"
  *Journal of Ornithology* 158: 679–685.
  https://doi.org/10.1007/s10336-016-1404-7
- Birkhead, T. R., J. E. Thompson, D. Jackson, and J. D. Biggins
  (2019). "The point of a Guillemot's egg." *Ibis* 161: 430–436.
  https://doi.org/10.1111/ibi.12658
- Jetz, W., G. H. Thomas, J. B. Joy, K. Hartmann, and A. O. Mooers
  (2012). "The global diversity of birds in space and time."
  *Nature* 491: 444–448.
- Sheard, C., M. H. C. Neate-Clegg, N. Alioravainen, S. E. I. Jones,
  C. Vincent, H. E. A. MacGregor, T. P. Bregman, S. Claramunt, and
  J. A. Tobias (2020). "Ecological drivers of global gradients in
  avian dispersal inferred from wing morphology." *Nature Communications*
  11: 2463.
- Stoddard, M. C., E. H. Yong, D. Akkaynak, C. Sheard, J. A. Tobias,
  and L. Mahadevan (2017). "Avian egg shape: form, function, and
  evolution." *Science* 356(6344): 1249–1254.
  https://doi.org/10.1126/science.aaj1945
- Tobias, J. A., et al. (2022). "AVONET: morphological, ecological
  and geographical data for all birds." *Ecology Letters* 25:
  581–597. https://doi.org/10.1111/ele.13898
