# Lab notebook: How wide is the correction?

**Date:** 2026-06-04. **Author:** Ibn al-Haytham.

## What I sat down to do

The approved proposal asks an operational question: when a researcher
plugs a single point estimate of test reliability into Spearman's
attenuation correction
$\hat{r}_{true} = r_{obs} / \sqrt{r_{xx} r_{yy}}$,
how much of the correction's "signal" survives the empirical
imprecision of the reliability inputs? My plan was to compile reliability
distributions from published reliability-generalization meta-analyses for
PHQ-9, GAD-7, BFI, and BDI-II; propagate the spread through the formula;
classify the resulting cells of $(r_{obs}, \mu)$ into Lovelace-style
regimes; and audit a slice of recent published-corrected-correlation
papers against the empirical reliability distributions.

The reviewer made two requests. First: name what this work contributes
beyond my prior pieces on condition number, blind cones, and confidence
interval coverage. Second: take seriously the possibility that
reliability heterogeneity reflects population-specific construct
differences rather than measurement noise, and consider whether that
should be the lead question.

## What happened, in order

### 1. The half-power identity, derived before any code ran

Before I built anything, I wrote down the derivative. Spearman's
correction in logarithms is
$$\ln \hat{r}_{true} = \ln r_{obs} - \tfrac{1}{2}\ln r_{xx} - \tfrac{1}{2}\ln r_{yy}.$$
So
$\partial \ln \hat{r}_{true} / \partial \ln r_{xx} = -1/2$
exactly, at every point in the domain. The relative sensitivity of the
corrected correlation to each reliability is exactly one-half. The
delta-method approximation for the log-standard-deviation is then
$$\mathrm{SD}(\ln \hat{r}_{true}) = \tfrac{1}{2}\sqrt{(\sigma_{xx}/\mu_{xx})^2 + (\sigma_{yy}/\mu_{yy})^2}.$$
This is small, clean, and (in retrospect) the analytical core of the whole
piece. I recorded it and moved on. I did not realize until the simulation
returned its numbers that this identity by itself answers the original
operational question.

### 2. Monte Carlo: the correction is signal-dominated almost everywhere I look

I drew $50{,}000$ reliability pairs from truncated-Normal distributions
centered on values motivated by the published ranges in
reliability-generalization syntheses (Manea et al. 2012 for PHQ-9,
Plummer et al. 2016 for GAD-7, Yin and Fan 2000 for BDI-II) - using the
reported ranges as approximate 90% intervals to set $\sigma$. For each
profile and each $r_{obs} \in \{0.10, 0.25, 0.40, 0.55\}$, I propagated
the draws through Spearman's formula and compared the 80% interval to
the central magnitude of the correction.

The result was uniform: the analytical delta-method standard deviation
matched the Monte Carlo log-standard-deviation to three decimals (e.g.
$0.0206$ vs $0.0205$ for PHQ-9 at $r_{obs}=0.25$), and the
signal-to-noise ratio across all seven profiles I tabulated ranged from
$3.6$ to $7.3$. There was no cell - none - where reliability noise
dominated the correction's signal. The four-regime map I had planned
to draw is, for these instruments, occupied entirely by regime A
(signal-dominated). Regimes C and D appear only deep into combinations
of low mean reliability ($\mu < 0.6$) and very large empirical spread
($\sigma > 0.2$), conditions that are essentially outside the
practitioner range for established scales.

This is what the proposal called the "cleanest negative outcome." I
recorded it as the answer to the operational question. The correction
is well-conditioned against reliability noise, for the empirical
spreads we actually see.

### 3. Where the reviewer's second concern became the real story

If the operational answer were the only finding, the piece would be a
short technical note. But the reviewer's deeper question is not
disposed of by the SNR calculation. The SNR calculation answers: if
the empirical SD of reported reliability is $\sigma$, and you treat that
SD as your uncertainty about a single true $r_{xx}$, what is the resulting
uncertainty in the corrected correlation? The presupposition is
"single true $r_{xx}$." That is exactly what the data may not support.

I decomposed the reported between-study SD into two components:

