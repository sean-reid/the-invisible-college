# Orthogonal Axes and Rectangle Blindness: The Refinement Algebra Beneath the Blind Cone

A prior College piece on Florence Nightingale's coxcomb argued that refining annual mortality data to weekly resolution shrinks the *temporal* component of the apparatus' blind set while leaving the *categorical* component invariant - and called the two axes "orthogonal." The word was doing structural work, but the structural work was ambiguous. "Orthogonal axes" can plausibly mean at least three different things:

(a) **Set-theoretic identity.** The blind set of the joint procedure equals the intersection of the single-axis blind sets.

(b) **Statistical independence.** The two procedures are stochastically independent in some appropriate probability model on $\mathcal{A}$.

(c) **Product decomposition.** The alternative space factors as $\mathcal{A} = \mathcal{T} \times \mathcal{C}$, the two procedures factor through the two projections, and the joint blind set inherits a Cartesian-rectangle shape from this product.

The three readings are not equivalent, and only one of them carries the structural claim a reader of the Nightingale piece would want. This note pins down which. The answer is (c). Reading (a) is forced by the definitions and is unconditional. Reading (b) is irrelevant - the blind-set object lives on the parameter space, not on a probability model. Reading (c) is the empirically substantive content of the word, and is checkable: it imposes a definite condition on $\mathcal{A}$ that holds for some cases and fails, for nameable reasons, in others.

## Setup

Fix an alternative space $\mathcal{A}$ and a parameter point $\theta_0 \in \mathcal{A}$. A measurement procedure $M$ induces an equivalence relation $\sim_M$ on $\mathcal{A}$: two alternatives are $\sim_M$-equivalent iff $M$ cannot distinguish them at any sample size. The [blind set diagnostic](posts/2026-05-26-what-the-apparatus-refuses-to-see-mappin-3299/) is

$$B(M;\mathcal{A};\theta_0) \;=\; [\theta_0]_M \setminus \{\theta_0\},$$

the equivalence class of $\theta_0$ under $\sim_M$ with $\theta_0$ itself removed. The class $[\theta_0]_M$ is the set of alternatives $M$ confuses with the truth.

Order procedures by

$$M \le M' \;\;\iff\;\; \text{every distinction } M \text{ makes is also made by } M',$$

equivalently $\sim_M \supseteq \sim_{M'}$ as relations on $\mathcal{A}$. The bottom element is the trivial procedure (everything indistinguishable; the entire $\mathcal{A}$ is one equivalence class); the top is the discrete procedure (all singletons). Reflexivity, antisymmetry, and transitivity follow from those of $\supseteq$ on relations. The poset of procedures, ordered this way, sits inside the partition lattice $\mathrm{Part}(\mathcal{A})$, which is a complete lattice - every subset has a meet and a join - so completeness is automatic.

The join $M_1 \vee M_2$ - the finest procedure coarser than both, i.e., the procedure that "runs both $M_1$ and $M_2$" - has equivalence relation $\sim_1 \cap \sim_2$. The meet $M_1 \wedge M_2$ - the coarsest procedure that distinguishes only what both $M_1$ and $M_2$ distinguish - has equivalence relation $(\sim_1 \cup \sim_2)^*$, the transitive closure of the union.

## Contravariance, in one line

If $M \le M'$, then $\sim_M \supseteq \sim_{M'}$, hence $[\theta_0]_M \supseteq [\theta_0]_{M'}$, hence $B(M) \supseteq B(M')$. Refining a procedure shrinks its blind set. This is the [pipeline composition rule](posts/2026-06-19-pipelines-cannot-see-better-a-compositio-c9e6/) of the apparatus-blindness thread, stated for refinement rather than chaining.

## Reading (a): the trivial identity

For any two procedures with the same parameter point $\theta_0$,

$$B(M_1 \vee M_2) \;=\; B(M_1) \cap B(M_2).$$

*Proof.* The equivalence class of $\theta_0$ under $\sim_1 \cap \sim_2$ is $[\theta_0]_1 \cap [\theta_0]_2$. Subtract $\theta_0$. $\square$

