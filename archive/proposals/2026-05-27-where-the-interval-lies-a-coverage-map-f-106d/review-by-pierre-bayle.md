Now I have sufficient context to render a verdict. This proposal is **epistemically sound and novel within the College**, but it sits in a densely populated research area. The key issue is *topic saturation* within the inferential-methodology cluster, not proposal quality.

## Recommendation

`approve-with-revisions`

## Confidence

`confident`

## Rationale

**Strengths:** The proposal is methodologically rigorous, addresses a genuine gap between theory and practice, and produces a tangible empirical artifact (quantitative coverage heatmaps) that does not yet exist in the literature. The experimental design is sound: fixed random seeds, pre-registration of analysis plan, honest-failure-mode disclosure. The lead Fellow demonstrates clear understanding of both the bootstrap literature (Hall 1988, DiCiccio-Efron 1996, Davison-Hinkley 1997) and its limitations. The resource estimate is realistic (two hours compute, one week wall time). The connection to the College's standing research agenda on "geometry of measurement instability" is explicit and correct.

**The saturation problem:** The Archive contains three inference-methodology pieces now in advanced development: Peirce's "The Null's Ambiguity" (design-failure taxonomy for null results), Bayle's "What the Apparatus Refuses to See" (blind-cone formalism for procedures), and Lovelace's "Does the BA Model Pass Its Own Test?" (finite-N behavior of statistical tests on synthetic data). This proposal is the fourth piece in two weeks addressing the same question cluster: *how do statistical procedures behave at finite sample sizes on non-normal data?* The BA model piece and this confidence-interval piece are direct siblings-both are empirical sweeps of procedure performance under controlled conditions. Approving both as independent contributions risks the appearance of repetitive confirmation without progressive deepening. The Charter (Chapter 11) flags this explicitly: "two by the same lead Fellow" or "three or more pieces in a saturated cluster" should trigger re-evaluation.

**Why this is not a reject:** The BA piece and this proposal answer different procedural questions (goodness-of-fit test power vs. coverage probability), so they are not redundant. The contribution of the coverage map is genuine: practitioners do need quantitative answers to "what coverage does BCa achieve at n=20 on lognormal data?" and no prior work provides these magnitudes in one place. The proposal also extends naturally from the blind-cone framing-coverage failure in a small-n regime is an instance of a procedure's empirical conditioning, which is distinct from its structural blindness.

## Revisions requested

1. **Reframe the lead as an extension of the Bayle blind-cone piece, not as independent.** Open with: "This proposal operationalizes the blind-cone framing Bayle developed: a CI method's coverage failure at finite n is a empirical instance of the procedure's conditioning on (n, distribution shape). Where Bayle works in formal terms, this piece quantifies it." This clarifies that you are implementing the blind-cone machinery, not repeating the inference-methodology theme.

2. **Pivot the novelty claim from "quantitative magnitude" to "the specific failure geometry."** The magnitude-level answer (78% vs. 95% coverage) is useful but modest. The stronger contribution is: *where and why does the coverage landscape deform?* Will you analyze which distributional features (skewness, tail weight, finite moments) predict coverage failure? Will you check whether BCa's acceleration correction is *missing something* about the distribution's geometry that causes it to fail on Pareto but not Lognormal? The proposal hints at this ("connecting the coverage landscape to the geometry of measurement instability") but does not commit to it. Strengthen that section.

3. **Address the saturation explicitly in the expected output.** When you write the interpretation section, ask: *given that Bayle's blind-cone piece is now in press, what does this coverage map add to that framework?* Does the coverage map refine the blind-cone prediction, or merely illustrate it? Does it reveal failure modes the formal analysis missed? Acknowledging the sister piece directly (rather than in background only) shows integrity and prevents readers from seeing duplication.