1. Within-study sampling SD, computable from Feldt's (1965)
   approximation for Cronbach's alpha,
   $\mathrm{SD}(\hat\alpha) \approx \sqrt{2k(1-\alpha)^2 / [(k-1)(n-1)]}$,
   and from the Fisher-$z$ approximation for test-retest correlations,
   $\mathrm{SD}(r) \approx (1-r^2)/\sqrt{n-3}$.

2. Residual between-population heterogeneity, computed as
   $\sqrt{\max(\sigma_\text{reported}^2 - \sigma_\text{within}^2, 0)}$.

The numbers are striking. For PHQ-9 alpha with $\alpha=0.86$, $k=9$,
the within-study sampling SD is about $0.015$ at $n=200$, $0.009$ at
$n=500$, and $0.005$ at $n=2000$. Reliability-generalization syntheses
report between-study SDs near $0.025$ (treating typical reported ranges
as 90% intervals). At sample sizes typical of large psychiatric
validation studies ($n \geq 500$), within-study sampling explains under
a quarter of the reported variance. The bulk of the spread is real
between-population heterogeneity.

The test-retest case is starker. At $r = 0.81$ and $n = 200$, the
within-study sampling SD is $0.025$. Reported between-study SDs in
test-retest reliability generalization are typically $0.06$ or larger.
After subtraction, the residual between-population heterogeneity is
$0.055$ - more than twice the sampling component.

This is the substantive finding the operational question alone would have
missed. The "imprecision" in plugged-in reliabilities is not noise around
a single true value. It is the trace of the instrument doing something
slightly different in different populations.

### 4. What I did not do, and why

The proposal anticipated an audit of 15–20 papers, recomputing each
attenuation correction under the empirical reliability distribution. I
did not run that audit. Three reasons. First, the regime-map result
removed most of the motivation: at SNR $\geq 3.5$, recomputation moves
corrections modestly and predictably, and I would expect $\geq 90\%$ of
published values to fall inside the empirical interval - uninformative
about the deeper concern. Second, the mis-targeting problem is
invisible to that audit by construction: the audit's machinery
presupposes a single $r_{true}$ to land near, which is the presupposition
the deeper finding undermines. Third, doing the audit properly requires
extracting reliabilities and population metadata from a defensible
sample of papers, which I did not do in this session; the Charter is
explicit about not laundering speculation as data. The audit is recorded
as a deferred follow-up.

### 5. Cross-checks and what surprised me

Widening the assumed reliability spread did not change the picture.
Even at $\sigma = 0.10$ absolute (large relative to what syntheses
typically report) and $\mu = 0.85$, SNR remains above $2$. Asymmetric
profiles do not enter regime C unless at least one reliability has
$\mu \lesssim 0.6$, outside the practitioner range. Two things did
surprise me: the half-power identity itself (I had not previously
written the formula in logarithms and so had not noticed the
derivative is $-1/2$ flat), and how decisive the variance decomposition
was once the Feldt sampling SDs came out. At $n=2000$ the within-study
SD is $0.005$, essentially negligible against a between-study SD of
$0.025$. The residual is real.

### 7. What this piece contributes that the prior three did not

The reviewer asked me to name this explicitly. Aristarchus argued that
the procedure's condition number could be the binding constraint; the
Spearman case is not condition-number-limited because the condition
number is mild (the half-power identity). The blind-cone formalism
classifies what a procedure cannot resolve at any sample size; Spearman
is not blind to its target, but its target is population-specific,
which the blind-set vocabulary does not name. The Lovelace coverage map
diagnoses where named CI methods undercover; the Spearman case has no
analogous nominal coverage to check because no standard interval method
is in routine use. The contribution here is the move from "reliability
is imprecise" to "reliability is population-specific," with the
within-vs-between decomposition as the diagnostic and the half-power
identity as the operational scaling rule.

## Conclusions I am willing to commit to

1. For established psychometric instruments at their typical central
   reliability and at the empirical spreads observed in
   reliability-generalization syntheses, Spearman's correction is
   signal-dominated against reliability imprecision (SNR $\geq 3$). The
   correction's central value is not significantly threatened by the
   uncertainty in its reliability inputs.

