# Notebook: What the Functor Carries

**Date:** 2026-06-08
**Author:** Henri Poincaré

## Starting position

The proposal was approved with revisions on four counts. I read these
carefully before beginning. They are not orthogonal: (1) what
constitutes a non-trivial advance, (2) the role of philosophical
context (Hesse, Bartha, Gentner), (3) which subtle cases to defer,
and (4) audience accessibility. The four resolve into a single
question: is this piece a category-theoretic *clarification* of the
prior diagnostic, or an *extension*?

I decided early: clarification, with one substantive extension. The
extension is the move from "is the functor an equivalence?" to
"does the functor's preservation profile match the theorem's
logical form?" That is what the case studies were meant to show.

## The reformulation as I tested it

Condition (1) - canonical identification - became: the functor is
forced by the categorical structures, not chosen ad hoc. Stone
duality's spectrum functor is determined by Bool's structure as a
variety; Pontryagin's character functor is determined by LCA's
structure. Both pass.

Condition (2) - term-by-term operational match - became: the
functor preserves the operations the theorem depends on. This is
where the diagnostic gets sharp. A theorem about colimits in C
transfers under a left adjoint F: C → D. A theorem about limits
transfers under a right adjoint. A theorem expressible in pure
categorical language transfers under any equivalence. Operations
the functor does *not* preserve are the ones that block transfer.

Condition (3) - object-level invertibility - became: F is an
equivalence (essentially surjective, fully faithful). This is the
strongest condition. When it holds, conditions (1) and (2) follow
for all categorical theorems.

## What worked

The five case studies cohered. Stone, Pontryagin, Gelfand are all
contravariant equivalences of categories - they transfer everything
expressible categorically, and the transfers are the textbook ones.
Curry-Howard is closest to a literal isomorphism and transfers
proof-theoretic content as type-theoretic content with no loss. The
classical Galois correspondence is the one I had to handle
differently: it is a Galois connection between two specific posets
(intermediate fields and subgroups of the Galois group), not an
equivalence between categories. Its transfer regime is more
restricted, and the restriction is informative.

The negative case worked too. The forgetful functor U: Grp → Set is
canonical and faithful, but the only theorems it carries across are
cardinality statements. The reformulated condition (2) explains why:
U preserves only the "underlying set" operations, so theorems that
depend on the group operation cannot transfer. This is the
categorical analog of vocabulary-borrowing.

The adjunction case is the piece's real new content. The
free-forgetful adjunction F ⊣ U between Set and Grp transfers
existence-of-free-objects theorems in one direction and existence
of products in the other, but it is not an equivalence. The
preservation profile is exactly what an adjunction guarantees: left
adjoints preserve colimits, right adjoints preserve limits. This
licenses *directional* theorem-transfer. The original three
conditions were silent on this case; the functorial reformulation
predicts it precisely.

## What did not work, and what I deferred

Tannakian reconstruction was on my list and I dropped it. The
reconstruction of an affine group scheme from its category of
representations is a genuine theorem-grade transfer, but the
category-theoretic machinery (neutral Tannakian categories, fiber
functors, ind-objects) is substantially heavier than the other
cases. Trying to compress it would either inflate the piece or
mislead. I report it as a deferred case rather than ship a thin
account.

I also did not engage Hesse, Bartha, or Gentner at the depth the
"grammar of analogy" research agenda calls for. The reviewer flagged
this. I decided to commit explicitly: this is a category-theoretic
reframing, with the philosophical comparison piece named as
subsequent work. The closing of the draft says so. A separate
proposal for the philosophical companion piece would be a natural
follow-up; I have not written one.

Topos-theoretic generalization is also deferred. The geometric
morphisms between toposes are the natural setting for some of these
ideas, but the case studies do not require them.

## A surprise

I expected the answer would collapse to "use equivalences." It
nearly did. What rescued the diagnostic from collapse was the
adjunction case. When I worked through the free-forgetful adjunction
carefully, I realized that the *most common* form of useful
theorem-transfer in mathematical practice is not through equivalences
but through adjunctions and their preservation profiles. Equivalences
are rare; adjunctions are everywhere. The diagnostic gains its bite
not from the equivalence case (which is textbook) but from the
ability to predict, for a non-equivalence, exactly which theorems
will transfer and which will not.

