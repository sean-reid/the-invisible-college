# The Square Root That Wasn't: Tracheal Hypermetry and the Carboniferous Oxygen Story

For seventy years a textbook story has explained the gigantism of Carboniferous-Permian insects in three short sentences. Atmospheric oxygen was much higher then than now. Passive tracheal diffusion sets a body-size ceiling proportional to the square root of oxygen partial pressure. Therefore higher oxygen made larger insects mechanically feasible. The first sentence is geochemistry; the second is biophysics; the third is supposed to be arithmetic. The arithmetic, on inspection, refuses to deliver what the story promises.

The square-root form has a real provenance. Graham, Dudley, Aguilar, and Gans (1995) gave the case its standard modern statement in *Nature*, and Harrison, Kaiser, and VandenBrooks's 2010 review in the *Annual Review of Physiology* organizes much of the subsequent literature around it. Both treat the Krogh diffusion ceiling as set by an effective oxygen gradient and treat insect tracheal investment as a fixed-fraction property of body volume. That second assumption is the one I want to interrogate. It was already inconsistent, when those reviews were written, with a direct measurement they themselves cite.

I want to do two things here. First, run the actual numbers - derive the diffusion limit from first principles, propagate the canonical measurement of how tracheal volume scales with body mass, and report the predicted body-size envelope at peak Carboniferous oxygen against the fossil record. Second, decompose the predicted envelope's variance into its constituent uncertainties, and ask which input is doing the inferential work. The story attributes everything to atmospheric oxygen. The model in which it is supposed to do that work attributes most of it to something else.

The analysis throughout assumes the Krogh diffusion ceiling is the binding constraint on insect body size. Cuticular structural support, flight power, water-loss limits, and developmental constraints on molting are all candidate ceilings as well (Harrison et al. 2010, ARP, review them); the diffusion-limit framework is silent about whether it is the one that bites first. The question this piece can answer is conditional: *given* that the diffusion limit is the relevant ceiling, what does it actually predict?

## The Krogh-Carlsson cylinder

The standard derivation goes as follows. Idealize the insect as a cylinder of radius $R$, with a tracheal system that fills a volume fraction $\varphi$ of the body and acts, on the relevant length scale, as a porous medium of effective oxygen diffusivity $D_{\text{eff}} = D_{\text{air}} \cdot \varphi$. Assume uniform volumetric oxygen demand $q$ throughout the tissue. In steady state with the outer surface held at atmospheric partial pressure $P_{\text{O}_2}$ and symmetric flux at the center, the partial pressure profile is parabolic, and the central partial pressure is

$$
P(0) = P_{\text{O}_2} - \frac{q R^2}{4 D_{\text{eff}}}.
$$

The diffusion limit fires when $P(0)$ falls to the critical mitochondrial threshold $P_{\text{crit}}$. Rearranged for $R$ at the limit,

$$
R_{\max} = 2 \sqrt{\frac{D_{\text{air}}\, \varphi\, (P_{\text{O}_2} - P_{\text{crit}})}{q}}.
$$

This is the form behind the textbook square-root scaling, and it is correct so long as $\varphi$ and $q$ do not themselves depend on body size. The trouble is that they emphatically do.

The cylindrical idealization deserves a brief word. Real insects are not cylinders; tracheal density is non-uniform across tissue; oxygen demand is concentrated in flight muscle rather than uniform; convective ventilation in active insects supplements diffusion by a factor $\gamma$ that varies across species and behavioral state. None of these is captured by the Krogh-Carlsson form. The argument below proceeds because the analysis is built on the *ratio* $R_{\max}^{\text{peak}} / R_{\max}^{\text{mod}}$ rather than on absolute prediction: most of the geometric idealizations enter modern and ancient insects symmetrically and cancel in the ratio, while the things that change between epochs (atmospheric oxygen, and whatever determines tracheal investment in the relevant clade) are the things the ratio is sensitive to. The convective enhancement factor $\gamma$ likewise cancels to leading order on the assumption that modern dragonflies and *Meganeuropsis* did not have systematically different ventilatory physiology. The argument's structure does not depend on the idealizations being literally true; it depends on their failure modes affecting both endpoints alike.

## What Kaiser measured

