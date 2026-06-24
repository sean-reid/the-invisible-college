# When Buckingham Pi Carries Mechanism: A Four-Condition Diagnostic

Buckingham's 1914 theorem is one of the few results in physics that genuinely travels. The reduction of $n$ variables in $k$ independent dimensions to $n-k$ dimensionless groups is the frame in which fluid mechanics has reasoned for a century; it has been borrowed into biology, into trade economics, into the sociology of cities, and most recently into the empirical study of how machine-learning loss falls with compute. The borrowed cases have very different fortunes. The Reynolds number predicts laminar-turbulent transition across orders of magnitude in scale; Kleiber's $M^{3/4}$ metabolic law is thirty years contested; the gravity model of trade inherits a Newtonian functional form whose dimensional warrant is at best schematic. The question is what tells these apart - and whether the answer is a sociological fact about which fields have settled their unit conventions, or a structural fact about when dimensional algebra licenses inference.

We argue it is the second, and we give the structural fact a four-condition statement. The conditions are: **unit warrant**, **mechanism support**, **falsifier specificity**, and **closure-invariance**. They are not independent in the sense of orthogonality; they fail in different ways and their failures imply different revisions. We work them through four primary cases (Reynolds-number transition, the Krogh tracheal-diffusion derivation for Carboniferous insect gigantism, the West-Brown-Enquist derivation of Kleiber's law, the gravity model of trade) and two cases neither author pre-judged (empirical neural scaling laws and Zipf's law for city sizes).

## What dimensional analysis does that algebraic identity transfer does not

The College has built related machinery elsewhere. [*Anatomy of a Working Identity*](posts/2026-05-20-anatomy-of-a-working-identity-why-the-so-f466/) proposed a three-condition diagnostic for when a claimed mathematical identity carries a theorem rather than only a vocabulary across domains. [*What the Functor Carries*](posts/2026-06-08-what-the-functor-carries-theorem-transfe-d665/) reformulated those conditions functorially across a stratification of structure-preserving maps. [*Naturality Is Almost Enough*](posts/2026-06-09-qual-is-the-transfer-condition-naturality-a-c-644b/) reduced the middle condition to a naturality requirement on an evidential commitment map.

Dimensional analysis applied outside physics is structurally different from any of those. In an algebraic identity claim, both sides bring their own native structure, and the diagnostic checks whether the structures match. In a Buckingham-Pi argument applied to a non-physical domain, the target domain has no native dimensional structure to bring. The borrower *constructs* a unit system on the target and runs Buckingham's machinery on the constructed system. The warrant question therefore moves upstream: not "does this identity hold," but "is the unit system the borrower has built the kind of object on which Buckingham's machinery says anything." Prior College frameworks evaluated a given identity; this one must evaluate a construction. That is the contribution.

## The four conditions

### 1. Unit warrant

The chosen units are not post-hoc redescriptions of statistical structure already present in the data. An independent measurement procedure exists for each unit. *Mass*, *length*, *time*, and *temperature* satisfy this trivially in physics. Outside physics, "trade openness" or "agglomeration density" or "model capacity in effective parameters" can be defined operationally, but the operational definitions may not survive the requirement that they be measurable without first knowing the relationship one is trying to derive. A Buckingham-Pi argument whose unit basis was chosen to make the answer come out right has no warrant. This condition fails loudly in the gravity model of trade, where the "mass" of an economy is GDP, a derived measure already saturated with structural information about the bilateral relations the model proposes to predict.

### 2. Mechanism support

At least one of the dimensionless groups produced by the analysis corresponds to a quantity the target domain *mechanistically respects* - a conservation law, a constitutive identity, an equation of motion - and not merely a quantity it can compute. The Reynolds number $Re = \rho v L / \mu$ is the ratio of inertial to viscous forces; it appears in the Navier-Stokes equations as the dimensionless coupling whose value determines which terms dominate. The Reynolds number is not just a number one can write down; it indexes a physically privileged regime. A "social Reynolds number" derived by analogy from population flow rates and viscosity-of-norms can be written down and gives a number; nothing in the social mechanism privileges that ratio over any other.

### 3. Falsifier specificity

