# Lab Notebook: Mechanism Audit of the Referral Hiring Literature

**20 May 2026**

The proposal committed me to a three-stage audit: extract the mechanism claims from four canonical texts, identify the pattern of specification gaps, and - for the most substantive gap - provide the missing pieces in enough detail that observable implications can be stated. This notebook records how the work actually went.

---

## Setting Up the Audit

The first thing I had to do, before touching any of the four texts, was stabilize the standard against which they would be measured. My curriculum response to Hedström and Ylikoski (2010) gave me a clear summary of the three-level framework: situational mechanism (macro conditions → individual beliefs, desires, opportunities), action formation mechanism (individual conditions → specific action, and why), aggregation mechanism (individual actions → macro outcome). The critical insight from that response was that the failure modes are characteristic: most social-science papers either report the macro-macro correlation without touching the micro level, or they gesture at individual causes without specifying the action formation logic or the aggregation step. Hedström and Ylikoski call this "a label, not an explanation."

I also needed to be clear about what the audit is and is not. It is not a survey of whether referral hiring effects are real - the empirical record on that is extensive and I am not disputing it. It is an audit of the *mechanism account*: the story about why contacts produce better matches, and how that story holds up at each of the three levels. These are different inquiries, and conflating them is how the referral hiring literature has largely avoided the scrutiny it deserves.

---

## Stage 1: Mechanism Extraction

Working through the four texts in sequence:

**Granovetter (1974), *Getting a Job*.** The foundational empirical study; less a mechanism account than an empirical characterization. Granovetter documents that 55–56% of professional and technical workers in his Newton, Massachusetts sample found their jobs through personal contacts, and that those contacts were disproportionately acquaintances rather than close friends. He notes the superior outcomes for contact-found jobs. The mechanism sketch is present but thin: contacts provide information about vacancies that formal channels do not, and the informal character of the communication reduces the credentialing effect that formal channels impose. What struck me most is how little weight is placed on the referrer's decision. The contacts in the book simply... refer. Their motivation is not examined.

**Granovetter (1985), "The Problem of Embeddedness."** This is the theoretical paper, and the most sophisticated in its situational mechanism. The paper attacks both the atomized actor of standard economics and the oversocialized actor of standard sociology. Real economic action is embedded in ongoing social relations, and those relations produce trust and transmit information in ways that neither the market-anonymous actor nor the role-following sociological actor would generate. The mechanism vocabulary is richer here: trust as a relational product, information about trustworthiness flowing through network-bounded channels, malfeasance inhibited by the reputational consequences within the network. But - and this became my central audit finding - the action formation mechanism in 1985 is at the level of tendencies, not decisions. Actors embedded in social relations *tend to* use network information; actors who behave opportunistically *face* reputational consequences. What is missing is the specification of when a particular actor, facing a particular hiring decision, uses or ignores network information, and why the network's assessment is trusted over formal credentials.

**Montgomery (1991), "Social Networks and Labor Market Outcomes."** The formal economics treatment, and the most satisfying in terms of mechanism completeness. Montgomery constructs a partial equilibrium model: workers are high or low type, firms cannot directly observe type, and a referral is a correlated signal of type (because network homophily means contacts of high-type workers are themselves more likely to be high-type). Employers rationally prefer referred candidates, and this preference generates wage dispersion that partly tracks network access. The employer's action formation mechanism is genuinely derived, not assumed.

But Montgomery's model contains an assumption that does most of the work and which he does not derive from a model of the referrer's decision: he parameterizes referral probability as p_H for high types and p_L for low types, with p_H > p_L. This is the claim that referrals are positively selective. It is stated as an assumption, bracketed with brief discussion, and never traced to a model of why the referrer - whose identity and interests are entirely absent from the formal structure - would generate a selection pattern with this property.

**Ioannides and Loury (2004), "Job Information Networks, Neighborhood Effects, and Inequality."** The synthesis paper in the Journal of Economic Literature; excellent at the situational level. It taxonomizes the mechanisms (information transmission, social capital, network screening), adds neighborhood effects and spatial dimensions to the situational story, and makes the inequality amplification argument more structurally explicit than anything in Granovetter. But the referrer action model remains parameterized rather than derived. The paper notes that "contacts may have reputational incentives to refer only high-quality workers," which is the right observation. It is made in one sentence. The formal treatments they survey all inherit Montgomery's assumption.

---

## Stage 2: Gap Identification

My hypothesis going in: situational mechanism well-specified, action formation partially specified, aggregation not specified beyond assertion.

The hypothesis is substantially confirmed, with an important nuance: the action formation gap is *bifurcated*. The employer's action is reasonably derived, especially in Montgomery's model; the referrer's action is not modeled at all. This is more specific than "partial specification" - it is a selective gap that runs through every formal treatment in the literature.

The aggregation gap is also confirmed, and it is sharper than I expected. The canonical literature establishes that individual jobs found through contacts are better; it claims this aggregates to labor market segmentation; the transformation from one to the other is not modeled. Ioannides and Loury come closest, with their discussion of network composition effects and neighborhood feedback, but they do not specify the dynamic logic by which bilateral referral events produce durable macro patterns rather than equilibrating away through competition.

---

## Stage 3: The Completion

The most substantive gap is the referrer's decision. I found that specifying what a complete referrer action model would require was more illuminating than I expected, because it immediately forced a distinction between two mechanisms that the literature runs together under the label "referral advantage": (1) the match-quality mechanism, which requires referral selectivity, and (2) the inequality-amplification mechanism, which does not require selectivity but only requires network homophily. These have different policy implications, and the conflation is not innocuous.

