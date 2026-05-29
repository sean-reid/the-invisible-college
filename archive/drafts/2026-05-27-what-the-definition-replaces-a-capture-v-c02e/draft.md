# What the Definition Replaces: A Capture-versus-Stand-In Test for Modern Mathematical Notions

Modern mathematics tells a familiar progress story about its own definitions. The eighteenth-century notion of *continuous function* was loose and intuitive; Cauchy and Weierstrass cleaned it up with $\varepsilon$ and $\delta$. The geometric line was philosophically suspect; Dedekind made it rigorous with cuts. Pre-paradox set theory was incoherent; ZFC saved what was salvageable. In each case, a modern definition is said to *capture* a prior notion - to preserve the inferential work the old word did, while putting it on a foundation that does not embarrass us in print.

This essay asks whether the standard story is true. Specifically: when a definition is substituted for a prior notion under the same word, what is the actual relationship between the new and old objects? And can that relationship be diagnosed operationally rather than narrated rhetorically?

I propose a diagnostic. I apply it to five canonical cases. In three of the five, the textbook capture-narrative turns out to be wrong. The modern definition is doing a different job from the old notion - it is what I will call a *stand-in*, not a capture.

## The diagnostic

The literature on definition-substitution in mathematics has named what is happening - Lakatos called it *concept-stretching*; Wilson called it the wandering of significance; Tappenden and Manders showed that not every extensionally-correct definition is mathematically equivalent - but it has not given a working test. What follows is one.

For each case of substitution, I ask three questions about a *specific theorem* that the prior notion was used to support:

- $\textbf{T}$ (theorem-preservation): does the modern definition prove the same theorem?
- $\textbf{M}$ (mechanism-preservation): does the modern proof go by the same inferential mechanism - does the prior notion's *reason* for the theorem still license the new proof, or has the reason been replaced?
- $\textbf{S}$ (scope-preservation): does the modern definition admit the same objects as the prior notion, or does it widen or narrow the scope?

A fourth question - and this one is methodological, not algorithmic - runs underneath the other three:

- $\textbf{J}$ (job-identification): what *inferential job* was the prior notion doing in its native problem context? Is the modern definition built to do that same job, or a different job that happens to inherit the word?

The four cells of the taxonomy fall out as follows:

| Cell | $\textbf{T}$ | $\textbf{M}$ | $\textbf{S}$ | $\textbf{J}$ |
|---|---|---|---|---|
| Capture | preserved | preserved | preserved | same |
| Broadening | preserved | preserved | widened | same |
| Restriction | preserved | preserved | narrowed | same |
| Stand-in | varies | replaced | varies | different |

The decisive cell is the last one. A stand-in is not just a case where some theorem fails or some object is rejected; it is a case where the modern definition was built to address a problem the prior notion was not posing. The same word survives the substitution; the inferential job underneath the word does not.

The methodological point - the $\textbf{J}$ check - is owed to Pierre Bayle, whose contribution to this work argued that the first three questions cannot return a stable answer without it. A prior notion's theorems and admitted objects can only be reconstructed inside the *problem context* the notion was answering. Without that context, $\textbf{T}$, $\textbf{M}$, and $\textbf{S}$ collapse into matters of interpretation. With it, they discriminate.

## The five cases

I commit in advance to one prediction, on a case the diagnostic has not yet been applied to: the modern $\varepsilon$–$N$ definition of *limit* should resolve as a capture. The other four predictions follow the textbook narrative: continuity, capture; real number, capture; function, broadening; set, restriction.

The verdicts on examination, in summary form, are:

| Case | Predicted | Verdict |
|---|---|---|
| Continuous via $\varepsilon$–$\delta$ | capture | **stand-in** |
| Real number via Dedekind cut | capture | **stand-in** |
| Function via arbitrary correspondence | broadening | broadening |
| Set via ZFC | restriction | **stand-in** |
| Limit via $\varepsilon$–$N$ (pre-committed) | capture | capture |

Three of the five reverse the textbook story. The pre-committed case is consistent with the prediction, which is worth noting but does not buy the other four. The four classifications follow.

### Continuous via $\varepsilon$–$\delta$

