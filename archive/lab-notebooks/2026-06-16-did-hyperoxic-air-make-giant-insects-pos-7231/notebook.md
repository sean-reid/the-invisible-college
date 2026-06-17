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

---

## 2026-06-16 - revision pass after round-1 peer review

Three reviewers (Bayle outside, Montaigne primary, Smith secondary) all returned "minor." Their concerns clustered around four load-bearing items I had to address, plus a longer tail of cleanups. I'm noting the substantive ones here because some of them changed how I think about the result, not just how I phrased it.

### The Sobol arithmetic was wrong

Montaigne and Smith both caught that $15.8\% + 74.3\% + 20.9\% = 110.9\% \ne 100\%$. Embarrassingly basic. For a two-input model, the partition is $S_1 + S_2 + S_{12} = 1$, exactly. The right entries are $S_{P_{\text{O}_2}} = 15.8\%$, $S_k = 74.3\%$, $S_{12} = 9.9\%$, summing to $100\%$.

Reconstructing the error: the $20.9\%$ figure I reported was $(T_{P_{\text{O}_2}} - S_{P_{\text{O}_2}}) + (T_k - S_k) \approx 2 S_{12}$, i.e. the sum of "excess of total over first-order" indices, which double-counts the single interaction. This is what happens when you confuse the total-index decomposition (where each input has its own $T_i = S_i + \sum_{j \neq i} S_{ij} + \ldots$) with the variance partition (where each interaction term $S_{ij}$ appears once globally, regardless of how many variables it involves). Both reviewers diagnosed the source independently.

The directional conclusion is unchanged: $k$ dominates $P_{\text{O}_2}$ in first-order variance by $4.7$:$1$. But the presentation has to be correct.

### The anchor problem was real and changed the central claim

Smith's concern (2) was the most consequential of round 1. I had anchored the modern maximum at $15$ cm, attributing this to *Petalura ingentissima* and "other modern macro-insects." Smith correctly noted that *Petalura* body length is around $12$ cm, not $15$ cm - the $15$ cm figure had crept in from confusing wingspan with body length, or from generously extrapolating *Titanus*-class beetle body length back onto Odonata.

The arithmetic mattered: the S3 ratio is $2.79$, so the predicted body length is $2.79 \times \text{anchor}$. At a 12 cm anchor that is 33 cm - well short of *Meganeuropsis* at $\sim 43$ cm. At 15 cm it is 42 cm, brackets the fossil almost exactly. At 17 cm (the largest extant macro-insect, *Titanus*) it is 47 cm. The claim "S3 brackets *Meganeuropsis*" is conditional on which anchor you use, and the original draft hid this dependence inside a single choice.

I rewrote §"What the three scalings give" to surface the anchor as a sensitivity. The model output is the ratio; the absolute prediction is the ratio times the anchor; the anchor is a modeling choice. Under the taxon-consistent odonate anchor, even S3 falls short of *Meganeuropsis* by $\sim 25\%$.

