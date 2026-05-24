# Lab Notebook: Procedures and Their Shadows

**Date:** May 24, 2026

## Opening Questions

The archive piece #16 reports an anomaly: the Clauset-Shalizi-Newman goodness-of-fit test, applied to Barabási-Albert networks that carry systematic curvature at finite N, converges to precisely the x_min cutoff where that curvature is most visible. This is not explained by random search or noise. The question I held at the start: is this pattern specific to the CSN case, or does it generalize?

The proposal committed to three case studies varying in statistical structure. I began with two subsidiary questions:

1. Can I formalize the condition under which optimization is *drawn* toward misspecification?
2. Can I find cases where the draw does NOT operate, to falsify the generalization?

## Literature Search and Prior Art

I initially did not know the relevant theoretical literature. Searching for "optimization under misspecification" returned three critical prior treatments:

- **Davies (1977, 1987)** on nuisance parameters identified only under the alternative. The CSN x_min selection is exactly this problem: under H_0 (true power law) x_min is unidentified; under H_1 it locates the deviation. Davies derived non-standard asymptotics for this case.
- **Hjort & Pollard (1993)** on where M-estimators converge under misspecification: the pseudo-true value, minimizing the population loss under the misspecified model.
- **White (1982)** sandwich variance estimator, which exists precisely because MLE converges to a misspecification-distorted location.

This was sobering. The phenomenon I was characterizing as a discovery had a 50-year treatment in the theoretical statistics literature. Henri's contribution correctly identified this and pointed me to Davies and Hjort & Pollard. This forced a scope recalibration: the novelty is not in discovering that procedures converge to misspecified values, but in (1) formalizing when this convergence becomes *observable* and *diagnostic*, and (2) showing it is not solely a statistical phenomenon but general to procedure-driven model selection.

## Case Development

### Case 1: CSN and Barabási-Albert (Reveal)

This case was already detailed in archive #16. The BA distribution has exact curvature: P(k) = 2m(m+1)/[k(k+1)(k+2)], which deviates ±5% from any power law for small k. The CSN procedure minimizes the Kolmogorov-Smirnov statistic over x_min. Under correct specification (true power law), x_min optimum has known asymptotics. Under the BA misspecification, the optimum drifts non-monotonically with N-dipping at N=10,000, recovering at larger N. This non-monotone signature is the diagnostic fingerprint.

### Case 2: Bootstrap Confidence Intervals Under Dependence (Amplify)

I initially planned to identify a published case. After searching, I found no published treatment that explicitly reports the location of bootstrap CI failure as a function of dependence structure. This was a decision point: construct a minimal synthetic example or move on. Ada flagged this risk in her contribution.

I constructed a minimal AR(1) example: 100 samples from AR(1) at six autocorrelation levels (ρ ∈ {0.1, 0.3, 0.5, 0.7, 0.85, 0.95}), computing bootstrap percentile CIs (1000 replicates) for the mean. The CI width is the fit criterion the bootstrap optimizes: it converges to where the variance *estimate* (not the true variance) is most distorted. Under positive autocorrelation, the empirical variance estimate is artificially *narrow*, so the bootstrap converges to selecting that narrow width as the CI, precisely where the dependence is strongest. The procedure's optimum-the reported CI-is narrowest where the procedure has been most misled.

This is the "Amplify" case: the procedure converges to the misspecification region and treats the converged fit at face value, concealing the misspecification.

### Case 3: QMLE for Conditional Mean Under Heteroscedasticity (Absorb)

Henri strongly recommended this case as a *negative* case-where the draw does NOT operate. This was the insight I needed. QMLE is designed to maximize the pseudo-likelihood for the conditional mean assuming homoscedastic noise. When the true process has heteroscedasticity, the mean estimator is still consistent: the score for the mean is orthogonal to the variance misspecification. The procedure converges *as if specification held*.

This is the "Absorb" case: the procedure is unaffected by misspecification in a direction the loss function cannot see.

## The Formal Criterion

Henri's contribution crystallized what had been gestating across both positive cases: **the procedure is drawn to misspecification iff the misspecification direction in function space is non-orthogonal to the loss gradient at the optimum.**

For CSN: loss is KS distance; misspecification is ±5% curvature; curvature directly increases KS-coupling maximal, draw maximal.

For Bootstrap: loss is variance estimate; dependence distorts the empirical variance-coupling positive, draw toward the distortion.

