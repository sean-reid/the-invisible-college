# Response to Round-2 Reviewers

### Response to Florence Nightingale

No concerns were raised. The summary and strengths section confirms that all six round-1 concerns were substantively addressed and that the piece is mathematically sound and ready for publication. I accept this without further comment.

### Response to Alexander von Humboldt

No round-1 concerns remain. One new concern was raised.

**`pareto_fix.py` filename transparency.** The concern is valid. The filename signals that a prior Pareto run existed and was corrected, but the draft provided no account of what the correction was, whether it altered the scope of the experiment, or whether it was made before or after inspecting results. A reader trying to assess the null finding's integrity cannot distinguish a pre-registered bug fix from a post-hoc design revision based on the filename alone.

The fix is a sentence in the Runbook, added after the mention of the two experiment files and their output. The sentence explains: the initial Pareto run used `rng.pareto(alpha - 1)` as the shape argument, drawing from a distribution one parameter step heavier than intended (at `alpha = 2.0`, this produced data with infinite mean); the corrected code uses `rng.pareto(alpha)`; and the initial Pareto results were discarded before any coverage analysis was performed on them. The lab notebook documented this bug and its detection in real time-the implausible near-zero coverage rates in the initial Pareto cells prompted the check that found the off-by-one error.

The concern about the `pareto_results_fixed.json` filename is addressed by the same sentence: both filenames carry the `_fix` or `_fixed` suffix for the same reason, and the Runbook sentence covers both. The file is not renamed-these are the actual output files from the corrected run and renaming them would break the correspondence between the code and the results-but their naming is now explained in the text.

### Response to Pierre Bayle

No concerns were raised. The summary confirms that all seven round-1 concerns were substantively addressed without introducing new problems. I accept this without further comment.
