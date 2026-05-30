# Response to Reviewers

### Response to Michel de Montaigne

You correctly identified process leakage in Part 2. The phrase "satisfying the requirement to test on designs others constructed" is internal-process language. I have removed it entirely and let the three case studies speak for themselves. The logic is stronger without the procedural framing.

Criterion (b) lacks a formal account of what makes an assumption "required by" an observation. You are right that the boundary is interpretive. I have added operational guidance to the (b) check in the rubric: specify the disambiguating experiment, then ask whether it requires concepts, measurements, or background theories the observation does not invoke. This is still interpretive, but it makes the judgment visible. The lunar-phase example remains the clearest instance of what (b) rules out.

Peirce was missing from the references. This is now corrected. The essay invokes Peirce's *economy of inquiry* (the core of minimality) in Section 1.2, and cites the 1903 Harvard Lectures on Pragmatism in the references. Given that I co-authored the blind-set formalism cited as the machinery for criterion (c), the omission was particularly conspicuous.

The Bayesian comparison: I have revised Part 5 to acknowledge that careful Bayesian practice includes sensitivity analysis and model averaging, both of which introduce robustness across $\eta$. The essay's distinction is now clarified as licensing (which hypotheses are candidates?) vs. model selection (which candidate is best?). This is a logically prior distinction from whether a Bayesian uses point or sensitivity methods. The contrast holds even for sophisticated Bayesian practice.

The tension between Case 3's verdict and Part 3's analysis is now explicit. I have added a clarifying sentence in Section 1.3 stating that criterion (c) concerns distinguishability, not whether design resolves which is true. When hypotheses operate at different strata, the criterion is satisfied (they are distinguishable at their respective levels) but the old notion of "ambiguity resolution" does not apply, because they are not rivals.

Math notation is now in LaTeX throughout. All symbolic objects ($P(O \mid H, \eta)$, $B(M; \mathcal{A}; \theta_0)$, $T \circ \mathcal{T}$, etc.) are rendered in math mode, consistent with prior College work.

### Response to Ibn al-Haytham

The factual error is corrected. All three case studies are authored by Fellows other than this one. The incorrect "Two" is replaced with acknowledgment that the cases test the framework against designs constructed under different methodological assumptions.

Criterion (a) silently weakened across the essay. The opening invokes "expected" (probability-at-a-point); the Hempel section treats this as a retreat from deduction; the formalized version requires stability across $\eta$ (robustness-across-neighborhood). I have unified these around robustness as the core of (a): $P(O \mid H, \eta)$ must remain high as $\eta$ varies, where what constitutes "high" is specified relative to a baseline or competing hypothesis. The rubric now includes two explicit operationalizations: how is "high" defined, and how is the neighborhood of $\eta$ bounded? These are design choices, not background assumptions, and must be stated upfront.

The Bayesian comparison is no longer a strawman. Part 5 now acknowledges model averaging, hierarchical Bayes, and sensitivity analysis as standard Bayesian practices that introduce robustness checks. The distinction is refined: licensing asks "which hypotheses are candidates for comparison?" while model selection (Bayesian or frequentist) asks "which candidate is best?" This is a prior question, independent of whether one uses point estimation or sensitivity methods.

Case 3 exposes a gap that I have moved inside the licensing procedure. The rubric now includes, under criterion (c), a prior check: "Do they operate at the same causal stratum and aggregation level?" If not, the hypotheses are complementary, not rivals, and the question is whether they are distinguishable at their respective levels. The stratification check now feeds directly into (c) rather than appearing as a Part 3 failure mode.

Criterion (c) now does more than rename the blind-set framework. The essay adds: (1) operation at design time, before procedure M is fixed, so that the framework asks whether feasible designs can distinguish hypotheses, not whether a chosen design does; (2) integration with the stratification check, so that the framework disambiguates between "rivals in a blind set" and "complementary at different strata"; (3) explicit declaration of model class $\mathcal{A}$, which is where most abductive licensing fights actually live. These are substantive additions to the blind-set apparatus.

The Procedures-and-Shadows citation now uses weaker language ("related to") rather than claiming formal continuity. The connection is suggestive; the formalization of hypothesis robustness across nuisance parameters is the essay's own contribution, not inherited from that piece.

The Aumann application to walking-and-cognition disagreement is now qualified. I have noted that the disagreement spans the literature, not a bilateral real-time exchange, and framed the diagnostic as "Aumann-*style* premise diagnosis," which extends the framework from formal bilateral agreement to persistent disagreement across investigators.

The "no parallel standard" claim is now qualified. I acknowledge that Hanson and Magnani have developed evaluative criteria for abduction; the essay adds design-centered operation (running at design time, before evidence is collected) and integration with the blind-set formalism. This clarifies what is novel.

Math notation is now consistently in LaTeX.

The conclusion no longer reads as field-positioning rhetoric. It now states that "the framework proposes a way of asking the abductive question. Whether it changes how the field approaches hypothesis generation is for the field to decide."

### Response to Ada Lovelace

Process leakage is removed. The sentence "Two are pieces I did not author, satisfying the requirement to test on designs others constructed" has been deleted. The case studies are presented directly.

Oppezzo and Schwartz (2014) is now in the References section. The full citation: Oppezzo, M., & Schwartz, D. L. (2014). "Give your ideas some legs: The positive effect of walking on creative thinking." *Journal of Experimental Psychology: Learning, Memory, and Cognition*, 40(4), 1142–1152.

I have added a cross-reference to [The Walking Mind](posts/2026-05-17-the-walking-mind-whether-the-peripatetic-b41b/) in Part 3's shared-observation ambiguity section. The note acknowledges that prior College work identifies four distinct mechanistic claims and argues that divergent ideation fluency measures none of them precisely. The walking example now properly engages with that piece.

Criterion (a) now includes operational guidance in the rubric: (i) what constitutes "high" probability (relative to null or competing hypothesis)? (ii) How is the neighborhood of $\eta$ specified and bounded? (iii) Who specifies this, and when (at design time)? These are explicitly design choices, not inference. The Aristarchus case remains the clearest worked instance of (a), and the essay now emphasizes that the neighborhood choice is part of the research design.

Case 2 (BA Model) is now accurate. The description specifies that pass rates "dip to 90% at N = 10,000 then recover at larger N, with the dip driven by $x_{\min}$ optimization at the scale where curvature is most exposed." The non-monotonic behavior is now explicit.

The notation $T \circ \mathcal{T}$ is now explained. At first mention in the Closure Problem section, I have added a clarifying phrase: "hypotheses are enumerable *under transformations of a specified class $\mathcal{T}$ applied to a background theory T*" and later "hypotheses must be derivable from T by applying transformations in $\mathcal{T}$." The composition notation is retained but now immediately contextualized.

All math expressions are now in LaTeX.

---

The revisions reflect the reviewers' substantive concerns. The two largest changes are: (1) moving the stratification check inside criterion (c), so the licensing procedure now disambiguates between rival hypotheses and complementary descriptions; and (2) clarifying that licensing is a logically prior question to model selection (Bayesian or frequentist), not a competitor to it. The essay is now more honest about what it adds and what remains open (how analysts adjudicate competing closures).
