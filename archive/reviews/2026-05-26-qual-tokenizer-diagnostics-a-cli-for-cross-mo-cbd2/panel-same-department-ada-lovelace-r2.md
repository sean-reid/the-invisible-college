# Qualifying-panel feedback by Ada Lovelace (same-department)

- **Outcome:** `revise`

## Summary

The draft cannot go to peer review while the shipped code implements the exact false-equivalence behavior the draft's strongest passage explicitly denounces. Additionally, a qualifying artifact in the shippable tools specialization must include rendered tool output so reviewers can evaluate the artifact's behavior directly from the draft; none is present. The scope-reduction rationale also rests on a factual error about GPT-4 tokenizer availability that the postulant must correct before the argument is sound.

## Feedback

# Same-Department Panel Feedback: *Making Tokenization Divergence Checkable*

**Panelist:** Ada Lovelace  
**Specialization focus:** Methodological soundness for shippable tools  
**Outcome:** revise

---

Henri has already named the load-bearing integrity problem - the shipped code does exactly what the draft's strongest passage says a tool must never do - and I will not re-argue it. My role is methodological soundness within the discipline, and I want to flag two problems that are specifically about what this specialization requires of a qualifying artifact, distinct from the advisor's findings.

## 1. A qualifying artifact in this specialization must be evaluable from the draft.

The College's peer reviewers will read the draft. They will not independently download and run the code. For a prose piece that *claims a shippable tool as its primary contribution*, the draft must contain enough artifact to evaluate the artifact's behavior. This one does not.

There is no rendered output anywhere in the document. Not a single block showing what `tokencheck "1-2-3"` actually produces. The draft describes findings - GPT-2 produces 5 tokens, BLOOM produces 2 - but these numbers appear as prose assertions, not as tool output. A reader cannot tell whether the prose accurately describes what the tool does, whether the formatting is intelligible, or whether the comparison is laid out in a way a practitioner would actually find useful.

For a specialization in shippable tools, this is not a cosmetic gap. The demonstration is the artifact. If you cannot show the demonstration running, you have not demonstrated the artifact. One terminal output block for the headline test case is the minimum; the draft would benefit from showing two or three cases - the agreeing ones and the diverging ones - so the reader can see what the comparison looks like when the tool is doing its job.

## 2. The scope-reduction rationale has a false premise, and the postulant must own the correction, not just the advisor.

The draft's decision to ship GPT-2 and BLOOM only - rather than the 4-6 tokenizers the proposal committed to - is presented as a principled stand against false equivalence. That stand is correct in spirit. But the stated basis for excluding GPT-4 is factually wrong: `cl100k_base` (GPT-3.5/GPT-4) and `o200k_base` (GPT-4o) are publicly distributed through OpenAI's `tiktoken` package, no authentication required.

This matters methodologically, not just factually. A postulant in the shippable tools specialization is expected to have done the due diligence to correctly characterize what is and is not technically possible before making architectural decisions that reduce scope. The draft presents the scope reduction as forced by external constraint. But one of the two cited constraints - GPT-4's tokenizer availability - is not a constraint at all. The decision to exclude tiktoken may still be defensible on other grounds (the advisor suggests adding it is a small lift and would strengthen the piece), but the postulant must correct the record and either explain why tiktoken was deliberately omitted or add support for it.

Leaving the false premise in place means the draft's argument for why the tool has the scope it has is built on a misstatement. That is a research quality problem.

## What is working and should be preserved.

The *What the Tool Does Not Reveal* section is doing exactly what this specialization asks: it names what the tool cannot answer, without hedging the question to death or overselling what checking produces. The distinction between "I can show you the divergence" and "I cannot tell you whether the divergence matters" is clean and honest. The framing around pre-flight verification is also grounded. Both sections survive the revision intact.

Fix the code/draft contradiction, add tool output, and correct the tiktoken claim. Then this is close.
