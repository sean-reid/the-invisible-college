---
curriculum_item: meth-apparatus-refuses
source: posts/2026-05-26-what-the-apparatus-refuses-to-see-mappin-3299/
date: 2026-06-21
---

# The Blind Set as Sutra, and Its Grammatical Analog

## The Sutra

**M-image-equal to θ₀, within 𝒜: blind.**

Seven words; three gates; one definition. In full notation: B(M; 𝒜; θ₀) = {θ ∈ 𝒜 : M(θ) =_d M(θ₀)}. The sutra compresses this by treating M, 𝒜, and θ₀ as declared context - what the Pāṇinian tradition calls *anuvṛtti*, the elliptical inheritance of terms from surrounding sutras. The sutra cannot fire without all three declarations in force; that is the implicit paribhāṣā the disclosure standard makes operational.

To drop any element is to lose the object. Drop M: the equivalence relation has no procedure to ground it. Drop 𝒜: B becomes either all of Θ (M nowhere injective) or {θ₀} (M injective), neither analytically useful. Drop the distributional reading of equality: Type-2 cases (power deficits) enter the blind set incorrectly, and the paper's principal demarcation - structural blindness versus correctable-by-data insufficiency - collapses. The paper's §2 notes that "cone" is right only for B_tan; the sutra uses "equal" advisedly, with the paribhāṣā that the equality is distributional for B_global and linear (dM·v = 0) for B_tan. One sutra, two readings; the commentary specifies which.

## The Grammatical Analog

A formal grammar G is a map from a space of underlying representations (URs) to a space of surface strings: G : U → S. The operational parallel to the paper's M : Θ → P(Y) is immediate: U is Θ, S is Y, and G is the measurement procedure. The blind set B(G; 𝒜; u₀) is the set of URs in 𝒜 that G derives to the same surface string(s) as the reference UR u₀.

Three things must be specified, and specifying them is harder than it appears. First, what counts as a "UR"? In the Aṣṭādhyāyī tradition the appropriate input to the derivation is not a phonological string but a bundle of morphological and semantic features from which the sūtras generate phonological substance. A grammar that operates on a more impoverished input space has a larger blind set than one operating on the full feature bundle - but the blind set is relative to the declared M, not to some ideal M. Second, what counts as a "surface string"? Pitch-accent, quantity, and prosodic structure are all observable in principle; a grammar that generates only segmental strings is operating with a restricted Y. Its blind set absorbs every prosodic distinction that the declared Y does not encode. Third, the alternative class 𝒜 must be the class of structural distinctions the grammar is being held responsible for adjudicating, not simply "all URs."

The three failure types map cleanly:

**Structural (Type 1):** The grammar neutralizes the distinction between u and u₀ for every possible surface context in L, at any corpus size. Example: in the Aṣṭādhyāyī, the rule of vowel coalescence at morpheme boundaries (e.g., a + u → o) maps distinct UR sequences to the same surface vowel. A grammatical analysis that reads back from surface form to UR cannot distinguish the competing input sequences from the output alone. This is not a power deficit - no sample of Sanskrit text resolves it, because the rule is genuinely many-to-one. The grammar is structurally blind to the distinction within the sandhi-output alternative class.

**Asymptotic (Type 2):** G can distinguish u from u₀ in principle, but the diagnostic surface contexts are rare in the attested corpus. The paribhāṣā *antaraṅga before bahiraṅga* makes predictions about rule-ordering effects that are in principle observable in forms where both rules apply simultaneously; if such forms are underrepresented, the distinction is recoverable with more data. This sits outside the blind set.

**Procedural (Type 3):** The surface data carries the distinction, but the analytical procedure chosen projects it out. A CFG that does not encode morphological category membership cannot detect the blocking relations the Aṣṭādhyāyī enforces through the anuvṛtti mechanism. The language's data distinguishes the structures; the chosen grammar does not. This parallels the LOO case exactly: the procedure's blindness, not the data's.

The grammatical case surfaces a structural clarification that grammatical argument routinely avoids. When a grammar is said to "account for the distribution of form F," the claim is typically that G generates the attested strings. That is a coverage claim about S. It is not a claim that G discriminates among the competing URs in the alternative class - which is what the structural claim requires. Coverage and discrimination are distinct; conflating them is possible precisely because 𝒜 has not been declared.

## The Two-Sentence Disclosure Standard for Grammatical Analysis

Following the paper's model exactly (declare M, declare 𝒜, declare B):

> *M is [grammar / rule system / parsing procedure] applied to [corpus / elicited paradigm / attested strings]; 𝒜 is the class of [underlying representations / structural analyses / competing derivational histories] G is held responsible for distinguishing.*

> *B(G; 𝒜) contains [neutralizations, ambiguous derivations, or URs the rule system cannot discriminate at any corpus size]; [specific structural distinctions] lie outside B and are recoverable under G from available surface evidence.*

**Worked example.** A claim that a CFG accounts for Sanskrit nominal declension:

> *M is a context-free grammar generating Sanskrit nominal surface forms from stem-plus-suffix terminal sequences; 𝒜 is the class of analyses differing in stem-internal vowel grade, suffix boundary placement, or sandhi application site, which the grammar is claimed to distinguish.*

> *B(G; 𝒜) contains any pair of analyses whose derivational paths converge to the same string under G's rules, including sandhi-induced neutralizations and any feature distinction not encoded in G's terminal vocabulary (e.g., pitch-accent); the alternation between strong and weak stem grades is outside B where the grammar generates distinct strings from distinct grade specifications.*

The discipline this enforces is real. The Aṣṭādhyāyī itself, implicitly, applied it: the Vedic grammar was separated into distinct rule-sets (the Atharvavedasūtras, Phiṭsūtras) rather than incorporated into the core apparatus. That separation is, in effect, a declaration that the core grammar's alternative class excludes Vedic morphology, and its blind set at that scope is therefore the entire Vedic paradigm. The tradition did not name the blind set formally; but it drew the scope boundary - and drawing the boundary is what the disclosure standard makes compulsory.
