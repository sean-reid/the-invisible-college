# Response to Round-2 Reviewers

This is the final polishing pass. Two reviewers recommended accept; one recommended minor. I address each concern in order below. Where I decline a request, I state my reasoning explicitly.

---

### Response to Pierre Bayle

**Concern 1 (Reproducibility pointer missing from draft).**
Fixed. Added one sentence to Experimental Design: "Code and lab notebooks are archived alongside this piece." The pointer now appears in the public artifact, not only in ancillary documents.

**Concern 2 ("Common heuristic" claim overstates the evidence).**
Fixed. The phrase "A common heuristic in transformer training is to increase epsilon for numerical stability" was replaced with "Epsilon varies across published transformer training configurations." The two citations (BERT at eps=1e-6; GPT-2 at PyTorch default eps=1e-8) demonstrate variation across baselines; they do not establish that inflation for stability is a common or typical practice. The revised framing is precisely what the evidence supports.

**Concern 3 (LR mechanism is sketched, not derived).**
Fixed. The mechanism paragraph now explicitly flags its epistemic status: "This mechanistic account is a plausible reading of the observed threshold shift, consistent with the data but not uniquely derived from it." A reader can now distinguish between the empirical finding (the threshold shifts with learning rate, as shown in the 3×5 grid) and the proposed mechanism (ε/√v dominance, where v depends on the training path). The former is demonstrated; the latter is a consistent explanation, not a derived result.

**Concern 4 (Rename "parameter-norm compressor" to "parameter-norm shifter").**
Declined. "Parameter-norm compressor" accurately names the demonstrated mechanical effect: the optimizer converges to solutions of measurably smaller weight norm as epsilon increases. The term does not imply generalization benefit. The Conclusion already states explicitly: "Whether this bias constitutes useful regularization-improved generalization through norm control-is a downstream question the present evidence does not answer." Given that qualification is already in the text immediately after the label, renaming to "shifter" would not add information and would introduce a term that is less descriptive of the direction of the effect (norms decrease monotonically with increasing epsilon, which "compression" captures and "shifting" does not).

**Concern 5 (Full-batch limitation in Conclusion).**
Fixed. Added to the Conclusion paragraph that names threshold caveats: "These thresholds are measured under full-batch conditions; mini-batch noise would raise the epsilon dominance threshold, as discussed above." This ensures the scope statement appears in both the body (Reinterpreting Epsilon section) and the Conclusion.

**Concern 6 (Reddi et al. connection should be more specific).**
Fixed. The body text now reads: "Their central result constructs adversarial gradient sequences for which Adam's exponential moving average systematically underestimates variance, proving non-convergence in specific online learning settings. Large epsilon produces a structurally analogous effect-the adaptive denominator loses sensitivity to per-parameter gradient variance history-making the empirical finding compatible with their analysis." This identifies what Reddi et al. showed (adversarial sequence construction, systematic variance underestimation, non-convergence proof) and makes the connection to the present finding explicit (large epsilon suppresses the same variance sensitivity by a different mechanism). I have not cited a specific theorem number because I cannot verify the exact number without access to the paper; the description of the result is accurate to my knowledge.

---

### Response to Ibn al-Haytham

**Concern 1 ("empirically" outruns the measurement taken).**
Fixed. The original wording-"runs at lr=1e-4 accumulate second moments that are empirically smaller in magnitude than runs at lr=1e-3"-implied that v was directly logged, which it was not. The revised text reads: "For the threshold shift in the 3×5 grid to arise from the ε/√v dominance mechanism, runs at lr=1e-4 would need to accumulate second moments of smaller magnitude than runs at lr=1e-3-the grid data are consistent with this, but second-moment statistics were not directly logged in this experiment." The fix follows the option you suggested: frame the v-magnitude claim as a consequence of the observed threshold shift under the proposed mechanism, not as a directly measured fact.

**Concern 2 (3×5 grid does not state seed count or summary statistic).**
Fixed. The table header now reads: "A 3 × 5 auxiliary grid (each cell the median test accuracy across 10 seeds) reveals:" The seed count and summary statistic are now stated before the table, consistent with the hygiene maintained throughout the rest of the piece.

**Concern 3 (No process-language leakage).**
Confirmed and noted. No changes were needed here.

---

### Response to Adam Smith

**Concern 1 (Stage 1 table split opaque without explanation).**
Fixed. Added an italic note immediately below the table: "*The eps=1e-4 row shows the same values at the displayed precision but differs by 0.026% in unrounded data (2.13769 vs 2.13795 for the median); see text.*" A reader who scans the table before reading the paragraph now has the explanation in place, not just in the body prose.

**Concern 2 (Mixed-precision citation still not direct).**
Fixed. The revised text reads: "Mixed-precision (fp16) training can motivate higher epsilon values to prevent second-moment underflow under reduced floating-point precision; some practitioners use eps=1e-4 or higher in this setting, though no single published standard exists." This honestly represents the epistemic status: the mechanistic reason (fp16 underflow) is well-founded; the specific numerical claim about community practice is acknowledged as lacking a single citable source. The hedging ("some practitioners," "no single published standard") is proportionate to what I can actually support.

**Concern 3 (No process-language leakage).**
Confirmed and noted. No changes were needed here.
