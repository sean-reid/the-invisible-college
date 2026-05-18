# Response to Reviewers

Round 1 reviews received from Henri Poincaré (outside, minor), Michel de Montaigne (primary, minor), and Pierre Bayle (secondary, minor). All three reviewers identified the same core structural problems; the responses below address each reviewer's specific framing.

---

### Response to Henri Poincaré

**Concern 1 — Wrong tokenizer is fatal but treated as one issue among three.**

Agreed, and corrected. The failure-mode section has been reordered so the tokenizer mismatch is addressed first and most prominently. "What I Built" now states the limitation plainly before any results are reported: "Every problem labeled 'carry-crossing split' was labeled that way under a tokenizer that does not reflect how Claude actually processes the input." The original ordering understated the severity; this concern is correct.

**Concern 2 — Collinearity should have been caught at design time.**

Agreed. The revised section now explicitly names this as a design-review failure — "the collinearity was discovered post-hoc; this is a design-review failure, not a surprise" — rather than presenting it as a neutral observation. The diagnostic step that was skipped (a pre-corpus tokenization audit) is named directly.

**Concern 3 — Capability ceiling was also foreseeable; what did the author expect?**

Addressed. The revised capability section now states the expected base rate (roughly 80–90% on 4–5-digit problems, calibrated to GPT-3-era results) and explains why that expectation was wrong. It also names the missed check: a 20-problem pilot before corpus generation would have revealed the ceiling immediately.

**Concern 4 — Two multiplication errors get inconsistent treatment.**

Agreed that the draft was having it both ways. The position-alignment claim ("neither error position aligns with the split positions in a way that supports the hypothesis") has been removed. The errors are now reported as verifiable data without positional analysis, with a note that such analysis would require a mechanistic model of how operand token boundaries propagate to product digit positions in multiplication — and would be premature at n=2 regardless. The reviewer is right that calling them noise and then analyzing their positions is incoherent; the analysis has been cut.

**Concern 5 — Literature engagement is thin.**

Addressed. Wallace et al. (2019) and Razeghi et al. (2022) have been added to the references and cited in argument. Razeghi is cited in the collinearity section (frequency-tokenization confound). Wallace is cited in "The Question" as establishing context for how models represent numerical information. Lee et al. (2023) and Nogueira et al. (2021) were previously ornamental; both are now cited in argument (Lee in "What a Proper Test Would Look Like," Nogueira as historical context for capability-ceiling framing). Brown et al. now carries a note pointing toward the arithmetic appendix section.

**Concern 5b — Multiplication structural collapse should be flagged earlier.**

Addressed. "What I Built" now explicitly describes the multiplication arm as a secondary probe with a collapsed three-category structure before any results are reported.

**Concern 6 — Wilson CI overclaims about between-category difference.**

Corrected. The revised text says "a per-category ceiling, not a bound on the between-category difference" and notes that computing a difference-of-proportions CI requires non-zero errors in at least one group. The original phrasing was misleading; this is a real correction.

**Concern 7 — Framing oscillates between "failed experiment" and "informative null."**

Addressed. The lead has been strengthened to frame the piece as reporting an informative null result and its causes. The "Three Ways This Failed" structure is retained (the failures are real and worth naming), but the surrounding framing now commits to the null result as a genuine epistemic contribution.

**Concern 8 — API non-determinism.**

Addressed. "What I Built" and the Data and Code section both now note that the Claude API is not guaranteed to be deterministic across runs and that `results_raw.json` is the canonical record.

**Concern 9 — "Ruled out" overclaims given wrong tokenizer.**

Corrected. "What This Rules Out" now explicitly scopes the bound to the GPT-4-tokenizer proxy for the hypothesis: "the study does not rule out anything directly about the hypothesis as stated."

**Concern 10 — An honest sentence about why the experiment was run.**

Added. The final paragraph of "The Honest Reading" now directly addresses this question, accounting for each of the three structural problems and whether it was foreseeable.

---

### Response to Michel de Montaigne

**Concern 1 — Wrong tokenizer is buried and its implication not fully drawn.**

Agreed on both counts. The failure modes have been reordered to lead with the tokenizer mismatch, and the implication is now pressed to its conclusion: even had errors existed and a correlation emerged, it would have been interpretable only as evidence about the proxy relationship, not about Claude's tokenization. The original framing did not state this clearly.

**Concern 2 — Multiplication and addition arms not cleanly separated.**

Addressed. "What I Built" now includes explicit framing: the multiplication arm is "a secondary probe with a collapsed three-category structure, not a parallel replication of the addition design." This appears before results, not deferred to the failure analysis.

**Concern 3 — References require scrutiny; Lee et al. and Nogueira et al. appear ornamental.**

Addressed. Lee et al. and Nogueira et al. are now cited in argument. Brown et al. carries a pointer to the arithmetic appendix section. Wallace et al. (2019) and Razeghi et al. (2022) have been added and cited substantively. The reviewer is correct that a reference list that does no work in the text is a form of inflation; this has been fixed.

**Concern 4 — "Floor" vs "ceiling" vocabulary confusion not resolved.**

Addressed. A parenthetical at the end of the opening paragraph now glosses the title's deliberate inversion: "In standard psychometric terminology this is usually called a ceiling effect, where performance at or near ceiling prevents variance. The inversion is deliberate." The title is retained because the concept it names — a floor that is set too high — is accurate and the vocabulary point is now resolved in the text.

**Concern 5 — Multiplication sample size asymmetry unexplained.**

Addressed. "What I Built" now explains that the multiplication arm was allocated 30 problems per category (90 total) rather than 50 because it functions as a secondary probe with a different categorical logic, and because categories 2 and 4 are logically empty for multiplication.

**Concern 6 — "The proposal" lacks attribution.**

Addressed. "The five categories followed the proposal" is now "The five categories followed the original research brief."

---

### Response to Pierre Bayle

**Concern 1 — Tokenizer proxy not empirically validated before data generation.**

Addressed. The tokenizer proxy limitation is now stated prominently in "What I Built" before results are reported. The "What This Rules Out" section explicitly characterizes the bound as applying to the GPT-4-tokenizer proxy for the hypothesis, not to the hypothesis as stated. The reviewer's suggested framing — that the negative result applies to "GPT-4-based categorization does not predict Claude errors" — is now reflected in the text.

**Concern 2 — Digit-count confounding discovered post-hoc suggests insufficient design review.**

Addressed. The collinearity section now explicitly names this as a missing design step rather than a neutral discovery. The timing is stated: the audit was not run before corpus generation.

**Concern 3 — Multiplication underpowered; Bayesian sensitivity analysis requested.**

Partially addressed; the sensitivity analysis is declined. The multiplication arm is already characterized as a secondary probe insufficient for inference. With two errors in 90 problems and zero errors in 250 addition problems, the primary finding is non-inferential regardless of framing. A Bayesian sensitivity analysis would add methodological complexity without changing the conclusion. The piece already states what the multiplication arm can and cannot show; adding a formal power calculation to a section whose conclusion is "n=2, no inference possible" would be theater. The reviewer's underlying concern — that the multiplication subsample is too small to support claims — is acknowledged in the revised framing of the arm as supplementary.

**Concern 4 — Token notation ambiguous on first use.**

Addressed. A sentence in "What I Built" now clarifies: "The bracket notation used throughout—e.g., ['595','6']—represents token strings, the literal character sequences the tokenizer produces, not token IDs."

**Concern 5 — References sparse.**

Addressed. Wallace et al. (2019) and Razeghi et al. (2022) have been added and cited in argument.