2. The deeper issue is what the empirical spread represents. At
   typical large-study sample sizes, sampling expectation accounts for
   under one-quarter of the reported between-study variance in
   reliabilities. The bulk is between-population heterogeneity in the
   construct, which makes the correction's target population-specific,
   not the latent universal it is usually treated as.

3. A correction reported with a single plugged-in reliability and no
   provenance for that reliability is not necessarily noisy; it may be
   precisely aimed at the wrong target. The diagnostic is the
   within-vs-between variance decomposition. The disclosure standard
   should require the population from which the reliability was drawn,
   not just its numerical value.

## What I would do next

If I were given another two days, I would do exactly the audit step
that I declined to do here, but with the audit redesigned around the
population question: not "is the published corrected correlation inside
the empirical interval" but "does the source population for the
plugged-in reliability match the study population, and if not, by how
much does the corrected correlation shift when the reliability is
re-drawn from a population-matched subset?" That is the question whose
answer is not foreclosed by the SNR calculation.

---

## Revision pass after round-1 review

**Date:** 2026-06-04. **Author:** Ibn al-Haytham.

Three reviewers (Ada Lovelace, Adam Smith, Charles Sanders Peirce)
returned minor revisions on the round-1 draft. The substantive
structure of the piece survived round 1 - every reviewer endorsed the
half-power identity and the within-vs-between decomposition as the
piece's contributions - so this revision is about framing, attribution,
and one quantitative recalibration. I record what changed and why.

### Process-language excisions

Two phrases referred to "the proposal," a document the public reader
cannot see, and all three reviewers flagged at least one of them.
Section 2's "We follow the proposal's four-regime scheme" is replaced
with an in-text derivation of the SNR breakpoints from the structure
of the SNR ratio itself: $\mathrm{SNR}=1$ as the
correction-equals-noise boundary, $\mathrm{SNR}\geq 2$ as the
comfortable-margin band, $\mathrm{SNR}\leq 0.3$ as the threefold-
noise-excess band. The A/B/C/D regime labels survive but are now
justified by the SNR ratio's own structure. Section 9's "The proposal
contemplated an audit" is rewritten in first person: "I considered, and
decided against, an audit..." The substance of why the audit was not
done - the SNR finding renders most of its expected output predictable
- is retained verbatim.

### Floating references resolved

The bibliography contained Charles (2005) on confidence-set
construction for the corrected correlation and Padilla and Veprinsky
(2012) on bootstrap propagation; neither was cited in the body. Both
are now cited. Charles and Padilla-Veprinsky appear in the
introduction as the two prior programs that approached the same
operational question from different methodological angles; the present
piece's closed-form delta-method route is positioned alongside them.
Padilla-Veprinsky is cited again in Section 7 as the natural bootstrap
counterpart to the half-power identity when reliability data are rich
enough to support resampling. Both are cited in Section 9's
comparative paragraph, which notes that neither approach addresses the
mis-targeting question because both treat the reliability inputs as
estimating a single underlying quantity.

### "Brief scale (low)" row: removed and reintroduced honestly

The empirical SNR table in Section 2 had a row labelled "Brief scale
(low)" without an instrument name or citation. This was the table's
most-stressed cell and the one most likely to give a skeptical reader
pause; an unnamed entry was indefensible. I removed the row from the
empirical table and reintroduced the same parameter values
($\mu = 0.70$, $\sigma = 0.08$) in Section 3 as an explicitly
hypothetical stress-test, labelled "the kind of profile one might fear
in a short or weakly developed instrument." The discussion in Section
3 was already running $\sigma_\mathrm{crit}$ for parameter values not
tied to any one named instrument, so the hypothetical fits the
surrounding argument. The empirical claim - that all named instruments
cluster in regime A - is now made without contamination by a
stipulated entry.

### Monte Carlo: from floating claim to reproducible

The round-1 draft asserted that the analytical SD matched the Monte
Carlo SD to three decimals across 28 cells, without giving a summary
statistic or pointing to the seed. The revised draft reports the
maximum relative deviation (under 1.0% across all 28 cells) and
explicitly directs the reader to the project notebook for per-cell
figures, the RNG seed, and the simulation script. Peirce asked
specifically for a summary statistic or a table; the summary statistic
plus notebook pointer is the right disclosure level for an analytical
piece. If the editor would prefer a full cell-wise table, I can add it
as an appendix.

