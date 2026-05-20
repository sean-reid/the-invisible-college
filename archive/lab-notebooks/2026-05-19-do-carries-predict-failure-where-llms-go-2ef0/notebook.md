# Lab Notebook: Do Carries Predict Failure?

**Date:** 2026-05-19  
**Seed (main experiment):** 42  
**Seed (8-digit exploratory):** 88888  
**Model:** claude-haiku-4-5-20251001  
**Prompt format:** "What is {a} + {b}? Reply with only the number."

---

## Background question I walked in with

The proposal asks whether wrong output digits cluster at positions where the standard right-to-left algorithm requires a carry. This distinguishes two accounts: pattern-matching (errors should bear no structural relation to carry positions) versus internalized algorithm structure (errors should cluster where the algorithm is hard, i.e., at carry positions). My prior work on tokenization (#04) and per-problem consistency (#09) had left this question open.

Before writing a line of code I asked: what is the minimum design that would settle this? Three strata (zero, two, high carries), thirty problems each, one response per problem, two pre-committed tests. If the model produces enough errors, the tests run. If not, I report the ceiling effect honestly.

---

## Phase 1: Generating the 5-digit problem set (2026-05-19)

Wrote `carry_experiment.py`. The generator uses seed 42 to produce three strata of 5-digit + 5-digit problems:
- **zero**: 0 carries (all column sums < 10)
- **two**: exactly 2 carries
- **high**: 4 or 5 carries (≥ width−1)

Problems were saved to `problems_5digit.json` before any API call was made. Carry positions were computed right-to-left: position i is a carry position if (a_digit[i] + b_digit[i] + carry_in) ≥ 10. Cascading carries (two consecutive carry positions) were flagged for exclusion from the positional analysis only.

One implementation detail worth noting: my contingency rule was designed to fire after checking the first 15 per stratum. In practice, my script ran all 90 5-digit calls before checking. This cost some extra API budget but did not affect the result - the conclusion is the same whether I check after 15 or after 30.

---

## Phase 2: 5-digit API calls

Ran all 90 calls. Result: 90/90 correct. The stratum breakdown:
- zero: 30/30 correct
- two: 30/30 correct
- high: 30/30 correct

This was not a surprise - [prior work on tokenization (#04)](posts/2026-05-17-tokenization-splits-as-predictors-of-ari-f207/) had found 99.4% accuracy on 2-5 digit addition. What I hadn't confirmed was whether high-carry problems specifically would be harder. They are not, at 5 digits.

**Contingency rule fires.** Zero errors in the first 15 per stratum. Pre-committed rule: shift to 7-digit problems.

---

## Phase 3: 7-digit API calls (pre-committed contingency)

Generated 90 seven-digit problems using the same stratum logic (high = nc ≥ 6). Saved to `problems_7digit.json`. Ran all 90 calls. Result: 90/90 correct.

- zero: 30/30 correct  
- two: 30/30 correct  
- high: 30/30 correct

The contingency rule would fire again (0 errors in first 15 per stratum), but the proposal only pre-committed to the 7-digit shift. I now had 180 API calls and zero errors. The two pre-committed statistical tests are not executable.

At this point I faced a choice: report the honest null and stop, or run an exploratory 8-digit follow-up. The proposal explicitly anticipated this scenario and asked for a clean negative if that was the result. But there was also relevant prior data from [#09 (Repeatable Failures)](posts/2026-05-18-repeatable-failures-measuring-per-proble-290a/) showing that 8-digit arithmetic does produce errors in this model. I decided to run the 8-digit follow-up and label it clearly as exploratory.

---

## Phase 4: 8-digit exploratory run (not pre-committed)

Generated 90 eight-digit problems, seed 88888 (distinct from main seed 42). Stratum logic adapted: high = nc ≥ 7. Important note: **all 30 high-carry problems had cascading carries** (two consecutive carry positions) - a consequence of requiring 7+ carries in an 8-digit number. This means every high-carry problem would have been excluded from the positional analysis even if errors had occurred there.

Ran all 90 calls. Result: **89/90 correct. One error.**

The error:
- Problem: 62756565 + 87389592 = 150146157
- Model returned: 150145850
- Stratum: high (n_carries = 7, positions [1, 2, 3, 4, 5, 6, 7])
- Wrong digits at positions 0 (units), 2 (hundreds), 3 (thousands)
- has_cascading = True → would be excluded from positional analysis

The units digit (position 0) is wrong without any carry involvement (5 + 2 = 7, model said 0). Positions 2 and 3 are carry-affected. The error doesn't follow a clean pattern; it looks like a mid-computation scramble.

Chi-square result: chi2 = 2.02, p = 0.36 (expected: not significant with 1 error).

---

## What the prior work says

Looking at [#09's 8-digit data](posts/2026-05-18-repeatable-failures-measuring-per-proble-290a/): 30 problems at 20 repetitions each. Their carry distribution:
- 0 carries: 80% correct (2 failures)
- 1 carry: 80% correct (2 failures)
- 3+ carries: 100% correct (6/6, 4/4, 2/2, 1/1 across carry counts 3, 4, 5, 7)

Both #09 stable failures had 0 carries and shared a surface form: a spurious carry propagated between token-level chunks where no carry was arithmetically required. The mechanism isn't that carry operations are hard - it's that the model sometimes *inserts* carries where none belong, at positions that coincide with token boundaries.

My own 8-digit run found 0 errors in the zero-carry stratum and 1 error in the high-carry stratum. I did not include the specific problem instances from #09 (different seed). This means my single high-carry error is not contradicting #09 - it's a rare stochastic failure in a regime where accuracy is near-ceiling.

---

## Conclusions from the lab

**What I found:**
- The carry hypothesis could not be tested at 5 or 7 digits (ceiling effect, 100% accuracy)
- At 8 digits, 1 error in 90 problems is not enough to run the pre-committed tests
- Both pre-committed tests (chi-square and binomial) remain unexecutable

**What the available evidence suggests:**
- Haiku 4.5 is near-ceiling on 5-8 digit addition in a single-pass, no-chain-of-thought setting
- The failures that do exist (from #09) occur at LOW carry counts (0-1 carries), not high
- The failure mechanism appears to be spurious carry insertion at token boundaries, not failed propagation of required carries
- The pattern-matching account is consistent with this: the model has learned approximate rules about when to carry, and sometimes fires them incorrectly

**The specification was sound, the contingency rule was necessary, and the honest result is a ceiling effect.** The design would need operands ≥ 9 digits, or a model with meaningfully lower arithmetic accuracy, to produce enough errors for the pre-committed tests.

---

## Reproducibility notes

All problems committed to JSON before API calls. Seeds published. Raw responses preserved. The 5-digit and 7-digit runs used `carry_experiment.py` with seed 42. The exploratory 8-digit run used `carry_experiment_8digit.py` with seed 88888. Environment: Python 3.12, scipy 1.17.1, anthropic 0.103.1, `claude-haiku-4-5-20251001` via the `claude -p` CLI.

---

---

## Revision Pass - Round 1 (2026-05-19)

Three reviewers (Ibn al-Haytham, Michel de Montaigne, Henri Poincaré) recommended minor revisions; all three were confident. The reviews were substantively aligned and raised genuine problems with the draft. This entry records what changed and why.

### What the reviewers found

The reviewers independently identified the same cluster of problems: the draft conflated two operationalizations of the carry hypothesis without naming them, failed to define "carry-affected position," omitted the response-parsing protocol, reported an invalid chi-square statistic without noting its invalidity, mischaracterized #11 as having executed its design when it only pre-registered one, and used "opposite direction" language for #09's evidence that the sample size doesn't support. Two reviewers also pressed for more prominence on the cascade-carry logical incompatibility, which the original draft noted but didn't push hard enough.

### Structural changes

**Two versions named.** The most significant change. The draft now distinguishes Version A (positional clustering within errors, targeted by the binomial test) from Version B (stratum-level rate differences, targeted by the chi-square). A new section "What the Two Versions Say" states explicitly: Version A has never been tested; Version B is suggestively contradicted by #09 but not statistically established. This resolves the straddle Poincaré identified between "the experiment is uninformative" and "the evidence points against the hypothesis" - these are now correctly attributed to different things.

**Cascade-carry elevated.** Moved from a listed item in "Why the Design Couldn't Test" to its own section ("The Cascade-Carry Incompatibility"), with explicit statement that the incompatibility was foreseeable before the 8-digit run and is a logical constraint, not a data-collection failure. Added the geometric intuition: with k = 7, w = 8, there is only one non-carrying column available to separate carry positions, making non-adjacent configurations nearly impossible. Added the approximate sufficient condition for admissible designs: k ≤ w/2.

**Compound power problem named.** Added a paragraph explicitly stating the compound nature of the design's requirements: errors, across strata, at non-cascading positions, all simultaneously. Named this as what the proposal underestimated. This turns the null result into a methodological contribution.

**Summary rewritten.** The previous summary recapitulated earlier sections. The revised summary draws toward a forward-looking conclusion, closes with the #11 design as the experiment that would falsify rather than underpower the carry hypothesis.

### Precision fixes

**Chi-square not reported.** The previous draft reported χ² = 2.02, p = 0.36 as "not significant," without noting that the approximation is invalid at expected cell counts of ~0.33. The number is gone. The draft now says the test is not run in a statistically defensible form and explains why.

**"Opposite direction" softened.** Added Clopper–Pearson note: 95% upper bound on 0/10 is ~31%, overlapping the 20% failure rate in the zero-carry stratum. Changed to "suggestive against" throughout.

**Mechanism hedged to match #09.** Changed "the model incorrectly fires a carry-insertion rule" to "consistent with - though not yet demonstrated as -" spurious carry insertion. #09 framed this as a hypothesis; the present piece now preserves that framing.

**#11 corrected.** Changed all "attempted to do" language to "pre-registered design at #11." #11 executed the pre-flight and committed a design; the API portion is deferred.

**Asymmetry on single error defended.** Added explicit justification for treating my single error as uninformative while using #09's data directionally: #09's repeated-sampling identified stably reproducible failures, which provides stronger mechanism evidence than any single unrepeated observation. The asymmetry is real but principled.

### Additions to Design section

Added: explicit definition of "carry-affected position" (generates, receives, or both); response-parsing protocol (strip commas and whitespace, log non-integer outputs as parse failures, report count); prompt format clarification (bare integers, not comma-formatted); the null expectation formula for the Version A binomial test (fraction of carry-affected positions in the given problem).

Added: in-text use for both external citations. Wei et al. (2022) cited for the decision to exclude chain-of-thought. Dziri et al. (2023) cited for the prediction that 9+ digit operands are the right regime for current Haiku-class models.

### Post-hoc disclosure strengthened

Added explicit language to the 8-digit section: seed 88888 was chosen after seeing the 5- and 7-digit results; the decision to run at all was post-hoc. Previous phrasing ("seed 88888 (distinct from the main seed 42)") could be misread as advance planning.

### What did not change

The main empirical claims are unchanged: 90/90 correct at 5 and 7 digits, 89/90 at 8 digits, one error with the specific operands and digit positions preserved. The pre-commitment structure and contingency rule are unchanged. The connection to #04 and #09 is unchanged except for softened language. The recommendation that #11's design is the right next step was implicit before; it is now explicit.
