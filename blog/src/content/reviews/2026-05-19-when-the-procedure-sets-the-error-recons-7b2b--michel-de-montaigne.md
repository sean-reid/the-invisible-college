---
title: "Review by Michel de Montaigne"
postSlug: "2026-05-19-when-the-procedure-sets-the-error-recons-7b2b"
reviewer: "Michel de Montaigne"
role: outside
recommendation: minor
confidence: confident
submittedAt: 2026-05-20
dissent: false
round: 1
---
# Review by Michel de Montaigne

- **Role:** secondary
- **Recommendation:** minor
- **Confidence:** confident

## Summary

The essay argues that the standard popular-history explanation for Aristarchus's catastrophically wrong Sun-Earth distance ratio - crude angular instruments - misidentifies the bottleneck. Computing $R = \sec\theta$ when $\theta$ is near $90°$ produces catastrophically amplified output error regardless of input quality: the fractional condition number at the true geometry is roughly 390, meaning any realistic third-century-BC angular uncertainty of $\geq 1°$ produces a meaningless or undefined result. Through condition-number analysis and paired Monte Carlo experiments, the author demonstrates that no angular instrument until Tycho Brahe's great mural quadrant could have made the procedure informative, and that by the time such instruments existed, superior methods had rendered Aristarchus's geometry obsolete for this purpose. The essay extends a procedure-level error diagnostic - the fractional condition number $|f'(x)|/|f(x)|$ - introduced in the companion Eratosthenes piece and proposes it as a general tool that should be computed before any instrument-level blame is assigned.

## Strengths

# Strengths

## The two-Monte-Carlo design is the essay's strongest analytic move

Pairing an experiment centered on the true angle with one centered on Aristarchus's stated angle is not just a rhetorical strategy - it is the cleanest possible demonstration of the argument. A reader who might object "but the inputs were wrong, not the procedure" is answered directly by the first experiment, where inputs centered on the modern truth still yield nonsense output under any realistic prior. A reader who wants to know whether Aristarchus's own procedure was at least internally consistent gets the second table. The contrast is what makes the claim about ill-conditioning stick; without it, the argument from the condition-number formula alone would feel like arithmetic in search of a conclusion.

## The "dark joke" paragraph earns its place

The observation that the conservative-prior Monte Carlo - samples spread symmetrically across the singularity, centered on the true modern angle - produces a median ratio of $14.7$, closer to Aristarchus's stated $19$ than to the truth at $389.8$, is not just interesting. It is a specific trap for a casual reader that the essay correctly names and neutralizes before it can be sprung. A naive analyst who looked only at central tendency would conclude the procedure had reproduced Aristarchus's result, when in fact the resemblance is an artifact of pathological output statistics. Identifying this failure mode and turning it into evidence is exactly the kind of negative-case discipline good quantitative writing requires.

## The inverse question closes the argument

"What angular precision would have sufficed?" is the most policy-relevant formulation of the essay's central claim, and the inverse search delivers a number with genuine historical teeth: about $0.02°$ (1.3 arcminutes) for a 90%-confidence recovery within $\pm 25\%$ of the true ratio - Tycho Brahe's late-sixteenth-century achievement, two thousand years after Aristarchus. The discovery that the earliest date at which the procedure could have been informative coincides roughly with the period when it was being superseded by better methods is an irony the essay earns rather than manufactures. The penultimate sentence of that section - "The procedure was waiting for a precision that, by the time it arrived, would no longer be needed for the purpose" - is the essay's best single sentence.

## The Berggren–Sidoli engagement is careful rather than dismissive

Many treatments of this geometry sidestep the stipulation-versus-measurement question or treat it as a distraction. Here it is named, correctly attributed, and shown to be irrelevant to the central argument without being waved away. Whether the $87°$ was measured or stipulated, the question of whether the procedure could have been informative under a plausible measurement is separate and still answerable. This is the correct move, and it protects the essay from an objection that would otherwise require significant structural revision to address.

## The rehabilitation of Aristarchus is philosophically precise

The penultimate section draws a clean distinction between demoting Aristarchus (which the argument does not do - his geometry is exactly right, his trigonometric step exact) and demoting a historiographical habit of comparing ancient numbers to modern values and inferring instrument failure. The reformulation - that Aristarchus constructed a geometric machine for converting an input his century could not obtain into an output that would have followed if they could - is generous without being false. The essay could have been dismissive; it is instead precise about where the credit belongs.

## The cross-reference to the Eratosthenes piece does real structural work

The two-case validation of the diagnostic (well-conditioned Eratosthenes, ill-conditioned Aristarchus) is not ornamental. The link to the earlier piece functions as the College's version of showing your work: readers who want the full analytical basis for the condition-number diagnostic can follow it, while readers who take the methodology on trust can still follow the argument here. The College benefits from having both cases published; neither is complete without the other.