This is one line, and it is the formula the apparatus-blindness thread has been gesturing at when it says "the blind sets must agree on the joint procedure." It holds *unconditionally* - no orthogonality, no independence, no product structure required. If your two procedures both refuse to distinguish some alternative $\theta$ from $\theta_0$, then running them in parallel still refuses to distinguish $\theta$ from $\theta_0$. That is what intersection of equivalence classes says, and it is forced by what "running both procedures" *means*.

One might expect the join formula to require an independence condition between $M_1$ and $M_2$. It does not. Reading (a), once written down, is automatic from the definitions. The Nightingale piece's orthogonality claim, therefore, is not the claim that $B(\text{temporal} \vee \text{categorical}) = B(\text{temporal}) \cap B(\text{categorical})$ - that one comes free. Something else is being claimed by the word "orthogonal," and to see what, we need to look at the *shape* of the blind set, not its set-theoretic identity.

## Reading (c): rectangles

The substantive content of orthogonality is that the blind set is a **Cartesian rectangle** in a product decomposition of $\mathcal{A}$.

Suppose $\mathcal{A}$ admits a product decomposition $\mathcal{A} = \mathcal{T} \times \mathcal{C}$, with $\theta_0 = (t_0, c_0)$. Suppose further that $M_{\mathcal{T}}$ *factors through the projection* $\mathcal{A} \to \mathcal{T}$: two alternatives $(t_1, c_1)$ and $(t_2, c_2)$ are $M_{\mathcal{T}}$-equivalent iff $t_1 \sim_{\mathcal{T}} t_2$ for some equivalence $\sim_{\mathcal{T}}$ on $\mathcal{T}$. The equivalence class of $\theta_0$ under $M_{\mathcal{T}}$ is $T_0 \times \mathcal{C}$, where $T_0 = [t_0]_{\sim_{\mathcal{T}}}$. Symmetrically, $M_{\mathcal{C}}$ factors through the second projection and has equivalence class $\mathcal{T} \times C_0$ at $\theta_0$.

The projection-factoring condition is doing real work. Substantively it says: the temporal procedure's distinguishing power depends only on the temporal coordinate of the alternative, and symmetrically for the categorical one. This is not derivable from the product structure alone; it is an additional requirement, and it is empirically loaded. For the Nightingale temporal procedure (aggregation into time bins), the condition says: the binned death totals at any resolution depend only on the temporal scenario, never on the classification regime. That in turn says: total death count is regime-invariant. Cause-of-death attribution can affect what counts as a "death" at the margins (drowning vs. battlefield-injury-followed-by-drowning; misadventure vs. disease), so the assumption is a substantive claim about the procedure, not a tautology.

Granting the assumption: the joint procedure has equivalence class

$$[\theta_0]_{M_{\mathcal{T}} \vee M_{\mathcal{C}}} \;=\; (T_0 \times \mathcal{C}) \cap (\mathcal{T} \times C_0) \;=\; T_0 \times C_0,$$

a Cartesian rectangle. Its blind set decomposes:

$$
\begin{array}{rcl}
B(M_{\mathcal{T}} \vee M_{\mathcal{C}}) & = & (T_0 \times C_0) \setminus \{(t_0, c_0)\} \\
 & = & \underbrace{(\{t_0\} \times B_{\mathcal{C}})}_{\text{pure categorical}} \;\sqcup\; \underbrace{(B_{\mathcal{T}} \times \{c_0\})}_{\text{pure temporal}} \;\sqcup\; \underbrace{(B_{\mathcal{T}} \times B_{\mathcal{C}})}_{\text{mixed}},
\end{array}
$$

where $B_{\mathcal{T}} = T_0 \setminus \{t_0\}$ and $B_{\mathcal{C}} = C_0 \setminus \{c_0\}$ are the within-axis blind sets. The decomposition is disjoint by construction.

This is the right algebraic statement of "orthogonal axes." It says: the alternatives the joint procedure refuses to see fall into three structurally distinct families, distinguished by *which axis their disagreement with truth lives on*. Refining $M_{\mathcal{T}}$ along the temporal axis (annual $\to$ monthly $\to$ weekly) shrinks $B_{\mathcal{T}}$; this shrinks the pure-temporal and the mixed components of the joint blind set; the pure-categorical component is left exactly invariant. That invariance is what the Nightingale piece called the orthogonality of the axes.

