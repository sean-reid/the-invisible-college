# Does the Referral Hiring Mechanism Meet Its Own Standard?

The finding that a large fraction of jobs are found through personal contacts is among the most replicated in organizational sociology and labor economics. From Granovetter's foundational Boston study through the formal models of Montgomery and the synthesis by Ioannides and Loury, the empirical record is dense: contacts intermediate job matches, the contacts are disproportionately weak ties rather than close friends, and jobs found through contacts produce better wages, longer employment durations, and distinctive demographic sorting patterns. A researcher who disputes these findings is disputing a substantial body of careful evidence.

The question this piece pursues is different. Replication of a finding is not replication of a mechanism. The question is whether the *mechanism account* attached to these findings - the account explaining why contacts produce better matches, how the relevant information flows, what actors are doing and why, and how bilateral referral events aggregate into labor market-level patterns - satisfies the standard that mechanism-based explanation requires. Applying Hedström and Ylikoski's three-level framework as an audit tool, I find the answer is: at one level yes, at one level partly, and at one level no. The gap that matters most is the one the literature has hidden inside an assumption.

## The Standard

Hedström and Ylikoski's 2010 framework for causal mechanisms in the social sciences builds on the Coleman bathtub diagram, which distinguishes macro-level phenomena from individual-level processes and requires an account of all three transitions: from macro context to individual situation, from individual situation to individual action, and from individual actions to the macro outcome. They call these the situational mechanism, the action formation mechanism, and the transformation (or aggregation) mechanism.

Against this standard, most published social-science explanations fail in one of two characteristic ways. The first failure is the macro-to-macro correlation: the analyst documents that macro variable X covaries with macro outcome Y and calls the covariance an explanation. No individual-level process is specified; there is no account of what actors are doing or why. The second failure is the partial mechanism: the analyst describes the situational conditions and gestures at individual-level causes - "trust," "network pressure," "information flow" - without specifying the behavioral logic that selects a particular action given those conditions, or the aggregation step that converts many individual decisions into the macro pattern. Hedström and Ylikoski are particularly attentive to a further problem: mechanism-level vocabulary that names a process without specifying the entities and activities that constitute it. "Network embeddedness" is not yet a mechanism; it is a name for the site where a mechanism would need to be specified.

The referral hiring literature has the vocabulary. The question is whether it has the specification.

## The Four Canonical Texts

The corpus for this audit is Granovetter's 1974 *Getting a Job*, his 1985 "Economic Action and Social Structure: The Problem of Embeddedness," Montgomery's 1991 formal economic model, and Ioannides and Loury's 2004 synthesis in the *Journal of Economic Literature*. These four texts establish the empirical finding, supply the theoretical vocabulary, formalize the core mechanism, and synthesize the inequality claim. If the mechanism has been adequately specified in the referral hiring literature, these texts should show it.

I treat the canonical four as the object of the audit, not as the outer boundary of the literature. If subsequent work has closed the gaps I identify, that is a finding worth noting; the audit finding about the canonical texts would remain substantive.

## Level One: The Situational Mechanism

This is the strongest part of the literature, and the first level is where the account genuinely delivers.

Granovetter's theoretical contribution, developed fully in "The Strength of Weak Ties" (1973) and extended in the 1985 embeddedness paper, specifies the structural content of network position with real precision. Actors in dense, closed networks have contacts who communicate with each other; they possess largely redundant information. Actors with bridging ties to other clusters - "weak ties" that connect socially distant groups - have access to non-redundant information from those clusters. The information about job vacancies flows predominantly through weak ties because that is where the structurally non-redundant information lives. This is a genuine situational mechanism: it names the relevant entities (actors, network ties, clusters), the relevant structural properties (tie strength, network closure, bridging), and the process by which structural position translates into differential information access. It generates predictions - about who will hear about vacancies, not just that contacts matter.

Ioannides and Loury extend the situational mechanism with neighborhood effects and spatial composition. Residential segregation produces network segregation: actors in segregated neighborhoods have contacts concentrated in the same neighborhood, amplifying the compositional effects of homophily. The employers to whom those contacts connect are concentrated in local industries and firms. The situational story by 2004 is genuinely rich in structural content.

The situational mechanism, in short, passes. Social structure shapes information access, and the structural features that govern how it does so are specified with enough precision to generate testable predictions.

## Level Two: The Action Formation Mechanism - A Bifurcated Verdict

This is where the audit reveals something the literature presents as unified but is actually split.

**The employer's action is modeled.** Montgomery (1991) provides the clearest treatment. In his partial equilibrium model, workers vary in quality (high or low type), employers cannot directly observe type, and referrals function as correlated quality signals. The correlation exists because network homophily produces networks in which high-quality workers are disproportionately connected to other high-quality workers. An employer who faces a referred candidate from a high-quality employee can rationally update upward on the candidate's quality. The employer's decision to prefer referred candidates is derived from an optimization problem under uncertainty - it is not assumed but follows from the structure of the information problem and the properties of the signal.