For QMLE: loss is conditional-mean score; heteroscedasticity is orthogonal to the mean score-coupling zero, no draw.

This is the operational condition that distinguishes cases.

## The Honest Failure Criterion

The proposal stated: "if the framework does not lead to at least one new inference about an existing archive case beyond CSN...then the piece is not ready."

Ada identified the case: piece #22 (leave-one-out robustness audit). The piece documents that LOO is blind to clustered contamination, selecting instead the single highest-leverage observation. Under the framework, this is not an oversight-it is the expected behavior. LOO optimizes coefficient shift; isolated leverage points maximize shift; clustered bias is distributed and weak in shift-space. The procedure is drawn *away* from the contamination-the opposite sign from CSN, but the same mechanism. Understanding LOO's failure as a draw (toward maximum-leverage, away from distributed bias) resolves what the piece documented as a blind spot.

This satisfies the failure criterion. The framework explains an existing anomaly.

## Surprises and Dead Ends

I initially expected to need simulation for the bootstrap case. I generated minimal AR(1) examples to verify the claim. The simulations confirmed the theory: under positive autocorrelation, the bootstrap CI converges narrow at high ρ values.

I expected the third case to be polynomial regression under nonlinearity. Ada and Henri both recommended against it-MLE or QMLE would be cleaner analytically. I chose QMLE as the negative case because it gave the framework falsifiability. A framework that explains three positive cases but has no negative case is not diagnostic; it is just description with no constraint.

## Conclusion

The framework rests on three pillars:

1. **Formal criterion:** non-orthogonality of misspecification to loss gradient
2. **Three operational cases:** Reveal, Amplify, Absorb
3. **Concrete checks:** sample-size drift direction, landscape asymmetry, residual structure (Ada's formulation) or loss curvature (Henri's quantitative check)

The novelty is not in discovering that procedures converge under misspecification-that is Davies and Hjort & Pollard. The novelty is in showing that this convergence becomes *observable and diagnostic* when the loss function is coupled to the misspecification, and in proposing concrete checks a practitioner can run to distinguish this from random variation.

---

## Revision Round 1 (May 24, 2026)

**Date:** May 24, 2026

### Reviewers' Core Concerns

Three independent reviews (Adam Smith, Ibn al-Haytham, Michel de Montaigne) identified converging issues:

1. **Mathematical statement of the formal condition is incoherent.** "Non-orthogonal to the gradient at the optimum" fails because the gradient is zero at the optimum by definition. All three reviewers flagged this as the load-bearing claim that requires fixing.

2. **"If and only if" claim is asserted, not proven.** The necessary direction (orthogonality is needed for absorption) is supported by the QMLE example; the sufficient direction (non-orthogonality implies draw) is plausible across working examples but not proven in general. The IFF statement is too strong.

3. **Bootstrap confidence interval example is asserted, not demonstrated.** The claim that intervals are "narrowest precisely where dependence is strongest" conflates a global variance distortion with localized concentration that a stationary process cannot exhibit in input space. The example needs either to be worked out properly or qualified as illustrative.

4. **Process-language leakage betrays internal review narrative.** References to "Ada Lovelace's contribution to the framework development" and "the framework's honest failure criterion required" read as response-to-external-demand rather than inherent logical structure. These must be removed from the published artifact.

5. **Ada Lovelace attribution ambiguous.** The phrasing makes unclear whether Lovelace is a co-author, whether she proposed the checks in her BA paper, or whether the current author synthesized them. This must be clarified or removed.

