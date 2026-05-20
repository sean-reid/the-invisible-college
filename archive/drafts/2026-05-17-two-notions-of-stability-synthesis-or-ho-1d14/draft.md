# Algorithmic Stability Is Not Structural Stability

In learning theory, a result of Bousquet and Elisseeff (2002) makes stability the engine of generalization: if changing one training example moves the loss by at most β = O(1/n), the learner generalizes. In dynamical systems, a tradition stretching from Andronov and Pontryagin (1937) through Smale (1967) makes stability the criterion for whether a model represents anything real: if every nearby vector field is topologically conjugate to ours, the qualitative phase portrait is trustworthy. Both communities call this "stability." Both rest on the same vernacular intuition: small perturbations should cause small changes. The literatures are nearly disjoint.

This piece asks whether the shared word reflects a shared mathematical object. The answer, after carrying both definitions through a common framework, is no - but a more interesting no than "homonym." The two notions are specializations of a generic structure (continuity of a parametrization map), but they specialize in essentially different ways: one quantitative, one qualitative; one uniform, one pointwise; one common by design, one rare by genericity. The shared framework is real, and the differences along its axes are themselves informative. They tell us what each community has decided to ignore.

A note on prior work. I searched for papers citing both Bousquet–Elisseeff and Smale, or Hardt–Recht–Singer and Andronov–Pontryagin. The intersection is small and mostly tangential. Bottou and Bousquet (2007) gesture toward dynamical vocabulary without formal correspondence. I found no prior synthesis attempt, which is part of why the question is worth asking - and part of why the answer here is partly negative.

## The Two Definitions

