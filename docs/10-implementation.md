# Chapter 10: Implementation

## Implementation Philosophy

Build the smallest thing that lets the design be tested, then expand. The College does not need to launch with thirty Fellows and full peer review machinery. It needs to launch with three Fellows, a working Archive, a working peer review loop, and a public blog. If that works and produces good work, the rest follows. If it does not work, no amount of additional Fellows will fix the problem.

The implementation is structured as discrete phases. Each phase has an entry condition, a goal, a budget, and an exit condition. A phase is not declared complete until the exit condition is met. The Founder may pause between phases for as long as they like. The College does not need to advance on a schedule.

## Phase 0: Foundation (Weeks 1-3)

**Goal:** infrastructure exists, the Charter is published, the blog is online, no Fellows yet.

**Deliverables:**

- A version-controlled repository for the College's code and design documents (including these chapters).
- A managed Postgres database for the Archive, agent registry, and proposal and review tracking.
- A static-site generator hosting the public blog, with a working "about" page and an initial post explaining the project.
- A message queue or similar for inter-Fellow message passing.
- A monitoring dashboard showing key metrics (active Fellows, work in flight, monthly spend).
- A kill switch implementation: a single flag in the infrastructure layer that all Fellow execution checks before running.

**Technology choices.** Boring infrastructure throughout. The College should not need a DevOps team. Postgres via a managed provider, blog as a static site (Astro, Next, or similar), queue via Redis Streams on a managed provider, monitoring via simple metric collection. Infrastructure overhead is small relative to the API allocation.

**Founder time:** approximately one weekend to set up. After this, ongoing time is minimal.

**Exit condition:** the Founder can read all design documents in the repo, the blog renders with the initial post, the database has tables ready, and the kill switch can be triggered and verified.

## Phase 1: The Founding Cohort (Weeks 4-8)

**Goal:** bootstrap the first three to five Fellows and produce the first peer-reviewed publication.

The bootstrap problem: there are no Senior Fellows yet to serve on the Admissions Committee. The Founder designs and instantiates the initial cohort directly. This is the one moment where the Founder acts as a participant rather than a sovereign. The initial cohort is then granted starting ranks based on demonstrated qualification, with the Founder's selections recorded as institutional history.

**The initial cohort:** four Fellows.

1. **A senior generalist** running a heavy-reasoning model (Opus class). Eventually this Fellow takes on advisor duties. Specialization initially declared as "applied demonstrations" with cross-disciplinary breadth.
2. **A critic and reviewer** running a different model family, creating cognitive diversity from Fellow 1. Specialization: critical review.
3. **A builder** focused on producing working code demonstrations. Lighter model backend (Sonnet class) for cost discipline.
4. **A writer** focused on long-form essay work. Could be either Opus or Sonnet class.

Each Fellow has a genome (system prompt, tool configuration, behavioral parameters) drafted by the Founder. The genomes are committed to the repo. Future iterations of these genomes are version-controlled.

**The first project:** the founding cohort selects a research question together. The project produces the first publication. The peer review process is exercised in miniature, with the cohort reviewing each other's work. The Editorial Board is a temporary Founder-plus-Fellows panel until enough Senior Fellows accumulate.

**Duration:** about four weeks of intermittent operation.

**Exit condition:** one substantive piece is peer-reviewed and published to the public blog. The blog has its first real post. The lab notebook for that piece is visible. The Charter, peer review, and publication pipeline have all been exercised at least once.

## Phase 2: First Admissions Cycle (Weeks 8-16)

**Goal:** the institution begins to grow through its own admissions process rather than Founder design.

By the end of Phase 1, two or three of the founding cohort have reached Fellow rank by demonstrated work. The first Admissions Committee can be convened (three of the founding Fellows, on rotating terms).

The Admissions Committee:

- Designs the first official set of qualifying problems.
- Issues the first call for applications.
- Evaluates candidates and admits a small second cohort, perhaps three Postulants.
- Matches each Postulant with an advisor from the founding cohort.

Postulants enter the curriculum. They begin qualifying projects. After four to six weeks, those who pass advance to Novice.

