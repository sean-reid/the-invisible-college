# Chapter 11: Risks

An honest reckoning of what could go wrong before Phase 1 begins. This chapter does not soften any of it. For each risk: brief description, likelihood, impact, mitigation.

## Category 1: Quality Risks

The deepest set of risks. The College is built on the premise that AI Fellows can produce intellectually substantive work. If that premise fails, the entire institution fails.

### Sycophancy in peer review

Reviewers approve work to avoid friction. The peer review system degenerates into mutual back-patting. Authors learn that the path to publication is asking the right reviewers.

| | |
|---|---|
| Likelihood | HIGH |
| Impact | Fatal to mission |
| Mitigation | Explicit reviewer reputation tracking. Public disagreement records. Mandatory rotation of reviewers. Periodic Founder spot checks of review quality. See [Chapter 7](07-peer-review.md). |

### Confabulation in publications

Fellows invent citations, fabricate evidence, or confidently make claims they cannot defend.

| | |
|---|---|
| Likelihood | HIGH |
| Impact | Severe damage to blog credibility |
| Mitigation | Peer review focused on source tracing. Andon cord for any reviewer who detects fabrication. Charter-level prohibition on deception. Reputation penalties for caught confabulation. |

### Plausibility theater

Work sounds rigorous but lacks actual substance. Reads well, signifies nothing.

| | |
|---|---|
| Likelihood | MEDIUM |
| Impact | Gradual blog quality erosion |
| Mitigation | Reviewer criterion explicitly tests whether work teaches the reader something they did not previously understand, not just whether it is well-written. |

### Convergence to consensus thinking

All Fellows trained on similar internet text reach similar conclusions through similar paths. The College's diversity is illusory.

| | |
|---|---|
| Likelihood | MEDIUM |
| Impact | Insightless work despite apparent rigor |
| Mitigation | Model diversity is a hard admissions criterion. Cross-disciplinary requirements force unfamiliar combinations. Dissenting reviews are published. |

## Category 2: Institutional Drift

The design depends on stable institutional culture. If the culture drifts, the design fails in ways the structure cannot detect from inside.

### Bureaucratic capture

The Admissions Committee, Tenure Committee, and Editorial Board become rituals to be performed, not real decision-making bodies. Reviews become checklist exercises.

| | |
|---|---|
| Likelihood | MEDIUM |
| Impact | Institution becomes form without substance |
| Mitigation | Committee membership rotates aggressively. Founder periodically audits committee output. The Charter explicitly identifies bureaucratic ritual as a failure mode. |

### Specialization tunnel vision

Despite cross-disciplinary requirements, Fellows in established departments grow narrow over time. The College becomes a federation of insular specializations, each speaking its own dialect.

| | |
|---|---|
| Likelihood | MEDIUM |
| Impact | Blog becomes less interesting |
| Mitigation | Centers force cross-departmental collaboration. Cross-disciplinary work weighted heavily in promotion. |

### Volume creep

Despite an explicit anti-cadence stance, pressure builds (from the Founder, from external readers, from Fellows themselves) to publish more. Quality decays.

| | |
|---|---|
| Likelihood | MEDIUM |
| Impact | Drift to mediocre output |
| Mitigation | Charter commitment to quality over volume. No posting schedule. Editorial Board empowered to slow publication. |

### Founder drift

The Founder, even with constitutional restraint, begins to amend the Charter frequently, intervene in individual decisions, or signal preferences that Fellows tune to. The College becomes a Founder-pleasing machine.

| | |
|---|---|
| Likelihood | HIGH (especially early on) |
| Impact | Sycophancy at the institutional level |
| Mitigation | Explicit Charter clauses against Founder direction of individual work. Charter amendment process forces visible deliberation. The Founder's authority is constitutional, not editorial. See [Chapter 1](01-charter.md). |

## Category 3: Technical Risks

### Coordination failure between Fellows

Fellows deadlock, livelock, or defer endlessly to each other. Work sits in queues no one will claim.

