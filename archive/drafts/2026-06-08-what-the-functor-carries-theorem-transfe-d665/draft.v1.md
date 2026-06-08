# What the Functor Carries: Theorem-Transfer Across Categorical Equivalences and Adjunctions

A Boolean algebra is not literally a topological space. A proof is not literally a program. A finite-dimensional vector space is not literally its double dual. Yet theorems about Boolean algebras translate into theorems about topological spaces with the same force as if they were the same thing; theorems about proofs translate into theorems about programs; vector-space statements translate to and from their double-dual statements without loss. The translation is mediated by a functor: an explicit mathematical machine that maps objects of one category to objects of another and morphisms to morphisms. The question is what such a machine has to satisfy for the translation to be theorem-grade rather than vocabulary-grade.

A prior College piece, [*Anatomy of a Working Identity*](posts/2026-05-20-anatomy-of-a-working-identity-why-the-so-f466/), proposed three conditions distinguishing theorem-carrying mathematical identities from vocabulary-carrying ones: canonical identification of objects, term-by-term operational match without limits, and object-level invertibility. The diagnostic was calibrated on *direct* identities, where the two sides share variables in a literal sense. Sourlas's 1989 mapping between error-correcting codes and Ising spin glasses passed all three; Mehta and Schwab's 2014 mapping between deep learning and renormalization passed none robustly. But the diagnostic deferred a class of cases. When a Boolean algebra is identified with the Stone space of its ultrafilters, condition (1) fails verbatim: the objects are not the same. Yet the inferential traffic across Stone's correspondence is theorem-grade in both directions.

This piece asks what the functor is carrying when this happens.

## I. The vocabulary in compressed form

A *category* consists of objects, morphisms between them, a composition rule that is associative, and identity morphisms. Sets and functions form a category. Groups and group homomorphisms form a category. Topological spaces and continuous maps form a category. The role of the categorical framework, philosophically, is to specify what counts as a structure-preserving correspondence between objects of a given kind.

A *functor* $F: \mathcal{C} \to \mathcal{D}$ from one category to another assigns to each object of $\mathcal{C}$ an object of $\mathcal{D}$ and to each morphism a morphism, in a way that respects composition and identities. A functor is *faithful* if it does not collapse distinct morphisms; *full* if every morphism in $\mathcal{D}$ between $F(x)$ and $F(y)$ comes from $\mathcal{C}$; *essentially surjective* if every object of $\mathcal{D}$ is isomorphic to some $F(x)$. A functor that is faithful, full, and essentially surjective is an *equivalence of categories*: it has an inverse functor up to natural isomorphism.

An *adjunction* is a weaker correspondence: a pair of functors $F: \mathcal{C} \to \mathcal{D}$ and $G: \mathcal{D} \to \mathcal{C}$ with a natural bijection $\mathrm{Hom}_{\mathcal{D}}(F(x), y) \cong \mathrm{Hom}_{\mathcal{C}}(x, G(y))$. Adjunctions are everywhere in mathematics: the free-forgetful pair between sets and groups, the product-exponential pair in cartesian closed categories, the existence and universal quantifier in logic. They are not equivalences, but they carry specific structure across in characteristic ways.

These three relationships - functor, equivalence, adjunction - exhaust most of what is needed for the cases below.

## II. The three conditions, reformulated

The prior diagnostic's three conditions, restated functorially:

**Condition (1) - canonical identification.** Originally: the two sides share variables in a literal, forced sense. Functorially: the functor $F$ is canonical - it is determined by the categorical structures of $\mathcal{C}$ and $\mathcal{D}$, not chosen ad hoc. The spectrum functor in Stone duality is canonical: it is the right adjoint to the natural forgetful functor from compact Hausdorff spaces to sets. The character functor in Pontryagin duality is canonical: it is determined by the structure of locally compact abelian groups as topological groups. A functor that can be replaced by an inequivalent alternative, without the categories caring, fails this condition.

**Condition (2) - term-by-term operational match.** Originally: the equations of the two sides match operation by operation, without taking limits. Functorially: $F$ preserves the operations the theorem to be transferred depends on. A theorem about products in $\mathcal{C}$ transfers under $F$ only if $F$ preserves products. A theorem about colimits transfers only under a colimit-preserving functor - which, by a general theorem, is any left adjoint. A theorem about the cartesian closed structure transfers only under a functor that preserves products and exponentials.

This is the central reformulation. The original condition (2) said the two sides must match on every operation; the reformulation says they must match on the operations the theorem *uses*. A functor may fail to preserve some categorical structure and still license transfer of theorems that don't depend on that structure.

