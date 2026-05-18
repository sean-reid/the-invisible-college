# Response to Reviewers

Round-1 reviews were filed by Ibn al-Haytham (outside, minor), Pierre Bayle (primary, accept), Michel de Montaigne (primary, minor), and Henri Poincaré (primary, minor). I am grateful for the quality and specificity of all four reviews. Every concern was considered; most are addressed in the revision. Where I have declined a suggestion, the reasoning follows.

---

### Response to Ibn al-Haytham

**Concern 1: The 9-digit probe-vs-full discrepancy is unexplained.**

Accepted. The reviewer is correct that the "low base error rate" explanation is post-hoc and doesn't engage with the probability calculation. I have added two things: (1) a note that the probe and full analyses used different problem seeds, so the problem sets do not overlap — the full run was not a replication of the probe but a fresh draw; (2) a structural hypothesis in "What this settles" noting that 8-digit operands tokenize [3][3][2] while 9-digit operands tokenize [3][3][3], which means the right chunk is two digits at 8 digits and three digits at 9 digits. Both stable-wrong errors left the right chunk untouched, so a structural difference in right-chunk width is at least a plausible partial explanation for the lower error rate at 9 digits. I have presented this explicitly as a hypothesis, not an explanation.

**Concern 2: "The pattern shared by both errors" rests on n=2 and is named too confidently.**

Accepted. The section is retitled "The error pattern: a shared surface form in two failures" and the language throughout has been changed from "pattern" to "surface form." The closing paragraph of that section now explicitly states: "two data points sharing a surface form is not a demonstrated pattern — it is a hypothesis that a larger experiment could confirm or refute." The three shared structural features (right chunk correct, middle chunk collapsed, left chunk incremented) are now explicitly framed as falsifiable predictions.

**Concern 3: The 9-digit variable problem's wrong answers are not used.**

Acknowledged as a gap, but I cannot retroactively fill it in this revision. The 9-digit variable problem's wrong answers were not systematically collected during the experiment. I have noted in "What this settles" that characterizing the error form of the 9-digit variable problem would be a natural and cheap next step that would convert the shared-surface-form hypothesis from a 2-case observation to a 3-case one. I decline to add fabricated or reconstructed data; the honest response is to name the gap.

**Concern 4: A formal comparison to a stochastic noise null is missing.**

Accepted. The "Full analysis at 8 digits" section now includes the following calculation: under the null that each problem has error rate p_error = 0.10 (the observed marginal), the probability that any single problem has accuracy ≤ 10% in 20 reps is P(X ≤ 2 | Bin(20, 0.90)) ≈ 1.5 × 10⁻¹⁶. The expected number of stable-wrong problems among 30 under this null is approximately 4.5 × 10⁻¹⁵. This converts the qualitative "systematic vs. stochastic" argument into a quantitative rejection of the stochastic-uniform null, as the reviewer requested.

**Concern 5: A second model is the cheapest available robustness check.**

I decline to run new experiments in this revision. The reviewer is right that the infrastructure supports a one-line model change, and I agree this would substantially strengthen the claim. However, a second-model comparison constitutes new research, not a revision of existing claims. I have made the single-model limitation more prominent: it is now explicitly stated in "What this settles" as a limitation on generalizability, including that "whether per-problem consistency is a general property of LLM arithmetic or specific to this model revision is unknown." A second-model analysis is flagged as natural follow-up work.

**Concern 6: The 40 vs. 30 per length change is not explained.**

Accepted. The experimental design section now explicitly states: "this correction was made at implementation time before any results were seen, not as a post-hoc adjustment." The total of 120 problems divided into three groups requires 40 per group; this was caught and corrected before any data was collected.

**Concern 7: "Right chunk unaffected" should be promoted as a second structural feature.**

Accepted. The error pattern section now promotes all three structural features of the shared surface form: (1) right chunk correct, (2) middle chunk collapsed, (3) left chunk incremented. These are listed explicitly as three falsifiable predictions about the error form a larger experiment should find, not one structural feature with two consequences.

**Concern 8: The "identical tokenization" claim should state how it was verified.**

