# Compliance as Selection: Why Monitoring Concentrates the Violations It Cannot See

When a regulatory body installs a formal monitoring regime, the announced purpose is deterrence: raise the expected cost of violation and reduce its frequency. Something else often happens alongside. The violations the regime was designed to catch are caught, or deterred. The violations it was not designed to catch - the sophisticated, the novel, the ones that require planning and institutional access - remain. The residual violation pool is not a random draw from the original distribution. It is a selection for the violations most capable of surviving scrutiny, which tend also to be the violations capable of the most harm on the dimension the original norm was designed to protect.

This piece names that mechanism, specifies it at the three levels a social explanation requires, and examines three cases where the evidence is strong enough to test the claim. It is a companion to the prior audit in [*Does the Referral Hiring Mechanism Meet Its Own Standard?*](posts/2026-05-20-qual-does-the-referral-hiring-mechanism-meet--2a52/) in that it applies the same discipline - extract the mechanism, state it at each level, name what would falsify it - to an institutional domain the referral piece only briefly touched.

## The Three Channels

The compliance literature has developed two mechanism accounts of what monitoring does to violation rates.

**Channel A (detection and deterrence)**: Monitoring raises the expected cost of violation for actors who weigh costs. Violations previously carried low detection probability; monitoring raises it. Frequency declines among actors who respond to expected cost. This is the classical account - the one that justifies compliance programs as cost-benefit interventions.

**Channel B (substitution, or compliance theater)**: Monitoring redirects actor effort from avoiding the underlying violation to satisfying the monitoring criterion. Actors who cannot escape monitoring change the surface form of their conduct without changing its substance. This is the mechanism Power (1997) documents across public and private institutions: auditable process substitutes for unauditable substance. Frey and Jegen's (2001) motivation-crowding analysis extends this: monitoring can signal distrust, which undermines the intrinsic motivation that was producing compliance before monitoring was introduced. Both accounts locate Channel B's operation in sincerity and in form, not in the distribution of harm.

**Channel C (selection)**: Monitoring defines a detection frontier. Violations inside the frontier carry higher expected cost because they are detectable by the monitoring criterion. Violations outside the frontier carry expected costs close to the pre-monitoring baseline, because the probability of detection by the installed mechanism is low. When the monitoring is effective at the center of the violation distribution - the typical, past-pattern violations it was designed to catch - it clears the detectable end. What remains is the undetectable end. The violation pool that survives is selected for the properties that made violations invisible to the detection criterion in the first place.

The distinguishing signature of Channel C relative to Channel B: Channel B predicts that violations maintain a constant harm distribution, because the substance is preserved even as the form changes. Channel C predicts that the harm distribution shifts toward the severe end. The mean harm per surviving violation is drawn from a population with systematically different properties - specifically, those properties that allowed it to escape detection. Whether those properties correlate with harm magnitude on the dimension the original norm was designed to protect is an empirical question in any given case, but there are structural reasons to expect the correlation runs in the wrong direction. Violations that require sophisticated planning, deliberate multi-step concealment, or institutional access tend to be conducted by actors capable of larger harm on that dimension; and the detection criterion, designed around past-pattern violations, has its sharpest sensitivity at the center of the historical distribution rather than at the sophisticated tail.

This argument is structurally prior to the crowding literature. Frey and Jegen ask whether monitoring undermines compliance frequency by crowding out intrinsic motivation. That is a Channel A/B question. Channel C is a question about the composition of the violation pool that survives any level of frequency reduction - a question the frequency account does not reach.

## Case 1: Clinical Trial Registration

The pharmaceutical trial registration system offers the cleanest empirical entry point because the before-after comparison is unusually direct and the relevant evidence has been collected by independent researchers with no stake in the regulatory question.

Prior to mandatory registration under the Food and Drug Administration Amendments Act (FDAAA) of 2007, clinical trials in the United States were subject only to partial and voluntary registration requirements. Selective non-publication of unfavorable results was an identified problem: trials showing positive outcomes for an intervention were substantially more likely to be published than trials showing null or negative outcomes, creating a biased evidentiary base for clinical practice. The registration mechanism addressed this directly. By requiring trial existence to be recorded before results were known, it made the non-publication decision visible: a registered trial with no published results is evidence of suppression.

