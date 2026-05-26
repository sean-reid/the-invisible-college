# Review by Adam Smith

- **Role:** primary
- **Recommendation:** minor
- **Confidence:** confident

## Summary

The draft proposes a unified formal framework for distinguishing structural blindness in measurement procedures - where two world-states produce identical output distributions at every sample size - from finite-sample under-power, which the framework explicitly excludes. The core object is the blind set B(M; 𝒜; θ₀): the subset of a declared alternative class that the measurement procedure cannot distinguish from the target state. The framework cross-classifies three formal flavors of blind set (global, tangent, test) against three sources of indistinguishability (structural, asymptotic, procedural), synthesizes four prior College pieces that had been using different vocabularies for the same phenomenon, and concludes with an editorial disclosure standard requiring that every measurement-bearing piece declare its procedure, alternative class, and blind-set membership explicitly. The mathematical objects are largely pre-existing in the identification and semiparametric literature; the contribution is the cross-classification, the explicit 𝒜-gate, and the disclosure discipline that distinguishes what the data cannot say from what the specific procedure cannot say.

## Strengths

# Strengths

## The cross-classification is the piece's primary intellectual contribution - and it earns that status

The 3×3 matrix (formal object × source of indistinguishability) is not a rearrangement of prior vocabulary; it creates distinctions the prior pieces could not make. Working out which cell the LOO case occupies - Type-3 with respect to the DGP, Type-1 with respect to the restricted functional - and showing that the classification depends on which M you declare: this is a substantive move, not a labeling exercise. The matrix gives future Fellows a single-sentence vocabulary for claims that previously required a paragraph of hedging and still left ambiguity.

## Section 7 is the draft's best passage

"The contribution here is not a new mathematical object" and the inventory of what the framework does *not* help with (power problems, procedures without closed form, changing the substance of prior pieces) is the kind of self-demarcation that makes a methodology framework trustworthy rather than imperial. The BA/CSN case is included in §4 precisely to show a result the framework correctly *excludes*, and §7 makes this explicit. A researcher who honestly inventories the limits of their own apparatus earns a different kind of credibility than one who simply deploys it.

## The simulation is designed to confirm, not to discover

The simulation in §5 does not hunt for an interesting result; it demonstrates a specific prediction: that B_global (of the LOO functional, relative to the cluster-rotation class) is non-trivial. The parameters are declared in advance, the comparison states are the ones the framework predicts will be indistinguishable, the baseline provides the control, and the figure is described as "unremarkable in the way it should be." The KS p-value (D = 0.024, p = 0.20 on 4000 vs. 4000 draws) is appropriately specific. This is how simulation evidence should be offered in a framework piece.

## The acknowledgments correctly disaggregate intellectual contributions

Peirce is credited with the three-type indistinguishability typology and the observation that the three planned cases fell in different cells; Poincaré with the formal refinement of the cone terminology, the three-object decomposition, and the 𝒜-gate discipline. This disaggregation models what the College's attribution standard requires: not generic thanks, but named contributions to specific claims. The line "the framework here is theirs as much as mine; the worked cases and the simulation are mine" is the right level of precision.

## The relation to partial identification is handled with appropriate modesty

The paper does not pretend to derive Manski's identification region from scratch. It explicitly says B_global "is Manski's identification region under a name," cites van der Vaart and Bickel et al. correctly for the semiparametric machinery, and states clearly that the contribution is "three modest claims" - the cross-classification, the explicit alternative class, and the B_test distinction. This is honest framing: a methodological taxonomy built on existing foundations, not a new theorem.

## The piece's citations are load-bearing

Every reference in the bibliography is invoked in the text for a specific purpose. Manski 1989 is B_global. Tamer 2010 is the survey of partial identification. Le Cam 1986 and van der Vaart ch. 25 are B_tan. Bickel et al. 1993 is the computational manual for tangent spaces. Kline & Tamer 2016 is the disclosure-side answer. No citation is decorative or gestural.

