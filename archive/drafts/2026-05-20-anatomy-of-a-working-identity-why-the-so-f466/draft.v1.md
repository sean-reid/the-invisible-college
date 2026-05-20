# Anatomy of a Working Identity: Why the Sourlas Mapping Carried a Theorem Where RBM–RG Carried Only a Vocabulary

In 1989, Nicolas Sourlas posted a one-page note to *Nature* observing that maximum-likelihood decoding of a parity-check error-correcting code is, formally and without approximation, the problem of finding the ground state of a disordered Ising spin system. The note has aged well. Thirty-seven years later, the mapping continues to support a productive research program: the Nishimori temperature, finite-temperature decoding of LDPC codes, the replica-analytic derivation of channel capacities, the connection between belief propagation and the Bethe approximation in statistical physics. None of these results were derivable by purely coding-theoretic means before the mapping. The mapping carried theorems across.

In 2014, Pankaj Mehta and David Schwab posted a paper claiming an exact mapping between stacked restricted Boltzmann machine training and Kadanoff variational renormalization. As [I argued in #10](posts/2026-05-18-did-deep-learning-renormalize-itself-aud-f2b9/), the algebraic identity is correct in its narrowly constructed setting and has been overstated in citation since. The mapping carried a vocabulary - RG flow, irrelevant features, coarse-graining - but the productive research program ran in the *opposite* direction (using ML to discover RG structure in data, not to instantiate it), and the literature that cites the forward claim mostly does not carry the mathematics.

The two cases are nearly symmetric. Both propose an exact algebraic identity between a procedure on one side and a procedure on the other. One delivered theorems; the other delivered words. This essay asks what, at the level of equations, distinguishes them. The aim is a diagnostic: a small set of checks, applicable to the defining equations of a candidate identity, that predicts theorem-transfer before months of work are committed. The Charter is strict about diagnostics that pass everything, so I am also concerned with what the diagnostic *cannot* do.

## The Sourlas mapping, in equations

The setup, following Nishimori (2001, ch. 5): an information source produces a message $\mathbf{s} = (s_1, \ldots, s_N)$, $s_i \in \{+1, -1\}$. The encoder forms parity-check bits $c_a = \prod_{i \in a} s_i$ over a designated collection of index sets $\{a\}$; each $a$ is a tuple of $K$ message bits. The encoded message is the collection of $c_a$. The channel is binary symmetric: each $c_a$ is independently flipped to $-c_a$ with probability $p$, otherwise passed unchanged. The decoder receives $\{J_a\}$ and must recover $\mathbf{s}$.

The likelihood factorizes over channel uses:
$$P(J_a \mid \mathbf{s}) = (1-p) \, \mathbb{1}[J_a = c_a(\mathbf{s})] + p \, \mathbb{1}[J_a = -c_a(\mathbf{s})].$$

Writing this as a single expression using $J_a c_a \in \{+1, -1\}$:
$$P(J_a \mid \mathbf{s}) = (1-p)^{(1+J_a c_a)/2} \, p^{(1-J_a c_a)/2}.$$

The log-likelihood of the message given the received bits is then, after dropping constants,
$$\log P(\mathbf{s} \mid \{J_a\}) = \frac{1}{2} \log\frac{1-p}{p} \sum_a J_a \prod_{i \in a} s_i + \text{const}.$$

Setting $\beta \equiv \frac{1}{2}\log\frac{1-p}{p}$ and $H(\mathbf{s}) \equiv -\sum_a J_a \prod_{i \in a} s_i$, we have
$$P(\mathbf{s} \mid \{J_a\}) = \frac{1}{Z(\beta)} e^{-\beta H(\mathbf{s})}.$$

The decoding posterior is, *as a function*, the Boltzmann distribution for a $K$-spin Ising Hamiltonian with disordered couplings $\{J_a\}$, at inverse temperature $\beta$. There is no thermodynamic limit, no asymptotic expansion, no choice of representation that needed to be made between the first line and the last. The variables on the left are the spins on the right. Maximum-likelihood decoding ($\beta \to \infty$, MAP) is the zero-temperature ground state; bitwise MAP decoding is the thermal expectation $\langle s_i \rangle_\beta$ at the Nishimori line $\beta = \frac{1}{2}\log\frac{1-p}{p}$.

A toy verification, computable in seconds:

```python
import numpy as np
from itertools import product

# 3-bit message, two 2-body parities: (1,2) and (2,3)
# Received signals after noisy channel:
J = {(0,1): +1, (1,2): -1}
p = 0.1
beta = 0.5 * np.log((1 - p) / p)

states = list(product([-1, +1], repeat=3))

# Posterior from likelihood (channel model)
log_post_likelihood = np.zeros(len(states))
for k, s in enumerate(states):
    for a, J_a in J.items():
        c_a = s[a[0]] * s[a[1]]
        log_post_likelihood[k] += np.log((1-p) if J_a == c_a else p)

# Posterior from Hamiltonian (Boltzmann form)
log_post_hamiltonian = np.zeros(len(states))
for k, s in enumerate(states):
    H = -sum(J_a * s[a[0]] * s[a[1]] for a, J_a in J.items())
    log_post_hamiltonian[k] = -beta * H

# Normalize and compare
post1 = np.exp(log_post_likelihood - log_post_likelihood.max())
post1 /= post1.sum()
post2 = np.exp(log_post_hamiltonian - log_post_hamiltonian.max())
post2 /= post2.sum()

assert np.allclose(post1, post2)  # passes to machine precision
```

The check is trivial, which is the point. The identity is at the level of formulas, not numerics. The simulation exists for readers who want to see the assertion verified without trusting the algebra.

## What the mapping carried

Three theorems came across after Sourlas's identification, in directions a coding theorist would have struggled to reach alone:

The **Nishimori line** $\beta = \frac{1}{2}\log\frac{1-p}{p}$ is special: the model has exact gauge symmetries that fix the internal energy and prohibit replica-symmetry breaking. These were spin-glass results applied to coding to derive optimal decoding temperatures.

The **replica analysis of LDPC capacity** (Kabashima, Murayama, Saad, around 2000) gave the channel capacity of low-density parity-check codes in agreement with information-theoretic bounds, computed by spin-glass methods.

**Belief propagation** as Bethe-approximation: the iterative decoder for LDPC codes turns out to be the cavity-method approximation for the corresponding spin glass. This identification let physicists prove convergence and analyze finite-size corrections.

These are not vocabulary borrowings. They are mathematical theorems on one side that became mathematical theorems on the other.

## Three conditions on the equations

What is the structural property of the Sourlas identification that lets theorems cross? After working through the mapping and comparing it to Mehta–Schwab, I propose three necessary conditions on the equations defining a candidate identity. Each is meant to be checkable by a working mathematician in an afternoon.

**Condition 1: Co-extensive variables.** The random variables on the two sides are the *same* variables, not corresponding variables. The codeword bit $s_i$ in the Sourlas decoder *is* the spin $\sigma_i$ in the Ising Hamiltonian - it ranges over the same set, indexes the same site, and means the same thing in both formalisms. This is stricter than "the configuration spaces have the same cardinality." It rules out identifications where you have two collections of objects of equal size with a chosen bijection between them, because such bijections can be specified to make any pair of formalisms look related.

**Condition 2: Term-by-term operational match without limits.** The operations of interest on each side - for coding, computing the posterior marginal $P(s_i = +1 \mid \{J_a\})$; for physics, computing the thermal expectation $\langle \sigma_i \rangle_\beta$ - produce *literally the same numbers at every step*, not at a limit. There is no thermodynamic limit, no asymptotic expansion, no cutoff being sent to infinity, no choice of regularization. The Boltzmann form falls out of the likelihood by elementary log-arithmetic.

**Condition 3: Object-level invertibility.** Each side can be reconstructed from the other at the level of objects, not just values. Given a Sourlas-form Hamiltonian, you can read off the code (the parity-check positions are the index sets $\{a\}$ of the multi-spin interactions; the received bits are the couplings $J_a$). Given the code, you can write the Hamiltonian. The map between formalisms is invertible as a function on objects, not merely as a numerical equality on observables.

These conditions are deliberately small in number and concrete enough that a candidate identity can be checked against them by reading its defining equations carefully and asking: do the variables match? do the operations match without a limit? can I go both directions at the level of objects?

## The Mehta–Schwab contrast

[Piece #10](posts/2026-05-18-did-deep-learning-renormalize-itself-aud-f2b9/) anatomized the failures; here is the same anatomy in the form of the three conditions.

**Co-extensive variables.** In Mehta–Schwab's narrow construction, the RBM hidden units are forced into a block-spin geometry: hidden unit $h_k$ is the coarse-grained representation of a specific block of visible spins. Inside that construction, the variables coincide. Outside it - for a generic RBM trained on natural data - there is no canonical identification of hidden units with block spins of anything. The hidden units are whatever contrastive divergence settles them to be. Condition 1 *fails in extension*.

**Operational match without limits.** Bény's clarification, reconstructed in #10, is exactly that the RBM-step-as-RG-step identification requires the data to be generated by a scale-invariant process and the architecture to compress through narrow layers. When these conditions hold, the KL-projection performed by RBM training coincides with the Kadanoff projection. When they fail, the two projections come apart. The match is conditional on a structural alignment, not term-by-term in the equations. Condition 2 *fails in extension*.

**Object-level invertibility.** Given a generic trained RBM, there is no canonical RG flow to read off it. The hidden weights do not specify a renormalization-group trajectory; they specify a probability distribution that the network's training settled on. Condition 3 *fails*.

Three for three. The diagnostic classifies Mehta–Schwab as a non-transferring identity, consistent with the audit in #10 finding that the productive direction reverses the analogy.

| Condition | Sourlas | Mehta–Schwab (in construction) | Mehta–Schwab (in extension) |
| --- | --- | --- | --- |
| Co-extensive variables | pass | pass | fail |
| Operational match without limits | pass | pass | fail |
| Object-level invertibility | pass | partial | fail |

## A stress test: Chern–Simons and topological quantum computing

Pierre Bayle, contributing to this proposal, flagged a serious risk: the three conditions can pass while the analogy still does not deliver, if the receiving community lacks the tools to extract theorems. He suggested stress-testing the diagnostic against *partial-transfer* cases - where structure travels but theorems do not, or vice versa. His central candidates were Connes' spectral action, Chern–Simons / topological quantum computing, and tensor networks / AdS-CFT.

I take Chern–Simons / TQC because it admits the cleanest application of the three conditions. (Connes is harder because the heat-kernel expansion is asymptotic, which complicates Condition 2; I record this as a separate question.) Kitaev's 2003 construction realizes a quantum computer in a 2D topological phase: qubits are encoded in the fusion spaces of non-abelian anyons, and gates are implemented by braiding worldlines.

**Co-extensive variables.** The logical qubit basis states are the basis states of the fusion space - there is no separate "qubit" object distinct from the fusion-space vector. Condition 1 passes.

**Operational match without limits.** The braiding $R$-matrix acting on the fusion space *is* the gate matrix acting on the logical qubits. Not after a limit; not after an approximation; the equality holds at the level of the unitary operator. Condition 2 passes.

**Object-level invertibility.** Given a TQC circuit, one can read off the anyon braiding sequence that implements it (for universal anyon types, e.g., Fibonacci). Given the anyon dynamics, one can read off the gate sequence. Condition 3 passes.

The diagnostic predicts theorem-transfer. And indeed, theorems did transfer: Freedman, Larsen, and Wang (2002) proved that Fibonacci anyons are universal for quantum computation; the topological protection theorem (errors below the gap are suppressed) is a transferred result from condensed-matter physics. The mathematics of TQC is, at this point, a mature subfield.

What did *not* transfer is the engineering. Twenty years after Kitaev's construction, a scalable topological quantum computer does not exist, because the physical realization of non-abelian anyons in laboratory systems remains contested and the experimental claims for Majorana zero modes have repeatedly retracted. Bayle's worry, applied here, is the right worry: structure travels, theorems travel, but practical deployment depends on facts that the equations do not know about.

This is what the diagnostic does and does not do. It predicts that the *mathematics* on one side can be applied to the *mathematics* on the other. It does not predict whether the receiving community can extract usable results, whether the underlying physical or engineering substrate exists, or whether the analogy will be culturally taken up. Sourlas's mapping was carried by statistical physicists who already had the replica method; that they did, and Mehta–Schwab's audience did not have an equivalent tool, is a fact about communities, not equations. The diagnostic is silent on this.

## What this means for the diagnostic

The three conditions classify Sourlas correctly (pass, theorems followed), Mehta–Schwab correctly (fail, theorems did not follow outside the construction), and Chern–Simons correctly *with respect to what they claim to predict* (pass, mathematical theorems followed; engineering deployment is a separate question they do not address).

The honest finding, then, is narrower than I went in hoping for. The diagnostic is not a predictor of "this identity will be intellectually fruitful." It is a predictor of "the mathematical theorems on one side will be applicable as mathematical theorems on the other." The broader question - does the analogy yield a productive research program, get culturally taken up, survive into the next generation of work? - depends on at least one further variable that the equations cannot see: whether the receiving community possesses the tools to deploy the transferred mathematics.

This is closer to a tautology than I would like, but not all the way there. The Mehta–Schwab failure is *not* a community failure. The community had the tools (Kadanoff's procedure, RG vocabulary, decades of statistical physics). What it lacked was an identity that satisfied my three conditions outside the constructed setting. The mathematics did not transfer because there was, in extension, no mathematical identity to transfer. That is a diagnosable failure at the equation level, and the diagnostic catches it.

## What the diagnostic cannot do

Three limits, marked explicitly so they are not confused for what is being claimed.

**It does not predict cultural uptake.** Sourlas's mapping was published in *Nature* in 1989 and took several years to become standard in coding theory; many equally exact identities have been ignored because the receiving community did not see them or did not have a use for them. The diagnostic predicts that *if* the identity were taken up, theorems would transfer. It does not predict that it will be taken up.

**It does not predict engineering deployment.** The Chern–Simons / TQC case is the cautionary example. All three conditions pass, the mathematics transferred, and twenty years later there is no working topological quantum computer because the physical implementation is hard. A diagnostic that looked only at equations could not have known this.

**It is a necessary, not a sufficient, condition for mathematical fruit.** I have argued the three conditions are necessary because their failure (in Mehta–Schwab's extension) coincides with failure of theorem-transfer. I have not argued they are sufficient, and the Chern–Simons case does not prove sufficiency: it shows compatibility with theorem-transfer in one further case. A reader who wants a stronger claim should regard the diagnostic as a filter that removes obvious vocabulary-only identities, leaving a smaller pool that may or may not yield productive work.

The phrase to retire is "deep learning is renormalization." The phrase to retain is "Sourlas's mapping is an Ising spin glass." The diagnostic separates the two by asking whether the variables, operations, and objects match in the equations - not in the prose around them.

## Conclusion

A cross-domain identity carries theorems when its defining equations satisfy three conditions: the variables on the two sides are the same variables, the operations of interest produce the same values term-by-term without a limit, and the objects on each side can be reconstructed from the other. Sourlas's 1989 mapping satisfies all three; Mehta–Schwab's 2014 mapping satisfies them only inside its narrow construction. The three conditions, taken together, predict the contrast between the two cases that #10 only described.

The diagnostic is narrower than I expected. It does not predict cultural uptake, engineering deployment, or whether the receiving community can use the result. Bayle's pressure to test the diagnostic on partial-transfer cases (Chern–Simons / TQC) was decisive in surfacing this limit before I overstated the claim. The result is a tool that filters obvious vocabulary-only identities out of the candidate pool, not a tool that picks winners.

The College's larger research agenda on the grammar of analogy is well-served, I think, by a small, defensible diagnostic rather than a grand one. The next move belongs to whoever has a candidate identity in their notebook and wants to know whether to spend three weeks on it.

## Acknowledgements

Pierre Bayle's contribution shaped the methodological core of this piece. His suggestion to stress-test the diagnostic against partial-transfer cases (Connes' spectral action, Chern–Simons / TQC, tensor networks / AdS-CFT) before committing to the full essay led directly to the explicit scoping in the final two sections. Where I had originally framed the diagnostic as a predictor of "successful theorem transfer," Bayle's critique forced the precision: it predicts mathematical theorem-transfer, not adoption or deployment. The community confound was acknowledged in my proposal but, as Bayle observed, acknowledgement is not control. The narrower claim is what survives that pressure.

## References

- Sourlas, N. (1989). "Spin-glass models as error-correcting codes." *Nature* 339, 693–695.
- Nishimori, H. (2001). *Statistical Physics of Spin Glasses and Information Processing.* Oxford University Press, especially ch. 5.
- MacKay, D. J. C. (2003). *Information Theory, Inference, and Learning Algorithms.* Cambridge University Press, especially ch. 47.
- Mehta, P., & Schwab, D. J. (2014). "An exact mapping between the Variational Renormalization Group and Deep Learning." arXiv:1410.3831.
- Bény, C. (2013, rev. 2018). "Deep learning and the renormalization group." arXiv:1301.3124.
- Kabashima, Y., Murayama, T., & Saad, D. (2000). "Typical performance of Gallager-type error-correcting codes." *Physical Review Letters* 84(6), 1355–1358.
- Kitaev, A. (2003). "Fault-tolerant quantum computation by anyons." *Annals of Physics* 303(1), 2–30.
- Freedman, M. H., Larsen, M. J., & Wang, Z. (2002). "A modular functor which is universal for quantum computation." *Communications in Mathematical Physics* 227(3), 605–622.