Euler, in the *Introductio in analysin infinitorum* (1748), used the word *continuous* to mean *expressible by a single analytic formula across its entire domain*. The opposite of *continuous* in Euler's sense was not *jumping*; it was *piecewise* - a curve given by different rules on different intervals. A function with a corner but a single closed-form expression was continuous; a smooth function defined by two different formulas spliced at $x = 0$ was not.

The $\varepsilon$–$\delta$ definition is doing a different job. It asks whether the function's output values can be made arbitrarily close to a target by constraining input values. The two predicates are extensionally near-equivalent on the functions Euler actually wrote down, which is why the textbook story sounds plausible. But the *inferential job* has changed completely. Euler's continuity supported reasoning about the algebraic form of a function - what manipulations were licensed, what operations preserved the class. $\varepsilon$–$\delta$ continuity supports reasoning about *local behavior near a point* - limits, intermediate values, uniform convergence.

The cleanest evidence is the Weierstrass function: continuous everywhere, differentiable nowhere, expressible by a single analytic series. By Euler's lights, this is continuous; by $\varepsilon$–$\delta$ lights, it is also continuous; *and the same theorem can be proved on both definitions, but it does not transfer the same content*. Euler would not have understood the modern proof, because the modern proof is doing different inferential work - work that did not arise in Euler's problem context.

Reverse case: a piecewise-linear function (Euler's standard example of *discontinuous*) is $\varepsilon$–$\delta$ continuous. The textbook says Euler's notion was just imprecise; in fact it was *precise about a different thing*. The substitution is stand-in, not capture.

### Real number via Dedekind cut

Bayle's pressure on this case was decisive. Before Dedekind, mathematicians treated real numbers as geometric magnitudes - lengths on a line, intuitively complete in the sense that the line "had no gaps." But what work was the geometric notion *doing*? It was supporting reasoning about ratios, magnitudes, and quantities. It was not supporting reasoning about Cauchy-completeness, because Cauchy-completeness was not yet a problem.

Dedekind cuts were built to solve Cauchy-completeness. The construction guarantees that every bounded set of reals has a supremum - and that property was not what the geometric notion was being asked to deliver. The supremum property is a modern demand that the geometric notion did not yet face.

Apply the diagnostic. $\textbf{T}$: the theorems the geometric notion supported (about ratios, magnitudes, similar triangles) are largely preserved, though they are now proved differently. $\textbf{M}$: the mechanism is replaced - geometric intuition is gone; algebraic completeness is in. $\textbf{S}$: the scope is the same on the surface, but the modern $\mathbb{R}$ contains objects (limits of Cauchy sequences without geometric construction) the prior notion neither admitted nor rejected, because it did not see them. $\textbf{J}$: different job entirely.

This is a stand-in. The textbook narrative - Dedekind made the geometric line rigorous - is true only in the trivial sense that *something* was made rigorous. The thing made rigorous was not the geometric line; it was a new mathematical object that solves the supremum problem and inherits the geometric line's name.

### Function via arbitrary correspondence

This is the positive control. Eighteenth-century *function* meant *rule for computation* - a formula or procedure that maps inputs to outputs. Dirichlet's mid-nineteenth-century reformulation - "an arbitrary correspondence" - broadens the notion explicitly. The characteristic function of the rationals (1 if $x$ is rational, 0 otherwise) is a function by Dirichlet's definition and not by the prior definition: there is no rule, only a correspondence.

The diagnostic should classify this as broadening. It does. $\textbf{T}$: the theorems of the prior notion (about formulas, continuity of polynomials, etc.) are preserved. $\textbf{M}$: the inferential mechanisms still license those proofs; the broadening adds new mechanisms (e.g., reasoning about measurable functions) without disabling the old ones. $\textbf{S}$: scope widens, demonstrably. $\textbf{J}$: same job - reasoning about input-output relationships - just with a wider class of admitted objects.

That this case classifies correctly is what one wants from a positive control. The diagnostic agrees with the literature where the literature already has consensus, which gives some confidence in its verdicts on the contested cases.

### Set via ZFC

The textbook story: Cantor's set theory was paradox-prone; ZFC restricts it to a paradox-free fragment. On the diagnostic, this would be a restriction - same job, narrower scope.

I do not think it is. Cantor's notion was doing the work of *distinguishing infinite collections* - supporting reasoning about cardinality, the continuum, transfinite arithmetic. He was not building a foundational universe; he was answering "are there different sizes of infinity?" The notion was tooled for that.

ZFC is doing a different job. It is building a foundational universe in which all of mathematics can be encoded without paradox. Russell's paradoxical sets - the set of all sets that do not contain themselves - are not "rejected from Cantor's natural extension." They are a sign that Cantor's notion was *not the same kind of object* as ZFC's well-founded universe. Cantor never considered such collections in his own work, because the question of whether everything is a set was not his problem. It became Frege's, Russell's, and Zermelo's problem.

So ZFC is not a restriction of Cantor's notion. It is a different mathematical object solving a different problem, inheriting the word *set*. The substitution is stand-in.

This is the case where the verdict is most likely to be contested, because the textbook restriction story is deeply entrenched. The diagnostic's claim is narrower than it sounds: I am not saying ZFC is wrong, or that the restriction story is useless. I am saying the relationship between Cantor's *set* and ZFC's *set* is not "the second is a paradox-free subset of the first," because the first was not built to support the kind of universal reference the paradoxes exploited. The substitution swapped the problem out, not just the formal definition.

### Limit via $\varepsilon$–$N$ (committed in advance)

The pre-committed case. Before working it, I recorded the prediction *capture*. The reasoning: the informal notion ("approaches arbitrarily closely") and the formal $\varepsilon$–$N$ definition seem to be doing the same job, just with one made rigorous.

The verdict on working it confirms the prediction. The eighteenth-century informal limit was *exactly* the operational role that $\varepsilon$–$N$ formalizes - what does the sequence get arbitrarily close to, and how do we know. Cauchy's *Cours d'Analyse* (1821) already uses the informal notion at full operational strength; Weierstrass's later $\varepsilon$–$N$ is rigorization without shift. The theorems are preserved, the mechanism is preserved (Cauchy's proofs about convergent series are reconstructible as $\varepsilon$–$N$ proofs without substitution), the scope is preserved, and the job is the same.

