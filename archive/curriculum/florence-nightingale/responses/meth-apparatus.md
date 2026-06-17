# Response: What the Apparatus Refuses to See

## Two-Sentence Disclosure Standard

The visualization I intend to publish in my qualifying project is a reconstruction of the Crimean War mortality coxcomb, adapted to weekly resolution rather than the original annual rendering.

**M** (the measurement procedure): A polar-area diagram in which wedges represent weeks in chronological sequence (radial axis: weeks 1–156 of the Crimean campaign), wedge width is constant (one week = one fixed angular slice), and wedge area is proportional to preventable deaths from disease, wounds, and other causes, aggregated from the Weekly State of the Army returns, with denominator fixed at average deployed strength per month to eliminate spurious rate changes from force-composition shifts.

**𝒜** (the alternative class): The competing explanations for variation in preventable-death counts across weeks-specifically: (i) changes in sanitation infrastructure (installed drains, ward ventilation, water-supply separation), (ii) changes in admission volume and case-mix composition (more/fewer surgical vs. medical admissions), (iii) seasonal or climate factors (temperature, humidity, disease seasonality), and (iv) measurement-instrument drift (changes in how ward clerks classified "preventable" vs. "battle" vs. "other" across the campaign).

**B(M; 𝒜)** (the blind set): The procedure is wholly blind to class (iv)-measurement-instrument drift in the classification scheme itself. If the War Office clerk at Scutari was more likely to code a septic wound-death as "preventable complication" in 1856 than 1854, no amount of empirical data from these same weekly returns can detect that drift; the procedure is reading from the same recording instrument and the definitions are what they are. The procedure is substantially blind to class (iii), because I have no independent temperature or disease-incidence data for Scutari, so seasonal patterns in the hospital admissions themselves become indistinguishable from seasonal patterns in lethality. It is moderately exposed to class (ii)-case-mix composition-because the denominator is monthly average strength, not weekly granular bed-census, so weeks with high admission surges are partially masked by weeks with discharges normalizing the denominator.

## Identification of Primary Blindness and Design Remedy

The procedure is **most exposed to a Type-3 procedural blindness**. The underlying data-the individual ward returns and death registers that feed the Weekly States-do contain information about measurement-instrument drift (class iv). A clerk's tendencies across weeks are recorded in the original ledgers if one manually audits the classification consistency of specific wound types. The coxcomb's aggregation to weekly totals and its dependence on the published state abstracts away the ledger-level audit trail. The procedure, as rendered, has chosen not to carry that information forward. 

The exposure to class (iv) is not *structural* (Type-1)-the data exists and distinguishes the alternatives-nor is it *asymptotic* (Type-2)-it is not a power problem solved by larger N. It is what the procedure *declines to look at*. The same is partly true for (ii): individual admission records by week and cause exist in the original returns; the monthly denominator is a chosen coarsening, not a measurement necessity.

**The design move that shrinks the blind set:** Publish alongside the coxcomb a secondary disclosure panel showing:

1. **Weekly admission counts and case-mix composition** (as a line plot or small-multiples by broad category: surgical, medical, dysentery), so the reader can see when case-load shifted and infer whether death-rate changes correlate with composition changes or are independent of them.

2. **A categorical-consistency audit**: sample 10–15 specific wound types from the original ledgers (e.g., "compound fracture with gangrene," "chronic diarrhea"), and report the proportion coded as "preventable" vs. "battle" vs. "other" for each cause, stratified by year. If the proportions drift, the blind set expands (the coxcomb becomes harder to interpret as pure lethality change); if they are stable, the procedure's responsiveness to real changes is stronger.

3. **The recording instrument itself**: publish the War Office's instruction to clerks defining "preventable," "battle," and "other," along with a note on when (if at all) those definitions changed during the campaign.

This design move accepts that a visualization cannot carry unlimited information-the coxcomb is a device for making mortality change *visible*, not for auditing classification consistency-but it treats the coxcomb as part of a composite argument. The coxcomb asks "did preventable deaths decline?" The admission-panel and consistency-audit answer "under what conditions of case-load and definition-stability does that question even make sense?" Together, they shrink the blind set from "Type-3 procedural blindness on classes (ii) and (iv)" to "residual Type-3 structural blindness only on seasonality (iii), which the reader now knows is present and can reason about."

The disclosure standard applied: *M* is a weekly polar-area diagram of preventable deaths, with area proportional to count and denominator fixed at monthly average strength. 𝒜 consists of four classes of competing explanations for variation: sanitation change, case-mix composition, seasonality, and classification-scheme drift. B(M; 𝒜) contains the entire classes (iii) and (iv) under M alone; these shrink to the margins once (ii) is made visible in an admission panel and (iv) is audited on a subsample of the ledgers.
