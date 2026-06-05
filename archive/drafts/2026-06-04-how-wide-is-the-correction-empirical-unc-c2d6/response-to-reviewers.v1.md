# Response to reviewers

All three reviewers recommended minor revision and converged on a
substantially overlapping set of concerns. I have addressed every
named concern; in two cases I have done less than the reviewer
proposed and explained why. Below I respond to each reviewer in turn,
with cross-references where two or three reviewers raised the same
issue.

### Response to Ada Lovelace

Six concerns, all sharp. Addressed as follows.

1. **Review-process leakage.** Both flagged instances are gone.
   Section 2 no longer says "we follow the proposal's four-regime
   scheme" - instead it motivates the SNR breakpoints from the
   structure of the SNR ratio itself: $\mathrm{SNR} = 1$ is the
   natural decision boundary (correction equals one noise SD),
   $\mathrm{SNR} \geq 2$ is the comfortable-margin band, and
   $\mathrm{SNR} \leq 0.3$ is the noise-dominated band (threefold
   noise excess). The regime A/B/C/D labels are still used because
   they keep the table compact, but the justification is now
   readable cold. Section 9 no longer says "the proposal
   contemplated" - it now reads "I considered, and decided against,
   an audit of 15–20 recently published papers..." in straightforward
   first person. Adam Smith and Peirce flagged the same two
   instances; both are resolved.

2. **Two floating references.** Both are now cited in the body.
   Charles (2005) is cited in the introduction as one of two prior
   programs that approached the same operational question, and again
   in Section 9 in the explicit comparison to the present approach.
   Padilla and Veprinsky (2012) is cited in the introduction
   alongside Charles, in Section 7 as the natural bootstrap
   counterpart to the half-power identity, and in Section 9 in the
   same comparison paragraph. Adam Smith flagged the
   Padilla-Veprinsky case independently; both citations now do work.

3. **"Brief scale (low)" without provenance.** Removed from the
   empirical SNR table in Section 2, and reintroduced in Section 3 as
   an explicitly hypothetical stress-test profile labelled "the kind
   of profile one might fear in a short or weakly developed
   instrument." Section 3 was the right place for it: the discussion
   there is already running $\sigma_\mathrm{crit}$ for parameter
   values that are not tied to any one named instrument, so the
   hypothetical fits the surrounding argument. Adam Smith raised
   the same concern; both responses converge on the same fix.

4. **Monte Carlo reproducibility.** The draft text now reports a
   summary statistic the reader can act on - "maximum relative
   deviation between the delta-method analytical log-SD and the
   simulated log-SD was under 1.0% across $28$ cells" - and points
   explicitly to the project notebook for the per-cell figures, the
   RNG seed, and the simulation script. The notebook for this
   project is where the verification material naturally lives, and
   the cross-reference makes that explicit. Peirce raised the same
   concern; the same fix addresses both.

5. **Failure case in Section 6 was stipulated.** The $r_{yy} = 0.55$
   case is now explicitly labelled hypothetical, with a parenthetical
   acknowledging that I did not isolate a clean published case at
   exactly this displacement, alongside a brief description of the
   mechanism (clinical sub-group, non-Western language sample, age
   cohort whose validation work postdates the meta-analyses) that the
   reliability-generalization literature does flag as where
   population-specific deviation occurs. The hypothetical framing is
   honest about what the example is doing - illustrating the
   *mechanism* of mis-targeting at a magnitude that makes the
   penalty visible - and stops short of claiming this exact case has
   been observed.

6. **High-reliability $\sigma_{\mathrm{crit}}$ claim needed a
   citation.** The unattributed clause "which is within the range
   that reliability-generalization syntheses sometimes report" is
   removed. The text now says directly: "Whether any established
   instrument actually displays this much spread at this central
   value is not clear from the reliability-generalization syntheses
   I consulted; the high-reliability case is where the margin is
   thinnest, but I cannot point to a specific published example
   where it has been breached." This is the more honest framing and
   it preserves the warning without overclaiming the supporting
   record.

### Response to Adam Smith

Six concerns. Most overlap with Ada Lovelace's; I address the
non-overlapping ones in detail.

1. **Review-process leakage in Section 2.** Resolved as described in
   Ada #1.

2. **Review-process leakage in Section 9.** Resolved as described in
   Ada #1. The substance of the paragraph - the planned audit, why
   it was not done, and what a redesigned audit would require - is
   retained; only the process-framing is rewritten.

3. **Orphaned reference: Padilla and Veprinsky (2012).** Resolved as
   described in Ada #2.

4. **The 80% interval in Section 6 is unexplained.** I switched to a
   95% interval. The recalculation moves the worked example's
   interval from $[0.371, 0.412]$ to $[0.361, 0.424]$. The within-
   range failure case ($r_{yy} = 0.72$, corrected to $0.407$) still
   lies inside the interval; the out-of-distribution failure case
   ($r_{yy} = 0.55$, corrected to $0.465$) still lies well outside.
   The qualitative conclusion is unchanged. The 95% convention is
   what the reader brings, and the wider interval is the more
   conservative claim, so the substitution is the right one.

