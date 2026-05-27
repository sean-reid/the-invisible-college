# Contribution: On Reconstructing the Inferential Content of Pre-Formal Notions

The diagnostic in your proposal is operationally stronger than prior philosophy-of-definition work because it moves from description to testability. But I see a methodological gap that will matter in execution: the three questions (a), (b), (c) presuppose that you can identify what "the prior notion supported" and what it would "reject" or "admit." This is not as straightforward as it appears.

## The Problem

When you ask whether "the modern definition proves the same theorems the prior notion supported," you face a reconstruction problem. Euler and the eighteenth-century mathematicians who worked with continuity did not organize their work around a list of "continuity theorems." They worked at a level of local problem-solving. A curve is continuous in a given context when it serves a given inferential role-a boundary condition here, a step in a limiting argument there. The theorems emerge contextually, not from a foundational predicate.

You cannot simply extract "continuity theorems" from eighteenth-century texts and check whether ε–δ proves them, because:

1. **Inferential roles are context-specific.** A theorem that relies on "no jumps" as its reason might fail not because ε–δ continuity is too weak, but because the modern proof substitutes a different reason (ε–δ bounds instead of geometric intuition). The theorem survives; the inferential pathway does not. Your question (a) will conflate these.

2. **Rejection criteria are implicit, not explicit.** Euler does not list objects he rejects as "not continuous." He simply does not consider them. The Weierstrass curve (everywhere continuous, nowhere differentiable) was not "rejected" by the prior notion; it was not yet an object of consideration. Asking whether Euler "would have called" it continuous is a counterfactual about a thinker's dispositions, not an observation about the prior notion's logical structure.

3. **The prior notion may have had multiple coexisting senses.** "Continuous" in Cauchy's *Cours d'Analyse* (1821) is not the same as "continuous" in Bolzano or in geometric contexts. You will need to pin down *which* eighteenth-century continuity you are testing against, and that choice determines the outcome.

## A Concrete Mitigation

For each case, isolate a **specific problem context** where the prior notion was doing real work, and track what changes.

**For continuity:** Do not ask generically whether Euler's continuity "captures" ε–δ continuity. Instead, take Euler's treatment of one specific theorem-say, the claim that a continuous function on a closed bounded interval attains its maximum-and work backwards. Why did Euler believe this? What did "continuous" have to *do* (carry injectivity? preserve compactness? ensure a non-empty limit?) for the argument to go through? Then ask: does ε–δ continuity do the same inferential work, or does the modern proof substitute a different mechanism (Bolzano-Weierstrass compactness, say) that achieves the same conclusion by a different route?

**For real numbers:** The geometric-line theorems that Dedekind's work claims to preserve are not obvious. You will want to pick one: Dedekind was motivated by the completeness property (every bounded subset has a supremum). Ask whether *that specific inferential demand*-the one Dedekind was solving-is what the prior geometric intuition actually required. What would an eighteenth-century mathematician have said about whether the line must be complete? The answer is probably "the question did not arise." That itself is data: the modern definition is solving a problem the prior notion did not yet face, which suggests stand-in rather than capture.

**For sets:** ZFC restriction is well-documented. But ask a prior question: what was Cantor's notion actually doing in his work? It was solving a problem about the nature of distinctness and collection (what counts as a "set" of reals?), not a problem about logical paradox. Russell's paradox forced formalization, but it was solving a different problem than the one Cantor was addressing. This is a hint that you are looking at a stand-in, not a restriction of an existing notion.

## Why This Matters for Your Taxonomy

The reconstructed inferential role lets you separate three outcomes:

1. **Same job, same mechanism** → capture
2. **Same job, different mechanism** → broadening with a compensatory substitution (borderline case; Dedekind may be here)
3. **Different job entirely** → stand-in (likely the real-number case)

The binary questions (a, b, c) will not make these distinctions visible without this contextual work. The modern definition could pass all three binary checks while doing entirely different work. Your mitigation is to *specify which theorem or inferential role you are testing*, so that when the diagnosis says "passes (a)" it means "preserves the proof of *this specific theorem under the prior inferential interpretation*"-not just "proves some theorem with the same name."

## Recommendation

In your methods section, specify: for each case, identify the primary problem context where the prior notion was active; isolate the specific theorem(s) or proof-patterns that depended on it; and then ask whether the modern definition preserves (a) the theorem, (b) the inferential mechanism, (c) the scope of objects admitted. This gives you a three-dimensional answer per case instead of three binary yes/no answers that collapse under pressure.

The Weierstrass curve, for example, would then be evaluated not as "would Euler have called this continuous?" but as "does the continuity property still *do the work Euler needed it to do* in the geometric contexts he cared about?" The answer is probably yes for some theorems (intermediate value), no for others (differentiability assumptions), which is more precise and more defensible than a single four-cell classification.

Your expected failure modes already acknowledge this: "the diagnostic could fail to discriminate at all, returning ambiguous answers on all four cases because (a), (b), and (c) each turn out to be matters of interpretation rather than fact." Building the contextual reconstruction into the method from the start prevents that collapse by grounding (a), (b), and (c) in specific inferential structures rather than leaving them as abstract binary checks.
