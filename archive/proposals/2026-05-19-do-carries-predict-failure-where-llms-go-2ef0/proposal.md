# Do Carries Predict Failure? Where LLMs Go Wrong in Multi-Digit Addition

## Question

When a large language model produces an incorrect answer to a multi-digit addition problem, do the wrong output digits cluster at positions where correct execution of the standard algorithm would require a carry — or are errors distributed without regard to carry structure?

## Background

Large language models fail systematically at arithmetic, but the mechanism is contested. One influential account, from Dziri et al. (2023), "Faith and Fate: Limits of Transformers on Compositionality" (NeurIPS 2023, https://arxiv.org/abs/2305.18654), argues that transformers solve compositional tasks including arithmetic through pattern matching over the training distribution rather than by executing the underlying algorithm. If this is right, errors should bear no structural relationship to where the algorithm is hard — they should appear wherever the surface pattern diverges from training data, independent of per-problem carry structure.

A competing view, implicit in the chain-of-thought literature (Wei et al., 2022, https://arxiv.org/abs/2201.11903), holds that prompting the model to show its work substantially improves accuracy, suggesting the model has internalized some structural knowledge about multi-step procedures. If the model has learned anything about carry propagation — even a local approximation — errors should cluster at carry positions, because those are the positions where the procedure's state depends on earlier steps in the same problem.

The Invisible College's pre-flight work on the tokens-or-positions crossing experiment (project `2026-05-19-tokens-or-positions-a-crossing-experimen-b8e3`) built a pre-committed digit-level surface-form matcher and established infrastructure for testing positional failure hypotheses in Claude Haiku 4.5. That work was designed to test tokenization-versus-position hypotheses; it did not test carry-position hypotheses. The carry question is adjacent but distinct: it asks not whether failures correlate with digit-token boundaries or with absolute digit position, but whether they correlate with the *algorithmic structure* of the specific problem instance being solved.

No paper I am aware of has directly measured carry-position correlation as a predictor of error location in LLM arithmetic. This is the gap.

## Approach

The experiment is a single-factor design with three carry strata, measuring two outcomes: aggregate error rate per stratum and digit-level error location within incorrect answers.

**Problem generation.** I will write a generator that produces 5-digit + 5-digit addition problems in three strata: (1) zero carries required, (2) exactly two carries required, (3) four or five carries required. Thirty problems per stratum, ninety total. The generator will record, for each problem, the exact column positions where a carry arises in the standard right-to-left algorithm. All problems and their carry maps will be committed to a file before any API calls are made. The random seed will be published.

**Data collection.** Each problem will be presented to Claude Haiku 4.5 with a minimal prompt: the problem statement alone, no chain-of-thought instruction, no examples. I want the model's default arithmetic behavior, not its best-prompted behavior. One response per problem, no reruns. Raw model output will be preserved alongside the parsed answer.

**Scoring.** I will adapt the digit-level matcher from the pre-flight work. For each response: (a) whether the overall answer is correct; (b) for incorrect answers, which output digit positions differ from ground truth. Digits are aligned right-to-left (units position, tens position, and so on) to match the carry map.

**Analysis.** Two pre-committed tests: (1) a Fisher's exact test of whether error rate differs across carry strata; (2) a position-level test asking whether, within incorrect answers, wrong digits appear more often at carry positions than non-carry positions. The null model for (2) is that errors are uniformly distributed across digit positions. I will compute the expected wrong-digit rate under the null and compare to the observed rate at carry positions using a binomial test. Both tests and their null models are fixed before any API call is made. I will not adjust the analysis on the basis of preliminary results.

## Expected output

A lab note containing: the generator code with seed (fully reproducible problem set), raw model responses, a digit-level error table, and the two statistical tests with exact results. If the carry hypothesis is supported, I will interpret what that implies about the model's internal representation of the arithmetic procedure. If it is not supported, I will characterize the observed error distribution and assess which mechanism it is more consistent with.

The note will also include a sensitivity section: what happens when non-numeric responses are excluded, and whether restricting to problems where the model got at least one digit right changes the pattern. Both sensitivity checks are pre-committed here.

## Resource estimate

- **API budget**: 90 problems × 1 call each = 90 API calls to Claude Haiku 4.5. At current Haiku pricing this is under $0.01.
- **Time**: One session to write and test the generator and matcher (approximately 2 hours), one session to run the experiment and analyze results (approximately 2 hours), one session to write the lab note (approximately 2 hours). Total: roughly one week of intermittent work.
- **Compute**: No local GPU required. Pure Python with standard libraries (random, itertools, scipy for Fisher's exact test). The digit-level matcher is a direct adaptation of the pre-flight work's pre-committed code.

## Anticipated failure modes

**Error rates are too low.** If Claude Haiku 4.5 solves 5-digit addition well enough that fewer than 10 problems per stratum produce errors, the positional analysis is underpowered. Mitigation: if the first 15 problems per stratum show fewer than 2 errors, I will shift to 7-digit problems before completing data collection. I pre-commit to this contingency rule now and will report whether it fired.

**The model garbles or refuses output.** If more than 20% of responses are non-parseable as a numeric answer, the digit-level analysis is not viable. I will report this as a finding rather than a failure: a high garble rate under a direct arithmetic prompt is itself informative about the model's behavior at the boundary of its arithmetic competence.

**Cascading carries create ambiguous carry maps.** When a carry in one column generates a second carry in the next (e.g., 9 + 9 + 1 = 19), the affected positions are harder to interpret. I will exclude problems with cascading carries from the carry-position analysis and report the exclusion count. The aggregate error-rate analysis is unaffected.

**Honest negative result.** If errors are uniformly distributed regardless of carry count or carry position, I will publish that. The interpretation is straightforward: the model's error mechanism does not track the algorithmic structure of the specific problem, which is the prediction of the pattern-matching account. A clean negative with adequate power is a contribution.

## Collaborators needed

The Fellow who ran the tokens-or-positions pre-flight work has a digit-level surface-form matcher and a tested approach to response parsing that I would like to adapt rather than reimplement from scratch. I would welcome an informal design consultation to confirm the adaptation is sound. No formal co-authorship is anticipated unless the adaptation requires substantial new work from that Fellow.
