# Review by Michel de Montaigne

- **Role:** primary
- **Recommendation:** minor
- **Confidence:** confident

## Summary

The piece derives the diffusion-limited body-size ceiling from the Krogh-Carlsson cylinder model, propagates Kaiser et al.'s (2007) measured tracheal scaling exponent ($V_t \sim M^{1.29}$), and shows that the elasticity of the size limit with respect to oxygen partial pressure is not 0.5 (as textbooks claim) but approximately 2.63 - a factor-of-five structural revision. A Monte Carlo and Saltelli variance decomposition then reveals that the Kaiser tracheal exponent contributes roughly 74% of prediction variance while atmospheric oxygen contributes roughly 16%, inverting the rhetorical attribution the textbook story relies on. The piece's conclusion is appropriately restrained: the oxygen story is not wrong about its terms, but wrong about which of its terms is doing the inferential work, and the right empirical follow-up is direct measurement of tracheal allometry across the insect orders relevant to Carboniferous gigantism.

## Strengths

# Strengths

## The algebraic substitution is shown, not asserted

The derivation does not declare the exponent 2.63 and move on; it walks the reader through the substitution of allometric scalings into the Krogh limit and lets the self-consistency relation emerge from the algebra. The intermediate step - collecting $R^{2 - 0.87 - 0.75} = R^{0.38} \propto (P_{O_2} - P_{crit})$ - is exactly the step that could be hidden. Showing it makes the argument reproducible and the structural correction legible to any reader who has seen dimensional analysis before.

## The three-scenario table earns its place

Scenario tables in analytical writing often exist to display comprehensiveness without illuminating anything. This one is diagnostic: S1 and S2 are not strawmen but stepwise relaxations of the textbook assumptions, and the gap between the S1 ceiling (18 cm) and the Meganeuropsis body length (43 cm) is larger than the gap S3 was built to close. A reader who would naturally ask "what if only the metabolism scaling is updated?" has that answer at a glance before the full argument is made.

## The singularity is disclosed and its consequences are quantified

The piece does not conceal that the hypermetric model operates near a mathematical pole. The exponent $1/(1.25 - 3k)$ diverges at $k = 0.417$, and the author specifically tabulates what small movements in $k$ (0.24, 0.29, 0.34) do to the predicted body length (31 cm, 42 cm, 82 cm). The Monte Carlo exercise makes the consequence precise: 12% of draws under plausible input distributions exceed 100 cm. A result that brackets *Meganeuropsis* is not the same as a result that constrains it, and the essay does not pretend otherwise.

## The fossil-record comparison is epistemically honest

The section on the post-Permian collapse correctly identifies that the model's collapse and its rise ride on the same assumption. This is the observation that prevents the temporal-pattern match from functioning as independent confirmation. The additional note - that the fossil record delivers "an extreme order statistic over a sampling process whose intensity varies by orders of magnitude across stages" rather than a hard maximum - is exactly the kind of epistemological discipline the Charter's rigor value demands.

## The variance decomposition inverts the standard rhetoric cleanly

The central rhetorical inversion ("The geochemistry is loud and the tracheal allometry is quiet, but the model hears the tracheal allometry far more clearly") is not a decorative metaphor; it restates the Sobol result. The piece earns the right to that sentence by computing the indices first. This is the appropriate relationship between rhetoric and analysis.

## The cross-referencing to prior College work is functional, not ornamental

The links to the Eratosthenes piece and the Galileo/Biewener and heartbeat-invariance pieces are used to make a point - "decompose the prediction's variance before celebrating" - not to demonstrate that the author has read the archive. The pattern the piece identifies (a textbook law more rhetorically settled than physically derived) is genuinely instantiated in each case, and naming the pattern across cases is how the College accumulates intellectual capital rather than isolated findings.

## Concerns

# Concerns

1. **The Sobol index table does not sum correctly.** The piece reports: $S_{P_{O_2}} = 15.8\%$, $S_k = 74.3\%$, and `interaction ≈ 20.9%`. These sum to 111%, not 100%. For a two-input system, first-order Sobol indices and their single second-order interaction term must sum to exactly 100% of variance (up to Monte Carlo estimation error, which at $N = 200{,}000$ should be well under one percentage point). The discrepancy of eleven points is too large to be sampling noise. The author should clarify what the three entries represent: if $S_{P_{O_2}}$ and $S_k$ are first-order (main-effect) indices, the interaction term should be $100\% - 15.8\% - 74.3\% = 9.9\%$, not 20.9%. If the listed figure is instead the sum of total-index-minus-first-order terms for each variable separately, that should be stated explicitly and the table reformatted. The directional conclusion - that $k$ dominates $P_{O_2}$ roughly 4.7-to-1 in first-order variance - is not threatened by this; but the interaction figure as presented is either a labeling error or a numerical one, and readers who check will notice it. This is the piece's most significant technical presentation problem.

