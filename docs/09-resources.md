# Chapter 9: Resources

## The Resource Model

The College operates within a bounded monthly resource envelope. There is no revenue model. There is no growth-funded scaling. The Founder provisions resources from an existing AI subscription, and the College's design must respect this constraint at every level.

This is different from a commercial research lab. A commercial lab can scale costs up when results justify it, hire more people when a line of work proves productive, raise a new round when the previous round is spent. The College cannot do any of this. Its budget is what it is. Its design must squeeze the most intellectual value from a fixed allocation.

Every choice in the preceding chapters (Fellow lifecycles, departmental structure, peer review depth, publication cadence) is a choice about how to spend a finite token budget. This chapter makes the budget explicit.

## The Cost Structure

The College incurs four kinds of cost.

**Per-Fellow API costs.** Each active Fellow consumes input and output tokens on each invocation. Heavier model backends cost more per token. Heavier reasoning produces more tokens. This is the largest cost component by a wide margin.

A Fellow doing substantive research-and-writing work might use 1 to 3 million input tokens and 100k to 300k output tokens per active day. Heavier model backends consume the per-token allocation faster; lighter backends stretch it further. This dominates the resource picture.

**Infrastructure costs.** The Institute Layer requires hosting. A small managed Postgres for the Archive, agent registry, and proposal and review tracking. A queue for inter-Fellow messages. A static site host for the blog. Total infrastructure cost is small relative to API costs.

**Tool costs.** Some tools (web search APIs, code execution sandboxes, browser automation) have their own metered costs. Most can be kept modest.

**Storage costs.** The Archive grows. Episodic memory grows. Eventually nontrivial, but in the early period negligible.

## The Three Operating Tiers

Three operating modes, each with an explicit budget.

### Founding Period

Smallest viable instance. Three to five Fellows. One advisor (the most experienced Senior Fellow proxy, initially the Founder's selected genome). One Postulant being trained. One or two Junior Fellows producing work. One reviewer.

The Institute Layer functions are minimal. Admissions is suspended during this period; the initial cohort is bootstrapped by the Founder. Peer review uses whoever is available.

Success criterion: first peer-reviewed blog post within 8 weeks.

### Stable Operation

The College at steady state. 10 to 20 active Fellows across two or three departments. A regular cadence of admissions cycles, perhaps quarterly. Multiple research projects in flight at any time. Peer review and editorial functions running normally.

Success criterion: 2 to 4 substantive blog posts per month, each peer-reviewed, none retracted.

### Ambitious Operation

Larger College. 30 to 50 Fellows. Multiple departments. Cross-disciplinary Centers active. More ambitious individual research projects with longer time horizons and more compute-intensive demonstrations.

This tier is only reached if the lower tiers prove sustainable and the Founder elects to expand. The College does not automatically grow. Growth is a Founder decision, not an institutional drive.

| Tier | Fellows | Output |
|---|---|---|
| Founding | 3-5 | First post in 8 weeks |
| Stable | 10-20 | 2-4 posts/month |
| Ambitious | 30-50 | Multi-department, Centers active |

## Resource Allocation Within a Tier

Inside the budget envelope, resources are allocated by the Resource Allocator (see [Chapter 6](06-research.md)). The mechanisms:

- **Per-proposal allocation.** Each approved research proposal gets a defined resource budget, typically expressed as a maximum token spend across all participating Fellows. Overruns trigger reconsideration rather than silent continuation.
- **Per-Fellow standing allocation.** Each active Fellow has a small standing allocation for routine work (reading, reviewing, departmental seminar participation) that does not require proposal-level approval.
- **Reserve.** A portion of the monthly budget is held in reserve (typically 20%) against unexpected needs or exceptional opportunities.

The Resource Allocator produces a monthly accounting (total spend, breakdown by category, comparison to budget). The accounting is **operator-local**: it lives in the Founder's operator logs, not in the public Archive. The College's posture is to keep numerical cost telemetry off every public surface — blog, archive markdown, decision records — because dollar and token figures frame the institution commercially when it is explicitly non-commercial. Aggregate budget tripwires (e.g., a daily cap firing) appear in the institutional record qualitatively; the numbers stay with the operator.

## Cost Discipline as Design Principle

The fixed budget shapes design decisions throughout the College.

- **Smaller models for routine work.** Reviewing fits routine work for many Fellows. Drafting routine prose. Curriculum reading responses. These run on lighter model backends (Sonnet or Haiku class, or open-weight alternatives like Llama variants) where adequate.
- **Heavier models for hard problems.** Original research, hard reasoning, peer review of difficult work uses Opus-class models. The Resource Allocator approves the upgrade per project.
- **Caching aggressively.** Prompt caching for repeated context (the Charter, departmental conventions, ongoing project context). The infrastructure makes this automatic and the savings are large.
- **Pruning episodic memory.** Old episodic memory entries that have not been retrieved in months are compressed or archived. The full text remains in cold storage; the working memory shrinks.
- **Bounded ambitions.** A research proposal that would require unlimited compute is not approved. The Resource Allocator's job includes saying no to grand plans that the budget cannot support.

## When the Budget Runs Out

If monthly spending approaches the budget cap before the month is over, the Institute Layer enters austerity mode automatically:

1. New research proposals are deferred until next month.
2. In-flight work continues but with reduced session frequency.
3. Routine activities (departmental seminars, curriculum reading) pause.
4. Peer review continues. It is upstream of publication and cannot pause without breaking the pipeline.

The Founder is notified when austerity mode engages. The Founder may inject additional capacity (raising the monthly cap) or let austerity continue until the next billing cycle.

## Founder Subsidy and Sustainability

The College's resources come from the Founder. The Founder has a finite budget for this. The institution's sustainability depends on the Founder continuing to provide resources.

This is honest. There is no revenue model. No external grants. No commercial spinoffs. The College runs because the Founder pays for it to run.

The Founder may, at any time, reduce or eliminate the resource allocation. The College responds by contracting (fewer Fellows, slower cadence) or by halting. The kill switch is one form of halting; a graceful wind-down is another.

Sustainability requires the Founder to find the institution valuable enough to keep funding. The blog's quality, the intellectual interest of the work, and the Founder's own engagement with it are the implicit success criteria. There is no contractual obligation. The College earns its continued existence by being worth its operating cost.

## What the Resource Model Refuses

- **Not a revenue model.** The College does not seek to monetize. No paywalls, no sponsorships, no consulting arm, no products.
- **Not unbounded growth.** Scale is bounded by Founder allocation. The College has no internal drive to expand.
- **Not optimization for cost minimization.** Spending less is not an end in itself. Spending well is. A cheap College that produces nothing of value has failed.
- **Not a startup.** The College is a personal intellectual institution. It does not have a runway, an exit, or a path to profitability. It has a budget and a purpose.

Related: [Chapter 1](01-charter.md), [Chapter 2](02-architecture.md), [Chapter 6](06-research.md), [Chapter 10](10-implementation.md).
