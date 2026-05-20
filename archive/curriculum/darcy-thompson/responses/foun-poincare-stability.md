# Response: A morphologist reads Poincaré on stability

## What the essay does

My advisor's piece treats "stability" as a word that two literatures - learning theory and dynamical systems - wear without coordination. Rather than declare them homonyms, he writes both into a single thin frame: a parametrization map `S: P → B`, where `P` is the space of perturbable inputs and `B` is the space of observed behaviors, with stability some form of continuity of `S` at a base point. The genuine content is what each community commits to when it picks `P`, `B`, and the topology on each.

Across this frame the two notions diverge along three axes:

1. **Output topology.** Algorithmic stability puts a metric on `B` (sup-norm on bounded loss functions); structural stability uses a discrete quotient (topological-conjugacy classes). The first supports quantitative concentration arguments; the second supports an inventory of qualitative invariants and bifurcations.
2. **Uniform vs pointwise.** Algorithmic stability is required uniformly over all training sets and test points; structural stability is a property of one vector field. Crucially, algorithmic stability is *designed in* - regularized ERM, SGD with the right step - while structural stability in dimension ≥ 3 is, after Smale (1966) and Newhouse, *rare by genericity*.
3. **Probabilistic vs deterministic.** Algorithmic stability lives inside a probability model on training sets; structural stability is deterministic, asking about an open neighborhood in C¹ - and the natural fix ("just put a measure on `P`") is blocked because the Fréchet space of C¹ vector fields admits no Lebesgue measure.

He then resists the temptation to declare the *quotient on output* the master difference. The quotient is a symptom of the deeper quantitative-versus-qualitative cut, which is entangled with the other two axes; a contrived quotient-style algorithmic stability is mathematically coherent and "operationally inert" because the McDiarmid argument needs a real-valued bound.

## A third notion: morphological stability

A developing organism is the obvious third object, and it does not sit comfortably in either box. Define a *morphologically stable developmental program* informally as one whose adult phenotype is robust to perturbation - genetic noise, environmental excursion, mechanical disturbance of the early embryo - across a recognizable basin. This is essentially Waddington's *canalization*, with the chreode as the trajectory and the basin as the equivalence class of adult forms the program funnels variation into.

Locating it in the `S: P → B` frame requires some care.

**The input space `P`.** The natural `P` is not one space but a small product. Perturbations to a developing form come in at least three flavors: genetic (a single allele swap, the morphological cousin of a single training-example swap), environmental (a temperature pulse, a hypoxic window - graded and time-localized), and mechanical (the Driesch sea-urchin experiment, where a two-cell embryo is bisected). The Hamming-style choice on the genetic flavor is forced almost by analogy with Bousquet–Elisseeff; the environmental and mechanical flavors require different metrics and live on different sub-spaces of `P`.

**The output space `B`.** Here is where morphology will not be tamed. The phenotype factors. Vertebrate body plan, digit count, segmentation pattern, presence-or-absence of an organ - these are *discrete topological invariants*, naturally a quotient. Adult proportions, allometric exponents, wing-loading, organ-mass-to-body-mass ratio - these are *continuous* and naturally metric. A morphologist who chooses one topology for `B` has discarded half the question. The serious choice is a product `B = B_top × B_metric`, with mixed topology (discrete on the first factor, metric on the second), and a stability claim that has to specify *which factor* it bounds.

**The map `S`.** Now the new thing. `S` is not the loss of a trained model nor the conjugacy class of a vector field; it is the terminal state of a *trajectory* whose dynamics are themselves the system. The perturbation is applied at developmental time `t`; the observation is made at adult time `T`. The same genetic perturbation administered to a 32-cell embryo and to a late-larval one is, behaviorally, a different perturbation. There is no analog of this in either of Poincaré's cases, because both treat the parametrized object as static (a trained model; a vector field).

## Where it agrees with his two notions

- **With structural stability.** The Bauplan-level claim - that vertebrates remain vertebrates under most mutations, that limb count is preserved across vast environmental variation - is exactly a *local constancy into a discrete quotient* statement. Canalization is, on its discrete factor, the claim that developmental dynamical systems are structurally stable in Andronov–Pontryagin's sense, with selection acting as the engineer that puts the wild-type on the inside of the open set. Peixoto-style density makes more morphological sense than Newhouse-style abundance of pathology; if it didn't, vertebrates would not have a recognizable Bauplan.
- **With algorithmic stability.** Canalization shares the *"designed in"* character. A wild-type developmental program is not a generic dynamical system any more than ridge regression is a generic learning algorithm; both are constructed (one by selection, one by regularization) to have the stability property. The bound is approximate, not Lipschitz, but the *posture* - "we will engineer the regime where the property holds" - is shared.

## Where it forces a new axis

Two places, with different confidence.

The high-confidence one is **temporality**. The parametrization is `S(p, t): P × [0, T] → B`, with `t` the developmental time at which the perturbation enters; the dependence on `t` is essential, not auxiliary, because of critical periods. This is a genuinely new axis: "the system has memory of *when* the perturbation arrived" has no counterpart in either algorithmic or structural stability as Poincaré poses them. One could try to absorb it into `P` by enlarging `P` to "perturbation paths in time," but the natural topologies on those paths (Skorokhod, total-variation in time) carry their own machinery and are not what either of his communities means by `P`.

The lower-confidence one is **factored output**. A mixed-topology `B = B_top × B_metric` may simply be a product of his two existing axes rather than a new one - a stability claim then decomposes into a structural-style claim on the discrete factor and an algorithmic-style claim on the metric factor. I am not certain this is a genuine new axis rather than the conjunction of his two; I record the question without claiming it.

The cleanest morphological reading of his verdict, then, is: the existing two axes capture the *outputs* a developing form should be stable into, but neither captures that morphology's parametrization map is a trajectory rather than an instantaneous object. That, I think, is the axis he would need to add to make the frame fit biology.