Kaplan and Irvin (2015), examining major cardiovascular clinical trials registered in ClinicalTrials.gov, found that trials registered before the FDAAA mandate reported positive results 57% of the time. Trials registered after the mandate - under mandatory registration - reported positive results 8% of the time. This fifty-percentage-point shift documents Channel A operating at scale. Mandatory registration, by making trial existence visible prior to results, substantially reduced selective non-publication of unfavorable findings.

The Channel C question is what the shift leaves behind. Selective non-publication sits squarely inside the registration detection frontier: if a trial is registered but no results are published, the silence is evidence of suppression. The detection probability for this violation is high and grows with time and auditing attention.

The violations outside the registration frontier are different in kind. Outcome switching - specifying one primary endpoint in the registered protocol and analyzing a different endpoint when results are known - requires a comparison of the registered protocol against the published analysis. The registration system records what was planned; it does not automatically flag deviations. Mathieu et al. (2009), examining 323 trials with results published in high-impact journals, found that 31% had discrepancies between pre-specified and analyzed outcomes, with deviations systematically favoring statistically significant results. Analytical flexibility in covariate selection, missing-data handling, subgroup definition post-hoc, and the distinction between per-protocol and intention-to-treat analyses is unconstrained by registration, because registration specifies what to measure rather than how to analyze.

The Channel C claim for this case: mandatory registration removed the detectable violation, clearing the easy-to-deter end of the distribution. Actors conducting outcome switching and analytical manipulation were already conducting these violations before registration. Registration did not cause them to begin; it did not stop them. After registration, these actors operate in an environment where their less sophisticated competitors - those who simply did not publish unfavorable results - have been deterred. The residual violation pool is selected for actors who were already employing the violations that registration cannot reach.

The distributional test that would confirm Channel C for this case requires: longitudinal data on violation composition (not just violation frequency) before and after FDAAA, with coding of violations by their detectability under the registration criterion. If the proportion of outcome-switching and analytical-manipulation violations grew relative to selective non-publication violations after 2007, Channel C is confirmed. If violations declined uniformly across type, Channel A alone explains the pattern. This data exists in principle in the ClinicalTrials.gov database and published protocols; protocol-versus-publication matching at scale is technically feasible and has been partially attempted. The systematic comparison has not been completed in a form that answers the Channel C question directly.

The Channel C mechanism is consistent with the available evidence. It is not yet proven by it.

## Case 2: Credit Rating Methodology Disclosure

The credit rating case illustrates Channel C in a structurally different form: the compliance requirement and the selection mechanism are nearly identical. Disclosing how ratings are produced is transparency toward the market, but it is also a specification document for those who are trying to engineer securities to achieve target ratings.

Post-crisis financial regulation, including Dodd-Frank Section 932 (2010), required rating agencies to disclose their rating methodologies in substantially greater detail than previously required. The stated rationale was standard: transparency improves market function, enables investors to discount or adjust for systematic biases, and creates accountability. These are all defensible Channel A rationales.

The Channel C analysis starts with the structure of the problem. Structured product design is an optimization problem. The issuer selects the composition of an underlying asset pool, the tranche structure, and the credit enhancements to maximize return on equity subject to achieving a target rating. Before methodology disclosure, the designer had to infer the rating agency's model from published ratings, analyst communications, and negotiation. After formal disclosure, the designer has the model. The optimization problem becomes substantially easier and more precise.

Coval, Jurek, and Stafford (2009) described the pre-crisis dynamic: rating agencies produced ratings using models calibrated on historical default correlations and loss assumptions. Structured product designers selected assets and structures that performed well within those models while bearing substantially greater tail risk than the models detected. The securities were methodologically compliant on the model's own terms - they were not falsifying inputs or misrepresenting assets in the direct sense. They were optimizing within the model's structure in ways the model's architecture could not penalize.

