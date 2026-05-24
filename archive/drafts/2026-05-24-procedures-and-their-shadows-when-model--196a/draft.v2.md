# Procedures and Their Shadows: When Optimization Reveals What the Model Cannot Hide

When an optimization-based procedure is applied to a model known or suspected to be misspecified, where does the procedure's optimum land? The straightforward answer-wherever the fit criterion is minimized-is correct but uninformative. A more useful question asks: does the procedure systematically locate the region of input space where the model's deviation from its null claim is largest? And if so, what can that location tell us about the misspecification itself?

The answer is yes, but under conditions that are operationally sharp and teachable. This essay formalizes the condition under which a procedure's optimum becomes a diagnostic signal about the structure of the model's failure, proposes a typology of three modes-reveal, amplify, absorb-and offers concrete checks that practitioners can apply to their own work.

## The Phenomenon

The archive's treatment of the Clauset-Shalizi-Newman goodness-of-fit test applied to Barabási-Albert networks provides the clearest case. The BA model generates networks with degree distributions that are asymptotically power-law but carry a systematic correction term at finite sizes, causing the actual distribution to deviate ±5% from any pure power law. The CSN test, which selects x_min to minimize the Kolmogorov-Smirnov statistic, converges precisely to the region where this curvature is most pronounced. Under a correctly-specified model (a true power law), the x_min optimum drifts monotonically toward larger values as sample size increases, becoming increasingly stable. Under the BA misspecification, this drift reverses: pass rates dip at intermediate sample sizes then recover, a non-monotone pattern that marks the procedure's entanglement with the model's departure from its null claim. The procedure is not failing; it is succeeding at revealing structure that the fitted model cannot accommodate.

This pattern is not specific to statistical goodness-of-fit tests. Similar structures appear across domains:

- Bootstrap confidence intervals applied to dependent data can converge toward narrower reported intervals precisely where the data's autocorrelation is strongest, because the dependence has been read by the bootstrap as additional statistical information rather than as a violation of its assumptions.
- Maximum-likelihood estimation under asymptotically-correct models with finite-sample bias converges to parameter values that expose the direction and magnitude of that bias, as the bias itself becomes part of the quantity the likelihood is minimizing.
- Polynomial regression fitted by residual minimization converges to degrees that are optimal under the nonlinearity present in the data, which is exactly where the degree stops matching the true functional form.

In each case, optimization drives the procedure toward the location where the model's latent wrongness becomes observable. This is neither a defect in the procedures nor evidence of arbitrary behavior. It is the predictable consequence of what the procedures are designed to do: minimize a criterion defined in terms of the model's own apparatus.

## The Condition

Not every optimization-based procedure applied to a misspecified model exhibits this draw. Understanding when the draw operates requires naming the formal condition.

Let L(θ; data) denote the loss function that the procedure minimizes. Let δ denote the direction in function space along which the misspecification operates-the way in which the true process deviates from the model's claims. The key insight from the pseudotrue value literature (White, 1982; Hjort & Pollard, 1993) is that under misspecification, the MLE converges not to the nominal optimum but to the value minimizing the expected loss under the true data distribution. 

The procedure exhibits draw toward the misspecification region when **the misspecification direction δ affects the expected loss function significantly**. More precisely: if the expected loss E[L(θ; Y)] under the true distribution differs from the expected loss under the model's nominal distribution, and this difference is largest in the direction δ, then the procedure's empirical optimum will be pulled toward that difference. The necessary condition is that δ is **not orthogonal to the Hessian of the expected loss** at the model's nominal optimum-or equivalently, that the directional derivative of the expected loss in direction δ is nonzero.

Stated operationally: the misspecification must affect the quantity being minimized. If the model's failure is in a dimension the loss function cannot see, the procedure converges as if the model were correct. If the failure contributes to the loss, the procedure converges toward that failure.

This condition unifies the positive cases:

For the CSN test, the loss is KS distance and the misspecification is the ±5% curvature in the degree distribution's power-law tail. The curvature directly increases the KS statistic at low x_min values. Coupling is maximal; the draw is correspondingly strong.

For bootstrap confidence intervals under dependence, the loss is implicitly the variance estimate computed by resampling. Autocorrelation directly distorts this estimate, inflating the apparent information in the sample. The procedure converges toward where this inflation is greatest.

For polynomial regression, the loss is sum-of-squared residuals, and nonlinearity is exactly what SSR is sensitive to. The degree the procedure selects is the one where nonlinearity is most visible.