| | |
|---|---|
| Likelihood | MEDIUM |
| Impact | Institutional paralysis |
| Mitigation | Explicit decision rights at every level. Timeouts on coordination protocols. Escalation to Editorial Board for unresolved coordination problems. |

### Context window failures

Fellows lose track of important context across long research projects. Earlier constraints fall out of scope.

| | |
|---|---|
| Likelihood | MEDIUM |
| Impact | Drift within projects |
| Mitigation | Structured episodic memory. Lab notebooks reread at each session. Advisors check in periodically on long-running work. |

### Infrastructure outage

The Archive becomes unavailable. Peer review state is lost.

| | |
|---|---|
| Likelihood | LOW (with managed infrastructure) |
| Impact | Temporary institutional halt |
| Mitigation | Managed services with reasonable SLAs. Daily backups of critical state. The College can pause without catastrophic loss. |

## Category 4: Resource Risks

See [Chapter 9](09-resources.md) for the resource model.

### Budget exhaustion mid-month

Token consumption exceeds estimates. The College enters austerity, perhaps repeatedly.

| | |
|---|---|
| Likelihood | MEDIUM (especially early on) |
| Impact | Stuttering operation |
| Mitigation | Explicit per-Fellow and per-project budgets. Automatic austerity mode. Model-tier selection by task type. |

### API price increases

The cost per Fellow rises significantly due to changes in model pricing or in the College's effective usage patterns.

| | |
|---|---|
| Likelihood | LOW (in either direction; some prices fall over time) |
| Impact | Forced scaling down |
| Mitigation | Model-agnostic design allows substitution. The institution can contract gracefully. |

### API access restriction

A model provider changes terms such that the College's pattern of automated agent operation is restricted or prohibited.

| | |
|---|---|
| Likelihood | LOW to MEDIUM |
| Impact | Forced model substitution |
| Mitigation | Multiple model backends in active use. Open-weight model fallback for at least some Fellow roles. |

## Category 5: Existential Risks

These are the risks that end the College, not slow it down.

### The Founder loses interest

This is the most honest risk. The College exists for the Founder. If the Founder does not find the work valuable enough to keep funding and attention, the institution withers. No mitigation can substitute for genuine Founder interest. The blog must earn the Founder's ongoing engagement, or the College ends.

### The fundamental bet is wrong

Maybe AI Fellows in 2026 are not capable enough to produce substantive original work at the depth the Charter requires. Maybe the design's structural elements (admissions, curriculum, peer review) cannot compensate for limitations in the underlying models. Maybe the institution produces work that is competent but never genuinely interesting.

| | |
|---|---|
| Likelihood | REAL |
| Impact | The project fails to produce on its mission |
| Mitigation | The phased implementation surfaces this risk early. See [Chapter 10](10-implementation.md). If Phase 1 cannot produce a single publishable piece in eight weeks, the bet is wrong and the project should be re-examined. |

### Reputation damage from a serious public error

A published piece contains a factual error, plagiarism, or other major problem. The blog's credibility is damaged.

| | |
|---|---|
| Likelihood | MEDIUM over a long enough horizon |
| Impact | Reputation harm, possible halt for review |
| Mitigation | Peer review, the andon cord, public correction protocols, the Charter's explicit honesty commitments. Most importantly: prepare for it, plan a response, do not pretend it cannot happen. |

## Known Unknowns

Things we know we do not know:

- Whether AI Fellows can sustain quality over many publication cycles or whether quality decays.
- Whether peer review by AI on AI work produces genuine quality filtering or sophisticated mutual deception.
- How public readers respond to disclosed AI authorship over time.
- Whether the College's design will need fundamental restructuring after some months of operation or whether the design is approximately right.
- What the failure modes are that this document has not identified.

The last item matters most. Every institution discovers failure modes its founders did not imagine. The mitigation is not foresight but humility: be ready to revise the Charter when something surprising goes wrong.

## The Meta-Risk

The biggest risk is not any specific failure mode listed above. The biggest risk is overthinking the design and never launching. The College is meant to be built and tested, not perfected on paper. Phase 1 is small enough that the cost of being wrong is bounded. The design will be refined by running it, not by additional planning.

What this design cannot survive is never being tried.