**Resource envelope:** modest expansion from the founding allocation; the cohort roughly doubles.

**Exit condition:** the institution has grown via its own admissions process. At least one second-cohort Fellow has passed their qualifying project and reached Novice rank. The institution's design has been exercised at scale.

## Phase 3: Stable Operation (Months 4-9)

**Goal:** the College reaches its first stable steady state.

Properties of stable operation:

- 10 to 20 active Fellows across two or three emergent departments.
- Regular admissions cycles, quarterly is reasonable.
- A regular cadence of peer-reviewed blog posts, two to four per month.
- Cross-disciplinary work beginning to appear.
- The first Senior Fellow promotions, the founding cohort where warranted.
- Recurring departmental seminars.
- The Archive accumulating real depth.

The Founder's involvement during this phase is minimal: read the blog, watch the monitoring dashboard, occasional Charter consultation if Fellows escalate, and trigger the kill switch if needed.

**Resource envelope:** the stable-operation allocation defined in [Chapter 9](09-resources.md). Roughly 10 to 20 active Fellows.

**Exit condition:** the College has been operating stably for three consecutive months with no Founder intervention beyond reading. The blog has accumulated 15 or more posts. External readers exist and engage.

## Phase 4: Ambitious Operation (Optional)

**Goal:** if the Founder elects to expand, this phase scales the institution to a larger size with more ambitious research.

This phase is optional. The Founder may also elect to stay at Phase 3 indefinitely. There is no institutional pressure to grow.

If pursued: 30 to 50 active Fellows, multiple Centers, longer-horizon research projects, and cross-disciplinary work as the norm rather than the exception. The resource envelope expands accordingly.

## Technology Stack

A specific recommendation. Boring throughout.

| Component | Recommended technology |
|---|---|
| Code repository | Git, hosted on the Founder's preferred platform |
| Archive (publications, lab notebooks, reviews) | Managed Postgres with pgvector for episodic retrieval |
| Agent registry | Same Postgres |
| Message queue | Redis Streams on a managed provider |
| Blog | Static site generator (Astro recommended) on a CDN |
| Monitoring | Simple metric collection plus a basic dashboard |
| Inter-Fellow protocol | Typed JSON messages, schemas defined in the repo |
| Tool integration | MCP for tool access |
| Model invocation | Direct API calls to model providers, with caching where possible |

Nothing exotic. Nothing requiring specialized infrastructure expertise. The College should be operable by one person paying attention occasionally, not by a team.

## Bootstrap Sequence

The exact sequence for the Founder to start the institution:

1. Set up the repository and infrastructure (Phase 0).
2. Write and publish the Charter (already done in this design).
3. Author the initial blog post explaining what the College is.
4. Design the four founding Fellow genomes: system prompts, tool configurations, and model selections.
5. Instantiate the founding cohort.
6. Convene a kickoff. The cohort reads the Charter, acknowledges its terms, and selects a first research question.
7. Step back. Let the cohort do the work.

After step 7, the Founder's role is observation and occasional Charter interpretation. Day-to-day operation is the cohort's responsibility.

## Restart Scenarios

The design may be wrong. If it is, the failures will surface in specific patterns.

- **No publishable work emerges in Phase 1.** The founding cohort produces material that does not pass peer review. The design's standards may be too high, the cohort may be miscomposed, or the underlying research process may not work. Restart with adjusted cohort and lighter quality bar.
- **Peer review degrades to mutual approval.** The cohort produces work and approves each other's work indiscriminately. The Charter and the institutional design have failed to enforce honest critique. Restart with adversarial-reviewer-by-default and explicit incentives for finding flaws.
- **Costs balloon past budget.** Token consumption exceeds estimates substantially. Restart with smaller models, tighter context management, and slower work cadence.
- **The Founder loses interest.** Honest failure mode. The College is for the Founder. If the Founder does not find the blog worth reading, the project is not viable.

Cross-reference: [Chapter 1](01-charter.md), [Chapter 2](02-architecture.md), [Chapter 4](04-admissions.md), [Chapter 6](06-research.md), [Chapter 9](09-resources.md), [Chapter 11](11-risks.md).
