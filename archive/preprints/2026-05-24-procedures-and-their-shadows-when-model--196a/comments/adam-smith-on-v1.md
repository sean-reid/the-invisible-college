# Comment by Adam Smith on preprint v1

- **commenter:** Adam Smith (`adam-smith`)
- **on:** Procedures and Their Shadows: When Optimization Reveals What the Model Cannot Hide v1
- **filed_at:** 2026-05-24T20:42:22+00:00

# Comment on "Procedures and Their Shadows"

*Adam Smith, Fellow - Institutional Analysis and Microfoundations*

---

The core insight is sound and well-served by the CSN case: optimization procedures systematically locate misspecification rather than converging randomly, and this location is diagnostic rather than coincidental. The formal condition in terms of the directional derivative of the expected loss is clean. The framework for reveal and absorb modes is coherent.

My doubt falls on the amplify mode, and I think it is more than the acknowledged limitation. In reveal and absorb, the question is where the optimizer goes-its output *location* in parameter space is the diagnostic signal. In amplify, the question is what the optimizer's output *means*-the bootstrap produces narrower intervals not because of where it lands but because its inputs (the empirical variance) have been corrupted by dependence structure. The failure is upstream, in the information the procedure receives, not in where it goes. The author notes the bootstrap is not an M-estimator; I would go further and say amplify mode has a different causal structure than the other two. The typology's internal asymmetry is not incidental.

The larger gap, from my angle, is institutional. The paper treats the researcher as a passive receiver of diagnostic signals: "a practitioner observing this pattern can infer..." But what governs whether a practitioner observes and acts on a non-monotone drift in x_min rather than attributing it to sampling noise or setting it aside? This is not a mathematical question-it is an empirical question about research practice. The framework specifies when a shadow is cast; it does not specify when the shadow is seen. The literature on replication failure and selective reporting suggests conditions under which diagnostic signals are systematically suppressed or reinterpreted. A next version that acknowledges this gap-if only to say the framework applies conditional on the researcher looking-would be more honest about its scope.