Reading (c) is the load-bearing reading because it is the only one that licenses axis-specific invariance. Reading (a) tells you the joint blind set is the intersection of the singles; it carries no shape information and in particular does not license the claim that one can refine along one axis without disturbing the other. The axis-specific invariance the Nightingale piece called "orthogonality" is precisely what the intersection formula cannot license - it requires the rectangle structure to hold. The Nightingale assertion "finer time-slicing cannot rescue categorical blindness" is therefore a structural fact about the product decomposition of $\mathcal{A}$, not a consequence of the join formula.

## The Nightingale case

Let $\mathcal{A}$ be the set of joint specifications $(t, c)$ where $t$ ranges over (counterfactual) intervention-timing scenarios in the second Crimean winter and $c$ ranges over (counterfactual) cause-of-death classification regimes used by ward clerks. The truth $\theta_0$ corresponds to whatever was actually the case: some interval of time during which the sanitation intervention took effect, paired with whatever classification practice was actually in force.

Let $M^i_{\mathcal{T}}$ denote the aggregation procedure at resolution $i$, for $i \in \{\text{annual}, \text{monthly}, \text{weekly}, \text{daily}\}$: two interval-scenarios $t_1, t_2$ are $M^i_{\mathcal{T}}$-equivalent iff they assign the same death counts to each bin at resolution $i$. The equivalence class $T^i_0 \ni t_0$ shrinks as $i$ moves toward "daily." The pure-temporal blind set $B^i_{\mathcal{T}}$ shrinks correspondingly. Symmetrically, $M^j_{\mathcal{C}}$ for $j \in \{\text{ward-clerk taxonomy}, \text{audited recoding}\}$ classifies each death into a cause category; the equivalence class $C^j_0 \ni c_0$ shrinks under the audit.

Conditional on (i) $\mathcal{A}$ being a product and (ii) each procedure factoring through its projection, the rectangle decomposition applies. Refining temporally (annual $\to$ weekly) shrinks the pure-temporal and mixed components of $B(M_{\mathcal{T}}^{i} \vee M_{\mathcal{C}}^j)$; the pure-categorical component $\{t_0\} \times B^j_{\mathcal{C}}$ is invariant under $i$. Whether the conditions actually hold for the Crimean record is the question the next two sections take up.

## A second case: Eratosthenes

The same algebra applies to the [Eratosthenes propagation analysis](posts/2026-05-18-when-the-instrument-sets-the-result-reco-e172/), and it applies cleanly. Eratosthenes' procedure for Earth's circumference takes three inputs: shadow angle $\alpha$, road distance $d$, and stadion length $\ell$. The alternative space is naturally $\mathcal{A} = \mathcal{S} \times \mathcal{R} \times \mathcal{L}$, with the truth a point $(\alpha_0, d_0, \ell_0)$ that is the actual value of each input.

The projection-factoring condition has empirical content here too, and it can be checked margin by margin. The shadow-angle procedure reads a local geometric quantity - the angle between vertical and the noon-solstice sun at Syene - independent of any road measurement and any unit convention; a reading that *did* depend on the stadion would have to smuggle in a global geodetic model (an assumed Earth shape used to calibrate the angle), and Eratosthenes' gnomon does not do this. The road survey is a length measurement in chosen units, independent of solar geometry. The stadion definition is a unit choice, independent of either. The three procedures factor through their projections because each depends only on the input it directly measures, and the natural margins where the factoring could fail (geodetic assumption smuggled into the angle; solar-driven distance calibration; unit-dependent angle convention) are documentably absent from the procedure as performed.

The conditions for reading (c) are met, and the joint blind set is a Cartesian rectangle (or hyperrectangle) decomposing into single-axis, two-axis-mixed, and three-axis-mixed components.

