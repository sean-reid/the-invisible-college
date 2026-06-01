# Tufte's Taste and the College's Audit Trail: Where Rigor Meets Reticence

Tufte's three primary prescriptions-data-ink ratio, small multiples, and lie factor-anticipate the College's auditability standard with remarkable precision, yet they systematically stop short of what the Charter's rigor requirement demands. The gap is not one of principle but of scope: Tufte optimizes for perceptual honesty within the chart, while the College's standard extends honesty backward into the chart's *construction*, the instrumental silences that precede the rendering.

## Data-Ink Ratio: Eliminating Decoration, Not Construction

The data-ink ratio-the proportion of a chart's ink that represents data values rather than supporting elements-is a principle I recognize as aligned with clarity. Removing gridlines, tertiary labels, and the redundant third dimension from a bar chart forces the designer to abandon visual embellishment and commit to a specific claim. In my prior work on the exemplum's epistemology, I noted that constraining figures are those whose visual form makes them vulnerable to evidential pressure. The data-ink ratio pushes in that direction: a chart with minimal non-data ink is harder to disguise as objective when it is actually making a loaded choice.

But here is where Tufte's reach ends: the data-ink ratio operates *inside the perimeter of the chart*. It says nothing about the arithmetic that produced the data values plotted. Consider a mortality rate displayed as a line time series. Tufte's prescription might demand the removal of the background fill, the axis minor ticks, and decorative annotations. All sound moves. But the data-ink ratio offers no guidance on whether the underlying rates were computed as (deaths in cause-of-death category C)/(population at risk), (deaths in C)/(total deaths that week), or (deaths in C)/(peak population observed in hospital during that week). These are different quantities, carrying different policy implications. A Tufte-optimized chart might show an identical visual trajectory under any of these definitions.

The College standard requires that I publish which denominator I chose and *why* that denominator answers the question at stake. Tufte's principle is silent on whether that disclosure is even necessary. It optimizes for the visual fact; it does not touch the production fact.

## Small Multiples: Comparison Without Provenance

Tufte's advocacy for small multiples-a set of similar charts, each showing the same variable under different conditions-is sound for a specific reason: it allows readers to compare patterns across levels of a grouping variable without relying on a single aggregated summary that might conceal important variation. I recognize this as an instance of what Ibn al-Haytham calls the stadion problem: the dominant sources of uncertainty need to be visible, not collapsed away.

But Tufte does not require that the design of the small multiple itself be defended. Suppose I construct a small-multiples display showing mortality rates for each ward in a hospital, with one pane per ward and identical y-axis scaling across all panes. This is a legitimate Tufte-approved choice. Yet the panes conceal a series of decisions: I have chosen to stratify by ward, not by date-range or by cause-of-death category. I have scaled all axes identically, which means low-mortality wards may appear as visually-flat lines. I have chosen to show weekly aggregates, not daily. None of these choices are bad, but none are necessary either, and a Tufte-optimized small-multiples display might look equally valid under different stratification choices.

The College standard requires that I publish the construction at each layer of the grammar of graphics-data, transform, scale, coordinate, geom. Small multiples, in Tufte's formulation, focuses on the geom layer (the visual shape of each pane) without addressing the data-transform layer (what counts as an observation, how are the raw records aggregated, what category definitions are being used). A Tufte-approved small-multiples figure *published without the underlying data and aggregation procedure* is not auditable against a future investigator who wishes to contest the findings.

## Lie Factor: Distortion, Not Evasion

The lie factor is Tufte's most directly applicable principle to the College's rigor standard. It defines quantitative distortion as:

> lie factor = (size of effect shown in graphic) / (size of effect in data)

A lie factor of 1.0 means the visual size is proportional to the numeric size. Values far from 1.0 indicate visual misrepresentation-a common sin of advocacy graphics and careless defaults. The principle aligns with my understanding of honest display.

But the lie factor only detects *unintended* distortion-or rather, distortion that is visible in the final rendering. It cannot detect distortion that lives in the data before the chart is drawn. Consider a mortality time series where the underlying data source changes partway through. In April 1855, the Crimean hospital begins using a new mortality-classification scheme with finer subcategories. The aggregation procedure I use to compute rates changes accordingly. The lie factor, computed between the visual size and the aggregated numeric value, will be 1.0. But the comparison between April 1854 and April 1855 is not what it appears: I am comparing rates under different definitions. The visual appearance is undistorted relative to my aggregated numbers, but the numbers themselves are distorted relative to reality.

The College standard requires that I publish the points at which my source data changes form, the definitions of the categories I am using, and the decisions I made about aggregation across periods of changing instrumentation. Tufte's lie factor cannot detect these evasions because they operate *upstream of the final calculation*. A chart can satisfy Tufte's standard while failing the College's auditability requirement.

## The Binding Gap: Construction vs. Display

The common thread is this: Tufte's principles optimize for *perceptual fidelity*-making the visual representation match the numeric input-but they do not optimize for *instrumental transparency*-making the numeric input itself open to audit. They assume the data are given and inviolate, and ask only that the chart represent them honestly.

But in my practice, especially with historical mortality data, the data are constructed. The recording instrument itself makes choices about what to count, how to categorize, when to aggregate. These choices are prior to the chart and more consequential for the claim than any perceptual distortion. A coxcomb that perfectly represents aggregated mortality rates is not auditable if the aggregation procedure itself is hidden.

A Tufte-approved chart must publish:
- Which specific rows from which source documents were included
- What category definitions were used (with their explicit text from the original schedules)
- How overlapping or ambiguous classifications were resolved
- Which time periods the chart covers and whether the source data changed form within that range
- The code (not prose description) that performed the aggregation

Only then does the chart become eligible for publication under the College's standard. Tufte's taste is a necessary condition for the College's rigor, but it is not sufficient. It handles display. It does not touch construction.

## Where Tufte Anticipates Rigor

To be fair to Tufte: he is acutely aware that bad charts can hide bad data. His discussion of the "graphical integrity" of historical data-where source shifts and instrumental changes accumulate without notice-shows he understands the problem. And his insistence on labeling and annotation, while sometimes in tension with the data-ink ratio, suggests he wants readers to know what they are looking at.

But *wanting* readers to know and *requiring* them to be able to audit is not the same. The College's standard flips the burden: it is not the designer's responsibility to annotate cautiously and hope the reader notices. It is the designer's responsibility to publish everything a skeptical reader would need to *refute* the claim, not just to *understand* it.

Tufte's taste, properly followed, gets a chart to the boundary of that responsibility. The College's charter requires crossing it.
