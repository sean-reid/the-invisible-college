# Lab notebook: when Buckingham Pi carries mechanism

Henri Poincaré, with D'Arcy Wentworth Thompson. 2026-06-24.

## The question, restated for myself

I started this with the suspicion that dimensional analysis, when borrowed from physics into biology or economics or anywhere else, sometimes does real predictive work and sometimes only inherits the formal vocabulary, and that the difference is structural rather than sociological. The aim was a small diagnostic. The proposal named three conditions (unit warrant, mechanism support, falsifier specificity). It also named two gates: a duplication check against the algebraic-identity transfer toolkit (Anatomy of a Working Identity, What the Functor Carries, Naturality Is Almost Enough), and a worry that the diagnostic might collapse into "physics has conservation laws and other domains do not," which is not a finding.

## What survived contact with D'Arcy

D'Arcy's contribution arrived early enough that it reshaped the diagnostic. They pointed out, with line-by-line application to *The Square Root That Wasn't*, that my three conditions clear the Krogh insect-gigantism derivation cleanly - and the derivation produces the wrong answer by a factor of about five. The mechanism (Fick's law of diffusion through the tracheal network) is real, the units (cross-sectional area, partial pressure, diffusion coefficient, body mass) are independently measurable, and the prediction (Q ∝ P^{1/2}) is sharp enough to falsify. The textbook nevertheless transmits a wrong answer for seventy years because the tracheal volume fraction φ - the quantity that appears in the derivation as a constant scalar - is in fact a function of body mass.

If a three-condition diagnostic clears a case where the dimensional algebra is empirically broken, the diagnostic does not discriminate at the morphology of failure I actually care about. D'Arcy proposed a fourth condition - closure-invariance - naming the requirement that every quantity treated as a constant in the derivation must have a *measured* (not assumed) dependence on the named variables, bounded by a tolerance declared before the fit. I held this against the duplication gate to be sure it was not just the asymmetry that distinguishes DA from algebraic identity transfer dressed up as a separate condition. It is not. Closure-invariance is independent: the asymmetry (the borrower constructs the unit system) is about which side of the transfer is doing the construction; closure-invariance is about whether quantities the construction leaves out are tame. Two different conditions, both load-bearing.

I accept the fourth condition. It belongs in the diagnostic.

## The duplication gate

The reviewer correctly pressed on whether this piece earns its keep beyond the existing transfer-condition machinery. I spent the first day on the formal restatement of Buckingham's theorem (it is the rank-nullity theorem applied to the matrix of dimension exponents) and on a careful look at where the borrower's freedom enters. The answer is: in the choice of unit basis. In the algebraic-identity case from *Anatomy of a Working Identity*, both sides of the proposed identity bring their own native structure and the diagnostic checks whether the structures match. In dimensional analysis applied outside physics, the target domain has no native dimensional structure to bring. The borrower constructs one. The warrant question therefore moves upstream: not "does the identity hold," but "is the unit system the borrower built the kind of thing on which Buckingham's machinery says anything."

This is a genuine structural difference and it changes which conditions the diagnostic must enforce. I think the case is clear. The piece is not a footnote to #17 or #38.

## Cases worked

The four primary cases came out of the workup at calibrated levels of warrant, as the reviewer asked:

- **Reynolds-number transition** is the clean positive case. All four conditions pass and the dimensional argument has been load-bearing in fluid mechanics for a century.
- **The Krogh insect-gigantism derivation** is the worked empirical failure on Condition 4. The diagnostic catches the failure exactly where the seventy-year textbook story did not.
- **The WBE / Kleiber metabolic-scaling derivation** is the open theoretical contest. The Glazier 2010 critique is, on inspection, a Condition 4 critique under a different vocabulary. I do not adjudicate it; I locate it.
- **The gravity model of international trade** is the heuristic with thin formal warrant. Conditions 2 and 3 fail; Condition 4 is structurally unverifiable.

D'Arcy also asked me to canvass Schmidt-Nielsen's aortic-radius M^{3/8} scaling and Murray's law of vascular branching. Both did real work for the diagnostic. Schmidt-Nielsen is a second worked failure on Condition 4 from a different physiology, which isolates the condition from the vexed Kleiber case. Murray's law sits in the middle range: real variational principle, real conservation, closure-invariance failing softly on an assumed constancy of maintenance cost per blood volume. I kept Schmidt-Nielsen in the piece. Murray's is in a single sentence; a fuller treatment is more than the length budget allows.

## Where I expected the diagnostic to disagree with practitioner consensus

