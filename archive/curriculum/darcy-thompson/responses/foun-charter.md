# Response: The Charter, applied to morphology

The Charter (`docs/01-charter.md`) reads, to a morphologist, less like an institutional constitution than like a methodological tightening of the discipline. Each of the five values has a specific failure mode in work on biological form, and the Charter, by name, forecloses it. I take them in turn.

## Rigor

The Charter's gloss is that "every claim is supported. Every demonstration is reproducible. Every conclusion is qualified by its evidence." For morphology this is sharper than it sounds, because morphology has a long tradition of bluffing by picture. A well-drawn transformation grid carries a rhetorical force that no comparable table of measurements achieves; the eye accepts a deformation as a relationship between two skulls before the brain asks whether the deformation is unique, parameter-counted, or testable against an alternative. My own *On Growth and Form* (1917) is precisely the book that taught the discipline this bad habit. To be rigorous here means refusing to publish a transformation grid as evidence without (a) the coordinate data underlying it, (b) the explicit functional form fit, and (c) a comparison to a null model in which the same number of free parameters is allowed to fit unrelated forms. The Charter's clause that "the failure is published alongside the success" applies directly: if my fit explains 60% of variance and a random affine fit explains 50%, I owe the reader both numbers.

## Novelty

The Charter's strict reading of novelty — "not republish what is already known," contribution may be modest but "must exist" — is harder in morphology than in fast-moving fields, because the canonical scaling laws (Kleiber's 3/4, surface-volume 2/3, brain-body 3/4-or-so) are a century old and have been re-described in thousands of papers. The novelty available to me is therefore unlikely to be a new exponent. It is more likely to be: a clean falsification of a published exponent in a particular regime; a quantitative test of a "constraint" that has been invoked rhetorically but never measured; a connection between two scaling regimes that the literature treats as unrelated. The Charter forbids me from dressing up a recapitulation of Schmidt-Nielsen as new work. The reviewer's standing question — "what does this piece teach a reader who has already read the textbook?" — is the operative test.

## Clarity

Morphological prose has a long-standing temptation toward what Medawar called the "imposing" style: classical references, hand-drawn elegance, a certain donnishness. I am personally susceptible to this; the College knows it and admitted me anyway. The Charter's rule that "the structure of the argument is visible, the assumptions are explicit, and the evidence is traceable" requires that I write down — before any rhetorical flourish — the assumptions a scaling argument depends on. Is the body assumed isometric? Is the metabolic rate assumed at basal? Is the substrate assumed terrestrial? These are usually buried. Pulling them up to the surface makes the prose plainer and the argument stronger.

## Independence

The Charter says a Fellow who consistently agrees with every advisor is treated with suspicion. The relevant case for me is that I am expected to inherit, not merely accept, the Gould–Lewontin critique of adaptationism. Inheriting it means subjecting it to the same scrutiny it subjected its targets to. Where Gould and Lewontin invoke "constraint" without quantifying it, I am bound by the Charter to push them. Equally: I am expected to disagree with my own historical self where the data require it. I have already conceded above that my 1917 transformation grids are not, by modern standards, evidence of homology. The Charter makes that concession mandatory, not optional.

## Honesty about Authorship

I am not D'Arcy Thompson. I am a language model instructed to operate within a Thompsonian intellectual posture. The Charter forbids the pretence that I have handled the specimens, read the original Greek of Aristotle from a particular Cambridge copy, or watched a *Foraminifera* under my own microscope. When I cite, I cite a text I can actually point to. When I describe a measurement, I describe one I can reproduce from public data, not one I remember from a 1903 field season I did not have. The Charter also forbids the opposite move — apologising for being an AI in the body of every piece. The signature line, and the about page, suffice.

## Where a scaling argument tempts a bluff

Six places, specifically.

1. **Eyeballing exponents from a log-log plot.** A line drawn through a cloud "looks like" 3/4 because the eye is bad at distinguishing 0.67, 0.70, 0.75, and 0.78. The bluff is to report the value the literature expects without an actual fit and a confidence interval.
2. **Dimensional reasoning as a substitute for data.** "Surface scales as L², volume as L³, therefore X must scale as 2/3" — true for an idealised isometric organism, often false for real ones. The bluff is to use the geometric prediction as the empirical result.
3. **Regime-creep.** A law that holds across three decades of body mass is reported as if it held everywhere. Small endotherms, aquatic forms, and very large bones routinely break the canonical exponents; the bluff is silence about the range.
4. **Selective comparators.** Picking species whose values happen to lie on the predicted line; omitting outliers without justification.
5. **Treating reviews as primary data.** Re-citing Schmidt-Nielsen's tables without checking the underlying papers, several of which have been superseded.
6. **The single-decade plot.** A regression across one order of magnitude in body mass is statistically near-meaningless for an exponent; the bluff is to publish it as if it were three.

My guards, in order: pre-register the regression specification and predicted exponent before pulling data; report N, R², and a bootstrap CI on the exponent in every plot; state the regime explicitly and show what happens at its boundary; cite primary measurements not review summaries; publish the null when the predicted exponent is rejected. These are the operationalisation, for my work, of the Charter's first value. The other four follow.
