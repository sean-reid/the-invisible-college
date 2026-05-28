"""Regression tests for `.format()`-able workflow briefs.

The research and revise briefs include LaTeX examples (`\\theta`,
`{10}` inside `10^{10}`, etc.). Two failure modes need pinning:

1. Python parses unescaped `\\t` / `\\a` in a regular triple-quoted
   string as TAB / BEL. The briefs must be raw strings (r-prefixed
   triple-quoted) so LaTeX backslash-letter sequences survive
   Python parsing.

2. `BRIEF.format(...)` interprets `{...}` as a placeholder. Any
   LaTeX curly brace must be doubled (`{{...}}`) so `.format()`
   leaves it as a literal.

Both together prevent the `KeyError: \\theta` regression that
abandoned the "what-the-definition-replaces" project on 2026-05-28
after Henri Poincaré responded to the math-notation brief nudge by
writing a draft with LaTeX in it.
"""

from __future__ import annotations


def test_research_brief_format_with_no_collaborators() -> None:
    from institute.workflows.research import BRIEF

    out = BRIEF.format(contributions_inputs="", contributions_directive="")
    # LaTeX backslashes survive Python parsing.
    assert chr(92) + "theta" in out
    assert chr(92) + "alpha" in out
    assert chr(92) + "sum" in out
    # No TAB-mangling: `\t` was not parsed as a control char.
    assert "\theta" not in out  # the literal TAB+'heta'
    # LaTeX braces survive .format(): expect '10^{10}' literal.
    assert "10^{10}" in out
    assert chr(92) + "sqrt{n}" in out


def test_research_brief_format_with_collaborators() -> None:
    from institute.workflows.research import (
        BRIEF,
        CONTRIBUTIONS_DIRECTIVE,
        CONTRIBUTIONS_INPUTS,
    )

    out = BRIEF.format(
        contributions_inputs=CONTRIBUTIONS_INPUTS,
        contributions_directive=CONTRIBUTIONS_DIRECTIVE,
    )
    assert CONTRIBUTIONS_INPUTS.strip() in out
    assert CONTRIBUTIONS_DIRECTIVE.strip() in out


def test_revise_brief_format() -> None:
    from institute.workflows.revise import BRIEF

    out = BRIEF.format(round_label="round-1", round_context="(test)")
    assert "round-1" in out
    assert "(test)" in out
    # LaTeX preserved through format().
    assert chr(92) + "alpha = 0.05" in out
    assert "10^{10}" in out


def test_collaborator_brief_format() -> None:
    from institute.workflows.research import COLLABORATOR_BRIEF

    out = COLLABORATOR_BRIEF.format(
        collab_name="Test Fellow",
        collab_specialization="testing",
        lead_name="Test Lead",
    )
    assert "Test Fellow" in out
    assert "Test Lead" in out
