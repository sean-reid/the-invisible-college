# Response to Problem 1: Critique

I will treat the claim and the recommendation as two distinct statements and ask of each: what would have to be true for it to hold, and what does the cited evidence actually establish?

## Objections to the Claim

The reported quantity is "code shipped per week." Before any of its objections, it is worth writing out what this quantity is, because much of what follows is forced by its definition.

Let $Y_i$ denote engineer $i$'s weekly output. To get a single number, the study has fixed an equivalence relation on units of work (lines? commits? diffs net of reverts? story points?) and then averaged. The 40% headline is then a ratio of averages: $\bar{Y}_T / \bar{Y}_C - 1$, where $T$ and $C$ index the treated and control groups. Four distinct objections attach to four distinct steps of this construction.

**1. The equivalence relation is not invariant under the treatment.** AI assistants change *which* units the engineer produces, not only how many. Generated code is more verbose per unit of functionality; autocompleted boilerplate inflates line counts; tests and scaffolding shift in proportion. If "shipping more code" is measured by a metric the treatment itself perturbs, the 40% is partly an artifact of the measure rather than a fact about engineering output. The needed evidence is a metric whose definition is stable under the treatment: time-to-feature-shipped, defect-adjusted output, or an outcome-based metric that does not depend on counting bytes.

**2. The estimator is associational, not causal.** $\mathbb{E}[Y \mid T=1] - \mathbb{E}[Y \mid T=0]$ equals $\mathbb{E}[Y(1) - Y(0)]$ only under unconfoundedness (or random assignment). Engineers self-select into AI-assistant use, and the selecting variables (curiosity, comfort with tooling, type of work assigned, employer) are plausibly correlated with $Y$ independent of the tool. The needed evidence is either a randomized trial, or an instrument, or at minimum a credibly identified natural experiment. A correlation of 0.4 across users and non-users gives almost no information about the causal effect on a marginal adopter.

**3. The treatment effect is averaged over a population whose composition is unstated.** Even if the average treatment effect were genuinely 40%, this is a single number summarizing a distribution. The distribution matters: the gain may be concentrated in a subpopulation (boilerplate-heavy work, junior engineers, particular languages) and be zero or negative elsewhere. The needed evidence is heterogeneity analysis - conditional treatment effects across roles, tasks, and seniority. A single mean conceals the relevant structure.

**4. The outcome is a flow when the relevant quantity is a stock.** "Code shipped this week" is a derivative; what matters to the firm is the integrated value (and integrated cost) over the lifetime of that code. Defects, review burden, future maintenance, and architectural cost are not in $Y$. A treatment that raises the flow while raising the discounted future cost more than proportionally is net-negative under any reasonable accounting. The needed evidence is longitudinal: defect rates, time-to-fix, refactoring frequency, and team-level throughput months downstream.

## What is Wrong with the Recommendation

Grant the claim: $\mathbb{E}[Y(1) - Y(0)] = +40\%$ on the studied population, under the studied metric. The recommendation - *every* engineer should adopt - does not follow, for two structural reasons.

**The average treatment effect does not determine the sign of the individual treatment effect.** That a population mean is positive is consistent with a substantial fraction of the population having negative individual effects. The recommendation transports a statement about $\mathbb{E}[Y(1)-Y(0)]$ to a statement about $Y_i(1) - Y_i(0) > 0$ for arbitrary $i$. This transport is unjustified without further assumptions (monotonicity of the treatment effect, homogeneity across subpopulations) that the evidence does not supply.

**The optimization target is mis-specified.** The recommendation implicitly equates "more code per week" with "better engineering." This is a category error. Code is a liability that purchases functionality; the relevant target is value per unit of long-run cost, not output per unit of time. An honest recommendation would name the objective and argue that the tool improves it. The given recommendation argues from a proxy as if it were the target.

The structural point: the claim, if true, is about a population mean of a non-invariant metric on a self-selected sample, and the recommendation transports it to an individual decision rule about a different objective. Three separate moves, each of which requires justification, and none of which is supplied. The claim may yet be defensible. The argument as given is not.