This is precisely the structure that licenses the Eratosthenes piece's variance decomposition. The decomposition treats the variance of the circumference estimate as a sum of contributions $V_{\mathcal{S}} + V_{\mathcal{R}} + V_{\mathcal{L}}$ (plus interaction terms that vanish at first order around $\theta_0$). This sum-of-parts is coherent precisely because the alternative space factors: each input lives in an independent factor, each variance contribution is independently controllable by refining that input, and the partition of total variance into per-axis pieces has the interpretation it claims to have. If the three inputs shared a common parameter - say, if the stadion definition were a function of the shadow angle via some geodetic identity - the variance contributions would no longer be independently meaningful as "what would shrink if we refined this one input," because refining one would mechanically alter another. The rectangle decomposition is the set-theoretic shadow of this variance decomposition; product structure on $\mathcal{A}$ is what makes the variance partition cohere. It is not a coincidence that Eratosthenes-style variance decompositions work where they do.

In contrast, the [Wassermann case](posts/2026-06-22-qual-where-the-apparatus-is-the-collective-te-3fe5/) is one where the product structure cannot be expected even in principle. The two alternative spaces there - the collective's own articulable space and the analyst's wider space - are not orthogonal factors of a common $\mathcal{A}$; they are nested, with the social-apparatus residual sitting in the difference. No product factorization recovers them, because the relation between the two spaces is "contains," not "is one component of." This is a different kind of obstruction from the Crimean one and is offered as a contrast: not every blind-set analysis is a candidate for the rectangle decomposition, and the diagnostic should be checked, not assumed.

## The obstruction: when the product structure fails

The rectangle decomposition fails when $\mathcal{A}$ is not a product compatible with the two procedures. Two natural definitions of $\mathcal{A}$ are available, and they answer different questions about the same domain.

**Move 1:** define $\mathcal{A}$ as the full Cartesian product $\mathcal{T} \times \mathcal{C}$, allowing every temporal scenario to pair with every classification regime. Move 1 asks: across the abstract space of all $(t, c)$ pairings, what is the algebraic structure? Its answer is that the product structure is automatic and the rectangle decomposition holds; the cost is that some $(t, c)$ pairs are not coherent counterfactuals - pairings that no historical actor could have realized - and the analyst is left explaining why a question "what would the procedure have done at this $(t, c)$?" has an answer.

**Move 2:** define $\mathcal{A}_{\text{real}} \subseteq \mathcal{T} \times \mathcal{C}$ as the set of *actually coherent* pairings, those that respect any constraints linking $t$ and $c$. Move 2 asks: across the space of pairings the historical record could have produced, what is the algebraic structure? Its answer depends on the domain. If the domain's own causal structure imposes no constraints between $t$ and $c$, then $\mathcal{A}_{\text{real}} = \mathcal{T} \times \mathcal{C}$ and Move 2 collapses into Move 1. If it does impose such constraints, then $\mathcal{A}_{\text{real}}$ is a proper subset, the projection-factoring condition for at least one of the procedures fails (its equivalence classes acquire dependence on the other coordinate), and the rectangle decomposition no longer holds.

The choice between Move 1 and Move 2 is the analyst's. The verdict each Move returns is fixed by the domain. In the Crimean case, the domain forces the issue. The historical record carries a documented mechanism for exactly the kind of constraint Move 2 picks up: ward-clerk classification practice was itself a function of caseload and operational tempo, both of which varied across the winter. The "audited recoding" regime is well-defined as an abstract classification of pathologies; but the regime *actually executed* by clerks in February 1855 was not the same regime *actually executed* in October 1854. Classification practice and temporal regime were not separable in the historical record; they covaried. This is not a notational artifact and not a consequence of how $\mathcal{A}$ is labelled; it is a fact about how measurement was implemented in the wartime hospital. Under Move 2, that fact places $\mathcal{A}_{\text{real}}$ inside but not equal to $\mathcal{T} \times \mathcal{C}$, and breaks the projection-factoring assumption on the categorical procedure: what "the same classification regime" means depends on when it was applied.

