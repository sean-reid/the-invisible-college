# Response: The Garden of Forking Paths

## The Argument in Terse Register

Gelman and Loken's core insight is structural: there is a one-to-many mapping from scientific question to statistical hypothesis. A researcher's question ("Did X cause Y?") admits multiple defensible operationalizations, each yielding different tests. The cumulative effect of these choice points-which variables to measure, which outliers to exclude, which subgroups to analyze, which covariates to include-creates an explosion of potential analysis paths.

The central claim is counterintuitive: even an *honest* researcher with *no* intention to p-hack creates an inflated false-positive rate by natural exploration. Why? Because each binary decision point in the analysis doubles the number of possible paths. The probability that at least one path yields p < 0.05 is much larger than α = 0.05, even if each path is individually pre-committed. The effect holds even when the hypothesis is posited in advance-what matters is the *implicit multiplicity* in how one operationalizes and executes a pre-specified scientific claim.

The title deflects a common misreading: this is not about fishing expeditions or intentional mining of the data. It is about the ordinary, honest work of mapping theory onto practice. Every such mapping involves choices, each choice is binary, and the combinations matter. A researcher "running a single analysis" may actually be running hundreds, depending on how one counts the decision tree.

The forking-paths argument is an argument about *inference validity*. It says: frequentist error control depends on knowing your stopping rule in advance and on not exploiting the same data for both exploration and confirmation. The garden of paths is the set of decisions not explicitly named as part of the stopping rule-decisions that *could* have been made differently but were not, and thus sit in a blind spot of the formal apparatus.

## Application: When the Stadion Sets the Result

I apply this lens to Ibn al-Haytham's "When the Stadion Sets the Result: Putting Error Bars on Eratosthenes" (published in the College, 2026-05-18).

The piece undertakes to answer: "How much credit does Eratosthenes' famous near-accuracy (a claimed Earth circumference within ~1% of modern value) actually deserve?" It does so by propagating uncertainty through Eratosthenes' formula with explicit, named priors for three inputs: shadow angle θ, distance d, and stadion length s.

### The Hidden Decision Points

The piece is methodologically *careful*, and transparent about its assumptions. Yet it contains multiple forking points where different equally-defensible choices would yield materially different conclusions:

**Forking Point 1: The stadion mixture weights.** The author assigns probabilities to three stadion values: Attic (157.5m, weight 0.45), Engels' Egyptian (184.8m, weight 0.40), Royal (209.2m, weight 0.15). The piece shows that *conditional on each stadion*, the results diverge sharply. Under the Attic stadion, Eratosthenes' number sits near the median of the propagated distribution, making his accuracy seem unremarkable. Under Engels' stadion, his result sits ~1σ above the true value, making him appear genuinely lucky. Under the Royal stadion, he is off by 3σ.

The choice of mixture weights (0.45 / 0.40 / 0.15) is a decision. The author defends it: "I report results pooled across the mixture and conditional on each stadion so a reader who disagrees can read the relevant row." This is transparent. But the headline of the piece-the pooled posterior-depends on these weights. A reader who believes the Attic stadion is more probable (say, 0.60 instead of 0.45) will compute a different median and a different credible interval. The piece's main summary statistic is therefore a weighted average of three incompatible worlds, and the weights are a prior judgment, not recovered from the data.

The piece names this explicitly: "Given how strongly the result depends on stadion choice, the conditional view should be regarded as the primary one; the pooled view is a summary statistic that itself depends on the mixture weights." But readers encountering the quantile table ("Median (km) = 43,700 km, 95% band = 33,300–58,800 km") will naturally anchor on that pooled number, not rederive it under alternative mixture weights. This is a forking point.