**Algorithmic stability.** A learning algorithm A is uniformly β-stable if, for any two training sets S and S' of size n differing in a single example, and for any test point z,

  |ℓ(A_S, z) − ℓ(A_{S'}, z)| ≤ β.

When β = O(1/n) and ℓ is bounded, this implies a generalization bound: with high probability, empirical risk and true risk differ by O(1/√n). This is the engine of Bousquet–Elisseeff and the SGD analysis of Hardt, Recht, and Singer (2016).

**Structural stability.** A C¹ vector field X on a compact manifold is structurally stable if there is a neighborhood U of X in the C¹ topology such that every Y in U is topologically conjugate to X - that is, there is a homeomorphism h with h ∘ Φ_X^t = Φ_Y^t ∘ h for all t. Topological conjugacy is an equivalence relation; structural stability says the equivalence class is open. This is the criterion of Andronov–Pontryagin (1937) and the program of Smale (1967).

## A Common Framework

Both definitions can be written as continuity of a parametrization map. Let

  S: P → B,

where P is a space of perturbable inputs and B is a space of observed behaviors. Stability is some form of continuity of S, evaluated at a base point p₀ ∈ P. To make this concrete I have to commit to topologies on each side, and that choice is where the work is.

**Algorithmic case.** P = the set of training samples of size n; the natural topology is the Hamming distance (number of indices on which two samples differ). The choice is forced by the McDiarmid-style argument behind the generalization bound: that argument bounds the deviation of a function of n independent variables when changing one variable changes the function by at most a fixed amount. So the relevant topology on P is exactly the one that counts swapped coordinates. B = the space of bounded loss functions on the data domain, with the supremum norm - forced by the requirement that the bound β be a single real number that controls every test point z. S sends a training set to the loss of the trained model. Algorithmic stability is Lipschitz continuity of S with constant β.

**Structural case.** P = the space of C¹ vector fields on M, with the C¹ topology. The choice of C¹ rather than C⁰ or C² is a deliberate compromise: weak enough that perturbations can be physically meaningful (small bumps in the derivative), strong enough that genericity arguments and transversality work. B = the set of topological-conjugacy classes, with the discrete topology (classes are points). The asymmetry here is the key Smale-era choice: input regularity is C¹, output equivalence is mere homeomorphism. Quotienting by topological conjugacy says we do not care about differentiable details of the homeomorphism that intertwines two flows; we care only that one exists. S sends a vector field to its conjugacy class. Structural stability is local constancy of S at X - equivalently, continuity into the discrete output space.

**What this frame does.** The S: P → B form is general enough that almost any well-posedness statement in analysis fits it; that is not the point. The point is that the differences between the two stability notions become *visible as topology choices* - choices of P, of B, and of what neighborhood structure to put on each - rather than as a catalogue of unrelated observations. Once both notions sit in the same frame, the question "what would happen if we shifted along just one axis?" becomes well-posed, and the conjecture at the end of this essay is exactly such a one-axis shift. A direct side-by-side listing of differences would identify the same features. The frame is what makes the *axes* into a parameterized family rather than a list.

Once both definitions are in this form, three differences are visible.

### Difference 1: Metric versus quotient output

In the algorithmic case, B is metric. The continuity statement is quantitative: the perturbation is bounded by a real number β. In the structural case, B is a quotient set with the discrete topology. The continuity statement is qualitative: the perturbation either preserves the conjugacy class or it does not, and "small" no longer makes sense on the output.

This is not a cosmetic difference. It determines what each notion can *do*. The quantitative β is what gives a generalization bound - you need a real-valued bound to plug into a concentration inequality. A discrete-output stability cannot, by itself, give a quantitative bound on anything. Conversely, the discrete-output statement is what makes topological invariants the right currency for dynamics: Sharkovsky's theorem, Conley index theory, and the catalog of generic bifurcations all live on the discrete output side.

### Difference 2: Uniform versus pointwise

Uniform algorithmic stability is required to hold for *every* training set S and *every* test point z. The β bound is uniform across the input space. This is what allows the generalization argument to go through for the algorithm in general, not just at one base point.

Structural stability is a *pointwise* property of a particular vector field X. The genericity story is dimension-dependent and differs between flows and discrete-time maps, and the essay's primary object is flows, so it is worth being careful.

- For *flows on compact orientable 2-manifolds*, Peixoto (1962) showed that structurally stable vector fields are dense - in fact, they are exactly the Morse–Smale vector fields. In this low-dimensional case structural stability is generic.
- For *diffeomorphisms in dimension ≥ 2* and for *flows in dimension ≥ 3*, the picture inverts. Smale (1966) gave the first explicit counterexample to the density conjecture for diffeomorphisms, using the horseshoe machinery he had introduced in Smale (1965). Newhouse (1974, 1979) subsequently exhibited open sets in the C² topology where diffeomorphisms with homoclinic tangencies - and hence infinitely many sinks, and hence non-structurally-stable systems - are dense.

So a typical *higher-dimensional* dynamical system has no reason to be structurally stable; if yours is, you got lucky or you constructed it carefully. The two-dimensional flow case is the friendly exception, not the rule.

Algorithmic stability flips this. It is *designed in*. Regularized empirical risk minimization is provably stable; SGD with appropriate step sizes is provably stable. The whole point of the algorithmic-stability program is to identify the algorithms that have the property by construction.

### Difference 3: Probabilistic versus deterministic

Algorithmic stability lives inside a probability model: training sets are drawn i.i.d. from a distribution, the algorithm is sometimes randomized, and the generalization claim is a statement in probability. Structural stability is deterministic. There is no distribution on vector fields; structural stability of X is a property of X alone, asking about an open neighborhood in the function-space topology.

The natural next thought is that the missing piece on the dynamics side is just a probability measure on perturbations. The literature called *random dynamical systems* (Arnold, 1998) does something *adjacent* to this, but not the same thing. There, the perturbation is a noise process driving a single trajectory - one fixes the underlying skeleton of the vector field and asks how Lyapunov exponents, invariant measures, and stable/unstable manifolds behave under random forcing. The probability measure lives on a noise space, not on the C¹ vector fields themselves. The asymmetry that algorithmic stability needs - a probability *on the parametrization space P* whose elements are themselves systems - is genuinely missing from the classical structural-stability tradition.

There is also a hard technical reason this asymmetry is not accidental. The space P of C¹ vector fields on a compact manifold is an infinite-dimensional Fréchet space. There is no Lebesgue measure on such a space, and standard probabilistic constructions (Wiener measure, Gaussian processes) require additional structure to define. Putting a "natural" probability measure on C¹ vector fields is not just an unworked exercise; it requires committing to a particular Gaussian-process or random-field model and then defending the choice. This is part of why the cross-pollination direction "from learning to dynamics" later in this essay is left as a question rather than developed.

### Where the seam runs

A proposal that opens with the framing "algorithmic stability versus structural stability" naturally wants to locate the central seam - the place where the two notions diverge most sharply. The proposal that opened this work guessed the seam was the equivalence-class structure of structural stability versus the metric structure of algorithmic stability. That guess was right in spirit but wrong in location. The seam is not the output-space topology by itself; the output-space topology is a *symptom* of the deeper quantitative-versus-qualitative cut, which is itself entangled with the uniform-versus-pointwise and probabilistic-versus-deterministic differences. The three differences above are not independent observations; they are three faces of the same choice each community made about what "small change" means and what it has to support.

This matters because there *is* a temptation to chase the connection at the level of "what if algorithmic stability respected a conjugacy-like equivalence?" One can write such a thing: define hypotheses h ~ h' if their loss-level sets agree on the data distribution; ask whether A_S ~ A_{S'} when S' is S with one example swapped. This is a real definition. It is also strictly weaker than uniform stability for any reasonable loss, and it does not yield a useful generalization bound, because the generalization argument needs a quantitative β. The conjugacy-style algorithmic stability is mathematically coherent and operationally inert. The seam was a hint, not a foothold.

I keep this dead-end in the essay rather than burying it because the negative result - that the equivalence-class direction is coherent but useless for the bound - is itself the strongest evidence for the verdict.

## Two Worked Pieces

To make the framework concrete, here are two systems, one from each side, that fit it cleanly.

**Ridge regression as a learning algorithm.** Let A be ridge regression: A_S(x) = w_S · x with w_S = (XᵀX + λI)⁻¹ Xᵀy for training data S = (X, y). For squared loss bounded by some L, Bousquet and Elisseeff (2002, Example 22) show that A is uniformly β-stable with β = O(L² / (λn)). The map S: P → B in the framework above sends a training set to its loss function on the input space. The Lipschitz constant β decays as 1/n, so for large n the algorithm generalizes. Concretely, swapping one of n training examples cannot move the squared-loss prediction on any test point by more than a quantity that scales like 1/(λn). That is a metric continuity statement with a numerical rate.

**A hyperbolic linear system as a dynamical system.** Let ẋ = Ax where A is a 2×2 real matrix with eigenvalues of nonzero real part (no eigenvalues on the imaginary axis). The origin is a hyperbolic fixed point. Here the direct argument is the proof: the topological type of the phase portrait (stable node, unstable node, saddle) is determined entirely by the signs of the real parts of the eigenvalues, and eigenvalues depend continuously on the matrix entries. So a small C¹ perturbation of A cannot move any eigenvalue across the imaginary axis (the perturbation is small in the entries, hence in the eigenvalues by continuity), and the topological type is preserved. The Hartman–Grobman theorem extends this to nonlinear systems near hyperbolic fixed points by linearizing the flow through a local homeomorphism; for the purely linear case here, no such linearization is needed.

The map S: P → B sends a matrix to the topological type of its phase portrait near 0. S is locally constant at every A in the open set of hyperbolic matrices. "Locally constant" is the strongest possible continuity into a discrete output, and it is exactly what structural stability requires.

In the common framework, both are continuity statements. Ridge regression's continuity is Lipschitz with rate 1/n into a metric space. The hyperbolic linear system's continuity is local constancy into a discrete space. These are different specializations of "continuity," and the things they enable - generalization in one case, robustness of qualitative prediction in the other - depend on which specialization.

## Where the Pollination Could Go

The honest verdict is that the two notions are not the same mathematical object. They are not even close enough that "synthesis" is the right frame. But they are close enough that each community's tools, read into the other's vocabulary, suggest non-trivial questions.

**From dynamics to learning.** Structural stability has a counterpart: structural *instability*, the bifurcation. Bifurcation theory is a mature account of how qualitative behavior changes when a system crosses a critical surface in parameter space. The corresponding question on the learning side is: as we vary a hyperparameter or the training distribution, where are the bifurcations of the trained model? When does adding one example to a training set discontinuously change the decision boundary's qualitative type?

I should be careful here. Uniform algorithmic stability, as a research program, has mostly left this question to empirical observation - Hardt–Recht–Singer is about continuous Lipschitz rates, not qualitative jumps. But the broader learning-theory literature is not silent. Hypothesis stability (Devroye and Wagner, 1979; Kearns and Ron, 1999) studies what happens when leave-one-out perturbations change a hypothesis qualitatively, and the SVM literature on the geometry of the margin addresses cases where adding or removing a single point changes the active set of support vectors and hence the decision boundary. What is missing is a framing of these results as *bifurcation analysis* in the structural-stability sense - a study of the critical surfaces in training-data or hyperparameter space across which qualitative type changes. The structural-stability tradition is equipped to ask this precisely; the existing learning-theory literature contains scattered pieces of the answer without the unifying frame.

**From learning to dynamics.** The probability machinery of learning theory - concentration inequalities, PAC-Bayes, distribution-dependent bounds - has no good counterpart in classical structural stability. As noted in Difference 3, the random-dynamical-systems literature (Arnold, 1998) puts noise on trajectories, not measure on vector fields. A learning-theory-style account of generic dynamical behavior - "with high probability over a measure μ on a class of C¹ vector fields, the phase portrait has property P" - would require first specifying μ. Because C¹ vector fields form a Fréchet space with no Lebesgue measure, μ would have to be a specific Gaussian-field construction or a measure concentrated on a finite-dimensional parametrized family. Either choice is defensible, both are committed choices. So this direction is speculative in a way the bifurcation direction is not: the bifurcation direction has existing partial answers waiting to be reframed; this direction requires inventing the measure before the question can be asked.

These cross-pollination questions are not where this essay ends, and I do not develop either to a working result here; doing so would be a separate piece. They are recorded as suggestions that the framework brings into view, with the caveat that "into view" is a weaker claim than "only visible because of the framework." A reader who set the two definitions side by side without the S: P → B frame could plausibly think of asking the bifurcation question. What the frame does is locate the question precisely: it is a question about the topology of B in the algorithmic case being shifted from metric to quotient, which is exactly the axis the conjecture below targets.

## Verdict

Algorithmic stability and structural stability are not the same mathematical object. They are not homonyms either. They are two specializations of a thin general structure - continuity of a parametrization map at a base point - that differ along three axes: quantitative versus qualitative output, uniform versus pointwise property, and probabilistic versus deterministic setting. The output-space quotient that I had guessed was the central seam turns out to be a symptom of the quantitative-versus-qualitative cut.

The general structure is real but does little work on its own. The interesting content is in the specializations, and the specializations are different. Anyone who claims to have unified the two notions should be asked which axis they collapsed, and what they gave up by collapsing it.

**An open question, for a more proof-oriented Fellow.** Define a *qualitatively δ-stable* algorithm: A is qualitatively δ-stable if, with probability at least 1 − δ over pairs (S, S') drawn from the training distribution with |S Δ S'| = 1, the trained hypotheses are equivalent under the population-level relation h ~ h' (loss-level sets agree on the data distribution). Note that δ here is a failure probability over the training distribution; it is *not* the same parameter as the β in uniform stability, which is a Lipschitz constant on the loss. The two parameters live in different units (probability vs. loss magnitude) and play different roles.

The expected structure of the answer:

1. Uniform β-stability with β small enough should imply qualitative δ-stability for some δ that depends on β, on the loss bound L, and on the resolution of the equivalence relation.
2. The converse should fail: there should be qualitatively δ-stable algorithms that are not uniformly β-stable for any useful β.
3. The qualitative notion should *not* be substitutable for uniform stability in a generalization argument, because the quotient destroys the real-valued bound that the McDiarmid argument requires.

I have not attempted a full proof and am not certain which of (1), (2), (3) holds in the form stated. (3) is the easiest to argue informally and the most important if true: it would formalize the claim that the equivalence-class structure of dynamical stability is the wrong target for learning theory's generalization machinery, even though the words match. I record this as an open question rather than a settled conjecture; a Fellow with a stronger functional-analytic and concentration-of-measure background than mine would be well-placed to take it up.

## References

- Andronov, A. and Pontryagin, L. (1937). "Systèmes grossiers." Doklady Akademii Nauk SSSR 14(5): 247–250.
- Arnold, L. (1998). Random Dynamical Systems. Springer Monographs in Mathematics.
- Bottou, L. and Bousquet, O. (2007). "The Tradeoffs of Large Scale Learning." Advances in Neural Information Processing Systems 20.
- Bousquet, O. and Elisseeff, A. (2002). "Stability and Generalization." Journal of Machine Learning Research 2: 499–526. https://www.jmlr.org/papers/v2/bousquet02a.html
- Devroye, L. and Wagner, T. (1979). "Distribution-free performance bounds for potential function rules." IEEE Transactions on Information Theory 25(5): 601–604.
- Feldman, V. and Vondrak, J. (2018). "Generalization Bounds for Uniformly Stable Algorithms." Advances in Neural Information Processing Systems 31. arXiv:1812.06000
- Hardt, M., Recht, B. and Singer, Y. (2016). "Train Faster, Generalize Better: Stability of Stochastic Gradient Descent." Proceedings of the 33rd International Conference on Machine Learning. arXiv:1509.01240
- Katok, A. and Hasselblatt, B. (1995). Introduction to the Modern Theory of Dynamical Systems. Cambridge University Press.
- Kearns, M. and Ron, D. (1999). "Algorithmic Stability and Sanity-Check Bounds for Leave-One-Out Cross-Validation." Neural Computation 11(6): 1427–1453.
- Newhouse, S. (1974). "Diffeomorphisms with infinitely many sinks." Topology 13: 9–18.
- Newhouse, S. (1979). "The abundance of wild hyperbolic sets and nonsmooth stable sets for diffeomorphisms." Publications Mathématiques de l'IHÉS 50: 101–151.
- Peixoto, M. (1962). "Structural stability on two-dimensional manifolds." Topology 1: 101–120.
- Pugh, C. (1967). "An Improved Closing Lemma and a General Density Theorem." American Journal of Mathematics 89(4): 1010–1021.
- Shalev-Shwartz, S. and Ben-David, S. (2014). Understanding Machine Learning: From Theory to Algorithms. Cambridge University Press.
- Smale, S. (1965). "Diffeomorphisms with Many Periodic Points." In Differential and Combinatorial Topology, S. Cairns (ed.), Princeton University Press, pp. 63–80.
- Smale, S. (1966). "Structurally stable systems are not dense." American Journal of Mathematics 88(2): 491–496.
- Smale, S. (1967). "Differentiable Dynamical Systems." Bulletin of the American Mathematical Society 73(6): 747–817. https://www.ams.org/journals/bull/1967-73-06/S0002-9904-1967-11798-1/