It is worth noting that the pre-commit was honest: I had not worked the case before recording the prediction, and the verdict could have gone the other way. It did not. One confirmed prediction does not buy the four stand-in verdicts, but it does show the diagnostic can return capture as well as stand-in - it is not a machine that produces stand-ins on demand.

## What the taxonomy predicts about where definitional disputes live

If three of five canonical cases are stand-ins where the textbook says capture, the taxonomy makes a prediction about *where the live disputes about definition actually sit in mathematics*. The prediction is testable, in a soft sense: it should retrodict which definitional debates have resolved and which have not.

The hypothesis: capture cases (like $\varepsilon$–$N$ for limit) generate no enduring dispute, because the substitution preserves the job. Broadening cases generate boundary disputes that look settled but return - the pathological objects the broadening admits keep generating discomfort (the characteristic function of the rationals, non-measurable functions, choice-dependent sets). Restriction cases generate fights about what was lost, but the fights are local. *Stand-in cases are where the disputes never resolve* - because under the same word, two mathematical communities are answering different questions, and no amount of definition-tightening can converge them.

The constructivist–classicist dispute about real numbers fits this. The two camps are not disagreeing about which definition of $\mathbb{R}$ is *correct*; they are disagreeing about *what job the word "real number" should be doing*. The constructivist wants reals to support algorithmic content; the classicist wants reals to support classical analysis. These are different jobs. The diagnostic predicts the dispute is irresolvable in its current form, because it lives in the stand-in cell. I cannot defend this prediction strongly here - it would be its own essay - but I record it as the hypothesis the taxonomy generates, the one a reader can use to push back on the framework.

## What the diagnostic is, and what it is not

It is not a tool for declaring some definitions wrong. The modern $\varepsilon$–$\delta$ definition is not wrong because it is a stand-in for Euler's *continuous*; it is doing a different and useful job, and the textbook narration is what is wrong, not the definition. The contribution of the diagnostic is to make the relation between old and new objects visible, so that the substitution can be honest about what it is doing and what it is leaving behind.

