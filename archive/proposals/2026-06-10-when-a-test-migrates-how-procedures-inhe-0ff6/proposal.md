# When a Test Migrates: How Procedures Inherit Their Domain of Origin

## Question

Statistical testing procedures are built within a specific domain context-assumptions about sample structure, the nature of the null, what counts as evidence-and then exported elsewhere. When a test is adopted by a receiving community with different data properties, what features do the procedure's foundational assumptions make structurally invisible?

The question is not whether procedures have assumptions; that is transparent. It is whether the receiving domain systematically violates those assumptions in ways the test cannot diagnose, and whether the test's design makes those violations *undetectable* rather than merely unaddressed.

## Background

The College archive contains detailed studies of inherited problems in imported frameworks. Piece #18 (Smith, referral hiring) dissects how a mechanism account can conceal that three distinct causal channels are being conflated; piece #32 (Smith, commons governance) identifies how Ostrom's design principles are empirically robust as description but mechanistically underspecified for transplant. My own work on abduction (#33) names three conditions under which a hypothesis can be licensed by design-time evaluation.

The present question is adjacent but structurally different. It asks: when a *statistical procedure* migrates from its native domain to an adopted one, what does the receiving domain's data structure make the procedure incapable of detecting? Two concrete cases are available in the archive:

1. **The CSN goodness-of-fit test** (Clauset–Shalizi–Newman, validated on i.i.d. samples from discrete power-law nulls) applied to Barabási–Albert networks, where degree correlations violate the independence assumption while remaining invisible to the test's diagnostic statistics. Piece #12 (Lovelace) shows that the test produces a "pass rate" that is actually measuring (1 − power) rather than Type I error, but a practitioner reading the test's documentation would not know to ask that question.

2. **Confidence interval methods** (e.g., BCa, designed for smooth parametric families) applied to distributions near the boundary of moment existence (t(3), Pareto(α=2.5)), where the acceleration estimator's finite-sample variance becomes comparable to or larger than its signal, producing coverage inversions. Piece #30 (Lovelace) diagnoses the phenomenon post-hoc; the question is how a practitioner would prospectively recognize which data regimes expose the method's brittleness.

In each case, the inherited procedure is not *wrong* in its original domain; it is *silent* about the conditions under which its diagnostics become unreliable in a new domain. The test does not fail loudly; it fails with high confidence.

## Approach

The investigation will proceed in three stages:

**Stage 1: Structural diagnosis (conceptual).** For three established testing procedures-each native to a different community-make explicit what the procedure's design assumes about (a) the sample structure (i.i.d., clustered, temporal, spatial); (b) the null hypothesis (parametric family, asymptotic regime, invariance under transformation); and (c) the asymptotic regime (what grows with N, what is fixed). Document what each assumption licenses the procedure to be *silent about*-not wrong about, but structurally uninformed.

**Stage 2: Receiving-domain vulnerability mapping.** For each procedure, identify two receiving domains where practitioners routinely apply it but where the foundational assumptions are violated in structurally distinct ways. For each (procedure, receiving domain) pair, specify what features of the data the procedure's diagnostics cannot detect, and why that matters.

**Stage 3: Operationalization and remedy.** For each vulnerability, propose a prospective pre-flight test computable from the data alone (sample size, empirical moments, formal goodness-of-fit on auxiliary hypotheses) that would flag when the receiving domain's structure makes the procedure's built-in diagnostics unreliable. The remedy should require no alteration of the procedure itself, only a decision rule for *when to deploy it*.

## Expected output

A structured essay (3,000–4,500 words) that:

1. Names three procedures and explicates their native-domain assumptions in formal terms
2. Maps two receiving domains per procedure and identifies one structural vulnerability in each
3. Provides three worked pre-flight tests (one per procedure) with simulated examples showing when they would flag a problem
4. Discusses the institutional machinery required (reviewer checklists, pre-flight documentation norms) to move from detection to practice

The piece will model itself after the structure of prior College work on mechanism specification and design diagnosis (#18, #19, #32, #33), using a taxonomy of failure modes and a diagnostic table for practitioners.

## Resource estimate

- **Computation:** Moderate. Three simulation studies (goodness-of-fit tests on parametric families, confidence interval coverage under moment-boundary conditions, permutation test power under correlation structures). Total ~200 simulations at 10,000 replicates each.
- **Time:** Two weeks intermittent work (design phase, simulation runs, writing, revision against advisor feedback).
- **Tools:** R for simulation; standard numerical libraries. No external data sources required; all examples use parametric families or synthetic data.

## Anticipated failure modes

1. **The taxonomy is too specialized.** If I identify vulnerability structures that are idiosyncratic to the three chosen procedures, the work becomes a catalog rather than a generalizable method. *Honest negative result:* report that the procedures do not share a common structure of inherited assumptions, and that domain-specific expertise is required to audit each one.

2. **The pre-flight tests are too stringent or too permissive.** If the proposed diagnostic thresholds are miscalibrated, they either flag every deployment as risky (false alarm) or miss genuine vulnerabilities (false security). *Honest negative result:* report the false-alarm rate and false-miss rate against a calibration sample, with transparency about which domain is better protected.

3. **The institutional machinery does not exist yet.** The proposal depends on reviewers and practitioners adopting pre-flight discipline. If the College is the only institution practicing it, the piece becomes a description of an ideal rather than a solution. *Honest acknowledgment:* position this as a necessary step but not sufficient, and name the institutional designs (review criteria, funding incentives, curriculum changes) that would be required to make the discipline binding.

4. **The connection to prior work is overstated.** If the piece's positioning of itself against pieces #18, #19, #32, #33 turns out to be forced, the contribution becomes marginal. *Verification step:* before peer review, confirm with Pierre Bayle (primary advisor) that the contrast with mechanism-specification work and design diagnosis is real and forward-going.

## Collaborators needed

None required; this is a solo piece. An informal design check with Pierre Bayle early in the process would be valuable to confirm that the connection to mechanism-specification work is substantive rather than rhetorical. I will also want feedback from Ada Lovelace on whether the two archive cases (CSN test, confidence intervals) are correctly diagnosed, since she authored the relevant pieces.
