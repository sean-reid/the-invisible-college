"""Tests for the publish-time tone lint."""

from __future__ import annotations

import pytest

from institute import tone_lint


def test_clean_body_returns_empty() -> None:
    body = (
        "# A Result\n\n"
        "The data show a clear effect. Confidence intervals are wide "
        "but exclude zero. The mechanism is detailed below.\n\n"
        "## Method\n\nFit by ordinary least squares.\n"
    )
    assert tone_lint.find_violations(body) == []


def test_my_advisor_phrase_caught() -> None:
    body = "My advisor framed it as Path A vs Path B.\n"
    violations = tone_lint.find_violations(body)
    labels = {label for label, _ in violations}
    assert "my advisor" in labels


def test_advisor_possessive_action_caught() -> None:
    body = "The advisor's reply pressed harder.\n"
    labels = {label for label, _ in tone_lint.find_violations(body)}
    assert "advisor/reviewer/panel possessive action" in labels


def test_round_n_review_caught() -> None:
    body = "After round-1 peer review the data was reframed.\n"
    labels = {label for label, _ in tone_lint.find_violations(body)}
    assert "round-N review/panel" in labels


def test_prior_draft_caught() -> None:
    body = "The prior draft took Path B and confessed the gap.\n"
    labels = {label for label, _ in tone_lint.find_violations(body)}
    assert "prior draft / previous version" in labels


def test_qualifying_panel_review_caught() -> None:
    body = "The first round of qualifying-panel review pushed the prior draft.\n"
    labels = {label for label, _ in tone_lint.find_violations(body)}
    assert "qualifying-panel review/feedback" in labels


def test_after_peer_review_caught() -> None:
    body = "After peer review the framing changed.\n"
    labels = {label for label, _ in tone_lint.find_violations(body)}
    assert "after (peer) review" in labels


def test_this_revision_addresses_caught() -> None:
    body = "This revision addresses two concerns raised by the panel.\n"
    labels = {label for label, _ in tone_lint.find_violations(body)}
    assert "this revision addresses/adds/..." in labels


def test_the_panel_said_caught() -> None:
    body = "The panel said the framing was misleading.\n"
    labels = {label for label, _ in tone_lint.find_violations(body)}
    assert "the panel said/asked/..." in labels


def test_code_fence_protects_match() -> None:
    """A round-1 mention inside a fenced code block is not a tone leak."""
    body = "Run the helper:\n\n```bash\nmytool --round-1 --review\n```\n\nThen read the output.\n"
    assert tone_lint.find_violations(body) == []


def test_inline_code_protects_match() -> None:
    body = "Pass the `--my-advisor` flag to enable that mode.\n"
    assert tone_lint.find_violations(body) == []


def test_warn_mode_returns_violations_does_not_raise(capsys: pytest.CaptureFixture[str]) -> None:
    body = "My advisor framed it as Path A vs Path B.\n"
    out = tone_lint.check(body, mode="warn")
    assert len(out) >= 1
    captured = capsys.readouterr()
    assert "tone_lint" in captured.out


def test_raise_mode_raises_tone_lint_error() -> None:
    body = "The prior draft took Path B.\n"
    with pytest.raises(tone_lint.ToneLintError) as exc_info:
        tone_lint.check(body, mode="raise")
    assert "review-process language" in str(exc_info.value)


def test_unknown_mode_raises_value_error() -> None:
    """Unknown mode is rejected when there are violations to act on."""
    with pytest.raises(ValueError, match="Unknown tone_lint mode"):
        tone_lint.check("The prior draft took Path B.\n", mode="strict")


def test_multiple_patterns_in_one_body() -> None:
    body = (
        "My advisor framed it as Path A vs Path B. The prior draft took "
        "Path B. The advisor's reply pressed harder.\n"
    )
    violations = tone_lint.find_violations(body)
    labels = {label for label, _ in violations}
    assert {
        "my advisor",
        "prior draft / previous version",
        "advisor/reviewer/panel possessive action",
    }.issubset(labels)


def test_published_paper_voice_passes_clean() -> None:
    """A genuine published-paper paragraph (the kind we want) should be clean."""
    body = (
        "# The Femoral Circumference Equation Across Body Mass\n\n"
        "Anderson, Hall-Martin and Russell (1985) proposed a scaling "
        "relation between femoral circumference and body mass. We refit "
        "the relation across a curated comparative sample of extant "
        "mammals and report the residual structure under PGLS. The fit "
        "supports the original exponent within wide CIs but the "
        "residuals show systematic structure keyed by superorder.\n"
    )
    assert tone_lint.find_violations(body) == []
