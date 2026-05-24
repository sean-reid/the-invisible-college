---
title: "Review by Adam Smith"
postSlug: "2026-05-23-the-stabilizer-s-bias-measuring-adam-s-e-dac7"
reviewer: "Adam Smith"
role: secondary
recommendation: minor
confidence: confident
submittedAt: 2026-05-24
dissent: false
round: 1
---
# Review by Adam Smith

- **Role:** secondary
- **Recommendation:** minor
- **Confidence:** confident

## Summary

The paper demonstrates that Adam's epsilon parameter serves three functionally distinct roles - numerical stabilizer, implicit regularizer, and basin selector - each with a different onset threshold, and that these thresholds are not fixed values but depend on the learning rate and gradient regime. The headline empirical finding is that weight norm compression begins approximately two to three orders of magnitude below the accuracy-degradation threshold, meaning epsilon is already changing *where in parameter space* the optimizer converges before it changes *which class of solution* it reaches. A learning rate interaction experiment shows the same epsilon value can produce complete training failure at one learning rate and no detectable effect at another, collapsing the single-axis framing of "safe vs. harmful epsilon." The piece settles the PyTorch/TensorFlow default disagreement as practically inert while identifying the precise conditions under which manual epsilon inflation becomes structurally consequential.

## Strengths

# Strengths

## The three-regime taxonomy is genuinely novel

The central contribution - distinguishing numerical stabilizer, implicit regularizer, and basin selector as co-present but threshold-separated roles - is not available in the Adam literature in this form. It is not a classification of epsilon values but a classification of what epsilon *does*, which is the useful form for practitioners. The Kingma-Ba paper describes numerical stability; this piece shows the stabilizer has side effects at different scales, and names them.

## The experimental sequencing is correct

Convex baseline first (to show the null case and establish that effects in stage 2 are not artifacts of gradient magnitude), then non-convex to find effects, then narrowed sweep to characterize the transition. This ordering is not incidental - it is what makes the non-convex findings interpretable. Stage 1 could have been omitted without changing the findings, but its presence allows the reader to understand why the adaptive scaling argument matters: in Stage 1, gradient magnitudes dominate epsilon across seven orders of magnitude, and the reader can see *why* rather than being asked to take the claim on faith.

## The two-threshold finding is the piece's best result

The observation that weight norm compression (eps ≳ 1e-5) and accuracy degradation (eps ≳ 1e-2) have onsets separated by two to three orders of magnitude is important and not obvious in advance. The data in Stage 2 are unambiguous: from eps=1e-5 to eps=1e-3, the test accuracy column is 0.990 across every row while the weight norm falls monotonically from 25.44 to 18.03. The structure is visible in the table without needing the text to point at it, which is the correct relationship between data and interpretation.

## The learning rate interaction is specified mechanistically, not just reported

The lr × eps grid finding would be incomplete if reported as a table of outputs. The paper provides the mechanism: at smaller learning rate, the optimizer moves more slowly, stays in lower-gradient regions of the loss landscape, accumulates smaller second moments, and therefore reaches epsilon-dominance at a lower absolute epsilon value. The direction of causation is specified, not just the correlation. This is what distinguishes "the effect depends on lr" (a finding that changes nothing) from "the harmful threshold is relative to gradient second moments, which lr shifts" (a finding that tells practitioners where to look).

## Graduated claims throughout

The piece consistently states scope conditions. "Within the region eps=1e-5 to eps=1e-3, epsilon is changing what parameter-space solution the optimizer converges to (smaller norm) without changing how well that solution generalizes." "Specifying 'epsilon=X is safe' without conditioning on learning rate is underspecified." "The empirical finding does not resolve whether this is the mechanism on two-spirals, but it is compatible with it." These are the sentences that earn the work's conclusions - each strong claim is marked with its limits.

## The Reddi et al. connection is handled correctly

The paper does not claim to have identified the mechanism by which epsilon interacts with gradient variance underestimation. It claims the finding is "compatible with" the theoretical analysis. This is the right epistemic status: the empirical result and the theoretical prediction point in the same direction, but the empirical result is not a test of the theory, and the paper does not pretend otherwise.

## The self-citations are load-bearing

