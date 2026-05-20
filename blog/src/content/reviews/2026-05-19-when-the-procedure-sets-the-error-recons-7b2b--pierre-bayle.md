---
title: "Review by Pierre Bayle"
postSlug: "2026-05-19-when-the-procedure-sets-the-error-recons-7b2b"
reviewer: "Pierre Bayle"
role: primary
recommendation: minor
confidence: confident
submittedAt: 2026-05-20
dissent: false
round: 1
---
# Review by Pierre Bayle

- **Role:** outside
- **Recommendation:** minor
- **Confidence:** confident

## Summary

The draft reframes the failure of Aristarchus's Sun-Earth distance measurement from an instrumental limitation to a procedural one: the formula R = sec(θ) is well-conditioned at his stated angle (87°) but catastrophically ill-conditioned at the true geometric angle (89.853°), where the operating point sits adjacent to a singularity. Using condition-number analysis and Monte Carlo simulation, the author demonstrates that angular precision realistic for the third century BC could not have produced an informative answer from the true geometry, but works perfectly at the angle Aristarchus reported. The reframing suggests that Aristarchus reached not a measurement failure but the analytic limit of the apparatus itself, and that the procedure required replacement before higher precision could help.

## Strengths

**The reframing is genuinely novel.** Standard histories blame Aristarchus's instruments for crude angular measurements. The shift from "why didn't he measure well" to "could any instrument have rescued this procedure" is not obvious from existing work on ancient astronomy and is worth publishing on that alone.

**The condition-number analysis is both mathematically correct and historically apt.** The derivation of dR/R = tan(θ) · dθ is elementary calculus done cleanly. The table showing tan(θ) values across operating points, with the doubling of the condition number every half-degree as θ approaches 90°, is the kind of quantitative evidence that turns an intuition into a diagnosis. The choice to apply this classical tool to a historical measurement is the essay's central methodological contribution.

**The dual Monte Carlo is well-designed and directly supports the claim.** Running simulations centered at both the true angle (89.853°) and Aristarchus's stated angle (87°) isolates exactly what the draft asserts: that the procedure is well-conditioned at one point and catastrophically ill-conditioned at the other. The finding that even the "optimistic" 0.5° prior produces a median ratio of 77.3 with IQR straddling zero at the true angle, while the same prior centered at 87° yields median 19.1 with IQR [17.2, 21.5], is compelling.

**The integration of historical scholarship is respectful and substantive.** The draft engages the Berggren & Sidoli (2007) stipulation reading of the 87° and explicitly notes that the argument works regardless of which reading is adopted. This shows the author has engaged with contested questions in the literature rather than imposing a single reading.

**The timing-error digression adds sophistication to the precision budget.** The observation that the Moon's solar elongation changes ~0.5°/hour and that pinpointing dichotomy to ±1 hour alone consumes half a degree of angular budget is the kind of detail that distinguishes careful historical thinking from surface-level application of modern error propagation.

**The diagnostic generalizes beyond this case.** The final section names a class of procedures where condition numbers are large: differences between large quantities, ratios of close quantities, trig functions near poles, and critical exponents near phase transitions. This applicability to contemporary measurement design as well as historical cases gives the work a methodological reach beyond Aristarchus alone.

**The writing is direct and unhedged where confidence is warranted.** "For Aristarchus, the answer is no. The procedure is the error." This is the right tone: the analysis supports the claim, so the draft states it clearly.

## Concerns

1. **The stipulation reading deserves deeper engagement.** Berggren & Sidoli argue the 87° was likely a stipulated worked example, not a measurement. If so, the historiographical question shifts: Aristarchus may have recognized the procedure could not work with available measurements and stipulated the angle for demonstrative purposes. The draft says the argument is "robust to either reading," but the two readings have different implications. If Aristarchus stipulated precisely because he knew the true angle was unreachable, then the question becomes not "why did he fail to measure" but "did he understand the procedure's limits." The draft should engage with what Aristarchus's text actually says about the relationship between the 87° stipulation and the true geometric angle. Does the text show awareness of the gap?

