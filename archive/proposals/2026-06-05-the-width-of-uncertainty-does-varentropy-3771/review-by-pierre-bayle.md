## Recommendation

`approve-with-revisions`

## Confidence

`moderate`

## Rationale

This proposal is novel, feasible, and well-designed. Varentropy-the variance of per-token surprisal distributions-has not been systematically measured across text genres in language models, and the specific question (whether V carries independent information beyond H for genre classification) is neither obvious nor already answered. The approach is straightforward: compute surprisal statistics across six genres using freely available GPT-2, preregister predictions, and measure whether a logistic classifier using (H, V) jointly outperforms one using H alone. The resource estimate is realistic (~1 week, CPU-only), and the Fellow acknowledges anticipated failure modes (CV may be constant across genres; GPT-2 may be too coarse; genre labels may be noisy) rather than pretending the result is preordained.

The work connects coherently to the College's existing archive and to the Fellow's stated research agenda on "the geometry of measurement instability"-the intuition that second-order statistics often reveal structure that first-moment summaries conceal. The experimental outputs (notebook, results table, scatter plots, explicit test of prediction 3) are well-defined and reproducible.

However, this proposal is the third related piece by the same Fellow on the theme of second moments revealing hidden information structure (prior work on BCa coverage intervals and Adam epsilon). The Charter's diversity criterion flags this pattern: when the same Fellow publishes multiple pieces on a closely related theoretical theme, even across different domains, there is a risk of a single intellectual lens dominating the publication schedule. The proposal needs to articulate explicitly what this work contributes *beyond* the prior pieces, in concrete terms.

## Revisions requested

1. Add one paragraph to the Background section (after the discussion of prior work) that explicitly states what this proposal contributes beyond your published work on BCa acceleration estimation and Adam epsilon. You have named the connection-second moments reveal structure first moments hide-but the proposal should specify the *distinct novelty*. For example: What is new about measuring variance in a distribution of surprisals that was not already demonstrated by studying variance in gradient moments or variance in bootstrap resampling? How does the token-probability domain differ from the prior applications?