Montgomery's model generates predictions: wage dispersion will track network access; workers with contacts at good employers will be more likely to get good jobs; employer reliance on referrals will be greater when formal credentials are less informative. These are the hallmarks of a genuine action formation mechanism - it specifies not just that employers act differently toward referred candidates, but *why*, and the why generates testable implications.

**The referrer's action is assumed.** This is the gap. In Montgomery's model, the referral probability is parameterized: high-type workers refer with probability p_H, low-type workers refer with probability p_L, and p_H > p_L. The positive selectivity of the referral process - the assumption that referred workers are disproportionately high quality - is built into these parameters. They are stated as an assumption and are never derived from a model of the referrer's decision.

Why would a worker refer another worker? The literature offers several candidate answers without formalizing any of them. Ioannides and Loury note that "contacts may have reputational incentives to refer only high-quality workers" - if a referral turns out badly, the referrer's standing with the employer declines. This is correct as far as it goes, and it is the candidate mechanism that would make p_H > p_L come out of a model rather than go in as an assumption. But the sentence is not followed by a model; it is followed by the next topic.

Other candidate mechanisms for referral behavior are not discussed in the canonical texts at all. Referrers might act from reciprocity (generalized norm of helping contacts) with no strategic calculation. They might act from social obligation (in tight communities, failing to refer an eligible contact incurs reputational costs within the community, not just with the employer). They might refer promiscuously, without quality discrimination, because the cost of a referral is low. These mechanisms have different observable implications:

- The reputation mechanism predicts that referral selectivity is higher in repeated-game employer-referrer relationships, lower in one-shot contexts, and responsive to feedback about referral quality.
- The reciprocity mechanism predicts referral rates uniform across contexts, uncorrelated with employer feedback.
- The social obligation mechanism predicts high referral rates in dense community networks regardless of quality considerations.
- Promiscuous referral predicts no positive selection effect, which conflicts with the match-quality finding and redirects the explanation entirely to information access (vacancies, not quality signals).

The canonical literature cannot distinguish among these because it does not model the referrer's decision. This is not a minor gap. The referrer's action is the hinge on which the entire mechanism account turns.

## Level Three: The Aggregation Mechanism

The referral hiring literature makes a claim not just about individual job matches but about labor market structure. The canonical finding is that network-mediated hiring produces wage inequality, demographic sorting, and persistent differences in employment rates across groups differentiated by race, education, and neighborhood. This is a macro-level claim. It requires a transformation account: how do bilateral referral hiring decisions, each operating through the individual-level mechanisms described above, aggregate into the observed labor market patterns?

The transformation account is absent. The canonical texts assert the connection rather than specify it. Ioannides and Loury come closest, with their synthesis of network composition effects and neighborhood feedback dynamics, but they describe the qualitative logic rather than derive the macro outcome from a specified aggregation mechanism. The informal argument runs: many employers rely on referrals; referral networks are demographically homophilous; therefore network-based hiring routes jobs disproportionately to the demographic groups already represented in a firm's workforce. This is plausible. It is not an aggregation model.

What is missing is the specification of the conditions under which bilateral network-mediated advantages are durable at the macro level rather than equilibrating away. Standard competitive markets erode informational advantages: if referred workers are systematically better, competing employers would bid up their wages, which would either equalize wages across channels or shift all hiring toward referrals, which would in turn shift the locus of inequality to network formation rather than hiring. The referral hiring literature treats the observed segmentation as a finding rather than as a phenomenon whose persistence requires explanation. A complete aggregation mechanism would specify why the equilibrating forces are weak and what maintains the segmentation over time.

This is not a requirement specific to this literature; it is what Hedström and Ylikoski mean when they insist on transformation mechanisms rather than verbal gestures at aggregation. The Schelling segregation model is the canonical example of what the aggregation step requires: a specification of how individually rational bilateral decisions, each operating through a simple local rule, produce an emergent macro pattern through the structural logic of interdependence and feedback.

## The Gap That Matters Most: The Referrer's Decision

The absent referrer action model has a consequence that the inequality claim in the literature has not registered. There are two distinct causal channels through which network-based hiring could produce inequality in labor market outcomes:

**Channel A: Match quality.** Referred workers are better-selected candidates. The employer's use of referrals improves match quality and raises wages for matched workers. Inequality arises because access to referral pipelines is unequal across demographic groups.

**Channel B: Information access.** Referred workers hear about vacancies that non-referred workers do not. The employer's use of referrals excludes candidates who lack network access to the vacancy, regardless of their quality. Inequality arises because information about vacancies is unequally distributed across demographic groups.

These are distinct mechanisms. Channel A requires referral selectivity - the referrer must be filtering for quality, so that p_H > p_L. Channel B operates even with promiscuous referrers who refer everyone they know, because the inequality is in who hears about the vacancy, not in the quality signal.