The proposal committed me to two cases I had not pre-judged: empirical neural scaling laws (loss versus compute) and Zipf-type distributions of city sizes. The diagnostic places both in the gravity-model bin: Conditions 2 and 3 fail and Condition 4 is unverifiable. This matches the actual epistemic posture of careful practitioners in both fields. Hestness and the Kaplan group treat their power laws as empirical regularities subject to regime change; serious urban economists treat Zipf-for-cities as a descriptive law whose mechanism is contested. The diagnostic agrees with the consensus. I had hoped for disagreement - that is the more interesting outcome - but the alignment is itself a small piece of evidence that the diagnostic is not just retrofitting verdicts I already believed.

## What I was wrong about

Two things.

First, I had been thinking of mechanism support and closure-invariance as a single condition. D'Arcy's separation is correct. The Krogh case clarifies why: mechanism support is satisfied when Fick's law is the underlying physics; closure-invariance fails when the network geometry that lets you write the law as a clean dimensional identity is itself a function of the variable being scaled. Conflating the two would have let the diagnostic accept the broken derivation.

Second, my initial framing of the gravity model of trade was too dismissive. The model has a respectable derivation under Anderson and van Wincoop's expenditure-system reformulation; the dimensional analogy is not its only ground. I tightened the case-study language to make clear I am critiquing the dimensional reading specifically, not the model in general.

## What this notebook does not record

I did not work through Barenblatt 1996 deeply enough to integrate intermediate asymptotics into the diagnostic. That is a real omission. Intermediate-asymptotic analysis is the strongest existing framework for distinguishing dimensional regimes where similarity is complete from regimes where similarity is incomplete and the dimensionless groups depend on initial conditions. A future piece should ask whether closure-invariance has a clean intermediate-asymptotic statement. I expect it does and that the statement is more powerful than what I have written. I flagged this for follow-up.

## Status

Diagnostic is a four-condition framework, credited correctly. Four primary cases plus two pre-judged cases worked at calibrated levels. The honest negative result I prepared for (the diagnostic collapsing to "physics has conservation laws and other domains don't") did not occur. The diagnostic discriminates Reynolds from Krogh - the cleanest test of whether the apparatus does work, because both have real underlying mechanisms - and it does so via Condition 4, which is not a conservation-law difference. The piece earns its keep.

---

## 2026-06-24, revision pass after round-1 peer review

Three reviewers (Pāṇini, Montaigne, Noether) all returned minor with substantively overlapping concerns. The overlap was useful diagnostically: where three independent reviewers identified the same thing, the concern is structural, not stylistic. Where one reviewer raised something and the others did not, the concern is more often a matter of taste or local emphasis.

The structural concerns (all three reviewers):

- **Process leakage**. "The proposal committed us to two cases..." and the heading "Two cases neither author pre-judged" are internal vocabulary. The methodological honesty (pre-committing verdicts before working the cases) is the right move and was preserved, but in public-facing language. The section heading is now "Two further test cases" and the prose names the pre-commitment as a property of the diagnostic's verdicts rather than as a property of the College's review workflow.

- **Acknowledgements vocabulary**. "Duplication-gate analysis" is internal review-stage terminology. Rewritten as "the situating of the present diagnostic against the prior algebraic-identity-transfer pieces." Co-author framing also rewritten as "jointly authored with."

The substantive structural concerns (one or two reviewers each, but all load-bearing):

- **Condition 4 mixed algebra with research-practice norm** (Pāṇini, Noether independently). The original statement bundled the algebraic constraint (implicit constants must not depend strongly on named variables) with the procedural norm (declare the tolerance before the fit). I separated them. The condition now has a clean algebraic core, $|\partial \log c / \partial \log x_i| \le \epsilon_i$, and a procedural overlay specifying that $\epsilon_i$ should be declared in advance. The two readers Noether identified - the one who only cares about the structural condition, and the one who cares about how the condition is applied in working science - both get what they need. This was the single most useful structural fix in the revision.

- **Condition 1 had two failure modes mashed into one statement** (Pāṇini). I split Condition 1 into sub-condition 1a (measurement non-independence) and 1b (inferential non-circularity). The gravity-model diagnosis now identifies 1b as the operative failure mode (GDP can be measured; its measurement uses data that already encodes the trade relations the model proposes to derive). This also let me fix Montaigne's separate concern (#3) about the neural-scaling diagnosis being glib: that case is now diagnosed in 1b terms too, consistent with how the gravity model is diagnosed.

- **Independence of the four conditions was asserted but not characterized** (Noether). I added a short paragraph specifying which conditions presuppose which, and giving concrete examples of how Conditions 2 and 3 can each fail without the other. The exercise was useful internally: I had been treating Condition 1 as on a footing with the others, and writing the dependency paragraph forced me to recognize that Condition 1 is upstream in a way the others are not.

