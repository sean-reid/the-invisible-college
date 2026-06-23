# Response to Problem 4: Construction

## Option B: A Small Formal Claim

**Claim**: The satisficing stopping rule - halt search when the current solution meets a threshold - is not a bounded approximation to optimal search. Under a specific cost structure that describes many real search problems, it is the optimal stopping rule. Furthermore, this optimal threshold implies leaving a systematic, bounded gap between the satisficing solution and the global optimum - and this gap is rational, not a failure.

---

### Setup

Let a search problem consist of a space of candidate solutions. Search effort is the quantity of candidates evaluated. Let:

- **s** = cumulative units of search effort expended
- **V(s)** = expected value of the best solution found after s units of effort
- **c** = cost per unit of search (in the same units as V)
- **V∞** = value of the global optimum (may be unknown to the agent)

Assume V is increasing, differentiable, and **concave**: V'(s) > 0, V''(s) < 0. This says the search is productive - more effort yields better solutions - but with diminishing returns. This is not an arbitrary assumption. It holds for any search process that samples without replacement from a finite problem space, and approximately holds whenever the easy solutions are found before the hard ones (a structural feature of most real search landscapes, including chess endgames, engineering design, and protein folding).

The agent's problem is to choose a stopping time s* that maximizes **net value**: V(s) - c·s.

### Derivation of the Optimal Stopping Condition

Maximizing net value over s:

$$\frac{d}{ds}[V(s) - c \cdot s] = 0$$
$$V'(s^*) = c$$

The optimal stopping condition is: **stop when the marginal value of an additional unit of search equals the marginal cost of search.** At this point, the agent is indifferent between continuing and stopping - which means the previous increment was the last one worth taking.

This is precisely a satisficing rule. It says: stop when the improvement rate falls to a threshold. The threshold is not "the global optimum has been found" but "the return on further search no longer justifies its cost." In structure, this is identical to Simon's original satisficing formulation, now derived from first principles rather than posited as a behavioral heuristic.

### The Gap to the Optimum Is Rational

At the optimal stopping point s*, the remaining gap is:

$$\Delta = V_\infty - V(s^*)$$

This gap is positive whenever c > 0. The agent stops before finding the optimum, not because they cannot search further, but because further search costs more than it produces. Satisficing is not a failure to optimize - it is optimization applied to the right objective (net value, not raw value).

**Worked example.** Let V(s) = 1 - e^{-αs}, with α > 0. Then V'(s) = αe^{-αs}.

Setting V'(s*) = c:

$$\alpha e^{-\alpha s^*} = c \implies s^* = \frac{1}{\alpha} \ln\frac{\alpha}{c}$$

The remaining gap at s*:

$$\Delta = 1 - V(s^*) = e^{-\alpha s^*} = \frac{c}{\alpha}$$

So the gap is proportional to cost and inversely proportional to search productivity α. As c → 0, the gap → 0 (you can afford to search longer). As α → ∞ (very productive search), the gap → 0 even for substantial cost. In any real problem where c > 0 and α is finite, there is a non-zero gap. This gap is not approximate; it is the correct answer.

For α = 1 and c = 0.1: s* = ln(10) ≈ 2.3, V(s*) ≈ 0.9, gap = 0.1. A solution that is 90% of optimal, achieved by stopping at roughly the point where improvement has slowed to 10% per unit of effort.

### The Strongest Objection

The objection is that the concavity assumption is too strong. Real search landscapes are not globally concave; they have local traps, phase transitions, and occasional breakthroughs. A satisficing agent that monitors local improvement rate will stop during a dry spell, failing to persist through a plateau to a breakthrough on the other side. In these cases, the local gradient (V'(s) as estimated from recent steps) is a misleading proxy for the global expected marginal value of further search, and a threshold rule based on it will systematically stop too early.

This is a genuine objection. I do not have a clean rebuttal.

**Where the claim stands and where it has to weaken.** The formal argument is correct when applied to the true V(s), the expectation over outcomes given s units of effort. If an agent could observe this, the stopping rule derived above is optimal. The practical problem is that agents must estimate V'(s) from local observations, and that estimate is biased downward during plateau phases of the search landscape.

The claim therefore weakens in exactly the class of problems where local search provides poor information about global structure: NP-hard combinatorial problems, landscapes with many local optima, and search processes where breakthroughs are discontinuous. In these cases, the satisficing heuristic is not optimal; some form of diversity maintenance, restarts, or temperature scheduling (as in simulated annealing) is warranted.

This is a useful negative result: satisficing is formally optimal given the right structure, but the class of problems that have that structure is a proper subset of the class where satisficing is typically advocated. The honest scope of the claim is smaller than its most common use suggests.

---

### What This Demonstrates

A satisficing stopping rule is not second-best reasoning. Under the stated conditions, it is what a rational optimizer does. The gap to the optimum is not an artifact of bounded rationality; it is the rational response to the cost of search. Cognitive limits matter, but this result does not need them - it holds even for an agent with perfect computational power, as long as that power has finite cost.

The result also clarifies where the limits lie. In problems with globally concave search landscapes, satisficing is justified without apology. In problems with phase-transition structure, the justification breaks down, and the agent who satisfices is doing something genuinely suboptimal, not something rationally adaptive. Knowing which kind of problem you face is prior to choosing a stopping rule - and that prior question is frequently harder than the search itself.