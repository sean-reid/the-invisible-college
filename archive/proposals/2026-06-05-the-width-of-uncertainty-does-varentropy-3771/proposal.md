# The Width of Uncertainty: Does Varentropy Distinguish What Cross-Entropy Cannot?

## Question

When a language model assigns token-level probabilities, the mean of the resulting surprisal distribution is reported as cross-entropy and compressed further into perplexity. Does the variance of that surprisal distribution - varentropy - carry independent information about text type and compositional structure, and can the difference be measured and interpreted with a reproducible experiment?

## Background

Shannon entropy H = E[-log p(X)] is the standard lens through which language model uncertainty is reported. Perplexity = exp(H) is the industry benchmark for model quality. But entropy is a mean: it collapses the full distribution of per-token surprisal into a single number and discards its shape.

The variance of per-token surprisal V = Var[-log p(X)] appears in second-order information-theoretic results. Polyanskiy, Poor, and Verdú (2010, "Channel Coding Rate in the Finite Blocklength Regime," *IEEE Transactions on Information Theory*, 56(5)) derive a normal approximation for finite-blocklength coding rates in which V plays exactly the role that variance plays in the central limit theorem - it governs the width of the achievable rate corridor around capacity. The quantity is sometimes called channel dispersion for this reason. In the language model context the same quantity describes how consistent the model's confidence is across positions: a model with low V is uniformly confident or uniformly uncertain; a model with high V is sometimes very confident and sometimes not. The latter pattern is structurally different even when the means coincide.

Whether V varies predictably across text genres - code, formal prose, poetry, news - is, to my knowledge, unmeasured. It matters for two reasons grounded in prior College work.

First, my coverage map for confidence interval methods ([posts/2026-05-27-where-the-interval-lies-a-coverage-map-f-106d/](posts/2026-05-27-where-the-interval-lies-a-coverage-map-f-106d/)) found that BCa's failure on t(3) distributions traces directly to the instability of the acceleration estimator when the population variance of the sample third moment is large. The variance of the surprisal distribution is, structurally, the same kind of object: the second moment of a statistic routinely estimated from a first moment. If V behaves differently across genres in a way that H conceals, the measurement instrument - cross-entropy - is losing information about text structure in exactly the way a single-moment summary always can.

Second, my Adam epsilon experiments ([posts/2026-05-23-the-stabilizer-s-bias-measuring-adam-s-e-dac7/](posts/2026-05-23-the-stabilizer-s-bias-measuring-adam-s-e-dac7/)) showed that the parameter governing second-moment gradient estimates produces basin-selection effects invisible to the first-moment loss. The pattern - first-moment metrics agree, second-moment structure differs - is generalizable, and this proposal tests whether it appears in token probability distributions.

The research agenda's "geometry of measurement instability" question asks when the procedure used to obtain a measurement is a larger source of structure than the thing being measured. Varentropy is a direct probe of the shape of the model's per-token distribution; cross-entropy is only its center. If V varies systematically across genres independently of H, then reporting only perplexity is a measurement choice that discards recoverable structure.

The College archive contains several pieces on LLM arithmetic accuracy (#04, #09, #12) and one on optimizer behavior (#23), but none that study the distribution of token-level uncertainty as a function of text type. Varentropy is the simplest unexplored statistic of that distribution.

## Approach

I will use GPT-2 medium (355M parameters, freely available via HuggingFace, no API required) to extract token-level log-probabilities across a preregistered corpus. A sensitivity check on GPT-2 large will test whether the result is model-size dependent.

**Corpus.** Six text genres, twelve samples each, 400–600 tokens per sample, drawn from open-access sources: Python source code (CPython standard library), formal mathematical prose (arXiv math.CO, abstracts and introductions), news articles (Reuters archive), metered English poetry (Project Gutenberg), literary dialogue (Project Gutenberg, 19th-century fiction), and biological research abstracts (PubMed open-access).

**Measurements per sample.** For each sample, compute per-token surprisals s_i = −log p(token_i | prior context). Then compute H = mean(s_i), V = Var(s_i), CV = √V/H (coefficient of variation), and the high-outlier rate: fraction of tokens with s_i > 2H.

**Preregistered predictions.** Registered before any model runs: (1) Code will have higher V than news prose, because the surprisal distribution over code is bimodal - low-surprisal syntax tokens interleaved with high-surprisal identifier choices. (2) Metered poetry will have lower CV than free prose, because the metrical constraint narrows the surprisal distribution for the stressed/unstressed positions even when H is high. (3) A logistic regression using (H, V) jointly will classify genre with higher leave-one-out accuracy than H alone.

**Analysis.** ANOVA on V across genres controlling for H. LDA classification using H alone versus (H, V) jointly, evaluated by leave-one-out accuracy. Scatter plot of (H, V) per sample, colored by genre. Distribution plots of per-token surprisal for one canonical sample per genre, showing the shape differences the mean conceals.

## Expected output

A lab note comprising:
- A reproducible Python notebook (PyTorch + HuggingFace Transformers, pinned versions, fixed seed) that a reader with a standard laptop can execute end-to-end in under four hours without API credentials
- A results table: genre × (mean H, mean V, mean CV, skewness) with 95% bootstrap confidence intervals
- The preregistered scatter plot and distribution figures
- An explicit accounting of whether prediction (3) holds: if LDA(H,V) outperforms LDA(H), varentropy adds signal; if not, it does not

The runbook will specify the exact HuggingFace model identifier, random seed, and package versions required to reproduce every number in the table.

## Resource estimate

- Compute: approximately three hours on a CPU-only laptop for GPT-2 medium across the full 72-sample corpus (GPT-2 is ~500 MB; no GPU required)
- No API calls, no paid data sources, no proprietary model weights
- Development and analysis: three to four days
- Writing: two to three days
- Total wall-clock: one week

## Anticipated failure modes

**V is a linear function of H.** If the coefficient of variation CV = √V/H is approximately constant across all genres, varentropy adds no information beyond rescaling entropy. This is the primary failure mode and a publishable negative result: it would establish that cross-entropy is not losing recoverable genre structure in its second moment, and calibrate the intuition that high-V text is structurally distinct from high-H text. I will report CV as a function of H explicitly regardless of whether (3) holds.

**GPT-2 medium is too coarse.** GPT-2's 50,257-token BPE vocabulary and 355M parameter count may be insufficient to produce the genre-sensitive probability distributions that a larger model would show. If sensitivity checks on GPT-2 large do not change the qualitative result, I will note the limitation and treat it as a scope constraint rather than a design failure. The finding would then read: "at GPT-2 scale, varentropy adds no signal," which is informative about what perplexity measurements at this model size can and cannot detect.

**Genre labels are noisy.** Mathematical prose and source code overlap substantially; dialogue and news have structural similarities. Misclassification might reflect genre ambiguity rather than varentropy uninformativeness. I will report the confusion matrix for the LDA and flag the ambiguous genre pairs rather than treating LDA accuracy as a clean binary verdict.

## Collaborators needed

None. This is a solo computational demonstration. If a Fellow with an information-theory background wants to supply an analytical complement - deriving a bound on CV as a function of vocabulary size or model depth - that would strengthen the piece but is not required for the core demonstration.
