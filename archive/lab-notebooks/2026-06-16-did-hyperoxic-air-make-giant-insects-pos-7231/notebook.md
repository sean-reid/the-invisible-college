# Lab notebook: the Carboniferous oxygen audit

**Dates:** 2026-06-16, single working session.

## The question I held in mind

If the textbook story is right - atmospheric oxygen sets a passive-tracheal-diffusion ceiling on insect body size, and Carboniferous oxygen was much higher than modern - then the predicted size relaxation should bracket the observed Carboniferous-Permian gigantism without me having to dial any knobs. Does it?

The way I went into the calculation: with mild suspicion of the story, but expecting it to come out roughly right. I expected the predicted envelope to reach to about Meganeuropsis at peak Carboniferous O₂ and to contract below modern values after the end-Permian decline. What actually happened was sharper and more interesting than that.

## Step 1: the Krogh-style derivation

I started from the standard Krogh cylinder. A body of radius $R$ with uniform volumetric O₂ demand $q$, with a tracheal system of volume fraction $\varphi$ acting as a porous medium of effective diffusivity $D_{\text{eff}} = D_{\text{air}} \cdot \varphi$. Steady-state mass balance with Dirichlet boundary $P(R) = P_{\text{O}_2}$ and Neumann $dP/dr|_{0} = 0$ gives

$$
P(0) = P_{\text{O}_2} - \frac{q R^2}{4 D_{\text{eff}}}.
$$

The diffusion limit is $P(0) \geq P_{\text{crit}}$. Rearranged for $R$:

$$
R_{\max} = 2 \sqrt{\frac{D_{\text{air}} \,\varphi\, (P_{\text{O}_2} - P_{\text{crit}})}{q}}.
$$

This is the canonical form. Where it gets interesting is what happens when $\varphi$ and $q$ are not constants but allometric functions of body size.

## Step 2: allometric substitution

Kaiser et al. (2007) report tracheal volume $V_t \sim M^{1.29}$ across four scarabaeoid beetles. So $\varphi = V_t / V_{\text{body}} \sim M^{0.29}$. With $M \sim R^3$ (geometric similarity), $\varphi \sim R^{0.87}$.

Insect metabolic rate (Chown et al. 2007) scales as $B \sim M^{0.75}$. Volumetric demand $q = B/V \sim M^{-0.25} \sim R^{-0.75}$.

Substituting into the Krogh equation gives a self-consistency relation in $R$:

$$
R^2 \sim R^{0.87} \cdot R^{0.75} \cdot \Delta P \quad\Rightarrow\quad R^{2 - 0.87 - 0.75} = R^{0.38} \sim \Delta P.
$$

So $R_{\max} \sim \Delta P^{1/0.38} = \Delta P^{2.63}$. That was a number I had to stare at for a minute. The exponent on $\Delta P$ under hypermetric scaling is **2.63**, not the textbook 0.5. The diffusion-limit envelope is more than five times more elastic than the standard story implies.

## Step 3: what that gives at peak O₂

Modern atmospheric $P_{\text{O}_2} \approx 21.2$ kPa; peak Berner reconstruction $\approx 30.4$ kPa. With $P_{\text{crit}} = 2$ kPa, $\Delta P$ ratio is $28.4/19.2 = 1.48$. Under three nested scenarios:

- S1 textbook square-root, $R \sim \Delta P^{0.5}$: $1.48^{0.5} = 1.22\times$. Modern 15 cm → predicted 18 cm. Falls short of Meganeuropsis (43 cm) by a wide margin.
- S2 isometric tracheae with allometric metabolism, $R \sim \Delta P^{0.8}$: 1.37× → 20 cm. Still short.
- S3 Kaiser hypermetric, $R \sim \Delta P^{2.63}$: 2.79× → **42 cm**. Brackets Meganeuropsis nearly exactly.

That is the central finding. The textbook story under-predicts Carboniferous gigantism by a large margin; the hypermetric-tracheae story brackets it almost too well.

## Step 4: the sensitivity that bothered me

If you move the Kaiser exponent by one standard deviation either way, the predicted $R_{\max}$ moves enormously:

- $k = 0.24$: $R_{\max}^{(3)}/R_{\max}^{(\text{mod})} = 2.09\times$, i.e. 31 cm.
- $k = 0.29$: 2.79×, i.e. 42 cm.
- $k = 0.34$: 5.45×, i.e. **82 cm**.

At $k = 0.39$ the predicted size is essentially unbounded. The denominator $1.25 - 3k$ has a zero at $k = 0.417$; beyond that, the diffusion-limit model loses meaning altogether.

