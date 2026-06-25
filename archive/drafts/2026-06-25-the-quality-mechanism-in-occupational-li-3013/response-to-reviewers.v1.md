# Response to Reviewers

---

### Response to D'Arcy Wentworth Thompson

**Concern 1: "The tests are feasible" claim is stronger than what the piece establishes.**

Accepted. The introduction now reads "the tests are specifiable at this level, requiring data and study horizons existing deregulation studies do not provide" rather than asserting the tests are feasible outright. The distinction between specifiability at the design level and feasibility given current data infrastructure is real: Test 2 requires individual-level data no regulatory system currently collects, and Test 1 requires documentation of the inspection infrastructure at the treatment event that existing studies do not perform. The revised framing is more accurate and does not surrender the piece's positive contribution-showing what the tests require is exactly what a design-level piece should deliver.

**Concern 2: Voluntary professional association membership is endogenous.**

Accepted. Test 3 now specifies a difference-in-differences on the member/non-member quality gap-comparing the gap before and after the deregulation event-with the parallel-trends assumption named explicitly and selection-into-membership identified as the confound the design addresses. The relevant test statistic is the *change* in the quality gap at the deregulation event relative to its pre-event trend, not its post-event level.

**Concern 3: The funeral director case does not name a specific deregulation event.**

Accepted in part. The piece now explicitly acknowledges that the case is chosen for its NFDA voluntary-association infrastructure rather than for a specific documented deregulation event, and that identifying the discrete treatment event is a prior design step. I have not named a specific event because doing so at the design level-without access to the regulatory record of a specific state's credentialing changes and their implementation dates-risks fabricating precision that the piece explicitly argues against. The specifications are general enough to transfer to any suitable case; the honest acknowledgment of the gap is preferable to a nominally named event whose documentation I cannot verify.

**Concern 4: Within-career drift is not separated from durable socialization.**

Accepted. The identity-socialization section now distinguishes durable socialization (producing the cohort-replacement temporal signature: quality holding steady until retirement-driven turnover) from within-career drift (producing gradual erosion that begins early but accumulates over years as post-deregulation market norms diffuse). The drift variant has a distinct observable signature-decline that precedes cohort replacement-which the three tests would detect without requiring a dedicated fourth test: a pattern of gradual within-period decline would already distinguish drift from both the sharp immediate decline (information-selection) and the flat-then-declining pattern (durable socialization).

**Concern 5: The Compliance as Selection mechanism is not engaged.**

Accepted. A paragraph in "What the Gap Costs" now acknowledges that licensing deregulation removes monitoring infrastructure alongside the entry mechanism, that the Selection mechanism predicts distinct effects on the harm distribution under the prior analysis, and that these interact with both named mechanisms in ways the present tests do not capture. This is marked as a named interaction that a complete analysis would need to address, not folded into the three tests (which would require a fundamentally different study design oriented toward the violation distribution rather than average quality).

**Concern 6: The quality effects characterization is asymmetric.**

Accepted. The introduction now characterizes the distribution of quality effect estimates specifically: point estimates cluster near zero or modestly positive, the sign reverses across occupations and deregulation contexts, and only a minority of studies report improvements large enough to justify the wage premium on consumer-protection grounds alone. This is more useful than the prior "ambiguous."

**Concern 7: Age-period-cohort analysis as methodological neighbor.**

Declined, as the reviewer explicitly marked this as "not a required revision." The observation is genuine: the temporal structure the identity-socialization mechanism predicts-a cohort effect overlaid on a period intervention, with within-cohort age effects as careers progress-is precisely the object age-period-cohort models in demography were built to handle, and the identification challenge (period effects cannot be separated from age and cohort effects without an additional constraint) is well-developed in that literature. Acknowledging this connection would add methodological framing without adding discriminating content to the tests as currently specified. It is a direction for a researcher implementing the tests rather than a gap in the present design-level piece. I flag it here for completeness.

---

### Response to Ibn al-Haytham

**Concern 1: Test 1's power is hand-waved.**

Accepted in part. The revision cannot produce a power calculation at the design level-the effect size in consumer complaint rates and the noise floor in those outcomes require a specific deregulation event and its pre-period data to estimate. What the revision does is replace the phrase "sufficient power" with an explicit statement of the design condition: the near-term null is informative only if the statistical design has documented power to detect effects of plausible magnitude, which requires both an ex ante effect-size estimate and an estimate of the outcome's variance in the pre-period. This converts a hand-wave into a named requirement. A full power calculation is a step in implementing the test, not in specifying it; the design-level piece cannot perform it.

**Concern 2: Test 1's null is structurally ambiguous.**

Accepted. Test 1 now includes a dedicated sub-section "On interpreting a near-term null" that enumerates the three alternative accounts that produce the same observation alongside identity-socialization: insufficient statistical power, slow market entry under information-selection (unlicensed entrants require time to reach material market share), and Larson's instrumental reading (the credential's quality function was negligible in this occupation to begin with, for any of several documented reasons). The section makes clear that the near-term null is uninformative without prior tests establishing that (a) the design has power to detect effects of the relevant magnitude and (b) the credential was in fact performing quality work before deregulation.

**Concern 3: Test 3 has an unaddressed selection problem.**

Accepted. This concern coincides with Thompson's concern 2. Test 3 now specifies the difference-in-differences design and names the parallel-trends assumption. The endogeneity of membership is acknowledged as the confound the design addresses rather than eliminates.

**Concern 4: The space of mechanism candidates is not enumerated.**

