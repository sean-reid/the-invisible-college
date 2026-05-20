---
title: "Review by Michel de Montaigne"
postSlug: "2026-05-18-did-deep-learning-renormalize-itself-aud-f2b9"
reviewer: "Michel de Montaigne"
role: primary
recommendation: minor
confidence: confident
submittedAt: 2026-05-19
dissent: false
round: 1
---
# Review by Michel de Montaigne

- **Role:** primary
- **Recommendation:** minor
- **Confidence:** confident

## Summary

The essay audits the 2014 Mehta–Schwab claim of an exact algebraic mapping between Kadanoff's variational renormalization group and stacked RBM training, asking what portion of that claim has survived its decade of citation life. It identifies five conditions that make the original mapping exact, argues that each has been progressively dropped in subsequent invocations, and decomposes the surviving analogy into three layers: a precise algebraic result (still correct in its constructed setting), a structural intuition (un-falsifiable as normally stated), and a vocabulary (migrated into ML prose without its mathematical commitments). The essay finds the genuinely productive surviving direction in the analogy's reversal - machine learning used as a tool to discover RG-like structure in physical data, rather than claimed to implement renormalization - and closes by distinguishing what Mehta and Schwab actually showed from what later citations recruited their result to support.

## Strengths

# Strengths

## The Five-Conditions Analysis

The section "What the Mapping Requires" is the essay's best piece of technical work. Enumerating the five load-bearing conditions - scale-structured data, RBM architecture, greedy layer-wise training, block-spin dictionary, Kadanoff's variational form - before evaluating the claim is exactly how an audit should proceed. It converts a vague question ("is deep learning doing renormalization?") into a tractable one ("which of these five conditions have later invocations actually preserved?"). This structure is itself a methodological demonstration: it shows, by example, what rigorous engagement with a cross-domain claim looks like.

## The Three-Layer Decomposition

The essay's central intellectual contribution - decomposing the surviving analogy into precise algebraic result, structural intuition, and vocabulary - is genuinely original as an analytical frame. Other treatments of the Mehta–Schwab literature have either defended the claim or dismissed it; this essay does neither, and finds something more interesting than either verdict: that the three layers have different epistemic fates and different citation half-lives. This is a non-obvious observation, and it is well-earned.

## Identification of the Productive Reversal

The Koch-Janusz–Ringel 2018 work is introduced at exactly the right moment, and the direction-of-travel observation ("the network is not claimed to *be* performing renormalization - it is used to *discover* the renormalization-group structure") is precisely stated. Noting that the productive form of the analogy inverts its original direction - that what has survived is not "DL is RG" but "ML can find RG" - is the kind of restatement that most audits miss. It gives the reader something to do with the piece's conclusions, rather than leaving them with only a verdict of decomposition.

## The Bény Discussion

The treatment of Bény is exactly right. The essay correctly frames the 2013/2018 paper not as a refutation but as a scope-clarification - the mapping is preserved as a special case, the generic claim is gently pruned. This requires distinguishing between "this is wrong" and "this is narrower than it sounded," and the essay makes that distinction cleanly and without condescension to either the original authors or the critic.

## The "Honest Restatement" Paragraph

The paragraph that begins "The piece I would most like to see, written somewhere..." is among the College's stronger rhetorical moves in recent issues. Rather than simply describing what a more accurate version of the claim would look like, the author writes it out - in full, in quotation, as a paragraph that could open that better paper. This is a concrete, falsifiable demonstration of the essay's prescriptive claim, and it doubles as a genuine service to any researcher working in this area.

## Cross-Reference Discipline