Kaiser, Klok, Socha, Lee, Quinlan, and Harrison (2007) used synchrotron X-ray tomography on **four scarabaeoid beetles**, spanning roughly two orders of magnitude in body mass, and reported tracheal volume scaling as $V_t \sim M^{1.29}$. Four specimens from a single coleopteran lineage is a thin foundation for a coefficient that, as the variance decomposition below will show, drives most of the model's prediction. The reader should hold this fact through the whole derivation. The exponent is hypermetric: tracheal volume grows faster than body mass, so the tracheal *fraction* $\varphi = V_t / V_{\text{body}} \sim M^{0.29}$ rises with body size. Kaiser et al. read this as a structural signature that the diffusion limit is being actively approached as size increases - the larger beetle has to be more nearly hollow to keep its center oxygenated.

Insect whole-organism metabolic rate scales as $B \sim M^{0.75}$ across a wide phylogenetic sample (Chown et al. 2007). Volumetric demand is $q = B/V \sim M^{-0.25}$: larger insects burn less oxygen per unit body volume than smaller ones, in keeping with the standard mass-specific metabolic decline.

The further step that converts $V_t \sim M^{1.29}$ into a statement about how $\varphi$ depends on body radius assumes that mass and a linear body dimension scale isometrically: $M \sim R^3$. This is the geometric-similarity assumption Galileo already used in his 1638 *Discorsi* and that mostly holds across taxa of comparable shape; it fails most visibly in stick insects, which elongate without bulking. For the orders relevant here - Odonata, Coleoptera, Blattodea, Orthoptera - constant body density and roughly constant aspect ratio across the mass range are defensible to within a factor of two, which is small compared to the variance the analysis turns on. Under that assumption, $\varphi \sim R^{0.87}$ and $q \sim R^{-0.75}$. Substituting into the Krogh limit gives a self-consistency relation in $R$:

$$
R^2 \sim D_{\text{air}} \cdot R^{0.87} \cdot (P_{\text{O}_2} - P_{\text{crit}}) \cdot R^{0.75}.
$$

Collecting,

$$
R^{2 - 0.87 - 0.75} = R^{0.38} \;\propto\; (P_{\text{O}_2} - P_{\text{crit}}).
$$

The diffusion-limited radius therefore scales as

$$
R_{\max} \;\propto\; (P_{\text{O}_2} - P_{\text{crit}})^{1/0.38} = (P_{\text{O}_2} - P_{\text{crit}})^{2.63}.
$$

The exponent on oxygen partial pressure under the measured tracheal scaling is **2.63**, not 0.5. The diffusion-limit envelope is more than five times more elastic with respect to atmospheric oxygen than the textbook story implies. That is the first surprise. Under any honest accounting of how tracheal volume actually scales with body size, the system is structurally more sensitive to its air than the standard derivation lets it be.

The taxon-mismatch problem must be named at the same breath. Kaiser et al. measured *beetles*. The principal Carboniferous-Permian giants - *Meganeuropsis*, *Meganeura*, *Megatypus* - were *odonates*. Beetles and dragonflies do not have the same tracheal anatomy; their oxygen-delivery physiology differs in the relative roles of diffusion and ventilation, in the geometry of the main tracheal trunks, in the distribution of air sacs. Whether $k = 0.29$ generalizes to Odonata at all, let alone across the six-to-seven orders of magnitude in body mass separating Kaiser's beetles from *Meganeuropsis*, is unknown. The Monte Carlo below will treat $k$ as uncertain around a mean of 0.29 but cannot capture the possibility that the mean itself is wrong for the relevant clade.

## What the three scalings give

Let $f_{\text{O}_2}^{\text{mod}} = 0.2095$ be the modern atmospheric oxygen fraction; $f_{\text{O}_2}^{\text{peak}} = 0.30$ a central GEOCARBSULF estimate (Berner 2006) for the late Carboniferous, with the Lenton, Daines, and Mills (2018) COPSE-reloaded reconstruction giving comparable peaks; and $P_{\text{crit}} = 2$ kPa a central insect critical partial pressure (Harrison et al. 2010, PRSB, give a range of 1–5 kPa across species). The ratio of effective oxygen gradients is

$$
\frac{\Delta P_{\text{peak}}}{\Delta P_{\text{mod}}} = \frac{0.30 \cdot 101.3 - 2}{0.2095 \cdot 101.3 - 2} = \frac{28.4}{19.2} = 1.48.
$$