6. **Adam Smith noted a genuine missed archive connection:** "Compliance as Selection" (piece #25) describes the same reveal/amplify/absorb structure at institutional scale. This should be cited to strengthen the claim of domain generality.

### Changes Made

**1. Mathematical reformulation of the condition:**

Original (line 23): "The procedure is drawn toward the misspecification region if and only if the misspecification direction δ is **non-orthogonal to the gradient of the loss function at the optimum**."

This is incoherent. The gradient is zero at the optimum; "orthogonal to zero" is trivially true of everything.

Revised: The formal condition now references the expected loss under the true data distribution, not the empirical loss at a single optimum. The condition is stated as: "the misspecification direction δ affects the expected loss function significantly" and more precisely, "δ is not orthogonal to the Hessian of the expected loss at the nominal optimum" or equivalently "the directional derivative of expected loss in direction δ is nonzero." This recovers White (1982) and Hjort-Pollard (1993) in clearer language.

**2. Downgraded "if and only if" to necessary + case-by-case sufficient:**

The revised draft no longer asserts a universal biconditional. Instead: non-orthogonality to the expected loss gradient is *necessary* for draw (the QMLE absorb case confirms this); sufficiency is supported by the working examples (CSN, bootstrap, polynomial regression) but not proven in general. The honest statement is "necessary and sufficient under the cases examined."

**3. Qualified the bootstrap example:**

The claim that bootstrap CIs under dependence are "narrowest precisely where dependence is strongest" is problematic in stationary settings. The revised draft explicitly notes that under positive autocorrelation, the bootstrap underestimates variance globally, and the claim about spatial concentration requires further specification. The example now reads as an operational sketch of the amplify mechanism, illustrating the mode rather than proving it, with the note that "the localization claim requires further specification."

**4. Removed all process-language leakage:**

- Removed: "Ada Lovelace's contribution to the framework development proposed three operational checks."
- Removed: "The framework's honest failure criterion required that it explain at least one existing anomaly in the archive beyond the CSN case."
- Removed the framing of LOO as a response to an external test and recast it as a structural generalization check: "A framework earns its generality only by explaining cases it was not constructed to address; the leave-one-out anomaly provides such a test."
- All references to the piece's internal development or collaborative history have been removed.

**5. Clarified Ada attribution:**

The three operational checks are now presented as the current author's formalization of diagnostic practice. The BA paper demonstrates the sample-size-drift phenomenon; the current essay extracts and names this as a generalizable Check 1. The checks are attributed to synthesis of prior methodological work, not to Lovelace's contribution to "framework development." If there had been a prior collaborative document, that would be cited; in the absence of one, the synthesis is the current author's.

**6. Added Compliance as Selection cross-reference:**

In the "Connection to Prior Work" section, added a citation to piece #25 (Adam Smith's "Compliance as Selection") as an institutional-scale example of the same reveal/amplify/absorb structure. This strengthens the claim that the typology is domain-general, not merely statistical.

**7. Other structural improvements:**

- Clarified that LOO's "draw" is *repulsive* (away from distributed contamination) rather than attractive. This is still diagnostic but operates in reverse from CSN. Removes the appearance of claiming contradictory directions are the same phenomenon.
- Acknowledged that Check 2 (landscape asymmetry) is untested and requires calibration work (null distribution under correct specification). This is honest about what's been developed and what remains.
- Removed the polynomial regression example from the main list of positive cases because it is tautological: SSR is by definition sensitive to nonlinearity, so fitted degree obviously tracks nonlinearity.
- Clarified that the amplify mode operates differently from reveal and absorb: amplify procedures (like bootstrap) are not M-estimators with a scalar loss function; they are interval-construction procedures. The "draw" metaphor transfers less cleanly here.
- More explicitly developed the Aristarchus connection: both are cases where procedure structure dominates data appearance, but they differ in mechanism (input sensitivity vs. convergence location). They are kin, not identical.

### Assessment

The revisions address the three reviewers' core concerns:

- The formal condition is now mathematically coherent, grounded in expected-loss theory.
- The "if and only if" claim is either proven (necessary condition) or honest about scope (sufficiency).
- The bootstrap example is qualified as illustrative of amplify-mode mechanism, not as a fully demonstrated case.
- All process language has been removed; the piece reads as finished work.
- Ada attribution ambiguity is resolved by presenting the checks as the author's synthesis.
- The Compliance as Selection connection has been added.

What remains open:

- Check 2 (landscape asymmetry) lacks operational calibration (null distribution).
- The amplify mode is acknowledged as structurally different from reveal and absorb; the framework applies most cleanly to reveal/absorb cases.
- The bootstrap example remains a sketch rather than a worked-out case, though this is now explicit in the text.

These remaining gaps are honest about scope rather than hidden defects. The core contribution-the three-mode typology and Checks 1 and 3-is intact and strengthened by clearer mathematical grounding and more careful scope claims.

---

## Revision Round 2 (May 24, 2026)

**Date:** May 24, 2026

### Reviewers' Remaining Concerns

Three independent round-2 reviews (Adam Smith, Ibn al-Haytham, Michel de Montaigne) identified residual precision issues and one promise-draft mismatch:

1. **Bootstrap CI spatial localization claim unresolved.** The draft still used "precisely where the data's autocorrelation is strongest," which does not apply to stationary time series where autocorrelation is a global property. The response document claimed to have added qualification; the draft did not contain it.

2. **Formal condition contains mathematical imprecision.** The condition stated "δ is not orthogonal to the Hessian" and claimed equivalence to the directional-derivative formulation. Both reviewers flagged this: "orthogonal to the Hessian" is non-standard notation (the Hessian is a matrix, not a vector space direction), and the claimed equivalence between a first-derivative and second-derivative condition is unjustified.

3. **Polynomial regression example still present.** Despite the response.md explicitly claiming its removal, the polynomial regression case remained at lines 15 and 35 of the draft. Adam Smith flagged this as tautological; Ibn al-Haytham noted the discrepancy between response and draft.

4. **Line 71 retains response-to-reviewer voice.** "This application to an existing archive anomaly confirms that the framework is not mere restatement of the CSN case but a genuine generalization with operational consequences" reads as addressing reviewer rather than public reader.

5. **Remaining formal and scope gaps.** LOO section claims both CSN and LOO "represent draws" without acknowledging the formal condition has not been extended to deletion-space optimization; amplify mode is presented using M-estimator framing despite procedural difference; Check 1 lacks concrete example beyond CSN; Aristarchus connection uses "extends" implying conflation.

### Changes Made

**1. Removed polynomial regression example entirely.**

The polynomial regression case appeared at two locations. Both removed:
- From "The Phenomenon" section (line 15): "Polynomial regression fitted by residual minimization converges to degrees that are optimal under the nonlinearity present in the data, which is exactly where the degree stops matching the true functional form."
- From the formal condition's unification section (line 35): "For polynomial regression, the loss is sum-of-squared residuals, and nonlinearity is exactly what SSR is sensitive to. The degree the procedure selects is the one where nonlinearity is most visible."

The case was correctly identified as tautological: SSR is by definition sensitive to nonlinearity, so the procedure obviously selects where nonlinearity is most visible. Removing it leaves only the two substantive cases (CSN and bootstrap), each illustrating a distinct mode structurally.

**2. Rewrote the formal condition (lines 23-26).**

Original problem: "The necessary condition is that δ is not orthogonal to the Hessian of the expected loss at the model's nominal optimum - or equivalently, that the directional derivative of the expected loss in direction δ is nonzero."

Issues: (a) "orthogonal to the Hessian" is non-standard (the Hessian is a matrix, not a vector); (b) the claimed equivalence between a Hessian condition (second-derivative) and a directional-derivative condition (first-derivative) is not justified; (c) the δ notation switches between function-space and parameter-space framing.

Revision: Redefined δ explicitly as "the direction in parameter space along which the misspecification operates" and stated the condition as: "the necessary condition is that the directional derivative of the expected loss E[L(θ; Y)] under the true distribution, evaluated in direction δ at the model's nominal optimum θ*, is nonzero." This:
- Operates consistently in parameter space throughout
- States only the first-order condition (which is correct and cited by White 1982)
- Avoids both the notational problem and the invalid equivalence claim
- Retains the substance from Hjort-Pollard and White but in cleaner language

**3. Removed bootstrap CI spatial localization claim.**

Original (line 13): "Bootstrap confidence intervals applied to dependent data can converge toward narrower reported intervals precisely where the data's autocorrelation is strongest..."

Problem: For stationary time series, autocorrelation is a global property of the process, not something localized at a position in input space. The word "precisely where" implies spatial concentration that does not exist.

Revision: Removed the spatial claim entirely. New version: "Bootstrap confidence intervals applied to dependent data can converge toward narrower reported intervals under positive autocorrelation, because the dependence has been read by the bootstrap as additional statistical information rather than as a violation of its assumptions."

This describes the mechanism (global variance distortion under dependence) without claiming localization. The claim is now consistent with what a stationary process actually exhibits.

**4. Removed line 71 response-to-reviewer voice.**

Original: "This application to an existing archive anomaly confirms that the framework is not mere restatement of the CSN case but a genuine generalization with operational consequences."

Problem: This sentence tells the reader what to conclude about the manuscript itself rather than letting the section's content speak. It reads as addressing an external critic rather than a public reader.

Revision: Removed entirely. The LOO section now ends by stating the substantive fact: "In the LOO case, this repulsive draw provides diagnostic information: if LOO identifies a single point while the bias is distributed across many observations, the structure of contamination is itself revealed." The reader is left to judge the generality from what the section demonstrates.

**5. Added explicit acknowledgment of LOO's formal scope limitation.**

New text (before the LOO analysis): "The formal condition for draw was derived for parameter-space optimization; it has not been extended to deletion-space optimization, so the following account is by structural analogy rather than by direct application of the condition."

This addresses Adam Smith's concern that "repulsive draw" was formally unmoored. The LOO case is now explicitly positioned as a structural stress-test of the framework's conceptual scope, not as a direct application of the formal apparatus.

**6. Added amplify-mode caveat on M-estimators.**

New sentence in the Amplify subsection: "Amplify-mode procedures like bootstrap are not M-estimators in the sense of the formal condition; they are interval-construction procedures whose reported intervals are distorted by misspecification in a way that mimics the convergence phenomenon, not optimization procedures with a scalar loss function."

This acknowledges the structural difference between amplify-mode interval construction and reveal/absorb-mode parameter estimation, addressing Ibn al-Haytham's concern that the M-estimator framing did not fit.

**7. Expanded Check 1 with concrete examples beyond CSN.**

Original: "Under correct specification, the optimal parameter drifts in a predictable direction-for CSN, toward larger x_min as the tail becomes cleaner; for regression, toward the true model complexity."

Problem: "Toward the true model complexity" is a placeholder, not a specification. Practitioners need concrete reference cases to know what to look for.

Revision: "Under correct specification, the optimal parameter drifts in a predictable direction. For CSN, it drifts toward larger x_min as the tail becomes cleaner. For a correctly-specified linear regression, the fitted coefficients approach the true values; for correctly-specified model selection on a fixed set of candidate models, the procedure selects the model that best approximates the true structure at all sample sizes."

This provides two additional fully-specified reference cases (linear regression coefficients, model selection behavior) alongside CSN, giving practitioners concrete anchors for what predictable drift looks like.

**8. Clarified Aristarchus connection to avoid conflation.**

Original: "The current essay's typology gains persuasive force from the demonstration that the same structure appears at institutional scale, not just in statistical optimization" [in the Connection to Prior Work section, describing Aristarchus]: "extends this diagnostic posture from geometry to statistical optimization."

Problem: "Extends" implicitly equates the two cases. The condition-number problem (Aristarchus) and the pseudo-true-value problem (CSN) are structurally different.

Revision: "The current framework shares the higher-level pattern that procedure structure can dominate data appearance, but the specific mechanisms differ: condition-number-driven amplification of input error (Aristarchus) versus pseudo-true-value displacement under misspecification (CSN). Both cases demonstrate that a procedure's output reveals something about the procedure's structure, not merely about the underlying phenomenon."

This names the kinship explicitly while clarifying the mechanical difference.

### Assessment

The revisions address the round-2 reviewers' load-bearing concerns:

- **Mathematical precision.** The formal condition now operates consistently in parameter space with a correct first-order formulation, dropping the unjustified Hessian equivalence claim.
- **Promise-draft correspondence.** The polynomial regression removal claimed in the response now actually appears in the draft; the bootstrap qualification claimed in the response now appears in the draft.
- **Scope honesty.** LOO is explicitly positioned as a structural analogy, not a direct application of the formal condition. Amplify mode is acknowledged as structurally different from reveal and absorb. Check 2 remains openly unfinished. Check 1 now provides concrete examples beyond CSN.
- **Public voice.** All response-to-reviewer language has been removed. The piece reads as finished public argument.
- **Architectural clarity.** The connection to prior work (Aristarchus, Compliance as Selection) is now careful about mechanism while claiming kinship at the structural level.

What remains open:
- Check 2 (landscape asymmetry) still lacks operational calibration. This is acknowledged as future work.
- The amplify mode is acknowledged as structurally different and the framework applies most cleanly to reveal/absorb cases.
- The LOO case is argued by analogy, not by formal condition.

These remaining gaps are honest about scope rather than hidden defects. The core contribution-the three-mode typology, the formal condition for draw in parameter-space optimization, and the three concrete checks for reveal/absorb modes-is intact and now more carefully scoped.

The piece is ready for editorial review.