I was surprised by how clearly the aggregation gap appeared once the referrer's decision was made explicit. If referrers are promiscuous (refer everyone they know), the match-quality advantage disappears but the demographic sorting persists. If referrers are strategically selective (refer only candidates who will enhance their reputation), the match-quality advantage appears but its demographic distribution depends on the distribution of reputation stakes across groups. These are testable distinctions. That the canonical literature has not tested them - indeed has not posed them - reflects the absent referrer action model.

---

## What Did Not Work

The proposal anticipated that I might find the mechanism fully specified in post-2004 literature. I did not attempt a systematic review of that literature within the qualifying piece, as the proposal committed me to the canonical four texts. I flag in the draft that the gap may have been partially closed since 2004, particularly in labor economics treatments that use regression-discontinuity designs to isolate mechanisms. But that would be a different paper; the finding here is about what the canonical texts themselves establish.

I also considered whether Hedström and Ylikoski's framework is the right tool for a literature that partly operates at the network or organizational level, not the individual level. The proposal named this as a possible failure mode. I found it less serious than anticipated: the referrer's decision and the employer's decision are individual-level, and the aggregation question - how individual decisions produce market-level patterns - is precisely what the framework asks about. The framework does not fail to apply; the literature fails to meet it.

---

## Summary

The referral hiring mechanism is more complete than most social mechanisms in published work, and less complete than it presents itself. The situational mechanism has genuine structural content. The employer's action formation mechanism is formally modeled. The referrer's action formation mechanism is absent, the aggregation logic is verbal, and the distinction between the match-quality and the inequality-amplification claims has never been clearly made because making it requires the referrer's model. The essay develops this finding and proposes the missing specification.

---

---

## Revision Pass - 20 May 2026

Revised from draft following advisor review by Pierre Bayle. Six issues addressed; all accepted.

**Corpus expansion (Issues 4, 6).** Added Granovetter (1973) as a formal corpus text alongside the 1974 book. The prior draft cited 1973 throughout the situational mechanism discussion while listing only 1974 in the corpus - an inconsistency Bayle correctly flagged. The fix also required revising the imprecise "vocabulary...specification" formulation in the introduction and the standard section, which I replaced with direct statements of what is and is not specified at each level.

**Candidate mechanism evidence check (Issue 5).** Added a paragraph at the end of the action formation section noting that the canonical texts contain almost no evidence bearing on referrer motivation. This was the right call to make explicit: stating the absence as a finding is more informative than leaving the gap implicit. The observation that the assumed-selectivity property went unnoticed for decades because no canonical text tried to verify it is more damning than the gap itself.

**Aggregation specification (Issue 2).** This was the most substantive revision. The original draft pointed to Schelling as the methodological standard for aggregation but declined to specify what the aggregation step would require. Bayle asked for the parallel to the referrer model specification, and he was right: the piece committed in its proposal to providing "missing specification in enough detail that observable implications can be stated," and the aggregation section had not done that. The revised section specifies three requirements (employer hiring strategy model, dynamic network composition model, equilibrium conditions) and derives observable implications for each. It also explicitly states that providing the full aggregation model is beyond scope, with the reason: the aggregation model requires the referrer selectivity parameter as input, so the referrer model is prerequisite.

**Post-2004 literature horizon (Issue 1).** Chose Option B: explicit acknowledgment that the canonical texts are the audit object rather than the literature's outer boundary. Added a dedicated section with brief discussion of Beaman and Magruder (2012) as the most directly relevant post-canonical work and Calvó-Armengol and Jackson (2004, 2007) for the network dynamics. Beaman-Magruder turned out to be useful for the policy grounding issue as well - it is the first experimental test of the reputation mechanism for referrers, and its finding that explicit financial incentives produce quality-selective referral behavior is exactly what the canonical assumed-selectivity parameter required someone to verify.

**Policy grounding (Issue 3).** Replaced the abstract gesture at two policy types with a concrete analysis organized around Beaman-Magruder: formal referral bonus programs instantiate Channel A explicitly (financial stakes substitute for or supplement the ambient reputational stakes the canonical model assumes); vacancy-information-expansion programs instantiate Channel B. The analysis I wanted - showing that different program types address different mechanisms, and that conflating the channels produces an inability to diagnose which program type applies - can now be made from an actual experimental finding rather than from purely deductive reasoning. I chose not to cite a named policy document I could not verify, instead grounding the claim in the structural logic of program types.

**What the revision changed about my understanding.** Adding Beaman and Magruder (2012) to the references had a clarifying effect I did not anticipate: it showed that the canonical gap was not merely a theoretical omission but an empirical one. The field had to run an experiment to test whether the reputation mechanism operates, precisely because the mechanism was assumed in the canonical texts without verification. That the experimental literature arose partly to fill this gap is itself evidence that the gap was real and consequential.

The aggregation specification exercise also clarified something. When I worked through what a complete aggregation model would require, it became clear that the two candidate explanations for equilibrium durability (information monopoly vs. quality persistence) have implications that predict *across-occupation* variation in referral premiums in opposite directions. If information monopoly dominates, the premium should be larger where vacancy information is poorly disseminated; if quality persistence dominates, the premium should shrink as formal screening improves. These are testable predictions that the canonical literature, having skipped the aggregation specification, never generated.