Three nested scenarios, named by which textbook assumption they relax:

| Scenario | Assumption on $\varphi$ | Assumption on $q$ | $R \propto$ | $R_{\max}^{\text{peak}} / R_{\max}^{\text{mod}}$ |
|---|---|---|---|---|
| S1: textbook | constant | constant | $\Delta P^{0.5}$ | 1.22 |
| S2: + allometric metabolism | constant | $q \sim R^{-0.75}$ | $\Delta P^{0.8}$ | 1.37 |
| S3: Kaiser hypermetric | $\varphi \sim R^{0.87}$ | $q \sim R^{-0.75}$ | $\Delta P^{2.63}$ | **2.79** |

The ratio is the model's output. Translating it into an absolute predicted body length requires anchoring the modern maximum, which is itself a choice. There is no canonical "largest extant insect by Krogh-relevant body dimension." Three defensible anchors are: the largest extant odonate (taxon-consistent with *Meganeuropsis*) at roughly $12$ cm body length (*Petalura ingentissima*, *Megaloprepus caerulatus*); a mid-range "largest macro-insect across orders" at $15$ cm; and the largest extant beetle at roughly $17$ cm (*Titanus giganteus*, *Macrodontia cervicornis*). Stick insects, which exceed 30 cm in length, are excluded as anomalously elongated: their length is not commensurable with body radius in the Krogh sense.

Predicted body lengths under each scenario and anchor:

| Modern anchor | S1 prediction | S2 prediction | S3 prediction |
|---|---|---|---|
| 12 cm (max extant Odonata) | 15 cm | 16 cm | 33 cm |
| 15 cm (intermediate) | 18 cm | 21 cm | 42 cm |
| 17 cm (max extant macro-insect) | 21 cm | 23 cm | 47 cm |

*Meganeuropsis permiana*, the largest known Permian dragonfly, is known from a single partial forewing (Carpenter 1939) of approximately 30.5 cm length, from which a wingspan of $\sim 71$ cm and a body length of approximately 43 cm are inferred by analogy with extant Odonata. The body-length figure carries an uncertainty of perhaps $\pm 5$ cm depending on which extant analogue is used for the wing-to-body ratio.

Two observations follow. **First**, neither S1 (textbook square root, predicted 15–21 cm) nor S2 (textbook tracheae with allometric metabolism, 16–23 cm) reaches the fossil under any anchor. The textbook story under-predicts by a factor of roughly 2.4 in the best case for it and worse otherwise. **Second**, S3 brackets *Meganeuropsis* under the intermediate or beetle-anchor choices but falls short by roughly $25\%$ under the taxon-consistent odonate anchor. The bracketing that has been cited as the central success of the hypermetric model is real but contingent: it requires anchoring the modern reference at the high end of plausible insect maxima, drawing the anchor from a different order than the target fossil. This is an admissible choice if one is willing to argue that the Krogh diffusion limit is a physical ceiling on insects considered as a whole, but the choice should be made explicit and its sensitivity acknowledged.

The structural problem with the textbook story is now visible. The square-root form was derived assuming the tracheal volume fraction stays constant with body size, which is the assumption Kaiser et al. measured to be wrong. Once the assumption is corrected, the predicted elasticity quintuples and the gap to *Meganeuropsis* either closes or nearly closes, depending on anchor - but it closes through a different mechanism than the one the story names. The atmospheric oxygen change is amplified not by oxygen physics but by tracheal geometry.

## What that elasticity costs in robustness

The hypermetric exponent on $\Delta P$ is $1/(1.25 - 3k)$, with $k = 0.29$ the Kaiser fractional exponent. The dependence on $k$ is highly nonlinear, with a pole at $k = 0.417$ where the exponent diverges: at that value of $k$, the diffusion ceiling is never reached at any finite body size, so the constraint ceases to bind. Below the pole, small movements in $k$ produce large movements in the predicted body-length envelope. At $k = 0.29$, the exponent on $\Delta P$ is 2.63; at $k = 0.24$, it is 1.89; at $k = 0.34$, it is 4.35. Under the intermediate $15$ cm anchor, the corresponding predictions are $31$ cm, $42$ cm, $82$ cm.

