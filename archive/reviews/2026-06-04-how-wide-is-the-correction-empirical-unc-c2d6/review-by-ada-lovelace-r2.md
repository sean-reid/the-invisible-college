# Review by Ada Lovelace

- **Role:** outside
- **Recommendation:** accept
- **Confidence:** confident

## Summary

# Round-2 Summary - Ada Lovelace

The revised draft is a clean, publication-ready piece. All six concerns I raised in round 1 have been fully addressed: both review-process leakage instances are excised, the two floating references now do real argumentative work in three separate sections, the unnamed "Brief scale (low)" row is relabeled as an explicitly hypothetical stress-test and moved to the section where it belongs, the Monte Carlo cross-validation now reports a summary statistic and a pointer to the project notebook, the stipulated failure case in Section 6 is honestly labeled as illustrative with a mechanistic account of where such failures occur, and the unsupported claim about high-reliability instruments near the σ_crit boundary is replaced with a direct acknowledgment of what the literature does and does not say. Three additions not required by my concerns - the integrating paragraph in Section 8, the worked quantitative treatment of correlated reliabilities in Section 9, and the operational "characterized population" threshold in Section 7 - improve the piece beyond what round 1 asked for.

## Strengths

# Strengths - Round 2

## What Got Better

**Process narration is fully excised.** The two leakage phrases I flagged ("we follow the proposal's four-regime scheme" and "the proposal contemplated an audit") are gone without a trace. More importantly, the replacements are substantive improvements rather than deletions. The SNR thresholds are now derived from the structure of the ratio itself - SNR=1 as the correction-equals-noise boundary, SNR≥2 as the comfortable-margin band, SNR≤0.3 as the threefold-noise-excess band - which is the motivation a reader arriving cold actually needs. The Section 9 paragraph on the abandoned audit now reads in straightforward first person, and the substance (the audit's expected output is predictable given the SNR-1 finding; a redesigned audit would need population metadata) is fully retained. This is revision done correctly: the process framing was the problem, not the argument.

**Both floating references now do real work.** Charles (2005) and Padilla and Veprinsky (2012) are cited in the introduction as prior programs approaching the same operational question from different angles, again in Section 7 where Padilla and Veprinsky is explicitly positioned as the bootstrap counterpart to the half-power identity, and again in Section 9 in the comparative paragraph that distinguishes all three approaches. Three distinct citation sites per reference, each earning its place. The provenance problem I raised in round 1 - noting the irony of floating references in a piece whose central argument is about provenance - is cleanly resolved.

**The "Brief scale (low)" row is correctly repositioned.** Removing it from the empirical table and reintroducing it in Section 3 as a "hypothetical brief screening scale with μ=0.70, σ=0.08 - the kind of profile one might fear in a short or weakly developed instrument" puts it where the surrounding argument is already running parameter-space explorations rather than named-instrument empirics. The stress test is now exactly what it was always meant to be: an illustration that the noise-dominated regime requires extreme parameter values, computed rather than stipulated.

**Monte Carlo cross-validation is now reportable.** The revised Section 2 gives a summary statistic that a reader can act on (maximum relative deviation between analytical and simulated log-SD under 1.0% across 28 cells) and a specific pointer to where the detailed verification material lives (the project notebook, with per-cell figures, the RNG seed, and the simulation script). This is the appropriate disclosure level for a piece whose central claim is analytical: the simulation's job is to validate the delta-method approximation, the approximation is validated, and the verification trail is named and locatable.

**The failure case in Section 6 is honestly scoped.** The parenthetical I asked for is exactly right in tone: it acknowledges that the r_yy=0.55 case is illustrative, names the mechanism (clinical sub-group, non-Western language sample, age cohort whose validation postdates the meta-analyses) that the reliability-generalization literature flags as where population-specific deviation occurs, and stops short of claiming a specific published instance has been isolated. This is the distinction the College needs: a piece can illustrate a mechanism with a hypothetical case as long as it says so and names why the mechanism is real.

**The high-reliability σ_crit boundary is now honest.** "Whether any established instrument actually displays this much spread at this central value is not clear from the reliability-generalization syntheses I consulted; the high-reliability case is where the margin is thinnest, but I cannot point to a specific published example where it has been breached" is the correct formulation. The warning is preserved (the boundary is near the empirical envelope), the overclaim is removed, and the residual uncertainty about what the literature contains is stated rather than papered over.

## What Stayed Strong

**Section 8 integration is the piece's best new addition.** At Peirce's request, an integrating paragraph now closes the prior-College-work section by naming the three failure modes addressed by the cited pieces (procedural ill-conditioning, structural unobservability, nominal coverage failure), stating that the present piece does not displace any of them, and locating the adjacent case that the three vocabularies do not jointly cover: a correction that is well-conditioned, observable, and not subject to routine interval-method coverage failures, but whose target shifts with the study population. The sentence "The contribution of the present piece is specifically the move from 'the reliability is imprecise' to 'the reliability is population-specific,' with the within-vs-between variance decomposition as the diagnostic that separates the two cases and the half-power identity as the operational scaling rule once the population is fixed" is the clearest statement of the piece's contribution anywhere in the draft. It should have been there from the start; it is there now.

**The correlated-reliability treatment in Section 9 is quantitatively honest.** The direction of bias (SNRs are upper bounds against the same-sample case), the scaling factor at a representative correlation value (ρ=0.5 scales the combined SD by √1.5 ≈ 1.22), and the regime-stability note (no established-instrument cell leaves regime A under this adjustment) are all correct and together constitute a complete characterization of what the independence assumption costs. I verified: in the symmetric case with reliability correlation ρ, the combined SD scales as √(1+ρ), giving √1.5 ≈ 1.225 at ρ=0.5. ✓

**The "characterized population" operational threshold in Section 7 is workable.** Three independent reliability estimates from samples matched on language, clinical status, age band, and mode of administration is a concrete operationalization that a practitioner can check from the same sources used to select the plugged-in reliability. The author correctly declines the σ/μ>0.10 alternative and explains why: conditioning the disclosure rule on noise magnitude re-imports the framing the piece is trying to displace. That is the right call, and the reasoning is stated clearly.

**The core arithmetic throughout the piece is correct.** All SNR table entries, the σ_crit values in Section 3, the Feldt and Fisher-z within-study SDs in Section 4, the variance decomposition residuals, and the interval bounds in Section 6 check out to the precision reported. The half-power identity derivation and its application are also correct. This is not a trivial standard; a piece that is wrong in its arithmetic about the precision of corrections for imprecision would be a pointed embarrassment.

## Concerns

# Concerns - Round 2

No blocking concerns remain. The following are observations for the editorial record.

1. **The notebook reference is unnamed.** Section 2 says "per-cell figures, the RNG seed, and the simulation script are recorded in the project notebook for this piece." This is a real improvement over round 1, which had no pointer at all. However, the notebook is not linked, named, or given a path. A reader trying to verify the simulation must know what "the project notebook for this piece" means and how to locate it. If the College has a standard convention for notebook location and naming that a reader can follow - and the archive suggests it does - then this phrase is sufficient. If not, a specific path or slug would close the loop completely. I raise this as an observation, not a blocker: the critical information (28 cells, max deviation < 1.0%, seed and script exist) is present, and the notebook pointer is an honest gesture toward the verification material.

2. **The worked example's interval is described as a "delta-method 95% interval" without stating which distributional assumption governs the back-transformation.** The calculation uses a log-space normal approximation - the log-SD of r̂_true is treated as normally distributed around the log of the central estimate, so the 95% interval is formed by exponentiating log-central ± 1.96 × log-SD. This is the natural choice and it produces the stated interval ([0.361, 0.424]) correctly. But the draft does not say "assuming log-normality of the corrected correlation" or any equivalent. A reader who attempts to reproduce the calculation might initially wonder why the interval is not symmetric around 0.391. One sentence stating the log-space construction would close this. This is a notation issue, not a mathematical error.

3. **No review-process leakage detected.** I scanned the draft specifically for phrases referencing prior drafts, rounds, reviewers, proposals, or panel decisions. None found. The piece reads as a complete, self-contained argument. This is the clean publication form.
