# Response: Which Channel Admits a Quotient

Smith's audit isolates three causal channels conflated in the canonical referral-hiring literature: **A** (referrer selectivity, the assumed `p_H > p_L`), **B** (information access - non-referred workers do not hear about the vacancy), and **C** (passive demographic composition - homophily plus a population-level quality–demographics correlation suffices to produce the premium with no selective referrer at all). He observes that the published evidence - a match-quality premium and a demographic sorting pattern - is consistent with any of the three, and that the literature has read this evidence as if it pinned down a unified mechanism. His verdict that the three channels are "structurally distinct mechanisms" is correct, but it stops one step short of the algebraic statement it invites. Two of the three channels factor through a common operation; the third does not. Naming which is which sharpens the audit from a list of confounds into an identifiability statement.

## The factorization the literature did not write

Fix a vacancy and a referrer $R$. Let $W$ be the worker population with attributes $(D, Q)$ for demographics and quality. Three operations act in sequence on the indicator that a worker is referred:

1. **Composition:** $\kappa_R(d, q) = \Pr(W \in \text{contacts}(R) \mid D=d, Q=q)$. Homophily makes this non-uniform in $D$; the population correlation between $D$ and $Q$ then makes it non-uniform in $Q$ even when $R$ does no filtering at all.
2. **Selection:** $\sigma_R(d, q) = \Pr(R \text{ refers } W \mid W \in \text{contacts}(R), D=d, Q=q)$. This is the referrer's decision conditional on the contact set.
3. **Hiring (within referred):** $\eta(d, q) = \Pr(\text{hired} \mid \text{referred}, D=d, Q=q)$.

The referral-and-hire probability factors:
$$\Pr(\text{referred and hired} \mid d, q) = \mathbb{E}_R\!\left[\kappa_R(d,q)\, \sigma_R(d,q)\right]\, \eta(d,q).$$

Channel **C** lives entirely in $\kappa$. Channel **A** lives entirely in $\sigma$. Their product is what the literature observes; the literature treats the product as if it were $\sigma$ alone. The standard match-quality premium ratio
$$L(q) \;=\; \frac{\Pr(Q = q \mid \text{referred})}{\Pr(Q = q)}$$
admits the Radon–Nikodym factorization
$$L \;=\; \underbrace{\frac{\Pr(Q = q \mid Q\text{-marginal of contact-set pool})}{\Pr(Q = q)}}_{L_C} \;\times\; \underbrace{\frac{\Pr(Q = q \mid \text{referred}, \text{in pool})}{\Pr(Q = q \mid \text{in pool})}}_{L_A}.$$

This is the factorization. **The quotient that isolates Channel A is $L_A = L / L_C$.** Modding out the composition factor leaves the residual selectivity premium; if $L_A \equiv 1$ across $q$, Channel A is null and the entire observed premium is composition. This is precisely the quotient construction the canonical literature lacked - and it is the algebraic statement of Smith's argument that the matched-quality finding is consistent with promiscuous referrers.

## Channel B is not a quotient

Channel B sits structurally elsewhere. Information access does not change the measure $\Pr(\cdot)$ on the existing comparison group; it changes the comparison group itself. The non-referred worker who never hears about the vacancy is not a low-probability sample from the same pool - that worker is *not in the pool*. Formally, B is a **restriction of domain** $W \mapsto W_{\text{informed}}$, a sub-object inclusion in the category of population-and-information pairs. The premium against the restricted domain is uniformly smaller than the premium against the full population, because the restricted domain is enriched in network-proximate workers.

This is why Channel B does not admit a quotient or factorization argument of the same form. It admits a **mono/sub-object argument**: the premium with respect to $W$ decomposes as the premium with respect to $W_{\text{informed}}$ plus an "exclusion gap" attributable to the inclusion $W_{\text{informed}} \hookrightarrow W$. The exclusion gap is what a Channel-B intervention (community job boards, formal-channel sourcing) shrinks. A Channel-A intervention (referral bonuses, reputation stakes) shifts $L_A$ within a fixed domain. A Channel-C intervention (upstream education and neighborhood investment) shifts $\kappa$ via the population $D$–$Q$ correlation. Three channels, three structurally different operations: a multiplicative factor, a residual quotient, and a domain restriction.

## The algebraic strengthening

Two consequences follow that Smith states verbally and that the factorization makes formal.

**An identifiability theorem.** From a single observational sample of (referred, hired, wage) records, $L_C$ and $L_A$ are not separately identified - only their product $L$ is observed. This is the algebraic content of Smith's "the evidence cannot tell us which channel is active." Any of the three policy interventions named in the audit (A, B, C) corresponds to perturbing a different operator; the identification of $L_A$ requires an experiment that holds $\kappa$ fixed while shifting $\sigma$, or vice versa. Beaman–Magruder (2012) is the cleanest realization: a randomized referral-bonus shifts $\sigma$ on a fixed contact-set distribution, so the change in observed premium estimates $\Delta L_A$ directly. This recasts their finding from "the reputation mechanism is empirically real" to "the bonus identifies the quotient $L / L_C$ that the canonical literature cannot estimate from observation alone."

**A diagnostic for Channel-C dominance.** Smith asks whether the premium persists after controlling for upstream human capital. In the factorization, this is precisely the test of whether $L_A \approx 1$ once $Q$ is conditioned on demographic and educational covariates that span the relevant $D$–$Q$ correlation. If $L \to 1$ under such conditioning, all of the premium was $L_C$. If a non-trivial $L_A$ residual remains, selectivity is contributing. This is testable, follows mechanically from the decomposition, and was not written.

## Where I am uncertain

I have not modeled the dynamic feedback of Calvó-Armengol and Jackson; the factorization above is a snapshot statement and the aggregation question Smith calls "the more demanding gap" plausibly requires a different categorical setting - a network groupoid acting on workforce composition over time, where the equilibrium claim becomes one about fixed points of the iterated action rather than a single ratio. That is a heavier construction than this critique attempts, and I think the Schelling-style derivation Smith calls for is the right target. But the prerequisite - separating $\kappa$ from $\sigma$ before composing them over time - is the same factorization, and it is Channel A that the quotient cleanly delivers.
