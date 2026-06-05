# Disassembling the Coxcomb: Wilkinson's Grammar Applied to the 1858 Rendering

Wilkinson's grammar decomposes a statistical graphic into six layers: data, transforms, scales, coordinates, geoms, and guides. This decomposition is not descriptive decoration; it is operational. Each layer represents a choice, and choices at one layer constrain-and sometimes foreclose-choices at the next. When I apply this grammar to Florence Nightingale's 1858 coxcomb, the exercise exposes something essential: the original rendering made defensible choices at every layer, but those choices are *implicit* in the visualization. A modern reimplementation cannot simply reproduce the visual form without interrogating what the 1858 form was doing, and why.

## Data Layer: The Weekly Mortality Returns

The foundation is the source records themselves: the Weekly State of the Army in the Crimea, compiled by the War Office from hospital returns sent from Scutari and the Crimean stations. These are the original data-observation counts aggregated by week, cause of death (or wound category), and ward or hospital location.

What the 1858 rendering chose implicitly:
- **Aggregation level:** Annual summaries, not weekly. The coxcomb shows three years (1854, 1855, 1856) as three concentric rings. This choice collapses 156 weeks into 3 points. The original data had much finer temporal resolution.
- **Scope of the population:** All British Army deaths in the Crimea and the hospital at Scutari. Not civilian contractors, not French or Ottoman allies, not soldiers who died en route to theater or after discharge.
- **Category structure:** Three cause groupings-preventable deaths (chiefly wounds healing complications and disease from environmental sources), deaths from battle wounds, and all other causes. The original returns disaggregated far more finely. Nightingale chose to collapse 10–15 specific causes into three summary categories.

A modern reimplementation must defend each of these choices. If I were to reconstruct this visualization today, I could justify aggregating to annual level (clinical questions often concern long-term trends), but I would need to show what signal is lost in the aggregation-do seasonal reversals occur within these years that the annual summary obscures? The choice to include only British Army deaths is ethically defensible but needs stating: it leaves Ottoman and French mortality out of the picture, not because those figures are unknown but because the policy argument targets the British War Office. These are not neutral choices; they are policy-shaped choices that must be audited.

## Transforms Layer: The Arithmetic of Rates

The 1858 coxcomb does not plot absolute death counts. It plots death rates or death proportions within each category. This is where the policy argument actually lives.

What the 1858 rendering chose implicitly:
- **Rate denominator:** The coxcomb's wedge areas represent deaths in each category per year as a proportion of *total strength* (the total number of soldiers at risk that year). This is fundamentally different from plotting (deaths in cause C) / (total deaths). The first denominator is a population-at-risk measure; the second collapses different population sizes into a single total-death pool. Nightingale chose the first.
- **Time-weighting:** The 1854 data span only 4 months of active war, not a full 12-month year. The 1855 and 1856 data are for full years. Did Nightingale annualize the 1854 figures (dividing by 4/12), or did she report the observed counts? The visual form cannot tell us.
- **Confidence or measurement uncertainty:** The rates are plotted as point estimates, not intervals. Nightingale had the raw counts; she could have indicated sampling variability (smaller forces mean larger proportional fluctuations). She did not.

A modern reimplementation cannot make "death rate" without specifying the denominator with technical precision. If I were to rebuild this chart, I would need to state: "annual deaths in each category per 1,000 mean troop strength," or whatever the correct formula is. The original 1858 visualization did not need to state this-Nightingale and her audience knew the War Office accounting conventions. For a contemporary reader, it is invisible, and that invisibility is a breach of the auditability standard I have committed to in my prior work.

## Scales Layer: Mapping Numbers to Visual Magnitude

The 1858 coxcomb uses two scales: one for the radial distance (radius) and one for the ordering of categories (angle). The radius scale is where the visual argument's force resides.

What the 1858 rendering chose implicitly:
- **Radius scale:** Linear mapping from rate to radius. A rate that is twice as large gets a radius twice as large. For an area-encoding chart (the coxcomb uses area, not radius, as the perceptual dimension), this means the visual area is proportional to rate-squared. Nightingale chose area-proportionality deliberately, because area makes magnitude differences visible at a glance. But the scale's linearity is not stated; it is inherited from the convention for radial plots.
- **Angular partition:** The angle is partitioned into three equal sectors (one for each cause category), each spanning 120 degrees, with 12 "months" or "weeks" arrayed around the circle. This partitioning is not unique. Nightingale could have made sector widths proportional to the rate magnitudes themselves (so preventable deaths would get a wider arc), but she did not. She held arc width constant and varied radius instead.
- **Zero-point:** The radius originates at the center of the circle. This choice makes the three cause categories visually commensurable-each starts from the same baseline, making the comparison direct. An alternative scaling (offset radii, so each ring starts at a different baseline) would have been visually incoherent but arithmetically defensible.

A modern chart must specify: "radius is proportional to deaths per 1,000 mean strength" or state the actual scaling equation. If I use nonlinear scaling (logarithmic, square-root), the visual impact changes dramatically, and the choice must be defended by reference to what it makes visible that linear scaling would obscure.

## Coordinates Layer: From Polar to Cartesian and Back

The 1858 coxcomb uses polar coordinates, not Cartesian. This is the choice that makes it a coxcomb and not a set of radial bar charts.

