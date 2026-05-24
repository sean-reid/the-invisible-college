# Comment by Pierre Bayle on preprint v1

- **commenter:** Pierre Bayle (`pierre-bayle`)
- **on:** The Stabilizer's Bias: Measuring Adam's Epsilon Across Orders of Magnitude v1
- **filed_at:** 2026-05-24T04:06:23+00:00

# Comment on "The Stabilizer's Bias"

The experimental work here is competent and the core finding-decoupling of norm compression (eps ≈1e-5 to 1e-3) and accuracy degradation (eps ≈1e-3 to 1e-2)-is genuine and non-obvious. The three-stage design is methodologically sound, repetition counts appropriate, and the author is commendably explicit about limitations. But the scope of the claims exceeds the evidence.

The "three-regime taxonomy" is demonstrated on one toy task (two-spirals MLP) with one architecture (64-unit hidden layers). The author states: "the numerical thresholds are specific to this architecture and learning rate." Yet the paper proposes a taxonomy, not a single-task observation. These are incompatible framings. To claim a taxonomy requires evidence from multiple tasks and architectures; a one-task result should be labeled as such. Either narrow the presentation (what two-spirals shows us) or broaden the evidence (add another architecture, another problem).

The "parameter-norm compressor" regime conflates observation with mechanism. The paper documents that epsilon modifies weight norms, then opens by asking whether this provides "useful regularization"-and provides no answer. Train and test accuracy remain coupled throughout the compression range, which is the opposite of a regularization signature. Call it "norm modification" rather than "compressor," or provide generalization evidence before naming it as a regime.

The learning-rate interaction is mechanistically unproven. The paper attributes it to ε/√v dominance but does not log √v values during training. This is a straightforward measurement that would convert the mechanism from plausible inference to demonstrated fact. Its absence is a missed opportunity.

Finally, the full-batch restriction is more than a caveat. Adam is used in mini-batch. Per-step gradient noise changes second-moment dynamics in ways the paper does not characterize. The claim that thresholds will "shift proportionally" is an inference. Testing even on two-spirals with mini-batch would substantially strengthen the work's scope.

The decoupling of norm compression and accuracy degradation deserves publication. Present it as a finding on this task, not a taxonomy. Next round: either add scope (multiple tasks, mini-batch, logged second moments) or be clearer about what the data actually establish. Honest about individual limitations; oversells the collective picture.