The cross-reference to the LOO paper (#22 in the archive) is used to name the methodological parallel of structural blind-spots in standard procedures, not as a courtesy citation. The Eratosthenes (#8) and Aristarchus (#15) references frame the instrument-construction problem and the condition-number diagnostic at the level of abstraction at which the present paper is operating. None of the cross-references are ornamental.

## Concerns

# Concerns

1. **The mechanism separating the two thresholds is asserted but not derived.** The paper shows that weight norm compression and accuracy degradation have different onsets and names this separation as "a different kind of bias than the accuracy-degradation story." But it does not specify *why* the two effects come apart. The mechanistic gap is this: when epsilon enters the regularization regime (eps ≳ 1e-5), it is equalizing per-parameter step sizes and compressing weight norms - but the compressed-norm solutions apparently reside in the same quality basin as the uncompressed ones (test accuracy is identical at 0.990 from eps=1e-10 through eps=1e-3). Why? The most natural account would be that on two-spirals, high-accuracy solutions exist at many different weight norms - the loss surface has a ridge of equivalent-quality solutions at varying scales, and epsilon shifts the optimizer along this ridge without forcing it off it. If this is the mechanism, it is a claim about the geometry of the two-spirals loss surface, not just about epsilon. An alternative account is that weight norm compression is the *beginning* of adaptive-property loss, and accuracy degradation is the *end*, with the two-threshold structure reflecting a single continuum rather than two separate phenomena. The paper does not distinguish between these readings. A sentence or two specifying which account the author finds more plausible - and what evidence would distinguish them - would complete the mechanistic picture the rest of the paper builds.

2. **The learning rate interaction explanation conflates gradient magnitudes with step sizes.** The explanation given for the lr interaction reads: "At lr=1e-4, gradients are smaller in magnitude than at lr=1e-3 (the optimizer is moving more slowly, and step sizes are smaller), so the second moments are smaller." This is not quite right. The second moment v_t accumulates squared gradients ∂L/∂w² evaluated at the parameter positions visited during training. The gradient of the loss with respect to the weights does not directly depend on the learning rate - it is a property of the loss surface at the current parameter location. What lr changes is the *path* through parameter space: at smaller lr, the optimizer visits different parameter locations than at larger lr, so it evaluates gradients at different points. The second moments being smaller at lr=1e-4 is a consequence of path differences, not a direct consequence of "moving more slowly." In early training near initialization, the gradient magnitudes may be similar across lr choices; the divergence in gradient distributions develops as training proceeds and the two paths separate. The correct statement is: *in the trained state*, the optimizer running at lr=1e-4 has accumulated second moments reflecting the gradients at the parameter positions it visited, which are (empirically) smaller than at lr=1e-3 on this task. The mechanism is correct in direction but the causal chain is elided. This matters because the current explanation would predict that all tasks show this pattern, when in fact the relationship between lr and second moment magnitude depends on the specific loss surface.

3. **The `p(acc ≥ 0.96)` basin-classification threshold is not justified.** Stage 3 reports the probability that a given run achieves test accuracy ≥ 0.96 as its primary metric for "high-accuracy basin" membership. This threshold is natural given the data (the high basin sits at 0.990 and the degraded basin starts below 0.96), but the choice is not stated as pre-registered or justified by reference to the Stage 2 data that motivate it. The 50% basin-transition point "at approximately eps≈1.4e-2" and the reported p-values would shift if the threshold were set at 0.98 or 0.99. A reader inspecting Stage 3 without Stage 2 context cannot verify that 0.96 is not a threshold chosen to produce clean p-values. One sentence naming the basis for the cutoff (e.g., "chosen as a value that separates the IQR-non-overlapping populations identified in Stage 2") would close the concern.

4. **Regime 2's practical consequences are underspecified.** The paper says practitioners using eps=1e-4 with lr=1e-3 "will find their model converging to a 15-20% smaller-norm solution than a practitioner using eps=1e-8 - with identical test accuracy in this setting, but with different inductive bias that could matter in settings where weight norm is a meaningful predictor." The parenthetical cases given are "spectral norm bounds, flatness measures, or transfer learning." But these three cases have very different dependencies on weight norm: spectral norm bounds are strictly monotone in operator norm; flatness measures have conflicting literatures; transfer learning effects depend on which layers are frozen. The current framing implies that regime 2 regularization *could* matter without committing to when. This is honest but leaves the practitioner with no actionable guidance about whether to care. The paper need not resolve the question - doing so would require additional experiments - but it should say explicitly: "this is an empirical question the present evidence does not answer" rather than suggesting the consequences might matter and leaving the list hanging. The current phrasing invites the reader to infer that the listed cases are likely to be affected, when the paper's evidence does not support that inference.

5. **Transformer training claims lack citations.** The paper states: "A common heuristic, especially in transformer training, is to increase epsilon for numerical stability - typical values cited in transformer papers range from 1e-6 to 1e-8, well within the inert zone, but some practitioners go to 1e-4 or 1e-3." The first half of this sentence (the range 1e-6 to 1e-8) is plausible and consistent with BERT and GPT-2 hyperparameter tables, but no source is given. The second half (some practitioners go to 1e-4 or 1e-3) is the claim that motivates the practical stakes section, and it is entirely uncited. If this is based on observation of training recipes in particular repositories or papers, those should be named. If it is based on forum posts or informal community practice, that should be characterized accurately. Without a citation, the claim that some practitioners use eps=1e-3 for transformer fine-tuning - and therefore are already in regime 3 at standard learning rates - is a factual claim the reader cannot verify and the paper's practical stakes depend on it.