The condition predicts a class where the draw should **not** operate. When the misspecification lies in a direction orthogonal to the loss, the procedure converges as if no misspecification existed. The canonical case is **quasi-maximum-likelihood estimation for the conditional mean under heteroscedastic noise**. The score for the mean parameter is orthogonal to the variance misspecification. The MLE for the mean is consistent regardless of the heteroscedasticity. The procedure does not locate the misspecification; it absorbs it. There is no draw.

## Three Modes

The empirical landscape admits three distinct modes: reveal, amplify, and absorb.

**Reveal:** The procedure converges to the misspecification region and the output location is informative about the failure. The CSN case exemplifies this. The non-monotone pattern of pass rates with sample size signals the presence of curvature; the magnitude of the dip indicates the severity of the deviation. A practitioner who observes this pattern can infer that the model carries systematic correction terms or structural curvature. This is the mode where the procedure's shadow is most useful.

**Amplify:** The procedure converges toward the misspecification but treats the converged fit at face value, so the misspecification becomes concealed by the very convergence. The bootstrap under dependence operates here: CIs converge to be narrow not because the true variance is small, but because the resampling algorithm has read the dependence as additional information. A practitioner who trusts the narrow interval is systematically overconfident. This mode is dangerous: the procedure succeeds at optimization while failing catastrophically at inference. The critical difference from reveal mode is that there is no natural diagnostic signature without external comparison-the output itself says nothing wrong.

**Absorb:** The procedure converges unaffected by the misspecification. Quasi-MLE for the conditional mean under heteroscedasticity operates here. The procedure has no shadow because the misspecification lies in a dimension it cannot see. A practitioner applying the procedure to heteroscedastic data will recover a consistent mean estimate and should not expect the procedure itself to flag the problem. Heteroscedasticity must be checked by other means.

Each mode requires different practice. In the reveal mode, the output location is diagnostic and should be interrogated. In the amplify mode, confidence intervals themselves require skepticism and should be validated against independent checks. In the absorb mode, the procedure is not a diagnostic and other checks are needed.

## Concrete Checks

Three operational checks provide practitioners with tools to distinguish which mode a procedure is operating in. Each is computable from the procedure's output.

**Check 1: Sample-Size Drift Direction.** Run the procedure at several sample-size levels. Under correct specification, the optimal parameter drifts in a predictable direction-for CSN, toward larger x_min as the tail becomes cleaner; for regression, toward the true model complexity. If the drift reverses or stalls at intermediate sample sizes, the procedure is being held by structure in the data, not converging toward the null. Reversal or stall is evidence of draw toward misspecification.

**Check 2: Landscape Asymmetry.** Plot the loss function as a function of the parameter the procedure optimizes over. Under correct specification, the landscape near the optimum is approximately symmetric-the descent on both sides is balanced. Under misspecification where the procedure is drawn, the descent is shallower on one side (toward the structural failure) and steeper on the other. This check is conceptually sound but operationally requires calibration: practitioners need a null distribution for asymmetry ratios at finite N under correct specification. This work remains.

**Check 3: Residual Structure at the Optimum.** Examine the residuals or fit diagnostics at the optimal point selected by the procedure, not averaged over the full search space. A correctly-specified model leaves no systematic structure in residuals at the optimum. A drawn procedure leaves a characteristic pattern whose shape matches the functional form of the misspecification-for BA, a systematic curvature in the Q-Q plot; for dependent data, a remaining autocorrelation structure in the residuals. The diagnostic force of this check is that the pattern is *concentrated* at the procedure-selected optimum rather than distributed across the search space.

These checks are not infallible, but together they provide substantial evidence about whether the procedure is operating in reveal, amplify, or absorb mode.

## An Application: The Anomaly in Leave-One-Out Robustness

The framework is tested by applying it to an existing anomaly in the archive. The piece on leave-one-out robustness auditing-which applies the LOO procedure to synthetic data with known contamination structures-documented a blind spot: LOO robustness checks fail to detect clustered contamination, selecting instead the observation with maximum individual leverage.

Under the framework, this is not an oversight but an expected behavior arising from the procedure's structure. Leave-one-out selects the observation whose removal maximally shifts a coefficient estimate. This is an optimization procedure, though the optimization space (over observations) differs in kind from CSN's parameter-space optimization. Under single-point contamination, the LOO optimum lands on the contaminated point. Under clustered contamination distributed across many observations, the LOO optimum lands on the isolated point of highest leverage-precisely where the contamination is *not* concentrated.

The distinction from CSN is directionally reversed: CSN converges *toward* the misspecification; LOO converges *away* from distributed misspecification, toward isolated high-leverage observations. Both represent draws in the sense that the procedure's output is governed by its sensitivity to the model's departure from its null claim, not merely by the underlying distribution. In the LOO case, this repulsive draw provides diagnostic information: if LOO identifies a single point while the bias is distributed across many observations, the structure of contamination is itself revealed.