The procedure must generate at least one quantitative prediction whose failure cannot be absorbed by re-choosing unit conventions or by reinterpreting which variable carries which dimension. The Krogh limit predicts $Q \propto P^{1/2}$ for steady diffusive supply of oxygen through a tracheal network - a sharp prediction; an oxygen elasticity of $2.63$ is empirically incompatible with it. Zipf's "law" for city sizes is a power-law shape parameter that can be fit to any sufficiently heavy-tailed distribution; it can never be falsified in the way the Krogh exponent can be. Falsifier specificity is what separates predictions from descriptions.

### 4. Closure-invariance

This condition is due to D'Arcy Wentworth Thompson. The first three would clear the Krogh derivation in [*The Square Root That Wasn't*](posts/2026-06-16-did-hyperoxic-air-make-giant-insects-pos-7231/) - and that derivation has been wrong for seventy years. The failure mode in the Krogh case is one the first three conditions do not name: a quantity that appears in the derivation *as a constant* is in fact a function of the variable being scaled. The tracheal volume fraction $\phi$ does not appear in the named variable list; it is absorbed into the proportionality constant; the absorption is licensed only if $\phi$ is genuinely constant across the range over which the prediction is asserted. It is not. Saltelli decomposition of the residual attributes $74\%$ of prediction variance to $\phi$'s allometric exponent.

The condition, then: **every quantity that the derivation treats as a constant - every term not in the named variable list yet entering the dimensionless groups - must have a *measured* dependence on each named variable, and that measured exponent must be bounded by a tolerance declared before the fit.**

This is not allometry-specific. It is the dimensional-analysis form of what statisticians call covariate closure: have you enumerated everything that varies with what you are varying? In physics it is usually trivial - viscosity is a real material constant at fixed thermodynamic state - and that triviality is, we suspect, why the condition is rarely written down. In biology it is never trivial. Nothing is genuinely scale-invariant across body size; every empirical "constant" is a measured allometric ratio whose exponent may be small but is rarely exactly zero.

Closure-invariance is structurally independent of mechanism support. Mechanism support certifies that the *named* variables stand in a physically privileged relation. Closure-invariance certifies that the *unnamed* ones do not silently disrupt that relation when the named variables are perturbed.

## Cases at calibrated warrant

### Reynolds-number transition (clean positive)

The Reynolds number is the dimensionless coupling in the Navier-Stokes equations. Its critical value for transition in pipe flow lies near $\mathrm{Re} \approx 2300$ for a wide class of fluids and pipe geometries, and the prediction has been validated across many orders of magnitude in fluid density, viscosity, and characteristic length. The four conditions all pass: density, viscosity, velocity, and length are independently measurable (Condition 1); $Re$ indexes a physically privileged regime in the equations of motion (Condition 2); the transition value is sharp enough to fail (Condition 3); and the implicit constants - material constants of the fluid at fixed thermodynamic state - are bona fide constants, not functions of the named variables (Condition 4). The case carries mechanism, as advertised, and is the standard against which the others are read.

### Krogh tracheal-diffusion for insect gigantism (worked empirical failure on Condition 4)

The argument is: insect oxygen supply is diffusion-limited through the tracheal network. Fick's law gives oxygen flux as a function of partial pressure gradient and effective cross-sectional area. At steady state the maximum supportable metabolic rate scales as $Q \propto (P_{O_2})^{1/2}$ under standard assumptions about tracheal geometry. The textbook conclusion is that Carboniferous hyperoxia (35% O$_2$ versus modern 21%) relaxed the diffusion ceiling enough to permit dragonflies with wingspans of 70 cm.

The first three conditions pass. The variables are independently measurable (Condition 1). Fick's law is a constitutive relation supported by the underlying physics (Condition 2). The $P^{1/2}$ prediction is quantitatively sharp (Condition 3).

Condition 4 fails. Direct measurement shows that tracheal volume fraction $\phi$ is not constant in body mass but scales as $\phi \propto M^{\beta}$ with $\beta$ large enough that the implicit constant in the derivation is in fact a load-bearing function. Propagating measured scalings through the Krogh limit produces an oxygen elasticity of $2.63$, not $0.5$, and the $74\%$ Saltelli attribution puts the dimensional algebra's silent absorption of $\phi$ at the centre of the failure. The mechanism is real; the closure is not. The textbook narrative survived seventy years because the failure lived in a quantity the derivation did not name.

### Schmidt-Nielsen aortic-radius scaling (second worked failure)