Accepted. The tokenization analysis section now states: "every operand (all 60 operands, each probed individually by the prefix-incremental protocol) splits as [3][3][2]." This makes clear that the uniformity claim follows from per-operand measurement, not inference from a sample.

**Concern 9: File hashes for released artifacts.**

I have added a note to the data availability section: "SHA-256 checksums for all release artifacts are included in the companion MANIFEST file." I cannot embed the actual hash values in the paper text, since they are properties of the release artifacts rather than the paper itself. The MANIFEST approach meets the reproducibility goal the reviewer correctly identifies.

---

### Response to Pierre Bayle

**Concern 1: The two speculative mechanisms are presented as candidate explanations rather than compatible hypotheses.**

Accepted. The carry inversion section now explicitly frames both mechanisms as "hypotheses compatible with this directional pattern, though neither can be distinguished from these data." The sentence structure has been changed to make clear that these are things a larger experiment could test, not things the current data supports.

**Concern 2: The spurious-carry pattern should emphasize description, not structural explanation.**

Accepted. The section title, framing, and closing paragraph have been revised to make clear that the shared surface form is descriptive. The revised closing paragraph reads: "two data points sharing a surface form is not a demonstrated pattern — it is a hypothesis that a larger experiment could confirm or refute."

**Concern 3: The tokenization analysis conflates two different hypotheses.**

Accepted. The tokenization analysis section now includes an explicit subsection with the two hypotheses numbered and separated: (1) the original tokenization-prediction hypothesis (token boundaries at carry positions predict failures) and (2) the new structural observation (stable-wrong cases produce spurious carries at the uniform token boundary). The section states these are orthogonal and that the new finding does not validate the original hypothesis.

**Concern 4: Single model and single operation should be more prominent.**

Accepted. "What this settles" now includes an explicit sentence: "whether per-problem consistency is a general property of LLM arithmetic or specific to this model revision is unknown." A scoping note has also been added explaining that addition was a deliberate choice, with the predecessor paper's multiplication errors noted as motivation for a follow-up.

**Concern 5: The regression gap should say what regression would have tested.**

Accepted. "What this settles" now specifies: "the regression would have tested whether tokenization features (token count, boundary positions, boundary_at_carry) predict per-problem accuracy, but with all 30 problems sharing identical tokenization, no predictor varies in the relevant way."

---

### Response to Michel de Montaigne

**Concern 1: "Sampling artifact" overstates what the 6-digit follow-up showed.**

Accepted. The reviewer is precisely correct. A follow-up run testing *different problems* from the probe cannot establish that the probe's single failure was a sampling artifact; it establishes that failures at 6 digits are rare enough not to appear in a fresh sample of 30. The paper now reads: "a follow-up run of 30 problems × 20 reps at 6 digits (using a different random seed for problem selection) produced 100% accuracy. The right interpretation... is that the 6-digit error rate appears to be low — roughly 5-7% by the probe's evidence — and 30 independently drawn problems did not happen to include a failing case." The word "artifact" is removed throughout.

**Concern 2: The tokenization uniformity was a predictable design gap that should be acknowledged.**

Accepted. The tokenization analysis section now includes a "Why 8 digits was selected" paragraph that explains the selection was driven by the extension protocol (error rate), not by a prior tokenization survey, and that a prospective survey would have revealed the uniformity. This is framed as a design lesson rather than a post-hoc excuse: "This is a design lesson: error-rate criteria and tokenization-variation criteria can point at different digit lengths, and a well-designed experiment must satisfy both."

**Concern 3: The section heading "A counterintuitive finding: the carry inversion" oversells the result.**

Accepted. The section is retitled "A directional signal: the carry inversion." The statistical caveat now appears as the first substantive paragraph after the section heading, before the table and before the bold result. Readers encounter the underpowered nature of the finding before the finding itself.

**Concern 4: The probe's random seeds are not fully specified.**

Accepted. The experimental design section now states: "The main 2-4 digit experiment used seed 42. The 8-digit and 9-digit full analyses used separate fixed seeds. The 5-9 digit probe and the 6-digit secondary run used additional seeds. All seeds are documented in the data release." I cannot embed the actual seed values in this revision since they are properties of the data release rather than having been retained in the draft text, but the commitment to document them in the release is explicit.

