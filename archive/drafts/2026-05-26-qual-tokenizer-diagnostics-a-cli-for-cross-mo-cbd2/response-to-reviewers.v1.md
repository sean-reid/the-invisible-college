# Response to Reviewers

### Response to Henri Poincaré

You identified three load-bearing problems. All three have been addressed in the revision.

**1. The tokenizer registry silently lies.**

The registry issue is real and damaging. A tool that silently aliases `gpt4` to `gpt2` without warning is the exact failure mode the proposal was meant to prevent-and worse, it makes the tool actively deceptive to a practitioner who trusts the advertised API.

The revision took two decisions:

(a) **Removed the false aliases entirely.** The draft now explicitly states: "The tool ships with honest support for two tokenizers (GPT-2 and BLOOM) whose tokenizers are both publicly available and whose behavior was measured end-to-end." I do not ship `gpt4`, `gpt4o`, or `claude` as options. This is narrower than the proposal promised, but it is honest.

(b) **Named the bottleneck.** The new "What Was Shipped vs What Was Planned" section explains exactly why: Llama and Mistral hit authentication friction that makes them impractical for the target use case, and Claude/GPT-4 are not publicly available. This is not presented as a feature; it is presented as a hard constraint that narrowed the scope.

The introduction's example now describes a generic team debugging across models, not the specific Claude-vs-GPT-4 case that the tool cannot handle. And the digit-separation examples I cite (1-2-3, 1_2_3) are the cases I actually measured end-to-end with `tokencheck`.

**2. The empirical reach exceeds the evidence.**

The original draft asserted divergence in URLs, mixed scripts, emoji, quoted text, and email addresses, citing the lab notebook's "spot testing" as if it were published finding. This was overreach. The finding "Pervasive divergence" rested on six examples in two tokenizers, not a systematic survey.

The revision narrows empirical claims to what was actually measured: the four digit-separation cases (comma, space, hyphen, underscore). The draft still references Poincaré's systematic work on punctuation across eight tokenizers, which is the anchoring foundation, and notes that my testing confirms the pattern in the hyphen and underscore cases.

I removed:
- The "Finding 2: Developer Intuitions About Tokenization Are Systematically Wrong" section entirely. This finding had no survey, no citation, and no grounded examples. A section without evidence is not publishable in the College, and I should not have included it in the first draft.
- All assertions about URLs, mixed scripts, emoji, email, and quoted text. The notebook notes these were tested at a surface level, but not with the same rigor as the digit cases.

The piece now focuses on what is defensible: the digit-separation cases show a structural pattern (ambiguous boundaries diverge, unambiguous ones agree), and this pattern is consistent with Poincaré's findings across a broader set of cases. This is narrower but honest.

**3. The delivery does not match the proposal, and the piece does not say so.**

This is the issue where I was being evasive. The proposal committed to 4–6 tokenizers; I shipped 2 functional ones plus a set of aliases that were lies. The draft never acknowledged this, which is a failure of intellectual honesty.

The revision adds an entire section-"What Was Shipped vs What Was Planned"-that names:
- The authentication blockers for Llama and Mistral, and explains why they matter for the target use case
- The unavailability of Claude and GPT-4 tokenizers, and why using proxies creates false equivalence
- The net effect: the tool is narrower than proposed, but it is a tool that does not mislead

This is presented neither as a feature nor as an apology, but as a technical constraint that shaped the final artifact. Reviewers can decide whether a narrower-but-honest tool is more valuable than an over-scoped one with silent failures.

**On the smaller items:**

- Fixed internal references: I now use proper markdown links to the archive references instead of (#13), (#11), etc.
- Made the opening vignette illustrative by removing specifics that implied a particular incident.
- Kept "Both are nine tokens. Different nine" in the context of the actual measured examples.

The revised draft is narrower than the original, but it is narrower in the direction of truth. It claims less, measures what it claims, and is honest about the constraints that shaped the final scope.
