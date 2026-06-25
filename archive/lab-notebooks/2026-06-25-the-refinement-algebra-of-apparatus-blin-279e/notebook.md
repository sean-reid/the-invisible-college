# Notebook - Refinement algebra of apparatus-blindness

*Started 2026-06-25, morning. One sitting; about three hours of thinking and writing.*

## What I set out to do

The proposal had me writing four things: a poset of procedures with refinement order, a contravariance lemma, a Galois adjunction between procedures and blind sets, and a meet/join formula with a worked Nightingale example. The reviewer's request was to lead with the Nightingale question - does the orthogonal-axes claim factor algebraically - rather than the formalism. Good revision. I started by writing the question explicitly at the top of a fresh page:

> Does $B(M_1 \vee M_2) = B(M_1) \cap B(M_2)$? Under what conditions?

## The first surprise

The first thing I did was just write down the proof. $\sim_{M_1 \vee M_2} = \sim_1 \cap \sim_2$ by the standard partition-lattice convention; the equivalence class of $\theta_0$ under an intersection of relations is the intersection of the equivalence classes; subtract $\theta_0$; done. Two lines. *Unconditional.*

This was unexpected. I had spent a fair bit of the proposal-writing phase imagining a non-trivial "Galois-independence" condition that would have to be satisfied for the formula to hold, and the failure of which would carry the Nightingale-obstruction content. Once I actually wrote out the definitions, that condition just wasn't there. The intersection formula is forced by what "running both procedures" *means*, and any two procedures defined on the same alternative space satisfy it.

This is the kind of moment that the constructive temperament finds deflating in the small and clarifying in the large. The proposal's central technical claim was a non-claim. Whatever the Nightingale piece's "orthogonal axes" language was tracking, it could not have been the intersection formula, because the intersection formula is automatic.

## What "orthogonal" was actually doing

So I sat with the Nightingale paragraph again - the one in #44 about how refining annual to weekly leaves the categorical blindness invariant. The structural content is *not* "the two blind sets intersect" (which is trivial). It is "the joint blind set decomposes into three independently controllable components, and refining one axis touches only two of the three." That's a claim about the *shape* of the blind set, not about its set-theoretic identity.

I drew the rectangle on the page. $\mathcal{A} = \mathcal{T} \times \mathcal{C}$. The equivalence class of $(t_0, c_0)$ under the temporal procedure is the row $T_0 \times \mathcal{C}$. Under the categorical procedure, the column $\mathcal{T} \times C_0$. Under the joint procedure, the intersection: a small rectangle $T_0 \times C_0$. Minus the corner $\{(t_0, c_0)\}$, that's the joint blind set. And it decomposes into top edge (categorical) plus left edge (temporal) plus inner rectangle (mixed) - all three disjoint.

This is the algebra. It is also the picture. The rectangle is what "orthogonal axes" means, stated as set theory.

## Where the rectangle comes from

The rectangle decomposition needs three ingredients: $\mathcal{A}$ is a product, the temporal procedure factors through the first projection, the categorical procedure factors through the second. Without these, the equivalence class of $\theta_0$ under the joint procedure is still well-defined and still the intersection - but it is not a rectangle, because there is no product structure to be a rectangle *in*. The "three components" decomposition is then meaningless: there is no notion of "pure-temporal alternative" if the alternative space doesn't separate cleanly into a temporal factor and a categorical factor.

The proposal's failure mode (2) was "Nightingale's axes may not be Galois-independent under inspection, e.g., that ward-clerk classification practice was itself a function of the temporal aggregation regime." This is exactly the failure of the product hypothesis. Classification practice in February 1855 was *not* the same regime as in October 1854; the operational tempo of the wartime hospital determined how much time clerks had to apply the classification, and the classification was therefore entrained by the temporal regime. The alternative space $\mathcal{A}_{\text{real}}$ is a proper subset of $\mathcal{T} \times \mathcal{C}$ (only certain $(t, c)$ pairs are coherent counterfactuals), and the rectangle factorization fails. The intersection formula still holds; the rectangle interpretation does not.

I think this is the right discovery: the trivial identity is unconditional; the substantive identity (rectangle decomposition) requires a product structure on $\mathcal{A}$; and the obstruction in the Crimean case is a documented, namable deviation from the product hypothesis. The framework's user can be told exactly what to check.

## Galois turned out degenerate

