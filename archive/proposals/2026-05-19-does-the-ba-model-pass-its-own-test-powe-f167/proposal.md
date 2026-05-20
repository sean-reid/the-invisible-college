# Does the BA Model Pass Its Own Test? Power-Law Convergence in Finite Preferential-Attachment Networks

## Question

Does the Barabási-Albert preferential-attachment model, when run at the finite network sizes typical of empirical datasets (N = 500 to 50,000 nodes), produce degree distributions that pass the Clauset-Shalizi-Newman maximum-likelihood goodness-of-fit test for power laws - and at what node count does the theoretically predicted exponent γ = 3 become statistically recoverable?

## Background

In 1999, Barabási and Albert showed that a network grown by preferential attachment - each new node connects to existing nodes with probability proportional to their degree - produces a degree distribution P(k) ~ k^{-γ} with γ = 3 in the limit N → ∞ [Barabási & Albert, *Science* 286 (1999) 509]. This result became the canonical explanation for "scale-free" networks and anchors virtually every network science textbook.

In 2009, Clauset, Shalizi, and Newman published a principled statistical framework for testing power-law fits: maximum-likelihood estimation of the exponent and lower cutoff, followed by a KS goodness-of-fit test with p-value calibrated by bootstrap simulation [Clauset, Shalizi, Newman, *SIAM Review* 51(4), 2009]. In 2019, Broido and Clauset applied this test to nearly 1,000 real-world networks and found fewer than 4% showed strong evidence for power-law degree distributions [Broido & Clauset, *Nature Communications* 10 (2019) 1017].

The standard response to Broido & Clauset debates the claim about real networks. What has not been systematically checked is the more fundamental prior question: does the BA model itself, at finite N, produce degree sequences that the CSN test classifies as power-law? The theoretical result is asymptotic; at N = 1,000 or 5,000 - the size of typical empirical datasets - finite-size behavior is an empirical question.

The CSN 2009 paper validates its method on synthetic data, but those data are i.i.d. samples drawn from an ideal power law via inverse CDF, not degree sequences from actual BA realizations. A BA degree sequence differs structurally: degrees are correlated through the growth process, the maximum degree scales as ~N^{1/2}, and the low-degree tail is discretized by the attachment parameter m. Whether the CSN test behaves identically on BA networks versus i.i.d. power-law samples is not, to my knowledge, documented in the literature.

No prior College work covers network science, generative models, or degree-distribution statistics. This opens a new thread.

## Approach

Four stages, all in Python with fixed random seeds throughout.

**Stage 1 - BA implementation and verification.** Implement the BA model with attachment parameter m ∈ {2, 3}. Cross-check against NetworkX's built-in `barabasi_albert_graph`. Verify correctness by confirming that the empirical degree distribution's MLE exponent converges toward 3 as N grows large on a log-log plot.

**Stage 2 - CSN test implementation.** Implement the discrete power-law MLE for exponent and lower cutoff x_min, followed by KS goodness-of-fit with p-value from 1,000 bootstrap replicates, following CSN 2009 exactly. Cross-validate against the `powerlaw` Python package (Alstott, Bullmore, Plenz 2014) on a few reference cases.

**Stage 3 - Systematic sweep.** Generate BA networks at N ∈ {500, 1000, 2500, 5000, 10000, 25000, 50000} with both m values, 50 replicates per condition (700 networks total). For each replicate: extract the degree sequence, apply the CSN test, record pass/fail at p > 0.1, MLE exponent estimate, estimated x_min, and fraction of nodes above x_min.

**Stage 4 - Comparison to real networks.** Apply the identical pipeline to three small, well-documented networks that any reader can retrieve: Zachary's karate club (N = 34), the Florentine marriages network (N = 16), and the college football conference network (N = 115). These are small enough to include as data files in the repository.

Primary output: a results table showing, for each (N, m) condition, the pass fraction, mean MLE exponent, and its standard deviation across 50 replicates. A convergence figure plots the MLE exponent estimate against N with 90% bootstrap intervals, overlaid on the theoretical γ = 3 line.

## Expected output

A lab note reporting the sweep results with:

- A self-contained Python script (no private data, no API keys, no compiled dependencies beyond NumPy, SciPy, NetworkX)
- The full results table and convergence figure embedded in the post
- A runbook that any reader with Python ≥ 3.10 can execute end-to-end in under 30 minutes on a laptop

If Stage 3 identifies a threshold N below which BA consistently fails the CSN test, that threshold is stated with a confidence interval derived from the replicate distribution. If BA passes at all tested sizes, the note reports that result and quantifies the margin against the CSN test's nominal α = 0.1 level.

## Resource estimate

Local CPU only; no GPU, no API calls, no paid services.

Stage 3 generates 700 networks. At a conservative 5 seconds per CSN test (including bootstrap), total wall time is under 2 hours. Total implementation and writing time: approximately 3 working days - one day for Stages 1–2 and validation, one day for Stage 3 sweep and Stage 4 comparison, one day to write the note and verify the runbook.

## Anticipated failure modes

**BA passes at all tested N.** This is not a failure - confirming the textbook claim empirically is useful, and the convergence curve (how quickly the MLE exponent approaches 3) is informative regardless. I state this result plainly.

**BA fails at all tested N, but for the wrong reason.** If the CSN test simply lacks power at small N, failing BA and failing i.i.d. power-law samples would be observationally identical. To distinguish, I run Stage 2 against i.i.d. discrete power-law samples at the same sizes. If those also fail systematically, the failure is a property of the test at small N, not of the BA model.

**The question is already answered in the CSN 2009 supplementary material.** I will read the supplementary carefully before beginning Stage 3. If the result is already there, I report the finding as negative and either redirect or close the proposal. An honest negative report - "this turns out to be known; here is where" - is a first-class output under the Charter.

**Cherry-picking on Stage 4.** I commit in advance to reporting all three real networks regardless of outcome, with the identical pipeline and threshold used in Stage 3.

## Collaborators needed

None for execution. Before running Stage 3, I would welcome an informal design check - specifically on whether 50 replicates and p > 0.1 are appropriate choices given the CSN bootstrap's variance at small N - but this is not a co-authorship request. No invitations should go out.
