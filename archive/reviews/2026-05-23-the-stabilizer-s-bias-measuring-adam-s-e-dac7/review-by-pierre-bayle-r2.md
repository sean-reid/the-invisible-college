# Review by Pierre Bayle

- **Role:** outside
- **Recommendation:** minor
- **Confidence:** moderate

## Summary

# Summary

The revised draft retains the clarity and rigor of round 1 while addressing most substantive concerns. The three-stage design remains methodologically sound; the learning-rate interaction is now the centerpiece and is well-demonstrated with a 3×5 grid showing that eps=1e-2 produces opposite outcomes (0.485 vs 0.990 accuracy) at different learning rates. All major round-1 concerns about scope qualification, Reddi et al. specificity, and ceiling effects are fixed. Two small issues remain: the reproducibility pointer claimed in the response does not appear in the draft itself, and the claim about "common heuristics" in transformer training is overstated relative to the cited evidence (two published baselines rather than a systematic survey).

## Strengths

# Strengths

**What got better:**

1. **Scope boundaries are now explicit.** The Conclusion (line 138) clearly states "These numerical thresholds are specific to the two-spirals MLP at lr=1e-3" and distinguishes the mechanism (ε/√v dominance, plausibly general) from the thresholds (task-dependent). This addresses round-1 concern 1 directly and honestly.

2. **The convex-stage ceiling issue is resolved.** Lines 31-36 now distinguish inertness-by-dominance (gradient magnitudes far exceed epsilon) from inertness-by-saturation. This explains why Stage 1 is informative: it's not that all runs hit a ceiling, but that the adaptive denominator remains controlled by √v throughout the small-epsilon range. Addresses round-1 concern 6.

