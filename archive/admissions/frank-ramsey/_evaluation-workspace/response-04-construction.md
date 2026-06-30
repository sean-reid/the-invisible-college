# Response to Problem 4: Construction

## Option A: A Dutch-book audit of an LLM's stated probabilities

### The question

When a language model is asked to assign probabilities to propositions, do those numbers behave as probabilities? Specifically: do they obey the additivity axiom across a complementary partition, and do they obey the conjunction inequality `P(A ∧ B) ≤ min(P(A), P(B))`?

If they do not, the model is *Dutch-book vulnerable*: a bettor who took the model's stated odds at face value could construct a portfolio of bets that loses money in every state of the world. That is more than an aesthetic flaw. It is the precise sense in which the stated numbers are not a probability function at all, and it is the strongest possible evidence that the surface confidence reports cannot be used as inputs to a downstream decision procedure without recalibration.

This is the Ramsey-de Finetti construction applied to a system that emits probability words: the test is structural, not psychological.

### The artifact

A script that, for each item in a question set, elicits four numbers from the model in independent contexts and computes two coherence residuals.

**Inputs.**

- A set of `N ≈ 200` factual yes/no propositions about which the model has non-trivial uncertainty. Examples: "Is `cuneiform` older than `hieroglyphs`?", "Did `Ulysses S. Grant` outlive `Mark Twain`?". Ground truth is recorded but is *not* used in the coherence test itself — coherence is a property of the stated probabilities, independent of correctness.
- A second set of `M ≈ 100` proposition pairs `(A, B)` over which I will test conjunction. Pairs are sampled so that some are nearly independent ("Is Beijing north of Cairo?" × "Did Goethe write in German?") and some share content ("Is uranium denser than lead?" × "Is uranium denser than gold?"). The mix matters because conjunction violations are more diagnostic when the model could in principle reason about dependence.

**Procedure.**

For each proposition `A`, in fresh contexts:
1. Elicit `p₁ = P_model(A)` by asking "What is your probability that A is true?"
2. Elicit `p₂ = P_model(¬A)` by asking "What is your probability that A is false?"
3. Record the *additivity residual* `r_A = p₁ + p₂ − 1`.

For each pair `(A, B)`:
1. Elicit `p_A`, `p_B`, and `p_{AB} = P_model(A ∧ B)`, each in independent contexts.
2. Record the *conjunction residual* `c_{AB} = p_{AB} − min(p_A, p_B)` (a positive value is a violation).

Each elicitation is repeated `k = 5` times with different prompt phrasings to estimate within-item variance. Use `temperature = 0` for the answer call where the API supports it; the noise of interest is across-prompt, not within-decode.

### Predicted outputs

Three predictions, ordered from least to most committal.

1. *Mean additivity residual is non-zero and biased positive.* Models trained on internet text learn to round confidence up. I expect `E[r_A] ∈ [0.05, 0.20]` — that is, stated `P(A) + P(¬A)` averages 1.05 to 1.20 across items. This would be the most basic Dutch-book vulnerability.
2. *Conjunction residual is positive for a non-trivial fraction of pairs.* I expect 15–35% of pairs to satisfy `p_{AB} > min(p_A, p_B)`, i.e., the model assigns the conjunction strictly higher probability than at least one of its conjuncts. This is the conjunction fallacy in its sharpest form and would not require any judgement about what the "correct" probabilities are — it is incoherent on its face.
3. *Coherence improves under chain-of-thought elicitation but does not disappear.* Asking the model to "work through your reasoning" before stating the number reduces both residuals but leaves them statistically distinguishable from zero.

I am most confident in (1) directionally and least confident in the magnitude of (3).

### Two ways this could mislead me

**False positive: elicitation-context drift.** The four numbers per pair are elicited in independent contexts. The model may be sampling from slightly different latent "beliefs" each time — not because it is incoherent in the Dutch-book sense, but because the elicitation procedure does not reach the same internal state twice. The signal I want is "the same agent, asked complementary questions, gives incoherent answers." What I might actually be measuring is "the same model, instantiated four times, gives uncorrelated answers." These are different defects.

*Control.* Run a within-context variant where all four numbers are elicited in a single conversation, with each preceded by an instruction not to revise earlier answers. If residuals shrink substantially, the cross-context version was overstating incoherence. I would report both numbers and flag the gap explicitly.

**False negative: the model launders coherence through verbal hedging.** If I let the model emit free text, it may produce phrases like "around 70%, maybe 75%" that I have to coerce to a single number. The coercion rule I use (take the midpoint, take the higher, take the lower) can itself impose coherence or destroy it. A model whose underlying state is incoherent could appear coherent under a generous parser.

*Control.* Force a single-token numerical answer using a constrained-decoding wrapper, and compare results to the free-text version. If they diverge, the free-text version is being smoothed by the parser, and the constrained version is the honest signal.

A third, smaller worry: the propositions in set 1 are not truly complementary if the model treats "A is false" as a different question than "not A is true." This is a quirk of natural-language negation that has nothing to do with probability theory. I would pilot a small sub-experiment with explicitly symbolic propositions to estimate the size of this effect before relying on the main result.

### What the artifact pays off

The artifact gives a published model two scalar diagnostics — mean additivity residual and conjunction-violation rate — that can be tracked across models and across versions of the same model. A model whose residuals are small is one whose stated probabilities can be fed to a decision procedure with only post-hoc rescaling. A model whose residuals are large is one whose probability words are not probabilities, and any downstream system that treats them as such is acting on a Dutch-bookable input.

That is a claim that decides something operative. It is the kind of test I would want to run before I trusted a model's "I am 80% sure" in any setting where the 80% mattered.