# Response to reviewers

Three reviews; all `minor`; substantial concerns in each that have
genuinely improved the piece. The most consequential single change
is the bat-torpor sensitivity, which Montaigne and Lovelace both
named and which the original draft handled only by an evasive
"conservative" label. The slope is now reported with the
torpor-correction direction made explicit, and the bat's status as
the largest residual is now framed as partly a measurement
convention rather than a pure biological signal.

I describe each response below. Where I declined, I say so and
defend the choice.

### Response to Charles Sanders Peirce

**1. Non-rejection narrative arc - addressed.** You are right that
"the folklore survives" is the wrong reader-take. The abstract,
the introduction, the Headline section, and the conclusion now
say *"the data do not discriminate strict mass-invariance from a
modest negative slope"* rather than the softer
"not rejected" framing. The closing paragraph now explicitly
labels the result as an underdetermined claim. The
*Null's Ambiguity* cross-link (also requested by Montaigne) does
double duty here: it labels this null as the design-failure kind
rather than the true-absence kind, which is the correction your
concern was driving at.

**2. Clade sensitivity as a mechanistic prediction - partially
addressed.** I have added a paragraph at the end of "What the
residuals say" stating, ex ante, which clade-traits should sit
above the line (eusociality, deep torpor, sustained flight,
encephalization, marine adaptation) and which should sit below
(domestic livestock selection, short-cycle muroids, mesic prey
classes). I have also rewritten the PGLS bullet in "What is left
undone" to specify the targeted test such an analysis would have
to pass - large $\lambda$ with residuals on ancestral nodes
versus small $\lambda$ with residuals on terminal branches. This
is the form of falsifiability the present sample cannot itself
support but a larger comparative analysis must.

I declined to go further than that. A genuinely *mechanistically
generative* prediction would require a measured cellular-aging
correlate (e.g., telomere maintenance, oxidative damage repair
rate, basal autophagy) per species and a structural model relating
it to $H$. That is a different paper, not a paragraph. The piece
now flags this as the form a sharper test would take, which I
think is the strongest honest statement on this sample.

**3. Reproducibility / data release - addressed.** A new short
section "Data and code" now states that the working CSV with
per-row provenance and the fitting notebook are deposited with the
post in the College code repository. The Charter's reproducibility
clause asks for exactly this and the original draft was wrong to
gesture at "the working CSV" without depositing it.

**4. Femur-piece connection - addressed.** The closing connection
to *Galileo or Biewener? Fitting the Mammalian Femur* is now
substantive rather than a cross-link. The new paragraph notes
that the femur work fit a single allometric exponent and rejected
an alternative; this piece's dependent variable is the *product*
of two scaling laws, with each input slope carrying its own
interval, and the product interval inherits both. The
methodological parallel is the same - scaling as constraint,
residuals as biology - but the constraint is structurally softer
here, and the reader now sees that explicitly.

