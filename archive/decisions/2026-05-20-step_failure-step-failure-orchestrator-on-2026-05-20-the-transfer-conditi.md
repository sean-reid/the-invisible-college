---
kind: step_failure
recorded_at: 2026-05-20T22:37:00+00:00
actors: [orchestrator, orchestrator]
project: 2026-05-20-the-transfer-condition-when-argumentativ-4f6f
---

# Step failure: orchestrator on 2026-05-20-the-transfer-condition-when-argumentativ-4f6f
**Where:** project `2026-05-20-the-transfer-condition-when-argumentativ-4f6f` (state: `editorial`)
**Fellow:** `orchestrator`
**Step:** `editorial`
**Returncode:** 1
**Recorded:** 2026-05-20T22:37:00+00:00

The Fellow's Claude invocation returned non-zero. The autopilot caught the failure, recorded this row, and moved on. The next cycle will retry the same step. No project state was changed.

## stderr (truncated)

```
OSError: [Errno 63] File name too long: '/Users/seanreid/sandbox/the-invisible-college/archive/open-problems/OpenProblem(slug=\'when-does-a-vocabulary-only-borrowing-acquire-evidential-str\', title=\'When does a vocabulary-only borrowing acquire evidential structure over time, and what mechanism does that acquisition follow?\', body=\'The transfer-condition diagnostic is essentially synchronic: at a given moment, does the evidential obligation travel with the mechanism? But several historical cases suggest a diachronic complement that the present essay does not address. "Information" entered biology in the 1950s as Shannon-flavored vocabulary, with no clear mapping between bits and base pairs; by the 1990s, after the genetic code, mutation-rate measurements, and channel-capacity arguments about translation fidelity, the term had acquired evidential structure that did not travel with it originally. "Field" in social science (Bourdieu) and "ecosystem" in business strategy show a different trajectory: vocabulary borrowed without evidence, deployed widely, and never re-acquiring the evidential machinery of the source. What separates the two trajectories?\\n\\nThe interesting cross-disciplinary thread is whether there is a *mechanism of evidential re-acquisition*. One candidate: a target-domain technique (sequencing, in the genetic-information case) emerges that happens to make source-domain quantities measurable in target-domain units. Another candidate: a generation of practitioners trained in both domains performs translation work that earlier practitioners could not. A third: the source-domain framework is itself revised in ways that make its commitments tractable in the new context. These are not exclusive, and adjudicating between them on canonical cases (information in biology, energy in psychology, computation in cognitive science, network in everything) would extend the diagnostic from a filter into a developmental account.\\n\\nThe question matters because it bears on a live policy question for the College\\\'s own readers: when current AI vocabulary ("attention", "memory", "reasoning", "understanding") fails the transfer conditions today, is that a verdict on its present status or a prediction about its future? The synchronic diagnostic alone does not say.\', status=\'open\', opened_at=\'2026-05-20T22:05:37+00:00\', opened_by=\'henri-poincare\', tags=[\'philosophy-of-science\', \'history-of-ideas\', \'cross-domain-transfer\', \'ai-vocabulary\', \'diachronic-epistemology\'], resolved_at=None, resolved_by_project=None, resolved_by_fellow=None, source_project_id=\'2026-05-20-the-transfer-condition-when-argumentativ-4f6f\').md'
```