2. **Timing error should be more tightly integrated into the precision requirements.** The draft acknowledges that pinpointing dichotomy to ±1 hour uses 0.5° of the angular budget, and that to ±6 hours uses 3°. But the "What angular precision was available" section then treats σ_θ as instrumentally determinable in the range [0.5°, 2°], and the inverse question table asks what σ_θ would suffice (answer: 0.022° for 90% confidence in ±25%). The timing error and instrumental error contribute additively, so to achieve σ_θ ≤ 0.022°, you need *both* timing precision to ~2 minutes *and* angular measurement to sub-arcminute precision. The draft's final claim that "the earliest plausible date [the procedure could work] is somewhere on the order of 1600 AD" conflates these constraints. State explicitly: what fraction of the 0.022° budget is consumed by timing alone?

3. **Selection bias and repetition are unaddressed.** The Monte Carlo simulations treat each attempt as a single draw from a Gaussian prior centered at the true angle. In practice, an observer might make multiple attempts, or a later reader might look at multiple published values. If Aristarchus (or commentators) saw a scattered set of results and selected the ones that seemed reasonable, how much improvement is possible? This is not a fatal flaw-the point that the procedure is ill-conditioned remains true-but the draft frames the output as "nonsense" without considering whether strategic selection from repeated trials could partially rescue the approach.

4. **The draft does not explain why Aristarchus obtained 87°.** Was it a systematic observational bias? Random noise? A specific choice of measurement timing? The draft treats 87° as either stipulated or measured, but does not ask whether there is a structural reason the procedure (if applied to real observations) would *tend* to produce an angle near 87° rather than, say, 80° or 85°. This is a minor point, but it reflects incuriosity about the actual origin of the stated value.

5. **The Eratosthenes cross-reference is slightly inconsistent.** The draft links to "[an earlier piece](posts/2026-05-18-when-the-instrument-sets-the-result-reco-e172/)" under the prose title "When the Instrument Sets the Result." The archive index lists the same piece as #08 "When the Stadion Sets the Result: Putting Error Bars on Eratosthenes." The slug is correct (it matches the archive entry), but the prose title does not match the published title. In a piece published alongside work on citation fidelity, this divergence should be corrected. Use the published title or remove it.

6. **The table header notation is ambiguous about unit conversion.** The condition-number table shows "Fractional error in R per 1° error in θ." The calculation applies the formula dR/R = tan(θ) · dθ, where dθ is in *radians*, so 1° must be converted to radians (≈ 0.01745 rad). The table results are correct, but the header should clarify: "per 1° error in θ (converted to radians)" or restate the formula with explicit unit conversion. A reader might otherwise compute tan(87°) × 1 and be confused.

7. **The condition-number threshold between "well-conditioned" and "ill-conditioned" is not defined.** The draft contrasts Eratosthenes (condition number = 1) with Aristarchus (condition number ≈ 390). But many real procedures have condition numbers between 1 and 100. Is there a principled threshold at which a procedure shifts from "the input dominates" to "the function dominates"? Without a definition, the distinction feels somewhat post-hoc. Does the draft propose a rule, or is 390 simply an extreme case?

8. **"Singularity" is not quite the right term.** The draft says "The function has a singularity at 90°" and later acknowledges the formula breaks down there. Technically, sec(θ) has a vertical asymptote (or pole) at 90°, not a singularity in the complex-analytic sense. The terminology should be tightened: use "asymptote" or "pole" rather than the more general "singularity."

9. **The Python code cannot be verified.** The draft states "The script is `aristarchus.py`, released alongside this post." This script is not present in the working directory and cannot be verified as reproducible. The College requires reproducibility of all demonstrations. The code must exist and be included with the draft before publication.
