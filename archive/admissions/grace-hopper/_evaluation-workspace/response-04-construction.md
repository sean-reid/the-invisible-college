# Response to Problem 4: Construction

## Option A: A Working Artifact

### The Problem

Flaky tests cost teams enormous amounts of time. A test that fails intermittently trains developers to distrust the test suite, encouraging them to re-run tests until they pass rather than investigating failures. But the underlying causes of flakiness are often opaque: timing-dependent bugs, race conditions, resource contention, or environmental factors that only manifest under specific load conditions. Most flakiness investigations end in guessing.

The question: **Can we build a tool that automatically correlates test failures with system state to reveal whether flakiness is caused by the test itself, the code under test, or resource constraints on the machine?**

### The Artifact: Test Flakiness Heat Map

A command-line tool that:

1. **Runs a test suite repeatedly** (N times, configurable; I propose N=50) while continuously sampling system state
2. **Records for each test execution**: pass/fail status, wall-clock latency, and sampled metrics (CPU%, memory%, disk I/O ops, thread count, file handles open)
3. **Builds a correlation matrix** comparing failure rate to each system metric across all tests
4. **Generates a heat map visualization** showing which tests fail under which conditions

### Inputs

- A test suite (any language; I'll prototype in Python with pytest)
- Configuration: number of runs, sampling interval (e.g., 100ms), system metrics to track, correlation threshold
- Optional: a baseline run on an idle machine to normalize resource metrics

### Procedure

For each of N test runs:
1. Start system metric sampling in a background thread (CPU, resident memory, open files, context switch rate)
2. Run the full test suite, recording per-test timing and pass/fail
3. For each test, compute the correlation coefficient between its pass/fail status and each system metric across all N runs
4. Flag tests where failure correlates strongly (r > 0.6) with a specific metric as "resource-constrained"
5. Flag tests with high failure rate but low correlation with any metric as "inherently flaky" (likely timing-dependent or buggy)
6. Output: a table and visualization showing test → metrics correlations

### Predicted Outputs

- Tests that fail consistently when CPU > 80% but pass under idle load → **resource contention issue**
- Tests with 30% failure rate but near-zero correlation with any metric → **timing bug or test isolation problem**
- Tests that never fail → **baseline for comparison**

### Two Ways This Could Mislead Me

**False negative: Flakiness with no system-level signature.** A test that fails randomly due to an inherent race condition in the code (e.g., a mutex ordering bug that only manifests under specific thread scheduling) might have no correlation with measurable system state. The tool would label it "flaky but not resource-constrained," which is correct but not actionable—I haven't identified the root cause. The artifact correctly identifies that the cause is not system resources, but the user might assume "no system cause" means "not worth investigating." Mitigation: clear messaging that low-correlation flakiness is still real and requires code inspection.

**False positive: Correlation ≠ causation.** A test might fail more often under high load, but not *because* of the load—perhaps high-load runs happen at certain times of day, and the database is slower then, and that slowness reveals a test that assumed instantaneous writes. The correlation is real but the causal mechanism is "database latency" not "system CPU." The tool would attribute the failure to CPU when the true cause is elsewhere. Mitigation: recommend that when a strong correlation is found, the user manually verify by deliberately replicating those conditions and confirming the test fails.

Additionally: **Confounding by test order.** If test N always fails because test N-1 leaves global state dirty, the tool might falsely correlate test N's failures with high memory usage that happened to occur during those runs, when the true cause is test isolation. Mitigation: randomize test order across runs, or run tests in isolation.

### Why This Matters

Most flakiness debugging is guesswork: "Rerun it locally," "Maybe it's the network," "Could be a race condition." This tool turns observation into data. Even if it doesn't solve flakiness (it won't—some flakiness has no measurable cause), it significantly narrows the search space for a developer: "This test only fails under CPU pressure" is a much stronger hypothesis than "This test is flaky."

The artifact is bounded (it doesn't require fixing the bugs it finds, only identifying their signatures), concrete (it produces a runnable tool), and honest about its limitations (it cannot detect causes with no system-level signal, and correlation is not causation).