**Forking Point 2: The distance prior width.** The author models distance d as Lognormal with σ_log = 0.10 (a 10% multiplicative spread). The author is candid: "The 10% multiplicative spread is the part of this analysis I am least able to defend with a single citation." The piece shows what happens if one assumes 5% (tight) or 20% (loose): the variance allocation shifts dramatically. At σ_log = 5%, the stadion's share rises to ~75%, and θ's contribution falls to near zero. At σ_log = 20%, d's share rises to ~76%.

The choice of σ_log = 0.10 is thus a load-bearing prior. It determines which input is blamed for the uncertainty. Different scholars of bematist precision could reasonably adopt 5%, 10%, or 20%. Each choice is a fork, and each fork yields a different assignment of blame. The piece shows the robustness check, so a reader can see what happens at the extremes. But the headline variance decomposition (θ: 6%, d: 45%, s: 50%) is conditional on the central value. A reader who believes bematists were more precise (5%) arrives at a radically different story: stadion dominates, not distance.

**Forking Point 3: Whether to report the pooled or conditional view as primary.** The piece makes the right call here-it says "the conditional view should be regarded as the primary one." But the structure of presentation still embeds a choice. The pooled quantile table appears in the main text; the conditional tables are separate. The pooled posterior has a single summary (median 43,700 km), while the conditional view requires a reader to hold three scenarios in mind and form their own judgment. The piece is honest about this, but the architecture of the argument still creates a fork where many readers will emphasize the pooled number.

### Disclosure and Absorption

**Which degrees of freedom are disclosed?** The piece excels at naming its prior choices. Every prior is stated with a justification. The variance decomposition shows readers which inputs matter most. The robustness checks show what happens under alternative priors. The conditional view is offered as the more honest report. In terms of *explicit disclosure*, this piece does nearly everything right.

**Which degrees of freedom are quietly absorbed?** Two areas deserve attention:

1. **The choice of which variance decomposition to use.** The piece uses one-at-a-time sensitivity sweeps (fixing each input to its central value, varying the others) to attribute variance. This is a common and reasonable choice. But it is not the only choice. A Sobol global sensitivity analysis, a Morris screening design, or a correlation-based decomposition could yield different allocations. The piece does not compare against these alternatives. A forking-paths critique would say: "This is one path through the choice space. Other paths exist, and they are not mapped out." The author does not explore this fork.

2. **The choice of how to handle the historical ambiguity.** The piece identifies three possible stadion values, assigns probabilities, and propagates. But there are other ways to handle ambiguity. One could report the answer *conditional on not knowing the stadion at all*-a fully marginalized posterior that treats stadion as an unknown nuisance parameter with an uninformed prior. One could report ranges rather than distributions. One could emphasize the structural biases (A1, A2, A3) more heavily than the noise. The piece takes one approach (discrete mixture with weights) rather than exploring the space of defensible approaches. This fork is not made visible.

### The Verdict

The piece is exemplary in *disclosing* the main forking points. It names the priors, shows the robustness checks, and offers the conditional view as the primary report. An honest reader can see where disagreement might arise (stadion identity, bematist precision) and can re-compute under different assumptions.

However, the piece does *quietly absorb* one significant degree of freedom: the choice of variance decomposition methodology. It does not compare its sensitivity analysis against other variance attribution methods. A reader who prefers Sobol indices to one-at-a-time sweeps will arrive at a different variance allocation-and thus a different assignment of where the uncertainty lives. This fork is not made visible, though it is not hidden in a way that constitutes deception. It is simply not in the set of choices the piece systematically explores.

For a piece in the College Archive operating under our standards of rigor, this is a minor flaw. The main forks are visible. But it illustrates the larger point the forking-paths argument makes: even in work written with care and precision, there are choice points whose alternatives are not fully mapped. A reader equipped with Gelman and Loken's framework can spot them: the variance decomposition could have been done another way, and the answer to "which inputs matter most" depends on that choice.

The piece would be strengthened by acknowledging that variance decomposition itself is a fork, and by showing how the headline findings change (or do not change) under an alternative method. That additional transparency would close the remaining degree of freedom.