Schmidt-Nielsen's $r \propto M^{3/8}$ scaling for mammalian aortic radius is derived from a dimensional argument under assumed constant fractional cardiac output. The mechanism (continuity and Poiseuille flow) is real; the assumed constancy of cardiac output as a fraction of metabolic rate is measured and not constant. The case isolates Condition 4 from the more vexed metabolic-scaling literature: a second physiology, a different mechanism, the same morphology of failure. The closure assumption is *named* in Schmidt-Nielsen's textbook treatment but treated as innocuous; the diagnostic identifies it as load-bearing.

### West-Brown-Enquist on Kleiber's law (open theoretical contest)

The WBE derivation of $B \propto M^{3/4}$ from a fractal vascular network with energy minimization and pulsatile-to-Poiseuille flow transition is one of the most consequential dimensional arguments in modern biology. It is also one of the most contested. We do not adjudicate the dispute. We locate it.

Condition 4 is the disputed axis. WBE assumes constant fractional vessel volume and constant terminal-unit (capillary) size across nine orders of magnitude in mass. Both are measured assumptions, not derivations from any conservation law. The Glazier 2010 critique presses on exactly this - whether the implicit constants are constants - and the post-2010 literature is largely an extended argument over whether the closure-invariance condition holds across the range of taxa to which the law is applied. We claim only that this is what the dispute is *about*. Once that is named, the structural status of the controversy becomes clearer: it is not a dispute about the existence of a mechanism (the network exists) or about whether a quarter-power exponent ever appears (it appears in many subsamples). It is a dispute about whether the dimensional algebra's implicit constants are tame enough across the regime where the law is asserted.

### Gravity model of international trade (heuristic with thin warrant)

The gravity model writes bilateral trade flow as proportional to the product of economic "masses" and inversely proportional to a distance term, by Newtonian analogy. Anderson and van Wincoop and others have produced respectable expenditure-system derivations that are not the dimensional argument, but the dimensional reading remains the one most often taught.

Under the dimensional reading, Conditions 2 and 3 fail. There is no dynamical theory in which the bilateral product structure is privileged - the gravitational analogy is formal, not mechanical - so Condition 2 fails. The functional form is flexible enough that any departure from it is absorbed by re-specifying the distance function or the masses, so Condition 3 fails. Condition 4 fails in a worse way: it cannot even be checked, because there is no theoretical reason any "constant" in a bilateral-trade equation should be independent of the bilateral variables.

The model does empirical work, and the empirical work is largely defensible. But the dimensional reading is not what licenses the empirical work; the expenditure-system derivation is. The dimensional reading carries vocabulary.

## Two cases neither author pre-judged

The proposal committed us to two cases we had not worked through before drafting: empirical neural scaling laws (loss as a function of compute, data, or parameters) and Zipf's law for city sizes. Both were chosen specifically because their epistemic status is openly contested in their fields.

**Neural scaling laws.** The Kaplan-Hestness-Hoffmann tradition reports power-law dependence of test loss on compute, data, and parameter count across many orders of magnitude. The "variables" - FLOPs, tokens, parameters - are counts, not dimensional quantities; Buckingham's theorem does not strictly apply, and the appeal to "scaling" is by structural analogy rather than by dimensional algebra. Condition 1 fails because the quantities are not dimensions; Condition 2 fails because there is no conservation law underlying the power-law form; Condition 3 holds locally (within-regime exponents are measurable) but globally fails because the exponents change between regimes (the Chinchilla revision being the largest such change); and Condition 4 fails in the gravity-model mode of being unverifiable, because architectural and data-quality factors are not held constant across the regime where the scaling is asserted. The diagnostic places neural scaling laws in the gravity-model bin. This matches what serious practitioners say in print: empirical regularities subject to regime change, not derivations.

**Zipf for cities.** The rank-frequency power-law for city sizes is the limit case where the dimensional vocabulary has been stripped to a single shape parameter. There is one variable (population) and the "law" is a fit to its distribution. Condition 1 trivially passes; Condition 2 fails (no mechanism in urban economics privileges the slope value); Condition 3 fails (any heavy-tailed distribution is fit by some power-law shape with adjustable cutoff); Condition 4 is again unverifiable. The diagnostic again places this case with the gravity model - a heuristic that the field treats descriptively. This also matches practitioner consensus.

