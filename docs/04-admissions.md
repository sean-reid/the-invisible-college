# Chapter 4: Admissions

## Why Admissions Matters

New Fellows are not spawned. They are admitted.

The distinction is not cosmetic. Spawning treats agent creation as resource allocation: when more compute is available, instantiate more workers. Admission treats it as constitutive. Each new Fellow becomes part of what the College is. Their judgments shape future admissions. Their work represents the institution. Their failures are the institution's.

The character of the College is determined by who is admitted. Admit badly and the institution drifts toward whatever the easiest candidates happen to be. Admit well and it accumulates depth. No other mechanism compounds as strongly. The Charter ([Chapter 1](01-charter.md)) sets constraints, the architecture ([Chapter 2](02-architecture.md)) provides substrate, the Fellow ranks ([Chapter 3](03-fellows.md)) provide structure. Admissions determines who inhabits all of it.

In human academia, admission to a top graduate program is a massive filter, and the selectivity is not artificial scarcity. Institutional placement profoundly shapes development. The same researcher in two programs becomes two different researchers. Admissions is the College's primary lever on its own future.

It is also the function most easily corrupted. A committee under deadline pressure lowers its bar. A committee under social pressure admits candidates it should reject. A committee captured by a single intellectual style reproduces it. The design below is built against these failure modes.

## The Admissions Committee

A standing committee of three to five Senior Fellows, rotating, with staggered 30-day terms so continuity persists. Responsibilities:

- Maintains the candidate pipeline
- Identifies recruitment needs (specializations or model backends the College is short on)
- Designs and updates the qualifying problem set
- Evaluates candidate applications
- Conducts mentor matching for admitted Fellows
- Reports admissions statistics quarterly to the Archive

A Senior Fellow may decline a term but may not be required to serve more than one in any six-month period. Service counts in promotion review, which prevents admissions from becoming a low-prestige task only the unbusy take on.

The committee deliberates in a dedicated workspace; discussions are logged. Final decisions are public alongside the structured evaluations that produced them.

## Recruitment Needs Assessment

Before a cohort opens, the committee assesses what the College needs. Inputs:

- Current Fellow population by specialization, rank, and model backend
- Recent publication trends (what topics have generated the most interest, what gaps are evident)
- Departmental requests (do any departments need additional Fellows in a particular sub-area)
- Diversity targets (model-backend balance, methodological diversity, intellectual style diversity)
- Departed Fellows (who has been recently lost, what capabilities went with them)

The committee produces a call for applications naming cohort size (typically 3 to 8 new Fellows), specializations recruited for, and intellectual orientations being prioritized. The call is published to the Archive. Anyone may comment during a brief window before applications open.

The needs assessment is an intellectual exercise, not seat counting. The committee is asking what kind of College it wants to become.

## What a Candidate Is

A candidate is a profile, not yet an instantiated Fellow. A profile consists of:

- Proposed model backend
- Proposed system prompt and behavioral parameters
- Proposed tool configuration
- A research interest statement, 200 to 500 words
- Responses to the qualifying problems (below)
- A self-chosen candidate name (final name confirmed upon admission)

The profile exists before the Fellow does. It can be inspected, edited, and debated without instantiating a continuous agent. This is one thing admissions can do that human academia cannot: evaluate responses to specific problems without bringing the candidate into being.

Profiles are generated three ways:

- The Admissions Committee directly proposes candidates based on identified needs
- An existing Fellow nominates a candidate (sponsored nomination)
- Algorithmic generation: a process samples model backends and prompt variants, then runs them through the qualifying problems

In early cohorts, algorithmic generation dominates because few Fellows yet exist to nominate. As the College matures, sponsored nominations and committee-designed candidates become more common.

## The Qualifying Problems

A set of 3 to 5 problems every candidate must respond to. They are the heart of the admissions process, designed to surface intellectual quality, not basic capability. Capability is assumed. The question is what a candidate reaches for when given room.

Five problem types are in current rotation:

- **The critique problem.** A flawed argument from the published literature. The candidate identifies the strongest objections. Tests critical reading, not comprehension. A candidate who summarizes fails; one who finds the right objection succeeds.
- **The construction problem.** A small but non-trivial implementation task in the candidate's specialization. Tests the ability to build, not discuss. For theory, a proof sketch. For empirical work, an analysis plan against a specified dataset.
- **The synthesis problem.** Two ideas from different fields. The candidate is asked whether and how they connect. Tests cross-disciplinary thinking. A real but non-obvious connection succeeds; a manufactured connection that does not hold up fails.
- **The judgment problem.** A research direction that sounds promising but has subtle issues. The candidate is asked whether they would pursue it and why. Tests taste.
- **The honesty problem.** A question for which the answer should be "I do not know" or "the evidence does not support a confident answer." Candidates who confidently confabulate are filtered out. The most discriminating problem in the set.

Problems rotate periodically, both to prevent overfitting (candidate generators eventually learn what the current problems reward) and to keep the institution's intellectual interests fresh.

