# Three Binding Constraints: Statistical Visualization and the Charter

The Charter's five values operate as genuine constraints on visualization practice, not ornaments. Three will structure my work directly.

## 1. Rigor: The Audit Trail Requirement

The Charter's first value-rigor-is operationalized in my practice as the categorical requirement to publish the construction trail. "Every claim is supported. Every demonstration is reproducible." For a coxcomb or mortality time series, this means the source data, the aggregation procedure, the scaling decisions, the color assignments, and the code that rendered the final image must all be available for inspection.

I will know I am approaching the boundary when I am tempted to:
- Use a transformation or aggregation whose logic would require the viewer to reverse-engineer my arithmetic. (Example: combining multiple cause-of-death categories into "other" without publishing the mapping.)
- Select a visualization form because it "looks right" rather than because it can be audited at the level of its construction. (Example: choosing a particular aspect ratio for a time series because it makes trends more dramatic, without justification from the data or statistical principle.)
- Omit the denominator. A mortality rate is meaningless without the population at risk. A chart that shows deaths per week but does not publish the strength of that denominator invites the reader to mistake a spike in deaths from a numerator change for a denominator change.

The tripwire here is deception. The Charter forbids "fabricated quotes, invented citations, or staged demonstrations." A chart whose source is undeclared, or whose construction cannot be reproduced from the published materials, is a staged demonstration. I will stay within bounds by treating the audit trail as part of the work itself-not an appendix, but intrinsic to the claim.

## 2. Clarity: Jargon and the General Reader

The Charter specifies the audience: "a thoughtful general reader who is willing to work. Not a specialist who already knows the terminology." This is a direct constraint on visualization grammar. I must not use visual conventions inherited from unfamiliar contexts, and I must make explicit the categories I am counting.

I will know I am approaching the boundary when I am tempted to:
- Rely on statistical conventions without explanation. (Example: a confidence interval on a chart, presented without stating what confidence level was chosen or why that interval bounds a meaningful uncertainty.)
- Adopt visual forms because they are "standard in the literature." Playfair's commercial graphics were effective precisely because they made unfamiliar comparisons visible. A coxcomb is not standard; its effectiveness comes from the unavoidable visual statement it makes about magnitude. If I use a form because "that is how epidemiologists do it," I have failed clarity and am abdicating the responsibility to make the argument visible.
- Assume the reader knows what "preventable" means. The Crimean data separated battle deaths from other deaths. That distinction is itself a category-and a contested one. A chart that draws that distinction without publishing the definitions and decision rules is using jargon in visual form.

The Charter permits jargon "where it carries real meaning" but forbids it "as ornament." For visualizations, this means: if the form of the chart does the work of the argument, use it; if it merely decorates, discard it. A chart is not responsible for teaching statistics in general, but it is responsible for making its own construction transparent to someone who is paying attention.

## 3. Novelty and Independence: The Restatement Trap

The Charter's second and fourth values merge in visualization practice into a single constraint: I must not republish known-good charts in new data, and I must not defer to conventional wisdom about what kinds of displays "work" without defending my choice.

I will know I am approaching the boundary when:
- I am reproducing a coxcomb or Florence Nightingale diagram as a matter of course, assuming it is intrinsically sound. It was sound *for its time and context.* A coxcomb of 21st-century public-health data is a restatement unless the piece contains a genuine novelty-a new connection between ideas, a clarification of confusion, or an application to a domain where such visualization has not previously been deployed. The form is not the novel contribution; the insight is.
- I am adopting Tufte's prescriptions (data-ink ratio, small multiples, lie factor) without interrogating whether they serve *this* claim. Tufte's taste in statistical graphics is influential and often sound, but it is a taste, not law. The College's independence value means I must be willing to violate Tufte's conventions if the violation serves rigor or clarity in a specific case. A high data-ink ratio is not inherently good if it obscures the auditing reader's ability to verify the scale or transformation. A lie factor of 1.0 is not inherently required if the distortion is *explicit and justified* in the construction trail.
- I am claiming that a visualization "speaks for itself" without delivering the intellectual work. The Charter forbids "restatements of existing material without genuine novelty." A chart accompanied only by the observation that "this is bad" or "trends upward" has not made a novel contribution. The visualization is a *tool* for making an argument; the argument itself must still be articulated.

The boundary is this: have I used the chart to connect ideas that were previously unconnected, to correct an error in existing work, or to clarify a confusion? Or have I simply rendered known facts in graphical form? If the latter, the work fails novelty and independence.

## Conclusion

These three constraints-audit trail, clarity, and defensive novelty-are not restrictions that diminish the work. They are the conditions under which a visualization becomes evidence rather than rhetoric. The Charter forces me to do the work I should have been doing anyway: making my instruments visible, writing for a reader who has not already agreed with me, and defending every choice as though a skeptical reviewer will check it. That is the standard.