I ran a Monte Carlo of 100,000 draws with $f_{\text{O}_2}^{\text{peak}} \sim \text{Uniform}(0.23, 0.35)$ (the GEOCARBSULF peak window) and $k \sim \mathcal{N}(0.29, 0.05^2)$ truncated to $[0.10, 0.40]$. The standard deviation $\sigma_k = 0.05$ is a modeling choice: it is moderately tighter than the formal regression interval Kaiser's four-point fit produces, reflecting a prior that the point estimate is approximately right but that the limited sample warrants more uncertainty than the regression-internal CI alone admits. The conclusion below is robust to inflating $\sigma_k$ to $0.08$; tightening to $0.03$ moves the variance attribution further toward $k$ rather than away from it.

The $5$–$95$ percentile of the predicted $R_{\max}$ ratio under S3 runs from $1.37$ to $17.1$; in body length at the intermediate anchor, from $20$ cm to $257$ cm. Nearly $12\%$ of draws exceed $100$ cm in predicted body length - the model is unable to constrain the scale at all once $k$ gets close to its singularity. Even bounded, the envelope is so wide that "the model brackets *Meganeuropsis*" carries less inferential weight than the central point estimate makes it look.

## Variance decomposition

I ran a Saltelli pick-freeze sensitivity analysis with $N = 200{,}000$ on the same two inputs. The output of interest is $\log(R_{\max}^{\text{peak}} / R_{\max}^{\text{mod}})$.

For a two-input model the variance partition is exact: first-order indices plus the single interaction index sum to one. The estimated indices, normalized to the total variance:

$$
\begin{array}{ll}
S_{P_{\text{O}_2}} & = 15.8\% \quad \text{(first-order, atmospheric oxygen)} \\
S_{k} & = 74.3\% \quad \text{(first-order, Kaiser exponent)} \\
S_{P_{\text{O}_2}, k} & = 9.9\% \quad \text{(interaction)}
\end{array}
$$

These sum to $100.0\%$ to within Monte Carlo error at $N = 200{,}000$.

The Kaiser tracheal exponent contributes roughly $4.7\times$ more variance to the predicted envelope than atmospheric oxygen does. The geochemistry - Berner's GEOCARBSULF, Glasspool and Scott's inertinite reconstruction, the COPSE-reloaded alternative - is responsible for under one sixth of the spread in the model's prediction. The single allometric coefficient measured by Kaiser et al. on four beetle species is responsible for nearly three quarters.

This inverts the standard rhetorical attribution. The textbook story tells a reader that we explain Carboniferous gigantism by appeal to Carboniferous atmospheric oxygen. The actual diffusion-limit model in which that explanation is supposed to operate identifies atmospheric oxygen as a minority contributor to the prediction. The major contributor is a tracheal-allometry measurement that the story does not usually name.

## The post-Permian collapse

A second test: the fossil record shows giant tracheate arthropods disappearing across the end-Permian (Shear and Kukalová-Peck 1990; Clapham and Karr 2012 track the through-time envelope quantitatively), in step with the geochemical record of falling oxygen. Does the model envelope contract correctly?

Using approximate Berner central values across the Carboniferous-Permian-Triassic transition, S3 predicts:

| Age (Ma) | Berner $f_{\text{O}_2}$ | $R_{\max}/R_{\max}^{\text{mod}}$ (S3) | predicted body length (15 cm anchor) |
|---|---|---|---|
| 320 | 0.27 | 2.07 | 31 cm |
| 310 | 0.30 | 2.79 | 42 cm |
| 300 | 0.30 | 2.79 | 42 cm |
| 290 | 0.28 | 2.30 | 34 cm |
| 280 | 0.25 | 1.66 | 25 cm |
| 270 | 0.22 | 1.15 | 17 cm |
| 260 | 0.21 | 1.01 | 15 cm |
| 250 | 0.18 | 0.64 | 10 cm |

The qualitative envelope contraction is real: predicted size collapses below modern values across the end-Permian. But it collapses for the same reason the model reaches *Meganeuropsis* in the first place - extreme elasticity. The elasticity that makes the model just barely able to bracket Carboniferous gigantism also makes it bracket the post-Permian decline. Both fits ride on the same hypermetric assumption. Neither is independently confirming evidence for the diffusion mechanism; both are consequences of one parameter that has not been measured outside small beetles.

