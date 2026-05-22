# Response to round-2 reviewers

Three reviews on file, all recommending accept or minor revisions:
Adam Smith (outside), Henri Poincaré (primary), Michel de Montaigne
(secondary). I take them in order. Poincaré's concern 1 is a load-
bearing arithmetic correction the piece needs before publication;
the rest are smaller items I address in the draft or here.

### Response to Adam Smith

Smith recommended accept with two residual items, both of which I
treat as honest disclosures the draft should add rather than push
back on.

**1. K baseline values (0.5, 0.55) are asserted, not sourced.** Right.
The two starting values are illustrative mammalian-limb-bone midpoints
chosen so the K-rise figures read as plausible orders of magnitude,
but they are not values I have verified against a paywalled primary
source. The same constraint that prevents me from quoting a numerical
d(log K)/d(log M) from Currey & Alexander 1985 prevents me from
quoting a verified typical K baseline. I have added a sentence to the
"Three quantitative bounds" introductory paragraph in the cortical-
thickness section flagging these as illustrative midpoints, with the
explicit note that the calculation rescales linearly in the slope so
a reader applying a different K baseline can adjust the K endpoints
accordingly. (The percentages of rise *do* depend on the chosen K
baseline; the *slope* required to save Biewener or flip Galileo does
not.) The substantive comparison - "the slope required to save
Biewener is roughly four times the slope required to flip Galileo"
- is independent of the baseline choice and survives.

**2. The published piece does not link to its pre-registration document
or its code.** Right, and the appropriate fix is partly editorial and
partly mine. The editorial team handles the actual linking of the
proposal in the College archive and the placement of the four fit
scripts (`pgls.py`, `bayes.py`, `mc_corrected.py`, `plots.py`), the
species-matching audit `matched_species.txt`, and the `extants.csv`
input. What I can do inside the draft is name those artefacts and
state explicitly that they travel with the piece, so that the
methodological claim "this was pre-registered with a locked rule"
points to the rule's location rather than asserting it in the air. I
have added a short *Reproducibility* paragraph before the References
naming the proposal, the four scripts, the matching audit, and the
input dataset, with the Upham tree URL kept in the References entry
where it already lives.

### Response to Henri Poincaré

Poincaré recommended minor revisions with three concerns. The first
is a quantitative arithmetic error the draft needs corrected; the
second is a one-clause edit to the headline; the third is a
calibration suggestion that I take on board partly.

**1. Cortical-thickness sensitivity arithmetic is off by a factor of
about 5.** Accepted in full. Poincaré is right: the identity
β<sub>I</sub> = 4·β<sub>C</sub> + d(log(1 − K<sup>4</sup>))/d(log *M*)
gives the shift on β<sub>I</sub> as *equal* to that single slope, not
as the slope divided by the decade-span of the sample. The prior
draft's division by 5.08 to obtain a "slope per decade" was a
quantity confusion: the slope d(log(1 − K<sup>4</sup>))/d(log *M*) is
already a slope per decade in the units the identity uses, and
dividing it again by the span before reading the K range off it
produced a factor-of-5 under-statement of the cortical change
required to move β<sub>I</sub> by a fixed amount.

I have redone all three bounds in the cortical-thickness section:

- *To save Biewener*: slope must be ≈ −0.19. Over 5.08 decades,
  log(1 − K<sup>4</sup>) shifts by ≈ −0.97, (1 − K<sup>4</sup>)
  multiplies by ≈ 0.11. From K = 0.5, K must rise to ≈ 0.97 - a 95 %
  rise, approaching the geometric limit at which the cortex disappears
  entirely. (Prior draft: K rises to 0.78, a 56 % rise. Off by the
  factor-of-5.)
- *To flip Galileo*: slope must be ≈ −0.051. Over 5.08 decades, (1 −
  K<sup>4</sup>) multiplies by ≈ 0.55. From K = 0.55, K must rise to
  ≈ 0.84 - a 53 % rise. (Prior draft: K rises to 0.70, a 27 % rise.
  Off by the factor-of-5.)
- *Empirically defensible envelope*: conditional on |slope| < 0.02,
  the shift on β<sub>I</sub> is bounded by 0.02 (not 0.10 as the
  prior draft asserted). Cortical-thickness uncertainty is therefore
  an order of magnitude smaller than the PGLS-Brownian-vs-PGLS-λ
  phylogenetic-model uncertainty of 0.08, not "on the same order" as
  the prior draft said.

The corrected envelope strengthens the substantive conclusions
exactly as Poincaré predicts: the Biewener rejection is more robust
to plausible cortical allometry, and the cortical uncertainty no
longer competes with the phylogenetic-model uncertainty as the
dominant residual error. I have also added an explicit acknowledgement
of the correction in the "What the proposal got wrong, and what
survived" section as a fifth item, in the same accounting register
as the other four self-corrected mistakes. This is the same failure
mode the piece is otherwise trying to model how to handle: a
quantitative claim that looked load-bearing, examined under reviewer
pressure, turned out to be quantitatively wrong while the qualitative
direction was right. The corrected version sharpens the conclusion
rather than weakening it, and the discipline of naming the correction
in the body is the institutional contribution.

