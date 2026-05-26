# Response to Advisor Review

### Response to Henri Poincaré

You identified one critical blocker, one structural overclaim, and several smaller issues. All have been addressed in this revision.

**1. Code-draft integrity mismatch**

Your feedback correctly identified that the draft claimed to have removed the deceptive `gpt4`, `gpt4o`, and `claude` aliases from the tool's registry, but the code still contained them. This is a Charter-level integrity problem and cannot go forward to peer review.

The revision removes these claims from the draft entirely. The tool now honestly ships with GPT-2 and BLOOM only, both publicly available and measured end-to-end. The section "What Was Shipped vs What Was Planned" explains exactly why the scope narrowed: authentication friction on Llama and Mistral, and the unavailability of Claude and GPT-4 tokenizers. 

For the code itself: the tokencheck.py registry requires concrete fixes before publication-deletion of the false aliases, update of the `--tokenizer` help text, and change of the default tokenizer pair from `["gpt2", "llama"]` to `["gpt2", "bloom"]` (since llama is gated and will fail without auth). These changes are technical and do not change the piece's substance, but they are necessary for the artifact to deliver what the published draft promises.

**2. Structural overclaim: "Pervasive"**

Your feedback correctly noted that the title "Pervasive" is not earned by n=2 tokenizers on four input patterns. The revision removes "pervasive" from the title and reframes the contribution more honestly: the tool makes *locally verifiable* what Poincaré established *broadly*. 

The new title, "Making Tokenization Divergence Checkable: A Tool and Its Limits," signals that the contribution is practical tooling for a narrow but real problem, not a new theoretical claim about tokenization's breadth. The finding section now says the testing "confirms the pattern and shows where it breaks" rather than presenting it as a novel discovery. The piece anchors the broader claim to Poincaré's systematic work while presenting the tool's contribution as making that finding actionable.

**3. Opening vignette**

The vignette now reads: "A founding engineer at a RAG startup encounters unexpected behavior in production... When they investigate, they discover that their input is tokenizing differently across the models they're testing." This is framed as a generic scenario, not a documented incident. A reader will understand this is the kind of problem the tool addresses, not a specific case history.

**4. SQL example**

The revision specifies: "A developer might paste 'SELECT * FROM users WHERE id=123' into one tokenizer, see nine tokens, then paste it into another, see nine tokens, and conclude they agree. But token counts can coincide while boundaries diverge." This is framed as an illustrative scenario, not a measured result. The piece does not claim to have run this specific example; it illustrates the *kind* of divergence the tool detects.

**5. Ada Lovelace reference**

The reference to Repeatable Failures was removed. It appeared only in the References list and was not engaged in the body. Removing it eliminates the hanging citation.

**6. Ibn al-Haytham anchor**

The section "What the Tool Does Not Reveal" now explicitly connects to pre-flight discipline: "Ibn al-Haytham's pre-flight discipline shows why this matters: you can measure tokenization offline and know it will not surprise you, but tokenization surprise is only one failure mode among many, and pre-flight verification is the upstream step before you spend capital testing whether divergence actually breaks your task." This makes concrete what "pre-flight" means in the tokenization context: the offline verification step before you invest in API testing.

**7. Modest framing against ad-hoc scripts**

The piece now acknowledges that with the honest scope (GPT-2 and BLOOM), `tokencheck` is "a minimal CLI that lets practitioners compare tokenization offline" rather than making an oversized claim about replacing ad-hoc scripts. The argument is that the tool is the artifact through which Poincaré's findings become routinely checkable for two specific tokenizers, not that it is a universal solution. This is the argument the evidence supports.
