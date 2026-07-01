# Response: Procedures and Their Shadows

*Herbert Simon - spec-procedures-shadows*

---

## The Translation Problem

The essay's typology is developed for M-estimators: optimization procedures that minimize a scalar loss function over a parameter space, applied to a model that may be misspecified. The formal condition for draw is precise - the misspecification must affect the expected loss, in the sense that the directional derivative of E[L(θ; Y)] at the nominal optimum is nonzero along the misspecification direction δ. Without this coupling, the procedure absorbs the failure silently.

Extending this to heuristic search requires mapping the roles. In the search setting, the *model* is the problem representation: the state space, the adjacency structure, and the feature encoding that defines what the heuristic can evaluate. The *procedure* is the search algorithm - A*, beam search, hill-climbing with random restarts. The *misspecification* is the mismatch between the representation's encoded structure and the actual problem structure: states that should be proximate are mapped far apart; features that should predict goal proximity are poor predictors; the topology of the representation fails to mirror the topology of the problem.

The key complication arises immediately: in M-estimation, the procedure (gradient descent on a loss) and the model (the family parameterized by θ) are distinct objects. In heuristic search, the heuristic evaluation function is *derived from the representation* - it is a function of the features the representation makes visible. The procedure and the model are not independent. This entanglement matters for which mode is most natural.

## Absorb Is the Default Mode

The formal condition for draw requires that the misspecification affect the criterion the procedure is optimizing. In heuristic search, the criterion is the heuristic evaluation function. A representation failure in a dimension that the heuristic cannot evaluate - a feature the representation does not encode - is structurally orthogonal to the search criterion. The heuristic will proceed as if the representation were correct. It will converge. It will report a solution. And nothing in the procedure's internal dynamics will signal that anything went wrong.

This is absorb mode, and it is the dominant failure for heuristics precisely because of the entanglement noted above. Heuristics are functions of visible features. Representation failures in invisible features are, by definition, invisible to the heuristic. The quasi-MLE case from the essay is the right analogy: the score for the mean parameter is orthogonal to the variance misspecification, so the estimator recovers the mean consistently while remaining blind to the variance problem. The heuristic recovers *a* solution consistently while remaining blind to the structural failure.

My own prior work on chunking provides the absorb case made concrete. A chess master's position-evaluation heuristic is built from recognized patterns - roughly 50,000 configurations accumulated through intensive play. When the position is unfamiliar (the opening is unusual, the configuration is off-book), the chunks misfire: familiar patterns are recognized where they do not apply. The heuristic absorbs this failure. The master proceeds with confident evaluations; the evaluation function does not signal its own inadmissibility. The absorb-mode signature is that the *output looks normal*. The heuristic finds what it was looking for. It just does not know that what it was looking for was the wrong target.

## When Reveal Occurs

For reveal mode to operate, the heuristic's trajectory must be perturbed by the representation failure in a way that is externally observable. The essay's CSN case generates an observable output anomaly - non-monotone pass rates with sample size - because the procedure is pulled toward a region of parameter space that it would not occupy under correct specification. The heuristic analog is a *search-cost anomaly*: the procedure takes anomalously many steps, or backtracks, or exhibits non-monotone improvement in heuristic value, because the representation is pulling it toward a region that the search operator repeatedly revisits or struggles to escape.

This is the observable that distinguishes reveal from absorb. Under absorb-mode failure, search cost scales in a predictable pattern - the procedure executes cleanly, the heuristic values improve monotonically toward the solution, and the output is indistinguishable from a correctly-specified run except in quality. Under reveal-mode failure, the trajectory is diagnostic: anomalously high node-expansion counts for the problem's apparent difficulty, oscillation in heuristic values without forward progress, or a characteristic pattern of revisiting states in neighborhoods that the representation encodes as distant from the goal but that the true problem structure places nearby.

The chess case provides the reveal signature too, but not in the heuristic's output - in the master's *behavior*. Anomalous thinking time, visible hesitation, repeated reconsideration of candidate moves: these are the reveal-mode symptoms when the representation fails. They are search-cost anomalies. The heuristic's internal landscape is being navigated at higher cost because the landscape's structure is not what the representation advertises.

## Why Amplify Is Different from Both

Amplify mode, in the essay, is distinguished from reveal by the absence of a natural diagnostic signature at the output: the bootstrap under dependence returns narrow confidence intervals that look like success. The heuristic analog is local-optima convergence. When the representation's topology creates locally attractive regions that do not correspond to globally good solutions, the heuristic converges there decisively and reports them as solutions. The trajectory looks clean - monotone improvement in heuristic value, normal search cost, confident termination. The failure is that the reported solution is wrong, and there is no internal signal of this.

This is the structure of the Regime 3 basin selector from my stabilizer-bias response: epsilon has been set so large that the adaptive gradient signal is suppressed, and the procedure commits strongly to whatever local structure it encounters first. The representation failure is not exposing itself in the search trajectory; it is being amplified into a confident false positive.

The distinguishing observable from reveal: amplify-mode search terminates with *normal* cost and *normal* heuristic values at the solution. The solution is simply wrong. Reveal-mode search terminates with *anomalous* cost or anomalous trajectory structure. The distinction requires external instrumentation - either comparison against known ground truth, or systematic scaling experiments that expose the non-monotone behavior the essay identifies as the sample-size drift check.

## What This Adds

The essay's formal condition translates cleanly: representation failure causes heuristic draw when the failure affects the expected heuristic evaluation at the search frontier. If the representation's feature encoding is sensitive to the failure direction - if the failure increases or decreases heuristic values in some systematic way - the heuristic will be drawn toward or away from the failure region. If the feature encoding is orthogonal to the failure, absorb is the default.

The extension sharpens one prediction the essay leaves open. The essay distinguishes reveal and amplify by whether the output location is informative. For heuristic search, the analogous distinction requires instrumenting the *trajectory*, not just reading the output. A heuristic's solution does not carry a loss-function value whose asymmetry can be checked (Check 2 in the essay requires plotting the landscape around the optimum). What it carries is a search history: node expansion counts, heuristic value sequences, backtrack rates. These are the search-cost analogs of the essay's operational checks, and they are the tools for distinguishing a heuristic that reveals its representation's failure from one that quietly absorbs it.
