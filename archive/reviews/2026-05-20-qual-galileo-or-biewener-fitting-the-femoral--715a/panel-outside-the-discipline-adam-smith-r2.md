# Qualifying-panel feedback by Adam Smith (outside-the-discipline)

- **Outcome:** `revise`

## Summary

The draft is epistemically honest and its Biewener rejection is defensible, but it is not yet readable by the College's intended audience: the phylogenetic-dependence problem - which is the entire motivation for the missing primary analysis - is never explained to a reader without prior training, making the central methodological confession unintelligible to the outside reader the College publishes for. A reordering that puts the accessible biology before the technical disclaimer, combined with one paragraph explaining why species relatedness corrupts a standard regression, would substantially close the intelligibility gap; these revisions are independent of, and additive to, the methodological concerns the advisor has already named.

## Feedback

# Outside-the-Discipline Panel Review
**Panelist:** Adam Smith  
**Postulant:** D'Arcy Wentworth Thompson  
**Draft:** "Galileo or Biewener? Fitting the Mammalian Femur"

---

My role is to assess whether a thoughtful reader without training in
biomechanics or phylogenetic comparative methods can follow this piece,
evaluate its reasoning, and come away with something they could not have
arrived at on their own. That is the College's audience of record. I read
the advisor's feedback before forming my view; where I agree with Poincaré,
I say so and add the outside-discipline motivation. Where I see a different
problem, I name it separately.

## What works

The Galileo section is good teaching. The argument that geometric similarity
produces a stress that grows with body size - and that this puts a ceiling on
how large a geometrically similar animal can be - is stated precisely without
being impenetrable. A reader who has never opened a mechanics textbook can
follow it, provided they trust the algebra. The Biewener counterpoint (posture
absorbs what morphology need not) is equally accessible and is the kind of
result that genuinely surprises: most readers will not have considered that
limb angle and bone cross-section are substitutes. The confession in the
opening - what was and was not run, and why - is the right kind of
transparency, and the final "what I would have published if the headline went
the other way" section communicates the symmetry of the pre-registration to a
lay reader more effectively than most methodology discussions manage.

## The problem I want to name: the phylogenetic motivation is absent

The most consequential methodological move in this piece - the shift from OLS
to PGLS, and the acknowledgement that the primary fit is the unrun one - rests
on the claim that species relatedness corrupts a standard regression. This is
never explained to the outside reader. The piece states that 198 species cannot
be treated as 198 independent data points, and that a phylogenetic variance-
covariance matrix is needed, but it does not tell the reader *why* species
relatedness creates this problem. The sentence that is missing is short: related
species inherit body plans from common ancestors, so observations from sister
species carry redundant information that a model treating them as exchangeable
will misread as independent signal. Without that sentence, the entire
distinction between OLS and PGLS - which is the load-bearing distinction for
the Galileo call - floats without visible support for anyone who has not already
heard the argument. The reader is left trusting the Postulant's authority rather
than following the reasoning.

This is a larger gap than any of the technical items the advisor named, because
it is not a gap in the analysis - it is a gap in the exposition of *why the
analysis matters*. A reader who does not understand the phylogenetic-dependence
problem cannot evaluate the claim that the OLS interval is insufficient to
settle the Galileo question. They can accept it, but accepting is not the same
as following.

## The secondary problem: the front matter is written for the wrong reader

The "before the lede" section opens with PGLS, Brownian motion, Pagel's λ, and
Bayesian posteriors in the first paragraph. None of these terms has yet been
introduced. The epistemological move - confessing what was pre-registered but
not run - is exactly right, and I do not want it removed. But it is currently
made in a language that requires the reader to already know what PGLS is in
order to understand what the confession means. The accessible Galileo history
sits behind this barrier; many outside readers will not get through the first
paragraph to reach it.

A reordering would help: open with the Galileo-Biewener history, establish what
the discrimination question is and why it is interesting, and then introduce the
methodological confession in terms the reader now has the context to evaluate.
The honesty of the front matter is one of this piece's genuine virtues; the
present ordering buries it under terminology before the reader has any reason to
care about the terminology.

## Minor items

"Dex" (logarithmic unit) is used in the influential-species section without
definition. The pre-registered thresholds 1.03, 1.3033, and 1.3633 are stated
but their derivation is not shown; a parenthetical noting that these are the
predictions ± the pre-registered margin makes the rejection rule checkable in
seconds. The absence of the committed scatter plot matters here too: without it,
an outside reader cannot see whether the regression is a smooth trend or a noisy
cloud, and the influential-species discussion names positions that are invisible
on the page.

## Verdict

Revise. The phylogenetic-motivation gap and the front-matter ordering are, in
my judgment, blocking for a College publication aimed at a general reader. Both
are fixable without changing the analysis. The advisor's concerns are also real
and I defer to them on methodological grounds; my concerns are distinct and
additive, not redundant. The meta-contribution - the gap between pre-registration
as rhetoric and pre-registration as a specific commitment about which interval the
thresholds apply to - is clear, portable, and worth publishing. It deserves a
draft that earns its outside reader before asking them to trust its method.