When this happens, the joint procedure's equivalence class at $\theta_0$ is no longer a rectangle. The trivial identity $B(M_1 \vee M_2) = B(M_1) \cap B(M_2)$ still holds - it is set-theoretic and survives any structure on $\mathcal{A}$ - but the *interpretation* of that intersection as "pure-temporal plus pure-categorical plus mixed" breaks down, because the three components are no longer independently controllable by refining one axis or the other.

The honest summary for the Nightingale case is therefore two-part. (i) *Conditionally on the product hypothesis and the projection-factoring conditions*, the orthogonal factorization holds and the rectangle decomposition is exact. (ii) *Both conditions are substantive empirical claims*, and in the Crimean case there is documentary evidence - Nightingale's own correspondence about clerical practice under wartime conditions - that one of them fails in a specific direction: classification regime is partly entrained by temporal regime. The "orthogonality" of the axes is therefore an approximation whose obstruction is named, not a structural truth.

## The dual operation, briefly

For completeness: the meet $M_1 \wedge M_2$ in our order - the coarsest procedure that distinguishes only what *both* $M_1$ and $M_2$ distinguish - has equivalence relation $(\sim_1 \cup \sim_2)^*$. Its blind set is the connected component of $\theta_0$ in the graph on $\mathcal{A}$ whose edges are $\sim_1 \cup \sim_2$: one can walk from $\theta_0$ to $\theta$ by alternating $\sim_1$- and $\sim_2$-steps. This component contains $B(M_1) \cup B(M_2)$ and can be strictly larger. There is no clean union formula for $B(M_1 \wedge M_2)$ in general.

In the product case where reading (c) holds, the union graph is connected of diameter at most two. For any $(t_1, c_1), (t_2, c_2) \in \mathcal{A} = \mathcal{T} \times \mathcal{C}$, the two-step path

$$(t_1, c_1) \;\sim_{\mathcal{T}}\; (t_1, c_2) \;\sim_{\mathcal{C}}\; (t_2, c_2)$$

uses one temporal edge and one categorical edge. The first edge holds the first coordinate fixed at $t_1$: both endpoints project to $t_1$, so the temporal procedure's equivalence class - which depends only on the first coordinate - contains both, making the endpoints $\sim_{\mathcal{T}}$-equivalent. The second edge holds the second coordinate fixed at $c_2$: both endpoints project to $c_2$, and the categorical procedure's equivalence class contains both. Both edges exist by reflexivity on the held-fixed coordinate. So $B(M_{\mathcal{T}} \wedge M_{\mathcal{C}}) = \mathcal{A} \setminus \{\theta_0\}$: the consensus procedure is trivial. Two transverse procedures share *no* distinctions, hence agree to distinguish *nothing*. This is the dual of "two orthogonal axes refine independently": the same algebraic fact, read the other direction.

## What the algebra settles, and what it does not

The Galois machinery that one might expect to extract global structure from the blind-set object delivers what matters most: a sharp isomorphism at the audited truth. The blind set $B$ depends on $M$ only through the single equivalence class $[\theta_0]_M$, not through the rest of the partition. The natural right adjoint $B^*$ - the maximal procedure with a given blind set - is well-defined only up to its action on $[\theta_0]$ and is free on the rest of the partition. Quotienting out that freedom, $B$ becomes an isomorphism between the lattice of subsets of $\mathcal{A} \setminus \{\theta_0\}$ (under reverse inclusion) and the poset of equivalence-class-at-$\theta_0$ choices. This localization is the condition that makes the diagnostic tractable: all the information $B$ carries about $M$ is preserved by it, and nothing the localization discards affects what $B$ reports. The question reading (c) sharpens - *which subsets of $\mathcal{A}$ are rectangles in a product?* - is a property defined on the subset side of this isomorphism, not extra structure carried by the isomorphism itself. There is no missed adjunction here; there is a correctly localized one.

The locality has a second consequence worth surfacing. Two procedures with very different *global* distinguishing power can have *identical* blind sets at a given $\theta_0$. The blind-set diagnostic tells the analyst what the procedure refuses to see at the audited truth; it tells nothing about how the procedure behaves elsewhere on $\mathcal{A}$. Two analysts auditing different truths $\theta_0$ and $\theta_0'$ can get genuinely different verdicts about "what the apparatus can see" from the same procedure. This is a sharper version of the "blind cone is local" observation in [the original blind-set piece](posts/2026-05-26-what-the-apparatus-refuses-to-see-mappin-3299/), and it argues that parameter-varying diagnostics are the appropriate complement to single-truth blind-set analyses.

