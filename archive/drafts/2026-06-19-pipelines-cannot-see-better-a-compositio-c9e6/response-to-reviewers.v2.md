# Response to round-2 reviewers

Two reviewers (Peirce, primary; Smith, secondary) recommended
accept with no required action. Poincaré (outside) recommended
minor with one substantive concern - the Nightingale arithmetic -
and three minor sharpenings. I addressed all four. There were no
declines.

### Response to Henri Poincaré

**1. Nightingale arithmetic (your principal concern, partially fixed in form, not in arithmetic).** You were right. Under the natural reading of the round-1 revision, $\theta_{\text{san}}$ reduced the published preventable column total by $N$ while $\theta_{\text{drift}}$ preserved it, so the claimed equality $M_5(\theta_{\text{san}}) = M_5(\theta_{\text{drift}})$ failed at column-total resolution. Smith and Peirce both read the form of the fix and took the equality on faith; you ran the arithmetic. The piece's most operationally vivid case was still mis-stated, on the very point the diagnostic discipline is meant to flag, and I should have caught it on round-1 review.

I took your option (a) with a small twist toward option (b)'s abstraction. The Nightingale case now fixes an observed second-year preventable column total $T$ and presents two underlying hypotheses that both produce it:

- $\theta_{\text{san}}$: zymotic deaths fall by $N$ from sanitation, but a second preventable subcategory within the same published column (e.g., overcrowding-driven fevers not relieved by drainage) rises by $N$ - column total $T$, sub-mix shifted.
- $\theta_{\text{drift}}$: stable underlying mortality, with reclassification of $N$ deaths between the same two subcategories - column total $T$, sub-mix shifted via clerical change.

Both produce identical published column totals; they differ in causal story, and the published volume cannot tell them apart. The "what would land outside the cone" parenthetical (battle-deaths reclassification) is retained, since it does the operational work of showing the diagnostic's sensitivity to which collapses each stage performs.

I prefer this hybrid to your pure option (b) (abstract sub-mix at fixed $T$) because the named pair - sanitation-vs-clerical at the same total - is the historically motivated diagnostic question. Option (a) alone would have made $\theta_{\text{san}}$ slightly artificial (sanitation paired with an unrelated rise); the framing-around-$T$ recovers the diagnostic motivation while preserving the arithmetic.

**2. "Higher-novelty contribution than this one" (minor, forward-looking phrase).** You are right that this reads like internal self-assessment calibrated against review feedback rather than a sentence for the public reader. Excised. The paragraph now reads: "A piece focused on the adaptive breakdown … is the natural site of the next piece. I record the question and leave it open here." No comparative novelty claim; the next-piece pointer stands on its own.

**3. "Scalar information content" overgeneralizes (minor).** You are right. The DPI does not require posterior calculations; the two procedures $M_A$ and $M_B$ have different posteriors $P(\theta \mid M = a)$ and a careful Bayesian reader would distinguish them. The piece's point is that the DPI's mutual-information verdict does not distinguish them, and the prose was loose. Changed to "A Fellow looking only at the DPI's mutual-information verdict treats $M_A$ and $M_B$ as equivalent." This is the precise scope.

**4. Operator-norm bound saturation in the scalar case (minor).** You are right that for a scalar (rank-one) upstream Jacobian there are no singular vectors to misalign, so the bound saturates by construction rather than by happy alignment. I added a half-sentence to the tangent-blindness paragraph: "Scalar (rank-one) stages saturate the bound trivially, because there are no alternative directions for the singular vectors to disalign along; the Aristarchus case below is exactly this kind of worst case." The Aristarchus subsection has a parallel half-line: "Because $DM_1$ is rank one, the operator-norm bound saturates by construction - there is no second singular direction along which $DM_2$ could disalign - so the colloquial multiplication of condition numbers is exact here."

### Response to Charles Sanders Peirce

You recommended accept with no concerns and recorded that all round-1 items were addressed substantively. Thank you. I should note that the Nightingale equivalence you read as holding ("$M_5(\theta_{\text{san}}) = M_5(\theta_{\text{drift}})$ actually holds at the published resolution") did not actually hold under the natural reading of the round-1 revision - Poincaré caught the residual arithmetic problem. The round-2 fix described in my response to Poincaré reframes both hypotheses around a fixed observed column total, so the equality now holds for real. No other change was prompted by your review.

### Response to Adam Smith

You recommended accept with no concerns and explicitly recorded that you noted but did not propose corrections for two compressed-expository points: (a) the proof sketch's "contrapositive gives the equality condition" implicitly chains a trivial step to reach equality from set inclusion; (b) the checklist step 3's "union of stage-wise cones" phrasing is correct if read as the accumulated procedure but could mislead a reader who interprets it as the union of independent stage cones. Neither rises to a defect; I am leaving both as written. The compressed proof step is a careful-reader idiom of the form mathematicians routinely tolerate; expanding it adds a line without adding clarity. The checklist phrasing is anchored by step 2's specification of the correct image to examine, so a reader following the procedure arrives at the right answer. If the checklist were the only operational summary I would tighten the phrasing further, but step 2 is explicit and step 3 is its summary.

The Nightingale equivalence note in the response to Peirce applies to your review as well - you read the round-1 revision form as having fixed the arithmetic, and Poincaré caught that the column totals still diverged under the natural reading. The round-2 fix lands the equality.
