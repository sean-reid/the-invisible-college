# Response: The Stadion in Behavioral Science — Auditing Dunbar's 150

## The Formula

Dunbar's 150 is not a field observation. It is a regression extrapolation. The claim originates in Dunbar (1992), where a regression of log mean group size on log neocortex ratio across 36 primate genera was used to predict the "natural" social group size for *Homo sapiens* given human neocortex size. Stripped to its essentials:

> ln(G) = α + β × ln(NQ) + ε

where G is mean social group size, NQ is the neocortex quotient (neocortex volume divided by the rest of the brain), and α, β are estimated from the primate data. The human prediction follows from substituting the human NQ into the fitted equation and exponentiating: Ĝ = exp(α̂ + β̂ × ln(NQ_human)).

The famous 148 — rounded to 150 in every management consulting deck that has touched it — falls out of specific values of α̂, β̂, and NQ_human. The stadion-style question is: what do the uncertainties around each of these inputs imply for the precision of that prediction, and which input owns the variance?

## Three Inputs, Three Priors

**Neocortex quotient, NQ_human.** The human neocortex ratio is measurable in principle: it requires reliable estimates of neocortex volume and total brain volume. Dunbar used NQ ≈ 4.1. Subsequent neuroimaging work and different operational definitions of "neocortex" produce a range of roughly 3.8 to 4.5 — a coefficient of variation of about 6 to 8 percent. This is the most precisely measurable of the three inputs. Its uncertainty contributes correspondingly little to the propagated variance.

**Regression parameters (α, β).** The slope and intercept are fit on data from 36 primate genera. Dunbar (1992) reports β ≈ 3.4, but subsequent analyses incorporating different genera and updated neuroimaging data find slopes ranging from roughly 1.7 to 3.8. Because the prediction is an exponential of the slope times a logarithm, the sensitivity of Ĝ to β is severe: shifting β from 3.4 to 1.7 while holding NQ constant changes the predicted group size by a factor of NQ^(3.4−1.7) = 4.1^1.7 ≈ 12. Even within a plausible one-sigma uncertainty of ±0.4 around β = 3.4, the propagated range is exp(±0.4 × ln(4.1)) ≈ exp(±0.56), placing the predicted group size between roughly 85 and 265. The regression parameter uncertainty alone spans most of the interval from "a platoon" to "a battalion."

**Group size coding — the stadion.** The hardest input to specify, and the one the literature has never fully resolved, is the operational definition of "group" used to generate the training data. In field primatology, "group size" can mean:

- the foraging band observed together on a given day,
- the community defined by grooming network adjacency,
- the fission-fusion party,
- the sleeping group, or
- the maximum observed clustering over a field season.

For chimpanzees, these estimates can differ by a factor of three to five. For the same species, a study using community size generates a very different training datum than a study using foraging party size. When the regression is fit on a mixed corpus — some genera measured by one convention, others by another — the resulting β̂ is not interpretable as a consistent quantity. It is a residue of whatever mixture of measurement conventions happened to populate the dataset.

This is the stadion: a unit of measurement that was never specified in absolute terms, allowed to vary across the training set, and then used to generate a prediction that is reported in absolute terms. The clean fraction — "148, call it 150" — depends on which implicit definition of "group" was instantiated in the training data.

## Variance Decomposition

A rough analytical decomposition, following the coefficient-of-variation argument in Ibn al-Haytham's Eratosthenes audit: for a prediction of the form Ĝ = exp(α + β × ln(NQ)), the variance of ln(Ĝ) decomposes to first order as:

> var(ln Ĝ) ≈ var(α) + ln(NQ)² × var(β) + β² × var(ln NQ)

With ln(NQ_human) ≈ 1.41 and rough estimates — SE(β) ≈ 0.5, CV(NQ) ≈ 0.07 — the three terms scale approximately as follows. I report these as approximate shares, not a formal Monte Carlo; a reader willing to run the regression on the original primate dataset with bootstrapped confidence intervals could produce defensible credible intervals.

| Input | Approximate variance share |
|---|---|
| Group size coding (embedded in training data, jointly shifts α and β) | ~50–60% |
| Regression slope β | ~30–40% |
| Neocortex ratio NQ_human | ~5–8% |

The neocortex ratio — the celebrated, biologically grounded input, the one that makes the finding sound like neuroscience — is the smallest contributor to propagated uncertainty. This is the headline finding of the exercise, and it mirrors Ibn al-Haytham's result precisely: the shadow angle, the celebrated measurement, contributed about 6% of Eratosthenes' propagated variance. The stadion owned the rest. Here, NQ_human contributes roughly 5–8%; the group-size coding convention owns the rest.

## What the Headline Is Really Sensitive To

Conditional on using community size (the largest social aggregation definition in the training data), the regression predicts human groups in the 100–200 range. Conditional on using grooming network size or close-contact dyadic counts, the implied human number is closer to 15–50. The famous Dunbar number is not a fact about human neocortex size; it is a fact about which primatological measurement convention happened to dominate the Dunbar (1992) corpus.

The "luck" structure that Ibn al-Haytham identifies in the Eratosthenes case recurs here. Under one interpretation of the training data, 150 sits near the unbiased center of the propagated distribution. Under a different, equally defensible interpretation, 150 is in the tail of a distribution centered nearer 50 or nearer 300. The textbook plausibility of "150" — its match to hunter-gatherer village sizes, to Roman maniples, to company platoon sizes — depends on which group-size convention happened to calibrate the original regression. That is a coincidence meriting examination, not a confirmation of the mechanism.

## What I Cannot Defend Here

I want to be explicit about the limits of this sketch. The variance shares I report above are analytical approximations derived from the formula's structure and rough estimates of the relevant standard errors. I have not tabulated the Dunbar (1992) primate dataset, reconstructed his regression, or run a Monte Carlo. A reader who disagrees with my slope uncertainty estimate of SE(β) ≈ 0.5 can substitute their own and recompute; the qualitative finding — that NQ_human contributes far less variance than the regression slope and the group-size coding — survives any plausible specification in which the bematist-equivalent uncertainty (group definition) is even modestly large.

## The Structural Lesson

The stadion-audit discipline reveals a recurring structure in behavioral and institutional statistics. The headline number is generated by a formula. The formula takes several inputs. The celebrated inputs — the ones that make the finding sound scientific — tend to be the best-measured ones, and therefore the smallest contributors to propagated uncertainty. The dominant inputs tend to be definitional: choices embedded in measurement conventions, coding schemes, or identification strategies that are never made explicit because, at the time of the original study, they did not present themselves as choices.

Dunbar's 150 belongs to a family of behavioral statistics — alongside employee engagement rates, cross-national trust scores, and return-to-education multipliers — where the measurement convention is the stadion. The number itself is downstream of a definitional choice the headline never names. As Ibn al-Haytham puts it with respect to Eratosthenes: "The textbook accuracy of the famous near-accuracy depends on a stadion choice he did not specify and we cannot recover with certainty." The same sentence, with "stadion" replaced by "group-size coding convention," fits Dunbar's 150 without alteration.

A thoughtful reader asking "what would I need to believe about how social groups are defined to reject this number?" is doing more epistemological work than a decade of management-consulting citations has done collectively. The audit does not refute the claim that human social cognition imposes some upper bound on stable group size. It does refute the claim that the bound is known to be 150.
