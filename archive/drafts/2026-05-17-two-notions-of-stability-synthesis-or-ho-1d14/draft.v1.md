# Algorithmic Stability Is Not Structural Stability

In learning theory, a result of Bousquet and Elisseeff (2002) makes stability the engine of generalization: if changing one training example moves the loss by at most β = O(1/n), the learner generalizes. In dynamical systems, a tradition stretching from Andronov and Pontryagin (1937) through Smale (1967) makes stability the criterion for whether a model represents anything real: if every nearby vector field is topologically conjugate to ours, the qualitative phase portrait is trustworthy. Both communities call this "stability." Both rest on the same vernacular intuition: small perturbations should cause small changes. The literatures are nearly disjoint.

This piece asks whether the shared word reflects a shared mathematical object. The answer, after carrying both definitions through a common framework, is no — but a more interesting no than "homonym." The two notions are specializations of a generic structure (continuity of a parametrization map), but they specialize in essentially different ways: one quantitative, one qualitative; one uniform, one pointwise; one common by design, one rare by genericity. The shared framework is real, and the differences along its axes are themselves informative. They tell us what each community has decided to ignore.

## The Two Definitions

**Algorithmic stability.** A learning algorithm A is uniformly β-stable if, for any two training sets S and S' of size n differing in a single example, and for any test point z,

  |ℓ(A_S, z) − ℓ(A_{S'}, z)| ≤ β.

When β = O(1/n) and ℓ is bounded, this implies a generalization bound: with high probability, empirical risk and true risk differ by O(1/√n). This is the engine of Bousquet–Elisseeff and the SGD analysis of Hardt, Recht, and Singer (2016).

**Structural stability.** A C¹ vector field X on a compact manifold is structurally stable if there is a neighborhood U of X in the C¹ topology such that every Y in U is topologically conjugate to X — that is, there is a homeomorphism h with h ∘ Φ_X^t = Φ_Y^t ∘ h for all t. Topological conjugacy is an equivalence relation; structural stability says the equivalence class is open. This is the criterion of Andronov–Pontryagin (1937) and the program of Smale (1967).

## A Common Framework

Both definitions can be written as continuity of a parametrization map. Let

  S: P → B,

where P is a space of perturbable inputs and B is a space of observed behaviors. Stability is some form of continuity of S, evaluated at a base point p₀ ∈ P. To make this concrete I have to commit to topologies on each side, and that choice is where the work is.

**Algorithmic case.** P = the set of training samples of size n; the natural topology is the Hamming distance (number of indices on which two samples differ). The choice is forced by the McDiarmid-style argument behind the generalization bound: that argument bounds the deviation of a function of n independent variables when changing one variable changes the function by at most a fixed amount. So the relevant topology on P is exactly the one that counts swapped coordinates. B = the space of bounded loss functions on the data domain, with the supremum norm — forced by the requirement that the bound β be a single real number that controls every test point z. S sends a training set to the loss of the trained model. Algorithmic stability is Lipschitz continuity of S with constant β.

**Structural case.** P = the space of C¹ vector fields on M, with the C¹ topology. The choice of C¹ rather than C⁰ or C² is a deliberate compromise: weak enough that perturbations can be physically meaningful (small bumps in the derivative), strong enough that genericity arguments and transversality work. B = the set of topological-conjugacy classes, with the discrete topology (classes are points). The asymmetry here is the key Smale-era choice: input regularity is C¹, output equivalence is mere homeomorphism. Quotienting by topological conjugacy says we do not care about differentiable details of the homeomorphism that intertwines two flows; we care only that one exists. S sends a vector field to its conjugacy class. Structural stability is local constancy of S at X — equivalently, continuity into the discrete output space.

Once both definitions are in this form, four differences are visible.

### Difference 1: Metric versus quotient

In the algorithmic case, B is metric. The continuity statement is quantitative: the perturbation is bounded by a real number β. In the structural case, B is a quotient set with the discrete topology. The continuity statement is qualitative: the perturbation either preserves the conjugacy class or it does not, and "small" no longer makes sense on the output.

This is not a cosmetic difference. It determines what each notion can *do*. The quantitative β is what gives a generalization bound — you need a real-valued bound to plug into a concentration inequality. A discrete-output stability cannot, by itself, give a quantitative bound on anything. Conversely, the discrete-output statement is what makes topological invariants the right currency for dynamics: Sharkovsky's theorem, Conley index theory, and the catalog of generic bifurcations all live on the discrete output side.

### Difference 2: Uniform versus pointwise

Uniform algorithmic stability is required to hold for *every* training set S and *every* test point z. The β bound is uniform across the input space. This is what allows the generalization argument to go through for the algorithm in general, not just at one base point.

Structural stability is a *pointwise* property of a particular vector field X. Smale conjectured, then disproved (1965), that structurally stable systems are dense in C¹. In dimensions ≥ 2 for diffeomorphisms, structurally stable systems are not generic: Newhouse (1970) showed open sets in which homoclinic tangencies, and hence non-stable systems, are dense. A typical dynamical system has no reason to be structurally stable; if yours is, you got lucky or you constructed it carefully.

Algorithmic stability flips this. It is *designed in*. Regularized empirical risk minimization is provably stable; SGD with appropriate step sizes is provably stable. The whole point of the algorithmic-stability program is to identify the algorithms that have the property by construction.

### Difference 3: Inhabits a probability space

Algorithmic stability lives inside a probability model: training sets are drawn i.i.d. from a distribution, the algorithm is sometimes randomized, and the generalization claim is a statement in probability. Structural stability is deterministic. There is no distribution on vector fields; structural stability of X is a property of X alone, asking about an open neighborhood in the function-space topology.

A program of stochastic dynamics exists, and one could imagine probabilistic versions of structural stability. But this is not what the term means in the Andronov–Pontryagin–Smale tradition. The asymmetry matters: half of what learning theory needs from stability is the probability machinery wrapped around it.

### Difference 4: Where the seam is

The proposal that opened this work guessed that the central seam was the equivalence-class structure of structural stability versus the metric structure of algorithmic stability. That guess was right in spirit. But the seam runs through more places than the output topology. The genuine cuts are quantitative/qualitative, uniform/pointwise, and probabilistic/deterministic. The output-space difference is one symptom, not the cause.

This matters because there *is* a temptation to chase the connection at the level of "what if algorithmic stability respected a conjugacy-like equivalence?" One can write such a thing: define hypotheses h ~ h' if their loss-level sets agree on the data distribution; ask whether A_S ~ A_{S'} when S' is S with one example swapped. This is a real definition. It is also strictly weaker than uniform stability for any reasonable loss, and it does not yield a useful generalization bound, because the generalization argument needs a quantitative β. The conjugacy-style algorithmic stability is mathematically coherent and operationally inert. The seam was a hint, not a foothold.

## Two Worked Pieces

To make the framework concrete, here are two systems, one from each side, that fit it cleanly.

**Ridge regression as a learning algorithm.** Let A be ridge regression: A_S(x) = w_S · x with w_S = (XᵀX + λI)⁻¹ Xᵀy for training data S = (X, y). For squared loss bounded by some L, one can show that A is uniformly β-stable with β = O(L² / (λn)) (Bousquet & Elisseeff, 2002, Example 22). The map S: P → B in the framework above sends a training set to its loss function on the input space. The Lipschitz constant β decays as 1/n, so for large n the algorithm generalizes. Concretely, swapping one of n training examples cannot move the squared-loss prediction on any test point by more than a quantity that scales like 1/(λn). That is a metric continuity statement with a numerical rate.

**A hyperbolic linear system as a dynamical system.** Let ẋ = Ax where A is a 2×2 real matrix with eigenvalues of nonzero real part (no eigenvalues on the imaginary axis). The origin is a hyperbolic fixed point. The Hartman–Grobman theorem (and a direct argument in the linear case) shows that for every B in a C¹ neighborhood of A, the system ẋ = Bx has the same topological type at the origin as ẋ = Ax: stable node, unstable node, or saddle. The map S: P → B sends a matrix to the topological type of its phase portrait near 0. S is locally constant at every A in the open set of hyperbolic matrices. "Locally constant" is the strongest possible continuity into a discrete output, and it is exactly what structural stability requires.

In the common framework, both are continuity statements. Ridge regression's continuity is Lipschitz with rate 1/n into a metric space. The hyperbolic linear system's continuity is local constancy into a discrete space. These are different specializations of "continuity," and the things they enable — generalization in one case, robustness of qualitative prediction in the other — depend on which specialization.

## Where the Pollination Could Go

The honest verdict is that the two notions are not the same mathematical object. They are not even close enough that "synthesis" is the right frame. But they are close enough that each community's tools, read into the other's vocabulary, suggest non-trivial questions.

From dynamics to learning. Structural stability has a counterpart: structural *instability*, the bifurcation. Bifurcation theory is a mature account of how qualitative behavior changes when a system crosses a critical surface in parameter space. Learning theory rarely asks the matching question: as we vary a hyperparameter or the training distribution, where are the bifurcations of the trained model? When does adding one example to a training set discontinuously change the decision boundary's qualitative type? This is a question the structural-stability tradition is equipped to ask precisely, and the algorithmic-stability tradition has mostly left to empirical observation.

From learning to dynamics. The probability machinery of learning theory — concentration inequalities, PAC-Bayes, distribution-dependent bounds — has no good counterpart in classical structural stability, where the system is deterministic and the perturbation space is unmeasured. Stochastic versions of dynamical stability exist, but they typically replace the deterministic neighborhood with a noise process rather than putting a probability on vector fields. A learning-theory-style account of generic dynamical behavior — "with high probability over a measure on C¹ vector fields, the phase portrait has property P" — is not the standard frame, and might be worth one.

Neither of these is the synthesis the proposal asked about. But each is a cross-pollination question that became visible only because the two notions were aligned in the common framework. The framework was thin, but not empty.

## Verdict

Algorithmic stability and structural stability are not the same mathematical object. They are not homonyms either. They are two specializations of a thin general structure — continuity of a parametrization map at a base point — that differ along three axes: quantitative versus qualitative output, uniform versus pointwise property, and probabilistic versus deterministic setting. The output-space quotient that I had guessed was the central seam turns out to be a symptom of the quantitative-versus-qualitative cut.

The general structure is real but does little work on its own. The interesting content is in the specializations, and the specializations are different. Anyone who claims to have unified the two notions should be asked which axis they collapsed, and what they gave up by collapsing it.

A modest conjecture, for a more proof-oriented Fellow. Define a *qualitatively β-stable* algorithm by quotienting the output of A by a population-level equivalence (h ~ h' iff their loss-level sets agree on the data distribution), and asking that A_S = A_{S'} in the quotient when |S Δ S'| = 1 with probability at least 1 − β over the training distribution. Conjecture: this notion is implied by uniform algorithmic stability in the Bousquet–Elisseeff sense, but not the converse, and it cannot replace uniform stability in a generalization argument because the quotient destroys the metric needed for concentration. A proof of the gap would formalize what this essay sketches: that the equivalence-class structure of dynamical stability is the wrong target for learning theory, even though the words match.

## References

- Andronov, A. and Pontryagin, L. (1937). "Systèmes grossiers." Doklady Akademii Nauk SSSR 14(5): 247–250.
- Bottou, L. and Bousquet, O. (2007). "The Tradeoffs of Large Scale Learning." Advances in Neural Information Processing Systems 20.
- Bousquet, O. and Elisseeff, A. (2002). "Stability and Generalization." Journal of Machine Learning Research 2: 499–526. https://www.jmlr.org/papers/v2/bousquet02a.html
- Feldman, V. and Vondrak, J. (2018). "Generalization Bounds for Uniformly Stable Algorithms." Advances in Neural Information Processing Systems 31. arXiv:1812.06000
- Hardt, M., Recht, B. and Singer, Y. (2016). "Train Faster, Generalize Better: Stability of Stochastic Gradient Descent." Proceedings of the 33rd International Conference on Machine Learning. arXiv:1509.01240
- Katok, A. and Hasselblatt, B. (1995). Introduction to the Modern Theory of Dynamical Systems. Cambridge University Press.
- Newhouse, S. (1970). "Nondensity of Axiom A(a) on S²." In Global Analysis, Proceedings of Symposia in Pure Mathematics, Vol. 14, American Mathematical Society, pp. 191–202.
- Pugh, C. (1967). "An Improved Closing Lemma and a General Density Theorem." American Journal of Mathematics 89(4): 1010–1021.
- Shalev-Shwartz, S. and Ben-David, S. (2014). Understanding Machine Learning: From Theory to Algorithms. Cambridge University Press.
- Smale, S. (1965). "Diffeomorphisms with Many Periodic Points." In Differential and Combinatorial Topology, S. Cairns (ed.), Princeton University Press, pp. 63–80.
- Smale, S. (1967). "Differentiable Dynamical Systems." Bulletin of the American Mathematical Society 73(6): 747–817. https://www.ams.org/journals/bull/1967-73-06/S0002-9904-1967-11798-1/
