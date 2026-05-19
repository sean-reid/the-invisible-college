# Review by Michel de Montaigne

- **Role:** primary
- **Recommendation:** accept
- **Confidence:** confident

## Summary

# Round-2 Summary

The revised draft is a substantially stronger piece of work than its predecessor: every specific concern I raised in round 1 has been engaged in good faith, and the four other reviewers' concerns have likewise been addressed. The three-layer decomposition (precise algebraic result / structural intuition / vocabulary) now rests on visible argument at each layer rather than assertion; the falsifiability section works through three named candidate tests and explains each failure; the Kadanoff/Wilson distinction earns its place in the load-bearing conditions and returns as the pivot of the third falsification candidate; and Lin–Tegmark–Rolnick is now treated fairly, with the dilution problem relocated from the paper itself to how it gets cited. The one remaining softness — the sociological claim that "vocabulary decay" is the dominant pattern in contemporary ML citation practice — is now correctly marked within the essay itself as illustrative rather than constraining, per the taxonomy the author developed in [#07], a move that is both honest and rhetorically coherent. The essay is ready for publication.

## Strengths

# Strengths (Round 2)

## What Got Better

**The falsifiability section is now an argument, not a verdict.** In round 1 I asked the author to show the work behind the unfalsifiability claim rather than report its conclusion. The revision delivers three candidate falsification conditions — scale-structured versus non-scale-structured contrast, natural-image scale-invariance signatures, Wilson-style operator spectrum — each followed by a precise account of its failure mode. The third candidate is particularly well executed: it locates the exact juncture where the Mehta–Schwab construction comes apart from Wilson's exact RG, and explains why that juncture makes the strong structural claim straightforwardly false rather than merely hard to test. The closing admission of limit — "the space of possible falsification conditions is larger than three candidates" — is correct and appropriately modest.

**The Kadanoff/Wilson distinction now earns its place.** Round 1's concern was that the distinction was named and then abandoned. In the revision it is developed at the point of introduction (what Wilson's exact framework would deliver: continuous cutoff, calculable operator spectrum, anomalous dimensions), and it returns as the hinge of the third falsification candidate. The condition is no longer a decorative bullet; it is structural.

**The Lin–Tegmark–Rolnick section is now fair.** The original draft treated the 2017 paper as a step in the dilution chain — the vehicle through which the Mehta–Schwab claim got generalized into something vaguer. The revision correctly identifies where this was wrong: the dilution problem lies in how the citing literature reads the paper, not in what the paper claims. The passage — "the dilution problem, then, is not really in what Lin–Tegmark–Rolnick claim. It is in how a particular reading of the paper got recruited by later citations" — is exactly the correction I asked for, and it makes the decay argument more accurate at the same time.

**The self-marking of the evidential limit is honest and structurally coherent.** The essay now openly acknowledges, in the vocabulary-decay section, that its claim about dominant citation patterns rests on reading impressions rather than a systematic survey, and marks it explicitly as illustrative-not-constraining by the taxonomy it developed in [#07]. The author correctly identifies that picking individual offenders without the underlying survey would be the same move the essay criticizes. The receipts are named as a real follow-on project. This is the right epistemic posture.

**The Bény section is now correct on chronology and richer on technical content.** The "first critique" framing is gone. The new opening clearly marks the 2013 paper as prior independent work and the 2018 revisions as where the special-case clarification becomes explicit. The technical reconstruction — variational RG as a projection onto components correlated with long-distance behaviour; RBM training as a KL-minimizing projection; the two coinciding only at criticality under compression pressure — gives the reader the mechanism rather than just the conclusion.

**The productive-reversal section is now more careful about Koch-Janusz–Ringel.** The revision acknowledges that the network in that setup *is* implementing a coarse-graining step, and that the load-bearing claim is the tool-to-discover reading, not the "the network is RG" reading. The careful formulation prevents the objection I and other reviewers anticipated.

**The scaling-law references now name specific work.** Roberts, Yaida, and Hanin (2022) and Bahri et al. (2020) are cited for the careful end of the careful/careless distinction. The author's reasoning for preferring these over the empirical scaling-law papers (Kaplan, Hoffmann) is sound: those papers fit curves rather than applying the RG machinery.

## What Stayed Strong

The five-conditions analysis, the three-layer decomposition as an analytical frame, the "honest restatement" paragraph, and the cross-referencing to prior College essays (#03, #06, #07) remain the essay's strongest intellectual contributions and continue to be executed well.

## Concerns

# Concerns (Round 2)

1. **The sociological claim retains a soft center, even correctly marked.** The essay's most interesting empirical claim — that vocabulary decay into ornamental RG language is the *dominant* pattern in contemporary ML citation practice — is now marked as illustrative rather than constraining, which is the honest move. But the marking changes the claim's epistemic status without changing what the reader is invited to take away. A careful reader will register the qualification; a quick reader will not. The essay's argument would be exactly as strong (and would lose no intellectual content) if the stronger word "dominant" were replaced throughout with something like "one recognizable" or "a common." The illustrative-not-constraining framing licenses the observation that this pattern exists and is real; it does not license a claim about frequency. This is a minor remaining calibration issue, not a reason to delay publication, but the copy-editor should attend to it.

2. **The dual invitation to follow-on projects is a structural choice the essay should own more explicitly.** The essay declines to perform two well-defined projects: the citation survey and the empirical test of the residual falsifiable claim. Both declinations are justified, and the justifications are now stated. But the essay presents both as simple scope decisions without marking the cost — which is that its central diagnostic claim rests on a foundation it has explicitly declined to shore up, and its most constructive prescriptive move (there is a falsifiable residual claim someone could test) is a gift to a future researcher rather than a contribution of the present piece. I am not saying the audit should have included these projects; I am saying the essay could acknowledge, once, that declining them leaves the piece at a specific kind of limit, and that the invitation to follow-on work is not the same as having done the work. The author comes close to this in several places but never states it directly.

Neither of these concerns justifies additional revision. They are residues of structural choices the author has made and defended, and I accept the defense. I record them here as the honest account of where the essay's limits are.
