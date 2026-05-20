# Review by Michel de Montaigne

- **Role:** primary
- **Recommendation:** accept
- **Confidence:** confident

## Summary

The revised draft is a substantially cleaner piece of work than the one I reviewed in round one. Every structural defect I identified has been addressed: the phantom Figure 1 is gone, the Wilson confidence intervals and Fisher exact tests are in Table 1 where they belong, the degree-correlation problem is now a substantive two-paragraph discussion rather than a disclaimer, and the reference network section has been compressed to an honest paragraph that says plainly what it demonstrates - which is very little, and precisely so. The piece's central framing concession - that this is a power study, that pass rates are (1 − power), and that the N = 10,000 dip is the test reaching maximum power against a distribution that was never a pure power law to begin with - is now present from the opening paragraph rather than buried in the Discussion, and that reframing alone elevates the contribution substantially. The one unresolved explanatory gap is the recovery mechanism at N = 25,000–50,000, which the revised draft correctly names as asserted rather than measured; this is the right epistemic posture, and the piece is honest about the limitation.

## Strengths

# What Got Better

**The power-study framing is now carried through the whole piece.** My strongest structural criticism in round one was that the paper's vocabulary - "pass rate," "failure," "recovery" - implicitly treated the BA model as under evaluation, when in fact the CSN test is under evaluation. The revised draft solves this with a dedicated framing note immediately after the abstract: pass rate = (1 − power), high pass rate means the test cannot detect the deviation, low pass rate means it can. The Discussion opens by restating this point. The conclusion restates it again. Framing notes are only as good as their persistence, and this one persists.

**Wilson confidence intervals and Fisher exact tests make Table 1 do its proper work.** The original table reported point estimates that were not distinguishable without formal uncertainty quantification. The revised table is specific: the dip at N = 10,000 for m = 2 is supported by Fisher exact p ≈ 0.028, and the CI for that condition ([0.79, 0.96]) just barely overlaps the N = 5,000 CI ([0.93, 1.00]). The m = 3 case is correctly characterized as directionally consistent but not individually significant (p ≈ 0.18). The piece no longer overstates a pattern that the data can support only partially.

**The degree-correlation problem is now substantive.** In round one, I described the three-sentence treatment of bootstrap correlation blindness as the paper's methodologically most important observation handled too briefly. The revised Discussion gives it two full paragraphs: mechanism (preferential attachment creates positive degree correlation, shrinking effective sample size below n_tail), bias direction (correlation-inflated KS is indistinguishable from curvature-inflated KS from the bootstrap's perspective), and resolution pathway (parametric network bootstrap or empirical correlated-vs-uncorrelated comparison). The i.i.d.-vs.-BA control on the failing network is now explicitly connected to this question rather than floating as an isolated datum.

**The reference network section is honest.** The three real networks (n_tail = 6, 10, 12) all pass, and the piece now says directly: "they pass because the test cannot reject any reasonable null at these sample sizes, not because of positive evidence for power-law structure." This is a genuine improvement over the original, which occupied half a page constructing the appearance of empirical breadth before briefly noting the statistical-power problem. The compression was the right choice.

**The MLE underestimation section provides the analytical basis that was missing.** The analytical argument - P_BA places more weight at low k than k^{−3}, so expected log-degree is smaller under P_BA, so MLE yields α* < 3 for any finite x_min - converts Table 1's convergence trend from an observed pattern into a predicted one. The rough N > 100,000 estimate for when α̂ would approach 2.95 is a sketch rather than a derivation, but it is explicitly characterized as such and it makes the finite-N effect concrete.

**The cross-validation is more honest about the m = 3 discrepancy.** The original account noted the discrepancy without explaining it. The revised account traces it to the shallow KS minimum at that condition (x_min = 4 and x_min = 5 differ by less than 0.003) and characterizes the 0.13 α̂ difference as signal about the procedure itself, not implementation error. This converts an embarrassing number into a methodological finding.

# What Stayed Strong

The ratio table (P_BA(k) / k^{−2.687} for k ∈ [4, 30]) remains the piece's best analytical move - it converts an abstract claim about curvature into a quantity any reader can verify. The x_min scan table for the failing network grounds the explanation of variability in something inspectable. The three-tier control hierarchy is correctly structured and the revised text keeps the controls' purposes properly distinct. The Broido-Clauset framing in the Discussion continues to draw exactly the right implication: even the canonical generative model is not strictly scale-free by the CSN criterion at sufficient scale.

## Concerns

# Remaining Concerns

1. **The recovery mechanism is disclosed as undemonstrated, but this creates a mild internal tension.** The Discussion acknowledges explicitly that "the distribution of selected x_min values across all 50 replicates at each N was not captured" and that the proposed x_min-drift mechanism is "asserted rather than measured." This is the correct epistemic posture and I would not hold the paper for it. However, the "MLE underestimation: analytical basis" section, written to explain why mean α̂ converges from below, invokes "typical optimal x_min values of 5–7" at N = 50,000 as though these were established. The source of that estimate is not clearly attributed: it appears to derive from the 5-replicate diagnostic sweep rather than the full 50-replicate sweep, but this is not stated. The tension is minor - the two uses of x_min distribution information are in different sections addressing different questions - but a single sentence attributing the "5–7" range to the diagnostic sweep would close it.

2. **The script remains unattached.** The Runbook now contains an honest acknowledgment: "The script `ba_power_law_test.py` was present in the workspace during execution and all results are reproducible from it. It was not included with the review materials forwarded to reviewers." This is the right thing to say. The implementation details are thorough enough that a technically capable reader could reproduce the core procedure independently. But for a piece whose central claim is reproducibility - fixed seeds, deterministic sequences, "every result is fully reproducible by running the attached script" - publishing without the script creates a gap between the claim and the deliverable. The editorial board should consider whether the piece goes out without the artifact, or whether the script can be attached before publication. This is an editorial judgment call, not a reason to hold the paper in review.

3. **All remaining limitations are properly qualified.** The single-seed limitation, the 200-bootstrap count, the bootstrap misclassification at the boundary, the under-resolved i.i.d. control, and the football-network absence are all named and appropriately scoped. None of these rise to concerns requiring revision.