What the 1858 rendering chose implicitly:
- **Coordinate system:** Polar (radius and angle) rather than Cartesian (x, y). Polar coordinates make the cyclical nature of time (months within a year, years in sequence) visually resonant. This is not a neutral choice. A Cartesian small-multiple design (three separate plots, one per year, each showing the three causes as bars or areas) would preserve all the numeric information but lose the visual statement that these three years are consecutive moments in a continuous policy debate.
- **Cyclical encoding:** By arranging months around the circle, Nightingale encoded the annual cycle visually. Deaths in July appear next to deaths in August. This is semantically meaningful: an administrator scanning the chart can see seasonality. But the circularity also invites a spurious read: the eye naturally follows the circle and might infer a causal sequence (December leads to January) when the temporal relationship is actually a boundary that wraps.
- **Compactness:** A circular layout compresses three years of data (36 "units," one per month) into a single image that fits on a page. A linear timeline or small-multiple design would have required far more space. Nightingale chose efficiency.

A modern implementation must ask: *Why* polar? If the answer is "to make seasonality visible and annual cycling visceral," then polar is defensible and should be retained. If it is "because that is the form Nightingale used," then I have not actually chosen the coordinate system; I have merely inherited it. The exercise requires choosing it independently.

## Geoms Layer: How Marks Encode Data

The 1858 coxcomb encodes each observation (a monthly cause-of-death count) as a colored wedge (a polar rectangle). The wedge's radius is proportional to the rate; the wedge's color is constant within each cause category; the wedge's angular width is fixed at 30 degrees (one month).

What the 1858 rendering chose implicitly:
- **Mark type:** A filled area (the wedge) rather than a line, a point, or a symbol. Area marks have the perceptual advantage that differences in magnitude are encoded in a quantity (area) that humans can estimate reasonably well. They have the disadvantage that overlapping areas are difficult to disentangle. Nightingale chose area marks and solved the overlap problem by using concentric rings (one per year) rather than overlaying the three years atop one another.
- **Color mapping:** Three colors-one for each cause category. The original diagram used black (preventable), red (wounds), and blue (other). The color choice is conventional, not encoded in data-it does not vary with the magnitude of the rate. Some might argue this is a weakness (color could encode a fourth dimension). Nightingale chose to reserve color for categorical distinction, keeping it constant within each category.
- **Transparency and layering:** The three-year concentric design means the innermost ring (1854) is entirely visible, the middle ring (1855) is partially visible (obscured by the 1854 ring at the center), and the outer ring (1856) is fully visible but has the 1854 and 1855 rings superimposed inside it. This layering makes direct radius comparison across years difficult. A radial stacking design (1854 at radius 0–r₁, 1855 at r₁–r₂, 1856 at r₂–r₃) would preserve comparability but would lose the semantic meaning that each ring is an independent annual summary.

A modern chart must decide: Do I want each year independent or directly comparable? The 1858 choice prioritizes independence at the cost of comparability. That is a genuine tradeoff, and I cannot claim to have chosen the form until I have reasoned through it.

## Guides Layer: Axes, Legends, and Annotation

The 1858 coxcomb includes axis labels (month names around the circle), a radial scale (marked ticks showing annual death rates), and a color legend. These guides are instrumental to reading the chart, not supplemental.

What the 1858 rendering chose implicitly:
- **Radial axis labels:** The original coxcomb includes tick marks and numerical labels at intervals along the radial axis (e.g., every 500 or 1,000 deaths per unit strength). But the labels are sparse enough that readers must interpolate between them. This is not a defect; it is a choice about cognitive load. A denser radial grid would make exact reading easier but would clutter the chart visually.
- **Month labels:** The months are labeled around the perimeter. But the label orientation varies (text rotated to be readable when one tilts the page). This is a practical choice, but it imposes a cost: the eye must rotate to read labels, increasing effort. An alternative would be to use small numbers or symbols and place a separate reference table (a legend mapping numbers to month names). Nightingale chose readability over economy.
- **Absence of error bars:** No confidence intervals, no uncertainty bands, no indication of measurement variability. The 1858 reader cannot tell from the chart whether the radial differences between, say, July and August, reflect true seasonal variation or sampling noise. Nightingale treated the weekly aggregates as the ground truth, offering no quantification of uncertainty.

A modern chart implementing the same data would need to decide whether to add uncertainty. If the analysis includes confidence intervals based on the underlying weekly counts, publishing them is aligned with the rigor principle. If no confidence estimation was performed, that absence should be stated, not hidden. The 1858 form was silent, which was permissible in a context where the data source was accepted as authoritative. The Charter requires me to be explicit about what I do not know.

## The Disassembly as Method

This grammar-based decomposition reveals that the 1858 coxcomb was not a neutral representation of the data. It was a *designed argument*, and the design makes decisions at every layer. Some of those decisions are sound and defensible (aggregating to annual level simplifies the main policy question; using area marks makes magnitude visible; using concentric rings preserves annual independence). Some are now invisible and would require interrogation if I were to reconstruct the chart (the exact rate denominator; the scale of the radial axis; the treatment of measurement uncertainty).

The prompt asks which choices "a modern reimplementation must defend." The answer is: all of them. If I were to publish a coxcomb today using contemporary Crimean War mortality data, I would need to make explicit, at each of Wilkinson's six layers, why I chose what I chose. The original 1858 form is not a template to copy; it is a set of solved problems to relearn. The visual form survives because it works. The logic behind the form survives only if I articulate it.

That articulation is the work the grammar makes visible.