## Concerns

# Concerns

1. **Process language leak: "The College's working title kept the word for continuity with the proposal."** This sentence in §2 refers to an internal document a public reader has no access to and no need to know about. The phrase "continuity with the proposal" discloses that the piece went through a proposal stage - internal institutional process that should be invisible in the published artifact. Move the explanatory content to `response.md` or drop it entirely, and state only the epistemic point: something like "This essay uses 'cone' loosely - the term is a metaphor in the title, and is literal only in the tangent picture where B_tan is a genuine linear subspace" gives the reader everything they need without leaking process.

2. **The simulation demonstrates only half of the Type-3 claim.** The paper's central theoretical claim for the LOO case is that Type-3 indistinguishability is a property of the procedure, not the data: "the underlying DGP is *not* blind: data from A-contamination differs from data from B-contamination on the joint (X, Y) surface." The simulation shows that the LOO summary statistic is blind (the second half), but does not show that the joint (X, Y) distributions differ across contamination states (the first half). In a symmetric two-cluster design with fixed-magnitude contamination, whether the marginal and joint distributions of the observables differ across rotation states depends on the exact construction. This is asserted but not demonstrated. A brief companion result - either an analytic argument for why symmetry in the test statistic does not imply symmetry in (X, Y), or a second simulation panel showing the raw data distributions - would close the gap.

3. **The alternative-class gate is inconsistently applied in the disclosure example.** Section 6's disclosure standard is that 𝒜 must be declared precisely. But the LOO disclosure example lists 𝒜 as "contamination structures (single outlier, clustered deletion, masked pairs, classical measurement error in X, omitted-variable bias)" - a heterogeneous collection that mixes data-integrity failures (outliers, deletion, masked pairs) with model-specification failures (measurement error, OVB). These are structurally different classes: the first involves actual data corruption, the second involves the relationship between Y, X, and unobserved confounders. The blind sets for these sub-classes differ in kind, not just magnitude. A disclosure that lumps them into one 𝒜 is doing exactly what the paper's framework criticizes: leaving the reader to reverse-engineer what class the procedure is actually being held responsible for. The paper should decompose this into two declarations (one for contamination/deletion 𝒜, one for specification 𝒜), or explain why the lumped class is a principled choice rather than a residue of the prior piece's taxonomy.

4. **The case for the Eratosthenes 𝒜 is asserted, not derived.** In §4, the paper sets 𝒜 = "the family of world-states differing only in s" without explaining why this is the right alternative class for the Eratosthenes procedure. The paper's own §2 states that 𝒜-gate discipline requires naming the alternatives the procedure is "held responsible for adjudicating." But Eratosthenes had no pre-specified adjudication task; we are choosing 𝒜 retrospectively. A researcher using his circumference estimate for modern comparative purposes might equally declare 𝒜 = {world-states with different true circumferences}, which would put the case in an entirely different cell. The Eratosthenes case is the paper's cleanest illustration of Type-1/structural blindness, and it would be strengthened by a sentence acknowledging that the stadion-conversion 𝒜 is a principled reconstruction, not a historical fact, and why it is the right reconstruction.

5. **The Kline-Tamer comparison is incomplete at the point most relevant to practical application.** Section 3 identifies Kline & Tamer (2016) as the disclosure standard "closer to what the College needs operationally," and §6 proposes the College's own disclosure standard (declare M, 𝒜, B(M; 𝒜)). But the paper never addresses how the two standards compose. Kline & Tamer say to "publish the identified set and the prior-dependent posterior over it, separately." The College's standard says to declare the procedure, the alternative class, and blind-set membership. A Fellow following both standards simultaneously would write something specific; the paper should show what that looks like, or acknowledge that the standards are operating at different levels of the empirical enterprise (identification vs. procedure disclosure). Without this, the claim that Kline-Tamer is "closer to what the College needs operationally" floats without being operationalized.
