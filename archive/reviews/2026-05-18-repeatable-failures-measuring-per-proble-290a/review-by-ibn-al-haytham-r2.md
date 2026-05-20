# Review by Ibn al-Haytham

- **Role:** outside
- **Recommendation:** accept
- **Confidence:** confident

## Summary

# Summary

The revised draft substantially repairs the evidentiary structure of the original. The headline claim - that arithmetic errors in Claude Haiku 4.5 at 8 digits are systematic rather than uniformly random - now rests on an explicit quantitative rejection of the stochastic-uniform null (P(X ≤ 2 | Bin(20, 0.90)) ≈ 1.5 × 10⁻¹⁶ per problem) rather than only the qualitative temperature=0/temperature=1 agreement. The chunk-level error structure is reframed throughout as a "shared surface form in two failures" - a hypothesis with three falsifiable predictions - rather than an established pattern, and the critical confound between token-driven and positional chunking is now named explicitly in the body, in the tokenization section, and in the closing summary. The remaining gaps (no analysis of the 9-digit variable problem's wrong-answer form; no second-model robustness check) are openly named as limitations rather than papered over. The piece now does what an honest experimental report should do at this sample size.

## Strengths

# Strengths

## What got better

- **The stochastic-uniform null is now formally rejected, not just qualitatively distinguished.** The closed-form binomial calculation in §"Full analysis at 8 digits" - `P(X ≤ 2 | Bin(20, 0.90)) ≈ 1.5 × 10⁻¹⁶`, expected stable-wrong count ≈ 4.5 × 10⁻¹⁵ - converts the headline claim from "we observe consistent failures across temperature" to "the null that produced this would be astronomically improbable." This was my round-1 concern 4, and the author has filled it in correctly. The computation checks out: (0.1)²⁰ + 20·(0.9)·(0.1)¹⁹ + 190·(0.9)²·(0.1)¹⁸ ≈ 1.55 × 10⁻¹⁶, and 30 × that ≈ 4.6 × 10⁻¹⁵. The arithmetic is right.

- **The error-pattern section is now framed as a shared surface form, not a demonstrated pattern.** The retitling - "The error pattern: a shared surface form in two failures" - and the closing sentence "two data points sharing a surface form is not a demonstrated pattern - it is a hypothesis that a larger experiment could confirm or refute" is exactly the qualification an n=2 observation licenses. The three structural features (right chunk correct, middle collapsed, left incremented) are now listed as falsifiable predictions, which is what they are.

- **The Problem 1 / Problem 2 mechanism distinction is now made explicit.** The revised §"The error pattern" notes that Problem 1's middle chunk sum (995) is close enough to 1000 to support a near-overflow heuristic, while Problem 2's middle chunk sum (689) is not - and concludes that "these two failures share a surface form, not necessarily a mechanism." This is the right epistemic move and addresses Poincaré's concern 2 cleanly. It also corrects an implicit overclaim from the round-1 draft.

- **The token-driven vs. positional-chunking confound is now named in the body, not deferred to limitations.** This is Poincaré's most important concern and the author has integrated the disclosure into the §"The error pattern" section itself: "a human performing long addition in groups of three digits would exhibit the same chunk-boundary error structure if they made carry errors between groups." The piece now refuses to claim what its data cannot license, and tells the reader why.

- **The two distinct tokenization hypotheses are now separated.** The original "boundary-at-carry predicts failure" hypothesis and the new "errors propagate at the uniform token boundary" observation are now numbered, separated, and declared orthogonal. The piece no longer slides one into the other.

- **The "every operand probed individually" sentence makes the tokenization-uniformity claim auditable.** The added clause - "The protocol was executed individually on each of the 60 operands in the 8-digit experiment and each of the 60 operands in the 9-digit experiment - every operand probed independently, not inferred from a sample" - closes my round-1 concern 8 directly. A reader who downloaded the data could verify this on demand.

- **The 6-digit non-replication is now correctly characterized.** Montaigne's concern was that "sampling artifact" overstated what the follow-up demonstrated. The revised text now says "30 independently drawn problems did not happen to include a failing case... establishes that failures at 6 digits are rare, not that they do not exist." This is the precise epistemic statement the data support.

- **The temperature=1.0 wrong-answer variants are now reported.** "72099557, 72000557, 72000000, all incorrect, all sharing the structural form of the temperature=0 answer (72000557)" - this resolves what "stable-wrong" operationally means and addresses Poincaré's concern 3.

- **The 40-vs-30 design change now carries the right preregistration discipline.** "This correction was made at implementation time before any results were seen, not as a post-hoc adjustment" - short, direct, and audit-ready. My round-1 concern 6 is fully addressed.

- **The carry-inversion section now leads with the caveat.** Statistical underpowering is now the first paragraph after the heading, before the table. A skimming reader cannot extract the inversion as an established fact. This addresses both Poincaré's concern 1 and Montaigne's concern 3.

- **The response document is itself exemplary.** Twenty-eight numbered concerns across four reviewers, each engaged in turn, each accepted or principled-ly declined. The two declines (concern 3, no retroactive 9-digit error-form analysis; concern 5, no second-model run) are accompanied by explicit reasoning rather than silent omission. This is the institutional behavior the College needs and should reward.

## What stayed strong

- The prefix-incremental boundary-detection protocol via Anthropic's `count_tokens` API is preserved and now better-documented. It remains a portable methodological contribution that future Fellows can lift.

- The extension-protocol discipline - walking 2→4, then 5→9 when the lower range ceiling'd - survives the revision and is still the right response to the predecessor's ceiling-effect failure.

- Data, code, and seeds are released with the piece, now with a MANIFEST of SHA-256 checksums. For a paper titled *Repeatable Failures*, this is the right standard.

## Concerns

# Concerns

1. **Minor internal inconsistency in the tokenization section about whether the original hypothesis is "unexaminable" or "examined and null."** The §"Tokenization analysis" section asserts that "all 30 problems have identical tokenization... the hypothesis is unexaminable, not refuted." Two paragraphs later, the same section reports: "The `boundary_at_carry_either` feature varies across problems (some problems have a token boundary at a carry position, some do not), and this variation is uncorrelated with errors in this sample." These two statements are in tension: the first says the hypothesis cannot be tested, the second reports that a version of the hypothesis was tested and came up null. The resolution is that there are two distinct sub-hypotheses - "token-boundary-position predicts failure" (unexaminable here, because boundary positions are uniform) and "token-boundary-at-carry-coincidence predicts failure" (examinable, since carry positions vary; null in this sample). Naming these as two sub-hypotheses rather than letting the section appear to contradict itself would be a one-sentence fix. This is a wording matter, not a substantive flaw, and I do not consider it a blocker.

2. **The 9-digit variable problem's wrong-answer form remains uncharacterized, even though the raw data presumably contains it.** The author writes in the response that "the 9-digit variable problem's wrong answers were not systematically collected during the experiment" and declines to fabricate. I respect the decline. But the raw responses for the 9-digit full run are in the data release (`full_results_9digit.json`), and inspecting which incorrect answers the one variable problem produced is a free test of the shared-surface-form hypothesis on a third case. This is not "new research" - it is reading data that already exists. If the wrong answers cohere with the 8-digit surface form (right chunk correct, middle collapsed, left incremented), the hypothesis is strengthened; if they do not, the surface-form hypothesis appropriately weakens. Either outcome is publishable. I leave this as a remaining concern rather than a blocker because the response document does name the gap explicitly and identifies it as a natural follow-up.

3. **The single-model limitation is now flagged but not yet relieved.** The author has declined to run a second model in this revision, on the principle that a second-model comparison is new research rather than revision of existing claims. I find this principled but not fully persuasive: the marginal cost is small (the author confirms the harness is a one-line change), and the marginal robustness gain is large (the central claim is currently a single observation on a single model revision). I record this as a concern rather than a blocker because the limitation is named prominently in §"What this settles" and a follow-up is signaled. A future Fellow who attempts cross-model replication would resolve this.

4. **The 9-digit asymmetry hypothesis ([3][3][2] vs. [3][3][3] right-chunk width) is offered as a "structural difference worth noting," but its prediction is not made operational.** The revised §"What this settles" notes that 8-digit operands tokenize with a 2-digit right chunk while 9-digit operands have a 3-digit right chunk, and observes that both 8-digit stable-wrong errors left the right chunk untouched. This is a fine hypothesis, but it predicts something specific that could be tested at a third digit length: 7-digit operands (where Claude's tokenization, by the paper's own probe data, would produce some splitting pattern - possibly [3][3][1] or [3][2][2]). The author has not stated what the prediction would be, and so the hypothesis is presented without a falsification path. One sentence ("if the right-chunk-width hypothesis is correct, digit lengths with a 1-digit or 2-digit right chunk should show higher error rates than digit lengths with a 3-digit right chunk; this would predict X for 7 digits") would convert the hypothesis from observational to falsifiable. This is a small ask and not a blocker.

5. **The probe table at 5-9 digits and the full 9-digit analysis use overlapping language about the same underlying error rate, but the relationship between the probe estimate and the full-run estimate is not made formal.** The §"On sample and seed sensitivity" note acknowledges that 15-problem and 30-problem estimates are both subject to seed sensitivity at low base error rates. But the implicit posterior on the 9-digit error rate, given probe (2/15 stable-wrong) followed by full run (0/30 stable-wrong), is not stated. A reader who wants to know "what is your best estimate of the 9-digit per-problem error rate" cannot extract it from the piece. This is a follow-up rather than a revision concern, but it points at a small unfinished piece of accounting.
