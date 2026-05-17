"""Tests for the Charter loader."""

from institute import charter


def test_load_returns_non_empty_text() -> None:
    text = charter.load()
    assert text.strip() != ""
    assert "Charter" in text or "charter" in text.lower()


def test_header_describes_the_charter() -> None:
    h = charter.header()
    assert "Charter" in h
    assert h.endswith("\n")