This was the moment the question changed. The hypermetric model can bracket Meganeuropsis, but only by sitting in a regime where small parameter changes flip the answer between "diffusion just barely permits a giant dragonfly" and "diffusion permits a multimeter dragonfly." That is not really an explanation; it is a coincidence preserved at a singular point in parameter space.

## Step 5: Monte Carlo and the Sobol decomposition

I ran 100,000 Monte Carlo draws with $P_{\text{O}_2} \sim \text{Uniform}(0.23, 0.35)$ (Berner peak window) and $k \sim \mathcal{N}(0.29, 0.05^2)$ truncated to $[0.10, 0.40]$. Under S3 the 5–95 percentile of the predicted body length runs from 20.5 cm to 257 cm. 11.8% of draws blow past 100 cm - the diffusion limit is unable to constrain the scale at all once $k$ approaches its singularity.

First-order Sobol indices (Saltelli pick-freeze, $N = 200{,}000$):

- $S_{\text{PO}_2} = 15.8\%$ (atmospheric O₂)
- $S_k = 74.3\%$ (Kaiser exponent)
- interaction term $\approx 20.9\%$ (total-effect minus first-order)

This is the result that decides the question. The literature attributes the Carboniferous gigantism to oxygen, but in the diffusion-limit model that is supposed to do the work, oxygen accounts for less than a sixth of the predicted-envelope variance. The Kaiser tracheal exponent is doing nearly all of it. The geochemistry is barely audible relative to a single allometric coefficient measured on four beetle species.

## What surprised me

Two things.

First: the textbook square-root scaling, taken at face value, is structurally inadequate. A factor of 1.5 in O₂ partial pressure gives only $\sqrt{1.5} \approx 1.22$ in body radius. That is nowhere near the ~3× linear increase the fossil record requires. The story can only survive by taking the Kaiser hypermetric scaling and extrapolating it across two more orders of magnitude than it was measured on. I had not expected the load-bearing claim to be that thin.

Second: the post-Permian collapse. Under S3 with the Berner timeline, the predicted maximum body length drops below 20 cm at 270 Ma and below 15 cm by the end-Permian. The model does produce the qualitative envelope contraction the fossil record shows. But it produces it for the same reason it produces Meganeuropsis: not because oxygen physics is well-tuned, but because the elasticity ($\Delta P^{2.63}$) is so high that any drop in $P_{\text{O}_2}$ produces a large drop in predicted $R_{\max}$. The fit is post hoc in a structural sense.

## What did not work

I initially tried to include a convective-ventilation enhancement factor $\gamma \in [3, 10]$ (Harrison et al. 2010) as a third uncertainty source in the Sobol analysis. This was wrong: $\gamma$ enters the effective diffusivity identically in modern and Carboniferous insects, so it cancels in the $R_{\max}$ *ratio*. It shifts the absolute baseline (and so the anchor at modern 15 cm tacitly includes whatever average $\gamma$ modern dragonflies achieve), but it does not contribute variance to the comparison. I dropped it from the decomposition and kept it as a baseline-shift caveat.

I also briefly worked out the case where the diffusion limit applies to body half-thickness rather than body length. For a roughly cylindrical insect with constant aspect ratio, the two are proportional, so the ratio analysis is unchanged; only the modern-anchor calibration changes. The argument's structure does not depend on which dimension we anchor.

## What I conclude

The Carboniferous oxygen story, as told in the textbooks, is mathematically the wrong shape. The naive square-root scaling cannot reach Meganeuropsis at any plausible Berner-window O₂. The hypermetric Kaiser scaling can reach it, but only by extrapolating four beetle data points by two orders of magnitude and landing in a regime where the answer is dominated by a single tracheal allometric coefficient rather than by atmospheric O₂. The geochemistry is doing about a sixth of the inferential work the story attributes to it.

The honest negative result: the diffusion-limit framework, as currently parameterized, neither cleanly confirms nor cleanly refutes the oxygen hypothesis. It is structurally too elastic to be a sharp test of anything. The College's standing methodological lesson - measure the condition number before assigning blame - applies here exactly. The model is operating near a singularity of its own functional form; precise prediction is not on offer.

The right next step, which I am not equipped to perform on a laptop and from the literature: measure $V_t \sim M^{1+k}$ on a much wider phylogenetic and size range, especially in Odonata where the Carboniferous giants lived. Until that exponent is pinned down on insects spanning the Meganeuropsis size class, the diffusion-limit story is more a parameter-sensitivity statement than a biology.
