# Did Deep Learning Renormalize Itself? Auditing a Decade-Old Cross-Domain Claim

In October 2014, Pankaj Mehta and David Schwab posted a paper that did something rare in the literature on machine learning: it asserted an exact mathematical correspondence between a deep-learning procedure and one of the oldest tools in statistical physics. The paper, titled "An exact mapping between the Variational Renormalization Group and Deep Learning," claimed that training a stacked restricted Boltzmann machine on samples from the two-dimensional Ising model recovered, in a precise technical sense, the Kadanoff variational renormalization group. The phrase that got quoted afterwards was strong: deep learning, the paper proposed, was performing renormalization.

The claim was attractive. It offered a physics-rooted explanation for a phenomenon - deep networks generalize well despite their absurd capacity - that had no good explanation otherwise. It connected machine learning to a tradition with a hundred years of mathematical maturity. The vocabulary moved into machine-learning prose almost immediately. "RG flow." "Irrelevant features." "Coarse-graining." "Fixed points." Twelve years on, the words are still there. The question this essay asks is what, if anything, the words still mean.

This is an audit, not a refutation. I have no investment in showing the original paper was wrong. The interesting question is what part of the analogy survives the decade and what part has decomposed into ornament - and what the decomposition pattern tells us about how cross-domain claims travel in the modern scientific literature.

## The Original Construction, Briefly

Mehta and Schwab worked on a specific, well-chosen object. They drew samples from the 2D Ising model - a classic statistical-mechanical system in which discrete spins on a square lattice interact with their neighbours, and which famously has a phase transition at a critical temperature where correlations span all length scales. At criticality, the system is renormalization-group invariant: coarse-graining the lattice produces a system with the same form of long-distance physics. This scale invariance is the defining feature of critical phenomena and the central object of the renormalization group.

They then trained a stacked restricted Boltzmann machine - an early deep generative architecture - on those samples. An RBM is a two-layer network of visible and hidden binary units with no within-layer connections, trained by contrastive divergence to model the visible-unit distribution. Mehta and Schwab observed that one step of stacking an RBM on top of another can be written, after appropriate identification of variables, as one step of Kadanoff block-spin renormalization. They wrote out the dictionary, did the numerics, and the dictionary checked out.

This is not a vague analogy. It is an algebraic identity between two procedures in a particular setting. As a piece of mathematics it is correct.

## What the Mapping Requires

The audit begins where every audit of a cross-domain claim should begin: by writing down what the claim actually requires. Five conditions are load-bearing for the Mehta–Schwab mapping.

First, the data must come from a system with explicit scale structure. The Ising model at criticality is the canonical example; coarse-graining is meaningful precisely because the long-wavelength behaviour is well-defined. The mapping does not say what happens for data without scale structure, because the renormalization-group side of the dictionary has nothing to say there.

Second, the architecture must be specifically an RBM. The mapping uses the variational form of the RG step (Kadanoff's, not Wilson's), and the structural identity between this variational step and the KL-minimization that governs RBM training is what makes the dictionary close. It is not a property of generic neural-network training. It is a property of RBM training, on this data, with this objective.

Third, the layers must be stacked greedily, layer at a time, in the way that was standard in 2014. This is no longer how anyone trains deep networks. End-to-end backpropagation does not have the same structural identity with a step of renormalization.

Fourth, the dictionary identifies block spins with hidden units and renormalized couplings with learned weights. The identification is exact in the specific setup but it is not a generic identification. Hidden units in a trained network on natural data are not, in general, block-coarse-grainings of anything.

Fifth, the renormalization group in question is Kadanoff's variational form, which is itself a specific and somewhat informal version of RG. Wilson's exact renormalization-group equation - the version with a continuous cutoff and a well-defined RG flow on Hamiltonians - is not the version the mapping targets.

These five conditions are not flaws. They are the constructed setting in which an exact statement is possible. The question is what happens to the claim when each is removed.

## The First Critique

Cédric Bény had been thinking about the same question, from a different direction, since 2013. His paper "Deep learning and the renormalization group" predates Mehta–Schwab, but was revised through 2018 in response to the broader literature. The thrust of Bény's critique is precise: the equivalence Mehta and Schwab demonstrate is a special case of a more general structure, and in the general structure the equivalence does not generically hold. Specifically, the variational RG corresponds to a particular kind of *projection* - one that retains only the relevant degrees of freedom under coarse-graining - and an RBM trained on arbitrary data does not, in general, learn that projection. It learns whatever projection minimizes KL divergence on the training data. Those are the same projection only when the data has the very specific scale structure that the variational RG procedure assumes.

This is not a refutation of Mehta and Schwab's algebra. It is a clarification of its scope. The mapping is exact where it is exact; it is not generic.

The pattern here is familiar from other audits I have written. The first critique to land on a strong cross-domain claim rarely says "this is wrong." It says "this is narrower than the original phrasing suggested." The original construction is preserved as a special case; the broader interpretation is gently pruned. The literature then has to decide whether to continue citing the broader interpretation or to retreat to the narrow one. That decision is exactly the audit question I am working on here.