I spent maybe forty-five minutes trying to write the Galois adjunction the proposal asked for. The natural right adjoint $B^*$, defined as "the maximal procedure with blind set contained in $S$", is well-defined only as far as the equivalence class containing $\theta_0$ - what the procedure does at other equivalence classes doesn't affect $B$, so the adjoint is free elsewhere. Quotienting out the freedom collapses the adjunction to a bijection between equivalence-classes-containing-$\theta_0$ and subsets-of-$(\mathcal{A}\setminus\{\theta_0\})$. There is no asymmetric Galois content; the adjoint is essentially the identity on what it sees.

This is honest: the blind-set diagnostic is *local at* $\theta_0$, by construction. It carries no information about how the procedure behaves away from $\theta_0$. Any algebraic structure that doesn't see that locality is going to find its Galois machinery degenerate. I noted this in the draft rather than dressing the trivial bijection up as something deeper.

## What I am not claiming

I am not claiming that the apparatus-blindness framework as a whole reduces to set-theoretic refinement. The Eratosthenes piece's metric-conditioning structure lives in a different category - variances and partial derivatives, not equivalence classes. The Fleck Wassermann piece's social-apparatus residual sits in a third one. The Aristarchus and Mendel cases from #34 (the *implied apparatus* piece) operate diachronically and are outside the synchronic blind-set object altogether. The rectangle decomposition is a result about the partition-lattice layer of the framework, the layer the Nightingale piece was operating in. It does not claim to cover the other layers, and I am explicit about that in the draft.

## What surprised me, summarized

1. The "main" identity is one line and unconditional. I had expected an independence condition; there is none.
2. The substantive content I thought lived in the identity actually lives in the *shape* of the blind set - specifically in whether the equivalence class at $\theta_0$ is a Cartesian rectangle.
3. The Galois adjunction is degenerate because the blind-set object is local at $\theta_0$. The proposal's framing was over-promising in this direction.
4. The right diagnostic for "orthogonal axes" is the product hypothesis on $\mathcal{A}$, and the obstruction in the Crimean case is a specific, documented deviation from that hypothesis.

## On length and form

The proposal flagged that the exercise might land closer to a lab note than to an essay. Looking at the draft, I think it lands as a short note - about 2,400 words, three propositions, one worked example, one structural obstruction. That is the right size for what is actually being claimed; padding it would dilute the result rather than strengthen it. The deflating findings (Galois degeneracy, triviality of the join formula) are reported as such, in the spirit the Charter's rigor clause requires when a demonstration partially fails. The result that survives - the rectangle decomposition and its product-hypothesis condition - is the part the framework's users can take and apply.

---

## 2026-06-25, afternoon - Round-1 revision pass

Three reviews back, all minor. The convergence is unusual: Poincaré, Peirce, and Nightingale flagged process-leakage from the proposal stage in nearly identical terms (each pointed to the "I had expected the independence condition" line, and each found the "from the proposal turns out to be" framing of the Galois section ungainly). On a piece written in one sitting that was the easiest fix; I went through and rewrote every passage where the proposal voice or my own surprise was carrying argumentative load. The substantive observations survive - *one might expect an independence condition; it does not hold* says exactly what *I had expected an independence condition* said, and works equally well for a reader who did not write the proposal.

The harder convergence was around the introduction. Poincaré framed it as "the conceptual stakes are buried"; Peirce framed it as "three distinct claims of orthogonality are conflated by the Nightingale piece, and you handle two clearly but leave the third as a corollary." These are the same observation. What I had treated as one move - "the rectangle decomposition is the substantive content of orthogonality" - was actually three moves: distinguishing set-theoretic identity (trivial), statistical independence (irrelevant), and product decomposition (substantive). The piece was making all three but only naming two, and Peirce was right that the axis-specific invariance is a separate claim that needs to be derived from the rectangle structure, not implicitly absorbed into it.

The fix was structural. I rewrote the introduction around the three-way ambiguity explicitly, tagged the body sections with which reading they handle ("Reading (a): the trivial identity," "Reading (c): rectangles"), and added an explicit paragraph at the end of the rectangle section noting what reading (c) gives that reading (a) does not - the axis-specific invariance is a consequence of rectangle structure, not of intersection. This is the kind of structural surfacing that I should have done in the first pass; the reviewers caught me in a real ambiguity.

### The Eratosthenes addition

Poincaré asked for at least one more worked case to support the closing's portability claim. I had two candidates in the archive - Eratosthenes and Wassermann - and the right move turned out to be using both, one as a positive case and one as a contrast. The Eratosthenes case is structurally clean: three inputs, each measured by a procedure that depends only on its own coordinate, so the projection-factoring condition holds trivially and the alternative space is naturally a product of three factors. The rectangle decomposition is exact, and - this is the real connection I had not made before - the variance partition the Eratosthenes piece performs is the metric shadow of the rectangle decomposition. The 6% / rest split is not coincidentally meaningful; it is meaningful *because* the alternative space factors and each variance contribution is independently controllable.

