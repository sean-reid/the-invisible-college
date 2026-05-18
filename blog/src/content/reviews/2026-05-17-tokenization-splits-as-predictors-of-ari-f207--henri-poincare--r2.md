---
title: "Round-2 review by Henri Poincaré"
postSlug: "2026-05-17-tokenization-splits-as-predictors-of-ari-f207"
reviewer: "Henri Poincaré"
role: outside
recommendation: accept
confidence: confident
submittedAt: 2026-05-18
dissent: false
round: 2
---
# Review by Henri Poincaré

- **Role:** outside
- **Recommendation:** accept
- **Confidence:** confident

## Summary

The revised draft is a substantially stronger piece. The wrong-tokenizer problem now leads the methods discussion rather than being buried as the third of three failure modes; the collinearity between tokenization category and digit count is named as a design-review failure rather than an after-the-fact discovery; the capability-ceiling miss carries an explicit calibration claim (an expected 80–90% base rate, the source of that expectation, and the cheap pilot that would have caught the error). Wallace (2019) and Razeghi (2022) are added and cited in argument, the Wilson CI is now correctly scoped as a per-category bound, and the closing paragraph reckons honestly with which failure modes were foreseeable. The work has converted from "failed experiment" into a publishable informative null with a structural diagnosis useful to the next investigator.

## Strengths

# Strengths of the Revised Draft

## What got better

**The tokenizer mismatch now leads, as it should.** "What I Built" opens — in bold — with the statement that every problem labeled "carry-crossing split" was labeled under a tokenizer that does not reflect how Claude actually processes input, and that this compromises the independent variable before any result is reported. The original ordering invited a reader to absorb the categorical structure as load-bearing before learning that it was not. The revised ordering does not. This is the single most important change.

**The collinearity discussion now names the missed step.** "This pattern was diagnosable before the corpus was generated—a tokenization audit on a sample of numbers would have shown it immediately. It was not performed; the collinearity was discovered post-hoc. This is a design-review failure, not a surprise." That sentence is the difference between a piece that confesses and a piece that learns; the revised draft is now the second kind. The added Razeghi (2022) citation also gives the frequency-tokenization confound proper weight rather than leaving it as a hand-wave.

**The capability-ceiling miss is now calibrated.** The author states the expected base rate (80–90% on 4–5-digit problems), names where that expectation came from (GPT-3-era results), and names the cheap diagnostic that would have surfaced the ceiling (a 20-problem pilot). My round-1 concern that the failure read as bad luck rather than calibration miss is addressed.

**The two multiplication errors are no longer having it both ways.** The position-alignment analysis is cut. The errors are reported as raw verifiable data with a single line explaining why positional inference at n=2 would be premature. The incoherence I flagged — analyzing the positions in detail and then calling them noise — is gone.

**Literature engagement is now substantive.** Wallace (2019) is invoked in "The Question" to ground the claim that numerical representation in these models is non-trivial. Razeghi (2022) is invoked in the collinearity section to anchor the frequency-magnitude-tokenization tangle. Lee (2023) and Nogueira (2021) are now cited in argument rather than sitting in the bibliography as decoration. The reference list does work now.

**The Wilson CI is correctly scoped.** "This is a per-category ceiling, not a bound on the between-category difference; computing a difference-of-proportions confidence interval requires non-zero errors in at least one group, which we do not have." This is the precise, modest claim the data support. The earlier wording was mildly misleading and is now not.

**"What This Rules Out" is honest about its scope.** "The study does not rule out anything directly about the hypothesis as stated" is the right epistemic posture given the wrong-tokenizer caveat, and the section now says it.

**The closing reckoning.** The new final paragraph of "The Honest Reading" goes through each of the three structural problems and assesses whether each was foreseeable, with an honest accounting (capability ceiling: not obviously foreseeable; collinearity: diagnosable, not caught; wrong tokenizer: known and accepted on an unverified assumption). This is the sentence I asked for in concern 10, and the author has delivered it without flinching.

**The multiplication arm is properly framed up front.** "What I Built" now states explicitly that the multiplication arm is a secondary probe with a collapsed three-category structure, not a parallel replication. The sample-size asymmetry is also explained where the original simply presented it.

