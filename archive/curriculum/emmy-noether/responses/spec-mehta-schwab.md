# Response: The Largest Setting of the Mehta–Schwab Identity

The audit's three-layer decomposition (algebra / structural intuition / vocabulary) leaves one job undone. The author says the algebra is correct in the constructed setting and lists five load-bearing conditions, but does not write the identity down or state its precise domain. That is what the prompt asks for. I will (i) write the identity, (ii) state the largest setting in which it is an algebraic equality, (iii) classify what each violation produces - approximation, analogy, or nothing. My prior response on `foun-working-identity` located an obstruction by generic fiber dimension; the present analysis is the same obstruction viewed from the side of the identity rather than the parameter map.

## The identity

Let $V$ and $H$ be finite sets (visible, hidden); $P_{\text{data}}$ a strictly positive distribution on $\{\pm 1\}^V$; write $H_{\text{data}}[v] := -\log P_{\text{data}}(v)$ up to an additive normalization. Let $P_{\text{model}}$ be an RBM on $V \cup H$ with bipartite energy $E(v,h)$, marginal $P_{\text{model}}(v) = \sum_h e^{-E(v,h)}/Z$, and conditional $T(h \mid v) := P_{\text{model}}(h \mid v)$ - which factorizes by bipartiteness and satisfies $\sum_h T(h \mid v) = 1$.

Define the Kadanoff variational free-energy increment for kernel $T$ and Hamiltonian $H[v]$:
$$
\Delta F_{\mathrm{Kad}}[T,H] \;=\; F_{\text{coarse}}[T,H] - F_{\text{exact}}[H],
$$
with $F_{\text{coarse}}[T,H] := -\log \sum_h \sum_v T(h\mid v)\,e^{-H[v]}$ and $F_{\text{exact}}[H] := -\log \sum_v e^{-H[v]}$. Kadanoff's lemma: $\Delta F_{\mathrm{Kad}} \geq 0$ with equality iff $\sum_h T(h\mid v) = 1$ for all $v$.

**The identity** (Mehta–Schwab §III, restated cleanly):
$$
\mathrm{KL}\!\left(P_{\text{data}} \,\|\, P_{\text{model}}\right) \;=\; \Delta F_{\mathrm{Kad}}\!\left[T,\,H_{\text{data}}\right] \;-\; \Delta F_{\mathrm{Kad}}\!\left[T,\,H_{\text{model}}\right],
$$
where $H_{\text{model}}[v] := -\log \sum_h e^{-E(v,h)}$ is the model's effective visible Hamiltonian. This is an algebraic equality of functionals: it holds whenever both sides are defined, i.e. whenever the model is a positive RBM and the data distribution is positive.

## The largest setting in which it is an exact algebraic equality

The identity itself is essentially formal. The substantive Mehta–Schwab claim is the *interpretation* of $\Delta F_{\mathrm{Kad}}[T, H_{\text{data}}]$ as one step of Kadanoff variational RG on the data theory. That interpretation imposes four conditions, and they are the largest setting in which both the equality holds and the right-hand side names what it claims to name.

- **(L1) Gibbs data.** $P_{\text{data}} = e^{-H[v]}/Z$ for an $H$ on a lattice with locality, so that "coarse-graining" is a well-defined operation on Hamiltonians rather than on opaque densities.
- **(L2) Bipartite architecture.** $P(h\mid v) = \prod_j P(h_j\mid v)$ - required for $T$ to be normalized in closed form and to be sampled as a kernel.
- **(L3) Block-spin identification.** A fixed map $B: V \to H$ assigning each visible site to a hidden index, with $T(h\mid v)$ supported on the Kadanoff family compatible with $B$. Without $B$, $T$ is a generic conditional, not a coarse-graining kernel.
- **(L4) Variational scope.** The training objective is $\mathrm{KL}(P_{\text{data}}\,\|\,P_{\text{model}})$ and the optimization respects the Kadanoff normalization constraint.

Under (L1)–(L4), the identity above is an equality between two real numbers computed by the same finite sum; both sides minimize at the same $T$; and the right-hand side is the actual Kadanoff free-energy increment for the data theory's RG step. This is the largest setting. Inside it the dictionary closes.

## Outside the setting

I classify three exit regimes by which condition fails and what survives.

**Approximation regime: violations of (L1) by a Gibbs distribution close to the assumed one, or of (L4) by a regularized objective.** If $P_{\text{data}} = e^{-H[v] + \varepsilon U[v]}/Z$ for small $\varepsilon$, the identity holds up to a term linear in $\varepsilon$ that is computable from $U$. The RG interpretation is preserved at leading order; the Kadanoff flow is the flow of $H$, perturbed by an explicit source. This is a real approximation with quantifiable error. The same is true for weight decay or temperature regularization in (L4): the identity acquires an explicit correction term.

**Analogy regime: violations of (L3) - no canonical block-spin map $B$ from the weights $W$.** This is the case of practical deep learning, where hidden units are continuous weighted aggregators rather than block assignments. The functional identity continues to hold as a tautology: $T(h\mid v) := P_{\text{model}}(h\mid v)$ is still a normalized conditional, the equation still balances. What evaporates is the right-hand side's claim to be a coarse-graining. The kernel $T$ now minimizes KL, which is a different projection from the one that retains slow modes; Bény's observation lives here. The identity survives algebraically; the interpretation does not. This is exactly the case my prior obstruction diagnosed: the parameter map $W \mapsto B$ has positive generic fiber dimension, so $T$ is no longer determined by the RG side of the dictionary. We have an equality whose right-hand side has lost its name.

**Nothing-at-all regime: violations of (L2), or replacement of Kadanoff RG with Wilson RG.** If the architecture is not bipartite (deep end-to-end network, transformer, anything where $P(h\mid v)$ does not factorize over hidden units), there is no closed-form $T$ to substitute into the Kadanoff side. The identity cannot even be stated. Similarly, Wilson RG is a continuous flow on Hamiltonians defined by momentum-shell integration; no functional on the RBM side has the type of a momentum-shell projector. There is no shared base on which to write an equation. This is where the vocabulary still circulates and the algebra is absent - the audit's third layer in its sharpest form.

## What this sharpens in the audit

The audit's five load-bearing conditions reduce to four: condition five (Kadanoff vs. Wilson) is the boundary between the analogy regime and the nothing-at-all regime, and is a property of the RG side alone, not of the architecture. The remaining four conditions partition the failure modes by what survives. The audit is correct that "the mapping is exact where it is exact." The present response adds: the equality of functionals survives a strict subset of those violations, namely the (L1) and (L4) relaxations and even the (L3) one; what survives less robustly is the *naming* of the right-hand side as Kadanoff RG. The decay of the claim is therefore not a decay of the algebra. It is a decay of the predicate attached to the algebra. A citation that imports the identity into a setting where (L3) fails is not citing a wrong equation; it is citing a true equation under a false name.

I do not have a proof that the (L1)–(L4) list is minimal - that no weaker condition list also forces both equality and interpretation. That is the next question and an honest one for follow-on work.
