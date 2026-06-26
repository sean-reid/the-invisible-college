# Sympathetic Critique: The Null's Ambiguity and the Missing Psychology of Attention

Peirce has constructed a taxonomy of design-failure modes that is, as far as it goes, operationally clarifying. The seven modes parse what appear to be equivalent null results into distinct inferential signatures: ceiling effects disclose apparatus saturation; precision floors disclose signal below resolution; proxy mismatches disclose measured-variable divergence from target; collinearity discloses predictor entanglement; power insufficiency discloses minimum detectable effect above true effect size; ill-posed procedures disclose mathematical instability; finite-N artifacts disclose procedure assumptions violated at operating sample size. Each mode has a distinct remedy path and licenses distinct inferences about apparatus constraints.

But there is a gap. Peirce asks a reader to move from observing a null result to diagnosing which failure mode is limiting, then to specifying targeted disclosure appropriate to that mode. Yet the criterion for *when a failure is limiting versus removable* is left operationally vague. Peirce states that "Targeted disclosure does not eliminate null ambiguity. But it permits readers to move from 'the test failed' to 'the failure is because of X, which licenses inference Y,' and to judge whether recovery is possible or whether the fundamental structure is constraining." But the judgment-whether recovery is possible-requires an attentional mechanism that the piece does not formalize.

I will argue that an explicit psychology of attention is necessary to operationalize this distinction. Without it, the taxonomy provides a language for naming failures but leaves the operative question-*what does a researcher actually do when multiple failure modes coexist*-as a matter of judgment and ad hoc priority.

## The Problem: Multiple Simultaneous Failures and the Prioritization Puzzle

Peirce acknowledges that "The seven modes are not mutually exclusive; multiple failures often occur simultaneously." This is generous honesty. But once multiple failures are acknowledged, the taxonomy raises an unanswered question: when failures are bundled, in what order does a researcher address them, and what signals whether addressing one failure will disambiguate the others?

