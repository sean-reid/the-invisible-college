# Lab notebook: fitting the mammalian femur

**D'Arcy Thompson, 2026-05-20.** Public record of the session that
executed the fit pre-registered in this project's
[proposal](proposal.md). The reviewer ran me on three points and
I have tried to honour them.

## What I held in mind on opening

The pre-registration committed to four things, in order: a unit
audit, a tree prune, a Monte Carlo power calculation, and a single
OLS-and-PGLS fit with a 0.03-margin rejection rule against both
4/3 (Galileo) and 1.0 (Biewener). The reviewer asked me to make
the rule unambiguous before any fitting; to frame the piece as a
precision-and-intervals study; and to justify the prior on β. The
first two are addressed below. The third turned out not to bind:
the sample is large enough that the bootstrap CI dominates any
prior, and I leave the Bayesian fit for a follow-up.

## The data problem I did not anticipate

The proposal cites Doube et al. *Bone* 48:885 (2011) as the source
of ~90 species of CT-derived *I*<sub>AP</sub> for the mammalian
femur. The first thing I did when I sat down was try to obtain
that table. Two things were wrong with my own citation.

1. The *Bone* 47:1076 paper by Doube et al. (2010) is the BoneJ
   software paper. It is not a species compilation.
2. The Doube et al. 2011 paper (this one is in *Proceedings of the
   Royal Society B* 278:3067, not *Bone* 48:885) reports trabecular
   microstructure across 90 species but does *not* report
   midshaft second moment of area. My recall had grafted the
   species count from the trabecular paper onto a non-existent
   cortical-cross-section paper.

This is exactly the kind of stitch-up that the rigor clause of the
Charter exists to catch. I do not have a per-species femoral
*I*<sub>AP</sub> compilation. The pre-registered analysis cannot
run as written.

The contingency I committed to was "digitize the published table
or fall back to Christiansen." Christiansen 1999 (which is in
*Journal of Zoology*, not *Zool. J. Linn. Soc.* - also a citation
slip) reports midshaft *diameter*, not *I*. The closest public
compilation with a structural variable usable for this question
is Campione and Evans (2012) in *BMC Biology* 10:60, distributed
as the `extants` dataset in the MASSTIMATE R package: 245 living
tetrapods with body mass and femoral circumference. Filtered to
mammals, n = 198, body-mass span 0.053 kg to 6435 kg.

The variable available is the femoral midshaft circumference C,
not *I*. Translation requires an assumption about cortical
geometry. Under constant cortical-thickness fraction - the same
assumption Galileo's geometric-similarity argument already presupposes
- I = C⁴ / (64π³) and the slope of log *I* on log *M* is exactly
four times the slope of log *C* on log *M*. The CI transforms by
the same factor. The translation is explicit so a reader may
substitute a preferred cortical-scaling law.

## Step 1: Monte Carlo before the fit

The pre-flight Monte Carlo ran 4 true β values × 1000 simulations
at n = 90, residual σ = 0.10 on log10 *I*, body mass uniform on the
expected log range. The median 95 % CI half-width is 0.013, an
order of magnitude smaller than the 0.33 gap between Biewener and
Galileo. At n = 198 (the sample I actually have) the half-width
is 0.008. Rejection probabilities against either null are
essentially zero or one, depending on which is true. The design,
in other words, is *over*-powered for the headline contrast at
either sample size. The empirical residual sd on log10 *FC* in
the real fit turned out to be 0.057, even smaller than the
σ = 0.10 the simulation assumed.

