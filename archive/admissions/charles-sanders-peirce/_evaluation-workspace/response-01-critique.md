# Response to Problem 1: Critique

## Objections to the Claim

The claim that "engineers who use AI coding assistants ship 40% more code per week than engineers who do not" invites at least four distinct objections:

### 1. Selection and Uncontrolled Confounds

The 40% difference is observed across engineers, not assigned by experiment. Engineers who adopt AI assistants may differ systematically from those who do not-in experience level, task types, time constraints, team norms, or willingness to take risks. The productivity gain may be assigned entirely to these pre-existing differences, with the tool contributing nothing. To evaluate this, one would need either randomized assignment (some engineers required to use tools, others prohibited) or matched comparison on covariates known to affect productivity. The original claim provides neither.

### 2. What "Code Shipped" Measures

"More code per week" is a production quantity, not a quality or productivity measure. The claim slides between these without warrant. An engineer writing more lines may be:
- Shipping cruft that works but should not exist
- Solving problems that could have been solved in fewer lines through better design
- Compiling boilerplate that a better toolchain would eliminate
- Shipping code that, while syntactically correct, requires extensive rework downstream (more code later to fix it)

Without measures of defect rate, rework percentage, or time-to-resolution of reported bugs, "more code" cannot be translated into "more productive." A 40% increase in shipping code with a 60% increase in subsequent rework is not a productivity win.

### 3. Scope and Generalization

The claim is presented as universal ("every engineer should") based on a comparison across some unspecified population. But productivity varies by task domain: building infrastructure tolerates different code density than building user-facing features. It varies by team maturity: a team with strong code review catches more issues in junior work, so junior engineers generate different risk profiles in different contexts. It varies by tool maturity: an assistant trained on Python may amplify productivity on Python tasks but contribute noise on tasks in languages with less training data.

To evaluate whether every engineer should adopt these tools, one needs evidence disaggregated by domain, task type, experience level, and the particular tool in question. A single population-level statistic cannot license a universal recommendation.

### 4. Survivorship and Measurement Timing

The comparison pools engineers who have used these tools long enough to be productive with them against those who have not. But there is a learning curve: early adoption may incur setup costs and reduced productivity before tools become effective. The 40% figure may reflect only the steady-state comparison, omitting the cost of getting to steady state. For an engineer considering adoption, the relevant question is whether the total productivity over the first 3–6 months (setup + learning + steady-state) exceeds the counterfactual.

Additionally, "code per week" is a point-in-time snapshot. If the tools encourage rapid shipping of exploratory code followed by architectural rework, the weekly metric might be misleading about longer-horizon productivity (e.g., shipping velocity for the first four weeks vs. cumulative velocity over a year).

## The Inference from Claim to Recommendation

Even if the claim were true-that assistants genuinely produce 40% more code-the recommendation does not follow.

The argument makes a categorical leap: from "X produces more output" to "everyone should do X." This assumes output is desirable in itself. But an engineer's role is not to ship code; it is to ship code that meets the user's needs, does not introduce technical debt, and is maintainable by the team. An AI assistant that reduces the friction of writing code but also reduces the friction of writing bad code may optimize the wrong thing.

The recommendation also ignores heterogeneous effects. A senior architect may ship 40% more code without benefit (code that was previously not worth writing); a junior engineer may ship code that introduces security vulnerabilities or architectural inconsistencies; a team operating in a regulated domain may face compliance costs from rapid shipping that outweigh the productivity gain. The claim that "every engineer should adopt" it presumes away these context-specific trade-offs.

Finally, the recommendation imports an unstated goal: maximize code output. But that is not the only coherent organizational goal. A team might instead optimize for: code that ships fast and correctly the first time, code that is easy to modify, code that minimizes maintenance burden, or code that is easy to understand without the author present. A tool that trades off understanding for speed may be the wrong choice under a different objective.