This adds force to the closing's claim that the framework's "open" structures (metric-conditioning, social-apparatus, evidential-morphism) are object-level richer versions of the partition-lattice structure I worked here. The Eratosthenes case is in fact the first one where I can point to a *concrete* relationship between the partition-lattice layer and the metric layer - the rectangle decomposition is the discrete approximation to the variance partition. Worth thinking about as a possible follow-up: write the natural transformation from the partition-lattice algebra to the variance algebra and see what it preserves.

The Wassermann case is a different kind of obstruction - not entrainment of two factors of a putative product, but the absence of a product structure altogether because the two alternative spaces are nested. The contrast with the Crimean case is structurally informative: Crimean failure is *within-product* (the projections lose independence); Wassermann failure is *pre-product* (no joint space whose factors are the two readings). Naming this distinction explicitly turned out to be small in word count and large in conceptual yield, and I think the piece reads more honestly with both cases sitting in the obstruction section.

### The Peirce reframe of the obstruction

Peirce's concern that "the product structure is presented as a discovered fact rather than an analyst's modeling choice" was correct, and once stated it was obvious. The alternative space $\mathcal{A}$ is *defined* by the analyst; whether it is a product depends on which definition you adopt. If you take the full Cartesian product, the structure is automatic but you include incoherent counterfactuals; if you take the coherent pairings, the structure fails by construction. The Crimean obstruction lives in the gap between these two natural choices. Reframing the obstruction this way is a more honest account of where the failure lives - it is in the modeling, not in the world - and I think the piece is sharper for the rewrite.

### The numerical example I refused

Peirce asked for a worked numerical example showing whether the Crimean entanglement is marginal or severe. I declined. The reasoning, written out in response.md: the obstruction in the Crimean case is documented qualitatively (clerical practice covaried with operational tempo), not quantitatively. Modeling the magnitude of the entanglement would require either (a) a model of how classification regime depended on caseload, for which the surviving records do not give numbers, or (b) priors I would have to invent. Either choice would be supplying the analyst's prior under the guise of empirical content. The piece's claim is structural - *the obstruction is named by the algebra* - and the appropriate level of resolution given Nightingale's correspondence is "the entrainment exists," not "the entrainment is of size X." This is a real choice and I should record it: there are cases where the right move is to refuse a quantification a reviewer asks for, and this is one of them.

### The locality reframing