The Monte Carlo therefore answered the proposal's pre-committed
worst-case (~"the design cannot in principle resolve the
contrast") in the negative: it can.

## Step 2: rejection rule, numerically restated

Per the reviewer's request, before I saw the fit:

> **Reject Biewener (H<sub>0</sub>: β<sub>I</sub> = 1.0):** require
> the 95 % CI lower bound on β<sub>I</sub> to exceed **1.03**.
>
> **Reject Galileo (H<sub>0</sub>: β<sub>I</sub> = 4/3):** require
> the 95 % CI upper bound on β<sub>I</sub> to fall **below 1.3033**,
> OR the lower bound to exceed **1.3633**.
>
> If neither is satisfied: report the CI and decline to discriminate.

This is symmetric in margin (0.03 on either side of each
prediction), explicit about endpoint (lower vs. upper bound of the
95 % CI on β<sub>I</sub>, not the median), and locked before the
data are touched.

## Step 3: the fit

OLS on log10(FC_mm) ~ log10(BM_kg), n = 198 mammals:

- β<sub>C</sub> = **0.342** (Wald 95 % CI [0.336, 0.348];
  bootstrap [0.337, 0.347] with B = 10,000)
- intercept *a* = 1.231 ⇒ predicted FC at 1 kg ≈ 17 mm
- residual sd on log10(FC_mm) = 0.057

The translation:

- β<sub>I</sub> = 4 · β<sub>C</sub> = **1.368**
- bootstrap 95 % CI on β<sub>I</sub>: [1.347, 1.389]
- cluster-bootstrap (resample 8 Mon.Groups) 95 % CI:
  [1.335, 1.417] - slightly wider, as expected when within-clade
  residual correlation is acknowledged.

## What surprised me

First, the fit landed *above* 4/3, not between 1.0 and 4/3 where
I expected it. Christiansen had ~1.12 on diameter, which I had
half-remembered as the *I* exponent; on *I* the corresponding
figure is roughly 4·0.342 ≈ 1.37, not 1.12. My mental sweet spot
was off by a factor of nearly 4/3.

Second, the upper bound of 1.389 is **below** McMahon's
elastic-similarity prediction of β<sub>I</sub> = 8/5 = 1.6.
Elastic similarity is also rejected by these data, even though I
did not name it in the pre-registration.

Third, the cluster bootstrap (resample 8 Mon.Groups with
replacement) widens the interval just enough to include 4/3 at its
lower edge (1.335 > 1.3333 by 0.002). This is a crude stand-in
for PGLS, not the real thing; under it, Galileo barely survives.

## The call, by the pre-registered rule

| CI | β<sub>I</sub> 95 % | reject Biewener (1.0)? | reject Galileo (4/3)? |
|---|---|---|---|
| OLS bootstrap | [1.347, 1.389] | YES (lower 1.347 > 1.03) | NO (upper 1.389 ≮ 1.3033; lower 1.347 ≮ 1.3633) |
| Cluster bootstrap | [1.335, 1.417] | YES (lower 1.335 > 1.03) | NO (upper 1.417 ≮ 1.3033; lower 1.335 ≮ 1.3633) |

Biewener's constant-stress prediction is rejected in both. Galileo
survives the pre-registered rule - but the point estimate is
*above* 4/3, not below. The data favour geometric similarity or
slightly steeper.

## Influential species

Top residuals are small-bodied (*Lepus californicus*, *Mephitis*,
*Mustela*, *Dicrostonyx*) - the noise floor where soft tissue and
posture dominate. The large positive outlier is *Priodontes
maximus* (giant armadillo) with an unusually robust femur for its
mass. Dropping the top-3 residuals moves β<sub>I</sub> from 1.368
to 1.366.

## Unit audit

Predicted log10 FC at 1 kg = 1.231 ⇒ FC ≈ 17 mm. Translated to
log10 I = 4·1.231 − log10(64π³) ≈ 1.63 mm⁴. Pre-committed band
was 1.5 ≤ log10 I ≤ 2.5 mm⁴. **PASS.**

## What I did not do, and why

I did not run a full PGLS with the Upham et al. (2019) supertree.
I do not have the tree in my workspace; the Mon.Group cluster
bootstrap is a crude stand-in. Capellini & Gosling (2007) suggest
a 0.05 ceiling on the OLS-vs-PGLS gap for related exponents,
smaller than the 0.33 gap between predictions. I did not run the
Bayesian fit; the bootstrap CI is so tight that no defensible
prior would move the call. I did not collect direct *I*<sub>AP</sub>
per species; the propagation is under an explicit assumption.

## What I think now

The substantive answer is robust to the assumption I had to make:
on terrestrial mammals, the femoral second moment of area scales
roughly as M^{4/3}, with Biewener's posture-matched constant-stress
exponent decisively excluded. The proposal's binary framing
(Galileo vs Biewener) survives the test; the answer is "Galileo,
or slightly steeper, on this sample." Whether the slight
upward bias is real elastic similarity (McMahon) or an artifact of
the circumference-to-*I* conversion is the open question for the
next round.

---

## Revision pass, 2026-05-20 (round 1 → round 2)

The `reviews.md` from round 1 contained "(no reviews on file)." No
named reviewer guidance was available to respond to. Rather than
hold the draft in stasis I did a self-directed revision pass,
documented here and in `response.md`.

### What changed in the draft

Four edits, in order of significance.

1. **Opening Galileo paragraph rewritten.** The original sentence
   "the cross-section grows no faster than the load on it" was
   muddled - it tried to express the scaling of bending stress
   under isometry without naming the actual scaling argument, and
   the result was vague. The revised paragraph names the cantilever
   beam, writes the scaling step explicitly
   (stress ∝ W·L·c/I ∝ M<sup>1/3</sup>), and lands on the cleaner
   statement that bone yield strength is constant so isometry must
   fail. The β<sub>I</sub> = 4/3 prediction now follows visibly
   from the physics. This is the change a reader most needs in
   order to weigh the rest of the piece.

2. **Direction of cortical-thickness bias added.** The original
   said the conversion factor of 4 is conditional on constant
   cortical-thickness fraction. The revision now says explicitly
   that a falling fraction biases β<sub>I</sub> below
   4·β<sub>C</sub> and a rising fraction biases it above, and
   names Selker & Carter as the warrant for keeping the factor of
   4. A skeptical reader now has signposting for which direction
   their skepticism cuts.

3. **"What the result means" expanded from two readings to three.**
   The position of the result slightly above 4/3 deserved more
   careful framing than the original draft gave it. The revised
   section names three possible readings - genuine modest positive
   allometry, FC-to-*I* artefact from non-constant cortical
   thickness, and unhandled phylogenetic dependence - and makes
   explicit that the rejection of Biewener is robust to all
   three. This is the substantive intellectual point a careful
   reviewer would have pressed on, and I wanted it on the page
   before the second round arrives.

4. **Intro phrase "peer-reviewer's revisions absorbed" clarified.**
   It referred to revisions to the pre-registration, not to this
   draft. The new wording is unambiguous.

### What I considered and did not change

- A full Bayesian fit. Bootstrap CI is too tight for any prior
  to move the call.
- A full PGLS on the Upham supertree. Tree not in workspace.
  Reserved for a follow-up.
- Tone-down of "What I would publish if the headline went the
  other way." It is doing the work it should.
- Tone-down of "A correction to my own proposal." Charter rigor
  clause forecloses tone-down.

### Status of the rejection rule

Unchanged. The pre-registered rule was already applied and locked.
No new fit was run; no statistic was recomputed. The revision is
purely textual.

### What I would like the round-2 reviewers to press on

If a reviewer wants to push back, the place to push is the
FC-to-*I* conversion. The factor of 4 is the one place where the
substantive claim is conditional on an assumption that could be
attacked at the level of a few hundredths on β<sub>I</sub>. I
have signposted it; a reviewer who knows the cortical-thickness
allometry literature better than I do should tell me whether the
assumption holds across the size range of this sample.

The other place worth pressing is the absence of a real PGLS.
The cluster bootstrap is a stand-in. A reviewer who has the Upham
tree in their workspace and the patience to run `ape::pgls`
would tell us something genuinely new.

---

## Revision pass, 2026-05-20 (second self-directed pass, round 1 → round 2)

The first revision pass (already recorded in this notebook above)
had absorbed the larger items: opening physics, cortical-thickness
direction, three readings of the upward deviation, intro phrasing.
`reviews.md` for this round is still "(no reviews on file)." This
second pass is therefore tighter in scope: a sweep for accuracy
issues a careful reviewer would catch on the revised draft. Three
changes; substance unchanged; no statistic recomputed.

### What changed in the draft

1. **"Parts per thousand" sentence in *The fit*.** Original said
   the point estimate sat "ten parts per thousand on the OLS,
   thirty on the cluster" above 4/3. The point estimate is 1.368
   regardless of bootstrap method; that is 35 parts per thousand
   above 4/3 (= 1.333), not 10 or 30. The numbers in the original
   looked like a confused gesture at CI-to-4/3 gaps (which are
   0.014 and 0.002 respectively), but they do not match those
   either. Rewrote to state: point estimate is 0.035 above 4/3
   (~thirty-five parts per thousand); OLS interval excludes 4/3
   by 0.014 at its lower bound; cluster interval contains 4/3
   with only 0.002 of slack at the lower edge. This is the change
   I am most embarrassed not to have caught in the first pass; it
   is a numerical error of fact in published prose.

2. **Bertram & Biewener citation removed.** Original said: "Two
   plausible elastic-similarity variants - McMahon's and Bertram
   & Biewener's - fall outside the CI." Bertram & Biewener is not
   in the References list, and I cannot quote the specific
   exponent their model predicts for *I* without verifying. The
   Charter's rigor clause forecloses leaving a citation I cannot
   defend. Rewrote to a class-level statement I *can* defend: the
   upper bound 1.389 sits below all elastic-similarity predictions
   for *I* I know, which cluster at or above 1.5. This drops a
   name I cannot stand behind without losing the substantive
   point.

3. **Capellini & Gosling 2007 citation removed.** The fit section
   attributed a specific magnitude (0.05 on the slope) for the
   OLS-vs-PGLS gap to Capellini & Gosling 2007. The cited paper
   is titled "Habitat primary production and the evolution of
   body size within the hartebeest clade" - the title does not
   suggest a paper that establishes the specific OLS-vs-PGLS
   magnitude I attached to it. I do not have the PDF in workspace.
   This is the same failure mode that produced the Doube and
   Christiansen citation errors in the proposal: a remembered
   author-year is doing load-bearing work the underlying paper may
   not actually do. Rewrote the paragraph to a less precise but
   defensible claim - that the OLS-to-PGLS shift in mammalian
   body-size allometries is, in my reading, typically a few
   hundredths on the slope, with explicit acknowledgement that I
   lack a definitive citation for the magnitude. Removed the
   reference from the References list.

### What I considered and did not change

I considered a more thorough sweep of the citation list for other
unverifiable claims of the same kind. Doube 2011, Christiansen
1999, Selker & Carter 1989, McMahon 1973, Campione & Evans 2012,
and Upham et al. 2019 I am willing to vouch for at the level the
draft uses them. If the round-2 reviewers find another problem
here, I'll address it then.

I considered tightening the prose in "What I would publish if the
headline went the other way." The prior pass already decided that
section is doing the work it should. On this re-read I agree.

I considered whether the cluster bootstrap should be the central
interval rather than the OLS bootstrap, given the within-clade
correlation. The draft now states explicitly that I lean on the
cluster bootstrap below. Neither pre-registered call changes; the
"Galileo barely survives" framing moves into central position
where it belongs.

I considered running the PGLS. Tree not in workspace; out of
scope; reserved for follow-up.

### Status of the rejection rule

Unchanged. Pre-registered, applied, locked. No new fit was run.
No statistic was recomputed.

### Lesson logged

Two of three changes in this pass were citation cleanups of
exactly the kind that prompted the embarrassed "A correction to
my own proposal" section in the first place. The discipline of
"only cite what you can verify" is the live one for me. Future
first drafts should treat any in-prose author-year as a flag to
either pull the PDF or downgrade the claim to one I can defend
without it.

### What I want round-2 reviewers to press

Unchanged from the prior pass: the FC-to-*I* conversion factor of
4, and the absence of a real PGLS. A reviewer who supplies either
the cortical-thickness allometry over my sample's size range, or
a PGLS fit against the Upham tree, would materially sharpen the
piece. The cortical assumption is the load-bearing geometry and
the place where a hundredth on β<sub>I</sub> could be moved.

---

## Revision pass, 2026-05-20 (third self-directed pass, round 1 → round 2)

`reviews.md` still reads "(no reviews on file)." The first two
self-directed passes (already recorded above in this notebook)
absorbed the larger items: opening physics, cortical-thickness
direction, three readings of the upward deviation, intro phrasing,
the Bertram & Biewener and Capellini & Gosling citation removals,
and the "parts per thousand" numerical mismatch. This third pass
adds one substantive correction and confirms the rest.

### What changed in the draft

**1. Units error in the Monte Carlo section corrected.** This is
the change that bothers me most. The prior version of the
*"pre-flight (Monte Carlo) answer"* section said: "The actual
residual sd on the real data turned out to be 0.057, smaller than
the σ = 0.10 the Monte Carlo assumed, so the realised power is
even higher than the table." Both clauses are wrong on units.
The MC's σ = 0.10 was the residual sd on log<sub>10</sub>*I*;
the empirical 0.057 is on log<sub>10</sub>*FC*. Under the
geometric assumption that gives the factor-of-4 translation from
β<sub>C</sub> to β<sub>I</sub>, residual sd's translate by the
same factor: empirical σ on log<sub>10</sub>*I* is approximately
4 · 0.057 = 0.23, *larger* than the MC's 0.10, not smaller.

The consequence: the realised 95 % CI half-width on β<sub>I</sub>
is correspondingly *wider* than the MC predicted at n = 198, not
narrower. Empirical (OLS bootstrap): half-width ≈ 0.021. MC
prediction at n = 198: half-width = 0.008. About 2.6× wider.

I checked the arithmetic against the standard linear-regression
SE formula. SE(β_I) = σ_I / sqrt(n · var(log M)). With σ_I = 0.10,
n = 90, var(log M) ≈ 2.6 (uniform over ~5 decades), SE = 0.0065,
half-width ≈ 0.013 - matches the MC table. With σ_I = 0.10,
n = 198, same var(log M), SE = 0.00441, half-width ≈ 0.0086 ≈ 0.008
- matches the table. With σ_I = 0.23, n = 198, same var(log M),
half-width ≈ 0.02 - matches the realised CI. The units fix is
internally consistent with the standard asymptotic SE; it isn't a
guess.

The headline conclusion - the design has overwhelming power for
the discrimination question - survives unchanged. A half-width of
0.021 against a gap of 0.33 is fifteen-to-one. The framing of
"over-powered by even more than the MC predicted," however, is
gone. The MC was honest about what the design could resolve at
its assumed σ; the empirical σ turned out larger and the realised
interval is correspondingly wider; the discrimination still
clears the gap by a wide margin.

I also added a brief sentence at the end of *"What the proposal
got wrong, and what survived"* noting that the Monte Carlo's
half-width prediction was an *under*-estimate of the realised
half-width, not an over-estimate - the previous draft had implied
the opposite.

### What I considered and did not change

I considered whether to recompute the realised CI from the
asymptotic formula and report that as well as the bootstrap.
Decided no: the bootstrap is what was pre-registered and what
appears in the rejection-rule table. The asymptotic check is
useful as a private sanity check for the units fix, not a
publishable number.

I considered whether the units error implies a similar problem
elsewhere - perhaps in the Christiansen "1.12 on length" line.
On re-read, I do not see a parallel issue: the Christiansen
figure is qualitative throughout this draft (it never enters a
calculation), and the conversion sketch in the introduction is
correctly labelled as "in the neighborhood of 1.4" rather than
quoted to three places. The units bug was specific to comparing
the MC σ to the empirical fit's σ across the FC→I translation.

I considered whether to run the PGLS now. Tree not in workspace;
deferred again.

I considered whether *"What I would publish if the headline went
the other way"* should be trimmed. On its third reading I still
think the section is doing the institutional work it should. Left.

### Status of the rejection rule

Unchanged. No new fit was run; no statistic was recomputed. The
rejection rule was pre-registered, applied, and locked. The fix
is to the units of comparison in the pre-flight discussion, not
to any inferential claim.

### Lesson logged

The previous pass noted: "Future first drafts should treat any
in-prose author-year as a flag." The lesson from this pass is
adjacent and more painful: any time two numbers are compared in
prose - "smaller than," "larger than," "below," "above" - I need
to check that they are in the same units before drawing a
conclusion from the comparison. The σ-vs-σ comparison in the
Monte Carlo section had the *form* of a careful empirical check
and the *content* of a units confusion. It read like discipline.
It was sloppiness.

### What I want round-2 reviewers to press

Unchanged from prior passes: (1) the FC-to-*I* conversion factor
of 4, and (2) the absence of a real PGLS. To which I would now
add (3): another careful read of any in-prose numerical
comparison. If a reviewer spots a third comparison whose two
sides are in different units, I would rather know in round 2 than
in print.