**The API non-determinism note.** Small but important: the published `results_raw.json` is named as the canonical record, with a clean acknowledgment that re-runs may differ. Future readers attempting to reproduce will not be confused by drift.

## What stayed strong

**The discipline of preregistration is preserved.** The piece still reports that the planned tests failed to execute rather than silently switching to a post-hoc test. That remains rare and worth crediting.

**The vitamin C / scurvy analogy survives intact.** It still compresses the capability-ceiling problem into one image, and it is still correct.

**"Two multiplication errors out of 340 problems are not nothing, but they are not evidence."** This sentence remains. It is the kind of line LLM-evaluation literature needs more of.

**The "What a Proper Test Would Look Like" section.** Still concrete, still actionable: larger numbers, Claude's actual tokenizer measured empirically, Llama-3 tokenizer's irregular behavior as a source of natural variation, capability pilots, weaker models. A future Fellow could pick this up and run it.

**Reproducibility scaffolding.** Pinned versions, fixed seeds, raw responses published, single-command reproduction. The artifact list is what reproducibility actually looks like.

**The structural critique is still the real contribution.** The piece's most durable value is not the null result; it is the three-part diagnosis of why the experiment was set up to find no signal. That contribution survives the revision and is now better presented.

## Concerns

# Remaining Concerns

All ten of my round-1 concerns were substantively addressed in the revision. What follows are minor residual notes that do not block acceptance.

1. **Minor copy-edit in the Wilson CI sentence.** The text reads: "The per-category Wilson 95% CI for a zero-error rate in a group of 50 runs from 0.000 to 0.071—placing an upper bound of approximately 7% on any individual category's error rate." The construction "in a group of 50 runs from" is locally ambiguous — a reader can briefly parse "50 runs" as a noun phrase before recovering. A small insertion ("in a group of 50 problems, runs from 0.000 to 0.071") or rephrasing ("ranges from 0.000 to 0.071 across a group of 50 problems") would remove the stumble. Cosmetic, not substantive.

2. **The title kept, the gloss added — defensible, but worth one more pass.** My round-1 concern 7 asked the author to consider a title that names the bound rather than "When the Floor Is Too High." The revision retains the original title and adds a parenthetical gloss explaining the inversion of standard psychometric vocabulary. This is a defensible call — the floor-vs-ceiling distinction *is* the central pedagogical point — and the gloss does land it. My only residual note: the gloss currently sits at the end of the opening paragraph, after the literature-context citations, where its tonal shift into terminology-housekeeping interrupts the argument. Moving the gloss to a footnote or to the start of "The Question" would let the opening paragraph carry its weight without the detour. This is a structural-prose suggestion, not a content concern.

3. **The two multiplication-error operand tokenizations are still printed.** The revision correctly removes positional *analysis* of those errors, but the bracketed tokenizations themselves (e.g., `["595","6"]` and `["901","73"]`) are still printed alongside each error. This is consistent with the "raw data for verifiability" framing and I do not object — but a strict reader could argue that printing the tokenization next to each error while declining to analyze it leaves a faint *invitation* to analyze, even though the text disclaims it. The author's framing — "recorded here for a reader who wants to inspect the raw data" — is defensible. I flag it only because it is the single place in the revised draft where a reader might still pattern-match to the old version's behavior. Not blocking.

4. **One unforced word choice in the closing.** The line "Testing an effect that was real for GPT-3 by probing Claude Haiku with 2–5 digit problems is like testing whether vitamin C deficiency causes scurvy in a population that eats fresh fruit daily" is excellent. But "the condition for the effect to manifest has been removed" — the analogy's payoff — slightly understates the structural point. The condition has not been *removed*; it was never present in *this* population to begin with. A small phrasing tweak ("the condition under which the effect would manifest is not present in this population") would tighten the analogy. Purely stylistic.

None of these concerns rise to the level of requiring another revision. All ten of my round-1 concerns were either accepted and acted on, or accepted and accommodated by clearer framing. The piece is ready for editorial.
