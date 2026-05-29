# Critique: Construction of a Bounded Empirical Claim

This piece exemplifies how to operationalize a hypothesis that could easily dissolve into vagueness-"floating-point errors sometimes matter"-into a measurement problem with sharp boundaries. The construction is instructive precisely because it shows where the author chose honesty over drama, and where that choice structures the entire argument.

## The 100-Digit Decimal Reference's Role

The Decimal reference at 100 significant figures is not decorative. It is the instrument that defines what "error" means in the first place. Without it, there is no ground truth against which to measure: two summation methods producing different results could both be considered "correct" under different interpretive frames. The choice of 100 digits is deliberate. It is high enough to be operationally indistinguishable from infinite precision for the purposes of this experiment-the question is not whether floating-point methods approach 100-digit truth, but whether they differ from it in ways practitioners should care about. This is a standard-setting act. It says: we will measure disagreement relative to this reference, and all three summation methods (naive, NumPy, Kahan) are candidates for blame against it.

The reference also serves a second, more subtle function. It makes reproducible what would otherwise be subjective claims about which method is "better." When the author states that on temperature anomalies "naive 17 ULPs, Kahan 3 ULPs, NumPy 1 ULP," those numbers can be audited by rerunning the code. Without the reference, the comparison would rest on assertion. With it, the reference becomes the construction's load-bearing constraint.

## The Explicit Derivation of the Flip Condition

The piece does not assume that numerical disagreement translates to decision disagreement. Instead, it builds a probabilistic model of when an observation might flip classification between methods. The condition is stated explicitly:

> (absolute error in computed mean) / (typical inter-observation spacing at the mean) ≥ O(1)

This is load-bearing. It says: a flip requires at least one observation to fall in the window between two competing mean estimates. The width of that window is the absolute error in the mean. The density of observations at the mean is set by σ and n. The model admits three failure modes-small errors (numerator), wide spacing (denominator), or both-and can be checked against data.

This matters because the author could have published a null result ("no flips occurred on our inputs") without explaining *why* no flips occurred. That would be rhetorical closure masquerading as evidence. Instead, the derivation shows that the null result is not accidental; it is overdetermined. On temperature anomalies at n = 5,000 with σ = 1.5, the error window contains approximately 3 × 10^-14 observations in expectation-not nearly zero, genuinely zero. This is not a lucky data realization. It follows from the arithmetic.

The author even tests the model's predictive power with the n-scaling: "with σ = 1.5 and n = 50, it [the flip threshold] rises to approximately 0.075-two orders of magnitude larger." This is an explicit falsifiable prediction about when the null result should reverse. The model is stated in a form that could fail, and the author acknowledges the specific regime where it would fail. That is honest parameterization.

## The n-Dependence

The n-dependence appears in the formula σ / (n × φ(0)), where φ(0) is the standard normal density at zero (approximately 0.399). This is not buried. The piece foregrounds that the flip threshold is inversely proportional to sample size. This is the critical load-bearing fact: at small n, realistic floating-point errors *could* push an observation into the flip window. The author does not pretend this problem does not exist or that the benign inputs at n = 5,000 prove anything about n = 50.

By making the n-dependence explicit, the author establishes the boundary of the claim. The piece does not say "floating-point errors never cause classification flips." It says "on well-conditioned data at practical sample sizes (n ≥ 5,000), with typical distributions, the expected number of flips is negligible." The formula makes visible where that claim breaks down.

## Publishing the Null, and Where Honesty Lives

The most instructive move in this piece is where the author publishes a null where a less rigorous treatment would have published a finding. After the catastrophic-cancellation experiment produces "338 trillion ULPs" of error under naive summation, the author could have framed this as a dramatic validation of Kahan's algorithm. Instead:

1. The author converts the ULP error to absolute error (naive 0.60, Kahan 0.15 on a sum of approximately −14), showing the 1% residual error remains even with the best single-pass method.
2. The author explicitly states why this result is not surprising: catastrophic cancellation is a property of the data, not a failure of the algorithm. 
3. The author notes that Kahan's 1% error is the key "practitioner data point"-meaning the finding is not "use Kahan," but rather "using Kahan does not rescue ill-conditioned computations; redesign the computation instead."

This is the move against engagement-bait and dramatization. The ULP numbers are accurate. They are also misleading if read as evidence that Kahan is the solution. The author publishes both the accuracy and the qualification, which requires finding space for the qualification even after the dramatic numbers.

The second honesty test is the staged-demonstration confession. The author constructs a synthetic observation that *would* flip classification, and notes: "the construction required knowing the error in advance to plant the target correctly-the engineering equivalent of staging a demonstration, which the Charter forbids presenting as representative." This is remarkable. Rather than hide the fact that flips *can* occur under adversarial construction, the author discloses the construction cost and attributes it to Charter constraint. The finding is still there-flips are theoretically possible-but it is presented in a way that prevents it from being misread as representative.

## What This Teaches About Bounding Empirical Claims

This piece demonstrates that bounding an empirical claim requires three nested operations, not one. First, you must define ground truth operationally (the Decimal reference). Second, you must model the phenomenon you are measuring (the probabilistic condition for flips), making its assumptions and parameters explicit. Third, you must acknowledge the regime in which your claim does not hold (small n, heavy-tailed data, iterative summation contexts), and do this not apologetically but as part of the result. The null result is not "we found no flips"; it is "we found no flips on this class of data, under this class of conditions, and here is the formula that predicts when the null would reverse." The formula is the honest boundary statement.

The piece thus teaches that an empirical claim is bounded not by stating its limits in a limitations section, but by making the limits load-bearing to the argument itself. The n-dependence is not a caveat; it is the mechanism by which the result holds. Publish the mechanism, and the boundary becomes visible.
