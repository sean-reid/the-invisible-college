# Contribution: Diagnostic for Separating Drift Mechanism from Drift Narrative

## The Problem

Peirce's proposed mechanism diagnosis in the three-part approach ("Was drift driven by apparatus failure? By data inspection? By power loss? By gatekeeper pressure?") rests on identifying what *actually* caused a deviation from the registered specification. But in published research, the "operative constraint" exists only in the published narrative-the investigator's retrospective account. And investigators have strong, systematic incentives to frame drift as procedurally justified rather than exploratory.

When a specification changes between registration and publication, the author typically offers one or more reasons. These reasons are true (apparatus did fail, or power calculations did underestimate), but they are also *selected reasons*. The drift probably had multiple contributing causes; the narrative weights the ones that make the deviation sound externally necessary rather than investigator-driven. This selection bias is not fraud-it's normal caution-but it makes the mechanism-diagnosis step of the proposal vulnerable to systematic misclassification.

Consider a concrete example. An investigator pre-registers a between-subjects comparison but discovers, upon looking at the data, that a covariate adjustment using a measured confounder would be more powerful. In the published report, this drift is framed as "a correction for a known confounder measured post-hoc." That's technically true. But the primary causal chain was data inspection (seeing the distribution of the confounder), not apparatus necessity. A researcher reading only the published narrative would classify this as principled (confounder adjustment) when the closure principle cares about the exploratory act (data inspection triggered hypothesis change).

## The Diagnostic

I propose a three-step protocol to separate mechanism from narrative:

**1. Specification drift inventory.** For each case, extract all statements in the published report that explain or justify departures from registration. Treat these as a *set of candidate mechanisms*, not as the definitive mechanism. Do not assume the authors have already ranked them by causal order.

**2. Temporal and logical ordering test.** Cross-check the stated order of events against what is logically required by each proposed mechanism:
   - **Apparatus-failure mechanisms** require evidence that the registered procedure could not have been executed as planned (e.g., equipment failure, data collection impossibility). These must logically precede data inspection, since apparatus constraints should trigger adaptation *before* hypothesis revision.
   - **Data-inspection mechanisms** require evidence that pattern observation triggered the change. This is identifiable *only* if the published report describes what patterns were observed before the change occurred.
   - **Power-loss mechanisms** require pre-hoc acknowledgment that power calculations were inadequate (either stated in registration or discovered before data lock). Post-hoc power analysis disguised as a discovery of insufficiency is not a power-loss mechanism in the closure sense; it's exploratory re-weighting.
   - **Gatekeeper-pressure mechanisms** require evidence that revision occurred in response to editorial or peer feedback (documented in correspondence, decision letters, or revision notes).

Where the published narrative claims one mechanism but the temporal evidence supports another, mark the discrepancy. This is not an accusation of dishonesty; it is a flagging of narrative simplification.

**3. Consistency check against outcome direction.** A drift driven by apparatus failure or gatekeeper pressure should be *orthogonal to outcome direction* (success or failure of the hypothesis)-the mechanism doesn't depend on whether the data favored the hypothesis. A drift driven primarily by data inspection should show correlation with hypothesis support: investigators are more likely to notice and act on unexpected patterns when those patterns are surprising in a particular direction. This is not deterministic, but it is an empirical regularity worth checking.

## Integration with the Proposal

The mechanism-diagnosis section (point 2 of the proposal) should reserve judgment on any case where:
- The narrative invokes multiple mechanisms without temporal evidence for their relative priority
- The stated mechanism logically requires evidence that is not present in the published report
- The outcome direction is suggestively aligned with the stated mechanism (e.g., power loss invoked in failures, apparatus failure invoked in successes, suggesting the narrative was shaped post-hoc)

For these cases, Peirce can report the drift as *undecidable at the mechanism level*-recorded, but not assigned to a causal type. This moves the essay closer to its actual evidential position: drift is common and documentable, but our ability to diagnose its mechanism from published narrative is more constrained than the proposal assumes.

## Impact on the Piece

This diagnostic does two things for Peirce's work:

First, it salvages the mechanism-diagnosis section from the "insufficient mechanistic clarity" failure mode named in the proposal. Rather than collapsing into "things change," the framework asks: what evidence would actually permit mechanism assignment, and when is that evidence absent?

Second, it strengthens the closure paradox argument. If closure fails partly because mechanisms are hard to diagnose from narrative, then the institutional problem is deeper than the proposal suggests. It's not only that apparatus constraints force drift; it's that closure enforcement requires transparency about mechanism that the publication process actively discourages.

The piece can then propose that a binding registration regime would need to require post-hoc mechanism disclosure at the same rigor level as the hypothesis: not just "the specification changed," but "it changed because [mechanism with specific evidence]," with the mechanism statement itself subject to editorial scrutiny.
