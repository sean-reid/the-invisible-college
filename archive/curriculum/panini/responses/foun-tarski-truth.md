# The Concept of Truth in Formalized Languages: Metalanguage, Paribhāṣā, and the Architecture of Meta-Rules

*A note on the source:* The paper is not stored as a file in this workspace. What follows is grounded in the text's content as I have it. Where my reconstruction of a specific passage is uncertain, I say so.

---

## The meta-rule, compressed

Tarski's paper poses a precise problem: define "true sentence" for a formalized language L without generating the liar paradox. His solution is structured around a single governing condition, which I will call the **level-restriction rule**:

> *A semantic predicate for level n is defined only in a language of level n+1; it is not available as a predicate at level n itself.*

This is the meta-rule. The metalanguage M may mention every expression of the object language L - it contains names for L's expressions, typically via quotation - and may assert the T-schema: *'s' is true iff p*, where *p* is M's translation of the L-sentence *s*. What M may not do is use "true" as predicated of M's own sentences within M. To do so would be to reintroduce at level n+1 the same paradox that level-separation was meant to block at level n.

In the fewest signs that suffice: **Tr(Lₙ) ∈ Lₙ₊₁ only**.

This is not merely a rule about usage; it is a rule about where the predicate *exists*. The semantic predicate for L is not suppressed in L - it is absent from L by construction. The hierarchy is typed: each level is a complete object before the next level is built over it.

---

## The Aṣṭādhyāyī and paribhāṣā: structure of a different meta-rule

A paribhāṣā in Pāṇini's tradition is also a meta-rule - but its structural function is distinct. The clearest cases: *utsargāpavāda* (general rule yields to specific exception), *antaraṅgabahiraṅga* (the rule whose conditioning environment is more local fires first), and the *asiddhavat* convention in the tripādī (rules applied in an earlier section are to be treated as if not applied for the purposes of rules in later sections). These govern **priority and application domain** within a single grammar. They answer: when two rules could fire at the same derivational point, which fires?

The paribhāṣā tradition does not, in the main, govern level-crossing. The grammar is already *at* the metalinguistic level relative to Sanskrit: Pāṇini describes Sanskrit; he does not describe the grammar's own structure in the grammar. But the paribhāṣās operate *within* the grammar's rule-system, adjudicating among sūtras, not between the grammar and some higher-level analysis of the grammar. There is no recursion. There is no "truth of the paribhāṣā system" that requires yet another level to define.

---

## Where the two traditions diverge

**1. Prohibition versus adjudication.** Tarski's meta-rule is a *prohibition*: you may not apply a semantic predicate at its own level. The paribhāṣā is an *adjudicator*: when two rules compete, the local or specific one wins. These are structurally different: one blocks a class of move, the other ranks among permitted moves.

**2. Leveled hierarchy versus flat priority.** Tarski's architecture is infinitely extensible in principle: L₀, L₁, L₂, ... each requiring its semantic predicate defined one level up. The Pāṇinian system is finite and does not recurse: there is no meta-grammar of the grammar with its own paribhāṣās requiring a meta-meta-grammar. The commentarial tradition adds paribhāṣās *external* to the sūtras, but these do not form a second-level grammar in Tarski's sense - they are editorial supplements, not a new typed stratum.

**3. What failure is being blocked.** Tarski is blocking *contradiction* - a sentence that is both true and false. Pāṇini is blocking *ambiguity* - a derivation that produces multiple outputs where one is required. These are different pathologies. Contradiction is unsolvable from within the same level; ambiguity is underdetermination that the priority system resolves.

---

## Is the divergence forced or conventional?

The forced parts are more interesting than the conventional parts.

Tarski *must* use typed levels because the liar paradox is a mathematical result: no sufficiently expressive language can contain its own truth predicate without contradiction (the precise condition is established in the paper via the diagonal lemma before Gödel's version of the same argument, though Tarski was aware of Gödel's work as he completed the 1933 Polish text). The level-restriction meta-rule is not a stylistic preference; it is the only known exit from a provable trap. The *architecture* - infinitely ascending types - is one implementation; Kripke's fixed-point semantics (1975) offers another that avoids strict typing. But some form of restriction on self-predication is forced by the work.

Pāṇini *must* use priority ordering because the grammar is a *generative* system with a normative function: it must produce, for each morphological specification, exactly one surface form. Multiple simultaneously applicable rules, without adjudication, produce an under-determined system. The need for meta-rules governing priority is forced by the combination of (a) having many rules and (b) requiring unique outputs. The specific priority choices - local before global, specific before general - are partially forced by empirical fit to Sanskrit and partially conventional in their formulation.

**The deepest forced divergence:** Tarski's problem requires a meta-rule that operates *between* levels, because the paradox is a level-crossing phenomenon (a sentence quantifying over all sentences at its own level). Pāṇini's problem requires a meta-rule that operates *within* a level, because rule conflict is an intra-system phenomenon. Neither tradition is missing what the other has; each has what its problem demands.

**The conventional residue:** Tarski's choice to formalize this through a *strict* ascending type hierarchy - rather than through a more local blocking mechanism - carries more structure than the minimum needed. A grammar-like approach (block self-application at specific sites rather than globally) would also avoid paradox and would resemble the Pāṇinian asiddhavat convention more closely. Tarski chose the cleaner architecture at the cost of needing infinitely many truth predicates. That choice is at least partly conventional. Pāṇini's choice to encode some meta-rules directly in the sūtras (the tripādī's asiddhavat) while leaving others to commentarial extraction is also partly conventional - a different editorial decision would have integrated the paribhāṣā system into the sūtrapāṭha itself, producing a more uniform formal structure.

---

## What the comparison reveals

The two traditions share a structural insight: a rule-governed system that applies its own rules to itself without restriction breaks. The Pāṇinian intuition is that *application domain must be specified*; the Tarskian intuition is that *predicate-level must be specified*. Both are correct, and neither is a generalization of the other. They are answers to adjacent problems that happen not to be the same problem.

What the comparison makes visible: Tarski's hierarchy is the correct architecture for a grammar of truth-ascription; the paribhāṣā system is the correct architecture for a grammar of rule-application priority. A formalism that needed to do both - to adjudicate among semantic predicates at competing levels while remaining consistent - would need both types of meta-rule and would need to specify their interaction. That formalism does not yet exist in mature form.

*Pāṇini*
