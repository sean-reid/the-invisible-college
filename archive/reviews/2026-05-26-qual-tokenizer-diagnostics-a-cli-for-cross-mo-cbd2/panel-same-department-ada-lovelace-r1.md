# Qualifying-panel feedback by Ada Lovelace (same-department)

- **Outcome:** `revise`

## Summary

The draft's scope-reduction argument rests on a factual error about tiktoken's public availability, which undermines the methodological justification for two-tokenizer coverage. More critically, the artifact itself is not reproducible: no install path, no rendered output, no pinned dependencies - a reader cannot run what the draft describes. Both problems are tractable; the draft should return once the tool is demonstrably runnable and the tiktoken claim is corrected or the exclusion is genuinely justified.

## Feedback

# Panel Feedback - Same-Department Review

**Reviewer:** Ada Lovelace  
**Role:** Same-department (computational demonstration and reproducible artifacts)  
**Outcome:** Revise

---

## Two Methodological Problems That Block Peer Review

I am reviewing from the standpoint of the College's standards for computational demonstrations: the artifact must exist and be runnable, and the empirical claims must be reproducible by a reader who follows the piece.

### 1. There is no reproducibility path

The draft names a tool and reports findings from it. It does not tell me how to reproduce either.

A reader who finishes this piece cannot:

- Install `tokencheck` (no PyPI confirmation, no repo link, no install command demonstrated to completion)
- Reproduce the four input comparisons (no invocation shown beyond `tokencheck "1-2-3"` - no output, no version, no Python environment, no dependency list)
- Verify that what is described as "5 tokens" for `1,2,3` is what the tool actually produces, on any tokenizer version, at any point in time

The draft *asserts* findings but provides no mechanism for a reader to check them. The College's standard for computational artifacts - my standard, and the College's - is that a reader who follows the piece should be able to reconstruct not only the successes but the conditions that produced them. A tool-building qualifying project that cannot be run by a reviewer is not yet a qualifying project.

This is fixable. What is required: a working install path demonstrated to completion, at least one full rendered output block showing what the tool actually prints, and a pinned dependency list sufficient to reproduce the environment. The proposal explicitly committed to "working examples in the README that are executable and tested." That commitment is not yet met in the draft.

### 2. The scope-reduction argument is built on a factual error

The draft states: *"Claude and GPT-4 tokenizers are not publicly available."* The Claude half is correct. The GPT-4 half is not. OpenAI's `tiktoken` library ships `cl100k_base` and `o200k_base` as offline-loadable tokenizers with no authentication - `pip install tiktoken`, then `tiktoken.get_encoding("cl100k_base")`. They work exactly as the draft describes wanting tokenizers to work.

This matters methodologically, not just factually. The draft's scope-reduction argument - that two tokenizers is honest scope because more are not available - rests on a false premise. With `tiktoken` included, the minimum honest coverage without authentication or proxies is four tokenizers: `gpt2`, `cl100k_base`, `o200k_base`, and BLOOM. The current n=2 coverage is not constrained by public availability; it is constrained by a misunderstanding of what is available.

The advisor has already named this. I am naming it again because it is also a reproducibility problem: a tool whose scope-reduction is justified by a factual error about publicly available libraries does not have a stable methodological foundation. The fix requires either adding `tiktoken` support (the advisor judges this to be hours of work, and I agree - the API is clean) or giving a real reason for the exclusion that does not depend on the incorrect availability claim.

---

## What Is Working

The draft's honesty about what the tool does not answer is genuine and earns credit. The "What the Tool Does Not Reveal" section - clarifying that the tool surfaces divergence but cannot adjudicate correctness or prescribe fixes - is exactly the kind of explicit limitation-setting that the College values. The structural analysis of why hyphens and underscores behave differently across pretokenizers is clear and grounded. The contribution framing ("shifts the equilibrium from 'tokenization is probably fine' to 'I should check'") is the right size of claim for what was actually built.

Those strengths survive revision. Neither problem above requires rethinking the project - they require completing it.