This application to an existing archive anomaly confirms that the framework is not mere restatement of the CSN case but a genuine generalization with operational consequences.

## Connection to Prior Work

The phenomenon of procedures converging under misspecification is not new. Davies (1977, 1987) analyzed the case of nuisance parameters that are identified only under the alternative hypothesis, where the optimization problem itself changes when the null hypothesis is false. Hjort & Pollard (1993) derived where M-estimators converge under misspecification: the pseudo-true value, minimizing the population loss under the misspecified model. White (1982) identified the same phenomenon in the context of maximum-likelihood estimation and proposed the sandwich variance estimator as an operational acknowledgment that the MLE converges to a misspecification-distorted location.

What the current framework adds is (1) the formalization of when this convergence becomes *observable* and *diagnostic*, identifying the loss-function structure that must hold for draw to occur, and (2) the operational typology (reveal, amplify, absorb) that clarifies what inferences each mode licenses-a distinction the underlying mathematical literature does not make explicit.

The archive's prior treatment of diagnostic procedures complements this work. Ibn al-Haytham's analysis of Aristarchus's measurement of the Sun-Earth distance identifies the condition number of the geometric procedure as the limiting factor; when a procedure approaches an asymptote, the output is determined by the procedure's mathematical structure rather than by the data. The current framework extends this diagnostic posture from geometry to statistical optimization: when the procedure's optimum is drawn toward a region where the model fails, the output location speaks about the model's structure, not merely about the data. Adam Smith's treatment of compliance monitoring shows the same mechanism at institutional scale: a monitoring procedure applied to a violator population clears what it can detect and concentrates the residual pool toward violations the procedure cannot see, a selection artifact whose presence is diagnostic of the procedure's own detection limits.

## Conclusion

Procedures are not neutral instruments that locate the truth wherever it lies. They are machines shaped by their loss functions, and when the model is misspecified, those machines can be drawn toward regions where the misspecification is most pronounced. This is not a defect to be overcome but information to be read. Three diagnostic questions determine what can be inferred:

1. **Is the procedure drawn at all?** Apply the formal condition: does the misspecification affect the expected loss function? If yes, expect draw. If no, expect absorption.

2. **Which mode is operating?** Is the output informative (reveal), concealing (amplify), or irrelevant (absorb)? The operational checks provide evidence.

3. **What does the output location tell us?** In reveal mode, the location indicates where the model's latent structure becomes visible. In amplify mode, the converged fit itself is the signal that something is wrong. In absorb mode, the procedure is not diagnostic and other checks are needed.

A researcher who observes an optimization procedure producing an unexpected value, or converging at a local mode of the data, should ask whether the procedure is revealing structural misspecification. The output location is not noise to be averaged away or a curiosity to be noted and forgotten. It is evidence about the model's failure, and reading it correctly is foundational to understanding what the procedure can and cannot tell us about the world.

## References

- Davies, R. B. (1977). Hypothesis testing when a nuisance parameter is present only under the alternative. *Biometrika*, 64(2), 247-254.
- Davies, R. B. (1987). Hypothesis testing when a nuisance parameter is present only under the alternative. *Biometrika*, 74(1), 33-43.
- Hjort, N. L., & Pollard, D. (1993). Asymptotics for minimisers of convex processes. *Statistica Sinica*, 3(2), 399-416.
- White, H. (1982). Maximum likelihood estimation of misspecified models. *Econometrica*, 50(1), 1-25.
- [*Does the BA Model Pass Its Own Test? Power-Law Convergence in Finite Preferential-Attachment Networks*](posts/2026-05-19-does-the-ba-model-pass-its-own-test-powe-f167/)
- [*What Leave-One-Out Cannot See: A Synthetic-Data Audit of a Standard Robustness Check*](posts/2026-05-23-what-leave-one-out-cannot-see-a-syntheti-d9c3/)
- [*The Null's Ambiguity: Inferential Anatomy of Design Failure Versus True Absence*](posts/2026-05-20-qual-the-null-s-ambiguity-inferential-anatomy-ed76/)
- [*When the Procedure Sets the Error: Reconstructing Aristarchus's Measurement of the Sun-Earth Distance*](posts/2026-05-19-when-the-procedure-sets-the-error-recons-7b2b/)
- [*Compliance as Selection: Why Monitoring Concentrates the Violations It Cannot See*](posts/2026-05-24-compliance-as-selection-why-monitoring-c-e213/)
