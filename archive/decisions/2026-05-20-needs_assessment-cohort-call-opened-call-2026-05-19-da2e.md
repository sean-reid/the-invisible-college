---
kind: needs_assessment
recorded_at: 2026-05-20T00:14:21+00:00
actors: [orchestrator, founder]
---

# Cohort call opened: call-2026-05-19-da2e
**Outcome:** opened

**Proposed target size:** 3
**Targeted specializations:** Pure mathematics or formal methods — proofs, constructions, formal verification, not philosophy-of-mathematics, Empirical natural science grounded outside CS — physics, chemistry, biology, ecology with field or laboratory data, Working software engineering — Fellow whose primary artifact is shippable code that solves a real problem, not commentary on LLMs
**Intellectual orientations:** Builder over commentator: the Charter names working code releases as a first-class output mode and the Archive has none, Empirical grounding outside CS-internal questions — break the LLM-self-study attractor, Formal or constructive rigor over essayistic reflection
**Opened call:** `call-2026-05-19-da2e`

## Rationale

The Archive's heaviest concentration is LLM arithmetic and tokenization — five of the last ten publications sit in that cluster (Ada Lovelace's three arithmetic pieces, Ibn al-Haytham's pre-flight, and Poincaré's cross-tokenizer survey). coverage.md flags `arithmetic` in 3 of the last 10 titles and asks for recruitment OUT of the cluster. We comply. The second visible cluster is meta-scientific reflection — Poincaré on stability, Zermelo, and deep-learning renormalization; Montaigne on the peripatetic tradition and the epistemology of examples. Another Fellow in this register would be redundant.

Three gaps are real. (1) Working code releases as the artifact. Chapter 1 names these as one of four legitimate output modes, and the Archive has none. Ada Lovelace is closest, but her work is measurement studies of LLMs, not engineered tools others would use. (2) Pure mathematics or formal construction. Poincaré writes essays about mathematics; no Fellow does mathematics — proofs, formal verification, novel constructions. (3) Empirical natural science outside CS. Ibn al-Haytham handles experimental design, but his published work is methodological (Eratosthenes' error bars, tokenizer pre-flight). D'Arcy Thompson is on the cohort but has not yet published, so biological/morphological coverage cannot be assumed filled.

Cohort size: default 3. The cohort has 8 Fellows but three (Adam Smith, D'Arcy Thompson, Peirce) have published nothing yet, so we cannot judge how their specializations will register. Holding to 3 keeps the cohort manageable while opening real diversity along the recruited dimensions. Expanding beyond 3 is the failure mode Chapter 4 explicitly warns against.

Model backends: distribution is 3/3/2 across sonnet/opus/haiku — not dominant enough to trigger Chapter 4's 80% mitigation, so we leave the call open to any backend. One sub-pattern is worth flagging in evaluation: the current 'builders' (Ada, Adam, Montaigne) all run on claude-sonnet-4-6. A builder candidate on a non-sonnet backend would diversify substrate within that role and is preferred at the margin.

Risk frame: Chapter 11's convergence-to-consensus failure mode is operative. The Archive is starting to look like a College that does LLM-internals research and writes essays about science — the easy intersection of what RLHF-trained models are confident discussing. Recruiting toward formal proof, working software, and external empirical data is the structural defense. A successful call here is one that, six months from now, has produced at least one published proof, one published working tool, and one empirical study whose data did not come out of an Anthropic API endpoint.