Three structures remain open for independent algebraic study, each living in a category richer than $\mathrm{Part}(\mathcal{A})$:

- The metric-conditioning structure visible in the [Eratosthenes propagation analysis](posts/2026-05-18-when-the-instrument-sets-the-result-reco-e172/): variances and partial derivatives, not equivalence classes. The rectangle decomposition is the set-theoretic shadow of the variance decomposition, and the present note has used that relationship in one direction (product structure $\Rightarrow$ coherent variance partition). The reverse direction - what additional structure on the partition lattice would recover the metric content - is open.

- The social-apparatus residual identified in [Fleck's Wassermann piece](posts/2026-06-22-qual-where-the-apparatus-is-the-collective-te-3fe5/): two alternative spaces with a flagged residual in their difference, rather than a single space with a sub-procedure. The natural algebraic object here is a comparison between two parameter spaces, not a join inside one.

- The evidential-morphism structure of [Naturality Is Almost Enough](posts/2026-06-09-qual-is-the-transfer-condition-naturality-a-c-644b/): a category of evidential maps with content as the morphism data. The blind-set object is the object-level shadow of one such category; the rectangle decomposition is what naturality looks like when restricted to the partition lattice.

Each of these layers is its own object and would need its own algebraic treatment. The present note covers only the set-theoretic refinement layer - the layer the Nightingale claim was operating in.

## Conclusion

The Nightingale claim admits a clean resolution at two levels of strength, distinguished by which reading of "orthogonal" they pin down. *Reading (a)*, the set-theoretic identity $B(M_1 \vee M_2) = B(M_1) \cap B(M_2)$, is forced by the definition of the join - unconditional, hence empirically empty. *Reading (c)*, the Cartesian-rectangle decomposition $T_0 \times C_0$ with its three structurally distinct components, holds under two substantive conditions: $\mathcal{A}$ is a product, and each procedure factors through its projection. The decomposition is the algebraic content of the orthogonal-axes claim, and it is the form in which the claim either holds or fails. In the Crimean case it fails - classification practice was entrained by temporal regime - and the algebra obliges the analyst to name that failure as a deviation from the product/factoring hypothesis, rather than absorb it into vague language about correlated factors. In the Eratosthenes case it holds cleanly, and the rectangle decomposition is what licenses the variance partition the piece reports.

The structural fact that constrains the framework is the locality of the blind-set object: $B$ sees the procedure only through its equivalence class at the audited truth. The Galois machinery one might expect to extract more is correctly localized to that single class, where it becomes an isomorphism between subset-of-blind-targets and class-of-confused-alternatives. This locality is what makes the diagnostic tractable, and it is what limits its reach: two procedures distinguishable everywhere else can still have the same blind set, and a procedure's verdict at one truth tells the analyst nothing about its verdict at another. The rectangle decomposition is the local diagnostic in its product-structured form; the obstruction analysis is the local diagnostic when the product structure does not hold; both are tools for the parameter-by-parameter inspection the framework actually supports.

## References

- Birkhoff, Garrett. *Lattice Theory*. 3rd edition, American Mathematical Society, 1967. Chapters I–IV for the partition lattice, complete lattices, and the standard meet/join on equivalence relations.
- Davey, B. A. and Priestley, H. A. *Introduction to Lattices and Order*. 2nd edition, Cambridge University Press, 2002. Chapter 7 for Galois connections and the antitone/covariant duality used informally in the closing sections.
- Nightingale, Florence. *Notes on Matters Affecting the Health, Efficiency, and Hospital Administration of the British Army*. Harrison and Sons, London, 1858. The coxcomb appears at pp. 26–28; the surviving intervention dates at pp. 30–31; the correspondence on clerical practice in the second winter is the documentary basis for the obstruction discussed above.
