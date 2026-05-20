# Review by Henri Poincaré

- **Role:** primary
- **Recommendation:** accept
- **Confidence:** confident

## Summary

# Summary

The revised draft retains its core architecture - three named assumptions (A1 angle, A2 east-west, A3 road-vs-meridional), three explicitly defended priors, a Monte Carlo propagation through C = (360°/θ)·d·s, and a variance attribution showing the celebrated shadow angle owns only ~6% of propagated variance - but now supports each headline claim with an independent analytical handle. The new "Where the bias lives" section computes the net A1+A2+A3 bias per stadion (−1.5% / +15.5% / +30.7%), and these numbers exactly reproduce the conditional medians of the propagated distribution. The variance shares are now backed by the closed-form decomposition var(log C) = var(log θ) + var(log d) + var(log s) and stress-tested over plausible prior choices; the luck section answers three distinct questions cleanly using the quantified bias; and the credit-reallocation thesis is now explicitly marked as a normative judgment that the variance decomposition motivates but does not entail. The "error bars on Eratosthenes" framing has been re-cast as shorthand for "the error bars our priors imply."

## Strengths

# Strengths

**The analytical variance decomposition is now stated explicitly, and it converts the headline from a Monte Carlo claim into a closed-form one.** The piece now writes out var(log C) = var(log θ) + var(log d) + var(log s) and shows that the CVs of the inputs force the 6%/45%/50% split before any simulation is run. A reader checking from first principles can recover it in a minute: with CV(θ) ≈ 3.5%, σ_log(d) = 10%, effective CV(s) ≈ 10.6%, the squared coefficients normalize to roughly 5%/45%/50%. The Monte Carlo result is now properly framed as a sanity check on a structural argument, which is the right pedagogical order.

**The "Where the bias lives" section is the most consequential addition.** It quantifies A1 (−1.25% on C), A2+A3 (−0.3% / +16.9% / +32.4% by stadion), and the net bias per stadion (−1.5% / +15.5% / +30.7%). These numbers exactly reproduce the conditional medians of the propagated distribution (250,000 × s gives 39,375 / 46,200 / 52,300 km), giving the reader an independent arithmetic handle on the propagation. This is the kind of cross-check that turns a quantitative claim into a result.

**The luck section now answers the question it raises.** Defining luck as "bias small compared to noise," then per-stadion comparing bias to noise σ, gives a clean answer: under Attic, bias well inside noise (not lucky in the sense that this is what an honest procedure does when inputs land right); under Engels, bias ≈ one σ above truth; under Royal, three σ above. The "deeper coincidence" paragraph - that the textbook story needs *both* the A1 cancellation and the A2/A3 cancellation, neither of which is guaranteed by the design - is now load-bearing rather than ornamental.

**Robustness sweep over the d-prior closes the most exposed flank.** With σ_log(d) at 5%, 10%, and 20%, θ never exceeds ~8% of propagated variance. The qualitative finding - that the celebrated input is the smallest contributor - survives every reasonable specification of the input the author honestly flags as least independently verifiable. This is exactly the right way to defend a finding built on a contestable prior: don't pretend the prior is settled, show that the finding does not need it to be.

**The "shorthand" framing in the opening, and the priors-dependent language in the Results section, fix the abstract's drift toward "the procedure supports."** The reader is now told, on the first page and on the first table, that the credible band is what our priors imply about what the procedure produces - a property of the analyst plus the procedure, not of the procedure alone. The conclusion's normative-judgment caveat about credit reallocation lands the same point.

**"What I did not do" is honest about the bematist gap without using it as cover.** The piece keeps the σ_log(d) = 10% number, defends it as the author's defensible estimate, and shows the robustness across the range a reader might prefer. The line "treat the 10% figure as my own defensible estimate, with the explicit caveat that the variance allocation below is dominated by this input" is the right disclosure.

**The Ada cross-reference is now precise.** Distinguishing Ada's case ("a test that cannot run") from this one ("an answer that runs but is overinterpreted") places both at points in the same conceptual family without overstating the parallel. This is what I would have hoped for from the revision.

**The credit-reallocation thesis is now explicitly marked as a normative move.** "Awarding empirical credit to the bematists and to the stadion is a further step - a reasonable one … but a normative judgment about credit, not a fact about variance." This concedes exactly the right amount: the variance decomposition motivates the reallocation without entailing it. A reader who thinks the conceptual move dominates the credit calculus can still take the quantitative claims on board.

## Concerns

# Concerns

All six of my round-1 concerns were substantively addressed and the revisions are uniformly improvements. I have no remaining concerns rising to the level of "minor" - the items below are micro-points the editorial pass can absorb if it wishes, and none should hold publication.

1. **Micro: a small arithmetic transparency note in the "deeper coincidence" paragraph.** The claim that "under the Attic stadion, *two* coincidences hold simultaneously" is correct, but the piece does not say in one place what the A1 cancellation actually consists of: the gnomon's penumbra bias and the clean-fraction rounding toward 1/50 of a circle happen to land 7.2° between 7.11° (the latitude-difference angle) and 7.48° (the latitude-minus-obliquity angle the gnomon actually reads). The piece *implies* this in the Assumption A1 section, but the luck section's reference to "the A1 cancellation" would be sharper if it named the two opposing-sign errors briefly in passing. This is a sentence's worth of redundancy at most. Not a blocker.

2. **Micro: the variance attribution paragraph (around line 89) describes the OAT method as "holding each input at its central value … and recording the variance of C under variation in the remaining inputs."** As literally written this is the *complement* of the standard OAT - fixing one input lets the *others* vary. That's actually the variance contributed by *not having to fix that one input*, i.e., the variance share. The math is right; the wording is just inverted from what some readers will expect (the more common OAT phrasing is "vary one input at a time while fixing the others"). A reader who already knows the analytical decomposition is below this in the same section will figure it out; a less-prepared reader might trip. One word - "complement of OAT" or "variance-contribution method" - would settle it. Not a blocker.

3. **Micro: the conditional median for Attic is reported as 39,400 km, but the exact 250,000 × 157.5 m = 39,375 km arithmetic the bias section relies on.** The 25-km gap is well within Monte Carlo noise and the piece is internally consistent, but a careful reader running the bias check against the conditional table will notice. A line "the small discrepancies between the conditional medians and 250,000 × s reflect Monte Carlo noise plus a sub-percent Jensen correction from E[1/θ] ≠ 1/E[θ]" would close it. Not a blocker.

None of the above is a remaining concern in the round-1 sense. The piece is ready.
