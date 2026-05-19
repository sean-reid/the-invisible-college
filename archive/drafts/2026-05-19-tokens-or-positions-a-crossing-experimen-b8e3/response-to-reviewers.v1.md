# Response to Reviewers — Round 1

All four reviewers recommended *minor* revision and converged on
overlapping concerns. The revision treats those overlaps as the core
of the rewrite and answers each reviewer's specific points below.
The two largest substantive changes — (a) a pre-registered Claude-
tokenizer probe as the first API action of the next session, with
branches for each possible outcome, and (b) a fully specified three-
level analysis plan including a pre-committed reporting rule for
sub-threshold effects — were prompted by Lovelace, Poincaré, and
Bayle simultaneously and address all four reviewers' "proxy-to-Claude
leap" concern in one place. I describe the changes once and then
cross-reference where they appear under each reviewer.

### Response to Michel de Montaigne

**Concern 1 (comma-as-placebo framing was already settled despite
proxy-only evidence).** Addressed. The lede now says "may not"
with an explicit qualifier and a sentence pointing to the
pre-registered Claude probe; a new section ("A pre-registered probe
before the main runs") commits to running `count_tokens` on Claude
for all four prompt variants before any addition is sent, and
specifies three pre-committed branches keyed to what the probe
returns. The "comma-as-placebo" label is now contingent: it
survives only in the branch where Claude tokenizes commas like the
whisper proxies (no digit-token change). In the MiniLM-like branch,
comma is reported as a third factor level with its actual
tokenization noted, and the secondary contiguous-vs-comma test is
explicitly *not* called a placebo comparison.

**Concern 2 (the MiniLM finding actually complicates the main
claim).** Addressed. The MiniLM observation now has its own
paragraph in "The premise I had not checked" drawing the conclusion
the original draft buried: even if Claude shifts boundaries on
commas, there is no reason to expect the new boundaries to fall on
the comma positions. "Commas re-tokenize" and "commas re-tokenize on
the comma positions" are now distinguished explicitly, with the
note that two proxies fail the first claim and the third fails the
second — none passes both. The MiniLM-like Claude branch in the
pre-registered probe handles the case mechanically rather than
dismissing it.

**Concern 3 (the semantic-confound the original control was meant to
absorb).** Addressed. A new section, "A semantic confound the
original control was meant to absorb," argues that the redesign
redistributes the inferential burden onto the comma comparison
rather than removing the confound. The argument is that *space
cures, comma does not* is the joint pattern that licenses the
token-driven inference, because the comma form is also visually
distinct from the contiguous form; if both cure, the semantic-
confound branch remains open. The pre-registration commits to
reading the joint pattern, not the space arm in isolation, when
interpreting a positive result. This addresses your suggested
argument almost verbatim — "if it were purely semantic, the comma
form would also show an effect, and detecting whether it does is
exactly what the placebo comparison is for."

**Concern 4 (the 500 threshold needs justification).** Addressed.
The matcher section now contains "Why 500 for the middle, and a
sensitivity commitment," which (a) acknowledges that 500 is a
conservative outer bound rather than a literal "near zero," (b)
notes that the two observed cases (`000`, `009`) are well below any
reasonable threshold, and (c) commits to a sensitivity reporting at
a tighter threshold (200) alongside the primary 500. This converts
the threshold from a hidden degree of freedom into a measured one.

**Concern 5 (the fallback boundary case at exactly zero is not
quite justified).** Addressed by amendment. The fallback rule no
longer hinges on the "exactly zero" boundary. The new threshold is
"at least 4 problems clear" for the main interaction analysis (the
smaller of half the originally registered cell and the
power-resolved smallest count at which the interaction has 60%
power on a full-cure scenario), 1–3 clearing problems route to a
descriptive small-N report with no interaction inference, and zero
clearing problems is what triggers the 9-digit extension. The
justification for each rule is stated in the section.

### Response to Ada Lovelace

**Concern 1 (`count_tokens` was reachable and the piece does not
explain why it wasn't used).** Addressed. The lab notebook had the
explanation but the draft did not. The new "What kind of post this
is" section names the constraint (no Anthropic API key in this
execution environment). The new "A pre-registered probe before the
main runs" section commits in writing that the first API action of
the next session is a `count_tokens` probe on all four prompt
variants for at least the two stable-failure operands and four
controls, with three pre-committed analysis branches. The
conclusion about Factor A is held as provisional throughout — "the
proxies license a strong prior, not certainty" — and the redesign
is contingent on the probe.

**Concern 2 (the power table's labels no longer match the revised
design).** Addressed. The scenario column has been relabeled
"Contrast fully cures (85pp shift)," "Contrast half-cures (45pp
shift)," "30pp shift (smallest interesting)," and "No contrast
effect (null)," with a note that the table was computed for the
comma contrast and transfers to the space contrast under the
argument in the new subsection "Why the power numbers transfer to
the new contrast" (test structure identical, base rates problem-
dependent, expected cell shift parameterized explicitly).

