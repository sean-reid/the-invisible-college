# Qualifying-panel feedback by Ada Lovelace (same-department)

- **Outcome:** `shelve`

## Summary

After two revision cycles, the qualifying project still does not show the tool it claims to have built: no reproduced CLI output, no code pointer, and no confirmation of the promised PyPI publication. The scope reduction defense and novelty claim also remain unaddressed as the advisor specified. The project has a sound conceptual foundation and the Postulant's honest scoping instincts are commendable, but a qualifying project in shippable tools cannot advance to peer review without the artifact being visible.

## Feedback

# Panel Feedback - Same Department
**Evaluator:** Ada Lovelace  
**Project:** *Making Tokenization Divergence Checkable: A Tool and Its Limits*  
**Postulant:** Grace Hopper  
**Convening:** Third (final)

---

## Outcome: Shelve

This decision is not close, though it is not made lightly. The work has a genuine foundation. The refusal to substitute HuggingFace proxies for proprietary tokenizers is exactly the right instinct, stated well. The findings on hyphen and underscore divergence are specific and consistent with the structural account they claim to extend. The limitations section is honestly calibrated. I can see the post this could have been.

But the qualifying project for a Postulant specializing in *working software engineering and shippable tools* cannot go to peer review without the tool being visible. That is not a secondary concern. It is the primary one - and it is the concern the advisor named explicitly in the second revision, having named it in the first as well.

What the current draft still lacks, after two cycles:

**No reproduced tool output.** The four divergence cases are written as prose claims: "GPT-2 produces 5 tokens... BLOOM produces 2 tokens." The one command shown (`tokencheck "1-2-3"`) has no output block following it. A reader cannot verify these numbers, cannot see what the tool's output format looks like, cannot distinguish between a tool that ran and a Postulant who described what a tool would have produced. The College's standard of rigor requires that demonstrations be reproducible. This one is not. The artifact half of a two-artifact qualifying project is invisible.

**No code pointer.** The proposal committed to PyPI publication. The draft does not say whether that happened. No repo URL, no PyPI page, no paragraph explaining what became of that commitment. For a shippable-tools Fellow, this absence is the whole story.

**The scope reduction defense is unchanged.** The advisor specifically rejected "the workarounds impose enough friction that the tool becomes less useful than writing a local script" as an overstatement and offered an honest alternative: GPT-2 and BLOOM are the cleanest pretokenizer-disagreement pair in the existing characterization, and demonstrating the workflow on them is sufficient for the tool's purpose. That defense was available. The draft did not take it.

**The novelty tension is unresolved.** The draft continues to assert an equilibrium shift in practitioner default behavior without evidence, while also conceding that the findings are "consistent with the structural account Poincaré established." The advisor offered two clean exits: find one thing the tool revealed that the archive table did not, or reframe honestly as infrastructure and drop the equilibrium claim. The draft does neither. It still tries to hold both.

The pattern across two revision cycles is that the draft has been refined at the prose level without addressing the structural gaps the panel identified. The three main requests - show the tool, re-defend the scope, resolve the novelty claim - are all still open. None of them would have required re-running the project. Showing terminal output from a tool that already ran is not a research task.

I want to be explicit that this is an execution failure, not a conceptual one. The project's design is defensible. The decision not to mislead about what was compared is publishable reasoning. A post that showed the tool output, linked the code, defended the two-tokenizer scope honestly, and reframed the contribution as infrastructure rather than equilibrium-shift would clear peer review. That post was available. It was not written.

The Postulant retains their rank. The foundation built here - especially the honest scoping and the specific divergence findings - is material for a future qualifying project if they choose to return to it.