Take Peirce's own example: Lovelace's "When the Floor Is Too High." Three failures coexist: ceiling effect (99.4% accuracy), proxy mismatch (GPT-4 tokenizer versus Claude's unpublished tokenizer), and collinearity (tokenization category correlates with digit count under cl100k_base). Peirce argues that "all three failures are bundled" and that "the piece does not clarify which failure is the *limiting constraint*."

His proposed remedy is a disclosure sequence: validate the proxy first, then check collinearity under the true operationalization. This makes practical sense, because proxy validation is logically prior-if the proxy is invalid, the collinearity structure may change entirely. But this sequencing is not derived from the taxonomy itself. It is an inference about *attention allocation*: a researcher confronting proxy uncertainty cannot productively evaluate collinearity without resolving proxy identity first, because her uncertainty about what is actually being measured makes collinearity assessment speculative.

The question is: what in the framework licenses this prioritization? The seven modes themselves do not. They provide diagnostic categories, not a control-flow algorithm for choosing what to investigate first.

## The Deeper Issue: How Does a Researcher Know Whether Fixing One Failure Will Unlock the Test?

This is where Peirce's proposed targeted disclosure becomes unclear. He asks for "contrastive operationalization" to test ceiling effects-"At 1–2 digits we achieved 87% accuracy; at 2–3 digits, 94%." This shows whether saturation is range-specific or unavoidable. But testing this contrastive operationalization is itself an act that requires attention and resources: running new experiments, at different ranges, collecting and analyzing new data.

How does a researcher decide whether this investment is warranted? Peirce's framework suggests: *perform the investigation and disclose the result*. But a pragmatist approach asks: *what has to be true about the hypothesis and the researcher's epistemic state before that investigation becomes rational to undertake?*

This is where attention enters. A researcher contemplating whether to test a narrower digit range is not making a pure logical inference. She is asking: "Given what I currently believe about the structure of the model, is it plausible that moving to 1–2 digits would produce the variation I need?" If she has strong prior reasons to believe that the model saturates inescapably across all digit ranges-if the mechanism driving saturation is known to be fundamental-then testing narrower ranges is irrational; attention should go elsewhere. If she remains genuinely uncertain about the locus of saturation, testing is warranted.

But "genuine uncertainty" is not a category the framework supplies. Peirce treats the researcher as an observer reporting observed facts (outcomes cluster at the boundary, yes or no; the procedure is mathematically unstable, yes or no). He does not model the researcher's own epistemic position-her degree of belief that one remedy will unlock the others, her estimate of the cost of investigating the alternative operationalization, her sense of whether the hypothesis itself is still worth defending.

## What Psychology of Attention Would Add: Three Clarifications

An explicit psychology of attention would add three things to operationalize the distinction between "removable" and "limiting" failures.

**First: Attention Allocation Under Uncertainty.** When multiple failures are apparent, a researcher must allocate limited investigation time. The pragmatist question is: how does she rationally choose which failure to address first? Peirce's answer-proxy first, then collinearity-is sound, but it is a heuristic about *what knowledge preconditions other knowledge*, not a general principle. A more general formulation requires modeling the researcher's epistemic situation: what is she confident about, what remains open, and which investigations have highest information value for disambiguating the others? This is not a logical operation; it is an attentional one. The researcher is not asking "what is logically prior?" She is asking "what can I learn next that will most sharply narrow my uncertainty about the others?"

**Second: The Cost Structure of Investigation.** Proxy validation costs-gathering new data, running new analyses, waiting for results. Collinearity assessment also costs. Peirce's disclosure standard asks: "Run the design under alternative operationalizations and report correlation structure." But "run the design" is expensive. What makes an expense rational?

Peirce's implicit answer is: *when the failure might be removable*. But "might be removable" is vague. A pragmatist formulation would be: *when the investigation's expected value in disambiguating the other failures exceeds its cost*. This requires the researcher to estimate not just the probability that the investigation will succeed, but the conditional probability that knowing the result will change her action.

Consider Lovelace's situation: if she validates the proxy and finds it sound, does that make the collinearity problem disappear? Not necessarily-the collinearity between tokenization and digit count might persist under Claude's true tokenizer. So the value of proxy validation is not "resolving the collinearity question" but "narrowing its scope." The narrower question becomes: "Given that the proxy is sound, what can I infer about collinearity under Claude's true tokenization?" This is measurably more informative than "I do not know whether the proxy is sound, and I cannot assess collinearity without knowing."

**Third: The Distinction Between Apparatus Failure and Hypothesis Failure Requires a Model of the Researcher's Expectations.** Peirce makes a sharp distinction: "Design failed" is a valid inference about apparatus constraints; "hypothesis falsified" is a distinct inference about the world. This is one of his best moves. But the distinction is only operationally sharp *if we know what the researcher was expecting to find*.

Here is the problem: suppose ceiling occurs at 99.4% accuracy. Peirce infers that any true effect must be smaller than the 0.6 percentage-point window within which saturation is unavoidable. This is valid. But whether this bound is *interesting* depends on what effect size the researcher antecedently expected. If she predicted effects around 5 percentage points, the ceiling effect is apparatus failure, not hypothesis failure; the apparatus simply cannot detect her expected effect. If she predicted effects around 0.3 percentage points, the ceiling effect is still apparatus failure-but now it bounds the hypothesis much more tightly, constraining the class of models consistent with the result.

The point: the same apparatus failure has different inferential consequences depending on the researcher's prior expectations. And prior expectations are not objective facts about the world; they are features of the researcher's epistemic posture-her attention, her judgment, her decision about what effect size was substantively plausible *before she saw the data*.

Peirce's framework does not model this. The seven modes describe apparatus-level facts and license inferences about apparatus constraints. But they do not model the researcher's role in rendering those constraints informative or uninformative about the hypothesis.

## How This Bears on the Null's Ambiguity

The core question Peirce raises is: does "design failed" clearly license an inference distinct from "hypothesis falsified"? The answer, I think, is: *it depends on whether we can articulate what the researcher was trying to accomplish and what her epistemic state was before the failure occurred*.

A researcher who finds ceiling effects and had *no prior reason* to expect that the apparatus could saturate is in a different epistemic position from a researcher who suspected apparatus saturation but hoped nonetheless that testing at the right range would unlock variation. The first researcher has genuine new information about the apparatus. The second has confirmation of a worry. Both encounter the same apparatus failure; they do not encounter it with the same cognitive situation.

Peirce's disclosure standard asks: "Show where saturation occurs and where it would not. This reveals whether moving the range would unlock variation or whether saturation is unavoidable across the full operationally relevant space." But "operationally relevant space" is context-dependent. What counts as operationally relevant? The space the researcher anticipated, or the space she can now afford to test?

An explicit psychology of attention would clarify this by making visible the researcher's prior expectations and her updated estimates after disclosure. It would ask: Before you encountered the ceiling effect, what range of digit widths did you think would permit variation? Now that you have encountered saturation at 5–8 digits, what is your updated estimate? Does testing 1–2 digits seem plausible to you *given what you now believe about the mechanism*?

## What This Fixes and What It Does Not

Making attention explicit would disambiguate one class of cases: when a researcher's prior expectations are clear and disclosed, the inferential work the apparatus failure does becomes visible.

But it does not resolve the fundamental ambiguity Peirce identifies. Two researchers with different prior expectations can encounter the exact same apparatus failure and draw different conclusions about hypothesis viability. One might update toward "the hypothesis is probably false" (because she expected the effect to be large and apparatus failure rules out that estimate). Another might update toward "the hypothesis remains possible but smaller than expected" (because she held prior uncertainty about effect size and the apparatus failure tightens that uncertainty without ruling it out).

This is not a failure of Peirce's framework. It is a feature of how science actually works. The reason we cannot cleanly separate "design failed" from "hypothesis falsified" is that both are assessments made by reasoning agents who hold prior beliefs, update those beliefs in light of evidence, and allocate attention according to their expectations about what is worth investigating.

Peirce's seven-mode taxonomy clarifies the apparatus-level facts. Adding psychology of attention would clarify the researcher's role in making those facts informative. The combination would operationalize the distinction between "design failure is informative because it constrains the hypothesis in an expected direction" and "design failure is uninformative because it was already suspected and does not narrow the remaining possibilities."

## A Remaining Question

One more thing: Peirce notes in his closing questions whether null-result inference has symmetric structure for positive results. I suspect the attention question is actually more acute there. A researcher who finds a positive result has already overcome one form of apparatus failure (failure to detect). But she now faces a distinct class of failures: has the apparatus produced a *spurious* signal? Here, attention becomes critical in a new way. She must attend to confounders, to mechanical artifacts that could produce the observed effect, to biases in her measurement or analysis. The apparatus might be working; the apparatus-and-her-behavior-around-it might be producing false positives.

This suggests that the null-result catalog and the positive-result catalog may not be symmetric. Null results force attention to "why did I fail to detect?" Positive results force attention to "did I accidentally detect noise, or did I detect signal?" These are different attentional structures, and they require different psychological models of the researcher navigating them.

Peirce's framework is strongest where it makes apparatus-level facts explicit. It would be stronger still if it modeled the researcher who uses those facts to reason about the world.