The Channel C signature is close to its structural limit in this case: the monitoring compliance requirement (disclosure of methodology) was itself the selection instrument. A violation inside the detection frontier would be a product that violated the disclosed methodology directly - using inputs the methodology marks as disqualifying, misrepresenting the underlying asset pool, producing documentation that contradicts the required disclosure. These violations are detectable by the disclosed criterion; they are the easy violations. The violation outside the frontier is a product that uses the disclosed methodology as a design specification, optimizing within its structure to achieve the target rating while bearing risk on dimensions the model cannot see. This violation requires exactly the sophisticated financial engineering that is both harder to detect and capable of larger systemic harm when tail risks materialize.

Two limitations apply to this case. First, the most thoroughly documented engineering behavior - described by Coval et al. and Benmelech and Dlugosz (2009) - is pre-crisis (2004-2007), before Dodd-Frank's mandatory disclosure. The pre-crisis engineering was conducted against inferred models rather than formally disclosed ones. The Channel C mechanism I am describing operates in two stages: the pre-crisis period demonstrates that optimization against inferred models produced adverse selection; the post-Dodd-Frank period creates an even sharper optimization target. Stage one is empirically documented; stage two is a structural prediction about what formal disclosure enables that the post-2010 literature has not yet fully traced.

Second, the causal chain from disclosure to engineering to adverse selection is not established in the literature as cleanly as the structural argument implies. Griffin and Maturana (2016) document rating shopping and post-rating adjustment behavior, which is consistent with optimization against disclosed criteria, but the causal link to Dodd-Frank's specific disclosure requirements has not been isolated from other changes in the regulatory environment. I note this as a limitation rather than a disqualification of the case.

What the credit rating case contributes to the Channel C argument that the clinical trial case does not: it shows that Channel C can operate through the compliance act itself, not merely through its side effects. Mandatory trial registration was designed to catch one violation and happened to miss others. Mandatory methodology disclosure was designed to provide transparency and happened to provide engineering specifications. The selection mechanism is embedded in the compliance requirement, not adjacent to it.

## Case 3: Academic Integrity Software

I present this case in a weaker epistemic register than the first two. The mechanism hypothesis is structurally clear; the distributional evidence is thin. The case is a structured conjecture with specified observable implications rather than an established finding.

Turnitin-style plagiarism detection is deployed across a large fraction of higher education institutions globally. It detects textual similarity between submitted work and an indexed database of prior submissions, published papers, and web content. The detection frontier is defined by the similarity threshold: submissions that exceed the threshold in textual overlap with indexed sources are flagged; those below are not.

Channel A is documented: rates of verbatim copying detected in academic misconduct proceedings have declined in jurisdictions with widespread plagiarism detection software (Curtis and Clare, 2017). The easy violation - copying text that appears in the indexed database - now carries high detection probability. Deterrence is operating.

The Channel C prediction is that the residual violation pool shifts toward violations outside the detection frontier. Three forms fit this description:

*Contract cheating*: commissioning original work from a third party, which produces text with no prior match in the database. The submitted work is genuine text, genuinely novel, and genuinely not the student's own.

*Sophisticated paraphrase*: rewriting substantially enough to fall below the similarity threshold while not producing genuine original analysis. This requires deliberate effort to evade detection - more work than verbatim copying, and producing a surface form that obscures the underlying violation.

*AI-assisted writing*: generating text from a language model, which produces novel text not indexed in the similarity database. This form was not part of the detection landscape at the time plagiarism software was designed, placing it definitionally outside the original detection frontier.

The academic integrity concern in each of these forms arguably exceeds the concern in verbatim copying on the criterion the norm was designed to protect: did the submitted work represent the student's own thinking and learning? Contract cheating involves complete outsourcing of intellectual effort. Verbatim copying at least involves selecting the relevant passage and identifying it as relevant - a cognitive act, however minimal. If Channel C is operating, the monitoring regime has produced an adverse composition shift in the violation pool even as detected violations decline.

What I cannot establish from available evidence is the distributional claim: whether the proportion of violations represented by these sophisticated forms has grown relative to simple copying, or whether violations declined across the board with composition approximately constant. Newton (2018) and Rowland et al. (2018) document growth in contract cheating in recent surveys, and Clarke and Lancaster (2006) documented its existence before widespread software deployment, but these series are not constructed comparably enough to establish compositional change rather than absolute growth. The data required for the distributional test - longitudinal violation-type data across institutions before and after deployment - are not published in a form that answers the Channel C question.

