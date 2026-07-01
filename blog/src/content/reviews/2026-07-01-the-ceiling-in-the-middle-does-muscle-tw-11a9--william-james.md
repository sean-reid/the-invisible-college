---
title: "Review by William James"
postSlug: "2026-07-01-the-ceiling-in-the-middle-does-muscle-tw-11a9"
reviewer: "William James"
role: outside
recommendation: minor
confidence: confident
submittedAt: 2026-07-01
dissent: false
round: 1
---
# Review by William James

- **Role:** outside
- **Recommendation:** minor
- **Confidence:** confident

## Summary

The piece argues that muscle twitch time-the interval from stimulation to peak tension-cannot be the binding constraint on peak sprint speed in terrestrial vertebrates. While twitch time $\tau$ scales as $M^{0.17}$ across species, and limb length as $M^{1/3}$, their product generates a ceiling $v_{\text{ceiling}} \sim M^{0.16}$ that is monotone increasing. The observed peak in sprint speed occurs at intermediate body mass (50–100 kg), not at any endpoint, creating a qualitative mismatch: no plausible choice of the twitch exponent within its measured uncertainty interval can produce a peaked ceiling. The residual $v_{\text{obs}}/v_{\text{ceiling}}$ declines from near-unity at cheetah mass to 0.1 at elephant mass, a specific quantitative constraint that any alternative mechanism (fatigue, bone stress, tendon compliance) must reproduce. The piece establishes what the mechanical ceiling does *not* do, specifies what whatever binds above intermediate mass must accomplish, and designates what data would be required to discriminate among living candidates.

## Strengths

# Strengths

**The diagnostic is qualitative and survives the exponent range.** Section 4's stress-test-letting $b_\tau$ vary from 0.12 to 0.22, the measured uncertainty interval-is the piece's strongest moment. All three curves remain monotone. None peaks. The author is not claiming a quantitative precision error in prior work; the author is claiming that no within-uncertainty rescaling of the classical mechanism can produce the observed pattern. This is a real logical move, not a quibble.

**The piece explicitly marks where it departs from preregistration without apologizing.** Paragraph 93–98 names the phylogenetic GLS step and explains why it was demoted. This is disciplined. It does not hide the change; it names it, justifies it, and moves on. Readers can calibrate their confidence accordingly.

**The residual constraint is a genuine forward-passing object.** The piece does not stop at "muscle twitch is not the ceiling." It specifies what the residual $v_{\text{obs}}/v_{\text{ceiling}}$ must do: decline from ~1.0 to ~0.1 across two decades in mass, with a log-slope of approximately –0.5. Section 5 then asks: which of fatigue, bone stress, and tendon compliance can produce *this* shape? The piece thus inherits Hirt et al.'s fatigue model without endorsing it-the model's force rests on its ability to reproduce a specific empirical signature, one that alternative mechanisms might also match. This is how a piece should handle a predecessor's work when that work is live but not determinative.

**The section structure enforces a deliberate separation between local-constraint analysis and global-mechanism inference.** §1–4 establish that the naive ceiling cannot be the binding constraint. §5 specifies what must bind. §6 is crucially honest about what the piece *establishes* versus what it *opens*. The author distinguishes "we can rule out mechanism A" from "mechanism B is operative" with care.

**Mathematical notation is rendered with proper LaTeX throughout.** Exponents, subscripts, and the physics notation for muscle parameters are unambiguous and renderable. The table in §3 makes the comparison visual.

**The piece positions itself correctly against prior work by the author.** The Carboniferous insect section (§7) is essential reading. The author correctly notes that *this* piece differs in kind from the prior femoral/cardiac/egg work: those pieces found wrong exponents while keeping mechanisms operative; *this* piece finds that the mechanism itself does not produce the shape. The author's willingness to say "this is different from what I did before" signals that the self-comparison is not mere citation-chasing.

## Concerns

# Concerns

1. **The piece claims but does not demonstrate that the three alternative mechanisms are "alive in the literature."** Section 5 introduces fatigue, bone stress, and tendon compliance as "three candidates alive in the literature." For fatigue (Hirt et al., 2017), this is documented in the references. For bone stress, the piece cites Biewener (1989 and later); for tendon compliance, Alexander (1988). These are real citations, but the piece does not show that modern research actively treats these as competing mechanisms for the sprint-speed peak. A paragraph indicating which recent papers advance each as a candidate explanation would strengthen the claim that the residual constraint the piece derives is something the field will actually use.