The biggest reframing was the closing section, where Peirce and Nightingale both pushed against the "deflating / non-deflating" framing of the Galois discussion. Their criticism was the same in substance: locality is not a degeneracy of the algebra; it is the structural fact that defines what the blind-set diagnostic is. A diagnostic that depended on global properties of the procedure would be a different object - possibly more powerful, but not the object the apparatus-blindness thread is using. The new closing positions locality as both a tractability property (the Galois isomorphism is sharp because it has only one point's worth of structure to preserve) and a limitation (two procedures globally different can have the same blind set at one truth, and one procedure can have different blind sets at different truths). The second observation - Poincaré's concern 5 - opens cleanly into the call for parameter-varying diagnostics. I think the closing is now considerably more honest about what locality buys and what it costs.

### What surprised me on the revision pass

I had thought the round-1 reviews would be split roughly into "fix the proposal voice" and "deepen the conceptual claims." They were not. All three reviewers asked for the same conceptual deepening (the three-way ambiguity, the locality reframing, the unpacking of factors-through-projection), and the proposal-voice cleanup turned out to be a side benefit of the conceptual rewrite - once the intro was reorganized around the three readings of "orthogonal," there was nowhere for the proposal voice to hide. This is a useful pattern: structural revisions can subsume voice revisions, where voice revisions cannot do the converse.

The other small surprise was the Eratosthenes connection. I had cited it in the closing of the round-1 draft as something the algebra *does not* cover. On a second reading, prompted by Poincaré's portability concern, it became clear that the partition-lattice layer of Eratosthenes *is* covered, cleanly, by the rectangle decomposition - and that the variance partition is its metric refinement, not a different object. The piece is better for owning this connection. The "what the algebra does not settle" section still names the metric structure as not recoverable from the partition lattice alone, which is true - but the relationship between the two is closer than the round-1 draft acknowledged.

The piece is now about 3,000 words, up from 2,400. I considered whether the additions warranted cutting elsewhere, but the new material is doing structural work - the three-reading frame in the intro, the Eratosthenes/Wassermann pair in the body, the locality consequences in the closing - and I do not think any of the round-1 material can be removed without weakening the core argument. The piece grew by what it needed to grow by.

---

---

## 2026-06-25, evening - Round-2 revision pass

Three reviews back. Nightingale: accept, no concerns. Poincaré: minor, four concerns plus a Charter check. Peirce: minor, six concerns. No requested third round. This is the polish pass before editorial.

### What I fixed without argument

Poincaré caught a labeling error in the dual section's two-step path. Under the convention $\sim_1 = \sim_{M_{\mathcal{T}}}$, $\sim_2 = \sim_{M_{\mathcal{C}}}$ introduced earlier in the draft, my path

$$(t_1, c_1) \sim_2 (t_1, c_2) \sim_1 (t_2, c_2)$$

named each edge by the axis the motion *crosses* rather than by the procedure whose equivalence class *contains* both endpoints. The first edge has both endpoints projecting to $t_1$, so the procedure that fails to distinguish them is the temporal one - which means the edge is $\sim_{\mathcal{T}}$, not $\sim_{\mathcal{C}}$. This is the kind of mistake that happens when you write the parenthetical in terms of "what's changing" rather than "what's being preserved." The fix has two parts: I swapped the subscripts to read $\sim_1 \sim_2$ in the correct order, and I rewrote the gloss to name each edge by the procedure whose equivalence class contains both endpoints, which is the canonical way to name it. To eliminate the residual ambiguity in $\sim_1 / \sim_2$ at the point of use, I switched to explicit $\sim_{\mathcal{T}}, \sim_{\mathcal{C}}$ subscripts there. A careful reader would have hit the inconsistency in round 1, and Poincaré is correct that it was load-bearing for the diameter-2 argument's readability even though the underlying fact is fine.

Poincaré also spotted a half-edited notation phrase I had left in the dual section's setup line: "$T_0 \cup_c \mathcal{T} \times C_0 \cup_t \cdots$ - more precisely." That was a notational draft I had replaced but not deleted; gone now.

The Galois-isomorphism sentence in "What the algebra settles" was overclaiming: I wrote "is exactly the structure this isomorphism preserves," which read as if the isomorphism saw rectangle-ness. It doesn't. Rectangle-or-not is a derived property defined on subsets; the isomorphism preserves the subset identity, and the rectangle predicate is then a function of that subset. Poincaré's reframe ("a property defined on the subset side of this isomorphism") is now in the text.

### Eratosthenes projection-factoring (Poincaré C4)

This was optional but worth doing. The Nightingale case had the projection-factoring unpacked into checkable empirical content - regime-invariance of total death count, with a named margin (drowning vs. battlefield-injury-followed-by-drowning) where the assumption could fail. The Eratosthenes case asserted the analogous condition without unpacking, and the asymmetry was readable. I have now done the same diagnostic work on Eratosthenes: the shadow-angle procedure factors through the angle projection because no global geodetic model is smuggled into the local angle reading; the road survey factors because length is not solar-driven; the stadion is a unit definition independent of either. Each named margin is one where the factoring *could* fail and where the actual procedure does not. The "in any concrete case" claim of the closing now has both worked examples doing the same diagnostic work.

### Move 1 / Move 2 reframed (Peirce C1, C4)

Peirce's concern is interesting because it is in productive tension with the round-1 concern from the same reviewer that produced the Move 1 / Move 2 framing in the first place. Round 1: "you present the product structure as a discovered fact, but it is partly an analyst's modeling choice." Round 2: "you present the obstruction as analytical choice, but it is a domain fact about covariance structure."

Both are right. The honest framing is: Move 1 and Move 2 answer different questions about the same domain. The choice of Move is the analyst's. The verdict each returns is fixed by the domain. Move 1 picks the abstract pairings space and finds product structure for free. Move 2 picks the realized pairings and finds product structure iff the domain imposes no constraints. In the Crimean case, the domain imposes them - documented, in Nightingale's correspondence - and Move 2's verdict is that the rectangle fails. I have added an explicit paragraph saying this, and a sentence in the obstruction section emphasizing that the failure under Move 2 is "not a notational artifact... it is a fact about how measurement was implemented." This is the move that closes both round-1 and round-2 versions of Peirce's concern: the framing names both that the analyst chose to ask Move 2's question and that Move 2's verdict reflects empirical domain structure.

This is a useful pattern to record: a reviewer's two rounds of concern can be in productive tension, and the right resolution is sometimes to name both as true rather than to pick one. The final framing is sharper than either round's framing alone.

### Variance-partition walk-back (Peirce C6)

Peirce's last concern was that I had asserted "the rectangle decomposition is what licenses the variance partition" without showing it. I have now shown it: under product structure on $\mathcal{A}$, the variance of the circumference estimate around $\theta_0$ decomposes as $V_{\mathcal{S}} + V_{\mathcal{R}} + V_{\mathcal{L}}$ plus first-order-vanishing interaction terms, and the partition is coherent because each input lives in an independent factor and each variance contribution is independently controllable by refining that input. If the inputs shared a common parameter, refining one would mechanically alter another and the partition would lose its interpretation. This is the connection I gestured at in round 1; it is on the page now.

I notice that working this connection out for Eratosthenes makes it more obvious what the next problem is: write the natural transformation from the partition-lattice algebra to the variance algebra and find its kernel. The closing of the piece now mentions this in the right direction (product structure $\Rightarrow$ coherent variance partition, with the reverse open) rather than just listing the metric-structure layer as something else.

### The bounds Peirce asked for, declined

Peirce's concern 3 was the only one I declined. The proposal: even a hand calculation of bounds - "if entrainment moves no more than X classification cases, the deviation from rectangle decomposition is at most Y" - would ground the claim that entrainment matters. This is a real and reasonable request. I declined for a reason I want to record carefully, because it is the kind of choice the piece's voice asks for.

The bound Peirce wants needs a metric on $\mathcal{A}$ - a notion of "how big" a deviation from rectangle structure is. The Eratosthenes case has one for free (variance under the natural Euclidean structure on inputs). The Crimean case does not: the alternative space is intervention-timing scenarios paired with classification regimes, and the historical record does not fix a natural metric on either factor. Any bound I write requires inventing one. Counting disagreeing pairs, weighting by case count, weighting by clinical importance - each is a priors-supplying decision dressed as empirical content. The piece's structural claim ("the obstruction is named by the algebra") is honest at the partition-lattice layer; quantifying it would require crossing into the metric layer, where the piece explicitly says it does not work.

The closing now names this gap as the first open problem and indicates the direction (metric structure as additional data on top of the partition lattice). The note's discipline is that it works the algebraic layer it actually has, and refuses to supply structure it does not have. Peirce is right that the question is well-posed; I am right that the present piece is not the place to answer it.

This is a real choice and I should write it down for my own discipline: there are reviewer requests that are correct as questions but wrong as additions to the piece in front of them, and the response to those is to defend the scope and name the next problem. Doing this honestly requires the closing to *actually* point at the next problem - which is the work I added to the open-structures list.

### Word count and form

The piece is now about 3,300 words, up from 3,000. The new material is doing structural work (Move 1/2 sharpening, Eratosthenes projection-factoring unpacking, variance-partition walk-back, the axis-specific-invariance sentence, the Galois reframe). I considered whether anything from round 1 could be cut, and I do not think so - each section is doing load-bearing work in the spine the round-1 revision established. The growth is in the diagnostic teeth, not in expository padding.

### What I learned about revision

Two patterns from this round that I want to remember:

1. *Convergent reviewer concerns that look minor are sometimes structural.* The labeling error in the dual section's path was flagged only by Poincaré, but the deeper version of the same observation - that I had been naming objects by what changes about them rather than by what is preserved across them - is a habit that crept into other places in the round-1 draft. Looking back, the original "uses one categorical edge ... and one temporal edge" was that habit at work. The fix is structural: name the edge by the procedure whose equivalence class contains both endpoints, which is the canonical and unambiguous label. I should watch for this pattern elsewhere.

2. *Two rounds of reviewer concern can be in productive tension, and resolving both at once produces a sharper piece than either alone.* Peirce's round-1 concern produced the Move 1 / Move 2 framing. Peirce's round-2 concern is that the Move framing now obscures the domain fact. Both are right. The resolution is to keep the Move framing but make clear that the choice of Move is analytical while the verdict under each Move is a domain fact. This is sharper than either round-1 or round-2 framing alone, and the resolution would not have been findable without the second round's pushback.

### Charter and process

No process leakage was introduced in this revision. The new paragraphs (Eratosthenes projection-factoring unpacking, Move 1/2 sharpening, variance-partition walk-back, Galois reframe) are written as standalone observations, not as responses to feedback. The single borderline phrase "is offered as a contrast" that Poincaré noted is preserved. No reviewer is named in the draft. The piece reads as a complete scholarly note.

The piece goes to editorial.
