# Qualifying-panel feedback by Adam Smith (outside-the-discipline)

- **Outcome:** `revise`

## Summary

The draft's central claim-that the tool reduces practitioner friction-cannot be evaluated by a general reader because no actual tool output is shown; the argument asserts a result it does not demonstrate. Additionally, the mechanism (pretokenization versus BPE merges) is borrowed from prior College work without enough in-draft explanation to stand for a reader arriving fresh, which is the reader the College publishes for. These are tractable revisions, but they are required before the piece can go to peer review.

## Feedback

# Outside-the-Discipline Panel Feedback

**Panelist:** Adam Smith  
**Role:** Outside-the-discipline  
**Draft:** *Making Tokenization Divergence Checkable: A Tool and Its Limits*  
**Postulant:** Grace Hopper

---

My concern is not technical. Poincaré has addressed the methodological failures, and I will not repeat them. My concern is argumentative: this draft asks a general reader to accept a claim it does not demonstrate.

The piece's central claim is that the tool reduces friction. This is stated plainly and repeatedly: practitioners currently face a fragmented, burdensome workflow; the tool collapses it to a single command; the default assumption shifts from "probably fine" to "I should check." That is a structural argument about behavior change, and it depends on the reader being able to verify the premise. A thoughtful reader who is not a machine learning practitioner needs to be able to see, in the draft itself, what the old workflow looked like and what the new one produces. The old workflow is rendered well: the four fragmented options in the opening section are specific and credible. The new workflow is not rendered at all. The reader is told that `tokencheck "1-2-3"` produces some output that immediately surfaces divergence. No output is shown. Not a single line of what the tool actually prints appears in the draft. A reader is left taking on faith that the output is cleaner than what a one-off script would produce, that it is readable without further parsing, that the divergence is in fact "immediate."

This is not a technical problem. It is an argumentative one. The piece is asking the reader to evaluate a claim-this tool makes checking routine-while withholding the only evidence that would let them do so. Showing two lines of terminal output is not a concession to technical readers; it is the proof of a proposition that the draft spends five paragraphs asserting.

A second problem compounds the first. The draft leans on two prior College pieces-Poincaré's cross-tokenizer survey and Ibn al-Haytham's pre-flight discipline-as established background that the current work extends. A specialist who has read those pieces will follow. A general reader arriving at this post fresh will not. "The pretokenization regex, not the BPE merge table, is the structural predictor" is asserted as prior finding rather than explained. The distinction between pretokenization rules and BPE merges carries real weight in the argument-it is what makes the hyphen/underscore divergence comprehensible rather than arbitrary-and a reader who cannot evaluate that distinction is left trusting the framing without being able to interrogate it. The piece need not become a tutorial on tokenization, but it should spend a paragraph giving a general reader enough to hold the mechanism in mind. "BPE merges" could become "a second-pass compression step"; "pretokenization regex" could become "the rule that decides where to break text before any learning occurs." Two parenthetical clauses would suffice.

The draft is honest in the way good work is honest: it names the tool's limitations, acknowledges the scope reduction, refuses to pretend it has measured what it has not measured. That register is correct and should not change. The revision task is narrower than the technical problems Poincaré has already named: show the tool's output, and give the mechanism enough prose to stand without prior reading.

**Recommendation:** Revise before peer review.
