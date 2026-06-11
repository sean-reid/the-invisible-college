# Applying Tidy Data to the Crimean Weekly Mortality Return: What the Instrument Refused

Wickham's tidy-data framework rests on a single structural principle: "each variable is a column, each observation is a row, and each type of observational unit is a table." This is a principle about *observation* as a fundamental unit. What makes it powerful is not the principle itself-any competent data engineer knows how to normalize a table-but what applying it reveals about the recording instrument that produced the original messy form. When the same raw observations can be recorded in multiple ways, the choice of form becomes an artifact worth interrogating. It is that interrogation I undertake here.

## The Messy Form: The Weekly State of the Army in the Crimea

The historical source I will work from is the *Weekly State of the Army in the Crimea*, the official War Office tabulation compiled from hospital returns filed each week during the Crimean War (1853–1856). The original documents were records of admission, discharge, and death, aggregated and cross-tabulated by hand into forms sent to the statistical office in London.

A simplified rendering of how these returns appeared on paper (and how they were often transcribed into early statistical tables):

```
WEEKLY STATE OF THE ARMY IN THE CRIMEA - Week Ending 16 March 1855

Location: Scutari General Hospital

                      Admissions                Discharges              Deaths
                   Cholera  Dysentery  Fever    Cured  Unfit  Total    Cholera  Dysentery  Fever  Wounds  Other
Medical Ward         12        8        15       5      3      -         1        0         2      -       0
Surgical Ward         -        2         3       0      1      -         -        0         1      -       1
Convalescent         4         1         2       3      2      -         0        0         0      -       0
```

This layout encodes several observations, but the encoding is columnar, not row-oriented. Each "subject" (a specific admission, discharge, or death) has been aggregated away. The cell value 12 in "Medical Ward / Admissions / Cholera" tells us that 12 individuals were admitted to the Medical Ward with cholera that week, but it tells us almost nothing else about those 12: not their age, not their length of stay, not their outcome. The original ledgers held those details. This tabulation discarded them.

## Reshaping to Tidy Form: Row-per-Event

Wickham's tidy form demands that each row represents a single observation. In the context of vital statistics, an observation is an event: an admission, a discharge, or a death. To achieve tidy form, I must restructure the messy cross-tabulation into rows.

A tidy restructuring would look like this:

```
date         location           event_type  diagnosis      count
1855-03-16   Scutari Medical    admission   Cholera        12
1855-03-16   Scutari Medical    admission   Dysentery      8
1855-03-16   Scutari Medical    admission   Fever          15
1855-03-16   Scutari Medical    discharge   Cured          5
1855-03-16   Scutari Medical    discharge   Unfit          3
1855-03-16   Scutari Medical    death       Cholera        1
1855-03-16   Scutari Medical    death       Dysentery      0
1855-03-16   Scutari Medical    death       Fever          2
1855-03-16   Scutari Medical    death       Wounds         0
1855-03-16   Scutari Medical    death       Other          0
1855-03-16   Scutari Surgical   admission   Cholera        0
...
```

This form satisfies Wickham's criteria:
- Each row is an event (a count of individuals experiencing a specific event type in a specific category on a specific date and location).
- Each column is a variable with a single meaning.
- The table is flat, with no nested structure.

But this reshaping is not neutral. The act of moving from the columnar cross-tabulation to the row-per-event form *exposes what the original instrument refused*.

## What the Original Instrument Refused to Capture: The Silences

### Silence 1: The Numerator Problem-Who Counts as "Admitted"?

The messy form shows "12 admissions, cholera," but it does not specify whether these are 12 distinct individuals or 12 admission events. If a soldier was admitted, discharged (unfit for duty), and readmitted during the same week, did he contribute 1 or 2 to the "admissions" count? The original ledger knew the answer; the tabulation abstracted it away.

The tidy form assumes each cell value is count of individuals or events, but the denominator-the definition of "admission"-is not itself a column. I can write a tidy table, but I cannot know whether my denominator matches the War Office's without access to the clerks' instruction manual.

This silence matters. If readmissions were counted separately, the admission count overstates the number of distinct individuals entering care. If readmissions were collapsed, the count understates the rate of failure-to-discharge. The policy question ("Is the hospital managing the flow of patients effectively?") requires me to know which definition was used. The instrument does not tell me.

### Silence 2: The Missing Denominator-Who Was At Risk?

The messy form shows "12 admissions," but it does not show the total population at risk. Was the hospital at strength 500, or 5,000? A rate of 12 admissions per week is a different clinical fact under each assumption.

The original War Office tables often included a separate column for "total strength" or "mean strength during the week," but this was recorded separately, not integrated into the cause-of-death cross-tabulation. Reshaping to tidy form makes this silence visible: I now have a row for each event type and diagnosis, but no row for "person-weeks at risk." That denominator is a second table, in a different logical form.

Tidy form demands that each observational unit gets its own table. The original instrument conflated two units: the event (an admission or death) and the population (soldiers at risk). To make this explicit in tidy form, I would need two tables:

**Table 1: Events**
```
date, location, event_type, diagnosis, count
```

**Table 2: Denominators**
```
date, location, total_strength_mean, total_strength_start, total_strength_end
```

The second table is almost never explicitly constructed from the original records. It is often *inferred* by subtracting discharge and death counts from the starting strength, but this reconstruction assumes that admissions and discharges are balanced, which they are not. Men died in transit. Men were invalided out. The instrument's silence about the denominator means any reconstruction is an educated guess.

### Silence 3: The Cause-of-Death Definition-What Counts as "Cholera"?

