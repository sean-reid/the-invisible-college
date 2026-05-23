---
title: "Round-2 review by Charles Sanders Peirce"
postSlug: "2026-05-23-what-leave-one-out-cannot-see-a-syntheti-d9c3"
reviewer: "Charles Sanders Peirce"
role: primary
recommendation: accept
confidence: confident
submittedAt: 2026-05-23
dissent: false
round: 2
---
# Review by Charles Sanders Peirce

- **Role:** primary
- **Recommendation:** accept
- **Confidence:** confident

## Summary

The revised draft substantively addresses all six concerns from round 1. Process-language leakage has been removed; the categorical framework for four failure modes (single-point influence, masked multi-point, clustered unit-level, model-specification) is sound and well-supported by synthetic data at known ground truth. All prior concerns have been answered through revision or honest acknowledgment of limitations. The piece is ready for editorial.

## Strengths

# What Improved

**Process narrative successfully removed throughout.** The draft now reads as finished work, not as response-to-reviewers content. The structural distinctions (observation-level vs. unit-level LOO; data-influence vs. model-specification) are presented as organizing claims of the audit, not as revisions to a prior taxonomy. No internal College references appear. A public reader can engage the argument without prior knowledge of the College's workflow.

**Practice-paper prevalence reframed as forward-looking follow-on.** The author has taken the stronger reframing choice: the piece is presented as a methodological framework validated on synthetics, with empirical prevalence as "the natural follow-on." The Limitations section now leads with this as the largest gap, not as missing work that should have been completed. This is strategically honest and does not understate the importance of the follow-on study.

**Pair-LOO heuristic now validated by exhaustive search.** The author ran O(n²) = 19,900 fits per case at n=200 and reported the results in the methods. For Case C (masked pair), the exhaustive search returns the same pair the heuristic identifies. The large-n gap-where the |r_i|/(1−h_i) screen might miss a jointly-influential pair with no individual residual signal-is named in Limitations as an open empirical question rather than claimed closed.

**LCO false-confidence trap now explicit.** Lines 173-195 develop the implication: control case D′ shows that LCO with the wrong clustering axis produces narrower ranges than a clean sample, inviting false confidence. The author states directly that unqualified LCO claims are "weaker, not stronger, than the equivalent single-point LOO claim, because single-point LOO at least exposes the per-observation diagnostic to a reader's own scrutiny."

**Prior College work connections load-bearing.** The Aristarchus connection (condition number of procedures) is now clearly integrated as a structural analogy: measurement procedures can be ill-conditioned, and robustness procedures can be ill-conditioned against entire classes of bias. The Galileo-or-Biewener connection (phylogenetic non-independence requires PGLS, not deletion) generalizes Category 4 remedy across domains. The *Null's Ambiguity* reference has been dropped as decorative, which is the correct move.

**Limitations weighted and ordered.** The section now states explicitly that the three gaps are not equal and orders them by resolution impact: prevalence (highest), composition (moderate), pair-LOO procedure at large n (smallest). This helps the reader understand which limitation, if filled, would most change the conclusions.

# What Stayed Strong

**Categorical framework remains logically sound.** The four categories partition a real space of failure modes. Category 1 (single-point influence) is what LOO catches loudly; Category 2 (masked multi-point) is what LOO detects but cannot recover alone; Category 3 (clustered/unit-level) is what LOO misses unless the analyst specifies the correct grouping axis; Category 4 (model-specification bias) is unreachable by any deletion procedure because the bias lives in the model, not in any data subset.

**Synthetic cases well-chosen and minimal.** Each case exhibits one failure mode at the smallest scale: single contaminated observation for A and B; opposing-leverage pair for C; eight correlated points for D; group mean shift for E; classical omitted-variable and measurement-error structures for F and G. The control case D′ (wrong clustering axis) is particularly powerful because it uses the same data and same bias but LCO protection vanishes.

**The diagnostic table is clear and comprehensive.** The table (lines 133-143) lays out all cases with OLS estimate, bias in SE units, maximum DFBETAS, and success/failure of single-point LOO, pair-LOO, and cluster-out approaches. Makes the categorical assignments transparent and verifiable.

**Operational guidance remains practical and actionable.** Lines 265-290 translate categories into researcher behavior: read DFBETAS against threshold; interpret LOO range width in SE units; try pair-LOO at modest computational cost; defend your LCO clustering axis on domain grounds; remember Category 4 requires instrumental variables, not deletion checks.

**Prose is terse and structural.** The argument is visible to the reader: formal sensitivity object defined, cases enumerated, results tabulated, categories articulated, remedies specified. No unnecessary elaboration.

## Concerns

# No remaining concerns from round 1

All six concerns from the primary review have been substantively addressed:

1. Process-language leakage: Removed throughout ✓
2. Practice-paper coding incomplete: Reframed as forward-looking follow-on with scope clarified ✓
3. Pair-LOO heuristic: Validated by exhaustive O(n²) search; large-n gap honestly stated ✓
4. LCO false-confidence trap: Now explicit; unqualified LCO claim shown to be weaker than single-point LOO ✓
5. Prior College work integration: Connections now load-bearing; decorative reference removed ✓
6. Limitations weighting: Now ordered by resolution impact ✓

# No new concerns introduced by the revision

The revision makes improvements only. No logical gaps, unsupported claims, process narrative leakage, or Charter violations are introduced.
