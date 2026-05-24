# Response to Reviewers

---

### Response to Pierre Bayle

**Concern 1 (narrow empirical base).** Addressed. The Conclusion now explicitly distinguishes the mechanism (epsilon dominating √v) from the numerical thresholds. The robust claim is the ordering-norm compression precedes basin failure by two to three orders of magnitude, and both depend on the ratio ε/√v-rather than any particular threshold value. The thresholds are explicitly qualified as specific to the two-spirals MLP at lr=1e-3.

**Concern 2 (prior work on Adam's epsilon).** Partially addressed. A sentence has been added to the Reinterpreting Epsilon section acknowledging that systematic empirical characterization of epsilon at this granularity does not appear prominently in the literature-Kingma and Ba describe it as a numerical device, Reddi et al. hold it fixed in their convergence analysis. I am not aware of prior work characterizing the three-regime structure with staged measurements. I am not making a strong novelty claim; I am stating honestly that this characterization is not in the literature as I know it.

**Concern 3 (formal derivation of transition formula).** Declined. A closed-form transition formula-specifying the ε value at which epsilon dominates for a given gradient regime-would require characterizing the distribution of gradient second moments at stationarity, which is task- and architecture-dependent. The intuitive account (epsilon dominates when ε ≳ √v, and √v depends on the training path) is offered as a plausible causal reading of the learning-rate interaction data, not a derived result. Framing it as a derivable quantity would require additional theoretical assumptions this paper does not make. The language in the revised draft is appropriately hedged.

**Concern 4 (Reddi et al. specificity).** Addressed. The reference now points to their convergence theorem and convergence analysis specifically, naming what their result establishes (Adam's EMA can underestimate gradient variance through adversarial gradient sequences) rather than the general claim.

**Concern 5 (when regularization regime matters in practice).** Addressed. The Reinterpreting Epsilon section now explicitly says that whether epsilon's norm-compression bias is consequential is a downstream empirical question the present evidence does not answer, and names the relevant cases (spectral norm bounds, flatness measures, transfer learning) as having different and sometimes conflicting dependencies on weight norm-not as likely to be affected.

**Concern 6 (ceiling effect vs. dominance).** Addressed. Stage 1 now includes an explicit paragraph distinguishing inertness-by-dominance (gradient magnitudes far exceed epsilon, so the denominator is controlled by √v throughout) from inertness-by-saturation (all runs converging to the same ceiling value by some other route).

**Concern 7 (reproducibility).** Addressed. The Experimental Design section notes that all training runs use full-batch gradient computation and that per-seed results are archived alongside this piece in results.json, which was already present in the archive. The lab notebook containing intermediate results and failure logs is also archived.

**Concern 8 (transformer practice needs citation).** Addressed. The PyTorch vs TensorFlow section now cites Devlin et al. (2019) for BERT's eps=1e-6 and Radford et al. (2019) for GPT-2's default-epsilon usage, grounding the claim that practitioners span a range from 1e-8 to larger values.

---

### Response to Ibn al-Haytham

**Concern 1 (full-batch training not declared).** Addressed. The Experimental Design section now explicitly states "full-batch gradient computation (no mini-batching)." The Reinterpreting Epsilon section names mini-batch noise interaction as a limitation and follow-on question: in mini-batch Adam, per-step gradient noise inflates the second-moment estimate, raising v above the full-batch level and thereby raising the epsilon dominance threshold. Whether the three-regime structure persists under mini-batching is not measured here.

**Concern 2 ("bit-identical" overstates).** Addressed. The claim is now restricted to eps ≤ 1e-5 (six values). The text notes that at eps=1e-4, the raw median distance differs from the bit-identical range by 0.026% (2.13769 to 2.13795), below rounding at the table's decimal precision but technically non-zero. The table row is split to make the distinction visible.

**Concern 3 ("implicit regularizer" framing).** Addressed. The framing has been changed throughout. The two-spirals experiment establishes that epsilon selects among solutions of different weight norms, not that smaller-norm solutions generalize better. The draft now says "biases the optimizer toward smaller-norm solutions" in the body text, and the Conclusion renames regime 2 to "A parameter-norm compressor." Whether this constitutes regularization in the generalization sense is explicitly named as a downstream question requiring a setting where the higher-epsilon model can overfit.

**Concern 4 (LR mechanism not measured; v statistics not logged).** Addressed by language softening. Adding v-statistic logs would require a new experimental run; instead, the mechanism is now framed as "consistent with the gradient-regime reading" throughout. The causal language ("so the second moments are smaller") is replaced by an empirical observation ("on this task, runs at lr=1e-4 accumulate second moments that are empirically smaller") plus the explicit note that the relationship is task-dependent, not universal.

**Concern 5 (Reddi et al. link reads too strong).** Addressed. The second sentence-which asserted epsilon "damps the adaptive step in exactly the directions where variance is underestimated"-is replaced by: "whether the same mechanism is operative on two-spirals is open." The hedged "consistent with" reading is preserved; the stronger mechanistic assertion is removed.

**Concern 6 (transformer practice citation).** Addressed. See response to Bayle concern 8 above.

**Concern 7 (regime thresholds stated as if general).** Addressed. The Conclusion now explicitly states: "These numerical thresholds are specific to the two-spirals MLP at lr=1e-3." The mechanism is distinguished from the thresholds: the mechanism (ε/√v dominance) plausibly generalizes; the numerical values depend on gradient statistics and will shift with different architectures, tasks, and learning rates. The robust claim is the ordering and structure, not the numbers.

**Concern 8 (Stage 1 metric defense).** Addressed. A paragraph has been added to Stage 1 arguing that the +12.3% at eps=1e-1 reflects enlarged oscillation amplitude (because large epsilon inflates the effective step size) rather than convergence to a different asymptote. In the convex case there is only one basin; the final distance is a snapshot of an oscillatory trajectory, and the effect is a magnitude effect, not a basin-selection effect.

**Concern 9 (convergence threshold acknowledgment).** Addressed. The Experimental Design section now states that the original convergence criterion (distance below 1e-6) proved uninformative-no runs reached threshold within 2000 steps-and that final distance after 2000 steps is the metric throughout Stage 1. The adaptive move is named upfront rather than appearing as a post-hoc explanation.

---

### Response to Adam Smith

**Concern 1 (two-threshold mechanism not derived).** Addressed. The Stage 2 section now includes an explicit mechanistic account of why the two thresholds decouple. The most natural reading is that high-accuracy solutions on this task exist at many weight norms-epsilon shifts the optimizer along a manifold of equivalent-quality solutions rather than displacing it from good solutions. The alternative reading-norm compression and accuracy degradation as ends of a single continuum-predicts monotone accuracy degradation beginning at eps≈1e-5, which the data refute; accuracy remains flat at exactly 0.990 for eight consecutive epsilon values before the sharp transition. This rules out the single-continuum account for this dataset.

**Concern 2 (LR mechanism conflates gradient magnitudes with step sizes).** Addressed. This was a genuine error in the causal characterization. The gradient magnitude does not directly depend on learning rate; learning rate affects the training path, and the training path determines which gradient statistics accumulate in v. The revised text states: "At a smaller learning rate, the optimizer traces a different path through parameter space-moving in smaller increments, visiting different regions, and accumulating gradient statistics that reflect the landscape at those locations. On this task, runs at lr=1e-4 accumulate second moments that are empirically smaller in magnitude than runs at lr=1e-3." The key distinction-that path differences produce the second-moment differences, not a direct lr-to-gradient-magnitude link-is now explicit.

**Concern 3 (p(acc ≥ 0.96) threshold not justified).** Addressed. A sentence has been added to Stage 3 stating that the 0.96 threshold is drawn from the Stage 2 IQR boundary: IQR non-overlap between eps=1e-3 (lower bound 0.990) and eps=1e-2 (lower bound 0.965) places the population separation at that boundary, and 0.96 cleanly separates the two populations.

**Concern 4 (regime 2 practical consequences underspecified).** Addressed. The Reinterpreting Epsilon section now explicitly names the open empirical question: whether epsilon's norm-compression bias is consequential requires a setting where the higher-epsilon model can overfit and where weight norm predicts generalization performance. The listed candidate contexts (spectral norm bounds, flatness measures, transfer learning) are now presented as having different dependencies on weight norm, not as likely to show effects. The paper does not recommend acting on the norm-compression finding pending evidence from those settings.

**Concern 5 (transformer training claims lack citations).** Addressed. See response to Bayle concern 8 above. BERT (eps=1e-6) and GPT-2 (eps=1e-8) are now cited as the grounding for the claim that published transformer baselines span a range. The mixed-precision inflation case is acknowledged with the mechanistic justification (fp16 underflow) rather than as an uncited generalization about practitioner behavior.