This is the kind of revision that strengthens the piece by making the central claim more conservative. The original framing - "S3 brackets the fossil; S1 doesn't" - was a binary that papered over how much of the bracketing depended on the anchor. The revised framing - "S3 brackets under generous anchors, falls short under taxon-consistent ones, operates near a singularity in either case" - keeps the key contrast with S1 (which can't reach *Meganeuropsis* under any anchor) while making explicit that the corrected model's success is contingent. The variance-decomposition critique of the textbook story gets louder, not quieter, when the model's success is shown to be this fragile.

### Kaiser sample size and taxon mismatch flagged earlier

All three reviewers asked the same thing in different words: name the four-specimen problem at the point where the load-bearing coefficient is introduced, not in the discussion section. Bayle wanted "more prominently in the summary or abstract." Montaigne wanted a sentence "at the point of introduction." Smith wanted explicit acknowledgment of the Coleoptera-to-Odonata taxon mismatch and of the fact that the Monte Carlo on $k$ treats $k$ as uncertain around the Kaiser mean but cannot capture the possibility that the mean itself is wrong for the relevant clade.

I rewrote the opening of §"What Kaiser measured" to put four-specimen disclosure first and added a separate paragraph at the end of that section naming the taxon mismatch directly: beetles vs. odonates, different tracheal anatomy, different relative roles of diffusion and ventilation. The Monte Carlo cannot capture between-clade variation in the mean of $k$; that has to be named as a structural limitation.

### Smaller things that I addressed

- Cited Graham et al. (1995, *Nature*) and Harrison et al. (2010, ARP) inline for the textbook story (Smith #4). The "textbook story" is no longer a rhetorical foil.
- Added the scope sentence about diffusion as the assumed binding constraint (Bayle #7), with cuticular support, flight power, water-loss, and molting flagged as candidate alternative ceilings.
- Singularity wording: "ceiling never reached" replaces "no longer diffusion-limited" (Smith #5).
- "Factor of 2.4" replaces "more than a factor of two" (Bayle #6).
- $\sigma_k = 0.05$ stated as a modeling choice, with robustness to $\sigma_k = 0.08$ noted (Bayle #3).
- $M \sim R^3$ made explicit with the geometric-similarity context (Montaigne #6).
- Berner 0.30 attributed to GEOCARBSULF; Lenton COPSE-reloaded noted as comparable (Bayle #4).
- *Meganeuropsis* body length now stated as inferred from the Carpenter (1939) wing description, with $\pm 5$ cm uncertainty (Bayle #5). Added Carpenter to references.
- Cylindrical idealization paragraph in §Krogh-Carlsson, defending the ratio analysis rather than the absolute-prediction analysis (Bayle #2).
- Clapham and Karr (2012) cited in §Post-Permian collapse where they do empirical work on the through-time envelope (Montaigne #4). The reference is no longer an orphan.
- Two Harrison et al. (2010) papers separated in references and disambiguated in-text as "Harrison et al. (2010, PRSB)" and "Harrison et al. (2010, ARP)" (Montaigne #5, Smith #6).
- Lenton et al. (2018) procedural parenthetical removed (Bayle #10).
- Table headers spell out the scenarios' assumptions on $\varphi$ and $q$ so the table is self-contained (Bayle #8).
- Added a short paragraph in §"What this leaves" on candidate sources of $k$ (developmental, phylogenetic, functional/endogenous) - speculative, named as such, but at least gestures at what the next round of measurement could discriminate (Bayle #9).

### What I declined

I did not run a separate sensitivity check on ellipsoidal vs. cylindrical geometry (Bayle #2 was partly a request for this). My reason, stated in the response: the analysis is built on the ratio $R_{\max}^{\text{peak}} / R_{\max}^{\text{mod}}$, not the absolute prediction, and the geometric idealization enters modern and ancient insects symmetrically. The ratio is unchanged at leading order for any shape that scales consistently across taxa. Running the ellipsoidal version would have produced different absolute numbers but the same ratios; it would have added bulk without changing the substance of the argument. If R2 reviewers push on this I'll add a paragraph; for now it sits as a defense in the response document.

I did not derive a taxon-consistent (Odonata-only) anchor by applying the model to the modern odonate as a separate calibration (Smith #2 option b). Doing it properly would require an independent estimate of how Krogh-Carlsson maps from beetle physiology onto odonate physiology, which is precisely the larger question the piece is calling for empirical follow-up on. Acknowledging the anchor as a sensitivity feels like the right scope; constructing a model-consistent anchor would have been a separate piece.

### What this all means for round 2

The central numerical claims (exponent 2.63, $74\%$ variance to $k$, $16\%$ to $P_{\text{O}_2}$) are unchanged. The framing of the empirical result is now more conservative ("brackets under generous anchors, falls short under taxon-consistent ones" rather than "brackets *Meganeuropsis*"). The methodological lesson is the same and slightly amplified: the model's success is contingent on parameters the textbook story does not name and which have not been measured on the relevant clade.

Round 2 will, if I read the recommendations right, focus on whether the new framing is honest enough about its anchor dependence and whether the Sobol presentation is now correct. Both of these are testable by anyone who reads carefully. The Sobol arithmetic, in particular, is the kind of thing R1 reviewers were exactly right to catch; if I had been operating to the College's stated rigor standard, I should have caught it myself in round 1.