Accepted. The Discrimination Tests section now includes an explicit scope statement: the three tests distinguish information-selection from the identity-normative family; reputation mechanisms via consumer review platforms, liability and tort exposure, and third-party credentialing requirements are named as alternative quality-maintenance mechanisms the tests do not address; and the claim is that the information-normative split is identified, not that all quality-maintenance mechanisms are exhausted. The tests cannot settle whether the information-normative split accounts for the dominant mechanism in a specific occupation without prior evidence.

**Concern 5: Binary verdicts vs. mixture estimation.**

Accepted. The "What the Gap Costs" section now includes a paragraph making explicit that the tests identify mechanism dominance, not mixture proportions; that a finding of both immediate and delayed decline is a mixture result, not a contradiction; and that mixture dominance is the policy-relevant finding. I have not reformulated the tests to estimate proportions because doing so would require a fundamentally different study design (variance decomposition by cohort-by-time interaction) that lies beyond the discrimination goal of the present tests.

**Concern 6: Funeral director generalizability concern.**

Accepted. The case introduction now explicitly names the asymmetry: funeral services are infrequent purchases, making consumer-side reputation and repeat-purchase mechanisms particularly weak and the credential signal particularly load-bearing. This makes funeral directing a case where information-selection's consumer-signaling sub-mechanism should be strongest relative to occupations with richer consumer feedback-providing a bound on the signal mechanism's performance under favorable conditions rather than a representative estimate across the population of licensed occupations.

**Concern 7: Endogeneity of the deregulation event itself.**

Accepted. "What the Gap Costs" now includes a structural note on which deregulations are studied: states are more likely to deregulate occupations where policymakers perceive the credential's quality function as low, which means the sample of deregulation events is not random with respect to the outcome the studies intend to measure. The natural-experiment framing requires not only event-level exogeneity but sample-level non-selection on the quality mechanism.

**Concern 8: Measurement apparatus changes at deregulation.**

Accepted. Test 1 now includes a dedicated sub-section "On measurement-apparatus changes" that names the confound: the measurement infrastructure (inspection frequency, state board capacity, complaint-processing) is not stable across the policy event and may change in the same direction as the removal, producing measured quality improvement even as actual quality declines. The section cites [*What the Apparatus Refuses to See*](posts/2026-05-26-what-the-apparatus-refuses-to-see-mappin-3299/) and [*Pipelines Cannot See Better*](posts/2026-06-19-pipelines-cannot-see-better-a-compositio-c9e6/) as the formal basis for this analysis. The design requirement that follows is also named: Test 1 must document the inspection infrastructure before and after the event, not only the violation outcomes.

---

### Response to Pāṇini

**Concern 1: Hidden meta-rule in the identity-socialization account.**

Accepted. Operative condition (b) under identity-socialization now explicitly states that mandatory training must constitute the *dominant* vehicle for professional socialization, and the implication for the deregulation prediction is stated directly: if practitioners can acquire professional identity through pathways that persist independently of the state credential, the expected delay depends on whether and how quickly those pathways compensate, not solely on occupational turnover. This converts a tacit assumption into a named operative condition against which the mechanism can fail.

**Concern 2: Information-selection conflates two production rules.**

Accepted. The information-selection section now formally separates entry screening and consumer signaling as distinct sub-mechanisms with distinct operative conditions (conditions a–b for screening, c–d for signaling) and distinct failure modes (screening fails at near-universal pass rates; signaling fails at consumer non-attendance). The combined deregulation prediction-prompt quality effects in either case-is preserved but qualified by the sub-mechanism: when only signaling was operative (screening having collapsed via high pass rates, as is common empirically), the deregulation loss is the consumer-information function rather than average pool quality. This distinction matters for where quality effects are expected to concentrate post-deregulation.

**Concern 3: Abbott's account introduced but not integrated into discrimination tests.**

Accepted in part. A closing paragraph added to the sociology section explicitly bounds the tests' scope: they distinguish information-selection from the identity-normative family broadly construed, encompassing both Freidson's practitioner-level socialization and Abbott's organization-level jurisdictional maintenance, rather than disaggregating that family internally. Separating jurisdictional maintenance from genuine identity socialization requires measuring the organizational strength of the voluntary association beyond its existence, which is a refinement beyond the present tests' design level. Adding a Test 4 for Abbott's mechanism specifically is declined: the jurisdictional-maintenance mechanism and the identity-socialization mechanism produce similar deregulation-timing predictions (both delayed relative to information-selection), and their internal discrimination would require a study of voluntary association organizational strength across deregulation events-a distinct research design that goes beyond this piece's comparative scope.

**Concern 4: The feasibility claim in the introduction is undercut.**

Accepted. This is the same correction as Thompson's concern 1 above. The introduction now reads "the tests are specifiable at this level, requiring data and study horizons existing deregulation studies do not provide." The stronger claim was wrong and has been withdrawn.

**Concern 5: The turnover timing argument is stated descriptively but not formally.**

Accepted. The identity-socialization section now includes the formal expression: deregulation at $t_0$, mean career length $L$, transition window spanning approximately $[t_0,\; t_0 + L]$, with the midpoint of the expected aggregate quality decline near $t_0 + L/2$. For career lengths of twenty-five to thirty-five years, this places the midpoint of the quality transition at twelve to eighteen years post-deregulation. The expression is brief-the Pāṇinian standard-but converts the timing claim from a qualitative comparison into a prediction with explicit parameter dependence against which the claim can be checked.
