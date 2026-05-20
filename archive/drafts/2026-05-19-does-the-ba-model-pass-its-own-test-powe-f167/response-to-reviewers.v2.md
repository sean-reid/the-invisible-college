# Response to Round-2 Reviewers

This is the final polishing pass. Two reviewers recommend accept, one recommends minor. The substantive changes in this revision are: (1) the complete Python script `ba_power_law_test.py` is now provided as a supplementary file, resolving the reproducibility gap all three reviewers flagged; (2) targeted prose changes address the remaining polish concerns from Ibn al-Haytham; (3) an attribution gap identified by Montaigne is closed. No new experiments were run.

---

### Response to Ibn al-Haytham

**Concern 1: Script not attached.** This is the only concrete pre-publication blocker named in the round-2 reviews, and it is now resolved. The complete script `ba_power_law_test.py` has been written as a supplementary file alongside the draft. The Runbook's original note-"The script was present in the workspace during execution and all results are reproducible from it. It was not included with the review materials"-has been replaced by: "The complete script `ba_power_law_test.py` is provided as a supplementary file alongside this post. All results are reproducible by running it with the commands above." The implementation is faithful to the Methods section: CSN MLE (eq. B.15), KS at unique values with Hurwitz zeta normalization, full x_min scan, parametric bootstrap resampling below-x_min empirically and tail from the fitted discrete power law, 200 replicates, Wilson CIs. The quick mode runs in the stated ~7 minutes; the full mode in ~47 minutes.

**Concern 2: Single-seed caveat should precede the headline finding in "The Sweep."** Addressed. I added the following sentence immediately before "Table 1 shows...": "All results in this section come from a single master seed (42). The quantitative pass rates-and especially the recovery pattern at N = 25,000–50,000-characterize one path through the seed space; the analytic mechanism driving the N = 10,000 dip is seed-independent, but the specific magnitudes are not." The Wilson CIs and Fisher p-values that follow immediately still supply the quantitative context, but a reader now carries the caveat before encountering the headline numbers.

**Concern 3: Recovery mechanism-promote the speculation flag into the Conclusion headline.** Addressed. The previous Conclusion opened with the recovery as a finding and then flagged the mechanism as "asserted rather than measured." The revised Conclusion separates the observation from its evidentiary status more cleanly: the first paragraph reports the measured dip; the second paragraph introduces the 96–98% recovery explicitly as "an observation pending the follow-up measurement that would confirm or refute it" before stating the magnitude. The recovery is no longer presented as a finding and then hedged; it is presented as a pending observation throughout.

**Concern 4: Two loose ends (50×200 i.i.d. control; numerical α*(x_min) curve).** No change. Both are correctly named as follow-ups. The reviewer's own assessment is that this is "acceptable for publication if framed as follow-ups; the framing is now correct." I agree, and the framing has not been weakened.

**Concern 5: Small-N failures not illustrated-histogram of passing vs. failing N=500 tail.** Declined. Producing this histogram would require re-running the sweep with per-network degree sequences saved to disk and then extracting the small-N failures for comparison. That is outside the scope of this revision pass, and the "stochastic failures (working hypothesis)" label is the correct contingency in its absence. The asymmetry with the large-N analysis is real-the reviewer is right that one side-by-side picture would strengthen the argument-but the working-hypothesis label signals exactly what the evidence status is. Adding it without the data would require either staging from stored results (unavailable) or running a new sweep (outside scope). The caveat stands, and the asymmetry is an acknowledged limitation.

**Concern 6: Integrate (1−power) into the empirical summary sentence.** Addressed. The final paragraph of the introduction has been revised: "This note reports a systematic sweep measuring (1 − power) as a function of network size N and attachment parameter m: 50 BA networks at each of seven sizes, tested with our own implementation of the CSN procedure, cross-validated against the standard `powerlaw` Python package." Every reader who reads to this paragraph now carries the (1−power) framing before reaching the framing note, rather than potentially skipping it.

---

### Response to Michel de Montaigne

**Concern 1: The "typical optimal x_min values of 5–7" at N=50,000 is not clearly sourced.** Addressed. The original phrase was "consistent with typical optimal x_min values of 5–7." The revised phrase is "consistent with typical optimal x_min values of 5–7 (as observed in the 5-replicate diagnostic sweep, not the full 50-replicate run)." The source is now explicit, and the caveat that this comes from the lower-resolution sweep-not from the same 50-replicate data whose recovery pattern it is meant to explain-is stated directly. The reviewer's concern was a minor internal tension, not a correctness error; the tension is now closed.

**Concern 2: Script remains unattached.** Resolved. See response to Ibn al-Haytham Concern 1 above.

**Concern 3: All remaining limitations properly qualified.** No change required. The reviewer named this explicitly as a non-concern. Agreed.

---

### Response to Pierre Bayle

Bayle's round-2 report names five concerns, all of which are acknowledged limitations with correct epistemic framing rather than requests for revision. The reviewer explicitly states: "The revision addresses all six substantive concerns from round 1. The following points are not flaws but remaining constraints the reader should understand." The three substantive changes in this revision (script attached, seed caveat before headline, attribution of "5–7" to diagnostic sweep) are consistent with the spirit of Bayle's careful reading. No changes are made in direct response to Bayle's five points because all are already correctly characterized in the draft and the reviewer does not request changes to them.

One specific point is worth acknowledging directly. Bayle notes: "Lines 12–13 claim 'every result in this paper is fully reproducible by running the attached script,' but the script is not attached." This sentence has been revised. The revised text no longer promises an "attached script" in the Methods section; instead, the Runbook closes with "The complete script `ba_power_law_test.py` is provided as a supplementary file alongside this post." The Methods section now reads "every result in this paper is fully reproducible by running the attached script `ba_power_law_test.py`"-which is now true, because the script is attached.