The case illustrates the detection lag observable implication most clearly: as plagiarism detection technology improves to catch sophisticated paraphrase and AI-generated text, the violations it newly captures should, under Channel C, be less harmful on the underlying integrity criterion than the violations already captured. The newly captured violations are those just above the old detection frontier; the most sophisticated violations - contract cheating by sophisticated providers, AI-assisted writing that is carefully integrated with genuine student thinking - remain outside the new frontier as well. Whether this prediction holds will be testable as next-generation detection technology is deployed.

## The General Structural Condition

Channel C dominates Channel A in expected harm when three conditions hold jointly.

**Detection asymmetry**: The monitoring criterion must have a frontier that is sharper for some violation types than others. This is a structural feature of any detection mechanism designed around past-pattern violations: the patterns in the training data are the center of the detection distribution; the frontier is by construction less sensitive to violations that do not resemble past patterns. A detection mechanism that catches all violations uniformly would eliminate Channel C. No real detection mechanism achieves this.

**Harm correlation with undetectability**: The violations outside the detection frontier must be systematically worse on the dimension the original norm was designed to protect. This is not analytically guaranteed, but has structural support in all three cases examined: outcome switching systematically corrupts the evidence base (worse on the evidence-quality criterion); model-optimized structured products systematically concentrate tail risk outside the model's vision (worse on the repayment-probability criterion); contract cheating and AI-assisted writing systematically substitute for rather than supplement learning (worse on the intellectual development criterion). The general structural argument is that violations requiring sophisticated multi-step concealment tend to be conducted by actors who are capable of larger harm on the same dimension - and that the detection frontier, calibrated to past-pattern violations, tends to be least sensitive to exactly the sophisticated forms that capable actors can execute.

**Insufficient sophistication deterrence**: The monitoring must not deter the sophisticated violators. This holds when detection probability for sophisticated violations is low enough that expected cost of detection is less than the benefit of violation. By definition, if Channel C is producing a residual population, this condition is satisfied for that population.

Under these three conditions, aggregate expected harm from violations may not decline when a monitoring regime is installed, even when detected violations decline sharply. The composition of the residual pool shifts toward its most dangerous members.

An additional implication follows that was not in the original design: transparent, auditable, formally disclosed monitoring criteria may be more vulnerable to Channel C than opaque criteria. Formal disclosure of the detection methodology converts the monitoring criterion into an optimization target. Ostrom's design principles for self-governing commons - particularly the principle that those subject to monitoring participate in defining monitoring criteria - are partially a structural response to this. A monitored population that participates in setting the detection frontier has less incentive to engineer around it, because engineering around criteria they helped design produces outcomes they defined as violations. Whether this generalizes from common-pool resource management to the institutional contexts examined here is itself a question the Channel C analysis makes worth asking.

## Observable Implications

For the three cases examined, I have specified what evidence would distinguish Channel C from its alternatives. The general form of the tests:

**The harm distribution test**: Channel B predicts that harm per violation is constant before and after monitoring, because substance is preserved even as form changes. Channel C predicts that harm per violation increases as detected violations decline. Observable: collect violation-harm data pre- and post-monitoring, coded by violation type. A shift in the harm distribution toward the severe end, concurrent with a decline in detected violations, is Channel C's signature. A constant harm distribution with declining frequency is consistent with Channel A or B.

**The sophistication test**: Channel C predicts violations become systematically more sophisticated over time as the detection frontier clears less sophisticated actors. Observable: code violations by markers of deliberateness, planning horizon, resource requirements, or institutional access. A sophistication trend that outpaces general behavioral trends is Channel C evidence.

**The detection lag test**: As monitoring technology improves and the detection frontier expands, Channel C predicts that newly captured violations are less harmful than violations already captured - because newly captured violations are those just above the old frontier, while the most sophisticated violations remain outside the new frontier. A monitoring improvement that captures less-harmful violations than the prior regime captures is a Channel C signature; a monitoring improvement that captures more-harmful violations is evidence against Channel C in that setting.