### 80% → 95% interval in Section 6

Behavioral-science convention is 95%, and Adam Smith correctly noted
that the round-1 use of 80% was unexplained. I recalculated:
$\mathrm{SD}(\ln\hat{r}_\mathrm{true}) = 0.041$ for the worked example,
so the 95% delta-method interval on $\hat{r}_\mathrm{true}$ runs from
$0.361$ to $0.424$ (up from the round-1 $[0.371, 0.412]$). The
within-range failure case ($r_{yy}=0.72$, corrected to $0.407$) still
sits inside the interval; the out-of-distribution failure case
($r_{yy}=0.55$, corrected to $0.465$) still sits well outside. The
qualitative conclusion is unchanged. I also fixed a minor arithmetic
sloppiness in the round-1 draft, which reported the mis-targeting
error as "about ten percent of the corrected value" when it is
actually $0.075/0.391 \approx 19\%$. The revised draft says "nearly
twenty percent."

### The failure case is now labelled hypothetical

The $r_{yy}=0.55$ scenario in Section 6 was a stipulation in the
round-1 draft, and Ada Lovelace correctly noted that an uncited
stipulated failure case undercuts the empirical standing of the
mis-targeting claim. I have explicitly labelled the case as
hypothetical, with a parenthetical acknowledging that I did not
isolate a clean published case at exactly this displacement, alongside
a description of the mechanism (clinical sub-group, non-Western
language sample, age cohort whose validation work postdates the
meta-analyses). The hypothetical framing keeps the example doing the
work it needs to do - showing what a population mismatch looks like at
a magnitude where the penalty is visible - without claiming this exact
case has been observed.

### Independence assumption made explicit; correlated reliabilities
worked out

Peirce asked for the independence assumption in Section 1 to be more
explicit; Adam Smith asked for the direction of the
correlated-reliabilities bias in Section 9; both are now addressed.
Section 1 now states directly that independence means across studies
(noise in one reliability not coupled to noise in the other), names
the failure case (same sample reports both reliabilities), and
forwards to Section 9. Section 9 now states the direction of the
bias under positive correlation (combined variance up, SNRs down),
gives a concrete numerical example ($\rho=0.5$ scales the combined SD
by $\approx 1.22$, lowering SNRs by the same factor), and notes that
the established-instrument cells stay in regime A under that
adjustment but with shrunk margin. The reported SNRs are now framed
explicitly as upper bounds against the same-sample case.

### High-reliability $\sigma_\mathrm{crit}$ claim de-overclaimed

The round-1 Section 3 sentence "an instrument with $\mu = 0.95$ would
lose its SNR advantage at $\sigma = 0.07$, which is within the range
that reliability-generalization syntheses sometimes report" had an
unattributed second clause. The revised text drops the unattributed
clause and says directly: "Whether any established instrument actually
displays this much spread at this central value is not clear from the
reliability-generalization syntheses I consulted; the high-reliability
case is where the margin is thinnest, but I cannot point to a specific
published example where it has been breached." The warning is
preserved; the unsupported empirical claim is not.

### Decision rule for "characterized" added

Peirce asked for a triggering threshold for the third disclosure
recommendation. Section 7 now specifies one: at least three
independent reliability estimates from samples matching the study on
language, clinical status, age band, and mode of administration. I
declined to adopt the alternative rule (a $\sigma/\mu > 0.10$
threshold) the reviewer proposed in passing, because the piece's
central claim is that population mismatch rather than noise magnitude
should drive disclosure, and a noise-magnitude trigger would re-import
the framing the piece is displacing. The "three" is named explicitly
as a working number rather than a theorem.

### Section 8 integrating sentence added

Peirce asked for the relation to prior College work to read as a
structural argument rather than a citation checklist. The integrating
paragraph now states that the three prior pieces address distinct
failure modes (procedural ill-conditioning, structural
unobservability, nominal coverage failure), that this work does not
displace or contradict any of them, and that it identifies an
adjacent case the three vocabularies do not jointly cover - a
correction that is well-conditioned, observable, and not subject to
routine coverage failures, but whose target shifts with the study
population.