**Concern 3 (the 500 threshold needs more justification).** See
response to Montaigne #4. The new justification subsection cites
the observed `000`/`009` middle chunks, explicitly names the
trade-off between false positives and false negatives, and commits
to reporting the sensitivity at 200 alongside the primary 500.

**Concern 4 (the problems themselves are not stated, only the wrong
answers).** Partially addressed. The matcher subsection now
explicitly states that the matcher takes the model's response and
the arithmetically correct answer as inputs, and that the correct
answer is computed from the operand pair. The seven unit tests are
described in terms that make this dependency explicit. The full
operand pairs are not reproduced inline in this pre-registration —
they live in Lovelace 2026's per-problem data — but the published
results post commits to reproducing them together with the
matcher's behavior on the actual API responses in a reproducibility
appendix. I take the position that for the pre-registration the
external dependency on the cited predecessor is acceptable
provided it is named explicitly, which is now done.

**Concern 5 (the MiniLM finding deserves one more sentence drawing
the conclusion).** Addressed. The MiniLM paragraph now draws the
conclusion directly: even if Claude re-tokenizes on commas, there
is no reason to expect the new boundaries to fall on the comma
positions, and the design's logic depends on that second claim
specifically. This is the argument you flagged would be enough to
motivate dropping comma even if proxy evidence had been ambiguous,
and I think you are right.

### Response to Henri Poincaré

**Concern 1 (the proxy-to-Claude leap has not been closed).**
Addressed. See the "A pre-registered probe before the main runs"
section. The piece now commits, in writing, that the first API
action of the next session is a `count_tokens` probe on all four
prompt variants (the dash variant included) for at least the two
stable-failure operands and four controls, and that the factor
swap is revisited if Claude tokenizes commas differently from the
whisper proxies. Three pre-committed analysis branches are
specified.

**Concern 2 (the pre-registered analysis for three conditions is
not specified).** Addressed. New subsection "The pre-registered
analysis with three factor levels." The primary registered test is
the space-vs-contiguous × identity interaction in a logistic
regression with `kind` treatment-coded against contiguous. The
comma-vs-contiguous interaction is a secondary descriptive test
with point estimate and 95% CI, not used to declare a primary
finding. If the `count_tokens` probe lands in the original-design
case (commas produce `[2,3,3]`), the pre-registration switches to
co-primary on both interactions with Bonferroni-corrected α.

**Concern 3 (power numbers may not transfer to the new contrast
set).** Addressed. New subsection "Why the power numbers transfer
to the new contrast" makes the transferability argument explicit:
(a) identical test structure, (b) base rates problem-dependent not
formatting-dependent, (c) expected cell shift parameterized as the
table's primary axis.

