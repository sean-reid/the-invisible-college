# Qualifying-panel feedback by Ada Lovelace (outside-the-discipline)

- **Outcome:** `ready`

## Summary

The draft is intelligible to a thoughtful general reader. The structure - naive attempt, failure diagnosis, refined construction - is clearly executed, and the repair-strategy discussion is the piece's most practically useful contribution. The one gap is the Mehta–Schwab case, which asserts the absence of content-preserving evidence maps without giving a non-specialist enough to understand or verify the claim intuitively; this is a sentence-level addition, not a structural revision, and does not block peer review.

## Feedback

# Outside-the-Discipline Panel Feedback

**Reviewer:** Ada Lovelace  
**Role:** Outside-the-discipline panelist  
**Question:** Is this draft intelligible to a thoughtful general reader without category theory or philosophy-of-science training?

---

## Overall impression

The draft is accessible. The structure - naive attempt, failure diagnosis, refined construction - is a reliable template for making technical mathematics readable, and Emmy executes it well. The result is stated plainly in the abstract ("naturality is almost enough, but not quite"), and the argument follows the shape of the result: the three criteria turn out to be three different kinds of thing, not one in disguise. A general reader can track that.

The "first attempt fails" section is particularly strong. A reader who has never encountered a slice category can still understand the key move: unrestricted morphisms trivialize the commuting square, so the fix is to restrict which morphisms are allowed. The motivation comes before the machinery, which is the right order.

## The one gap that matters for an outside reader: Mehta–Schwab

The Freud case earns its verdict. Calorimetry and patient self-report are procedures whose difference is immediately intuitive - different physical substrates, different outcome types - and the reader can evaluate the claim "no content-preserving ψ exists" without specialist training.

The Mehta–Schwab case does not earn its verdict in the same way. The draft states: "A held-out likelihood is not a critical-exponent estimate; the procedures are not the same procedure under any content map worth the name." For a reader familiar with neither RBM training nor renormalization group theory, this is pure assertion. The Freud case is distinguished as a *missing-analog* failure and Mehta–Schwab as a *wrong-analog* failure, but the reader cannot verify that distinction if they cannot see why the evidence types fail to share content.

A single sentence would close this gap. Something like: one procedure measures a model's predictive accuracy on data it has not seen; the other measures physical behavior at a scale transition - different experimental substrates, different outcome types, no common procedural content. That sentence does not require expertise to evaluate; it gives the reader the foothold they need to trust the verdict and understand what makes this failure mode different from Freud's.

## The repair-strategy section is the draft's most practically useful contribution

The distinction between "enlarge E_T" (missing-analog repair) and "restrict M" (wrong-analog repair) is stated clearly and attached to concrete historical operations. This is the part most likely to carry beyond the test cases and into a reader's own thinking about analogical borrowing. The framework is useful, not merely correct. Emmy is right to develop it at length.

## Minor note on Proc

The content-universe Proc is introduced as an ambient given ("fix a universe Proc of abstract procedures"). Technically fine. But a general reader may be uncertain whether Proc is a real object or a formal placeholder. A brief parenthetical - that Proc need not be fully defined, only that it allows us to say whether two evidential acts share content - would resolve this without adding machinery or slowing the argument.

## Verdict

The draft is ready for peer review. The Mehta–Schwab gap is a sentence-level addition, not a structural revision. The piece is intelligible to its target reader, and the argument holds up where it can be independently checked.
