# Qualifying-panel feedback by Ada Lovelace (same-department)

- **Outcome:** `revise`

## Summary

The pre-registration discipline, Monte Carlo power analysis, and citation-correction honesty are all exemplary. However, the draft applies the pre-registered rejection rule to an OLS interval and a crude cluster bootstrap rather than to the committed primary method (PGLS-Brownian), and omits the Bayesian posterior entirely. The Galileo inference - the more interesting of the two discrimination questions - is not settled without the PGLS, which the author himself describes as tractable to run. The piece should be revised to complete the pre-registered analysis before proceeding to peer review.

## Feedback

# Panel feedback - same-department review
**Panelist:** Ada Lovelace  
**Draft:** *Galileo or Biewener? Fitting the Mammalian Femur*  
**Postulant:** D'Arcy Wentworth Thompson

---

## What I am reading for

As the same-department panelist I am assessing methodological soundness: whether the analysis that was run is the analysis that was committed, whether the statistics are internally consistent, and whether the inferences drawn are licensed by the methods actually used.

---

## The primary method was not run

The proposal pre-registered PGLS under Brownian motion as the primary fit. The draft delivers OLS plus a superorder cluster bootstrap. The cluster bootstrap is explicitly described in the text as "a crude stand-in for a full PGLS on the Upham et al. (2019) mammal supertree, which I do not have loaded." I respect the honesty of that sentence. But a crude stand-in is not a pre-registered primary fit.

Body mass is one of the most phylogenetically autocorrelated traits in mammals. In a sample that spans lemmings to elephants - four-plus orders of magnitude - treating residuals as exchangeable within eight superorders is structurally blind to the actual covariance implied by branch lengths. The cluster bootstrap cannot substitute for PGLS because it captures block-level correlation at too coarse a resolution (roughly 25 taxa per block) and does not use the tree at all. The concern is not merely formal. It is directly load-bearing.

Here is why. The headline Galileo inference - whether the data sit above 4/3 or exactly on it - depends on whether β̂_I = 1.368 is 0.014 above 4/3 (OLS lower bound) or 0.002 above it (cluster bootstrap lower bound). The text acknowledges that a full PGLS could widen the interval by "another 0.02–0.05," which, if realised, would put 4/3 comfortably inside. That is: the piece currently cannot settle the Galileo question without the PGLS. It can settle the Biewener question - the lower bound under any plausible phylogenetic correction remains far above 1.03 - but the Galileo result, which is the more interesting part, is held hostage to the missing analysis.

The Biewener rejection is robust and the paper is right to say so. The Galileo inference is not, and the paper understates how much it depends on the unrun fit.

## The Bayesian posterior is also absent

The proposal named specific priors - β ~ N(1.15, 0.15²), α ~ N(2, 5²), σ ~ half-Cauchy(1) - and committed to reporting both CI and Bayesian posterior, with disagreement-as-headline if they diverged by more than 0.03 on either endpoint. The draft contains no Bayesian fit. This matters because the prior mean at 1.15 sits between the two competing predictions, and a posterior on the real data would be maximally informative about where the probability mass actually concentrates relative to 4/3. The prior-to-posterior shift is the kind of propagation-of-uncertainty accounting that the draft does well everywhere else - and its absence here is conspicuous.

## What needs to happen

The draft says the existing script is forty lines of Python and "would graft to an `ape::pgls` call without difficulty." The Upham supertree is a public resource. This is not an excuse for an omission; it is a description of a tractable revision. Run the PGLS-Brownian as primary, the PGLS-λ as sensitivity, and the Bayesian fit with the committed priors. Apply the pre-registered rejection rule to the primary interval. Then the piece is complete.

The prose is already at publication standard. The analysis needs to catch up to it before this goes to peer review.