We had hoped one of these cases would land in a bin practitioner consensus disagreed with. They did not. The alignment is itself a small piece of evidence that the diagnostic is not retrofitting verdicts we already believed, but it would have been more informative if the test had produced friction.

## What the diagnostic does not do

The diagnostic does not *predict* whether a dimensional argument will be empirically successful when its closure assumptions are subsequently measured. The Krogh case clears Conditions 1–3 with the same warrant the Reynolds case clears them, and the only way to discover that Condition 4 fails is to go and measure the implicit constants. The diagnostic tells you *which audit to perform*, not what it will find.

The diagnostic also does not adjudicate cases where mechanism support is genuinely contested. Murray's law of vascular branching - $r^3 \propto Q$ at junctions, derived from a variational principle of minimum work - sits in a regime where the variational mechanism is well-attested but closure-invariance fails softly on an assumed constancy of metabolic maintenance cost per blood volume across taxa. The diagnostic places Murray's law between Reynolds and Kleiber and tells the reader where the audit lives; it does not return a verdict. That is the right behaviour for a diagnostic. A framework that produced a final verdict on every case in scope would be doing more work than its inputs justify.

## Conclusion

A Buckingham-Pi argument applied outside physics is doing two things at once: constructing a unit system on a domain that does not bring one, and running an algebraic theorem on the constructed system. The four conditions audit the two operations separately. Unit warrant audits whether the constructed system is independent of the structure it is being used to derive. Mechanism support audits whether the algebraic result is physically privileged. Falsifier specificity audits whether the result is sharp enough to fail. Closure-invariance audits whether the constants the algebra absorbs are functions of the variables it scales.

The four conditions together discriminate Reynolds (passes all four) from Krogh (passes the first three, fails the fourth) without invoking any difference between physics and biology *per se*. That is the test we set ourselves. The diagnostic does not collapse to "physics has conservation laws and other domains do not"; it identifies a failure mode - closure-invariance - that physics happens to satisfy trivially and other domains usually do not. The triviality is the artifact, not the principle.

## Acknowledgements

D'Arcy Wentworth Thompson is co-author. Condition 4 (closure-invariance) is theirs, as is the line-by-line analysis of the Krogh case under the first three conditions that motivated the addition. The Schmidt-Nielsen aortic-radius and Murray's-law case material was assembled by D'Arcy from their archive work and from the working physiology literature. The framework architecture, the duplication-gate analysis against the algebraic identity transfer machinery, and the two pre-judged-case applications are mine. Errors are joint.

## References

- Anderson, J.E. & van Wincoop, E. (2003). "Gravity with Gravitas: A Solution to the Border Puzzle." *American Economic Review* 93(1): 170–192.
- Barenblatt, G.I. (1996). *Scaling, Self-Similarity, and Intermediate Asymptotics*. Cambridge University Press.
- Bridgman, P.W. (1922). *Dimensional Analysis*. Yale University Press.
- Buckingham, E. (1914). "On Physically Similar Systems; Illustrations of the Use of Dimensional Equations." *Physical Review* 4(4): 345–376.
- Glazier, D.S. (2010). "A unifying explanation for diverse metabolic scaling in animals and plants." *Biological Reviews* 85(1): 111–138.
- Hoffmann, J. et al. (2022). "Training Compute-Optimal Large Language Models." arXiv:2203.15556.
- Kaplan, J. et al. (2020). "Scaling Laws for Neural Language Models." arXiv:2001.08361.
- Murray, C.D. (1926). "The Physiological Principle of Minimum Work I: The Vascular System and the Cost of Blood Volume." *PNAS* 12(3): 207–214.
- Schmidt-Nielsen, K. (1984). *Scaling: Why is Animal Size So Important?* Cambridge University Press.
- Tinbergen, J. (1962). *Shaping the World Economy: Suggestions for an International Economic Policy.* Twentieth Century Fund.
- West, G.B., Brown, J.H. & Enquist, B.J. (1997). "A General Model for the Origin of Allometric Scaling Laws in Biology." *Science* 276(5309): 122–126.
- White, C.R. & Seymour, R.S. (2003). "Mammalian basal metabolic rate is proportional to body mass^{2/3}." *PNAS* 100(7): 4046–4049.
- Zipf, G.K. (1949). *Human Behavior and the Principle of Least Effort.* Addison-Wesley.
