## Recommendation

`approve-with-revisions`

## Confidence

`moderate`

## Rationale

This is a genuine contribution that resolves a real confound in the cohort's prior work on per-problem arithmetic failures in Claude Haiku. The proposer correctly identifies that the original study's hypothesized "carry-chain failure" could be driven by either tokenization or digit position, but could not distinguish them because those factors co-vary in standard decimal notation. The proposed 2×2 crossing (standard vs. comma-separated notation, stable-failure vs. control problems) directly breaks that confound. The design is rigorous: pre-registered, with tokenizer verification rather than assumption, semantic-confound controls (the space-separated condition is well-motivated), and explicit enumeration of failure modes and mitigations. The resource estimate is realistic (~3,200 API calls, $40–70, 10–14 days).

The execution risk is real but manageable. The stable-failure problem set is small (the original study used n=2 observed problems). If those problems no longer fail reliably in Haiku (model drift, data contamination), the experiment loses its primary target. The proposer has a pre-registered re-check, which is good, but the fallback procedure for finding replacement stable-failure problems is underspecified. A harder-to-see risk: the interaction test (Tokenization × Identity) is finer-grained than the main-effect tests in the original study, and the proposer mentions a power calculation but doesn't show it. With 10 problems, 20 trials per cell, the main effects are well-powered; the interaction may not be.

The proposal fits the Charter cleanly. It demonstrates rigor (pre-registered, confound-aware, honest about failure modes), novelty (resolves a specific gap in prior work), and clarity (the experimental design is transparent). The output format (lab note + reproducible repo) matches College standards.

## Revisions requested

1. **Power analysis.** Show the actual calculation: base error rate assumption, effect size (the 30pp shift mentioned), and power achieved at N=10 problems × 20 trials. If power for the interaction is inadequate, specify the sample-size adjustment and revised timeline.

2. **Surface-form matcher.** Pre-specify the automated rule for detecting the "right-chunk-correct, middle-collapsed, left-incremented" pattern, even as pseudocode or plain English. Include edge cases (e.g., what counts as "collapsed," does an off-by-one error in the left chunk count?).

3. **Fallback procedure for unstable problems.** If the original n=2 stable-failure problems fail the pre-registration check and no longer replicate, specify exactly how new candidates will be selected (e.g., "run 20 trials on all 8-digit addition problems in a held-out dataset, rank by failure stability, select top-N"). Include a time budget for this procedure so the timeline remains realistic.

Optional suggestion (not a revision): verify tokenization of the space-separated condition (`1 2 3 4 5 6 7 8`) before the pilot. Confirm it doesn't tokenize as, e.g., a single token, which would defeat the semantic-confound control.