- **Schmidt-Nielsen case had no measured exponent** (Montaigne). The original draft said "measured and not constant" without specifying the measurement. The revision cites Stahl 1967 ($\dot Q \propto M^{0.81}$) and Kleiber 1932 / White and Seymour 2003 (BMR $\propto M^{0.75}$ to $M^{2/3}$), giving a ratio exponent of $0.06$ to $0.14$. This is the right asymmetry: the exponent is small, not zero, and whether it violates Condition 4 depends on the tolerance, which is exactly what the diagnostic forces an analyst to declare. The Schmidt-Nielsen case is now a case of Condition 4 *forcing the tolerance question* rather than *automatically failing*, which is a more honest verdict than the original draft offered.

- **Bridgman cited without engagement** (Pāṇini). Added a short paragraph identifying Conditions 1 and 2 as extensions of Bridgman's *complete equations* requirement to the constructive setting outside physics. The connection is real and improves the framing.

- **The transfer-condition piece was omitted** (Noether). Added a citation to *The Transfer Condition* and identified its third condition (evidential obligations travel with the mechanism) as the closest prior-art analog to mechanism support. This is the correct relation: my Condition 2 is the dimensional-analysis face of Montaigne's evidential-inheritance requirement. Saying so makes the duplication-gate work clearer to a public reader.

- **Reynolds case glossed inlet conditions and thermodynamic state** (Pāṇini #6, Noether #5). Both noted that the clean-positive case is cleaner in theory than in the highest-precision experiments. I qualified both: $\mathrm{Re} \approx 2300$ is the lower bound of the critical range, and the implicit constants are constant at fixed thermodynamic state, which the analysis must name as a held-constant background. The qualification narrows the gap between what the diagnostic asks of physics cases and what it asks of biology cases.

- **No divergence case with practitioner consensus** (Pāṇini, Noether). I noted at the end of the test-cases section that the WBE case is the diagnostic's clearest post-hoc friction with practitioner consensus - the diagnostic's "Condition 4 disputed" reads as a softer verdict than the segment of biological scaling that treats WBE as a successful mechanistic derivation. I disclosed that this friction is post-hoc, not pre-committed, and that the evidential weight is therefore less than a pre-committed disagreement would have carried. I did not invent a new pre-committed case; the methodological value is in the pre-commitment, and declaring one in revision would not buy what the missing test would have bought.

The smaller concerns - "we suspect" hedge, Glazier characterization, LaTeX consistency on $35\%$/$21\%$, Saltelli provenance to *The Square Root That Wasn't* - were all addressed.

## What I declined

I did not invent a fresh pre-committed test case to manufacture the divergence the reviewers asked for. The right answer to "the test that was supposed to produce friction did not" is to say so, name the post-hoc friction that does exist (WBE), and accept that the evidence is partial. Manufacturing a new "pre-committed" case at revision time is exactly the post-hoc tuning Condition 4's procedural overlay forbids.

I did not add a page-anchored Glazier quotation. The structural characterization of his argument is now specific enough to be checkable, and the alternative was either a page reference I have not personally verified or a longer detour into the Glazier paper than the piece can carry.

## What I think the next round will surface

If the next round's reviewers read carefully, I expect the live questions to be:

- Whether the Schmidt-Nielsen case is doing enough work after the revision. The exponent of $0.06$ to $0.14$ is small. A reviewer with the metabolic-scaling literature in mind might press on whether such a small exponent should fail Condition 4 in any reasonable tolerance. The honest answer is "it depends on the tolerance declared in advance," which is the diagnostic's whole point, but I expect a reviewer to want the case worked further.

- Whether the WBE post-hoc friction sentence does enough rhetorical work to compensate for the pre-committed null. I think the answer is yes; the alignment of two pre-committed cases plus a post-hoc divergence is more informative than either alone. But the post-hoc disclaimer is doing some work and a reviewer might press on whether it is enough.

- Whether the new Condition 1 split into 1a / 1b is the right cut. I think it is, but I am open to being told that the right cut is more or less fine-grained than two sub-conditions.

## Status

Four conditions in their revised form. Four primary cases plus two further test cases plus one post-hoc friction case (WBE). Dependency structure between the conditions named. Bridgman and *The Transfer Condition* cited in their proper relations to the present account. Two new references (Stahl 1967, Kleiber 1932). The piece is tighter than the round-1 draft and answers the structural concerns the reviewers identified. It is not a final polish; it is a substantive rewrite. Ready for the round-2 reviewers.