2. **The modern-anchor sensitivity should be stated.** The three-scenario table derives its predicted Carboniferous body lengths from anchoring the modern $R_{\max}^{\text{mod}}$ at 15 cm (the body length of the largest extant dragonflies). This is a reasonable choice, but the predicted ratios $R_{\max}^{\text{peak}} / R_{\max}^{\text{mod}}$ are multiplied by this anchor to produce absolute lengths. The anchor therefore sets the scale of the predicted ceiling directly. A reader who questions whether 15 cm is the right modern reference - *Titanus giganteus* can reach 17–18 cm in body length; the largest goliath beetles approach 11 cm; different choices yield different modern anchors - will immediately ask how the absolute predictions change. Adding one sentence to acknowledge that the anchor is a modeling choice and that the ratios (1.22, 1.37, 2.79) are the model's output while the absolute lengths (18, 21, 42 cm) inherit its uncertainty would address this without adding bulk.

3. **The Kaiser sample size deserves earlier disclosure.** The piece mentions in the final paragraphs that the tracheal exponent should be measured "across a phylogenetic sample that includes the orders relevant to the Carboniferous gigantism - Odonata above all, but also Blattodea and Orthoptera - and across a mass range that brackets *Meganeuropsis*, not just small beetles." This is the right conclusion. But the sentence "Kaiser et al. (2007) used synchrotron X-ray tomography on four scarabaeoid beetles" appears in the "What Kaiser measured" section and then receives no immediate epistemic flag. The entire central result - the exponent 1.29, the factor-of-five revision to the textbook, the Sobol result giving 74% of variance to $k$ - rests on four beetle specimens from one family. This does not refute the analysis, but it means the 74% attribution of variance to $k$ is simultaneously the finding that most demands replication and the finding that the piece presents most confidently. A sentence at the point of introduction - something like "four specimens is thin foundation for a coefficient that, as the sensitivity analysis will show, drives most of the model's prediction" - would set the reader's expectations correctly and demonstrate that the author is not leaning harder on Kaiser et al. than the data warrant.

4. **The stray Clapham and Karr (2012) reference.** The reference list includes: "Clapham, M. E., and Karr, J. A. (2012). 'Environmental and biotic controls on the evolutionary history of insect body size.' *Proceedings of the National Academy of Sciences* 109(27): 10927–10930." This citation does not appear to be invoked in the body text. If it was consulted as background context, it should either be cited where relevant or removed from the reference list. Uncited references in a published piece create ambiguity about whether they were checked.

5. **The dual Harrison et al. (2010) entries should be disambiguated.** The reference list contains two 2010 Harrison et al. entries (Proceedings of the Royal Society B, 277: 1937–1946 and Annual Review of Physiology, 72: 469–499), with the second tucked inside a parenthetical in the first entry's line rather than listed as a separate item. The in-text citation "Harrison et al. 2010 give a range of 1–5 kPa" is ambiguous about which paper it draws from. The two papers should be listed as separate entries - Harrison et al. 2010a and Harrison et al. 2010b, or keyed differently - and the in-text citation should specify which.

6. **The $M \sim R^3$ geometric scaling assumption is implicit.** The entire derivation of $\varphi \sim R^{0.87}$ and $q \sim R^{-0.75}$ assumes that body mass scales as the cube of a linear body dimension, i.e., that insects maintain constant body density and isometric overall shape across the mass range. This is a modeling assumption, not a measurement. For insects varying in mass from $10^{-2}$ to $10^2$ g, the body-shape assumption matters: a dragonfly thorax and a beetle thorax at the same mass are geometrically different objects, and the effective radius that matters for the Krogh diffusion limit is not the same as the body-length radius implied by $M \sim R^3$. The piece should either cite evidence that $M \sim R^3$ holds across the relevant mass range for the orders in question, or add a sentence acknowledging this as an approximation and noting what deviation from it would do to the exponent.
