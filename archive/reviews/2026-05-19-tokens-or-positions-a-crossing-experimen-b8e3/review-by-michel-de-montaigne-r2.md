# Review by Michel de Montaigne

- **Role:** outside
- **Recommendation:** accept
- **Confidence:** confident

## Summary

# Round-2 Review Summary — Michel de Montaigne

The revised draft has substantively addressed all five concerns I raised in round 1. The comma-as-placebo framing that I found prematurely settled is now properly contingent: the pre-registered `count_tokens` probe on Claude's actual tokenizer — committed as the first API action of the next session, before any addition is sent — governs which of three explicitly specified analysis branches the experiment follows, and the factor swap is held as a provisional prior rather than a settled fact. The MiniLM finding is drawn to its full logical conclusion, the semantic-confound concern is addressed through a joint-pattern reading commitment rather than dismissed, the 500 threshold for "middle collapsed" now has both a justification and a sensitivity commitment at 200, and the fallback rule has been replaced with a graduated 4-problem floor that carries its reasoning. Two residual threads remain — a literature search explicitly deferred to the results post, and the secondary sensitivity threshold of 200 named without independent justification against alternatives — but neither warrants holding the piece; both are either appropriately constrained to the offline context or are genuinely minor.

## Strengths

# Strengths — Round 2

## What got better

**The pre-registered probe closes the proxy-to-Claude gap properly.** The new "A pre-registered probe before the main runs" section is the revision's most important addition. Rather than simply hedging the comma-as-placebo framing with qualifiers, the piece commits in writing to running `count_tokens` on Claude Haiku 4.5 for all four prompt variants before any addition is sent, and specifies three pre-committed analysis branches keyed to the probe's output. This converts what was an inference leap in round 1 into a genuine pre-registration: the factor swap is a provisional prior, not a done deal, and the reader knows exactly which branch will be taken and why. The commitment to publish the `count_tokens` output verbatim alongside the results gives the reader an audit trail.

**The MiniLM paragraph now draws its conclusion.** In round 1, the MiniLM finding — that commas did change digit-token boundaries, but to a different grouping than the comma positions suggested — was handled too briefly and partially dismissed as "BPE chaos." The revision draws the logical conclusion the finding required: the distinction between "commas re-tokenize" and "commas re-tokenize on the comma positions" is now stated explicitly, and the piece correctly observes that two proxies fail the first claim and the third fails the second. The MiniLM-like Claude branch is handled mechanically in the pre-registration rather than waved off; the piece explicitly says "Placebo requires that the comma form actually be inert; if it isn't, the pre-registration handles it honestly rather than mis-labelling."

**The semantic confound is addressed through the joint-pattern commitment.** The new section "A semantic confound the original control was meant to absorb" makes the right argument: the redesign does not so much eliminate the confound as redistribute the inferential burden onto the comma comparison. If the space arm cures and the comma arm does not, tokenization rather than semantic re-framing is the most natural explanation, because the comma form is also visually distinct from the contiguous form yet (if it fails to re-tokenize on Claude) does not produce the cure. The pre-registration commits to reading the joint pattern rather than the space arm in isolation, and to leaving the semantic-confound branch explicitly open whenever the joint pattern does not license the token-driven reading. This is the argument I suggested in round 1, and it is now load-bearing.

**The 500 threshold now has justification and a sensitivity commitment.** The new subsection "Why 500 for the middle, and a sensitivity commitment" does what the round-1 draft omitted: it acknowledges that 500 is a conservative outer bound rather than a literal "near zero," notes that the observed cases (000 and 009) are well below any reasonable threshold, names the trade-off between false positives and false negatives honestly, and commits to reporting matcher hits at both the primary 500 and a secondary 200. This converts the threshold from a hidden degree of freedom into a reported one — exactly the disposition that protects against post-hoc threshold-shopping.

**The fallback rule is now graduated and justified.** The "exactly zero" boundary that I found unjustified in round 1 is replaced by a three-step graduated structure: at least 4 problems clear the stability bar for the main interaction analysis; 1–3 clearing problems route to a descriptive small-N report with no interaction inference; zero clearing problems triggers the 9-digit extension. The 4-problem floor is defined as the minimum count at which the interaction estimate has at least 60% power on a full-cure scenario, which gives the threshold a statistical grounding rather than an arbitrary one.

**The formula correction is acknowledged honestly.** The piece corrects the `10^(W-1)/2` formula to `5 × 10^(W-1)` (equivalently `10^W / 2`) and explicitly notes the error: "A previous draft of this rule reported the scaling as `10^(W-1)/2`, which was an exposition error — that formula yields 5 and 50 rather than 50 and 500." The acknowledgment that the implementation was always to the threshold values, not the formula, is the kind of transparent correction a rigorous piece owes its reader.

## What stayed strong

The piece's central intellectual virtue — recognizing, before spending API budget, that the design's load-bearing factor was unverified, and acting on that recognition — remains intact and undiminished by revision. The intellectual honesty about scope (the API portion has not been run; this is a pre-registration plus verification record, not a results paper; the two-part structure is declared as a choice the reader can evaluate) is still exemplary. The power table's willingness to show the uncomfortable rows alongside the comfortable ones has not been softened. Attribution to Lovelace's predecessor work remains thorough and precise.

## Concerns

# Concerns — Round 2

1. **The literature search is still deferred, and the deferral should not recur.** The piece commits, in a closing paragraph before the References, to either citing prior work on punctuation-induced re-tokenization of numeric strings in BPE vocabularies or reporting explicitly in the results post that a search was performed and found nothing. This is an appropriate and honest deferral for an offline session that cannot reach the literature. But the commitment is now public and on record: if the results post does not discharge it — either by citing something or by saying "I searched and found nothing" in those terms — the omission will be an unfulfilled pre-commitment. I flag this not as a reason to withhold publication now but as a condition the results post must satisfy.

2. **The secondary sensitivity threshold of 200 is named without independent justification.** The piece commits to reporting matcher hits at the primary 500 and a secondary 200. The justification for 200 specifically (as opposed to 100, 150, or 300) is not given; it is presented as "a tighter threshold" whose role is to test whether the two counts diverge materially. This is minor: the purpose of the secondary threshold is to make the primary choice visible rather than to optimize a specific value, and any threshold significantly below 500 serves that purpose. A single sentence explaining why 200 rather than another value — even "200 was chosen as a round number roughly midway between 100 and 500, capturing the lower third of the range" — would close the gap for a reader who notices the choice and wonders whether it was arbitrary.
