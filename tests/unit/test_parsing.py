"""Tests for the bootstrap workflow's helpers.

We do not exercise the full `run()` because it makes a real subprocess
call to `claude`. Instead, we test the pure helpers that parse and
validate the orchestrator's response.
"""

from institute import parsing as bootstrap


def test_extract_json_object_unwraps_code_fence() -> None:
    text = '```json\n{"fellows": []}\n```'
    assert bootstrap.extract_json_object(text) == '{"fellows": []}'


def test_extract_json_object_finds_object_after_prose() -> None:
    text = 'Here is the JSON for the cohort:\n\n{\n  "fellows": [1,2]\n}\n'
    extracted = bootstrap.extract_json_object(text)
    assert extracted is not None
    assert extracted.startswith("{") and extracted.endswith("}")
    assert '"fellows"' in extracted


def test_extract_json_object_handles_nested_braces() -> None:
    text = '{"a": {"b": {"c": 1}}, "d": [1, 2, {"e": "}"}]}'
    extracted = bootstrap.extract_json_object(text)
    assert extracted == text


def test_extract_json_object_ignores_braces_in_strings() -> None:
    text = '{"name": "} not a closer", "ok": true}'
    extracted = bootstrap.extract_json_object(text)
    assert extracted == text


def test_extract_json_object_returns_none_when_no_object() -> None:
    assert bootstrap.extract_json_object("Submitted the genomes.") is None
    assert bootstrap.extract_json_object("") is None
    assert bootstrap.extract_json_object("[1, 2, 3]") is None  # not an object


def test_parse_json_or_dump_repairs_unescaped_quote_in_string(tmp_path) -> None:
    """Regression: an LLM produced a JSON string with an interior `." ` that
    closed the string prematurely. json_repair should still recover the payload.
    """
    bad = """```json
{
  "summary": "Good piece.",
  "concerns": "1. The piece reads as \\"here is X\\" rather than \\"here is what I discovered by pursuing one of these." At minimum, a partial example would help.",
  "recommendation": "minor"
}
```"""
    out = bootstrap.parse_json_or_dump(bad, dump_path=tmp_path / "raw.txt", context="test")
    assert out["summary"] == "Good piece."
    assert out["recommendation"] == "minor"
    assert "partial example" in out["concerns"]


def test_parse_json_or_dump_dumps_and_raises_when_unsalvageable(tmp_path) -> None:
    """Truly garbage input should be saved to the dump path and raise."""
    import pytest

    dump = tmp_path / "raw.txt"
    with pytest.raises(RuntimeError, match="could not parse JSON"):
        bootstrap.parse_json_or_dump(
            "this is not json at all",
            dump_path=dump,
            context="test",
        )
    assert dump.exists()
    assert dump.read_text() == "this is not json at all"