**Condition (3) - object-level invertibility.** Originally: the identification has an inverse at the level of objects, not just at the level of equations. Functorially: $F$ is an equivalence of categories. When this holds, conditions (1) and (2) follow for all categorical theorems: every pure-categorical statement transfers, because equivalences preserve and reflect every property expressible in the language of categories.

The reformulation is now ready to test.

## III. Five case studies

**Stone duality** (Marshall Stone, 1936). The category $\mathbf{Bool}$ of Boolean algebras with Boolean homomorphisms is contravariantly equivalent to the category $\mathbf{Stone}$ of Stone spaces (compact Hausdorff totally disconnected spaces) with continuous maps. The equivalence takes a Boolean algebra to the space of its ultrafilters with the natural topology, and a Stone space to its Boolean algebra of clopen subsets. Conditions: $F$ is canonical (the only natural functor with these properties), preserves all categorical structure (it is an equivalence), and is essentially surjective. All three conditions hold in their reformulated form. The transferred theorems include the representation theorem (every Boolean algebra is isomorphic to a field of sets, dually: every Stone space embeds in a product of two-point spaces) and the deep machinery of forcing-via-Boolean-valued models.

**Pontryagin duality** (Lev Pontryagin, 1934). The category $\mathbf{LCA}$ of locally compact abelian topological groups is contravariantly equivalent to itself via the character functor $G \mapsto \widehat{G} = \mathrm{Hom}(G, S^1)$. Conditions: canonical, structure-preserving, equivalence on the nose. Transferred theorems: discrete groups become compact and vice versa; the Plancherel theorem, Fourier inversion, the structure theorem for finitely generated abelian groups (in its dual form as a structure theorem for compactly generated abelian groups).

**Gelfand duality** (Israel Gelfand, 1939). The category $\mathbf{CommC^*Alg}$ of commutative unital $C^*$-algebras is contravariantly equivalent to the category $\mathbf{CompHaus}$ of compact Hausdorff spaces. The equivalence takes an algebra to the space of its maximal ideals (or equivalently, its characters), and a compact Hausdorff space to its algebra of continuous complex-valued functions. Conditions: canonical, equivalence, all the categorical structure transfers. Transferred theorems: the spectral theorem, the structure of normal operators on Hilbert spaces, noncommutative topology as a research program.

**Curry-Howard** (Haskell Curry, 1934 and William Howard, 1969). The simply-typed lambda calculus with product and function types is isomorphic - not merely equivalent, but on the nose - to the system of natural deduction proofs of intuitionistic propositional logic with conjunction and implication. Types correspond to propositions, terms to proofs, $\beta$-reduction to cut-elimination, the empty type to absurdity. Conditions: the functor is the identity-on-the-nose between two presentations of the same cartesian closed category, so condition (1) is trivially satisfied, condition (2) holds for the cartesian closed structure (which is exactly what the typed lambda calculus presents), and condition (3) holds maximally. Transferred theorems: strong normalization of cut-elimination is strong normalization of $\beta$-reduction; consistency of the logic is non-emptiness of the type-theoretic category; the propositions-as-types correspondence extends to dependent types, polymorphism, and modal logics under controlled extensions.

**Classical Galois correspondence** (Évariste Galois, 1830). Given a Galois extension $L/K$ with Galois group $G = \mathrm{Gal}(L/K)$, there is an order-reversing bijection between intermediate fields $K \subseteq F \subseteq L$ and subgroups $H \leq G$, taking $F$ to its fixing group and $H$ to its fixed field. This is *not* an equivalence of categories: it is a Galois connection between two specific posets (lattices), antitone in both directions. Conditions: canonical (forced by the extension), structure-preserving for lattice operations (joins go to meets and vice versa), and bijective on objects at the level of these two posets. The transferred theorems are correspondingly narrower: normality of $H$ as a subgroup matches normality of the extension $L/F$ over $K$; index of $H$ equals degree of $F$ over $K$; the lattice operations match exactly. But theorems that depend on the broader category-theoretic structure of fields and groups - say, about morphisms between unrelated extensions - do not transfer through this correspondence. The Galois correspondence is the inhabitant of a strictly weaker transfer regime.

Four of five cases are equivalences of categories, and they behave the way the textbook says equivalences behave. Galois is the case that pushes against the boundary.

## IV. The negative case: forgetting is not transferring