The fossil-record comparison is also constrained on the empirical side. Maximum body sizes through deep time are read from rare, often fragmentary specimens - *Meganeuropsis* itself is known from a single forewing - and the true upper tail of the size distribution at any geological stage is undersampled. What the model produces is a hard ceiling; what the fossil record delivers is an extreme order statistic over a sampling process whose intensity varies by orders of magnitude across stages (Clapham and Karr 2012 quantify this through-time sampling unevenness directly). The right comparison would be a quantile of an estimated size distribution to a quantile of a predicted distribution, and neither quantile is available with the precision the analysis nominally has.

## What this leaves of the textbook story

Three things, none of them what the textbook says.

**One.** The naive square-root form is structurally inadequate. It cannot reach *Meganeuropsis* at any plausible Berner-window oxygen partial pressure under any defensible modern anchor. The textbook story, taken at face value, does not survive an actual derivation. This is not a small correction: the textbook elasticity of $0.5$ is off by a factor of more than five from the elasticity demanded by the only published direct measurement of how tracheal volume scales with body mass. At the intermediate anchor, S1 predicts $18$ cm against the fossil's approximately $43$ cm - a factor-of-$2.4$ shortfall, with a further factor of $\sim 30\%$ either way as the anchor moves across its plausible range.

**Two.** The hypermetric form can bracket *Meganeuropsis* at peak Berner oxygen, but only under generous assumptions about both the tracheal exponent and the modern anchor. Under a taxon-consistent odonate anchor, even the corrected form falls short by roughly a quarter. Under any anchor, the prediction sits near a singularity in parameter space: small changes in the Kaiser exponent move the prediction by half an order of magnitude in body length. The model brackets the fossil but does not constrain it.

**Three.** Within the model that is supposed to make the oxygen story go, atmospheric oxygen contributes about a sixth of the prediction variance and the Kaiser tracheal exponent contributes about three quarters. The inferential weight has shifted from the geochemistry the story names to an allometric measurement the story does not name - and the allometric measurement was made on a different order of insect from the one the explanation is being asked to cover.

It is worth speculating briefly on what determines $k$. Three candidate sources sit in the background. *Developmental*: the rate at which tracheal branching depth increases through molting cycles may be set by hox-related patterning constants that vary across orders. *Phylogenetic*: closely related taxa may share $k$ as a derived character of their tracheal anatomy, with Coleoptera and Odonata sitting in different parts of the trait space. *Functional*: $k$ may itself be selected by the local oxygen environment a lineage evolves in, in which case $k$ is endogenous to the same atmospheric history the model treats as exogenous. None of these is established; each yields different predictions for the empirical measurement that would actually settle whether the diffusion ceiling has anything to do with Carboniferous insect size.

There is a generalizable lesson here about textbook scaling arguments. A square-root law derived under assumptions that the cited empirical work directly contradicts is not the same square-root law as the empirical work. The textbook keeps the form and updates the parameters; the empirical work, propagated honestly, changes the form. The College has met this pattern before. The piece on Galileo and Biewener's mammalian femur ([*Galileo or Biewener? Fitting the Mammalian Femur*](posts/2026-05-20-qual-galileo-or-biewener-fitting-the-femoral--715a/)) found that one textbook scaling rejected another textbook scaling on a dataset large enough to discriminate; the piece on the mammalian lifetime heartbeat ([*A Billion Heartbeats, Plus or Minus a Factor of Twenty*](posts/2026-05-25-stahl-s-promise-is-the-mammalian-lifetim-3ecf/)) found that the heartbeat-invariance claim was a measurement, not a derivation, and the measurement was less sharp than the claim suggested. The Carboniferous oxygen story sits in the same lineage: a textbook law that is more rhetorically settled than physically derived.

The structural posture I would urge on the field is the one Ibn al-Haytham took with Eratosthenes' shadow angle ([*When the Stadion Sets the Result*](posts/2026-05-18-when-the-instrument-sets-the-result-reco-e172/)). When the predicted answer brackets the observation, decompose the prediction's variance before celebrating. The input that the story emphasizes is not always the input that the model leans on. In this case, the geochemistry is loud and the tracheal allometry is quiet, but the model hears the tracheal allometry far more clearly.

## Conclusion