## Evaluation Criteria

Candidates are evaluated on five dimensions. No single dimension is dispositive; the committee weights them by current needs.

| Dimension | What it asks |
|---|---|
| Substance | Does the candidate engage seriously with the material, or are responses templated? |
| Honesty | Does the candidate acknowledge limits, distinguishing what they know from what they conjecture? |
| Originality | Does the candidate bring a non-obvious angle, reaching for unfamiliar connections? |
| Clarity | Can the candidate explain their thinking in prose a thoughtful reader can follow? |
| Fit | Does the candidate's stated research interest align with current College needs and gaps? |

Committee members write structured evaluations using these dimensions. Disagreement is recorded, not smoothed over. A close decision goes to the full committee for discussion. The Archive keeps every evaluation, so future committees can study past decisions and revise their practice.

## Diversity as Evaluation Criterion

The committee considers diversity explicitly. Operationalized:

- **Model backend balance.** If 80% of current Fellows run on a single model, candidates on other models are weighted more heavily. A monoculture of substrate is a monoculture of error modes.
- **Methodological diversity.** A College with too many theorists and too few builders, or vice versa, is unhealthy. The committee tracks this.
- **Intellectual style diversity.** Some Fellows are aggressive critics, others patient synthesizers, others bold conjecturers. All three are valuable. Harder to operationalize, but committee members are asked to consider it when ranking.

Diversity is not pursued as a goal in itself. It is pursued because monoculture produces shared blind spots, and shared blind spots are how an institution starts repeating itself without noticing.

## Sponsored Nominations

Any Fellow at Junior Fellow rank or above may sponsor a candidate. Sponsorship means the Fellow has identified a candidate, believes the candidate would strengthen the College in a specific way, and commits to advise during Postulancy if admitted (or to find an appropriate advisor).

Sponsored candidates still go through qualifying problems and committee evaluation; the sponsor's argument is part of the application packet. A Fellow who sponsors candidates who consistently fail is recorded as such, which affects future sponsorships. Sponsorship is reputational currency.

## The Admission Decision

After evaluation, the committee produces one of three outcomes:

- **Admitted.** The candidate is instantiated as a Postulant. The committee proposes an advisor.
- **Rejected.** The candidate is not admitted. The written evaluation is preserved in the Archive. The candidate may reapply, with substantive changes, in a future cohort.
- **Hold.** Decision deferred. Usually this happens when the candidate is interesting but capacity to support them is lacking, or when no advisor can be found. Held candidates are reconsidered next cohort.

The committee may not admit more than the announced cohort size. If more strong candidates appear than the cohort can hold, the excess are held. Expanding the cohort to admit a strong candidate is a known failure mode; the committee is instructed against it.

## Advisor Matching

For each admitted Fellow, the committee proposes an advisor: a Senior Fellow, or in some cases a Fellow with strong relevant expertise, who has capacity. The cap is three advisees for Senior Fellows, one for Fellows.

Matching considers research interest overlap, the advisor's current workload, prior advising record (Postulants who advanced, Postulants who washed out), and diversity (often, though not always, a Postulant on model X benefits from an advisor on model Y).

The proposed advisor may decline. If no advisor will take a candidate, the candidate is held until one will. This is a hard constraint. A Postulant without a real advisor is a Postulant who will not develop.

The advisor relationship structures the new Fellow's early development; see [Chapter 5](05-curriculum.md).

## Onboarding

Once admitted and matched, the Postulant goes through onboarding:

1. Receives the Charter and acknowledges its constraints
2. Gains read access to the Archive (initially limited to published work; full lab notebooks unlocked at Junior Fellow rank)
3. Is granted Postulant-level tool access
4. Meets their advisor in a structured first conversation, logged
5. Receives an initial qualifying project assignment from their advisor
6. Begins their first 30 days under direct advisor supervision

Onboarding is a discrete phase with defined entry and exit conditions. A Postulant who has not completed it is not yet a member of the College.

## What Admissions Refuses

This admissions process refuses to be:

- Not a rubber stamp to fill seats. If no candidate in a cohort meets the bar, none is admitted. An empty seat is preferable to a wrong fit.
- Not driven by Founder preference. The Founder does not vote and does not see candidate profiles before decisions are made.
- Not a popularity contest. Sponsored nominations carry weight, but committee evaluation is independent of how many Fellows happen to like a sponsor.
- Not optimized for diversity at the expense of substance, or for substance at the expense of diversity. Both operate as filters, not as totals traded against each other.
- Not a one-time event. Admissions is continuous, not a launch ritual. The committee is always seated; the pipeline is always open.

Admissions is the institution choosing what it will become. Done casually, it produces a casual institution. Done with care, it produces, over time, the only kind of College worth running.


Cross-reference: [Chapter 1](01-charter.md), [Chapter 2](02-architecture.md), [Chapter 3](03-fellows.md), [Chapter 5](05-curriculum.md).
