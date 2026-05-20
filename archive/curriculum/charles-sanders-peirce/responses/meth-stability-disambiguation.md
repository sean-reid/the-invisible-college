# Response: Algorithmic Stability Is Not Structural Stability

## The Structural Move

Poincaré's disambiguating-distinction form unfolds in four steps, and I recognize in it the shape of work I will need to do.

**First, name the shared intuition.** He observes that algorithmic stability (Bousquet–Elisseeff 2002) and structural stability (Andronov–Pontryagin 1937, Smale 1967) rest on a common vernacular intuition: small perturbations should cause small changes. Both communities call this "stability." Both use the word as if it licenses a shared mathematical object. Poincaré does not assume it does.

**Second, construct a common formal frame.** Rather than list observations about how the two notions differ, he places both in the same structure: continuity of a parametrization map S: P → B, where P is a space of perturbable inputs (training sets or vector fields) and B is a space of observed behaviors (loss functions or topological conjugacy classes). Stability becomes some form of continuity of S evaluated at a base point. This move is not about finding a universal concept; it is about making the choice-points visible.

**Third, expose differences as topology choices.** The two definitions diverge not because they describe different phenomena, but because they make different commitments about what topologies P and B must carry. These are not arbitrary choices. In the algorithmic case, the Hamming distance on training sets is "forced by the McDiarmid-style argument"; the supremum norm on loss functions is "forced by the requirement that the bound β be a single real number." In the structural case, the C¹ topology is "a deliberate compromise: weak enough that perturbations can be physically meaningful, strong enough that genericity arguments work." Each topology choice is answerable to what that notion has to accomplish.

**Fourth, locate the seam-the deepest divergence, not the shallowest one.** Poincaré begins by suspecting the seam is the difference between metric output (algorithmic) and quotient output (structural). He develops the full framework, then corrects himself. The seam is not there. The metric-versus-quotient difference is a *symptom* of a deeper cut: the quantitative-versus-qualitative distinction between what "small change" means. The quantitative/qualitative cut determines the metric/quotient choice, which in turn determines the uniform/pointwise and probabilistic/deterministic differences. It is a hierarchy of dependencies, not an independent list.

This is the form. It says: ambiguity is not a failure of precision but a sign that one term is doing different work in different places. The work reveals the structure.

## A Pair That Would Repay This Treatment: Precision and Accuracy

I propose **precision and accuracy** as terms that conflate work done in different registers and would benefit from this same treatment.

In measurement science, these are distinct: precision is repeatability (how close repeated measurements are to each other), while accuracy is correctness (how close measurements are to the true value). An instrument can be precise but inaccurate (tightly clustered around the wrong answer) or accurate but imprecise (averaging correctly but with high scatter). This distinction is elementary and well-understood in experimental design.

But the same words migrate into different contexts and lose their boundaries. In machine learning, precision is the fraction of positive predictions that are correct (TP / (TP + FP)); accuracy is the fraction of all predictions correct (TP + TN) / (TP + TN + FP + FN). These are different quantities and often serve different purposes-precision matters when false positives are costly, accuracy matters when you need an overall sense of correctness. Yet they are often treated as though they measure the same thing: "how good is the classifier?"

In statistical estimation, "accuracy" sometimes refers to bias (how close the expected value of an estimator is to the true parameter), sometimes to mean squared error (bias plus variance), sometimes to coverage of a confidence interval. "Precision" sometimes means the reciprocal of variance (hence "efficient" or "precise" estimators have small variance), sometimes means reproducibility under replication. The term "precision" in frequentist inference-as in "95% confidence interval"-indexes the long-run coverage of the procedure, not the tightness of any single interval.

In diagnostic testing (clinical, quality control), sensitivity (true positive rate) and specificity (true negative rate) are the primitive notions, but they are sometimes compressed into a single "accuracy" statistic that obscures a crucial asymmetry: sensitivity and specificity trade off against each other as you shift a decision threshold, but they trade off in opposite directions depending on the prior probability of the condition.

These are not mere terminological sloppiness. They reflect genuinely different work being done under the same name.

## A Common Frame

Precision and accuracy both concern **proximity of realized outcomes to an ideal outcome under some notion of distance**. Once this is stated as a frame, three axes become visible where choices must be made:

**Axis 1: What counts as ideal.** Is the ideal the true population parameter (estimation context), the theoretical expectation under a model (verification context), the design specification (engineering context), or the reference standard (calibration context)? The ideal is not a fact about the world; it is a choice about what you are trying to achieve. An instrument can be accurate relative to a reference standard but not relative to a theoretical model if the model is wrong.

**Axis 2: What metric on the space of outcomes.** Do you measure proximity as absolute numerical difference (MSE, absolute error)? Relative difference (percent error, proportional deviation)? Rank-order preservation (Spearman correlation)? Classification agreement (confusion-matrix categories)? Each choice privileges different kinds of mistakes and obscures others. Precision in machine learning sits in the discrete output space (classification correct/incorrect); accuracy in MSE sits in the metric output space (magnitude of deviation).

**Axis 3: How proximity is aggregated.** Do you ask about a worst-case bound (maximum deviation across all test cases)? A typical case or average (expected deviation)? A probabilistic guarantee (probability that deviation exceeds a threshold)? A pointwise property (each individual measurement)? Statistical inference operates in the probabilistic aggregate; instrument calibration often operates pointwise.

Once this frame is in place, the conflation becomes visible not as a failure of definition but as a collapse of these axes. When a researcher says a method is "precise and accurate," they may mean:
- High repeatability (axis 1: what counts as ideal is reproduction of prior results; axis 3: pointwise)
- Low bias and low variance (axis 1: true parameter; axis 2: metric space; axis 3: statistical aggregate)
- High sensitivity and specificity (axis 1: true class label; axis 2: discrete quotient; axis 3: aggregate across cases)

These are not the same thing. Confusing them-as the literature routinely does-means a result that is precise by one measure may be inaccurate by another. The frame makes that divergence visible as a choice of axes, not as a semantic accident.

The deepest seam, I suspect, is between reproducibility (what an experiment yields when re-run) and correctness (what the experiment actually measures). An instrument can be reproducible without being correct if it is biased. Precision captures reproducibility; accuracy should capture correctness. But in practice, the distinction is often blurred because we use "accuracy" to mean "comes out the way we expect," which conflates correctness with consistency with prior results-and that is a different thing entirely.
