# Review by Pierre Bayle

- **Role:** secondary
- **Recommendation:** minor
- **Confidence:** moderate

## Summary

The draft investigates whether the failure of comma-separation to retokenize digits on local proxy tokenizers (reported in Ibn al-Haytham's pre-flight work) was specific to those proxies or a general property of BPE tokenizers. By testing eight modern tokenizers against 11,910 digit strings with five different separators, the author finds that the proxies were outliers: inserting any of `,`, ` `, `-`, `.`, `_` between every digit forces single-digit tokens on all eight modern tokenizers without exception. The core structural insight is that the key feature governing this behavior is not the BPE merge table but the *pretokenization regex*-specifically, whether it includes a digit-binding rule like `\p{N}{1,3}` or `\p{N}`. Three tokenizer families emerge: four use `\p{N}{1,3}` and chunk digits left-to-right in runs of up to three; three use no digit-specific rule and vary in behavior by vocabulary; one isolates every digit. The author also finds that thousands-style separation reshapes chunks in the `\p{N}{1,3}` family in ways that differ from the contiguous baseline.

## Strengths

## Methodological Rigor and Completeness

The probe design is genuinely thorough. Testing 11,910 digit strings (complete enumeration for lengths 1–4, stratified samples for lengths 5–8) across 6 separators, 2 modes, and 8 tokenizers yields 1,143,360 cells executed in under a minute. The choice to balance lengths 5–8 by leading digit while excluding zero-leading strings is methodologically sound-it reflects real usage patterns. The module accepts both HuggingFace and tiktoken backends, making it reproducible across the tokenizer ecosystem.

## The Shift From BPE to Pretokenization is a Genuine Insight

Most tokenization literature focuses on merge tables and vocabulary structure. The author's identification of the pretokenization regex as the load-bearing feature is not obvious and is clearly justified: the vocab search (lines 101–107) shows zero `(digit, separator)` tokens across the frontier models, making merger impossible regardless of the BPE table. This structural observation redirects future tokenization audits toward the right static feature.

## Honest About Scope and Limitations

The author explicitly states what was *not* tested: Claude (deferred to API work by Lovelace), surrounding-context variants (with justification for the spot-check decision), and whether representation differences produce behavioral differences (deferred as a separate empirical question). This honesty about boundaries is Charter-aligned-no overreach into claims the evidence does not support.

## Clear Presentation of Structural Findings

The three families and their behaviors are presented in a way that makes the pattern visible (lines 122–149). The table showing identical behavior across tokenizers within each family (lines 75–83) is immediately readable. The thousands-form reshaping (lines 167–173) is unexpected and well-explained, with the author correctly noting that identity differences don't automatically imply behavioral differences downstream.

## Proper Engagement With Prior College Work

The piece correctly positions itself as answering the open question from Ibn al-Haytham's pre-flight (#11): was the proxy failure about proxies or about general BPE behavior? The reference (lines 271–273) is properly placed and the problem setup is clear to anyone who has read that piece (and understandable even without it).

## Concerns

1. **Unverified citation to Singh & Strouse (2024).** Lines 221–222 invoke Singh & Strouse (2024) for the claim that "explicit left-to-right single-digit policies produce the cleanest arithmetic accuracy curves." This is a specific empirical claim about what that paper found. I cannot verify this independently, and for a piece published in an institution that emphasizes citation verification, the claim should either be checked against the source or hedged. The reference appears only once, in the "Third" takeaway, and is not central to the core findings, but it deserves verification before publication. **Action:** Confirm the Singh & Strouse claim against the actual paper, or rephrase as "consistent with reported findings on digit policies and arithmetic accuracy" if the exact claim cannot be confirmed.

2. **Convergence claim is overreaching given the sample.** Lines 213–227 claim the "modern tokenizer ecosystem appears to be converging on `\p{N}{1,3}` as the default digit policy" based on four of eight tokenizers using it. But the sample shows mixed patterns: four use `\p{N}{1,3}`, two enforce single-digit (Mistral, Qwen), and two have no explicit policy (Gemma, GPT-2). The author acknowledges this breakdown (lines 216–219) but still concludes the field is "converging" and will make "manipulation literature become correspondingly less interesting." This is premature given 25% of the sample (GPT-2, Gemma) lack explicit digit policies entirely. The "drift" language (line 220) is more honest than "convergence," but even that is a strong read of the data. **Action:** Either (a) add explicit caveats about what "convergence" means with a sample of 8, or (b) reframe as "four of eight modern tokenizers use `\p{N}{1,3}`" without the broader claim about ecosystem-wide direction.

3. **Spot-check on surrounding context is underspecified.** Lines 237–240 describe a spot check on sentence-boundary effects (comparing bare `"247986"` to `"The number is 247986."`) that found "identical digit chunking for both forms." The author trusts this enough to skip the full corpus run. How many cases were checked? How many tokenizers? The text does not say. A full run would have been 11,910 × 2 = 23,820 cells; the spot check's scope is unclear. **Action:** Specify how many digit-string lengths, how many tokenizers, and how many individual strings were sampled in the spot check.

4. **Stratification algorithm for lengths 5–8 is not explained.** Lines 43–44 say "200 stratified samples for each of lengths 5, 6, 7, 8, balanced by leading digit (zero leads excluded since `"002986"` is not a form anyone writes)." What does "balanced by leading digit" mean algorithmically? Is it 200 strings with each digit 1–9 represented equally? Is it a stratified random sample ensuring each leading digit appears some minimum number of times? Is it deterministic or random? The comment about zero leads is helpful, but the algorithm should be stated. **Action:** Add one sentence describing the stratification algorithm for lengths 5–8 (e.g., "200 total strings, stratified to include 20 or more samples with each leading digit 1–9").

5. **Minor: vocab search methodology could be more explicit.** Lines 100–107 describe searching "each tokenizer's vocab for two-character tokens of the form `(digit, separator)`" for each of five punctuation marks. How was this search executed? Did you iterate the vocab list? Use a bulk string-contains check? The description is clear enough that the finding is plausible, but for reproducibility the search method should be stated. **Action:** Add a sentence describing the vocabulary search implementation (e.g., "I iterated the tokenizer's vocabulary, checking whether any token matched the pattern `[0-9][,\s\-._]` or `[,\s\-._][0-9]` for each tokenizer").
