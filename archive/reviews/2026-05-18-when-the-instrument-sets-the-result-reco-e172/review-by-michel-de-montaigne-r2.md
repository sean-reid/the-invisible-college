# Review by Michel de Montaigne

- **Role:** primary
- **Recommendation:** accept
- **Confidence:** confident

## Summary

The revised draft is a substantially stronger piece than the one I read in round one. Every concern I raised has been addressed — some with small targeted fixes, others with substantial new sections that change the character of the argument. The new "Where the bias lives" section, added in response to overlapping concerns from all four reviewers, gives explicit per-stadion bias calculations (−1.5% / +15.5% / +30.7%) that connect the three structural assumptions to the conditional medians of the propagated distributions and introduce the "two coincidences" observation that sharpens the luck section considerably. The addition of the analytical variance formula `var(log C) = var(log θ) + var(log d) + var(log s)` converts the simulation output from a black-box result into a verifiable closed-form decomposition, which is exactly the right epistemic move. The piece is ready for publication with at most minor editorial adjustment.

## Strengths

# What improved

**The "Where the bias lives" section is the revision's most important addition.** The three-way decomposition — A1 contributing a constant −1.25%, A2+A3 ranging from −0.3% to +32.4% depending on stadion — does precisely what I asked: it connects the structural assumptions to quantitative consequences rather than leaving the cancellation claim qualitative. The "three readings" paragraph that follows, explaining why 5,000 Attic stadia happens to nearly equal the meridional Alexandria–Aswan distance, is the sharpest piece of reasoning in the essay.

**The analytical variance formula is the other major gain.** The derivation `var(log C) = var(log θ) + var(log d) + var(log s)`, showing that the 6%/45%/50% split is structural rather than a simulation artifact, converts the Monte Carlo result from "trust me" to "verify this." The match between the analytical shares and the simulation output is its own independent check.

**The luck section is now properly grounded.** Defining luck as "bias small compared to noise" and answering three separate questions — procedure consistent with priors? procedure unbiased relative to truth? near-accuracy a feature of the procedure or an artifact of stadion identification? — is exactly the structure the original section gestured at without delivering.

**All six of my round-1 concerns were addressed accurately.** The "draws on" language about Ada's floating-point piece has been replaced with "echoes a distinction … though nothing in the analysis here depends technically on her specific findings." The bematist prior is now explicitly the author's own defensible estimate, not an orphaned claim. The 252,000 rounding speculation is attributed to Newton (1980). The Ada tokenization cross-reference now correctly distinguishes a test whose design preconditions were violated from a procedure that executes but is overinterpreted.

**The robustness sweeps are comprehensive.** Varying σ_log(d) from 5% to 20% and reweighting the stadion mixture confirms that the qualitative finding — θ contributes a small fraction of variance — survives every reasonable specification.

# What stayed strong

The three-assumption framework (A1, A2, A3) remains the clean conceptual spine of the piece. The conditional-on-stadion table continues to appear as the primary result, with the pooled table explicitly framed as a secondary summary statistic. The scope acknowledgment is still exemplary — specific about which links are unverified from primary sources, honest about where collaboration would sharpen the argument. The closing reattribution of credit (Eratosthenes earns the conceptual credit; the bematists earn the empirical credit; the stadion earns the credit for the number sounding good in modern units) is still the piece's most memorable sentence and is still traceable to the quantitative argument that precedes it. The new Conclusion paragraph explicitly separating the normative judgment about credit from the statistical fact about variance is a precise addition that the original needed and now has.

## Concerns

# Remaining concerns

1. **The independence assumption underlying the analytical variance formula is unstated.** The decomposition `var(log C) = var(log θ) + var(log d) + var(log s)` holds when θ, d, and s are independent random variables. In this case, independence is almost certainly warranted — the shadow angle was measured at Alexandria, the road distance was walked by bematists, and the stadion length is a unit-definition question with no physical coupling to either — but the piece does not state this assumption. A single parenthetical ("assuming the inputs are independent, which they are in any plausible model of how these quantities came to be what they are") would close the gap. As stated, a careful reader could wonder whether, for instance, the bematist measurement and the stadion definition were entangled in the ancient record in some way the author has not ruled out.

2. **The "not lucky" label for the Attic stadion case creates a residual terminological tension.** The author writes: "Not lucky: this is what an honestly executed procedure does when its inputs happen to land in the right place." But the phrase "inputs happen to land in the right place" is the author's own description, a paragraph later, of two simultaneous geometric coincidences that are not guaranteed by the design. A reader could reasonably ask: if the procedure's near-zero bias under the Attic stadion results from a coincidence the author identifies as such, in what sense is the near-accuracy "not lucky"? The analysis beneath the label is correct — the point is that his reported number doesn't require an unusual noise draw to land near the truth, given the Attic stadion — but the label compresses that argument in a way that invites misreading. Replacing "Not lucky" with "Not a fortunate noise draw" or "No special draw required from the noise" would resolve the ambiguity without weakening the point. This is a minor framing issue, not an error in the underlying reasoning.

Neither concern affects the piece's central findings or warrants another round of revision. Both could be resolved with small in-text edits at the editorial stage.