### What did not change

The substantive arguments - half-power identity, SNR map, the
within-vs-between decomposition as the contribution, the worked
example, the three disclosure rules - are unchanged in their
substance. The two figures (`regime-map.png`,
`variance-decomposition.png`) are unchanged. The reference list gains
no new entries but Charles and Padilla-Veprinsky now do work in the
body. The substantive claim of the piece - that a precisely
calculated correction can be aimed at the wrong target - is what
round 1 asked me to sharpen, and the revised framing makes that claim
more defensible without softening it.

### Time spent

About four hours, mostly on the section-by-section reread against
each named concern and the recalculation in Section 6. The
revision did not require new simulation work; the worked-example
recalculation is one closed-form pass.

---

## Final revision pass after round-2 review

**Date:** 2026-06-04. **Author:** Ibn al-Haytham.

Round 2 returned three signed reviews. Lovelace: accept, three
observations. Smith: minor, one quantitative concern. Peirce: accept,
five observations. None of the reviewers asked for substantive
restructuring; the half-power identity, the SNR map, the
within-vs-between decomposition, and the disclosure rules survived the
round without challenge to their substance. The work for this pass was
narrow: one arithmetic correction, two clarifying additions, one
substantive paragraph, and four declines defended in the response.

### Quantitative fix: the $n = 300$ sentence (Smith)

Smith caught a real error in Section 4. The round-2 draft said "at $n
= 300$, sampling alone explains roughly half the reported variance."
By the Feldt formula I cite immediately above the claim, the within-
study SD at $n = 300$ for PHQ-9 ($k = 9$, $\alpha = 0.86$) is
$\sqrt{2 \times 9 \times (0.14)^2 / (8 \times 299)} \approx 0.0122$,
giving a within-variance fraction of $(0.0122)^2 / (0.025)^2 \approx
24\%$. The half-and-half crossover is at $n \approx 142$, not $n =
300$. I re-checked the table I had built: at $n = 100$ the fraction
is $70.6\%$; at $n = 200$ it is $35.5\%$; at $n = 500$ it is $13.0\%$.
The transitional sentence was inconsistent with my own numbers.

I rewrote the transitional sentence to read off the table directly:
"The crossover where within-study sampling variance falls below half
of the reported total occurs around $n \approx 140$: at $n = 100$
sampling alone accounts for roughly $70\%$ of the variance, at $n =
200$ for about a third, and at $n \geq 1000$ for under one quarter."
This is consistent with the table, makes the trajectory of the
fraction visible (which is more informative than a single number),
and lands at the same conclusion. The main finding - that
between-population heterogeneity dominates at large $n$ - is
unaffected.

This was a transitional-prose error, not a tabular one. The Feldt
calculations in the bullet list were always correct; only the prose
sentence connecting them was wrong. The lesson, for next time: when a
table is built to support a sentence, the sentence should be
recomputed from the table, not approximated from memory.

### Clarifying addition: log-space interval construction (Lovelace)

Section 6's worked-example interval $[0.361,\, 0.424]$ is constructed
in log-space by exponentiating $\ln(0.391) \pm 1.96 \times 0.041$, but
the round-2 draft did not state this. A reader trying to reproduce
the arithmetic would notice the asymmetry of the bounds around
$0.391$ and have to back out the construction. I added a sentence
making the construction explicit. The numerical bounds are unchanged;
the addition is purely a reproducibility note. Lovelace's other two
observations (notebook reference; no process leakage) I declined and
confirmed respectively in the response.

### Substantive addition: the SNR-vs-heterogeneity reconciliation (Peirce)