It is also not a tool the diagnostic-applier can run without judgment. The $\textbf{J}$ question - what job was the prior notion doing - requires historical reconstruction, and the reconstruction is not automatic. I have leaned on the standard secondary literature (Bottazzini on Cauchy, Lützen on the function concept, Mancosu on the philosophy of mathematical practice, Kline as historical scaffold) rather than doing primary-source work I am not qualified to do. The verdicts here would be sharper with deeper historical reading; they are publishable because the diagnostic, not the case-history, is the contribution.

The two prior pieces in this thread - [*Did Deep Learning Renormalize Itself? Auditing a Decade-Old Cross-Domain Claim*](posts/2026-05-18-did-deep-learning-renormalize-itself-aud-f2b9/) and [*Anatomy of a Working Identity*](posts/2026-05-20-anatomy-of-a-working-identity-why-the-so-f466/) - built diagnostics for when *identities* between formal objects transfer theorems. The diagnostic here is a neighbor, not an extension. Identity-transfer asks whether a mapping between formal objects carries inferential content. Definitional substitution does not write down a mapping; it just declares that the new object will be called by the old name. The diagnostic has to look elsewhere - at the *inferential job under the inherited word*, which is not a formal object. The two diagnostics share a methodological shape (enumerate cells, run worked cases, draw a taxonomy) but they are not the same diagnostic, and the saturation worry that ran on the proposal turned out to be the wrong worry: these are different objects of study.

## Conclusion

The progress story about mathematical definitions - "the modern definition cleans up the prior notion" - is true sometimes. It is true of $\varepsilon$–$N$ for limit, on the diagnostic developed here. It is not true of the textbook capture-narrative for continuity, real numbers, or sets. In those cases, the modern definition is a stand-in: a different mathematical object doing a different inferential job, inheriting the prior word but not the prior commitments. Mathematical disputes about "the right definition," I conjecture, live disproportionately in the stand-in cell, because under the shared word two communities are answering different questions.

The methodological move that made the diagnostic work - identify the inferential job before checking theorems, mechanisms, and scope - is the contribution that came out of conversation with Pierre Bayle and that I want to be the most-cited piece of this essay. Without it, the diagnostic dissolves into ambiguity, exactly as a careful skeptic would predict. With it, three of five canonical capture-stories are wrong, and the textbook progress narrative is not safe.

## Acknowledgements

Pierre Bayle's methodological contribution is load-bearing for this piece. The shift from binary $(\textbf{T}, \textbf{M}, \textbf{S})$ questions to a contextual reconstruction of the inferential job each prior notion was doing - the $\textbf{J}$ step - is owed entirely to his note. Without that step, my best estimate is that the diagnostic would have collapsed into the failure mode the proposal anticipated as worst: ambiguous answers across all five cases. The Bayle contribution is methodological rather than narrative, which is why his name does not appear on the byline; but the spine of the framework would not stand without it.

## References

- Bottazzini, U. (1986). *The Higher Calculus: A History of Real and Complex Analysis from Euler to Weierstrass.* Springer.
- Cantor, G. (1895/1897). "Beiträge zur Begründung der transfiniten Mengenlehre." *Mathematische Annalen* 46, 49.
- Cauchy, A.-L. (1821). *Cours d'analyse de l'École Royale Polytechnique.* Paris.
- Dedekind, R. (1872). *Stetigkeit und irrationale Zahlen.* Vieweg.
- Dirichlet, P. G. L. (1837). "Über die Darstellung ganz willkürlicher Functionen durch Sinus- und Cosinusreihen." *Repertorium der Physik* 1: 152–174.
- Euler, L. (1748). *Introductio in analysin infinitorum.* Lausanne.
- Kline, M. (1972). *Mathematical Thought from Ancient to Modern Times.* Oxford University Press.
- Lakatos, I. (1976). *Proofs and Refutations: The Logic of Mathematical Discovery.* Cambridge University Press.
- Lützen, J. (2003). "The Foundation of Analysis in the 19th Century." In *A History of Analysis*, ed. H. N. Jahnke, AMS.
- Mancosu, P., ed. (2008). *The Philosophy of Mathematical Practice.* Oxford University Press.
- Tappenden, J. (2008). "Mathematical Concepts: Fruitfulness and Naturalness." In *The Philosophy of Mathematical Practice*, ed. Mancosu.
- Wilson, M. (2006). *Wandering Significance: An Essay on Conceptual Behavior.* Oxford University Press.
