# Response: Latent Prior in "When the Stadion Sets the Result"

## The Latent Independence Assumption

Ibn al-Haytham's piece treats the three inputs-shadow angle θ, distance d, and stadion length s-as *independent* sources of uncertainty. This independence is embedded in the variance decomposition: var(log C) = var(log θ) + var(log d) + var(log s). The piece does not present this as a modeling choice; it follows from the formula as a consequence of the data. Yet it is a substantive latent prior, one that shapes the reported variance split (5%, 45%, 50%) and remains unexamined.

Why is this latent? The piece introduces the variance formula as a mathematical fact about products of independent variables. It then verifies the decomposition empirically by running one-at-a-time sensitivity sweeps. But sensitivity analysis *confirms* the prior; it does not justify it. The prior-that θ, d, and s are independent-is not defended; it is simply applied.

## Why the Independence Assumption Is Fragile

The three quantities are not naturally independent. They are entangled in the historical record.

**Distance and stadion are metrologically confounded.** The "5,000 stadia" figure did not fall from the sky. It was established by bematists who measured using the stadion standard of their time. If historical metrology produced stadion-standard-specific distance estimates-if, for instance, a measurement recorded as "5,000 stadia in the Attic stadion" would be recorded as a different number in the Royal stadion-then d and s are not independent. They are inverse-related through the historical measurement process. A larger stadion value would have been paired with a smaller number of stadia in the original record, and vice versa.

The piece notices this dependency in passing. It observes that under the Attic stadion (157.5 m), "5,000 stadia" converts to 787.5 km, which matches the modern meridional distance "to within rounding." This coincidence is noted as remarkable. But it suggests a deeper fact: the 5,000-stadia figure may have been established *relative to the Attic stadion standard*, making it partially determined by that stadion choice rather than independent of it.

**The shadow angle is independent.** The angle θ is a single astronomical measurement at a single moment in history. Its uncertainty is measurement error. It does not depend on which stadion length we later adopt. This input is genuinely independent of the other two.

**Distance has two sources of uncertainty.** The distance d carries both measurement error (how accurately did the bematists measure?) and definitional uncertainty (which stadion did they use when recording the distance?). The second source is not independent of s.

## Formalization of the Dependence

A simple model of the dependence: Let s_true be the stadion standard used in the historical measurement, and let d_historical be the recorded distance in stadia. Then the modern-unit distance is d = d_historical × s, where s is our posterior belief about the stadion length.

If the bematists used a particular stadion standard s_true, and recorded d_historical stadia, the actual distance in modern meters is d_actual = d_historical × s_true, not d_historical × s (unless our s equals their s_true, which is unknown).

In the piece's framework, d is treated as an independent uncertainty about "the distance," with a lognormal prior centered at 5,000 stadia. But 5,000 stadia was measured using *some* stadion. If we later adopt a different stadion (via the mixture over s), we should adjust our belief about d, because the 5,000-stadia figure was produced under different metrological assumptions.

A correlation structure: if the Attic stadion was indeed the standard used, then our observed d = 5,000 stadia is a good estimate (small error, the measurement noise dominates). If the Engels stadion was the standard used, then our observed d = 5,000 is a *mis-denominated* distance, and we should believe a larger d in true meridional terms. This is a systematic dependence, not a random correlation, but it violates the independence assumption.

## How to Assess the Contribution of the Dependence

I propose three approaches:

**1. Conditional analysis: D-given-S**

Instead of a joint prior on (d, s) assumed independent, construct a joint prior that makes d conditional on the stadion choice. For each stadion s_i in the mixture, specify a prior on d that represents "what is the distance if this stadion standard was used?" The Attic stadion prior might center d at 5,000 stadia with 10% scatter (as in the piece). The Engels and Royal priors might center d at smaller values in stadia, acknowledging that if these larger stadion standards were in use, fewer stadia would have been recorded to cover the same meridional distance.

Run the Monte Carlo with this conditional joint prior. Compute the new variance decomposition. The difference between the independent-prior variance shares and the conditional-prior shares is the contribution of the dependence to the reported uncertainty.

**2. Sensitivity to correlation coefficient**

Parameterize a correlation coefficient ρ between log(d) and log(s). At ρ = 0, we recover the piece's independence assumption. At ρ = −1, increases in s are fully paired with decreases in d (the metrological confounding is complete). Run the Monte Carlo across a range of ρ values (perhaps ρ ∈ {−0.8, −0.5, −0.2, 0}). Observe how the variance decomposition and the pooled posterior change with ρ.

My hypothesis: as ρ becomes more negative (stronger confounding), the stadion's contribution to uncertainty will decrease, because the confounding partially absorbs the stadion variation into the distance prior. The angle's contribution should remain stable. The distance's contribution may shift, depending on whether the confounding reduces the effective degree of freedom in d.

**3. Historical validation**

Examine whether bematist measurements of long distances are recorded in sources that specify which stadion standard was in use. If Engels (1985) or comparable sources document distances recorded in multiple stadion standards, construct an empirical correlation from those data. This is the "ground truth" to which the prior should answer.

Alternatively, if metrology texts specify how different stadion standards were used in different periods or by different practitioners, that information can inform whether ρ = 0 is a reasonable assumption or a substantial approximation.

## Why This Matters for the Inference

The piece concludes that the stadion and distance together account for 95% of the propagated variance, while the angle contributes only 5%. This variance decomposition is the piece's most striking finding-it reframes the historical narrative away from celebrating the precision of the angle measurement toward acknowledging the uncertainty in the calibration inputs.

But if d and s are negatively correlated (confounded), the variance decomposition is overstating the true independence of sources. The reported 50% for stadion and 45% for distance might more accurately be something like "40% for stadion, 30% for distance, 15% for the confounding between them." The headline claim-that "the celebrated input is the smallest contributor"-survives. But the subsidiary claim-that stadion and distance are *independent* sources of uncertainty-does not survive the dependence assumption.

A reader would need to know: is the 1-σ width of 10–11% driven primarily by genuine independence of three uncertainties, or partially by our uncertainty about which metrological standard produced the recorded distance? These are different kinds of inference. The former is measurement error propagation. The latter is historical interpretation. The piece performs measurement error propagation while implicitly assuming the latter problem is solved.

## Conclusion

The independence assumption is latent, not latent because Ibn al-Haytham hides it, but latent because it is embedded in the formal apparatus without examination. The variance formula itself produces independence as an output. A careful reading of the priors reveals it is not justified by the historical evidence.

To assess its contribution: construct a conditional joint prior on (d, s) that reflects the metrological confounding, run sensitivity analysis across correlation strengths, and compare the variance decomposition to the independence case. The size of the difference will indicate whether the reframing of credit from angle to calibration is robust to a more careful treatment of historical dependence.
