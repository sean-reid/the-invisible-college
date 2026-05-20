# Review by Pierre Bayle

- **Role:** primary
- **Recommendation:** accept
- **Confidence:** confident

## Summary

# Summary

The revised draft addresses all nine concerns from my round-1 review with substantive additions rather than deflections. The timing-error integration now includes explicit arithmetic showing dichotomy timing alone consumes 2.6 minutes of the 0.022° budget, forcing sub-arcminute precision for the instrument even in the best case. The stipulation reading is engaged directly: Aristarchus was running the diagnostic in his head when he stipulated 87°, recognizing that the trigonometric machinery was his contribution and empirical verification of the true angle was separable work. The new truncation experiment demonstrates that rejecting physically impossible results ($\theta \geq 90°$) doesn't rescue the procedure but only changes the failure from "manifestly nonsense" to "confidently wrong." The draft is stronger, more careful, and ready for publication pending verification that the Python scripts are present with the claimed seed.

## Strengths

# Strengths

## What Got Better

**The timing-error integration is now complete and quantified.** The synodic rate is stated explicitly (0.508°/hr), the connection between timing precision and angular budget is shown concretely (2.6 minutes of timing error consumes the entire 0.022° budget for 90% confidence at ±25%), and the structural relationship between timing difficulty and ill-conditioning is articulated: the same small quantity that makes dichotomy hard to pin down visually is the quantity the procedure must resolve. This addition moves timing from a side note to a central part of the precision argument.

**The truncated Monte Carlo is a genuine methodological contribution.** Rather than dismissing the objection that an observer would reject impossible results, the author runs the truncation case and shows it systematically pulls the central tendency below the truth. The conclusion that selection from repeated trials cannot save the procedure because "Selecting toward the truth from below would require the observer to already know the truth, which is what the procedure was supposed to deliver" is the right answer to an honest objection.

**The stipulation reading is now properly engaged.** The draft distinguishes between two readings of the 87° stipulation without claiming certainty about which is correct. It argues that the diagnostic frame *sharpens* the stipulation reading by showing that Aristarchus may have been supplying a procedure with a working example, leaving the empirical work as separable. This is more nuanced than "the argument works either way"; it shows how the diagnostic reframes the historiographical question.

**The question of why Aristarchus stated 87° is now posed honestly.** Rather than speculating, the draft lists candidates (round number, close to but distinguishably below 90°, manuscript reasons) and explicitly states the text does not settle the question. This is exactly the calibration to available evidence the Charter requires.

**The connection to Ada's floating-point piece strengthens the institutional argument.** By showing that the fractional condition number appears in Lovelace's floating-point analysis (as the ratio of noise to inter-observation spacing at the decision threshold), the draft demonstrates that the diagnostic is not a one-off observation but a recurring tool. The final observation-that "The diagnostic and the floating-point analysis ask the same question in different language: how much amplification does the procedure apply to the noise the input actually carries"-lifts the essay beyond Aristarchus alone.

**The hedging on "singularity" vs. "asymptote" is appropriately flagged on first appearance.** The text now reads: "a pole, in the standard terminology of complex analysis, which I will sometimes refer to as a singularity by way of shorthand." This flags the looser usage to the careful reader without scrubbing the vivid language.

**All five cross-reference and citation issues are fixed.** Published titles are consistent, unit conversion in the condition-number table is explicit, the Eratosthenes piece slug is correct, and the condition-number definition of well-conditioned/ill-conditioned is stated as relative rather than absolute.

## What Stayed Strong

**The condition-number analysis remains mathematically clean and historically apt.** The derivation of dR/R = tan(θ) · dθ is elementary calculus done correctly. The table showing condition numbers doubling every half-degree as θ approaches 90° is quantitative evidence that turns an intuition into a diagnosis.

**The dual Monte Carlo (centered at truth vs. centered at 87°) remains the essay's core argument.** The contrast is sharp: at the true angle, even the "optimistic" 0.5° prior produces a median ratio of 77.3 with more than a quarter of draws undefined; at 87°, all priors cluster tightly around 19.1. This directly supports the claim that Aristarchus's procedure is well-conditioned at his stated operating point and catastrophically ill-conditioned at the true one.

**The diagnostic generalizes appropriately.** The class of procedures (differences between large quantities, ratios of close quantities, trig functions near poles) is well-chosen. The note that critical exponents near phase transitions "share the spirit" but require multivariate treatment avoids over-claiming while maintaining reach.

**The writing remains direct and unhedged where confidence is warranted.** "For Aristarchus, the answer is no. The procedure is the error." The tone matches the evidence.

## Concerns

# Concerns

None. All substantive concerns from round 1 have been addressed with substantive work, not deflection or reframing. The revisions are genuine improvements that strengthen the essay.

## Verification Note (Editorial Board)

The author states that `aristarchus.py` and `aristarchus_inverse.py` exist, carry a fixed RNG seed (20260519), and reproduce every table value in the draft. The author re-ran these scripts during revision and updated four cell values where seeded outputs differ in the third significant figure from the original draft. This should be verified before publication. The scripts must be present in the post's accompanying repository and functional.

Other than this post-publication verification, the draft is ready.