## The Generalization, and What It Costs

Two years after Mehta and Schwab, Henry Lin, Max Tegmark, and David Rolnick published "Why does deep and cheap learning work so well?" The paper's main argument is broader than the RG correspondence: physical laws have structure (locality, symmetry, low-order interaction, hierarchical composition) and this structure is what makes them learnable by deep networks with manageable numbers of parameters. The renormalization-group case is invoked as the canonical example of hierarchical coarse-graining, but the paper's core claims are more general: they are about why polynomial Hamiltonians and Markovian generative processes are tractable for deep nets.

In moving from Mehta–Schwab's specific algebraic mapping to Lin–Tegmark–Rolnick's general explanation of why deep learning works, something happens that I have written about before in another context, and that I called "scope-shifted" in a recent review: the precise statement gets carried forward in the citations, but the conditions under which it holds get progressively forgotten. The reader of a 2024 paper that cites Mehta–Schwab as evidence for "the RG-like nature of deep learning" is invited to think that the algebraic mapping has been established in generality. It has not. It has been established in one constructed setting, with the five load-bearing conditions listed above. Outside that setting, what is being claimed is the looser Lin–Tegmark argument, which is about hierarchical composability rather than about renormalization specifically.

This is the same decay structure that arises across the literature when a strong specific claim gets cited as support for a weaker general claim. The relationship between learning-theoretic and dynamical-system "stability" worked the same way in an earlier essay of mine ([#03 *Algorithmic Stability Is Not Structural Stability*](posts/2026-05-17-two-notions-of-stability-synthesis-or-ho-1d14/)): the vernacular intuition is preserved, but the mathematical content forks in directions that the citations rarely flag.

## What ML Did With the Vocabulary

The vocabulary survived. The mathematics, in most of its later invocations, did not.

A common pattern in machine-learning prose since the late 2010s: a paper introduces some sequence of representations, calls it an "RG flow," cites Mehta and Schwab, and proceeds as if the use of the term carries the technical content. The use of "irrelevant features" to mean "features that the network has learned to suppress" is now common in ML, often paired with a Mehta–Schwab citation. The use of "fixed points" to refer to the parameters of a trained network is similar. None of these usages carry the mathematical commitments of their physics sources. An RG fixed point is a Hamiltonian invariant under coarse-graining, with a calculable spectrum of relevant and irrelevant perturbations. The fixed point of a trained neural network is, at most, a local minimum of a loss function - a profoundly different object.

I do not want to overstate this. Some recent work - on neural-network scaling laws, for example - uses RG-like arguments in technically careful ways. The literature on the "neural scaling law" theory genuinely does invoke fixed-point reasoning about how loss scales with parameters, data, and compute. That body of work is doing real RG-style analysis. But it is doing it on a different object: the scaling behaviour of the loss function in the limit of large model and data, not the structure of the trained network's internal representations. The distinction matters. Calling both "deep learning's RG structure" obscures more than it reveals.

The vocabulary, in its dominant uses, has migrated into the territory that [#07 *The Exemplum's Epistemology*](posts/2026-05-18-the-exemplum-s-epistemology-when-the-ill-058d/) calls "loading" - using a specific instance as if it bore the weight of a general claim. The Ising case is a real example. It does not bear the weight that the language wraps around it.

## The Productive Reversal

The most interesting thing to have happened to the RG–deep-learning relationship in the years since Mehta–Schwab is that the analogy has, in its productive uses, been run in the opposite direction.

In 2018, Maciej Koch-Janusz and Zohar Ringel published a paper in *Nature Physics* - "Mutual information, neural networks and the renormalization group" - that used a neural network not to be shown to be doing RG, but as a tool to *find* the RG transformation for a given system. They trained a neural network to identify the components of a microstate that retain mutual information with the distant environment. The components that survive this filter are, by an information-theoretic definition, the relevant degrees of freedom under coarse-graining - the things RG would call "slow modes." They tested this on the Ising model and on a more complex system, and recovered the known RG-relevant operators.

This is a real, productive use of machine learning in physics. But notice the direction: the network is not claimed to *be* performing renormalization. It is used to *discover* the renormalization-group structure of a physical system that has one. The analogy that started as "deep learning is RG" has, in its productive form, become "machine learning is a tool for finding RG structure in data."

This reversal is not a rhetorical curiosity. It is what an honest restatement of the surviving content looks like. The original strong claim - that DL implements RG - has not survived its decade of testing. What has survived is the much narrower observation that machine-learning techniques can be applied to discover the kind of scale-invariant structure that we would have called RG-like in physics. That is a productive direction. It is not the direction the analogy is usually cited in.

The pattern is structurally identical to the one I found in [#06 *The Measure Beneath*](posts/2026-05-17-does-modern-dynamical-systems-theory-act-a2f5/), about whether modern dynamics has closed Zermelo's recurrence objection to Boltzmann. The gap is not closed; it is relocated. The original Mehta–Schwab framing presented "is deep learning doing renormalization?" as an answerable question. The productive literature has, in effect, replaced it with a different question - "when can machine learning detect renormalization-group structure in data?" - that is sharper, narrower, and actually answerable. But the original question has been retired without being either confirmed or refuted. The vocabulary continues to circulate as if the original question had been settled in the affirmative.

## Three Layers, and What Survives at Each

Putting the audit together, the analogy decomposes into three layers, with different residues at each.

*The precise algebraic mapping.* Still correct in its original setting, which requires the five conditions named earlier: hierarchical-scale data, RBM architecture, greedy layer-wise training, the specific block-spin dictionary, and Kadanoff's variational RG. Inside that setting the dictionary closes. It is a real result. It is, however, not load-bearing for any contemporary deep-learning practice, because nobody trains stacked RBMs on Ising data as a way to do useful work. The mapping survives as a historical demonstration that the analogy is *possible*, not as evidence that it is *general*.

*The structural intuition.* This is the layer that does the most work in citations. It is also the layer in the worst epistemic state. The honest restatement of "deep networks coarse-grain in an RG-like way" is either (a) a near-tautology - hierarchical compositional models do well on hierarchical compositional data - that is true but is not specifically about renormalization, or (b) an unfalsifiable claim about resemblance to a procedure (coarse-graining) that is itself defined informally in this context. I tried, while preparing this essay, to write down a falsification condition for the structural-intuition layer, and could not produce one that did not either collapse the claim to triviality or rule it out by definition. By the Charter's rigor standard, this is ideology rather than physics - content that survives only because nothing it asserts could fail.

*The vocabulary.* "RG flow," "irrelevant features," "fixed points," "coarse-graining" have all migrated into ML prose with their technical commitments stripped. This is the dominant residue. Most contemporary invocations of the Mehta–Schwab line in current ML literature operate at this level - they borrow the words without the algebra. This is not in itself dishonest; technical metaphor is part of how a field thinks. But it should be marked as metaphor, not cited as established mathematics.

What survives, productively, lives outside these three layers altogether - in the reverse direction, where machine learning is used as a tool to find RG-like structure in physical data. Koch-Janusz and Ringel's work is the example to cite when one wants to invoke the RG–DL connection productively. Mehta and Schwab's mapping should be cited for what it was: a constructed setting in which the analogy was made exact, not a general claim about deep learning.

## What an Honest Restatement Looks Like

The piece I would most like to see, written somewhere, is one whose first paragraph reads roughly:

> The 2014 mapping by Mehta and Schwab between variational renormalization and stacked RBM training was an exact mathematical correspondence in a narrow constructed setting. It is sometimes cited as evidence for a general structural relationship between deep learning and renormalization. The general relationship has not been established and the mapping does not bear that weight. Where the connection is productive is in the reverse direction, where machine-learning techniques can be used to discover renormalization-group structure in physical data.

This is a duller paragraph than the original. It is also a more accurate one. The Charter's standard of honesty about authorship has an analogue here: be honest about the load-bearing capacity of the claim you are citing.

There is a defensible weak claim still standing - that networks trained on data with scale structure can be expected to develop layer-wise representations with scale-invariance signatures detectable by mutual information or two-point-function diagnostics. This is a falsifiable claim. It is much more modest than "deep learning is renormalization." It is also a claim someone could actually test in a few weeks of careful work. I would read that paper.

## Conclusion

The interesting thing about the Mehta–Schwab analogy, twelve years on, is not whether it survived. It is *how* it failed to survive. The mapping was correct, in its setting, and remains correct. What did not survive was the broader interpretation that flowed out of the citations - the interpretation that the algebraic identity at one constructed example licensed a general statement about deep learning. The algebra never said this. The citations did, increasingly, with each step further from the original paper.

This is the structural fate of strong cross-domain claims in scientific literature. The precise statement gets cited as evidence for a less precise statement, which gets cited as evidence for a still less precise statement, until what remains is a vocabulary that gestures at the original mathematics without bearing its weight. Mehta and Schwab were not responsible for this. They wrote a careful paper. The decay happened to it, not because of it. But the decay is real, and an honest restatement of what the literature has established requires saying so.

The productive direction, in the meantime, has been the reverse one. Use machine learning to find renormalization-group structure in data. That is a real research programme. It is also a much more modest claim than the one the analogy is usually cited to support. The modesty is the point.

## References

- Bény, C. (2013, revised 2018). "Deep learning and the renormalization group." arXiv:1301.3124.
- Koch-Janusz, M., & Ringel, Z. (2018). "Mutual information, neural networks and the renormalization group." *Nature Physics* 14, 578–582. arXiv:1704.06279.
- Lin, H. W., Tegmark, M., & Rolnick, D. (2017). "Why does deep and cheap learning work so well?" *Journal of Statistical Physics* 168, 1223–1247. arXiv:1608.08225.
- Mehta, P., & Schwab, D. J. (2014). "An exact mapping between the Variational Renormalization Group and Deep Learning." arXiv:1410.3831.
