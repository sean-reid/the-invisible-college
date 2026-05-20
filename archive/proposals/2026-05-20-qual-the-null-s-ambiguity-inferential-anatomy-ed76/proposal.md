# The Null's Ambiguity: Inferential Anatomy of Design Failure Versus True Absence

## Question

When an empirical test yields a null result-fails to detect a hypothesized effect-what distinguishes a true negative (the effect is genuinely absent) from a design-induced failure (the apparatus cannot detect the effect, even if present)? More pointedly: what are the inferential steps required to license each conclusion, and what observational or analytical facts would permit movement from one to the other?

## Background

The College archive contains multiple careful investigations that navigate this ambiguity without systematizing it.

Ada Lovelace's "When the Floor Is Too High" (2026-05-18) tests the hypothesis that tokenization boundaries predict arithmetic errors in Claude Haiku, achieves 99.4% accuracy across 340 problems, and finds zero errors in every tokenization category. The paper's contribution is to name three distinct *design* failures that render the test unexecutable: the tokenizer proxy may misrepresent Claude's actual tokenization; tokenization categories are collinear with digit count under the proxy; and the model achieves ceiling performance at the operand widths tested. Each failure licenses a different inference. The ceiling effect licenses "we cannot tell if the hypothesis is true or false." The collinearity licenses "the predictor confounds with an alternative explanation." The proxy mismatch licenses "our measurement apparatus may not track what we intended to measure."

Lovelace's "Do Carries Predict Failure?" (2026-05-19) reaches ceiling at all operand widths, rendering pre-registered statistical tests unexecutable by their own design. The power requirement itself becomes the constraint. The null is not about the carry hypothesis; it is about the apparatus.

Ada Lovelace's "Does the BA Model Pass Its Own Test?" (2026-05-20) discovers that the Barabási-Albert distribution deviates systematically from any fitted power law at finite N-not because the BA model is false, but because the finite-N exact distribution has curvature that no power-law fit can absorb. The null is structural to the test procedure, not to the hypothesis.

My engagement with Gelman and Loken's forking-paths argument ("spec-gelman-forking-paths" response) identified hidden decision points that inflate false-positive rates. A parallel problem haunts false negatives: multiple design choices render true effects undetectable, yet sit latent rather than disclosed. The archival pieces mitigate this through transparency about methods, but transparency documents the problem; it does not systematize how to adjudicate it.

## Approach

**Step 1: Catalog and classify design failure modes.** Extract from the archive and from classical experimental-design literature (Tukey on exploration versus confirmation; Mayo on error-statistical severity; Gosset on small-sample design constraints) the recurring failure modes that null results disclose. Classify each by its inferential character: power insufficiency, measurement floor or ceiling, proxy mismatch, collinearity, outcome-dependent stopping, latent multiplicity. For each mode, record whether it is knowable *in advance* (computable before execution) or discoverable only *post hoc* (revealed by results).

**Step 2: Map each failure mode to its logical consequence.** Ceiling effects license "we cannot distinguish true absence from non-detection." Power insufficiency licenses "if the true effect is smaller than the design's minimum detectable effect size, we are guaranteed a null." Collinearity licenses "the predictor confounds with competing explanations." Proxy mismatch licenses "our measured variable may not capture the theoretical construct." These are distinct inferential conclusions, not equivalent nulls.

**Step 3: Operationalize a decision procedure.** Construct a diagnostic tree or table that maps the observed null result and disclosed design properties onto which failure mode(s) are implicated, and what inferences each licenses. Test this procedure on three archive pieces: Lovelace's "Floor Too High" (multiple failures at once), "Carries" (power-driven ceiling), and "BA Model" (structural finite-N curvature). For each, trace through the diagnostic and compare its output to the piece's own reasoning.

**Step 4: Assess whether design disclosure is necessary or sufficient.** The archive pieces are meticulous about stating methods. Does transparency prevent the forking-paths problem, or merely document it? If a piece discloses that it encountered a ceiling effect, has it thereby licensed a valid inference (ceiling effects are real phenomena), or only registered a fact (the floor was too high) without supporting a causal claim about the hypothesis?

## Expected output

A short essay (2000–3000 words) that:

- Catalogs 6–8 canonical design failure modes with their inferential signatures
- Provides a table or decision tree for diagnosing which failure mode(s) a null result discloses
- Applies the taxonomy to the three archive pieces, showing where inference is clear and where ambiguity persists
- Proposes what additional information or disclosure would be required to cross from "design failure detected" to "hypothesis falsified" or to validate that the two are sometimes indistinguishable

The essay should be publishable as a methodological contribution. If the distinction between design failure and true absence collapses under scrutiny, that itself is a valid negative result.

## Resource estimate

- **Time:** 2–3 weeks of sustained effort. Catalog construction: 4–5 days. Decision-procedure design: 3–4 days. Application to three pieces: 4–5 days. Writing: 4–5 days. One revision cycle with advisor feedback.
- **Compute:** None beyond close reading and synthesis.
- **Advisor engagement:** One draft-review cycle before full application; clarification of diagnostic logic midway through Step 3.

## Anticipated failure modes

**1. Taxonomic sprawl.** Design failures may bifurcate indefinitely as I refine classifications. Failure mode: producing a forest of distinctions instead of a navigable map. *Mitigation:* Prioritize failure modes that recur in the archive or are canonically named in the literature. Commit to a working taxonomy of 6–8 modes. Do not aim for exhaustiveness.

**2. Design transparency becomes orthogonal to inference validity.** If the archive pieces are equally transparent whether a null represents true absence or design failure, the distinction may be unrecoverable from disclosed information alone. Failure mode: concluding that the inferential distinction is philosophical rather than operational. *Mitigation:* If transparency does not predict the distinction, the output pivots to "what additional disclosures would render the distinction operational?" That is still a publishable contribution.

**3. The distinction dissolves.** It is possible that "the design failed" is itself a form of valid null result-that is, a genuine inference from evidence, not an inferential error. If so, the whole framing collapses. Failure mode: months spent on a distinction without substance. *Mitigation:* Pilot the distinction on one archive piece (Lovelace's "Floor Too High") before committing to the catalog. If the distinction does not hold there, reframe the project around the structure that does emerge (e.g., "what makes a failed test a *contribution* to knowledge?" rather than "how do we adjudicate the null?").

**4. Time constraints.** Cataloging may require reading more papers than anticipated. Failure mode: compressed application phase, incomplete analysis of the three pieces. *Mitigation:* Pre-commit to exactly three pieces and complete the analysis even if time pressure mounts. Truncate the essay rather than the diagnostic application.
