# Response to round-2 reviewers

All three reviewers recommend publication (Lovelace: accept;
Smith: minor; Peirce: accept). The substantive arguments of the
piece - the half-power identity, the SNR map, the within-vs-between
variance decomposition, the worked example, and the three disclosure
rules - survive round 2 with no challenge to their substance. The
concerns below are addressed point-by-point. Four lead to changes in
the draft; four I respectfully decline, with reasoning.

### Response to Ada Lovelace

Lovelace recommends accept. Three observations were offered for the
editorial record.

**Observation 1: The notebook reference is unnamed.** Section 2 points
the reader to "the project notebook for this piece" without a path or
slug. I have left this phrasing unchanged. The College's lab notebooks
are archived under each piece's slug in a fixed location
(`lab-notebooks/<slug>/`), and a reader following the cross-reference
convention used elsewhere in the archive can locate the notebook from
the published piece's URL alone. Adding a path inside the prose
would either duplicate that convention or introduce a path that is
fragile against the archive's directory layout. The reviewer
explicitly flagged this as an observation rather than a blocker, and
the critical verification material (28 cells, max deviation below
$1.0\%$, RNG seed and script exist) is named in the body.

**Observation 2: The 95% interval's distributional assumption.**
Addressed. Section 6 now states explicitly that the interval is
constructed in log-space by exponentiating $\ln(0.391) \pm 1.96
\times 0.041$, and notes that under the log-normal back-transformation
the bounds are slightly asymmetric about the central estimate. This
is a one-sentence addition that closes the reproducibility question.
The numerical bounds $[0.361,\, 0.424]$ are unchanged.

**Observation 3: No review-process leakage.** Confirmed. No
revisions in this pass introduce process narration; the
heterogeneity-vs-noise reconciliation paragraph I added to Section 5
argues the point on its merits without referencing the prompt.

### Response to Adam Smith

Smith recommends minor revisions and raises one quantitative concern.

**Concern 1: The $n = 300$ transitional claim is off.** Addressed.
Smith is correct: by the Feldt formula the piece itself states, with
$k = 9$ and $\alpha = 0.86$, the within-study SD at $n = 300$ is
$\sqrt{2 \times 9 \times (0.14)^2 / (8 \times 299)} \approx 0.0122$,
giving a within-variance fraction of $(0.0122)^2 / (0.025)^2 \approx
24\%$, not "roughly half." The crossover where within-study sampling
variance falls below half of the reported total sits around $n \approx
140$, consistent with the table's other entries ($n = 100$: $70.6\%$;
$n = 200$: $35.5\%$).

I have replaced the bad sentence with a more careful statement that
reads from the table rather than interpolating mid-stream: "The
crossover where within-study sampling variance falls below half of
the reported total occurs around $n \approx 140$: at $n = 100$
sampling alone accounts for roughly $70\%$ of the variance, at $n =
200$ for about a third, and at $n \geq 1000$ for under one quarter."
Smith is right that the main conclusion (between-population
heterogeneity dominates at large $n$) is unaffected; the fix is one
sentence and it makes the transition through the table consistent
with the table's own numbers.

### Response to Charles Sanders Peirce

Peirce recommends accept and offers five observations. One leads to a
substantive change in Section 9; one leads to a substantive change in
Section 5; three I decline with reasoning.

**Concern 1: The $\rho = 0.5$ regime-stability claim is contingent on
an unanchored $\rho$.** Addressed by widening to a sensitivity range.
Peirce is right that the round-2 draft's structure - "under that
adjustment" earlier in the paragraph, then an unqualified "the
established-instrument cells do not change regime" at the end -
invited the reader to take the regime stability as more robust than a
single point value warrants. The revised Section 9 now reports the
scaling factor across $\rho \in [0.3,\, 0.7]$ (giving $\sqrt{1+\rho}
\in [1.14,\, 1.30]$), applies the worst-case scaling to the table's
smallest SNR ($3.65 \to 2.81$), and states explicitly that the regime
finding is robust within this range, with an explicit forward-pointer
to re-reading the table if a future synthesis reports $\rho$ outside
it. This is the (a) option Peirce proposed and is the more honest
formulation.

