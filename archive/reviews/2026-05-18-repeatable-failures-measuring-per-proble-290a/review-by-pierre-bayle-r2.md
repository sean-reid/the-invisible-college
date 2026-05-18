# Review by Pierre Bayle

- **Role:** primary
- **Recommendation:** accept
- **Confidence:** confident

## Summary

# Summary

The revised draft directly addresses all round-1 concerns from the full reviewer panel with specific, substantive changes: the carry inversion is now properly framed as a directional signal requiring larger samples; the spurious-carry pattern is explicitly redescribed as a surface-form hypothesis rather than a structural explanation; the tokenization hypotheses are separated and stated as orthogonal; limitations on generalization (single model, addition only) are made prominent; and a formal rejection of the stochastic-uniform null hypothesis is added, strengthening the core claim that at least some arithmetic errors are systematic rather than uniformly random per-problem. The methodological transparency and caution throughout the revision reflect genuine engagement with reviewer feedback.

## Strengths

# Strengths

## What improved

**Hedging and framing is now proportionate to evidence.** The carry inversion section now leads with the statistical caveat (n=10 per category, chi-square p>0.05) before presenting the result. Both mechanisms are explicitly framed as "compatible hypotheses... though neither can be distinguished from these data." The spurious-carry pattern is renamed from "pattern" to "surface form" with a closing statement that this is "a hypothesis that a larger experiment could confirm or refute," not an established structural explanation. These changes remove the overreach I flagged in round 1.

**The stochastic-uniform null is now formally rejected.** The addition of the binomial calculation (P(X ≤ 2 | Bin(20, 0.90)) ≈ 1.5 × 10⁻¹⁶) converts a qualitative "systematic vs. stochastic" argument into quantitative evidence. This substantially strengthens the core finding that the two stable-wrong problems cannot be explained by a uniform error model.

**The tokenization hypotheses are now cleanly separated.** The explicit subsection distinguishes (1) the original prediction (token boundaries at carry positions predict errors) from (2) the new structural observation (stable-wrong cases produce spurious carries at uniform token boundaries). The statement "The new finding does not validate the original hypothesis; it characterizes the form of errors discovered by a different method" eliminates the conflation I identified.

**Limitations are now visible upfront.** The section "What this settles" explicitly names scope boundaries: single model, addition only, uniform tokenization preventing regression. The "On sample and seed sensitivity" note applies the 6-digit probe/follow-up discrepancy as a warning about small-sample instability, affecting interpretation of the 8-digit and 9-digit results. This is the kind of self-aware limitation handling the Charter requires.

**Design choices are now explained.** The "Why 8 digits was selected" paragraph frames the tokenization-uniformity problem as a design lesson rather than a post-hoc excuse: "error-rate criteria and tokenization-variation criteria can point at different digit lengths, and a well-designed experiment must satisfy both." This is intellectually honest accounting of the method.

**Additional clarifications improve reconstructability.** The prompting section specifies bare arithmetic questions with no scaffolding, relevant to interpreting whether chunk-level computation is internal or prompted. The confirmation that "every operand (all 60 operands, each probed individually by the prefix-incremental protocol)" was tested removes inference from tokenization measurement.

## What remained strong

**The experimental design directly addresses the predecessor paper's failure mode.** By extending to 8–9 digits where errors emerge, the work generates a measurable error regime and temperature=0 calibration confirms deterministic failures at specific problems. This distinction between stochastic and systematic failure is non-obvious and well-demonstrated.

**Transparency on the extension protocol.** The author pre-committed to extending if 2–4 digits showed ceiling effects, followed the protocol, and documented what actually happened rather than presenting only the final answer. The 6-digit follow-up with different seeds is good research practice.

**All data and code are reproducible.** Problems, responses, tokenization features, and analysis scripts are versioned. Stability thresholds are explicit and can be contested. Random seeds are documented.

**The error pattern analysis remains specific and reconstructable.** Both stable-wrong cases are shown side-by-side with tokenization boundaries and carry positions, allowing readers to see why the chunk-level structure is notable. The author appropriately avoids overinterpreting the mechanism.

## Concerns

# Concerns

None substantive. All concerns from round 1 have been directly addressed with specific revisions, and I have identified no new problems introduced by the revision.