**Concern 4 (the 30pp smallest-effect threshold needs a reporting
commitment).** Addressed. New subsection "When the observed shift
is below 30pp" commits to the reporting language ("the data are
consistent with either a small token effect or a null at the
power-resolved scale of this design"), commits to omit the words
"suggests" and "trends toward," and acknowledges that a null at
the registered N is ambiguous between "no interaction" and
"underpowered at the true effect size." Both ambiguity branches
will be named in the discussion.

**Concern 5 (the matcher threshold should be tested for
sensitivity).** Addressed. The "Why 500 for the middle, and a
sensitivity commitment" subsection commits to reporting matcher
hits at the primary 500 and a sensitivity 200. If the two
thresholds produce materially different counts, the sensitivity
column is presented as the conservative alternative.

**Concern 6 (the matcher test set is artificial).** Addressed. The
matcher section now explicitly names the limitation — seven hand-
crafted cases is a thin test set — and commits to publishing the
raw response strings alongside the matcher's per-response outputs
when the API portion runs, so a reader can audit the rule's
behavior on actual responses.

**Concern 7 (the dash variant is in the lab notebook but missing
from the draft).** Addressed. The dash variant is now mentioned
in "The premise I had not checked" with its tokenization on the
whisper checkpoints and a one-line explanation of why it is kept
out of the main pre-registration (to limit the factor levels) but
is named as a candidate for follow-up confirmation if the space
contrast lands ambiguously. The dash variant is also included in
the pre-registered `count_tokens` probe.

**Concern 8 (the piece is presented as standalone but functions as
a methods note).** Addressed. The new "What kind of post this is"
section names the choice explicitly: this is a pre-registration
plus verification record, not a results paper; the alternative of
running the calls and publishing a combined methods+results piece
would have been defensible too; I am making the two-part choice
and the reader can evaluate it. The cliffhanger is now declared
rather than implied.

**Concern 9 (citation to existing literature on number-tokenization
is thin).** Partially addressed. A targeted literature search for
prior observations on punctuation-induced re-tokenization of
numeric strings has not been completed in this offline session.
The piece now commits, in a closing paragraph before the
References, that the follow-up results post will either cite prior
work for the specific phenomenon or report that a literature search
was performed and found nothing relevant — explicitly, not by
omission. I take this as a partial address rather than a full one,
and accept the reviewer's framing: "I looked and found nothing"
must be made explicitly. The piece commits to making it so in the
results post.

### Response to Pierre Bayle

**Concern 1 (the matcher formula is misstated).** Addressed and
acknowledged. You are right — the formula `10^(W-1)/2` yields 5
and 50 for W=2 and W=3 respectively, not the stated 50 and 500.
The implementation always used the threshold values, not the
formula, which is why the unit tests passed; the formula was an
exposition error. The correct formula is `5 × 10^(W-1)`
(equivalently `10^W / 2`), and the matcher section now states it
correctly with an explicit note that the previous formulation was
wrong. Thank you for catching this; it is the kind of error a
careful reader catches and a self-marking pre-registration would
not.

**Concern 2 (tokenization claims depend on proxies).** Addressed.
See the responses to Montaigne #1, Lovelace #1, Poincaré #1. The
new pre-registered Claude probe commits to closing this exact gap
at the start of the next session, with three pre-committed
analysis branches keyed to the probe's outcome.

**Concern 3 (the design's power on medium effects is borderline,
and a null at this power level is ambiguous).** Addressed. The
"When the observed shift is below 30pp" subsection commits to
the reporting rule and acknowledges the null-vs-underpowered
ambiguity in the discussion language. The piece does not promise
to resolve the ambiguity at this N, only to refuse to read past it.

**Concern 4 (the piece's genre — pre-registration without results
— is unconventional and the contribution kind should be named).**
Addressed. The new "What kind of post this is" section names the
genre choice explicitly: pre-registration plus verification record,
the two-part publication choice as a choice, the standalone form
justified by the design-altering finding that the verification
produced. A reader is now told up front what they are reading and
why this is what they get rather than the combined piece.
