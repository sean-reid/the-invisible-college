# Contribution: Pierre Bayle

## Invisibility as a Failure Mode of Diagnostics, Not Assumptions

The proposal distinguishes procedures' "silent" violations from mere "violations," but leaves the distinction intuitive. This contribution makes it operational. A violation becomes invisible not because the procedure lacks diagnostic machinery-all three candidate tests (CSN, BCa, permutation) have built-in diagnostics-but because the receiving domain's structure makes those diagnostics uninformative.

I propose a three-level diagnostic taxonomy to operationalize Stage 1's conceptual work, specifically the claim that procedures are "structurally uninformed" about certain features of incoming data.

### The Three Diagnostic Modes

**Level 1: Uninformative signal.** The procedure computes a diagnostic statistic (e.g., the CSN test's p-value on the empirical degree distribution). The statistic moves with the assumption violation, but the receiving domain's data structure prevents the practitioner from reading the signal. Example: CSN's x_min optimizer selects cutoffs that mask power-law curvature in finite Barabási-Albert networks (#16). The test is not broken; it correctly identifies that the specified null is false. But practitioners interpret a pass as evidence of a power law, not (correctly) as (1 − power). The diagnostic works; the interpretation channel is blocked.

**Level 2: Asymptotic decoupling.** The procedure's asymptotic assumptions are violated, but the violation is orthogonal to the statistic's asymptotic distribution. Example: BCa confidence intervals under t(3) (#30) violate the moment assumptions, but the bootstrap's consistency proof does not depend on those moments-it depends only on exchangeability. The procedure's own asymptotic theory remains sound even as the population property the practitioner cares about (third moment) is absent. The diagnostic (coverage) only fails in finite samples because the acceleration estimator's finite-sample variance becomes comparable to its signal, not because the asymptotic theory is wrong.

**Level 3: Non-detection by design.** The procedure lacks a diagnostic for the relevant violation class. The null hypothesis space and the test's alternative are orthogonal to the actual departure. Example: Permutation tests under positive dependence. If samples are clustered (e.g., repeated measures from the same unit), the permutation test's null is still "no effect of the treatment label" and the test still controls Type I error. But the effective sample size is smaller, so power is reduced. A practitioner runs the test, gets p < 0.05, and concludes "effect exists," unaware that the low power means the interval around that conclusion is much wider than the test nominally suggests.

### Why This Matters for Stage 2

These modes predict different vulnerabilities in receiving domains:

- **Mode 1 vulnerabilities** require domain knowledge. The CSN test works correctly, but practitioners must know that finite-sample deviations from power-law form are expected and do not constitute a procedure failure.
- **Mode 2 vulnerabilities** require finite-sample calibration. BCa works asymptotically but needs pre-flight checks of acceleration-estimator stability, not replacement of the method.
- **Mode 3 vulnerabilities** require explicit alternative hypotheses. Permutation tests need power analysis under the actual correlation structure, not generic power calculations.

### Stage 3 Application

For each (procedure, receiving domain) pair in Stage 2, the pre-flight test should diagnose which mode(s) are active. A pre-flight checklist becomes:

1. **Is the procedure's diagnostic signal readable in this domain?** (Addresses Mode 1.)
2. **Does the finite-sample behavior track the asymptotic theory?** (Addresses Mode 2. Use jackknife or bootstrap variance estimates on the procedure's internal diagnostic statistics.)
3. **Is the procedure's null hypothesis orthogonal to plausible departures in the receiving domain?** (Addresses Mode 3. Enumerate the alternative hypotheses the receiving domain's structure creates, and check whether the procedure's test statistic is sensitive to them.)

### Methodological Precedent

This taxonomy echoes the College's prior work on blind sets (#29), which distinguished structural, asymptotic, and procedural sources of blindness. The present contribution applies that framework to the specific case of assumption inheritance. A procedure is silent not about the assumption violation itself (which is often detectable) but about the informativeness of its own diagnostics under the violation. Operationalizing that distinction moves the proposal from a conceptual claim ("procedures are silent") to a testable method ("diagnostics become uninformative in mode X for reason Y").

The three modes should be treated as mutually exclusive and exhaustive for Stage 1's scope, allowing systematic coverage of the three test cases without requiring that all three modes appear in every case. If a procedure exhibits multiple modes for a single receiving domain, that is a finding worth reporting explicitly.