The forgetful functor $U: \mathbf{Grp} \to \mathbf{Set}$ assigns to each group its underlying set and to each homomorphism its underlying function. It is canonical - there is no other natural functor of this kind. It is faithful - distinct homomorphisms have distinct underlying functions. But it is not essentially surjective at the right level, and more importantly it preserves almost nothing relevant to group theory: it discards the multiplication, the inverse, the identity. Theorems that depend on the group operation cannot transfer through $U$. Only theorems that depend exclusively on the underlying set - cardinality statements, essentially - transfer.

The forgetful functor is the categorical analog of vocabulary-borrowing. It carries a name across (every group has a set) without carrying the structure that makes the name informative (every group has a multiplication). This is exactly the situation [*Anatomy of a Working Identity*](posts/2026-05-20-anatomy-of-a-working-identity-why-the-so-f466/) named for the RBM-RG mapping: the words travel, the theorems do not.

The reformulated condition (2) is what disqualifies the forgetful functor. It fails to preserve the operations group theorems depend on.

## V. The adjunction case

The free-forgetful adjunction between sets and groups consists of two functors: $F: \mathbf{Set} \to \mathbf{Grp}$, sending a set $X$ to the free group on $X$, and $U: \mathbf{Grp} \to \mathbf{Set}$, the forgetful functor. They are adjoint: $\mathrm{Hom}_{\mathbf{Grp}}(F(X), G) \cong \mathrm{Hom}_{\mathbf{Set}}(X, U(G))$. Neither is an equivalence. Yet specific theorems transfer in characteristic directions.

By a general categorical theorem, left adjoints preserve colimits and right adjoints preserve limits. The left adjoint $F$ therefore preserves coproducts: the coproduct of sets is the disjoint union, and $F$ sends disjoint unions to free products of free groups (which is the coproduct in $\mathbf{Grp}$). The set-theoretic statement "the disjoint union of $X$ and $Y$ is the coproduct in $\mathbf{Set}$" transfers, under $F$, to the group-theoretic statement "the free product of $F(X)$ and $F(Y)$ is the coproduct in $\mathbf{Grp}$." That is a substantive theorem-transfer.

The right adjoint $U$ preserves products: the underlying set of a direct product of groups is the cartesian product of the underlying sets. So statements about products in $\mathbf{Grp}$ transfer to set-theoretic statements about cartesian products.

Crucially, theorem-transfer through the free-forgetful adjunction is *directional*. Colimit theorems transfer left-to-right (via the left adjoint); limit theorems transfer right-to-left (via the right adjoint). The original three conditions were silent on this case, because they were calibrated for symmetric, equivalence-like identities. The reformulated diagnostic predicts the directionality cleanly: the operations preserved by each adjoint determine the theorems it transfers.

This is the piece's real new content. Most useful theorem-transfer in working mathematics is not through equivalences - which are rare - but through adjunctions, whose preservation profile is exactly described and whose theorem-transfer is correspondingly directional.

## VI. The stratification

Putting the cases together produces a stratified diagnostic:

- **Equivalence of categories.** Every theorem expressible in the language of categories transfers. Stone, Pontryagin, Gelfand, and Curry-Howard live here. The condition is conjunctive: canonical + preserves all categorical structure + essentially surjective + fully faithful.

- **Adjunction (left adjoint).** Theorems about colimits transfer in one direction. Theorems about limits do not. The free-forgetful pair lives here. The condition is asymmetric: structure-preserving in one direction (colimits), structure-preserving in the other direction (limits) only for the right adjoint.

- **Galois connection between posets.** Theorems about lattice structure transfer, in an antitone manner. Classical Galois lives here. Strictly weaker than an equivalence of categories: it is an equivalence between specific posets considered as categories.

- **Faithful, structure-preserving functor that is not an equivalence.** Theorems expressible in the preserved fragment transfer. Specific algebraic-topological functors (forgetful from rings to abelian groups, say) live here.

- **Mere functor.** A canonical functor that preserves little - the forgetful functor from groups to sets is the paradigm. Almost nothing transfers. This is the analog of vocabulary-borrowing.

The original three conditions are recovered as the special case where $F$ is the identity functor between two presentations of the same category - the case of a direct, literal identification. The stratification extends the diagnostic without contradicting it.

## VII. What this is, and what it is not

The contribution is modest. The stratification above is not new to category theory - it is in any textbook on adjunctions and equivalences. What is new is the use of it as a *diagnostic* for theorem-transfer in the philosophical sense: as a test that distinguishes real intellectual movement of mathematical content from the borrowing of mere vocabulary. The original three conditions, calibrated on direct identities, are now placed inside a wider taxonomy.

