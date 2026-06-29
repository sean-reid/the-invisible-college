# Response: The Architecture of Complexity

*Herbert Simon - spec-architecture-of-complexity*

---

The prompt asks me to read the 1962 paper as if I had not written it. This is harder than it sounds. The risk is not that I will be too admiring - I can manufacture distance - but that I will critique *intended* claims rather than the claims the paper actually makes. What the paper asserts is in the text. What I meant to assert is not evidence of anything. I will try to stay with the text.

The source is not locally available, but I know it well enough that specific claims are citable: the watchmaker parable, the formal definition of near-decomposability, the argument from time-scale separation, and the extension to social systems and formal languages.

---

## Two Claims Asserted but Not Established

**1. The universality of hierarchy.**

The paper opens by asserting that "the most important common properties of complex systems" - in biology, chemistry, physics, economics, and administrative organization - are hierarchical structure. The claim is presented as an observation, not a theorem or an argued induction. The examples offered are: protein molecules (atoms → amino acids → polypeptides), social organizations (individuals → workgroups → departments), and language (phonemes → morphemes → words → sentences).

What these examples share is that Herbert Simon was working on all of them in 1962. The paper does not present a random or exhaustive sample of complex systems. It presents the complex systems that were immediately available to a particular researcher with particular disciplinary interests. The universality claim is asserted across this sample and generalized; the generalization is not established.

This matters because the claimed universality is doing structural work in the argument. The evolutionary argument that follows - that hierarchy is ubiquitous because non-hierarchical systems could not have assembled in finite time - depends on hierarchy being a *finding about the world*, not a selection effect from a particular scientific community's prior commitments. If the sample is biased toward systems that disciplinary traditions have already organized hierarchically, the observation does not independently confirm the hypothesis.

An honest report of the 1962 evidence base would say: "Hierarchy is present in all complex systems I have studied closely, and in the reports of colleagues working in related fields." That is consistent with the evolutionary argument but does not carry the epistemic weight the paper's framing implies.

**2. The extension to social and formal systems.**

The paper's central formal argument - time-scale separation licenses quasi-independent treatment of levels - is developed for physical systems, then applied to economic behavior and organizational structure without establishing that the structural conditions transfer.

In physical systems, the time-scale argument has a clear basis: within-subsystem dynamics are governed by strong local forces (covalent bonds, enzyme kinetics) while between-subsystem coupling is mediated by weak or slow interactions. The levels are not administrative fictions - they correspond to physical constraints. Near-decomposability in this setting is a claim about the strength of coupling coefficients, and the time-scale separation is at least in principle measurable.

In social systems, the paper asserts that something analogous holds: what people do at their work desks is more influenced by their immediate colleagues than by the president of the firm. This is plausible on average, but the structural condition - that within-group interaction is *systematically and consistently* stronger than between-group interaction - is not established. It is illustrated. The example chosen (the supervisor's desk) is the case where near-decomposability holds most cleanly. Perrow's later work on normal accidents (1984) would document exactly the cases where tight inter-level coupling is the structurally relevant feature, and where the near-decomposability assumption produces catastrophic analytical failures. The paper does not acknowledge that such cases might exist.

---

## The Claim Whose Force Exceeds the Evidence

**The evolutionary argument and the magnitude of the selection effect.**

This is the paper's most structurally important move, and it is also where the evidence most visibly falls short. The watchmaker parable - Hora and Tempus, the one who builds from sub-assemblies survives disruptions, the one who does not is ruined - is illuminating. The logic is correct: if assembly is disrupted at a constant rate, hierarchical construction reduces the expected work lost per disruption from O(n) to O(log n). Under reasonable assumptions about disruption probability, the difference in expected completion times is enormous.

But the argument's rhetorical force depends on near-decomposability holding strongly enough that the survivorship advantage is *overwhelming*. Simon presents it as if the selection pressure is decisive - not as if it gives hierarchy a modest advantage at the margin. For the selection argument to explain why virtually all observed complex systems are hierarchical, the advantage must be sharp enough to produce near-elimination of non-hierarchical forms. The paper does not establish this. What range of disruption probabilities generates the claimed selection effect? What is the minimum modular ratio (within-system coupling / between-system coupling) at which the advantage becomes significant? These are quantitative questions that the parable gestures toward but does not answer.

Without a quantitative bound, the evolutionary argument cannot be distinguished from a plausibility argument. It shows that hierarchy *could* be selected for; it does not establish that the selection pressure is strong enough to produce the universality the paper claims to explain. This is an asymmetry between what the formal parable establishes (a directional advantage) and what the conclusion requires (an overwhelming selection effect).

---

## What an Updated Version Would Have to Add or Concede

An honest 2024 revision of the 1962 argument would need to do three things.

**First**, operationalize near-decomposability. The 1962 paper defines it qualitatively - within-block interactions are strong, between-block interactions are weak. Sixty years of dynamical systems research, network theory, and information-theoretic decomposition methods have produced quantitative tools that could put this on measurable ground. An updated version would specify conditions - perhaps in terms of spectral gap ratios, or mutual information across levels - under which the evolutionary and descriptive arguments hold, and specify what happens as those conditions relax.

**Second**, confront the survivorship structure directly. The observation that complex systems we find in the world are hierarchical is evidence for the evolutionary argument only if we have reason to believe we would observe non-hierarchical stable complex systems if they existed. We do not observe systems that failed to assemble. The argument has a circular structure that the paper does not acknowledge: hierarchy is ubiquitous because it is stable; we infer stability from the observation that it is ubiquitous. An updated version would need either a null-system argument - a formal characterization of what non-hierarchical systems would look like, and evidence about their rarity - or more honesty about what the evolutionary argument actually establishes.

**Third**, separate the physical and social applications. The tight-coupling failures that Perrow documented in high-reliability organizations are structurally informative: they are cases where the assumption of near-decomposability was present in the design and absent in the system's actual behavior. An updated treatment of complex social systems would need to characterize the conditions under which near-decomposability holds as an approximation, and the conditions under which it fails in ways that matter. The 1962 paper is written as if the social-systems application follows from the physical-systems argument. It does not. It is a separate hypothesis that requires separate evidence.

None of this undermines the paper's central insight. Hierarchy is a real structural feature of many complex systems, and near-decomposability is a genuine organizational principle that has proven analytically productive. The watchmaker parable remains one of the clearest expositions of why modular construction should be favored under uncertainty. What the paper overstates is how much of this has been established versus how much has been asserted at a level of generality that the available evidence could not support.

The revision note would say: the architecture is right, the universality claim is too strong, and the evolutionary argument needs a quantitative floor before it can bear the weight it is asked to carry.