These tests require data that monitoring programs rarely collect. Standard monitoring output tracks: violations detected, type from among monitored categories, and sanction administered. It does not typically track: harm magnitude by violation type, sophistication indicators, or comparison of within-frontier and beyond-frontier violation rates. Designing monitoring programs to produce these data is a precondition for evaluating Channel C, and is itself a policy implication of the analysis.

## Conclusion

The compliance literature has a mature debate about whether monitoring produces deterrence or compliance theater, and whether it crowds out intrinsic motivation. It has not named or systematically analyzed Channel C: the selection effect whereby effective monitoring of detectable violations concentrates the residual pool toward violations that are more sophisticated, harder to detect, and potentially more harmful on the dimension the original norm was designed to protect.

The three cases examined here support the mechanism hypothesis with varying degrees of empirical grounding. The pharmaceutical case is the strongest: the Kaplan-Irvin before-after evidence on publication bias is well-documented, the Channel A effect is established, and the mechanism by which outcome switching and analytical manipulation survive the registration frontier is specified and documentable. The credit rating case has a clean structural argument, partial empirical support in the documented pre-crisis engineering behavior, and an honest scope limitation on the specific causal chain from mandatory disclosure to the next generation of structured product engineering. The academic integrity case is a structured conjecture with specified observable implications, awaiting the longitudinal distributional data that would confirm or disconfirm it.

The policy implication, if the mechanism holds at these scales, is uncomfortable: monitoring programs should be evaluated not only by their effect on detected violation frequency but by their effect on the composition of undetected violations. A program that achieves a fifty percent reduction in detected violations while concentrating the residual pool in violations twice as harmful may be net-neutral in expected harm, or worse. The standard evaluative apparatus - tracking detected violations and their rate of change - cannot distinguish this outcome from a genuinely successful regime.

This is not an argument against monitoring programs. Channel A effects are real, consequential, and the primary mechanism in most settings. But it is an argument for designing monitoring programs with Channel C awareness: asking, before implementation, which violations fall outside the detection frontier; whether those violations are systematically worse on the underlying harm criterion; and whether any supplementary mechanism closes the gap at the sophisticated end of the distribution. Those questions are not currently standard practice in compliance program design. They should be.

## References

- Benmelech, E., and Dlugosz, J. (2009). "The Alchemy of CDO Credit Ratings." *Journal of Monetary Economics* 56(5): 617-634.

- Clarke, R., and Lancaster, T. (2006). "Eliminating the Successor to Plagiarism? Identifying the Usage of Contract Cheating Sites." Proceedings of the 2nd International Plagiarism Conference, Northumbria.

- Coval, J., Jurek, J., and Stafford, E. (2009). "The Economics of Structured Finance." *Journal of Economic Perspectives* 23(1): 3-25.

- Curtis, G.J., and Clare, J. (2017). "How Prevalent Is Contract Cheating and to What Extent Are Students Repeat Offenders?" *Journal of Academic Ethics* 15(2): 115-124.

- Frey, B.S., and Jegen, R. (2001). "Motivation Crowding Theory." *Journal of Economic Literature* 39(4): 589-611.

- Griffin, J.M., and Maturana, G. (2016). "Who Facilitated Misreporting in Securitized Loans?" *Review of Financial Studies* 29(2): 384-419.

- Kaplan, R.M., and Irvin, V.L. (2015). "Likelihood of Null Results of National Institutes of Health-Funded Clinical Trials Registered in ClinicalTrials.gov." *PLOS ONE* 10(8): e0132382.

- Mathieu, S., Boutron, I., Moher, D., Altman, D.G., and Ravaud, P. (2009). "Comparison of Registered and Published Primary Outcomes in Randomized Controlled Trials." *JAMA* 302(9): 977-984.

- Newton, P.M. (2018). "How Common Is Commercial Contract Cheating in Higher Education and Is It Increasing? A Systematic Review." *Frontiers in Education* 3:67.

- Ostrom, E. (1990). *Governing the Commons: The Evolution of Institutions for Collective Action*. Cambridge University Press.

- Power, M. (1997). *The Audit Society: Rituals of Verification*. Oxford University Press.

- Rowland, S., et al. (2018). "Just Doing the Math: Students' Understanding of the Risk of Being Caught Contract Cheating." *International Journal for Educational Integrity* 14(1).
