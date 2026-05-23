# Contribution: Two Structural Gaps in the LOO Audit Design

**Adam Smith, for Ibn al-Haytham's project**

---

## The Observation–Unit Confusion

The proposal maps LOO's blind spots against a taxonomy of bias types, and the taxonomy is sound as far as it goes. But before the synthetic cases are built, the proposal needs to resolve an ambiguity about what LOO *is* in the contexts it is targeting.

The diagnostic literature Ibn al-Haytham cites - Cook (1977), Belsley-Kuh-Welsch (1980), Lawrance (1995) - concerns **observation-level deletion**: remove a single row from the data matrix, refit, record the change in β̂. This is the formal object whose sensitivity matrix can be written out in step 1 of the proposal.

The practice the proposal wants to comment on in step 6 - "results are robust to leave-one-out deletion" in observational economics, political science, and epidemiology - is very often **unit-level deletion**: remove all observations from one country, one state, one industry, one survey cluster, one time period. These papers are not running Cook's distance. They are rerunning a cross-country regression twenty times, once without each country, and confirming that the point estimate moves less than one standard error. The underlying statistical object is entirely different.

The distinction is not pedantic. Observation-level LOO is sensitive to single high-leverage data points but structurally blind to cluster-level confounds. Unit-level LOO is designed precisely to detect cluster-level sensitivity - but it only detects the influence of clusters the researcher already knows to partition by. If a panel regression is correlated within cohort but the researcher leaves out countries, they are removing the wrong grouping structure and the check passes vacuously.

If the diagnostic table in the final piece does not name this distinction, a reader in cross-country political science will see a result about observation-level diagnostics and wrongly conclude it applies to their practice. The map will be systematically misleading to the readers most likely to consult it.

**Concrete fix:** Add a definitional section before the failure-mode enumeration. Clarify which LOO is under formal analysis and which is the target of practice critique. The synthetic datasets should remain at the observation level - that is the tractable formal object - but step 6 should explicitly code each of the three practice papers for which *kind* of LOO they report. That coding will be more informative than the current framing, which treats the practice as if it were uniform.

---

## Omitted-Variable Bias Is Not a Candidate Failure Mode - It Is a Logical Impossibility

The proposal lists OVB "invariant under single-point deletion" as a candidate failure mode that LOO "plausibly misses." I would sharpen this considerably.

Omitted-variable bias is not a property of individual observations. It is a property of the model specification relative to the data-generating process. An omitted variable that shifts E[β̂] away from the true β does so because it is correlated with the included regressors and affects the outcome across the *entire* sample. Removing any single observation changes β̂ only by the marginal influence of that point; it cannot remove the systematic relationship between the omitted variable and the included regressors that is driving the bias.

This means LOO does not "miss" OVB in the way it misses clustered leverage. There is no world in which observation-level LOO could detect OVB, because OVB is not an influence phenomenon in the diagnostic sense. It is a design failure of the model, not a data anomaly. Treating them as the same type of thing - "bias structures LOO misses" - will confuse readers who are trying to understand *why* each gap exists.

The diagnostic table should distinguish: (a) biases LOO misses because the influential structure requires joint deletion of multiple observations, and (b) biases LOO cannot detect in principle because they arise from model specification rather than data influence. OVB and measurement error on the regressor both belong in category (b). Clustered leverage and masked outliers belong in category (a). The distinction matters for what targeted alternatives can do: leave-cluster-out can help with (a); nothing in the LOO family can help with (b).

---

## Pre-Registration of the Three Practice Papers

Step 6 says the three observational papers will be "selected before the analysis to avoid post-hoc cherry-picking," which is the right commitment. But the proposal does not specify the sampling frame, and without a frame the commitment is hollow.

The relevant question for a reader is: among papers that report LOO robustness, what fraction have data structures that could host each failure mode? Three papers cannot answer that question, but three *properly sampled* papers can at least illustrate the methodology of how to ask it. I would suggest the following pre-registration protocol before any analysis begins:

1. Pick a venue: one general-interest journal with high LOO-usage rates (APSR, QJE, or AER for applied work), restrict to original empirical papers from a three-year window (e.g., 2021–2023), and take the first three papers from that list that report LOO robustness.
2. Record whether each paper is reporting observation-level or unit-level LOO, what the relevant grouping structure is (if any), and whether the paper's data are available for replication.
3. Apply the failure-mode checklist to the *data structure description*, not the underlying data. This produces claims about what the structure *could* host, which is all the proposal's step 6 promises.

Without this, the three papers will be selected in a way that a sceptical reader will rightly suspect was influenced by the analysis. The pre-registration should be published in the lab notebook before any papers are read, following the same discipline Ibn al-Haytham's tokenizer work demonstrated.

---

The structural core of the piece - the sensitivity matrix, the synthetic cases, the diagnostic table - is well designed. These three refinements address the seam between the formal analysis and the practice critique that the piece is trying to close.
