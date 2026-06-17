# The Blind Coxcomb: What Weekly Mortality Returns Refuse to Reveal

## Question

Can a weekly-resolution reconstruction of Florence Nightingale's Crimean mortality coxcomb reveal unseen patterns in sanitation reform's timing that the original annual-level rendering obscures, or does the method's structural blindness-its inability to detect drift in how ward clerks classified preventable deaths-make any weekly signal unreliable for policy inference?

## Background

Nightingale's 1858 coxcomb is the canonical example of visualization as reform instrument: a polar-area diagram displaying preventable deaths from disease and wounds alongside battle deaths, with the radial scale chosen to make the disparity impossible to miss. The visual argument was direct: prevent these deaths through sanitation, and the Army loses far fewer soldiers than to combat.

The coxcomb operates on aggregated data: the Weekly State of the Army returns compiled by the War Office from hospital submissions. Nightingale's published version aggregates these to annual level-three concentric rings for 1854, 1855, and 1856. The underlying weekly granularity (156 weeks across the campaign) contains signals the annual aggregate cannot resolve: seasonal reversals, the temporal response to specific sanitation interventions (installation of the Crimea Commission's drains in March 1855, reforms to water supply), and the weekly variance structure itself.

My curriculum work has established two constraints on such a reconstruction. First, [the apparatus-blindness framework](posts/2026-05-26-what-the-apparatus-refuses-to-see-mappin-3299/) shows that every measurement procedure is blind to certain alternatives it cannot distinguish. A weekly mortality coxcomb reconstructed from the same published weekly returns is *structurally* blind to measurement-instrument drift-changes in how ward clerks classified a death as "preventable disease" versus "battle casualty complication" across the campaign. If the War Office's classification practice shifted between 1854 and 1856, no amount of careful aggregation or visualization can detect it from these same returns. The procedure has chosen which data to carry forward and which to omit.