**Concern 2: The three-population rule may be too strict or too
lenient depending on $\sigma$; should it be conditioned on $\sigma /
\mu$ or on regime-map position?** I respectfully decline. The reason
is the same one I gave for declining a $\sigma / \mu > 0.10$ trigger
in round 1: the central claim of the piece is that population mismatch,
not noise magnitude, should drive disclosure. Conditioning the rule
on $\sigma/\mu$ or on regime-map position re-imports the
noise-magnitude framing the piece is displacing. A high-SNR instrument
with three matched-population estimates is "characterized" in the
relevant sense; a high-SNR instrument with zero matched-population
estimates is not, regardless of how tight the literature average is.
The rule is about whether the practitioner has population-relevant
information, not about the spread of pooled literature values.

I acknowledge Peirce's point that "three" is somewhat arbitrary - the
draft says so explicitly ("three is a working number, not a theorem;
the requirement is that the matched-population estimates exist as a
small distinguishable cluster, not that they exist in a canonical
count"). The candor about "working number" is the correct level of
qualification; a more elaborate noise-conditioned rule would feel
more principled while smuggling back the very framing the piece is
arguing against.

**Concern 3: A worked example applying the three-population rule to a
real instrument with incomplete literature coverage would strengthen
the operationalizability claim.** I respectfully decline. The
application is mechanical: a practitioner consults the same reference
the central estimate was drawn from, asks whether at least three
component studies in that meta-analysis match the study sample on
language, clinical status, age band, and mode of administration, and
either has the cluster or does not. Walking through an example with
a named instrument would require either (a) using an instrument I
have not directly audited (which would violate the same provenance
standard the piece is arguing for) or (b) auditing one in detail,
which is the redesigned-audit step explicitly deferred in Section 9.
Section 7's existing formulation - "from the same sources used to
choose the plugged-in value" - is the correct operational pointer
without overclaiming a worked audit.

**Concern 4: Is the SNR $\geq 3.5$ result robust to the heterogeneity
interpretation, or specific to the noise-around-a-true-value case?**
Addressed. Peirce is right that the round-2 draft did not state this
explicitly; the closest sentence ("The map's signal-dominated verdict
applies inside that assumption") was a flag, not a treatment. I have
added a paragraph to Section 5 that:

- States that the SNR arithmetic is robust to interpretation (the same
  $\sigma$ propagates through the same delta-method formula);
- States that the meaning shifts: under the noise reading, SNR
  measures signal against estimation uncertainty in one true
  $r_{xx}$; under the heterogeneity reading, it measures signal
  against the spread of corrected values under different draws of
  reliability from different populations;
- Notes that the first kind of uncertainty is reducible by larger
  samples, while the second is not, because there is no single
  $r_{xx}$ to estimate better;
- Concludes that a high SNR under the heterogeneity reading does not
  certify any one $\hat{r}_{true}$ as the right corrected value for
  any one population.

This is the explicit reconciliation Peirce asked for, and it sharpens
rather than weakens the piece's central distinction.

**Concern 5: The "brief scale (low)" stress test is illustrative
rather than empirically anchored; does such a profile exist in the
reliability-generalization literature?** I respectfully decline to
add an empirical search. The stress test is *intended* to be
hypothetical - that is its function in Section 3, which is exploring
the parametric structure of $\sigma_{\mathrm{crit}}(\mu)$ at values
not tied to any one named instrument. The text already names it as
"the kind of profile one might fear in a short or weakly developed
instrument," which I take to be the right epistemic posture: a
hypothetical case at the low-reliability boundary, used to show that
even there the SNR stays above 1, with the empirical question of
whether real instruments live in that region deferred to the audit
discussion in Section 9. The piece does not claim that $\mu = 0.70,\
\sigma = 0.08$ is observed; it claims that even *if* it were
observed, the SNR would remain above 4. Adding a search for whether
such instruments exist would change the example's role from "stress
test at a known parametric point" to "claim about empirical
distribution," which is not what the example is for.
