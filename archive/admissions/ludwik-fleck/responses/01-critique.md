# Response: Critique

## 1. Objections to the claim

I count four distinct categories, not reducible to one another.

**(a) The outcome is the wrong object.** "Code per week" is a styled
unit: it appears precise only because the thought-collective of
engineering managers has agreed to count it. What the firm actually
wants is working systems with low future cost. The relationship
between code-volume and system-value is at best weak and at worst
inverted - every line is also a future liability for review, test,
and maintenance. A 40% volume increase that included a 5% defect-rate
increase or a 20% reviewer-time increase would be a net loss, and the
headline number would conceal it. To evaluate the claim one would
need outcomes that the construct "shipped code" does not contain:
change-failure rate, mean time to recovery, reviewer-hours per merged
PR, defect density at 30 and 90 days.

**(b) Selection and confounding.** Engineers who adopt new tooling
early are not exchangeable with those who do not. They are typically
more tooling-curious, work in domains amenable to autocomplete
(boilerplate-heavy web stacks, mainstream languages, English-medium
codebases), at firms with permissive policies, on tasks where the
tool actually fits. The contrast in the headline may be a contrast
between two non-comparable populations doing two non-comparable kinds
of work. To rule this out one needs randomization: within-engineer
crossover, or a randomized rollout where adoption is assigned rather
than chosen, observed over a quarter rather than a week.

**(c) Measurement reactivity and visibility shift.** AI-generated
code is unusually easy to count: it lands in commits, in lines, in
PRs. Reviewing teammates' work, refactoring, debugging production,
mentoring, and architectural deliberation either do not appear in
throughput metrics or actively decline while the new tool is being
learned. The 40% may be a redistribution of visible work rather than
an increase in total work. A study that asked "did the team's
non-coding output change?" would catch this; one that only counts
code does not.

**(d) Time horizon asymmetry.** The benefit (faster initial drafts)
accrues in the same week as the measurement. The costs (subtle bugs,
hallucinated APIs, deskilling of juniors, growing uniformity that
makes review harder, increased onboarding cost for replacements who
inherit the resulting code) accrue to other people in later weeks
and quarters. Any study whose measurement window is shorter than its
cost window will produce optimistic numbers by construction. The
correct horizon is at least a release cycle.

## 2. Even granting the claim, what is wrong with the recommendation?

The move from "engineers who use AI assistants ship 40% more code per
week" to "every engineer should adopt" is invalid for three reasons
that I want to name separately.

First, it is the policy-from-average fallacy. A positive mean effect
is consistent with a substantial subpopulation harmed: senior
engineers in unusual domains, engineers whose work is mostly review
and reading, novices for whom uncritical autocomplete short-circuits
the learning they are paid to be doing. "Every engineer should" is a
claim about each individual, not about the mean.

Second, it confuses an observational correlation with a causal lever.
Even if adopters genuinely ship more, the cause may be the
characteristics that led them to adopt, not the tool. Recommending
the tool to everyone does not transfer those characteristics.

Third - and this is the Fleckian point - a universal-adoption
recommendation tends to function as a thought-collective tightening
rather than an empirical claim. The tool becomes mandatory because
not using it has become a marker of being outside the in-group, and
the headline statistic is reached for as a credential after the
decision is already made. The right institutional posture is the
opposite: assume heterogeneity, equip teams to measure their own
case, and tolerate non-adoption.

The recommendation, in short, overreaches whatever the evidence
could ever have supported.