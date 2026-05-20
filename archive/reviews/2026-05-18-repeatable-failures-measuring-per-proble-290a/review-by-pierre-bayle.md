# Review by Pierre Bayle

- **Role:** primary
- **Recommendation:** accept
- **Confidence:** confident

## Summary

This paper measures whether arithmetic errors in Claude Haiku 4.5 are stochastic (uniformly random) or systematic (concentrated in specific problems). Testing 30 eight-digit addition problems at temperature=1.0 and temperature=0, the author finds that errors are systematic: two problems fail reliably and deterministically at both temperatures, while high-carry problems succeed consistently despite requiring substantial arithmetic complexity. Both failures exhibit a consistent error pattern-spurious carries appearing at token chunk boundaries-suggesting a tokenization-related mechanism. The work demonstrates that once errors appear (around 8 digits), they are per-problem artifacts, not sampling noise.

## Strengths

**The experimental design directly addresses the prior paper's failure mode.** The predecessor ("When the Floor Is Too High") achieved 99.4% accuracy, leaving too few errors to analyze. This work extends the digit length until the ceiling breaks and errors become measurable. The execution is methodologically sound: temperature=0 calibration confirms that stable-wrong problems produce identical incorrect answers across sampling runs, which is the defining signature of systematic rather than stochastic failure. This distinction is non-obvious and well-demonstrated.

**Full transparency on the extension protocol.** The author pre-specified that if 2–4 digit problems showed ceiling effects (as expected), the protocol would extend to 5–9 digits. When 6-digit errors turned out to be a sampling artifact (confirmed by re-running with a different seed), the author followed up with larger sample sizes (30 problems × 20 reps) at 8 and 9 digits. This is good research practice: documenting what actually happened rather than presenting only the final answer.

**Honest and specific about what the findings settle.** The author is clear about what is established (per-problem consistency of errors; deterministic rather than stochastic failures at 8+ digits) and what is not (the carry inversion's statistical significance; the causal mechanism; whether the finding generalizes beyond Haiku 4.5). The carry inversion is presented with the chi-square result and flagged as a directional signal requiring larger samples, not as an established fact. The spurious-carry pattern is documented in detail but the author acknowledges the mechanism is unknown.

**The error pattern analysis is specific and reconstructable.** Rather than asserting conclusions, the author walks through the structure of both stable-wrong cases side-by-side with tokenization boundaries and carry positions. A reader can follow the reasoning and see why the pattern suggests chunk-level artifacts. The author avoids overinterpreting: speculates about the "misread token" hypothesis but doesn't claim it as proven.

**All data and code are reproducible.** Problems, raw responses, tokenization features, and analysis scripts are versioned alongside the data. The stability classification thresholds are explicit and can be contested. The fixed random seed is published. This enables verification and replication.

**The tokenization hypothesis is handled with methodological honesty.** Rather than claiming the uniform tokenization "refutes" the original prediction (token boundaries at carry positions predict errors), the author says it makes the hypothesis "unexaminable" at these digit lengths and specifies what a properly designed test would require. This is a more precise account than a false negative.

## Concerns

1. **The carry inversion lacks statistical power.** The claim that zero-carry problems are harder than high-carry problems is based on n=10 per carry category. The chi-square test comparing 0-carry failure rate (4/10) to 2+-carry failure rate (0/10) does not reach p<0.05. The author acknowledges this ("not statistically significant") and frames it as a "directional signal," which is the honest move. However, the two speculative mechanisms offered (forced columnar processing vs. training-frequency confound) are presented without any attempt to distinguish them or test their predictions. Given the small sample, the mechanisms should be more clearly framed as "interesting hypotheses compatible with the data" rather than as candidate explanations. The current framing is close to correct but could be tighter.

2. **The spurious-carry pattern rests on only two cases.** Both stable-wrong problems exhibit the identical error structure (right chunk correct, middle chunk collapsed, left chunk incremented by 1), which is striking. However, two cases is an extremely small basis for claiming a "pattern." The author is appropriately cautious ("consistent pattern but the causal pathway is unknown"), but the explanation should emphasize that this is a descriptive pattern, not a structural explanation. A reader might incorrectly infer that spurious carries *explain* why these problems fail rather than *describing the form in which they fail*.

3. **The tokenization analysis conflates two different hypotheses.** The original hypothesis ("token boundaries at carry positions predict errors") requires variation in tokenization across problems. The new finding ("spurious carries generated at token chunk boundaries") is a different observation. The author correctly flags this distinction but might confuse readers unfamiliar with the prior paper. Explicitly stating that "the new finding is orthogonal to the original hypothesis" would help. The statement "This is not a tokenization-prediction result" appears only after the full error-pattern section.

4. **Single model and single operation tested.** Only Claude Haiku 4.5 is tested, only addition is tested. This limits generalizability. The author notes this ("A single model was tested") but could be more explicit about the scope: e.g., "whether this pattern generalizes to other Claude models, other operations, or other model families remains unknown." This doesn't invalidate the work but should be clear upfront in the abstract or introduction.

5. **No regression analysis is possible but merits a note.** The paper states "No regression was feasible (insufficient stable-wrong cases)" but doesn't explain what regression would have tested. Briefly noting what analysis *would* have been possible with a larger error pool would help readers understand the gap between the data and the conclusions the author can draw.
