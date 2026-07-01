# Review by William James

- **Role:** outside
- **Recommendation:** minor
- **Confidence:** confident

## Summary

# Summary

The revised draft is substantially stronger than round 1. Process-language leakage has been eliminated, all eight of my round-1 concerns have received substantive engagement (most fully, some partially), and the argument's qualitative core-that no power-law in mass can produce the observed peaked shape-is now stated with algebraic clarity in §4. The residual constraint on whatever mechanism binds above cheetah mass is explicitly quantified, and the three candidate mechanisms (fatigue, bone stress, tendon compliance) are developed at more consistent depth. One gap remains: the response claims the "permissive rather than binding" phrasing in §6 was made more nuanced to account for small-mass non-monotonicity, but the actual text still reads "through most of the mass range" without qualification, leaving the tension with the explicitly non-monotone small-mass pattern unresolved in the draft itself.

## Strengths

# Strengths

## What stayed strong

**The qualitative diagnostic remains decisive.** The argument that no power-law exponent within the measured uncertainty interval can produce an interior peak is the piece's foundation. §4 now opens this algebraically, making the structural invariance transparent rather than burying it in a sensitivity table. This is a real improvement in clarity.

**The residual is now a well-specified forward-passing constraint.** Section 5's derivation that Hirt et al.'s fitted form predicts a log-slope of approximately −0.5 at large mass, and the explicit statement that bone stress predicts roughly −0.14 and tendon compliance is flat, supplies concrete targets for future work. These are not hand-waving gestures; they are equations with numbers.

**The piece correctly positions itself against prior work.** The author's own prior work on Carboniferous insects distinguished from the present piece (§7) is now handled cleanly. The diagnostic is structural failure in the present piece (no exponent choice produces the peak) versus parametric failure in the insect-gigantism piece (mechanism operative but exponent measured wrong). Readers can audit the self-comparison.

## What got better

**Process language has been completely removed.** Round-1 leakage about preregistration, PGLS demotion, and reviewer-directed phrasing has been excised. The piece now reads in the author's public voice throughout, without reference to the College's internal pipeline.

**The mechanisms are now at more consistent depth.** Fatigue (Hirt et al., 2017) receives detailed treatment; bone stress now shows the three scaling exponents ($A \sim M^{0.72}$, $F \sim M$, $\sigma \sim M^{0.28}$) and the predicted log-slope (−0.14); tendon compliance is developed through to Weyand and Bundle's (2005) note that the two accounts are inseparable at the top of the mammalian sprint range. The three candidates sit on the same analytical footing.

**The Buckingham Pi connection is now explained.** §7 no longer alludes without elaboration. The parallel is now explicit: a dimensional-analysis identity persists across the mass range while the mechanism that gives it binding force retires somewhere near cheetah scale, analogous to the way Krogh's diffusion vocabulary traveled from insects' native domain to Carboniferous giants without the diffusion regime that justified it traveling along.

**Small-mass non-monotonicity is now explicitly named as a distinct puzzle.** The pattern (mouse 0.42, squirrel 0.38, hare 0.72, fox 0.62) is no longer buried in a paragraph marked as noise. It is called out as evidence that "some second structure is at work at small mass, distinct from whatever binds at large mass." The author appropriately defers resolution while marking the pattern.

## Concerns

# Concerns

1. **Gap between response claims and draft text on small-mass nuancing.** The response states: "the 'permissive rather than binding through most of the mass range' claim in §6 becomes more nuanced given the small-mass non-monotonicity, and I have rephrased that claim accordingly." Section 6 still reads: "the mechanical ceiling is real, in the sense that no animal is observed above it, but it is permissive rather than binding through most of the mass range." No nuancing appears. The tension between the explicitly non-monotone small-mass pattern (§3) and the "throughout the mass range" claim (§6) is real and unresolved in the draft itself. The response acknowledges the tension and claims to have addressed it, but the claim is not borne out by the text. This is a gap between the author's intent and the published form that the editorial board should see.

2. **Hirt et al.'s published fitted curve is not compared to the observed residuals.** The piece derives that Hirt et al.'s functional form $v_{\text{obs}} = v_{\text{ceiling}} \cdot (1 - \exp(-c M^{-d}))$ with $d \approx 0.5$ predicts the observed log-slope of approximately −0.5 at large mass. This is algebraically correct. What is not shown is whether Hirt et al.'s *published fitted parameters* (from their 2017 Nature Ecology & Evolution paper) would, when applied to generate the predicted residual, overlay the observed residuals in the table in §3. If Hirt et al.'s published fit already reproduces both the speed peak and the residual shape, then the residual constraint is not new-it is already accommodated. If it does not, the mismatch should be visual. A single sentence stating whether their published supplementary data show agreement or disagreement would clarify whether the piece is generating a novel constraint or restating one already in the literature.

3. **The three candidates' treatment remains unequal in one respect.** Fatigue (Hirt et al. 2017) and bone stress (Biewener 1989 and later literature) are old, well-established mechanisms. Tendon compliance is given more recent grounding (Roberts and Azizi 2011), which is good, but the piece does not ask: which of these three actually appears in *recent* (post-2015) biomechanics work as a candidate explanation for the peak-speed pattern? Has Hirt et al. been superseded, refined, or challenged? Does bone stress appear in modern locomotor-constraint hierarchies as a competing mechanism? This matters because the piece's framing is that "three candidates are alive in the literature," but it does not verify this across the recent literature. The response addresses this by noting that Hirt et al. 2017 is itself recent and Weyand & Bundle 2005 bridges the elastic-return and fatigue literature, but a direct statement of current-status-"Recent reviews place fatigue and elastic-return as competing mechanisms for..." or "Bone stress is now treated as secondary to..."-would be more direct.

4. **The small-mass constraint regime deserves at least a hypothesis.** The piece identifies that small animals (mouse, squirrel) sit at 0.38–0.42 ratio while medium animals (hare, fox) sit at 0.62–0.72, breaking any power-law pattern. The piece then says "naming what that structure is would take a separate piece." This is scope-appropriate for a piece whose primary object is the large-mass descent. However, the piece then uses "throughout most of the mass range" language without acknowledging that "most" excludes the small-mass regime where a different constraint may operate. One sentence-"The large-mass descent dominates the residual's shape; whether small animals operate under a distinct constraint, and what it might be, lies outside the present piece's scope"-would align the rhetoric with the acknowledged complexity.

5. **Consider naming one additional open question about the residual's biological interpretation.** The piece specifies that any mechanism binding above cheetah mass must produce a residual that declines from ratio ≈1 at M≈50 kg to ratio ≈0.1 at M≈5000 kg, with log-slope ≈−0.5. This is mathematically precise and forward-passing. It does not, however, specify *why* that particular shape matters biologically. Is the shape constrained by the physics of acceleration, or by the physiology of fatigue or stress development, or by the biomechanics of skeletal stiffness? The three mechanisms advance different answers, but the piece does not ask: which of these mechanisms, if operative, would produce precisely *this* residual shape and no other? Framing the residual as a "quantitative demand on whatever mechanism does bind" is correct. Asking what biological property would generate that demand shape could sharpen future empirical work.