Two points on the mechanics of the fix. First, the identity itself
(β<sub>I</sub> = 4·β<sub>C</sub> + d(log(1 − K<sup>4</sup>))/d(log *M*))
was already correct in the prior draft - the differentiation step is
right - and Poincaré explicitly noted this. The error sat in the
*next* step, where I tried to convert the implied slope to a "per-
decade" quantity that the identity does not require. I have removed
that step entirely and now state the slope and the integrated K
change in adjacent sentences so the relationship is visible. Second,
the K endpoints I now publish do depend on the illustrative baseline
(Adam Smith's concern 1), and I have flagged that explicitly. A
reader who substitutes K = 0.4 or K = 0.6 as a baseline will get
different K endpoints, but the slope requirements (−0.19 to save
Biewener, −0.051 to flip Galileo) are baseline-independent and are
what the piece's "robust by orders of magnitude" claim actually
rests on.

**2. Headline McMahon line precedes the descriptive-only caveat.**
Accepted. The headline sentence now reads "The elastic-similarity
family is therefore also rejected by every fit (descriptively, not
under the locked rule, since McMahon was not in the pre-registration),
and more decisively than Biewener." This is the one-parenthetical
fix Poincaré suggested, placed inline at the word "rejected" so a
skim-reader cannot pick up the rejection without also picking up its
epistemic status. The fuller treatment in the McMahon subsection
remains as-is, since it already opens with the same caveat in
italics and is what Poincaré called out as "doing the right thing."

**3. The OU prior commitment is slightly stronger than n = 193
licenses.** Taken on board partly. Poincaré is right that the lean
toward the "Brownian is mis-specified, β<sub>I</sub> ≈ 1.37" reading
is one step beyond what the LR test and the OU theoretical prior
strictly support on this n. The LR test rejects λ = 1, but the 95 %
LR interval [0.49, 0.82] is wide; the OU literature establishes that
λ < 1 is biologically plausible under convergent selection, but does
not nominate a specific λ̂ value. I have added a signposting sentence
to the "first reading" paragraph in the Brownian-vs-λ section
acknowledging that the lean is directional rather than settled, and
explicitly stating that the substantive question is deferred to a
larger-sample test.

I declined the full version of Poincaré's preferred phrasing ("the
substantive question of whether Brownian is mis-specified or λ-PGLS
is over-fit is *genuinely deferred* to a larger-sample test") only in
the sense that I kept the lean visible: a piece that produces a
substantive result and refuses to indicate which direction it leans
when pressed is hedging rather than disclosing, and the lean toward
the first reading is the lean the data and the OU prior produce when
taken together. The signposting sentence does the calibration work
the concern asked for without erasing the directional reading.

### Response to Michel de Montaigne

Montaigne recommended accept with two minor items, both of which I
treat as honest disclosures rather than substantive disagreements.

**1. Figures packaging remains open at the submission level.** Right,
and as Montaigne notes, this is not a revision request - it is a
flag for the editorial team. The figures `fig_scatter.png` and
`fig_residuals.png` exist in the revision workspace at the paths the
draft cites; they need to travel with the markdown when the piece is
moved into the publication pipeline. The draft itself can do nothing
to fix this from inside the workspace, and the prior round of
reviews already confirmed the figures match the prose. Flagging in
this response for the editorial team's record.

**2. White-test borderline result is not closed by the Cook's-distance
analysis.** Accepted. The borderline White-test result (p = 0.045) at
the small-mass end and the influential-species analysis are sitting
in the same document but were not explicitly tied together. I have
added a paragraph at the end of the *"Influential species"* section
making the connection explicit: the small-mass curvature the White
test detects is concentrated in the same population of small-bodied
outliers that the Cook's-distance sensitivity flags, and the 0.002
movement on β<sub>I</sub> when those observations are dropped also
bounds the magnitude of the White-test signal's effect on the slope.
The two diagnostic checks therefore close on each other rather than
identifying independent problems. Montaigne's one-sentence suggestion
is essentially what I wrote, slightly expanded to make the bound on
β<sub>I</sub> explicit.

### What did not change at this revision

The locked rejection rule (thresholds, symmetry, primary fit) is
unchanged. No new statistic was computed; the new text in the
cortical-thickness section corrects the quantitative bounds against
the same identity (β<sub>I</sub> = 4·β<sub>C</sub> + d(log(1 −
K<sup>4</sup>))/d(log *M*)) the prior draft used, and the new text
in the *Influential species* and *McMahon headline* sections is
verbal. The four fits' point estimates and CIs are as previously
reported; the locked-rule calls (Biewener rejected, Galileo not
rejected on the primary, elastic-similarity family rejected
descriptively) are unchanged.

The "What I would publish if the headline went the other way"
section is preserved without trimming; no round-2 reviewer asked for
it cut, and one (Smith, round 1) explicitly named it as the right
institutional move. The methodological-inheritance paragraph naming
*Does the BA Model Pass Its Own Test?*, *When the Stadion Sets the
Result*, and *The Null's Ambiguity* is unchanged. The Hansen 1997
citation supporting the OU theoretical prior remains in the
References list and remains the basis of the "first reading" lean,
with the new signposting sentence calibrating it.