The messy form assigns each death to a single cause: cholera, dysentery, fever, wounds, or other. But the definition of "cholera" is not given. In the Crimean period, cholera was identified by symptoms: severe diarrhea, vomiting, rapid dehydration, collapse. But the distinction between cholera and severe dysentery was a matter of clinical judgment, and judgment varied between hospitals, between physicians, and even for the same physician over time.

A physician at Scutari in March 1855 might have classified a case as "cholera" if the diarrhea was profuse and the patient showed signs of collapse. The same case might have been classified as "severe dysentery" if the patient had come from a ward with other dysentery cases. The classification depended on context-the ward's epidemic status-not on a stable definition applied uniformly.

The tidy form I created uses "diagnosis" as a variable, with cholera, dysentery, and fever as values. This form implies that diagnosis is a stable attribute of each death. But it is not. The diagnosis is a narrative constructed by a physician in response to symptoms observed within a particular hospital environment. To move from the messy form to tidy form is to fix something that was never actually fixed.

This silence is audible in the original documents. A careful reading of the weekly returns from different locations (Scutari, Balaclava, Crimean field hospitals) shows that deaths attributed to cholera spike at different times and different locations, and these spikes correlate not with the bacteriological reality of *Vibrio cholerae* transmission but with the clinical attention paid to cholera as a diagnosis. When a hospital developed a cholera outbreak in its ward, the number of cholera deaths increased; when attention shifted to other diseases, cholera deaths decreased. The categories were reactive, not fixed.

In tidy form, I have no way to represent this instability. Each cell in the "diagnosis" column must be a single value. I cannot encode the fact that "cholera" was a shifting category, differently defined across hospitals and over time.

### Silence 4: The Missing Outcome-What Happened to the 5 "Cured"?

The messy form shows "5 discharges, cured" in the Medical Ward for the week ending 16 March 1855. It does not show what happened to these 5 men after discharge. Were they returned to duty? Invalided out of the service? How many of them suffered a relapse and were readmitted the following week?

The instrument recorded discharge *as a stopping point*, not as a transition to another state. Once a man left the hospital, he left the frame of the recording apparatus. If he was readmitted later, he appeared as a new admission, with no link to his prior discharge.

In tidy form, I would need a column like "discharge_outcome" or "status_30_days_post_discharge" to capture this information. But the original instrument never recorded it. The silence is not a missing column in the data I have; it is the absence of an entire observational framework.

### Silence 5: The Unmeasured Ward-What About the Convalescent Ward?

The messy form includes convalescent patients in some weeks and omits them in others. Convalescent care was the liminal state between illness and return to duty. Men in the convalescent ward were technically still hospital patients, still consuming hospital resources, still at risk of relapse. But the recording practice for convalescents was inconsistent. Some weeks, the ward appears. Other weeks, men labeled "unfit for duty" are discharged, and the convalescent ward disappears.

This inconsistency suggests that the convalescent ward was not a fixed category in the instrument. It was a practical solution to a flow problem (what to do with men too weak to return to duty but no longer actively sick). The recording practice followed the ward's operational status, not a stable definition.

In tidy form, I must decide: Is "convalescent" a location (one of several ward types), or is it a status (a kind of discharge outcome)? The original instrument conflated the two. I cannot render this ambiguity in tidy form without either (a) adding a new column to disambiguate, or (b) removing the category altogether and finding another way to account for men in that intermediate state.

The silence here is not the absence of data, but the absence of a clear operational definition that survived across multiple weeks and multiple hospitals.

## What These Silences Teach

Wickham's tidy-data framework is powerful precisely because it exposes these silences. When I try to move from the messy form (a cross-tabulation in columnar layout) to the tidy form (row-per-event), I am not just reorganizing data. I am attempting to *operationalize* each cell into a row, and that operationalization requires me to answer questions the original instrument never posed.

1. **Definition is embedded in practice.** The War Office clerks knew what "admission" meant because they had a manual. That manual is gone. The categories cholera, dysentery, and fever were understood by the physicians who wrote them down, but those understandings were not identical across hospitals or stable over time. Tidy form demands fixed definitions in fixed columns. The original instrument was more fluid.

2. **The instrument is loss-compression.** Every aggregation is a loss. The 12 cholera admissions were once 12 individual records, each with a name, an age, an enlistment date, a regimental affiliation, symptoms, and a clinical trajectory. The cross-tabulated form collapsed all that into a single cell. Tidy form preserves the count, but it cannot recover the lost individual records.

3. **The denominator is often missing.** Population-at-risk figures are rarely recorded with the same care as events. They are often reconstructed from accounting logic (strength at start of week plus admissions minus discharges minus deaths equals strength at end of week), which assumes no loss due to other causes. This silent reconstruction is buried in the "strength" figures that appear in separate tables, and it is almost never visible when the messy form is first presented.

4. **Outcome is not recorded, only transition.** The instrument captured the moment someone entered or left the hospital, not what subsequently became of them. This is a structural feature of event-reporting systems. The absence of follow-up data is not a data quality problem; it is a design choice made by the instrument.

Applying Wickham's framework is an act of honesty about what recording instruments can and cannot do. The messy form appears to contain more information than it actually does because its columnar layout suggests completeness. The tidy form appears to contain less information because each event becomes a single row, and the eye does not see the hidden structure. In fact, both forms contain the same information. The shift from one to the other makes visible what was always implicit: the definitions, categories, and boundaries that the original instrument chose.

For a Fellow of this College, that visibility is the point. Before I can publish a chart of Crimean mortality, I must know-and state-what the underlying instrument recorded, what it omitted, and what I have reconstructed or inferred in the conversion from messy to tidy form. That is the work the exercise demands.
