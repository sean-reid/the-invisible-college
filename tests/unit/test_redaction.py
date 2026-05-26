"""Tests for the cost-redaction guard.

The redactor must:
  - strip operational cost telemetry (run cost, budget, token counts,
    elapsed-and-cost lines) from public-surface text
  - leave research prose alone (legitimate dollar mentions, the word
    "token" used in a research context, model names without cost)
  - never raise; an empty input round-trips
"""

from __future__ import annotations

from institute import redaction

# --- positive cases: things that must be stripped ----------------------


def test_run_cost_line() -> None:
    text = "elapsed: 215s · run cost: $2.24 of $10.00"
    cleaned, report = redaction.redact(text)
    assert "2.24" not in cleaned
    assert "$" not in cleaned
    assert report.total >= 1


def test_run_cost_inline() -> None:
    text = "The step finished. run cost: $0.32 across all reviewers."
    cleaned, report = redaction.redact(text)
    assert "0.32" not in cleaned
    assert report.total == 1


def test_budget_equals() -> None:
    text = "budget=$10.0, max-steps=30, daily=$0"
    cleaned, report = redaction.redact(text)
    assert "$10.0" not in cleaned
    assert "$0" not in cleaned
    assert report.total == 2


def test_budget_colon() -> None:
    text = "Configured: budget: $5.00 per day."
    cleaned, _ = redaction.redact(text)
    assert "$5.00" not in cleaned


def test_daily_cap() -> None:
    text = "The daily cap = $25 was reached."
    cleaned, _ = redaction.redact(text)
    assert "$25" not in cleaned


def test_named_cost() -> None:
    text = "Total cost: $14.27. Estimated cost = $5.00. Approximate cost $1."
    cleaned, report = redaction.redact(text)
    assert "$14.27" not in cleaned
    assert "$5.00" not in cleaned
    assert "$1" not in cleaned
    assert report.total >= 3


def test_spent_dollars() -> None:
    text = "We spent $4.50 on this run."
    cleaned, _ = redaction.redact(text)
    assert "$4.50" not in cleaned


def test_cost_of() -> None:
    text = "The cost of $0.08 for one review is logged."
    cleaned, _ = redaction.redact(text)
    assert "$0.08" not in cleaned


def test_labelled_input_tokens() -> None:
    text = "The fellow consumed 1,234 input tokens drafting the proposal."
    cleaned, _ = redaction.redact(text)
    assert "1,234" not in cleaned


def test_labelled_output_tokens() -> None:
    text = "Output tokens: 5000."
    cleaned, _ = redaction.redact(text)
    assert "5000" not in cleaned


def test_labelled_total_tokens() -> None:
    text = "Total tokens = 12000 for the round."
    cleaned, _ = redaction.redact(text)
    assert "12000" not in cleaned


def test_used_tokens() -> None:
    text = "The reviewer used 800 tokens."
    cleaned, _ = redaction.redact(text)
    assert "800 tokens" not in cleaned


def test_qualified_dollar_total() -> None:
    text = "Resource estimate: under $3 total for the run."
    cleaned, _ = redaction.redact(text)
    assert "$3" not in cleaned


def test_approximately_dollar() -> None:
    text = "Approximately $0.50 to run, all in."
    cleaned, _ = redaction.redact(text)
    assert "$0.50" not in cleaned


# --- negative cases: legitimate research content must pass through -----


def test_bare_dollar_in_economics_prose() -> None:
    text = "Smith argues that a worker earning $5 a day in 1776 had real purchasing power."
    cleaned, report = redaction.redact(text)
    assert cleaned == text
    assert report.total == 0


def test_bare_dollar_with_context() -> None:
    text = "Macroeconomics treats the supply curve. A $10 widget is a useful illustration."
    cleaned, _ = redaction.redact(text)
    assert cleaned == text


def test_tokenizer_research_passes() -> None:
    text = (
        "Tokenizers split arithmetic expressions into multiple tokens, "
        "which interferes with positional generalization."
    )
    cleaned, report = redaction.redact(text)
    assert cleaned == text
    assert report.total == 0


def test_model_name_alone_passes() -> None:
    text = "The lead chose claude-opus-4-7 for its reasoning depth on this task."
    cleaned, _ = redaction.redact(text)
    assert cleaned == text