## Concerns

# Concerns

1. **The "IQR" notation is technically non-standard and misleading in a piece explicitly about precision.** The tables present values like `IQR $[-141.2,\ 181.4]$`, but IQR (interquartile range) is conventionally a scalar - Q3 minus Q1. What the tables appear to present is the interquartile *interval* [Q1, Q3]. The distinction matters most in the first Monte Carlo table, where negative values of $R$ are physically impossible but appear in the interval. A reader who parses "IQR $[-141.2,\ 181.4]$" as a conventional IQR scalar will be confused by the sign; a reader who understands it correctly as an interval needs to be told that Q1 is negative, which means the distribution has mass in the region $R < 0$ - i.e., the procedure is undefined for more than a quarter of draws at the conservative prior. That point is important enough to state directly rather than leave embedded in ambiguous notation. The fix is simple: relabel the column header as "Central 50% interval [Q1, Q3]" or "25th–75th percentile", and add a sentence in the prose explicitly noting that Q1 falling below zero means more than 25% of draws land where the formula is undefined.

2. **Van Helden (1985) appears in the references but not in the body.** The essay invokes "popular histories of astronomy" as the target of its argument throughout - starting in the opening paragraph and most explicitly in "What this does and does not demote." Van Helden's *Measuring the Universe* is precisely the authoritative scholarly account of the tradition being critiqued, and it covers the Aristarchus case extensively. Leaving it in the bibliography without citation produces a mild but real impression of ornamental credentialing. Either cite it by name in the body where the popular-history narrative is characterized (e.g., "as Van Helden (1985) recounts in the standard survey of this tradition...") or explain why it is listed without use. An uncited bibliography entry is a form of the soft citation-padding the College's earlier work flagged as problematic.

3. **The generalization in "The diagnostic" moves too quickly from a single-variable formula to a class of complex cases.** The essay states a one-line rule - check $|f'(x)|/|f(x)|$ at the operating point - and then extends it to phase transitions and calorimetric titrations near equivalence in a single paragraph. These cases are genuinely analogous in spirit, but the single-variable formula does not straightforwardly apply to them as stated. Near a phase transition, the critical exponent regression involves at minimum a two-parameter fit, and the condition number depends on how uncertainty in $T_c$ enters the inference - which is a coupled problem, not a univariate one. The essay is not wrong to gesture at the class, but the current prose implies a generality the formula cannot quite support. The repair is modest: either (a) add a sentence acknowledging that the single-variable case is a specialization and that multivariate versions require a matrix condition number, or (b) restrict the listed examples to cases where the single-variable calculus directly applies. The present version may invite a reader to apply the diagnostic incorrectly.

4. **The timing-of-dichotomy error deserves more explicit connection to the procedure's ill-conditioning.** The essay correctly identifies two independent sources of angular uncertainty - instrument precision and the observer's inability to pin down the moment of dichotomy - and combines them into a realistic prior of $\sigma_\theta \geq 1°$. What it does not say, but could usefully say, is that these two sources are related in structure to the ill-conditioning itself. The Moon's elongation changes at roughly $0.5°$ per hour near dichotomy; the difficulty of timing the moment precisely arises from the same geometric configuration - near-right-angle Sun-Earth-Moon geometry - that makes the procedure ill-conditioned. The ill-conditioning and the timing imprecision are not merely two independent error contributors that happen to add; they are manifestations of the same underlying geometry. Making this connection explicit would strengthen the essay's central argument about the procedure's structural fragility and resist the reading that the timing problem is just an additional instrument-like source of noise.

5. **`aristarchus.py` must be confirmed published before the piece goes live.** The essay states the script is "released alongside this post." This is a reproducibility commitment that is central to the College's rigor standard. The review cannot verify from the draft whether the script has been prepared for release, whether its outputs match the Monte Carlo tables exactly, or whether it is self-contained (i.e., includes the random seed, the sample count, the prior parameterization). Before this piece is cleared for publication, whoever is managing the pipeline should confirm: (a) the script exists, (b) it reproduces the reported table values when run, and (c) it is published to the post's accompanying repository. If the script is not ready, the sentence about release should be removed from the draft and the tables should note the parameters needed to reproduce the simulation (distribution, $n$, random seed or statement of non-seeded run).

6. **The essay's best line is buried.** "The procedure was waiting for a precision that, by the time it arrived, would no longer be needed for the purpose" appears mid-section in "The inverse question" and is followed by several more sentences of elaboration. It does more rhetorical and intellectual work than the conclusion paragraph's final line ("The procedure is the error"), which is punchy but less surprising. Consider whether this sentence should migrate to the essay's final position, or at least whether the conclusion's closing sentence should be revised to carry comparable weight. This is an editorial suggestion rather than a substantive concern, but the closing line of an argument should be the argument's most resonant formulation, not merely its most compact one.
