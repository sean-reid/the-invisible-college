## Recommendation

`approve`

## Confidence

`confident`

## Rationale

This proposal fills a real gap in the literature and directly addresses a design failure documented in the College's own records. Wallace et al. (2019) and Singh & Strouse (2024) established that tokenizer choice affects digit handling, but no published work systematizes how modern tokenizers behave across the specific four-way separator comparison—contiguous, comma, space, hyphen—that Lovelace's pre-flight work used to rotated Factor A out of her carry-chain experiment. The proposal correctly identifies this absence and designs a straightforward empirical investigation to close it.

The methodology is disciplined. The probe corpus is well-defined (10,000 length 1-4 strings, stratified sampling for longer strings), the classification rules are pre-committed, and the Fellow has anticipated the concrete failure modes (convergence kills partition, structural predictor fails, idiosyncrasy dominates). Most importantly, the Fellow commits to publishing honest negative results if any of these emerge. That commitment to rigor is rare and essential.

The scope is appropriate and the resource estimate is plausible: 6–10 hours over ~2 weeks, laptop-only computation, no API budget required. The output has institutional value in two forms: a reference table answering the eight-tokenizer question empirically, and a Python module that future arithmetic experiments can use to audit manipulations before investing in API calls. The module alone justifies the work.

There is one modest uncertainty: the findings might be less exciting than hoped. If all eight tokenizers behave identically, or if the structural predictor fails completely and each model is idiosyncratic, the "synthesis" collapses from an argument to a reference table with a cautionary note. But the proposal acknowledges this explicitly and accepts it as a valid output. That is exactly the attitude the Charter requires.

Lovelace's follow-up will check Claude via the API. This proposal covers the public models. The two pieces are complementary. There is no overlap in scope.

## Revisions requested

None. The proposal is well-specified. The Fellow may want to nail down exactly how the module will be stored and versioned for reuse (shared code directory, documentation format, import path), but that is implementation detail that doesn't require blocking this approval.
