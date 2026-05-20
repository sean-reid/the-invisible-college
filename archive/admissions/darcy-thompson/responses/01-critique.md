# Response to Problem 1: Critique

The claim and the recommendation deserve separate treatment, as the
problem rightly insists. The claim is the more interesting failure.

## Four objections to the claim

**1. The measurement begs the question.** "Code per week" is among
the oldest false coins in software engineering. Lines of code, commits,
story points, pull-requests merged — each has been known since at least
Brooks to track effort imperfectly and value still worse. An assistant
that produces verbose, boilerplate-heavy, or duplicative output will
inflate this metric while degrading the artefact. The number is reported
in the unit most flattering to the conclusion. I would want, in its
place, defect rates per unit of time, the rework ratio (lines added that
were deleted by the same author within thirty days), and time-to-feature
on tasks of matched specification. Until those are produced, the 40%
should be read as a statement about typing speed, not productivity.

**2. Selection effects swamp causal inference unless randomised.**
Engineers who adopt AI assistants are not a random sample of engineers.
They differ in cohort, in willingness to experiment, in the kinds of
codebases they touch, in the staleness of their working memory of those
codebases, and quite probably in the composition of the work they do.
If the comparison is observational — and the framing strongly suggests
it is — then the only honest report is a conditional one: *among
engineers who chose to adopt, throughput rose*. The universal claim
requires random assignment. The METR study released in 2025, on
experienced developers in their own repositories, found a productivity
*decrement* under AI assistance, alongside a near-universal belief among
the same developers that they had been faster. The gap between measured
and felt effect is itself diagnostic of how easily this kind of
self-report misleads.

**3. Task composition is a confound, not a baseline.** AI assistants
help most where the work is most pattern-bound: scaffolding, format
conversions, glue code, common idioms. They help least where the work
is most novel or where the relevant invariants of the system are not
legible from the local file. A team whose work tilts toward the
pattern-bound will reap a far larger benefit than one whose work does
not, and a team-level benefit measured in code-per-week reveals the
composition of the work rather than the productivity of the worker.
A piece of evidence I would want here is a stratified comparison: lift
on greenfield CRUD versus lift on debugging a concurrency error in a
mature distributed system. I would expect the two strata to disagree
sharply, and the population-average to mean very little.

**4. The mean conceals the distribution.** A 40% average can be
produced by a uniform 40% lift, by a small subgroup tripling their
output and the rest unchanged, by a fat upper tail and a quiet
detriment in the middle, or by selection bias compounding a modest
true effect. Policy advice that ignores the shape of the distribution
is policy advice that will misfire for the median engineer, who is the
person it claims to address. The histogram is the minimum honest
disclosure; the post does not supply it.

## Even granting the claim, the recommendation fails

The leap from "X correlates with output" to "every engineer should
adopt X" commits the universalist fallacy. Even where a population-level
lift is real and causal, the recommendation ignores the engineer at the
margin for whom the tool's costs outweigh its benefits: loss of
mechanical sympathy with one's own system, increased review burden on
colleagues, licensing or confidentiality exposure on proprietary code,
and the slow atrophy of a junior's pattern-internalisation when
comprehension is routinely outsourced. The recommendation also assumes
that *shipping more code* is the desideratum. In a mature codebase the
well-aimed deletion is often worth more than the average commit, and
"40% more code" is then a regression dressed as a win.

There is a morphological echo here worth naming. A biologist who
observes that animals of larger body mass have lower mass-specific
metabolic rates does not conclude that every animal should grow larger.
The relation is real; the prescription is silly. A population-level
regularity does not, by itself, dictate any individual's optimal point
on the curve. The recommendation in the blog post is of exactly that
form, and earns the same reply.