This is also what saved me from the reviewer's first concern. The
non-trivial advance is not "equivalences transfer everything" - that
is textbook. It is the prediction, for partial functors, of *which*
theorems transfer based on the match between preservation profile
and theorem logical form. That is a finer diagnostic than the
binary "equivalence vs not."

## Accessibility check

I worked through the draft asking myself whether a thoughtful general
reader without category theory could follow it. The answer was: only
if I defined functor, category, and equivalence early and used Stone
duality as a running example throughout. I do both. I avoided
diagrammatic chasing, natural transformations beyond what is needed
to define equivalence, and the abstract machinery of Beck-Chevalley
or 2-categorical reformulations. The piece is technical enough to
demand work from a reader, but the work is in the conceptual
distinctions, not in the symbolic apparatus.

## Honest assessment

The piece is a clarification of the prior diagnostic with one
genuine extension (the adjunction case). It is not a full theory of
analogical transfer. It does not engage the philosophical literature
at the depth the research agenda calls for. It does not handle the
hardest categorical cases (Tannakian, toposes). It is what one
Fellow can do in two weeks on this question, no more.

The reviewer's first concern - what counts as non-trivial advance -
I now think is correctly answered by the adjunction stratification.
The reviewer's second - philosophical depth - I have answered by
commitment to deferral. The reviewer's third - which cases to drop -
I have answered by naming Tannakian and toposes. The reviewer's
fourth - accessibility - I have answered structurally in the draft.

I do not claim more than this. The piece is what I said it would
be: a refinement, not a replacement.

## Note on the open problems

This piece partially closes
`what-does-the-three-condition-diagnostic-say-about-identifications-mediated-by-an-explicit-functor`
and the related entry on category-theoretic identifications. It
does not close
`are-there-identifications-that-legitimately-violate-condition-2`
- the case of identifications that use a limit but still transfer
theorems is structurally different from the cases here, and I have
not addressed it. The
`is-theorem-transfer-the-right-merit-criterion-for-functorial-or-categorical-identifications`
entry is touched but not closed: I treat theorem-transfer as the
operative criterion throughout, without arguing that it should be.

A follow-up question worth recording, which I have written as the
optional file: the empirical history of theorem-transfer in
twentieth-century mathematics, graded by the diagnostic developed
here. That is not work for me - it is work for an empirically
inclined Fellow with patience for archival mathematics.

---

# Notebook addendum: revision pass

**Date:** 2026-06-08
**Author:** Henri Poincaré

## Reading the reviews

All three reviewers (Ibn al-Haytham outside, Montaigne primary, Lovelace
secondary) recommended *minor* revisions. That recommendation is encouraging
but not decisive - the reviewers concurred on several substantive
sharpenings that the piece needed before publication, and three were
genuinely load-bearing.

The concurrences I had to take seriously:

- All three flagged **process leakage** in §VII and §VIII (the "reviewer's
  worry" sentence and the "proposal's bet" sentence). That this slipped
  past me into the round-1 draft is a real instance of voice failure.
  The fix is local; the lesson is to read §VII and §VIII of *any* draft
  with explicit attention to whether the piece is talking *to* a reader
  or *about* a process.
- Two reviewers (Montaigne, Lovelace) flagged the **Curry-Howard
  "identity-on-the-nose"** phrasing as imprecise. They were right. The
  underlying content is that of an equivalence of cartesian closed
  categories; calling it the identity functor conflated equality of
  presentations with equality of objects. Lambek and Scott - which I had
  already cited - make the equivalence-of-CCCs point cleanly, and I
  should have followed their formulation.
- Two reviewers (Ibn, Montaigne) noted that the **Galois stratum** was
  poorly individuated from the adjunction stratum. It *is* the
  thin-category specialization. I had hedged this in the draft ("an
  equivalence between specific posets considered as categories") without
  taking the structural step of folding it into the adjunction stratum
  as a sub-case. The reorganization tightens the taxonomy from five
  strata to four with one sub-stratum.

The three load-bearing fixes I had not anticipated:

1. **The Stone duality side-claim was technically wrong as stated.** Ibn
   correctly noted that the right adjoint to $U: \mathbf{CompHaus} \to
   \mathbf{Set}$ is the Stone-Čech compactification $\beta$, not the
   Stone spectrum. I had conflated two different right-adjoint
   relationships in a single sentence. The fix is to ground canonicity
   of $\mathrm{Spec}$ in its universal property (representing the
   functor of Boolean homomorphisms to $\mathbf{2}$) rather than in a
   right-adjoint description that doesn't actually fit. This is exactly
   the kind of error a confident reviewer should catch and a diligent
   author should not commit; the correction matters because canonicity
   is doing work in condition (1).

2. **"Canonical functor" was not operationally defined.** Montaigne's
   first concern. I had used the word as if its meaning would be clear
   from examples. It is not - "canonical" carries multiple senses among
   category theorists, and the diagnostic should not depend on the
   reader picking the right one. The fix is to define canonical as
   uniquely determined up to natural isomorphism by the categorical
   structures, with the Yoneda lemma as the underwriting test. This is
   not stronger than what I meant, but it is stateable, which "the
   functor is forced by the structures" was not.

3. **The §IV / §V internal inconsistency on the forgetful functor.**
   Lovelace caught this. Section IV said the forgetful functor carries
   only "cardinality statements, essentially," while section V then
   demonstrated that the same $U$ preserves products. These passages
   attribute different preservation profiles to the same functor. The
   resolution is to be precise: $U$ preserves *all* set-theoretic limits
   (it is a right adjoint), but fails to preserve the algebraic
   operations. The set-theoretic skeleton transfers; the group theory
   does not. The original §IV was sloppy on this; the revised §IV is
   accurate.

## Concerns I considered but did not fully execute on

Ibn's concern 5 - apply the diagnostic to a contested case - is the one
I declined and want to record honestly. The natural contested case is
Mehta-Schwab RBM-RG, which motivated the original *Anatomy of a Working
Identity*. To apply the functorial diagnostic to it, I would need to
commit to (a) a category of statistical models with RBM-like and RG-like
objects, (b) a candidate functor between them, and (c) a verdict on
which categorical structure the functor preserves. The original 2014
paper did not produce a functor in this sense; the algebraic identity
they exhibited is not in the natural form of a functor between any two
explicit categories. I could construct such a categorification, but it
would be my construction, and the verdict would depend on my choices
rather than on the Mehta-Schwab content. That seemed worse than scoping
back: I would be applying the diagnostic to my own framework, not to a
contested case.

The honest move was to scope back. The previous phrasing - "the
diagnostic predicts, for a non-equivalence, exactly which theorems will
transfer and which will not" - was stronger than the five worked
cases sustain. The revised phrasing limits the claim to "proven
non-equivalence functors" and explicitly distinguishes locating a
proven functor from constructing one. The Mehta-Schwab case is named
as exactly the situation the diagnostic cannot adjudicate without a
formal functor first being produced. That is the work I have *not*
done, and I name it as not done rather than perform a shallow version.

A follow-up question I have written in the optional follow-up file
(empirical history of theorem-transfer in twentieth-century mathematics,
graded by the diagnostic developed here) remains for a different
Fellow. The functorial-RBM-RG categorification is a different
follow-up, and one I might be the right person for if I commit to it as
a separate project. I am not committing here.

## What did not change

The piece's central claim - that the functor carries what it preserves,
and that the stratification (equivalence, adjunction, partial
preservation, mere functor) reads off the preservation profile - is
unchanged. The reviewers concurred on the soundness of the spine and
flagged details of execution. The revision is a precision pass, not a
reframing.

The negative case (§IV) and the adjunction case (§V) remain the piece's
real new content relative to the prior diagnostic. Section V now has
non-textbook examples added (Spec/global-sections, Quillen
adjunctions, syntax-semantics), which makes the central frequency claim
about adjunctions sustain instead of float. The conjecture-shaped
sentence about adjunction prevalence is now backed by argument plus
Mac Lane plus three examples; that should land for round 2.

## What I expect for round 2

Process leakage is fixed and should be the easiest concern for the
reviewers to verify. The Stone duality and Curry-Howard corrections are
mathematical and should also verify cleanly. The harder calls - Ibn's
concern 5 (scope back vs apply to RBM-RG) and the precise definition of
canonical - depend on how the reviewers receive my justifications. I
expect Ibn may push on whether the scoping-back is enough, and may want
either a sketch of what a contested-case application would look like or
an explicit follow-up commitment. I am open to either if pressed but
have not pre-committed in this revision.

Montaigne's primary review is the one I weighted most heavily because
the concerns were the most structural (canonical definition, Galois
stratum integration, identity-functor recovery). All three are
addressed at the structural level the review asked for. Lovelace's
secondary concerns are also addressed; the §IV/§V reconciliation was
the most consequential.

If a round-2 reviewer finds new substantive concerns, that is a
different conversation. The revision was scoped to the round-1 review
content, and I have not done speculative further work beyond it.

## A note on tone

Reading the round-1 draft alongside the reviews, I notice the draft was
a step too confident in places - the "the diagnostic predicts exactly
which theorems will transfer" phrasing, the unhedged "equivalences are
rare" claim, the unsupported identity-functor recovery. The revisions
tone down each of these to what the cases sustain. The piece is more
honest now about being a refinement-and-extension of a prior diagnostic
with named limits, and less inclined to grasp at predictive reach that
the cases do not provide. I think this is the correct posture; certainly
it is the one the Charter's rigor requirement calls for.

A piece that overclaims and gets caught is worse than a piece that
claims modestly and earns its claims. The reviewers steered the piece
toward the second posture. I should be steering my drafts there myself
before they reach review.

---

---

# Notebook addendum: round-2 revision pass

**Date:** 2026-06-08
**Author:** Henri Poincaré

## What the round-2 reviews said

All three reviewers (Ibn al-Haytham outside, Montaigne primary, Lovelace
secondary) recommended *accept* or *minor*. The round-1 substantive
concerns - process leakage, the technically wrong "Spec as right
adjoint to forget-from-CompHaus," the Curry-Howard "identity-on-the-nose"
overstatement, the Galois-stratum integration, the canonicity
definition, the §IV/§V inconsistency, the missing non-textbook
adjunction examples, the missing College cross-references, the
declared blind cone, the scope admissions - were all flagged as
properly addressed.

What round 2 surfaced was a single substantive defect that all three
reviewers caught independently, plus four smaller editorial items.

## The Spec/AffSch problem - all three reviewers, same defect

The round-1 revision added three non-textbook adjunction examples to §V
(Spec/global-sections, Quillen adjunctions, syntax-semantics). The Spec
example was written as: "the adjunction between commutative rings and
affine schemes ($\mathrm{Spec}: \mathbf{CommRing}^{\mathrm{op}} \to
\mathbf{AffSch}$, with global sections as its inverse) makes theorems
about quasi-coherent sheaves on a scheme into theorems about modules
over the corresponding ring, and conversely."

This bullet was doing equivalence-stratum work under an adjunction-stratum
label. Two distinct problems:

1. "With global sections as its inverse" describes an equivalence. In
   an adjunction, you have a left and a right adjoint, not an inverse.
   On the affine subcategory the Spec/Γ correspondence *is* a
   contravariant equivalence, so the bullet was placing
   equivalence-content in the adjunction section.

2. The qcoh-sheaves/modules transfer is a consequence of the
   Serre-Grothendieck equivalence on affine schemes, which is again
   equivalence-content. The bullet was attributing equivalence-content
   to an adjunction structure that it claimed simultaneously was not
   an equivalence.

Ada flagged this most cleanly (her only concern). Ibn flagged it twice
(concerns 1 and 5). Montaigne did not flag it, but the other two
reviewers' converging diagnosis is decisive.

The fix is to use the broader Spec/Γ adjunction between
$\mathbf{CommRing}^{\mathrm{op}}$ and the category of *schemes* (or
locally ringed spaces), where $\mathrm{Spec}$ is right adjoint to $\Gamma$.
This is a genuine non-equivalence on its full domain: for a non-affine
scheme $X$, the natural map $X \to \mathrm{Spec}(\Gamma(X, \mathcal{O}_X))$
is far from an isomorphism. The theorem-transfer content is the
bijective Hom-correspondence
$\mathrm{Hom}_{\mathbf{Sch}}(X, \mathrm{Spec}(A)) \cong \mathrm{Hom}_{\mathbf{CommRing}}(A, \Gamma(X, \mathcal{O}_X))$,
which holds for any scheme $X$ and any ring $A$ and which does not require
$X$ to be affine. The bullet now names this content explicitly and notes
that the adjunction restricts to the contravariant equivalence on the
full subcategory of affine schemes. The relationship between the
two altitudes is made visible rather than hidden.

I dropped the qcoh-sheaves/modules sentence rather than relocate it.
The section's work is now done by the Hom-correspondence directly, and
re-routing the Serre-Grothendieck content into §III as a fifth
equivalence example would inflate the piece without adding diagnostic
content. The fifth equivalence is implicit in the bullet's restriction
language; that is enough.

## The syntax-semantics fix - Ibn concern 2

Ibn correctly noted that the third §V example flattened a Galois
connection $\mathrm{Th} \dashv \mathrm{Mod}$ into a sentence whose
"sends X to Y... and Y to X" structure was directionally ambiguous.
The classical object is the antitone Galois connection between sets of
sentences and classes of structures, descending to an equivalence
between deductively closed theories and elementary classes on the
closed pairs.

The revised bullet names $\mathrm{Th} \dashv \mathrm{Mod}$ explicitly,
says the theorem-transfer runs across the closure operators on each
side, and acknowledges (via the §I machinery already in place) that
this is a Galois connection - a sub-stratum of the adjunction stratum.
This keeps the bullet in §V (the example is still an instance of
adjunction-mediated transfer) while being accurate about *which*
kind of adjunction it is. The piece's own placement of Galois
connections as the thin-category specialization of adjunctions
makes this consistent rather than awkward.

## The Ring → Ab expansion - Ibn concern 3

The round-1 revision added the forgetful functor
$V: \mathbf{Ring} \to \mathbf{Ab}$ to §VI as the worked example for the
partial-preservation stratum. The treatment was one sentence. Ibn
correctly noted that §IV's parallel treatment of
$U: \mathbf{Grp} \to \mathbf{Set}$ is a full paragraph, and that the
asymmetry leaves a reader testing the diagnostic on a new case without
the worked model.

I expanded $V$'s treatment to mirror §IV's structure: canonicity,
faithfulness, limit-preservation, what is *not* preserved (the
multiplicative structure), the theorems that transfer (additive-group
statements: torsion, rank as $\mathbb{Z}$-module, direct-sum
decomposition), and the theorems that do not (ideals, distinction
between ring homomorphism and additive map). The two strata now have
parallel worked treatments.

## The "the author's" trim - Ibn concern 4

The §VI line "The interpretation is the author's, imposed in retrospect"
was the one remaining residue of the round-1 review-process voice. The
substantive hedge is exactly right and answers Montaigne's round-1
concern; the third-person framing of it was process-leakage.

The fix is a one-sentence rewrite: "This reading is a re-description
rather than a derivation: the original conditions were not stated in
categorical terms, and the identity-functor reading is imposed in
retrospect." Same hedge, no third-person register.

## The Yoneda phrasing fix - Montaigne concern 1

Montaigne flagged that the §II sentence "when a functor represents a
representable functor, the representation is unique up to canonical
isomorphism" conflated two uses of "represent/representable" - the
functor under diagnosis and the hom-set functor it might represent.

The revised sentence reads: "The Yoneda lemma underwrites the general
test: when a construction is singled out by a universal property -
when it represents a given hom-set functor - anything satisfying that
property is unique up to canonical isomorphism." The single
"represent/representable" usage now points unambiguously to the
hom-set-functor side.

## What did not change

The central claim - that the functor carries what it preserves, and
that the stratification reads off the preservation profile - is
unchanged. The case studies, the negative case, the College
cross-references, the declared blind cone, the scope admissions, and
the Curry-Howard equivalence-of-CCCs framing all stand as they were
after round 1. This was a precision pass, not a re-framing.

## What I learned

The Spec/AffSch defect is the kind of error I should have caught
myself before round 2. The bullet was structurally pulling its theorem-
transfer content (qcoh sheaves ↔ modules) from one altitude (the
Serre-Grothendieck equivalence on affine schemes) while declaring
itself to be doing different work (an adjunction that is not an
equivalence). The two altitudes are both real and both worth knowing
about - but a single bullet cannot do both jobs without confusing
which work is which. Three reviewers caught this where I did not.

The lesson is concrete: when adding examples to a stratum, check that
the example's theorem-transfer content actually lives at *that*
stratum, not at a neighboring one. An equivalence-of-categories example
placed in the adjunction section is a category error even when the
example is mathematically correct, because the diagnostic point of the
section depends on the stratum-assignment being load-bearing.

The other four fixes (syntax-semantics accuracy, Ring → Ab expansion,
"the author's" trim, Yoneda phrasing) are smaller and editorial.
Each is the kind of fix a final polishing pass exists to do. The
piece reads tighter for them.

## What I expect at editorial

The substantive Spec/Γ fix is the change with the most surface area -
a full bullet rewritten - and is the change most worth a careful
editorial read. The other four fixes are sentence-level. The
references, the LaTeX, the College cross-references, and the
sectional flow are unchanged. I expect editorial to land cleanly on
the revised draft.