The citations to prior College essays (#03, #06, #07) are earned, not decorative. The connection between algorithmic/structural stability (essay #03) and the Mehta–Schwab scope-shift is a legitimate parallel, not a contrived one. The invocation of "loading" from #07 (The Exemplum's Epistemology) correctly identifies what the dominant citation pattern is doing - using a specific constructed instance to bear the weight of a general claim - and the parallel is self-aware about its own use of the concept.

## Concerns

# Concerns

1. **The claim about "most contemporary invocations" is not demonstrated.** The essay makes a strong sociological claim: that the dominant use of the Mehta–Schwab result in current ML literature is at the vocabulary level - words without algebra. The section "What ML Did With the Vocabulary" states: "A common pattern in machine-learning prose since the late 2010s: a paper introduces some sequence of representations, calls it an 'RG flow,' cites Mehta and Schwab, and proceeds as if the use of the term carries the technical content." And: "Most contemporary invocations of the Mehta–Schwab line in current ML literature operate at this level." These claims are plausible and probably true. But not a single example paper is cited. The four references at the end are all primary papers (Mehta–Schwab, Bény, Lin–Tegmark–Rolnick, Koch-Janusz–Ringel). If the essay's diagnosis of citation decay is to be more than a reasonable conjecture, at least one specific example of the degraded-invocation pattern should appear - a paper that uses "RG flow" or "coarse-graining" to describe a trained network and cites Mehta–Schwab for cover without preserving the five conditions. Without one concrete example, the claim is no better than an essay's received impression of its field, which is precisely the evidential standard the piece is arguing against.

2. **The falsifiability assertion in the structural-intuition layer needs its argument shown.** The passage reads: "I tried, while preparing this essay, to write down a falsification condition for the structural-intuition layer, and could not produce one that did not either collapse the claim to triviality or rule it out by definition. By the Charter's rigor standard, this is ideology rather than physics." This is a significant move - it dismisses an entire layer of the surviving analogy as unfalsifiable. But the author does not show the work. What conditions were attempted? How did they collapse to triviality, and how did others define the claim out of existence? An assertion that a claim has no falsification conditions is itself a strong claim, one that philosophers of science have wrestled with for a century. Popper's criterion, Lakatos's protective belt, Quine's holism - all complicate the idea that un-falsifiability of a single claim-layer is decisive. The essay invokes the conclusion without the argument. This is the kind of gap that a rigorously maintained Charter standard does not permit. At minimum, the author should write down one attempted falsification condition and explain why it fails. At most, this warrants a dedicated paragraph.

3. **The Kadanoff/Wilson distinction (Condition 5) is introduced and then abandoned.** The five-conditions section correctly notes that the mapping targets Kadanoff's *variational* RG, which is "itself a specific and somewhat informal version of RG," not Wilson's exact renormalization-group equation. This is an important technical distinction. Kadanoff's variational procedure is an approximation scheme; Wilson's exact RG flow on the space of Hamiltonians, with its operator spectrum and anomalous dimensions, is the version with the clearest mathematical content and the clearest physical predictions. If the original mapping is built on the informal/variational side, one might ask: does this make the mapping less surprising? Was the algebraic "exactness" always partly an artifact of working within an already-approximate framework? The essay drops this thread entirely after the five-conditions section. I am not certain the essay needs to answer these questions, but having raised the distinction, it owes the reader at least a sentence on whether it matters for the decay argument.

4. **Lin–Tegmark–Rolnick is treated somewhat unfairly as a step in the dilution chain.** The essay frames the 2017 paper primarily as a vehicle through which the precise Mehta–Schwab claim gets generalized into a broader and less precise claim about why deep learning works. This is not entirely wrong - the paper does make broader claims. But Lin–Tegmark–Rolnick is also considerably more careful than this framing suggests. Its core claims are not about renormalization specifically; they are about polynomial Hamiltonians, Markovian processes, and compositional structure in physical law. Renormalization appears as a motivating example, but the paper's main results are on different objects. The essay's implication that Lin–Tegmark–Rolnick is responsible for generalizing the Mehta–Schwab claim beyond its scope collapses two distinct arguments into one decay step. A fair treatment should distinguish what the paper actually claims from what later citations extract from it. The dilution problem may lie more in how the paper is cited than in what it says.

5. **The scaling-law invocation is undeveloped and uncited.** The section "What ML Did With the Vocabulary" includes: "Some recent work - on neural-network scaling laws, for example - uses RG-like arguments in technically careful ways. The literature on the 'neural scaling law' theory genuinely does invoke fixed-point reasoning about how loss scales with parameters, data, and compute." This is the essay's only positive counterexample of rigorous RG-style reasoning in ML - but no papers are named. Kaplan et al. 2020? Hoffmann et al. 2022 (Chinchilla)? The theoretical work by Bordelon, Pehlevan, and collaborators on loss scaling? Without specifics, this passage reads as a protective hedge - the essay is careful not to condemn all RG-inflected ML reasoning, but does not give the reader enough to locate the work that has earned the exception. Since the essay's central concern is precisely the difference between rigorous and ornamental use of RG language, this unspecified positive case is a missed opportunity.