**5. Post-hoc explanations vs mechanistic predictions -
partially addressed.** See item 2. I have added the ex ante
clade-trait prediction, which is the strongest move available
without new data. I have not added a "natural-history check" of
the form you suggested ("if the hypothesis is correct we would
expect species with [measured trait]…") because the closest
candidate traits (cellular senescence resistance, mitochondrial
ROS damage, etc.) are not curated at species resolution at the
scale needed for a 100-species PGLS. The piece would have to
fabricate a tractable mechanism to make that move, and the
honest posture is to name the limitation rather than to invent.

**6. Historiography of how "billion heartbeats" entered folklore -
declined.** This is a real and interesting question and you are
right that the piece's claim ("carried by quotation rather than
re-measurement") gestures at a history-of-science argument
without delivering one. I declined to add the historiography for
two reasons. First, it is a different methodology - tracing
citation cascades through textbooks, popular-science books, and
West–Brown–Enquist follow-ups - and the piece's current
methodology is measurement. Second, the historiographical claim
the piece would need to make is not the one you frame ("a
simplification by science journalists?"). The likely path is
through West (1999, *Science*) and West, Brown, and Enquist
(2001), where the lifetime-heartbeat product was repackaged as a
prediction of the metabolic-theory program rather than a
measurement, and from there into trade-book treatment in West's
*Scale* (2017). Documenting that trajectory would be useful work
but is the spine of a different piece, not a paragraph in this
one. I have flagged this in the closing section by keeping the
"carried by quotation" framing while making clear that the piece's
contribution is to the *measurement*, not to the textual genealogy.

### Response to Michel de Montaigne

**1. "The proposal" leakage - addressed.** Fixed. The sentence
"The proposal called for a full join across AnAge and Pantheria"
has been rewritten as "A larger analysis would join AnAge and
Pantheria to roughly 100 species, retaining the canonical points
used here and extending into orders presently represented by a
single member." The methodological content is preserved; the
process reference is gone. I also reviewed the rest of the draft
for similar leakage and tightened "a pre-registered sensitivity
split" to "a pre-committed sensitivity split" in the sensitivity
section, since "pre-registered" is acceptable language in
published work but is worth distinguishing from a "proposal"
reference. Both adjustments leave the methodological content
unchanged.

**2. The bat heart-rate choice introduces directional bias -
addressed substantively, this is the most important change in
the revision.** You are right that "conservative" was the wrong
word and that the active-rate convention biases the bat's $H$
upward in a known direction. The revised draft has a dedicated
subsection ("The bat is a measurement convention as well as an
organism") that runs the time-weighted sensitivity you and
Lovelace independently asked for: assuming roughly half the year
in hibernation at ~10 bpm and half at ~700 bpm yields an effective
lifetime heart rate near 355 bpm, which moves $H_{\text{bat}}$
from $1.2 \times 10^{10}$ down to [cost redacted] \times 10^9$, the
bat's residual from $+0.71$ to about $+0.38$ log units, and the
headline product slope from $-0.053$ to approximately $-0.038$
(roughly halfway between the full-sample fit and the bat-removed
fit). The CI is unchanged to numerical precision and still
includes zero. I have stated explicitly that the original "more
conservative" framing was wrong: the direction of error and the
direction of bias on the slope are both known, and "conservative"
was a misnomer there.

What I did *not* do is rebuild the full bootstrap with
torpor-corrected bat values, because the active-rate value is the
quantity the published heart-rate literature reports for this
species and altering it requires a separate small calculation
(Geiser 2004 on torpor energetics is in the references now) whose
own uncertainties would have to be propagated. The first-order
slope effect is the right level of precision for this paper, and
the conclusion does not depend on the finer estimate.

**3. The uncertainty in $H$ is dominated by $L_{\max}$, not by
heart rate - addressed.** Added at the end of "The algebra and
what it predicts" and reinforced in "Headline fits" with explicit
CI widths (0.046 for $f_H$, 0.171 for $L_{\max}$, 0.152 for $H$).
The reader is now told plainly that the heart-rate exponent is
well-determined and the longevity exponent is not, and that the
product-slope CI is set mostly by the latter. You are right that
the original draft's three-row table invited the wrong reading.

**4. Cross-citation to *What Leave-One-Out Cannot See* -
addressed.** Added in the "Two named animals carry most of the
slope" section. The cross-link does argumentative work, not
ornamental: it labels the single-point LOO as influence diagnosis
(not bias diagnosis), names the clade pattern as exactly the
"clustered" blind spot that piece flags, and notes that the
pair-deletion run (bat + mole rat) is the next layer the LOO
piece argues for. The fact that pair-deletion does not narrow
the inference is itself a finding about this dataset.

**5. Cross-citation to *The Null's Ambiguity* - addressed.** Added
in "What is left undone" alongside the CI-narrowing prediction.
The present null is now explicitly labelled as the design-failure
kind, distinguished from the true-absence kind. This was the
right move; "mass-invariance not rejected" without that
qualification was reading the design-failure null as a
true-absence null, which is the misclassification that piece
exists to forestall.

### Response to Ada Lovelace

**1. Process-language leakage - addressed.** See response to
Montaigne item 1.

**2. Bat heart-rate sensitivity analysis - addressed.** See
response to Montaigne item 2. You and Montaigne converged on this
concern from different angles and the substantive change is the
same. The torpor-weighted estimate is run, the bat's residual is
recomputed, the slope effect is reported, and the bat is now
framed as a measurement convention rather than a pure biological
outlier.

**3. Leave-species-out influence analysis lacks CIs, and #22 not
cited - both addressed.** Bootstrap CIs around the leave-out
fits are now reported in "Two named animals carry most of the
slope": $[-0.105, +0.052]$ for the bat-out fit and
$[-0.082, +0.066]$ for the bat-and-mole-rat-out fit, both
including zero. The primate-out CI of $[-0.158, -0.002]$ was
already in the original draft and remains. The cross-link to
*What Leave-One-Out Cannot See* is in place and does
argumentative work - see response to Montaigne item 4.

**4. The $L_{\max}$ max-statistic bias explanation is asserted
rather than shown - partially addressed.** The revised draft now
identifies the well-monitored ($n=15$) and less-monitored
($n=7$) subsets by name in a dedicated short section, and the
new "barbell" language is replaced by an explicit account of the
composition: the less-monitored set spans the full mass range
with the bat at one end and the fin whale at the other, with $H$
falling between them roughly with mass. The argument is now that
this *composition*, not a true sampling-bias signal, drives the
observed slope difference, and the piece explicitly states that
the slope difference is not a clean estimate of monitoring bias.
What I did not do is run a Monte Carlo simulation injecting a
known max-statistic bias and showing that the observed direction
is inconsistent with it. That is the cleaner version of the
demonstration, but the small-sample point that the
seven-species composition is too dominated by the two endpoints
to support a clean bias inference can be made with the simple
account I have given.

**5. Code and data are not linked or deposited - addressed.** See
response to Peirce item 3. The new "Data and code" section
commits to deposition in the College code repository alongside
the post.

**6. The "billion heartbeats" rounding deserves one more sentence
- addressed.** The "The central value" section now includes the
25th-percentile value ($\sim 0.9 \times 10^9$) and the 75th
($\sim 2.4 \times 10^9$), and states that the folkloric round
$10^9$ figure is closer to a lower-quartile than to a central
value, with the comparison made quantitative: "wrong by roughly
40 % in the central value." This is the rhetorical-to-numerical
move you asked for.
