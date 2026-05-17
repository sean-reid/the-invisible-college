## Title
When the Same Sum Gives Different Answers: Floating-Point Non-Associativity in Scientific Computing Pipelines

## Question
How large are the numerical disagreements that arise from floating-point non-associativity in standard scientific computing operations, and are these disagreements ever large enough to change a downstream result in a realistic data analysis pipeline?

## Background
Floating-point arithmetic is not associative: `(a + b) + c ≠ a + (b + c)` in general, because each operation rounds to the nearest representable value. This is formalized in the IEEE 754-2019 standard and documented accessibly in Goldberg's 1991 ACM Computing Surveys paper "What Every Computer Scientist Should Know About Floating-Point Arithmetic" (https://dl.acm.org/doi/10.1145/103162.103163). Worst-case error bounds for various summation algorithms are given in Higham, *Accuracy and Stability of Numerical Algorithms*, 2nd ed. (SIAM, 2002), Chapter 4.

The practical situation is less well-mapped than the theory. NumPy uses pairwise summation by default (documented at https://numpy.org/doc/stable/reference/generated/numpy.sum.html), which is more stable than naive sequential summation but not identical to Kahan compensated summation. PyTorch explicitly documents that floating-point reductions are non-deterministic across hardware and parallelism levels (https://pytorch.org/docs/stable/notes/randomness.html). Yet reproducibility standards in computational science rarely address this class of non-determinism: the standard advice is to pin library versions and random seeds, but not to specify summation order.

This has become newly relevant in three contexts. First, ML training pipelines that shuffle input batches before computing gradient aggregations introduce ordering variation. Second, data analysis pipelines that apply different sort orders before aggregation (e.g., after a merge join) may produce numerically distinct results even with identical inputs. Third, cross-platform replication studies frequently use different hardware with different SIMD widths, which can change the reduction tree structure NumPy uses internally. The question of whether these disagreements are in the noise or are large enough to affect reported results has not, to my knowledge, been answered with a systematic empirical demonstration using real datasets and real pipelines.

## Approach

**Step 1: Implement and characterize four summation methods.** Naive sequential (left-to-right in Python), pairwise (delegate to `numpy.sum`), Kahan compensated summation (implemented from scratch, not via any library), and shuffled-order (random permutation before naive sum, repeated across 1,000 seeds to produce a distribution of results). Use Python's `decimal.Decimal` with precision set to 100 significant figures as the reference "exact" result.

**Step 2: Construct a grid of input types.** Adversarial inputs: arrays with values spanning 10+ orders of magnitude; arrays with catastrophic cancellation structure (large positive and negative values summing to a small result); Kahan's classic example (1, 1e15, -1e15). Benign inputs: daily temperature anomalies from NOAA's Global Historical Climatology Network (GHCN, publicly available at https://www.ncei.noaa.gov/products/land-based-station/global-historical-climatology-network-daily), S&P 500 daily returns, and a random sample of 32-bit image pixel intensities from the CIFAR-10 dataset (available via torchvision or direct download).

**Step 3: Measure disagreement.** For each (input type, method pair), compute: absolute error vs. the Decimal reference; error in ULPs (units in last place); and Pearson correlation between the shuffled-order distribution of results and the true value. The goal is to characterize when disagreements are sub-ULP, single-ULP, or multi-ULP.

**Step 4: Construct a downstream consequence demonstration.** Build a minimal pipeline: compute the mean of a real dataset, use it as a classification threshold (values above mean → class 1), and count how many predictions change when the summation method changes. If no predictions change on the benign inputs, use adversarial inputs and report the pipeline construction required to produce a visible change.

**Step 5: Document inline.** Every experiment that does not produce the expected result is logged in the notebook at the point of failure, not omitted or moved to an appendix.

## Expected output

A Jupyter notebook, committed to the College's repository with pinned dependencies via `requirements.txt` (numpy, pandas, scipy, and nothing else), that:

- Runs to completion from a single `jupyter nbconvert --to notebook --execute` call on a standard CPU
- Produces all figures and tables from the data without manual intervention
- Includes a runbook that specifies exact Python and library versions, plus instructions for downloading the GHCN and CIFAR-10 data from their public sources
- Summarizes results in one table: input type × summation method × disagreement magnitude
- States clearly whether downstream predictions changed, and if so, under what conditions

The accompanying blog post will be approximately 1,200 words, structured as: the phenomenon stated plainly, the demonstration results, what they mean for practitioners, and what conditions produce visible downstream effects.

## Resource estimate

Compute: no GPU required; all experiments run on a single CPU core. The GHCN daily data download is approximately 3 GB compressed but can be filtered to a small subset for the demonstration. CIFAR-10 is 170 MB. Total compute time estimated at under 2 hours of wall time.

Time: approximately 8–12 hours of intermittent work across one week. The implementation of Kahan summation and the decimal reference computation are the most time-consuming parts; the analysis and writing are straightforward once the measurement framework is in place.

Tool use: standard Python scientific stack only. No cloud APIs, no paid services, no LLM calls during experiment execution.

## Anticipated failure modes

**The disagreements are too small to matter.** On benign, well-conditioned inputs, all four methods may agree to 15 significant figures, and the downstream threshold demonstration may show zero prediction changes. This is an honest and publishable result: it would mean that practitioners worrying about summation order are, for typical data, worrying about the wrong thing. The post would say so plainly.

**The adversarial inputs are too artificial.** I may fail to find a realistic dataset where summation order visibly affects a downstream result, making the demonstration feel staged. If this happens, I will publish the failure alongside the adversarial case and characterize exactly what input structure is required to produce a visible effect.

**NumPy's pairwise algorithm is already good enough.** If pairwise and Kahan agree to within one ULP on all tested inputs, the demonstration collapses to "use numpy, not your own loop." That is still a useful operational conclusion, and I will publish it as such.

**The GHCN data download or format changes.** As a fallback, I will use synthetic data drawn from distributions matched to the real datasets, and note the substitution explicitly.

## Collaborators needed

None required for execution. If the results suggest a theoretical bound is being violated or a surprising pattern requires explanation, a Fellow specializing in mathematical analysis would be useful for a follow-on piece. The current proposal is self-contained.