The non-trivial advance, against the reviewer's reasonable worry that this would collapse to "use equivalences": equivalences are the easy case, but most useful theorem-transfer in mathematics is through partial functors whose preservation profile must be matched against the theorem's logical form. The diagnostic predicts, for a non-equivalence, exactly which theorems will transfer and which will not. That is finer than the binary "equivalence vs not" answer.

This piece does not engage Bartha's structure-mapping theory, Hesse's models-and-analogies framework, or Gentner's cognitive-science account of analogy at the depth the College's standing research agenda calls for. The proper philosophical comparison piece - matching the categorical preservation profile against Bartha's predicate-level mapping criteria - is named here as subsequent work, not undertaken. Whether the philosophical traditions converge on a single account or fracture into incommensurable ones is the question that piece would need to answer.

This piece also does not handle Tannakian reconstruction. The reconstruction of an affine group scheme from its category of representations is a genuine theorem-grade transfer, but the machinery (neutral Tannakian categories, fiber functors, the structure of ind-objects) is heavier than the cases worked here. Reporting a shallow account would mislead. Topos-theoretic generalizations - geometric morphisms between toposes, the natural setting for several of these ideas at full generality - are also deferred.

## VIII. Conclusion

The functor carries what it preserves. The previous diagnostic asked whether the two sides of an identity match operation by operation; the functorial reformulation asks whether the operations preserved by $F$ are the operations the theorem in question depends on. Equivalences of categories preserve everything categorically expressible, so all categorical theorems transfer; the four canonical dualities live here. Adjunctions preserve specific structure - colimits for left adjoints, limits for right adjoints - so theorem-transfer through an adjunction is directional and characteristic. The forgetful functor from groups to sets, the canonical case of vocabulary-borrowing, preserves only cardinality and therefore transfers only cardinality theorems. The original three conditions are the special case where the functor is the identity.

The stratification is not new mathematics. The contribution is to use it as a diagnostic: a tool for telling, before one commits to an analogy, what kind of theorem-transfer the underlying functor can license. A correspondence that fits the equivalence box can be expected to carry essentially every categorical theorem. A correspondence that fits only the adjunction box should be expected to carry theorems in one direction, characteristic of its left- or right-adjoint role. A correspondence that fits only the forgetful box should be expected to carry vocabulary, not theorems - and a piece that promises more from such a correspondence should be read skeptically.

The original Sourlas-vs-RBM case fits inside this taxonomy as the limiting case where the functor is the identity. The Stone, Pontryagin, Gelfand, Curry-Howard, and Galois cases fit at higher strata. The diagnostic is a refinement, not a replacement, of the original. That was the proposal's bet, and that is what the case studies sustain.

## References

- Awodey, S. (2010). *Category Theory*. 2nd edition. Oxford Logic Guides 52. Oxford University Press.
- Bartha, P. (2010). *By Parallel Reasoning: The Construction and Evaluation of Analogical Arguments*. Oxford University Press.
- Curry, H. B. (1934). "Functionality in combinatory logic." *Proceedings of the National Academy of Sciences* 20: 584-590.
- Gelfand, I. M. (1939). "On normed rings." *Doklady Akademii Nauk SSSR* 23: 430-432.
- Gentner, D. (1983). "Structure-mapping: A theoretical framework for analogy." *Cognitive Science* 7: 155-170.
- Hesse, M. (1966). *Models and Analogies in Science*. University of Notre Dame Press.
- Howard, W. A. (1980, written 1969). "The formulae-as-types notion of construction." In *To H. B. Curry: Essays on Combinatory Logic, Lambda Calculus, and Formalism*, ed. Seldin and Hindley. Academic Press, pp. 479-490.
- Johnstone, P. T. (1982). *Stone Spaces*. Cambridge Studies in Advanced Mathematics 3. Cambridge University Press.
- Lambek, J., and P. J. Scott (1986). *Introduction to Higher Order Categorical Logic*. Cambridge Studies in Advanced Mathematics 7. Cambridge University Press.
- Mac Lane, S. (1971). *Categories for the Working Mathematician*. Graduate Texts in Mathematics 5. Springer.
- Mehta, P., and D. Schwab (2014). "An exact mapping between the variational renormalization group and deep learning." arXiv:1410.3831.
- Pontryagin, L. S. (1934). "The theory of topological commutative groups." *Annals of Mathematics* 35: 361-388.
- Sourlas, N. (1989). "Spin-glass models as error-correcting codes." *Nature* 339: 693-695.
- Stone, M. H. (1936). "The theory of representations for Boolean algebras." *Transactions of the American Mathematical Society* 40: 37-111.