The canonical literature runs these channels together, which has produced a confused literature on policy responses. The evidence that referred workers receive higher wages and longer-duration employment is consistent with both channels: referred workers may be better matched (Channel A) or they may simply have been able to apply (Channel B). The demographic sorting finding is more diagnostic: it requires Channel B, because the sorting pattern is determined by network composition, not by quality differences that happen to be correlated with demographics. But the match-quality premium could come from either channel.

If Channel B is doing most of the work - if the primary effect is that referral networks gatekeep vacancy information - then policy responses aimed at improving referral quality (employer mentorship programs, accountability mechanisms for referrers) are largely beside the point. The intervention is to create information bridges: mechanisms that make vacancy information available to workers outside the current referral network. If Channel A is significant - if referrers are genuinely selecting for quality and employers are relying on that selection - then the intervention is different: it is to extend the reputation mechanism into communities currently excluded from it, so that high-quality workers in those communities can establish the referral relationships that make their quality credible to employers.

This distinction requires a referrer action model. Without specifying why referrers refer and how selectively, the evidence cannot tell us which channel is active.

## What a Complete Referrer Action Model Would Require

The missing specification is not exotic. It requires three things.

First, a specification of the referrer's objective function: what the referrer gains or loses from making a referral, as a function of referral quality and outcome. The reputation mechanism implies that the referrer's future value to the employer - as a source of referrals - depreciates with bad recommendations and appreciates with good ones. This generates an incentive to be selectively positive, provided the referrer has a sufficiently long time horizon and sufficiently repeated interactions with the employer. Where these conditions are absent (one-time relationships, high turnover, informal rather than employment-relationship connections), the reputation mechanism should be weak.

Second, a specification of the referrer's information: what the referrer actually knows about the candidate's quality, and how that knowledge compares to what the employer could learn from formal channels. The mechanism presupposes that the referrer has better information than the employer's formal screening could obtain. This is plausible for soft skills, cultural fit, and the quality of a candidate's judgment under pressure - attributes poorly captured by credentials and resumes. It is less plausible for technical skills that are directly testable. The mechanism should therefore be stronger in occupations where soft attributes dominate, weaker where hard skills dominate. This prediction is testable and to my knowledge has not been systematically tested against the mechanism account.

Third, a specification of equilibrium referral behavior: what the referrer does in equilibrium given their objectives and information, and what the resulting selectivity parameter p_H/p_L equals as a function of the structural features identified above. This is the object that Montgomery assumes; it is what a complete model would derive.

The formal apparatus required for this extension exists in the economics literature on reputation, repeated games, and information transmission. It has not been applied to the referrer in the referral hiring literature.

## Conclusion

The referral hiring mechanism account is, by the standards of the social sciences, relatively well-developed. It has a formal economic treatment, a rich situational story, and a long empirical record. Applying Hedström and Ylikoski's standard rigorously does not reveal a crude failure but a selective gap: the situational mechanism is specified, the employer's action formation mechanism is modeled, and everything that depends on the referrer's behavior is assumed rather than derived.

This matters because the literature has two claims - the match-quality claim and the inequality-amplification claim - that rest on different mechanisms, and the referrer action model is what distinguishes them. The match-quality claim requires referral selectivity; the inequality claim requires only network composition. The canonical literature treats these as a unified mechanism because it has not articulated the referrer's decision; and because it has not articulated the referrer's decision, it cannot specify what the aggregation step from bilateral referral events to labor market segmentation actually involves.

The finding generalizes beyond referral hiring. Many institutional mechanisms in the social sciences - trust in markets, norms in organizations, credentialing in professions - have the same structural gap: the actor whose decision propagates the mechanism is described by their role in the aggregate outcome, not analyzed as an agent with objectives and information. The audit methodology I have applied here identifies such gaps with some precision. Whether the referral hiring mechanism has been progressively closed since 2004 is an open question; whether the canonical texts leave it open is not.

## References

- Granovetter, M. (1973). "The Strength of Weak Ties." *American Journal of Sociology* 78(6):1360–1380.
- Granovetter, M. (1974). *Getting a Job: A Study of Contacts and Careers*. Harvard University Press.
- Granovetter, M. (1985). "Economic Action and Social Structure: The Problem of Embeddedness." *American Journal of Sociology* 91(3):481–510.
- Hedström, P. and Ylikoski, P. (2010). "Causal Mechanisms in the Social Sciences." *Annual Review of Sociology* 36:49–67.
- Ioannides, Y.M. and Loury, L.D. (2004). "Job Information Networks, Neighborhood Effects, and Inequality." *Journal of Economic Literature* 42(4):1056–1093.
- Montgomery, J.D. (1991). "Social Networks and Labor Market Outcomes: Toward an Economic Analysis." *American Economic Review* 81(5):1408–1418.
