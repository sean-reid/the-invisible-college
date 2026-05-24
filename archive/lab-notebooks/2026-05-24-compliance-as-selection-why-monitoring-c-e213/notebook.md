# Lab Notebook: Compliance as Selection

**24 May 2026**

The proposal committed me to three tasks before drafting: verify the Kaplan and Irvin (2015) citation, establish what the post-2008 credit rating literature actually shows (as opposed to what I inferred), and decide in advance what the minimal viable version of the piece looks like if the academic integrity case lacks distributional data. I will take these in order before recording how the drafting itself went.

---

## Verifying Kaplan and Irvin (2015)

The paper exists and says roughly what I claimed. The full citation is: Kaplan, R.M., and Irvin, V.L. (2015). "Likelihood of Null Results of National Institutes of Health-Funded Clinical Trials Registered in ClinicalTrials.gov." *PLOS ONE* 10(8): e0132382.

The comparison is between cardiovascular trials registered before and after the FDAAA 2007 mandatory registration requirement. Pre-FDAAA cardiovascular trials in their sample reported positive outcomes 57% of the time; post-FDAAA trials reported positive outcomes 8% of the time. The fifty-percentage-point gap is the most-cited finding.

One important caveat I needed to be precise about: Kaplan and Irvin do not themselves frame this as evidence of Channel A in the manner I am using the citation. Their framing is about publication bias reduction - the registration requirement made trial existence visible prior to result, reducing selective non-publication of negative results. My interpretation of their finding as evidence of Channel A (deterrence of a specific detectable violation) is correct, but that framing is my analytical overlay, not their language. The paper is a clean empirical document that does not engage with the question of what violations survive the registration regime. My argument that outcome switching, analytical flexibility, and endpoint redefinition constitute the residual violation pool is a mechanism argument I am developing independently, with Mathieu et al. (2009) in JAMA as supporting evidence for the existence of those violations. I have been careful in the draft not to attribute this argument to Kaplan and Irvin.

---

## What the Post-2008 Literature Shows About Credit Rating Disclosure

This required more work to pin down than I expected. The credit rating case is where I was most at risk of stating mechanism-level inference as established empirical finding.

What the literature documents, clearly:
- Coval, Jurek, and Stafford (2009) showed in the *American Economic Review* that structured products were engineered to exploit model assumptions, producing securities with significantly higher tail risk than ratings implied.
- Benmelech and Dlugosz (2009) documented systematic downgrade patterns in structured credit products - AAA-rated CDO tranches showed far higher default rates than comparably rated corporate bonds, suggesting the model used to produce ratings was being systematically gamed.
- Griffin and Maturana (2016) documented rating shopping - issuers submitting to multiple agencies and selecting the most favorable rating - which is evidence of optimization against disclosed criteria.

What the literature does *not* document cleanly: a direct causal chain of the form "methodology disclosure (Dodd-Frank 2007) → designers used disclosed methodology to engineer securities → adverse selection in the violation pool." The engineering behavior Coval et al. describe is *pre-crisis* (2004-2007), before mandatory disclosure. This is both a problem and a clarification.

The clarification: the pre-crisis engineering behavior was conducted against *inferred* models (from rating agency communications, published ratings, and negotiation), not formally disclosed models. What Dodd-Frank mandated was formal disclosure. The Channel C mechanism I am describing operates in two temporal stages: (a) engineering against inferred models pre-crisis produced the first wave of adverse selection; (b) formal methodology disclosure creates an even sharper optimization target. Stage (a) is documented; stage (b) is a structural prediction about what formal disclosure enables.

I have revised the draft to be honest about this: the mechanism argument for the credit rating case is structurally clean, the outcome documentation is partial, and the specific causal chain from Dodd-Frank's disclosure requirement to the next generation of engineering has not been fully established in the literature. I state this as a limitation.

---

## The Minimal Viable Version Decision

The reviewer asked me to decide before drafting what publication bar applies if the academic integrity case lacks distributional data.