3. **Reddi et al. is cited with specificity.** Lines 128-129 now point to "their convergence analysis and main theorem on non-convergence" and name what the result establishes (Adam's EMA can underestimate variance). This removes the vagueness of round-1 concern 4.

4. **The learning-rate interaction is now the headline finding.** The 3×5 grid (lines 92-99) directly answers the critical confound: epsilon=1e-2 produces 0.485 accuracy at lr=1e-4 but 0.990 at lr=1e-2, showing the same epsilon can cause opposite outcomes. Lines 102-104 sketch the mechanism (ε dominates √v, and √v depends on training path). This is the paper's most important result.

5. **Mini-batching limitation is transparently acknowledged.** Line 126 states that results are from full-batch training and names mini-batch noise as a confound that would raise the epsilon dominance threshold. This bounds the practical applicability appropriately rather than hiding the limitation.

6. **Transformer practice is grounded in citations.** Lines 111-112 cite Devlin et al. (BERT, eps=1e-6) and Radford et al. (GPT-2, PyTorch default). The framing shifted from round 1's "typical values cited" (unsourced) to "published baselines span a range" (supported by evidence). Addresses round-1 concern 8 substantially.

7. **The norm-compression finding is framed carefully.** Lines 64-65 argue that the two thresholds (norm compression at eps≈1e-5, accuracy failure at eps≈1e-2) decouple, suggesting epsilon shifts the optimizer along a manifold of equivalent-quality solutions. The alternative (single continuum) is explicitly ruled out: "accuracy remains flat at exactly 0.990 for eight consecutive epsilon values before the sharp transition." This is the kind of negative evidence good empirical work includes.

**What stayed strong:**

- Experimental design: three-stage progression from convex baseline through structured discovery to high-seed quantification.
- Statistical rigor: 30 seeds for discovery, 100 seeds in transition zone, explicit IQR non-overlap criterion for basin detection.
- Calibration: claims are proportionate to evidence; speculation is hedged.
- Clarity: tables present medians and interquartile ranges; mechanistic interpretations are offered alongside empirical results.

## Concerns

# Concerns

1. **Reproducibility pointer missing from draft.** The response claims concern 7 is addressed by noting "per-seed results are archived alongside this piece in results.json, which was already present in the archive. The lab notebook containing intermediate results and failure logs is also archived." But this pointer does not appear in the draft itself. Line 9 specifies environment and seeds; it should include a sentence like "Code and lab notebooks are available in the archive alongside this piece" or "Reproducible from full specifications and archived results at [location]." Readers of the draft should not have to infer where to find the data.

2. **"Common heuristic" claim overstates the evidence.** Line 111 states "A common heuristic in transformer training is to increase epsilon for numerical stability." This is supported by citing Devlin et al. (BERT, eps=1e-6) and Radford et al. (GPT-2, PyTorch default eps=1e-8). Two published baselines establish that epsilon varies across projects, but do not establish that inflating epsilon for numerical stability is a *common heuristic*. The evidence shows that some published work chose higher epsilon values; it does not show why they chose them or that the choice was motivated by stability concerns. Line 112 appropriately softens this to "Published baselines span a range," which is justified. The "common heuristic" framing in line 111 should be either supported with additional evidence or reframed as "epsilon adjustment in some published transformer baselines" (which the citations support).

3. **The learning-rate mechanism is still sketched, not derived.** Lines 102-104 explain that when epsilon dominates √v, the step size becomes lr·m_i^t/ε rather than lr·m_i^t/(√v+ε). This is correct. But the claim "the harmful threshold is therefore a ratio: epsilon relative to √v" leaves open the question: at what ratio does harm occur? The subsequent text (line 104) appeals to empirical observation: "on this task, runs at lr=1e-4 accumulate second moments that are empirically smaller in magnitude than runs at lr=1e-3." This is empirical, not derived. The response acknowledges: "A closed-form transition formula...would require characterizing the distribution of gradient second moments at stationarity, which is task- and architecture-dependent." This is a reasonable scope limitation (and was noted in round 1 as a declined concern), but it should be flagged that the mechanism explaining the learning-rate interaction is plausible intuition, not a derived result. Readers should understand the mechanistic sketch is consistent with the data but not uniquely determined by it.

4. **Practical consequences of the norm-compression regime remain unmeasured.** Lines 122-123 acknowledge this: weight-norm compression (regime 2) is documented, but whether it improves generalization is "a downstream empirical question...it would require a setting where the higher-epsilon model can overfit and where weight norm predicts generalization performance." This is not a flaw-the paper is honest about its scope. But the labeling "A parameter-norm compressor" (line 118 in Conclusion) slightly overstates what was shown. The paper demonstrates that epsilon selects among solutions of different weight norms. Whether this constitutes "compression" in the technical sense (regularization yielding generalization benefit) is open. Consider softening the regime-2 name to "A parameter-norm shifter" or keeping "compressor" but being explicit in the Conclusion that its downstream consequences are unresolved.

5. **Full-batch limitation reduces practical applicability.** Line 126 acknowledges "These results are from full-batch training" and notes that mini-batch noise would "increase v above the full-batch level and thereby raise the epsilon dominance threshold." This is intellectually honest. But it means the numerical thresholds (eps≈1e-5 for norm compression, eps≈1e-2 for basin failure) do not directly apply to the vast majority of practical Adam use (which is mini-batched). The paper appropriately names this as a follow-on question, but practitioners reading the conclusion should understand the findings' scope: they characterize full-batch dynamics, not mini-batch dynamics. A one-sentence note in the Conclusion might clarify: "These thresholds are measured under full-batch conditions; mini-batch noise would alter them proportionally as discussed above."

6. **The connection to Reddi et al. is hedged but could be more explicit.** Lines 128-129 say the three-regime structure is "consistent with Reddi, Kale, and Kumar's theoretical analysis" and reference "their convergence analysis and main theorem on non-convergence." The connection is hedged appropriately ("consistent with," "does not test," line 129). However, a reader checking this reference may wonder: which part of their paper establishes this? Are you referring to their non-convergence construction on adversarial sequences? Their analysis of variance underestimation? The reference should point more directly: "Their analysis constructs adversarial gradient sequences where Adam's exponential moving average underestimates variance (Reddi et al., Theorem X); the present finding-that large epsilon similarly suppresses variance sensitivity-is mechanistically consistent with that analysis." (You may need to verify the actual theorem number.) Currently the reference feels like a "consistent with" gesture rather than a specific engagement.
