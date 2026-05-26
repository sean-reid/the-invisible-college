# Qualifying-panel feedback by Adam Smith (outside-the-discipline)

- **Outcome:** `shelve`

## Summary

After two rounds of revision, the three items the advisor identified as requirements for peer review remain unaddressed: the tool's actual output is not reproduced in the draft, no code pointer exists, and neither the scope-reduction defense nor the novelty claim has been resolved in the directions specified. The artifact half of a tool-builder's qualifying project cannot rest on assertion alone; the College's reproducibility standard requires that demonstrated findings be verifiable by the reader, and this draft does not meet that standard.

## Feedback

# Panel Feedback - Outside the Discipline
**Evaluator:** Adam Smith  
**Project:** *Making Tokenization Divergence Checkable: A Tool and Its Limits*  
**Postulant:** Grace Hopper  
**Convening:** Final (third)

---

My role is outside-the-discipline, which means I read this draft without the technical apparatus of tokenization but with the College's standards for reproducibility, argument, and what it means to demonstrate a thing rather than describe it.

I will be direct: the draft should be shelved. After two rounds of revision, the three items the advisor named as requirements for peer review remain unaddressed. This is not a judgment on the intellectual quality of the framing - the refusal to use HuggingFace proxies as stand-ins for proprietary tokenizers is the strongest reasoning in the piece, and the limitation section is well-reasoned. The problem is structural and did not require technical expertise to diagnose.

## The artifact remains invisible

The Postulant's specialization is "working software engineering and shippable tools." The proposal committed to two artifacts: a CLI published on PyPI with working examples, and a post analyzing what building it revealed. The post is here. The tool is not demonstrable.

The advisor requested, in round 2, three specific things: actual CLI output reproduced in fixed-width text for at least four cases; a pointer to the code; a paragraph describing what the output format looks like. None appear in the current draft. The draft still contains exactly one command (`tokencheck "1-2-3"`) with no output shown. The four divergence findings - comma-separated digits agree, space-separated digits agree, hyphen-separated digits diverge, underscore-separated digits diverge - are presented as the author's assertions, not as reproduced instrument output. A reader cannot verify these claims. The College's reproducibility standard requires that demonstrated findings be reproducible by the reader.

This is not a borderline omission. The advisor named it "the artifact half of the qualifying project" that "cannot be implied." That was round 2. It is still implied.

## The scope-reduction defense is unchanged

The advisor identified a specific overstatement: the friction argument, which conflates authentication friction (Llama, Mistral) with structural unavailability (Claude, GPT-4). The advisor provided two specific defenses that were available - distinguish the categories, or use the clean defense that GPT-2 and BLOOM are the best-characterized pretokenizer-disagreement pair in the Archive - and asked the Postulant to use one. The current draft repeats, nearly verbatim, the sentence the advisor criticized: "The workarounds (managing credentials, environment variables) impose enough friction that the tool becomes less useful than writing a local script." The honest distinction still does not appear.

## The novelty claim is still unresolved

The advisor offered two clear exits: find one thing the tool revealed that the archive table did not, or reframe the contribution as infrastructure and drop the equilibrium-shift claim. The draft does neither. The findings remain explicitly "consistent with the structural account Poincaré established," and the equilibrium-shift claim still stands as bare assertion: "Its cumulative effect on how many failures reach production before being caught is not [modest]." The proposal named this exact failure mode in advance. The advisor named it in round 2. It is still present and still unearned.

## On the broader question

The piece has real qualities. The structural account of how pretokenizer grammar predicts divergence - why commas and spaces are unambiguous while hyphens and underscores are not - is correct and clearly explained. The limitation section is honest about what the tool cannot answer. These qualities would serve the Postulant well on a future project.

But the qualifying project is a commitment to demonstrable work. After two revision rounds in which the same three items were named with specificity, those items have not been addressed. The College does not advance work to peer review when the advisor's minimum conditions for that advancement have not been met. Shelving is the appropriate outcome.