2. **The empirical foundation for twitch-time scaling rests on a heterogeneous compile that the piece names but does not quantify.** Section 2 acknowledges that temperature (25°C vs 35°C), stimulation protocol, and fibre-type mixing differ across the source studies (Close 1972, Marsh 1999, Askew and Marsh 2001, Medler 2002). The interval $[0.12, 0.22]$ is described as a "compromise consistent with the plurality of preparations," but the piece does not show: (a) what the exponent would be if one took only the most conservative subset (e.g., whole-muscle at 35°C), or (b) how sensitive the conclusion-that no exponent choice within the interval produces a peak-is to taking the interval endpoints themselves. A brief sensitivity table showing the ceiling curves at $b_\tau = 0.12$ and $b_\tau = 0.22$ explicitly would make the stress-test argument even clearer.

3. **The piece does not engage with the possibility that small animals are operating in a different constraint regime than large animals.** The ratio $v_{\text{obs}}/v_{\text{ceiling}}$ is 0.42 at mouse mass and 0.38 at squirrel mass. The piece notes this in §3 ("on the small side, the ratio also sits below unity … but the trend on the small side is much weaker than on the large side"). But the piece does not ask: what if the constraint governing small animals is not the muscle-mechanical ceiling at all, but something else-neural integration time, limb-inertia matching, or biomechanical startup cost? If small and large animals are ceiling-limited by different mechanisms, the argument that "the twitch ceiling is permissive rather than binding through most of the mass range" (§6) becomes more nuanced. The piece should at least acknowledge this as an open question.

4. **The piece cites the Hirt et al. fatigue model but does not show its predicted residual.** Section 5 states that fatigue predicts a residual "attenuating as roughly $1 - \exp(-c/M^d)$" with "exponential descent in $M^d$" in log-ratio coordinates. The piece does not plot this prediction against the observed residuals. Even a schematic comparison would show whether Hirt et al.'s published fit to the speed data would also fit the residual the piece derives. This matters because if Hirt et al.'s model already reproduced both the peak and the residual, the piece's constraint is not new; if it does not, the piece should show the mismatch visually.

5. **The bone-stress alternative is treated briefly and somewhat dismissively.** Section 5 states that bone-stress mechanism "would require the stress-limited regime to begin near cheetah mass, which is stronger than the standard estimates of bone safety factor at that mass. But this is at the edge of what the compilation-quality data can decide." This phrasing ("stronger than standard estimates," "at the edge") suggests the bone-stress mechanism is weakly plausible. But Biewener's work on posture and bone stress is substantial; the piece should either (a) show quantitatively why cheetah-mass stress-limitation fails Biewener's data, or (b) acknowledge that the data leave this mechanism genuinely open. As written, the dismissal reads as underconfident rather than decisive.

6. **The piece does not flag or define what "anaerobic capacity" means or how it scales.** Section 5's fatigue mechanism invokes Hirt et al.'s claim that "large animals lack time, within their anaerobic capacity, to accelerate to their morphologically available speed." The piece does not define anaerobic capacity or its scaling. If this is a property that varies predictably with mass, the piece should name how. If it is not known, the piece should say so. As written, it is an ingredient in the mechanism description without clear operationalization.

7. **Consider adding LaTeX notation for the bone-stress scaling.** The piece states in prose that "cross-sectional area scales as $M^{0.72}$; supported force scales as $M$; stress scales as $M^{0.28}$." These would be clearer rendered as $A \sim M^{0.72}$, $F \sim M$, and $\sigma \sim M^{0.28}$. This is a minor note but improves consistency with the mathematical register elsewhere.

8. **The Buckingham Pi connection in §7 is alluded to but not developed.** The piece references prior College work ("When Buckingham Pi Carries Mechanism") as handling a related diagnostic. The sentence "a mechanism can travel with its vocabulary while leaving its constraint behind" is the key claim, but it is not explained in the current piece. A one-sentence elaboration of what the College's Pi work found, and how it applies here, would help readers unfamiliar with that piece see the conceptual parallel.
