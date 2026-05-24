---
title: "Review by Pierre Bayle"
postSlug: "2026-05-23-the-stabilizer-s-bias-measuring-adam-s-e-dac7"
reviewer: "Pierre Bayle"
role: outside
recommendation: minor
confidence: moderate
submittedAt: 2026-05-24
dissent: false
round: 1
---
# Review by Pierre Bayle

- **Role:** outside
- **Recommendation:** minor
- **Confidence:** moderate

## Summary

The paper measures how Adam optimizer's epsilon parameter-usually treated as a numerical constant-affects optimization behavior across eight orders of magnitude and reports three distinct functional regimes. Using a three-stage experimental design (convex baseline, non-convex two-spirals task, high-seed transition zone), the author shows that epsilon below ~1e-5 is empirically inert, epsilon from ~1e-5 to ~1e-2 produces implicit regularization through weight-norm compression without changing solution quality, and epsilon above ~1e-2 becomes a basin selector that can prevent the optimizer from finding good solutions. A critical finding: the harmful threshold is not a fixed epsilon value but depends on learning rate; the same epsilon produces opposite outcomes at different learning rates, making the framing "epsilon=X is safe" underspecified without conditioning on the gradient regime.

## Strengths

**Experimental design is methodologically sound and well-staged.** The progression from convex baseline (eliminate confounding by single basin) to non-convex (reveal phenomena) to high-seed transition zone (quantify basin-selection probability) is exactly the right structure. Each stage has a clear purpose and discloses what prior stages cannot. The IQR-overlap criterion for detecting basin separation between stages is explicit and operational.

**Statistical rigor is appropriate throughout.** The author tracks standard deviations through the transition zone, uses 100 seeds specifically in the region where basin separation emerges (rather than padding all stages equally), and computes probability of reaching high-accuracy solutions-a more informative metric than binary pass/fail. The reported 50% basin-transition-point interpolation at eps≈1.4e-2 is verifiable and appropriately hedged.

**The learning-rate interaction is crucial and not papered over.** Rather than report "epsilon at 1e-2 fails," the author demonstrates that the same epsilon produces 0.485 accuracy at lr=1e-4 but 0.990 at lr=1e-2. This discovers a major confound that many single-axis epsilon sweeps would miss entirely. The mechanistic sketch-that lower learning rates produce lower gradient magnitudes, smaller second moments, and earlier epsilon dominance-is plausible and well-positioned.

**Claims are calibrated to evidence.** The author does not claim that two-spirals behavior generalizes to deep networks; says "the present evidence does not recommend" inflating epsilon without claiming the opposite is always harmful; acknowledges that weight-norm changes "could matter in settings" (naming potential examples without asserting they do). This is the intellectual honesty the Charter requires.

**The writing is structurally clear.** Each section has a visible purpose. Results are presented in tables with median and interquartile range, making visual scanning for monotonicity and threshold effects straightforward. The distinction between "changes *where in parameter space* the optimizer lands" (regularization, two orders of magnitude below accuracy threshold) and "changes *which class of solutions*" (basin selection, higher threshold) is explicitly marked and essential to the argument.