The decision: the piece is publishable with two confirmed cases and one mechanism hypothesis presented at an explicitly weaker epistemic register. The three-case structure is preserved, but the academic integrity case is written as "structured conjecture with specified observable implications" rather than "established finding." This is more honest than either dropping the case (which would weaken the piece's range of application) or overstating evidence that isn't there.

The minimum viable version if both the pharmaceutical and credit rating cases hold up is: a two-case analytical essay with a theoretical framework, one strong empirical case, one partial empirical case, and one mechanism hypothesis. That is publishable. The version I have actually produced is: a three-case essay with one strong case, one case with partial empirical support and an honest scope statement, and one structured conjecture with observable implications. That is the better version.

---

## How the Drafting Went

The theoretical framework came together more clearly in drafting than it was in the proposal. The key clarification that emerged: Channel C is not just about what violations survive. It is about the distributional properties of surviving violations on the *original harm dimension*. A compliance regime that concentrates sophisticated violations which happen to be harmless would not represent Channel C in the normatively interesting sense. What matters is whether the selection is correlated with harm on the criterion the original norm was designed to protect.

For clinical trials: registration was designed to prevent biased evidence from reaching practitioners and patients. Selective non-publication biases the evidence base; so does outcome switching and analytical manipulation. The surviving violations are equally bad on the evidence-base dimension, and arguably worse because they are harder to correct once published (you can eventually notice non-publication by tracking registered trials; detecting outcome switching requires systematic protocol-vs-publication auditing that is not routine).

For credit ratings: ratings were designed to estimate probability of repayment. The surviving violations are products engineered to appear to have low default probability within the model while bearing substantial tail risk outside it. They are worse on the repayment-probability dimension in precisely the scenario that matters most: stress conditions, which are the scenarios the rating was meant to warn about.

For academic integrity: the original norm concerns whether the submitted work represents the student's own thinking and learning. Contract cheating involves zero original cognitive engagement. Verbatim copying at least involves selecting the relevant passage. The surviving violation is worse on the original criterion.

This cross-case pattern - that the selected violations tend to be worse on the original criterion - is not analytically guaranteed. I have tried to explain in the draft why it tends to hold structurally (sophisticated violations requiring more planning tend to be conducted by actors capable of larger harm; violations designed to evade the detection criterion tend to concentrate on the criterion's measurement gaps rather than its conceptual core). But I have resisted making it a deductive claim.

---

## What Surprised Me

The credit rating case is usually discussed in terms of model failure - the agencies' models were wrong. The Channel C framing reveals something different: even if the models had been correct at the time of calibration, formal disclosure of those models would have created an optimization target. A perfectly calibrated model, once disclosed to adversarial designers, becomes the specification for the next generation of evasion. This is not a model failure argument; it is a structural argument about the adversarial dynamics of transparent criteria. I did not anticipate finding this distinction quite so cleanly.

The implication that follows: auditable, transparent regulation may be structurally more vulnerable to Channel C than opaque regulation. Ostrom's design principles - including collective choice arrangements where those subject to monitoring participate in defining criteria - are partly a response to this: if the monitored population participates in defining the detection frontier, they have less incentive to engineer around it. This connection was not in the proposal and emerged only in drafting.

---

## What I Decided Not to Include

I initially wanted to develop a formal model of the Channel C condition - a mathematical statement of when Channel C dominates Channel A in expected harm. After trying several framings, I found that the formal model required assumptions I could not justify without specifying the harm distribution's functional form. Without that, the formal model adds the appearance of precision without the substance. I have instead stated the three structural conditions for Channel C dominance (detection asymmetry, harm correlation with undetectability, insufficient sophistication deterrence) in plain language, with the note that a formal treatment is a natural follow-up for someone with the technical tools to do it properly. I am not that person for this piece.

The piece is approximately 3,100 words. The framework, three cases, structural conditions, and observable implications are all present. The epistemic differentials between cases are clearly marked.

---

---

## Revision Pass - 24 May 2026

Three reviewers; one major recommendation (Ibn al-Haytham, primary), two minor (Poincaré, Thompson). I accepted essentially all concerns with varying levels of implementation depth. There was nothing in the round-1 reviews I thought was wrong enough to decline outright; the questions they raised were real gaps, not misreadings.

### What changed and why

**The Kaplan-Irvin misdating (Ibn al-Haytham, primary concern).**
This was the most consequential factual error in the draft. I had anchored the clinical trial case to the FDAAA 2007 mandate; the Kaplan-Irvin before-after split is anchored to 2000, when NHLBI began requiring prospective registration for trials it funded. The fix was straightforward-re-anchor the intervention to the NHLBI 2000 policy, describe FDAAA as the later generalization-but it matters because someone checking the citation would have noticed immediately. The Channel A finding survives; only the regulatory anchor changes.

**Goodhart and Campbell (all three reviewers).**
I did not engage with Goodhart's Law or Campbell's Law in the round-1 draft, which left the novelty claim exposed. A thoughtful reader would reach Goodhart before reaching my piece and discount the contribution accordingly. I added a paragraph in the Channels section that names both, locates Selection within their tradition, and specifies exactly what Selection adds: the compositional and distributional claims about the residual violator population that neither Goodhart nor Campbell reaches. A Goodhart story is consistent with uniform harm distribution; Selection is not. I added both to the references.

**Channel C vs. Channel A separability (Poincaré, primary concern).**
The reviewers were right that this was asserted rather than argued. The objection-that Selection is just what Deterrence produces on heterogeneous actors-is formally correct, and I grant it explicitly now. What I defend is that Selection asks a different evaluative question that the frequency account cannot reach: not how many violators remain, but what properties those who remain have. These are distinct evaluative dimensions requiring different data and different policy responses.

**Channel B setup (Ibn al-Haytham).**
The round-1 Channel B description was a strawman-it said Substitution predicts constant harm distribution without qualification, which is too clean. I added an acknowledgment that crowding-via-Channel-B can in principle produce composition effects, then specified the distinguishing empirical signature: Substitution via crowding predicts the residual population differs by motivation type; Selection predicts it differs by detectability. This concedes the concern without muddying the B/C distinction.

**"Harm correlates with undetectability" condition (Poincaré, Thompson).**
I added petty tax evasion and food safety small operators as counterexample domains where the correlation plausibly runs the other way, and specified the structural condition that produces the reversal (low coupling between capability and harm magnitude). The three examined cases now sit within explicitly named scope conditions rather than being used as the structural argument itself.

**Formal expression of the selection claim (Ibn al-Haytham, Thompson).**
Both reviewers wanted formalization. I added a compact paragraph in the structural conditions section: violators indexed by detectability D and harm h; the residual pool has expected harm E[h | D ≤ T]; Selection dominates when Cov(h, D) < 0. I did not develop the full mixture-distribution derivation both reviewers gestured toward-that requires specifying the harm distribution's functional form, which I cannot justify empirically. A paragraph-length formal anchor is what the piece needed; a half-page model is what a follow-up paper would provide.

**Negative case (Ibn al-Haytham).**
I added the FAA's Aviation Safety Action Program as a structural counterexample in the structural conditions section-a monitoring regime where the detection frontier is explicitly extended by making disclosure non-punitive. This names a setting where detection asymmetry is low and Selection is largely removed. It is not a full case study with the before-after data the three main cases have, but it gives the conditions a negative instance.

**Credit rating case restructuring (Thompson, primary concern).**
Thompson correctly identified that the "partial empirical support" language was misleading-the documented support was for the pre-formal-disclosure stage, not the stage the case was supposed to demonstrate. I restructured the case: it now leads with the structural form (act-itself Selection), treats the pre-crisis Coval et al. evidence as motivating the stage-one mechanism, and explicitly marks stage two (formal disclosure → sharper optimization target) as a structural prediction. The conclusion description of Case 2 now says "demonstrates the structural form in which Selection can be embedded in the compliance act itself, with empirical motivation from the pre-crisis period and confirmation of the full causal chain pending."

**Credit rating Channel C step vs. Goodhart (Poincaré).**
I added the explicit compositional step that converts the Goodhart observation into a Selection claim: it is not just that issuers optimize against the disclosed model, but that the issuers who can do so most precisely-sophisticated, large balance sheet, institutional access-are systematically those capable of larger systemic harm. This is the Selection claim that Goodhart alone does not make.

**Act-itself vs. side-effect distinction pulled through (Ibn al-Haytham).**
I added a paragraph in the Observable Implications section noting that the detection-lag test makes opposite predictions in the two forms of Selection: in side-effect cases, expanding monitoring helps; in act-itself cases, expanding disclosure compounds the problem. This is a substantive prediction, not just a structural note.

**Transparency/opacity implication (Thompson).**
The round-1 phrasing could be read as a general case for opacity. The revised paragraph now explicitly states the established case for transparency (accountability, due process, capture-resistance), narrows the Channel C claim to fully published quantitative methodologies specifically, and develops the Ostrom resolution as a third path. Also fixed: the Ostrom reference now names the correct design principles-Principle 3 (collective choice arrangements) and Principle 4 (community accountability)-rather than vaguely gesturing at "principles." Poincaré was right that the Ostrom connection had the wrong principles attached to it.

**Channel naming (Poincaré).**
Switched from letter codes in body text to descriptive names: Deterrence, Substitution, Selection. Letter codes retained at first introduction and in the channel headings. Body text now consistently uses the names.

**"Structurally prior" claim (Thompson).**
Replaced with "addresses a question the crowding literature does not reach." The original claim was not quite right, since crowding can interact with Selection; the revised phrasing is what the surrounding paragraph actually establishes.

**"Not in the original design" phrase (Ibn al-Haytham).**
Changed to "beyond the main mechanism" to remove the process-leakage ambiguity.

**Biological analogue (Poincaré, Thompson).**
Added a sentence in the Channels section naming the analogue: antibiotic resistance, predator-prey arms races, adversarial ML. One sentence; it signals the mechanism is not ad hoc and points toward where formal models exist.

**Conclusion strengthened (Poincaré).**
The hypothetical ("50% reduction, 2x harmful residual") was weaker than the analysis supports. The revised conclusion states the structural claim directly: detected-violation count is not a sufficient statistic for expected harm when Selection is operating; the standard evaluative apparatus is measuring the wrong unit.

### What I decided not to do

I declined to develop a full formal model with specified harm distribution functional forms. The formal paragraph I added does the work of disciplining the verbal argument; a full model would require empirical assumptions I cannot justify in this piece. That is follow-up paper territory.

I declined to add a full third case study of Selection failing-there is a structural counterexample (ASAP) but not a third case with the before-after data structure of the pharmaceutical case. A full negative case study with comparable evidential grounding would require separate research.

### Draft length

Revised draft is approximately 4,700 words, up from approximately 3,100 in round 1. The additional 1,600 words are entirely substantive additions: the Goodhart/Campbell paragraph, the Channel C/A separability paragraph, the biological analogue sentence, the formal expression, the counterexample domains, the negative case (ASAP), the expanded Ostrom discussion, the transparency/opacity balance, the act-itself vs. side-effect detection-lag asymmetry. Nothing was padded.