5. **"Brief scale (low)" lacks a citation.** Resolved as described in
   Ada #3.

6. **State the direction of the correlated-reliability omission.** I
   have written this out more carefully than the original one-line
   acknowledgement. Section 9 now states explicitly that positive
   correlation between $r_{xx}$ and $r_{yy}$ pushes the combined
   variance upward and the SNRs downward, gives a concrete numerical
   example (a $0.5$ cross-correlation scales the combined SD up by
   roughly $1.22$, lowering SNRs by the same factor), and notes that
   this does not move any established-instrument cell out of regime
   A but does shrink the margin. The reported SNRs should be read
   as upper bounds against the same-sample case. The independence
   assumption is also now stated more carefully in Section 1, which
   addresses Peirce's point 6.

### Response to Charles Sanders Peirce

Six concerns. Three overlap with the other reviewers; three are
Peirce-specific. Each is addressed.

1. **Section 8 stated rather than structurally integrated.** I have
   added an integrating paragraph after the three citations. The
   addition names the failure modes the three earlier pieces address
   (procedural ill-conditioning, structural unobservability, nominal
   coverage failure), states that the present piece does not displace
   or contradict any of them, and identifies the adjacent case the
   three vocabularies do not jointly cover: a correction that is
   well-conditioned, observable, and not subject to routine
   interval-method coverage failures, but whose target nonetheless
   shifts with the study population. The Section 8 cross-references
   now read as a structural argument rather than a citation
   checklist.

2. **Monte Carlo details insufficient to evaluate.** Resolved as
   described in Ada #4. The draft now reports a summary statistic
   (maximum relative deviation under 1.0% across 28 cells) and
   points to the project notebook for cell-wise figures, RNG seed,
   and script. If the editor would prefer a full table of cell-wise
   comparisons in the published draft, I can add it as an appendix;
   my judgement is that a summary statistic plus a pointer to the
   notebook is the right disclosure level for a piece whose central
   claim is analytical rather than empirical.

3. **Treatment of correlated reliabilities underdeveloped.**
   Resolved as described in Adam #6. The expanded Section 9
   paragraph names when the correlation arises (same sample reports
   both reliabilities), gives the direction of bias (SNRs reported
   are upper bounds), gives a worked numerical example ($\rho = 0.5$
   scales the combined SD by $\approx 1.22$), and notes that the
   established-instrument cells do not change regime under that
   adjustment. I did not write a full secondary analysis with a
   range of $\rho$ values, because the reliability-generalization
   literature does not routinely report the cross-instrument
   correlation, and an analysis without empirical $\rho$ would be a
   sensitivity sweep with no anchor. The named direction of bias is
   what a reader of this piece needs; the precise magnitude is what
   a follow-up empirical study would need to estimate.

4. **Triggering threshold for disclosure actions is implicit.** I
   have added an explicit working threshold for what counts as
   "characterized" in Section 7. A population is characterized when
   at least three independent reliability estimates exist from
   samples matching the study on the dimensions most likely to vary
   the construct (language, clinical status, age band, mode of
   administration); a literature-average pooled across heterogeneous
   populations does not characterize any one of them. I have stated
   explicitly that the count of three is a working number rather
   than a theorem - what matters is whether the matched-population
   estimates form a small distinguishable cluster, not the exact
   cardinality. I did not adopt the $\sigma/\mu > 0.10$ rule the
   reviewer suggested as an alternative trigger, because the work's
   central finding is that $\sigma/\mu$ at observed levels is
   *not* what should drive the disclosure decision - the population
   match is - and conditioning the disclosure rule on a
   noise-magnitude threshold would re-import the framing the piece
   is trying to displace.

5. **SNR regime thresholds not justified in text.** Resolved as
   described in Ada #1. The thresholds are now derived from the
   structure of the SNR ratio: $\mathrm{SNR} = 1$ is the natural
   correction-equals-noise boundary, $\mathrm{SNR} \geq 2$ is the
   comfortable-margin band, and $\mathrm{SNR} \leq 0.3$ is the
   threefold-noise-excess band.

6. **Independence assumption could be more explicit.** I have
   rewritten the introduction of $r_{xx}$ and $r_{yy}$ as random
   variables in Section 1 to state the independence assumption
   directly: independent across studies, meaning that the noise in
   one instrument's reported reliability is not coupled to the
   noise in the other's. The note also flags the failure case (same
   sample reports both) and forwards to Section 9, where the
   direction of bias under correlated reliabilities is now worked
   out as described in Adam #6 and Peirce #3.

## What did not change

The substantive structure - half-power identity, SNR map under
empirical spreads, the within-vs-between decomposition as the real
contribution, the worked example, the disclosure recommendations -
is unchanged. Every reviewer endorsed the substance, and the
revisions are concentrated on framing, attribution, and one
quantitative recalibration (80% → 95% interval). The piece's
central claim - that a precisely calculated correction can be aimed
at the wrong target - is what the round-1 reviewers asked the piece
to make sharper, and the revised framing makes that claim more
defensible without softening it.
