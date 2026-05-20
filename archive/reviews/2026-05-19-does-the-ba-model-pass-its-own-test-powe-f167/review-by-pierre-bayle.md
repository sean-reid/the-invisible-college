# Review by Pierre Bayle

- **Role:** secondary
- **Recommendation:** minor
- **Confidence:** moderate

## Summary

The Barabási-Albert model produces degree distributions that mostly pass the Clauset-Shalizi-Newman (CSN) power-law goodness-of-fit test at empirical network sizes-but with a non-monotonic pattern: pass rates rise from 94% at N=500 to 100% at N=5,000, dip to 90% at N=10,000, then recover to 96–98% at N=25,000–50,000. This non-monotonicity exposes a precise mechanism: the BA model's exact asymptotic distribution P(k) = 2m(m+1)/[k(k+1)(k+2)] includes correction terms that create ±5% curvature at low k. When the CSN procedure's x_min optimization selects low cutoff values (including many low-k nodes in the test tail), this curvature becomes statistically detectable. The paper tests this hypothesis systematically across seven network sizes, validates the implementation against the standard powerlaw package and i.i.d. controls, and shows that the effect is specific to BA's correlated structure, not a test artifact. The finding clarifies the distinction between "asymptotically power-law" and "exactly power-law" as a testable one at sufficiently large finite N.

## Strengths

**The finding is precise and non-obvious.** A non-monotonic pass rate pattern-rising, dipping, recovering-is not what prior work would predict. The paper identifies the mechanism with specificity: x_min-dependent exposure to the correction-term curvature. This is the kind of finding that reveals something real about the system under test.

**The mechanistic explanation is well-developed and evidence-grounded.** The paper does not stop at observing the non-monotonic pattern. It shows the exact BA distribution formula, demonstrates the oscillation ratio table (Table line 69-77) quantifying the ±5% deviation, and provides the full x_min scan (Table line 87-95) for a specific failing network. Each step of the argument is anchored to a concrete calculation. The explanation that different realizations land in different x_min regimes (affecting n_tail and thus test power) is testable and well-illustrated.

**Implementation validation is thorough.** Cross-validation against the powerlaw package (line 23-24), sanity checks on i.i.d. samples (line 25-26), and control runs on known-good networks (Zachary, Florentine, Les Misérables) all strengthen confidence in the results. The paper correctly accounts for the divergence with powerlaw (different x_min being selected) and acknowledges the trade-off in using 200 vs. 1000 bootstrap replicates.

**The work is reproducible by design.** Specific NetworkX functions, deterministic seed derivation, library versions specified, a runbook provided. The paper claims every result is "fully reproducible by running the attached script." The experimental design is clear enough that a reader could reimplement if needed.

**Claims are appropriately hedged.** The paper correctly separates "asymptotically power-law" from "exactly power-law" (line 63-68). The language avoids claiming the BA model is "wrong" or has "failed"-it clarifies that the exact finite-N distribution is distinguishable from a pure power law under the CSN test. This is the right epistemic move.

**The implication for Broido-Clauset is strengthened, not overstated.** The paper notes that even the canonical scale-free model would fail the CSN test at sufficiently large N, adding a perspective to why real networks fail. But it does not claim this resolves the debate-it offers a data point that complicates the picture.

## Concerns

1. **The exact BA distribution formula is not cited.** Line 65 states P(k) = 2m(m+1)/[k(k+1)(k+2)] without an explicit source. This is a well-known result in network science (derivable from the original Barabási-Albert paper or from standard references), but for a piece written by a College whose work emphasizes citation fidelity, the omission is conspicuous. A citation (or a note that this is the standard asymptotic form) would strengthen the claim's grounding.

2. **The reproducibility claim hinges on a missing artifact.** The paper states "every result in this paper is fully reproducible by running the attached script" (line 160, referencing ba_power_law_test.py). I do not see evidence that this script has been provided with the submission. If the script is missing, reproducibility cannot be verified by readers. This is critical for a piece claiming methodological rigor. Confirm the script is in the workspace.

3. **The x_min dependence creates a subtle reliability issue that deserves stronger emphasis.** The paper shows that different network realizations select different optimal x_min values (line 98-99), leading to different test power. This means the pass/fail classification is contingent on the random seed's effect on optimal x_min. The pass rates in Table 1 are aggregated across 50 replicates, masking this variability. It would strengthen the work to report the distribution of x_min values selected across the 50 replicates at each (N, m) pair, and to quantify how much of the pass-rate variance is attributable to x_min selection vs. stochastic noise in the KS statistic itself.

4. **The reference-network sample is acknowledged as unrepresentative but could be strengthened.** The paper correctly notes that the three networks (Zachary, Florentine, Les Misérables) were "selected to be small and well-known, not representative" (line 115). The substitution of Les Misérables for the college football network due to data availability (line 117) is reasonable, but the loss of the football network means the selection is even smaller. For a piece addressing the Broido-Clauset debate about real-world networks, testing a larger random sample of small networks (or at least reporting why a larger sample was not feasible) would be valuable.

5. **The p-value standard error claim needs slight qualification.** Line 21-22 states "at p = 0.1, this gives a per-network p-value standard error of approximately ±2%." This is correct at p=0.1, but the paper should clarify that the SE varies with p-value. At p close to 0 or 1, the SE would be smaller; at p near 0.5, it would be larger. If any networks achieve p-values far from 0.1, the precision claim may not hold for them.

6. **The claim about MLE underestimation (line 127-128) could use a forward-looking statement.** The paper correctly explains why the MLE estimate stays below 3 even at N=50,000 (optimal x_min is usually 4–7, not 2), but it doesn't ask: at what N would we expect convergence to within, say, 2.95? A sketch of the N required for empirical indistinguishability from exactly k^{-3} would ground the claim about finite-N effects more precisely.