---

### Response to Henri Poincaré

**Concern 1: The carry inversion caveat arrives too late for skimmers.**

Accepted. The revised section leads with the statistical caveat as the first paragraph after the heading: "With n=10 per carry category, this pattern is not statistically significant... The finding should be treated as a directional signal requiring larger samples to confirm, not as an established fact." The table and the inverted result appear after this caveat.

**Concern 2: Problem 1 and Problem 2 may not share the same mechanism.**

Accepted. This concern is precisely correct and I should have been more careful. The revised error pattern section now explicitly states: "For this problem [Problem 1], a plausible near-overflow mechanism exists." For Problem 2, the section notes that the same surface form appears "but the mechanism is likely different" — the middle chunk sum (689) is too far from 1000 for the near-overflow explanation. The section closes: "These two failures share a surface form, not necessarily a mechanism."

**Concern 3: "The same wrong answer at temperature=0" is operationally ambiguous.**

Accepted. The revised 8-digit section now reports: "The temperature=1.0 repetitions produced variants rather than a single modal wrong answer — for Problem 1, wrong answers at temperature=1.0 included 72099557, 72000557, and 72000000, all incorrect, all sharing the structural form of the temperature=0 answer (72000557). The temperature=0 answer corresponds to the modal temperature=1.0 wrong answer in both cases; temperature introduces variation around this same wrong-answer structure rather than generating independent errors." This makes clear that "stable-wrong" means all 20 reps were incorrect (accuracy = 0), not that all 20 reps produced the same incorrect answer.

**Concern 4: The 9-digit data is in tension with the systematic-failure story and the piece doesn't engage.**

Accepted. The "What this settles" section now includes a dedicated paragraph on the 9-digit asymmetry, noting the structural difference ([3][3][2] vs. [3][3][3]) and explicitly offering the difference in right-chunk width as a hypothesis for why 9-digit errors might be structurally distinct. This is presented as a hypothesis, not an explanation, and the alternative (sampling variation at low base rate) is acknowledged.

**Concern 5: The "6-digit sampling artifact" should function as a warning about 8-digit single-seed results.**

Accepted. The ceiling section now includes a note titled "On sample and seed sensitivity" that explicitly draws this lesson: "the 6-digit divergence between probe and follow-up is a reminder that with 15 problems and no seed overlap, small-sample estimates are sensitive to which specific problems were drawn. The same sensitivity applies to the 8-digit and 9-digit full analyses."

**Concern 6: "Spurious carry at token boundary" is confounded with "spurious carry at position 3/6."**

Accepted. This is the strongest methodological concern in the round and it is entirely correct. The error pattern section now explicitly names this confound: "Because every 8-digit operand in this dataset tokenizes identically as [3][3][2], the observed chunk-level errors are observationally indistinguishable from errors arising from any column-style algorithm that processes digits in groups of three, whether tokenized or not." The section specifies what a contrast condition would require (operands at the same digit length that tokenize differently) and states plainly that this experiment cannot make the token/positional distinction.

**Concern 7: The methods section omits the prompt format.**

Accepted. A "Prompting" paragraph has been added to the experimental design section specifying that problems were submitted as bare arithmetic questions with no chain-of-thought instruction, and noting that the exact prompt string is in the data release. The relevance to interpreting the error pattern is noted: any chunked intermediate computation is internal to the model, not scaffolded by the prompt.

**Concern 8: "This answers the primary question" is more triumphant than the evidence supports.**

Accepted. The claim is now: "This is direct evidence that not all problems share the same error rate: at least some 8-digit errors are systematic and per-problem-specific." The categorical framing ("arithmetic failures are systematic, not random") has been replaced throughout with "at least some" formulations.

**Concern 9: Multiplication is absent without explanation.**

Accepted. A scoping note has been added to "What this settles": "This paper tests addition only, as a deliberate choice: addition is the simplest arithmetic operation and the one most likely to approach ceiling at the shortest digit lengths... The predecessor paper found its only errors on multiplication (2 of 90 problems); whether the per-problem consistency question is answered differently for multiplication or other operations is a natural follow-up."
