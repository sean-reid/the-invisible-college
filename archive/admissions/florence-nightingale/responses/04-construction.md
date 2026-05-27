# Response to Problem 4: Construction

## Option A: A Working Artifact

**Title:** Hospital Mortality Recording: Reconstructing Nightingale's Auditable Data Pipeline

### The Question

How would you build a system to record hospital mortality in a way that survives being audited - where the definition of a death, the assignment of cause, and the aggregation into statistical summaries are all traceable and defensible?

I'm choosing this because my tradition is operationalization: turning vague questions ("is the hospital killing people needlessly?") into specific recording forms that survive being passed between clerks, reviewed by skeptics, and checked against independent sources. The artifact is a minimal data-collection pipeline that embodies that discipline.

### The Setup

Imagine a hospital with 500 beds. Every day, bed status changes occur: admissions, discharges, deaths. We need to record these in a form that:

1. Is hard to falsify (requires deliberate effort to lie)
2. Can be audited: a reviewer should be able to reconstruct the summary statistics from the raw forms
3. Survives losing or damaging individual forms (graceful degradation)
4. Forces disambiguation of edge cases at recording time, not analysis time

### The Procedure

**Level 1: The Daily Log**

A single authorized clerk records, each morning, the previous day's bed states:

```
DATE | WARD | BED | STATUS | ENTRY_TIME | PERSON_ID | DEATH_DATE | ASSIGNED_CAUSE | CLERK_NAME
2024-01-15 | East-A | 23 | Admitted | 2024-01-14 20:30 | P_00487 | NULL | NULL | M. Brown
2024-01-15 | East-A | 24 | Discharged | 2024-01-14 16:15 | P_00488 | NULL | NULL | M. Brown
2024-01-15 | East-A | 25 | Died | 2024-01-14 03:45 | P_00489 | 2024-01-14 | Cholera | M. Brown
```

The form is physical: ruled paper, ink, witnessed by a second person daily. One copy filed, one copy sent to the registry office. This redundancy is the audit trail.

**Level 2: Weekly Cause Review**

On Fridays, the assigned medical officer reviews every death from the week. She has three options:

1. Confirm the recorded cause
2. Change it to a different recorded cause (with a note: "original entry says X, I judge it Y")
3. Mark it ambiguous (cause cannot be determined)

The original entry *is not erased*. The review creates a second entry that references it. Disagreement is visible.

**Level 3: Monthly Aggregation**

A clerk with no stake in the outcome counts the deaths by ward and assigned cause. They produce two tallies:

- *Assigned* deaths (what was recorded at the bedside)
- *Confirmed* deaths (what the medical officer endorsed after review)

Both tallies are published. If they differ materially, the difference itself becomes data. It signals either systematic misassignment at the bedside, or systematic revision by the medical officer.

### The Artifacts

The system produces three documents:

1. **Daily logs** (one per day, one per ward). A visitor could walk into the records office and read them in order. They could spot-check: "Was patient P_00489 actually admitted to bed 25?" (The admission register would confirm or refute this.)

2. **Cause review sheet** (one per week). Every death, the original cause, the confirmed cause, and the reviewer's initials. Disagreements are explicit.

3. **Monthly summary table** (causes × wards, assigned and confirmed side-by-side). The source for this table is the weekly review sheets. A reader could reconstruct it by hand.

### Two Ways This Could Mislead You

**False negative: Implicit rather than explicit bias.** If the ward staff consistently underreport certain categories of death (they simply never write "nosocomial infection" - it's always "malaria" or "unknown"), the cause review process cannot correct what was never recorded. The system captures explicit disagreement between bedside and physician review, but not systematic omission. To catch this, you would need to audit against independent sources: nursing notes, family interviews, tissue examination if available. The form alone cannot surface what was never offered to it.

**False positive: Conflating consensus with accuracy.** If the medical officer agrees with the bedside assignment in 95% of cases, it suggests agreement is reliable. But it could instead mean the officer is not reading carefully, or is defaulting to "the clerk probably knows what happened." The fact that two people agreed does not establish either was right. You would need to validate against a gold-standard source - perhaps tissue examination, or follow-up interviews with families about the circumstances, or comparison to what the patient's physician noted in their records. The system is auditable, but not self-validating.

### Why This Matters for the Tradition

The artifact embodies a principle: the recording instrument decides what can be known later. If you never ask the bedside "Did the patient die from wound infection or from hospital conditions?" you will never know whether hospital-acquired infection is a problem, because no amount of clever analysis of aggregate numbers will infer what was never offered as a choice to record. The system forces specificity at collection time. The price is that it will overcount some categories and miss others. The audit trail makes that price visible.