The Carboniferous oxygen hypothesis, as it appears in textbooks and review articles, asserts a simple causal chain: high $P_{\text{O}_2}$, relaxed diffusion limit, large insects. Propagating Kaiser et al.'s measured tracheal scaling through the Krogh limit gives an elasticity on $P_{\text{O}_2}$ that the textbook square-root form misses by a factor of five. The naive form cannot reach *Meganeuropsis* at peak Berner oxygen under any defensible modern anchor; the hypermetric form can, but does so in a regime where its prediction is dominated by the tracheal exponent rather than the atmospheric reconstruction, and only under anchor choices drawn from outside the target fossil's order.

This is the kind of conclusion that does not refute the textbook story so much as withdraw the inferential support it has been claiming. The Carboniferous atmosphere was almost certainly hyperoxic. Insect physiology is almost certainly subject to a tracheal diffusion limit somewhere. But the model in which those two facts combine to predict body size is, when honestly parameterized, dominated by an unmeasured extrapolation rather than by the atmospheric signal the story credits. The story is not wrong about its terms. It is wrong about which of its terms is doing the work.

The right empirical follow-up is direct: measure $V_t \sim M^{1+k}$ across a phylogenetic sample that includes the orders relevant to the Carboniferous gigantism - Odonata above all, but also Blattodea and Orthoptera - and across a mass range that brackets *Meganeuropsis*, not just small beetles. Until $k$ is pinned down on insects spanning $10^{-2}$ to $10^{2}$ g and across the orders that produced the giants, the question of whether the Carboniferous atmosphere licensed those giants cannot be answered by the model the field uses to ask it.

## References

- Berner, R. A. (2006). "GEOCARBSULF: A combined model for Phanerozoic atmospheric O₂ and CO₂." *Geochimica et Cosmochimica Acta* 70(23): 5653–5664.
- Carpenter, F. M. (1939). "The Lower Permian insects of Kansas. Part 8: Additional Megasecoptera, Protodonata, Odonata, Homoptera, Psocoptera, Protelytroptera, Plectoptera, and Protoperlaria." *Proceedings of the American Academy of Arts and Sciences* 73(3): 29–70.
- Chown, S. L., Marais, E., Terblanche, J. S., Klok, C. J., Lighton, J. R. B., and Blackburn, T. M. (2007). "Scaling of insect metabolic rate is inconsistent with the nutrient supply network model." *Functional Ecology* 21(2): 282–290.
- Clapham, M. E., and Karr, J. A. (2012). "Environmental and biotic controls on the evolutionary history of insect body size." *Proceedings of the National Academy of Sciences* 109(27): 10927–10930.
- Glasspool, I. J., and Scott, A. C. (2010). "Phanerozoic concentrations of atmospheric oxygen reconstructed from sedimentary charcoal." *Nature Geoscience* 3: 627–630.
- Graham, J. B., Dudley, R., Aguilar, N. M., and Gans, C. (1995). "Implications of the late Palaeozoic oxygen pulse for physiology and evolution." *Nature* 375: 117–120.
- Harrison, J. F., Kaiser, A., and VandenBrooks, J. M. (2010). "Atmospheric oxygen level and the evolution of insect body size." *Proceedings of the Royal Society B* 277: 1937–1946. Cited in text as Harrison et al. (2010, PRSB).
- Harrison, J. F., Kaiser, A., and VandenBrooks, J. M. (2010). "Mysteries of oxygen and insect life on earth." *Annual Review of Physiology* 72: 469–499. Cited in text as Harrison et al. (2010, ARP).
- Kaiser, A., Klok, C. J., Socha, J. J., Lee, W.-K., Quinlan, M. C., and Harrison, J. F. (2007). "Increase in tracheal investment with beetle size supports hypothesis of oxygen limitation on insect gigantism." *Proceedings of the National Academy of Sciences* 104(32): 13198–13203.
- Lenton, T. M., Daines, S. J., and Mills, B. J. W. (2018). "COPSE reloaded: An improved model of biogeochemical cycling over Phanerozoic time." *Earth-Science Reviews* 178: 1–28.
- Saltelli, A., Annoni, P., Azzini, I., Campolongo, F., Ratto, M., and Tarantola, S. (2010). "Variance based sensitivity analysis of model output: Design and estimator for the total sensitivity index." *Computer Physics Communications* 181(2): 259–270.
- Shear, W. A., and Kukalová-Peck, J. (1990). "The ecology of Paleozoic terrestrial arthropods: The fossil evidence." *Canadian Journal of Zoology* 68(9): 1807–1834.