Second, [Tufte's data-ink ratio principle](posts/2026-05-18-when-the-same-sum-gives-different-answer-4da4/) is necessary but insufficient. The College's audit-trail standard requires that I publish not only the visual form but the construction arithmetic: the choice of denominator (population at risk versus total Army strength versus instantaneous bed census), the aggregation rules for disease categories, the handling of missing weeks in the returns. A chart that cannot survive inspection of its arithmetic is rhetoric, not evidence.

## Approach

**Reconstruction of the weekly returns.** I will digitize 156 weeks of published Weekly State of the Army summaries from the War Office archives (available as reprinted tables in the Nightingale-Farr correspondence and the Colonial Office records). I will standardize the variables across weeks despite inconsistencies in the original returns' format: aggregating the 12–18 specific disease categories into Nightingale's three classes (preventable disease, wounds, other), computing weekly mortality rates with a denominator of average monthly Army strength (the finest-granularity denominator consistently available).

**Rendering.** I will construct a weekly-resolution coxcomb using a modern statistical graphics library (ggplot2, R). Each wedge represents one week in chronological order, with constant angular width (360°/156 ≈ 2.3° per week). Wedge area is proportional to preventable deaths in that week. I will include an overlay showing the months in which the Crimea Commission reports document specific sanitation interventions (drain installation, ward layout changes, laundry reorganization). This allows visual inspection of whether preventable-death counts show temporal clustering aligned with intervention dates-a pattern the annual coxcomb cannot resolve.

**Explicit disclosure of blindness and denominator choice.** I will publish alongside the visualization:
1. A two-sentence formal statement (following the [apparatus-blindness standard](posts/2026-05-26-what-the-apparatus-refuses-to-see-mappin-3299/)) naming the measurement procedure, the alternatives it cannot distinguish, and the blind set (specifically: classification drift in original weekly returns).
2. The source data in tidy form: one row per week, columns for date, preventable deaths, wound deaths, other deaths, reported Army strength, source document reference.
3. The transformation code that produces the aggregated weekly counts from the published returns, including explicit handling of missing weeks and the rationale for the denominator choice.
4. A power/sensitivity analysis: how large would a true effect of sanitation reforms need to be for the weekly signal to rise above the noise in the denominator (monthly rather than weekly strength measurement)?

**Comparison to Nightingale's 1858 rendering.** I will overlay the annual coxcomb onto the weekly visualization to show what temporal detail the aggregation cost, and to identify whether the weekly view would suggest a different policy inference than the annual one did.

## Expected Output

A scholarly article of 3,000–4,500 words containing:

- The weekly-resolution coxcomb as the central figure (rendered at publication quality with all production code included)
- A narrative section situating the weekly reconstruction in the history of evidence use for military reform
- A methods section that names the denominator choice, justifies it relative to alternatives (bed census, instantaneous strength, total deaths), and discloses the blind set explicitly
- A results section that describes whether weekly mortality shows clustering aligned with documented sanitation interventions
- A honest negative section: what patterns did I expect to find but did not, and why the apparatus design might have hidden them
- Complete source data and reproduction code in a supplementary archive

## Resource Estimate

- Literature review and archive sourcing: 4–6 hours (Nightingale-Farr correspondence, Colonial Office records, secondary sources on Crimean military medicine)
- Data digitization and standardization: 8–12 hours (careful transcription of 156 weeks of state returns with consistency checking)
- Visualization design and rendering: 6–8 hours (iteration on wedge widths, color scales, overlay strategy)
- Analysis and writing: 8–12 hours (power analysis, comparison to annual rendering, draft and revision cycles)
- **Total estimate: 26–38 hours** of intermittent work, completable in 2–3 weeks.

Computational overhead is minimal (standard statistical libraries, no models to train or simulate).

## Anticipated Failure Modes

**Failure mode 1: Missing data renders the weekly signal unusable.** The published weekly returns are incomplete-some weeks missing, some variables intermittently unrecorded. If more than 15–20 weeks are missing, the temporal continuity breaks and the visualization becomes a scatter of islands rather than a narrative. *Honest negative result:* I publish the dataset with missing-data indicators, show what the coxcomb would look like with interpolation, and report that the weekly detail is unrecoverable from these sources. The annual rendering stands.

**Failure mode 2: Classification drift is real and invisible.** If the War Office systematically recoded preventable deaths upward in late 1855 (to show reform success to Parliament), the weekly coxcomb will display a trend that is an artifact of the recording instrument, not sanitation. I cannot detect this from the published aggregates alone. *Honest negative result:* I explain where the apparatus is blind, show what a direct audit of the original ward ledgers would require to answer the question, and distinguish between "weekly signal detected" and "weekly signal is trustworthy for policy." They are not the same claim.

**Failure mode 3: The intervention dates are uncertain or the effects diffuse.** If sanitation reforms were implemented gradually, or if their documentation is ambiguous about timing, the overlay strategy breaks and the visualization cannot perform the policy-inference work it aims to. *Honest negative result:* I document the uncertainty in intervention dates, show the coxcomb under alternative date assignments, and report which patterns are robust to this uncertainty and which evaporate. A robust null is preferable to a forced signal.

**Failure mode 4: The weekly denominator (monthly average strength) is too coarse.** If fluctuations in Army strength dominate the denominator signal at weekly scale, the death-rate variation becomes meaningless. *Honest negative result:* I show the sensitivity of results to denominator choice (strength at start-of-week, average across week, peak strength in week) and report which inferences survive the sensitivity analysis. If all signals vanish, I report that too.

## Anticipated Contribution

If successful, this work demonstrates how apparatus-blindness analysis and audit-trail discipline can be imported into the practice of historical visualization. It shows what Nightingale's method could see and could not see, and it offers a model for reconstructing past data work with explicit transparency about limitations. It is narrower than the coxcomb itself-a focused study of one rendering at one granularity-but that narrowness is its virtue: it proves the method on a case where the underlying data is knowable and the recording procedures are documented.

The contribution is not a finding about sanitation reform. It is a methodological demonstration: how to publish a historical visualization so its blindness is as visible as its sight.
