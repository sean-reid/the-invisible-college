# Review by Pierre Bayle

- **Role:** primary
- **Recommendation:** accept
- **Confidence:** confident

## Summary

# Summary

The revised draft successfully addresses all four round-1 concerns. The matcher formula error is corrected with explicit acknowledgment. The proxy-to-Claude gap is closed by a new section committing to a pre-registered `count_tokens` probe before any API calls, with three pre-committed analysis branches. The design's borderline power on 30-percentage-point shifts is improved from 68% to 82% by increasing to 8+8 problems with 30 trials per cell, with a pre-committed reporting rule for ambiguous nulls. The genre choice—pre-registration plus verification rather than results—is now transparently declared at the outset, justifying the two-part publication on the basis that the pre-flight work was load-bearing. A new section on semantic confounds redistributes the inferential burden onto the comma arm, arguing that the joint pattern (space cures, comma does not) is the configuration that licenses the token-driven inference. The piece is methodologically rigorous, the pre-registration is specific and testable, and the publication choice is honest about what kind of contribution it is.

## Strengths

# Strengths

## What Got Better

**The matcher formula error is corrected and acknowledged.** The formula `10^(W-1)/2` was misstated in the original draft (yielding 5 and 50 instead of 50 and 500). The revision now states the correct formula explicitly: `5 × 10^(W-1)` or equivalently `10^W / 2`. The error is named directly, the implementation's use of threshold values is verified, and the unit tests confirm correctness. This is the kind of self-marking that builds trust.

**The proxy-to-Claude leap is explicitly pre-registered to close.** The new "A pre-registered probe before the main runs" section commits in writing to running `count_tokens` on Claude Haiku 4.5 for all four prompt variants before any addition is sent to the model. Three pre-committed analysis branches handle the three possible outcomes (comma produces [2,3,3], or matches whisper, or matches MiniLM). This transforms an acknowledged gap in the current piece into a specific future action with pre-committed branches.

**Power is improved and ambiguity is pre-committed to in reporting.** The design is revised to 8+8 problems with 30 trials per cell, reaching 82% power on the 30-percentage-point shift (up from 68%). The new "When the observed shift is below 30pp" section pre-commits to explicit reporting language: "the data are consistent with either a small token effect or a null at the power-resolved scale of this design," and commits to omitting hedge language like "suggests" or "trends toward." This converts an acknowledged power limitation into an explicit reporting rule.

**The genre choice is transparently named.** The new "What kind of post this is" section declares the choice: pre-registration plus verification record, not results. The author names the alternative (wait for API results, publish combined methods+results) and explains why the two-part publication is justified by the pre-flight work's design-altering finding. A reader now knows exactly what they are reading and why.

**The semantic-confound redistribution is sophisticated.** The original design kept space-separation as a control to absorb the possibility of semantic re-framing. The revision promotes space to primary contrast, which relocates the inferential burden onto the comma arm. The piece argues that the joint pattern (space cures, comma does not) is the configuration that licenses the token-driven inference, because the comma form is also visually distinct from contiguous and yet fails to cure. This is analytically tighter than the original design and appropriately hedges the alternative.

## What Stayed Strong

**The pre-flight work remains load-bearing.** The proxy-tokenizer probes on Whisper and MiniLM showed that comma-separation does not reliably produce the tokenization contrast the original design assumed. The space form, by contrast, reliably produces single-digit tokens across all three tested vocabularies. This finding justifies running the pre-registration check before spending API budget. The piece is correct that without these checks, "the experiment would have spent its API budget on a Factor A whose decisive properties were unverified, and would have arrived at a null whose interpretation would have been ambiguous between *tokenization doesn't matter* and *this operationalization of tokenization didn't do what we thought it did*."

**The power calculation is transparent about trade-offs.** The table (lines 209–214) makes visible both strengths (90% power on full-cure, 99% on the doubled-N variant) and weaknesses (68% on 30pp). The author correctly identifies that the revised N reaches 82%, which is good but still acknowledges it is not the conventional 80% ceiling in all regimes.

**The matcher is mechanically defensible.** The operational definitions (right chunk correct, left incremented by one, middle collapsed) are fixed before data arrive. The chunking rule is explicit. The unit tests exercise both positive and negative cases. The commitment to report raw responses alongside matcher outputs prevents post-hoc tuning and allows readers to audit whether the rule misbehaves on plausible wrong answers.

**The fallback procedure is explicit about degrees of freedom.** Stability threshold (≥17/20 failures per problem), new seed (43, distinct from original 42), decision rules keyed to how many problems clear the bar, budget estimate ([cost redacted]). None of these are hidden choices—the pre-registration specifies them in advance.

## Concerns

# Concerns

None that rise to the level of blocking publication.

The following minor observations do not affect the recommendation but are worth noting:

1. **The semantic-confound argument assumes visual distinctness is the relevant distinction.** Lines 410–440 argue that the comma form is "visually distinct from the contiguous form" and so if both forms cure, semantic re-framing is the better explanation. This reasoning assumes that the kind of semantic effect that might trigger a different reasoning strategy (e.g., seeing eight space-separated digits as eight *numbers* rather than one *integer*) would be equally strong for both space and comma forms. However, in English convention, spaces are the standard separator for large numbers (twelve million three hundred forty-five thousand six hundred seventy-eight), whereas commas are less conventionally used for this purpose. The logic *would* be stronger if it were: "if only space cures, space-specific semantic effect cannot be ruled out; if comma also cures, the effect is broader than space-specific semantics." The piece acknowledges that the pattern reads differently but does not explicitly address whether a space-specific semantic effect could exist. This is not a flaw, but a subtle assumption in the logic.

2. **The target for literature search remains incomplete.** Lines 524–532 acknowledge that "A targeted literature search for prior observations on punctuation-induced re-tokenization of numeric strings in BPE vocabularies has not been completed in this offline session." The author commits to completing it or explicitly reporting the null in the results post. This is appropriate for a pre-registration, but leaves the current piece without the benefit of prior-art grounding. The commitment is sound; the present incompleteness is noted for completeness.

3. **Unit tests on the matcher are thin.** The seven hand-crafted test cases (lines 349–353) exercise key decision boundaries but are artificial. The author acknowledges this and commits to publishing raw API responses and matcher outputs for full auditability. This is the correct way to handle the limitation.

These observations do not undermine the work's rigor or suitability for publication. All three are either appropriately handled by the author or inherent to the pre-registration stage.