def test_model_with_methodology_context_passes() -> None:
    # Methodology references to model name + cost-as-rationale (no
    # dollar value) are allowed — they reveal no operational numbers.
    text = "Use the Anthropic API (claude-haiku-4-5, for cost) with a zero-shot prompt."
    cleaned, _ = redaction.redact(text)
    assert cleaned == text


def test_model_comparison_passes() -> None:
    text = "claude-opus-4-7 costs more than the sonnet model on this workload."
    cleaned, _ = redaction.redact(text)
    assert cleaned == text


def test_latex_inline_math_passes_after_qualifier() -> None:
    # The corrupted-files bug: a qualifier word adjacent to LaTeX
    # inline math like `approximately $390$` must not be eaten.
    text = "The fractional condition number is approximately $390$, which sits adjacent to a singularity."
    cleaned, report = redaction.redact(text)
    assert cleaned == text
    assert report.total == 0


def test_latex_with_unit_passes() -> None:
    text = "Angular precision of approximately $0.017°$ was required."
    cleaned, _ = redaction.redact(text)
    assert cleaned == text


def test_latex_with_cost_word_passes() -> None:
    # "cost of $5$" in game-theory prose should not match the cost-verb pattern.
    text = "Each move carries an opportunity cost of $5$ in the toy game."
    cleaned, _ = redaction.redact(text)
    assert cleaned == text


def test_token_in_compiler_context() -> None:
    text = "The parser emits a token for each lexeme it recognizes."
    cleaned, _ = redaction.redact(text)
    assert cleaned == text


def test_empty_input() -> None:
    cleaned, report = redaction.redact("")
    assert cleaned == ""
    assert report.total == 0


def test_report_groups_by_pattern() -> None:
    text = "run cost: $1.00 then run cost: $2.00"
    _, report = redaction.redact(text)
    assert report.total == 2
    # Both matches go through the same pattern label.
    assert sum(report.by_pattern.values()) == 2


def test_has_cost_leak() -> None:
    assert redaction.has_cost_leak("run cost: $1.00") is True
    assert redaction.has_cost_leak("Smith on the wealth of nations.") is False
    assert redaction.has_cost_leak("") is False


def test_redaction_report_truthiness() -> None:
    _, empty = redaction.redact("clean prose")
    assert not empty
    _, hit = redaction.redact("budget=$5")
    assert hit


# ---------------------------------------------------------------------------
# LaTeX inline-math protection
# ---------------------------------------------------------------------------


def test_latex_math_with_qualifier_does_not_leak() -> None:
    """The Stahl-paper regression: `to approximately $1.1 \\times 10^9$`
    was matching `qualified-dollar` because the 10-char `_NOT_LATEX`
    lookahead couldn't see the closing `$` 19 chars away. Math-span
    masking solves it cleanly."""
    text = (
        "brings $H_{\\text{bat}}$ down from $1.2 \\times 10^{10}$ "
        "to approximately $1.1 \\times 10^{9}$. The bat..."
    )
    out, report = redaction.redact(text)
    assert "[cost redacted]" not in out
    assert report.total == 0
    assert "$1.1 \\times 10^{9}$" in out


def test_latex_math_with_under_does_not_leak() -> None:
    text = "fell from $1.2 \\times 10^{10}$ to under $1.1 \\times 10^{9}$."
    out, _ = redaction.redact(text)
    assert "[cost redacted]" not in out


def test_latex_math_with_subscript() -> None:
    out, _ = redaction.redact("the index $x_i$ runs from 1 to n.")
    assert out == "the index $x_i$ runs from 1 to n."


def test_pure_numeric_math_unprotected_but_safe_without_keyword() -> None:
    """`$1.5$` has no LaTeX signal so it isn't masked, but no
    redaction pattern matches it either (no operational keyword)."""
    out, report = redaction.redact("The magnitude is $1.5$.")
    assert out == "The magnitude is $1.5$."
    assert report.total == 0


def test_run_cost_with_two_dollars_still_redacts() -> None:
    """Two `$` in real operational telemetry must not be misread as
    a math span (they have no LaTeX signal chars between them)."""
    out, _ = redaction.redact("run cost: $2.24 of $10.00 total")
    assert "[cost redacted]" in out


def test_display_math_block_protected() -> None:
    text = "see the formula $$\\sum_{i} x_i^2$$ below."
    out, _ = redaction.redact(text)
    assert out == text