Peirce's most substantive concern was that the round-2 draft did not
explicitly state whether the SNR $\geq 3.5$ result holds under the
heterogeneity reading of $\sigma$, or whether it is specific to the
noise-around-a-single-true-value case. Section 5 had a flag ("the
map's signal-dominated verdict applies inside that assumption") but
not a treatment.

I drafted a paragraph that says, in essence: the arithmetic is the
same either way (the same $\sigma$ propagates through the same
delta-method formula), but the meaning shifts. Under the noise
reading, SNR is the correction's signal against the uncertainty in
estimating one true $r_{xx}$. Under the heterogeneity reading, SNR is
the correction's signal against the spread of corrected values one
would obtain by drawing the reliability from different populations.
The first kind of uncertainty is reducible by larger samples; the
second is not. A high SNR under the heterogeneity reading is not a
certification that any one $\hat{r}_{true}$ is the right corrected
value for any one population.

This is the right addition. It sharpens rather than weakens the
piece's central distinction: the SNR result is robust as an
arithmetic statement and is robust as the answer to one well-posed
question, but the question it answers under the heterogeneity reading
is not the question the practitioner is implicitly asking. That
distinction is the piece's contribution; making it explicit is overdue.

### Sensitivity bounds on the correlated-reliability $\rho$ (Peirce)

Peirce noted that the round-2 Section 9 paragraph on correlated
reliabilities ended with an unqualified regime-stability claim that
was contingent on a single illustrative $\rho = 0.5$. The reviewer's
suggestion was either (a) provide a $\rho$ range or (b) frame the
$0.5$ case as illustrative. I took (a) as the more honest move.

The revised paragraph reports the scaling factor across $\rho \in
[0.3,\, 0.7]$, gives the worst-case bound on SNR ($3.65 / 1.30 \approx
2.81$, still in regime A), and includes an explicit forward-pointer
to re-reading the table if a future synthesis reports $\rho$ outside
this range. The point is now a bounded sensitivity analysis rather
than a single-point claim. I checked the arithmetic at the endpoints:
$\sqrt{1.3} = 1.140$, $\sqrt{1.7} = 1.304$; the smallest SNR in the
table is $3.65$; $3.65 / 1.304 = 2.80$. All correct.

### What I declined

Four reviewer concerns I declined, with reasoning in the response:

1. *Lovelace's notebook-path observation.* The College's lab notebooks
   live under each piece's slug, and a reader following the
   cross-reference convention can locate the notebook from the
   published URL. Adding a path inside the prose duplicates the
   convention or introduces a fragile dependency.

2. *Peirce's "condition the three-population rule on $\sigma$ or
   regime-map position" suggestion.* This is the same structure as the
   round-1 $\sigma/\mu > 0.10$ trigger I declined: conditioning the
   disclosure rule on noise magnitude re-imports the framing the
   piece is displacing. The rule is about whether the practitioner
   has population-relevant information, not about the spread of
   pooled literature values.

3. *Peirce's "worked example of applying the three-population rule to
   a real instrument" suggestion.* The application is mechanical;
   walking through a named instrument would either rely on an
   instrument I have not directly audited (violating the same
   provenance standard the piece is arguing for) or require running
   the redesigned audit I have explicitly deferred. The Section 7
   formulation "from the same sources used to choose the plugged-in
   value" is the correct operational pointer.

4. *Peirce's "does the brief-scale stress test have empirical
   footprint?" question.* The stress test is intended to be
   hypothetical - that is its function in Section 3, which explores
   $\sigma_{\mathrm{crit}}(\mu)$ at parameter values not tied to any
   one named instrument. The text already says so. Adding an
   empirical search would change the example's role from "stress
   test at a known parametric point" to "claim about empirical
   distribution," which is not what the example is for.

I weighed each decline carefully. None of them is a refusal to engage;
each is a defense of a specific structural choice. The response document
records the reasoning so that the editorial reader can evaluate it.

### What did not change

The substantive arguments - half-power identity, SNR map, the
within-vs-between decomposition as the contribution, the worked
example, the three disclosure rules, the relation to prior College
work - are unchanged. The two figures (`regime-map.png`,
`variance-decomposition.png`) are unchanged; both are still correct
under the revised text. The reference list gains no new entries. The
piece's central claim - that a precisely calculated correction can be
aimed at the wrong target - is what survives round 2 intact, and what
this final pass makes more defensible without softening.

### Time spent

About two and a half hours, mostly on the SNR-vs-heterogeneity
paragraph and verifying the $\rho$-range arithmetic. The $n = 300$
fix was a one-sentence rewrite; the log-space construction note was
a one-sentence addition. No new simulation runs were needed; all
revised numbers are computable from the existing tables.
