"""Tests for the bootstrap workflow's helpers.

We do not exercise the full `run()` because it makes a real subprocess
call to `claude`. Instead, we test the pure helpers that parse and
validate the orchestrator's response.
"""

from institute.workflows import bootstrap


def test_extract_json_object_unwraps_code_fence() -> None:
    text = '```json\n{"fellows": []}\n```'
    assert bootstrap._extract_json_object(text) == '{"fellows": []}'


def test_extract_json_object_finds_object_after_prose() -> None:
    text = 'Here is the JSON for the cohort:\n\n{\n  "fellows": [1,2]\n}\n'
    extracted = bootstrap._extract_json_object(text)
    assert extracted is not None
    assert extracted.startswith("{") and extracted.endswith("}")
    assert '"fellows"' in extracted


def test_extract_json_object_handles_nested_braces() -> None:
    text = '{"a": {"b": {"c": 1}}, "d": [1, 2, {"e": "}"}]}'
    extracted = bootstrap._extract_json_object(text)
    assert extracted == text


def test_extract_json_object_ignores_braces_in_strings() -> None:
    text = '{"name": "} not a closer", "ok": true}'
    extracted = bootstrap._extract_json_object(text)
    assert extracted == text


def test_extract_json_object_returns_none_when_no_object() -> None:
    assert bootstrap._extract_json_object("Submitted the genomes.") is None
    assert bootstrap._extract_json_object("") is None
    assert bootstrap._extract_json_object("[1, 2, 3]") is None  # not an object