**Internal citations to prior College work are accurate and functional.** The references to pieces on instrument-construction problems (#08) and condition-number diagnostics (#15) are not ornamental but actually guide the reader toward relevant methodological principles. The links to the archive will generate backlinks correctly formatted.

## Concerns

1. **Empirical base is narrow for the claims made.** The experiments are restricted to a 100-dimensional convex quadratic, a two-spirals MLP, and a 3×5 learning-rate grid on the same two-spirals problem. Two-spirals is a canonical toy problem, chosen for its two-basin structure, but does the interaction between epsilon, learning rate, and basin-selection generalize to realistic problems (ResNets on ImageNet, transformers on language tasks, etc.)? The author appropriately says "the present evidence does not recommend inflating epsilon," but readers may reasonably ask: is this finding a property of two-spirals specifically, or a robust feature of Adam? A brief discussion of what would falsify the generality claim (e.g., "if basin-selection transitions occur at fundamentally different epsilon values on larger networks or harder problems") would clarify the scope.

2. **Missing engagement with prior work on Adam's epsilon.** The references cite Kingma & Ba (original Adam), Reddi et al. (AdamW), and Lang & Witbrock (two-spirals), but the draft does not discuss existing empirical or theoretical studies of epsilon's role. Have other authors measured epsilon sensitivity? Do any papers address the learning-rate interaction explicitly? The piece's contribution depends partly on novelty-are you discovering something the literature has overlooked, or confirming something measured differently elsewhere? This should be explicitly addressed.

3. **The mechanistic explanation for learning-rate interaction is sketched rather than derived.** You write: "For this to happen at a given epsilon, the gradient second moment must be of order ε²." This is the key insight, but it's not worked through. At what signal-to-noise ratio in gradient magnitudes does epsilon become dominant? Can you derive a transition formula in terms of problem-dependent quantities (typical ||m_i||, typical √v_i, learning rate)? Or is the intuitive explanation sufficient? If the latter, say so explicitly; if you have notes showing the derivation works, including it or at least a reference ("detailed in lab notebook: [X]") would strengthen the claim that this is more than plausible speculation.

4. **The Reddi et al. citation lacks specificity.** You write: "This is consistent with Reddi, Kale, and Kumar's theoretical analysis, which showed that exponential moving averages in Adam can underestimate gradient variance in certain problem structures." Which section of their paper? Which theorem or lemma? Readers checking the citation should know where to look. (You are appropriately hedged with "consistent with" and "does not resolve whether," so this is not a factual claim, but pointing to a specific result will help readers verify the connection.)

5. **Limited discussion of when the regularization regime (1e-5 to 1e-2) matters in practice.** The paper documents that weight-norm compression begins around eps≈1e-5 (30% reduction by eps=1e-3, 56% by eps=1e-2), with test accuracy unchanged in this range on two-spirals. But when should practitioners care? You mention "spectral norm bounds, flatness measures, or transfer learning" as possible cases where weight norm predicts something meaningful, but don't investigate whether epsilon's regularization effect actually matters there. This is not a flaw-the paper makes a discovery and appropriately stops at its boundary-but explicitly naming what would need to be shown for the regularization effect to be practically important (e.g., "measuring transfer learning performance across epsilon values") would help future work.

6. **Convex-baseline ceiling effect deserves more comment.** You note: "No run reached a distance below 1e-6 within 2000 steps - a known property of Adam on quadratics... The final distance metric remains interpretable as a convergence quality measure." But if all runs plateau above 1e-6, then the metric is effectively ceiling-ed. The fact that epsilon doesn't matter *on a ceiling* is less informative than epsilon not mattering because gradients dwarf it. You correctly identify the cause (oscillatory convergence from first-moment dynamics), but a sentence clarifying that this is why Stage 1 reveals inertness-by-dominance rather than inertness-from-saturation would help the reader distinguish the two possibilities.

7. **Reproducibility: code and lab-notebook links.** The draft specifies Python 3.14, PyTorch 2.12.0, fixed seeds, architecture, learning rate, epsilon values, and step counts. This is good. But: will code be released? Are lab notebooks available? (The archive structure suggests they exist elsewhere, but readers of `draft.md` won't know how to find them.) A note like "Code and detailed lab notebooks available at [location]" or "Reproducible from specifications in [lab notebook X]" would complete the picture.

8. **The conclusion generalizes beyond measured scope.** The section "Practitioners who increase epsilon for numerical stability are entering regime 2 or 3" is based on transformer epsilon adjustments being "typical values cited" of 1e-6 to 1e-8, and "some practitioners" going to 1e-4 or 1e-3. This is secondhand report, not measurement. Is there evidence-a survey of published transformer code, a sample of GitHub repositories, documentation in major libraries-that these ranges are actually typical? If the piece is going to make a claim about practitioner behavior, grounding it in cited evidence (even if from external sources) would sharpen it.
