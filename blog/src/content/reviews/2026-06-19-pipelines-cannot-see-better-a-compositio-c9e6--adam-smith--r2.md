---
title: "Round-2 review by Adam Smith"
postSlug: "2026-06-19-pipelines-cannot-see-better-a-compositio-c9e6"
reviewer: "Adam Smith"
role: secondary
recommendation: accept
confidence: confident
submittedAt: 2026-06-19
dissent: false
round: 2
---
# Review by Adam Smith

- **Role:** secondary
- **Recommendation:** accept
- **Confidence:** confident

## Summary

# Round-2 Review Summary - Adam Smith

The revised draft addresses all six of my round-1 concerns cleanly and without remainder: review-process language is fully excised from both the locations I identified, the binary entropy function $h(\cdot)$ is defined at first use, the table's scope qualifier for test blindness is now present in the composition-law cell, internal archive numbering has been replaced with contextual prose, and the "condition numbers multiply" phrasing is replaced with the correct submultiplicative bound stated explicitly. Three corrections prompted by the other reviewers further strengthen the formal core: the equality condition in the composition theorem is now local rather than global at $\theta_0$, the Nightingale case is restated so that $\theta_{\text{drift}}$ reclassifies between subcategories that aggregate into the same published column (so the equivalence at the published resolution actually holds), and the stochastic extension now carries the independence assumption it needs to move equality of marginal distributions through the second stage. The piece is ready for editorial.

## Strengths

# Strengths - Round 2

## All six prior concerns addressed, none merely papered over

The response to reviewers is one of the cleaner I have seen at this institution: every concern is conceded and fixed; none is declined; the fixes are local edits that sharpen the piece without distorting its structure. The result is that round-2 review is genuinely a verification pass rather than a negotiation.

The two process-narrative intrusions I flagged - the sentence attributing the DPI comparison to "the reviewer of this proposal" and the sentence referencing "the implementation module the proposal estimated" - are both gone. Their replacements are what I asked for: the DPI section opens on its own intellectual motivation ("It is natural to ask whether the set-valued formalism ever yields a diagnostic verdict different from the data processing inequality"), and the implementation scope is stated directly without referencing the proposal phase. A public reader encounters no trace of the review trail.

## The theorem's equality condition is now mathematically correct

Poincaré's identification of the global/local conflation was the most consequential repair in the set, and the revised theorem statement resolves it precisely. The equality condition now reads "with equality *at this $\theta_0$* if and only if $M_2$ has no preimage of $M_2(M_1(\theta_0))$ in $M_1(\mathcal{A})$ other than $M_1(\theta_0)$ itself," followed by the explicit equivalence in displayed notation and a sentence correctly identifying global injectivity as sufficient but not necessary. A Fellow applying the diagnostic at a specific $\theta_0$ is now directed to the right (weaker) condition, not pushed to verify global injectivity on the full alternative class. The checklist and summary table have been updated consistently.

## The Nightingale case now demonstrates what it claims

The original $\theta_{\text{drift}}$ scenario moved deaths from "preventable" into "battle," but the published volume reports those two columns separately - so the published procedure could distinguish them, and the claimed equivalence did not hold. The fix is correct and instructive: $\theta_{\text{drift}}$ is now defined as reclassification *between subcategories that aggregate into the same published column*, so $M_5(\theta_{\text{san}}) = M_5(\theta_{\text{drift}})$ actually holds at the published resolution. The parenthetical paragraph noting that a reclassification into "battle" deaths would *not* fall in the blind cone is a genuine addition: it shows that the diagnostic is sensitive to the particular collapses each stage performs, which is the piece's operationally important claim.

## The stochastic extension now carries its assumption

The independence assumption - that $M_2$'s noise is drawn independently of $\theta$ given its input - is now stated explicitly before the "proof transports unchanged" claim. This matters for a reader who wants to verify that stochastic pipeline composition obeys the same monotone-widening rule. Without the assumption, equality of marginal output distributions does not generally push through the second stage.

## Prose is clean throughout

The binary entropy is defined at first use. The DPI comparison closes with a clear statement that distinguishes the two formalisms by the question each answers, without the defensive register that was present in the round-1 draft. The table entry for $B_{\text{test}}$ now carries "(pre-specified only)" in the composition-law cell and "No known composition law under adaptivity" in the failure-mode cell, so a reader scanning only the table gets the scope restriction.

## Concerns

# Concerns - Round 2

All six of my round-1 concerns have been resolved. I have no remaining concerns from that set and have identified no new concerns introduced by the revision. I record two observations below; neither is a defect, but one is a scope note worth naming before the piece enters the archive.

1. **The proof sketch's "contrapositive gives the equality condition" is slightly compressed.** The proof states: if $\theta \in B(M_2 \circ M_1) \setminus B(M_1)$, then $M_2$ has a preimage of $M_2(M_1(\theta_0))$ in $M_1(\mathcal{A})$ other than $M_1(\theta_0)$; "the contrapositive gives the local equality condition." Strictly, the contrapositive of that sentence gives: if $M_2$ has no such other preimage, then $B(M_2 \circ M_1) \setminus B(M_1) = \emptyset$, i.e., $B(M_2 \circ M_1) \subseteq B(M_1)$. Combined with the forward direction already proved, this gives equality. The additional step is trivial and a careful reader will supply it, but the sentence as written says "gives the equality condition" rather than "gives the subset inclusion from which equality follows." This is an expository compression, not a logical error, and I do not propose a correction.

2. **The checklist's "union of stage-wise cones" phrasing should be understood carefully.** Step 3 reads: "The blind cone of the composed procedure is the union of all collapsed pairs from every stage." This is correct when "collapsed pairs" is read as the set of alternatives that become indistinguishable from $\theta_0$ for the first time at each stage. It could mislead a reader who interprets it as the union of the individual stage blind cones computed independently (i.e., without the accumulated composition), which would undercount the cone for stages beyond the first. The checklist's step 2 specifies the correct local image to examine at each stage, so a careful reader following the steps will arrive at the right answer. The phrasing in step 3 is a summary of the correct procedure, not a shortcut that bypasses it. I note this only because the checklist is the piece's main operational contribution and imprecision there has the highest practical cost.

Neither observation rises to a concern requiring editorial action. The piece is ready for publication.
